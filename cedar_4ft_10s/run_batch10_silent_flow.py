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
PLATE_DIR = os.path.join(OUT_DIR, "batch40_plates")
REF_DIR = os.path.join(OUT_DIR, "clean_refs")

PLATES = [
    "PLATE_01_PAIR_HALFDOOR_45PCT_16x9.jpg",
    "PLATE_02_PAIR_MEDIUM_HERO_56PCT_16x9.jpg",
    "PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg",
    "PLATE_04_SINGLE_HERO_LEFT_68PCT_16x9.jpg",
    "PLATE_05_SINGLE_HERO_RIGHT_66PCT_16x9.jpg",
    "PLATE_06_SINGLE_WIDE_ROOM_50PCT_16x9.jpg",
]

PAIR_LOCK = (
    "Edit this 16:9 product photograph (using the second 1024x1024 reference image for close-up molded leaf and matte-black square planter detail): "
    "keep BOTH potted artificial plants and their matte-black tapered square planters 100% pixel-identical to the 16:9 plate in exact position, height, "
    "pot width-to-height proportions, snug recessed square top rim, plump symmetrical rounded-cone outer contour, and dense two-tone green molded plastic leaf texture "
    "— DO NOT slim the pots, DO NOT pinch the waist above the pot rim, and DO NOT redraw or alter the leaves into spiky pine needles. "
    "Replace ONLY the pure white background with "
)

SINGLE_LOCK = (
    "Edit this 16:9 product photograph (using the second 1024x1024 reference image for close-up molded leaf and matte-black square planter detail): "
    "keep the potted artificial plant and its matte-black tapered square planter 100% pixel-identical to the 16:9 plate in exact position, height, "
    "pot width-to-height proportions, snug recessed square top rim, plump symmetrical rounded-cone outer contour, and dense two-tone green molded plastic leaf texture "
    "— DO NOT slim the pot, DO NOT pinch the waist above the pot rim, and DO NOT redraw or alter the leaves into spiky pine needles. "
    "Replace ONLY the pure white background with "
)

