import asyncio
import glob
import json
import os
import shutil
import websockets

from contact_sheet import BRAIN_DIR, build_2fps_contact_sheet
from download_1080p_winners import DL_TMP, HD_DIR, probe_video
from download_remaining_1080p import extract_mid_frame_rgb_mean, mean_abs_diff
from finish_videos_2_3_4 import download_card_mp4_robust
from fix_1080p_and_reassemble import download_1080p_strict
from gen_batch_images import MANIFEST_PATH, get_flow_ws_url
from gen_video_shot1 import VIDEOS_DIR, FlowVideoCDP
from review_fix_keyframes_step1 import clear_composer_strict
from review_fix_keyframes_step2 import select_asset_in_open_flow_menu


async def set_video_frame_slot_verified(flow, slot_label, uuid_str, search_query=None):
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)
    await flow.find_and_trusted_click(f"text.includes({json.dumps(slot_label)}) && r.y > 620", f"Frame slot {slot_label}")
    await asyncio.sleep(0.85)
    chosen = await select_asset_in_open_flow_menu(flow, uuid_str, search_query=search_query)
    print(f"  VERIFIED Frame Slot [{slot_label}] = {chosen[:12]}...")


async def get_video_tab_card_count_and_top_rect(flow):
    await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
    await asyncio.sleep(1.1)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
    await asyncio.sleep(0.4)
    info = await flow.js("""
    (() => {
        const moreBtns = Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]'))
            .map(b => {
                const r = b.getBoundingClientRect();
                return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
            })
            .filter(b => b.w > 0 && b.x > 240 && b.y > 60 && b.y < 700);
        const pct = Array.from(document.querySelectorAll('div, span'))
            .map(e => (e.innerText || '').trim())
            .filter(t => /^\\d+%$/.test(t));
        // Top-left card in 2-column grid sits at x=248..700, y=82..336 with more_vert near x~660, y~88
        const hasTopLeftReady = moreBtns.some(b => b.x >= 550 && b.x <= 710 && b.y >= 70 && b.y <= 130);
        return {moreCount: moreBtns.length, hasTopLeftReady, pct, topMore: moreBtns[0] || null};
    })()
    """)
    return info


