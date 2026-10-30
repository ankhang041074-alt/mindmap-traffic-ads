import argparse
import asyncio
import base64
import json
import os
import sys
import urllib.request
import websockets

sys.path.insert(0, "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro")
from gen_batch_images import FlowCDP
from review_fix_keyframes_step1 import clear_composer_strict

PORT = 49273
PROJECT_ID = "dfcf77a5-5374-4678-9f80-1c5ea7b5c305"
OUT_DIR = "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/cedar_4ft_10s"

# Exact verified UUIDs of all 10 generated 16:9 scenes in Project dfcf77a5-5374-4678-9f80-1c5ea7b5c305
VIDEOS_10 = [
    {
        "key": "V01_PORCH_WALNUT_BRICK_4S",
        "uuid": "3d63c790-7d60-4f2d-bce6-05114ca84031",
        "title": "Cảnh 01 — Hiên Cửa Gỗ Óc Chó 2.45m & Tường Gạch Kem (2 Cây = 1/2 Cửa)",
        "move": "Slow Gimbal Pull-Back 6% (Kéo lùi mở đại cảnh qua tiền cảnh lá vườn bokeh)",
        "prompt": (
            "4-second 35mm cinema gimbal slow pull-back (6%) from the sunlit dark-walnut front door, creating gentle 3D parallax past the blurred foreground garden leaves bottom-right. "
            "Dappled afternoon tree shadows shift subtly on the cream brick wall while both 4ft potted artificial plants and matte-black square planters remain 100% rigid, symmetrical, "
            "and unchanged in exact shape and molded leaf texture. No people, zero morphing, zero text."
        ),
    },
    {
        "key": "V07_LIVING_FLUTED_CREDENZA_LINEN_4S",
        "uuid": "d81a1ece-9b49-4d8f-8576-510de683db46",
        "title": "Cảnh 07 — Phòng Khách Tủ Gỗ Rãnh, Rèm Voan Linen & Ly Gốm Bokeh (1 Cây Hero Trái)",
        "move": "Lateral Slider Glide-Left (Trượt ngang 3 lớp qua ly gốm bokeh tiền cảnh)",
        "prompt": (
            "4-second 50mm cinema slider slow lateral glide-left behind the softly defocused foreground oak coffee table and ceramic mug, revealing rich three-plane optical parallax "
            "against the 4ft potted artificial plant, fluted oak credenza, and sunlit sheer linen curtains. Warm wall sun-streaks hold steady while the matte-black square planter "
            "and dense two-tone green molded foliage stay 100% still and unchanged. No people, zero morphing, zero text."
        ),
    },
    {
        "key": "V05_LIVING_LIMESTONE_FIREPLACE_4S",
        "uuid": "e89c5d87-3173-42d1-85ae-4a4edd69bb76",
        "title": "Cảnh 05 — Lò Sưởi Đá Vôi Pháp Trần Cao 3.4m & Gương Vòm Đồng (2 Cây Ngang Kệ 1.22m)",
        "move": "Axial Dolly Push-In 6% (Đẩy trục chính qua cạnh sofa bouclé tiền cảnh)",
        "prompt": (
            "4-second 35mm cinema dolly slow push-in (6%) past the softly blurred foreground cream bouclé sofa edge toward the carved French limestone fireplace flanked symmetrically "
            "by the twin 4ft potted artificial plants. Warm afternoon window sun-slashes hold across the Roman plaster wall while both matte-black square planters and dense molded crowns "
            "remain 100% motionless, rigid, and identical. No people, zero morphing, zero text."
        ),
    },
    {
        "key": "V02_PORCH_WHITE_CLAPBOARD_3Q_4S",
        "uuid": "5d275a3e-f828-4419-854f-a70ae267077a",
        "title": "Cảnh 02 — Hiên Biệt Thự Mỹ Gỗ Trắng Góc Xiên 3/4 (2 Cây Chiều Sâu 3D)",
        "move": "Diagonal Slider Glide-Right (Trượt ngang xiên 3/4 khoe chiều sâu bậc thềm)",
        "prompt": (
            "4-second 50mm cinema slider slow lateral glide-right along the angled white clapboard porch steps, emphasizing natural 3D depth parallax between the nearer left 4ft potted plant, "
            "the dark paned front door, and the farther right 4ft potted plant. Warm golden-hour sunlight holds steady while both matte-black square planters and dense two-tone green molded crowns "
            "remain 100% solid and unchanged. No people, zero morphing, zero text."
        ),
    },
    {
        "key": "V08_STUDY_WALNUT_DESK_BOOKCASE_4S",
        "uuid": "7a13b09d-c6cd-4dac-8732-d828f3a5429f",
        "title": "Cảnh 08 — Phòng Đọc Sách Bàn Gỗ Óc Chó & Kệ Vòm Vữa Ấm (1 Cây Hero Trái)",
        "move": "Slow Pull-Back Over Walnut Desk (Kéo lùi trượt qua mặt bàn gỗ óc chó bokeh)",
        "prompt": (
            "Smooth 4-second 50mm slow camera push-in (5%) with subtle rightward parallax past the softly blurred foreground dark-walnut writing desk and closed linen notebook "
            "toward the 4ft potted artificial plant beside the sunlit warm plaster arched bookcases. The matte-black square planter, dense two-tone green molded foliage, "
            "and warm afternoon shelf sunlight remain 100% still, sharp, and unchanged. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V04_TERRACE_TEAK_RATTAN_LOUNGE_4S",
        "uuid": "65f2c152-5db9-4ca7-8996-7dfd76b2ce9e",
        "title": "Cảnh 04 — Sân Hiên Có Mái Ghế Bành Mây Gỗ Teak & Vườn Nắng Sớm (1 Cây Hero Phải)",
        "move": "Slider Glide-Right Past Teak Table (Trượt phải qua bàn Teak bokeh, lá vườn xa khẽ lung linh)",
        "prompt": (
            "4-second 50mm cinema slider slow glide-right past the blurred foreground teak coffee table corner toward the 4ft potted artificial plant beside the woven rattan lounge chair. "
            "Distant blurred backyard garden leaves shimmer gently in morning sunlight while the foreground 4ft potted plant, its matte-black square planter, and dense two-tone molded foliage "
            "remain 100% still, rigid, and unchanged. No people, zero morphing, zero text."
        ),
    },
    {
        "key": "V09_STAIRCASE_GLASS_WINDOW_GARDEN_4S",
        "uuid": "7ef37782-5c33-4d76-972c-49b87d27735b",
        "title": "Cảnh 09 — Cầu Thang Gỗ Sồi Bay & Vách Kính Sát Trần Nhìn Ra Vườn (1 Cây Hero Phải)",
        "move": "Lateral Slider Glide-Right (Trượt phải qua ghế gỗ bokeh mở góc cầu thang & vườn)",
        "prompt": (
            "4-second 50mm cinema slider slow lateral glide-right past the softly blurred foreground oak bench edge, creating crisp architectural parallax between the floating white-oak staircase, "
            "the 4ft potted artificial plant, and sunlit garden greenery outside the floor-to-ceiling window. Indoor plant, matte-black square planter, and dense molded foliage stay 100% rigid and still. "
            "No people, zero morphing, zero text."
        ),
    },
    {
        "key": "V03_PATIO_FRENCH_DOORS_TRAVERTINE_4S",
        "uuid": "4f63712c-37c9-433d-8457-a47e3672cf34",
        "title": "Cảnh 03 — Cửa Đôi Kính Khung Đen Sân Hiên Đá Travertine (2 Cây Cận Trung 50mm)",
        "move": "Slow Dolly Push-In 6% (Đẩy nhẹ qua tay ghế gỗ Teak tiền cảnh)",
        "prompt": (
            "4-second 50mm cinema dolly slow push-in (6%) past the softly defocused foreground teak lounge chair toward the black-framed French glass patio doors flanked by the twin 4ft potted plants. "
            "Crisp afternoon stucco sunlight and natural 3-layer patio parallax while both matte-black square planters and dense two-tone molded green crowns stay 100% rigid and pixel-true. "
            "No people, zero morphing, zero text."
        ),
    },
    {
        "key": "V06_FOYER_OAK_CONSOLE_TABLE_4S",
        "uuid": "56d84fb5-e098-432f-89ad-3c2b54ae048c",
        "title": "Cảnh 06 — Sảnh Foyer Bàn Console Gỗ Sồi 85cm & Tranh Lớn (2 Cây Đối Xứng)",
        "move": "Subtle Gimbal Push-In 5% (Đẩy cận tinh tế tôn vinh sảnh vào nhà sang trọng)",
        "prompt": (
            "Smooth 4-second 50mm slow camera push-in (5%) toward the white-oak console table flanked symmetrically by the twin 4ft potted artificial plants in warm afternoon side-window light. "
            "Cream limewash walls, oak floor shadows, matte-black square planters, and dense two-tone green molded foliage remain 100% sharp, motionless, and unchanged. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V10_DINING_SUNROOM_OAK_SIDEBOARD_4S",
        "uuid": "ebc19d89-96d5-431c-bf48-65672b2852ec",
        "title": "Cảnh 10 — Phòng Ăn Trần Cao Tủ Buffet Gỗ Sồi & Nắng Ban Mai (1 Cây Đại Cảnh)",
        "move": "Wide Architectural Push-In 6% (Đẩy chậm xuyên nắng sớm phòng ăn trần cao)",
        "prompt": (
            "4-second 35mm cinema gimbal slow push-in (6%) across the sunlit herringbone oak dining room floor between the warm oak buffet sideboard and oak dining table, framing the 4ft potted artificial plant "
            "under tall morning-lit casement windows. Morning sunbeams hold steady while the matte-black square planter and dense two-tone green molded crown remain 100% still and unchanged. "
            "No people, zero morphing, zero text."
        ),
    },
]


async def ensure_veo31_fast_4s_16x9(flow):
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.3)

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

    is_open = await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))")
    if not is_open:
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "open settings")
        await asyncio.sleep(0.45)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('Video')", "Video radio")
    await asyncio.sleep(0.35)
    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('Khung hình')", "Khung hình radio")
    await asyncio.sleep(0.35)
    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('16:9')", "16:9 radio")
    await asyncio.sleep(0.3)

    model_txt = await flow.js("(document.querySelector('[aria-label=\"Chọn nhóm mô hình\"]')?.innerText || '').trim()")
    if "Veo 3.1 - Fast" not in model_txt:
        await flow.find_and_trusted_click("aria === 'Chọn nhóm mô hình'", "model dropdown")
        await asyncio.sleep(0.45)
        await flow.find_and_trusted_click("el.getAttribute('role') === 'menuitem' && text.includes('Veo 3.1 - Fast')", "Veo 3.1 - Fast")
        await asyncio.sleep(0.4)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === '4 giây'", "4 giây")
    await asyncio.sleep(0.25)
    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === 'x1'", "x1")
    await asyncio.sleep(0.25)
    await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "close settings")
    await asyncio.sleep(0.4)


