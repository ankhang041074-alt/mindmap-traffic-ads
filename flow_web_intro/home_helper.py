#!/usr/bin/env python3
"""
Cross-Machine (Office <-> Home) Helper for Google Flow Veo 3.1 Project Automation.
Automatically discovers the live AdsPower SunBrowser CDP port on macOS & Windows,
prevents the AdsPower 'USE_LOCAL_COOKIE' stale-cookie logout bug, and provides
direct CDP cookie backup (--save-session) & emergency restore (--inject-session)
straight inside AdsPower SunBrowser without needing Playwright.
"""

import argparse
import asyncio
import glob
import json
import os
import sys
import time
import urllib.parse
import urllib.request

FLOW_PROJECT_ID = "e77d4088-8126-4cb4-8d09-edec09be18ff"
FLOW_PROJECT_URL = f"https://flow.google.com/project/{FLOW_PROJECT_ID}"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)
DEFAULT_SESSION_FILE = os.path.join(REPO_ROOT, "flow_session.json")

REQUIRED_GOOGLE_AUTH_COOKIES = {"SID", "HSID", "SSID", "APISID", "SAPISID", "__Secure-1PSID"}


def _candidate_adspower_cache_dirs():
    home = os.path.expanduser("~")
    patterns = [
        # macOS AdsPower Global
        os.path.join(home, "Library", "Application Support", "adspower_global", "cwd_global", "source", "cache", "*"),
        os.path.join(home, "Library", "Application Support", "AdsPower Global", "cwd_global", "source", "cache", "*"),
        # Windows AdsPower Global
        os.path.join(os.environ.get("APPDATA", ""), "adspower_global", "cwd_global", "source", "cache", "*"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "adspower_global", "cwd_global", "source", "cache", "*"),
        # Linux AdsPower
        os.path.join(home, ".config", "adspower_global", "cwd_global", "source", "cache", "*"),
    ]
    dirs = []
    for pat in patterns:
        if pat and "*" in pat:
            dirs.extend([d for d in glob.glob(pat) if os.path.isdir(d)])
    dirs.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0, reverse=True)
    return dirs


def _candidate_devtools_port_files():
    files = []
    for d in _candidate_adspower_cache_dirs():
        pf = os.path.join(d, "DevToolsActivePort")
        if os.path.isfile(pf):
            files.append(pf)
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
    for tab in tabs:
        if tab.get("type") == "page" and FLOW_PROJECT_ID in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
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

    for tab in tabs:
        if tab.get("type") == "page" and "webSocketDebuggerUrl" in tab:
            return tab["webSocketDebuggerUrl"]

    raise RuntimeError(
        f"Đã kết nối AdsPower ({base}) nhưng chưa mở tab Google Flow.\n"
        f"👉 Hãy dán link này vào trình duyệt AdsPower: {FLOW_PROJECT_URL}"
    )


async def _cdp_call(ws, msg_id, method, params=None):
    payload = {"id": msg_id, "method": method}
    if params:
        payload["params"] = params
    await ws.send(json.dumps(payload))
    while True:
        raw = await asyncio.wait_for(ws.recv(), timeout=15.0)
        data = json.loads(raw)
        if data.get("id") == msg_id:
            if "error" in data:
                raise RuntimeError(f"CDP {method} error: {data['error']}")
            return data.get("result", {})


