import asyncio
import glob
import json
import os
import shutil
import websockets

from contact_sheet import BRAIN_DIR, build_2fps_contact_sheet
from gen_batch_images import MANIFEST_PATH, get_flow_ws_url
from gen_video_shot1 import VIDEO_MANIFEST_PATH, VIDEOS_DIR, FlowVideoCDP

DL_TMP = os.path.join(VIDEOS_DIR, "dl_tmp")
os.makedirs(DL_TMP, exist_ok=True)


async def get_finished_16x9_video_cards(flow):
    cards = await flow.js("""
    Array.from(document.querySelectorAll('img'))
        .filter(i => {
            const r = i.getBoundingClientRect();
            return r.x > 240 && r.width > r.height * 1.4 && r.width > 200 && i.naturalWidth > 200 && r.y > 60 && r.y < 750;
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
    # Deduplicate by thumb preserving top-to-bottom left-to-right order
    seen = set()
    out = []
    for c in sorted(cards, key=lambda item: (item["y"] // 40, item["x"])):
        if c["thumb"] and c["thumb"] not in seen:
            seen.add(c["thumb"])
            out.append(c)
    return out


async def wait_for_n_16x9_videos(flow, expected_count):
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.4)
    await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
    await asyncio.sleep(1.2)

    for step in range(65):
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.3)
        pct = await flow.js("""
        Array.from(document.querySelectorAll('div, span'))
            .map(e => (e.innerText || '').trim())
            .filter(t => /^\\d+%$/.test(t))
        """)
        cards = await get_finished_16x9_video_cards(flow)
        print(f"    [wait {step*3}s] pct={pct}, 16:9_count={len(cards)} (need >={expected_count})")
        if len(cards) >= expected_count and not pct:
            return cards
        await asyncio.sleep(3.0)
    await flow.shot(f"err_wait_{expected_count}_videos.jpg")
    raise RuntimeError(f"Timed out waiting for {expected_count} 16:9 videos")


async def download_card_mp4_robust(flow, card, out_mp4, res_choice="720p"):
    for f in glob.glob(os.path.join(DL_TMP, "*")):
        os.remove(f)
    try:
        await flow.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP, "eventsEnabled": True})
    except Exception:
        await flow.call("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP})

    for attempt in range(3):
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
            print(f"    Retry {attempt+1}: more_vert not visible yet")
            continue

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
            print(f"    Retry {attempt+1}: Tải xuống menuitem not visible")
            continue

        await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": dl_item["cx"], "y": dl_item["cy"]})
        await asyncio.sleep(0.8)

        res_rect = await flow.js(f"""
        (() => {{
            const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes({json.dumps(res_choice)}));
            if (!m) return null;
            const r = m.getBoundingClientRect();
            return {{cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)}};
        }})()
        """)
        if not res_rect:
            print(f"    Retry {attempt+1}: {res_choice} submenu not open yet, clicking Tải xuống directly...")
            await flow.trusted_click(dl_item["cx"], dl_item["cy"])
            await asyncio.sleep(0.7)
            res_rect = await flow.js(f"""
            (() => {{
                const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes({json.dumps(res_choice)}));
                if (!m) return null;
                const r = m.getBoundingClientRect();
                return {{cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)}};
            }})()
            """)
        if res_rect:
            await flow.trusted_click(res_rect["cx"], res_rect["cy"])
            break
    else:
        await flow.shot("err_download_submenu.jpg")
        raise RuntimeError(f"Could not open download {res_choice} submenu for {out_mp4}")

    downloaded_file = None
    for _ in range(60):
        await asyncio.sleep(1.0)
        files = glob.glob(os.path.join(DL_TMP, "*"))
        mp4s = [f for f in files if f.endswith(".mp4") and not f.endswith(".crdownload") and os.path.getsize(f) > 50000]
        cr = [f for f in files if f.endswith(".crdownload")]
        if mp4s and not cr:
            downloaded_file = mp4s[0]
            break
    if not downloaded_file:
        raise RuntimeError(f"Timed out waiting for download file {out_mp4}")

    shutil.move(downloaded_file, out_mp4)
    print(f"  SAVED {out_mp4} ({os.path.getsize(out_mp4)} bytes)")


async def submit_flf_job(flow, clip_key, start_uuid, end_uuid, prompt):
    print(f"\n=== SUBMITTING {clip_key} ===")
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.4)

    pill = await flow.js("(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]')?.innerText || '').trim()")
    if "Video" not in pill or "4 giây" not in pill or "crop_16_9" not in pill or "x1" not in pill:
        await flow.ensure_video_frames_mode(model_name="Veo 3.1 - Fast", duration_label="4 giây")

    await flow.set_frame_slot("Bắt đầu", start_uuid)
    await flow.set_frame_slot("Kết thúc", end_uuid)

    ed_rect = await flow.js("""
    (() => {
        const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
        const r = el.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    await flow.trusted_click(ed_rect["cx"], ed_rect["cy"])
    await asyncio.sleep(0.2)
    await flow.js("""
    (() => {
        const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
        if (el) {
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
        }
    })()
    """)
    await asyncio.sleep(0.15)
    await flow.call("Input.insertText", {"text": prompt})
    await asyncio.sleep(0.5)
    await flow.shot(f"before_{clip_key}.jpg")

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
        raise RuntimeError(f"Submit button not enabled for {clip_key}: {btns}")
    await flow.trusted_click(target["cx"], target["cy"])
    print(f"  Clicked submit for {clip_key}! Waiting 8s for placeholder card...")
    await asyncio.sleep(8.0)


def build_and_copy_sheet(clip_key, out_mp4):
    contact_local = os.path.join(VIDEOS_DIR, f"{clip_key}_contact_2fps.jpg")
    build_2fps_contact_sheet(out_mp4, contact_local)
    contact_brain = os.path.join(BRAIN_DIR, f"flow_16x9_{clip_key}_contact_2fps.jpg")
    shutil.copy2(contact_local, contact_brain)
    print(f"  2fps contact sheet ready: {contact_brain}")


async def main():
    with open(MANIFEST_PATH) as f:
        m = json.load(f)

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")

        # 1. Wait for already-submitted shot2_v1 (expected 2 finished 16:9 videos: newest = cards[0])
        print("=== WAITING FOR IN-FLIGHT shot2_v1 ===")
        cards = await wait_for_n_16x9_videos(flow, expected_count=2)
        shot2_mp4 = os.path.join(VIDEOS_DIR, "shot2_v1.mp4")
        await download_card_mp4_robust(flow, cards[0], shot2_mp4, res_choice="720p")
        build_and_copy_sheet("shot2_v1", shot2_mp4)

        # 2. Submit & download shot3_v1 (expected 3 finished 16:9 videos: newest = cards[0])
        prompt3 = (
            "Locked-off static tripod 16:9 commercial macro shot with zero camera movement. "
            "0.0s to 0.8s: The woman's right hand smoothly lowers the clear cylindrical glass cup of layered iced milk latte straight down 4 cm until the glass base presses firmly onto the center of the flat moss-green crochet coaster with cream-white scalloped border. "
            "0.8s to 1.2s: Triggered instantly by the weight of the cold glass pressing the internal drawstring mechanism inside the coaster pad, all 6 thin green crochet yarn stems with sage-green leaves and small tight crimson-red and dusty-pink crochet rosebuds hinge crisply and rapidly upward 90 degrees around their fixed cream rim anchor points in one fast elastic spring pop-up snap (pivoting strictly from the coaster border while remaining physically attached to the crochet rim at all times, zero floating rosebuds, zero detached petals, zero slow levitation), standing upright hugging the lower half of the iced latte glass. "
            "1.2s to 2.2s: Her fingers gently release the upper rim of the glass and her hand withdraws smoothly upward-right out of frame. "
            "2.2s to 4.0s: Completely settled, motionless hero iced latte glass surrounded by 6 upright miniature red and pink crochet rosebuds on the warm sunlit walnut table. Subtle natural foley of glass cup touching soft woven cotton yarn followed by a crisp light yarn spring snap, quiet afternoon room ambience, no voice, no music, no text."
        )
        await submit_flf_job(flow, "shot3_v1", m["shot3_start"]["uuid"], m["shot3_end"]["uuid"], prompt3)
        cards = await wait_for_n_16x9_videos(flow, expected_count=3)
        shot3_mp4 = os.path.join(VIDEOS_DIR, "shot3_v1.mp4")
        await download_card_mp4_robust(flow, cards[0], shot3_mp4, res_choice="720p")
        build_and_copy_sheet("shot3_v1", shot3_mp4)

        # 3. Submit & download shot4_v1 (expected 4 finished 16:9 videos: newest = cards[0])
        prompt4 = (
            "Locked-off static tripod 16:9 commercial macro shot at a 38-degree elevated tabletop angle with zero camera movement. "
            "0.0s to 0.8s: The woman's right fingertips smoothly lower the glossy white wireless earbuds charging case straight down 4 cm until it settles onto the center of the flat matcha-green crochet daisy coaster. "
            "0.8s to 1.2s: As the white case presses onto the center pad, the pastel-green scalloped crochet rim curls gently upward into a cozy shallow nest while all 6 thin green crochet yarn stems with tiny green leaves and small dainty 2.2cm white crochet daisies hinge crisply and rapidly upward 85-90 degrees around their fixed rim anchor points in one fast elastic spring pop-up snap (pivoting strictly from the coaster border while remaining physically attached to the crochet rim at all times, zero floating daisies, zero slow levitation). "
            "1.2s to 2.1s: Her fingertips lightly release the white case and her hand withdraws smoothly out of frame to the upper-right. "
            "2.1s to 4.0s: Completely settled, motionless hero white earbuds case cradled inside the popped-up green crochet daisy basket on the sunlit light-oak desk corner. Subtle natural foley of smooth case touching soft cotton yarn and a crisp light yarn spring snap, quiet morning room ambience, no voice, no music, no text."
        )
        await submit_flf_job(flow, "shot4_v1", m["shot4_start"]["uuid"], m["shot4_end"]["uuid"], prompt4)
        cards = await wait_for_n_16x9_videos(flow, expected_count=4)
        shot4_mp4 = os.path.join(VIDEOS_DIR, "shot4_v1.mp4")
        await download_card_mp4_robust(flow, cards[0], shot4_mp4, res_choice="720p")
        build_and_copy_sheet("shot4_v1", shot4_mp4)


if __name__ == "__main__":
    asyncio.run(main())
