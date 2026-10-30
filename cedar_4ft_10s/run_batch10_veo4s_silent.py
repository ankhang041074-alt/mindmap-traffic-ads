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
        "move": "Wide Architectural Push-In (Đẩy chậm xuyên nắng sớm phòng ăn trần cao)",
        "prompt": (
            "Continuous, clearly visible 4-second 35mm forward camera push-in across the sunlit herringbone oak dining room floor between the warm oak buffet sideboard and oak dining table, "
            "moving smoothly from a wide view toward a closer medium framing of the 4ft potted plant under tall morning-lit casement windows. Subtle golden dust motes drift gently in the morning sunbeams "
            "while preserving the exact solid shape, matte-black tapered square planter geometry, and dense two-tone green molded foliage of the plant. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
]

# Exact verified UUIDs of all 10 Batch 2 generated 16:9 scenes (S11 -> S20) in Project dfcf77a5-5374-4678-9f80-1c5ea7b5c305
VIDEOS_BATCH2_10 = [
    {
        "key": "V11_PORCH_LIMESTONE_ARCH_OAK_DOORS_4S",
        "uuid": "94476b2c-f110-4c1a-9c08-ee3d514ccc6c",
        "title": "Cảnh 11 — Hiên Vòm Đá Vôi Santa Barbara & Cửa Đôi Gỗ Sồi 2.45m (2 Cây = 1/2 Cửa)",
        "move": "Forward Camera Push-In Past Foreground Olive Foliage (Đẩy tiến xuyên cành ô-liu mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 35mm forward camera push-in toward the sunlit carved limestone archway and arched white-oak double front doors, "
            "so the blurred olive-branch leaves in the bottom-left foreground sweep outward across the edge of the frame in strong 3D optical parallax. "
            "Dappled golden tree-canopy shadows sway gently across the textured limestone wall while preserving the exact solid shape, matte-black tapered square planter geometry, "
            "and dense two-tone green molded foliage of both 4ft potted plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V12_SUNROOM_WINDOW_BENCH_TERRACOTTA_4S",
        "uuid": "72972fcc-5a93-464b-8324-399a9185d9d2",
        "title": "Cảnh 12 — Phòng Kính Sunroom Ngập Nắng Sớm & Bệ Ghế Cửa Sổ Gỗ Sồi 50cm (1 Cây Hero Trái)",
        "move": "Lateral Camera Truck-Right Across Conservatory (Trượt ngang sang phải mở chiều sâu bệ ghế & vườn nắng)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the sun-drenched conservatory sunroom, gliding smoothly from left to right "
            "to create rich three-dimensional architectural parallax between the foreground 4ft potted plant, the built-in white-oak window bench with linen pillows, "
            "and the sunlit outdoor garden trees beyond the tall oak-framed glass windows. Subtle golden dust motes drift gently in the morning sunbeams "
            "while preserving the exact solid shape, matte-black tapered square planter geometry, and dense two-tone green molded foliage of the plant. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V13_COURTYARD_LOGGIA_POOL_COLONNADE_4S",
        "uuid": "7cf09a22-e08a-4bb0-9634-ef73a6450557",
        "title": "Cảnh 13 — Hành Lang Cột Đá Sân Trong Nhìn Ra Hồ Bơi Xanh Ngọc Góc 3/4 (2 Cây Lệch Tầng)",
        "move": "Lateral Camera Truck-Left Along Pool Colonnade (Trượt ngang qua hàng cột đá & mặt nước hồ bơi lấp lánh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-left along the sunlit Mediterranean travertine colonnade terrace, creating dramatic multi-plane 3D parallax "
            "between the tall warm-cream plaster pillars, the staggered pair of 4ft potted plants, and the sunlit courtyard lap pool behind. Turquoise pool water ripples shimmer "
            "with golden afternoon reflections and distant garden bougainvillea sways softly in warm breeze while preserving the exact solid shape, matte-black tapered square planter geometry, "
            "and dense two-tone green molded foliage of both plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V14_KITCHEN_MARBLE_ISLAND_SLIDING_GLASS_4S",
        "uuid": "80fe0aac-30fb-4d56-9fc3-8cd36fdeeba0",
        "title": "Cảnh 14 — Góc Đảo Bếp Marble & Gỗ Sồi Rãnh Cạnh Cửa Kính Sân Vườn (1 Cây Hero Phải)",
        "move": "Lateral Camera Truck-Right Past Foreground Ceramic Pitcher (Trượt phải qua bình gốm mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the sunlit open-concept kitchen, so the blurred oak breakfast table and matte ceramic pitcher "
            "in the bottom-left foreground sweep visibly leftward across the frame in strong 3D optical parallax against the marble-and-fluted-oak island, the 4ft potted plant, "
            "and the sunlit stone garden terrace outside the black-framed glass doors. Subtle golden dust motes float in the afternoon sunbeams while preserving the exact solid shape, "
            "matte-black tapered square planter geometry, and dense two-tone green molded foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V15_GALLERY_ARCHWAY_WAINSCOTING_PORTAL_4S",
        "uuid": "c8560aa3-3ce7-401f-831e-7cee9e229b90",
        "title": "Cảnh 15 — Cổng Vòm Thông Phòng Ốp Phào Chỉ 95cm Mở Ra Phòng Khách Nắng (2 Cây Cận Trung)",
        "move": "Forward Camera Push-In Past Right Doorframe Through Archway (Đẩy tiến xuyên khung cửa tiền cảnh vào vòm nắng)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm forward camera push-in along the French herringbone oak hallway toward the sunlit arched interior doorway, "
            "so the blurred foreground doorway frame on the right sweeps past the edge of the lens in strong 3D architectural parallax, revealing deeper perspective "
            "into the sun-drenched living room and cream linen sofa beyond. Soft golden dust motes drift gently in the afternoon window sunbeams while preserving the exact solid shape, "
            "matte-black tapered square planter geometry, and dense two-tone green molded foliage of both 4ft potted plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V16_BEDROOM_BALCONY_CURTAINS_LOUNGE_CHAIR_4S",
        "uuid": "88270262-e787-4d12-809c-1c3fb0a01be9",
        "title": "Cảnh 16 — Góc Thư Giãn Phòng Ngủ Master Rèm Voan Ban Công & Ghế Linen (1 Cây Hero Trái)",
        "move": "Lateral Camera Truck-Left Past Foreground Bed Throw (Trượt trái qua mép giường linen tiền cảnh, rèm voan thở nhẹ)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-left across the sunlit primary bedroom sitting corner, so the softly defocused linen bed corner "
            "in the bottom-right foreground glides visibly rightward across the frame in rich 3D optical parallax against the oatmeal lounge chair, the 4ft potted plant, "
            "and the open French balcony doorway. The sheer warm-ivory linen curtains breathe very softly in a gentle morning breeze while preserving the exact solid shape, "
            "matte-black tapered square planter geometry, and dense two-tone green molded foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V17_COURTYARD_ARCHED_OAK_WINDOW_STONE_4S",
        "uuid": "255b13ff-e051-4f6b-8fc6-5de808f483de",
        "title": "Cảnh 17 — Sân Vườn Đá Châu Âu Cửa Sổ Vòm Gỗ Sồi & Bóng Nắng Đốm Lá (2 Cây Cận Trung)",
        "move": "Lateral Camera Truck-Right Past Foreground Bistro Chair (Trượt phải qua lưng ghế sắt nghệ thuật mờ tiền cảnh)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-right across the sunlit European limestone courtyard, so the blurred cream wrought-iron garden chair back "
            "in the bottom-left foreground sweeps visibly leftward across the frame in strong 3D parallax against the weathered stone flagstones, the twin 4ft potted plants, "
            "and the arched natural-oak window. Warm dappled tree-canopy sun patterns shimmer gently across the honey-cream limestone masonry while preserving the exact solid shape, "
            "matte-black tapered square planter geometry, and dense two-tone green molded foliage of both plants. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V18_SPA_BATHROOM_FREESTANDING_TUB_SUNLIGHT_4S",
        "uuid": "357a083b-bb15-4391-8461-42c738a6d409",
        "title": "Cảnh 18 — Phòng Tắm Master Organic Spa Bồn Tắm Đá Trắng & Nắng Sớm (1 Cây Hero Phải)",
        "move": "Forward Diagonal Push-In Past Teak Towel Stool & Tub (Đẩy tiến qua đôn khăn gỗ Teak & thành bồn tắm trắng)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm forward camera push-in with subtle rightward parallax across the sun-filled organic-modern spa bathroom, "
            "so the teak towel stool and curved rim of the matte-white freestanding tub on the left sweep smoothly past the foreground in natural 3D depth toward the 4ft potted plant "
            "beside the tall oak window. Outdoor olive-branch foliage beyond the window glass sways gently in morning sunlight while preserving the exact solid shape, "
            "matte-black tapered square planter geometry, and dense two-tone green molded foliage of the indoor plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V19_ROOFTOP_TERRACE_TEAK_DECK_GOLDEN_HOUR_4S",
        "uuid": "03731287-04a9-477e-a037-843e39e6cdf2",
        "title": "Cảnh 19 — Ban Công Penthouse Sàn Gỗ Teak Lan Can Kính Hoàng Hôn Góc 3/4 (2 Cây Chiều Sâu)",
        "move": "Lateral Camera Truck-Left Past Foreground Outdoor Sofa Arm (Trượt trái qua tay sofa ngoài trời nắng hoàng hôn)",
        "prompt": (
            "Continuous, clearly visible 4-second 50mm lateral camera truck-left along the golden-hour penthouse teak terrace, so the cream outdoor linen sofa arm "
            "in the bottom-right foreground sweeps visibly rightward across the frame in dramatic 3D parallax against the teak deck planks, the staggered pair of 4ft potted plants, "
            "the glass terrace parapet, and the glowing sunlit hillside trees in the distance. Warm golden sun rays shimmer softly across the distant hillside canopy "
            "while preserving the exact solid shape, matte-black tapered square planter geometry, and dense two-tone green molded foliage of both plants. "
            "No people, no camera equipment, zero morphing, zero text."
        ),
    },
    {
        "key": "V20_COASTAL_GREAT_ROOM_OCEAN_WINDOWS_4S",
        "uuid": "2a636fef-0562-4470-ad3d-8ff399015f8f",
        "title": "Cảnh 20 — Phòng Khách Đồi Ven Biển Malibu Trần Xà Gỗ Nhìn Ra Biển (1 Cây Đại Cảnh)",
        "move": "Forward Wide-to-Medium Push-In Across Coastal Great Room (Đẩy tiến mở tầm nhìn sofa kem & cửa kính biển)",
        "prompt": (
            "Continuous, clearly visible 4-second 35mm forward camera push-in across the sunlit California coastal hillside living room, advancing smoothly from a wide architectural view "
            "toward a closer medium composition so the low oak coffee table, jute rug, and cream linen sectional sofa on the left glide past in rich 3D parallax against the 4ft potted plant "
            "and the panoramic ocean-view windows. Distant coastal hillside brush and calm ocean horizon shimmer softly in late-afternoon sunlight while preserving the exact solid shape, "
            "matte-black tapered square planter geometry, and dense two-tone green molded foliage of the plant. No people, no camera equipment, zero morphing, zero text."
        ),
    },
]