async def generate_and_export_1080p_clip(flow, clip_key, start_spec, end_spec, prompt, ref_sigs):
    print(f"\n==========================================")
    print(f"=== GENERATING 16:9 VEO 3.1 CLIP: {clip_key} ===")
    print(f"==========================================")

    await flow.find_and_trusted_click("text.includes('Tất cả nội dung') && r.x < 240", "All media tab")
    await asyncio.sleep(0.8)
    await flow.ensure_video_frames_mode(model_name="Veo 3.1 - Fast", duration_label="4 giây")
    await clear_composer_strict(flow)

    # Ensure both Bắt đầu and Kết thúc slots are empty
    await flow.js("""
    (() => {
        const rmBtns = Array.from(document.querySelectorAll('button')).filter(b => {
            const r = b.getBoundingClientRect();
            const aria = (b.getAttribute('aria-label') || '').toLowerCase();
            const txt = (b.innerText || '').trim();
            return r.y > 620 && r.x > 240 && r.x < 650 && (aria.includes('xoá') || aria.includes('xóa') || txt === 'close' || txt === 'cancel');
        });
        for (const b of rmBtns) b.click();
    })()
    """)
    await asyncio.sleep(0.4)

    s_uuid, s_q = start_spec
    e_uuid, e_q = end_spec
    await set_video_frame_slot_verified(flow, "Bắt đầu", s_uuid, search_query=s_q)
    await set_video_frame_slot_verified(flow, "Kết thúc", e_uuid, search_query=e_q)

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
        raise RuntimeError(f"Submit button not ready for {clip_key}: {btns}")
    await flow.trusted_click(target["cx"], target["cy"])
    print(f"  Submitted {clip_key}! Switching to Video tab in 6s to monitor progress...")
    await asyncio.sleep(6.0)

    await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
    await asyncio.sleep(1.0)

    saw_progress = False
    for step in range(65):
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        st = await flow.js("""
        (() => {
            const moreBtns = Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]'))
                .map(b => {
                    const r = b.getBoundingClientRect();
                    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
                })
                .filter(b => b.w > 0 && b.x > 240 && b.y > 60 && b.y < 700);
            const pct = Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t));
            const hasTopLeftReady = moreBtns.some(b => b.x >= 550 && b.x <= 710 && b.y >= 70 && b.y <= 135);
            return {pct, hasTopLeftReady, topMore: moreBtns[0] || null};
        })()
        """)
        if st["pct"]:
            saw_progress = True
        print(f"    [{clip_key} +{(step*3)+6}s] pct={st['pct']} topLeftReady={st['hasTopLeftReady']} saw_progress={saw_progress}")
        if (saw_progress or step >= 8) and not st["pct"] and st["hasTopLeftReady"]:
            break
        await asyncio.sleep(3.0)

    import hashlib
    sd_mp4 = os.path.join(VIDEOS_DIR, f"{clip_key}.mp4")
    existing_hashes = set()
    for existing_mp4 in glob.glob(os.path.join(VIDEOS_DIR, "*.mp4")):
        if os.path.abspath(existing_mp4) != os.path.abspath(sd_mp4):
            with open(existing_mp4, "rb") as ef:
                existing_hashes.add(hashlib.sha256(ef.read()).hexdigest())

    top_left_card = {"x": 248, "y": 82, "w": 452, "h": 254, "cx": 474, "cy": 209}
    for attempt in range(6):
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.5)
        await download_card_mp4_robust(flow, top_left_card, sd_mp4, res_choice="720p")
        with open(sd_mp4, "rb") as nf:
            h_new = hashlib.sha256(nf.read()).hexdigest()
        new_sig = extract_mid_frame_rgb_mean(sd_mp4)
        print(f"  [attempt {attempt+1}] 720p {sd_mp4} ({os.path.getsize(sd_mp4):,} bytes), sha256={h_new[:12]}, is_new={h_new not in existing_hashes}")
        if h_new not in existing_hashes:
            break
        print(f"  Top-left card sha256 matched an already-downloaded clip; waiting 10s for {clip_key} card to settle...")
        await asyncio.sleep(10.0)
    else:
        raise RuntimeError(f"Failed to download distinct new 720p clip for {clip_key}!")

    ref_sigs[clip_key] = new_sig

    # Build 2fps contact sheet + copy to brain dir
    sheet_path = os.path.join(VIDEOS_DIR, f"{clip_key}_contact_2fps.jpg")
    build_2fps_contact_sheet(sd_mp4, sheet_path, cols=4)
    brain_sheet = os.path.join(BRAIN_DIR, f"flow_16x9_{clip_key}_contact_2fps.jpg")
    shutil.copy2(sheet_path, brain_sheet)
    print(f"  Saved 2fps contact sheet: {brain_sheet}")

    # Immediately export Native Flow 1080p verified strictly against this exact clip's RGB signature!
    ok_1080 = await download_1080p_strict(flow, top_left_card, clip_key, {clip_key: new_sig}, timeout_s=95)
    print(f"  Native Flow 1080p export for {clip_key}: {ok_1080}")
    return sd_mp4


