#!/usr/bin/env python3
"""
Cross-Machine (Office <-> Home) Helper for Google Flow Veo 3.1 Project Automation.
Automatically discovers the live AdsPower SunBrowser CDP port on macOS & Windows
(since AdsPower assigns a new random DevTools port every time the profile opens),
checks project login status, and verifies all local keyframes & 1080p deliverables.
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

FLOW_PROJECT_ID = "e77d4088-8126-4cb4-8d09-edec09be18ff"
FLOW_PROJECT_URL = f"https://flow.google.com/project/{FLOW_PROJECT_ID}"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)


def _candidate_devtools_port_files():
    home = os.path.expanduser("~")
    patterns = [
        # macOS AdsPower Global
        os.path.join(home, "Library", "Application Support", "adspower_global", "cwd_global", "source", "cache", "*", "DevToolsActivePort"),
        os.path.join(home, "Library", "Application Support", "AdsPower Global", "cwd_global", "source", "cache", "*", "DevToolsActivePort"),
        # Windows AdsPower Global
        os.path.join(os.environ.get("APPDATA", ""), "adspower_global", "cwd_global", "source", "cache", "*", "DevToolsActivePort"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "adspower_global", "cwd_global", "source", "cache", "*", "DevToolsActivePort"),
        # Linux AdsPower
        os.path.join(home, ".config", "adspower_global", "cwd_global", "source", "cache", "*", "DevToolsActivePort"),
    ]
    files = []
    for pat in patterns:
        if pat and "*" in pat:
            files.extend(glob.glob(pat))
    # Sort newest modified first so the most recently launched AdsPower profile wins
    files.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0, reverse=True)
    return files


def discover_cdp_http_url(explicit_url=None):
    """Return live 'http://127.0.0.1:<port>' for the open AdsPower / Chrome CDP session."""
    candidates = []
    if explicit_url:
        candidates.append(explicit_url.rstrip("/"))
    if os.environ.get("FLOW_CDP_URL"):
        candidates.append(os.environ["FLOW_CDP_URL"].rstrip("/"))

    for port_file in _candidate_devtools_port_files():
        try:
            with open(port_file, "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f.readlines() if ln.strip()]
            if lines and lines[0].isdigit():
                candidates.append(f"http://127.0.0.1:{lines[0]}")
        except OSError:
            continue

    candidates.append("http://127.0.0.1:9222")

    seen = set()
    for base in candidates:
        if base in seen:
            continue
        seen.add(base)
        try:
            with urllib.request.urlopen(f"{base}/json/version", timeout=2.0) as resp:
                info = json.loads(resp.read().decode("utf-8"))
                if "webSocketDebuggerUrl" in info or "Browser" in info:
                    return base
        except Exception:
            continue

    raise RuntimeError(
        "Không tìm thấy trình duyệt AdsPower đang mở!\n"
        "👉 Cách xử lý: Mở app AdsPower -> bấm nút 'Mở' (Open) ở profile 'flow veo', "
        "đợi trình duyệt SunBrowser hiện lên rồi chạy lại lệnh này."
    )


def list_cdp_tabs(cdp_http_url=None):
    base = discover_cdp_http_url(cdp_http_url)
    with urllib.request.urlopen(f"{base}/json/list", timeout=4.0) as resp:
        return base, json.loads(resp.read().decode("utf-8"))


def get_flow_ws_url(cdp_http_url=None, auto_open_project=True):
    """Find the WebSocket debugger URL for the Google Flow project tab (opening it if needed)."""
    base, tabs = list_cdp_tabs(cdp_http_url)
    # Prefer exact project tab first
    for tab in tabs:
        if tab.get("type") == "page" and FLOW_PROJECT_ID in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    # Fallback: any flow.google tab
    for tab in tabs:
        if tab.get("type") == "page" and "flow.google" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]

    if auto_open_project:
        encoded = urllib.parse.quote(FLOW_PROJECT_URL, safe=":/?=&-")
        req = urllib.request.Request(f"{base}/json/new?{encoded}", method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                new_tab = json.loads(resp.read().decode("utf-8"))
                if "webSocketDebuggerUrl" in new_tab:
                    return new_tab["webSocketDebuggerUrl"]
        except Exception:
            with urllib.request.urlopen(f"{base}/json/new?{encoded}", timeout=5.0) as resp:
                new_tab = json.loads(resp.read().decode("utf-8"))
                if "webSocketDebuggerUrl" in new_tab:
                    return new_tab["webSocketDebuggerUrl"]

    raise RuntimeError(
        f"Đã kết nối AdsPower ({base}) nhưng chưa mở tab Google Flow.\n"
        f"👉 Hãy dán link này vào trình duyệt AdsPower: {FLOW_PROJECT_URL}"
    )


def check_workspace_assets():
    checks = {
        "Ảnh gốc sản phẩm sạch 0% chữ (clean_product_refs)": os.path.join(BASE_DIR, "clean_product_refs"),
        "Keyframes 16:9 START & END (frames)": os.path.join(BASE_DIR, "frames"),
        "Source Videos 1080p gốc từ Flow (videos/hd_1080p)": os.path.join(BASE_DIR, "videos", "hd_1080p"),
        "Video thành phẩm Web Intro 16:9 (deliverables)": os.path.join(BASE_DIR, "deliverables"),
        "Bảng kiểm định 2fps (contact_sheets)": os.path.join(BASE_DIR, "contact_sheets"),
    }
    print("\n=== 1. KIỂM TRA TÀI NGUYÊN TRONG REPO LOCAL ===")
    for label, path in checks.items():
        if os.path.isdir(path):
            files = [f for f in os.listdir(path) if not f.startswith(".")]
            print(f"  ✅ {label}: {len(files)} files ({path})")
        else:
            print(f"  ⚠️  {label}: Chưa có thư mục ({path})")


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra & kết nối nhanh AdsPower + Google Flow Veo 3 khi về nhà")
    parser.add_argument("--cdp-url", default=None, help="Chỉ định URL CDP thủ công nếu cần (vd: http://127.0.0.1:52602)")
    parser.add_argument("--check", action="store_true", help="Kiểm tra toàn bộ kết nối AdsPower + tài nguyên")
    parser.add_argument("--open-project", action="store_true", help="Tự động mở đúng tab project Veo 3 đang làm dở trong AdsPower")
    parser.add_argument("--export-session", action="store_true", help="Trích xuất lưu dự phòng flow_session.json từ AdsPower vào máy nhà")
    args = parser.parse_args()

    check_workspace_assets()

    print("\n=== 2. KIỂM TRA KẾT NỐI ADSPOWER SUNBROWSER & GOOGLE FLOW ===")
    try:
        base, tabs = list_cdp_tabs(args.cdp_url)
        print(f"  ✅ Đã tự động bắt được cổng AdsPower CDP: {base}")
        page_tabs = [t for t in tabs if t.get("type") == "page"]
        flow_tabs = [t for t in page_tabs if "flow.google" in t.get("url", "")]
        print(f"  ✅ Số tab đang mở: {len(page_tabs)} | Số tab Google Flow: {len(flow_tabs)}")
        for t in flow_tabs:
            print(f"     -> {t.get('title', 'Flow')} | {t.get('url')}")

        if args.open_project or not flow_tabs:
            ws = get_flow_ws_url(base, auto_open_project=True)
            print(f"  ✅ Tab Project Veo 3 đã sẵn sàng: {FLOW_PROJECT_URL}")
            print(f"     (WebSocket: {ws})")

        if args.export_session:
            mgr = os.path.join(REPO_ROOT, "flow_session_manager.py")
            out_sess = os.path.join(REPO_ROOT, "flow_session.json")
            if os.path.exists(mgr):
                print("\n=== 3. TRÍCH XUẤT DỰ PHÒNG FLOW_SESSION.JSON TẠI MÁY NHÀ ===")
                subprocess.run([sys.executable, mgr, "--export-from-cdp", base, "--session", out_sess], check=False)
            else:
                print(f"  ℹ️ Không tìm thấy {mgr}, bỏ qua bước xuất flow_session.json.")

        print("\n🎉 TẤT CẢ SẴN SÀNG! Bạn có thể làm tiếp ngay trên project:")
        print(f"   {FLOW_PROJECT_URL}")
    except RuntimeError as e:
        print(f"  ❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
