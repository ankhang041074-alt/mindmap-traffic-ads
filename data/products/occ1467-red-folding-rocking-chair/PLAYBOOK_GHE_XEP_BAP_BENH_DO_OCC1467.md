# 🎬 Sổ Tay Chuẩn Hóa Tạo Ảnh & Video 8 Giây — Ghế Xếp Bập Bênh Đỏ `OCC1467` (Google Flow: `Nano Banana Pro 16:9` + `Veo 3.1 - Fast 8s`)

> [!IMPORTANT]
> **Mục tiêu tài liệu này:** Ghi lại trọn vẹn bộ công thức tạo **8 Ảnh TVC (`S01..S08`)** và **8 Video `8 giây` (`V01..V08`)** đã được kiểm chứng thực chiến bằng `ffmpeg` từng giây (`Sec 1` đến `Sec 8`) cho sản phẩm **Ghế Xếp Bập Bênh Đỏ `OCC1467`** trên Google Flow (`project_id: 1d71c3d4-623e-4656-8d1e-915fbe5e59bd`), sẵn sàng đồng bộ giữa máy ở Nhà và máy ở Công ty.

---

## 1. Cấu Trúc 8 Cảnh TVC Chuẩn & Cặp Plate / Reference Tương Ứng (`S01..S08`)