FORBIDDEN_VIDEO_WORDS = (
    "slider", "gimbal", "dolly", "tripod", "steadicam", "crane", " rig ", " rig.", " rig,",
    "100% still", "stay still", "remain still", "motionless", "hold steady", "5%", "6%", "frozen", "static",
)
for _v in VIDEOS_BATCH2_10:
    _low = _v["prompt"].lower()
    for _fw in FORBIDDEN_VIDEO_WORDS:
        if _fw in _low:
            raise ValueError(f"Forbidden video word {_fw!r} found in {_v['key']}!")


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
    if await flow.js("Boolean(document.querySelector('[role=\"radio\"]'))"):
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
    for scroll_y in range(0, 5800, 260):
        await flow.js(f"""
        (() => {{
            const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
            if (lb) lb.scrollTop = {scroll_y};
        }})()
        """)
        await asyncio.sleep(0.34)
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
        raise RuntimeError(f"Could not find image UUID {target_uuid} inside Bắt đầu picker!")

    await asyncio.sleep(0.3)

    async def inspect_start_modal():
        return await flow.js(f"""
        (() => {{
            const uid = {json.dumps(target_uuid)};
            const el = Array.from(document.querySelectorAll('[role="option"]')).find(e => (e.querySelector('img')?.src || '').includes(uid));
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
            if (addBtn) {{
                let container = addBtn.parentElement;
                while (container && !container.querySelector('[role="option"]') && container.parentElement) {{
                    container = container.parentElement;
                }}
                if (container) {{
                    const pSrcs = Array.from(container.querySelectorAll('img'))
                        .filter(i => !i.closest('[role="option"]'))
                        .map(i => (i.src || '').split('?')[0]);
                    previewMatches = pSrcs.some(s => s.includes(uid));
                }}
            }}
            return {{coords, hasAdd: Boolean(addBtn), previewMatches}};
        }})()
        """)

    slot_ok = False
    for click_dx in [0, 55, 105]:
        st0 = await inspect_start_modal()
        if st0["coords"] and not st0["previewMatches"]:
            await flow.trusted_click(st0["coords"]["cx"] + click_dx, st0["coords"]["cy"])
        for _ in range(7):
            await asyncio.sleep(0.32)
            st1 = await inspect_start_modal()
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
                break
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