async def clear_frame_slots_and_text(flow):
    await clear_composer_strict(flow)
    # If Bắt đầu already has a thumbnail attached, click the ✕ clear button inside the composer frame bar (x=680..755, y=770..855)
    for _ in range(3):
        has_empty_start = await flow.js("""
        Array.from(document.querySelectorAll('button, [role="button"]')).some(b => {
            const r = b.getBoundingClientRect();
            const txt = (b.innerText || '').trim();
            const aria = b.getAttribute('aria-label') || '';
            return r.y > 680 && r.width > 0 && txt.includes('Bắt đầu') && !aria.includes('Bắt đầu tạo');
        })
        """)
        if has_empty_start:
            break
        clicked_x = await flow.js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => {
                const r = b.getBoundingClientRect();
                if (r.width <= 0 || r.y < 760 || r.y > 860 || r.x < 660 || r.x > 760) return false;
                const txt = (b.innerText || '').trim().toLowerCase();
                const aria = (b.getAttribute('aria-label') || '').toLowerCase();
                return txt === 'close' || txt === 'clear' || txt === '×' || txt === '✕' || aria.includes('xoá') || aria.includes('xóa') || aria.includes('đóng') || r.width < 48;
            });
            if (btns.length) {
                const r = btns[0].getBoundingClientRect();
                return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
            }
            return null;
        })()
        """)
        if clicked_x:
            await flow.trusted_click(clicked_x["cx"], clicked_x["cy"])
            await asyncio.sleep(0.4)
        else:
            break


async def set_start_frame_by_uuid(flow, target_uuid):
    # Click 'Bắt đầu' slot button in composer
    await flow.find_and_trusted_click("text.includes('Bắt đầu') && !aria.includes('Bắt đầu tạo') && r.y > 660", "Bắt đầu slot")
    await asyncio.sleep(0.85)

    # Clear search input inside modal if non-empty
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
    await asyncio.sleep(0.35)

    # Scroll cdk-virtual-scroll-viewport until target_uuid appears in [role="option"]
    found_opt = None
    for scroll_y in [0, 260, 520, 780, 1040, 1300, 1600, 1900, 2300, 2700]:
        await flow.js(f"""
        (() => {{
            const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
            if (lb) lb.scrollTop = {scroll_y};
        }})()
        """)
        await asyncio.sleep(0.38)
        opt = await flow.js(f"""
        (() => {{
            const uid = {json.dumps(target_uuid)};
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const img = el.querySelector('img');
                const src = img?.src || '';
                if (src.includes(uid)) {{
                    el.scrollIntoView({{block: 'center'}});
                    const r = (img || el).getBoundingClientRect();
                    return {{
                        cx: Math.round(r.x + r.width / 2),
                        cy: Math.round(r.y + r.height / 2),
                        txt: (el.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 50)
                    }};
                }}
            }}
            return null;
        }})()
        """)
        if opt:
            found_opt = opt
            break

    if not found_opt:
        raise RuntimeError(f"Could not find image UUID {target_uuid} inside Bắt đầu picker!")

    await asyncio.sleep(0.2)
    found_opt = await flow.js(f"""
    (() => {{
        const uid = {json.dumps(target_uuid)};
        const el = Array.from(document.querySelectorAll('[role="option"]')).find(e => (e.querySelector('img')?.src || '').includes(uid));
        const r = (el.querySelector('img') || el).getBoundingClientRect();
        return {{cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)}};
    }})()
    """)
    for click_dx in [0, 48]:
        await flow.trusted_click(found_opt["cx"] + click_dx, found_opt["cy"])
        await asyncio.sleep(0.75)

        has_add = await flow.js("""
        Array.from(document.querySelectorAll('button')).some(
            b => (b.innerText || '').trim() === 'Thêm vào câu lệnh' && b.getBoundingClientRect().width > 0
        )
        """)
        if has_add:
            await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
            await asyncio.sleep(0.75)

        slot_ok = await flow.js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => b.getBoundingClientRect().y > 680 && b.getBoundingClientRect().width > 0);
            const hasEmptyStart = btns.some(b => (b.innerText||'').trim() === 'Bắt đầu');
            const hasEmptyEnd = btns.some(b => (b.innerText||'').trim().includes('Kết thúc'));
            return !hasEmptyStart && hasEmptyEnd;
        })()
        """)
        if slot_ok:
            break
    if not slot_ok:
        raise RuntimeError(f"Start Frame slot did not populate cleanly for {target_uuid}!")
    print(f"  + Verified Start Frame [{target_uuid[:8]}] populated in Bắt đầu slot!")


