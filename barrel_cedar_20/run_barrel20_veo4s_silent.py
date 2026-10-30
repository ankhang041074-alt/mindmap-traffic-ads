import argparse
import asyncio
import base64
import json
import os
import re
import sys
import urllib.request
import websockets

sys.path.insert(0, "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro")
from gen_batch_images import FlowCDP
from review_fix_keyframes_step1 import clear_composer_strict

PORT = 49273
PROJECT_ID = "dfcf77a5-5374-4678-9f80-1c5ea7b5c305"
OUT_DIR = "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/barrel_cedar_20"
SCENE_UUIDS_PATH = os.path.join(OUT_DIR, "barrel20_scene_uuids.json")

VIDEOS_BARREL_20 = [
    {
        "key": "VB01_PORCH_CHARCOAL_DOOR_STONE_COLUMNS_4S",
        "scene_key": "B01_PORCH_CHARCOAL_DOOR_STONE_COLUMNS",
        "title": "Cảnh B01 — Hiên Cửa Xám Than 2.4m & Cột Đá Vôi Kem (2 Cây Thùng Gỗ Đai Đen Cao Hơn Tay Nắm ~18cm)",
        "move": "Forward Camera Push-In Past Foreground Garden Foliage (Đẩy tiến xuyên lá vườn mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 35mm forward camera push-in toward the sunlit matte-charcoal front door and warm-cream limestone porch columns, "
            "so the softly blurred garden leaves in the bottom-right foreground sweep outward across the edge of the frame in strong 3D optical parallax. "
            "Warm late-afternoon golden sun patterns and subtle tree shadows sway gently across the pale stucco wall while preserving the exact solid conical shape, "
            "weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, and dense green molded foliage of both potted plants. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB02_PORCH_FARMHOUSE_BOARD_BATTEN_3Q_4S",
        "scene_key": "B02_PORCH_FARMHOUSE_BOARD_BATTEN_3Q",
        "title": "Cảnh B02 — Hiên Farmhouse Mỹ Vách Gỗ Trắng & Cửa Gỗ Sồi Kính Góc Xiên 3/4 (2 Cây Chiều Sâu)",
        "move": "Lateral Camera Truck-Right Along Diagonal Farmhouse Porch (Trượt ngang sang phải mở chiều sâu bậc thềm gạch đá)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right along the angled modern farmhouse front porch steps, "
            "creating rich multi-plane 3D architectural parallax between the nearer left plant, the natural white-oak glass-paned front door, "
            "the farther right plant, and the crisp white board-and-batten siding. Warm golden-hour diagonal porch-beam shadows shimmer subtly across the siding "
            "while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, "
            "and dense green molded foliage of both plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB03_FIREPLACE_CARVED_LIMESTONE_LIVING_4S",
        "scene_key": "B03_FIREPLACE_CARVED_LIMESTONE_LIVING",
        "title": "Cảnh B03 — Phòng Khách Trần Cao 3.3m Lò Sưởi Đá Vôi Chạm Khắc & Gương Vòm Đồng (2 Cây Đối Xứng)",
        "move": "Forward Camera Push-In Past Foreground Linen Sofa Arm (Đẩy tiến qua tay sofa linen mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 35mm forward camera push-in across the herringbone white-oak living room floor toward the hand-carved French limestone fireplace, "
            "so the softly blurred cream linen sofa arm in the bottom-left foreground glides outward past the lens in rich 3D parallax. "
            "Subtle golden dust motes drift gently through the warm diagonal afternoon window sunbeams while preserving the exact solid conical shape, "
            "weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, and dense green molded foliage of both plants. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB04_PATIO_BLACK_FRENCH_DOORS_FLAGSTONE_4S",
        "scene_key": "B04_PATIO_BLACK_FRENCH_DOORS_FLAGSTONE",
        "title": "Cảnh B04 — Cửa Đôi Kính Khung Thép Đen & Sân Đá Phiến Tự Nhiên (2 Cây Cận Trung 50mm)",
        "move": "Lateral Camera Truck-Right Past Foreground Teak Lounge Arm (Trượt phải qua tay ghế gỗ Teak tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the sunlit backyard flagstone terrace, "
            "so the softly defocused teak outdoor lounge chair arm in the bottom-left foreground sweeps visibly leftward across the frame in strong 3D parallax "
            "against the twin potted plants and tall black-steel French glass doors. Warm afternoon garden reflections shimmer gently in the upper glass panes "
            "while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, "
            "and dense green molded foliage of both plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB05_COURTYARD_FOUNTAIN_TERRACOTTA_3Q_4S",
        "scene_key": "B05_COURTYARD_FOUNTAIN_TERRACOTTA_3Q",
        "title": "Cảnh B05 — Sân Trong Villa Địa Trung Hải Đài Phun Nước Đá & Vòm Ô-Liu Góc 3/4 (2 Cây Lệch Tầng)",
        "move": "Lateral Camera Truck-Left Across Mediterranean Courtyard (Trượt trái khoe đài phun nước & vòm ô-liu nắng chiều)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-left across the sunlit Santa Barbara travertine courtyard, "
            "revealing dramatic multi-plane 3D parallax between the staggered pair of potted plants, the carved limestone water-basin fountain, "
            "and the honey-cream plaster colonnade arches. Gentle water ripples shimmer in the stone fountain basin and distant background olive branches sway softly "
            "in golden-hour light while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, "
            "and dense green molded foliage of both plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB06_FOYER_RECLAIMED_OAK_CONSOLE_4S",
        "scene_key": "B06_FOYER_RECLAIMED_OAK_CONSOLE",
        "title": "Cảnh B06 — Sảnh Foyer Bàn Console Gỗ Sồi Tự Nhiên 85cm & Tranh Linen Tối Giản (2 Cây Đối Xứng)",
        "move": "Forward Architectural Push-In Toward Oak Console Foyer (Đẩy tiến tôn vinh bàn console gỗ sồi & nắng xiên)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm forward camera push-in across the wide-plank European oak foyer floor, "
            "moving smoothly from a medium-wide view into a closer heroic framing of the solid white-oak console table, stoneware bowl, and twin potted plants. "
            "Soft golden dust motes float gently across the warm afternoon side-window sunbeams raking over the cream plaster wall while preserving the exact solid conical shape, "
            "weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, and dense green molded foliage of both plants. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB07_PORCH_STONE_ARCH_WALNUT_DOORS_4S",
        "scene_key": "B07_PORCH_STONE_ARCH_WALNUT_DOORS",
        "title": "Cảnh B07 — Vòm Đá Vôi Dinh Thự Châu Âu & Cửa Đôi Gỗ Óc Chó 2.45m (2 Cây Đối Xứng)",
        "move": "Forward Camera Push-In Past Foreground Olive Greenery (Đẩy tiến xuyên nhánh lá ô-liu mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 35mm forward camera push-in toward the carved honey-cream limestone archway and arched dark-walnut double front doors, "
            "so the softly blurred olive-branch leaves in the bottom-left foreground sweep outward past the edge of the frame in strong 3D optical parallax. "
            "Dappled late-afternoon tree-canopy shadows dance gently across the limestone masonry while preserving the exact solid conical shape, "
            "weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, and dense green molded foliage of both plants. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB08_COURTYARD_ARCHED_OAK_WINDOW_STONE_4S",
        "scene_key": "B08_COURTYARD_ARCHED_OAK_WINDOW_STONE",
        "title": "Cảnh B08 — Sân Vườn Đá Napa Valley & Cửa Sổ Vòm Gỗ Sồi (2 Cây Cận Trung 50mm)",
        "move": "Lateral Camera Truck-Right Past Foreground Bistro Chair (Trượt phải qua lưng ghế sắt sân vườn mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the sunlit Napa Valley stone garden courtyard, "
            "so the blurred wrought-iron bistro chair back in the bottom-left foreground glides visibly leftward across the frame in crisp 3D parallax "
            "against the weathered courtyard flagstones, the twin potted plants, and the tall arched oak casement window. Warm dappled tree shadows shimmer gently "
            "on the dressed limestone wall while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, "
            "and dense green molded foliage of both plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB09_TERRACE_PERGOLA_TEAK_DECK_3Q_4S",
        "scene_key": "B09_TERRACE_PERGOLA_TEAK_DECK_3Q",
        "title": "Cảnh B09 — Sàn Gỗ Teak Giàn Pergola Nắng Chiều Vườn Sau Góc 3/4 (2 Cây Lệch Tầng)",
        "move": "Lateral Camera Truck-Left Past Foreground Outdoor Cushion Arm (Trượt trái qua tay ghế đệm kem ngoài trời)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-left along the sunlit timber-pergola teak deck, "
            "so the softly blurred cream outdoor cushion arm in the bottom-right foreground sweeps visibly rightward across the frame in dramatic 3D parallax "
            "against the teak decking, the staggered pair of potted plants, and the sunlit backyard greenery behind. Distant garden leaves shimmer gently in golden-hour breeze "
            "while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, "
            "and dense green molded foliage of both plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB10_GALLERY_ARCHED_PORTAL_WAINSCOTING_4S",
        "scene_key": "B10_GALLERY_ARCHED_PORTAL_WAINSCOTING",
        "title": "Cảnh B10 — Cổng Vòm Nội Thất Phào Chỉ Cổ Điển 90cm Mở Ra Phòng Khách Nắng (2 Cây Cận Trung)",
        "move": "Forward Camera Push-In Past Right Doorframe Into Sunlit Archway (Đẩy tiến qua khung cửa phải vào vòm phòng khách)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm forward camera push-in along the French herringbone oak gallery hallway toward the plastered arched interior doorway, "
            "so the softly blurred foreground doorway frame edge on the far right sweeps outward past the lens in rich 3D architectural parallax, opening deeper perspective "
            "into the sun-drenched living room beyond. Subtle golden dust motes float gently in the bright afternoon floor sunbeams while preserving the exact solid conical shape, "
            "weathered grey-brown wooden stave barrel planters with three horizontal black metal hoops, and dense green molded foliage of both plants. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB11_VERANDAH_TEAK_LOUNGE_GARDEN_4S",
        "scene_key": "B11_VERANDAH_TEAK_LOUNGE_GARDEN",
        "title": "Cảnh B11 — Hiên Vườn Có Mái Ghế Bành Gỗ Teak Đan Mây & Vườn Nắng Sớm (1 Cây Hero Phải)",
        "move": "Lateral Camera Truck-Right Past Foreground Teak Coffee Table (Trượt phải qua góc bàn Teak mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the covered country-estate bluestone verandah, "
            "so the blurred teak coffee table corner in the bottom-left foreground glides visibly leftward across the frame in strong 3D optical parallax "
            "against the woven-rattan lounge armchair, the potted plant on the right, and the white timber verandah columns. Distant sunlit garden foliage shimmers softly "
            "in morning breeze while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter with three horizontal black metal hoops, "
            "and dense green molded foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB12_LIVING_OAK_CREDENZA_LINEN_CURTAINS_4S",
        "scene_key": "B12_LIVING_OAK_CREDENZA_LINEN_CURTAINS",
        "title": "Cảnh B12 — Phòng Khách Tủ Gỗ Sồi Rãnh, Rèm Voan Linen & Ly Gốm Thủ Công (1 Cây Hero Trái)",
        "move": "Lateral Camera Truck-Left Past Foreground Ceramic Mug & Table (Trượt trái qua ly gốm & bàn trà gỗ sồi tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-left across the sunlit organic-modern living room, "
            "so the softly blurred oak coffee table corner and handmade stoneware ceramic mug in the bottom-right foreground sweep visibly rightward across the frame "
            "in rich three-plane 3D parallax against the bouclé armchair, the potted plant, and the fluted white-oak credenza. Tall sheer warm-ivory linen curtains breathe very softly "
            "in warm afternoon light while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter with three horizontal black metal hoops, "
            "and dense green molded foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB13_SUNROOM_WINDOW_BENCH_TERRACOTTA_4S",
        "scene_key": "B13_SUNROOM_WINDOW_BENCH_TERRACOTTA",
        "title": "Cảnh B13 — Phòng Kính Sunroom Bệ Ghế Cửa Sổ Gỗ Sồi 50cm & Sàn Gạch Terracotta (1 Cây Hero Trái)",
        "move": "Lateral Camera Truck-Left Past Foreground Rattan Table (Trượt trái qua mép bàn mây đan tiền cảnh mở chiều sâu vườn)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-left across the sun-drenched glass conservatory sunroom, "
            "so the softly blurred woven rattan coffee table edge in the bottom-right foreground glides visibly rightward across the frame in crisp 3D parallax "
            "against the built-in white-oak window bench, the potted plant on terracotta tiles, and sunlit outdoor garden trees beyond the mullioned glass windows. "
            "Subtle golden dust motes drift in the morning sunbeams while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter "
            "with three horizontal black metal hoops, and dense green molded foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB14_KITCHEN_MARBLE_OAK_ISLAND_PATIO_4S",
        "scene_key": "B14_KITCHEN_MARBLE_OAK_ISLAND_PATIO",
        "title": "Cảnh B14 — Góc Đảo Bếp Đá Marble & Gỗ Sồi Rãnh Cạnh Cửa Kính Sân Vườn (1 Cây Hero Phải)",
        "move": "Lateral Camera Truck-Right Past Foreground Ceramic Pitcher (Trượt phải qua bình gốm bàn ăn sáng mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the sunlit farmhouse-luxury kitchen, "
            "so the softly blurred oak breakfast table corner and matte ceramic pitcher in the bottom-left foreground sweep visibly leftward across the frame in strong 3D parallax "
            "against the Calacatta-marble and fluted-oak island, the saddle-leather stool, and the potted plant beside the tall black-steel patio glass door. "
            "Outdoor garden leaves shimmer gently in afternoon sun while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter "
            "with three horizontal black metal hoops, and dense green molded foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB15_DINING_OAK_SIDEBOARD_MORNING_SUN_4S",
        "scene_key": "B15_DINING_OAK_SIDEBOARD_MORNING_SUN",
        "title": "Cảnh B15 — Phòng Ăn Trần Cao Tủ Buffet Gỗ Sồi 85cm & Bàn Ăn Nắng Sớm (1 Cây Đại Cảnh)",
        "move": "Forward Wide-to-Medium Push-In Across Sunlit Dining Room (Đẩy tiến xuyên nắng ban mai phòng ăn trần cao)",
        "prompt": (
            "Continuous, clearly visible 4-second 35mm forward camera push-in across the sunlit country-modern dining room floor, "
            "advancing smoothly between the solid white-oak buffet sideboard on the left and the oak dining table with linen chairs on the right toward a closer medium framing "
            "of the potted plant beneath tall paned casement windows. Subtle golden dust motes drift gently in the slanting morning sunbeams while preserving the exact solid conical shape, "
            "weathered grey-brown wooden stave barrel planter with three horizontal black metal hoops, and dense green molded foliage of the plant. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB16_STUDY_WALNUT_DESK_ARCHED_SHELVES_4S",
        "scene_key": "B16_STUDY_WALNUT_DESK_ARCHED_SHELVES",
        "title": "Cảnh B16 — Phòng Đọc Sách Bàn Gỗ Óc Chó & Kệ Sách Vòm Vữa Đất Sét (1 Cây Hero Trái)",
        "move": "Forward Diagonal Push-In Past Foreground Walnut Desk & Notebook (Đẩy tiến qua góc bàn gỗ óc chó & sổ da tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm forward camera push-in with gentle leftward parallax across the sunlit luxury home study, "
            "so the softly blurred dark-walnut writing desk corner and closed tan-leather notebook in the bottom-right foreground glide smoothly outward past the edge of the frame "
            "in rich 3D depth toward the potted plant and warm clay-plaster arched bookcases. Soft golden dust motes float in the raking afternoon window light "
            "while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter with three horizontal black metal hoops, "
            "and fine lacy green flat-fan foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB17_STAIRCASE_OAK_IRON_GARDEN_WINDOW_4S",
        "scene_key": "B17_STAIRCASE_OAK_IRON_GARDEN_WINDOW",
        "title": "Cảnh B17 — Cầu Thang Gỗ Sồi Lan Can Sắt Đen & Vách Kính Cao Sát Trần Nhìn Ra Vườn (1 Cây Hero Phải)",
        "move": "Lateral Camera Truck-Right Past Foreground Oak Bench (Trượt phải qua mép ghế gỗ sồi tiền cảnh mở góc cầu thang)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the sunlit modern-rustic villa hallway, "
            "so the softly blurred oak bench edge in the bottom-left foreground sweeps visibly leftward across the frame in crisp architectural 3D parallax "
            "against the open white-oak timber staircase, the potted plant on honed cream limestone tiles, and sunlit garden greenery outside the floor-to-ceiling window. "
            "Outdoor garden leaves sway softly in daylight breeze while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter "
            "with three horizontal black metal hoops, and dense green molded foliage of the indoor plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB18_BEDROOM_BALCONY_CURTAINS_ARMCHAIR_4S",
        "scene_key": "B18_BEDROOM_BALCONY_CURTAINS_ARMCHAIR",
        "title": "Cảnh B18 — Góc Thư Giãn Phòng Ngủ Master Rèm Voan Ban Công & Ghế Bành Linen (1 Cây Hero Trái)",
        "move": "Lateral Camera Truck-Left Past Foreground Bed Throw (Trượt trái qua mép khăn trải giường tiền cảnh, rèm voan thở nhẹ)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-left across the serene sunlit primary bedroom sitting corner, "
            "so the softly blurred linen bed-throw corner in the bottom-right foreground glides visibly rightward across the frame in rich 3D optical parallax "
            "against the oatmeal-linen accent armchair, the potted plant, and the open timber-framed French balcony doorway. Sheer warm-ivory linen curtains breathe gently "
            "in morning air while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter with three horizontal black metal hoops, "
            "and dense green molded foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB19_POOL_CABANA_TRAVERTINE_DAYBED_4S",
        "scene_key": "B19_POOL_CABANA_TRAVERTINE_DAYBED",
        "title": "Cảnh B19 — Cabana Hồ Bơi Resort Đá Travertine & Sofa Daybed Gỗ Teak (1 Cây Hero Phải)",
        "move": "Lateral Camera Truck-Right Past Foreground Travertine Table (Trượt phải qua bàn đá Travertine mờ tiền cảnh, nước hồ lấp lánh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the sunlit Mediterranean poolside travertine terrace, "
            "so the low blurred travertine table edge in the bottom-left corner sweeps visibly leftward across the frame in smooth 3D parallax "
            "against the recessed low-profile teak lounge daybed on the left, the full-sized foreground potted plant on the right, and the bright backyard pool behind. "
            "Turquoise pool water ripples shimmer with golden sun reflections while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter "
            "with three horizontal black metal hoops, and fine lacy green flat-fan foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "VB20_COASTAL_GREAT_ROOM_OCEAN_VIEW_4S",
        "scene_key": "B20_COASTAL_GREAT_ROOM_OCEAN_VIEW",
        "title": "Cảnh B20 — Phòng Khách Đồi Ven Biển California Trần Xà Gỗ Sồi & Cửa Kính Đại Dương (1 Cây Đại Cảnh)",
        "move": "Forward Wide-to-Medium Push-In Across Coastal Great Room (Đẩy tiến mở tầm nhìn sofa kem & chân trời biển Thái Bình Dương)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm forward camera push-in across the sunlit California coastal hillside living room, "
            "advancing smoothly from a medium-wide architectural view toward a closer hero composition so the low solid-oak coffee table, woven jute rug, and cream linen sectional sofa "
            "on the left glide past in rich 3D parallax against the potted plant and panoramic ocean-view windows. Distant coastal greenery and calm ocean light shimmer softly "
            "while preserving the exact solid conical shape, weathered grey-brown wooden stave barrel planter with three horizontal black metal hoops, "
            "and fine lacy green flat-fan foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
]

FORBIDDEN_VIDEO_WORDS = (
    "slider", "gimbal", "dolly", "tripod", "steadicam", "crane",
    "100% still", "stay still", "remain still", "motionless", "hold steady", "5%", "6%", "frozen", "static",
    "cedar", "topiary", "slender", "teardrop", "chartreuse", "conifer", "spruce", "cypress", "juniper",
)
for _v in VIDEOS_BARREL_20:
    _low = _v["prompt"].lower()
    if re.search(r"\brig\b|\bpine\b", _low):
        raise ValueError(f"Forbidden regex word found in {_v['key']}!")
    for _fw in FORBIDDEN_VIDEO_WORDS:
        if _fw in _low:
            raise ValueError(f"Forbidden video word {_fw!r} found in {_v['key']}!")


def load_scene_uuids():
    if not os.path.exists(SCENE_UUIDS_PATH):
        raise FileNotFoundError(f"Scene UUID mapping file missing: {SCENE_UUIDS_PATH}")
    with open(SCENE_UUIDS_PATH, "r") as f:
        return json.load(f)


async def exit_edit_view_if_needed(flow):
    href = await flow.js("window.location.href")
    if "/edit/" in (href or ""):
        await flow.find_and_trusted_click("aria === 'Nút quay lại để quay về trang trước'", "exit /edit/ view")
        await asyncio.sleep(1.0)


async def ensure_veo31_fast_4s_16x9(flow):
    await exit_edit_view_if_needed(flow)
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.3)

    if await flow.js("Boolean(document.querySelector('[aria-label=\"Chỉ dẫn cho tác nhân\"]'))"):
        await flow.find_and_trusted_click("text === 'Tác nhân' && r.y > 780 && r.y < 920", "toggle OFF Tác nhân")
        await asyncio.sleep(0.75)

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

    model_txt = await flow.js("""
    (() => {
        const el = document.querySelector('[aria-label="Chọn nhóm mô hình"]')
            || Array.from(document.querySelectorAll('button, [role="button"]')).find(b => {
                const r = b.getBoundingClientRect();
                return r.width > 0 && r.y > 480 && r.y < 820 && (b.innerText || '').includes('Veo');
            });
        return (el?.innerText || '').trim();
    })()
    """)
    if "Veo 3.1 - Fast" not in model_txt:
        await flow.find_and_trusted_click("(aria === 'Chọn nhóm mô hình' || text.includes('Veo')) && r.y > 480 && r.y < 820", "model dropdown")
        await asyncio.sleep(0.45)
        await flow.find_and_trusted_click("el.getAttribute('role') === 'menuitem' && text.includes('Veo 3.1 - Fast')", "Veo 3.1 - Fast")
        await asyncio.sleep(0.4)

    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === '4 giây'", "4 giây")
    await asyncio.sleep(0.25)
    await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === 'x1'", "x1")
    await asyncio.sleep(0.25)
    if await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))"):
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "close settings")
        await asyncio.sleep(0.4)


