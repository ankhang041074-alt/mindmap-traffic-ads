"""
Silent Google Flow CDP Operations Engine (AdsPower SunBrowser).

Packages all 5 production-hardened Google Flow operations:
0. Optional Studio White-BG Isolation (Nano Banana Pro 1:1) for non-white raw photos
1. Silent Ingredient Upload + Nano Banana Pro 16:9 Dual-Lock Image Generation
2. CDK Virtual-Scroll 1-to-1 Scene -> UUID/Token Mapping
3. Silent Veo 3.1 - Fast (4s, 16:9) 3D-Parallax & 2-Frame Video Generation
4. Native 1080p Video Batch Upscale/Download + Lossless/CRF-16 FFmpeg Master Assembly

STRICT INVARIANT: Uses Emulation.setFocusEmulationEnabled({"enabled": True}) ONLY
and NEVER calls focused window activation APIs so AdsPower stays silently in background.
"""

import asyncio
import base64
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from PIL import Image, ImageChops, ImageOps, ImageStat
import websockets

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOW_WEB_INTRO_DIR = os.path.join(REPO_ROOT, "flow_web_intro")
if FLOW_WEB_INTRO_DIR not in sys.path:
    sys.path.insert(0, FLOW_WEB_INTRO_DIR)

from gen_batch_images import FlowCDP  # noqa: E402
from home_helper import discover_cdp_http_url  # noqa: E402

from .guardrails import validate_sku_config  # noqa: E402
from .plate_engine import composite_to_rgb_white  # noqa: E402
from .presets import get_preset  # noqa: E402

FFMPEG = "/opt/homebrew/bin/ffmpeg" if os.path.exists("/opt/homebrew/bin/ffmpeg") else "ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe" if os.path.exists("/opt/homebrew/bin/ffprobe") else "ffprobe"
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
UPLOADED_EXT_RE = re.compile(r"\.(?:jpe?g|png|webp)\b", re.IGNORECASE)


def resolve_cdp_base_url(port: Optional[int] = None, cdp_url: Optional[str] = None) -> str:
    """Resolve live AdsPower / Chrome CDP HTTP endpoint ('http://127.0.0.1:<port>')."""
    if cdp_url:
        return discover_cdp_http_url(cdp_url)
    env_port = os.environ.get("FLOW_CDP_PORT", "").strip()
    if port:
        return discover_cdp_http_url(f"http://127.0.0.1:{int(port)}")
    if env_port.isdigit():
        return discover_cdp_http_url(f"http://127.0.0.1:{env_port}")
    return discover_cdp_http_url()


def get_project_ws_url(
    project_id: str,
    port: Optional[int] = None,
    cdp_url: Optional[str] = None,
    auto_open: bool = True,
) -> str:
    """Find (or silently reuse/open) the Google Flow project tab WebSocket debugger URL."""
    base = resolve_cdp_base_url(port=port, cdp_url=cdp_url)
    with urllib.request.urlopen(f"{base}/json/list", timeout=4.0) as resp:
        tabs = json.loads(resp.read().decode("utf-8"))

    for tab in tabs:
        if tab.get("type") == "page" and project_id in (tab.get("url") or ""):
            return tab["webSocketDebuggerUrl"]

    if auto_open:
        # Prefer silently navigating an already-open idle flow.google.com home tab over PUT /json/new
        for tab in tabs:
            u = tab.get("url") or ""
            if tab.get("type") == "page" and "flow.google.com" in u and "/project/" not in u:
                if "webSocketDebuggerUrl" in tab:
                    return tab["webSocketDebuggerUrl"]

        project_url = f"https://flow.google.com/project/{project_id}"
        encoded = urllib.parse.quote(project_url, safe=":/?=&-")
        req = urllib.request.Request(f"{base}/json/new?{encoded}", method="PUT")
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            new_tab = json.loads(resp.read().decode("utf-8"))
            if "webSocketDebuggerUrl" in new_tab:
                return new_tab["webSocketDebuggerUrl"]

    raise RuntimeError(
        f"Google Flow tab for project {project_id!r} not found on {base}. "
        f"Open https://flow.google.com/project/{project_id} in AdsPower SunBrowser first."
    )


async def init_silent_flow_session(ws, project_id: Optional[str] = None) -> FlowCDP:
    """Initialize FlowCDP with silent background focus emulation (zero window focus stealing)."""
    flow = FlowCDP(ws)
    await flow.call("Page.enable")
    await flow.call("DOM.enable")
    await flow.call("Emulation.setFocusEmulationEnabled", {"enabled": True})
    if project_id:
        cur_href = await flow.js("window.location.href") or ""
        if project_id not in cur_href:
            await flow.call("Page.navigate", {"url": f"https://flow.google.com/project/{project_id}"})
            await asyncio.sleep(5.0)
    return flow


async def press_escape(flow: FlowCDP, wait_s: float = 0.3) -> None:
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(wait_s)


async def clear_composer_strict(flow: FlowCDP) -> None:
    """Clear all attached ingredient chips and prompt text without importing legacy scratch modules."""
    await press_escape(flow, 0.3)
    for _ in range(3):
        remaining = await flow.js("""
        (() => {
            const clearAll = document.querySelector('button[aria-label="Xoá câu lệnh"]');
            if (clearAll && clearAll.getBoundingClientRect().width > 0) {
                clearAll.click();
            }
            const chips = Array.from(document.querySelectorAll('button[aria-label="Thành phần"]'));
            for (const c of chips) {
                if (c.getBoundingClientRect().width > 0) {
                    c.click();
                }
            }
            const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
            if (el && (el.innerText || '').trim().length > 0) {
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
            }
            return document.querySelectorAll('button[aria-label="Thành phần"]').length;
        })()
        """)
        await asyncio.sleep(0.32)
        if remaining == 0:
            break


async def exit_edit_view_if_needed(flow: FlowCDP) -> None:
    href = await flow.js("window.location.href") or ""
    if "/edit/" in href or "/trash" in href:
        await flow.find_and_trusted_click("aria === 'Nút quay lại để quay về trang trước'", "exit /edit/ or /trash view")
        await asyncio.sleep(1.0)


async def disable_agent_mode_if_active(flow: FlowCDP) -> None:
    """Turn OFF Flow's post-reload 'Tác nhân' mode across any browser window height."""
    if await flow.js("Boolean(document.querySelector('[aria-label=\"Chỉ dẫn cho tác nhân\"]'))"):
        await flow.find_and_trusted_click(
            "text === 'Tác nhân' && r.y > Math.max(200, window.innerHeight - 280)",
            "toggle OFF Tác nhân",
        )
        await asyncio.sleep(0.75)


async def switch_gallery_tab(flow: FlowCDP, tab_label: str) -> None:
    """Switch top-left Flow gallery tab ('Hình ảnh' or 'Video')."""
    await exit_edit_view_if_needed(flow)
    await press_escape(flow, 0.25)
    tab = await flow.js(f"""
    (() => {{
        const label = {json.dumps(tab_label)};
        const btns = Array.from(document.querySelectorAll('button, [role="tab"]')).filter(b => {{
            const r = b.getBoundingClientRect();
            const txt = (b.innerText || '').trim();
            return r.width > 0 && r.x < 360 && r.y > 40 && r.y < 280 && txt.includes(label);
        }});
        if (!btns.length) return null;
        const r = btns[0].getBoundingClientRect();
        return {{cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)}};
    }})()
    """)
    if tab:
        await flow.trusted_click(tab["cx"], tab["cy"])
        await asyncio.sleep(0.65)


async def ensure_image_mode(flow: FlowCDP, aspect_ratio: str = "16:9") -> None:
    """Ensure manual Image composer: Hình ảnh · Nano Banana Pro · <16:9 or 1:1> · x1."""
    await exit_edit_view_if_needed(flow)
    await press_escape(flow, 0.25)
    await disable_agent_mode_if_active(flow)

    crop_token = "crop_16_9" if aspect_ratio == "16:9" else "crop_square"
    pill = await flow.js("(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]')?.innerText || '').trim()")
    has_plus = await flow.js("Boolean(document.querySelector('[aria-label=\"Thêm thành phần vào ô nhập câu lệnh\"]'))")
    if "Nano Banana Pro" in pill and crop_token in pill and "x1" in pill and has_plus:
        return

    await switch_gallery_tab(flow, "Hình ảnh")

    if not await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))"):
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "open settings pill")
        await asyncio.sleep(0.45)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('Hình ảnh')", "Hình ảnh radio")
    await asyncio.sleep(0.4)
    await flow.find_and_trusted_click(
        f"el.getAttribute('role') === 'radio' && text.includes({json.dumps(aspect_ratio)})",
        f"{aspect_ratio} radio",
    )
    await asyncio.sleep(0.3)

    already_pro = await flow.js("""
    Array.from(document.querySelectorAll('button, [role="button"]')).some(b => {
        const r = b.getBoundingClientRect();
        return r.width > 0 && r.y > Math.max(120, window.innerHeight - 560) && r.y < window.innerHeight - 60 && (b.innerText || '').includes('Nano Banana Pro');
    })
    """)
    if not already_pro:
        await flow.find_and_trusted_click(
            "(text.includes('Nano Banana') || text.includes('Imagen')) && r.y > Math.max(120, window.innerHeight - 560) && r.y < window.innerHeight - 60",
            "image model dropdown",
        )
        await asyncio.sleep(0.4)
        await flow.find_and_trusted_click(
            "el.getAttribute('role') === 'menuitem' && text.includes('Nano Banana Pro')",
            "Nano Banana Pro",
        )
        await asyncio.sleep(0.3)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === 'x1'", "x1 radio")
    await asyncio.sleep(0.3)

    if await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))"):
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "close settings pill")
        await asyncio.sleep(0.4)


async def ensure_veo31_fast_4s_16x9(flow: FlowCDP) -> None:
    """Ensure manual Video composer: Video · Khung hình · 16:9 · Veo 3.1 - Fast · 4 giây · x1."""
    await exit_edit_view_if_needed(flow)
    await press_escape(flow, 0.3)
    await disable_agent_mode_if_active(flow)

    pill = await flow.js("(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]')?.innerText || '').trim()")
    has_start_slot = await flow.js("""
    Array.from(document.querySelectorAll('button, [role="button"]')).some(b => {
        const r = b.getBoundingClientRect();
        const txt = (b.innerText || '').trim();
        return r.y > Math.max(180, window.innerHeight - 340) && r.width > 0 && (txt.includes('Bắt đầu') || txt.includes('Kết thúc') || (b.getAttribute('aria-label')||'').includes('Hoán đổi khung hình'));
    })
    """)
    if "Video" in pill and "4 giây" in pill and "crop_16_9" in pill and "x1" in pill and has_start_slot:
        return

    if not await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))"):
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "open settings")
        await asyncio.sleep(0.45)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('Video')", "Video radio")
    await asyncio.sleep(0.35)
    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('Khung hình')", "Khung hình radio")
    await asyncio.sleep(0.35)
    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('16:9')", "16:9 radio")
    await asyncio.sleep(0.3)

    model_txt = await flow.js("""
    (() => {
        const el = document.querySelector('[aria-label="Chọn nhóm mô hình"]')
            || Array.from(document.querySelectorAll('button, [role="button"]')).find(b => {
                const r = b.getBoundingClientRect();
                return r.width > 0 && r.y > Math.max(120, window.innerHeight - 560) && r.y < window.innerHeight - 60 && (b.innerText || '').includes('Veo');
            });
        return (el?.innerText || '').trim();
    })()
    """)
    if "Veo 3.1 - Fast" not in model_txt:
        await flow.find_and_trusted_click(
            "(aria === 'Chọn nhóm mô hình' || text.includes('Veo')) && r.y > Math.max(120, window.innerHeight - 560) && r.y < window.innerHeight - 60",
            "model dropdown",
        )
        await asyncio.sleep(0.45)
        await flow.find_and_trusted_click("el.getAttribute('role') === 'menuitem' && text.includes('Veo 3.1 - Fast')", "Veo 3.1 - Fast")
        await asyncio.sleep(0.4)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === '4 giây'", "4 giây")
    await asyncio.sleep(0.25)
    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === 'x1'", "x1")
    await asyncio.sleep(0.25)

    if await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))"):
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "close settings")
        await asyncio.sleep(0.4)


