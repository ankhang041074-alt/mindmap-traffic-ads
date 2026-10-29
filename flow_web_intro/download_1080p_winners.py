import asyncio
import glob
import json
import os
import shutil
import subprocess
import websockets

from gen_batch_images import OUT_DIR, get_flow_ws_url
from gen_video_shot1 import VIDEOS_DIR, FlowVideoCDP

DL_TMP = os.path.join(VIDEOS_DIR, "dl_1080p")
HD_DIR = os.path.join(VIDEOS_DIR, "hd_1080p")
os.makedirs(DL_TMP, exist_ok=True)
os.makedirs(HD_DIR, exist_ok=True)


def probe_video(path):
    res = subprocess.run(
        ["/opt/homebrew/bin/ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,duration", "-of", "json", path],
        capture_output=True, text=True, check=True
    )
    return json.loads(res.stdout)["streams"][0]


async def try_download_1080p(flow, card, out_mp4):
    for f in glob.glob(os.path.join(DL_TMP, "*")):
        os.remove(f)
    try:
        await flow.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP, "eventsEnabled": True})
    except Exception:
        await flow.call("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP})

    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.4)

    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": card["cx"], "y": card["cy"]})
    await asyncio.sleep(0.6)

    more_btn = await flow.js(f"""
    (() => {{
        const btns = Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]'))
            .map(b => {{
                const r = b.getBoundingClientRect();
                return {{cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2), x: r.x, y: r.y, w: r.width}};
            }})
            .filter(b => b.w > 0 && b.x >= {card['x'] - 15} && b.x <= {card['x'] + card['w'] + 15} && b.y >= {card['y'] - 15} && b.y <= {card['y'] + card['h'] + 15});
        return btns[0] || null;
    }})()
    """)
    if not more_btn:
        return False

    await flow.trusted_click(more_btn["cx"], more_btn["cy"])
    await asyncio.sleep(0.6)

    dl_item = await flow.js("""
    (() => {
        const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('Tải xuống'));
        if (!m) return null;
        const r = m.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    if not dl_item:
        return False

    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": dl_item["cx"], "y": dl_item["cy"]})
    await asyncio.sleep(0.8)

    rect_1080 = await flow.js("""
    (() => {
        const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('1080p'));
        if (!m) return null;
        const r = m.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    if not rect_1080:
        return False

    await flow.trusted_click(rect_1080["cx"], rect_1080["cy"])
    print("    Triggered Flow 1080p upscale & download, waiting up to 45s...")

    for step in range(45):
        await asyncio.sleep(1.0)
        files = glob.glob(os.path.join(DL_TMP, "*"))
        mp4s = [f for f in files if f.endswith(".mp4") and not f.endswith(".crdownload") and os.path.getsize(f) > 100000]
        cr = [f for f in files if f.endswith(".crdownload")]
        if mp4s and not cr:
            shutil.move(mp4s[0], out_mp4)
            info = probe_video(out_mp4)
            print(f"    SUCCESS 1080p native Flow upscale: {info['width']}x{info['height']} ({os.path.getsize(out_mp4)} bytes)")
            return True
    return False


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")
        await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
        await asyncio.sleep(1.2)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.5)

        # List all visible 16:9 cards with their title button text
        cards = await flow.js("""
        (() => {
            const imgs = Array.from(document.querySelectorAll('img')).filter(i => {
                const r = i.getBoundingClientRect();
                return r.x > 240 && r.width > r.height * 1.4 && r.width > 200 && i.naturalWidth > 200 && r.y > 60 && r.y < 900;
            });
            const seen = new Set();
            const out = [];
            for (const i of imgs) {
                const thumb = (i.currentSrc || i.src || '').split('?')[0];
                if (!thumb || seen.has(thumb)) continue;
                seen.add(thumb);
                const r = i.getBoundingClientRect();
                out.push({
                    thumb,
                    x: Math.round(r.x), y: Math.round(r.y),
                    w: Math.round(r.width), h: Math.round(r.height),
                    cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)
                });
            }
            out.sort((a, b) => (Math.floor(a.y / 40) - Math.floor(b.y / 40)) || (a.x - b.x));
            return out;
        })()
        """)
        print(f"Found {len(cards)} 16:9 cards in Video viewport:")
        for idx, c in enumerate(cards):
            print(f"  [{idx}] pos=({c['x']},{c['y']}) size={c['w']}x{c['h']} thumb={c['thumb'][-36:]}")

        # Test native 1080p download on newest card (index 0 = shot4_v2) first
        if cards:
            ok = await try_download_1080p(flow, cards[0], os.path.join(HD_DIR, "shot4_v2_1080p.mp4"))
            print("Card 0 (shot4_v2) 1080p result:", ok)
            if ok and len(cards) >= 3:
                # Index 2 is shot3_v1 (index 1 was shot4_v1)
                await try_download_1080p(flow, cards[2], os.path.join(HD_DIR, "shot3_v1_1080p.mp4"))

        # Switch back to 'Tất cả nội dung nghe nhìn' and take a clean project showcase screenshot!
        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(0.4)
        await flow.find_and_trusted_click("text.includes('Tất cả nội dung') && r.x < 240", "All media tab")
        await asyncio.sleep(1.2)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.8)
        await flow.shot("24_final_project_overview_16x9.jpg")


if __name__ == "__main__":
    asyncio.run(main())