async def clear_frame_slots_and_text(flow):
    await clear_composer_strict(flow)
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


async def _try_set_start_frame_once(flow, target_uuid):
    target_uuid = target_uuid.split("=")[0][:48]
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)

    await clear_frame_slots_and_text(flow)
    await flow.find_and_trusted_click("text.includes('Bắt đầu') && !aria.includes('Bắt đầu tạo') && r.y > 660", "Bắt đầu slot")
    await asyncio.sleep(0.9)

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

    found_opt = None
    for scroll_y in range(0, 10400, 260):
        await flow.js(f"""
        (() => {{
            const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
            if (lb) lb.scrollTop = {scroll_y};
        }})()
        """)
        await asyncio.sleep(0.32)
        opt = await flow.js(f"""
        (() => {{
            const uid = {json.dumps(target_uuid)};
            const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
            const lbRect = lb ? lb.getBoundingClientRect() : null;
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const img = el.querySelector('img');
                const src = img?.src || '';
                if (src.includes(uid)) {{
                    if (lb && lbRect) {{
                        const er = el.getBoundingClientRect();
                        lb.scrollTop += (er.top + er.height / 2) - (lbRect.top + 150);
                    }}
                    return {{matched: true, txt: (el.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 50)}};
                }}
            }}
            return null;
        }})()
        """)
        if opt:
            found_opt = opt
            break

    if not found_opt:
        return False, f"UUID {target_uuid} not found in virtual scroll"

    await asyncio.sleep(0.35)

    async def recenter_and_inspect():
        return await flow.js(f"""
        (() => {{
            const uid = {json.dumps(target_uuid)};
            const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
            const lbRect = lb ? lb.getBoundingClientRect() : null;
            let el = Array.from(document.querySelectorAll('[role="option"]')).find(e => (e.querySelector('img')?.src || '').includes(uid));
            if (el && lb && lbRect) {{
                const er0 = el.getBoundingClientRect();
                if (er0.top < lbRect.top + 60 || er0.bottom > lbRect.top + 280) {{
                    lb.scrollTop += (er0.top + er0.height / 2) - (lbRect.top + 150);
                }}
            }}
            el = Array.from(document.querySelectorAll('[role="option"]')).find(e => (e.querySelector('img')?.src || '').includes(uid));
            let coords = null;
            if (el) {{
                const img = el.querySelector('img');
                const r = (img && img.getBoundingClientRect().width > 10 ? img : el).getBoundingClientRect();
                coords = {{cx: Math.round(r.x + Math.min(r.width / 2, 45)), cy: Math.round(r.y + r.height / 2)}};
            }}
            const addBtn = Array.from(document.querySelectorAll('button')).find(
                b => (b.innerText || '').trim() === 'Thêm vào câu lệnh' && b.getBoundingClientRect().width > 0
            );
            let previewMatches = false;
            let pSrcs = [];
            if (addBtn) {{
                let container = addBtn.parentElement;
                while (container && !container.querySelector('[role="option"]') && container.parentElement) {{
                    container = container.parentElement;
                }}
                if (container) {{
                    pSrcs = Array.from(container.querySelectorAll('img'))
                        .filter(i => !i.closest('[role="option"]'))
                        .map(i => (i.src || '').split('?')[0]);
                    previewMatches = pSrcs.some(s => s.includes(uid));
                }}
            }}
            return {{coords, hasAdd: Boolean(addBtn), previewMatches, pSrcs}};
        }})()
        """)

    for click_dx in [0, 55, 110, 160]:
        st0 = await recenter_and_inspect()
        if st0["coords"] and not st0["previewMatches"]:
            await flow.trusted_click(st0["coords"]["cx"] + click_dx, st0["coords"]["cy"])
        for _ in range(8):
            await asyncio.sleep(0.32)
            st1 = await recenter_and_inspect()
            if st1["hasAdd"] and st1["previewMatches"]:
                await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
                await asyncio.sleep(0.65)
            slot_ok = await flow.js("""
            (() => {
                const btns = Array.from(document.querySelectorAll('button, [role="button"]')).filter(b => b.getBoundingClientRect().y > 680 && b.getBoundingClientRect().width > 0);
                const hasEmptyStart = btns.some(b => (b.innerText||'').trim() === 'Bắt đầu');
                const hasEmptyEnd = btns.some(b => (b.innerText||'').trim().includes('Kết thúc'));
                return !hasEmptyStart && hasEmptyEnd;
            })()
            """)
            if slot_ok:
                return True, st1
    st_last = await recenter_and_inspect()
    return False, f"preview did not lock: {st_last}"


