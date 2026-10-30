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
import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import websockets

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOW_WEB_INTRO_DIR = os.path.join(REPO_ROOT, "flow_web_intro")
if FLOW_WEB_INTRO_DIR not in sys.path:
    sys.path.insert(0, FLOW_WEB_INTRO_DIR)

from gen_batch_images import FlowCDP  # noqa: E402
from home_helper import discover_cdp_http_url  # noqa: E402
from review_fix_keyframes_step1 import clear_composer_strict  # noqa: E402

from .guardrails import validate_sku_config  # noqa: E402
from .presets import get_preset  # noqa: E402

FFMPEG = "/opt/homebrew/bin/ffmpeg" if os.path.exists("/opt/homebrew/bin/ffmpeg") else "ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe" if os.path.exists("/opt/homebrew/bin/ffprobe") else "ffprobe"


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
    """Find (or silently open) the Google Flow project tab WebSocket debugger URL."""
    base = resolve_cdp_base_url(port=port, cdp_url=cdp_url)
    with urllib.request.urlopen(f"{base}/json/list", timeout=4.0) as resp:
        tabs = json.loads(resp.read().decode("utf-8"))

    for tab in tabs:
        if tab.get("type") == "page" and project_id in (tab.get("url") or ""):
            return tab["webSocketDebuggerUrl"]

    if auto_open:
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


async def init_silent_flow_session(ws) -> FlowCDP:
    """Initialize FlowCDP with silent background focus emulation (zero window focus stealing)."""
    flow = FlowCDP(ws)
    await flow.call("Page.enable")
    await flow.call("DOM.enable")
    await flow.call("Emulation.setFocusEmulationEnabled", {"enabled": True})
    return flow


async def press_escape(flow: FlowCDP, wait_s: float = 0.3) -> None:
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(wait_s)


async def exit_edit_view_if_needed(flow: FlowCDP) -> None:
    href = await flow.js("window.location.href")
    if "/edit/" in (href or ""):
        await flow.find_and_trusted_click("aria === 'Nút quay lại để quay về trang trước'", "exit /edit/ view")
        await asyncio.sleep(1.0)


async def disable_agent_mode_if_active(flow: FlowCDP) -> None:
    """Turn OFF Flow's post-reload 'Tác nhân' mode so manual Nano Banana / Veo controls appear."""
    if await flow.js("Boolean(document.querySelector('[aria-label=\"Chỉ dẫn cho tác nhân\"]'))"):
        await flow.find_and_trusted_click("text === 'Tác nhân' && r.y > 760 && r.y < 940", "toggle OFF Tác nhân")
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
            return r.width > 0 && r.x < 280 && r.y > 60 && r.y < 260 && txt.includes(label);
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
        return r.width > 0 && r.y > 480 && r.y < 820 && (b.innerText || '').includes('Nano Banana Pro');
    })
    """)
    if not already_pro:
        await flow.find_and_trusted_click(
            "(text.includes('Nano Banana') || text.includes('Imagen')) && r.y > 480 && r.y < 820",
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
        return r.y > 660 && r.width > 0 && (txt.includes('Bắt đầu') || txt.includes('Kết thúc') || (b.getAttribute('aria-label')||'').includes('Hoán đổi khung hình'));
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
                return r.width > 0 && r.y > 480 && r.y < 820 && (b.innerText || '').includes('Veo');
            });
        return (el?.innerText || '').trim();
    })()
    """)
    if "Veo 3.1 - Fast" not in model_txt:
        await flow.find_and_trusted_click("(aria === 'Chọn nhóm mô hình' || text.includes('Veo')) && r.y > 480 && r.y < 820", "model dropdown")
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


async def open_ingredient_modal(flow: FlowCDP) -> None:
    if not await flow.js("document.querySelectorAll('[role=\"option\"]').length > 0"):
        await flow.find_and_trusted_click("aria === 'Thêm thành phần vào ô nhập câu lệnh'", "open '+' modal")
        await asyncio.sleep(0.85)


