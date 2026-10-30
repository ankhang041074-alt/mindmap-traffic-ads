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
OUT_DIR = "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/barrel_cedar_20"
PLATE_DIR = os.path.join(OUT_DIR, "plates_2k")
REF_DIR = os.path.join(OUT_DIR, "clean_refs")
UUID_CACHE_PATH = os.path.join(OUT_DIR, "barrel_plate_uuids.json")

PLATES = [
    "BARREL_PLATE_01_PAIR_DOOR_52PCT_16x9.jpg",
    "BARREL_PLATE_02_PAIR_MEDIUM_62PCT_16x9.jpg",
    "BARREL_PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg",
    "BARREL_PLATE_04_SINGLE_HERO_LEFT_72PCT_16x9.jpg",
    "BARREL_PLATE_05_SINGLE_HERO_RIGHT_70PCT_16x9.jpg",
    "BARREL_PLATE_06_SINGLE_WIDE_55PCT_16x9.jpg",
    "BARREL_PLATE_07_SINGLE_WIDE_RIGHT_36PCT_16x9.jpg",
    "BARREL_PLATE_08_SINGLE_COASTAL_RIGHT_56PCT_16x9.jpg",
    "BARREL_PLATE_09_SINGLE_HERO_RIGHT_76PCT_16x9.jpg",
]

PAIR_LOCK = (
    "Edit this 16:9 product photograph (using the second 1024x1024 reference image for close-up molded leaf sprig and rustic wooden barrel planter detail): "
    "keep BOTH potted artificial plants and their weathered grey-brown wooden stave barrel planters with three horizontal riveted matte-black metal hoops "
    "100% pixel-identical to the 16:9 plate in exact position, height, barrel width-to-height proportions, three black metal bands with rivets, "
    "tall conical outer contour, and dense natural green molded plastic leaf texture — DO NOT change the wooden barrel planters into plain pots, "
    "DO NOT remove or alter the three black metal hoops, DO NOT widen or slim the plant silhouettes, and DO NOT redraw or alter the leaves into spiky pine needles. "
    "Replace ONLY the pure white background with "
)

STRICT_SINGLE_CUTOUT_LOCK = (
    "Edit this 16:9 product photograph (using the second 1024x1024 close-up reference image for exact fine lacy flat-fan foliage sprigs, "
    "delicate airy feathery outer branchlet tips, and weathered grey-brown wooden stave barrel planter detail): "
    "treat the potted plant and wooden barrel in the 16:9 plate as an untouched locked foreground photograph cutout — "
    "keep every single fine flat-fan leaf sprig, delicate lacy outer branch edge, smooth tapered conical contour, full foliage width, full barrel width and height, "
    "and three horizontal riveted matte-black metal hoops 100% pixel-identical to the 16:9 plate without shrinking, narrowing, clumping, thickening, or redrawing any leaf or barrel pixels. "
    "Outpaint ONLY the pure white background with "
)

SINGLE_LOCK = STRICT_SINGLE_CUTOUT_LOCK