async def set_start_frame_by_uuid(flow, target_uuid):
    last_reason = ""
    for attempt in range(1, 4):
        ok, info = await _try_set_start_frame_once(flow, target_uuid)
        if ok:
            print(f"  + Verified Start Frame [{target_uuid[:8]}] populated in Bắt đầu slot (attempt {attempt})!")
            return
        last_reason = str(info)
        print(f"  [retry {attempt}/3] Start Frame {target_uuid[:8]} retry needed: {last_reason[:140]}")
        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(1.0)
    raise RuntimeError(f"Start Frame slot did not populate cleanly for {target_uuid} after 3 attempts! ({last_reason})")


async def submit_veo_clip(flow, item, target_uuid):
    print(f"\n=== QUEUEING 4S VEO 3.1 CLIP: {item['key']} (img={target_uuid[:8]}) ===")
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
    await asyncio.sleep(0.25)
    await ensure_veo31_fast_4s_16x9(flow)
    await clear_frame_slots_and_text(flow)
    await set_start_frame_by_uuid(flow, target_uuid)

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


async def wait_for_video_wave(flow, wave_label, max_steps=48):
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


async def capture_video_qa_pages(flow):
    await exit_edit_view_if_needed(flow)
    vid_tab = await flow.js("""
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="tab"]')).filter(b => {
            const r = b.getBoundingClientRect();
            const txt = (b.innerText || '').trim();
            return r.width > 0 && r.x < 260 && r.y > 60 && r.y < 260 && txt.includes('Video');
        });
        if (!btns.length) return null;
        const r = btns[0].getBoundingClientRect();
        return {cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)};
    })()
    """)
    if vid_tab:
        await flow.trusted_click(vid_tab["cx"], vid_tab["cy"])
        await asyncio.sleep(1.2)

    for idx, sy in enumerate((0, 540, 1080, 1620)):
        await flow.js(f"""
        (() => {{
            const scrollers = Array.from(document.querySelectorAll('div, main')).filter(el => el.scrollHeight > el.clientHeight + 200);
            for (const s of scrollers) s.scrollTop = {sy};
            window.scrollTo(0, {sy});
        }})()
        """)
        await asyncio.sleep(0.95)
        res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
        p = os.path.join(OUT_DIR, f"qa_barrel20_veo_page{idx+1}.jpg")
        with open(p, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("Saved Video QA page:", p)

    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")


async def run_video_waves(flow, videos, scene_uuids):
    for w_i in range(0, len(videos), 2):
        wave = videos[w_i:w_i + 2]
        for it in wave:
            uid = scene_uuids.get(it["scene_key"], "")
            if not uid:
                raise RuntimeError(f"Missing scene UUID for {it['scene_key']} in {SCENE_UUIDS_PATH}!")
            await submit_veo_clip(flow, it, uid)
        await wait_for_video_wave(flow, f"Barrel20 Veo Wave {w_i//2 + 1} ({len(wave)} clips)")
    await asyncio.sleep(4.0)
    await capture_video_qa_pages(flow)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["all20", "slice", "only", "qa-only"], default="all20")
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--only-key", type=str, default="")
    args = parser.parse_args()

    scene_uuids = load_scene_uuids()
    videos = VIDEOS_BARREL_20
    if args.phase == "only":
        videos = [v for v in videos if args.only_key in v["key"] or args.only_key in v["scene_key"]]
        if not videos:
            raise ValueError(f"No video matching --only-key={args.only_key!r}")

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

        if args.phase == "qa-only":
            await capture_video_qa_pages(flow)
        elif args.phase == "slice":
            await run_video_waves(flow, videos[args.start_index:], scene_uuids)
        elif args.phase in ("all20", "only"):
            await run_video_waves(flow, videos, scene_uuids)


if __name__ == "__main__":
    asyncio.run(main())