SCENES_10 = [
    {
        "key": "S01_PORCH_WALNUT_BRICK",
        "refs": ["PLATE_01_PAIR_HALFDOOR_45PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 35mm-50mm live-action Kodak Vision3 250D sunlit luxury front porch: a tall 2.45-meter solid dark-walnut 6-panel front door with sidelights "
            "and overhead glass transom window rising to the high porch ceiling soffit centered between both plants, aged-brass lever door handle aligned right at plant-top height "
            "(strictly 1/2 door scale), two high-mounted aged-brass carriage wall lanterns on warm cream-limewash brick walls, grey bluestone steps with a plain unmarked natural coir doormat, "
            "soft blurred foreground green garden leaf bokeh bottom-right, warm late-afternoon dappled tree-shadow sunlight on the brick wall, clean natural daylight on both plants, "
            "realistic floor contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S02_PORCH_WHITE_CLAPBOARD_3Q",
        "refs": ["PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm live-action Kodak Vision3 250D American coastal Hamptons front porch viewed at a natural 20-degree three-quarter diagonal perspective matching the staggered depth of the two plants: "
            "crisp white painted wood clapboard siding, a tall 2.4-meter matte-charcoal paned front door angled between the nearer left plant and farther right plant with its brushed-brass handle "
            "right at plant-top height, natural limestone porch steps with an unmarked woven jute mat, warm golden-hour sunlight casting soft porch-column shadows across the white siding, "
            "clean natural daylight on both plants, realistic stone contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S03_PATIO_FRENCH_DOORS_TRAVERTINE",
        "refs": ["PLATE_02_PAIR_MEDIUM_HERO_56PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm medium-shot live-action Kodak Vision3 250D luxury backyard travertine terrace: centered between both plants are tall black-steel framed French double glass patio doors "
            "whose upper glass panes extend past the top edge of the 16:9 frame (aged-brass lever handles positioned slightly below the plant tops to lock true 4ft scale), "
            "warm cream Mediterranean stucco walls, honed beige travertine stone patio tiles, softly blurred outdoor teak lounge arm bottom-left, warm afternoon sunbeams on the stucco wall, "
            "clean daylight on both plants, realistic contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S04_TERRACE_TEAK_RATTAN_LOUNGE",
        "refs": ["PLATE_05_SINGLE_HERO_RIGHT_66PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D covered luxury garden verandah: on the left beside the plant sits a low 75cm natural teak and woven-rattan outdoor lounge chair "
            "with cream linen cushions (reaching two-thirds up the plant), warm travertine stone deck floor, creamy plaster verandah columns and softly blurred sunlit green backyard garden bokeh behind, "
            "blurred foreground teak coffee table corner bottom-left, warm morning sun-streaks on the stone floor, clean natural daylight on the plant, realistic floor contact shadow under the planter, zero text."
        ),
    },
    {
        "key": "S05_LIVING_LIMESTONE_FIREPLACE",
        "refs": ["PLATE_01_PAIR_HALFDOOR_45PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 35mm-50mm live-action Kodak Vision3 250D soaring 3.4-meter high-ceilinged European-American living room: centered between both plants is a hand-carved cream French limestone fireplace "
            "whose 1.22m mantel shelf aligns strictly level with the top tips of both plants, surmounted by a tall arched antique-brass mirror rising toward crown molding, warm Roman plaster walls, "
            "herringbone white-oak floor, softly blurred cream bouclé sofa edge bottom-left, warm diagonal afternoon window sun-slashes on the plaster wall, even natural daylight on both plants, "
            "realistic floor contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S06_FOYER_OAK_CONSOLE_TABLE",
        "refs": ["PLATE_02_PAIR_MEDIUM_HERO_56PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm medium-shot live-action Kodak Vision3 250D luxury home entryway foyer: centered between both plants is an 85cm natural white-oak console table (reaching ~70% of plant height) "
            "styled with a minimalist travertine bowl, with a large minimalist neutral linen framed artwork hanging high on the warm cream limewash wall above it extending toward the top edge of the frame, "
            "wide-plank European oak flooring, warm afternoon window light across the wall, clean natural daylight on both plants, realistic floor contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S07_LIVING_FLUTED_CREDENZA_LINEN",
        "refs": ["PLATE_04_SINGLE_HERO_LEFT_68PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sunlit modern organic living room: an 80cm fluted natural-oak credenza cabinet on the left reaching two-thirds up the plant, "
            "tall sheer warm-ivory linen curtains behind continuing past the top edge of the frame, an oatmeal bouclé armchair on the right, wide-plank oak floor with realistic planter contact shadow, "
            "softly blurred foreground oak coffee table corner with a handmade ceramic mug bottom-right, warm afternoon sun-streaks on the plaster wall, clean natural daylight on the plant, zero text."
        ),
    },
    {
        "key": "S08_STUDY_WALNUT_DESK_BOOKCASE",
        "refs": ["PLATE_04_SINGLE_HERO_LEFT_68PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D luxury home office study: built-in warm clay-plaster arched bookcases styled with neutral books behind continuing past the top edge of the frame, "
            "warm oak plank floor with realistic planter contact shadow, a softly blurred 75cm dark-walnut writing desk corner (reaching ~62% of plant height) with a closed unmarked linen notebook "
            "and tan leather chair edge in the right foreground, warm afternoon window sunlight across the plaster shelves, clean natural daylight on the plant, zero text."
        ),
    },
    {
        "key": "S09_STAIRCASE_GLASS_WINDOW_GARDEN",
        "refs": ["PLATE_05_SINGLE_HERO_RIGHT_66PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D architectural modern villa hallway: on the left rises an open floating white-oak staircase with minimalist black-steel railing, "
            "behind the plant is a tall floor-to-ceiling black-framed window continuing past the top edge of the frame revealing softly blurred sunlit garden greenery outside, "
            "warm limestone tile floor with realistic planter contact shadow, softly blurred foreground oak bench edge bottom-left, warm natural daylight streaming across the floor, "
            "clean true-green light on the plant, zero text."
        ),
    },
    {
        "key": "S10_DINING_SUNROOM_OAK_SIDEBOARD",
        "refs": ["PLATE_06_SINGLE_WIDE_ROOM_50PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 35mm-50mm live-action Kodak Vision3 250D high-ceilinged sunlit dining room: beside the plant on the left is an 85cm warm oak buffet sideboard (reaching ~70% of plant height), "
            "on the right a softly angled solid oak dining table with linen-upholstered chairs, tall paned casement windows along the back cream plaster wall streaming warm morning sunbeams "
            "onto the herringbone oak floor, realistic contact shadow under the planter, clean natural daylight on the plant, zero text."
        ),
    },
]


async def check_ingredient_exists(flow, query_stem):
    await flow.js(f"""
    (() => {{
        const inp = document.querySelector('[aria-label="Tìm kiếm thành phần"]');
        if (!inp) return;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(inp, {json.dumps(query_stem)});
        inp.dispatchEvent(new Event('input', {{bubbles: true}}));
    }})()
    """)
    await asyncio.sleep(0.45)
    names = await flow.js("""
    Array.from(document.querySelectorAll('[role="option"]')).map(o => (o.innerText || '').trim())
    """)
    return any(query_stem in t for t in names)


async def upload_missing_plates(flow, ws):
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)
    await flow.js("""
    (() => {
        if (!document.querySelector('[role="option"]')) {
            document.querySelector('[aria-label="Thêm thành phần vào ô nhập câu lệnh"]')?.click();
        }
    })()
    """)
    await asyncio.sleep(0.8)

    required_files = [(REF_DIR, "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg")] + [(PLATE_DIR, p) for p in PLATES]
    missing = []
    for d, fname in required_files:
        ok = await check_ingredient_exists(flow, fname.split(".")[0])
        if not ok:
            missing.append(os.path.join(d, fname))

    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)
    if not missing:
        print("All required reference & 6 plates already uploaded!")
        return

    print(f"Uploading {len(missing)} plates silently...")
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
                raise RuntimeError("fileChooserOpened did not fire!")
            mode = fc_ev["params"].get("mode", "")
            if mode == "selectMultiple":
                batch_files = missing[idx:]
                idx = len(missing)
            else:
                batch_files = [missing[idx]]
                idx += 1
            print(f"  Setting {len(batch_files)} file(s) (mode={mode})...")
            await flow.call("DOM.setFileInputFiles", {
                "files": batch_files,
                "backendNodeId": fc_ev["params"]["backendNodeId"],
            })
            # Wait until upload % indicators finish
            last_base = os.path.basename(batch_files[-1]).split(".")[0]
            for _ in range(30):
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
                if cards and not pct:
                    print(f"  ✅ Uploaded through {last_base}!")
                    break
    finally:
        await flow.call("Page.setInterceptFileChooserDialog", {"enabled": False})


async def attach_ingredient_exact(flow, filename):
    stem = filename.split(".")[0]
    await flow.js("""
    (() => {
        if (!document.querySelector('[role="option"]')) {
            document.querySelector('[aria-label="Thêm thành phần vào ô nhập câu lệnh"]')?.click();
        }
    })()
    """)
    await asyncio.sleep(0.8)

    await flow.js(f"""
    (() => {{
        const inp = document.querySelector('[aria-label="Tìm kiếm thành phần"]');
        if (!inp) return;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(inp, {json.dumps(stem)});
        inp.dispatchEvent(new Event('input', {{bubbles: true}}));
    }})()
    """)
    await asyncio.sleep(0.55)

    async def inspect_dialog():
        return await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(stem)};
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            let targetOpt = null;
            for (const el of opts) {{
                const txt = (el.innerText || '').trim();
                const img = el.querySelector('img');
                const src = img?.src || '';
                if (txt.includes(idStr) || src.includes(idStr)) {{
                    el.scrollIntoView({{block: 'center'}});
                    const r = (img || el).getBoundingClientRect();
                    targetOpt = {{
                        txt: txt.replace(/\\s+/g, ' ').slice(0, 70),
                        uuid: src.split('?')[0].split('/').pop(),
                        cx: Math.round(r.x + r.width / 2),
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
                        .filter(i => !i.closest('[role="option"]') && i.getBoundingClientRect().width > 120)
                        .map(i => (i.src || '').split('?')[0]);
                }}
            }}
            return {{targetOpt, hasAddBtn: Boolean(addBtn), previewSrcs, allOpts: opts.map(o => (o.innerText||'').trim().slice(0,50))}};
        }})()
        """)

    st = await inspect_dialog()
    if not st["targetOpt"]:
        raise RuntimeError(f"Ingredient {filename!r} not found! Visible: {st['allOpts']}")

    target_uuid = st["targetOpt"]["uuid"]
    is_previewed = any(target_uuid in u for u in st["previewSrcs"]) and st["hasAddBtn"]
    if not is_previewed:
        await asyncio.sleep(0.2)
        st = await inspect_dialog()
        await flow.trusted_click(st["targetOpt"]["cx"], st["targetOpt"]["cy"])
        await asyncio.sleep(0.55)
        st2 = await inspect_dialog()
        if not any(target_uuid in u for u in st2["previewSrcs"]):
            await flow.trusted_click(st["targetOpt"]["cx"] + 40, st["targetOpt"]["cy"])
            await asyncio.sleep(0.55)
            st2 = await inspect_dialog()
        if not any(target_uuid in u for u in st2["previewSrcs"]):
            raise RuntimeError(f"Could not preview {filename!r} ({target_uuid})")

    await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
    await asyncio.sleep(0.55)

    chip_uuids = await flow.js("""
    Array.from(document.querySelectorAll('button[aria-label="Thành phần"] img'))
        .map(i => (i.src || '').split('?')[0].split('/').pop())
    """)
    if target_uuid not in chip_uuids:
        raise RuntimeError(f"Chip mismatch for {filename}: expected {target_uuid} in {chip_uuids}")
    print(f"  + Attached {stem} ({target_uuid[:8]})")


async def get_rendered_uuids(flow):
    imgs = await flow.js("""
    Array.from(document.querySelectorAll('img'))
        .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth}))
        .filter(i => i.src.includes('flow-content.google/image/') && i.nw >= 700)
    """)
    return {im["src"].split("?")[0] for im in imgs}


async def submit_scene(flow, sc, wait_for_render=True):
    print(f"\n=== SUBMITTING {sc['key']} ===")
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.25)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
    await asyncio.sleep(0.25)
    await flow.ensure_image_16x9_pro()
    await clear_composer_strict(flow)

    before_uuids = await get_rendered_uuids(flow)

    for ref in sc["refs"]:
        await attach_ingredient_exact(flow, ref)

    ed_rect = await flow.js("""
    (() => {
        const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
        const r = el.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    await flow.trusted_click(ed_rect["cx"], ed_rect["cy"])
    await asyncio.sleep(0.15)
    await flow.call("Input.insertText", {"text": sc["prompt"]})
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
        raise RuntimeError(f"Submit button not ready for {sc['key']}: {btns}")
    await flow.trusted_click(target["cx"], target["cy"])
    print(f"  🚀 Queued {sc['key']}!")

    if not wait_for_render:
        await asyncio.sleep(1.5)
        return

    for step in range(45):
        await asyncio.sleep(2.0)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
        cur_uuids = await get_rendered_uuids(flow)
        if len(cur_uuids - before_uuids) >= 1:
            print(f"  ✅ Rendered {sc['key']} in {(step+1)*2}s!")
            return
    print(f"  ⚠️ Timeout waiting for {sc['key']}, continuing...")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["check1", "rest9", "all10"], default="check1")
    args = parser.parse_args()

    tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list").read())
    t = next((x for x in tabs if PROJECT_ID in (x.get("url") or "")), None)
    if not t:
        raise RuntimeError(f"Flow tab for project {PROJECT_ID} not found!")

    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=30 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        # CRITICAL: Silent background focus emulation ONLY — NEVER call Page.bringToFront!
        await flow.call("Page.enable")
        await flow.call("DOM.enable")
        await flow.call("Emulation.setFocusEmulationEnabled", {"enabled": True})

        await upload_missing_plates(flow, ws)

        if args.phase == "check1":
            await submit_scene(flow, SCENES_10[0], wait_for_render=True)
            await asyncio.sleep(1.5)
            res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 85})
            p = os.path.join(OUT_DIR, "qa_batch10_check1.jpg")
            with open(p, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("Saved check1 QA screenshot:", p)
        elif args.phase == "rest9":
            # Submit in waves of 3 concurrent jobs so Google Flow Ultra renders 3x faster!
            rest = SCENES_10[1:]
            for w_idx in range(0, len(rest), 3):
                wave = rest[w_idx:w_idx + 3]
                before_wave = await get_rendered_uuids(flow)
                for i, sc in enumerate(wave):
                    await submit_scene(flow, sc, wait_for_render=False)
                print(f"  Waiting for wave {w_idx//3 + 1} ({len(wave)} images) to finish rendering...")
                for step in range(55):
                    await asyncio.sleep(2.0)
                    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
                    cur = await get_rendered_uuids(flow)
                    done_n = len(cur - before_wave)
                    if done_n >= len(wave):
                        print(f"  ✅ Wave {w_idx//3 + 1} finished ({done_n}/{len(wave)}) in {(step+1)*2}s!")
                        break
            await asyncio.sleep(6.0)
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
            await asyncio.sleep(1.0)
            res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
            p = os.path.join(OUT_DIR, "qa_batch10_top6.jpg")
            with open(p, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            # Scroll main gallery container down by 520px to inspect the remaining 4 cards of the 10-image batch
            await flow.js("""
            (() => {
                const scrollers = Array.from(document.querySelectorAll('div, main')).filter(el => el.scrollHeight > el.clientHeight + 200);
                for (const s of scrollers) s.scrollTop = 520;
                window.scrollTo(0, 520);
            })()
            """)
            await asyncio.sleep(1.0)
            res2 = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
            p2 = os.path.join(OUT_DIR, "qa_batch10_bot4.jpg")
            with open(p2, "wb") as f:
                f.write(base64.b64decode(res2["data"]))
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
            print("Saved final batch10 QA screenshots:", p, p2)


if __name__ == "__main__":
    asyncio.run(main())