SCENES_20 = [
    {
        "key": "B01_PORCH_CHARCOAL_DOOR_STONE_COLUMNS",
        "refs": ["BARREL_PLATE_01_PAIR_DOOR_52PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 35mm-50mm live-action Kodak Vision3 250D sunlit luxury front porch: centered between both plants is a tall 2.4-meter matte-charcoal 4-panel front door "
            "with a brushed-brass handle positioned ~18cm below the pointed top tips of both plants (locking true 4ft+ scale slightly above the door handle), "
            "flanked by classic warm-cream limestone porch columns and pale stucco walls, honed grey bluestone porch steps with a plain unmarked natural coir doormat, "
            "softly blurred foreground garden foliage bokeh bottom-right, warm late-afternoon raking golden sunlight casting soft column shadows, "
            "clean natural daylight on both plants and wooden barrels, realistic stone contact shadows under both barrel bases, zero text."
        ),
    },
    {
        "key": "B02_PORCH_FARMHOUSE_BOARD_BATTEN_3Q",
        "refs": ["BARREL_PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm live-action Kodak Vision3 250D modern American farmhouse front porch viewed at a natural 20-degree three-quarter diagonal perspective matching "
            "the staggered depth of the two plants: crisp warm-white painted board-and-batten wood siding, a tall 2.4-meter natural white-oak glass-paned front door "
            "angled between the nearer left plant and farther right plant with its matte-black handle positioned ~18cm below plant-top height, weathered brick-and-bluestone "
            "porch steps with an unmarked woven jute mat, warm golden-hour sunlight casting diagonal porch-beam shadows across the white siding, "
            "clean natural daylight on both plants and wooden barrels, realistic floor contact shadows, zero text."
        ),
    },
    {
        "key": "B03_FIREPLACE_CARVED_LIMESTONE_LIVING",
        "refs": ["BARREL_PLATE_01_PAIR_DOOR_52PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 35mm-50mm live-action Kodak Vision3 250D soaring 3.3-meter high-ceilinged sunlit living room: centered between both plants is a hand-carved warm-cream "
            "French limestone fireplace whose 1.15m mantel shelf sits ~12cm below the pointed top tips of both plants, surmounted by an arched antique-brass mirror "
            "and warm Roman plaster walls, herringbone white-oak parquet floor, softly blurred foreground cream linen sofa arm bottom-left, "
            "warm diagonal afternoon window sunbeams across the plaster wall, clean natural daylight on both plants and wooden barrels, realistic floor contact shadows, zero text."
        ),
    },
    {
        "key": "B04_PATIO_BLACK_FRENCH_DOORS_FLAGSTONE",
        "refs": ["BARREL_PLATE_02_PAIR_MEDIUM_62PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm medium-shot live-action Kodak Vision3 250D sunlit backyard stone terrace: centered between both plants are tall black-steel framed French double glass patio doors "
            "whose upper glass panes extend past the top edge of the 16:9 frame (aged-brass lever handles positioned ~18cm below the plant tips to lock true 4ft+ scale), "
            "warm cream Mediterranean limewash walls, natural beige flagstone patio pavers underfoot, softly blurred foreground teak outdoor lounge arm bottom-left, "
            "warm afternoon sun-slashes across the wall and stone, clean daylight on both plants and wooden barrels, realistic contact shadows, zero text."
        ),
    },
    {
        "key": "B05_COURTYARD_FOUNTAIN_TERRACOTTA_3Q",
        "refs": ["BARREL_PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm live-action Kodak Vision3 250D sunlit Santa Barbara Mediterranean villa courtyard viewed at a natural 20-degree three-quarter diagonal perspective "
            "matching the staggered depth of the two plants: warm travertine courtyard flagstones leading past a low 55cm carved limestone courtyard water-basin fountain "
            "and sunlit olive-tree arches softly defocused in the background, warm honey-cream plaster colonnade wall, golden-hour late-afternoon sun raking diagonally "
            "across the stone paving, clean natural daylight on both plants and wooden barrels, realistic long contact shadows, zero text."
        ),
    },
    {
        "key": "B06_FOYER_RECLAIMED_OAK_CONSOLE",
        "refs": ["BARREL_PLATE_02_PAIR_MEDIUM_62PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm medium-shot live-action Kodak Vision3 250D sunlit farmhouse-luxury entryway foyer: centered between both plants is an 85cm solid natural white-oak "
            "console table (reaching two-thirds up both plants) styled with a matte stoneware bowl, with a large minimalist neutral linen framed artwork hanging on the warm "
            "cream plaster wall above it, wide-plank European oak flooring, warm afternoon side-window sunbeams raking across the wall and floor, "
            "clean natural daylight on both plants and wooden barrels, realistic floor contact shadows, zero text."
        ),
    },
    {
        "key": "B07_PORCH_STONE_ARCH_WALNUT_DOORS",
        "refs": ["BARREL_PLATE_01_PAIR_DOOR_52PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 35mm-50mm live-action Kodak Vision3 250D sunlit European country-estate front entrance: centered between both plants is a grand 2.45-meter arched natural dark-walnut "
            "double front door recessed inside a carved honey-cream limestone archway, forged matte-black ring handles positioned ~18cm below the plant tips, "
            "limestone threshold step with an unmarked woven jute doormat, softly blurred foreground olive-branch greenery bokeh bottom-left, "
            "warm late-afternoon dappled tree-canopy shadows dancing across the limestone masonry, clean natural daylight on both plants and wooden barrels, realistic shadows, zero text."
        ),
    },
    {
        "key": "B08_COURTYARD_ARCHED_OAK_WINDOW_STONE",
        "refs": ["BARREL_PLATE_02_PAIR_MEDIUM_62PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm medium-shot live-action Kodak Vision3 250D sunlit Napa Valley stone garden courtyard: centered between both plants is a tall arched natural-oak mullioned "
            "casement window set into warm honey-cream dressed limestone masonry with a low 40cm carved stone sill aligned near upper-barrel height, weathered courtyard flagstones, "
            "softly blurred foreground wrought-iron bistro chair back bottom-left, warm late-afternoon dappled courtyard tree sunlight across the stone wall, "
            "clean natural daylight on both plants and wooden barrels, realistic stone contact shadows, zero text."
        ),
    },
    {
        "key": "B09_TERRACE_PERGOLA_TEAK_DECK_3Q",
        "refs": ["BARREL_PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm live-action Kodak Vision3 250D sunlit timber-pergola backyard deck viewed at a natural 20-degree three-quarter diagonal perspective matching the staggered depth "
            "of the two plants: warm natural teak wood decking and a wide limestone garden step leading out toward sunlit backyard greenery and low outdoor linen lounge chairs "
            "in soft golden-hour bokeh, overhead timber pergola casting warm diagonal sun-and-shadow stripes across the wood deck, softly blurred foreground outdoor cream cushion arm "
            "bottom-right, clean natural daylight on both plants and wooden barrels, realistic contact shadows, zero text."
        ),
    },
    {
        "key": "B10_GALLERY_ARCHED_PORTAL_WAINSCOTING",
        "refs": ["BARREL_PLATE_02_PAIR_MEDIUM_62PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": PAIR_LOCK + (
            "a 50mm medium-shot live-action Kodak Vision3 250D sunlit modern-classic interior gallery hallway: centered between both plants is a wide plastered arched interior doorway "
            "looking deep into a sun-drenched living room with tall casement windows and a cream linen sofa; warm ivory walls with 90cm classic raised-panel wainscoting "
            "(reaching ~70% up both plants), French herringbone oak floor, softly blurred foreground doorway frame edge on the far right, bright afternoon sunbeams streaming "
            "from the back room across the oak floor, clean daylight on both plants and wooden barrels, realistic floor contact shadows, zero text."
        ),
    },
    {
        "key": "B11_VERANDAH_TEAK_LOUNGE_GARDEN",
        "refs": ["BARREL_PLATE_05_SINGLE_HERO_RIGHT_70PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D covered country-estate garden verandah: on the left beside the plant sits a low 76cm natural teak and woven-rattan "
            "outdoor lounge armchair with cream linen cushions (reaching ~60% up the plant), honed bluestone verandah paving, warm white timber verandah columns and softly blurred "
            "sunlit green garden bokeh behind, blurred foreground teak coffee table corner bottom-left, warm morning sun-streaks across the stone floor, "
            "clean natural daylight on the plant and wooden barrel, realistic floor contact shadow, zero text."
        ),
    },
    {
        "key": "B12_LIVING_OAK_CREDENZA_LINEN_CURTAINS",
        "refs": ["BARREL_PLATE_04_SINGLE_HERO_LEFT_72PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sunlit organic-modern living room: an 80cm fluted natural white-oak credenza cabinet on the left reaching ~62% up the plant, "
            "tall sheer warm-ivory linen curtains behind continuing past the top edge of the frame, an oatmeal bouclé armchair on the right, wide-plank European oak floor "
            "with realistic barrel contact shadow, softly blurred foreground oak coffee table corner with a handmade stoneware ceramic mug bottom-right, "
            "warm afternoon sun-streaks on the limewash plaster wall, clean natural daylight on the plant and wooden barrel, zero text."
        ),
    },
    {
        "key": "B13_SUNROOM_WINDOW_BENCH_TERRACOTTA",
        "refs": ["BARREL_PLATE_04_SINGLE_HERO_LEFT_72PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sun-drenched architectural glass conservatory sunroom: extending to the right of the plant is a built-in 50cm natural white-oak "
            "window bench seat with a cream linen cushion and neutral woven pillows (reaching well below mid-plant height to lock true 4ft+ scale), tall thin-framed white-oak "
            "mullioned windows behind revealing softly blurred sunlit garden greenery outside, pale matte terracotta floor tiles with realistic barrel contact shadow, "
            "softly blurred foreground woven rattan coffee table edge bottom-right, crisp morning sunbeams slanting across the bench and floor, clean daylight on the plant, zero text."
        ),
    },
    {
        "key": "B14_KITCHEN_MARBLE_OAK_ISLAND_PATIO",
        "refs": ["BARREL_PLATE_05_SINGLE_HERO_RIGHT_70PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sunlit open-concept farmhouse-luxury kitchen corner: on the left sits the corner of a 90cm honed Calacatta-marble and fluted "
            "white-oak kitchen island (reaching ~70% up the plant) with a tan saddle-leather and oak counter stool, behind the plant is a tall slim black-steel glass patio door "
            "continuing past the top edge of the frame opening onto a sunlit stone garden patio, wide-plank oak floor with realistic barrel contact shadow, "
            "softly blurred foreground oak breakfast table corner with a matte ceramic pitcher bottom-left, warm afternoon sunbeams raking across the oak floor, clean daylight, zero text."
        ),
    },
    {
        "key": "B15_DINING_OAK_SIDEBOARD_MORNING_SUN",
        "refs": ["BARREL_PLATE_07_SINGLE_WIDE_RIGHT_36PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 35mm live-action Kodak Vision3 250D high-ceilinged sunlit country-modern dining room with a 3.2-meter white-oak beamed ceiling (DO NOT move or enlarge the plant — "
            "keep its exact compact 4ft / 1.25m height on the right so its pointed tip reaches only ~40cm above the 85cm sideboard and stays well below mid-window height with over 1.9 meters "
            "of open window and plaster wall above it up to the ceiling): on the left stands an 85cm solid warm white-oak buffet sideboard and an oak dining table with linen-and-oak chairs "
            "resting on a woven jute rug, tall paned casement windows behind streaming golden morning sunbeams onto wide-plank oak flooring, realistic barrel contact shadow, clean daylight, zero text."
        ),
    },
    {
        "key": "B16_STUDY_WALNUT_DESK_ARCHED_SHELVES",
        "refs": ["BARREL_PLATE_04_SINGLE_HERO_LEFT_72PCT_16x9.jpg", "BARREL_REF_2_CLOSEUP_LEAF_BARREL_1024.jpg"],
        "prompt": STRICT_SINGLE_CUTOUT_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sunlit luxury home study (preserve 100% of the fine lacy flat-fan foliage sprigs and delicate feathery outer branchlet tips "
            "from the plate with even, clean natural daylight around the plant — DO NOT paint dark shadow bands over the plant or alter its leaf texture): "
            "built-in warm clay-plaster arched bookcases styled with neutral linen books and matte ceramic vessels behind continuing past the top edge of the frame, "
            "wide-plank European oak floor with a realistic contact shadow directly beneath the wooden barrel base, a softly blurred foreground 75cm dark-walnut writing desk corner "
            "with a closed unmarked tan-leather notebook bottom-right, soft golden afternoon window sunlight illuminating the right-hand plaster shelves, zero text."
        ),
    },
    {
        "key": "B17_STAIRCASE_OAK_IRON_GARDEN_WINDOW",
        "refs": ["BARREL_PLATE_05_SINGLE_HERO_RIGHT_70PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sunlit modern-rustic villa hallway: on the left rises an open white-oak timber staircase with slim matte-black iron balusters, "
            "behind the plant is a tall floor-to-ceiling black-framed window continuing past the top edge of the frame revealing softly blurred sunlit garden greenery outside, "
            "honed cream limestone floor tiles with realistic barrel contact shadow, softly blurred foreground oak bench edge bottom-left, warm natural daylight streaming across the floor, "
            "clean true-green light on the plant and wooden barrel, zero text."
        ),
    },
    {
        "key": "B18_BEDROOM_BALCONY_CURTAINS_ARMCHAIR",
        "refs": ["BARREL_PLATE_04_SINGLE_HERO_LEFT_72PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D serene sunlit primary bedroom sitting corner: behind the left side of the plant hang tall sheer warm-ivory linen curtains "
            "beside an open timber-framed French balcony door continuing past the top edge of the frame, on the right sits a low 72cm oatmeal-linen accent armchair "
            "(reaching slightly above mid-plant height) and a small round solid-oak side table on a handwoven cream wool rug over pale oak plank flooring, "
            "softly blurred foreground linen bed-throw corner bottom-right, golden morning sunlight filtering softly through the sheer curtains, realistic barrel contact shadow, zero text."
        ),
    },
    {
        "key": "B19_POOL_CABANA_TRAVERTINE_DAYBED",
        "refs": ["BARREL_PLATE_09_SINGLE_HERO_RIGHT_76PCT_16x9.jpg", "BARREL_REF_2_CLOSEUP_LEAF_BARREL_1024.jpg"],
        "prompt": STRICT_SINGLE_CUTOUT_LOCK + (
            "a 50mm Hero live-action Kodak Vision3 250D sunlit Mediterranean resort poolside travertine terrace (DO NOT shrink, slim, or narrow the plant or wooden barrel — "
            "keep its full 76% frame-height and full lush width in the right foreground so it looks substantial and full-sized): "
            "the plant stands prominently in the right foreground on honed cream travertine stone pavers; recessed ~1.4 meters further back on the left sits a low-profile 65cm "
            "outdoor teak lounge daybed with white linen cushions (scaled proportionally in depth so its seat cushion aligns near the middle-to-upper black hoop of the wooden barrel "
            "and its low white backrest cushion reaches ONLY halfway ~48% up the plant, with NO vertical timber post next to the plant and overhead pergola beams kept high near the top edge), "
            "calm sunlit turquoise pool water and soft olive-tree garden bokeh behind, subtle low blurred travertine table edge at far bottom-left corner, warm golden sunlight across the stone, realistic barrel contact shadow, zero text."
        ),
    },
    {
        "key": "B20_COASTAL_GREAT_ROOM_OCEAN_VIEW",
        "refs": ["BARREL_PLATE_08_SINGLE_COASTAL_RIGHT_56PCT_16x9.jpg", "BARREL_REF_1_SINGLE_CLEAN.jpg"],
        "prompt": SINGLE_LOCK + (
            "a 50mm medium-wide live-action Kodak Vision3 250D sunlit California coastal hillside living room (DO NOT shrink, enlarge, or move the plant — "
            "keep its exact 56% frame-height bounding box on the right so its pointed top tip stands ~50cm taller than the 78cm sofa backrest, reaching slightly above mid-window height "
            "while leaving generous open panoramic glass and white-oak ceiling beams well above the plant tip): on the left sits a 78cm cream linen sectional sofa (whose backrest reaches "
            "~60% up the plant) and a low solid-oak coffee table on a woven natural jute rug over warm wide-plank oak flooring, behind are tall slim dark-bronze framed panoramic ocean-view "
            "windows overlooking sunlit coastal hillside greenery and a calm blue Pacific ocean horizon, warm late-afternoon sunlight across the oak floor, realistic barrel contact shadow, zero text."
        ),
    },
]

FORBIDDEN_WORDS = ("cedar", "pine ", "pine,", "pine.", "topiary", "slender", "teardrop", "chartreuse", "conifer", "spruce", "cypress", "juniper")
for _sc in SCENES_20:
    _low = _sc["prompt"].lower().replace("do not redraw or alter the leaves into spiky pine needles", "")
    for _fw in FORBIDDEN_WORDS:
        if _fw in _low:
            raise ValueError(f"Forbidden word {_fw!r} found in {_sc['key']}!")


def load_uuid_cache():
    if os.path.exists(UUID_CACHE_PATH):
        with open(UUID_CACHE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_uuid_cache(d):
    with open(UUID_CACHE_PATH, "w") as f:
        json.dump(d, f, indent=2)


KNOWN_UUIDS = load_uuid_cache()


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
        await asyncio.sleep(0.55)


async def ensure_gallery_and_image_mode(flow):
    await exit_edit_view_if_needed(flow)
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.25)

    if await flow.js("Boolean(document.querySelector('[aria-label=\"Chỉ dẫn cho tác nhân\"]'))"):
        await flow.find_and_trusted_click("text === 'Tác nhân' && r.y > 780 && r.y < 920", "toggle OFF Tác nhân")
        await asyncio.sleep(0.75)

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


async def open_ingredient_modal(flow):
    has_opts = await flow.js("document.querySelectorAll('[role=\"option\"]').length > 0")
    if not has_opts:
        await flow.find_and_trusted_click("aria === 'Thêm thành phần vào ô nhập câu lệnh'", "open '+' modal")
        await asyncio.sleep(0.85)


async def scan_all_project_options(flow, max_steps=18):
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
            vp.scrollTop += 300;
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

    all_opts = await scan_all_project_options(flow, max_steps=16)
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)

    required_files = [
        (REF_DIR, "BARREL_REF_1_SINGLE_CLEAN.jpg"),
        (REF_DIR, "BARREL_REF_2_CLOSEUP_LEAF_BARREL_1024.jpg"),
    ] + [(PLATE_DIR, p) for p in PLATES]
    missing = []
    for d, fname in required_files:
        stem = fname.split(".")[0]
        known_u = KNOWN_UUIDS.get(fname, "")
        matched_u = next(
            (u for u, txt in all_opts.items() if (known_u and known_u in u) or (stem in txt)),
            None,
        )
        if matched_u:
            KNOWN_UUIDS[fname] = matched_u
        else:
            missing.append((fname, os.path.join(d, fname)))

    save_uuid_cache(KNOWN_UUIDS)
    if not missing:
        print("All barrel reference & 6 plates verified with UUIDs!")
        return

    print(f"Uploading {len(missing)} barrel plate/ref file(s) silently: {[m[0] for m in missing]}...")
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
                    print(f"  ✅ Uploaded through {last_base}!")
                    break
    finally:
        await flow.call("Page.setInterceptFileChooserDialog", {"enabled": False})

    await asyncio.sleep(1.2)
    refreshed = await scan_all_project_options(flow, max_steps=14)
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)
    for fname, _ in missing:
        stem = fname.split(".")[0]
        matched_u = next((u for u, txt in refreshed.items() if stem in txt), None)
        if matched_u:
            KNOWN_UUIDS[fname] = matched_u
            print(f"  📌 Registered UUID for {fname}: {matched_u}")
    save_uuid_cache(KNOWN_UUIDS)


