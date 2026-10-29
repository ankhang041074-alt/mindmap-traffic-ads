import asyncio
import glob
import json
import os
import shutil
import websockets

from contact_sheet import BRAIN_DIR, build_2fps_contact_sheet
from gen_batch_images import MANIFEST_PATH, OUT_DIR, get_flow_ws_url
from gen_video_shot1 import VIDEO_MANIFEST_PATH, VIDEOS_DIR, FlowVideoCDP

DL_TMP = os.path.join(VIDEOS_DIR, "dl_tmp")
os.makedirs(DL_TMP, exist_ok=True)


async def get_finished_16x9_video_cards(flow):
    cards = await flow.js("""
    Array.from(document.querySelectorAll('img'))
        .filter(i => {
            const r = i.getBoundingClientRect();
            return r.x > 240 && r.width > r.height * 1.4 && r.width > 200 && r.y > 60 && r.y < 700;
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
    return [c for c in cards if c["thumb"]]


async def download_card_mp4(flow, card, out_mp4, res_choice="720p"):
    for f in glob.glob(os.path.join(DL_TMP, "*")):
        os.remove(f)
    try:
        await flow.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP, "eventsEnabled": True})
    except Exception:
        await flow.call("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP})

    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": card["cx"], "y": card["cy"]})
    await asyncio.sleep(0.5)

    more_btn = await flow.js(f"""
    (() => {{
        const btns = Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]'))
            .map(b => {{
                const r = b.getBoundingClientRect();
                return {{cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2), x: r.x, y: r.y, w: r.width}};
            }})
            .filter(b => b.w > 0 && b.x >= {card['x'] - 12} && b.x <= {card['x'] + card['w'] + 12} && b.y >= {card['y'] - 12} && b.y <= {card['y'] + card['h'] + 12});
        return btns[0] || null;
    }})()
    """)
    if not more_btn:
        raise RuntimeError(f"Could not find more_vert on card {card}")

    await flow.trusted_click(more_btn["cx"], more_btn["cy"])
    await asyncio.sleep(0.5)

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

    await flow.find_and_trusted_click(
        f"el.getAttribute('role') === 'menuitem' && text.includes({json.dumps(res_choice)})",
        f"Download {res_choice}"
    )

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
        raise RuntimeError(f"Timed out waiting for download of {out_mp4}")

    shutil.move(downloaded_file, out_mp4)
    print(f"  SAVED {out_mp4} ({os.path.getsize(out_mp4)} bytes)")


async def generate_one_clip(flow, clip_key, start_uuid, end_uuid, prompt):
    print(f"\n=== GENERATING VIDEO {clip_key} ===")
    await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
    await asyncio.sleep(0.8)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
    await asyncio.sleep(0.4)
    before_16x9 = await get_finished_16x9_video_cards(flow)
    seen_thumbs = {c["thumb"] for c in before_16x9}
    print(f"  Existing 16:9 video cards: {len(seen_thumbs)}")

    # Ensure Video -> Khung hình -> 16:9 -> Veo 3.1 - Fast -> 4 giây -> x1
    pill = await flow.js("(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]')?.innerText || '').trim()")
    if "Video" not in pill or "4 giây" not in pill or "crop_16_9" not in pill or "x1" not in pill:
        await flow.ensure_video_frames_mode(model_name="Veo 3.1 - Fast", duration_label="4 giây")

    # Clear any old attached frames if present
    await flow.js("""
    (() => {
        const rmBtns = Array.from(document.querySelectorAll('button')).filter(b => {
            const r = b.getBoundingClientRect();
            const aria = (b.getAttribute('aria-label') || '').toLowerCase();
            const txt = (b.innerText || '').trim();
            return r.y > 640 && r.x > 250 && r.x < 550 && (aria.includes('xoá') || aria.includes('xóa') || txt === 'close');
        });
        for (const b of rmBtns) b.click();
    })()
    """)
    await asyncio.sleep(0.3)

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
    print(f"  Submitted {clip_key}! Waiting for 16:9 render completion...")

    new_card = None
    for step in range(60):
        await asyncio.sleep(3.0)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        pct = await flow.js("""
        Array.from(document.querySelectorAll('div, span'))
            .map(e => (e.innerText || '').trim())
            .filter(t => /^\\d+%$/.test(t))
        """)
        cur_16x9 = await get_finished_16x9_video_cards(flow)
        for c in cur_16x9:
            if c["thumb"] not in seen_thumbs:
                new_card = c
                break
        print(f"    [{(step+1)*3}s] pct={pct}, new_16x9={bool(new_card)}")
        if new_card and not pct:
            break

    if not new_card:
        await flow.shot(f"err_{clip_key}_timeout.jpg")
        raise RuntimeError(f"Timed out waiting for {clip_key}")

    out_mp4 = os.path.join(VIDEOS_DIR, f"{clip_key}.mp4")
    await download_card_mp4(flow, new_card, out_mp4, res_choice="720p")

    contact_local = os.path.join(VIDEOS_DIR, f"{clip_key}_contact_2fps.jpg")
    build_2fps_contact_sheet(out_mp4, contact_local)
    contact_brain = os.path.join(BRAIN_DIR, f"flow_16x9_{clip_key}_contact_2fps.jpg")
    shutil.copy2(contact_local, contact_brain)
    print("  Copied 2fps contact sheet ->", contact_brain)

    vman = {}
    if os.path.exists(VIDEO_MANIFEST_PATH):
        with open(VIDEO_MANIFEST_PATH) as f:
            vman = json.load(f)
    vman[clip_key] = {
        "thumb": new_card["thumb"],
        "local_path": out_mp4,
        "contact_sheet": contact_local,
        "brain_contact_sheet": contact_brain,
    }
    with open(VIDEO_MANIFEST_PATH, "w") as f:
        json.dump(vman, f, indent=2)


async def main():
    with open(MANIFEST_PATH) as f:
        m = json.load(f)

    jobs = [
        (
            "shot2_v1",
            m["shot2_start"]["uuid"],
            m["shot2_end"]["uuid"],
            (
                "Locked-off static tripod 16:9 commercial macro shot with zero camera movement. "
                "0.0s to 0.8s: The woman's right hand smoothly lowers the glossy mustard-yellow ceramic coffee mug straight down 4 cm until the mug base presses firmly onto the center of the flat dark-brown and lime-green crochet sunflower coaster. "
                "0.8s to 1.2s: Triggered instantly by the weight of the mug pressing the internal drawstring mechanism inside the coaster pad, all thin green crochet yarn sunflower stems hinge crisply and rapidly upward 90 degrees around their fixed lime-green rim anchor points in one fast elastic spring pop-up snap (pivoting strictly from the coaster border while remaining physically attached to the crochet rim at all times, zero floating flowers, zero detached petals, zero slow levitation), locking upright into 2 tiers around the yellow mug (2 tall side crochet sunflowers at mug rim height and 2 shorter front crochet sunflowers at half mug height). "
                "1.2s to 2.2s: Her fingers gently release the right mug handle and her hand withdraws smoothly out of frame to the right. "
                "2.2s to 4.0s: Completely settled, motionless hero yellow coffee mug framed by upright miniature yellow crochet sunflowers on the sunlit oak desk. Subtle natural foley of ceramic mug pressing onto soft cotton yarn followed by a crisp light yarn spring snap, quiet sunlit room ambience, no voice, no music, no text."
            ),
        ),
        (
            "shot3_v1",
            m["shot3_start"]["uuid"],
            m["shot3_end"]["uuid"],
            (
                "Locked-off static tripod 16:9 commercial macro shot with zero camera movement. "
                "0.0s to 0.8s: The woman's right hand smoothly lowers the clear cylindrical glass cup of layered iced milk latte straight down 4 cm until the glass base presses firmly onto the center of the flat moss-green crochet coaster with cream-white scalloped border. "
                "0.8s to 1.2s: Triggered instantly by the weight of the cold glass pressing the internal drawstring mechanism inside the coaster pad, all 6 thin green crochet yarn stems with sage-green leaves and small tight crimson-red and dusty-pink crochet rosebuds hinge crisply and rapidly upward 90 degrees around their fixed cream rim anchor points in one fast elastic spring pop-up snap (pivoting strictly from the coaster border while remaining physically attached to the crochet rim at all times, zero floating rosebuds, zero detached petals, zero slow levitation), standing upright hugging the lower half of the iced latte glass. "
                "1.2s to 2.2s: Her fingers gently release the upper rim of the glass and her hand withdraws smoothly upward-right out of frame. "
                "2.2s to 4.0s: Completely settled, motionless hero iced latte glass surrounded by 6 upright miniature red and pink crochet rosebuds on the warm sunlit walnut table. Subtle natural foley of glass cup touching soft woven cotton yarn followed by a crisp light yarn spring snap, quiet afternoon room ambience, no voice, no music, no text."
            ),
        ),
        (
            "shot4_v1",
            m["shot4_start"]["uuid"],
            m["shot4_end"]["uuid"],
            (
                "Locked-off static tripod 16:9 commercial macro shot at a 38-degree elevated tabletop angle with zero camera movement. "
                "0.0s to 0.8s: The woman's right fingertips smoothly lower the glossy white wireless earbuds charging case straight down 4 cm until it settles onto the center of the flat matcha-green crochet daisy coaster. "
                "0.8s to 1.2s: As the white case presses onto the center pad, the pastel-green scalloped crochet rim curls gently upward into a cozy shallow nest while all 6 thin green crochet yarn stems with tiny green leaves and small dainty 2.2cm white crochet daisies hinge crisply and rapidly upward 85-90 degrees around their fixed rim anchor points in one fast elastic spring pop-up snap (pivoting strictly from the coaster border while remaining physically attached to the crochet rim at all times, zero floating daisies, zero slow levitation). "
                "1.2s to 2.1s: Her fingertips lightly release the white case and her hand withdraws smoothly out of frame to the upper-right. "
                "2.1s to 4.0s: Completely settled, motionless hero white earbuds case cradled inside the popped-up green crochet daisy basket on the sunlit light-oak desk corner. Subtle natural foley of smooth case touching soft cotton yarn and a crisp light yarn spring snap, quiet morning room ambience, no voice, no music, no text."
            ),
        ),
    ]

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")
        for clip_key, s_uuid, e_uuid, prompt in jobs:
            await generate_one_clip(flow, clip_key, s_uuid, e_uuid, prompt)
            await asyncio.sleep(1.5)


if __name__ == "__main__":
    asyncio.run(main())