async def scan_all_project_options(flow: FlowCDP, max_steps: int = 22) -> List[Dict[str, str]]:
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
    seen: Set[str] = set()
    for _ in range(max_steps):
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
            if tok and tok not in seen:
                seen.add(tok)
                ordered.append(it)
        moved = await flow.js("""
        (() => {
            const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
            if (!vp) return false;
            const prev = vp.scrollTop;
            vp.scrollTop += 280;
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
    existing_opts = await scan_all_project_options(flow, max_steps=18)
    await press_escape(flow, 0.3)

    missing: List[Tuple[str, str]] = []
    for fname, fpath in file_entries:
        stem = os.path.splitext(fname)[0]
        known_u = uuid_cache.get(fname, "")
        hit = next(
            (it["token"] for it in existing_opts if (known_u and known_u in it["src"]) or (stem in it["txt"])),
            None,
        )
        if hit:
            uuid_cache[fname] = hit[:48]
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
    refreshed = await scan_all_project_options(flow, max_steps=18)
    await press_escape(flow, 0.3)
    for fname, _ in missing:
        stem = os.path.splitext(fname)[0]
        hit = next((it["token"] for it in refreshed if stem in it["txt"]), None)
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
    """Attach 1 ingredient in '+' modal, verifying chip count increments by +1."""
    stem = os.path.splitext(filename)[0]
    known_uuid = uuid_cache.get(filename, "")
    await open_ingredient_modal(flow)

    await flow.js("""
    (() => {
        const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
        if (vp) vp.scrollTop = 0;
    })()
    """)
    await asyncio.sleep(0.3)

    hit = False
    for _ in range(35):
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
                        token: src.split('?')[0].split('/').pop().split('=')[0],
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
    if not st["targetOpt"] or not st["targetOpt"]["token"]:
        raise RuntimeError(f"Ingredient {filename!r} matched but token empty: {st}")

    target_core = st["targetOpt"]["token"][:48]
    uuid_cache[filename] = target_core
    if uuid_cache_path:
        with open(uuid_cache_path, "w", encoding="utf-8") as f:
            json.dump(uuid_cache, f, indent=2)

    is_previewed = any(target_core in u for u in st["previewSrcs"]) and st["hasAddBtn"]
    if not is_previewed:
        for dx in (0, 55, 105):
            st_cur = await inspect_dialog()
            if not st_cur["targetOpt"]:
                break
            await flow.trusted_click(st_cur["targetOpt"]["cx"] + dx, st_cur["targetOpt"]["cy"])
            for _ in range(7):
                await asyncio.sleep(0.3)
                st2 = await inspect_dialog()
                if any(target_core in u for u in st2["previewSrcs"]) and st2["hasAddBtn"]:
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


async def get_rendered_gallery_urls(flow: FlowCDP) -> List[str]:
    imgs = await flow.js("""
    Array.from(document.querySelectorAll('img'))
        .filter(i => !i.closest('button[aria-label="Thành phần"]') && !i.closest('[role="option"]'))
        .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth, top: i.getBoundingClientRect().top}))
        .filter(i => (i.src.includes('flow-content.google/image/') || i.src.includes('/asb/') || i.src.includes('googleusercontent.com/')) && i.nw >= 512)
        .sort((a, b) => a.top - b.top)
    """)
    return [im["src"] for im in imgs]


async def _click_retry_if_failed_card(flow: FlowCDP, label: str) -> bool:
    has_fail = await flow.js("(document.body.innerText || '').includes('Không thành công')")
    if not has_fail:
        return False
    retry_btn = await flow.js("""
    (() => {
        const cards = Array.from(document.querySelectorAll('div')).filter(d => {
            const r = d.getBoundingClientRect();
            return r.width > 300 && r.width < 560 && r.height > 180 && r.height < 420 && (d.innerText || '').includes('Không thành công');
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
    and save the clean 1024x1024 JPG locally for build-plates.
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
            uuid_cache = json.load(f)

    ws_url = get_project_ws_url(project_id, port=port, auto_open=True)
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws)
        await switch_gallery_tab(flow, "Hình ảnh")
        await ensure_image_mode(flow, aspect_ratio="1:1")
        await upload_missing_files_silent(flow, ws, [(fname, os.path.abspath(input_image_path))], uuid_cache, tmp_cache_path)

        await clear_composer_strict(flow)
        before_urls = {u.split("?")[0].split("=")[0] for u in await get_rendered_gallery_urls(flow)}
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

        new_full_url = ""
        for step in range(50):
            await asyncio.sleep(2.0)
            await _click_retry_if_failed_card(flow, "white-isolation")
            cur_urls = await get_rendered_gallery_urls(flow)
            for u in cur_urls:
                base_u = u.split("?")[0].split("=")[0]
                if base_u not in before_urls:
                    new_full_url = u
                    break
            pcts = await flow.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            if new_full_url and not pcts and step >= 5:
                break

        if not new_full_url:
            raise RuntimeError("Timed out waiting for 1:1 white-background isolation render on Google Flow.")

        b64_data = await flow.js(f"""
        (async () => {{
            const resp = await fetch({json.dumps(new_full_url)}, {{credentials: 'include'}});
            const buf = await resp.arrayBuffer();
            let binary = '';
            const bytes = new Uint8Array(buf);
            const chunk = 0x8000;
            for (let i = 0; i < bytes.length; i += chunk) {{
                binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
            }}
            return btoa(binary);
        }})()
        """)
        with open(output_white_path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        print(f"Saved clean white-background SKU master -> {output_white_path}")
    return output_white_path


async def submit_single_image_scene(
    flow: FlowCDP,
    scene: Dict[str, Any],
    uuid_cache: Dict[str, str],
    uuid_cache_path: str,
    wait_for_render: bool = True,
) -> None:
    print(f"\n=== SUBMITTING IMAGE SCENE: {scene['key']} ===")
    await press_escape(flow, 0.25)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
    await asyncio.sleep(0.25)
    await ensure_image_mode(flow, aspect_ratio="16:9")
    await clear_composer_strict(flow)

    before_bases = {u.split("?")[0].split("=")[0] for u in await get_rendered_gallery_urls(flow)}
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
        return

    saw_pct = False
    for step in range(52):
        await asyncio.sleep(2.0)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
        if await _click_retry_if_failed_card(flow, scene["key"]):
            continue
        pcts = await flow.js("""
        Array.from(document.querySelectorAll('div, span'))
            .map(e => (e.innerText || '').trim())
            .filter(t => /^\\d+%$/.test(t))
        """)
        if pcts:
            saw_pct = True
        cur_bases = {u.split("?")[0].split("=")[0] for u in await get_rendered_gallery_urls(flow)}
        if not pcts and (saw_pct or step >= 7) and len(cur_bases - before_bases) >= 1:
            print(f"  Rendered {scene['key']} in {(step + 1) * 2}s!")
            return
    print(f"  Warning: timeout waiting for {scene['key']}, continuing...")


async def capture_qa_pages(flow: FlowCDP, qa_dir: str, prefix: str, tab_label: str) -> None:
    os.makedirs(qa_dir, exist_ok=True)
    await switch_gallery_tab(flow, tab_label)
    for idx, sy in enumerate((0, 540, 1080, 1620)):
        await flow.js(f"""
        (() => {{
            const scrollers = Array.from(document.querySelectorAll('div, main')).filter(el => el.scrollHeight > el.clientHeight + 200);
            for (const s of scrollers) s.scrollTop = {sy};
            window.scrollTo(0, {sy});
        }})()
        """)
        await asyncio.sleep(0.9)
        res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 86})
        out_p = os.path.join(qa_dir, f"qa_{prefix}_page{idx + 1}.jpg")
        with open(out_p, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("Saved local QA screenshot:", out_p)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")


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
        scenes = [s for s in scenes if only_key and only_key in s["key"]]
        if not scenes:
            raise ValueError(f"No scene matching --only-key={only_key!r}")
    elif phase == "check1":
        scenes = scenes[:1]
    elif phase == "rest":
        scenes = scenes[1:]
    elif phase == "slice":
        scenes = scenes[start_index:]

    # Collect unique required files across active scenes
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
        flow = await init_silent_flow_session(ws)
        await switch_gallery_tab(flow, "Hình ảnh")
        await ensure_image_mode(flow, aspect_ratio="16:9")
        await upload_missing_files_silent(flow, ws, needed_files, uuid_cache, uuid_cache_path)

        if len(scenes) == 1:
            await submit_single_image_scene(flow, scenes[0], uuid_cache, uuid_cache_path, wait_for_render=True)
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
            for sc in wave:
                await submit_single_image_scene(flow, sc, uuid_cache, uuid_cache_path, wait_for_render=False)
            print(f"  Waiting for {slug} wave {w_idx // 3 + 1} ({len(wave)} images)...")
            saw_pct = False
            zero_streak = 0
            for step in range(60):
                await asyncio.sleep(2.2)
                await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
                await _click_retry_if_failed_card(flow, f"wave-{w_idx // 3 + 1}")
                pcts = await flow.js("""
                Array.from(document.querySelectorAll('div, span'))
                    .map(e => (e.innerText || '').trim())
                    .filter(t => /^\\d+%$/.test(t))
                """)
                if pcts:
                    saw_pct = True
                    zero_streak = 0
                elif saw_pct or step >= 6:
                    zero_streak += 1
                if zero_streak >= 2:
                    print(f"  Wave {w_idx // 3 + 1} finished!")
                    break

        await asyncio.sleep(3.5)
        await capture_qa_pages(flow, qa_dir, f"{slug}_img", "Hình ảnh")


async def map_scene_uuids_pipeline(
    config: Dict[str, Any],
    project_dir: str,
    port: Optional[int] = None,
) -> Dict[str, str]:
    """Stage 2: Walk virtual-scroll picker newest-first and lock 1-to-1 scene_key -> token."""
    slug = config["slug"]
    prefix = config["prefix"].upper()
    scenes = config.get("scenes", [])
    if not scenes:
        raise ValueError("No scenes defined in SKU config.")

    uuid_cache_path = os.path.join(project_dir, f"{slug}_plate_uuids.json")
    plate_tokens: Set[str] = set()
    if os.path.isfile(uuid_cache_path):
        with open(uuid_cache_path, "r", encoding="utf-8") as f:
            plate_tokens = set(json.load(f).values())
    exclude_tokens = set(config.get("exclude_uuids", []))

    ws_url = get_project_ws_url(config["project_id"], port=port, auto_open=True)
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws)
        await exit_edit_view_if_needed(flow)
        await press_escape(flow, 0.3)
        await ensure_image_mode(flow, aspect_ratio="16:9")
        ordered = await scan_all_project_options(flow, max_steps=30)
        await press_escape(flow, 0.3)

    filtered = [
        it for it in ordered
        if it["token"] not in plate_tokens
        and it["token"] not in exclude_tokens
        and not it["txt"].lower().endswith(".jpg")
        and not it["txt"].lower().endswith(".png")
        and f"{prefix}_PLATE_" not in it["txt"]
        and f"{prefix}_REF_" not in it["txt"]
        and "Video" not in it["txt"]
    ]
    if len(filtered) < len(scenes):
        raise RuntimeError(
            f"Expected at least {len(scenes)} generated images for {slug}, found only {len(filtered)}."
        )

    newest_n = filtered[:len(scenes)]
    oldest_to_newest = list(reversed(newest_n))
    mapping: Dict[str, str] = {}
    for sc, it in zip(scenes, oldest_to_newest):
        mapping[sc["key"]] = it["token"]
        print(f"  {sc['key']:40s} -> {it['token']} | {it['txt'][:60]}")

    out_path = os.path.join(project_dir, f"{slug}_scene_uuids.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)
    print(f"Saved {len(mapping)} scene UUIDs -> {out_path}")
    return mapping


async def clear_frame_slots_and_text(flow: FlowCDP) -> None:
    await clear_composer_strict(flow)
    for _ in range(4):
        has_empty_both = await flow.js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => b.getBoundingClientRect().y > 680 && b.getBoundingClientRect().width > 0);
            const s = btns.some(b => (b.innerText || '').trim().includes('Bắt đầu') && !(b.getAttribute('aria-label') || '').includes('Bắt đầu tạo'));
            const e = btns.some(b => (b.innerText || '').trim().includes('Kết thúc'));
            return s && e;
        })()
        """)
        if has_empty_both:
            break
        clicked_x = await flow.js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => {
                const r = b.getBoundingClientRect();
                if (r.width <= 0 || r.y < 740 || r.y > 880 || r.x < 620 || r.x > 880) return false;
                const txt = (b.innerText || '').trim().toLowerCase();
                const aria = (b.getAttribute('aria-label') || '').toLowerCase();
                return txt === 'close' || txt === 'clear' || txt === '×' || txt === '✕' || aria.includes('xoá') || aria.includes('xóa') || aria.includes('đóng') || r.width < 48;
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


async def _populate_frame_slot_by_token(flow: FlowCDP, slot_label: str, target_token: str) -> None:
    """Populate either 'Bắt đầu' or 'Kết thúc' frame slot with virtual-scroll re-centering + 3 retries."""
    tok = target_token.split("=")[0][:48]
    last_err = ""
    for attempt in range(1, 4):
        await press_escape(flow, 0.3)
        await flow.find_and_trusted_click(
            f"text.includes({json.dumps(slot_label)}) && !aria.includes('Bắt đầu tạo') && r.y > 660",
            f"{slot_label} slot",
        )
        await asyncio.sleep(0.85)

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
        await asyncio.sleep(0.3)

        found = False
        for scroll_y in range(0, 10400, 260):
            await flow.js(f"""
            (() => {{
                const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
                if (lb) lb.scrollTop = {scroll_y};
            }})()
            """)
            await asyncio.sleep(0.3)
            hit = await flow.js(f"""
            (() => {{
                const uid = {json.dumps(tok)};
                const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
                const lbRect = lb ? lb.getBoundingClientRect() : null;
                for (const el of Array.from(document.querySelectorAll('[role="option"]'))) {{
                    const src = el.querySelector('img')?.src || '';
                    if (src.includes(uid)) {{
                        if (lb && lbRect) {{
                            const er = el.getBoundingClientRect();
                            lb.scrollTop += (er.top + er.height / 2) - (lbRect.top + 150);
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
            last_err = f"token {tok} not found in virtual scroll"
            continue

        await asyncio.sleep(0.35)

        async def recenter_and_inspect():
            return await flow.js(f"""
            (() => {{
                const uid = {json.dumps(tok)};
                const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
                const lbRect = lb ? lb.getBoundingClientRect() : null;
                let el = Array.from(document.querySelectorAll('[role="option"]')).find(e => (e.querySelector('img')?.src || '').includes(uid));
                if (el && lb && lbRect) {{
                    const er0 = el.getBoundingClientRect();
                    if (er0.top < lbRect.top + 60 || er0.bottom > lbRect.top + 280) {{
                        lb.scrollTop += (er0.top + er0.height / 2) - (lbRect.top + 150);
                    }}
                }}
                el = Array.from(document.querySelectorAll('[role="option"]')).find(e => (e.querySelector('img')?.src || '').includes(uid));
                let coords = null;
                if (el) {{
                    const img = el.querySelector('img');
                    const r = (img && img.getBoundingClientRect().width > 10 ? img : el).getBoundingClientRect();
                    coords = {{cx: Math.round(r.x + Math.min(r.width / 2, 45)), cy: Math.round(r.y + r.height / 2)}};
                }}
                const addBtn = Array.from(document.querySelectorAll('button')).find(
                    b => (b.innerText || '').trim() === 'Thêm vào câu lệnh' && b.getBoundingClientRect().width > 0
                );
                let previewMatches = false;
                if (addBtn) {{
                    let container = addBtn.parentElement;
                    while (container && !container.querySelector('[role="option"]') && container.parentElement) {{
                        container = container.parentElement;
                    }}
                    if (container) {{
                        const pSrcs = Array.from(container.querySelectorAll('img'))
                            .filter(i => !i.closest('[role="option"]'))
                            .map(i => (i.src || '').split('?')[0]);
                        previewMatches = pSrcs.some(s => s.includes(uid));
                    }}
                }}
                return {{coords, hasAdd: Boolean(addBtn), previewMatches}};
            }})()
            """)

        locked = False
        for click_dx in (0, 55, 110, 160):
            st0 = await recenter_and_inspect()
            if st0["coords"] and not st0["previewMatches"]:
                await flow.trusted_click(st0["coords"]["cx"] + click_dx, st0["coords"]["cy"])
            for _ in range(8):
                await asyncio.sleep(0.32)
                st1 = await recenter_and_inspect()
                if st1["hasAdd"] and st1["previewMatches"]:
                    await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
                    await asyncio.sleep(0.65)
                slot_filled = await flow.js(f"""
                (() => {{
                    const lbl = {json.dumps(slot_label)};
                    const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => b.getBoundingClientRect().y > 680 && b.getBoundingClientRect().width > 0);
                    return !btns.some(b => (b.innerText || '').trim() === lbl);
                }})()
                """)
                if slot_filled:
                    locked = True
                    break
            if locked:
                break
        if locked:
            print(f"  + Locked {slot_label} frame [{tok[:10]}] (attempt {attempt})")
            return
        last_err = f"slot {slot_label!r} did not lock on attempt {attempt}"
        await press_escape(flow, 0.8)

    raise RuntimeError(f"Failed to populate {slot_label!r} slot for {tok}: {last_err}")


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
        videos = [v for v in videos if only_key and (only_key in v["key"] or only_key in v.get("scene_key", ""))]
        if not videos:
            raise ValueError(f"No video matching --only-key={only_key!r}")
    elif phase == "slice":
        videos = videos[start_index:]

    ws_url = get_project_ws_url(config["project_id"], port=port, auto_open=True)
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws)
        if phase == "qa-only":
            await capture_qa_pages(flow, qa_dir, f"{slug}_veo", "Video")
            return

        for w_i in range(0, len(videos), 2):
            wave = videos[w_i:w_i + 2]
            for item in wave:
                start_tok = item.get("uuid") or scene_uuids.get(item.get("scene_key", ""), "")
                if not start_tok:
                    raise RuntimeError(f"Missing start UUID for video {item['key']} in {uuids_path}")
                end_tok = item.get("end_uuid") or (
                    scene_uuids.get(item["end_scene_key"], "") if item.get("end_scene_key") else ""
                )

                print(f"\n=== QUEUEING 4S VEO 3.1 CLIP: {item['key']} ===")
                await ensure_veo31_fast_4s_16x9(flow)
                await clear_frame_slots_and_text(flow)
                await _populate_frame_slot_by_token(flow, "Bắt đầu", start_tok)
                if end_tok:
                    await _populate_frame_slot_by_token(flow, "Kết thúc", end_tok)

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
                await flow.find_and_trusted_click("aria === 'Bắt đầu tạo' && !el.disabled", f"submit {item['key']}")

                for _ in range(18):
                    await asyncio.sleep(0.5)
                    reset_done = await flow.js("""
                    Array.from(document.querySelectorAll('button, [role="button"]'))
                        .filter(b => b.getBoundingClientRect().y > 680 && b.getBoundingClientRect().width > 0)
                        .some(b => (b.innerText || '').trim() === 'Bắt đầu')
                    """)
                    if reset_done:
                        break
                await asyncio.sleep(0.6)

            wave_label = f"{slug} Veo Wave {w_i // 2 + 1} ({len(wave)} clips)"
            print(f"  Waiting for {wave_label}...")
            saw_pct = False
            zero_streak = 0
            for step in range(50):
                await asyncio.sleep(3.0)
                await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
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

    ws_url = get_project_ws_url(project_id, port=port, auto_open=True)
    ordered_clip_paths: List[str] = []
    async with websockets.connect(ws_url, max_size=40 * 1024 * 1024) as ws:
        flow = await init_silent_flow_session(ws)
        try:
            await flow.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": dl_tmp, "eventsEnabled": True})
        except Exception:
            await flow.call("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": dl_tmp})

        await switch_gallery_tab(flow, "Video")

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

                row = card_idx // 2
                col = card_idx % 2
                target_sy = max(0, round(row * 270.25 - 100))
                await flow.js(f"""
                (() => {{
                    for (const el of Array.from(document.querySelectorAll('*'))) {{
                        if (el.scrollHeight > el.clientHeight + 200 && el.getBoundingClientRect().width > 500) {{
                            el.scrollTop = {target_sy};
                        }}
                    }}
                }})()
                """)
                await asyncio.sleep(0.55)
                card = await flow.js(f"""
                (() => {{
                    const sc = Array.from(document.querySelectorAll('*')).find(el => el.scrollTop > 0 && el.getBoundingClientRect().width > 500);
                    const actualSy = sc ? sc.scrollTop : 0;
                    const expX = {248 if col == 0 else 716};
                    const expY = 76 + {row} * 270.25 - actualSy;
                    const media = Array.from(document.querySelectorAll('img, video')).filter(m => {{
                        const r = m.getBoundingClientRect();
                        return Math.abs(r.x - expX) < 35 && Math.abs(r.y - expY) < 50 && r.width > 380;
                    }});
                    if (!media.length) return null;
                    const r = media[0].getBoundingClientRect();
                    return {{
                        x: Math.round(r.x), y: Math.round(r.y),
                        w: Math.round(r.width), h: Math.round(r.height),
                        cx: Math.round(r.x + r.width / 2),
                        cy: Math.round(r.y + Math.min(r.height / 2, 110)),
                    }};
                }})()
                """)
                if not card:
                    await switch_gallery_tab(flow, "Video")
                    continue

                await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 110, "y": 320})
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
                        .filter(b => b.w > 0 && b.x >= {card['x'] - 20} && b.x <= {card['x'] + card['w'] + 20} && b.y >= {card['y'] - 20} && b.y <= {card['y'] + card['h'] + 20});
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