async def main():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        m = json.load(f)

    shot1_end_uuid = m["shot1_end"].get("uuid") or m["shot1_end"]["base_url"].split("/")[-1]
    shot1_start_v2_uuid = m["shot1_start_v2"]["uuid"]
    shot5_start_uuid = m["shot5_start"]["uuid"]
    shot5_end_uuid = m["shot5_end"]["uuid"]
    shot6_start_uuid = m["shot6_start"]["uuid"]
    shot6_end_uuid = m["shot6_end"]["uuid"]

    ref_sigs = {
        k: extract_mid_frame_rgb_mean(os.path.join(VIDEOS_DIR, f"{k}.mp4"))
        for k in ["shot1_v1", "shot2_v1", "shot3_v1", "shot4_v1", "shot4_v2"]
        if os.path.exists(os.path.join(VIDEOS_DIR, f"{k}.mp4"))
    }

    jobs = [
        (
            "shot1_v2",
            (shot1_start_v2_uuid, None),
            (shot1_end_uuid, "Crochet daisy coaster and mug"),
            (
                "Locked-off static tripod 16:9 commercial macro shot at a 25-degree tabletop angle with zero camera movement. "
                "INSTANT MECHANICAL POP-UP RIGHT ON MUG TOUCHDOWN (ZERO DELAY): "
                "0.0s to 0.5s: The woman's right hand smoothly lowers the steaming cream-white ceramic hot tea mug straight down 3.5 cm onto the center of the plain flat matcha-green crochet coaster pad in one fluid continuous motion. "
                "0.5s to 0.9s: THE EXACT INSTANT the ceramic mug base touches the green crochet pad (zero pause, zero delay), the thin green crochet yarn stems with tiny green leaves and dainty miniature 2.2cm white crochet daisies hinge crisply upward 90 degrees from flat on the table to vertical upright around the mug in one snappy mechanical spring pop-up, anchored firmly to the pastel-green crochet rim at all times (zero floating flowers, zero morphing). "
                "0.9s to 1.7s: Her fingers immediately release the mug handle and her hand glides smoothly and continuously out the right edge of the frame, never returning. "
                "1.7s to 4.0s: Motionless hero shot of the steaming cream ceramic tea mug embraced by the upright miniature white crochet daisies on the sunlit cafe table, soft tea steam rising gently. Subtle natural foley of ceramic mug touching soft cotton coaster yarn, quiet room tone, no voice, no music, no text."
            ),
        ),
        (
            "shot5_v1",
            (shot5_start_uuid, None),
            (shot5_end_uuid, "Crochet coaster holding matcha"),
            (
                "Locked-off static tripod 16:9 commercial macro shot at a 25-degree tabletop angle with zero camera movement. "
                "INSTANT MECHANICAL POP-UP RIGHT ON GLASS TOUCHDOWN (ZERO DELAY): "
                "0.0s to 0.5s: The woman's right hand gently lowers the clear cylindrical glass cup of layered iced green matcha milk latte straight down 3.5 cm onto the center of the plain flat matcha-green crochet coaster pad. "
                "0.5s to 0.9s: THE EXACT INSTANT the glass bottom touches the green crochet pad (zero pause), all 4 thin green crochet yarn stems with tiny green crochet leaves and dainty miniature 2.2cm white crochet daisies hinge crisply upward 90 degrees from flat on the birch table to vertical upright hugging the glass sides in one snappy mechanical spring pop-up, remaining physically anchored to the crochet rim at all times (zero floating petals). "
                "0.9s to 1.7s: Her fingers immediately release the upper rim of the glass and her hand glides smoothly out the upper-right edge of the frame, never returning. "
                "1.7s to 4.0s: Completely hands-free motionless hero hold of the layered iced matcha latte glass surrounded by the 4 upright miniature white crochet daisies on the sunlit Scandinavian birch desk. Subtle natural foley of glass setting gently onto soft cotton yarn, quiet room ambience, no voice, no music, no text."
            ),
        ),
        (
            "shot6_v1",
            (shot6_start_uuid, None),
            (shot6_end_uuid, "Crochet flower coasters on table"),
            (
                "Locked-off static tripod 16:9 commercial shot on a sunlit oak dining table with zero camera movement. The right-side open flat moss-green and cream crochet rosebud coaster stays 100% motionless on the wooden table throughout the entire clip. "
                "INSTANT MECHANICAL POP-UP ON THE LEFT SUNFLOWER COASTER RIGHT ON MUG TOUCHDOWN: "
                "0.0s to 0.5s: The woman's right hand smoothly lowers the hand-painted cream-and-blue floral ceramic mug straight down 3.5 cm onto the center of the left dark soil-brown and lime-green crochet coaster pad. "
                "0.5s to 0.9s: THE EXACT INSTANT the blue-floral ceramic mug base touches the brown crochet center pad (zero delay), all 4 yellow crochet sunflower stems (2 tall side stems at 9 o'clock and 3 o'clock reaching mug rim height plus 2 shorter front stems at 7 o'clock and 5 o'clock reaching mid-mug height) hinge crisply upward 90 degrees from flat on the oak table to vertical upright hugging the mug in one snappy spring pop-up, anchored firmly to the lime-green grass border (zero floating petals). "
                "0.9s to 1.7s: Her fingers immediately let go of the ceramic mug handle and her hand glides smoothly out the upper-right edge of the frame, never returning. "
                "1.7s to 4.0s: Completely hands-free motionless dual-coaster hero hold showing the popped-up 2-tier yellow sunflower coaster embracing the blue-floral mug on the left beside the open flat red-and-pink rosebud coaster on the right. Subtle foley of ceramic mug touching soft cotton yarn, quiet morning room ambience, no voice, no music, no text."
            ),
        ),
    ]

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")
        for clip_key, s_spec, e_spec, prompt in jobs:
            await generate_and_export_1080p_clip(flow, clip_key, s_spec, e_spec, prompt, ref_sigs)

        # Leave Flow cleanly on All Media tab with empty composer and capture clean overview screenshot
        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(0.4)
        await flow.find_and_trusted_click("text.includes('Tất cả nội dung') && r.x < 240", "All media tab")
        await asyncio.sleep(1.0)
        await clear_composer_strict(flow)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.6)
        await flow.shot("26_review_upgraded_project_overview.jpg")

    shutil.rmtree(DL_TMP, ignore_errors=True)
    print("\n=== Completed All 3 New 16:9 Veo 3.1 Clips + Native 1080p Exports! ===")


if __name__ == "__main__":
    asyncio.run(main())