async def attach_ingredient_exact(flow, filename):
    stem = filename.split(".")[0]
    known_uuid = KNOWN_UUIDS.get(filename, "")
    await open_ingredient_modal(flow)

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
                        vp.scrollTop += (er.top + er.height / 2) - (vpRect.top + 150);
                    }}
                    return {{matched: true, uuid}};
                }}
            }}
            return {{matched: false, uuid: ''}};
        }})()
        """)

    hit = False
    for _ in range(35):
        m = await find_visible_match()
        if m["matched"]:
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
        raise RuntimeError(f"Ingredient {filename!r} (uuid={known_uuid!r}) not found!")

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
        raise RuntimeError(f"Ingredient {filename!r} matched but uuid empty: {st}")

    target_uuid = st["targetOpt"]["uuid"]
    target_core = target_uuid.split("=")[0][:48]
    KNOWN_UUIDS[filename] = target_core
    save_uuid_cache(KNOWN_UUIDS)

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
            raise RuntimeError(f"Could not preview {filename!r} ({target_uuid})")

    before_chips = await flow.js("document.querySelectorAll('button[aria-label=\"Thành phần\"]').length")
    await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")

    chip_srcs = []
    for _ in range(12):
        await asyncio.sleep(0.3)
        chip_srcs = await flow.js("""
        Array.from(document.querySelectorAll('button[aria-label="Thành phần"] img'))
            .map(i => (i.currentSrc || i.src || '').split('?')[0].split('/').pop())
            .filter(Boolean)
        """)
        if len(chip_srcs) >= before_chips + 1:
            break
    if len(chip_srcs) < before_chips + 1:
        raise RuntimeError(f"Chip count did not increment for {filename}: before={before_chips}, after={chip_srcs}")
    print(f"  + Attached {stem} (chip={chip_srcs[-1][:14]})")


async def get_rendered_uuids(flow):
    imgs = await flow.js("""
    Array.from(document.querySelectorAll('img'))
        .filter(i => !i.closest('button[aria-label="Thành phần"]') && !i.closest('[role="option"]'))
        .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth}))
        .filter(i => (i.src.includes('flow-content.google/image/') || i.src.includes('/asb/') || i.src.includes('googleusercontent.com/')) && i.nw >= 600)
    """)
    return {im["src"].split("?")[0].split("=")[0] for im in imgs}


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

    saw_pct = False
    for step in range(48):
        await asyncio.sleep(2.0)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
        pcts = await flow.js("""
        Array.from(document.querySelectorAll('div, span'))
            .map(e => (e.innerText || '').trim())
            .filter(t => /^\\d+%$/.test(t))
        """)
        if pcts:
            saw_pct = True
        cur_uuids = await get_rendered_uuids(flow)
        if not pcts and (saw_pct or step >= 7) and len(cur_uuids - before_uuids) >= 1:
            print(f"  ✅ Rendered {sc['key']} in {(step+1)*2}s!")
            return
    print(f"  ⚠️ Timeout waiting for {sc['key']}, continuing...")


async def run_waves(flow, scenes):
    for w_idx in range(0, len(scenes), 3):
        wave = scenes[w_idx:w_idx + 3]
        for sc in wave:
            await submit_scene(flow, sc, wait_for_render=False)
        print(f"  Waiting for barrel20 wave {w_idx//3 + 1} ({len(wave)} images) to finish rendering...")
        saw_pct = False
        zero_streak = 0
        for step in range(60):
            await asyncio.sleep(2.2)
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
            pcts = await flow.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            if pcts:
                saw_pct = True
                zero_streak = 0
            else:
                if saw_pct or step >= 6:
                    zero_streak += 1
            if zero_streak >= 2:
                print(f"  ✅ Wave {w_idx//3 + 1} finished in {round((step+1)*2.2)}s!")
                break

    await asyncio.sleep(4.0)
    await switch_gallery_to_images_once(flow)
    for idx, sy in enumerate((0, 540, 1080, 1620)):
        await flow.js(f"""
        (() => {{
            const scrollers = Array.from(document.querySelectorAll('div, main')).filter(el => el.scrollHeight > el.clientHeight + 200);
            for (const s of scrollers) s.scrollTop = {sy};
            window.scrollTo(0, {sy});
        }})()
        """)
        await asyncio.sleep(0.9)
        res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        p = os.path.join(OUT_DIR, f"qa_barrel20_img_page{idx+1}.jpg")
        with open(p, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("Saved QA page:", p)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["check1", "rest19", "slice", "all20"], default="check1")
    parser.add_argument("--start-index", type=int, default=0)
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

        await switch_gallery_to_images_once(flow)
        await ensure_gallery_and_image_mode(flow)
        await upload_missing_plates(flow, ws)

        if args.phase == "check1":
            await submit_scene(flow, SCENES_20[0], wait_for_render=True)
            await asyncio.sleep(1.5)
            res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
            p = os.path.join(OUT_DIR, "qa_barrel20_check1.jpg")
            with open(p, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("Saved check1 QA screenshot:", p)
        elif args.phase == "rest19":
            await run_waves(flow, SCENES_20[1:])
        elif args.phase == "slice":
            await run_waves(flow, SCENES_20[args.start_index:])
        elif args.phase == "all20":
            await run_waves(flow, SCENES_20)


if __name__ == "__main__":
    asyncio.run(main())