async def submit_veo_clip(flow, item):
    print(f"\n=== QUEUEING 4S VEO 3.1 CLIP: {item['key']} ===")
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
    await asyncio.sleep(0.25)
    await ensure_veo31_fast_4s_16x9(flow)
    await clear_frame_slots_and_text(flow)
    await set_start_frame_by_uuid(flow, item["uuid"])

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
    if not target:
        raise RuntimeError(f"Submit button not enabled for {item['key']}: {btns}")
    await flow.trusted_click(target["cx"], target["cy"])
    print(f"  🎬 Submitted {item['key']}! Waiting for composer post-submit reset...")
    for _ in range(18):
        await asyncio.sleep(0.5)
        reset_done = await flow.js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => b.getBoundingClientRect().y > 680 && b.getBoundingClientRect().width > 0);
            return btns.some(b => (b.innerText || '').trim() === 'Bắt đầu');
        })()
        """)
        if reset_done:
            break
    await asyncio.sleep(0.6)


async def wait_for_video_wave(flow, wave_label, max_steps=45):
    print(f"  Waiting for {wave_label} to complete rendering...")
    saw_pct = False
    zero_streak = 0
    for step in range(max_steps):
        await asyncio.sleep(3.0)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
        st = await flow.js("""
        (() => {
            const pct = Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t));
            const vids = document.querySelectorAll('video').length;
            return {pct, vids};
        })()
        """)
        if st["pct"]:
            saw_pct = True
            zero_streak = 0
        else:
            if saw_pct or step >= 5:
                zero_streak += 1
        print(f"    [{wave_label} +{(step+1)*3}s] pct={st['pct']} videoTags={st['vids']}")
        if zero_streak >= 2:
            print(f"  ✅ {wave_label} completed!")
            return


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["test2", "rest8", "all10"], default="test2")
    args = parser.parse_args()

    tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list").read())
    t = next((x for x in tabs if PROJECT_ID in (x.get("url") or "")), None)
    if not t:
        raise RuntimeError(f"Tab for {PROJECT_ID} not found!")

    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=30 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        # CRITICAL: Silent background focus emulation ONLY — NEVER call Page.bringToFront!
        await flow.call("Page.enable")
        await flow.call("DOM.enable")
        await flow.call("Emulation.setFocusEmulationEnabled", {"enabled": True})

        if args.phase == "test2":
            for it in VIDEOS_10[:2]:
                await submit_veo_clip(flow, it)
            await wait_for_video_wave(flow, "Test Wave (V01 + V07)")
            await asyncio.sleep(2.0)
            res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 86})
            p = os.path.join(OUT_DIR, "qa_veo4s_test2.jpg")
            with open(p, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("Saved test2 video QA screenshot:", p)
        elif args.phase == "rest8":
            rest = VIDEOS_10[6:]  # First 6 clips already rendered/queued; finish remaining 4 clips (2 + 2)!
            for w_i in range(0, len(rest), 2):
                wave = rest[w_i:w_i + 2]
                for it in wave:
                    await submit_veo_clip(flow, it)
                await wait_for_video_wave(flow, f"Wave {w_i//3 + 1} ({len(wave)} clips)")
            await asyncio.sleep(4.0)
            # Switch to left-sidebar Video tab to capture clean 10-video QA grid
            try:
                await flow.find_and_trusted_click("text.includes('Video') && r.x < 220", "Left sidebar Video tab")
                await asyncio.sleep(1.2)
            except Exception as e:
                print("Video tab click note:", e)
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
            await asyncio.sleep(1.0)
            res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
            p = os.path.join(OUT_DIR, "qa_veo4s_all10_top6.jpg")
            with open(p, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            await flow.js("""
            (() => {
                const scrollers = Array.from(document.querySelectorAll('div, main')).filter(el => el.scrollHeight > el.clientHeight + 200);
                for (const s of scrollers) s.scrollTop = 520;
                window.scrollTo(0, 520);
            })()
            """)
            await asyncio.sleep(1.0)
            res2 = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
            p2 = os.path.join(OUT_DIR, "qa_veo4s_all10_bot4.jpg")
            with open(p2, "wb") as f:
                f.write(base64.b64decode(res2["data"]))
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
            print("Saved all10 video QA screenshots:", p, p2)


if __name__ == "__main__":
    asyncio.run(main())