async def save_cdp_cookies_to_file(cdp_http_url=None, session_path=DEFAULT_SESSION_FILE):
    """Export all live cookies directly from AdsPower SunBrowser via CDP Storage.getCookies."""
    import websockets

    ws_url = get_flow_ws_url(cdp_http_url, auto_open_project=False)
    async with websockets.connect(ws_url, max_size=16 * 1024 * 1024) as ws:
        res = await _cdp_call(ws, 1, "Storage.getCookies")
        cookies = res.get("cookies", [])

    google_names = {c.get("name") for c in cookies if "google" in c.get("domain", "")}
    present_auth = REQUIRED_GOOGLE_AUTH_COOKIES.intersection(google_names)
    if len(present_auth) < 4:
        print(f"  ⚠️ CẢNH BÁO: Trình duyệt hiện tại CHƯA đăng nhập đủ Google Auth cookies (chỉ thấy {sorted(present_auth)}).")
        print("     Hãy đăng nhập Google Flow trong AdsPower trước khi chạy --save-session!")
        return False

    payload = {
        "exported_at_unix": int(time.time()),
        "exported_at_human": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "project_url": FLOW_PROJECT_URL,
        "cookie_count": len(cookies),
        "cookies": cookies,
    }
    with open(session_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    try:
        os.chmod(session_path, 0o600)
    except OSError:
        pass

    print(f"  ✅ Đã lưu dự phòng {len(cookies)} cookies Google Flow sống vào: {session_path}")
    print(f"  ✅ Xác nhận đủ khoá phiên Google: {sorted(present_auth)}")
    print("  🔒 File này đã được khoá trong .gitignore (không bao giờ lộ lên GitHub).")
    print("  💡 Nếu tối về nhà sợ AdsPower quên đồng bộ, bạn gửi riêng file flow_session.json này")
    print("     vào 'Cloud của tôi' trên Zalo / USB đem về nhà để chạy --inject-session là sống lại ngay!")
    return True


async def inject_cdp_cookies_from_file(cdp_http_url=None, session_path=DEFAULT_SESSION_FILE):
    """Inject backed-up cookies straight into open AdsPower SunBrowser via CDP Storage.setCookies."""
    import websockets

    if not os.path.isfile(session_path):
        raise RuntimeError(
            f"Không tìm thấy file dự phòng {session_path}!\n"
            "👉 Hãy chép file flow_session.json (đã lưu ở công ty bằng --save-session) vào thư mục gốc của repo này."
        )

    with open(session_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    cookies = raw.get("cookies", [])
    if not cookies:
        raise RuntimeError(f"File {session_path} không có danh sách cookies hợp lệ!")

    clean_cookies = []
    for c in cookies:
        item = {
            "name": c["name"],
            "value": c["value"],
            "path": c.get("path", "/"),
            "secure": bool(c.get("secure", False)),
            "httpOnly": bool(c.get("httpOnly", False)),
        }
        # Respect RFC 6265bis __Host- cookie rule (no domain attribute allowed; requires url + path="/")
        if c["name"].startswith("__Host-"):
            host = c.get("domain", "accounts.google.com").lstrip(".")
            item["url"] = f"https://{host}/"
            item["path"] = "/"
            item["secure"] = True
        else:
            item["domain"] = c.get("domain", ".google.com")

        if c.get("expires") and c["expires"] > 0:
            item["expires"] = float(c["expires"])
        if c.get("sameSite") in ("Strict", "Lax", "None"):
            item["sameSite"] = c["sameSite"]
        if c.get("priority") in ("Low", "Medium", "High"):
            item["priority"] = c["priority"]
        clean_cookies.append(item)

    ws_url = get_flow_ws_url(cdp_http_url, auto_open_project=False)
    async with websockets.connect(ws_url, max_size=16 * 1024 * 1024) as ws:
        await _cdp_call(ws, 1, "Storage.setCookies", {"cookies": clean_cookies})
        await _cdp_call(ws, 2, "Page.navigate", {"url": FLOW_PROJECT_URL})

    print(f"  ✅ Đã bơm thành công {len(clean_cookies)} cookies thẳng vào trình duyệt AdsPower đang mở!")
    print(f"  ✅ Đã tự động chuyển hướng trình duyệt vào project: {FLOW_PROJECT_URL}")
    print("  👉 Hãy nhìn sang cửa sổ AdsPower (chờ 3 giây trang tải xong) để kiểm tra!")


def force_cloud_cookie_on_next_open():
    """
    Fix AdsPower 'USE_LOCAL_COOKIE' bug:
    AdsPower compares local `<cache>/cookie_updated_time` >= server `cookieUpdatedTime`.
    Resetting local `cookie_updated_time` to `0` while SunBrowser is closed forces AdsPower
    to download the freshest Cloud Cookie (`USE_SERVER_COOKIE`) on the very next Open click.
    """
    try:
        base = discover_cdp_http_url()
        print(f"  ⚠️ Trình duyệt AdsPower đang MỞ ({base}).")
        print("  👉 Hãy bấm 'Close' (Đóng) profile 'flow veo' trong AdsPower trước rồi chạy lại --force-cloud-cookie!")
        return False
    except RuntimeError:
        pass

    touched = 0
    for d in _candidate_adspower_cache_dirs():
        stamp_file = os.path.join(d, "cookie_updated_time")
        if os.path.isfile(stamp_file):
            with open(stamp_file, "w", encoding="utf-8") as f:
                f.write("0")
            print(f"  ✅ Đã reset dấu thời gian cookie cũ về 0: {stamp_file}")
            touched += 1

    if touched == 0:
        print("  ℹ️ Chưa có thư mục cache cục bộ nào cần reset (AdsPower sẽ mặc định tải cookie từ Cloud).")
    else:
        print("  🎉 Xong! Bây giờ bấm 'Open' (Mở) trong AdsPower, nó sẽ bắt buộc tải Cookie mới nhất từ Cloud (USE_SERVER_COOKIE)!")
    return True


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
    parser = argparse.ArgumentParser(description="Kiểm tra, kết nối & bảo vệ phiên AdsPower + Google Flow Veo 3 giữa Công ty <-> Nhà")
    parser.add_argument("--cdp-url", default=None, help="Chỉ định URL CDP thủ công nếu cần")
    parser.add_argument("--check", action="store_true", help="Kiểm tra toàn bộ kết nối AdsPower + tài nguyên")
    parser.add_argument("--open-project", action="store_true", help="Tự động mở đúng tab project Veo 3 đang làm dở trong AdsPower")
    parser.add_argument("--save-session", action="store_true", help="Lưu dự phòng toàn bộ Cookie Google sống từ AdsPower ra file flow_session.json")
    parser.add_argument("--inject-session", action="store_true", help="Bơm khẩn cấp Cookie từ flow_session.json ngược vào trình duyệt AdsPower đang mở")
    parser.add_argument("--force-cloud-cookie", action="store_true", help="Ép AdsPower tải Cookie mới nhất từ Cloud (sửa lỗi USE_LOCAL_COOKIE khi chuyển máy)")
    parser.add_argument("--session-file", default=DEFAULT_SESSION_FILE, help="Đường dẫn file flow_session.json")
    args = parser.parse_args()

    if args.force_cloud_cookie:
        force_cloud_cookie_on_next_open()
        return

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

        if args.inject_session:
            print("\n=== 3. BƠM KHẨN CẤP COOKIE DỰ PHÒNG VÀO ADSPOWER ===")
            asyncio.run(inject_cdp_cookies_from_file(base, args.session_file))
            return

        if args.open_project or not flow_tabs:
            ws = get_flow_ws_url(base, auto_open_project=True)
            print(f"  ✅ Tab Project Veo 3 đã sẵn sàng: {FLOW_PROJECT_URL}")
            print(f"     (WebSocket: {ws})")

        if args.save_session:
            print("\n=== 3. LƯU PHAO CỨU SINH COOKIE DỰ PHÒNG (FLOW_SESSION.JSON) ===")
            asyncio.run(save_cdp_cookies_to_file(base, args.session_file))

        print("\n🎉 TẤT CẢ SẴN SÀNG! Bạn có thể làm tiếp ngay trên project:")
        print(f"   {FLOW_PROJECT_URL}")
    except RuntimeError as e:
        print(f"  ❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