async def _wait_visible_option_thumbnails(flow: FlowCDP, max_polls: int = 5) -> None:
    """Wait briefly for lazy-loaded <img class='asset-thumbnail-image'> inside visible [role='option'] rows."""
    for _ in range(max_polls):
        pending = await flow.js("""
        Array.from(document.querySelectorAll('[role="option"]')).filter(el => {
            const r = el.getBoundingClientRect();
            if (r.width <= 0 || r.bottom < 0 || r.top > window.innerHeight) return false;
            const txt = (el.innerText || '').trim();
            if (txt.endsWith('Video') || txt.startsWith('videocam')) return false;
            const img = el.querySelector('img');
            return !img || !(img.currentSrc || img.src || '');
        }).length
        """)
        if not pending:
            return
        await asyncio.sleep(0.22)


async def open_ingredient_modal(flow: FlowCDP) -> None:
    if not await flow.js("document.querySelectorAll('[role=\"option\"]').length > 0"):
        await flow.find_and_trusted_click("aria === 'Thêm thành phần vào ô nhập câu lệnh'", "open '+' modal")
        await asyncio.sleep(0.85)
    await _wait_visible_option_thumbnails(flow)


async def build_gallery_media_bridge(flow: FlowCDP, max_steps: int = 65) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Walk the 'Hình ảnh' gallery virtual scroller collecting <img data-media-id='<UUID>' src='.../asb/ANqvLO...'>
    so permanent 36-char UUIDs stored in Git map 1-to-1 to post-reload /asb/ANqvLO... tokens and vice versa.
    """
    await switch_gallery_tab(flow, "Hình ảnh")
    prev_sy = await flow.js("""
    (() => {
        const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
        if (!sc) return 0;
        const p = sc.scrollTop;
        sc.scrollTop = 0;
        return p;
    })()
    """)
    await asyncio.sleep(0.35)

    uuid_to_asb: Dict[str, str] = {}
    asb_to_uuid: Dict[str, str] = {}
    for _ in range(max(max_steps, 60)):
        for _ in range(4):
            ready = await flow.js("""
            (() => {
                const vis = Array.from(document.querySelectorAll('img[data-media-id]')).filter(i => {
                    const r = i.getBoundingClientRect();
                    return r.bottom > 0 && r.top < window.innerHeight;
                });
                return vis.length > 0 && vis.every(i => Boolean(i.currentSrc || i.src));
            })()
            """)
            if ready:
                break
            await asyncio.sleep(0.1)

        rows = await flow.js("""
        Array.from(document.querySelectorAll('img[data-media-id]')).map(i => ({
            mediaId: (i.getAttribute('data-media-id') || '').trim(),
            tok: (i.currentSrc || i.src || '').split('?')[0].split('/').pop().split('=')[0]
        }))
        """)
        for row in rows:
            mid = row["mediaId"]
            tok = row["tok"]
            if mid and tok:
                core = tok[:48]
                uuid_to_asb[mid] = core
                asb_to_uuid[core] = mid
                asb_to_uuid[tok] = mid

        moved = await flow.js("""
        (() => {
            const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
            if (!sc) return false;
            const prev = sc.scrollTop;
            sc.scrollTop += 480;
            return sc.scrollTop > prev;
        })()
        """)
        if not moved:
            break
        await asyncio.sleep(0.2)

    await flow.js(f"""
    (() => {{
        const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
        if (sc) sc.scrollTop = {int(prev_sy or 0)};
    }})()
    """)
    await asyncio.sleep(0.2)
    return uuid_to_asb, asb_to_uuid


def _token_matches_set(tok: str, known_set: Set[str], asb_to_uuid: Optional[Dict[str, str]] = None) -> bool:
    """Match a picker token against a set of full /asb/ tokens, 48-char cores, or permanent 36-char UUIDs."""
    if not tok:
        return False
    clean = tok.split("?")[0].split("=")[0]
    core = clean[:48]
    if clean in known_set or core in known_set:
        return True
    if asb_to_uuid:
        mapped_uuid = asb_to_uuid.get(clean) or asb_to_uuid.get(core)
        if mapped_uuid and mapped_uuid in known_set:
            return True
    for k in known_set:
        if not k:
            continue
        k_clean = k.split("?")[0].split("=")[0]
        if len(k_clean) >= 24 and (clean.startswith(k_clean[:48]) or k_clean.startswith(core)):
            return True
    return False


async def scan_all_project_options(flow: FlowCDP, max_steps: int = 65) -> List[Dict[str, str]]:
    """Walk CDK virtual-scroll picker top-to-bottom returning ordered [{txt, src, token}]."""
    await open_ingredient_modal(flow)
    await flow.js("""
    (() => {
        const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
        if (vp) vp.scrollTop = 0;
    })()
    """)
    await asyncio.sleep(0.35)

    ordered: List[Dict[str, str]] = []
    seen_keys: Set[str] = set()
    for _ in range(max_steps):
        await _wait_visible_option_thumbnails(flow)
        items = await flow.js("""
        Array.from(document.querySelectorAll('[role="option"]'))
            .map(el => {
                const rawSrc = (el.querySelector('img')?.src || '').split('?')[0];
                const tok = rawSrc.split('/').pop().split('=')[0];
                return {
                    top: el.getBoundingClientRect().top,
                    txt: (el.innerText || '').trim().replace(/\\s+/g, ' '),
                    src: rawSrc.split('=')[0],
                    token: tok,
                };
            })
            .sort((a, b) => a.top - b.top)
        """)
        for it in items:
            tok = it["token"]
            dedupe_key = tok[:48] if tok else f"txt:{it['txt']}"
            if dedupe_key and dedupe_key not in seen_keys:
                seen_keys.add(dedupe_key)
                ordered.append(it)
        moved = await flow.js("""
        (() => {
            const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
            if (!vp) return false;
            const prev = vp.scrollTop;
            vp.scrollTop += 260;
            return vp.scrollTop > prev;
        })()
        """)
        if not moved:
            break
        await asyncio.sleep(0.26)
    return ordered


async def upload_missing_files_silent(
    flow: FlowCDP,
    ws,
    file_entries: Sequence[Tuple[str, str]],
    uuid_cache: Dict[str, str],
    uuid_cache_path: str,
) -> Dict[str, str]:
    """Silently upload missing plate/ref files via intercepted fileChooser + DOM.setFileInputFiles."""
    await press_escape(flow, 0.3)
    existing_opts = await scan_all_project_options(flow, max_steps=65)
    await press_escape(flow, 0.3)

    missing: List[Tuple[str, str]] = []
    for fname, fpath in file_entries:
        stem = os.path.splitext(fname)[0]
        known_u = uuid_cache.get(fname, "").split("=")[0][:48]
        matched_opt = next(
            (
                it for it in existing_opts
                if (known_u and known_u in (it.get("src") or "")) or (stem in (it.get("txt") or ""))
            ),
            None,
        )
        if matched_opt is not None:
            if matched_opt.get("token"):
                uuid_cache[fname] = matched_opt["token"][:48]
        else:
            if not os.path.isfile(fpath):
                raise FileNotFoundError(f"Required ingredient file missing on disk: {fpath}")
            missing.append((fname, fpath))

    with open(uuid_cache_path, "w", encoding="utf-8") as f:
        json.dump(uuid_cache, f, indent=2)

    if not missing:
        print(f"All {len(file_entries)} ingredient file(s) already uploaded & verified on Flow!")
        return uuid_cache

    print(f"Uploading {len(missing)} ingredient file(s) silently: {[m[0] for m in missing]}...")
    await flow.call("Page.setInterceptFileChooserDialog", {"enabled": True})
    try:
        idx = 0
        while idx < len(missing):
            rect = await flow.js("""
            (() => {
                const el = document.querySelector('[aria-label="Trình đơn thêm nội dung nghe nhìn"]');
                const r = el.getBoundingClientRect();
                return {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)};
            })()
            """)
            await flow.trusted_click(rect["x"], rect["y"])
            await asyncio.sleep(0.55)
            item_rect = await flow.js("""
            (() => {
                const els = Array.from(document.querySelectorAll('[role="menuitem"]'))
                    .filter(el => (el.innerText || '').includes('Tải lên'));
                const r = els[0].getBoundingClientRect();
                return {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)};
            })()
            """)
            await ws.send(json.dumps({"id": 99001, "method": "Input.dispatchMouseEvent", "params": {"type": "mouseMoved", "x": item_rect["x"], "y": item_rect["y"]}}))
            await ws.send(json.dumps({"id": 99002, "method": "Input.dispatchMouseEvent", "params": {"type": "mousePressed", "x": item_rect["x"], "y": item_rect["y"], "button": "left", "clickCount": 1}}))
            await ws.send(json.dumps({"id": 99003, "method": "Input.dispatchMouseEvent", "params": {"type": "mouseReleased", "x": item_rect["x"], "y": item_rect["y"], "button": "left", "clickCount": 1}}))

            fc_ev = None
            for _ in range(35):
                raw = await asyncio.wait_for(ws.recv(), timeout=6.0)
                d = json.loads(raw)
                if d.get("method") == "Page.fileChooserOpened":
                    fc_ev = d
                    break
            if not fc_ev:
                raise RuntimeError("Page.fileChooserOpened did not fire during silent upload!")

            mode = fc_ev["params"].get("mode", "")
            if mode == "selectMultiple":
                batch_entries = missing[idx:]
                idx = len(missing)
            else:
                batch_entries = [missing[idx]]
                idx += 1

            batch_files = [m[1] for m in batch_entries]
            await flow.call(
                "DOM.setFileInputFiles",
                {"files": batch_files, "backendNodeId": fc_ev["params"]["backendNodeId"]},
            )
            last_base = os.path.splitext(os.path.basename(batch_files[-1]))[0]
            for up_step in range(30):
                await asyncio.sleep(1.2)
                pct = await flow.js("""
                Array.from(document.querySelectorAll('div, span'))
                    .map(e => (e.innerText || '').trim())
                    .filter(t => /^\\d+%$/.test(t))
                """)
                cards = await flow.js(f"""
                Array.from(document.querySelectorAll('button'))
                    .map(b => b.getAttribute('aria-label') || '')
                    .filter(a => a.includes({json.dumps(last_base)}))
                """)
                if (cards or up_step >= 5) and not pct:
                    print(f"  Uploaded through {last_base}!")
                    break
    finally:
        await flow.call("Page.setInterceptFileChooserDialog", {"enabled": False})

    await asyncio.sleep(1.2)
    refreshed = await scan_all_project_options(flow, max_steps=65)
    await press_escape(flow, 0.3)
    for fname, _ in missing:
        stem = os.path.splitext(fname)[0]
        hit = next((it["token"] for it in refreshed if stem in it["txt"] and it.get("token")), None)
        if hit:
            uuid_cache[fname] = hit[:48]
            print(f"  Registered token for {fname}: {uuid_cache[fname]}")
    with open(uuid_cache_path, "w", encoding="utf-8") as f:
        json.dump(uuid_cache, f, indent=2)
    return uuid_cache


async def attach_ingredient_verified(
    flow: FlowCDP,
    filename: str,
    uuid_cache: Dict[str, str],
    uuid_cache_path: Optional[str] = None,
) -> None:
    """Attach 1 ingredient in '+' modal, tolerating lazy-loaded thumbnails and verifying chip +1."""
    stem = os.path.splitext(filename)[0]
    known_uuid = uuid_cache.get(filename, "").split("=")[0][:48]
    await open_ingredient_modal(flow)

    await flow.js("""
    (() => {
        const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
        if (vp) vp.scrollTop = 0;
    })()
    """)
    await asyncio.sleep(0.3)

    hit = False
    for _ in range(75):
        await _wait_visible_option_thumbnails(flow, max_polls=3)
        m = await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(stem)};
            const ku = {json.dumps(known_uuid)};
            const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
            const vpRect = vp ? vp.getBoundingClientRect() : null;
            for (const el of Array.from(document.querySelectorAll('[role="option"]'))) {{
                const txt = (el.innerText || '').trim();
                const src = el.querySelector('img')?.src || '';
                if ((idStr && txt.includes(idStr)) || (ku && src.includes(ku))) {{
                    if (vp && vpRect) {{
                        const er = el.getBoundingClientRect();
                        vp.scrollTop += (er.top + er.height / 2) - (vpRect.top + 150);
                    }}
                    return true;
                }}
            }}
            return false;
        }})()
        """)
        if m:
            await asyncio.sleep(0.35)
            await _wait_visible_option_thumbnails(flow, max_polls=5)
            hit = True
            break
        moved = await flow.js("""
        (() => {
            const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
            if (!vp) return false;
            const prev = vp.scrollTop;
            vp.scrollTop += 260;
            return vp.scrollTop > prev;
        })()
        """)
        if not moved:
            break
        await asyncio.sleep(0.25)

    if not hit:
        raise RuntimeError(f"Ingredient {filename!r} (token={known_uuid!r}) not found in Flow modal!")

    async def inspect_dialog():
        return await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(stem)};
            const ku = {json.dumps(known_uuid)};
            let targetOpt = null;
            for (const el of Array.from(document.querySelectorAll('[role="option"]'))) {{
                const txt = (el.innerText || '').trim();
                const img = el.querySelector('img');
                const src = img?.src || '';
                if ((idStr && txt.includes(idStr)) || (ku && src.includes(ku))) {{
                    const r = (img && img.getBoundingClientRect().width > 10 ? img : el).getBoundingClientRect();
                    targetOpt = {{
                        token: src ? src.split('?')[0].split('/').pop().split('=')[0] : '',
                        cx: Math.round(r.x + Math.min(r.width / 2, 45)),
                        cy: Math.round(r.y + r.height / 2),
                    }};
                    break;
                }}
            }}
            const addBtn = Array.from(document.querySelectorAll('button')).find(
                b => (b.innerText || '').trim() === 'Thêm vào câu lệnh' && b.getBoundingClientRect().width > 0
            );
            let previewSrcs = [];
            if (addBtn) {{
                let container = addBtn.parentElement;
                while (container && !container.querySelector('[role="option"]') && container.parentElement) {{
                    container = container.parentElement;
                }}
                if (container) {{
                    previewSrcs = Array.from(container.querySelectorAll('img'))
                        .filter(i => !i.closest('[role="option"]'))
                        .map(i => (i.src || '').split('?')[0]);
                }}
            }}
            return {{targetOpt, hasAddBtn: Boolean(addBtn), previewSrcs}};
        }})()
        """)

    st = await inspect_dialog()
    if not st["targetOpt"]:
        raise RuntimeError(f"Ingredient {filename!r} disappeared from viewport during inspection.")

    target_core = (st["targetOpt"]["token"] or known_uuid)[:48]
    if st["targetOpt"]["token"]:
        uuid_cache[filename] = target_core
        if uuid_cache_path:
            with open(uuid_cache_path, "w", encoding="utf-8") as f:
                json.dump(uuid_cache, f, indent=2)

    def _matches_preview(st_obj: Dict[str, Any], core: str) -> bool:
        if not st_obj.get("hasAddBtn"):
            return False
        if not core:
            return len(st_obj.get("previewSrcs") or []) > 0
        return any(core in u for u in (st_obj.get("previewSrcs") or []))

    is_previewed = _matches_preview(st, target_core)
    if not is_previewed:
        for dx in (0, 55, 105):
            st_cur = await inspect_dialog()
            if not st_cur["targetOpt"]:
                break
            if st_cur["targetOpt"]["token"] and not target_core:
                target_core = st_cur["targetOpt"]["token"][:48]
            await flow.trusted_click(st_cur["targetOpt"]["cx"] + dx, st_cur["targetOpt"]["cy"])
            for _ in range(7):
                await asyncio.sleep(0.3)
                st2 = await inspect_dialog()
                if st2["targetOpt"] and st2["targetOpt"]["token"]:
                    target_core = st2["targetOpt"]["token"][:48]
                    uuid_cache[filename] = target_core
                    if uuid_cache_path:
                        with open(uuid_cache_path, "w", encoding="utf-8") as f:
                            json.dump(uuid_cache, f, indent=2)
                if _matches_preview(st2, target_core):
                    is_previewed = True
                    break
            if is_previewed:
                break
        if not is_previewed:
            raise RuntimeError(f"Could not lock preview for ingredient {filename!r} ({target_core})")

    before_chips = await flow.js("document.querySelectorAll('button[aria-label=\"Thành phần\"]').length")
    await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")

    after_chips = before_chips
    for _ in range(12):
        await asyncio.sleep(0.3)
        after_chips = await flow.js("document.querySelectorAll('button[aria-label=\"Thành phần\"]').length")
        if after_chips >= before_chips + 1:
            break
    if after_chips < before_chips + 1:
        raise RuntimeError(f"Chip count did not increment for {filename}: before={before_chips}, after={after_chips}")
    print(f"  + Attached {stem} (chips={after_chips})")


async def get_rendered_gallery_items(flow: FlowCDP) -> List[Dict[str, str]]:
    """Return top-to-bottom rendered gallery images [{src, base, media_id}]."""
    imgs = await flow.js("""
    Array.from(document.querySelectorAll('img'))
        .filter(i => !i.closest('button[aria-label="Thành phần"]') && !i.closest('[role="option"]'))
        .map(i => ({
            src: i.currentSrc || i.src || '',
            mediaId: (i.getAttribute('data-media-id') || '').trim(),
            nw: i.naturalWidth,
            top: i.getBoundingClientRect().top
        }))
        .filter(i => (i.src.includes('flow-content.google/image/') || i.src.includes('/asb/') || i.src.includes('googleusercontent.com/')) && i.nw >= 512)
        .sort((a, b) => a.top - b.top)
    """)
    out: List[Dict[str, str]] = []
    for im in imgs:
        src = im["src"]
        base = src.split("?")[0].split("=")[0]
        mid = im["mediaId"]
        if not mid and "flow-content.google/image/" in base:
            cand = base.split("/")[-1]
            if UUID_RE.match(cand):
                mid = cand
        out.append({"src": src, "base": base, "media_id": mid})
    return out


async def get_rendered_gallery_urls(flow: FlowCDP) -> List[str]:
    return [it["src"] for it in await get_rendered_gallery_items(flow)]


async def _fetch_flow_image_bytes(flow: FlowCDP, img_url: str) -> bytes:
    """
    Download full-resolution image bytes from Google Flow without triggering cross-origin CORS errors:
    - Upgrades same-origin '/asb/...=s1600-rw' FIFE URLs to '=s0' (uncompressed original JPEG)
    - Uses credentials='same-origin' for flow.google.com and credentials='omit' for cross-origin
      signed URLs (flow-content.google / googleusercontent.com, where credentials='include' fails CORS!)
    - Validates HTTP 200 status & byte length, falling back to an offscreen <canvas> capture if needed.
    """
    b64_data = await flow.js(f"""
    (async () => {{
        const origUrl = {json.dumps(img_url)};
        const candidates = [];
        if (origUrl.includes('/asb/') && /=s\\d+[^?]*$/.test(origUrl)) {{
            candidates.push(origUrl.replace(/=s\\d+[^?]*$/, '=s0'));
        }}
        candidates.push(origUrl);

        const toB64 = (buf) => {{
            let binary = '';
            const bytes = new Uint8Array(buf);
            const chunk = 0x8000;
            for (let i = 0; i < bytes.length; i += chunk) {{
                binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
            }}
            return btoa(binary);
        }};

        let lastErr = '';
        for (const u of candidates) {{
            try {{
                const sameOrigin = u.startsWith(window.location.origin + '/');
                const resp = await fetch(u, {{credentials: sameOrigin ? 'same-origin' : 'omit'}});
                if (!resp.ok) {{
                    lastErr = 'HTTP ' + resp.status + ' for ' + u.slice(0, 70);
                    continue;
                }}
                const buf = await resp.arrayBuffer();
                if (buf.byteLength < 1024) {{
                    lastErr = 'Payload too small (' + buf.byteLength + 'B)';
                    continue;
                }}
                return toB64(buf);
            }} catch (e) {{
                lastErr = String(e);
            }}
        }}

        // Fallback: draw matching loaded DOM <img> onto an offscreen canvas if CORS allows
        const baseTarget = origUrl.split('?')[0].split('=')[0];
        const domImg = Array.from(document.querySelectorAll('img')).find(
            i => (i.currentSrc || i.src || '').includes(baseTarget) && i.naturalWidth >= 512
        );
        if (domImg) {{
            try {{
                const c = document.createElement('canvas');
                c.width = domImg.naturalWidth;
                c.height = domImg.naturalHeight;
                c.getContext('2d').drawImage(domImg, 0, 0);
                const dataUrl = c.toDataURL('image/png');
                return dataUrl.split(',')[1];
            }} catch (e) {{
                lastErr += ' | canvas: ' + String(e);
            }}
        }}
        throw new Error('Failed to fetch rendered Flow image bytes: ' + lastErr);
    }})()
    """)
    return base64.b64decode(b64_data)


async def _click_retry_if_failed_card(flow: FlowCDP, label: str) -> bool:
    has_fail = await flow.js("(document.body.innerText || '').includes('Không thành công')")
    if not has_fail:
        return False
    retry_btn = await flow.js("""
    (() => {
        const cards = Array.from(document.querySelectorAll('div, flow-grid-tile-container')).filter(d => {
            const r = d.getBoundingClientRect();
            return r.width > 240 && r.width < 680 && r.height > 140 && r.height < 480 && (d.innerText || '').includes('Không thành công');
        });
        if (!cards.length) return null;
        const btns = Array.from(cards[0].querySelectorAll('button'));
        if (!btns.length) return null;
        const r = btns[0].getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    if retry_btn:
        print(f"  Detected 'Không thành công' on {label} — clicking native Retry...")
        await flow.trusted_click(retry_btn["cx"], retry_btn["cy"])
        await asyncio.sleep(4.0)
        return True
    return False


def _decode_and_normalize_flow_image_bytes(raw_bytes: bytes) -> Image.Image:
    """Decode JPEG/WebP/PNG Flow image bytes, apply EXIF transpose, composite alpha onto #FFFFFF, and verify size."""
    with Image.open(io.BytesIO(raw_bytes)) as decoded:
        transposed = ImageOps.exif_transpose(decoded)
        clean_rgb, _had_alpha = composite_to_rgb_white(transposed)
    if clean_rgb.size[0] < 256 or clean_rgb.size[1] < 256:
        raise RuntimeError(f"Decoded Flow image too small: {clean_rgb.size}")
    return clean_rgb


async def isolate_white_on_flow(
    input_image_path: str,
    output_white_path: str,
    project_id: str,
    preset_name: str = "crochet_decor",
    custom_prompt: str = "",
    port: Optional[int] = None,
) -> str:
    """
    Stage 0: Upload a raw messy-background product photo (e.g. crochet item on a wooden desk)
    to Google Flow Nano Banana Pro (1:1), isolate it onto pure #FFFFFF white background,
    and save a validated full-resolution RGB image locally for build-plates.
    """
    if not os.path.isfile(input_image_path):
        raise FileNotFoundError(f"Raw input image not found: {input_image_path}")
    preset = get_preset(preset_name)
    prompt = custom_prompt.strip() or preset.white_isolation_prompt
    fname = os.path.basename(input_image_path)
    out_dir = os.path.dirname(os.path.abspath(output_white_path))
    os.makedirs(out_dir, exist_ok=True)
    tmp_cache_path = os.path.join(out_dir, "_white_iso_uuid_cache.json")
    uuid_cache: Dict[str, str] = {}
    if os.path.isfile(tmp_cache_path):
        with open(tmp_cache_path, "r", encoding="utf-8") as f:
            raw_cache = json.load(f)
            uuid_cache = {str(k): str(v) for k, v in raw_cache.items() if isinstance(v, str)}

    ws_url = get_project_ws_url(project_id, port=port, auto_open=True)
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws, project_id=project_id)
        await switch_gallery_tab(flow, "Hình ảnh")
        await ensure_image_mode(flow, aspect_ratio="1:1")
        await upload_missing_files_silent(flow, ws, [(fname, os.path.abspath(input_image_path))], uuid_cache, tmp_cache_path)

        await clear_composer_strict(flow)
        before_items = await get_rendered_gallery_items(flow)
        before_bases = {it["base"] for it in before_items}
        await attach_ingredient_verified(flow, fname, uuid_cache, tmp_cache_path)

        ed_rect = await flow.js("""
        (() => {
            const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
            const r = el.getBoundingClientRect();
            return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
        })()
        """)
        await flow.trusted_click(ed_rect["cx"], ed_rect["cy"])
        await asyncio.sleep(0.2)
        await flow.call("Input.insertText", {"text": prompt})
        await asyncio.sleep(0.4)
        await flow.find_and_trusted_click("aria === 'Bắt đầu tạo' && !el.disabled", "submit 1:1 white isolation")
        print("  Submitted 1:1 white-background studio isolation on Flow...")

        new_item: Optional[Dict[str, str]] = None
        for step in range(55):
            await asyncio.sleep(2.0)
            await flow.js("""
            (() => {
                const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
                if (sc) sc.scrollTop = 0;
                window.scrollTo(0, 0);
            })()
            """)
            await _click_retry_if_failed_card(flow, "white-isolation")
            cur_items = await get_rendered_gallery_items(flow)
            for it in cur_items:
                if it["base"] not in before_bases:
                    new_item = it
                    break
            pcts = await flow.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            if new_item and not pcts and step >= 5:
                break

        if not new_item:
            raise RuntimeError("Timed out waiting for 1:1 white-background isolation render on Google Flow.")

        raw_bytes = await _fetch_flow_image_bytes(flow, new_item["src"])
        clean_rgb = _decode_and_normalize_flow_image_bytes(raw_bytes)

        out_base = os.path.basename(output_white_path)
        if output_white_path.lower().endswith(".png"):
            clean_rgb.save(output_white_path, "PNG")
        else:
            clean_rgb.save(output_white_path, "JPEG", quality=96, subsampling=0)

        # Record generated 1:1 isolation render tokens so map-uuids never confuses it with a 16:9 TVC scene
        iso_tok = new_item["base"].split("/")[-1][:48]
        if iso_tok:
            uuid_cache[f"__isolated_render__:{out_base}:token"] = iso_tok
        if new_item.get("media_id"):
            uuid_cache[f"__isolated_render__:{out_base}:media_id"] = new_item["media_id"]
        with open(tmp_cache_path, "w", encoding="utf-8") as f:
            json.dump(uuid_cache, f, indent=2)

        print(f"Saved clean white-background SKU master ({clean_rgb.size[0]}x{clean_rgb.size[1]}) -> {output_white_path}")
    return output_white_path


async def submit_single_image_scene(
    flow: FlowCDP,
    scene: Dict[str, Any],
    uuid_cache: Dict[str, str],
    uuid_cache_path: str,
    wait_for_render: bool = True,
) -> Optional[str]:
    print(f"\n=== SUBMITTING IMAGE SCENE: {scene['key']} ===")
    await press_escape(flow, 0.25)
    await flow.js("""
    (() => {
        const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
        if (sc) sc.scrollTop = 0;
        window.scrollTo(0, 0);
    })()
    """)
    await asyncio.sleep(0.25)
    await ensure_image_mode(flow, aspect_ratio="16:9")
    await clear_composer_strict(flow)

    before_items = await get_rendered_gallery_items(flow)
    before_bases = {it["base"] for it in before_items}
    for ref_name in scene["refs"]:
        await attach_ingredient_verified(flow, ref_name, uuid_cache, uuid_cache_path)

    ed_rect = await flow.js("""
    (() => {
        const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
        const r = el.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    await flow.trusted_click(ed_rect["cx"], ed_rect["cy"])
    await asyncio.sleep(0.15)
    await flow.call("Input.insertText", {"text": scene["prompt"]})
    await asyncio.sleep(0.35)

    btns = await flow.js("""
    Array.from(document.querySelectorAll('[aria-label="Bắt đầu tạo"]')).map(el => {
        const r = el.getBoundingClientRect();
        const cx = Math.round(r.x + r.width / 2);
        const cy = Math.round(r.y + r.height / 2);
        const topEl = document.elementFromPoint(cx, cy);
        const hit = Boolean(topEl && (el === topEl || el.contains(topEl)));
        return {cx, cy, hit, disabled: el.disabled};
    })
    """)
    target = next((b for b in btns if b["hit"] and not b["disabled"]), None)
    if not target:
        raise RuntimeError(f"Submit button not ready for {scene['key']}: {btns}")
    await flow.trusted_click(target["cx"], target["cy"])
    print(f"  Queued {scene['key']}!")

    if not wait_for_render:
        await asyncio.sleep(1.8)
        return None

    saw_pct = False
    for step in range(55):
        await asyncio.sleep(2.0)
        await flow.js("""
        (() => {
            const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
            if (sc) sc.scrollTop = 0;
            window.scrollTo(0, 0);
        })()
        """)
        if await _click_retry_if_failed_card(flow, scene["key"]):
            continue
        pcts = await flow.js("""
        Array.from(document.querySelectorAll('div, span'))
            .map(e => (e.innerText || '').trim())
            .filter(t => /^\\d+%$/.test(t))
        """)
        if pcts:
            saw_pct = True
        cur_items = await get_rendered_gallery_items(flow)
        new_items = [it for it in cur_items if it["base"] not in before_bases]
        if not pcts and (saw_pct or step >= 7) and new_items:
            newest = new_items[0]
            rendered_id = newest.get("media_id") or ""
            if not rendered_id:
                tok_cand = newest["base"].split("/")[-1][:48]
                _, asb_to_uuid = await build_gallery_media_bridge(flow, max_steps=6)
                rendered_id = asb_to_uuid.get(tok_cand, tok_cand)
            print(f"  Rendered {scene['key']} in {(step + 1) * 2}s! (id={rendered_id})")
            return rendered_id
    print(f"  Warning: timeout waiting for {scene['key']}, continuing...")
    return None


async def capture_qa_pages(flow: FlowCDP, qa_dir: str, prefix: str, tab_label: str) -> None:
    os.makedirs(qa_dir, exist_ok=True)
    await switch_gallery_tab(flow, tab_label)
    for idx, sy in enumerate((0, 540, 1080, 1620)):
        await flow.js(f"""
        (() => {{
            const primary = document.querySelector('.cdk-virtual-scrollable.page-container');
            if (primary) {{
                primary.scrollTop = {sy};
            }} else {{
                const scrollers = Array.from(document.querySelectorAll('div, main')).filter(el => el.scrollHeight > el.clientHeight + 200);
                for (const s of scrollers) s.scrollTop = {sy};
            }}
            window.scrollTo(0, {sy});
        }})()
        """)
        await asyncio.sleep(0.9)
        res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 86})
        out_p = os.path.join(qa_dir, f"qa_{prefix}_page{idx + 1}.jpg")
        with open(out_p, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("Saved local QA screenshot:", out_p)
    await flow.js("""
    (() => {
        const primary = document.querySelector('.cdk-virtual-scrollable.page-container');
        if (primary) primary.scrollTop = 0;
        window.scrollTo(0, 0);
    })()
    """)


async def run_images_pipeline(
    config: Dict[str, Any],
    project_dir: str,
    phase: str = "check1",
    start_index: int = 0,
    only_key: str = "",
    port: Optional[int] = None,
) -> None:
    """Stage 1: Validate prompts + local plates, upload missing ingredients, render 16:9 scenes."""
    errs = validate_sku_config(config, project_dir=project_dir, require_local_plates=True)
    if errs:
        raise ValueError("SKU config failed pre-flight validation:\n  - " + "\n  - ".join(errs))

    slug = config["slug"]
    scenes = list(config.get("scenes", []))
    if not scenes:
        raise ValueError("No scenes defined in SKU config.")

    if phase == "only":
        only_tokens = [tok.strip() for tok in (only_key or "").split(",") if tok.strip()]
        scenes = [s for s in scenes if only_tokens and any(tok in s["key"] for tok in only_tokens)]
        if not scenes:
            raise ValueError(f"No scene matching --only-key={only_key!r}")
    elif phase == "check1":
        scenes = scenes[:1]
    elif phase == "rest":
        scenes = scenes[1:]
    elif phase == "slice":
        scenes = scenes[start_index:]

    if not scenes:
        print(f"No remaining scenes to render for phase={phase!r}.")
        return

    # Collect unique required files across config scenes
    needed_files: List[Tuple[str, str]] = []
    seen_f: Set[str] = set()
    for sc in config.get("scenes", []):
        for rf in sc["refs"]:
            if rf in seen_f:
                continue
            seen_f.add(rf)
            p_plate = os.path.join(project_dir, "plates_2k", rf)
            p_ref = os.path.join(project_dir, "clean_refs", rf)
            needed_files.append((rf, p_plate if os.path.isfile(p_plate) else p_ref))

    uuid_cache_path = os.path.join(project_dir, f"{slug}_plate_uuids.json")
    uuid_cache: Dict[str, str] = {}
    if os.path.isfile(uuid_cache_path):
        with open(uuid_cache_path, "r", encoding="utf-8") as f:
            uuid_cache = json.load(f)

    qa_dir = os.path.join(project_dir, "qa")
    ws_url = get_project_ws_url(config["project_id"], port=port, auto_open=True)
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws, project_id=config["project_id"])
        await switch_gallery_tab(flow, "Hình ảnh")
        await ensure_image_mode(flow, aspect_ratio="16:9")
        await upload_missing_files_silent(flow, ws, needed_files, uuid_cache, uuid_cache_path)

        if len(scenes) == 1:
            new_uuid = await submit_single_image_scene(flow, scenes[0], uuid_cache, uuid_cache_path, wait_for_render=True)
            if new_uuid:
                scene_uuids_path = os.path.join(project_dir, f"{slug}_scene_uuids.json")
                scene_uuids: Dict[str, str] = {}
                if os.path.isfile(scene_uuids_path):
                    with open(scene_uuids_path, "r", encoding="utf-8") as f:
                        scene_uuids = json.load(f)
                scene_uuids[scenes[0]["key"]] = new_uuid
                with open(scene_uuids_path, "w", encoding="utf-8") as f:
                    json.dump(scene_uuids, f, indent=2)
                print(f"  Updated {os.path.basename(scene_uuids_path)}[{scenes[0]['key']!r}] -> {new_uuid}")

            os.makedirs(qa_dir, exist_ok=True)
            await asyncio.sleep(1.5)
            res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 86})
            out_p = os.path.join(qa_dir, f"qa_{slug}_{scenes[0]['key']}.jpg")
            with open(out_p, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("Saved single-scene QA screenshot:", out_p)
            return

        for w_idx in range(0, len(scenes), 3):
            wave = scenes[w_idx:w_idx + 3]
            await flow.js("""
            (() => {
                const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
                if (sc) sc.scrollTop = 0;
                window.scrollTo(0, 0);
            })()
            """)
            await asyncio.sleep(0.3)
            wave_before_bases = {it["base"] for it in await get_rendered_gallery_items(flow)}
            for sc in wave:
                await submit_single_image_scene(flow, sc, uuid_cache, uuid_cache_path, wait_for_render=False)
            print(f"  Waiting for {slug} wave {w_idx // 3 + 1} ({len(wave)} images)...")
            saw_pct = False
            zero_streak = 0
            for step in range(75):
                await asyncio.sleep(2.2)
                await flow.js("""
                (() => {
                    const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
                    if (sc) sc.scrollTop = 0;
                    window.scrollTo(0, 0);
                })()
                """)
                if await _click_retry_if_failed_card(flow, f"wave-{w_idx // 3 + 1}"):
                    saw_pct = True
                    zero_streak = 0
                    continue
                pcts = await flow.js("""
                Array.from(document.querySelectorAll('div, span'))
                    .map(e => (e.innerText || '').trim())
                    .filter(t => /^\\d+%$/.test(t))
                """)
                cur_items = await get_rendered_gallery_items(flow)
                new_wave_items = [it for it in cur_items if it["base"] not in wave_before_bases]
                if pcts:
                    saw_pct = True
                    zero_streak = 0
                elif (len(new_wave_items) >= len(wave) and (saw_pct or step >= 5)) or step >= 55:
                    zero_streak += 1
                if zero_streak >= 2:
                    print(f"  Wave {w_idx // 3 + 1} finished ({len(new_wave_items)}/{len(wave)} new rendered cards ready)!")
                    break

        await asyncio.sleep(3.5)
        await capture_qa_pages(flow, qa_dir, f"{slug}_img", "Hình ảnh")


async def map_scene_uuids_pipeline(
    config: Dict[str, Any],
    project_dir: str,
    port: Optional[int] = None,
    only_key: str = "",
    force_remap: bool = False,
) -> Dict[str, str]:
    """
    Stage 2: Bridge gallery permanent 36-char data-media-id UUIDs <-> /asb/ picker tokens,
    filter out uploaded plates/raws/videos/exclusions, and lock 1-to-1 scene_key -> permanent UUID.
    """
    slug = config["slug"]
    prefix = config["prefix"].upper()
    scenes = list(config.get("scenes", []))
    if not scenes:
        raise ValueError("No scenes defined in SKU config.")

    target_scenes = scenes
    if only_key:
        only_tokens = [tok.strip() for tok in (only_key or "").split(",") if tok.strip()]
        target_scenes = [
            s for s in scenes
            if only_tokens and any(tok in s["key"] for tok in only_tokens)
        ]
        if not target_scenes:
            raise ValueError(f"No scene matching --only-key={only_key!r}")

    excluded_all: Set[str] = set(str(x) for x in config.get("exclude_uuids", []) if x)
    cache_candidates = [
        os.path.join(project_dir, f"{slug}_plate_uuids.json"),
        os.path.join(project_dir, "_white_iso_uuid_cache.json"),
        os.path.join(project_dir, "clean_refs", "_white_iso_uuid_cache.json"),
    ]
    for cp in cache_candidates:
        if os.path.isfile(cp):
            with open(cp, "r", encoding="utf-8") as f:
                raw_d = json.load(f)
            for v in raw_d.values():
                if isinstance(v, str) and v:
                    excluded_all.add(v)
                elif isinstance(v, list):
                    excluded_all.update(str(x) for x in v if x)

    ws_url = get_project_ws_url(config["project_id"], port=port, auto_open=True)
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws, project_id=config["project_id"])
        await exit_edit_view_if_needed(flow)
        await press_escape(flow, 0.3)
        _, asb_to_uuid = await build_gallery_media_bridge(flow, max_steps=65)
        await ensure_image_mode(flow, aspect_ratio="16:9")
        ordered = await scan_all_project_options(flow, max_steps=75)
        await press_escape(flow, 0.3)

    filtered: List[Dict[str, str]] = []
    seen_norm: Set[str] = set()
    for it in ordered:
        raw_tok = (it.get("token") or "").strip()
        txt = (it.get("txt") or "").strip()
        if not raw_tok:
            continue
        if UPLOADED_EXT_RE.search(txt):
            continue
        if txt.endswith(" Video") or txt.lower().startswith("videocam"):
            continue
        if f"{prefix}_PLATE_" in txt or f"{prefix}_REF_" in txt:
            continue
        if _token_matches_set(raw_tok, excluded_all, asb_to_uuid):
            continue
        norm_tok = asb_to_uuid.get(raw_tok) or asb_to_uuid.get(raw_tok[:48]) or raw_tok
        if norm_tok in seen_norm:
            continue
        seen_norm.add(norm_tok)
        filtered.append({"token": norm_tok, "raw_token": raw_tok, "txt": txt})

    if len(filtered) < len(target_scenes):
        raise RuntimeError(
            f"Expected at least {len(target_scenes)} generated image(s) for {slug}, found only {len(filtered)}."
        )

    out_path = os.path.join(project_dir, f"{slug}_scene_uuids.json")
    existing_mapping: Dict[str, str] = {}
    if os.path.isfile(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            existing_mapping = json.load(f)

    if not only_key and len(existing_mapping) >= len(scenes) and len(filtered) > len(scenes) and not force_remap:
        raise RuntimeError(
            f"Found {len(filtered)} generated images for {len(scenes)} scenes while {os.path.basename(out_path)} "
            f"already has {len(existing_mapping)} locked entries (likely after single-scene re-renders). "
            f"Use `map-uuids --only-key <SCENE_KEY>` to update just the re-rendered scene, or pass "
            f"`--force-remap` to overwrite all {len(scenes)} scenes newest-first."
        )

    newest_n = filtered[:len(target_scenes)]
    oldest_to_newest = list(reversed(newest_n))
    mapping: Dict[str, str] = dict(existing_mapping) if only_key else {}
    for sc, it in zip(target_scenes, oldest_to_newest):
        mapping[sc["key"]] = it["token"]
        print(f"  {sc['key']:40s} -> {it['token']} | {it['txt'][:60]}")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)
    print(f"Saved {len(mapping)} scene UUID(s) -> {out_path}")
    return mapping


async def clear_frame_slots_and_text(flow: FlowCDP) -> None:
    await clear_composer_strict(flow)
    for _ in range(4):
        has_empty_both = await flow.js("""
        (() => {
            const minY = Math.max(180, window.innerHeight - 340);
            const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(
                b => !b.closest('[data-media-id]') && b.getBoundingClientRect().y > minY && b.getBoundingClientRect().width > 0
            );
            const s = btns.some(b => (b.innerText || '').trim().includes('Bắt đầu') && !(b.getAttribute('aria-label') || '').includes('Bắt đầu tạo'));
            const e = btns.some(b => (b.innerText || '').trim().includes('Kết thúc'));
            return s && e;
        })()
        """)
        if has_empty_both:
            break
        clicked_x = await flow.js("""
        (() => {
            const minY = Math.max(180, window.innerHeight - 310);
            const maxY = window.innerHeight - 35;
            const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => {
                if (b.closest('[data-media-id]') || b.closest('[role="dialog"]')) return false;
                const r = b.getBoundingClientRect();
                if (r.width <= 0 || r.width > 64 || r.height > 64 || r.y < minY || r.y > maxY) return false;
                const txt = (b.innerText || '').trim().toLowerCase();
                const aria = (b.getAttribute('aria-label') || '').toLowerCase();
                if (aria.includes('bắt đầu tạo') || aria.includes('thêm nội dung') || aria === 'thành phần') return false;
                return txt === 'close' || txt === 'clear' || txt.includes('cancel') || txt === '×' || txt === '✕' || aria.includes('xoá') || aria.includes('xóa') || aria.includes('đóng') || aria.includes('khung hình') || aria.includes('thành phần tạo hình ảnh');
            });
            if (!btns.length) return null;
            const r = btns[0].getBoundingClientRect();
            return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
        })()
        """)
        if clicked_x:
            await flow.trusted_click(clicked_x["cx"], clicked_x["cy"])
            await asyncio.sleep(0.4)
        else:
            break


async def _populate_frame_slot_by_token(
    flow: FlowCDP,
    slot_label: str,
    target_token: str,
    alt_tokens: Sequence[str] = (),
) -> None:
    """
    Populate either 'Bắt đầu' or 'Kết thúc' frame slot with virtual-scroll re-centering + 3 retries.
    Matches permanent 36-char UUIDs AND bridged '/asb/ANqvLO...' picker tokens seamlessly.
    """
    cand_tokens: List[str] = []
    for raw in (target_token, *alt_tokens):
        if not raw:
            continue
        c = raw.split("?")[0].split("=")[0][:48]
        if c and c not in cand_tokens:
            cand_tokens.append(c)
    if not cand_tokens:
        raise ValueError(f"Empty token passed to _populate_frame_slot_by_token for {slot_label!r}")

    last_err = ""
    for attempt in range(1, 6):
        await press_escape(flow, 0.35)
        slot_rect = await flow.js(f"""
        (() => {{
            const lbl = {json.dumps(slot_label)};
            const minY = Math.max(180, window.innerHeight - 360);
            const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(el => {{
                if (el.closest('[data-media-id]') || el.closest('[role="dialog"]')) return false;
                const r = el.getBoundingClientRect();
                if (r.width <= 0 || r.height <= 0 || r.y <= minY) return false;
                const text = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                const aria = el.getAttribute('aria-label') || '';
                return text.includes(lbl) && !aria.includes('Bắt đầu tạo');
            }});
            if (!btns.length) return null;
            const r = btns[btns.length - 1].getBoundingClientRect();
            return {{cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)}};
        }})()
        """)
        if not slot_rect:
            last_err = f"composer slot button {slot_label!r} not visible on attempt {attempt}"
            await asyncio.sleep(0.6)
            continue
        await flow.trusted_click(slot_rect["cx"], slot_rect["cy"])
        await asyncio.sleep(0.85)

        has_lb = await flow.js(
            "Boolean(document.querySelector('cdk-virtual-scroll-viewport[role=\"listbox\"], [role=\"listbox\"]'))"
        )
        if not has_lb:
            last_err = f"picker listbox did not open for {slot_label!r} on attempt {attempt}"
            continue

        await flow.js("""
        (() => {
            const inp = document.querySelector('[aria-label="Tìm kiếm thành phần"]');
            if (inp && inp.value) {
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(inp, '');
                inp.dispatchEvent(new Event('input', {bubbles: true}));
            }
        })()
        """)
        await asyncio.sleep(0.25)

        found = False
        for scroll_y in range(0, 24000, 260):
            await flow.js(f"""
            (() => {{
                const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
                if (lb) lb.scrollTop = {scroll_y};
            }})()
            """)
            await asyncio.sleep(0.26)
            await _wait_visible_option_thumbnails(flow, max_polls=3)
            hit = await flow.js(f"""
            (() => {{
                const cands = {json.dumps(cand_tokens)};
                const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
                const lbRect = lb ? lb.getBoundingClientRect() : null;
                for (const el of Array.from(document.querySelectorAll('[role="option"]'))) {{
                    const src = el.querySelector('img')?.src || '';
                    if (cands.some(uid => src.includes(uid))) {{
                        if (lb && lbRect) {{
                            const er = el.getBoundingClientRect();
                            lb.scrollTop += (er.top + er.height / 2) - (lbRect.top + lbRect.height / 2);
                        }}
                        return true;
                    }}
                }}
                return false;
            }})()
            """)
            if hit:
                found = True
                break

        if not found:
            last_err = f"tokens {cand_tokens} not found in virtual scroll"
            continue

        await asyncio.sleep(0.32)
        await _wait_visible_option_thumbnails(flow, max_polls=4)

        async def recenter_and_inspect():
            scrolled = await flow.js(f"""
            (() => {{
                const cands = {json.dumps(cand_tokens)};
                const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
                const lbRect = lb ? lb.getBoundingClientRect() : null;
                const el = Array.from(document.querySelectorAll('[role="option"]')).find(
                    e => cands.some(uid => (e.querySelector('img')?.src || '').includes(uid))
                );
                if (el && lb && lbRect) {{
                    const er0 = el.getBoundingClientRect();
                    if (er0.top < lbRect.top + 28 || er0.bottom > lbRect.bottom - 28) {{
                        lb.scrollTop += (er0.top + er0.height / 2) - (lbRect.top + lbRect.height / 2);
                        return true;
                    }}
                }}
                return false;
            }})()
            """)
            if scrolled:
                await asyncio.sleep(0.28)
            return await flow.js(f"""
            (() => {{
                const cands = {json.dumps(cand_tokens)};
                const el = Array.from(document.querySelectorAll('[role="option"]')).find(
                    e => cands.some(uid => (e.querySelector('img')?.src || '').includes(uid))
                );
                let coords = null;
                let isSelected = false;
                if (el) {{
                    const r = el.getBoundingClientRect();
                    const img = el.querySelector('img');
                    const ir = img ? img.getBoundingClientRect() : null;
                    const baseX = (ir && ir.width > 10) ? ir.x : r.x;
                    coords = {{cx: Math.round(baseX + 24), cy: Math.round(r.y + r.height / 2), optWidth: Math.round(r.width)}};
                    isSelected = (
                        el.getAttribute('aria-selected') === 'true'
                        || el.classList.contains('asset-item-active')
                    );
                }}
                const addBtn = Array.from(document.querySelectorAll('button')).find(
                    b => (b.innerText || '').trim() === 'Thêm vào câu lệnh' && b.getBoundingClientRect().width > 0 && !b.disabled
                );
                let addCoords = null;
                let previewMatches = false;
                if (addBtn) {{
                    const ar = addBtn.getBoundingClientRect();
                    addCoords = {{cx: Math.round(ar.x + ar.width / 2), cy: Math.round(ar.y + ar.height / 2)}};
                    let container = addBtn.parentElement;
                    while (container && !container.querySelector('[role="option"]') && container.parentElement) {{
                        container = container.parentElement;
                    }}
                    if (container) {{
                        const pSrcs = Array.from(container.querySelectorAll('img'))
                            .filter(i => !i.closest('[role="option"]'))
                            .map(i => (i.src || '').split('?')[0]);
                        previewMatches = pSrcs.some(s => cands.some(uid => s.includes(uid)));
                    }}
                }}
                return {{coords, isSelected, hasAdd: Boolean(addBtn), addCoords, previewMatches}};
            }})()
            """)

        async def check_slot_filled() -> bool:
            return bool(await flow.js(f"""
            (() => {{
                const lbl = {json.dumps(slot_label)};
                const hasLb = Boolean(document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]'));
                if (hasLb) return false;
                const minY = Math.max(180, window.innerHeight - 340);
                const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(
                    b => !b.closest('[data-media-id]') && b.getBoundingClientRect().y > minY && b.getBoundingClientRect().width > 0
                );
                return !btns.some(b => (b.innerText || '').trim() === lbl);
            }})()
            """))

        locked = False
        for click_dx in (0, 55, 110):
            st0 = await recenter_and_inspect()
            if st0["coords"] and not (st0["previewMatches"] or st0["isSelected"]):
                max_dx = max(0, st0["coords"].get("optWidth", 180) - 48)
                dx = min(click_dx, max_dx)
                await flow.trusted_click(st0["coords"]["cx"] + dx, st0["coords"]["cy"])
                await asyncio.sleep(0.22)
                st_post = await recenter_and_inspect()
                if not (st_post["previewMatches"] or st_post["isSelected"]) and click_dx > 0:
                    await flow.js(f"""
                    (() => {{
                        const cands = {json.dumps(cand_tokens)};
                        const el = Array.from(document.querySelectorAll('[role="option"]')).find(
                            e => cands.some(uid => (e.querySelector('img')?.src || '').includes(uid))
                        );
                        if (el) el.click();
                    }})()
                    """)
                    await asyncio.sleep(0.22)

            clicked_add = False
            for poll_i in range(10):
                if await check_slot_filled():
                    locked = True
                    break
                st1 = await recenter_and_inspect()
                if st1["hasAdd"] and (st1["previewMatches"] or st1["isSelected"]):
                    if not clicked_add:
                        await flow.trusted_click(st1["addCoords"]["cx"], st1["addCoords"]["cy"])
                        clicked_add = True
                        await asyncio.sleep(0.55)
                        continue
                    elif poll_i >= 5:
                        await flow.js("""
                        (() => {
                            const b = Array.from(document.querySelectorAll('button')).find(
                                x => (x.innerText || '').trim() === 'Thêm vào câu lệnh' && x.getBoundingClientRect().width > 0 && !x.disabled
                            );
                            if (b) b.click();
                        })()
                        """)
                        await asyncio.sleep(0.55)
                        continue
                elif not clicked_add and poll_i >= 2:
                    break
                await asyncio.sleep(0.28)
            if locked:
                break
        if locked:
            print(f"  + Locked {slot_label} frame [{cand_tokens[0][:10]}] (attempt {attempt})")
            return
        last_err = f"slot {slot_label!r} did not lock on attempt {attempt}"
        await press_escape(flow, 0.8)

    raise RuntimeError(f"Failed to populate {slot_label!r} slot for {cand_tokens}: {last_err}")


async def run_videos_pipeline(
    config: Dict[str, Any],
    project_dir: str,
    phase: str = "all",
    start_index: int = 0,
    only_key: str = "",
    port: Optional[int] = None,
) -> None:
    """Stage 3: Render 4-second Veo 3.1 - Fast 16:9 clips (supports 1-Frame Parallax & 2-Frame Start+End)."""
    errs = validate_sku_config(config, project_dir=project_dir, require_local_plates=False)
    if errs:
        raise ValueError("SKU config failed pre-flight validation:\n  - " + "\n  - ".join(errs))

    slug = config["slug"]
    qa_dir = os.path.join(project_dir, "qa")
    uuids_path = os.path.join(project_dir, f"{slug}_scene_uuids.json")
    scene_uuids: Dict[str, str] = {}
    if os.path.isfile(uuids_path):
        with open(uuids_path, "r", encoding="utf-8") as f:
            scene_uuids = json.load(f)

    videos = list(config.get("videos", []))
    if phase == "only":
        only_tokens = [tok.strip() for tok in (only_key or "").split(",") if tok.strip()]
        videos = [
            v for v in videos
            if only_tokens and any(tok in v["key"] or tok in v.get("scene_key", "") for tok in only_tokens)
        ]
        if not videos:
            raise ValueError(f"No video matching --only-key={only_key!r}")
    elif phase == "slice":
        videos = videos[start_index:]

    if phase != "qa-only" and not videos:
        print(f"No remaining videos to render for phase={phase!r}.")
        return

    ws_url = get_project_ws_url(config["project_id"], port=port, auto_open=True)
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws, project_id=config["project_id"])
        if phase == "qa-only":
            await capture_qa_pages(flow, qa_dir, f"{slug}_veo", "Video")
            return

        # Bridge permanent 36-char UUIDs -> post-reload '/asb/ANqvLO...' picker tokens before queueing clips
        uuid_to_asb, _ = await build_gallery_media_bridge(flow, max_steps=65)

        for w_i in range(0, len(videos), 2):
            wave = videos[w_i:w_i + 2]
            for item in wave:
                start_tok = item.get("uuid") or scene_uuids.get(item.get("scene_key", ""), "")
                if not start_tok:
                    raise RuntimeError(f"Missing start UUID for video {item['key']} in {uuids_path}")
                end_tok = item.get("end_uuid") or (
                    scene_uuids.get(item["end_scene_key"], "") if item.get("end_scene_key") else ""
                )

                start_alts = [uuid_to_asb[start_tok]] if start_tok in uuid_to_asb else []
                end_alts = [uuid_to_asb[end_tok]] if end_tok and end_tok in uuid_to_asb else []

                print(f"\n=== QUEUEING 4S VEO 3.1 CLIP: {item['key']} ===")
                await ensure_veo31_fast_4s_16x9(flow)
                await clear_frame_slots_and_text(flow)
                await _populate_frame_slot_by_token(flow, "Bắt đầu", start_tok, alt_tokens=start_alts)
                if end_tok:
                    await _populate_frame_slot_by_token(flow, "Kết thúc", end_tok, alt_tokens=end_alts)

                ed_rect = await flow.js("""
                (() => {
                    const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
                    const r = el.getBoundingClientRect();
                    return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
                })()
                """)
                await flow.trusted_click(ed_rect["cx"], ed_rect["cy"])
                await asyncio.sleep(0.15)
                await flow.call("Input.insertText", {"text": item["prompt"]})
                await asyncio.sleep(0.4)

                btns = await flow.js("""
                Array.from(document.querySelectorAll('[aria-label="Bắt đầu tạo"]')).map(el => {
                    const r = el.getBoundingClientRect();
                    const cx = Math.round(r.x + r.width / 2);
                    const cy = Math.round(r.y + r.height / 2);
                    const topEl = document.elementFromPoint(cx, cy);
                    const hit = Boolean(topEl && (el === topEl || el.contains(topEl)));
                    return {cx, cy, hit, disabled: el.disabled};
                })
                """)
                target = next((b for b in btns if b["hit"] and not b["disabled"]), None)
                if target:
                    await flow.trusted_click(target["cx"], target["cy"])
                else:
                    await flow.find_and_trusted_click("aria === 'Bắt đầu tạo' && !el.disabled", f"submit {item['key']}")

                for _ in range(18):
                    await asyncio.sleep(0.5)
                    reset_done = await flow.js("""
                    (() => {
                        const minY = Math.max(180, window.innerHeight - 340);
                        return Array.from(document.querySelectorAll('button, [role="button"]'))
                            .filter(b => b.getBoundingClientRect().y > minY && b.getBoundingClientRect().width > 0)
                            .some(b => (b.innerText || '').trim() === 'Bắt đầu');
                    })()
                    """)
                    if reset_done:
                        break
                await asyncio.sleep(2.4)

            wave_label = f"{slug} Veo Wave {w_i // 2 + 1} ({len(wave)} clips)"
            print(f"  Waiting for {wave_label}...")
            saw_pct = False
            zero_streak = 0
            for step in range(65):
                await asyncio.sleep(3.0)
                await flow.js("""
                (() => {
                    const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
                    if (sc) sc.scrollTop = 0;
                    window.scrollTo(0, 0);
                })()
                """)
                if await _click_retry_if_failed_card(flow, wave_label):
                    saw_pct = True
                    zero_streak = 0
                    continue
                pcts = await flow.js("""
                Array.from(document.querySelectorAll('div, span'))
                    .map(e => (e.innerText || '').trim())
                    .filter(t => /^\\d+%$/.test(t))
                """)
                if pcts:
                    saw_pct = True
                    zero_streak = 0
                elif saw_pct or step >= 5:
                    zero_streak += 1
                if zero_streak >= 2:
                    print(f"  Completed {wave_label}!")
                    break

        await asyncio.sleep(3.5)
        await capture_qa_pages(flow, qa_dir, f"{slug}_veo", "Video")


def _probe_video(path: str) -> Dict[str, Any]:
    res = subprocess.run(
        [
            FFPROBE, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration,r_frame_rate",
            "-of", "json", path,
        ],
        capture_output=True, text=True, check=True,
    )
    return json.loads(res.stdout)["streams"][0]


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


async def _index_gallery_tiles_responsive(flow: FlowCDP, max_needed_idx: int) -> List[Dict[str, Any]]:
    """
    Walk '.cdk-virtual-scrollable.page-container' from scrollTop=0 downward and index unique
    '<flow-grid-tile-container>' cards in reading order (rowTop, colLeft).
    Works across any window width, column count (1..4), sidebar state, or mixed row heights.
    """
    await flow.js("""
    (() => {
        const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
        if (sc) sc.scrollTop = 0;
    })()
    """)
    await asyncio.sleep(0.45)

    tiles_by_key: Dict[str, Dict[str, Any]] = {}
    max_steps = max(18, (max_needed_idx // 2) + 14)
    for _ in range(max_steps):
        batch = await flow.js("""
        (() => {
            const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
            if (!sc) return {sy: 0, items: []};
            const sr = sc.getBoundingClientRect();
            const rawTiles = Array.from(document.querySelectorAll('flow-grid-tile-container'));
            const items = rawTiles.map(el => {
                const r = el.getBoundingClientRect();
                if (r.width < 160 || r.height < 100) return null;
                const m = el.querySelector('video, img');
                const docTop = Math.round(r.top - sr.top + sc.scrollTop);
                const docLeft = Math.round(r.left - sr.left);
                const mid = (m?.getAttribute('data-media-id') || '').trim();
                const posKey = (Math.round(docTop / 24) * 24) + ':' + (Math.round(docLeft / 24) * 24);
                return {key: mid || posKey, mid, docTop, docLeft, w: Math.round(r.width), h: Math.round(r.height)};
            }).filter(Boolean);
            return {sy: sc.scrollTop, items};
        })()
        """)
        for it in batch.get("items") or []:
            k = it["key"]
            if k not in tiles_by_key:
                tiles_by_key[k] = it

        sorted_now = sorted(tiles_by_key.values(), key=lambda t: (round(t["docTop"] / 24), t["docLeft"]))
        if len(sorted_now) > max_needed_idx + 2 and (batch.get("sy") or 0) > sorted_now[max_needed_idx]["docTop"] + 320:
            break

        moved = await flow.js("""
        (() => {
            const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
            if (!sc) return false;
            const prev = sc.scrollTop;
            sc.scrollTop += 520;
            return sc.scrollTop > prev;
        })()
        """)
        if not moved:
            break
        await asyncio.sleep(0.28)

    return sorted(tiles_by_key.values(), key=lambda t: (round(t["docTop"] / 24), t["docLeft"]))


async def _scroll_to_indexed_tile(flow: FlowCDP, tile_meta: Dict[str, Any]) -> Optional[Dict[str, int]]:
    """Scroll target indexed tile into clear viewport range and return its live bounding box."""
    target_sy = max(0, int(tile_meta["docTop"]) - 130)
    await flow.js(f"""
    (() => {{
        const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
        if (sc) sc.scrollTop = {target_sy};
    }})()
    """)
    await asyncio.sleep(0.55)
    return await flow.js(f"""
    (() => {{
        const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
        if (!sc) return null;
        const sr = sc.getBoundingClientRect();
        const targetMid = {json.dumps(tile_meta.get("mid") or "")};
        const expTop = {int(tile_meta["docTop"])};
        const expLeft = {int(tile_meta["docLeft"])};

        let best = null;
        let bestDist = 1e9;
        for (const el of Array.from(document.querySelectorAll('flow-grid-tile-container'))) {{
            const r = el.getBoundingClientRect();
            if (r.width < 160 || r.height < 100) continue;
            const m = el.querySelector('video, img');
            const mid = (m?.getAttribute('data-media-id') || '').trim();
            const docTop = Math.round(r.top - sr.top + sc.scrollTop);
            const docLeft = Math.round(r.left - sr.left);
            if (targetMid && mid === targetMid) {{
                best = m || el;
                bestDist = 0;
                break;
            }}
            const dist = Math.abs(docTop - expTop) + Math.abs(docLeft - expLeft);
            if (dist < 75 && dist < bestDist) {{
                best = m || el;
                bestDist = dist;
            }}
        }}
        if (!best) return null;
        const r = best.getBoundingClientRect();
        if (r.bottom < 70 || r.top > window.innerHeight - 90) return null;
        return {{
            x: Math.round(r.x),
            y: Math.round(r.y),
            w: Math.round(r.width),
            h: Math.round(r.height),
            cx: Math.round(r.x + r.width / 2),
            cy: Math.round(r.y + Math.min(r.height / 2, 110)),
        }};
    }})()
    """)


async def resolve_video_card_indices_by_start_frame(
    config: Dict[str, Any],
    project_dir: str,
    port: Optional[int] = None,
    max_match_l1: float = 24.0,
) -> List[Tuple[int, str]]:
    """
    Automatically resolve live Video-tab card indices (0..M-1) to config 'videos' entries
    by matching each Video-tab card's t=0.0s/0.1s start-frame thumbnail against the locked
    scene UUID images on the 'Hình ảnh' tab. Prevents single-clip ('--phase only') re-renders
    from shifting positional card indices during 1080p batch export.
    """
    slug = config["slug"]
    project_id = config["project_id"]
    videos = list(config.get("videos", []))
    if not videos:
        raise ValueError("No videos defined in SKU config.")

    uuid_path = os.path.join(project_dir, f"{slug}_scene_uuids.json")
    scene_uuid_map: Dict[str, str] = {}
    if os.path.isfile(uuid_path):
        with open(uuid_path, "r", encoding="utf-8") as f:
            scene_uuid_map = json.load(f)

    target_uuid_by_vidx: Dict[int, str] = {}
    needed_uuids: Set[str] = set()
    for i, v in enumerate(videos):
        u = (v.get("uuid") or "").strip() or (scene_uuid_map.get(v.get("scene_key", "")) or "").strip()
        if not u:
            raise RuntimeError(
                f"Cannot auto-resolve Video-tab card order: video {v.get('key')!r} has no locked scene UUID in {uuid_path}."
            )
        target_uuid_by_vidx[i] = u
        needed_uuids.add(u)

    def _mean_l1(im1: Image.Image, im2: Image.Image) -> float:
        return sum(ImageStat.Stat(ImageChops.difference(im1, im2)).mean) / 3.0

    ws_url = get_project_ws_url(project_id, port=port, auto_open=True)
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws, project_id=project_id)
        await exit_edit_view_if_needed(flow)
        await press_escape(flow, 0.25)

        # 1. Extract 160x90 RGB templates for all target scene UUIDs from the 'Hình ảnh' tab
        await switch_gallery_tab(flow, "Hình ảnh")
        await flow.js("""
        (() => {
            const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
            if (sc) sc.scrollTop = 0;
        })()
        """)
        await asyncio.sleep(0.35)

        uuid_thumbs: Dict[str, Image.Image] = {}
        wanted_list = list(needed_uuids)
        for _ in range(65):
            rows = await flow.js(f"""
            (() => {{
                const wanted = new Set({json.dumps(wanted_list)});
                const out = [];
                for (const img of Array.from(document.querySelectorAll('img[data-media-id]'))) {{
                    const mid = (img.getAttribute('data-media-id') || '').trim();
                    if (!wanted.has(mid) || !img.complete || img.naturalWidth < 64) continue;
                    try {{
                        const c = document.createElement('canvas');
                        c.width = 160;
                        c.height = 90;
                        c.getContext('2d').drawImage(img, 0, 0, 160, 90);
                        out.push({{mid, du: c.toDataURL('image/jpeg', 0.90)}});
                    }} catch (e) {{}}
                }}
                return out;
            }})()
            """)
            for row in rows or []:
                mid = row["mid"]
                if mid not in uuid_thumbs and (row.get("du") or "").startswith("data:image/"):
                    b64 = row["du"].split(",", 1)[1]
                    uuid_thumbs[mid] = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
            if len(uuid_thumbs) >= len(needed_uuids):
                break
            moved = await flow.js("""
            (() => {
                const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
                if (!sc) return false;
                const p = sc.scrollTop;
                sc.scrollTop += 480;
                return sc.scrollTop > p;
            })()
            """)
            if not moved:
                break
            await asyncio.sleep(0.22)

        if len(uuid_thumbs) < len(needed_uuids):
            missing_u = sorted(needed_uuids - set(uuid_thumbs.keys()))
            raise RuntimeError(f"Could not locate {len(missing_u)} scene image(s) on 'Hình ảnh' tab: {missing_u[:5]}")

        # 2. Scan top Video-tab cards and capture each card's clean t=0.0s/0.08s start frame
        await switch_gallery_tab(flow, "Video")
        await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 16, "y": 240})
        scan_limit = len(videos) + 8
        tiles = await _index_gallery_tiles_responsive(flow, scan_limit)
        card_thumbs: List[Tuple[int, Image.Image]] = []

        for card_idx in range(min(scan_limit, len(tiles))):
            tm = tiles[card_idx]
            target_sy = max(0, int(tm["docTop"]) - 105)
            await flow.js(f"""
            (() => {{
                const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
                if (sc) sc.scrollTop = {target_sy};
            }})()
            """)
            await asyncio.sleep(0.24)
            clip_info = await flow.js(f"""
            (async () => {{
                const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
                if (!sc) return null;
                const sr = sc.getBoundingClientRect();
                let best = null, bestD = 1e9;
                for (const el of Array.from(document.querySelectorAll('flow-grid-tile-container'))) {{
                    const r = el.getBoundingClientRect();
                    if (r.width < 140 || r.height < 90) continue;
                    const dt = Math.round(r.top - sr.top + sc.scrollTop);
                    const dl = Math.round(r.left - sr.left);
                    const d = Math.abs(dt - {int(tm["docTop"])}) + Math.abs(dl - {int(tm["docLeft"])});
                    if (d < 80 && d < bestD) {{ best = el; bestD = d; }}
                }}
                if (!best) return null;
                const txt = (best.innerText || '').trim();
                if (txt.includes('Không thành công')) return null;
                const v = best.querySelector('video');
                if (v && (v.currentSrc || v.src) && v.readyState >= 2 && v.currentTime > 0.25) {{
                    v.pause();
                    await new Promise((resolve) => {{
                        let done = false;
                        const fin = () => {{ if (!done) {{ done = true; resolve(); }} }};
                        v.addEventListener('seeked', fin, {{once: true}});
                        setTimeout(fin, 600);
                        v.currentTime = 0.08;
                    }});
                    await new Promise(r => setTimeout(r, 40));
                }}
                best.setAttribute('data-resolve-tile', '1');
                for (const ch of Array.from(best.querySelectorAll('button, [role="button"]'))) {{
                    ch.setAttribute('data-prev-vis-r', ch.style.visibility || '');
                    ch.style.visibility = 'hidden';
                }}
                for (const ov of Array.from(document.querySelectorAll('.cdk-overlay-container, mat-snack-bar-container'))) {{
                    ov.setAttribute('data-prev-vis-ov', ov.style.visibility || '');
                    ov.style.visibility = 'hidden';
                }}
                const ed = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
                if (ed) {{
                    let comp = ed.parentElement;
                    while (comp && comp.parentElement && !comp.contains(sc) && comp.getBoundingClientRect().height < 340) {{
                        comp = comp.parentElement;
                    }}
                    if (comp && !comp.contains(sc)) {{
                        comp.setAttribute('data-prev-vis-ov', comp.style.visibility || '');
                        comp.style.visibility = 'hidden';
                    }}
                }}
                const r = best.getBoundingClientRect();
                return {{x: Math.round(r.x) + 4, y: Math.round(r.y) + 4, width: Math.round(r.width) - 8, height: Math.round(r.height) - 8, scale: 1}};
            }})()
            """)
            if not clip_info:
                continue
            try:
                shot = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 86, "clip": clip_info})
                im = Image.open(io.BytesIO(base64.b64decode(shot["data"]))).convert("RGB").resize((160, 90), Image.Resampling.BILINEAR)
                card_thumbs.append((card_idx, im))
            finally:
                await flow.js("""
                (() => {
                    const t = document.querySelector('[data-resolve-tile="1"]');
                    if (t) {
                        for (const ch of Array.from(t.querySelectorAll('[data-prev-vis-r]'))) {
                            ch.style.visibility = ch.getAttribute('data-prev-vis-r') || '';
                            ch.removeAttribute('data-prev-vis-r');
                        }
                        t.removeAttribute('data-resolve-tile');
                    }
                    for (const ov of Array.from(document.querySelectorAll('[data-prev-vis-ov]'))) {
                        ov.style.visibility = ov.getAttribute('data-prev-vis-ov') || '';
                        ov.removeAttribute('data-prev-vis-ov');
                    }
                })()
                """)

        await flow.js("""
        (() => {
            const sc = document.querySelector('.cdk-virtual-scrollable.page-container');
            if (sc) sc.scrollTop = 0;
        })()
        """)

    # 3. Assign newest matching Video-tab card (lowest card_idx) to each video entry without collisions
    used_cards: Set[int] = set()
    resolved_pairs: List[Tuple[int, str]] = []
    for i, v in enumerate(videos):
        u = target_uuid_by_vidx[i]
        ref_thumb = uuid_thumbs[u]
        candidates = [
            (cidx, _mean_l1(cth, ref_thumb))
            for cidx, cth in card_thumbs
            if cidx not in used_cards
        ]
        if not candidates:
            raise RuntimeError(f"Ran out of Video-tab cards while matching {v['key']!r}.")
        best_cidx, best_l1 = min(candidates, key=lambda kv: (kv[1], kv[0]))
        if best_l1 > max_match_l1:
            raise RuntimeError(
                f"Could not match video {v['key']!r} (UUID {u}) to any Video-tab card (closest card #{best_cidx} had L1={best_l1:.2f} > {max_match_l1})."
            )
        used_cards.add(best_cidx)
        resolved_pairs.append((best_cidx, f"{i + 1:02d}_{v['key']}"))
        print(f"  [Auto-Match] {i + 1:02d}_{v['key']:36s} -> Video card #{best_cidx:02d} (L1={best_l1:.2f})")

    return resolved_pairs


async def download_and_merge_1080p_pipeline(
    project_id: str,
    card_index_to_slug: Sequence[Tuple[int, str]],
    target_dir: str,
    master_filename: str = "MASTER_1080p.mp4",
    port: Optional[int] = None,
) -> str:
    """
    Stage 4: Silently hover Video-tab cards -> Tuỳ chọn khác -> Tải xuống -> 1080p,
    verify 1920x1080 via ffprobe + SHA-256 dedupe, and merge into +faststart 1080p master MP4.
    """
    if not card_index_to_slug:
        raise ValueError("card_index_to_slug must contain at least one (card_index, slug) pair.")

    clips_dir = os.path.join(target_dir, "clips_1080p")
    dl_tmp = os.path.join(target_dir, "_dl_1080p_tmp")
    master_mp4 = os.path.join(target_dir, master_filename)
    os.makedirs(clips_dir, exist_ok=True)
    os.makedirs(dl_tmp, exist_ok=True)

    seen_hashes: Set[str] = set()
    for existing in sorted(glob.glob(os.path.join(clips_dir, "*.mp4"))):
        try:
            inf = _probe_video(existing)
            if int(inf["width"]) >= 1900 and int(inf["height"]) >= 1060:
                seen_hashes.add(_sha256_file(existing))
        except Exception:
            pass

    ordered_clip_paths: List[str] = []
    pending_downloads: List[Tuple[int, str, str]] = []
    for card_idx, slug in card_index_to_slug:
        out_mp4 = os.path.join(clips_dir, f"{slug}_1080p.mp4")
        ordered_clip_paths.append(out_mp4)
        if os.path.exists(out_mp4):
            try:
                inf = _probe_video(out_mp4)
                if int(inf["width"]) >= 1900 and int(inf["height"]) >= 1060:
                    print(f"Skipping already verified 1080p clip: {os.path.basename(out_mp4)}")
                    continue
            except Exception:
                os.remove(out_mp4)
        pending_downloads.append((card_idx, slug, out_mp4))

    if pending_downloads:
        max_card_idx = max(idx for idx, _, _ in pending_downloads)
        ws_url = get_project_ws_url(project_id, port=port, auto_open=True)
        async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
            flow = await init_silent_flow_session(ws, project_id=project_id)
            try:
                await flow.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": dl_tmp, "eventsEnabled": True})
            except Exception:
                await flow.call("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": dl_tmp})

            await switch_gallery_tab(flow, "Video")
            indexed_tiles = await _index_gallery_tiles_responsive(flow, max_card_idx)
            if len(indexed_tiles) <= max_card_idx:
                raise RuntimeError(
                    f"Requested Video-tab card #{max_card_idx}, but only {len(indexed_tiles)} video tile(s) exist in project {project_id}."
                )

            for card_idx, slug, out_mp4 in pending_downloads:
                print(f"[{slug}] Downloading Video-tab card #{card_idx} in native 1080p...")
                saved = False
                for attempt in range(1, 4):
                    for stale in glob.glob(os.path.join(dl_tmp, "*")):
                        try:
                            os.remove(stale)
                        except OSError:
                            pass

                    await press_escape(flow, 0.3)
                    await flow.js("""
                    (() => {
                        const b = Array.from(document.querySelectorAll('button')).find(el => (el.innerText || '').trim() === 'Đóng');
                        if (b) b.click();
                    })()
                    """)

                    if card_idx >= len(indexed_tiles):
                        await switch_gallery_tab(flow, "Video")
                        indexed_tiles = await _index_gallery_tiles_responsive(flow, max_card_idx)
                        if card_idx >= len(indexed_tiles):
                            continue

                    card = await _scroll_to_indexed_tile(flow, indexed_tiles[card_idx])
                    if not card:
                        await switch_gallery_tab(flow, "Video")
                        indexed_tiles = await _index_gallery_tiles_responsive(flow, max_card_idx)
                        continue

                    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 40, "y": 240})
                    await asyncio.sleep(0.2)
                    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": card["cx"], "y": card["cy"]})
                    await asyncio.sleep(0.65)

                    more_btn = await flow.js(f"""
                    (() => {{
                        const btns = Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]'))
                            .map(b => {{
                                const r = b.getBoundingClientRect();
                                return {{cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2), x: r.x, y: r.y, w: r.width}};
                            }})
                            .filter(b => b.w > 0 && b.x >= {card['x'] - 24} && b.x <= {card['x'] + card['w'] + 24} && b.y >= {card['y'] - 24} && b.y <= {card['y'] + card['h'] + 24});
                        return btns[0] || null;
                    }})()
                    """)
                    if not more_btn:
                        continue
                    await flow.trusted_click(more_btn["cx"], more_btn["cy"])
                    await asyncio.sleep(0.55)

                    dl_item = await flow.js("""
                    (() => {
                        const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('Tải xuống'));
                        if (!m) return null;
                        const r = m.getBoundingClientRect();
                        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
                    })()
                    """)
                    if not dl_item:
                        continue
                    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": dl_item["cx"], "y": dl_item["cy"]})
                    await asyncio.sleep(0.75)

                    rect_1080 = await flow.js("""
                    (() => {
                        const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('1080p'));
                        if (!m) return null;
                        const r = m.getBoundingClientRect();
                        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
                    })()
                    """)
                    if not rect_1080:
                        continue
                    await flow.trusted_click(rect_1080["cx"], rect_1080["cy"])

                    for _ in range(85):
                        await asyncio.sleep(1.0)
                        files = glob.glob(os.path.join(dl_tmp, "*"))
                        mp4s = [f for f in files if f.endswith(".mp4") and not f.endswith(".crdownload") and os.path.getsize(f) > 200_000]
                        crs = [f for f in files if f.endswith(".crdownload")]
                        if mp4s and not crs:
                            cand = mp4s[0]
                            h = _sha256_file(cand)
                            if h in seen_hashes:
                                os.remove(cand)
                                continue
                            inf = _probe_video(cand)
                            if int(inf["width"]) < 1900 or int(inf["height"]) < 1060:
                                os.remove(cand)
                                break
                            seen_hashes.add(h)
                            shutil.move(cand, out_mp4)
                            print(f"  Saved {os.path.basename(out_mp4)} ({inf['width']}x{inf['height']})")
                            saved = True
                            break
                    if saved:
                        break
                if not saved:
                    raise RuntimeError(f"Failed to download 1080p clip for card #{card_idx} ({slug})")

    concat_txt = os.path.join(dl_tmp, "concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in ordered_clip_paths:
            esc = p.replace("'", "'\\''")
            f.write(f"file '{esc}'\n")

    res = subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", "-movflags", "+faststart", master_mp4],
        capture_output=True, text=True,
    )
    if res.returncode != 0 or not os.path.exists(master_mp4):
        subprocess.run(
            [
                FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
                "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", master_mp4,
            ],
            check=True, capture_output=True,
        )
    shutil.rmtree(dl_tmp, ignore_errors=True)
    print(f"Merged 1080p master MP4 -> {master_mp4}")
    return master_mp4