async def run_video_waves(flow, videos, tag):
    for w_i in range(0, len(videos), 2):
        wave = videos[w_i:w_i + 2]
        for it in wave:
            await submit_veo_clip(flow, it)
        await wait_for_video_wave(flow, f"{tag} Wave {w_i//2 + 1} ({len(wave)} clips)")
    await asyncio.sleep(4.0)
    try:
        await flow.find_and_trusted_click("text.includes('Video') && r.x < 240", "Left sidebar Video tab")
        await asyncio.sleep(1.2)
    except Exception as e:
        print("Video tab click note:", e)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
    await asyncio.sleep(1.0)
    res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 88})
    p = os.path.join(OUT_DIR, f"qa_veo4s_{tag}_top6.jpg")
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
    p2 = os.path.join(OUT_DIR, f"qa_veo4s_{tag}_bot4.jpg")
    with open(p2, "wb") as f:
        f.write(base64.b64decode(res2["data"]))
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
    print(f"Saved {tag} video QA screenshots:", p, p2)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", choices=["batch1", "batch2"], default="batch2")
    parser.add_argument("--phase", choices=["test2", "all10", "slice", "only"], default="all10")
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--only-key", type=str, default="")
    args = parser.parse_args()

    videos = VIDEOS_10 if args.batch == "batch1" else VIDEOS_BATCH2_10
    tag = "batch1" if args.batch == "batch1" else "batch2"
    if args.phase == "only":
        videos = [v for v in videos if args.only_key in v["key"]]
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

        if args.phase == "test2":
            for it in videos[:2]:
                await submit_veo_clip(flow, it)
            await wait_for_video_wave(flow, f"{tag} Test2")
            await asyncio.sleep(2.0)
            res = await flow.call("Page.captureScreenshot", {"format": "jpeg", "quality": 86})
            p = os.path.join(OUT_DIR, f"qa_veo4s_{tag}_test2.jpg")
            with open(p, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("Saved test2 video QA screenshot:", p)
        elif args.phase == "slice":
            await run_video_waves(flow, videos[args.start_index:], tag)
        elif args.phase in ("all10", "only"):
            await run_video_waves(flow, videos, tag)


if __name__ == "__main__":
    asyncio.run(main())
