import asyncio
import json
import os
import websockets

from finish_videos_2_3_4 import (
    VIDEOS_DIR,
    build_and_copy_sheet,
    download_card_mp4_robust,
    get_finished_16x9_video_cards,
)
from gen_batch_images import MANIFEST_PATH, get_flow_ws_url
from gen_video_shot1 import FlowVideoCDP


async def set_frame_slot_safe(flow, slot_label, image_uuid):
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.4)

    await flow.find_and_trusted_click(f"text.includes({json.dumps(slot_label)}) && r.y > 650", f"Slot {slot_label}")
    await asyncio.sleep(0.9)

    # Check if the right-side preview already shows image_uuid!
    already_previewed = await flow.js(f"""
    (() => {{
        const dialogImgs = Array.from(document.querySelectorAll('img')).filter(i => {{
            const r = i.getBoundingClientRect();
            return r.width > 180 && r.height > 100 && (i.src || '').includes({json.dumps(image_uuid)});
        }});
        const addBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Thêm vào câu lệnh');
        return Boolean(dialogImgs.length && addBtn);
    }})()
    """)
    if not already_previewed:
        await flow.js(f"""
        (() => {{
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const imgSrc = el.querySelector('img')?.src || '';
                if (imgSrc.includes({json.dumps(image_uuid)})) {{
                    el.scrollIntoView({{block: 'center'}});
                    return true;
                }}
            }}
            return false;
        }})()
        """)
        await asyncio.sleep(0.3)
        await flow.find_and_trusted_click(
            f"el.getAttribute('role') === 'option' && imgSrc.includes({json.dumps(image_uuid)})",
            f"Frame option {image_uuid}"
        )
        await asyncio.sleep(0.5)

    await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
    await asyncio.sleep(0.6)


async def main():
    with open(MANIFEST_PATH) as f:
        m = json.load(f)

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")

        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(0.4)

        await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
        await asyncio.sleep(1.0)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.4)
        before_cards = await get_finished_16x9_video_cards(flow)
        seen_thumbs = {c["thumb"] for c in before_cards}
        print("Seen top 16:9 thumbs:", len(seen_thumbs))

        pill = await flow.js("(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]')?.innerText || '').trim()")
        if "Video" not in pill or "4 giây" not in pill or "crop_16_9" not in pill or "x1" not in pill:
            await flow.ensure_video_frames_mode(model_name="Veo 3.1 - Fast", duration_label="4 giây")

        # Clear any partial frame attachments
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
        await asyncio.sleep(0.4)

        has_empty_start = await flow.js("""
        Array.from(document.querySelectorAll('button')).some(b => {
            const r = b.getBoundingClientRect();
            return r.y > 600 && (b.innerText || '').includes('Bắt đầu');
        })
        """)
        if has_empty_start:
            await set_frame_slot_safe(flow, "Bắt đầu", m["shot4_start"]["uuid"])
        else:
            print("  'Bắt đầu' already populated with shot4_start!")
        await set_frame_slot_safe(flow, "Kết thúc", m["shot4_end"]["uuid"])

        prompt4_v2 = (
            "Locked-off static tripod 16:9 commercial macro shot at a 38-degree elevated tabletop angle with zero camera movement. "
            "ONE SINGLE CONTINUOUS SMOOTH HAND PLACEMENT AND IMMEDIATE EXIT: "
            "0.0s to 0.7s: The woman's right hand gently lowers the glossy white wireless earbuds charging case straight down 4 cm onto the center of the flat matcha-green crochet daisy coaster in one smooth downward motion. "
            "0.7s to 1.0s: Immediately as the white case touches the center pad, the pastel-green scalloped crochet rim curls slightly upward into a shallow nest while all 6 thin green crochet yarn stems with tiny green leaves and small dainty 2.2cm white crochet daisies hinge crisply upward 90 degrees around their fixed rim anchor points in one instant spring pop-up snap (stems remain physically attached to the crochet rim at all times, zero floating flowers). "
            "1.0s to 1.7s: Her fingertips immediately let go of the white case and her hand glides smoothly and continuously out of the upper-right edge of the frame, NEVER returning or touching the case again. "
            "1.7s to 4.0s: Completely empty frame around the motionless hero white earbuds case resting inside the popped-up green crochet daisy basket on the sunlit light-oak desk corner with zero hand in frame. Subtle foley of smooth case touching soft cotton yarn and a crisp light yarn spring snap, quiet morning room ambience, no voice, no music, no text."
        )

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
        await flow.call("Input.insertText", {"text": prompt4_v2})
        await asyncio.sleep(0.5)

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
        await flow.trusted_click(target["cx"], target["cy"])
        print("Submitted shot4_v2! Waiting 8s...")
        await asyncio.sleep(8.0)

        new_card = None
        for step in range(60):
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
            pct = await flow.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            cur_cards = await get_finished_16x9_video_cards(flow)
            for c in cur_cards:
                if c["thumb"] not in seen_thumbs:
                    new_card = c
                    break
            print(f"  [wait {step*3}s] pct={pct}, new_card={bool(new_card)}")
            if new_card and not pct:
                break
            await asyncio.sleep(3.0)

        if not new_card:
            raise RuntimeError("Timed out waiting for shot4_v2")

        shot4_v2_mp4 = os.path.join(VIDEOS_DIR, "shot4_v2.mp4")
        await download_card_mp4_robust(flow, new_card, shot4_v2_mp4, res_choice="720p")
        build_and_copy_sheet("shot4_v2", shot4_v2_mp4)


if __name__ == "__main__":
    asyncio.run(main())
