import asyncio
import glob
import json
import os
import shutil
import subprocess
import websockets

from gen_batch_images import FlowCDP, OUT_DIR, SCREENSHOT_DIR, get_flow_ws_url

VIDEOS_DIR = os.path.join(OUT_DIR, "videos")
DL_TMP = os.path.join(VIDEOS_DIR, "dl_tmp")
BRAIN_DIR = "/Users/dudumac5/.gemini/antigravity/brain/b5518d8f-8b2d-4488-85b7-420814826233"
os.makedirs(DL_TMP, exist_ok=True)


def make_2fps_contact_sheet(mp4_path, out_jpg):
    # Probe duration and resolution
    probe = subprocess.run(
        ["/opt/homebrew/bin/ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,duration", "-of", "json", mp4_path],
        capture_output=True, text=True, check=True
    )
    info = json.loads(probe.stdout)
    print("FFPROBE:", info)
    vf = (
        "fps=2,scale=480:-1,"
        "drawtext=text='t=%{pts\\:hms}':x=12:y=12:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.65,"
        "tile=4x2:padding=6:margin=6"
    )
    subprocess.run(
        ["/opt/homebrew/bin/ffmpeg", "-y", "-i", mp4_path, "-vf", vf, "-frames:v", "1", "-q:v", "2", out_jpg],
        check=True, capture_output=True
    )
    print("Created 2fps contact sheet:", out_jpg)


async def download_top_16x9_video(flow, out_mp4, res_choice="720p"):
    # Clear dl_tmp
    for f in glob.glob(os.path.join(DL_TMP, "*")):
        os.remove(f)

    # Set download path via Browser.setDownloadBehavior or Page.setDownloadBehavior
    try:
        await flow.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP, "eventsEnabled": True})
    except Exception:
        await flow.call("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP})

    # Ensure we are on Video tab and scrolled to top
    await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
    await asyncio.sleep(0.8)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
    await asyncio.sleep(0.5)

    # Wait until no '%' progress indicator and a 16:9 card image is visible
    card_16x9 = None
    for step in range(40):
        pct = await flow.js("""
        Array.from(document.querySelectorAll('div, span'))
            .map(e => (e.innerText || '').trim())
            .filter(t => /^\\d+%$/.test(t))
        """)
        cards = await flow.js("""
        Array.from(document.querySelectorAll('img'))
            .filter(i => {
                const r = i.getBoundingClientRect();
                return r.x > 240 && r.width > r.height * 1.4 && r.width > 200 && r.y > 60 && r.y < 500;
            })
            .map(i => {
                const r = i.getBoundingClientRect();
                return {
                    thumb: (i.currentSrc || i.src || '').split('?')[0],
                    x: Math.round(r.x), y: Math.round(r.y),
                    w: Math.round(r.width), h: Math.round(r.height),
                    cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)
                };
            })
        """)
        print(f"  [wait {step*2}s] pct={pct}, 16:9_cards={len(cards)}")
        if cards and not pct:
            card_16x9 = cards[0]
            break
        await asyncio.sleep(2.0)

    if not card_16x9:
        await flow.shot("err_no_16x9_video_card.jpg")
        raise RuntimeError("No finished 16:9 video card found!")

    await flow.shot("23_shot1_video_card_ready.jpg")
    # Hover the 16:9 card so its top-right action buttons (favorite, redo, more_vert) become visible
    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": card_16x9["cx"], "y": card_16x9["cy"]})
    await asyncio.sleep(0.5)

    # Find the more_vert ("Tuỳ chọn khác") button inside this card's bounding box
    more_btn = await flow.js(f"""
    (() => {{
        const btns = Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]'))
            .map(b => {{
                const r = b.getBoundingClientRect();
                return {{cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2), x: r.x, y: r.y, w: r.width}};
            }})
            .filter(b => b.w > 0 && b.x >= {card_16x9['x'] - 10} && b.x <= {card_16x9['x'] + card_16x9['w'] + 10} && b.y >= {card_16x9['y'] - 10} && b.y <= {card_16x9['y'] + card_16x9['h'] + 10});
        return btns[0] || null;
    }})()
    """)
    if not more_btn:
        raise RuntimeError(f"Could not find more_vert button on card {card_16x9}")

    await flow.trusted_click(more_btn["cx"], more_btn["cy"])
    await asyncio.sleep(0.5)

    # Hover 'Tải xuống'
    dl_item = await flow.js("""
    (() => {
        const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('Tải xuống'));
        if (!m) return null;
        const r = m.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": dl_item["cx"], "y": dl_item["cy"]})
    await asyncio.sleep(0.5)

    # Click resolution item ('720p' or '1080p')
    res_item = await flow.find_and_trusted_click(
        f"el.getAttribute('role') === 'menuitem' && text.includes({json.dumps(res_choice)})",
        f"Download {res_choice}"
    )
    print(f"  Clicked download {res_choice}: {res_item}")

    # Wait for file to finish downloading in DL_TMP
    downloaded_file = None
    for step in range(45):
        await asyncio.sleep(1.0)
        files = glob.glob(os.path.join(DL_TMP, "*"))
        mp4s = [f for f in files if f.endswith(".mp4") and not f.endswith(".crdownload") and os.path.getsize(f) > 50000]
        cr = [f for f in files if f.endswith(".crdownload")]
        if mp4s and not cr:
            downloaded_file = mp4s[0]
            break
        if step % 3 == 0:
            print(f"    [dl {step+1}s] files={[os.path.basename(x) for x in files]}")

    if not downloaded_file:
        raise RuntimeError(f"Download timed out in {DL_TMP}")

    shutil.move(downloaded_file, out_mp4)
    print(f"  SAVED MP4 ({os.path.getsize(out_mp4)} bytes): {out_mp4}")
    return card_16x9["thumb"]


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        await flow.call("Page.enable")
        out_mp4 = os.path.join(VIDEOS_DIR, "shot1_v1.mp4")
        await download_top_16x9_video(flow, out_mp4, res_choice="720p")

    contact_local = os.path.join(VIDEOS_DIR, "shot1_v1_contact_2fps.jpg")
    make_2fps_contact_sheet(out_mp4, contact_local)
    contact_brain = os.path.join(BRAIN_DIR, "flow_16x9_shot1_v1_contact_2fps.jpg")
    shutil.copy2(contact_local, contact_brain)
    print("Copied contact sheet to brain dir:", contact_brain)


if __name__ == "__main__":
    asyncio.run(main())
