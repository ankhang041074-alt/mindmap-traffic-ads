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

SCENES_BATCH2_10 = [
    {
        "key": "S11_PORCH_LIMESTONE_ARCH_OAK_DOORS",
        "refs": ["PLATE_01_PAIR_HALFDOOR_45PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 35mm-50mm live-action Kodak Vision3 250D sunlit Santa Barbara Mediterranean villa front entrance: centered between both plants is a grand 2.45-meter arched natural white-oak "
            "double front door set deep inside a carved warm-cream limestone archway, hand-forged matte-black ring door handles aligned strictly at plant-top height (1/2 door scale), "
            "honed limestone porch threshold step with an unmarked woven jute doormat, softly blurred foreground olive-branch greenery bokeh bottom-left, warm late-afternoon raking golden sunlight "
            "casting dappled tree-canopy shadows across the textured limestone masonry, clean natural daylight on both plants, realistic stone contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S12_SUNROOM_WINDOW_BENCH_TERRACOTTA",
        "refs": ["PLATE_04_SINGLE_HERO_LEFT_68PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sun-drenched architectural conservatory sunroom: extending to the right of the plant is a built-in 50cm natural white-oak window bench seat "
            "topped with a cream linen cushion and neutral woven pillows (reaching well below mid-plant height to lock true 4ft scale), tall thin-framed white-oak mullioned windows behind "
            "revealing softly blurred sunlit garden greenery outside, pale matte terracotta floor tiles with realistic planter contact shadow, softly blurred foreground woven rattan coffee table edge "
            "bottom-right, crisp morning sunbeams slanting through the window mullions onto the bench and floor, clean natural daylight on the plant, zero text."
        ),
    },
    {
        "key": "S13_COURTYARD_LOGGIA_POOL_COLONNADE",
        "refs": ["PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm live-action Kodak Vision3 250D luxury Mediterranean resort villa courtyard loggia viewed at a natural 20-degree three-quarter diagonal perspective matching the staggered depth "
            "of the two plants: warm cream honed travertine terrace steps leading out toward a calm sunlit turquoise courtyard lap pool and low teak sun-loungers softly defocused in the background, "
            "tall warm-ivory limewash plaster colonnade pillars flanking the walkway, warm golden-hour afternoon sunlight raking diagonally across the travertine paving with subtle shimmering water light "
            "on the plaster pillars, clean natural daylight on both plants, realistic long floor contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S14_KITCHEN_MARBLE_ISLAND_SLIDING_GLASS",
        "refs": ["PLATE_05_SINGLE_HERO_RIGHT_66PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sunlit open-concept luxury kitchen corner: on the left sits the waterfall edge of a 90cm warm Calacatta-marble and fluted white-oak kitchen island "
            "(reaching three-quarters up the plant) paired with a tan saddle-leather and oak counter stool, behind the plant is a tall slim black-steel sliding glass patio door continuing past the top edge "
            "of the frame opening onto a sunlit stone garden terrace, wide-plank European white-oak floor with realistic planter contact shadow, softly blurred foreground oak breakfast table corner "
            "with a matte ceramic pitcher bottom-left, warm afternoon sun-slashes raking across the oak floor, clean natural daylight on the plant, zero text."
        ),
    },
    {
        "key": "S15_GALLERY_ARCHWAY_WAINSCOTING_PORTAL",
        "refs": ["PLATE_02_PAIR_MEDIUM_HERO_56PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm medium-shot live-action Kodak Vision3 250D sunlit modern-classic architectural interior gallery hallway: centered between both plants is a wide plastered arched interior doorway "
            "whose upper arch extends past the top edge of the 16:9 frame, looking into a sun-drenched living room with tall casement windows and a cream linen sofa in soft background depth; "
            "warm ivory walls finished with 95cm classic raised-panel wainscoting reaching three-quarters up both plants, French herringbone oak parquet floor, softly blurred foreground doorway casing edge "
            "on the far right, bright afternoon window sunbeams streaming through the sunlit back room across the oak floor, clean daylight on both plants, realistic contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S16_BEDROOM_BALCONY_CURTAINS_LOUNGE_CHAIR",
        "refs": ["PLATE_04_SINGLE_HERO_LEFT_68PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D serene sunlit primary bedroom sitting corner: behind the left side of the plant hang tall sheer warm-ivory linen curtains beside an open timber-framed "
            "French balcony door continuing past the top edge of the frame, on the right sits a low 72cm oatmeal-linen upholstered accent lounge chair (reaching slightly above mid-plant height) "
            "and a small solid-oak round side table over a handwoven cream wool rug and pale oak plank floor, softly blurred foreground linen bed-throw edge bottom-right, golden morning sunlight "
            "filtering softly through the sheer curtains across the plaster wall and rug, realistic floor contact shadow under the planter, clean natural daylight on the plant, zero text."
        ),
    },
    {
        "key": "S17_COURTYARD_ARCHED_OAK_WINDOW_STONE",
        "refs": ["PLATE_02_PAIR_MEDIUM_HERO_56PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm medium-shot live-action Kodak Vision3 250D sunlit European garden courtyard terrace: centered between both plants is a tall arched natural-oak mullioned casement window "
            "set into warm honey-cream limestone masonry with a low 45cm carved stone sill aligned near planter-rim height, weathered natural limestone courtyard flagstones underfoot, "
            "softly blurred foreground cream wrought-iron garden chair back bottom-left, warm late-afternoon dappled courtyard tree-canopy sunlight casting organic leaf-filtered light patterns "
            "across the limestone wall and glass panes, clean natural daylight on both plants, realistic stone contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S18_SPA_BATHROOM_FREESTANDING_TUB_SUNLIGHT",
        "refs": ["PLATE_05_SINGLE_HERO_RIGHT_66PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sun-filled organic-modern luxury spa bathroom: the plant stands in a dry sunlit architectural corner beside a tall natural-oak framed window "
            "continuing past the top edge of the frame revealing softly blurred sunlit olive-and-bamboo private courtyard greenery; on the left sits the curved end of a 60cm matte-white sculpted stone "
            "freestanding soaking tub (reaching halfway up the 4ft plant) beside a small natural teak stool with folded white linen towels, warm sand-toned tadelakt plaster walls and honed travertine stone floor, "
            "bright morning sunbeams slanting across the plaster wall and tub rim, realistic floor contact shadow under the planter, clean natural daylight on the plant, zero text."
        ),
    },
    {
        "key": "S19_ROOFTOP_TERRACE_TEAK_DECK_GOLDEN_HOUR",
        "refs": ["PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm live-action Kodak Vision3 250D upscale sunlit hillside penthouse terrace balcony viewed at a natural 20-degree three-quarter diagonal perspective matching the staggered depth "
            "of the two plants: warm natural teak wood decking underfoot, a 1.10-meter cream architectural stone-and-clear-glass balcony parapet running behind the two plants just below their top tips, "
            "sunlit lush coastal hillside greenery glowing in soft golden-hour bokeh in the distance, softly blurred foreground outdoor cream linen sofa arm bottom-right, warm low late-afternoon golden sun "
            "raking across the teak deck planks, clean natural daylight on both plants, realistic long floor contact shadows under both planters, zero text."
        ),
    },
    {
        "key": "S20_COASTAL_GREAT_ROOM_OCEAN_WINDOWS",
        "refs": ["PLATE_06_SINGLE_WIDE_ROOM_50PCT_16x9.jpg", "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 35mm-50mm live-action Kodak Vision3 250D sunlit California coastal hillside living room with a 3.3-meter white-oak beamed ceiling: the plant stands naturally beside slim dark-bronze framed "
            "panoramic windows overlooking sunlit coastal hillside greenery and a calm distant Pacific ocean horizon; on the left sits a generous 75cm cream linen sectional sofa and low solid-oak coffee table "
            "resting on a woven natural jute rug over warm wide-plank oak flooring, consistent late-afternoon sunlight entering from the ocean-facing windows casting natural window-mullion light patterns "
            "across the floor and sofa, realistic floor contact shadow under the planter, clean natural daylight on the plant, zero text."
        ),
    },
]

FORBIDDEN_WORDS = ("cedar", "pine ", "pine,", "pine.", "topiary", "slender", "teardrop", "chartreuse", "conifer", "spruce", "cypress")
for _sc in SCENES_10 + SCENES_BATCH2_10:
    _low = _sc["prompt"].lower()
    # Allow "spiky pine needles" inside the explicit negative lock "DO NOT redraw or alter the leaves into spiky pine needles"
    _body = _low.replace("do not redraw or alter the leaves into spiky pine needles", "")
    for _fw in FORBIDDEN_WORDS:
        if _fw in _body:
            raise ValueError(f"Forbidden word {_fw!r} found in {_sc['key']}!")


KNOWN_PLATE_UUIDS = {
    "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg": "96a57777-a359-4546-a363-756a1f5ccd73",
    "PLATE_01_PAIR_HALFDOOR_45PCT_16x9.jpg": "5aae13ec-4112-4ba8-aede-fb6762e83210",
    "PLATE_02_PAIR_MEDIUM_HERO_56PCT_16x9.jpg": "cc3942a3-2658-4ba9-82db-9ea5df94939f",
    "PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg": "fac94f0b-7394-4520-8f36-41232fbf67a2",
    "PLATE_04_SINGLE_HERO_LEFT_68PCT_16x9.jpg": "dc2fce54-5c3a-4179-9abc-c1670f98d6c0",
    "PLATE_05_SINGLE_HERO_RIGHT_66PCT_16x9.jpg": "b1b5b5eb-f77b-4c1b-9b28-d29493285231",
    "PLATE_06_SINGLE_WIDE_ROOM_50PCT_16x9.jpg": "af938552-9103-46c2-84c8-3bb0716f0140",
}


async def open_ingredient_modal(flow):
    has_opts = await flow.js("document.querySelectorAll('[role=\"option\"]').length > 0")
    if not has_opts:
        await flow.find_and_trusted_click("aria === 'Thêm thành phần vào ô nhập câu lệnh'", "open '+' modal")
        await asyncio.sleep(0.85)


async def scan_all_project_options(flow, max_steps=30):
    await open_ingredient_modal(flow)
    await flow.js("""
    (() => {
        const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
        if (vp) vp.scrollTop = 0;
    })()
    """)
    await asyncio.sleep(0.35)
    found = {}
    for _ in range(max_steps):
        items = await flow.js("""
        Array.from(document.querySelectorAll('[role="option"]')).map(el => ({
            txt: (el.innerText || '').trim().replace(/\\s+/g, ' '),
            uuid: (el.querySelector('img')?.src || '').split('?')[0].split('/').pop()
        }))
        """)
        for it in items:
            if it["uuid"] and it["uuid"] not in found:
                found[it["uuid"]] = it["txt"]
        moved = await flow.js("""
        (() => {
            const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
            if (!vp) return false;
            const prev = vp.scrollTop;
            vp.scrollTop += 320;
            return vp.scrollTop > prev;
        })()
        """)
        if not moved:
            break
        await asyncio.sleep(0.25)
    return found


async def upload_missing_plates(flow, ws):
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)

    all_opts = await scan_all_project_options(flow, max_steps=32)
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)

    required_files = [(REF_DIR, "CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg")] + [(PLATE_DIR, p) for p in PLATES]
    missing = []
    for d, fname in required_files:
        stem = fname.split(".")[0]
        known_u = KNOWN_PLATE_UUIDS.get(fname, "")
        matched_u = next(
            (u for u, txt in all_opts.items() if (known_u and known_u in u) or (stem in txt)),
            None,
        )
        if matched_u:
            KNOWN_PLATE_UUIDS[fname] = matched_u
        else:
            missing.append((fname, os.path.join(d, fname)))

    if not missing:
        print("All required reference & 6 plates verified with UUIDs!")
        return

    print(f"Uploading {len(missing)} missing plate/ref file(s) silently: {[m[0] for m in missing]}...")
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
                batch_entries = missing[idx:]
                idx = len(missing)
            else:
                batch_entries = [missing[idx]]
                idx += 1
            batch_files = [m[1] for m in batch_entries]
            print(f"  Setting {len(batch_files)} file(s) (mode={mode})...")
            await flow.call("DOM.setFileInputFiles", {
                "files": batch_files,
                "backendNodeId": fc_ev["params"]["backendNodeId"],
            })
            last_base = os.path.basename(batch_files[-1]).split(".")[0]
            for _ in range(35):
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

    await asyncio.sleep(1.0)
    refreshed = await scan_all_project_options(flow, max_steps=12)
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)
    for fname, _ in missing:
        stem = fname.split(".")[0]
        matched_u = next((u for u, txt in refreshed.items() if stem in txt), None)
        if matched_u:
            KNOWN_PLATE_UUIDS[fname] = matched_u
            print(f"  📌 Registered UUID for {fname}: {matched_u}")


async def attach_ingredient_exact(flow, filename):
    stem = filename.split(".")[0]
    known_uuid = KNOWN_PLATE_UUIDS.get(filename, "")
    await open_ingredient_modal(flow)

    # Reset virtual scroll to top and scan downward in 280px steps matching either stem or known_uuid
    await flow.js("""
    (() => {
        const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
        if (vp) vp.scrollTop = 0;
    })()
    """)
    await asyncio.sleep(0.3)

    async def find_visible_match():
        return await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(stem)};
            const ku = {json.dumps(known_uuid)};
            const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
            const vpRect = vp ? vp.getBoundingClientRect() : null;
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const txt = (el.innerText || '').trim();
                const img = el.querySelector('img');
                const src = img?.src || '';
                const uuid = src.split('?')[0].split('/').pop();
                if ((idStr && txt.includes(idStr)) || (ku && src.includes(ku))) {{
                    if (vp && vpRect) {{
                        const er = el.getBoundingClientRect();
                        vp.scrollTop += (er.top + er.height / 2) - (vpRect.top + vpRect.height / 2);
                    }}
                    return {{matched: true, uuid}};
                }}
            }}
            return {{matched: false, uuid: ''}};
        }})()
        """)

    hit = False
    for _ in range(38):
        m = await find_visible_match()
        if m["matched"]:
            await asyncio.sleep(0.35)  # Allow lazy img.src & centered bounding rect to settle!
            hit = True
            break
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

    if not hit:
        raise RuntimeError(f"Ingredient {filename!r} (uuid={known_uuid!r}) not found in virtual scroll list!")

    async def inspect_dialog():
        return await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(stem)};
            const ku = {json.dumps(known_uuid)};
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            let targetOpt = null;
            for (const el of opts) {{
                const txt = (el.innerText || '').trim();
                const img = el.querySelector('img');
                const src = img?.src || '';
                if ((idStr && txt.includes(idStr)) || (ku && src.includes(ku))) {{
                    const r = (img && img.getBoundingClientRect().width > 10 ? img : el).getBoundingClientRect();
                    targetOpt = {{
                        txt: txt.replace(/\\s+/g, ' ').slice(0, 70),
                        uuid: src.split('?')[0].split('/').pop(),
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
    if not st["targetOpt"] or not st["targetOpt"]["uuid"]:
        raise RuntimeError(f"Ingredient {filename!r} matched but img.src uuid still empty: {st}")

    target_uuid = st["targetOpt"]["uuid"]
    KNOWN_PLATE_UUIDS[filename] = target_uuid

    is_previewed = any(target_uuid in u for u in st["previewSrcs"]) and st["hasAddBtn"]
    if not is_previewed:
        for dx in (0, 55, 105):
            st_cur = await inspect_dialog()
            if not st_cur["targetOpt"]:
                break
            await flow.trusted_click(st_cur["targetOpt"]["cx"] + dx, st_cur["targetOpt"]["cy"])
            for _ in range(6):
                await asyncio.sleep(0.3)
                st2 = await inspect_dialog()
                if any(target_uuid in u for u in st2["previewSrcs"]) and st2["hasAddBtn"]:
                    is_previewed = True
                    break
            if is_previewed:
                break
        if not is_previewed:
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


async def exit_edit_view_if_needed(flow):
    href = await flow.js("window.location.href")
    if "/edit/" in (href or ""):
        await flow.find_and_trusted_click("aria === 'Nút quay lại để quay về trang trước'", "exit /edit/ view")
        await asyncio.sleep(1.0)


async def switch_gallery_to_images_once(flow):
    await exit_edit_view_if_needed(flow)
    img_tab = await flow.js("""
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="tab"]')).filter(b => {
            const r = b.getBoundingClientRect();
            const txt = (b.innerText || '').trim();
            return r.width > 0 && r.x < 260 && r.y > 60 && r.y < 260 && txt.includes('Hình ảnh');
        });
        if (!btns.length) return null;
        const r = btns[0].getBoundingClientRect();
        return {cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)};
    })()
    """)
    if img_tab:
        await flow.trusted_click(img_tab["cx"], img_tab["cy"])
        await asyncio.sleep(0.5)


async def ensure_gallery_and_image_mode(flow):
    await exit_edit_view_if_needed(flow)
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.25)

    pill = await flow.js("(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]')?.innerText || '').trim()")
    has_plus = await flow.js("Boolean(document.querySelector('[aria-label=\"Thêm thành phần vào ô nhập câu lệnh\"]'))")
    if "Nano Banana Pro" in pill and "crop_16_9" in pill and "x1" in pill and has_plus:
        return

    await switch_gallery_to_images_once(flow)

    is_open = await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))")
    if not is_open:
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "open settings pill")
        await asyncio.sleep(0.45)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('Hình ảnh')", "Hình ảnh radio")
    await asyncio.sleep(0.4)
    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('16:9')", "16:9 radio")
    await asyncio.sleep(0.3)

    already_pro = await flow.js("""
    Array.from(document.querySelectorAll('button, [role="button"]')).some(b => {
        const r = b.getBoundingClientRect();
        return r.width > 0 && r.y > 480 && r.y < 820 && (b.innerText || '').includes('Nano Banana Pro');
    })
    """)
    if not already_pro:
        await flow.find_and_trusted_click("(text.includes('Nano Banana') || text.includes('Imagen')) && r.y > 480 && r.y < 820", "image model dropdown")
        await asyncio.sleep(0.4)
        await flow.find_and_trusted_click("el.getAttribute('role') === 'menuitem' && text.includes('Nano Banana Pro')", "Nano Banana Pro")
        await asyncio.sleep(0.3)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === 'x1'", "x1 radio")
    await asyncio.sleep(0.3)

    if await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))"):
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "close settings pill")
        await asyncio.sleep(0.4)


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
    await ensure_gallery_and_image_mode(flow)
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
        await asyncio.sleep(1.8)
        return

    for step in range(45):
        await asyncio.sleep(2.0)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
        cur_uuids = await get_rendered_uuids(flow)
        if len(cur_uuids - before_uuids) >= 1:
            print(f"  ✅ Rendered {sc['key']} in {(step+1)*2}s!")
            return
    print(f"  ⚠️ Timeout waiting for {sc['key']}, continuing...")


async def run_waves(flow, scenes, tag):
    for w_idx in range(0, len(scenes), 3):
        wave = scenes[w_idx:w_idx + 3]
        before_wave = await get_rendered_uuids(flow)
        for sc in wave:
            await submit_scene(flow, sc, wait_for_render=False)
        print(f"  Waiting for {tag} wave {w_idx//3 + 1} ({len(wave)} images) to finish rendering...")
        for step in range(60):
            await asyncio.sleep(2.0)
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
            cur = await get_rendered_uuids(flow)
            pcts = await flow.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            done_n = len(cur - before_wave)
            if done_n >= len(wave) and not pcts:
                print(f"  ✅ Wave {w_idx//3 + 1} finished ({done_n}/{len(wave)}) in {(step+1)*2}s!")
                break
    await asyncio.sleep(5.0)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
    await asyncio.sleep(1.0)
    res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
    p = os.path.join(OUT_DIR, f"qa_{tag}_top6.jpg")
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
    p2 = os.path.join(OUT_DIR, f"qa_{tag}_bot4.jpg")
    with open(p2, "wb") as f:
        f.write(base64.b64decode(res2["data"]))
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
    print(f"Saved final {tag} QA screenshots:", p, p2)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", choices=["batch1", "batch2"], default="batch2")
    parser.add_argument("--phase", choices=["check1", "rest9", "all10", "slice"], default="all10")
    parser.add_argument("--start-index", type=int, default=0)
    args = parser.parse_args()

    scenes = SCENES_10 if args.batch == "batch1" else SCENES_BATCH2_10
    tag = "batch10" if args.batch == "batch1" else "batch2_10"

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

        await switch_gallery_to_images_once(flow)
        await ensure_gallery_and_image_mode(flow)
        await upload_missing_plates(flow, ws)

        if args.phase == "check1":
            await submit_scene(flow, scenes[0], wait_for_render=True)
            await asyncio.sleep(1.5)
            res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 85})
            p = os.path.join(OUT_DIR, f"qa_{tag}_check1.jpg")
            with open(p, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("Saved check1 QA screenshot:", p)
        elif args.phase == "rest9":
            await run_waves(flow, scenes[1:], tag)
        elif args.phase == "slice":
            await run_waves(flow, scenes[args.start_index:], tag)
        elif args.phase == "all10":
            await run_waves(flow, scenes, tag)


if __name__ == "__main__":
    asyncio.run(main())