Mọi Concept mới (như Concept 4: *Napa Valley Vineyard Stone Villa*, Concept 5: *Santa Barbara Montecito Spanish-Revival Villa*, hoặc bất kỳ Concept 6, 7... nào tiếp theo) đều giữ nguyên danh bạ Plate & Reference tại [`products/occ1467_red_rocking_chair/`](file:///c:/Users/ADMIN/Documents/antigravity/optimistic-hubble/products/occ1467_red_rocking_chair/sku_project.json):

| Thứ tự | Mã Cảnh | Cặp Plate + Reference Bắt Buộc | Nội Dung & Quy Tắc Khóa Chi Tiết Sản Phẩm |
| :--- | :--- | :--- | :--- |
| **1** | `S01_PISTON_DETAIL` | `OCC1467_PLATE_07_CLOSEUP_DETAIL_16x9.jpg` + `OCC1467_REF_3_MACRO_L_BAR_PIVOT_1024.jpg` | Cận trung cơ khí khung thép chữ X sơn tĩnh điện đen (có tem vàng nhỏ), 2 thanh đế phẳng chạm sàn, **2 trụ piston nhún hình trụ tròn màu đen có tem cảnh báo màu vàng** ở phần chân sau, túi đựng ly vải đỏ viền xám bên phải, mặt ghế đỏ-lưới xám có 2 đường chỉ trắng dọc. |
| **2** | `S02_SINGLE_LEFT_COURTYARD` | `OCC1467_PLATE_02_SINGLE_LEFT_58PCT_16x9.jpg` + `OCC1467_REF_2_CLOSEUP_1024.jpg` | Ghế đơn trống bên trái (`58%`) đặt cạnh bàn trà thấp bên phải (`x=58%..84%`) trên sân đá phẳng. |
| **3** | `S03_SINGLE_LEFT_VEHICLE` | `OCC1467_PLATE_02_SINGLE_LEFT_58PCT_16x9.jpg` + `OCC1467_REF_2_CLOSEUP_1024.jpg` | Ghế đơn trống bên trái (`58%`) đặt cạnh bàn picnic/rương gỗ thấp ở giữa và xe cổ điển (Defender / Cruiser / Airstream) có mái hiên vải bên phải. |
| **4** | `S04_FOLDED_CARRY` | `OCC1467_REF_5_FOLDED_CARRY_S4_1024.jpg` + `OCC1467_CHAR_2_SHEET.jpg` | Nhân vật nữ (`CHAR_2_SHEET`) đi bộ từ trái sang phải, 1 tay xách ghế xếp phẳng: khung thép đen xếp phẳng, **trụ piston đen có tem vàng nằm ngang**, vải đỏ-xám gấp gọn và **túi đựng ly đỏ treo rủ ở cạnh dưới**. |
| **5** | `S05_REAR_3Q_SEATED` | `OCC1467_REF_REAR_3Q_CLIFF_POSE.jpg` + `OCC1467_REF_4_REAR_MESH_1024.jpg` + `OCC1467_CHAR_2_SHEET.jpg` | Góc lưng 3/4 nhìn ra thung lũng/hồ/biển (sàn phẳng mở, **CẤM có tường đá chắn trước ghế**): khoe mảng lưới xám thoáng khí sau lưng, 2 khuyên kim loại bạc ở góc trên, đai vải đỏ an toàn chéo khung chữ X, 2 piston đen tem vàng phía sau, **đúng 1 bình nước đen trong túi đựng ly bên phải**, và **BẮT BUỘC đúng 2 chiếc giày nâu đặt phẳng trên sàn (CẤM vắt chân, CẤM sinh ra chiếc giày thứ 3)**. |
| **6** | `S06_SEATED_SINGLE_WITH_DOG` | `OCC1467_PLATE_01B_SINGLE_RIGHT_FACING_LEFT_58PCT_16x9.jpg` + `OCC1467_REF_2_CLOSEUP_1024.jpg` + `OCC1467_CHAR_2_SHEET.jpg` | Nhân vật nữ ngồi ghế đơn bên phải (`58%`) cầm máy ảnh cổ điển trên đùi, **hai đầu gối gập vuông góc `90°`, hai ống chân thẳng đứng và 2 giày nâu đặt phẳng ngay trước chân ghế trên mặt sàn gỗ thoáng (`CẤM đặt giỏ mây, bình gốm hay đồ vật sát mũi giày ở x=45%..58%` vì Veo 3.1 sẽ tưởng là ghế đôn gác chân)**; bên trái (`x=14%..46%`) là chú chó Golden Retriever nằm thư giãn trên sàn gỗ. |
| **7** | `S07_PAIR_RIGHT_FIREPLACE` | `OCC1467_PLATE_09_PAIR_RIGHT_TERRACE_16x9.jpg` + `OCC1467_REF_2_CLOSEUP_1024.jpg` + `OCC1467_COUPLE_CAMP_TALK_REF.jpg` + `OCC1467_CHAR_1_SHEET.jpg` + `OCC1467_CHAR_2_SHEET.jpg` | Cặp đôi (`CHAR_2` nữ bên trái, `CHAR_1` nam bên phải) ngồi trò chuyện trên cặp ghế bên phải (`PLATE_09`), bên trái (`x=0%..24%`) là lò sưởi đá/vòm trắng ngoài trời. |
| **8** | `S08_PAIR_LEFT_WATER_FINALE` | `OCC1467_PLATE_10_PAIR_LEFT_STREAM_16x9.jpg` + `OCC1467_REF_2_CLOSEUP_1024.jpg` + `OCC1467_COUPLE_CAMP_TALK_REF.jpg` + `OCC1467_CHAR_1_SHEET.jpg` + `OCC1467_CHAR_2_SHEET.jpg` | Cặp đôi ngồi trên cặp ghế bên trái (`PLATE_10`) cầm ly inox cắm trại trò chuyện vui vẻ bên hồ nước / suối và cầu đá lúc hoàng hôn. |

---

## 2. Bộ 4 Công Thức Prompt Video `8 Giây` Chuẩn (`Veo 3.1 - Fast 8s`) — Đã Kiểm Chứng Qua `ffmpeg` `1fps` (`Sec 1..8`)

### Công Thức 1 — Nhóm Cảnh Ghế Trống & Cận Cảnh Cơ Khí (`V01`, `V02`, `V03`): Khóa Chống Rung Tuyệt Đối (`Camera-Only 3D Arc`)
- **Nguyên tắc:** Chỉ cho camera di chuyển vòng cung 3D (`only the camera moves in a smooth, gentle 3D lateral-and-forward arc`), khóa chiếc ghế trống và bàn/xe đứng yên tuyệt đối trên sàn (`with zero self-movement, zero vibration, and zero swaying`) để ghế không tự đung đưa hay rung chân.
- **Mẫu Prompt Chuẩn (`V02`):**
  ```text
  Continuous, clearly visible 8-second 35mm Kodak Vision3 250D architectural lifestyle shot in a sunlit [location]: only the camera moves in a smooth, gentle 3D lateral-and-forward arc across the [floor surface] toward the single empty crimson-red and cool-grey mesh folding outdoor chair on the left and the low [side table] on the right, while both the empty chair and the side table remain completely fixed and planted in their exact spots on the stone floor with zero self-movement, zero vibration, and zero swaying. Showcase the crisp crimson-red Oxford fabric, breathable cool-grey mesh backrest with two vertical white piping lines, red padded armrests, right-side crimson cup-holder pouch, matte-black X-frame, and dual rear vertical black cylindrical pistons with small yellow labels in warm golden-hour sunlight. Strictly one empty chair anchored on the floor, zero morphing, zero text.
  ```

### Công Thức 2 — Cảnh Đi Bộ Xách Ghế Gấp Phẳng (`V04` — `8s Lateral Tracking Walk`)
- **Mẫu Prompt Chuẩn (`V04`):**
  ```text
  Continuous, clearly visible 8-second 35mm Kodak Vision3 250D lifestyle tracking shot along a sunlit [pathway description]: as the camera performs a smooth 3D lateral tracking motion alongside her from left to right, the woman in the cream puffer vest, forest-green waffle sweater, camel chino pants, and two brown hiking boots walks gracefully forward along the path while effortlessly carrying the single folded-flat crimson-red and cool-grey mesh rocking chair at her right hip with her right hand gripping the upper black frame and red carry strap. The folded chair retains its exact flat-folded matte-black tubular steel frame, horizontal black cylindrical piston with yellow label, folded red-and-grey mesh panels, and single red fabric cup-holder pouch hanging cleanly at the bottom edge. Strictly one person with two boots and one folded chair, zero morphing, zero text.
  ```

### Công Thức 3 — Nhóm Cảnh Ngồi Đung Đưa (`V05` Góc Lưng 3/4 & `V07, V08` Cặp Đôi — Đồng Bộ Chuẩn Đế Ghế Phẳng + Chỉ Đung Đưa Thân Trên + Không Nhắc `boots/feet/legs`)
Có **2 biến thể chuẩn** đã kiểm chứng thực tế:

1. **Biến thể 3A — Công Thức Đung Đưa Thân Trên & Khóa Đế Sắt Phẳng (`Dùng chung cho V05, V06, V07, V08` — An toàn 100%, không nhấc chân ghế, không nhấc giày, không zoom-in):**
   - **Mẫu `V05` (Góc lưng 3/4):**
     ```text
     Continuous, clearly visible 8-second 35mm Kodak Vision3 250D [location] lifestyle shot from a rear-3/4 angle at a sunlit [terrace overlook]: as the camera performs a smooth, gentle lateral arc behind the chair with zero zoom-in, the chair's flat matte-black steel base frame stays planted flat on the stone floor while the woman in the cream puffer vest and forest-green waffle sweater seated in the single crimson-red and silver-grey mesh spring-cushioned chair gently sways only her upper torso and shoulders rhythmically back and forth against the backrest in a subtle, soothing motion while gazing out at the [vista description]. Her right hand remains resting calmly near the single matte-black tumbler sitting inside the right-side crimson-red cup-holder pouch while her left hand stays resting down on her lap out of view — she never lifts a second drink and no extra cup ever appears. Strictly one chair, one woman, and one single tumbler in the right-side cup-holder pouch, zero morphing, zero text.
     ```
   - **Mẫu `V07` / `V08` (Cặp đôi góc trước 3/4):**
     ```text
     Continuous, clearly visible 8-second 35mm Kodak Vision3 250D [location] lifestyle shot from a front-3/4 angle on a sunlit [terrace description]: as the camera performs a smooth, gentle lateral arc across the terrace with zero zoom-in, the flat matte-black steel base frames of both chairs stay planted on the floor while the woman in the cream puffer vest seated in the left crimson-red and silver-grey mesh spring-cushioned chair and the man in the blue linen shirt seated in the right crimson-red and silver-grey mesh spring-cushioned chair gently sway only their upper torsos and shoulders rhythmically back and forth against the backrests in a subtle, soothing motion while chatting and smiling warmly together. [Hand/mug lock]. Strictly two chairs and two people, zero morphing, zero text.
     ```

2. **Biến thể 3B — Công Thức Nhún Piston Góc Lưng 3/4 (`Video 5 Cũ` — `05_OCC1467_C4_V05_REAR_3Q_ROCKING_VINEYARD_VALLEY.mp4`, chuyên trị góc `Rear-3/4` khi muốn tả rõ 2 trụ piston phía sau, đã bỏ từ `boots` khỏi prompt video):**
   ```text
   Continuous, clearly visible 8-second 35mm Kodak Vision3 250D vineyard lifestyle shot from a rear-3/4 angle at a sunlit bluestone terrace overlook above a golden-green Napa Valley vineyard valley: as the camera performs a smooth, gentle lateral arc behind the single crimson-red and silver-grey mesh spring-cushioned chair with zero zoom-in, the flat bottom horizontal runner bars and rear base feet remain planted flat on the stone floor at all times (the rear chair legs never lift or tip off the ground) while the woman in the cream puffer vest and forest-green waffle sweater leans only her upper torso and shoulders gently back against the backrest to compress the two vertical black spring pistons and lets the spring mechanism softly rebound the backrest in a subtle, cushioned motion while gazing out at the rolling sunlit grapevine rows and distant golden hills. Her right hand remains resting calmly near the single matte-black tumbler sitting inside the right-side crimson-red cup-holder pouch while her left hand stays resting down on her lap out of view — she never lifts a second drink and no extra cup ever appears. Strictly one chair with its bottom runner bars planted flat on the stone floor, one woman, and one single tumbler in the right-side cup-holder pouch, zero morphing, zero text.
   ```
   > ⚠️ **Lưu ý kỹ thuật cực kỳ quan trọng:** Chỉ dùng câu tả cơ chế piston (`compress the two vertical black spring pistons...`) ở góc **Rear-3/4 (`V05`)** nơi 2 trụ piston nằm phía sau. Ở các góc **Front-3/4 (`V06, V07, V08`)**, **TUYỆT ĐỐI CẤM** viết câu `"front seat tubes rise into the two front vertical spring pistons"` hay `"hydraulic / compress downward"` vì Veo 3.1 sẽ kéo dài trụ piston thành cây cà kheo 40cm hoặc biến trụ đen thành lò xo xoắn ruột gà trần!

### Công Thức 4 — Cảnh Ngồi Ghế Đơn Góc Trước `PLATE_01B` Cùng Cún Golden (`V06` — Đung Đưa Nhịp Nhàng + Khóa Đế Ghế & 2 Giày Phẳng Sàn 100%, Không Zoom-In)
- **Bộ 3 Quy Luật Vàng Đã Kiểm Chứng Từng Giây Bằng `ffmpeg 1fps` (`Sec 1..8`):**
  1. **Quy luật Ảnh gốc (`S06` Open Floor Around Boots):** Trong `PLATE_01B`, hai ống chân của nhân vật đặt hơi chéo về phía trước chân ghế trái. Khi tạo ảnh `S06`, **BẮT BUỘC** yêu cầu `her knees bent naturally at 90 degrees, her lower legs vertical, and both dark-brown hiking boots planted flat on the open wood deck directly in front of the front chair legs` và **TUYỆT ĐỐI CẤM** đặt giỏ mây, bình gốm hay đồ vật sát mũi giày (`x=45%..58%`), vì khi nghiêng người ra sau ở giây thứ 3–4, Veo 3.1 sẽ tưởng vật thể đó là ghế đôn (ottoman/footstool) và nhấc chân gác lên!
  2. **Quy luật Vật lý Đế Ghế (`spring-cushioned chair` thay vì `rocker chair` ở góc đơn trước 3/4):** Khi viết `"rocker chair"` ở góc cận 1 ghế phía trước, Veo 3.1 hiểu nhầm thành ghế gỗ bập bênh đế cong nên bẩy cả thanh sắt đáy ghế phía trước lẫn 2 bàn chân nhấc lên khỏi sàn. Thay bằng `"spring-cushioned chair"` + `"the chair's flat matte-black steel base frame stays planted on the wood deck while the woman ... gently sways only her upper torso and shoulders rhythmically back and forth against the backrest in a subtle, soothing motion"` và khóa camera `"with zero zoom-in"`.
  3. **Quy luật Chống Rò Rỉ Chuyển Động Vào Đôi Giày (`Zero Token-to-Motion Leakage — Không nhắc từ "boots / feet / legs" trong Prompt Video`):** Trong Veo 3.1, nếu câu prompt vừa có động từ `"sways / rocks back and forth"` vừa xuất hiện danh từ `"boots / feet / legs"` (dù là câu khẳng định `"boots stay flat"` hay phủ định `"without lifting boots"`), cơ chế attention của AI vẫn truyền động năng đung đưa xuống đôi giày! Giống hệt `V07` và `V08`, **bỏ hoàn toàn từ `boots / feet / legs` khỏi Prompt Video** để động từ đung đưa chỉ tác động lên `"only her upper torso and shoulders"`, giúp 2 chiếc giày đứng yên 100% theo ảnh gốc suốt 8 giây!
- **Mẫu Prompt Ảnh `S06` Chuẩn:**
  ```text
  Extract the exact crimson-red and cool-grey mesh folding rocking chair from [Image 1] and place it at the exact same camera angle, position, and scale (58% on the right side of the frame, facing 3/4 left) on a wide, sunlit Santa Barbara honey-teak wood veranda deck under a rustic beam pergola draped with warm café string lights, framed by whitewashed Spanish stucco pillars and lush green orange trees and palms in the background. Use [Image 2] to lock exact hardware details: matte-black X-frame, dual vertical black cylindrical spring pistons with yellow warning labels, red padded armrests, right-side crimson fabric cup-holder pouch, and white vertical piping. Seated comfortably in the chair is the exact woman from [Image 3] (reddish-brown hair in a low ponytail, cream puffer vest over forest-green waffle sweater, camel chino pants, and two dark-brown hiking boots), holding a vintage silver-and-black rangefinder camera calmly in her lap and smiling warmly, with her knees bent naturally at 90 degrees, her lower legs vertical, and both dark-brown hiking boots planted flat on the open wood deck directly in front of the front chair legs. On the sunlit wood deck to the left (x=14%..46%), a friendly Golden Retriever dog lies peacefully on the open wood planks with clear, open wood decking around the woman's boots. Shot on 35mm Kodak Vision3 250D, 50mm lens, f/4, natural 4000K golden-hour sunlight. Zero extra legs, zero objects near her feet, zero text, zero watermarks.
  ```
- **Mẫu Prompt Video `V06` Chuẩn (`8s Gentle Rocking + Zero Boot Lift + Zero Zoom-In`):**
  ```text
  Continuous, clearly visible 8-second 35mm Kodak Vision3 250D Santa Barbara lifestyle shot from a front-3/4 angle under a sunlit Montecito teak-and-stucco pergola veranda: as the camera performs a smooth, gentle lateral arc across the wide honey-teak deck with zero zoom-in, the chair's flat matte-black steel base frame stays planted on the wood deck while the woman in the cream puffer vest and forest-green waffle sweater seated in the single crimson-red and silver-grey mesh spring-cushioned chair on the right gently sways only her upper torso and shoulders rhythmically back and forth against the backrest in a subtle, soothing motion, holding the vintage camera calmly in her lap and smiling warmly beside the Golden Retriever dog resting peacefully on the sunlit wood deck on the left. Strictly one chair, one woman, and one dog, zero morphing, zero text.
  ```

---

## 3. Lệnh Chạy Nhanh Bằng 1 Dòng CLI Khi Lên Công Ty

1. **Kiểm tra cấu hình:**
   ```bash
   python3 -m flow_sku_tvc_toolkit validate --config products/occ1467_red_rocking_chair/sku_project.json
   ```
2. **Tạo 8 Ảnh TVC (`Nano Banana Pro 16:9`):**
   ```bash
   python3 -m flow_sku_tvc_toolkit run-images --config products/occ1467_red_rocking_chair/sku_project.json --phase all --no-auto-audit
   python3 -m flow_sku_tvc_toolkit map-uuids --config products/occ1467_red_rocking_chair/sku_project.json --force-remap
   ```
3. **Tạo 8 Video `8 Giây` (`Veo 3.1 - Fast`):**
   ```bash
   python3 -m flow_sku_tvc_toolkit run-videos --config products/occ1467_red_rocking_chair/sku_project.json --phase all --no-auto-audit
   ```
   *(Hoặc chạy lẻ đúng 1 clip để test bằng `--phase only --only-key "OCC1467_C5_V06_..."`)*.
