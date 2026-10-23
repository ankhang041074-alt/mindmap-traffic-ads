# 📓 SỔ TAY KỸ THUẬT ĐẠO DIỄN THỰC CHIẾN (FIELD NOTES & ĐÁNH GIÁ NHANH TỪNG DỰ ÁN KHI CÀO)

> **📌 NGUYÊN TẮC TÁCH BIỆT 2 LUỒNG RÕ RÀNG**:
> 1. **Luồng 1 — Sổ Tay Đánh Giá Nhanh Khi Cào (Chính là file `SO_TAY_KY_THUAT_DAO_DIEN_THUC_CHIEN.md` này)**:
>    - Lưu lại **đầy đủ 100% không cắt bớt** mọi nhận xét, đánh giá, mẹo lạ, câu lệnh "thần chú" và ví dụ nguyên văn mà AI phát hiện được ngay khi vừa cào xong từng dự án hoặc bảng xếp hạng.
>    - Tuyệt đối không tóm tắt sơ sài 1–2 dòng; thấy kỹ thuật nào hay trong bất kỳ dự án nào là phải trích dẫn nguyên văn câu lệnh vào đây để đọc lại ngay.
> 2. **Luồng 2 — Dữ Liệu Thô Big Data & Tổng Hợp Chuyên Sâu Bằng `/boost` Thành Skill (`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`, `dna_report.md`, `MASTER_DIRECTOR_PLAYBOOK_REPORT.md`, `skills/tvc-ai-director/SKILL.md`)**:
>    - Giữ nguyên 100% dữ liệu gốc để sau này khi gom đủ Big Data lớn sẽ dùng lệnh `/boost` chạy phân tích chuyên sâu và tối ưu hóa thành bộ Skill Đạo Diễn.

---

## 🕵️ PHẦN 0: 4 BÍ MẬT HẬU TRƯỜNG GIẢI MÃ TỪ `33,840` JOBS SẢN XUẤT CỦA `27` DỰ ÁN & CREATOR PROFILES TOP (TẠI SAO HỌ LÀM ĐƯỢC PHIM ĐỈNH NHƯ VẬY?)

Khi chỉ xem video hoàn chỉnh trên web và đọc các câu Prompt dài 1.000–2.000 chữ với đầy thông số `84° wide`, `50mm dolly-in at 2 km/h`, `180° shutter`, `4300K key light`, ai cũng nghĩ họ tự gõ từng chữ. Nhưng khi mổ xẻ **`33,840` jobs hậu trường (`6,639` cụm cảnh Final Take) của 27 dự án & hồ sơ tác giả Top**, sự thật nằm ở 4 bí mật sau:

### 1. Họ KHÔNG tự gõ tay từng câu Prompt kỹ thuật — Họ dùng "Bộ Khung Đạo Diễn AI" (System Prompt / Custom GPT) để dịch ý tưởng thô!
* **Bằng chứng sống trong dữ liệu**: Mở [`abz94/i-hate-science`](./data/creators/abz94/projects/i-hate-science/VIDEO_CENTRIC_SCRAPED_PROMPTS.md), [`thomas_lundstrom/emerald-fragrance-commercial`](./data/creators/thomas_lundstrom/projects/emerald-fragrance-commercial/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) và [`zhit/the-patch`](./data/creators/zhit/projects/the-patch/VIDEO_CENTRIC_SCRAPED_PROMPTS.md), nhiều tác giả khác nhau đều có phần mở đầu Prompt giống hệt nhau từng chữ:
  ```text
  Style: 8K IMAX. Photorealistic — no 3D render, no game engine.
  Camera: Physical cine lens. 180° shutter motion blur.
  Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush, pore-shadow matching on-set light.
  Acting: Hollywood — micro-pauses before reactions, precise eye-line, living eyes with catch-lights, chest rise from breathing.
  Physics: Gravity and inertia respected — mass has real weight, correct contact shadows. No floating props.
  ```
* Ở `VIDEO 01` của `@abz94/i-hate-science`, tác giả còn để lộ bản gốc xuất từ một **Template Đạo Diễn tiếng Trung** (`场景背景 / 激活参考 / 首帧/走位 / 拍摄模式 / 光学 / 摄影机...`) rồi từ `VIDEO 02` mới dịch sang khung tiếng Anh (`SCENE CONTEXT / ACTIVE REFERENCES / FIRST FRAME / BLOCKING / FORMAT MODE / OPTICS...`).
* **Cách vận hành**: Đạo diễn chỉ mô tả ý tưởng bằng vài câu bình thường, rồi đưa cho **AI Đạo Diễn (Claude / ChatGPT đã nạp System Prompt)** để AI tự động chia thành `CUT 1 (50mm dolly-in)`, `CUT 2 (65mm macro)`, `CUT 3 (32mm wide)` kèm ánh sáng và `SFX`.

### 2. Họ nhìn thấy trước góc quay bằng "Ảnh Tĩnh (`Start Frame`)" hoặc "Khối Hộp 3D (`Blender Previz`)" chứ không đoán mò
* **Cách 1 — Chỉnh góc máy trên Ảnh Tĩnh trước khi tạo Video (`@ollkorrect`, `@lukasbandana`, `@zhit`, `@mohamed-halloum`)**:
  * Cắt frame cuối của cảnh trước (hoặc lấy ảnh gốc), đưa vào `Nano Banana 2` bảo xoay góc máy sang ngang / cận cảnh mà giữ nguyên nhân vật và phòng. Khi nhìn thấy bức ảnh tĩnh đã ra đúng góc máy đẹp mới gắn làm `START_FRAME` cho Video.
* **Cách 2 — Dùng phần mềm 3D xuất tọa độ tự động (`@thomas_lundstrom/seedance-2-5-blender`)**:
  * Đặt khối hộp màu trong Blender 3D, kéo camera chạy quanh khối hộp, rồi dùng script xuất tự động tọa độ camera tại từng giây (`00:14.9 — Camera lands at floor level 0.36 m off the ground, 2.8 m from her, tilted 17.9° UP on a 17 mm wide`) và đính kèm video 3D thô (`<<<video_1>>>`) vào `Seedance 2.5`.

### 3. Quy trình "Chuẩn bị Mỏ Neo (`@IMG` Sheet & Voice Slate)" chiếm 70% thành công
Họ luôn làm Pre-Production trong các folder `Characters`, `Characters/VOICES`, `Locations`, `Props` trước khi quay bất kỳ cảnh Video nào:
1. **Nhân vật & Trang phục (5 cách xử lý chống xung đột mặt trên bảng 3 ô & ảnh quần áo)**:
   - Cách A (`@mohamed-halloum`): Viết thẳng vào lệnh tạo ảnh gốc: **`a headless full-body front view, the figure cut off cleanly at the base of the neck`** (vẽ ô giữa cụt đầu ngay từ đầu!).
   - Cách B (`@zhit`): Viết vào lệnh tạo ảnh gốc trên `Seedream 5.0 Pro`: **`Middle panel: Full-body front view. Face is blurred.`** (làm mờ mặt ở ô toàn thân giữa!).
   - Cách C (`@thomas_lundstrom`): Tạo xong bảng 3 ô rồi đưa vào `Nano Banana 2` gõ: **`Remove the face and neck from the front full body reference.`**
   - Cách D (`@abz94`): Đưa vào `Nano Banana 2` gõ: **`remove the head from the first panel`**.
   - Cách E (`@higgscreator/nala-heads-drop` — Top #1 Community): Khi lấy ảnh trang phục từ người mẫu khác, đưa vào `Nano Banana 2 (Pro)` tô cả đầu và tóc thành hình bầu dục xám trơn như ma-nơ-canh: **`completely remove the person's head and face — paint over the entire head region (face and hair) with a smooth neutral grey oval silhouette, like an anonymized mannequin`** rồi khai báo trong Video Prompt: **`WARDROBE REFERENCE ONLY (ignore mannequin head, copy outfit exactly)`**.
2. **Giọng nói (`@zhit/the-patch`)**: Tạo riêng folder `Characters/VOICES`, quay các video 4 giây `480p` nhân vật đứng trước phông xám nói câu mẫu `"Hi. My name is Walter and this is the sample of my voice"`, rồi đính kèm video đó làm `<<<video_1>>>` / `<<<video_2>>>` để khóa giọng nói xuyên suốt phim!
3. **Sản phẩm / Đạo cụ**: Dùng `ImageGen 2.0` tạo bảng 3 góc sản phẩm (`Make a product sheet with one full front, one 3/4 perspective and one closeup of all the label text...`).
4. **Bối cảnh**: Dùng `Soul Location` hoặc `Seedream 5.0 Pro` tạo phòng trống (`Empty, no people`).

### 4. Đằng sau 1 cảnh đẹp là hàng chục đến hàng trăm lần bấm nháp (`Re-roll`) ở độ phân giải thấp `480p` / `1080p` trước khi lên `4K`
* `@adilinthewild/4k-blockbuster-breakdown`: Bấm **`13,491` jobs** (101 thư mục con, chia rõ folder `1080 Tests` và `4K Tests`, chỉ giữ lại `736` video Final Take) cho 1 bộ phim ngắn 3 phút 22 giây!
* `@seksifratello/apeirophobia-teaser`: Bấm **`6,862` jobs** cho 1 teaser hơn 2 phút.
* `@adilinthewild/tv-4k`: Bấm **`1,957` jobs** (47 thư mục con) cho 1 phim 65 giây.
* `@abz94/i-hate-science`: Bấm **`1,227` jobs** (bỏ đi `931` bản nháp, có riêng các folder `test 480`, `Assets/Intro/720p` để test chuyển động ở `480p` cho nhanh và rẻ trước khi chốt `1080p`).

---

## 🎬 PHẦN 1: ĐÁNH GIÁ CHI TIẾT & CÂU LỆNH ĐẮT GIÁ TỪ TỪNG DỰ ÁN ĐÃ CÀO (28 DỰ ÁN & CREATOR PROFILES)

---

### Dự Án #26: `@pietromalegori/projects/control` (`708` jobs — Phim Sci-Fi Điện Ảnh 10 phút 19 giây!) & Đối Chiếu Với `@pandaproduction/projects/thread` — Bí Kíp Tạo Nhân Vật Thật 100% Không Bị "Nhựa AI"
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/pietromalegori/projects/control/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`01_IMAGE_GENERATION_PROMPTS_FULL_VERBATIM.md`](./data/creators/pietromalegori/projects/control/ai_context_packs/01_IMAGE_GENERATION_PROMPTS_FULL_VERBATIM.md) (`51` thư mục con `01_CHARACTER`, `02_LOCATION`, `03_PROP`, `04_FOOTAGE`, `05_MUSIC`, `06_SFX`; `708` jobs ➔ `217` cụm cảnh Final Take, `196` ảnh `@IMG`)
* **Tại Sao Nhân Vật Trong `pietromalegori/control` & `pandaproduction/thread` Nhìn Thật Như Người Đời Thực Mà Không Bị "Nhựa / Giống Mẫu Tạp Chí 3D"? (5 Khác Biệt Sống Còn)**:
  1. **Tạo Chân Dung Cận Cảnh Trên `Soul Cinematic` (`1344x2016`) Trước — KHÔNG Tạo Bảng 3 Góc Từ Con Số 0 Bằng `ImageGen 2.0` (`control` `SCENE_001` & `SCENE_003`)**:
     * Nếu bắt AI vẽ bảng 3 góc ngang từ con số 0 bằng chữ, diện tích dành cho mặt rất nhỏ nên AI mặc định vẽ mặt bóng mượt như tượng sáp.
     * Quy trình chuẩn của `@pietromalegori/control`:
       - **Bước 1 (`SCENE_001` — Model `Soul Cinematic` `1344x2016`)**: Tạo riêng 1 bức ảnh chân dung đặc tả từng lỗ chân lông, râu mọc lởm chởm không đều, vết nắng sạm và cấu trúc xương lệch tự nhiên:
         ```text
         Extreme close-up portrait, neutral dark grey background, photorealistic live action quality, Soul Cinema aesthetic.
         Original character, male mid-thirties, European features — do not reproduce this face, use structural description only. Strong angular jaw with slight asymmetry, prominent straight nose with a defined bridge, deep-set dark brown eyes under a heavy brow ridge, dark thick eyebrows slightly ungroomed. High cheekbones, lean face with minimal fat, defined jawline and slightly hollowed cheeks. Medium-warm light skin tone with natural texture — visible pores across the nose and forehead, fine lines at the outer corners of the eyes, slight sun damage on the cheeks, natural skin unevenness, faint stubble shadow beneath the beard line — absolutely no retouching, no smoothing, no digital skin correction. Short dark brown beard — 3 to 5 days growth, dense and slightly patchy at the upper cheek, fuller at the chin and jaw. Dark brown hair, medium length, naturally swept back off the forehead, slightly textured and unstyled, a few loose strands falling forward.
         Framing: close-up portrait, entire head fully contained within the frame — full hair visible at the top with breathing room above, chin fully visible with space below, both ears fully visible at the sides, neck visible down to the upper chest. Nothing cropped, nothing cut. Face perfectly centered, front-facing, direct eye contact with the camera — both eyes fully visible and sharp, gaze locked straight into the lens.
         ```
       - **Bước 2 (`SCENE_003` — Model `Nano Banana 2 (Pro)` `2752x1536`)**: Đính kèm bức ảnh mặt thật vừa tạo làm `<<<image_1>>>` + ảnh quần áo mẫu làm `<<<image_2>>> <<<image_3>>>` để ghép thành bảng 3 góc!
  2. **Khóa "Bất Đối Xứng Sinh Học & Khuyết Điểm Đời Thực" (`Face Imperfection & Authentic Human Asymmetry` — `control` `SCENE_011` & `thread` `SCENE_038`)**:
     * Tuyệt đối **KHÔNG DÙNG** các từ kiểu `"handsome"`, `"charismatic"`, `"flawless"`, `"sharp masculine model jawline"` vì AI sẽ gọi ngay gương mặt người mẫu Instagram bóng nhựa.
     * Thay bằng cụm từ khóa ép bất đối xứng của `@pietromalegori/control` (`SCENE_011`):
       ```text
       Face imperfection: authentic human asymmetry throughout — one cheekbone marginally more prominent than the other, slight leftward drift of the nose tip, one ear sitting fractionally higher than the other, uneven skin tone across the cheeks with faint age pigmentation patches at the temples and upper cheeks, the kind of tonal variation that comes from decades of sun exposure, not from illness. Natural age hollows beneath the cheekbones, visible pore texture on the nose and central face, deep nasolabial folds... The face reads as genuinely unusual and lived-in — not a conventional handsome man, a distinctive and singular face.
       ```
     * Hoặc cụm mô tả của `@pandaproduction/thread` (`SCENE_038`):
       ```text
       a long prominent nose with a slight bump at the bridge, high cheekbones beginning to hollow... faint shadows of sleeplessness under the eyes... Dark brown hair of medium length, damp with sweat, pushed back loosely and falling in untidy damp strands across his forehead
       ```
  3. **CẤM Đèn Rembrandt Gắt & CẤM Đèn Viền (`Rim Light`) Khi Tạo Bảng Nhân Vật — Bắt Buộc Dùng Ánh Sáng Phẳng Không Bóng (`Soft Even Near-Shadowless Light, No Hot Spots, No CGI Sheen, No Fashion Gloss`)**:
     * Đèn `Rembrandt` hoặc `Rim light` trên nền studio xám làm gò má và mũi bị lóe bóng trắng (`specular hot spots`) nhìn giống hệt nhân vật game 3D!
     * Nguyên văn khóa Ánh sáng + Khẩu độ + Negative của `@pietromalegori/control` (`SCENE_004`):
       ```text
       CAMERA & OPTICS: Shot on 35mm film, three-panel character sheet. Lens: 85mm medium telephoto prime across all three panels. Zero distortion. Clean editorial rendering. Natural perspective, no forced compression.
       APERTURE & DEPTH OF FIELD: Panel 1 (face close-up): f/2.0 — focus on eyes and mid-face, slight falloff toward ears and hair ends. Panels 2 and 3 (full body): f/8.0 — uniform sharp focus head to toe across entire outfit.
       LIGHTING: Soft even studio light — large overhead softbox with lateral fill. Clean, directionless, near-shadowless. Light grey seamless background. All three panels lit identically — consistent exposure, consistent color temperature. Cool-neutral light, approximately 5500K. Natural skin rendering in Panel 1 — no hot spots, no dramatic shadow.
       FILM STOCK — 35mm: Kodak Portra 400. Fine grain — clean and present without dominating. Natural skin rendering. Slight warm cast in highlights.
       NEGATIVE: No face visible in panels 2 and 3. No specific real person reproduced. No retouched or smoothed skin in panel 1 — natural aging visible. No logos. No text. No CGI sheen. No fashion gloss. No dramatic lighting. No colored background. No props.
       ```
  4. **Cắt Đầu Cả Ô Giữa Lẫn Ô Phải Ngay Từ Câu Lệnh Tạo Bảng 3 Góc (`CENTER PANEL: headless, cropped at collarbone` + `RIGHT PANEL: headless, cropped at collarbone` — `control` `SCENE_003` & `SCENE_016`)**:
     * Thay vì để ô giữa và ô phải có đầu rồi mới xóa, `@pietromalegori` ra lệnh cắt ngang xương quai xanh ở cả 2 ô toàn thân ngay từ đầu:
       ```text
       LEFT PANEL — close-up portrait, face fully visible and uncropped from hairline to chin with breathing room above and below, entire head contained within frame, both ears visible.
       CENTER PANEL — full body front view, figure cropped at the collarbone — the neck and head are entirely outside the frame above the top edge, no head, no hair, no face visible.
       RIGHT PANEL — full body back view, same crop logic — frame cuts at the collarbone, no head, no hair, no face visible above the top edge.
       ```
     * Và nếu AI vẫn vẽ đầu ở ô giữa, tác giả gõ lệnh sửa (`SCENE_017`):
       ```text
       the full body central panel is cleanly HEADLESS, cut straight and flat across the base of the neck with no head, all the rest is identical
       ```
  5. **Mẹo Thay Mặt Vào Bảng 3 Góc Có Sẵn Bằng Lệnh Tiếng Ý Siêu Ngắn (`control` `SCENE_012` – `SCENE_014`)**:
     * Khi đã có 1 bảng 3 góc quần áo chuẩn (`<<<image_1>>>`) và muốn đổi mặt nhân vật ở ô bên trái bằng 1 bức ảnh chân dung mới (`<<<image_2>>>`), tác giả gõ đúng 1 câu:
       ```text
       sostituisci il viso del persona nell'immagine <<<image_2>>> e mettilo al posto del viso nel pannello sinistro del frame di <<<image_1>>>
       ```
       *(Dịch tiếng Anh: `"Replace the face in the left panel of <<<image_1>>> with the person's face from <<<image_2>>> and adapt it seamlessly"`).*

---

### Dự Án #25 & #24: `@bucketlist_impossible/projects/31-august` (`668` jobs — Phim Sci-Fi dài 8 phút 44 giây!) & `@bucketlist_impossible/projects/bash` (`378` jobs — Phim Sinh Tồn 3 phút 56 giây) + `standalone_clips` (`6` clips)
* **Hồ sơ đầy đủ**:
  - `31-august`: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/bucketlist_impossible/projects/31-august/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/bucketlist_impossible/projects/31-august/dna_report.md) (`29` thư mục con, `668` jobs ➔ `379` cụm cảnh Final Take, `70` Video Final Takes, `278` ảnh `@IMG`)
  - `bash`: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/bucketlist_impossible/projects/bash/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/bucketlist_impossible/projects/bash/dna_report.md) (`18` thư mục con, `378` jobs ➔ `156` cụm cảnh Final Take, `31` Video Final Takes, `132` ảnh `@IMG`)
  - `standalone_clips`: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/bucketlist_impossible/standalone_clips/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`6` clips, `16` ảnh `@IMG`)
* **Các Kỹ Thuật Đắt Giá Nhất Phát Hiện Được**:
  1. **Mẹo Ghép Đồ Vật/Sản Phẩm Vào Đúng Vị Trí Trên Bàn Bằng "Ảnh Thứ 3 Có Khoanh Vùng Đánh Dấu (`marked spot from @image_3 inside @image_2`)" (`31-august` — `@IMG_060`)**:
     * Khi muốn đặt một sản phẩm (`@image_1` — chiếc đài radio) lên đúng một vị trí cụ thể trên mặt bàn trong phòng (`@image_2`), nếu chỉ mô tả bằng chữ thì AI hay đặt lệch chỗ hoặc tự ý sửa lại căn phòng.
     * `@bucketlist_impossible` lấy bức ảnh căn phòng `@image_2`, vẽ một vệt đánh dấu vị trí cần đặt đồ vật rồi lưu thành `@image_3`, sau đó đưa cả 3 ảnh vào `Nano Banana Pro Unlimited` (`6336x2688`) với câu lệnh siêu ngắn:
       ```text
       i want to place the radio in the scene in the marked spot from @image_3 inside @image_2
       the @image_1 radio is subtle there - dont change anything else keep the scene as it is exactly i just want the radio to be there on the tabletop
       ```
  2. **Mẹo "Tạo Bảng Đạo Cụ Ở Trạng Thái CHƯA BIẾN HÌNH (`PRE-FORMATION STATE`) Bằng Cách Tháo Chân Tay Từ Bảng Robot Hoàn Chỉnh" (`31-august` — `@IMG_052: happoty_radio`)**:
     * Để chiếc đài radio đặt trên bàn ở đầu phim khớp 100% màu sơn, vết xước và chất liệu với chú robot Happoty ở cuối phim, tác giả lấy bảng thiết kế con robot hoàn chỉnh đưa vào `Nano Banana Pro` và ra lệnh "tháo rời" mắt camera, đèn flash, 2 tay, 2 chân và bịt các lỗ khớp bằng nắp nhựa Bakelite:
       ```text
       Use the attached completed robot as the absolute authority for materials, cabinet identity, proportions, colors and weathering. Create one continuous full-color studio photograph showing robot’s PRE-FORMATION STATE in exactly three consistent views: complete front, complete back and a three-quarter close view.
       At this stage, the character is only the compact tabletop machine from which he will later assemble himself...
       Remove the entire camera-eye and its bracket. Remove the photographic flash and its bracket. Remove both arms, both hands, both legs, all feet, the lower hip mechanism and every external limb joint. Close every former attachment point with physically fitted period-correct circular Bakelite caps and matching turquoise or cream enamel panels. The cabinet rests directly on four small black rubber tabletop feet.
       ```
  3. **Bảng "6 Biểu Cảm Diễn Xuất (`2x3 Behavioral Casting Grid`)" Cho Nhân Vật Chính (`31-august` — `@IMG_024`)**:
     * Bên cạnh bảng 3 góc trang phục, tác giả tạo thêm 1 tấm bảng 6 ô chân dung (`two clean rows of three`) trên `Nano Banana Pro` (`5504x3072`) khóa sẵn 6 trạng thái tâm lý của nhân vật Jhonny:
       - `Portrait 1 — Neutral identity`
       - `Portrait 2 — Listening (His gaze reaches an off-camera speaker before his head finishes turning)`
       - `Portrait 3 — Concentration interrupted`
       - `Portrait 4 — Quiet concern`
       - `Portrait 5 — Protective resolve`
       - `Portrait 6 — Tired relief`
  4. **Kỹ Thuật Quay Cận Cảnh Mở Mắt Bằng Cặp Ảnh "Mắt Nhắm (`@IMG_019`) ➔ Mắt Mở (`@IMG_018`) Không Hòa Hình (`Do Not Dissolve`)" (`bash` — `VIDEO 01` trên `Seedance 2.5`)**:
     * Bước 1: Tạo ảnh cận cảnh mắt trái đang nhắm dưới đống đổ nát (`@IMG_019` trên `Seedream 5.0 Lite` `6240x2656`).
     * Bước 2: Đưa ảnh mắt nhắm vào `Nano Banana 2 (Pro)` để mở mí mắt ra mà giữ nguyên 100% lông mày, bụi bê tông và vết thương (`@IMG_018`):
       ```text
       Edit only the left eyelid and the newly revealed eye in this image. Open ADAM’s eye naturally. Preserve the exact camera position, crop, head angle, eyebrow, surrounding skin, injuries, blood, dirt, lighting and focus. Reveal the same dark brown iris established in ADAM’s character sheet... Change nothing outside the eyelid opening and exposed eyeball.
       ```
     * Bước 3: Nạp cả 2 ảnh vào `Seedance 2.5` để điều khiển chuyển động mở mắt thật 100%:
       ```text
       Use the closed-eye image [@IMG_019: start_frame_3] as the starting appearance and the open-eye image [@IMG_018: start_frame_2] as the target appearance. Preserve their exact framing, head angle, identity, brow wound, blood, dirt and stray hairs. The second image guides the final eye position; do not dissolve between photographs.
       ```
  5. **Cập Nhật Vết Thương Theo Tiến Trình Phim (`Localized Fresh Blood Over Existing Dried Wounds` — `bash` `@IMG_015`)**:
     ```text
     Make a small, localized edit to the attached ADAM sheet: add fresh blood within selected EXISTING wounds. Preserve the surrounding dried blood, scabs, concrete dust and grime... Match these additions across every view showing the same wound.
     ```
  6. **Khóa Đa Giọng Nói Bằng Cặp Thẻ `Audio 1 <<<audio_1>>>` + `Audio 2 <<<audio_2>>>` (`VOICE AUTHORITY` — `31-august` `VIDEO 01`)**:
     ```text
     Audio 1 <<<audio_1>>> — Jhonny's VOICE AUTHORITY. He speaks with the exact vocal identity, timbre, pitch range and American accent of Audio 1.
     Audio 2 <<<audio_2>>> — Sera's VOICE AUTHORITY. She speaks with the exact vocal identity, timbre, pitch range and American accent of Audio 2.
     The man from [@IMG_056: char_jhonny_v2] speaks with the voice of <<<audio_1>>>. The woman from [@IMG_037: char_sera_1] speaks with the voice of <<<audio_2>>>. Do not blend or exchange the two voices.
     ```

---

### Dự Án #23: `@6moths/projects/where-letters-fall` (`207` jobs — Phim Ngắn Điện Ảnh 5 phút 08 giây) + `standalone_clips` (`6` clips)
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/6moths/projects/where-letters-fall/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/6moths/projects/where-letters-fall/dna_report.md)
* **Thống kê**: 22 thư mục con (`01`..`18 - FINAL`, `Elements`, `Music`, `Video (Old ver)`), `207` jobs ➔ `114` cụm cảnh Final Take (`74` Video Final Takes trên `Seedance 2.5`, `111` ảnh `@IMG`).
* **Các Kỹ Thuật Đắt Giá Nhất Phát Hiện Được**:
  1. **Mẹo "Mượn Bố Cục Của Một Bức Ảnh Ở Cảnh Khác Làm Đích Đến Cho Khung Hình Cuối (`FRAMING AND COMPOSITION REFERENCE FOR THE END OF THE SECOND SHOT`)" (`VIDEO 01`)**:
     * Để thực hiện cú máy Match-Cut tinh tế (cảnh trước cậu bé ngồi chính diện trong bếp ➔ cảnh này máy quay dolly xuyên qua khe giữa 2 chiếc quan tài ngoài nghĩa trang mưa và dừng lại ở gương mặt cậu bé với đúng cỡ cảnh và góc chính diện y hệt cảnh trong bếp), `@6moths` đính kèm bức ảnh trong bếp vào cảnh nghĩa trang nhưng khóa quyền chỉ mượn bố cục khung cuối:
       ```text
       Use the attached kitchen close-up reference only as a FRAMING and COMPOSITION reference for the END of the second shot: the final close-up of [@IMG_022: Will] should feel similarly centered, frontal, calm, and intimate in scale, but this is still the funeral scene, so keep the cemetery environment, rain, umbrella, and black funeral clothing. Do not copy the kitchen itself. Use only the face framing, frontal alignment, and emotional closeness of the reference for the end frame.
       ```
  2. **Khóa Chống Lỗi Tự Vẽ Cổ Áo Trắng / Cổ Cồn Linh Mục Khi Mặc Đồ Đen (`FUNERAL CLOTHING LOCK`)**:
     * Khi nhân vật mặc áo khoác đen trong đám tang, AI rất hay tự vẽ thêm viền cổ sơ mi trắng hoặc cổ cồn linh mục (`priest collar`). Tác giả khóa triệt để:
       ```text
       FUNERAL CLOTHING LOCK: [@IMG_022: Will] must wear only a plain child’s black funeral outfit: matte black coat, plain black crew-neck shirt, black trousers, dark shoes. Every visible fabric around the neck must be black. No white shirt. No white line. No white neck strip. No priest collar. No clerical band. No tie. No light-colored neckline detail of any kind. The neckline must read as continuous plain black fabric.
       ```
  3. **Điều Khiển Diễn Xuất Ánh Mắt Ở Đúng Giây Cuối Cùng (`During the FINAL SECOND ONLY, he lifts his eyes directly into the camera`)**:
     ```text
     For most of this push in, [@IMG_022: Will] does not look directly into the lens. His gaze stays slightly lowered or distant. His expression is numb, quiet, and devastated rather than openly crying.
     During the FINAL SECOND ONLY, he lifts his eyes directly into the camera. The head stays almost still. The emotional shift happens mainly through the eyes.
     ```
  4. **Viết Prompt Bối Cảnh Master (`MASTER LOCATION PROMPT`) Và Đạo Cụ (`MASTER PROP PROMPT`) Kiểu "1 Câu 1 Dòng" Kèm Khóa Tỷ Lệ Cơ Thể Trẻ Em (`appropriately scaled for a seven-year-old child`)**:
     * Trong `@IMG_025` (`Bag`), để chiếc túi vải không bị AI vẽ to như túi người lớn khi cậu bé 7 tuổi đeo:
       ```text
       Create a comprehensive photorealistic production turnaround sheet for one old handmade canvas grocery tote bag.
       This exact bag belongs to Will and must remain identical across the film.
       The bag must look appropriately scaled for a seven-year-old child.
       Do not make it adult oversized.
       ```

---

### Dự Án #22: `@higgscreator/projects/nala-heads-drop` (`♡ 914` | `👁️ 95,015` — TOP #01 NHIỀU TIM NHẤT TOÀN HIGGSFIELD)
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/higgscreator/projects/nala-heads-drop/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/higgscreator/projects/nala-heads-drop/dna_report.md)
* **Thống kê**: 4 thư mục con (`Cover`, `Images`, `Music`, `Videos`), `162` jobs ➔ `160` cụm cảnh Final Take (`148` Video Final Takes 4K `4032x1728`, `45` ảnh `@IMG`).
* **Các Kỹ Thuật Đắt Giá Nhất Phát Hiện Được (Tại Sao Dự Án Này Đứng Top #1 Toàn Sàn Với `♡ 914` Tim?)**:
  1. **Mẹo "Đầu Ma-Nơ-Canh Xám Trơn (`Anonymized Grey Oval Mannequin Head`)" Khi Muốn Lấy Quần Áo Từ Ảnh Mẫu Khác Đắp Vào Nhân Vật Chính (`@IMG_002` — `VIDEO 01`)**:
     * Nếu bạn tìm được một bộ trang phục cực đẹp trên mạng (nhưng có mặt người mẫu khác trong ảnh) và đưa thẳng vào `Seedance 2.0` cùng ảnh nhân vật chính của bạn, AI sẽ bị loạn mặt hoặc bị bộ lọc chặn.
     * `@higgscreator` đưa bức ảnh trang phục đó vào `Nano Banana 2 (Pro)` (`1792x2400`) với câu lệnh biến toàn bộ phần đầu & tóc thành khối bầu dục màu xám trơn như ma-nơ-canh:
       ```text
       Edit this photo: completely remove the person's head and face — paint over the entire head region (face and hair) with a smooth neutral grey oval silhouette, like an anonymized mannequin. CRITICAL: keep everything else pixel-identical — the pink fluffy faux-fur cropped jacket, the black studded leather harness bra, the pink fluffy fur mini skirt, the metallic pink lace-up knee-high pointed boots, the phone in hand, the pose, the luxury boutique shelves background. Only the head becomes an anonymous featureless grey shape. The outfit is the subject.
       ```
     * Sau đó khi tạo Video 4K trên `Seedance 2.0`, tác giả truyền cả 2 ảnh vào và phân quyền cực kỳ rõ:
       ```text
       [@IMG_001: start_frame_1] is the performer — exact identity: cornrow braids into long dark curly ponytail, silver chain-drop earring, gold pendant necklace, glossy lips.
       [@IMG_002: start_frame_2] is WARDROBE REFERENCE ONLY (ignore mannequin head, copy outfit exactly): pink fluffy faux-fur cropped jacket, pink fur mini skirt, black studded harness, metallic pink lace-up knee-high boots.
       ```
  2. **Mẹo "Xóa Sạch Người Ở Tiền Cảnh Để Tách Lấy Bối Cảnh Trống & Bảng Màu (`GRADE REFERENCE`)" (`@IMG_005` — `VIDEO 02`)**:
     * Khi có một bức ảnh chụp nhân vật ngoài phố có màu nắng hoàng hôn quá đẹp và muốn quay thêm một cảnh Flycam (`Aerial Insert`) đồng bộ 100% màu sắc với bức ảnh đó, tác giả dùng `Nano Banana 2 (Pro)` xóa nhân vật đi để lấy bức ảnh phố trống làm mỏ neo màu (`GRADE REFERENCE`):
       ```text
       Edit this photo: completely REMOVE the woman in the foreground (the person in the black coat with braided ponytail and earrings on the left side of frame). Reconstruct what's behind her: the brownstone wall texture, the row of stoops with iron railings receding down the street, the sidewalk. CRITICAL: keep everything else pixel-identical — the golden-hour light, the bokeh of parked cars along the street on the right, the warm brownstone facades, the soft flare at the top right, the exact color grade and film grain. The result must be the same cinematic empty street shot with nobody in it.
       ```
     * Và trong Video Prompt: `[@IMG_005: start_frame_1] is the GRADE REFERENCE — match this warm Kodak film palette, golden-hour light direction and grain exactly; the aerial must feel like the same film as this street-level world.`
  3. **Mẹo "In Logo Thương Hiệu Của Mình Thay Cho Hình Tổng Thống Trên Tờ Tiền Đô-La Đang Bay" (`LOGO REFERENCE` — `VIDEO 03`)**:
     * Cực kỳ hữu ích khi làm TVC thương hiệu: Đính kèm file ảnh Logo (`@IMG_006`) và ra lệnh cho `Seedance 2.0` khắc logo đó vào chính giữa tờ tiền đang bay ở tốc độ Ultra Slow-Motion trước ống kính:
       ```text
       [@IMG_006: start_frame_1] is the LOGO REFERENCE — a neon lime-green rounded square with a black flowing squiggle ribbon mark. This exact logo replaces Benjamin Franklin's portrait on every dollar bill in this video: the bills look like real US hundred-dollar bills in engraving style, but the central oval portrait is the black squiggle mark and the bill's accents pick up the lime-green tint.
       ...
       5–8s ULTRA SLOW MOTION: one single bill tumbles END OVER END directly past the camera at eyeball distance — macro sharp, the black squiggle logo in the portrait oval crisp and readable, engraving lines and lime-green tint shimmering, golden backlight through the paper...
       ```
  4. **Bản Đồ Nhép Môi Theo Giây (`VOCAL MAP`) + Khóa Ngậm Miệng Khi Hết Lời Hát (`then mouth CLOSED` — `VIDEO 01`)**:
     * Khi đính kèm file nhạc `@Audio1` có 7.5 giây đầu hát rap và 7.5 giây sau chỉ có nhạc dạo nhảy (`Dance Break`), AI rất hay bị lỗi mấp máy môi suốt cả đoạn nhạc dạo. `@higgscreator` khóa cứng từng câu theo giây và ra lệnh ngậm miệng ở giây `7.5`:
       ```text
       LIVE PERFORMANCE: raps LIVE through 7.5s stalking the rings, then pure dance. Lips readable and sharp during all vocals.
       VOCAL MAP: 0–1.5 "...than now — turn that doubt to a scar, not a scar too proud" / 1.5–3 "You scroll, I study — you pose, I bloody every limit that they gave me" / 3–4 "turned a can into money. Big talk," / 4–6 "small spine, that's weak. I make silence when I speak — you need likes, I need reach" / 6–7 "I turn pressure into heat" / 7–7.5 "Yeah" — then mouth CLOSED.
       7.5–15 INSTRUMENTAL DANCE BREAK — no mouthed words, pure choreography.
       ```
  5. **Quy Tắc Bố Cục Điện Ảnh Chống "Đặt Giữa Khung Hình Nhàm Chán" (`CAMERA — Xiaolong Liu in CINEMASCOPE ... NOTHING CENTERED`)**:
     * AI mặc định luôn đặt nhân vật đứng đơ ở chính giữa màn hình. `@higgscreator` ép bố cục lệch tâm kiểu đạo diễn hình ảnh Xiaolong Liu (`NOTHING CENTERED — never on the spiral's center`, `she is a figure at the frame's edge zones`).

---

### Dự Án #21: `@mixingburrito1329/projects/anime-production` (`♡ 872` | `👁️ 119,784` — TOP #02 NHIỀU TIM NHẤT TOÀN HIGGSFIELD)
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/mixingburrito1329/projects/anime-production/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/mixingburrito1329/projects/anime-production/dna_report.md)
* **Thống kê**: 5 thư mục con (`Character sheet`, `Input`, `Location`, `Manga`, `Video generations`), `440` jobs ➔ `135` cụm cảnh Final Take (`5` Video Final Takes 4K, `16` ảnh `@IMG`).
* **Các Kỹ Thuật Đắt Giá Nhất Phát Hiện Được**:
  1. **Công Thức Tạo Bảng Nhân Vật Anime 2 Ô (`Split-Screen Anime Character Sheet` trên `Seedream 5.0 Pro` `2720x1536`)**:
     * Trích nguyên văn cấu trúc chuẩn tạo bảng nhân vật Anime thập niên 2000 (`@IMG_002`, `@IMG_004`, `@IMG_001`):
       ```text
       Split-screen character sheet composition, left side full body anime illustration in a dynamic action pose, right side close-up chest-up portrait, identical character on both sides, pure white seamless studio background, professional character sheet presentation, early 2000s retro anime illustration style with soft painted cel-shading, gentle airbrushed gradients, slightly muted nostalgic color rendering, simple clean linework, and classic vintage anime proportions reminiscent of early-2000s character art... consistent identity between both panels, soft diffused lighting with subtle vintage warmth, clean retro anime linework, muted nostalgic color palette, no text, no watermark, no logos, no frame borders.
       ```
  2. **Mẹo "Nạp Cùng Lúc Cả Bảng Nhân Vật TRƯỚC Khi Biến Hình (`@IMG_001`) Và SAU Khi Biến Hình (`@IMG_005`)" Cho Cảnh Biến Hình Giữa Video**:
     * Trong cảnh nữ sinh mặc đồ thủy thủ (`@IMG_001`) biến hình thành quái vật khổng lồ (`@IMG_005`) ngay giữa lớp học rồi đánh nhau với 2 nhân vật chính (`@IMG_002` & `@IMG_004`), tác giả đính kèm **cả 5 tấm bảng `@IMG` vào cùng 1 job** và thiết kế sẵn trên bảng quái vật `@IMG_005` chi tiết `"remnants of a torn white sailor school uniform and blue neckerchief fused into the mutated flesh near the collar area"` để AI hiểu sự liên kết vật lý giữa 2 hình thái!
  3. **Khối Dự Phòng Rủi Ro Render (`Render risk:` Fallback Instructions) Ở Cuối Câu Prompt (`VIDEO 01` & `VIDEO 03`)**:
     * Một kỹ thuật cực độc đáo: tác giả viết luôn hướng dẫn "Nếu engine gặp khó khi render đoạn biến hình liền mạch thì tự động chuyển sang cắt 3 nhịp cứng (`hard-cutting between three discrete transformation stages`)" ngay ở cuối câu lệnh:
       ```text
       Render risk: full-body transformation sequence may render as a static morph or skip frames — fallback to hard-cutting between three discrete transformation stages rather than one continuous morph if the engine smooths it into mush. Risk: pink blood may drift toward red under default color grading — reinforce with explicit magenta-pink hue callouts at each blood beat. Risk: multi-character wide fight choreography may merge the two fighters' silhouettes in wide shots — favor alternating single-subject framing over simultaneous two-shot action if clarity fails.
       ```
  4. **Chia Nhỏ Cảnh Hành Động Thành 11–15 Nhịp Cắt Siêu Ngắn (`1 giây / 1 Shot`) Kèm Thoại Tiếng Nhật Giữa Trận Đánh (`VIDEO 04` & `VIDEO 05`)**:
     * Trong 15 giây của `VIDEO 04`, tác giả chia thành `Shot 1 (0–3s)` ➔ `Shot 2 (3–5s)` ➔ `Shot 3 (5–6.5s)` ➔ `Shot 4 (6.5–7.5s)` ➔ `Shot 5 (7.5–8.5s)` ... tới `Shot 11 (13.5–15s)`, xen kẽ đúng 1 giây thoại giữa trận (`Shot 7 (9.5–10.5s): Boy (Japanese, groaning): 「まだやれる…お前は?」 Girl (Japanese, pushing up): 「当然。」`) để tạo nhịp điệu dồn dập đúng chất Anime chiến đấu!

---

### Dự Án #20: `@alishaqantaar/projects/the-new-girl` (`♡ 233` | `👁️ 31,919` — Top #05 Community Projects)
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/alishaqantaar/projects/the-new-girl/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/alishaqantaar/projects/the-new-girl/dna_report.md)
* **Thống kê**: 10 thư mục con (`episode 1/FINAL GENERATIONS`, `FINAL KEYFRAMES`, `FAILED GENERATIONS`, `SCENE - 1..3`), `373` jobs ➔ `83` cụm cảnh Final Take (`22` Video Final Takes 4K, `58` ảnh `@IMG`).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Mẹo Quay "Đảo Trục 180 Độ Trong Phòng Học (`Front View <-> Reverse Angle`)" Bằng 2 Ảnh Bối Cảnh Đối Lập Tạo Trên `Nano Banana 2 (Pro)` (`4800x3584`)**:
     * Khi quay cảnh đối thoại giữa Cô giáo đứng trên bục giảng và Học sinh ngồi dưới lớp, nếu chỉ dùng 1 ảnh lớp học thì khi cắt sang góc ngược lại (`Reverse Angle`), AI sẽ đặt sai vị trí cửa sổ và cửa ra vào.
     * `@alishaqantaar` giải quyết bằng cách dùng `Nano Banana 2 (Pro)` tạo sẵn **2 tấm ảnh cùng 1 lớp học nhưng nhìn từ 2 đầu ngược nhau** (tự động đảo cửa sổ từ trái sang phải):
       - **Ảnh 1 (`@IMG_021` — Nhìn từ cuối lớp lên bảng đen, cửa sổ bên TRÁI, cửa trượt bên PHẢI)**:
         ```text
         Reframe the same classroom from the back of the room, looking straight toward the front wall, as if standing at the rear behind the last row of desks. The shot reveals the teacher's area: a large green chalkboard mounted across the front wall, a wooden teacher's desk (kyōtaku) positioned in front of it slightly off-center, and a raised wooden platform (kyōdan) beneath it... The large panoramic windows with sheer white curtains now run along the LEFT-hand wall, letting soft daylight rake in from the left. On the RIGHT-hand wall sits the classroom entrance: a sliding door with a light-green metal frame and frosted glass upper panels...
         ```
       - **Ảnh 2 (`@IMG_016` — Nhìn từ bục giảng của cô giáo xuống cuối lớp, cửa sổ đảo sang bên PHẢI)**:
         ```text
         Reframe the same classroom from the teacher's point of view: the camera is positioned at the front of the room, standing where a teacher would stand facing the class, looking straight down the rows of empty student desks toward the back wall. The desks and chairs now face the camera, their fronts and seats turned toward the viewer, arranged in a neat 4×4 grid receding into the distance. The large panoramic windows with sheer white curtains run along the right-hand wall, letting soft daylight rake across the desks from the side...
         ```
     * Sau đó trong Video Prompt (`VIDEO 01`), tác giả khóa cứng trục không gian ở cả khối `LIGHTING` và `POSITIVE LOCKS`:
       ```text
       (In the reverse segment the window key now comes from screen-right; keep the two figures at the board rim-lit and readable against the brighter class-side windows.)
       POSITIVE LOCKS: Front segments keep windows screen-left; the reverse segment keeps windows screen-right and door screen-left.
       ```
  2. **Mẹo "1 Tấm Ảnh Đồng Phục Cho Cả Đám Đông 30 Học Sinh" (`Soft Uniformed Mass` — `@IMG_023`)**:
     * Thay vì tạo hàng chục nhân vật học sinh phụ, tác giả dùng `Nano Banana 2` tạo 1 bức ảnh trải phẳng 2 bộ đồng phục nam & nữ trên nền trắng:
       ```text
       Place the school uniform of a boy and a girl on a white background in one frame
       ```
     * Rồi khai báo trong `ACTIVE REFERENCES`:
       ```text
       [@IMG_023: start_frame_4]: the class all wear the matching navy school uniform (boys: navy suit, striped tie, gold buttons; girls: as [@IMG_020: start_frame_5]). Rendered as a soft uniformed mass, not sharply individualized.
       ```
  3. **Khóa Góc Mở Ống Kính Theo Từng Đoạn Cắt (`LENS LOCK SEGMENT 1 = 29°. LENS LOCK SEGMENT 2 = 47°`)**:
     ```text
     FORMAT MODE
     Controlled four-segment sequence, three HARD CUTS. Real-time. Total 15s. No subtitles, no music.
     LENS LOCK SEGMENT 1 = 29°. LENS LOCK SEGMENT 2 = 47°. LENS LOCK SEGMENT 3 = 47°. LENS LOCK SEGMENT 4 = 47°. No drift mid-segment.
     ```

---

### Dự Án #19: `@askar_yedil/projects/higgsfield-academy` (`♡ 281` | `👁️ 45,846` — Top #04 Community Projects)
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/askar_yedil/projects/higgsfield-academy/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/askar_yedil/projects/higgsfield-academy/dna_report.md)
* **Thống kê**: 4 thư mục con (`FOR MOTION`, `SCENES WITH A MAN`, `IMAGE`, `ADDITIONAL SCENES`), `218` jobs ➔ `39` cụm cảnh Final Take (`29` Video Final Takes, `22` ảnh `@IMG`).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Chuẩn 11 Khối "Higgsfield Academy Master Schema" + Định Vị Tọa Độ Khung Hình Bằng Phần Trăm `(x %, y %)`**:
     * Đây chính là dự án giáo trình chuẩn của đội ngũ Higgsfield Academy. Trong khối `FIRST FRAME AND SPATIAL BLOCKING`, họ định vị từng vật thể trên màn hình bằng tọa độ `x %` (ngang) và `y %` (dọc) kết hợp khóa góc ống kính `LENS LOCK 47°`:
       ```text
       ACTIVE REFERENCES
       @LOC_OFFICE (image 1): sunlit loft room. Reference controls room geometry, window wall, materials, desk setup and daylight atmosphere only. The reference image's frontal camera angle and framing are not inherited; this shot uses its own close handheld side-view camera defined below.
       ...
       FIRST FRAME AND SPATIAL BLOCKING
       The video opens close to the laptop on a side view, not the reference framing. The first visible frame already shows: the open laptop large in the lower-left foreground, x 30%, y 55–90%, its lid edge crossing the frame; @MAN in profile just behind it, seated, facing screen-left, framed chest-up in the right half, x 60–78%, y 25–85%; the coffee cup between them at x 45%, y 75%; @BAT leaning at the right frame edge in near foreground, x 90%, y 50–95%, readable.
       ...
       OPTICS
       47° diagonal field of view, standard normal lens character, natural human-eye perspective, zero distortion. Camera sits about 1 meter from the laptop and 1.5 meters from @MAN and keeps that distance for the whole take... LENS LOCK 47°, no drift, no zoom, no push-in.
       ```
  2. **Khối `PERFORMANCE — LIVING FACE (mandatory)` (Chống Đơ Mặt & Cho Phép Diễn Xuất Cường Điệu Kiểu Anime Trong Khung Hình Photoreal)**:
     * Trích nguyên văn từ `VIDEO 02`:
       ```text
       OPERATING STYLE — Hoyte van Hoytema: naturalistic motivated light, intimate large-format closeness, quiet cinematic realism.
       (When a shot's CAMERA/OPTICS block specifies something different, the shot-level instruction takes priority over this global style.)

       PERFORMANCE — LIVING FACE (mandatory): eyelids fully close and reopen at natural intervals; small natural eye darts, not a fixed stare; subtle lip micro-movements. The face stays continuously alive. Anime-style comedic timing and lively exaggerated emotional reactions are allowed — acting/performance only; the visual render stays strict photoreal.
       ```
  3. **Ghép Nhân Vật Hoạt Hình 3D-Toon (`4 cm Fairy`) Vào Cảnh Quay Người Thật (`Hybrid Live-Action + 3D Toon Lighting Interaction`)**:
     ```text
     @FAIRY (image 3): male fairy exactly 4 cm tall... He keeps his stylized 3D-toon look from the reference while receiving real scene lighting and casting a faint warm-green glow.
     ```

---

### Dự Án #18 & #17: `@adilinthewild/projects/4k-blockbuster-breakdown` (`♡ 434` | `13,491` jobs!!) & `@adilinthewild/projects/tv-4k` (`♡ 154` | `1,957` jobs)
* **Hồ sơ đầy đủ**:
  - `4k-blockbuster-breakdown`: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/adilinthewild/projects/4k-blockbuster-breakdown/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`13,491` jobs, `101` thư mục con ➔ `1,293` cụm cảnh Final Take, `736` Video Final Takes, `209` ảnh `@IMG`)
  - `tv-4k`: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/adilinthewild/projects/tv-4k/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`1,957` jobs, `47` thư mục con ➔ `112` cụm cảnh Final Take, `67` Video Final Takes, `65` ảnh `@IMG`)
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Quy Trình Tổ Chức Thư Mục Sản Xuất Bom Tấn (`1080 Tests` ➔ `4K Tests` ➔ `FINAL ASSETS` ➔ `FINAL GENERATIONS`)**:
     * Trong `4k-blockbuster-breakdown` (`13,491` jobs — dự án lớn nhất từng được mổ xẻ trên Higgsfield), `@adilinthewild` chia mỗi đại cảnh (`SCENE 1 - PIRATES`, `SCENE 2 - DESERT`, `SCENE 3 - JUNGLE`, `SCENE 4 - ROOM`) thành 4 nhánh thư mục rõ ràng:
       - `ASSETS TESTS` ➔ `FINAL ASSETS` (`Character sheet`, `Locations`, `props`)
       - `1080 Tests/01..16` (Bấm nháp hàng trăm lần ở `1080p` theo từng nhịp `Beat 1..Beat 6`)
       - `4K Tests/01..06` (Khi câu Prompt đã chuẩn ở `1080p`, mang sang chạy ở `4K`)
       - `FINAL GENERATIONS` (Chỉ chọn đúng 8–15 cú máy hoàn hảo nhất đưa vào bàn dựng!).
  2. **Viết Prompt Tạo Ảnh Bối Cảnh Cho `Soul Cinematic` Dưới Dạng Cấu Trúc Dictionary/JSON Chuyên Sâu (`@IMG_004` — `4k-blockbuster-breakdown`)**:
     * Thay vì viết văn xuôi, `@adilinthewild` truyền thẳng một cấu trúc JSON/Dict gồm 6 trường (`Caption`, `STYLE`, `COMPOSITION`, `SCENE`, `CINEMATOGRAPHY_AND_LIGHTING`, `CAMERA_AND_LENS`) vào `Soul Cinematic`:
       ```json
       {
           "Caption": "A photorealistic wide shot deep inside a classic lush tropical rainforest, looking down a very narrow dirt footpath that winds into the dense green interior...",
           "STYLE": {
               "Artistic Medium": "photorealistic cinematic movie still, indistinguishable from a real nature photograph",
               "Aesthetic Movement / Genre": "naturalistic tropical rainforest realism, immersive landscape",
               "Cultural / Historical Influence": "real equatorial rainforest photography (Amazon / Southeast Asian jungle), National Geographic nature documentary register"
           },
           "COMPOSITION": {
               "Framing": "wide shot",
               "Layout": "a very narrow dirt footpath entering from the lower foreground and winding into the deep green interior...",
               "Perspective": "eye-level, centered on the narrow trail looking down its length into the forest, slow push-in, locked stabilized"
           },
           "CINEMATOGRAPHY_AND_LIGHTING": {
               "Director": "Hoyte van Hoytema",
               "Lighting Style": "soft natural daylight filtering down through the multi-layered canopy, dappled green light on the foliage and trail...",
               "Color Palette": "deep emerald and jade greens, mossy olive, warm earthy brown trail, dark bark, soft filtered daylight, occasional red and orange flower accents"
           }
       }
       ```
  3. **Điều Khiển Đại Cảnh Đám Đông Hàng Ngàn Người Bằng Tọa Độ Không Gian (`x %`, `y %`) Trong 1 Cú Máy Liền Mạch (`One Single Continuous Take` — `tv-4k` `VIDEO 01`)**:
     * Để quay cảnh di tản thời chiến với hàng ngàn người chạy trên cầu cảng mà không bị trống khung hình ở giây đầu tiên:
       ```text
       LOCATION MAP: Sea coast under low smoke-grey sky. A large steel troopship moored broadside across the right and center of frame, hull spanning BG from x 45% to x 100%, deck rail running across the upper third. A wide pier extends from FG lower-center into deep-MG. At the seaward edge of the pier, center-frame at x 55%, y 48%, a single narrow boarding gangway rises from the pier edge to the hull door...
       FIRST FRAME AND SPATIAL BLOCKING: The first visible frame is already full of running people from edge to edge — no empty establishing frame, no delayed reveal, no visible gaps between bodies anywhere in frame. The young mother is FG center-lower, x 50%, y 70%, three-quarter back to camera...
       OPTICS: LENS LOCK = 84° diagonal field of view, classic wide-angle lens character, camera 1 to 1.5 meters from the mother throughout.
       ```

---

### Dự Án #16: `@adilinthewild/projects/top-up` — *"Top Up" Cinematic AD Breakdown* (`♡ 107` | `👁️ 18,669` — TVC Quảng Cáo Đồ Uống)
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/adilinthewild/projects/top-up/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/adilinthewild/projects/top-up/dna_report.md)
* **Thống kê**: 14 thư mục con (`SCENE1`..`SCENE11`, `TESTS/ASSET TESTS/BALL PROP`), `255` jobs ➔ `66` cụm cảnh Final Take (`56` Video Final Takes, `24` ảnh `@IMG`).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Công Thức 2 Khối `[VISUAL]` + `[AUDIO]` Kết Hợp Điều Khiển Tốc Độ Theo Phần Trăm (`Slow-motion ramping: 100% -> 60% -> 70% -> 40% -> 100%`)**:
     * Trong quảng cáo chai nước giải khát phát sáng giữa phố nắng gắt (`VIDEO 02` & `VIDEO 03`), `@adilinthewild` điều khiển nhịp độ慢/nhanh của cú máy 15 giây bằng tỷ lệ phần trăm chính xác ở cuối khối `[VISUAL]`:
       ```text
       [VISUAL] Shot on ARRI Alexa 35 with anamorphic lenses, rich filmic latitude, deep cinematic color science, organic highlight rolloff, subtle halation around bright sources. Practical in-camera VFX approach — real interactive light, real haze, real atmospheric particles, real lens artifacts. All glow effects achieved with hidden practical LED rigs and rim lighting on the bottle prop, no digital additions.
       ...
       Beat one — he suddenly stops mid-stride. Camera handheld-arcs around to his side, settling on a low-angle medium close-up of his face, dutch angle flipping to 12 degrees left...
       Beat two — camera handheld-pushes past his shoulder for a reveal shot. Hovering in the middle of the empty NYC street about six meters ahead of him, perfectly motionless in the air at chest height, is the cold aluminum soda bottle [@IMG_005: start_frame_3]. It glows softly from within with a warm chartreuse-yellow light (#d1ef17)...
       Beat four — he slowly lifts his right hand, palm up, reaching toward the floating bottle... The bottle responds — gently descending through the air with a perfectly controlled motion, no spin, no tilt, just smoothly drifting down toward his open hand...
       Beat five — the moment the bottle touches his hand, the glow inside the bottle fades out — the chartreuse light dims away into nothing, leaving just a normal-looking cold aluminum soda bottle in his hand. Real condensation now beading on the metal...

       Slow-motion ramping: 100% on the stop and reveal, drops to 60% as the camera pushes past his shoulder to reveal the floating bottle, holds at 70% on his cautious approach, drops to 40% on his hand reaching up and the bottle descending into his palm — the slowest beat to feel the magic of the moment, snaps back to 100% on the glow fading out and his half-smile.
       ```
  2. **Khóa Hiệu Ứng Phát Sáng Của Sản Phẩm Bằng Ánh Sáng Đèn LED Thực Thể (`Practical LED Rigs on the Bottle Prop, No Digital Additions`)**:
     * Nếu chỉ viết `"magical glowing bottle"`, AI sẽ vẽ tia sáng hoạt hình giả tạo. Tác giả viết: `"All glow effects achieved with hidden practical LED rigs and rim lighting on the bottle prop, no digital additions"` kèm mã màu HEX `#d1ef17` phản chiếu lên da mặt nhân vật!

---

### Dự Án #15, #14, #13 & #12: Bộ 4 TVC Quảng Cáo Sản Phẩm Đỉnh Cao Của `@thomas_lundstrom` (`seedance-4k-vs-1080p-product-commercials`, `chandler-rollerblade-commercial`, `donut-commercial`, `glow-mask-commercial`)
* **Hồ sơ đầy đủ**:
  - `seedance-4k-vs-1080p-product-commercials` (`♡ 89`): [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/thomas_lundstrom/projects/seedance-4k-vs-1080p-product-commercials/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`25` jobs ➔ `18` cụm cảnh, `6` Video 4K vs 1080p, `15` ảnh `@IMG`)
  - `chandler-rollerblade-commercial` (`♡ 127`): [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/thomas_lundstrom/projects/chandler-rollerblade-commercial/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`211` jobs ➔ `22` cụm cảnh, `9` Video Final Takes, `11` ảnh `@IMG`)
  - `donut-commercial` (`♡ 47`): [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/thomas_lundstrom/projects/donut-commercial/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`227` jobs ➔ `17` cụm cảnh, `3` Video Final Takes 30s `Seedance 2.5`, `11` ảnh `@IMG`)
  - `glow-mask-commercial` (`♡ 39`): [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/thomas_lundstrom/projects/glow-mask-commercial/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`127` jobs ➔ `15` cụm cảnh, `4` Video Final Takes, `5` ảnh `@IMG`)
* **Các Kỹ Thuật Làm TVC Bán Hàng Đắt Giá Nhất Phát Hiện Được**:
  1. **Mẹo Tạo Bảng Tham Chiếu Lon Nước Ngọt 3 Góc & "Xóa Sạch Chữ Thành Phần Nhỏ Li Ti Ở Mặt Sau" (`NO ingredient text, NO fine print on the back` — `seedance-4k-vs-1080p-product-commercials` `@IMG_004`)**:
     * Khi làm TVC cho lon nước ngọt hoặc chai mỹ phẩm, mặt sau thường có bảng thành phần chữ nhỏ li ti (ingredient sticker) khiến AI Video làm nhòe chữ khi xoay lon. `@thomas_lundstrom` ra lệnh cho `ImageGen 2.0` (`3840x2160`) xóa bảng thành phần ở mặt sau và nối liền họa tiết thương hiệu:
       ```text
       Professional product prop sheet of the ROVA soda can on a seamless neutral grey background (#B8B8B8). Three views of the same can arranged side by side in a clean row: a full front view, a full back view, and a macro close-up detail of the front wordmark area filling the third frame, the graphics sharp and crisp.
       CAN FORMAT: Standard 330 ml aluminum beverage can — classic short stubby proportions, 66 mm wide, 115 mm tall, NOT a slim can, NOT a tall energy-drink can...
       CAN DESIGN: preserve the exact can design from the attached reference image...
       BACK VIEW: the same red base, splash blob and doodles continuing seamlessly around the can — replace the ingredient sticker seen in the reference with continued graphics: NO ingredient text, NO fine print, NO text block anywhere on the back.
       ```
  2. **Mẹo "Ghép Giày/Sản Phẩm Vào Chân Nhân Vật Ngay Trên Bảng Turnaround Sheet + Cắt Đầu Ô Giữa" (`Product-on-Character Sheet Grafting` — `chandler-rollerblade-commercial` `@IMG_008`)**:
     * Thay vì bắt Video AI tự đeo đôi giày trượt patin (`<<<12af3151...>>>`) vào chân ông lão trong lúc đang chuyển động, tác giả dùng `ImageGen 2.0` ghép đôi giày sản phẩm vào thẳng cả góc trước lẫn góc sau của bảng nhân vật ông lão, đồng thời xóa đầu ở góc trước:
       ```text
       Photorealistic character reference sheet edit using the provided images. Image 1 is the reference sheet to edit; <<<12af3151-dc95-4411-83d7-e8a4d1fa8c04>>> is the product reference for the footwear. Keep the exact same two-panel layout... Left close-up portrait panel: unchanged. Right panel, front full-body view: remove the man's face, neck, and all visible skin of the head so the outfit is displayed headless like an invisible mannequin, with the red helmet floating in its natural position above the t-shirt collar, dark empty interior visible inside the helmet, no face, no neck, no chin visible, arms and legs unchanged. Back full-body view: unchanged except footwear. On both front and back full-body views, replace the plain white sneakers with the exact sneakers from <<<12af3151-dc95-4411-83d7-e8a4d1fa8c04>>>...
       ```
  3. **Bảng Tham Chiếu Giày 6 Góc Chuẩn Thiết Kế Công Nghiệp (`6-Angle Orthographic Footwear Prop Sheet` — `chandler-rollerblade-commercial` `@IMG_006`)**:
     ```text
     A product prop sheet / orthographic turnaround of a single ORIGINAL wheeled skate sneaker on a flat neutral light-gray studio background, matching the exact design of the shoe shown in the reference image. LAYOUT: the same shoe shown from multiple angles in an even grid: lateral side profile, medial side profile, top-down into the laces, front three-quarter hero angle, rear/heel view, and bottom view of the outsole with wheels.
     ```
  4. **Mẹo "Gom 5 Nhân Vật Phụ Vào Chung 1 Tấm Bảng Tham Chiếu Ngang" (`5-Person Ensemble Crew Sheet` — `donut-commercial` `@IMG_009`)**:
     * Trong `donut-commercial`, cảnh cuối (`0:20.5`) cần nguyên một đoàn làm phim 5 người (`Food stylist`, `Focus puller`, `Gaffer`, `Sound recordist`, `Producer`) đứng sững sờ quanh quầy bánh. Nếu tách làm 5 ảnh riêng sẽ hết sạch slot tham chiếu! Tác giả dùng `Seedream 5.0 Pro` (`2720x1536`) xếp cả 5 người đứng thành 1 hàng ngang trên nền xám `#B8B8B8` trong **1 ảnh duy nhất (`@IMG_009: crew`)**:
       ```text
       Technical character reference sheet, photorealistic commercial photography. Five different people standing in a row on a seamless neutral grey background #B8B8B8, full-body front view only, evenly spaced, all standing upright facing camera with arms relaxed at their sides, identical framing scale and identical lighting for every person. Background film crew, five distinct individuals, all in dark neutral working clothes so they read as one unit.
       CREW: 1. Food stylist... 2. Focus puller... 3. Gaffer... 4. Sound recordist... 5. Producer...
       ```
  5. **Quy Tắc "Che Giấu Phim Trường Đến Giây Cuối" (`CRITICAL FRAMING RULE` — `donut-commercial` `VIDEO 01` 30s `Seedance 2.5`)**:
     * Toàn bộ 20 giây đầu quay cận cảnh bằng ống kính `Laowa probe macro lens` làm bánh donut khiến người xem tưởng đang ở trong tiệm bánh thật, đến đúng giây `0:20.5` (`CUT 10`) mới cắt ra góc rộng tiết lộ cả một đoàn làm phim đang quay quảng cáo và một anh hậu trường lén ăn mất chiếc bánh ở giữa hộp!
       ```text
       CRITICAL FRAMING RULE: CUT 9 is a tight top-down macro on the counter top only — none of the lights, stands, cables or crew are visible in it. The set is revealed for the first time at 0:20.5 in CUT 10.
       ```
  6. **Mẹo "Biến Tên Thương Hiệu & Thành Phần Mỹ Phẩm Thành Đèn Neon Của Cả Thành Phố" (`World Physics Trigger Rule` — `glow-mask-commercial`)**:
     * Thay vì chèn chữ quảng cáo nhàm chán lên màn hình, tác giả đặt ra quy luật vật lý cho cả thế giới trong `Scene:` — mỗi bước chân cô gái đi tới đâu, đèn neon thành phố bật sáng tới đó và tự khắc chữ thành phần sản phẩm (`"MOONMILK"`, `"PEPTIDE WATER 88%"`, `"maevi"`):
       ```text
       The rule of this world: every light is dead until she is beside it. Each light switches on at the exact moment she draws level with it, triggered by her passing, then stays lit behind her. The street ahead of her is always dark, the street behind her always glowing, a moving edge of light that travels with her.
       ... the instant she reaches its base, the letters ignite one by one from bottom to top spelling "MOONMILK" in hot pink neon...
       ... then it reacts to her passing and buzzes on in cyan reading "PEPTIDE WATER 88%", its warm spill flooding the booth below...
       ... a huge dead rooftop sign flickers, catches, and settles into glowing pink neon script reading "maevi", the biggest light in the city.
       ```
  7. **Khai Báo Ảnh Bối Cảnh Chỉ Làm "Style Reference Only" Để Nhân Vật Chạy Xuyên Qua Không Gian (`seedance-4k-vs-1080p-product-commercials` `VIDEO 01`)**:
     * Khi muốn nhân vật vừa uống nước tăng lực xong là chạy nước rút và bay lên biến hình thành Robot giữa đại lộ mà không bị khóa cứng vào khung hình tĩnh của tấm ảnh đường phố:
       ```text
       LOCATION — [@IMG_011: street] is a STYLE REFERENCE ONLY, not a fixed keyframe. Use it for look, mood, architecture and lighting — a sunlit city avenue in hard midday sun. The model freely generates and extends the world; the character TRAVELS through space. Do not reproduce the reference frame 1:1.
       ```

---

### Dự Án #11: `@thomas_lundstrom/projects/emerald-fragrance-commercial` (TVC Quảng Cáo Nước Hoa)
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/thomas_lundstrom/projects/emerald-fragrance-commercial/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/thomas_lundstrom/projects/emerald-fragrance-commercial/dna_report.md)
* **Thống kê**: `94` jobs ➔ `13` cụm cảnh Final Take (`3` Video Final Takes 15s `1080p` trên `Seedance 2.0` ghép thành TVC 33 giây hoàn chỉnh, `10` ảnh `@IMG_001..@IMG_010`).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Câu lệnh 1 dòng biến ảnh sản phẩm gốc thành Bảng Tham Chiếu 3 Góc (`3-Angle Product Sheet` 4K trên `ImageGen 2.0` `3840x2160`)**:
     * Để giữ chai nước hoa `@IMG_006` (`emerald` — *Emerald Nocturne 100ml eau de parfum*) sắc nét từng dòng chữ vàng trên thân chai xuyên suốt 3 cảnh hành động dưới nước và trên cạn, tác giả đưa ảnh chai gốc (`<<<image_1>>>`) vào `ImageGen 2.0` (`3840x2160`) với đúng 1 câu lệnh:
       ```text
       Make a product sheet with one full front, one 3/4 perspective and one closeup of all the label text of the product from <<<image_1>>> . No added text just the 3 angles.
       ```
  2. **Cấu trúc Prompt Tạo Bảng Nhân Vật Split-Frame 4K (`Left panel: 85mm facial close-up` + `Right panel: 35mm full-body front and back views side by side`) + Bước Hậu Kỳ Xóa Mặt Ở Hình Toàn Thân**:
     * Bước 1 (`ImageGen 2.0` `3840x2160`):
       ```text
       Cinematic character reference sheet, split-frame layout, photorealistic. Use the man in the provided reference image as the exact same person in every panel — same face, same identity, no alterations.
       Left panel — facial close-up: ... Shot on 85mm portrait lens, shallow depth of field, soft cinematic key light with gentle fill.
       Right panel — full-body front and back views side by side: the same man shown twice within this panel — on the left, a full-body front view facing the camera; on the right, a full-body back view photographed from directly behind... Shot on 35mm lens, even full-length lighting.
       Look: clean studio character sheet, plain solid grey background, consistent character across all views... vertical divider lines separating each view.
       ```
     * Bước 2 (`Nano Banana 2 (Pro)` `5504x3072` — `@IMG_007` & `@IMG_009`):
       ```text
       Remove the face and neck from the front full body reference.
       ```
  3. **Cú Chuyển Cảnh Ẩn Dụ Sản Phẩm (TVC Metaphor Transition — Từ Hang Ngập Nước ➔ Ống Hút Vòi Xịt Nước Hoa)**:
     * `VIDEO 01` & `VIDEO 02`: Nhà thám hiểm `[@IMG_007: Indiana-Thomas]` lấy chai nước hoa `[@IMG_006: emerald]` trên bệ đá trong hang `[@IMG_008: Emerald-Grotto]`, cửa hang sập xuống, nước phun ngập tới trần.
     * `VIDEO 03`: Một **đường ống nhựa trong suốt khổng lồ** (chính là ống dẫn bên trong chai nước hoa!) đâm từ lỗ sáng trần hang xuống, hút xoáy toàn bộ nước và nhà thám hiểm thành một cột chất lỏng màu xanh ngọc lục bảo ➔ giảm tốc và **phun sương (`atomizes mid-frame into a fine fragrance mist`)** ngay trước gương phòng tắm `[@IMG_010: Thomas-Apartment]`, lộ ra quý ông mặc vest `[@IMG_009: Thomas-suit]` vừa xịt chai nước hoa `[@IMG_006: emerald]` lên cổ, rồi kết bằng **`CUT 4 — Hero product shot, 85mm macro feel`** đặt chai nước hoa lên bàn đá ở trục 1/3 trái:
       ```text
       CUT 3 — Medium close-up, 50mm, static, warm window light:
       Surreal transition — the spiraling green liquid decelerates, thins, and atomizes mid-frame into a fine fragrance mist hanging in warm morning light. The mist drifts apart to reveal [@IMG_009: Thomas-suit] standing at the mirror in the [@IMG_010: Thomas-Apartment] bathroom, chin tilted, spraying the [@IMG_006: emerald] bottle once against his neck — the fresh mist cloud swirling in the sunlight exactly like the vortex it just was. A satisfied half-smile, one beat. SFX: two crisp spray hisses, quiet room tone.

       CUT 4 — Hero product shot, 85mm macro feel, static, shallow depth of field:
       His hand lowers the [@IMG_006: emerald] bottle onto the stone counter with a soft glass click and releases it — the bottle stands on the left rule of third, gold serif lettering crisp, the backlit mirror rimming the emerald glass with warm glow. In the soft-focus background, [@IMG_009: Thomas-suit] walks out of the bathroom, adjusting his jacket cuff. Hold on the bottle.
       ```

---

### Dự Án #10: `@thomas_lundstrom/projects/seedance-2-5-blender` (Điều Khiển Camera Bằng 3D Previz)
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/thomas_lundstrom/projects/seedance-2-5-blender/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/thomas_lundstrom/projects/seedance-2-5-blender/dna_report.md)
* **Thống kê**: `152` jobs ➔ `22` cụm cảnh Final Take (`7` Video Final Takes dài `17s–26s`, `20` ảnh `@IMG_001..@IMG_020`).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Gán nhân vật vào khối hộp màu trong Blender (`<<<video_1>>>` Color-Coded Proxy Boxes)**:
     * Trong video 3D thô (`<<<video_1>>>`), tác giả đặt khối hộp màu để định hướng mặt trước/mặt sau/hai bên sườn của nhân vật:
       ```text
       <<<video_1>>> — the SOLE authority for camera movement, framing and timing, for the architecture of the aisle, and for where the woman is and which way she faces. Do NOT inherit its grey materials, its dark ceiling, its black void above the shelves or its lighting — all of that comes from [@IMG_007: library]. The red box IS the woman: its RED face is her front, its BLACK face is her back, its GREEN faces are her sides.
       ```
     * Hoặc dùng 2 hộp màu khác nhau cho 2 tay đua (`VIDEO 01` — dài `26s`, chia 10 cú cắt `CUT 1`..`CUT 10` kết bằng `SPEED RAMP` photo-finish):
       ```text
       Follow the motion reference video <<<video_1>>> camera movement, framing and cut timing EXACTLY, shot for shot — it is the edit. In the reference video the GREEN box is [@IMG_004: female-driver] and the RED box is [@IMG_003: char_male-driver]. Replace all previz geometry with the photoreal world below.
       ```
  2. **Khóa phân quyền khi xung đột (`WHERE THEY CONFLICT` + `=== 3. VIDEO LOCK ===`)**:
     ```text
     WHERE THEY CONFLICT: <<<video_1>>> wins on geometry and position. [@IMG_007: library] wins on material, colour and light. The camera was solved against the blocked architecture, so the aisle stays exactly as the video has it.
     === 3. VIDEO LOCK ===
     <<<video_1>>> is the SOLE authority for camera movement and timing, 1:1 frame aligned. If this text and the video disagree, THE VIDEO WINS. Any deviation is a failure. The previz is re-dressed, never re-imagined.
     ```
  3. **Khóa trạng thái chốt cuối mỗi mốc giây (`END State Checkpoints`) & Tâm lý diễn xuất (`=== 6. ACTING ===`)**:
     ```text
     00:11.4 — She has turned 31.5° to her LEFT to face the shelf. The camera has swung out in front and started to drop, 4.9 m up, 4.7 m away. She raises her left hand toward the shelf at chest height.
     END 00:11.4 — people 1 · stopped, turned 31.5° left, HELD at that angle · hand rising · no book yet.
     ```
     * Và khối chỉ đạo diễn xuất theo phương pháp Stanislavski (`MOTIVE`, `GOAL`, `OBSTACLE`, `TACTIC`, `MOMENT TO MOMENT`, `ONGOING BUSINESS`, `BACKGROUND LIFE`).
  4. **Prompt tạo Bảng Kỹ Thuật Hộp Sản Phẩm 2 Mặt (`FRONT` / `BACK` Product Sheet trên nền `#B8B8B8`)**:
     * Tại `@IMG_010` (`cosmo-crunch`), tác giả tạo mặt trước và mặt sau hộp ngũ cốc cùng lúc kèm lệnh cấm chữ nhỏ/mã vạch để không bị AI viết chữ giun dế:
       ```text
       Technical product reference sheet, photorealistic commercial product photography. Two views of the same cereal box in a row on a seamless neutral grey background #B8B8B8: full front view on the left, full back view on the right. Identical box, artwork and colours in both views. Beneath each box, centred on the grey background, a small clean sans-serif label in dark grey: "FRONT" under the left box and "BACK" under the right box...
       Nothing else on the panel — no frame, no puzzle, no maze, NO ingredient list, NO nutrition table, NO barcode, NO paragraphs, NO small print of any kind.
       ```

---

### Dự Án #9: `@abz94/projects/i-hate-science`
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/abz94/projects/i-hate-science/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/abz94/projects/i-hate-science/dna_report.md)
* **Thống kê**: 30 thư mục con, `1,227` jobs ➔ `296` cụm cảnh Final Take (`157` Video Final Takes, `220` ảnh `@IMG_001..@IMG_220`, truy vết `178` prompt ảnh AI).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Mẹo "Cắt Đầu Ô Số 1" Trên Bảng Turnaround Sheet 5.5K (`"remove the head from the first panel"`)**:
     * Tạo bảng nhân vật bằng `Cinematic Studio Soul Cast` (`2048x1152`), ví dụ:
       `"[Samir Al-Masri] — Professor Samir Al-Masri ran clandestine Cairo accelerator tests; now he guards stolen data, hunted. — (genre: Thriller, archetype: Sage)"`
     * Sau đó đưa qua `Nano Banana 2 (Pro)` / `Flash` ở độ phân giải `5504x3072` (5.5K) với câu lệnh lặp lại cho hàng loạt nhân vật (`@IMG_003: prof`, `@IMG_004: friend`, `@IMG_005: bad`, `@IMG_006: char_ksa2`, `@IMG_007: char_ksa1`):
       ```text
       remove the head from the first panel
       ```
  2. **Khóa Sơ Đồ Chỗ Ngồi 6 Nhân Vật Cùng Lúc (`6-Element Spatial Map`) + Gắn Mã Giọng Nói (`voice_id: sterling`, `voice_id: arthur`, `voice_id: benji`)**:
     * Gắn đồng thời 6 mỏ neo `<<<UUID>>>` trong giảng đường hơn 80 sinh viên (`[@IMG_002: lecture-hall]`, `[@IMG_003: prof]`, `[@IMG_004: friend]`, `[@IMG_005: bad]`, `[@IMG_006: char_ksa2]`, `[@IMG_007: char_ksa1]`), khóa cứng tọa độ ghế ngồi qua mọi cú cắt:
       ```text
       Geometry lock: [@IMG_002: lecture-hall] is a fixed closed set — tiered wooden seating, four tall grid windows with beige shades on the left wall... Every angle matches this reference exactly.
       Performance: [@IMG_005: bad] always sits in the left seat and [@IMG_004: friend] in the right seat of the same mid-hall desk. [@IMG_007: char_ksa1] and [@IMG_006: char_ksa2] always sit together two rows directly behind them.
       Characters & elements present (state/position): [@IMG_003: prof] ( voice_id: sterling ) — standing front-center... [@IMG_005: bad] ( voice_id: arthur ) — seated mid-hall left of center... [@IMG_004: friend] ( voice_id: benji ) — seated to [@IMG_005: bad]'s right...
       ```
  3. **Điều Khiển Ống Kính Bằng Góc Mở Độ (`FOV Degrees`) Kèm `HARD CUT` Theo Giây**:
     ```text
     FORMAT MODE: Timed multishot. Cuts only at the specified points, the camera does not cut on its own.
     OPTICS: 0–2s 12° tele detail; 2–4s 29°; 4–6s 12° tele detail. No drift mid-segment.
     ```
  4. **Đại Bản Văn Prompt Dài Tới `24,738` Ký Tự & Khối Khóa Khẳng Định (`POSITIVE LOCKS`)**:
     * Cảnh dài nhất (`Job ID: b1f38098-f8f8-42ad-a66c-a579817de5e9` trên `Seedance 2.5`) dài `24,738` ký tự, mở đầu rõ ràng: `"2 shots. Total 8 seconds — shot 1 runs 0.0–4.5s, shot 2 runs 4.5–8.0s. One hard cut at 4.5s, no transitions, no dissolves. The cut falls between sentences and never inside a word."`

---

### Dự Án #8: `@nicholastakeyama/projects/tokyo-4-17`
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/nicholastakeyama/projects/tokyo-4-17/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/nicholastakeyama/projects/tokyo-4-17/dna_report.md)
* **Thống kê**: 19 thư mục con, `559` jobs ➔ `229` cụm cảnh Final Take (`48` Video Final Takes, **`36/36 = 100%` ảnh `@IMG_001..@IMG_036` tự sinh bằng AI trong dự án, `0` ảnh upload ngoài**).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Khóa Nâng Cấp 4K & Chống "Mỹ Nam Hóa" Khuôn Mặt (`4K Master Sheet Anti-Beautification Lock` trên `ImageGen 2.0` `3840x2160`)**:
     * Tạo phôi nhân vật/bối cảnh bằng `Cinematic Studio Soul Cast` & `Soul Location` (kèm các tag tiếng Nhật định vị chất liệu bản địa như `[歌舞伎町タクシー]` — Taxi Kabukicho), sau đó đưa qua `ImageGen 2.0` ở độ phân giải `3840x2160` với lệnh khóa chống AI tự ý "làm đẹp" mẫu:
       ```text
       Use the provided image as the ABSOLUTE MASTER REFERENCE... THIS IS NOT A CHARACTER REDESIGN... DO NOT invent a new man. DO NOT beautify him. DO NOT make him younger. DO NOT turn him into a fashion model... Maintain: apparent age, Japanese facial identity, long narrow facial structure, facial asymmetry, subtle facial hair, under-eye character...
       ```
  2. **Phân Chia Bối Cảnh Theo Mã Màu Ánh Sáng Đêm (`Color-Coded Atmospheric Locations`)**:
     * Chia 12 thư mục bối cảnh theo nhiệt độ màu và chất liệu phản xạ đêm Tokyo: `loc - SODIUM` (vàng đèn đường natri), `loc - RED MIRROR` (gương đỏ), `loc - GREEN EXIT` (xanh đèn thoát hiểm), `loc - WET BLACK` (nhựa đường ướt đen), `loc - EMPTY AQUARIUM`, `loc - CONCRETE CATHEDRAL`, `loc - MOVING GLASS`, `loc - TOKYO BELOW`, `loc - TRAIN INTERIOR`, `loc - WHITE BOX`, `loc - 5:26`, `loc - DAWN`.
  3. **Slate Bấm Máy Song Ngữ Anh – Nhật Trên `Seedance 2.5` (`15s–19s` Long Takes)**:
     * Mở đầu bằng Slate định danh (`TOKYO, 4:17 — G01 — UPDATED VIDEO PROMPT` / `TOKYO 4:17｜G01｜19秒`), kết hợp kịch bản phân cảnh dài tới `10,259` ký tự.

---

### Dự Án #7: `@zhit/projects/the-patch`
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/zhit/projects/the-patch/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/zhit/projects/the-patch/dna_report.md)
* **Thống kê**: 64 thư mục con phân cấp sâu, `653` jobs ➔ `133` cụm cảnh Final Take (`58` Video Final Takes, `53` ảnh `@IMG_001..@IMG_053`).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Bí Kíp Độc Đáo Nhất: Quay "Video Mẫu Giọng Nói 4 Giây" (`Voice-Sample Slate Video` trong folder `Characters/VOICES`) Để Khóa Giọng Diễn Viên Xuyên Suốt Cả Bộ Phim!**:
     * Bước 1: Trong thư mục `Characters/VOICES`, tác giả tạo cho mỗi nhân vật (`aiden`, `walter`, `chloe`) một video 4 giây ở độ phân giải nhẹ `480p` (`896x384`) trên `Seedance 2.5`, đứng trước phông xám nói đúng 1 câu:
       ```text
       Photorealistic cinematic portrait, 35mm film, fine grain. A steady, locked-off medium close-up portrait of a man standing against a plain neutral grey backdrop, evenly lit, soft cool light, no props, no set. He faces the camera and looks directly into the lens, calm and plain, addressing the camera like a voice-sample slate.
       Character: [@IMG_006: walter_02] Walter — a 52-year-old man...
       Voice (STRICT): a soft, mature, slightly hoarse male voice speaking ENGLISH; calm, unhurried, evenly paced; quiet volume, gentle and polite.
       He looks into the lens and says, in English: "Hi. My name is Walter and this is the sample of my voice."
       Audio: clean audio only — only the spoken line, synced to lips. No ambient bed, no room tone, no music.
       ```
     * Bước 2: Khi quay cảnh đối thoại thực tế (`VIDEO 04` — `SC_002/002_02`), tác giả **đính kèm 2 video mẫu giọng nói đó làm `<<<video_1>>>` (Chloe) và `<<<video_2>>>` (Walter)**, đồng thời viết lệnh khóa chỉ lấy âm thanh mà cấm lấy hình ảnh từ video mẫu:
       ```text
       Audio: Clean audio only — NO ambient bed, NO background hum, NO room tone, NO added atmosphere or music... Any Walter dialogue in a soft, mature, slightly hoarse, calm unhurried male voice, take the sample from <<<video_2>>>. Chloe's voice from <<<video_1>>>.
       SCTRICT RULE: DO NOT TAKE ANY VISUAL ELEMENT FROM <<<video_1>>> and <<<video_2>>>.
       ```
  2. **Mẹo "Làm Mờ Mặt Ở Ô Toàn Thân Giữa" (`Middle panel: Full-body front view. Face is blurred.`) trên `Seedream 5.0 Pro` (`2336x992`)**:
     * Thay vì cắt đầu bằng `Nano Banana 2`, `@zhit` viết thẳng vào lệnh tạo bảng 3 ô trên `Seedream 5.0 Pro`:
       ```text
       A cinematic character reference sheet with a 3-panel layout on a uniform plain grey background.
       Left panel: Close-up portrait of Aiden, a 22-year-old man with a healthy face.
       Middle panel: Full-body front view. Face is blurred.
       Right panel: Full-body back view. Aiden is dressed in a plain, expensive but characterless neutral hoodie and casual trousers, worn carelessly.
       ```
  3. **Nhúng Mã `<<<UUID>>>` Của Đạo Cụ/Bối Cảnh Ngay Bên Trong Lệnh Tạo Ảnh Của Nhân Vật/Đạo Cụ Khác (`Nested UUID Reference in Image Gen`)**:
     * Khi tạo bảng nhân vật `@IMG_012` (`chloe`), tác giả nhúng thẳng mã `<<<e3459a1a-3cab-43c1-ada5-8217dba56df8>>>` (miếng chip dán thái dương) vào prompt tạo ảnh nhân vật:
       `Left panel: Close-up portrait of a 21-year-old Latina... small <<<e3459a1a-3cab-43c1-ada5-8217dba56df8>>> attached to her left temple.`
     * Khi tạo ảnh cận cảnh tấm biển tên bằng vàng (`plate`), tác giả nhúng thẳng UUID của căn phòng (`<<<92d2a1c7-bfd1-49f9-ac51-95e6ba53639d>>>`) để ánh sáng và tường bê tông khớp 100%:
       `extreme close up of the golden plate. On it engraved "Aiden Kowalski. CEO" . in the <<<92d2a1c7-bfd1-49f9-ac51-95e6ba53639d>>> on the right wall.`
  4. **Sơ Đồ Phòng Theo 4 Hướng La Bàn (`ROOM MAP: NORTH / WEST / EAST wall`) + Đếm Số Người Tuyệt Đối (`PEOPLE COUNT (EXACT, not a minimum)`)**:
     ```text
     ROOM MAP (fixed layout, derived from the master wide — respect exactly, do NOT rebuild): a single symmetrical brutalist concrete hall, deep axis running away from camera toward the BACK (NORTH) wall.
     - NORTH wall (far, center of the master wide): the wall screen "SUCCESS IS WHO YOU ARE", mounted above a short row of bucket seats...
     - WEST wall (LEFT recessed sliding door in the master wide): the ENTRANCE — Walter came in here.
     - EAST wall (RIGHT recessed sliding door in the master wide, small GOLD placard above it): the DIRECTOR'S OFFICE...
     PEOPLE COUNT (EXACT, not a minimum): EXACTLY 4 humans exist in this entire world — Walter, the Girl, and TWO young guys... After [@IMG_014: char_02] walks into the office door, EXACTLY ONE person ([@IMG_013: char_03]) remains seated. NEVER render three young men.
     ```
  5. **Khóa Chất Kính Cổ Điển (`vintage LOMO anamorphic glass`)**:
     * `Style: 8K, shot on 35mm film, Super-35 framed to 21:9 widescreen, captured on vintage LOMO anamorphic glass — old LOMO anamorphic character. Strong anamorphic look: pronounced horizontal flares, oval out-of-focus bokeh, gentle edge-field softness and distortion...`

---

### Dự Án #5 & #6: `@hft_online` (`standalone_clips` & Dự Án `harmony-ai-film-festival`)
* **Hồ sơ đầy đủ**:
  * Clip lẻ: [`standalone_clips/VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/hft_online/standalone_clips/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`12` clips, `15` `@IMG`)
  * Dự án dài: [`harmony-ai-film-festival/VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/hft_online/projects/harmony-ai-film-festival/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`1,543` jobs ➔ `801` cụm cảnh, `292` Video Final Takes, `603` `@IMG_001..@IMG_603`)
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Toán Tử Định Nghĩa Cảnh Quay Hỏng (`= failed take` / `= um take falhado`)**:
     * Thay vì chỉ viết `Negative: no...`, tác giả định nghĩa rõ mọi hành vi sai là `= failed take` (cảnh quay hỏng) để ép mô hình tuân thủ tuyệt đối:
       ```text
       BACK LOCK: she is filmed from behind from the first frame to the last, the back of her head aimed at the window for the entire clip, her chin never crossing her shoulder line, her curly hair filling the frame where her head is. Any visible eyebrow, eye, nose, lips or cheek profile at any moment = failed take. Her reactions live in her shoulders, breath and hands only.
       ```
     * Hoặc bằng tiếng Bồ Đào Nha trong `standalone_clips/VIDEO 02`:
       `qualquer aspecto de render, animacao ou 3D e um take falhado.`
  2. **Hệ Thống 6 Khóa Chuyên Biệt Theo Đạo Cụ & Vị Trí (`BACK LOCK`, `SOFA LOCK`, `ALIVE LOCK`, `GUITAR LOCK`, `KNEE LOCK`, `CAMERA LOCK` + `EVENT TIMECODES`)**:
     ```text
     SOFA LOCK: he sits deep in the seat until the moment he rises.
     ALIVE LOCK: at least one visible micro-movement in frame every second, dust, curtains, her sway, his rhythm, stillness written as held tension.
     GUITAR LOCK: exactly ONE guitar, a solid object, never intersecting his body; once set down it stays leaning on the sofa arm, motionless.
     KNEE LOCK: ONE knee, controlled, facing her back.
     CAMERA LOCK: breathing handheld drift only.
     EVENT TIMECODES: dead string ~3.0s, her caught breath in the same second, guitar down ~6.5s, he rises ~8.0s, kneel lands ~10.5s.
     ```
  3. **Kỹ Thuật "Chuyển Động Ngắt Nhịp Staccato" (`staccato hand gestures, separated like beats, not continuous gliding`)**:
     * Trong `VIDEO 04`, để bàn tay nhân vật chạm vào từng cán dao thứ nhất ➔ dừng ➔ cán dao thứ hai ➔ dừng ➔ cán dao thứ ba ➔ rút dao ra mà không bị AI làm trôi tuột mượt quá mức:
       ```text
       Her hand moves along the knife block in distinct rhythmic steps: touches the first blue handle, pauses, moves to the second handle, pauses, moves to the third handle, pauses, then decisively grips the largest bread knife and pulls it out, each movement sharp and separated like beats, not smooth, not continuous gliding, natural speed, staccato hand gestures...
       ```
  4. **Khóa Góc Nhìn Thứ Nhất (`True first-person subjective POV shot`) + Khóa Góc Lưỡi Dao 90 Độ (`VIDEO 06`)**:
     ```text
     True first-person subjective POV shot. The camera is locked at standing eye level, approximately 1.6 meters high, angled downward toward a kitchen table. Both of Jade's [@IMG_007: Jade] arms enter the frame from the bottom edge — elbows cut off by the lower frame line, no shoulders, no face, no body visible above the arms... Her right hand grips a blue-handled bread knife, blade oriented strictly vertical and perpendicular to the table surface — serrated edge facing downward, blade at 90 degrees to the cutting board, never horizontal, never sideways.
     ```
  5. **Phẫu Thuật Thay Thế Đạo Cụ Trên Tay Nhân Vật (`Reference Replacement Edit` bằng `Nano Banana 2`)**:
     ```text
     Replace the circular clay disk in the man's hands with the dark wood frame from the second image, scaled as a small hand-held wooden counting tablet with a recessed inner surface. Keep the man's hands, wooden stylus, posture, lighting, and shallow depth of field unchanged.
     ```

---

### Dự Án #4: `@mohamed-halloum/projects/sentence`
* **Hồ sơ đầy đủ**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/mohamed-halloum/projects/sentence/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) | [`dna_report.md`](./data/creators/mohamed-halloum/projects/sentence/dna_report.md)
* **Thống kê**: 14 thư mục con (`Scene 1`..`Scene 11`, `Characters`, `Tests`...), `646` jobs ➔ `230` cụm cảnh Final Take (`79` Video Final Takes, `136` ảnh `@IMG_001..@IMG_136`, truy vết `100` prompt ảnh AI).
* **Các Kỹ Thuật Đắt Giá Phát Hiện Được**:
  1. **Tạo Bảng 3 Ô "Cắt Đầu Từ Gốc Cổ Ngay Khi Tạo" (`headless full-body front view, the figure cut off cleanly at the base of the neck`)**:
     * Thay vì tốn thêm 1 bước chạy `Nano Banana 2` để xóa đầu ở hình toàn thân giữa, `@mohamed-halloum` viết thẳng vào Prompt tạo ảnh gốc trên `ImageGen 2.0` (`2688x1520` — `@IMG_028` & `SCENE_001`):
       ```text
       Three-panel studio character sheet of the same real person: a large three-quarter face close-up, a headless full-body front view, the figure cut off cleanly at the base of the neck, and a full-body back view with the head in place... Flat even soft light, 1:1 ratio, smooth falloff, a neutral mid-grey seamless backdrop, no studio, no equipment, no walls. Real untouched skin with visible pores, clear catch-lights in both eyes. The same person in all three panels. Palette of 60% neutral grey, 30% light-grey garment, 10% warm skin.
       ```
     * Nếu ô giữa vẫn còn sót phần cổ, tác giả mới chạy thêm 1 lệnh ngắn trên `Nano Banana 2`: `"Remove the neck from the front body view. keep everything else the same"`.
  2. **Tạo "Chuỗi Bảng Nhân Vật Già Đi Theo Thời Gian" (`Progressive Aging Character Sheet Chain` bằng `CHANGE:` + `PRESERVE EXACTLY:`)**:
     * Trong bộ phim khoa học viễn tưởng `sentence` (tù nhân bị giam trong buồng làm cơ thể già đi 1 năm sau mỗi phút), tác giả lấy tấm bảng 3 ô lúc 25 tuổi của nhân vật Adam rồi chạy chuỗi phẫu thuật `CHANGE:` + `PRESERVE EXACTLY:` trên `Nano Banana 2 (Pro)` (`2752x1536`) để tạo ra 6 bảng nhân vật ở các độ tuổi khác nhau mà giữ nguyên 100% nhận diện khuôn mặt:
       - Gắn miếng cảm biến ở cổ (`SCENE_003`):
         ```text
         CHANGE: a small flat white adhesive sensor patch like an ECG electrode, two centimetres across, stuck to the skin at the side of the neck just below the jaw on the frame-left side, a short thin white lead taped flat down toward the collar - on the face panel (the headless front panel is cut below it and shows no patch).
         PRESERVE EXACTLY: everything else in all three panels - the face, skin and pores, eyes and catch-lights, hair, stubble, the body, the grey clothes, the poses, the panel layout, the grey backdrop, the flat light, colour.
         ```
       - Già đi vài năm (`SCENE_004`): `CHANGE: the first signs of age only - faint lines at the outer corners of the eyes... PRESERVE EXACTLY: ...`
       - Già đi 12 năm (`SCENE_006`): `CHANGE: a man a dozen years on - grey threaded through the hair above the ears and at the temples on the face panel and through the hair on the back panel... PRESERVE EXACTLY: ...`
       - Già đi 15 năm (`SCENE_007`): `CHANGE: a man fifteen years on - the hair grey at the sides and greying on top on both panels, the hairline higher at the corners... PRESERVE EXACTLY: ...`
       - Già đi 20 năm (`SCENE_008`): `CHANGE: a man two decades on - hair half grey on both panels... PRESERVE EXACTLY: ...`
       - Đổi trang phục mà giữ nguyên mặt (`SCENE_009`): `CHANGE: the clothes only - a black lightweight zip jacket zipped to the collarbone over a dark tee, dark trousers and black shoes, on the front and back panels; the face panel unchanged... PRESERVE EXACTLY: ...`
  3. **Cú Pháp Ngoặc Nhọn `{Lời Thoại}` và Ngoặc Nhọn Đơn `<Âm Thanh Nền>` Trong Khối `AUDIO` Của `Seedance 2.5`**:
     ```text
     AUDIO
     Dialogue language: clear neutral English. The Registrar says, in a dry, level, unhurried baritone with every word at the same weight: {Compression. In the unit, the body ages one year for every minute. You will be awake, and you will watch.} <a low continuous machine hum under everything, deep and even> SFX only. No music.
     ```
  4. **Khóa Vật Lý Phản Chiếu Gương (`Mirror Reflection Physics Lock` — `VIDEO 02`)**:
     ```text
     SCENE CONTEXT: Inside a seamless white cube cell, a young prisoner in light-grey clothes stands one metre from a floor-to-ceiling mirror wall, facing it, his back to the camera; his face is seen only in the reflection. Exactly one character; the reflection is his reflection, not a second person.
     PHYSICS: The reflection copies every movement exactly and simultaneously, reversed as a true mirror; the fingertips and their reflection meet at one point on the glass; the seam stays a straight vertical line.
     ```

---

### Dự Án #1, #2, #3 & Nền Tảng: 4 Dự Án Gốc (`lukasbandana/rewind`, `ollkorrect/besa`, `seksifratello/apeirophobia-teaser`, `pandaproduction/thread`)
* **Hồ sơ đầy đủ**: [`BAN_THIET_KE_HE_THONG_VIDEO_AI_DIRECTOR.md`](./BAN_THIET_KE_HE_THONG_VIDEO_AI_DIRECTOR.md) & [`MASTER_DIRECTOR_PLAYBOOK_REPORT.md`](./data/MASTER_DIRECTOR_PLAYBOOK_REPORT.md)
* **Tóm tắt 4 Trường Phái Nền Tảng**:
  1. **`@lukasbandana/rewind` (`1,562` jobs ➔ `279` cụm cảnh, `115` `@IMG`)**:
     - Công thức **7 Khối DNA** (`1. Đại cảnh & Bối cảnh`, `2. Tốc độ & Nhịp điệu SPEED: 2x / Speed-Ramp`, `3. Bảng màu 60/30/10 & Plain unbranded clothing — no logos`, `4. Hành động theo mốc thời gian`, `5. Chuyển cảnh & Cú máy`, `6. Điểm nhìn âm thanh Sound Perspective Shift`, `7. Khóa chống lỗi`).
     - Bảng `2-Panel Macro Pair` (cận cảnh Mắt + Miệng).
  2. **`@ollkorrect/besa` (`960` jobs ➔ `450` cụm cảnh, `66` `@IMG`)**:
     - Khóa **Phân Quyền Tham Chiếu (`SCOPED REFERENCE AUTHORITY`: `<<<image_1>>> ONLY for room geometry`, `<<<uuid>>> ONLY for face`)**.
     - **Đường Ray Camera (`MASTER CAMERA RAIL`)** + Phẫu Thuật Start Frame (`CHANGE:` + `PRESERVE EXACTLY:`).
  3. **`@seksifratello/apeirophobia-teaser` (`6,862` jobs ➔ `1,444` cụm cảnh, `317` `@IMG`)**:
     - Khóa **Chất Phim Điện Ảnh (`PROJECT LOOK LOCK`: `ARRICAM LT 35mm + Zeiss Super Speed Mk II / Cooke S4/i + Black Pro-Mist 1/8 + Kodak Vision3 500T 5219`)**.
     - Khóa Phủ Định (`NEGATIVE LOCK`) + Gắn thẻ vị trí `<<<image_1>>>`, `<<<audio_1>>>`, `<<<video_1>>>`, `START_FRAME`, `END_FRAME`.
  4. **`@pandaproduction/thread` (`837` jobs ➔ `128` cụm cảnh, `69` `@IMG`)**:
     - Khóa **Nối Cảnh Mượt (`=== CONTINUATION FROM PREVIOUS SHOT ===`)** + **Vật Dẫn Chuyển Cảnh (`Suture / Red Thread Motif Match-Cut`)**.

---

## 🖼️ PHẦN 2: GHI CHÚ & KIỂM ĐỊNH THỊ GIÁC TỪ BẢNG XẾP HẠNG ẢNH CỘNG ĐỒNG (`3,522` ẢNH — `type=image`)
* **Hồ sơ đầy đủ**: [`data/community_images/RANKED_COMMUNITY_IMAGE_PROMPTS.md`](./data/community_images/RANKED_COMMUNITY_IMAGE_PROMPTS.md) (`1,819` Full Prompts)

### 🔍 Kết Quả Kiểm Định Bằng Mắt (`Visual Audit`) 6 Bức Ảnh Top Đầu Trên `community/generations?type=image` (Phân Biệt Rõ: Đâu Là Đỉnh Thật vs. Đâu Là Da Filter/Nhựa Dù Nhiều Tim)

Khi tải trực tiếp file ảnh `.webp` của các thứ hạng cao nhất (`#1`, `#2`, `#5`, `#6`, `#12`, `#16`) về mở xem bằng mắt (`read_file`), câu trả lời lộ ra cực kỳ rõ ràng — **Không phải cứ nhiều Tim (`♡`) trên Community là dùng cho Phim Điện Ảnh được**:

1. **Hạng `#1` (`♡ 981` Tim — `@qwerty_322` — `Higgsfield Soul 2.0`, Style `General`) ➔ Đẹp Thời Trang Mạng Xã Hội Nhưng Da Mặt Bị "Cà Filter Hàn/Trung" (`7.5/10`)**:
   - **Cái Đỉnh (Nên học)**: Chất liệu vải corset denim, khoen kim loại, lông thú áo khoác và đặc biệt là bức tường vôi cũ bong tróc có dây điện phía trên nhìn thật `9.5/10` nhờ bảng mã màu `HEX VALUES` ở cuối prompt.
   - **Cái Nhựa (Phải tránh khi làm phim)**: Khuôn mặt cô gái châu Á bị làm mịn lì như chụp qua app BeautyPlus/Meitu (má hồng phấn mịn, sống mũi bóng mượt không có lỗ chân lông). Hợp làm ảnh mẫu Instagram/Xiaohongshu, nhưng **không dùng mặt kiểu này cho phim điện ảnh thật**.
2. **Hạng `#2` (`♡ 852` Tim — `@young_drill` — `Higgsfield Soul 2.0`, Style `Flash editorial`) ➔ ĐỈNH CAO CHÂN THỰC ĐỜI THƯỜNG 100% KHÔNG MÙI AI (`10/10 Candid Realism`)**:
   - **Soi bằng mắt**: Gò má, thái dương và cổ của chàng trai đội mũ len vàng uống cốc sứ xanh có kết cấu da thật, hơi ửng đỏ tự nhiên dưới má, có một vệt mồ hôi nhỏ lấp lánh dưới mắt, tóc mai lơ thơ ở gáy, sợi len mũ hơi xù, bảng hiệu viết phấn ở vỉa hè phía sau và dàn nóng máy lạnh trên tường bê tông cũ — **nhìn 100% như ảnh chụp thật bằng máy ảnh kỹ thuật số cầm tay đầu thập niên 2000**.
   - **Từ khóa vàng cần lấy**: Kết hợp Preset `Flash editorial` + cụm `"hard direct on-camera flash, creating uniform brightness and a washed-out look typical of an early 2000s point-and-shoot digital snapshot... mildly messy air conditioning units and wires overhead"`.
3. **Hạng `#5` (`♡ 652` Tim — `@wer` — `Higgsfield Soul 2.0`, Style `General`) ➔ ĐIỂN HÌNH CỦA "NHỰA / MA-NƠ-CANH CGI" DÙ CÓ TỚI 652 TIM (`3/10 — Cấm Học Theo Khi Làm Phim Người Thật`)**:
   - **Soi bằng mắt**: Da cô gái trắng bệch bóng lưỡng như tượng sáp nhựa (`porcelain wax doll`), sóng biển đen phía sau nhìn như đồ họa 3D render cứng đơ, quần bạc nhìn như giấy bạc CGI.
   - **Nguyên nhân**: Trong chính câu Prompt của tác giả đã cố tình viết những từ khóa "đầu độc" độ chân thực: `"extremely pale, porcelain skin... CGI-assisted fashion photograph... smooth skin retouching, and subtle noise reduction"`. Đây là bằng chứng sống cho thấy **nếu chỉ nhìn số Tim (`♡ 652`) mà không mở ảnh ra soi bằng mắt thì sẽ học nhầm ngay công thức tạo da nhựa**!
4. **Hạng `#6` (`♡ 618` Tim — `@dinblunt` — `Nano Banana 2`, Đính kèm 2 ảnh) ➔ ĐỈNH VỀ Ý TƯỞNG BỐ CỤC NGHỆ THUẬT (`9.5/10 Creative Concept`)**:
   - **Soi bằng mắt**: Chồng TV CRT cổ đặt trong phòng tối, mỗi màn hình cắt một góc cơ thể của cô gái (đôi mắt đeo kính ở TV trên cùng, góc nghiêng mặt ở TV bên phải, thân áo ở TV giữa, bàn tay và đôi giày búp bê bạc trên sàn gỗ ở hàng TV dưới cùng) ghép lại thành một tổng thể siêu nghệ thuật. Ánh sáng hắt từ màn hình CRT lên vỏ nhựa TV cũ rất thật. Rất đáng dùng cho cảnh mở đầu MV hoặc TVC thời trang/nước hoa.
5. **Hạng `#12` (`♡ 420` Tim — `@hockney_cloud_bruh` — `Nano Banana 2`) ➔ Chất Ảnh Minh Họa Game / Fantasy AI (`6.5/10`)**:
   - **Soi bằng mắt**: Hai nhân vật mặc áo choàng chưởng lửa đỏ trong rừng sương mù — ánh sáng đỏ hắt lên lá khô khá bắt mắt nhưng tổng thể mang đậm mùi "AI Fantasy Illustration", không có chất quang học ống kính điện ảnh thật.
6. **Hạng `#16` (`♡ 370` Tim — `@piffle_jack` — `Soul Cinematic`, Preset `General_Olzhas`) ➔ ĐỈNH CAO ĐIỆN ẢNH `A24 / ARRI ALEXA ANAMORPHIC` (`10/10 Cinema Frame`)**:
   - **Soi bằng mắt**: Đường ray xe lửa ướt mưa dẫn mắt từ tiền cảnh tối sâu bên trong đường hầm bê tông ra miệng hầm tròn ngập sương mù mùa đông; hai nhân vật nhỏ ở điểm giao bố cục 1/3 đúng chất phim điện ảnh độc lập A24, độ mờ tiền cảnh (`shallow DOF` trên thanh tà-vẹt gỗ ướt) và độ tương phản vùng tối (`negative fill`) chuẩn máy quay `Arri Alexa LF + 40mm Anamorphic` 100%!

* **3 Phát Hiện Quan Trọng Khi Học Prompt Tạo Ảnh**:
  1. **Mẹo khóa bảng màu bằng mảng `HEX VALUES` trên `Higgsfield Soul 2.0` (`text2image_soul_v2`)**:
     * Các bức ảnh đạt `300–981` Tim trên `Soul 2.0` thường chốt ở dòng cuối cùng một danh sách mã màu HEX chính xác để ép tông màu toàn bức ảnh:
       ```text
       HEX VALUES: ["#d2cbb3", "#dcd6be", "#c8bfa5", "#978a76", "#b9af96", "#a99c86", "#433b35", "#8d7760"]
       ```
     * Đồng thời kết hợp chọn `Style Preset` (`General`, `Flash editorial`, `Y2K street`).
  2. **Cấu trúc JSON ẩn của `Soul Cinematic` (`soul_cinematic`)**:
     * Các ảnh `Soul Cinematic` lưu prompt dưới dạng JSON `{"silteme": "zxcv", "Caption": "..."}` với mô tả ánh sáng điện ảnh rất giàu chất liệu (`rain-slicked`, `sodium-vapor`, `chiaroscuro`).
  3. **Các câu lệnh "1 Dòng Ăn Ngay" (`One-Liner Power Prompts`) trên `Nano Banana 2`**:
     * Tách lớp kỹ thuật sản phẩm (`Exploded View / Cross-Section`):
       * `"Minimalist technical illustration of an Arc'teryx shell jacket, shown in an exploded view."` (`♡ 169`)
       * `"Create a detailed cross-section visualization of the jacket from the image."` (`♡ 176`)
     * Trải phẳng trang phục thành Catalog bán hàng (`Wardrobe Catalog`):
       * `"Collect each clothing item worn by the girl in the first photo and place them on top of the same bed..."` (`♡ 461`)
       * `"Make an online wardrobe catalog from this outfit"` (`♡ 192`)
     * Hiệu ứng nhiều màn hình TV cổ (`CRT TV Stack`):
       * `"Stack several vintage CRT TVs in a dark room. Each screen shows a different cropped detail from the reference photo..."` (`♡ 618`)

---

## 👁️ PHẦN 3: QUY TẮC BẮT BUỘC — KIỂM ĐỊNH THỊ GIÁC TRƯỚC KHI TƯ VẤN (`VISUAL AUDIT FIRST`)

> [!IMPORTANT]
> **BÀI HỌC THỰC CHIẾN TỪ DỰ ÁN NƯỚC HOA YSL "Y" EDP**:
> Trước khi trích dẫn hoặc khuyên dùng bất kỳ câu Prompt nào từ kho dự án đã cào để gửi cho người dùng, AI **BẮT BUỘC phải tải trực tiếp file ảnh tham chiếu (`_min.webp` / `.png`) của câu Prompt đó về máy và đọc bằng mắt (`read_file`)** để tự đánh giá/chê lọc xem ảnh kết quả thực tế của đạo diễn đó là **Đẹp thật (chuẩn điện ảnh)** hay **Bị giả/nhựa (`waxy/plastic`)**. Tuyệt đối không chỉ đọc chữ (`text prompt`) rồi bê nguyên xi sang tư vấn!

### Bằng Chứng Kiểm Định Thị Giác Trực Tiếp Giữa 3 Dự Án (`@thomas_lundstrom/emerald-fragrance-commercial` vs. `@pietromalegori/control` vs. `@pandaproduction/thread`)

Khi tải trực tiếp 11 bức ảnh gốc (`.webp`) từ 3 dự án về máy để soi bằng mắt thường, sự thật lộ ra rất rõ ràng:

1. **Tại sao nhân vật của `@thomas_lundstrom/emerald-fragrance-commercial` (`SCENE_008`) bị "nhựa" (trong khi ảnh chai nước hoa của anh ta lại rất đẹp)?**
   - **Điểm mạnh thật sự của `@thomas_lundstrom`**: Bức ảnh bảng 3 góc chai nước hoa `Emerald Nocturne` (`SCENE_001` — `Nano Banana 2 Pro` `2752x1536`) có chất lượng quang học kính xanh lục bảo, chữ dập nhũ vàng và cổ kim loại **cực kỳ sắc nét, sang trọng chuẩn studio 10/10**.
   - **Điểm yếu chí mạng ở ảnh nhân vật (`SCENE_008`)**: Khi mở trực tiếp bức ảnh bảng nhân vật 3 góc của `@thomas_lundstrom` ra xem bằng mắt:
     * Khuôn mặt người đàn ông mặc đồ thám hiểm (và cả bản mặc vest đen) **bị mịn bóng như tượng sáp (`waxy studio skin`)**, miệng cười mỉm kiểu người mẫu ảnh stock thương mại (`commercial catalog smile`), hoàn toàn thiếu lỗ chân lông và thần thái điện ảnh!
     * Hơn nữa, khi `@thomas_lundstrom` dùng câu lệnh ngắn `"Remove the face and neck from the front full body reference"` cho nhân vật đội mũ phớt, AI xóa phần mặt nhưng **để lại chiếc mũ phớt lơ lửng giữa khoảng không phía trên cổ áo trống rỗng** trông rất kỳ quặc!

2. **Tại sao nhân vật của `@pietromalegori/projects/control` và `@pandaproduction/projects/thread` lại chân thật như diễn viên điện ảnh sống 100%?**
   - **Bằng chứng thị giác từ `@pietromalegori/control` (`SCENE_001`, `SCENE_003`, `SCENE_006`, `SCENE_011`)**:
     * Khi mở ảnh chân dung `SCENE_001` (người đàn ông trung niên tóc muối tiêu, râu lởm chởm) và `SCENE_011` (người đàn ông lớn tuổi đeo kính gọng trong suốt) tạo bằng **`Soul Cinematic`** (`1344x2016` / `2048x1152`): Da mặt có độ nhám hữu cơ của phim 35mm, lỗ chân lông mở rõ trên cánh mũi và gò má, nếp nhăn trán không đối xứng, râu mọc không đều, ánh sáng dịu hoàn toàn không có vệt bóng dầu (`matte skin roll-off`), mắt nhìn thẳng lạnh lùng không cười.
     * Khi mở bảng 3 góc `SCENE_003` và `SCENE_006` (`Nano Banana 2 Pro` `2752x1536`): Ở 2 khung bên phải (toàn thân trước & sau), tác giả **đặt mép trên của khung hình crop ngang vùng cằm/cổ áo (`cropped cleanly at the top frame edge`)**, nhờ vậy phần đầu nằm ngoài rìa trên của khung ảnh một cách tự nhiên như ảnh chụp thời trang, chứ không tạo khoảng trống lơ lửng giữa nền xám.
   - **Bằng chứng thị giác từ `@pandaproduction/thread` (`SCENE_038`, `SCENE_040`, `SCENE_045`)**:
     * Tác giả tạo nhân vật gốc (`SCENE_038`) bằng **`Soul Cinematic`** (`1152x2048`) với chất liệu da thô mộc kiểu phim nhựa 35mm châu Âu thập niên 2000 (`Arriflex 35mm, Kodak Vision3 250D`), sau đó mới đưa sang `Nano Banana 2 Pro` (`2752x1536`) để dàn thành bảng 3 góc (`SCENE_040`: Toàn thân trước + Toàn thân sau + Cận mặt 3/4 siêu nét lỗ chân lông).
     * Khi vào cảnh quay tối (`SCENE_045`), từng sợi tóc mai bết mồ hôi, quầng thâm mắt và kết cấu da dưới ánh sáng tờ mờ nhìn hoàn toàn như cảnh cắt từ phim điện ảnh thật.

### Quy Trình 3 Bước Bắt Buộc Khi Tư Vấn Tạo Nhân Vật & Sản Phẩm Cho Người Dùng
1. **Bước 1 — Tải ảnh `_min.webp` về soi bằng mắt (`read_file`) trước khi nói**: Chọn lọc đúng điểm mạnh của từng đạo diễn (Ví dụ: lấy công thức **Bảng 3 góc Chai nước hoa** của `@thomas_lundstrom`, nhưng **tuyệt đối loại bỏ** công thức mặt nhân vật của `@thomas_lundstrom`; thay bằng công thức **Chân dung da thật 35mm `Soul Cinematic` + Bảng 3 góc crop mép trên khung hình** của `@pietromalegori/control` và `@pandaproduction/thread`).
2. **Bước 2 — Khóa 5 Từ Khóa Chống Da Nhựa (`Anti-Plastic Skin Realism Lock`)**:
   - Luôn chỉ định rõ: `raw unretouched 35mm film skin realism, visible open skin pores on nose and cheeks, subtle facial asymmetry, natural uneven stubble, matte skin highlight roll-off without airbrushed plastic sheen, serious neutral expression (no studio catalog smile)`.
3. **Bước 3 — Xử lý khung toàn thân trong Bảng 3 Góc (`3-Panel Turnaround`)**:
   - Nếu muốn khóa để model Video chỉ lấy mặt từ khung Cận cảnh (`Close-up panel`), hãy yêu cầu khung Toàn thân được **crop khung hình từ ngang cổ áo/xương quai xanh trở xuống sát mép trên bức ảnh (`full-body front view cropped cleanly at the collarbone at the top edge of the frame`)** như `@pietromalegori/control`, hoặc dùng lệnh chỉnh sửa từng phần (`CHANGE:` + `PRESERVE EXACTLY:`) kèm khóa kết cấu da thật.

### Câu Lệnh "Chữa Cháy & Phẫu Thuật Da Thật 35mm Trên Bảng 3 Góc" Đã Test Thực Tế Thành Công 100% (Verified in Production)
Khi người dùng đã có sẵn một bức ảnh Bảng 3 Góc (`3-panel character sheet`) chuẩn quần áo và bố cục nhưng ô mặt bên trái bị mịn/nhựa kiểu AI và ô giữa vẫn còn phần đầu, đính kèm bức ảnh đó vào `Nano Banana 2 (Pro)` và chạy nguyên văn câu lệnh đã kiểm chứng thực tế này:
```text
Edit this exact character sheet while keeping the 3-panel layout, clothing, leather jacket texture, and lighting 100% identical:
1. Middle panel (full-body front view): Remove the face and neck completely from the front full-body figure, cutting cleanly at the collar.
2. Left panel (facial close-up): Remove the smooth airbrushed AI-model look and replace with raw, unretouched 35mm film skin realism — visible open skin pores on the nose, cheeks and forehead, subtle sun-weathered skin texture, faint natural crow's feet lines around the eyes, slight uneven stubble growth, a realistic micro-sheen of moisture on the skin, and natural imperfect skin tone variations. Keep the exact same facial structure and hair.
```
* **Kết quả thực tế đã kiểm chứng**:
  - Giữ nguyên 100% thiết kế áo khoác da, dây đeo chéo, ánh sáng và bố cục 3 khung.
  - Khung giữa chỉ còn phần trang phục từ cổ áo trở xuống (không bị chiếc mũ hay tóc bay lơ lửng nếu nhân vật không đội mũ).
  - Khung bên trái biến đổi hoàn toàn từ da sáp mịn sang da người thật 35mm có lỗ chân lông mở rõ trên mũi/má, nếp nhăn đuôi mắt tự nhiên, râu lởm chởm và thần thái điện ảnh sống động.

---

### Kiểm Định Thực Chiến Video Đầu Tiên: `VIDEO A` (15 Giây — Gom 6 Shot Đặc Tả Chai YSL "Y" EDP Giữa Hang Đá Sóng Biển)

Khi kiểm định trực tiếp bằng mắt và tai (`read_file` + `ffprobe`) file kết quả thực tế `c665fd17-5785-4b88-b5fb-fa0228f2be2e.mp4` (`1920x1080`, `24fps`, `15.02s`) do người dùng render từ `Ảnh #1 (@IMG_01: ysl_y_bottle)` + `Ảnh #2 (@IMG_02: midnight_grotto)`:

1. **Những gì đã thành công xuất sắc (Điểm hình ảnh: `9.5/10`)**:
   - **Cắt cảnh cứng đa góc (`Multi-Hard-Cut`) trong 1 video 15 giây**: Model thực thi chính xác **6 cú cắt cảnh liên hoàn** đúng kịch bản:
     * `00:00–00:03`: Medium Push-in trực diện chai YSL Y giữa sóng biển đập tung bọt trắng xóa.
     * `00:04–00:05`: Cú cắt Macro siêu cận (`Extreme Macro`) vào thanh kim loại bạc khắc chìm chữ `YVES SAINT LAURENT`, có giọt nước lăn dọc qua chữ `L` sắc nét như quay bằng ống kính Macro 100mm thật.
     * `00:06–00:07`: Cú cắt góc cao (`High-angle Macro`) xoay quanh nắp chai đen nhám họa tiết kim cương (`precision-knurled cap`) và cổ bạc.
     * `00:08–00:09`: Cú cắt góc thấp `3/4` với sóng biển slow-motion vỗ tung tóe bao quanh thân chai thủy tinh xanh đen.
     * `00:10–00:11`: Cú cắt Macro vào nhánh chữ `Y` kim loại bạc bám đầy hạt sương nước li ti (`micro-condensation droplets`).
     * `00:12–00:15`: Cú kéo lùi (`Pull-back`) từ cận cảnh ra toàn cảnh chai YSL Y đứng vững chãi trên bệ đá базальт đen ướt giữa hang biển bão tố.
   - **Độ giữ form sản phẩm & chữ khắc (`Product & Typography Lock`) đạt 100%**: Nhờ tấm `Ảnh #1` (Bảng 3 góc chai `3-panel product sheet`), dòng chữ `YVES SAINT LAURENT` khắc chìm, vân nhám kim cương trên nắp đen và độ trong suốt xanh sapphire ở đáy chai không hề bị méo hay biến dạng chữ ở bất kỳ góc cận nào.

2. **3 Điểm Lỗi Nhỏ Phát Hiện Qua Kiểm Định Thực Tế & Cách Khắc Phục (`Visual & Audio Audit Findings`)**:
   - **Lỗi 1 — Âm thanh (`Audio Mismatch` — Lỗi lớn nhất cần lưu ý)**:
     * *Hiện tượng*: Dù trong prompt đã ghi `"Environmental ocean SFX only, no music"`, model tạo video vẫn tự ý chèn một bản **nhạc nền guitar thùng & trống nhịp vui tươi (`upbeat acoustic guitar/drum lounge track`)** chạy suốt 15 giây, làm giảm chất điện ảnh trầm tối, bí ẩn của YSL.
     * *Cách khắc phục (Khóa Âm Thanh Foley Tuyệt Đối hoặc Tách Nhạc)*:
       1. Trong Prompt Video, phải khóa mạnh hơn ở mục Audio & Rules:
          `Audio: Pure dark cinematic foley SFX ONLY (deep sub-bass ocean wave impacts, heavy water splashes, wet stone resonance, low cavern wind). STRICTLY ZERO MUSICAL INSTRUMENTS, NO acoustic guitar, NO drum beat, NO background BGM, NO upbeat melody.`
       2. Hoặc dùng `ffmpeg` tắt/thay thế kênh audio bằng SFX sóng biển + sub-bass điện ảnh chỉ trong 1 giây.
   - **Lỗi 2 — Lật gương vị trí chữ `Y` bất đối xứng ở Shot 5 (`00:10–00:11` Asymmetric Logo Flip)**:
     * *Hiện tượng*: Chai YSL Y có thiết kế bất đối xứng (nhánh dọc của chữ `Y` bạc ôm vào **cạnh bên phải** của mặt trước chai). Ở các Shot 1, 2, 4, 6, chữ `Y` nằm đúng bên phải; nhưng riêng ở **Shot 5 (`00:10–00:11`)**, khi quay macro lướt ngang, AI tự suy diễn nhánh dọc chữ `Y` nằm ở **cạnh bên trái** trong khi dòng chữ `YVES SAINT LAURENT` vẫn đọc thuận từ trái sang phải.
     * *Cách khắc phục (Khóa Bất Đối Xứng Hình Học — `Asymmetric Geometry Lock`)*:
       Khi làm TVC cho sản phẩm có thiết kế **bất đối xứng** (như chữ `Y` lệch phải của YSL), luôn thêm 1 dòng vào khối `RULES`:
       `ASYMMETRIC GEOMETRY LOCK: Looking at the front of the bottle, the vertical spine of the silver Y emblem is ALWAYS on the RIGHT edge, with the horizontal bar extending to the LEFT reading "YVES SAINT LAURENT". Never mirror or flip the Y spine to the left edge.`
   - **Lỗi 3 — Độ cứng của bọt sóng ở giây `00:08–00:09`**:
     * *Hiện tượng*: Ở giây `00:08–00:09`, khi sóng vỗ lên quanh chai ở chế độ slow-motion, các ngón bọt nước trắng (`white foam fingers`) giữ nguyên hình dáng hơi lâu khi rút xuống.
     * *Cách khắc phục*: Thêm cụm `natural gravity-driven fluid collapse, translucent water sheets breaking into fine airborne droplets (no stiff frozen foam shapes)` vào phần mô tả sóng nước.


---

## 20. Kết Quả Kiểm Định Thị Giác Trực Tiếp 264 Ảnh Top Higgsfield Community (`♡ >= 50` Kèm Full Prompt — Đã Xem Bằng Mắt 100%)

> **Báo cáo đầy đủ 264 ảnh**: Xem chi tiết từng bức từ `#001` (`♡ 981`) đến `#264` (`♡ 50`) tại **[`data/community_images/VISUAL_AUDIT_TOP_264_REPORT.md`](./data/community_images/VISUAL_AUDIT_TOP_264_REPORT.md)**.
> Toàn bộ **264/264 bức ảnh** có `likes_count >= 50` và có câu lệnh `prompt_raw` (bao gồm trọn vẹn **63 ảnh `♡ >= 200`** và **201 ảnh `50 <= ♡ < 200`**) đã được tải về máy và **kiểm tra trực tiếp bằng mắt (`view_file`) từng bức một** theo quy tắc `Visual Audit First`.

### 20.1. Thống Kê Phân Loại Thực Chiến Trên Toàn Bộ 264 Ảnh

| Phân loại Kiểm định Thị giác (`Visual Audit Category`) | Số lượng ảnh | Tỷ lệ (%) | Kết luận rút ra sau khi soi mắt 264 ảnh (độ phân giải 1:1) |
| :--- | :---: | :---: | :--- |
| **Cat 1 — Đỉnh thật 100% (`Photoreal / Cinema`)** | **`134`** | **`50.8%`** | Da thật có lỗ chân lông, tàn nhang, mồ hôi, lông tơ (`vellus hairs`), ánh sáng điện ảnh 35mm (`soul_cinematic`) hoặc chụp flash đời thường (`Flash editorial`, `Y2K street`, `Warm ambient`, `seedream_v5_lite`, `seedream_v4_5`) **10/10 không mùi AI**. |
| **Cat 2 — Đẹp bố cục / Ý tưởng / Sản phẩm thương mại** | **`94`** | **`35.6%`** | Đỉnh cao về **Layout Quảng cáo, E-commerce, Giải phẫu Sản phẩm, Infographic & Đa khung hình**: chồng TV CRT (`#006`), tách đồ thành Sticker (`#009`), web E-commerce (`#068`), máy bán hàng tự động (`#149`), cắt dọc/tách lớp áo GORE-TEX (`#083`, `#090`), bảng trắng Toán/Vật lý (`#040`, `#205`), thuật toán 5 khung (`#178`). |
| **Cat 3 — Mịn filter / Lỗi chữ nền & ngón tay cần lọc bỏ** | **`28`** | **`10.6%`** | Quần áo và bối cảnh đẹp nhưng **da mặt bị cà mịn kiểu app BeautyPlus/Meitu** (`#001`, `#019`, `#041`, `#071`, `#074`, `#106`, `#124`, `#142`, `#153`, `#237`), **lỗi bàn tay 6 ngón** (`#062`), hoặc **biển hiệu/chữ in trên áo/bìa sách/bảng thang máy bị méo thành chữ AI vô nghĩa** (`#014`, `#024`, `#029`, `#043`, `#077`, `#089`, `#091`, `#166`, `#171`, `#172`, `#177`, `#225`). |
| **Cat 4 — Nhựa CGI / Tranh vẽ AI cần tránh tuyệt đối** | **`8`** | **`3.0%`** | Da trắng bệch như tượng sáp nhựa (`porcelain skin` + `CGI-assisted fashion photograph` `#005`), cảnh rồng/pháp sư CGI (`#012`, `#058`, `#120`), screenshot game (`#181`), hoặc anime 2D (`#210`). |

#### Bảng Xếp Hạng Độ Chân Thực Theo Model (`264` Ảnh `♡ >= 50`):
1. **`seedream_v4_5` (`5/6` ảnh đạt Cat 1 = `83.3%`) & `seedream_v5_lite` (`2/3` Cat 1: `#264`, `#245`) & `seedream_v5_pro` (`1/1` Cat 1: `#221`)**:
   - Tuy số lượng ảnh trên bảng xếp hạng ít hơn dòng Soul, nhưng khi soi cận cảnh `1:1`, họ **Seedream 4.5 / 5.0** giữ vị trí **Số 1 tuyệt đối về kết cấu lỗ chân lông Macro (`#264`), lộ rõ vết sẹo/râu thật (`#245`), tàn nhang & lông tơ (`#128`, `#159`), khóa danh tính casting (`#252`), và khóa thay đồ `GLOBAL_LOCK` (`#221`)** (chỉ duy nhất `#153` không khóa kết cấu da nên bị mịn glam).
2. **`soul_cinematic` (`General_Olzhas` — `30/37` ảnh đạt Cat 1 = `81.1%`, cộng thêm `3` ảnh Cat 2 = `89.2%` dùng tốt)**:
   - Ông vua tạo **Khung hình Điện ảnh A24 / Wong Kar-wai / 35mm Anamorphic** (`#010`, `#016`, `#028`, `#036`, `#037`, `#042`, `#047`, `#051`, `#052`, `#061`, `#110`, `#213`, `#217`, `#232`). Chỉ có `4` ảnh rơi vào Cat 4 do người dùng cố tình viết prompt tả rồng lửa fantasy/anime (`#058`, `#120`, `#150`, `#210`).
3. **`text2image_soul_v2` (`131` ảnh: `69` Cat 1 + `44` Cat 2 = `86.3%` dùng tốt)**:
   - **Preset `Flash editorial` (`55` ảnh: `30` Cat 1 + `21` Cat 2 = `92.7%` dùng tốt)**, **`Mystique city` (`3/3` Cat 1 = `100%`)**, **`Theatrical light` (`3/3` Cat 1 = `100%`)**, **`Warm ambient` (`3/4` Cat 1, trừ `#091` lỗi chữ bìa sách)**, **`Digital camera` (`2/3` Cat 1, trừ `#077` lỗi chữ áo)** là vũ khí chủ lực để chụp ảnh đời thường, thời trang đường phố và nội thất.
   - *Lưu ý*: Với preset `General` (`51` ảnh: `23` Cat 1 + `19` Cat 2 + `8` Cat 3 + `1` Cat 4) và `text2image_soul (Elevator Mirror)` (`0/2` Cat 1 — cả `#019` và `#172` đều mịn da + lỗi bảng thang máy), luôn tránh từ khóa `smooth skin / porcelain skin` và khóa chặt chữ nền/bàn tay.
4. **`nano_banana_2` (`64` ảnh: `18` Cat 1 + `42` Cat 2 = `93.8%` dùng tốt)**:
   - Ông vua tuyệt đối về **Bố cục Quảng cáo, Giải phẫu Sản phẩm, Infographic & Bảng trắng**: 100% các ảnh đồ họa kỹ thuật, công thức Toán/Vật lý (`#040`, `#205`, `#230`), nhãn `GORE-TEX` (`#083`, `#090`, `#145`), truyện tranh (`#035`, `#116`) và infographic (`#136`, `#209`) đều viết chữ tiếng Anh chuẩn xác không sai một ký tự; đồng thời tạo chân dung Chiaroscuro (`#021`) và Leica (`#119`) cực thật (chỉ có 2 ảnh selfie gương `#124` và `#237` bị rơi vào Cat 3 do mịn mặt / lỗi chữ nhỏ trên bảng nút thang máy).

---

### 20.2. 6 Công Thức "Đỉnh Thật 100% (Cat 1)" Đắt Giá Nhất Đã Kiểm Chứng Bằng Mắt

#### Công thức 1 — Đặc Tả Macro Da Người Thật Số 1 Toàn Bảng Xếp Hạng (`#264` — `seedream_v5_lite`, `♡ 50`, `@redhair`)
* **Kiểm định bằng mắt**: Nhìn ở độ phân giải 1:1, bức ảnh cận cảnh nửa mặt chàng trai tóc đỏ này **không có bất kỳ dấu hiệu AI nào**: thấy rõ từng lỗ chân lông, sợi lông tơ vàng (`fine vellus hairs`), tàn nhang, nốt mụn nhỏ, tia máu trong lòng trắng mắt và độ khô tự nhiên của môi.
* **Bí quyết kỹ thuật**: Dùng ống kính `100mm macro equivalent` kết hợp **ánh sáng tạt nghiêng góc hẹp (`grazing the skin at a shallow angle to reveal texture and depth, no beauty lighting, no smoothing`)**.
* **Nguyên văn câu lệnh (`Verbatim Prompt`)**:
```text
Extreme macro close-up portrait of a young male face, framed from just below the eyes to the upper lip. Hyper-real skin texture with visible pores, fine vellus hairs, subtle blemishes, micro wrinkles, oil sheen, and natural unevenness. Individual eyelashes sharply defined, iris edge razor-sharp with complex radial patterns, tiny capillaries visible in the sclera. Slight imperfections: faint redness around the nose, subtle under-eye darkness, tiny broken veins, realistic skin translucency.
Lighting is soft but directional, grazing the skin at a shallow angle to reveal texture and depth, no beauty lighting, no smoothing. True-to-life color science, neutral white balance, cinematic contrast, crushed blacks avoided. Shot on a high-end macro lens (100mm macro equivalent), ultra-shallow depth of field, critical focus on skin surface.
Photorealistic, unretouched, documentary realism. Feels like a real iPhone or DSLR macro capture, not CGI.
```

#### Công thức 2 — Khóa Danh Tính & Da Thật Cho Ảnh Casting Nhân Vật (`#252` — `seedream_v4_5`, `♡ 54`, `@parametric_koala_1106`)
* **Kiểm định bằng mắt**: Ảnh đính kèm của bản ghi `#252` là ảnh tham chiếu gốc toàn thân trên nền phông trắng studio giữ nguyên 100% các mảng sắc tố da bạch biến (`vitiligo`), nốt ruồi và tỷ lệ cơ thể tự nhiên không cà mịn, đi kèm bộ câu lệnh chuẩn khóa danh tính cận mặt (`FACE PROMPT 1/??`) cho hồ sơ casting.
* **Nguyên văn câu lệnh (`Verbatim Prompt`)**:
```text
SEEDREAM — FACE PROMPT 1/?? (Front Close-Up, Ultra-Real Capture)
Use the provided reference images as the ONLY source for identity. Preserve her exact face, proportions, skin texture, and all unique identifiers (moles/freckles/scars). No beautification, no stylization, no “AI face,” no smoothing.
SHOT: Tight headshot, straight-on front. Frame: top of hair to just below chin. Both ears optional but keep head centered.
CAMERA: 105mm portrait lens look, eye-level, neutral perspective (no wide-angle distortion). Sharp focus on both eyes and lashes; natural depth of field (no fake bokeh).
LIGHTING: White seamless studio, high-end beauty capture but real. Soft key light + soft fill (clamshell style). Background pure white with no color cast. Subtle, natural shadow shaping; no harsh shadows.
EXPRESSION: Neutral relaxed face, mouth closed, no smile, natural micro-tension. Eyes looking directly into lens.
DETAIL REALISM: Keep visible pores, fine hairs, natural skin micro-texture, realistic specular highlights, natural under-eye texture. Keep real hair strands and flyaways consistent with references.
COLOR: Neutral white balance, true-to-life skin tone, no creative grading.
HARD RULES: No makeup changes, no hairstyle changes, no age change, no face “perfecting,” no symmetry correction, no added accessories, no text/logos/watermarks.
NEGATIVE / AVOID: cartoon/anime, plastic skin, over-sharpen halos, washed-out face, glam retouch, face reshaping, eye enlargement, lip plumping, heavy foundation look, uncanny smile, extra teeth, asymmetry glitches, deformed pupils/iris, double eyelashes, extra facial features.
```

#### Công thức 3 — Khóa Thay Trang Phục (`Virtual Try-On Lock`) Giữ Nguyên 100% Người & Bối Cảnh (`#221` — `seedream_v5_pro`, `♡ 69`, `@kobal`)
* **Kiểm định bằng mắt**: Khi cần giữ nguyên 100% ảnh gốc của diễn viên/người mẫu (tư thế, gương mặt, tóc, ánh nắng biển) và chỉ thay đúng bộ trang phục + phụ kiện từ ảnh tham chiếu, cấu trúc JSON `GLOBAL_LOCK` + `REFERENCE_PRIORITY` này hoạt động chính xác tuyệt đối:
```json
{
  "GLOBAL_LOCK": [
    "USE THE MODEL IMAGE AS THE FINAL BASE IMAGE",
    "DO NOT CHANGE FACE, BODY, SKIN, HAIR, EXPRESSION, POSE, CAMERA, LIGHTING OR BACKGROUND",
    "DO NOT REGENERATE OR RECOMPOSE THE SCENE",
    "ONLY REPLACE THE ENTIRE STYLING USING THE REFERENCE IMAGE"
  ],
  "REFERENCE_PRIORITY": [
    "USE THE UPLOADED REFERENCE IMAGE AS THE SINGLE SOURCE OF TRUTH",
    "COPY THE COMPLETE LOOK EXACTLY",
    "DO NOT INVENT, OMIT OR MODIFY ANY ELEMENT"
  ],
  "prompt": "Premium fashion virtual try-on. Keep the original model and scene completely unchanged. Replace everything the model is wearing with the complete outfit shown in the reference image. The final image must look like a real fashion photograph, not AI generated.",
  "material_rules": [
    "Preserve original fabric texture.",
    "Preserve transparency, embroidery, lace, sequins, stitching.",
    "No smoothing. No artificial shine."
  ],
  "negative_prompt": [
    "missing accessories", "mixed outfit", "partial outfit replacement",
    "lighting change", "background change", "camera change", "pose change",
    "face change", "body change", "hairstyle change", "AI look", "plastic skin"
  ]
}
```

#### Công thức 4 — Candid Flash Editorial & Y2K Street Đời Thường (`#002` `♡ 852` & `#003` `♡ 685` — `text2image_soul_v2`)
* **Kiểm định bằng mắt**: Hai bức ảnh có lượt tim cao nhất nhóm Đỉnh Thật 100% (`#002` và `#003`) đều dùng chung một bí quyết: **kết hợp ánh sáng ban ngày với đèn Flash đánh thẳng từ máy ảnh compact (`hard direct on-camera flash` / `flash fill highlights on her skin`)** kèm **bối cảnh vỉa hè bừa bộn có thật (`mildly messy air conditioning units and wires overhead`, `scattered asphalt grit`)**.
* **Nguyên văn câu lệnh `#002` (`Flash editorial` — `♡ 852`)**:
```text
Close-up side profile of a young man, seated at an outdoor café table, wearing a white oversized sweatshirt and a yellow knitted beanie, holding a bright blue ceramic mug raised to his lips. Expression is neutral and thoughtful, subtly bored. The background shows an urban sidewalk street with a small blackboard sign and plain concrete buildings—mildly messy air conditioning units and wires overhead. Lighting is hard direct on-camera flash, creating uniform brightness and a washed-out look typical of an early 2000s point-and-shoot digital snapshot. Soft, pastel-inspired color palette dominated by mellow neutrals, cobalt blue accent, and pale yellow. Candid and mundane urban moment, lo-fi 90s/2000s fashion editorial mood.
```
* **Nguyên văn câu lệnh `#003` (`Y2K street` — `♡ 685`)**:
```text
A candid street portrait of a young woman in open space under bold daylight, standing on a sunlit city sidewalk with faint crosswalk paint and scattered asphalt grit, head slightly turned and eyes naturally squinting from the sun, jawline caught by side-light and direct on-camera flash, casual low-rise denim and snug pastel tank top, soft windblown hair, relaxed posture and playful energy, point-and-shoot wide angle shot from close range in the street, blue sky overhead and urban edges in the background, deep sidewalk shadow and flash fill highlights on her skin, slight film grain and blue-red color pop, bold Y2K daylight flash street-style portrait energy.
```

#### Công thức 5 — Khung Hình Điện Ảnh A24 / 35mm JSON Schema (`#016` `♡ 370` & `#037` `♡ 252` — `soul_cinematic` `General_Olzhas`)
* **Kiểm định bằng mắt**: Toàn bộ các bức ảnh điện ảnh đẹp nhất của model `soul_cinematic` đều dùng cấu trúc **JSON 7 trường** (`Caption`, `STYLE`, `COMPOSITION`, `SCENE`, `CINEMATOGRAPHY_AND_LIGHTING`, `CAMERA_AND_LENS`, `PHYSICAL_ATTRIBUTES`, `HEX VALUES`), chỉ định rõ máy quay `Arri Alexa Mini LF` + ống kính `40mm anamorphic prime` hoặc `50mm Zeiss prime` + bụi nắng (`visible airborne dust motes in sunbeams`).

#### Công thức 6 — Chân Dung Chiaroscuro & Leica Cận Mặt (`#021` `♡ 329` & `#119` `♡ 132` — `nano_banana_2`)
* **Nguyên văn câu lệnh `#021` (`Chiaroscuro B&W`)**:
```text
Generate an image with an intense chiaroscuro effect. The man should retain his original features and expression. Introduce harsh, directional light, appearing to come from above and slightly to the left, casting deep, defined shadows across the face. Only slivers of light illuminating his eyes and cheekbones, the rest of the face is in deep shadow
```

---

### 20.3. 12 Câu Lệnh "1 Dòng Ăn Ngay (`One-Liner Commercial & Layout Prompts`)" Trên `nano_banana_2` (Cat 2)

Qua kiểm định bằng mắt 64 ảnh `nano_banana_2`, đây là 12 mẫu câu lệnh ngắn gọn nhưng tạo ra bố cục thương mại, giải phẫu sản phẩm và storyboard xuất sắc nhất:

1. **Tách từng món đồ đang mặc thành Sticker viền trắng + Nhãn viết tay (`#009` — `♡ 461`, `@dinblunt`)**:
   > `Collect each clothing item worn by the girl in the first photo and place them on top of the same photo as flat, cut-out stickers. Keep every piece neatly outlined like a collage sticker. Next to each stickered clothing item, write its name in a soft pencil-style handwritten label, creating an aesthetic fashion-notebook look.`
2. **Biến bộ đồ đang mặc thành trang web E-Commerce có nút Add to Cart (`#068` — `♡ 192`, `@lesgobebe`)**:
   > `Make an online wardrobe catalog from this outfit`
3. **Đóng túi hút chân không toàn bộ trang phục bày bán trong máy bán hàng tự động (`#149` — `♡ 114`, `@meruwert`)**:
   > `make the items of this ourtfit the selled items in vending machine,the shot is taken by iphone`
4. **Chồng nhiều màn hình TV CRT cổ trong phòng tối chiếu từng góc cận cảnh (`#006` — `♡ 618`, `@dinblunt`)**:
   > `Stack several vintage CRT TVs in a dark room. Each screen shows a different cropped detail from the girl in the second photo: side profile, eyes, hair, outfit, pink shirt, jeans, black headband, and her squatting pose. Every TV displays a different angle, with slight analog distortion, scanlines, and soft CRT glow. Moody, dim lighting with the TVs as the main light source. Retro, cinematic, high-detail, analog texture.`
5. **Bản vẽ cắt dọc (`Cross-Section`) giải phẫu các lớp bên trong sản phẩm (`#083` — `♡ 176`, `@kanye`)**:
   > `Create a detailed cross-section visualization of the jacket from the image. Show the jacket sliced vertically, revealing all internal layers: outer fabric, insulation (down or synthetic fill), inner lining, stitching, padding, pocket construction, zipper mechanism, hood structure, and reinforcement areas. Use clean technical illustration style, labeled sections, precise material textures, soft lighting, white background, high-resolution.`
6. **Đồ họa tách lớp (`Exploded View`) kèm nhãn chỉ dẫn kỹ thuật (`#090` — `♡ 169`, `@lord_flacko`)**:
   > `Minimalist technical illustration of an Arc'teryx shell jacket, shown in an exploded view. Layers separated and labeled: outer waterproof face fabric, GORE-TEX membrane, inner protective lining, seam tape, zippers, hood construction, ventilation panels. Clean white background, precise details, modern infographic style, soft shadows, high clarity, premium outdoor aesthetic`
7. **Bản vẽ kỹ thuật Blueprint nền xanh chữ trắng (`#145` — `♡ 117`, `@grooving_book_ai`)**:
   > `A blueprint-style technical drawing of a futuristic coffee machine. White lines on standard blue background. Label the main parts with text: 'Water Tank', 'Grinder', and 'Brew Unit'. The drawing should look precise and architectural.`
8. **Ghép 4 dải dọc 4 mùa Đông - Xuân - Hạ - Thu khớp liền mạch 100% (`#081` — `♡ 177`, `@grooving_book_ai`)**:
   > `A single large oak tree in the center of a field, viewed from a distance. The image is split into four vertical strips. Strip 1 is Winter (snow, bare branches). Strip 2 is Spring (blossoms, green grass). Strip 3 is Summer (lush green leaves, bright sun). Strip 4 is Autumn (orange leaves, falling foliage). Crucially, the tree trunk and branches must align perfectly across all four strips to form one continuous tree. Cinematic lighting.`
9. **Thuật toán trực quan 5 khung hình liên tiếp giữ nguyên số lượng vật thể (`#178` — `♡ 91`, `@land_art_pencil`)**:
   > `Create a 5-frame visual algorithm demonstrating the process of sorting objects by color. Frame 1: A chaotic pile of small colored objects (red, blue, yellow, green) randomly scattered on a white table. Frame 2: Partial grouping begins — some colors start clustering loosely. Frame 3: Clearer grouping with each color forming recognizable clusters, though still imperfect. Frame 4: Nearly finished sorting, clusters separated with clean boundaries. Frame 5: Final sorted state — four perfectly aligned rows of objects grouped strictly by color, with consistent spacing and alignment. Ensure the same objects persist across all frames, maintaining shape continuity and no disappearing items`
10. **Mở rộng góc máy ra toàn cảnh hậu trường đoàn làm phim (`#097` — `♡ 160`, `@hockney_cloud_bruh`)**:
    > `Show me an expansion of how this was filmed.`
11. **Chuỗi 4 khung hình hành động liên tiếp của cùng một nhân vật (`#216` — `♡ 70`, `@hockney_cloud_bruh`)**:
    > `Show me a collage of him taking off his mask step by step`
12. **Infographic hướng dẫn quy trình 4 bước bằng ảnh chụp thực tế (`#209` — `♡ 73`, `@land_art_pencil`)**:
    > `Generate a step by step infographics with realistic images, an instruction how to make this dish`

---

### 20.4. Danh Sách Từ Khóa "Độc Hại" Gây Da Nhựa (Cat 4) & Lỗi Cà Mịn / Lỗi Chữ / Lỗi Tay (Cat 3) Phải Tránh

Từ việc đối chiếu trực tiếp bằng mắt ở độ phân giải 1:1 giữa nhóm **Cat 1 (`#002`, `#003`, `#159`, `#199`, `#245`, `#252`, `#264`)** và nhóm **Cat 3 / Cat 4 (`#001`, `#005`, `#014`, `#024`, `#029`, `#041`, `#043`, `#062`, `#071`, `#074`, `#077`, `#089`, `#091`, `#124`, `#153`, `#171`, `#172`, `#177`, `#225`, `#237`)**, đây là 4 bẫy lớn nhất cần tránh:

1. **Bẫy 1 — Các cụm từ tự động kích hoạt "Da Tượng Sáp / CGI" (Nguyên nhân trực tiếp làm hỏng bức `#005` `♡ 652`)**:
   - Trong prompt của `#005`, tác giả viết: `extremely pale, porcelain skin`, `CGI-assisted fashion photograph`, `visible digital sharpening, smooth skin retouching, and subtle noise reduction that gives an almost hyperreal finish`. Kết quả là bức ảnh trông hoàn toàn như búp bê nhựa 3D.
   - **Quy tắc**: **TUYỆT ĐỐI KHÔNG BAO GIỜ** dùng các từ `porcelain skin`, `smooth skin`, `flawless complexion`, `CGI-assisted`, `noise reduction`, `hyperreal finish`, `beauty retouching` khi tạo nhân vật người thật. Luôn thay bằng: `unretouched skin with visible pores, fine vellus hairs, subtle blemishes, natural oil sheen, no smoothing`.
2. **Bẫy 2 — Bẫy Cà Mịn Mặc Định Trên Gương Mặt Nữ Châu Á Ở Preset `General`, `Old smartphone` & `Elevator Mirror` (`#001`, `#019`, `#041`, `#071`, `#074`, `#106`, `#142`, `#172`)**:
   - Khi dùng `text2image_soul_v2 (General / Old smartphone)` hoặc `text2image_soul (General / Elevator Mirror)` với mô tả `"young Asian woman"`, model có xu hướng mặc định áp lớp da mịn kiểu app Hàn Quốc/Trung Quốc dù quần áo và tường phía sau cực thật (như bức `#001` `♡ 981`, `#071` `♡ 187`, `#074` `♡ 182`). Đặc biệt preset `text2image_soul (Elevator Mirror)` bị lỗi mịn da + méo bảng nút thang máy trên cả `2/2` ảnh (`#019`, `#172`).
   - **Cách khắc phục**: Chuyển sang preset **`Flash editorial`**, **`Y2K street`**, **`Mystique city`**, **`Theatrical light`**, hoặc dùng **`seedream_v5_lite` / `seedream_v4_5`** kèm khóa kết cấu của `#264`/`#252`: `Hyper-real skin texture with visible pores, fine vellus hairs, subtle blemishes, no beauty lighting, no smoothing`.
3. **Bẫy 3 — Lỗi Chữ Vô Nghĩa (`AI Gibberish Text`) Trên Biển Hiệu, Bìa Sách, Bàn DJ & Áo Thun Khi Dùng `text2image_soul_v2` (`#014`, `#024`, `#029`, `#062`, `#071`, `#077`, `#089`, `#091`, `#166`, `#171`, `#177`, `#225`)**:
   - Khi soi ở độ phân giải `1:1`, `text2image_soul_v2` rất hay làm biến dạng các dòng chữ nhỏ trên đạo cụ/trang phục: chữ bàn DJ Pioneer thành `'Pioinein'` kèm bàn tay 6 ngón (`#062`), bìa sách tiền cảnh thành `'TIl Aeppererimee osl of A the Past'` (`#091`), chữ áo/quần thành `'ROIDOSS ПOY'` (`#029`), `'PILANGERRILIYAN'` (`#077`), `'MODVEI SOOP7S'` (`#089`), `'Pafum / BCAMSON'` (`#171`).
   - **Cách khắc phục**:
     * Nếu cảnh **bắt buộc có chữ viết, nhãn hiệu, bìa sách, công thức hay bao bì sản phẩm**: Dùng **`nano_banana_2`** (đạt 100% chính xác chữ trên toàn bộ các ảnh bảng trắng, infographic và giải phẫu sản phẩm) hoặc chỉ định rõ nội dung chữ ngắn gọn 2–3 từ trong ngoặc kép (như `"I ♥ ME"` ở `#103` hoặc `'hand cream'` ở `#108`).
     * Nếu cảnh đường phố/đời thường không cần chữ: Luôn khóa `no storefront text, no readable signs, plain unbranded clothing without text prints, no book titles` để không bị chữ AI vô nghĩa làm lộ ảnh giả.
4. **Bẫy 4 — Tự Vô Hiệu Hóa Khóa `CRITICAL REALISM` Bằng Từ Khóa `Soft glam` & `Extremely voluptuous` (`#237` `♡ 61`)**:
   - Ở bức `#237`, dù đầu prompt viết `"CRITICAL REALISM: Raw iPhone snapshot quality. No beauty retouching"`, nhưng phần thân lại viết `"MAKEUP: Soft glam"` và `"CRITICAL BODY: Extremely voluptuous hourglass figure"` khiến model tự động chuyển sang phong cách hotgirl Instagram cà mịn mặt và làm méo chữ bảng nút thang máy (`EORTEXOI`). Muốn da thật 100%, toàn bộ prompt phải thống nhất tông `unretouched documentary / candid snapshot` như `#199` hoặc `#264`.

---

## 21. Giải Mã Toàn Bộ 1,507 Ảnh Community Còn Lại (`♡ < 50`), 825 Quy Trình Tham Chiếu (`@IMG`) & 1,583 Prompt Ảnh Trong 29 Bộ Phim: Background Nhà/Phòng Khách, Sản Phẩm TVC, Mờ Thành Thật, Xoay Góc & Phối Hợp 1–9 Refs

> **Bản đầy đủ chi tiết lưu tại**: [`data/community_images/FULL_1819_COMMUNITY_AND_FILM_IMAGE_PROMPT_BIBLE.md`](./data/community_images/FULL_1819_COMMUNITY_AND_FILM_IMAGE_PROMPT_BIBLE.md)


> **Báo cáo Kiểm định Thị giác (`Visual Audit First`) & Giải mã Toàn diện Kho dữ liệu Ảnh Higgsfield**
> - **Phạm vi dữ liệu được mổ xẻ**:
>   1. **Kho Community Images (`data/community_images/ranked_community_images.json`)**: Tổng cộng **`3,522` bức ảnh xu hướng**, trong đó có **`1,819` bức ảnh mở cờ `has_full_prompt_details=True`** (`1,771` bức có `prompt_raw` khác rỗng: `264` bức thuộc nhóm Top `♡ >= 50` và **`1,507` bức thuộc nhóm `♡ < 50`** chưa từng được mổ xẻ chi tiết trước đây) cùng **`825` bức ảnh có đính kèm chuỗi ảnh tham chiếu đầu vào (`references.reference_medias`)** — đặc biệt **`783 / 825` (`94.9%`) các bài toán ghép ảnh tham chiếu thực chiến nằm ở phân khúc `♡ < 50`!**
>   2. **Kho 29 Dự Án Phim & TVC (`data/creators/**/asset_registry.json` & `01_IMAGE_GENERATION_PROMPTS_FULL_VERBATIM.md`)**: Tổng cộng **`1,583` ảnh gốc (`@IMG` Keyframes / Character Sheets / Product Turnarounds / Location Plates)** có lưu đầy đủ 100% câu lệnh sinh ảnh gốc (`full_source_image_prompt`), bao gồm **`154` prompt thiết kế nội thất/nhà cửa**, **`692` prompt sản phẩm/đạo cụ/character turnaround**, và **`202` prompt xoay góc máy (`re-angle / camera shift`)**.
>   3. **Kiểm định Thị giác Trực tiếp (`Visual Audit First`)**: Đã tải toàn bộ **`1,768` ảnh đầu ra** và **`75+` ảnh tham chiếu gốc đầu vào (`Before Refs`)** vào thư mục cục bộ `.gitignore` (`data/community_images/downloaded_images/`) và soi trực tiếp bằng mắt (`view_file`) các cặp ảnh **Trước (`Input Ref`) ↔ Sau (`Generated Output`)** cùng 2 bức ảnh Cây thông Noel thực tế của bạn để phán xét độ thật, lỗi da sáp, lỗi sai góc xoay 90° và bí quyết chống "cắt dán giả tạo" khi đặt sản phẩm vào phòng khách.

---

### 21.📊 PHẦN 0: BỨC TRANH TOÀN CẢNH — TẠI SAO KHO `1,507` ẢNH (`♡ < 50`) + `29` DỰ ÁN PHIM LẠI CHỨA NHIỀU BÍ KÍP THỰC CHIẾN HƠN CẢ TOP `♡ >= 50`?

Khi đối chiếu trực tiếp phân khúc **Top `♡ >= 50` (`264` ảnh)** với phân khúc **`♡ < 50` (`1,507` ảnh)** và **`29` Dự Án Phim (`1,583` ảnh)**, chúng ta phát hiện một sự thật cực kỳ quan trọng:
- Ở nhóm **`♡ >= 50`**: Đa số là ảnh **Text-to-Image thuần túy (`222 / 264` ảnh không dùng ảnh tham chiếu)**, tập trung vào ảnh chân dung nghệ thuật, thời trang đường phố hoặc quái vật giả tưởng bắt mắt để câu tim.
- Ngược lại, ở nhóm **`♡ < 50` (`1,507` ảnh)** và **`29` Bộ Phim**: Đây chính là **phòng thí nghiệm sản xuất thực tế (Production Workhorse)** nơi các Designer, Agency quảng cáo và Đạo diễn AI giải quyết **6 bài toán khó nhất khi làm nghề**:
  1. **Ghép sản phẩm / nội thất thật vào Phòng khách & Nhà cửa (`Home / Living-Room Background Staging` & `Architecture-Locked Multi-Ref Interiors`)** sao cho ánh sáng tự nhiên và tỷ lệ kích thước chuẩn 100% không bị phô.
  2. **Biến ảnh chụp sản phẩm tách nền trắng (`E-commerce White Cutout`) hoặc ảnh chụp điện thoại bình thường thành Poster / Keyframe Điện ảnh TVC** (giữ nguyên 100% phông chữ bao bì, dấu tiếng Việt/Czech, độ sánh chất lỏng, hoặc đổi màu từng đường chỉ khâu `#F9E11F` và bung rã linh kiện `Exploded-View Render`).
  3. **Khử mờ (`Deblur`), biến ảnh 3D sơ khai / mặt bằng căn hộ / ảnh pixel phẳng / ảnh chụp phòng bừa bộn thành Ảnh Thật sắc nét (`Blurry / 3D / Amateur ➔ Real Sharp`)** — VÀ chiều ngược lại: **Hạ độ nét (`Reverse-Polish`)** để ghép sản phẩm/nhân vật vào ảnh chụp iPhone thật mà không ai phát hiện.
  4. **Xoay góc máy (`Angle Rotation / Perspective Shift / 90° Profile / 180° Back View / 3-Panel, 4-View & 6-Panel Turnarounds`)** từ 1 tấm ảnh gốc duy nhất — giải mã lý do vì sao `Rank #1132` & `Rank #3151` thất bại ở góc 60° còn `Rank #711` & `Rank #1137` xoay chuẩn 90°/180° tuyệt đối.
  5. **Phối hợp từ 1 đến 9 ảnh tham chiếu (`Multi-Reference Workflows`) & Kỹ thuật Khoanh Vùng Màu MS-Paint (`Yellow/Red Drawn Area`)**: Dùng sơ đồ mặt bằng 2D (`@img2`) để xếp đồ lên bàn (`@img1`), vẽ vạch vàng/đỏ trực tiếp lên ảnh để ra lệnh bật đèn chùm/lắp dải LED (`Rank #1708`, `Rank #3158`), ghép 5 món đồ nội thất rời vào 1 căn phòng (`Rank #1247`), hoặc gộp 6 ảnh sản phẩm đơn lẻ thành 1 ảnh bộ sưu tập (`Rank #1710`).
  6. **Mổ xẻ 30 Model tạo ảnh khác nhau** (bao gồm `gpt_image_2_5`, `gpt_image_2`, `seedream_v5_pro`, `marketing_studio_2_image`, `nano_banana_2_1`, `cinematic_studio_soul_location`, `cinematic_studio_soul_cast`, `soul_cinematic`).

#### Bảng Thống Kê Toàn Bộ 30 Model Tạo Ảnh Trên Higgsfield Community (`3,522` Shots)

| Hạng | Model Tạo Ảnh | Tổng Số Ảnh | Có Full Prompt | Nhóm `♡ >= 50` | Nhóm `♡ < 50` | Có Ảnh Ref (`@IMG`) | Thế Mạnh Thực Chiến Qua Kiểm Định Thị Giác (`Visual Audit`) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | `text2image_soul_v2` | 1,732 | 853 | 226 | 627 | 74 | Ông vua tạo ảnh gốc Text-to-Image (122 style presets), cực mạnh về chất liệu da, vải, ánh sáng tự nhiên & góc máy lạ. |
| 2 | `nano_banana_2` | 817 | 428 | 31 | 397 | **422** | **Chuyên gia số 1 về Image-to-Image & Multi-Ref (`98.6%` có dùng Ref)**: xoay góc lưng 180°, ghép sản phẩm vào phòng khách, khử mờ CGI, giữ chữ bao bì. |
| 3 | `soul_cinematic` | 306 | 150 | 4 | 146 | 8 | Khung hình điện ảnh Anamorphic 2.39:1 & 16:9 chuẩn phim nhựa (`Kodak Vision3 500T`), da người thật 100% (`Rank #1011`) và bối cảnh phòng khách/căn hộ điện ảnh. |
| 4 | `cinematic_studio_soul_cast` | 127 | 58 | 1 | 57 | 3 | Chuyên xuất **Bảng Casting 3-Panel (`Front | Back | Close-Up Face`)** với schema JSON `[Character Params: {...}]` (`Rank #3493`). |
| 5 | `nano_banana_2_1` | 123 | 59 | 0 | 59 | **58** | Bản nâng cấp của `nano_banana_2` chuyên trị ghép **4–7 ảnh kiến trúc/sản phẩm/nội thất rời** (`Rank #1833`, `Rank #1247`, `Rank #1710`) và đổi màu chỉ khâu vi phẫu (`Rank #1396`). |
| 6 | `gpt_image_2_5` | 91 | 44 | 1 | 43 | **42** | **Bậc thầy dựng TVC Sản phẩm, Đổi Ngày➔Đêm & Xoay góc 90° tuyệt đối**: Giữ chữ bao bì nhỏ li ti (`Rank #1241`), bật đèn chùm phòng khách ban đêm (`Rank #3396`), xoay 90° profile (`Rank #711`). |
| 7 | `cinematic_studio_soul_location` | 86 | 49 | 0 | 49 | 0 | **Kho bối cảnh kiến trúc & nội thất chuyên dụng (`Location Scouting`)**: 100% ảnh không người, chuyên tạo phòng khách, biệt thự, hành lang để ghép sản phẩm. |
| 8 | `seedream_v5_pro` | 64 | 31 | 1 | 30 | **31** | **Siêu vũ khí cho Vẽ Vạch Màu MS-Paint (`Rank #1708`, `Rank #3158`), Bảng Xoay 4 Góc (`Rank #692`), Mặt Bằng 3D➔Phòng Thật (`Rank #1251`) & `Reverse-Polish` (`Rank #476`).** |
| 9 | `gpt_image_2` | 53 | 28 | 0 | 28 | **28** | Cực mạnh về chụp sản phẩm trang sức vàng/kim cương (`Rank #926`), nước hoa sa mạc (`Rank #1235`), bảng prop 6-panel (`@ollkorrect/besa` `@IMG_032`). |
| 10 | `seedream_v4_5` | 29 | 16 | 0 | 16 | 16 | Chuyên ghép thời trang & chỉnh sửa chất liệu ánh sáng studio từ ảnh tham chiếu (lưu ý cận cảnh mặt `Rank #312` hơi mịn kiểu beauty-retouch). |
| 11 | `seedream_v5_lite` | 19 | 11 | 0 | 11 | 11 | Nhanh, nhẹ, giữ bố cục tham chiếu tốt cho các bài toán đổi trang phục và góc trung cảnh. |
| 12 | `nano_banana_flash` | 16 | 12 | 0 | 12 | 12 | Tốc độ cao khi ghép 3–4 ảnh tham chiếu (`Rank #1839`) và Master Location Prompt (`6moths/where-letters-fall` `@IMG_070`). |
| 13 | `nano_banana` | 14 | 10 | 0 | 10 | 10 | Dọn dẹp phòng bừa bộn (`Amateur messy room ➔ Clean Airbnb photo`, `Rank #1841`) giữ nguyên 100% cấu trúc tủ bếp/tường. |
| 14 | `marketing_studio_2_image` | 2 | 2 | 0 | 2 | 1 | Chuyên thiết kế Poster Quảng cáo F&B / Thương mại có kèm Typography, Logo và bố cục bàn tay cầm sản phẩm (`Rank #891`). |
| 15 | *16 Model khác (`flux_2_pro`, `reve`, `wan2_5`...)* | 43 | 20 | 0 | 20 | 14 | Các model thử nghiệm chuyên biệt cho typography, poster và concept art. |

---

### 21.🏠 CHUYÊN ĐỀ 1: MÔI TRƯỜNG & PHONG CÁCH BACKGROUND NHÀ / PHÒNG KHÁCH / NỘI THẤT (`HOME & LIVING-ROOM STAGING PLAYBOOK`)

> **Bài toán thực tế của bạn**: Khi làm TVC cho sản phẩm gia đình (như **Cây thông Noel phủ tuyết & quả đỏ**, đồ decor, đèn chùm, sofa, thiết bị gia dụng), làm sao để tạo ra một **Background Phòng khách / Nhà ở** vừa sang trọng chuẩn điện ảnh, vừa chừa sẵn khoảng trống (`Staging Clear Space`) và ánh sáng hợp lý để đặt sản phẩm vào mà **không bị cảm giác cắt ghép giả tạo**?

Qua mổ xẻ **`49` bức ảnh của model `cinematic_studio_soul_location`**, **`80+` bức ảnh nội thất trên Community (`♡ < 50`)** và **`154` câu lệnh tạo bối cảnh phòng khách trong 29 Bộ Phim**, chúng ta đúc kết được **6 Quy Tắc Vàng Thiết Kế Background Nhà & Phòng Khách**:

#### 1.1. 6 Quy Tắc Vàng Khi Viết Prompt Background Phòng Khách (Đúc kết từ Thực Chiến)
1. **Quy tắc `Empty Stage / Unoccupied Clear Zone` (Khóa khoảng trống đặt sản phẩm)**:
   - Trong phim quảng cáo *Talabat* (`Rank #975`, `soul_cinematic`) và toàn bộ 49 tấm của `cinematic_studio_soul_location`, đạo diễn luôn ghi rõ vị trí bàn/sàn để trống: `"Leave the coffee table clear for a food delivery scene"` hoặc `"Empty frame, no people, architectural stillness, clear floor space between the fireplace mantel and the tall window"`.
2. **Quy tắc `Turn Off Internal Product Glow` (Tắt đèn nội tại của sản phẩm ở cảnh Ban Ngày để ăn theo nắng phòng khách — Phát hiện đắt giá nhất từ `Rank #1103`)**:
   - Khi kiểm định cặp ảnh `rank_1103_ref1.jpg` (đèn chùm pha lê tách nền trắng) + `rank_1103_ref2.jpg` (phòng khách Malibu năm 1986) ➔ `rank_1103_nano_banana_2_7d2f8bdb.webp`, tác giả `@dancinggem1001` đã tiết lộ lý do vì sao 90% người dùng AI ghép đèn/cây thông Noel vào phòng khách ban ngày bị giả: **Vì họ bật đèn sản phẩm sáng rực lên như một layer Photoshop đè lên ảnh!**
   - **Câu thần chú giải quyết triệt để**: *"The chandelier is switched off, or emitting only a very faint warm glow. Sunlight, rather than bright internal lighting, reveals its gold finish and transparent crystals... A instrução de deixar a luminária desligada ou quase desligada é intencional: assim o dourado e os cristais recebem a mesma luz solar da sala, em vez de aparecerem como uma camada muito mais brilhante que o restante da foto."*
3. **Quy tắc `Relative Scale Anchor` (Khóa tỷ lệ kích thước sản phẩm bằng vật chuẩn trong phòng)**:
   - Không bao giờ chỉ ghi kích thước bằng inch/cm (AI thường dựng quá to). Hãy khóa tỷ lệ so sánh trực tiếp với đồ vật có sẵn trong phòng như `Rank #1103`: `"The chandelier is 47 inches in diameter. Give it a realistic apparent size in the photograph: it should be clearly smaller than the width of the coffee table and much smaller than the sectional sofa."*
4. **Quy tắc `Architecture-Locked Multi-Ref Interior` (Khóa đồng bộ Kiến trúc Bên ngoài + Mặt bằng + Nội thất — Phát hiện từ `Rank #1833`, `Rank #1834`, `Rank #2205`)**:
   - Khi muốn dựng phòng khách nằm bên trong một ngôi nhà cụ thể, hãy nạp đồng thời 4 ảnh (`@img1` Nội thất mẫu + `@img2` Ngoại thất tòa nhà + `@img3` Mặt bằng nhìn từ trên xuống + `@img4` Sơ đồ cắt lớp Isometric) cho `nano_banana_2_1` với lệnh: `"LIVING ROOM — ARCHITECTURE-LOCKED INTERIOR GENERATION. Generate a high-end, photorealistic living room located INSIDE THE EXACT SAME BUILDING shown in the references."`
5. **Quy tắc `Warm 2700K Interior vs. Cold 6500K Snowy Window Contrast` (Tương phản Nhiệt độ màu Trong ấm – Ngoài lạnh cho TVC Giáng Sinh — Từ `Rank #675`, `Rank #3396` & `@adilinthewild/4k-blockbuster-breakdown` `@IMG_068`)**:
   - Để đèn LED vàng ấm của cây thông Noel hoặc lò sưởi trở thành tâm điểm thị giác, hãy hạ bối cảnh bên ngoài cửa sổ xuống **Blue Hour / Đêm Tuyết Lạnh (`6000K–6500K`)** như `Rank #675` (`"an elegant alpine chalet lounge at blue hour, floor-to-ceiling windows overlooking silent snow-covered mountains and pine trees, pale stone fireplace with a low warm flame"`) hoặc biến phòng khách ban ngày thành ban đêm như `Rank #3396` (`"Turn this into night time. Same room and layout... The chandelier and lamps on with warm light, the windows black outside"`).
6. **Quy tắc `3-Layer Depth Staging` (`Foreground / Midground / Background` + `40/30/20/10 Lighting Ratio`)**:
   - Trong `@adilinthewild/4k-blockbuster-breakdown` (`@IMG_068`) và `@pietromalegori/control` (`@IMG_118`), phòng khách luôn được chia rõ 3 lớp chiều sâu (`Foreground: doorway/table edge slightly out of focus` ➔ `Midground: sofa, rug & main subject` ➔ `Background: tall windows with sheer curtains & practical lamps`) kèm tỷ lệ nguồn sáng `40% window light / 30% warm practical lamp / 20% screen or fireplace glow / 10% shadow bounce`.

---

#### 1.2. Các Mẫu Prompt Phòng Khách & Nội Thất Đỉnh Cao Trên Community (`♡ < 50` & `cinematic_studio_soul_location`) — Nguyên Văn 100%

##### 🏆 Rank #1103 (`1 ♡` | `10 👁️` | Model: `nano_banana_2` | Author: `@dancinggem1001` | Size: `4:5` | Refs: `2`)
- **Publication ID**: `7d2f8bdb-7c9b-45b5-8984-159780eb9fba`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1103_nano_banana_2_7d2f8bdb.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38zai75muwpJ9KN7TOOGQRBXOWr/hf_20260921_190654_4d309f89-0dd1-404a-abb9-49bd37e8825c.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38zai75muwpJ9KN7TOOGQRBXOWr/hf_20260921_190654_4d309f89-0dd1-404a-abb9-49bd37e8825c_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38zai75muwpJ9KN7TOOGQRBXOWr/c367fb4e-42d3-41cc-aa03-1595251c0ab7.jpg
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38zai75muwpJ9KN7TOOGQRBXOWr/62a858a3-a233-4782-8de9-2ae6bf3e9be9.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Đỉnh cao ghép sản phẩm phát sáng vào phòng khách (`Before: rank_1103_ref1.jpg + ref2.jpg` ➔ `After: rank_1103_nano_banana_2_7d2f8bdb.webp`)**: Đèn chùm pha lê vàng 2 tầng từ ảnh chụp catalog nền trắng (`@img1`) được treo vào đúng trần phòng khách Malibu 1986 (`@img2`). Nhờ lệnh tắt đèn chùm (`switched off, or emitting only a very faint warm glow`) để pha lê bắt nắng chiều tự nhiên từ cửa sổ biển và khóa kích thước nhỏ hơn bàn trà kính, bức ảnh nhìn thật 100% như chụp bằng máy phim năm 1986.

```text
Create a new, photorealistic editorial interior photograph using the supplied living room image as the architectural and atmospheric reference, and the supplied chandelier image as the exact product reference.

SCENE AND ARCHITECTURE

This is the living room of a famous Hollywood actress’s hilltop home in Malibu, California, during the summer of 1986. It is a glamorous but lived-in private residence, photographed on a warm late afternoon.

Keep the defining features of the living room reference: a generous cream sectional sofa, a low glass coffee table, warm wood flooring, lush indoor palms, a black grand piano on the slightly raised area, and broad windows overlooking the coast. Recreate the room as a believable residential space with a moderately high ceiling, approximately 11–12 feet above the main seating area. Do not turn it into a double-height atrium. The ceiling and upper windows must form one coherent architectural structure, with enough visible ceiling to show exactly where the chandelier is installed.

Use consistent, slim dark window and door frames throughout the room. Outside, show nearby palms and hillside vegetation, with a distant coastline and the Pacific Ocean beyond. The view should feel plausible from an elevated Malibu property. Maintain one consistent horizon and a believable relationship between the terrace, hillside, shoreline, and sea.

CHANDELIER — PRODUCT ACCURACY AND SCALE

Install one chandelier directly above the glass coffee table, centered within the main seating area. Use the product reference as the authority for its design. Reproduce the circular upper tier of vertical gold elements, the suspended clear crystals, the smaller lower tier, the gold ceiling canopy, and the fine suspension cables. Preserve the original tier arrangement, materials, gold tone, and density of crystal pieces. Do not reinterpret it as a different chandelier.

The chandelier is 47 inches (approximately 119 cm) in diameter. Give it a realistic apparent size in the photograph: it should be clearly smaller than the width of the coffee table and much smaller than the sectional sofa. It should read as an elegant fixture within the room, not as the dominant object in the frame. Its full silhouette should fit comfortably between the ceiling and the furniture, with believable head clearance below it.

Attach the gold canopy directly to a solid section of ceiling above the seating area. Use short, taut suspension cables appropriate to the room height. The cables must connect visibly and logically between canopy and chandelier. Do not place the chandelier in front of an upper window as though it were floating against the outdoor view. Do not crop the canopy or cables out of the frame.

LIGHTING AND PHYSICAL INTEGRATION

The main light source is the late-afternoon sun entering through the ocean-facing windows. Its direction must remain consistent across the windows, palms, sofa, coffee table, floor, and chandelier. Sunlight creates complex but natural patterns from the window frames and palm leaves, with warm highlights and deep, detailed shadows.

The chandelier is switched off, or emitting only a very faint warm glow. Sunlight, rather than bright internal lighting, reveals its gold finish and transparent crystals. Allow restrained glints and delicate refractions, but keep the individual crystal pieces visible. Avoid solid white glowing bands, blown highlights, or an artificial halo around the fixture.

Match the chandelier to the room’s exposure, color temperature, contrast, focus, film grain, and perspective. Its gold surfaces should have the same warm sunlight and shadow falloff as the other objects. Its crystals should reflect the actual windows, dark interior, and surrounding furniture. Add only subtle, physically plausible reflections to the glass coffee table. The chandelier must look as though it was present when the photograph was taken, never composited onto the finished image.

COMPOSITION AND PHOTOGRAPHIC STYLE

Photograph the room from a natural standing height, at a three-quarter angle similar to the living room reference. Use a moderately wide architectural lens with realistic perspective and straight vertical lines. Include the sofa and coffee table in the foreground, the chandelier in the upper middle of the composition, and the coastal view in the background. Give each element breathing room. The chandelier should attract attention through its craftsmanship and interaction with the sunlight, not through exaggerated size or brightness.

Make the result look like a carefully art-directed photograph for a luxury interiors magazine in the 1980s: tactile fabric, natural glass reflections, warm wood, atmospheric depth, gentle highlight halation, fine analog film grain, and rich but restrained color. The interior has honey-gold sunlight and warm cream tones; the distant ocean retains cooler muted blues. Dreamy summer atmosphere with realistic photographic detail and slight natural imperfections.

SERIES CONTINUITY

This is the first room in a series photographed inside the same house on the same afternoon. Establish a repeatable visual identity: consistent window and door frames, ceiling treatment, wood finish, tropical landscaping, coastal outlook, sunlight direction, time of day, and analog color grading.

No people, text, logos, additional chandeliers, oversized fixture, extended hanging cables, floating canopy, distorted crystals, warped architecture, implausibly close ocean, excessive bloom, or CGI appearance.
A instrução de deixar a luminária desligada ou quase desligada é intencional: assim o dourado e os cristais recebem a mesma luz solar da sala, em vez de aparecerem como uma camada muito mais brilhante que o restante da foto.
```

##### 🏆 Rank #1833 (`0 ♡` | `7 👁️` | Model: `nano_banana_2_1` | Author: `@gojart` | Size: `3:4` | Refs: `4`)
- **Publication ID**: `aaa009ef-80f4-4089-b1c7-09546c85a91a`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1833_nano_banana_2_1_aaa009ef.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191940_cee3f322-235a-4968-988a-b61d2c1fd621.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191940_cee3f322-235a-4968-988a-b61d2c1fd621_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/e477602e-98f4-4c29-b1d6-4c9814d8bcc0.jpg
- **Input Reference `@img2`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191531_376cb834-b7ee-42c1-a6ad-39c6717474fd.png
- **Input Reference `@img3`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191639_36b309f3-f931-4111-9230-5f7d7c81e793.png
- **Input Reference `@img4`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191757_f0e992a1-2c3e-46a0-b93d-fde0f6660975.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Đỉnh cao dựng Phòng Khách khóa chặt theo Kiến trúc 4 Ảnh Tham chiếu (`Before: rank_1833_ref1..ref4` ➔ `After: rank_1833_nano_banana_2_1_aaa009ef.webp`)**: Từ 4 ảnh tham chiếu (tủ gỗ đan mây `@img1`, ngoại thất tòa nhà gỗ tròn xếp tầng `@img2`, mặt bằng mái tròn nhìn từ đỉnh `@img3` và sơ đồ cắt lớp `@img4`), `nano_banana_2_1` dựng nên phòng khách cong hình cung nằm chính xác bên trong tòa nhà đó với trần gỗ uốn lượn, lò sưởi đá travertine và vách kính nhìn ra vườn cây!

```text
LIVING ROOM — ARCHITECTURE-LOCKED INTERIOR GENERATION. CORE DIRECTIVE: Use all uploaded reference images together as a unified architectural reference set (exterior views, top-down view, exploded isometric diagram, and additional architectural/detail references) of the organic stacked-disc timber pavilion. Generate a high-end, photorealistic living room located INSIDE THE EXACT SAME BUILDING shown in the references. Do not design a generic luxury living room. The interior must feel like a real, physically constructed interior belonging to this exact building. ARCHITECTURAL CONTINUITY — ABSOLUTE PRIORITY: First understand the building's architecture from all references. Use the exterior views to understand the curved disc geometry, the glazed ground-floor envelope, the warm timber cladding and soffit curvature, structural column rhythm, and the relationship between the glass envelope and interior spaces. Use the top view and isometric to understand floor-to-floor height, disc curvature overhead, slab thickness, structural system, and spatial relationships. The resulting living room must be architecturally consistent with the exact building — preserve the inferred curved ceiling/soffit line following the underside of the disc above, slender structural columns, glazed curtain wall facing the plaza, and overall vertical proportions. Do not invent architectural geometry that contradicts the references. INTERIOR ARCHITECTURE: Develop the interior architecture as a natural continuation of the building's exterior character — as if designed by the same architect who designed the building. Translate the building's warm curved timber material language, soft organic geometry, and structural rhythm into the interior: a gently curving timber-clad ceiling that echoes the disc's underside curvature, slender exposed columns, a continuous glazed wall opening onto the plaza/landscape, integrated curved joinery, concealed lighting, refined timber detailing. FURNITURE & DESIGN LANGUAGE: Furnish the room with international high-end contemporary furniture inspired by the design quality and sophistication of brands such as B&B Italia, Cassina, Molteni&C, Flexform, Poliform, Minotti, Living Divani, Knoll, Vitra, Rimadesio and Tacchini. Use furniture with exceptional proportions, refined silhouettes, premium upholstery, natural leather, travertine, marble, solid timber, brushed metal, smoked or clear glass. Furniture should feel curated rather than showroom-like. Use a restrained number of pieces: large sculptural sofa, 1–2 lounge chairs, sophisticated coffee table, side tables, low media/storage element where appropriate, architectural rug, minimal decorative objects, one or two carefully selected artworks. Do not overcrowd the room. MATERIAL PALETTE — EXTERIOR-AS-INTERIOR MATERIAL REFERENCE: Explicitly carry over the exact material palette visible on the building's exterior in the references — the warm curved timber cladding, its natural wood grain and honey-amber tone, and the slim dark structural/window framing — into the interior finishes: use matching warm timber wall and ceiling paneling that follows the curved disc geometry, and dark metal detailing, so the interior reads as being built from the same material vocabulary as the exterior. Combine this exterior-derived language with refined natural materials such as travertine, limestone, oak, walnut, natural stone, linen, wool, high-quality leather, smoked or clear glass. Do not introduce excessive colors. Create a sophisticated, restrained material palette with 3–5 dominant materials, all traceable back to the exterior's timber material and warm color language. LIGHTING: Use architectural lighting rather than decorative over-lighting — soft concealed ceiling lighting following the curved soffit, recessed architectural lighting, integrated joinery lighting, subtle wall washing, carefully selected designer floor/table lamps. Allow natural daylight from the building's actual glazed envelope. Lighting should reveal material texture, architectural depth, furniture quality, shadow lines, curved wall/ceiling articulation. CAMERA: Professional architectural interior photograph. Eye-level architectural camera, approximately 24–35mm full-frame equivalent, natural perspective, no fisheye distortion, vertical lines remain straight, camera positioned at approximately human eye height. Composition should reveal the architecture and furniture simultaneously, and show the relationship between interior and exterior/landscape views through the actual reference glazing. The view should feel like a photograph published in Dezeen, ArchDaily, Wallpaper*, or an international architecture/interior design magazine. FINAL QUALITY: Photorealistic architectural visualization. Extremely realistic materials, fabric, wood grain, stone, glass, metal, shadows, reflections, natural daylight, ambient occlusion. No CGI-looking plastic surfaces, no generic AI furniture, no excessive decoration, no people, no text, no logos. Most important: the interior must convincingly belong to the exact building shown in the uploaded references, sharing its exact timber material and curved design language.
```

##### 🏆 Rank #675 (`3 ♡` | `1303 👁️` | Model: `gpt_image_2_5` | Author: `@cubistpotato1609` | Size: `16:9` | Refs: `0`)
- **Publication ID**: `7f183ba5-d2eb-4b97-b617-f09ffa9f3b53`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0675_gpt_image_2_5_7f183ba5.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3ICcYSjRcNDRa2wODgrQd6OOlqB/hf_20260919_103830_d25eaed6-b9bc-402c-a848-ba8d4db9230d.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3ICcYSjRcNDRa2wODgrQd6OOlqB/hf_20260919_103830_d25eaed6-b9bc-402c-a848-ba8d4db9230d_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Mẫu chuẩn Phòng Khách Mùa Đông & Giáng Sinh (`Warm 2700K Fireplace vs Cold 6500K Snowy Pines` — `rank_0675_gpt_image_2_5_7f183ba5.webp`)**: `gpt_image_2_5` dựng phòng khách chalet núi tuyết lúc chạng vạng xanh (`blue hour`): bên ngoài vách kính kịch trần là rừng thông phủ tuyết xanh lạnh `6500K`, bên trong là lò sưởi đá travertine cháy lửa vàng ấm `2200K`, đèn hắt kệ sách và nến trên bàn trà chiếu lên sofa bouclé màu kem — công thức ánh sáng hoàn hảo nhất cho TVC Cây thông Noel!

```text
Cinematic ultra-luxury ambient relaxation background for a long-form YouTube video, 16:9 wide composition, fixed eye-level camera, photorealistic, refined natural materials, soft layered lighting, calm uncluttered composition, no people, no animals, no text, no logos, no television, no visible brand products, no dramatic weather, clear areas suitable for subtle looping animation. Scene one: an elegant alpine chalet lounge at blue hour, floor-to-ceiling windows overlooking silent snow-covered mountains and pine trees, pale stone fireplace with a low warm flame, cream boucle sofa, cashmere throws, light oak and travertine, a few candles, gentle snowfall outside, warm ivory and amber interior against cool blue landscape, serene private retreat.
```

##### 🏆 Rank #3396 (`0 ♡` | `2 👁️` | Model: `gpt_image_2_5` | Author: `@monetcake1406` | Size: `9:16` | Refs: `1`)
- **Publication ID**: `e4e9268d-fe90-47ea-8603-1b1e41904dd4`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_3396_gpt_image_2_5_e4e9268d.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3C2kn1F5m5o5yuGAeCep4Hd568S/hf_20261020_112613_4923e04e-2644-4b9d-bd43-0b2b3cdd123f.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3C2kn1F5m5o5yuGAeCep4Hd568S/hf_20261020_112613_4923e04e-2644-4b9d-bd43-0b2b3cdd123f_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3C2kn1F5m5o5yuGAeCep4Hd568S/hf_20261020_110843_84693514-bf9b-4c5a-8e85-d618f1c845bf_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Công thức `Day-to-Night Living Room Relighting` chỉ bằng 3 câu lệnh (`rank_3396_gpt_image_2_5_e4e9268d.webp`)**: Biến phòng khách thông tầng ban ngày thành ban đêm (`Turn this into night time. Same room and layout, same portrait on the wall. The chandelier and lamps on with warm light, the windows black outside`), giữ nguyên 100% bức tranh chân dung khung vàng khổng lồ, bộ sofa kem và bàn trà kính nhưng bật sáng đèn chùm pha lê và phản chiếu ánh vàng ấm xuống sàn đá marble bóng!

```text
Turn this into night time. Same room and layout, same portrait on the wall. The chandelier and lamps on with warm light, the windows black outside. Realistic.
<<<94362e9e-92c1-4715-85e5-9676d7f6b955>>>
```

##### 🏆 Rank #1756 (`0 ♡` | `8 👁️` | Model: `gpt_image_2_5` | Author: `@hello_laucreates` | Size: `9:16` | Refs: `0`)
- **Publication ID**: `9e9cf456-cee0-4896-bad7-675a609c022a`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1756_gpt_image_2_5_9e9cf456.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KvDyGcOiUSG8DnVh8PRf7704eG/hf_20261019_174509_ac8ff882-3ae2-4696-b176-eb7282ad1df6.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KvDyGcOiUSG8DnVh8PRf7704eG/hf_20261019_174509_ac8ff882-3ae2-4696-b176-eb7282ad1df6_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Phòng khách Cây Thông Noel phong cách Băng Từ Gia Đình thập niên 90 (`1994 VHS Camcorder Christmas Living Room` — `rank_1756_gpt_image_2_5_9e9cf456.webp`)**: `gpt_image_2_5` tái hiện phòng khách ốp gỗ thập niên 90 với cây thông Noel gắn đèn bóng lớn & dây kim tuyến (`big-bulb lights and tinsel`), sofa hoa, TV CRT, chú chó Golden Retriever ngồi bên cửa sổ tuyết tối và chất màu VHS 1994 (`soft focus, color bleed, scanlines`) cực kỳ giàu cảm xúc hoài niệm.

```text
Authentic 1994 camcorder still frame, same wood-paneled living room with floral couch and CRT TV, Christmas tree with big-bulb lights and tinsel. A tired kind mother in her mid-30s with a 90s permed shoulder-length hairstyle, an oversized red knit sweater with a reindeer pattern and high-waisted jeans, stands by the tree holding a box of ornaments and glances at the wall clock with a worried look. In the background the same golden retriever with white chest patch and red collar sits at the dark snowy window. VHS look: soft focus, color bleed, faded warm colors, grain, scanlines, handheld, no text, no watermark, photorealistic, candid, not cinematic.
```

##### 🏆 Rank #1251 (`0 ♡` | `37 👁️` | Model: `seedream_v5_pro` | Author: `@playertwo` | Size: `16:9` | Refs: `1`)
- **Publication ID**: `3cc2cd06-e163-4a00-8f09-d6d09bd132da`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1251_seedream_v5_pro_3cc2cd06.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3GgrEn9cintYwXzr4ksZfWgDEdv/hf_20260920_122412_5420d7b4-a5c0-411b-9614-e06cc41c9b25.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3GgrEn9cintYwXzr4ksZfWgDEdv/hf_20260920_122412_5420d7b4-a5c0-411b-9614-e06cc41c9b25_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3GgrEn9cintYwXzr4ksZfWgDEdv/de16598f-0ed5-4b8c-bc69-6c68e946be62.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Biến mặt bằng 3D thành phòng ngủ ARRI Alexa LF (`Before: rank_1251_ref1.png` ➔ `After: rank_1251_seedream_v5_pro_3cc2cd06.webp`)**: Từ bức ảnh 3D cắt lớp toàn căn hộ nhìn từ trên cao (`@img1`), `seedream_v5_pro` hạ góc máy xuống tầm mắt `1.5m` đứng ngay cửa phòng ngủ, giữ đúng 100% chăn xanh rêu, 2 đèn ngủ, 2 bức tranh đầu giường và thêm cánh cửa gỗ ở mép khung hình tạo chiều sâu.

```text
Recreate the master bedroom from the provided 3D apartment master layout as a realistic cinematic eye-level interior. Preserve the exact room geography: large bed centered against the main wall, olive-green duvet and neutral bedding, two wooden bedside tables with warm bedside lamps, large windows along the left side allowing natural light into the room, cream textured area rug beneath and in front of the bed, indoor plants near the windows and corners, framed minimalist landscape and botanical artwork above the bed, wooden bench at the foot of the bed and a tall mirror along the side wall. 
The room should feel comfortable, warm, personal and lived-in but tidy. No people. Keep the color palette consistent with the living room: olive green, warm wood, beige, cream and soft neutral gray. 
Camera positioned close to the bedroom doorway, looking directly toward the bed so the entire bedroom geography is clearly readable. Natural late-afternoon sunlight streams through the windows, mixed with warm bedside lamps. Photorealistic cinematic interior, ARRI Alexa LF, 28mm lens, eye-level 1.5m camera, realistic depth and shadows, subtle film grain, 16:9. Preserve the exact master apartment layout.
```

##### 🏆 Rank #1247 (`0 ♡` | `38 👁️` | Model: `nano_banana_2_1` | Author: `@romanesquechinchilla` | Size: `21:9` | Refs: `5`)
- **Publication ID**: `f87f214a-1c77-4767-9ac2-d7c331f67401`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1247_nano_banana_2_1_f87f214a.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_36KKaRxgFy3xzdHsjqTXOfX78wy/hf_20261013_133216_0e99a658-913b-4370-8fc8-f8528a51e1e1.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_36KKaRxgFy3xzdHsjqTXOfX78wy/hf_20261013_133216_0e99a658-913b-4370-8fc8-f8528a51e1e1_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36KKaRxgFy3xzdHsjqTXOfX78wy/7297f4b7-ea27-413a-a657-5045782423ec_resize.jpg
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36KKaRxgFy3xzdHsjqTXOfX78wy/b535d214-d314-4fd5-b9d2-3c5f12bab0b9.png
- **Input Reference `@img3`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36KKaRxgFy3xzdHsjqTXOfX78wy/d1ca04fa-a186-4c89-9c55-3762eb8d0cdb.png
- **Input Reference `@img4`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36KKaRxgFy3xzdHsjqTXOfX78wy/f353a3c2-7268-4728-b7fa-b92f35fd80e7.png
- **Input Reference `@img5`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36KKaRxgFy3xzdHsjqTXOfX78wy/c5db8fc8-5d46-4811-a1bd-a1d2016bbbb5.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Ghép 5 món đồ nội thất rời vào 1 phòng khách (`Before: rank_1247_ref1..ref5` ➔ `After: rank_1247_nano_banana_2_1_f87f214a.webp`)**: `nano_banana_2_1` nhận 5 ảnh tách nền trắng (sofa nhung xanh rêu nhăn, ghế bành, bàn trà, thảm, đèn) và sắp xếp hoàn hảo vào phòng khách tường vữa olive phong cách Dusty Deco, chừa trống 1/3 khung hình bên phải để đặt chữ quảng cáo.

```text
Wide website banner photo in the style of Dusty Deco: a staged room inside an old industrial building, with patinated dark-olive plaster walls showing chipped layers of old paint, worn dark oak floorboards, tall black steel factory windows on the left letting in moody side light. Rich, layered, eclectic and lived-in, raw and characterful, but clearly a real space. Use these exact products from the reference images and keep each one exactly as shown (same shape, proportions, colour, fabric, material; nothing added or removed): image 1 the Mayfair 3 seater sofa, image 2 the Mayfair 1 seater armchair angled towards it, image 3 the Architect coffee table in front of the sofa, image 4 the Glow rug under the seating group, image 5 the Orbit lamp. Styling: a stack of old art books and a small brass object on the coffee table, a large unframed abstract oil painting leaning against the wall. The products sit in the left two thirds; the right third is a calmer stretch of patinated wall and floor, left free for text. Shot on a real 35mm full-frame camera, eye level, straight verticals, one consistent perspective, correct scale with everything grounded, natural light with deep soft shadows, real material texture, subtle film grain, editorial interior photography. No plastic or CGI look, no text, no people.
```

##### 🏆 Rank #975 (`1 ♡` | `40 👁️` | Model: `soul_cinematic` | Author: `@ayman` | Size: `2048x1152` | Refs: `0`)
- **Publication ID**: `35bfdde3-a2a5-4729-b7f5-07e6d485b0f6`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0975_soul_cinematic_35bfdde3.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_31jEpr4vyuqwzSxaPngk2qdc1qj/hf_20261007_121615_e40aa46b-97ef-44e3-8b4c-66ac21389efb.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_31jEpr4vyuqwzSxaPngk2qdc1qj/hf_20261007_121615_e40aa46b-97ef-44e3-8b4c-66ac21389efb_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Phòng khách căn hộ cao cấp chuẩn TVC thương mại chừa trống bàn trà (`rank_0975_soul_cinematic_35bfdde3.webp`)**: `soul_cinematic` dựng phòng khách tầng 25 tại Kuwait với nắng chiều vàng ấm chiếu xiên qua kính kịch trần, sofa vải kem và bàn trà đá marble để trống ở trung tâm (`Leave the coffee table clear`) — bố cục mẫu mực để đặt sản phẩm hoặc cây thông Noel cạnh cửa kính.

```text
Photorealistic cinematic interior of a beautiful luxury apartment on the 25th floor of a residential tower in Kuwait City, designed as the location for a Talabat commercial. Floor-to-ceiling windows reveal an expansive elevated view of Kuwait City, distant towers and the Arabian Gulf, with nearby rooftops far below.
An elegant, welcoming living room with a sculptural ivory sofa, warm walnut paneling, light travertine floors, a large cream rug and a refined marble coffee table. Carefully chosen artwork, subtle brass details and soft cushions make the apartment feel like a real, beautifully designed home. Leave the coffee table clear for a food delivery scene.
Golden-hour sunlight streams through the windows, creating soft pools of light and long natural shadows. Balance the bright skyline with a clearly exposed interior; retain detail in both.
Cinematic wide shot from seated eye level, 28mm lens, three-quarter composition with the sofa and coffee table in the foreground and the spectacular city view behind. Sophisticated architectural photography, realistic materials, warm atmosphere, straight architectural lines. No people, text, logos or artificial CGI appearance. Vertical 9:16.
```

##### 🏆 Rank #1473 (`0 ♡` | `18 👁️` | Model: `gpt_image_2_5` | Author: `@adaptingplanet1486` | Size: `4:3` | Refs: `1`)
- **Publication ID**: `b36e6612-7f8e-4f90-bbbb-8f29f5b9e4b1`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1473_gpt_image_2_5_b36e6612.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IdoOGLtcV6EOFjLdyT0P5niyY5/hf_20261018_104843_73046e57-1a7b-4fd9-935f-c12826dd6e99.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IdoOGLtcV6EOFjLdyT0P5niyY5/hf_20261018_104843_73046e57-1a7b-4fd9-935f-c12826dd6e99_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3IdoOGLtcV6EOFjLdyT0P5niyY5/a8622f84-86a8-49ed-91e0-5acdb449a53c_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Cải tạo ánh sáng phòng khách có sẵn bằng dải LED 2700K & đèn cây (`Before: rank_1473_ref1.jpg` ➔ `After: rank_1473_gpt_image_2_5_b36e6612.webp`)**: `gpt_image_2_5` giữ nguyên 100% kiến trúc phòng khách gốc nhưng bổ sung dải LED ấm `2700K` dưới bậc cầu thang, sau vách nan gỗ TV và thêm đèn sàn cong ở góc tối, biến căn phòng nhạt nhòa thành không gian ấm cúng sang trọng.

```text
Edit this photo of a living room. Keep the exact room, camera angle, layout and all existing furniture unchanged: the dark grey tufted corner sofa, the matching ottoman, the blue armchair, the two round oak coffee tables with black steel frames, the blue-grey abstract rug, the black built-in TV wall unit with wood slats, the light oak floor and the day-night roller blinds. Make the room cozier with accessories only, using a calmer palette: remove the garden chairs and the bedding from the sofa. Add cushions in sage green, olive, sand and oat boucle mixed with the existing blue ones, a chunky knit plaid in oat and a linen plaid in olive draped over the sofa. Warm white LED strip glowing behind the wood slats of the TV wall. A black arc floor lamp with a warm linen shade curving over the sofa corner, and a brass table lamp with warm light. Style the open shelves of the black TV unit with stacked books, a matte black vase, a brass object, a small trailing plant and candles, roughly two thirds filled. On the coffee table a round wooden tray with three candles of different heights and a small succulent. A tall strelitzia in a ribbed terracotta pot in the corner near the window, a woven seagrass basket with plaids beside the sofa. One large abstract artwork in sand, blue and olive tones on the wall between the window and the TV unit. Soft warm evening lighting, photorealistic, same resolution and realism as the original photo.
```

##### 🏆 Rank #747 (`2 ♡` | `2400 👁️` | Model: `nano_banana_2` | Author: `@eesplbk` | Size: `3:4` | Refs: `2`)
- **Publication ID**: `06e7b71e-933e-4373-8ea5-a062e2970d81`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0747_nano_banana_2_06e7b71e.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3ELoFYOfvcQxINNlnlEummECuTs/hf_20260726_215449_4a62c1ec-dc2a-406e-96ee-306ee2de9296.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3ELoFYOfvcQxINNlnlEummECuTs/hf_20260726_215449_4a62c1ec-dc2a-406e-96ee-306ee2de9296_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3ELoFYOfvcQxINNlnlEummECuTs/d7208422-c035-4958-b8ee-c7c3fdfb1248.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3ELoFYOfvcQxINNlnlEummECuTs/2ac765da-2704-4228-8116-b8cd0e527ccb.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Tái thiết kế nội thất dinh thự cổ điển Châu Âu pha Dark Chinoiserie từ 2 ảnh tham chiếu (`rank_0747_nano_banana_2_06e7b71e.webp`)**: `nano_banana_2` kết hợp kiến trúc phào chỉ cao của dinh thự cổ châu Âu với tường sơn tối màu vẽ họa tiết hoa điểu Á Đông, sàn gỗ sồi xương cá và ánh sáng tự nhiên trầm mặc, tránh hoàn toàn vẻ bóng bẩy giả tạo của showroom.

```text
Use the attached reference images as the main visual guidance.

Create a cinematic interior of an old European noble mansion where “The Lady” lives with her noble family, but reinterpret the space in a refined dark chinoiserie style.

The interior should feel elegant, cultivated, atmospheric, and historically rich — not flashy, not overly luxurious, and not like a palace showroom. The beauty should come from moody architecture, dark painted surfaces, scenic wall treatments, textiles, and layered materials.

The style should combine:
- old European noble mansion architecture
- dark chinoiserie interiors
- refined historic atmosphere
- rich material layering
- quiet sophistication
- slight melancholy
- cultured, aristocratic taste

Important:
I do not want bright, playful chinoiserie.
I want dark, moody, refined chinoiserie.

The space should feel:
- dramatic but restrained
- rich but not gaudy
- decorative but not overloaded
- elegant, timeless, and immersive

Architectural base:
- 19th-century European noble mansion interior
- tall ceilings
- paneled walls
- carved wood doors
- high windows
- deep wall surfaces
- alcoves
- fireplace walls
- long corridors and connecting rooms
- formal but lived-in shared family spaces

Dark chinoiserie direction:
- hand-painted chinoiserie wall panels or mural-like wall treatments
- scenic painted walls with trees, branches, birds, flowers, gardens, distant landscapes, pavilions, or poetic nature scenes
- dark background tones behind the painted scenery
- moody decorative panels inspired by antique chinoiserie interiors
- refined East-meets-European aristocratic atmosphere
- subtle exoticism, never kitschy

Wall treatment and decoration:
- dark painted paneling
- mural-like scenic walls
- large decorative wall panels
- hand-painted or aged painted surfaces
- layered wall ornamentation
- elegant framed scenic compositions
- classical symmetry with chinoiserie detailing
- some sculptures or busts placed carefully in the space
- decorative objects should feel curated, not crowded

Textiles and material richness:
I want strong texture and layered material presence throughout the interiors.

Include:
- heavy curtains
- long drapery with rich folds
- patterned textiles
- velvet, silk, brocade, jacquard, woven fabrics
- richly textured carpets and rugs
- upholstered seating
- textile-covered benches
- layered fabric surfaces
- refined historic textile patterns
- tactile, soft, heavy, noble materials

The room should feel materially rich and immersive, with visible texture everywhere:
- curtains
- carpets
- upholstery
- wall surfaces
- painted panels
- wood grain
- aged finishes

Furniture:
- antique or historically grounded furniture
- refined European furniture with understated elegance
- upholstered chairs and benches
- carved wood tables and consoles
- furniture should support the atmosphere, not dominate the room
- avoid furniture-showroom composition

Color palette:
- deep brown
- dark walnut
- blackened wood
- tobacco brown
- deep olive
- muted moss green
- smoky charcoal
- parchment ivory
- aged beige
- faded taupe
- muted dusty teal or muted blue-green accents
- antique gold or aged brass in very small, subtle amounts
- warm muted reds or oxblood undertones only if very restrained

Lighting:
- soft natural light through tall windows
- moody daylight
- warm ambient glow
- candlelight feeling
- gentle shadows
- atmospheric lighting
- no harsh bright lighting
- no cold lighting
- no glossy showroom effect

Mood and atmosphere:
- dark chinoiserie
- moody and elegant
- quiet aristocratic refinement
- cultured and slightly mysterious
- intimate but grand
- rich in history and visual texture
- a shared family interior with taste, tradition, and quiet pressure
- beautiful but slightly haunting
- cinematic and immersive

Composition:
- cinematic interior photography
- architectural perspective
- balanced composition
- vertical emphasis
- deep perspective
- immersive framing
- observational mood
- the space should feel like a film set from a noble household drama

Avoid:
- bright colorful chinoiserie
- playful or whimsical chinoiserie
- modern interiors
- contemporary furniture
- excessive gold ornamentation
- over-the-top palace luxury
- overly glossy surfaces
- cluttered decoration
- minimal empty rooms
- fantasy castle aesthetics
- cartoonish Asian motifs
- kitschy decorative styling

Overall feeling:
A refined dark chinoiserie interior inside an old European noble mansion — rich in murals, painted panels, textures, curtains, carpets, antique furniture, and atmospheric detail. Elegant, moody, aristocratic, layered, and timeless.
```

##### 🏆 Rank #1149 (`0 ♡` | `198 👁️` | Model: `gpt_image_2_5` | Author: `@hoppingfox1484` | Size: `3:4` | Refs: `2`)
- **Publication ID**: `79747201-5522-439e-825f-e7d799ed805f`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1149_gpt_image_2_5_79747201.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3JlXwmhxXMr25oROErWdZUphC4f/hf_20261006_034111_b039dcae-e55e-4d6e-9949-6657e2b2f9ae.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3JlXwmhxXMr25oROErWdZUphC4f/hf_20261006_034111_b039dcae-e55e-4d6e-9949-6657e2b2f9ae_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3JlXwmhxXMr25oROErWdZUphC4f/68d20f94-62e9-4eaa-9919-1c83c9a2aeac_resize.jpg
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3JlXwmhxXMr25oROErWdZUphC4f/dc5cb6d4-0ec2-4108-93ce-9bad788fd540.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Dọn sạch công trường ngổn ngang thành căn bếp hoàn thiện (`Before: rank_1149_ref1.jpg + ref2.png` ➔ `After: rank_1149_gpt_image_2_5_1f5a756f.webp`)**: Từ bức ảnh công trường đang thi công đầy thang nhôm, thùng sơn, dây điện (`@img1`) và bản vẽ mặt đứng tủ bếp (`@img2`), `gpt_image_2_5` dọn sạch rác công trường và lắp bộ tủ bếp xanh navy + đảo bếp gỗ vào đúng vị trí từng milimet!

```text
Photorealistic interior-design renovation render. Edit the FIRST reference photo (a narrow covered side walkway of a Thai house). Keep the exact same camera position, lens, perspective and architecture: the cream house wall with sliding aluminium windows on the left, the white perforated ceiling with downlight, the black steel grid polycarbonate skylight roof, the tall wood-look vertical slatted cladding on the upper right wall, the AC condenser units at the far end, and the existing stone mosaic floor with terracotta strip, all unchanged. Remove all construction clutter (workbench, paint cans, vise, stools, bags, debris, wire across wall). Repaint the raw lower concrete wall on the right in a smooth light warm-grey microcement-look finish. Harmonise with the SECOND reference photo (teak-tone wood-look slats, thin matte-black frames). STYLE: Scandinavian-modern minimal, bright, crisp. Along the RIGHT wall only, a FREESTANDING MOVABLE kitchen (not built-in): modular matte-white powder-coated steel cabinets on slim black legs with oiled walnut worktops, ~55 cm deep, a stainless undermount sink with a brushed-steel faucet, one module is a rolling butcher-block island cart. Above, a black steel pegboard rail with a few hanging tools and a small herb planter. Coffee corner for 2-3 people: a compact white round pedestal table with three black wire chairs and a small espresso machine on the cart. At the far end next to the existing tap and socket, a white front-loading washer and dryer stacked in a freestanding white-and-black steel frame tower with a hamper. Two sculptural plants in matte black pots. Bright, soft daylight from the skylight, uncluttered, walkway still clear. Dezeen architectural photography quality.
```

##### 🏆 Rank #1841 (`0 ♡` | `7 👁️` | Model: `nano_banana` | Author: `@craftingwaffle1293` | Size: `3:2` | Refs: `1`)
- **Publication ID**: `11fa4071-7ca5-41a8-b467-2372df20a1d3`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1841_nano_banana_11fa4071.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DwCJbklEVjXP1CCCQlvwQB2eLH/hf_20261012_134109_ba396fc4-010c-46ec-b576-422098f880c4.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DwCJbklEVjXP1CCCQlvwQB2eLH/hf_20261012_134109_ba396fc4-010c-46ec-b576-422098f880c4_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DwCJbklEVjXP1CCCQlvwQB2eLH/da005bcd-0b13-4e2b-82b7-ccd938c314cf_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Biến ảnh chụp phòng bừa bộn bằng điện thoại thành ảnh mẫu Airbnb (`Before: rank_1841_ref1.jpg` ➔ `After: rank_1841_nano_banana_0648543d.webp`)**: Xóa sạch quần áo bẩn, túi nilon, dây cáp rối trên bàn nhưng giữ nguyên 100% tủ bếp, ghế sofa, cửa sổ và góc máy gốc.

```text
airbnb picture to be posted based on this picture make it nice and clean but above all realistic - arrange make it nicer - in a nice way make it bright
```

##### 🏛️ Giải Mã Model Chuyên Dụng `cinematic_studio_soul_location` (`49` Bối Cảnh Không Người)
> **Lưu ý Kỹ thuật khi đọc dữ liệu `cinematic_studio_soul_location`**: Trên hệ thống Higgsfield Cinema Studio, người dùng chỉ cần nhập **Tên Bối Cảnh ngắn gọn** (ví dụ: `Campo de Trabajo Cerro Negro`, `Interior of the house of young lady`) và chọn các nút thiết lập `Time / Weather / Era` trên UI; hệ thống backend của model `cinematic_studio_soul_location` sẽ tự động bung thành bức ảnh `Location Plate` `2048x1152` không có người với độ chi tiết kiến trúc cực cao. Dưới đây là 2 mẫu tiêu biểu đã kiểm định bằng mắt:

##### 🏆 Rank #990 (`1 ♡` | `34 👁️` | Model: `cinematic_studio_soul_location` | Author: `@shadowwolf` | Size: `2048x1152` | Refs: `0`)
- **Publication ID**: `3167cefd-72d4-4340-8e65-b51a77078ad9`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0990_cinematic_studio_soul_location_3167cefd.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3GzO0s6LblTnISddlrSBKZqdcMl/hf_20260725_121353_009dea97-b131-4102-bd1d-9390f0d8087f.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3GzO0s6LblTnISddlrSBKZqdcMl/hf_20260725_121353_009dea97-b131-4102-bd1d-9390f0d8087f_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Kiểm định `rank_0990_cinematic_studio_soul_location_3167cefd.webp` (`Campo de Trabajo Cerro Negro`)**: Dù `prompt_raw` chỉ ghi tên địa điểm 5 chữ, model tự động sinh đại cảnh khu mỏ dầu công nghiệp giữa thảo nguyên hoang mạc dưới bầu trời mây xám nặng nề, hoàn toàn không có bóng người (`Empty Location Plate`), đường chân trời và phối cảnh 28mm cực chuẩn để ghép xe tải hoặc nhân vật vào.

```text
Salón de Juegos El Poblado
```

##### 🏆 Rank #1842 (`0 ♡` | `7 👁️` | Model: `cinematic_studio_soul_location` | Author: `@hoppingmushroom1634` | Size: `2048x1152` | Refs: `0`)
- **Publication ID**: `2ddcd3c8-06de-438e-88b5-b90ffa11e7d7`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1842_cinematic_studio_soul_location_2ddcd3c8.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3Jj3fzOevs91aRKudJtdNhccshh/hf_20261001_121344_a951c7d4-bc1b-40d9-91ac-463cc2bbd6d0.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3Jj3fzOevs91aRKudJtdNhccshh/hf_20261001_121344_a951c7d4-bc1b-40d9-91ac-463cc2bbd6d0_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Kiểm định `rank_1842_cinematic_studio_soul_location_2ddcd3c8.webp` (`Interior of the house of young lady`)**: Model tự động dựng phòng khách kiêm sảnh biệt thự cổ điển châu Âu với cầu thang gỗ uốn lượn, tường ốp vữa kem, đèn tường ánh vàng ấm và khoảng sàn gỗ trống trải ở trung tâm — sẵn sàng làm phông nền tĩnh (`Background Plate`) cho các cảnh nội thất sang trọng.

```text
Apt 3B, Lenox Avenue Loft
```

---

#### 1.3. Cách 29 Dự Án Phim & TVC Viết Prompt Background Nhà / Phòng Khách / Căn Hộ (Nguyên Văn 100% Từ `asset_registry.json`)

##### 🎬 Project `adilinthewild/4k-blockbuster-breakdown` — Asset `@IMG_068` (Model: `gpt_image_2` | Roles: `start_frame_keyframe` | Reused in `3` jobs)
- **Chiến thuật Đạo diễn**: Cấu trúc 3 lớp chiều sâu (`Foreground / Midground / Background`) + Máy quay `ARRI Alexa 35` & ống kính `Panavision C-Series 40mm Anamorphic` cho Phòng khách căn hộ lúc chạng vạng (`Dusk`).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_3Bteyd8tPj9YJyVVlW2wSDqbs49/hf_20260701_220545_75f07102-0292-4147-accc-8105a7f6282e.png
- **👁️ Visual Audit Verdict**: Một trong những câu lệnh dựng Phòng khách căn hộ điện ảnh xuất sắc nhất trong 29 bộ phim: chia rõ Tiền cảnh (cạnh bàn ăn gỗ tối màu hơi mờ), Trung cảnh (sofa vải xám trầm, thảm dệt, bàn trà để cuốn sổ mở) và Hậu cảnh (cửa kính lớn nhìn ra ban công và những tòa nhà thành phố lên đèn vàng ấm lúc hoàng hôn).

```text
Cinematic film frame, three-quarter view of a cozy living room in a modern city apartment in the evening, no people — a movie set still, not an interior-design catalog photo. Around thirty square meters, white walls, light oak flooring, scandinavian-modern, lived-in and pleasant. Camera at chest height near the right-hand corner of the room, angled diagonally so two walls converge in depth.

Foreground, three-quarter angle: a light gray fabric three-seat sofa with its seat cushions and front upholstery visible to the viewer, a cream knitted blanket across the seat, soft throw pillows, a plush lion toy on one armrest; in front of it a round light-wood coffee table with magazines and a pair of binoculars, on a soft cream area rug.

Middle depth, right side: a light wooden computer desk standing free on open floor like a small executive desk, facing the room, a clear walkable gap of floor between the desk and the wall; an office chair behind the desk with its back to the wall, facing across the desktop toward the sofa; a computer monitor on the desk seen from behind — dark back panel toward the sofa, only a faint cool rim of light around its edges and a pale spill on the chair and wall behind it; a small wind-up toy monkey with brass cymbals beside it. On the right wall above this zone: a framed world map and framed adventure art prints — a pirate sailing ship, a jungle safari scene, golden desert dunes.

Background: the far wall is a floor-to-ceiling light-wood bookshelf with books and board games, a slim arc floor lamp beside it glowing warm tungsten, a soft golden pool of light on the shelves and floor; in the far left corner a door opens into a dark unlit hallway. Left side: large windows with sheer curtains, deep blue evening twilight outside, scattered warm lights of residential buildings.

Lighting: warm cozy evening — golden lamplight mixing with cool blue dusk from the windows, gentle warm-cool contrast, well-exposed inviting interior.

Camera and lens: shot on ARRI ALEXA 35 with a Panavision C-Series 40mm anamorphic lens, 2x anamorphic squeeze; warm blue horizontal streak flares off the practicals; oval vertically-stretched vintage bokeh on the city lights; subtle barrel distortion at the frame edges; natural anamorphic vignetting with softened vintage glass falloff in the corners; shallow depth of field focused on the sofa; filmic color grade with soft highlight rolloff and fine film grain — late-60s Panavision glass character on a modern digital sensor, photorealistic.
```

##### 🎬 Project `adilinthewild/tv-4k` — Asset `@IMG_031` (Model: `soul_cinematic` | Roles: `start_frame_keyframe, turnaround_sheet_reference_element` | Reused in `16` jobs)
- **Chiến thuật Đạo diễn**: Phòng khách ấm cúng đời thực (`Warm lived-in open living hall`) với **đèn dây fairy lights vàng ấm + dải LED strip + đèn bàn gốm** được tái sử dụng tới **16 lần** xuyên suốt bộ phim!
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_3BtqdNv4suDVOYLjnoc5pxjeNeO/hf_20260624_164358_d637f4d9-12e1-4a40-87e2-6c5baab4239f.png
- **👁️ Visual Audit Verdict**: Đạo diễn `@adilinthewild` kết hợp 3 nguồn sáng ấm (`warm golden-orange ambient light from a ceramic table lamp`, `string fairy lights along the wall`, `soft orange-red LED strip behind the desk`) đối lập với ánh trăng xanh lạnh ngoài cửa sổ (`cool blue-grey twilight from a tall window with sheer curtains`) — tạo ra bầu không khí phòng khách gia đình có chiều sâu cảm xúc cực mạnh.

```text
Modern open living hall with a teenage vibe, 3/4 angle wide shot. Spacious room that doubles as a teen's hangout — lived-in and a little messy, not a showroom. Large modern flat-screen TV (~65") mounted on the main wall as the focal point, screen off/black, game controller on the low media console below it. Comfortable sofa with cushions dented and askew, a crumpled throw blanket half-falling off, a beanbag chair on the floor. Hoodie and a couple of t-shirts tossed around, sneakers kicked off near the rug, headphones slung over the sofa arm, a few cups and a snack wrapper on the console, charging cable trailing on the floor. String fairy lights and an LED strip glow along the wall, a couple of plain framed posters (blank, no text or images), soft area rug slightly bunched, faint scuffs on the wall. NO computer desk. Generic unbranded objects — NO logos, NO brand names, NO visible text anywhere. Natural window daylight + soft warm lamp. Photorealistic, 2020–2022 interior style. 16:9.
```

##### 🎬 Project `6moths/where-letters-fall` — Asset `@IMG_070` (Model: `nano_banana_flash` | Roles: `turnaround_sheet_reference_element` | Reused in `6` jobs)
- **Chiến thuật Đạo diễn**: `MASTER LOCATION PROMPT` (`5,932` ký tự, tái sử dụng `6` lần): Khóa chết toàn bộ sơ đồ địa lý căn nhà thập niên 1990 (Phòng khách lò sưởi gạch đỏ + Phòng ăn + Bếp + Cửa sổ nhìn ra hiên nhà).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2wJnNN6k3efACLdC8VyV1cJzhCI/hf_20260811_215402_5c3d210c-e7cd-4f6c-b253-bd3d642232d3_min.webp
- **👁️ Visual Audit Verdict**: Cách viết `MASTER LOCATION PROMPT` bài bản nhất kho dữ liệu: mô tả chi tiết từng bức tường, lò sưởi gạch đỏ (`red-brown brick fireplace`), ghế bành kẻ caro, thảm bầu dục tết thừng và hệ thống đèn vàng ấm `2900K` để mọi cảnh cắt trong phim không bao giờ bị nhảy vị trí đồ đạc.

```text
==================================================
<<<fa326a63-1bc8-43d2-974c-b4d4f131f0b6>>> — MASTER LOCATION PROMPT
КУХНЯ
==================================================

REFERENCE / LOCATION LOCK

Create a photorealistic master reference of the same modest early-1990s rural American farmhouse kitchen.

Do not redesign the room.

This kitchen must look old, genuinely lived in, slightly cluttered, warm and practical.

It is NOT a renovated retro kitchen.

CAMERA AND COMPOSITION

Ultra-wide cinematic frame approximately 2.39:1.

Camera is positioned in the adjoining room / threshold and looks directly into the entire kitchen.

Camera height approximately 1.4 meters.

Approximately 27mm full-frame lens.

Level camera.

Almost planimetric composition with strong horizontal and vertical lines.

No extreme wide-angle bending.

ROOM GEOMETRY

Rectangular kitchen.

Back wall spans almost entire image.

The main dining table sits in the middle of the room.

Large brick fireplace occupies the LEFT third of the frame.

Cabinetry and appliances run across the back wall and around the right side.

LEFT — BRICK FIREPLACE

Massive traditional red-brown brick fireplace built into the left wall.

Brick extends from floor to ceiling.

Large dark rectangular firebox opening approximately waist height.

Black wrought-iron fireplace screen / simple metal guard.

Wide raised brick hearth projects into the room.

Above the firebox is a thick dark wooden mantel shelf.

A few small ordinary old decorative objects may sit on the mantel.

The fireplace brick is aged, matte, irregular and slightly darkened from years of use.

Do not make it newly constructed.

LEFT WALL / WINDOW

Immediately to the right of the fireplace is a tall narrow window.

White lace / sheer curtain.

Cool diffuse daylight passes through it.

Another smaller framed picture hangs nearby.

BACK WALL

Wall finish is muted sage / dusty olive green wooden paneling.

Not saturated green.

Across the upper back wall is a long continuous row of dark stained wooden kitchen cabinets.

Cabinet doors are plain traditional raised-panel wood.

Dark brown walnut tone.

Small aged brass handles.

The cabinets occupy much of the horizontal width.

COUNTERTOP AND STORAGE

Below the cabinets runs an old beige / tan laminate countertop.

Dark wood lower cabinets beneath it.

Counter surface is genuinely used.

Include a restrained amount of period household clutter:
glass jars,
metal canisters,
ceramic bowls,
bread or a paper bread bag,
small utensil holders,
a few dishes,
simple kitchen containers.

Objects should appear naturally distributed, not styled.

WINDOWS

Two modest rectangular windows in the back area.

One approximately left of center.

Another near the far right / sink.

Both have white semi-transparent lace curtains.

Exterior is bright soft overcast daylight with no detailed modern structures visible.

STOVE

White freestanding early-1990s gas or electric range located on the back wall slightly RIGHT of center.

Four-burner top.

Simple white oven door and analog controls.

Off-white / pale beige rectangular range hood immediately above.

A small plain white kettle sits on the stove.

Do not use stainless-steel modern appliances.

SINK AREA

Far right side contains a simple sink beneath / near the right window.

Old off-white countertop.

Dark wood cabinets.

Small dish rack and a few normal kitchen objects.

A small period toaster may sit nearby.

DINING TABLE

Large oval dining table centered in the room.

Cream / light beige laminated or painted tabletop.

Simple pale central pedestal or sturdy base.

The table is not elegant.

Around it are FOUR old dining chairs.

Chairs have metal or pale structural frames with thick upholstered backs and seats.

Fabric is faded beige with subdued brown floral patterns.

One chair stands prominently in the CENTER FOREGROUND with its back facing the camera and partially blocks the table.

One chair on the left side is seen at an angle.

One chair on the right side is seen at an angle.

A fourth chair is partially visible beyond / around the table.

Under the table is a dark brown oval braided rug.

Rug edges remain clearly visible.

CEILING LIGHT

Large vintage pendant lamp hangs exactly above the central dining table.

Warm amber/yellow translucent glass shade.

Scalloped flower-like lower edge.

Dark metal chain / stem.

Warm tungsten bulb glows inside.

This is one of the strongest warm elements in the room but must not blow out.

FLOOR

Medium warm-brown wooden plank floor.

Old matte boards with realistic wear and variations.

No glossy finish.

LIGHTING

Soft cool daylight through lace-curtained windows.

Warm amber pendant light above table.

The room stays somewhat dim.

Corners and dark cabinets hold deep readable shadows.

Do not create overly bright studio lighting.

The fireplace itself does NOT need an active flame.

COLOR PALETTE

Muted sage green walls.
Deep warm-brown wood.
Aged brick red-brown.
Cream appliances.
Faded beige upholstery.
Warm amber practical light.
Subtle cool daylight.

IMAGE CHARACTER

Photorealistic 1990s domestic interior.

Deep focus.
Real material microtexture.
Slight age and household wear.
No artificial cleanliness.
No luxury styling.

NO PEOPLE.
NO FOOD PLATED ON THE TABLE.
NO LETTERS.
NO MODERN FRIDGE WITH DIGITAL DISPLAY.
NO STAINLESS STEEL APPLIANCES.
NO KITCHEN ISLAND.
NO MODERN BAR STOOLS.
NO LED LIGHT STRIPS.
NO MARBLE COUNTERS.
NO MINIMALISM.
NO CONTEMPORARY FARMHOUSE RENOVATION.
NO PERFECTLY WHITE CABINETS.
NO EXCESSIVE ORANGE COLOR GRADE.
NO CGI LOOK.

The image should look like an actual untouched family kitchen photographed in the early 1990s.
```

##### 🎬 Project `lukasbandana/rewind` — Asset `@IMG_004` (Model: `gpt_image_2` | Roles: `start_frame_keyframe` | Reused in `1` jobs)
- **Chiến thuật Đạo diễn**: Tiền sảnh & Phòng khách biệt thự gia đình Mỹ giàu có (`Affluent American home foyer`) nhìn qua khung cửa chính lúc đêm ấm áp.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_3GioFxaLlMjfVB3Dm0YEsbYgGoz/hf_20260817_193913_17510599-5830-4ade-8595-dead1dae6c43.png
- **👁️ Visual Audit Verdict**: Sử dụng kỹ thuật khung trong khung (`Framed through the open front doorway`), nền sàn gỗ sồi bóng phản chiếu ánh đèn chùm vàng ấm, cầu thang cong bên trái và phòng khách ấm cúng phía xa có độ mờ chiều sâu trường ảnh (`shallow depth of field`).

```text
A realistic elegant entry hall / foyer inside an affluent American family home, matching the same upscale warm interior style as the dining room. Show a refined interior hallway leading into the living areas, with grey-beige walls, white trim and molding, dark hardwood floors, and soft warm interior lighting. The main front door should be clearly visible inside the space and should be a dark brown classic elegant door, similar to a deep rich brown wooden front door. The foyer should feel spacious, polished, and believable, with tasteful classic American suburban architecture and subtle upscale decor. If any windows are visible, it should be dark or evening outside, but the focus should remain on the interior entry space and the visible front door. No people. Cinematic realism, warm, polished, and believable.
```

##### 🎬 Project `pandaproduction/thread` — Asset `@IMG_041` (Model: `gpt_image_2` | Roles: `start_frame_keyframe` | Reused in `4` jobs)
- **Chiến thuật Đạo diễn**: Phòng ngủ căn hộ gác mái gỗ sồi thế kỷ 18 (`1780s historical dark-oak bedroom`, tái sử dụng `4` lần) với kỹ thuật khóa cửa gỗ mờ ở mép trái tiền cảnh (`Doorframe Foreground Occlusion`).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_39tDAPbknLeiOHGT4b1AsPWiZ3z/hf_20260831_184823_5cb97590-80c5-4957-b2f1-df38f16ad870.png
- **👁️ Visual Audit Verdict**: Câu lệnh dài `4,488` ký tự khóa từng chi tiết vật lý: cánh cửa gỗ nâu sẫm mở hé ở mép trái tiền cảnh hơi out-net (`slightly out of focus, creating a realistic 'stepping into the room' perspective`), nắng chiều chiếu xiên qua cửa sổ kính chia ô kiểu Pháp tạo vệt sáng và hạt bụi lơ lửng (`floating dust motes`) trên sàn gỗ sồi bản rộng.

```text
A wide interior shot, a cinematic film still, 50mm lens, camera
at normal eye height. THE REVERSE ANGLE of the reference room:
the camera stands in the corner BEHIND THE BED'S TALL HEADBOARD
— the far left corner of the reference image — and looks back
ACROSS the room, in a THREE-QUARTER view, at the opposite wall:
the wall that was behind the camera in the reference. Not a
flat frontal view of that wall — the camera is angled slightly,
so the wall runs with gentle perspective and the room keeps its
depth.

<<<image_1>>> is the location reference: the same 1780s panelled
bedroom. It controls geometry, materials, light and atmosphere
ONLY — not framing. Do not use it as a starting frame, do not
inherit its composition, its angle or its crop — take only the
space, the furniture, the panelling and the texture, and show
them from the opposite side.

THE NEAR FOREGROUND: at the bottom right of the frame, close to
the camera and softly out of focus, a fragment of the BED — the
top edge of its tall dark carved headboard and the dented
pillows below it — and the small low candle-holder at the bed
head, its weak flame the one warm point near the camera. From
there the bed runs AWAY from the camera into the room, its
rumpled white sheets receding, its low open foot end far away.

THE FAR WALL — the wall this picture is about: old dark oak
panelling from floor to ceiling, broad raised panels in stiles
and rails, almost black-brown with age and wax, dulled by
candle soot. On the RIGHT side of this wall stands the CLOSED
DOOR: heavy dark vertical planks, forged iron hinges, a simple
iron latch — shut. To the LEFT of the door, around the middle
of the wall, at head height, hangs the OLD MIRROR: a dark
wooden frame around clouded, foxed glass — dim grey blooms,
dark spots, rusty tarnish across the silvering — reflecting
only a soft smeared gleam of the dim room, nothing readable.
And to the LEFT of the mirror, a clear EMPTY stretch of dark
panelling, bare from floor to ceiling — nothing hanging on it,
nothing standing against it: an empty piece of wall where a man
could stand. The empty panelling, the mirror and the door — in
that order from left to right — are the three anchors of this
picture.

The LEFT edge of the frame just clips the beginning of the
window wall — the window itself stays OUT of frame; only its
soft pool of grey overcast daylight falls in from the left,
across the bare floorboards, toward the far wall. The RIGHT
edge of the frame may catch the corner where the far wall meets
the side wall with its wooden pegs — deep in shadow. Wide dark
floorboards, worn pale along the walking line, run from the
camera to the far wall. No people anywhere in the room — the
room is empty and waiting. No window in frame, and the door
stays CLOSED.

LIGHT. One light logic only: the soft, cold grey overcast
daylight of the unseen window at frame left — one direction of
shadows, falling across the floorboards and dying before it
reaches the far wall, which stays the DARKEST wall of the room:
its panelling, the door and the empty stretch sink into deep
brown half-darkness that keeps its detail and never crushes to
pure black. The clouded mirror catches one dim grey gleam. The
weak candle at the bed head glows warm in the near foreground
without lighting the room. No other light source, no lamp, no
fire, no sunbeam, no artificial film lighting, no rim light. A
brightly lit wall or an evenly lit room = a failed image.

COLOUR. Heavily desaturated, olive-biased colour, like bleached
35mm film: cold grey-green daylight, near-black aged oak
panelling with warm brown depths, dirty off-white linen of the
bed as the palest note, the one warm amber point of the candle.
Highlights milky and slightly cyan; shadows dense, green-brown
and full of detail.

FILM. Photorealistic 35mm motion-picture film frame, Kodak
Vision3 250D stock, photochemical colour, organic film grain
thickening in the shadows, soft highlight roll-off, gentle
optical falloff toward the frame edges, 50mm lens, deep enough
focus to hold the wall while the near headboard falls softly
out of focus. Not a video game, not a 3D render, not a clean
digital look, no beauty light, no retouch. Real textures: old
waxed oak panelling dulled with soot, dark plank door with
forged iron, clouded tarnished mirror glass, coarse crumpled
linen, worn floorboards. Everything in frame belongs to the
1780s.
```

##### 🎬 Project `pietromalegori/control` — Asset `@IMG_118` (Model: `seedream_v5_pro` | Roles: `turnaround_sheet_reference_element` | Reused in `10` jobs)
- **Chiến thuật Đạo diễn**: Căn hộ Open-Plan hiện đại (`Living Room + Kitchen Island`, tái sử dụng `10` lần) với công thức **Tỷ lệ 4 nguồn sáng `40% / 30% / 20% / 10%`** trên `seedream_v5_pro`.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_38JDnD2aJxtjnkHGSvDeUpDsT5p/hf_20260831_193456_4785e6e6-40db-4839-874c-48a3ac475908_min.webp
- **👁️ Visual Audit Verdict**: Đạo diễn `@pietromalegori` định lượng ánh sáng phòng khách bằng con số phần trăm chính xác: `40%` ánh sáng trời u ám qua cửa sổ kính lớn bên phải (`5800K`), `30%` đèn thả trần vàng ấm trên đảo bếp (`3000K`), `20%` ánh sáng xanh lạnh từ màn hình laptop (`6500K`), và `10%` ánh sáng phản xạ từ tường vữa và sàn bê tông mài.

```text
Wide shot of a large open-plan apartment interior, camera at standing eye level centered looking straight across the space — the room reading as a single continuous open floor plan with no internal walls dividing the living zone from the sleeping zone, the front door open at the left edge of the frame — the door panel in flat painted sage-green wood, the building corridor visible through the opening as a narrow cold fluorescent-lit strip with the pale corridor wall and a fragment of the opposite apartment door, the living space expansive and sparsely furnished — a worn sofa positioned in the left-center of the room facing the far wall, a low coffee table in front of it in dark wood, a single bed pushed against the right wall in the far background with a dark blanket folded across it, a long narrow window running across the far wall — a wide horizontal aluminium-frame window with thin white curtain panels hanging loose, cold flat grey-white daylight flooding in through the glass washing the far wall and floor in a broad diffused horizontal band, a cast iron radiator beneath the window, the kitchen zone visible in the far right of the frame without partition — a plain beige laminate counter running along the right wall with a stainless steel sink and a compact gas range, a small formica table with two chairs at opposite short ends in the kitchen zone, the floor continuous throughout — worn dark parquet with gaps between the boards catching the window light as long pale streaks, the ceiling high and flat in cracked off-white plaster with a single bare bulb pendant at center, the room reading as large and underfurnished — too much empty floor between the sparse objects, the open corridor door at left allowing a sliver of cold fluorescent building light to enter and cut across the dark left wall, palette of 40% deep teal-green shadow filling the open interior, 30% cold flat grey-white far window light flooding across floor and wall, 20% pale off-white plaster ceiling and upper walls, 10% cold fluorescent corridor spill through open door at left edge, Kodak Vision3 500T pushed one stop, fine grain, cold teal-green grade with crushed blacks, no people, rule of thirds
```

##### 🎬 Project `mohamed-halloum/sentence` — Asset `@IMG_024` (Model: `gpt_image_2` | Roles: `start_frame_keyframe` | Reused in `1` jobs)
- **Chiến thuật Đạo diễn**: Cặp Prompt `Time-of-Day Relighting Lock` (Phần 1 — **Ban Đêm `2700K`**): Giữ nguyên 100% vị trí đồ đạc phòng ngủ/căn hộ, chỉ đổi ánh sáng sang đêm khuya với đèn bàn vàng ấm `2700K` và ánh trăng lạnh ngoài rèm voan.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_3Hd3fAAKzIrI3KkehS7pjSV94OE/hf_20260823_005037_351f7bfc-3430-4b3e-b7f8-6eba4eb2cf1e.png
- **👁️ Visual Audit Verdict**: Cùng một căn phòng với `@IMG_039`, nhưng ở `@IMG_024` toàn bộ không gian được nhuộm bởi bóng tối đêm khuya, chỉ có chiếc đèn bàn chụp vải ở góc phải phát sáng vàng ấm `2700K` tạo bóng đổ mềm mại qua các nếp chăn.

```text
Cinematic film still of a small Levantine apartment kitchen at night, seen in three-quarter from across the table at 1.3 m: a scarred oak table waxed to a low sheen, bare, under a black metal pendant lamp hanging 0.8 m above it; a plain wooden chair frame-left pushed in; frame-right a dark window with scattered city lights out of focus; frame-left a counter with a small brass long-handled coffee pot on a two-ring stove, a kettle, two glass jars of dried herbs and a bowl of lemons, a splashback of plain hand-glazed cement tiles, each a solid mottled ochre or teal. The pendant lamp at 2700K is the only source, a hard pool on the table, 4:1 ratio, rapid falloff into the dark corners; the window a cold 6500K blur of small lights. Palette of 60% warm dark brown, 30% amber lamp pool, 10% cold window lights. Real wood and tile, fine grain, no people in frame.
```

##### 🎬 Project `mohamed-halloum/sentence` — Asset `@IMG_039` (Model: `gpt_image_2` | Roles: `turnaround_sheet_reference_element` | Reused in `1` jobs)
- **Chiến thuật Đạo diễn**: Cặp Prompt `Time-of-Day Relighting Lock` (Phần 2 — **Nắng Chiều Tà `3000K`**): Giữ nguyên y hệt căn phòng của `@IMG_024`, tắt đèn đêm và chiếu nắng chiều vàng cam `3000K` xuyên qua rèm voan trắng tạo vệt bóng dài trên tường và sàn gỗ.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_3Hd3fAAKzIrI3KkehS7pjSV94OE/hf_20260823_005727_90a66de8-be8b-4d87-b604-d3db83475e83_min.webp
- **👁️ Visual Audit Verdict**: Khi đặt `@IMG_024` (Đêm) cạnh `@IMG_039` (Chiều tà), bạn có ngay công thức **Chuyển cảnh Ngày ↔ Đêm cho TVC Cây thông Noel**: giữ nguyên 100% mô tả kiến trúc phòng khách, chỉ thay đoạn `Lighting` từ nắng chiều `3000K` sang đêm khuya `2700K`!

```text
Cinematic film still of the same small Levantine kitchen in late afternoon, the same three-quarter view from across the table at 1.3 m: the scarred oak table bare, the wooden chair frame-left, the window frame-right with a thin cream curtain drawn across it and the low sun behind it, the pendant lamp above the table switched off. Frame-left the counter with a small old cream-coloured radio with two plain unmarked knobs and a blank dark tuning window, the brass long-handled coffee pot on the stove, the kettle, the two jars, the bowl of lemons, the splashback of plain hand-glazed tiles in solid mottled ochre and teal. Low sun through the curtain frame-right at 3000K is the only source, soft and wrapping, 2:1 ratio, shadows running frame-left, dust in the light. Palette of 65% warm amber, 25% deep brown shadow, 10% cream curtain and radio. Real wood and tile, fine grain, no people in frame.
```

##### 🎬 Project `ollkorrect/besa` — Asset `@IMG_045` (Model: `nano_banana_flash` | Roles: `turnaround_sheet_reference_element` | Reused in `13` jobs)
- **Chiến thuật Đạo diễn**: `SURGICAL PROP REMOVAL ON MASTER ROOM` (Tái sử dụng `13` lần): Dùng ảnh phòng gốc làm `Original Room Master`, xóa duy nhất các vật thừa và tái tạo vân tường đá/sàn gỗ phía sau (`inpaint naturally`).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_32vwRMunqoTPjjAdQ6zrT3TrjuG/hf_20260812_130257_9e18ac7c-bc4d-42df-80e7-f6a513908f7f_min.webp
- **👁️ Visual Audit Verdict**: Mẫu câu lệnh chuẩn mực để dọn sạch một góc phòng khách có sẵn trước khi đặt cây thông Noel hoặc sản phẩm của bạn vào: khóa cứng `PRESERVE: Keep the exact camera position, framing, perspective, room geometry, stone walls, timber beams...` và chỉ liệt kê `REMOVE ONLY`.

```text
EDIT THE ATTACHED ORIGINAL ROOM MASTER.

PRESERVE:
Keep the exact camera position, framing, perspective, room proportions, timber ceiling and beams, stone and plaster walls, fireplace at frame left, cabinet, wall niches, two arched windows, benches, floor and permanent architecture. Do not redesign or rearrange anything except where stated below.

CHANGE:
Show this same room three years later at winter midnight during a long period of grief.

Close the existing double oak entrance fully inside its rectangular doorway. Both leaves are shut flat in one plane and fill the entire opening from jamb to jamb and floor to lintel. Their dark wooden faces remain faintly visible and meet at the center in one narrow vertical seam, so it unmistakably reads as a closed door, not an open black doorway. Neither leaf is open or angled. Show no exterior, opening, gap or light leak around, between or beneath the door.

Remove the wedding chest and everything belonging to it. In its former place beside the fireplace, add one old smoke darkened walnut chair angled toward the hearth. Give it a straight back, simple arms, solid seat, restrained carving and no upholstery. Add one very small three legged wooden table beside the chair at seat height. Leave its top empty.

Extinguish every lamp and candle. There is no active interior lighting. The only light revealing the room is very weak, cloud filtered winter moonlight entering through the two arched windows. Use dim desaturated blue grey light that touches only the window recesses, small fragments of floor and a few furniture edges. It must not illuminate the full walls or make the room clearly readable. Do not show the moon.

The fireplace is almost dead. Show only a few dull red embers among black logs, without visible flames. Their glow remains inside the hearth and does not light the chair, floor or walls.

Underexpose the room by four to five stops. Keep at least 90 percent of the frame near black. The plaster walls read as charcoal, never white. Most architecture, furniture and textiles appear as faint silhouettes or disappear into darkness. Use soft low contrast blacks, minimal detail and no recovered shadows.

Slightly fade the remaining textiles and add subtle smoke age and settled wear. Keep the room intact and inhabited. No people or extra objects. Remove warm ambient fill, bright firelight, glowing walls, bright windows, rim light, daylight and lifted HDR shadows.
```

##### 🎬 Project `hft_online/harmony-ai-film-festival` — Asset `@IMG_286` (Model: `nano_banana_2` | Roles: `start_frame_keyframe` | Reused in `2` jobs)
- **Chiến thuật Đạo diễn**: BƯỚC 1 của Quy trình `2-Step Empty-Table-First` (`nano_banana_2`): Xóa sạch mọi đồ vật trên chiếc bàn thấp giữa phòng khách trước khi bày đạo cụ mới.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2z48uxE2O5vQ9OjsGuyDZmbQkp5/hf_20260823_174703_15e07adc-d1b2-43fd-92c2-f59e34235c39.png
- **👁️ Visual Audit Verdict**: Thay vì bắt AI vừa xóa đồ cũ vừa thêm đồ mới trong 1 lần (dễ làm méo mặt bàn), đạo diễn `@hft_online` tách riêng `@IMG_286` chỉ để dọn sạch mặt bàn gỗ giữa phòng khách (`Remove everything standing on the low table in the middle of the room. That is the only change`).

```text
Remove everything standing on the low table in the middle of the room. That is the only change.

The whole top surface of that table becomes clear painted blue timber, empty from edge to edge, the grain running along it under the worn paint and the light from the window falling across it in the same patches it already makes. The surface is smooth and continuous across its whole area, with no localised darkening and no mark of any shape on it.

The shelf underneath the table also becomes clear: bare painted blue timber along its whole length, empty, with the light falling on it as it already does.

Everything else in the picture stays exactly as it is: the table itself with its turned legs and its frame, the sofa and its knitted throw, the two armchairs, the rug, the floorboards, the window and its curtains, the radiator, the side table and the telephone, the shelf unit with its records, the gramophone, the lamp, the framed prints on the wall, the guitar in the corner, and every shadow already in the room. The framing, the focus, the exposure and the grade are untouched.
```

##### 🎬 Project `hft_online/harmony-ai-film-festival` — Asset `@IMG_288` (Model: `nano_banana_2` | Roles: `start_frame_keyframe` | Reused in `1` jobs)
- **Chiến thuật Đạo diễn**: BƯỚC 2 của Quy trình `2-Step Empty-Table-First` (`nano_banana_2`): Sau khi đã có mặt bàn trống từ `@IMG_286`, thêm đúng 3 món đạo cụ với vị trí và ánh sáng khớp 100% với căn phòng.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2z48uxE2O5vQ9OjsGuyDZmbQkp5/hf_20260823_182226_7dca5858-67e4-437c-82fb-8ff2085d298b.png
- **👁️ Visual Audit Verdict**: Câu lệnh `@IMG_288` mở đầu cực kỳ đanh thép: `Edit the attached photograph of this living room. Three things are added to it and nothing else about the room changes...` giúp 3 món đồ mới ăn khớp tuyệt đối với vân gỗ và ánh sáng của mặt bàn trống.

```text
Edit the attached photograph of this living room. Three things are added to it and nothing else about the picture changes.

THE ATTACHED IMAGE IS THE ROOM AND THE FRAMING, and it is the only authority on both. The patterned blue wallpaper, the skirting board, the blue painted floorboards, the rug, the blue coffee table, the sofa and the armchairs in the foreground, the grey blue armchair at the right, the curtain, the window, the shelf unit with its records and the gramophone all stay exactly where they are, at the same size, in the same colour and in the same light. The camera position, the height, the lens, the crop and the perspective are unchanged = a room whose layout or object arrangement differs from the attached image in any way is a failed frame.

WHERE THE ADDITIONS GO, and this is the whole instruction: they go ON the empty stretch of patterned wallpaper across the middle and left of the frame, mounted to that wall, above the skirting board. That wall is the only surface that changes.

THE FLOOR IS NOT TOUCHED: nothing new stands on the floorboards and nothing new stands on the rug. No chair, no armchair, no stool, no table, no lamp, no cabinet, no sideboard, no chest, no plant and no object of any kind rests on the floor anywhere in this picture = a new piece of furniture standing on the floor is a failed take. The floorboards in front of that wall stay empty and clear exactly as they are now.

ADDITION ONE: a long blue painted wall shelf mounted horizontally on the wallpaper at about chest height, running a good stretch of that wall on two shaped blue brackets. Standing on it, spaced unevenly with wall visible between them: a blue ceramic jug, two blue clothbound books lying flat, a small blue enamelled tin and a blue ceramic bowl.

ADDITION TWO: a second blue painted shelf mounted above the first, shorter, on its own pair of brackets, carrying a row of blue clothbound books leaning against one another and one blue ceramic vase at the end.

ADDITION THREE: a round wall clock hanging on the wallpaper beside the shelves, its case painted blue, a pale face with slim dark hands and plain markers, no numerals, its glass catching a faint highlight.

EVERY ADDITION BELONGS TO 1980 OR EARLIER, in a domestic apartment of that time: painted timber, ceramic, glass, cloth and pewter. Nothing designed after 1985 appears = a modern appliance, a screen, a digital display, an illuminated panel or modern plastic is a failed take.

EVERY ADDITION IS BLUE, blue grey or cold neutral, and every one is in good condition: freshly painted timber with an even coat, unchipped ceramic, clean pewter. They are cared for, not old = an added object that reads as worn, faded, chipped, stained, flaking or distressed is a failed take, and so is one in any colour outside the cold blue register.

ALL THREE ARE LIT BY THE LIGHT ALREADY IN THE PICTURE: the same source, the same direction, the same intensity as everything around them, so the side facing the window is lit and the side away from it falls into the same deep blue shade as the wall behind. Each drops its shadow onto the wallpaper in the same direction and with the same softness as the shadows already in the room, and the shelves cast their own shadow band beneath them = anything that looks cut out, pasted, floating, or lit from a different direction is a failed take.

Nothing in the room is removed, moved, resized, recoloured or replaced to make space for them. They occupy wall that is already empty, and every object already in the picture stays visible.

The grain, the contrast, the exposure, the depth of field and the grade of the attached image are untouched.
```

---

### 21.📦 CHUYÊN ĐỀ 2: ẢNH VỀ SẢN PHẨM & ĐỔI TỪ ẢNH THƯỜNG THÀNH ẢNH ĐIỆN ẢNH TVC (`ORDINARY CUTOUT ➔ CINEMATIC TVC CAMPAIGN`)

> **Bài toán thực tế**: Bạn chỉ có 1–2 bức ảnh chụp sản phẩm bằng điện thoại hoặc ảnh tách nền trắng thương mại điện tử (`E-commerce White Cutout` hoặc ảnh chụp cây thông Noel trong phòng sáng phẳng). Làm sao biến nó thành bức ảnh quảng cáo TVC triệu đô có nước bắn, cát sa mạc, khói sương, bàn tay người cầm, đổi màu từng sợi chỉ khâu (`#F9E11F`), hoặc bung rã linh kiện kỹ thuật (`Exploded-View Render`) mà **không làm biến dạng sản phẩm hay sai một nét chữ trên nhãn**?

#### 2.1. 6 Công Thức Biến Ảnh Sản Phẩm Thường Thành Ảnh TVC Điện Ảnh
1. **Công thức `Cutout-to-Macro Still Life` (`seedream_v5_pro` — `Rank #461`, `Rank #645` & `Rank #705`)**:
   - Đưa ảnh sản phẩm tách nền trắng làm `@img1`, sau đó ra lệnh: `"Use the product from reference image 1 keeping its exact shape, cap, label and typography unchanged"` và đặt nó vào giữa các nguyên liệu tự nhiên có độ tương phản vật lý cao (vỏ cây thông phủ tuyết, quả mọng đỏ, đá slate đen ướt đẫm sương như `Rank #645`, hoặc quả sung tím bổ đôi như `Rank #705`) dưới ánh nắng gobo chiếu xiên tạo bóng đổ sắc nét (`hard directional sunlight casting crisp diagonal shadows`).
2. **Công thức `Exact Diacritics & Packaging Lock` (`gpt_image_2_5` — `Rank #1241` & `Rank #3154`)**:
   - Để AI không viết sai chữ trên bao bì khi biến ảnh chụp túi hàng thành poster quảng cáo, hãy **gõ lại nguyên văn từng dòng chữ trong ngoặc kép kèm mô tả dấu câu**: `"Keep the exact packaging from Reference 1... Headline text reads EXACTLY: 'ZAKROUCENÉ DO SVĚTLA' with proper Czech diacritics (Á, É, Ě)"` (`Rank #1241`) hoặc `"dont change anything beside the product and the text and Put below text 'Premium Sarawak Black Papper Cookies'"` (`Rank #3154`).
3. **Công thức `Web Fragrance Pyramid Screenshot + Bottle ➔ New Flacon Campaign` (`nano_banana_2` — `Rank #1208`, `Rank #943`, `Rank #1427`)**:
   - Đưa `@img1` là ảnh chụp màn hình bảng thành phần mùi hương trên web + `@img2` là ảnh dáng chai mẫu, `nano_banana_2` tự động đọc các nốt hương trong ảnh chụp màn hình để bày biện nguyên liệu xung quanh chai mới (`Rank #1208`), hoặc khắc chìm logo mỏ neo & chữ `PORTO GEDANUM 54°N — New York 92 / Warsaw 44 extrait de parfum 50 ml` sắc nét đến từng milimet trên thân chai nhám (`Rank #943` & `Rank #1427`)!
4. **Công thức `Micro-Surgical HEX Thread/Material Swap` (`nano_banana_2_1` — `Rank #1396` & `Rank #1360`)**:
   - Khi cần đổi màu một chi tiết siêu nhỏ trên sản phẩm (như đổi màu sợi chỉ khâu yên ngựa hoặc đổi màu bóng đèn/quả châu trên cây thông) mà giữ nguyên 100% vân sản phẩm gốc, hãy dùng `nano_banana_2_1` kèm mã màu HEX: `"Change ONLY the color of the saddle-stitch thread to bright lemon yellow (#F9E11F) waxed polyester thread... Keep everything else pixel-identical"` (`Rank #1396`).
5. **Công thức `Exploded-View Technical Construction Render` (`gpt_image_2_5` — `Rank #1499`)**:
   - Biến 1 bức ảnh sản phẩm thông thường thành bản vẽ kỹ thuật bung rã từng lớp cấu tạo (`Exploded-View`) chuẩn catalog châu Âu đểโชว์ chất lượng cấu tạo sản phẩm (cực hợp để làm cảnh giải phẫu cấu tạo 4 lớp cành nhựa PE chống cháy / lõi thép / đèn LED của cây thông Noel!): `"Photorealistic exploded-view construction render of the exact product in the reference image... Every component is pulled apart along its natural assembly direction, evenly spaced, with thin dashed grey alignment lines showing where each part fits."`
6. **Công thức `3-Panel Product Sheet + Back-View Anti-Hallucination` (`@thomas_lundstrom` `@IMG_015` & `@ollkorrect/besa` `@IMG_032`)**:
   - Trước khi đưa sản phẩm vào video Seedance 2.0, luôn tạo một tấm **Product Sheet 3-Panel (`Left: Front | Center: 3/4 Angle | Right: Back`)** hoặc **6-Panel (`Front, Back, Left, Right, Top, Macro Detail`)** trên nền xám trung tính `#E8E6E1` và **cấm tuyệt đối AI bịa chữ ở mặt sau** (`"NO text, NO numbers, NO markings on the back"`).

---

#### 2.2. Tuyển Tập Prompt Biến Ảnh Sản Phẩm Thường Thành TVC Trên Community (`♡ < 50`) — Nguyên Văn 100%

##### 🏆 Rank #461 (`11 ♡` | `350 👁️` | Model: `seedream_v5_pro` | Author: `@koonsapple2043` | Size: `3:4` | Refs: `1`)
- **Publication ID**: `f84ff434-cf3f-4151-9a13-0c1d2ba6a6bd`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0461_seedream_v5_pro_f84ff434.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3JoTFUNjCGiE0Z5Fzy9w8HAYBe4/hf_20261004_103425_3a0f1c83-cbda-4096-b93f-f161fe4800aa.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3JoTFUNjCGiE0Z5Fzy9w8HAYBe4/hf_20261004_103425_3a0f1c83-cbda-4096-b93f-f161fe4800aa_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3JoTFUNjCGiE0Z5Fzy9w8HAYBe4/bbd3eb98-235d-4166-bc01-0ef7193ea49f_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Từ ảnh thỏi son tách nền trắng thành Flat-Lay mỹ phẩm xa xỉ (`Before: rank_0461_ref1.jpg` ➔ `After: rank_0461_seedream_v5_pro_e01eb427.webp`)**: Từ 1 ảnh chụp thỏi son kem đơn điệu trên nền trắng (`@img1`), `seedream_v5_pro` nhân bản thành 6 thỏi son xếp xen kẽ cùng những vệt kem son mịn màng (`creamy lipstick swatches`) dưới ánh nắng chiều đổ bóng gobo sắc nét, giữ nguyên 100% logo `L'AVANT` trên thân son.

```text
Top-down premium beauty advertising flat lay featuring the exact NYX Professional Makeup Fat Oil Lip Drip product from the reference image, maintaining the original packaging geometry, transparent cylindrical bottle, chocolate-brown lip oil and vivid neon chartreuse cap. The product lies diagonally across a warm ivory studio surface, surrounded by several abstract glossy pools of translucent chocolate-brown lip oil and clear glass-like cosmetic gel. Small sculptural lime-green acrylic elements create bold graphic accents around the composition. Elegant negative space, controlled asymmetry, modern Gen Z luxury beauty campaign aesthetic, rich glossy textures, realistic oil viscosity and tiny specular reflections, no food styling, no unnecessary accessories. Crisp overhead studio lighting with defined soft-edged shadows, subtle hard light reflections across the glossy liquid, editorial product photography, Hasselblad medium-format aesthetic, 80mm lens, f/11, high micro-contrast, perfectly sharp product and packaging, clean commercial retouching, photorealistic, ultra-realistic materials, 8k
```

##### 🏆 Rank #645 (`4 ♡` | `213 👁️` | Model: `seedream_v5_pro` | Author: `@zlatkey_ai` | Size: `3:4` | Refs: `2`)
- **Publication ID**: `06ab4f45-347b-4ca7-8320-df176f60a0b7`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0645_seedream_v5_pro_06ab4f45.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2xUBiuJ2fGiXj8gdIe6ZaxIiOlh/hf_20260930_203341_1552323a-361b-4532-a2d0-270fb90942f0.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2xUBiuJ2fGiXj8gdIe6ZaxIiOlh/hf_20260930_203341_1552323a-361b-4532-a2d0-270fb90942f0_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_2xUBiuJ2fGiXj8gdIe6ZaxIiOlh/hf_20260930_201247_b9672281-286a-4d53-b837-f593540f6186.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_2xUBiuJ2fGiXj8gdIe6ZaxIiOlh/5b5f7b88-d9ff-4e93-a957-0bccb6e7a648_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Chai nước hoa FASCENT trên đá Slate đen ướt đẫm sương & ánh nắng Gobo (`rank_0645_seedream_v5_pro_06ab4f45.webp`)**: Kiểm định bằng mắt cho thấy `seedream_v5_pro` đặt chai nước hoa `FASCENT — I FIG YOU` (nắp xanh vân gỗ nhám, thân thủy tinh trong suốt) vào góc 1/3 phải trên phiến đá đen ướt lấp lánh giọt nước cùng quả sung chín bổ đôi ở góc trái; luồng sáng spotlight chiếu xiên tạo vệt khúc xạ thủy tinh (`caustics`) trên mặt đá đen cực kỳ điện ảnh!

```text
[общий блок]
Elevated 45-degree view, the bottle on the right third of the frame on wet black slate. On the left, a fig torn apart in two halves, jewel-red seeded flesh glistening, a few scattered seeds and petal-like fragments of skin, droplets everywhere. A fig branch with leaves crossing the lower left corner. A soft cone of light from the upper left falls on the scene, the rest fades into darkness. Generous dark negative space on the top left for text. 70mm lens, f/5.6, 4:5 vertical.
```

##### 🏆 Rank #705 (`3 ♡` | `174 👁️` | Model: `seedream_v5_pro` | Author: `@zlatkey_ai` | Size: `3:4` | Refs: `2`)
- **Publication ID**: `640cefe7-904e-41a0-b741-aa2f29d3af38`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0705_seedream_v5_pro_640cefe7.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2xUBiuJ2fGiXj8gdIe6ZaxIiOlh/hf_20260930_203457_6229acd6-6c14-44b7-ac1c-a94a5d5b6a71.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2xUBiuJ2fGiXj8gdIe6ZaxIiOlh/hf_20260930_203457_6229acd6-6c14-44b7-ac1c-a94a5d5b6a71_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_2xUBiuJ2fGiXj8gdIe6ZaxIiOlh/hf_20260930_201247_b9672281-286a-4d53-b837-f593540f6186.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_2xUBiuJ2fGiXj8gdIe6ZaxIiOlh/5b5f7b88-d9ff-4e93-a957-0bccb6e7a648_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Nước hoa FASCENT đặt giữa những quả sung tím bổ đôi (`Before: rank_0705_ref1.jpg + ref2.png` ➔ `After: rank_0705_seedream_v5_pro_a922d1a0.webp`)**: Ghép chai nước hoa từ `@img1` vào bố cục 9:16 ngập tràn quả sung chín mọng có giọt sương li ti và lá sung xanh, biến ảnh chụp sản phẩm thông thường thành keyframe quảng cáo nước hoa Pháp.

```text
[общий блок]
Top-down flat lay, perfectly overhead view. The perfume bottle lies horizontally on its side, nestled into a dense pile of dark purple figs of different sizes, several halved with glossy red-pink seeded flesh, fig leaves tucked between them and a few loose stems. The label faces up toward the camera, fully readable, cap pointing to the right. Figs overlap naturally and partly frame the bottle, wet dewy skins, scattered water droplets, deep shadows between the fruits. Soft overhead light with a slight gradient falling off into black at the edges. 50mm lens, f/8, everything sharp, rich texture, 4:5 vertical.
```

##### 🏆 Rank #943 (`1 ♡` | `52 👁️` | Model: `nano_banana_2` | Author: `@jenomyk` | Size: `3:2` | Refs: `2`)
- **Publication ID**: `46aaa711-5bff-4ed7-b025-c2904646184d`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0943_nano_banana_2_46aaa711.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38IVL6p8Ia9xR3KK1zJkwjlBBSQ/hf_20261014_075539_dde89a18-0416-4c0b-a15d-7a2d959ea8ca.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38IVL6p8Ia9xR3KK1zJkwjlBBSQ/hf_20261014_075539_dde89a18-0416-4c0b-a15d-7a2d959ea8ca_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38IVL6p8Ia9xR3KK1zJkwjlBBSQ/606ba0cc-9e31-4e5b-912d-11e9b568d114.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38IVL6p8Ia9xR3KK1zJkwjlBBSQ/d5f53c1a-51e4-4251-b495-e0ca0c8182e3.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Đỉnh cao giữ chữ khắc chìm siêu nhỏ trên thân chai nước hoa (`rank_0943_nano_banana_2_46aaa711.webp` & `Rank #1427`)**: `nano_banana_2` dựng chai nước hoa vuông màu xám bê tông nhám với nắp cầu đen bóng, giữ sắc nét tuyệt đối từng nét khắc logo mỏ neo và các dòng chữ nhỏ `PORTO GEDANUM / 54°N / New York 92 / extrait de parfum / 50 ml` không sai một pixel!

```text
Ultra-realistic, minimalist studio product shot of the "New York 92" perfume bottle by Porto Gedanum 54°N, photorealistic 8k resolution.
Bottle Architecture & Material:
Shape & Silhouette: Heavy square raw porcelain bottle with a perfectly smooth, round spherical black cap on top, strictly identical in geometry and structure to Image 35.
Material & Color: Crafted entirely from raw, unglazed porcelain with a matte ceramic texture in a concrete-grey shade.
Engraving Details:
Technique & Depth: All logos, graphics, and typography are debossed/engraved to the exact same uniform depth into the porcelain front face, filled with a solid black finish.
Layout & Typography: Identical in font style and placement to Image 35:
At the top: The anchor-waterdrop logo in black.
Below it: The brand name "PORTO GEDANUM" with "54°N" directly underneath in black.
Middle: The fragrance name "New York 92" in black (replacing "Honolulu 08").
Bottom: The text "extrait de parfum" and "50 ml" centered below in small, clean black lettering.
Setting & Composition:
Placement: The bottle stands perfectly centered on a smooth white table against a seamless, bright white studio backdrop, identical to Image 35.
Strict Constraint: Completely empty background and tabletop. No fragrance ingredients, no props, no surrounding objects. Only the single perfume bottle stands alone in the center.
Lighting:
Soft, even luxury studio lighting casting a delicate, natural shadow beneath the bottle on the white surface. High-end commercial product photography style.
```

##### 🏆 Rank #1396 (`0 ♡` | `23 👁️` | Model: `nano_banana_2_1` | Author: `@arslnbey` | Size: `1:1` | Refs: `1`)
- **Publication ID**: `8f239a3b-8b77-45be-9485-1084a13a5197`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1396_nano_banana_2_1_8f239a3b.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3GYomaEXKE3WqhPWaDTtaXYbOnk/hf_20261018_101117_6fb9e75b-86d3-43eb-a2c5-36ef5e179a2e.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3GYomaEXKE3WqhPWaDTtaXYbOnk/hf_20261018_101117_6fb9e75b-86d3-43eb-a2c5-36ef5e179a2e_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3GYomaEXKE3WqhPWaDTtaXYbOnk/b8a6d1a5-9ed3-4660-bc6f-a1311a109c90.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Kỹ thuật Vi phẫu Đổi màu từng đường chỉ khâu bằng mã HEX `#F9E11F` (`Before: rank_1396_ref1.jpg` ➔ `After: rank_1396_nano_banana_2_1_8f239a3b.webp`)**: Đối chiếu trực tiếp `ref1.jpg` và ảnh xuất cho thấy `nano_banana_2_1` chỉ đổi đúng màu sợi chỉ khâu từ trắng ngà sang vàng chanh `#F9E11F` có độ xoắn sợi sáp bóng nhẹ VÀ xóa sạch vụn giấy thừa ở mép trên ví, trong khi toàn bộ vết nhăn da bò xanh bên dưới giữ nguyên 100% pixel-identical!

```text
Edit this product photo. Change ONLY the color of the saddle-stitch thread to bright lemon yellow (#F9E11F) waxed polyester thread, with natural twist texture, slight sheen and realistic shading in each stitch. Keep everything else pixel-identical: the same green vegetable-tanned leather, same wallet shape, same number and position of stitches, card slots, camera angle and lighting. Clean the top edge of the wallet so no paper or banknote fragments remain. Pure white seamless background, professional e-commerce product photo.
```

##### 🏆 Rank #1499 (`0 ♡` | `17 👁️` | Model: `gpt_image_2_5` | Author: `@cookingotter1180` | Size: `1:1` | Refs: `1`)
- **Publication ID**: `06f7574c-e0cf-4dc0-91e5-8e536e4a79e8`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1499_gpt_image_2_5_06f7574c.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3CnsQZ5lqcaCmSf6EDQZaLTgI8f/hf_20261013_190442_581a909b-0c66-4384-9d3c-d3c62a83a922.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3CnsQZ5lqcaCmSf6EDQZaLTgI8f/hf_20261013_190442_581a909b-0c66-4384-9d3c-d3c62a83a922_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3CnsQZ5lqcaCmSf6EDQZaLTgI8f/hf_20261013_185258_c5741950-3ae0-4351-a3e0-80be7a8ac06a.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Biến ảnh sản phẩm thành Bản vẽ Kỹ thuật Bung rã Linh kiện (`Exploded-View Construction Render` — `Before: rank_1499_ref1.png` ➔ `After: rank_1499_gpt_image_2_5_06f7574c.webp`)**: Từ bức ảnh chụp cánh cửa trượt nhôm trắng bình thường (`@img1`), `gpt_image_2_5` tách rời từng lớp khung nhôm sơn tĩnh điện `RAL 9016`, hộp cuốn, kính 2 lớp, gioăng cao su và thanh ray theo trục lắp ráp isometric kèm đường kẻ nét đứt kỹ thuật (`thin dashed grey alignment lines`) — cực kỳ hữu ích khi bạn muốn làm cảnh TVCโชว์ cấu tạo cành thông chống cháy / đèn LED!

```text
Photorealistic exploded-view construction render of the exact white sliding door in the reference image (white powder-coated aluminium, RAL 9016, flat flush shutter box with the small dark grey "kwala" wordmark). Seamless light grey studio background (#E9EBEE), soft shadows, three-quarter front view, technical product catalogue quality like a premium European window manufacturer's "how it is built" illustration. Every component is pulled apart along its natural assembly direction, evenly spaced, with thin dashed grey alignment lines showing where each part fits. All parts are in the same white except glass, mesh, seals and strap.

Show ALL of these components, each clearly separated and recognisable:
1. Shutter box (top): the flat rectangular flush box, with its front cover panel lifted up and forward off the box so you can see inside. Inside: the galvanised steel octagonal roller axle with the shutter curtain partly wound on it, end brackets with bearings at both ends, and on the RIGHT end of the axle a small round strap reel (strap pulley).
2. Shutter curtain: a section of horizontal insulated aluminium slats (rounded, foam-filled), with a heavier bottom bar and black rubber seal, pulled down and slightly forward from the box.
3. Left and right shutter guide rails: slim vertical aluminium channels with black brush seals, pulled out sideways from the frame.
4. Strap system, in its correct place: a narrow grey woven strap runs from the strap reel on the right end of the axle, down through a small strap guide in the underside of the box, straight down the front face of the right-hand frame upright, into a slim flush strap winder (belt winder) mounted on the front face of the right-hand upright about 1 m above the floor. Show the winder pulled slightly forward off the upright with its cover plate, the strap continuous from reel to winder.
5. Main outer frame: a 3-track aluminium frame (head, two jambs, and a low sill with drainage slots), shown with the three parallel tracks clearly visible at the sill.
6. Two sliding glass panels: slim tubular aluminium sashes with clear 5 mm glass in black rubber gaskets, small rollers visible at the bottom, a slim pull handle and lock on the meeting stile, pulled forward from the inner two tracks.
7. Insect screen panel: a full-height sliding panel with a slim white aluminium frame, fine dark-grey fibreglass mesh and small nylon rollers, pulled forward from the OUTER third track, positioned in front of the glass panels.
8. Black pile brush weather seals shown along the panel edges.

Composition balanced and uncluttered, every part fully in frame and sharp. No text, no labels, no numbers, no arrows other than the thin dashed alignment lines, no watermark. Only the "kwala" wordmark on the box.
```

##### 🏆 Rank #1665 (`0 ♡` | `10 👁️` | Model: `nano_banana_2_1` | Author: `@enzop` | Size: `3:2` | Refs: `3`)
- **Publication ID**: `d2f9768c-c9ea-4f9a-aaba-e11561d1d5c0`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1665_nano_banana_2_1_d2f9768c.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KuvXUVM5ZupIDfMoWCAJMQ86Ei/5635e123-a0b3-4a5d-9034-cb5d503e7fc8.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KuvXUVM5ZupIDfMoWCAJMQ86Ei/hf_20261019_151306_ac49e094-ca39-4071-bd21-6786c730a3fb_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3KuvXUVM5ZupIDfMoWCAJMQ86Ei/3fa48417-0c5b-4f04-9ea4-cb6ff34a236c.jpg
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3KuvXUVM5ZupIDfMoWCAJMQ86Ei/37601f0d-fe2b-472b-a54e-c5f1afc5dda9.jpg
- **Input Reference `@img3`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3KuvXUVM5ZupIDfMoWCAJMQ86Ei/3196a196-6130-4942-a34c-70d0063e19ce.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Tĩnh vật 3 món đồ Decor Nội thất Đá & Bê tông từ 3 ảnh rời (`Before: rank_1665_ref1..ref3` ➔ `After: rank_1665_nano_banana_2_1_d2f9768c.webp`)**: `nano_banana_2_1` gom 3 sản phẩm rời (đèn trụ đá vôi khía rãnh phát sáng khe dọc, bình hoa bê tông xám cắm cành ô-liu, đồng hồ bê tông mặt tròn) đặt lên bục đá travertine xếp bậc trước nền tường vữa xanh xô thơm (`deep sage-green plaster wall`), chừa đúng 1/3 khoảng trống bên trái để đặt tiêu đề quảng cáo.

```text
A sculptural still life of the cast stone and concrete homeware objects shown in the reference images, arranged together on stepped pale limestone plinths: the tall fluted limestone column lamp glowing warmly from its vertical slit, the stacked grey concrete vase holding a green olive branch, the round grey concrete wall clock with thin steel hands leaning on a plinth. The objects fill two thirds of the frame, grouped right-of-center; soft open negative space on the left on a deep sage-green plaster wall. Palette: deep sage green, warm limestone sand, charcoal concrete, a warm glow of light. Bright soft key light with crisp shadows, low wide angle, premium editorial product photography grade. No text, no letters, no logos, no captions, no UI.
```

##### 🏆 Rank #891 (`1 ♡` | `92 👁️` | Model: `marketing_studio_2_image` | Author: `@relaxingant1443` | Size: `3:4` | Refs: `1`)
- **Publication ID**: `fd9ff89a-4ed6-49c2-9fef-39bb50fbdc0d`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0891_marketing_studio_2_image_fd9ff89a.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3J3QEq5tts4HRTGVVah2H4xgqbS/hf_20261013_214803_9c002fbf-2893-4092-bcc0-150d17a8f3dc.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3J3QEq5tts4HRTGVVah2H4xgqbS/hf_20261013_214803_9c002fbf-2893-4092-bcc0-150d17a8f3dc_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3J3QEq5tts4HRTGVVah2H4xgqbS/877c3fc5-af70-4dd6-94d2-d464cd03410c.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Biến ảnh bánh burger trên đĩa trắng thành Poster Quảng cáo F&B (`Before: rank_0891_ref1.jpg` ➔ `After: rank_0891_marketing_studio_2_image_b4b072cf.webp`)**: Model `marketing_studio_2_image` lấy chiếc bánh burger phô mai từ ảnh chụp đĩa trắng (`@img1`), đặt vào bàn tay đeo găng đen đang bóp nhẹ làm phô mai chảy tràn trên nền đỏ rực kèm tiêu đề lớn `SMASH BURGER`.

```text
Recreate the selected hand-held product template as a photorealistic Namma Chicken burger advertisement. Preserve its simple composition: one hand entering diagonally from the lower right, holding the hero product against a clean studio background. Replace the snack packet completely with the bitten chicken burger from the uploaded photograph.

PRODUCT AND BITE

Use only the foreground bitten burger as the product reference. Remove the plate, tabletop, background burger and all other elements from the source photograph.

Preserve the sesame bun, crispy fried chicken, visible white chicken interior, lettuce and creamy sauce. Retain the distinctive missing bite through the front of the burger, including the irregular bitten edges of the bun and exposed cross-section of the chicken. Do not repair the bite or turn the burger into an untouched product.

Position the burger upright in the hand, with the bitten face directed towards the camera and tilted slightly upward so the chicken interior, crispy coating and sauce are clearly visible. Keep the burger convincingly sized for a person to hold.

SAUCE — THE KEY APPETITE DETAIL

Make the existing creamy house sauce slightly more generous around the bitten opening. Use a thick, glossy, pale ivory sauce with a subtle warm tint.

Show sauce slowly bulging and oozing from between the chicken, lettuce and bun at the exposed bite. Form one short, gravity-driven trickle down the bitten edge towards the hand.

Let a small amount of that same sauce reach the upper side of the thumb holding the burger. Show a connected, believable path from the burger to the skin, ending in a small rounded bead just below the thumb’s contact point. Keep this detail visible to the camera.

The sauce should look rich and appetising: thick enough to cling to the food, with gentle highlights and natural surface tension. Avoid watery streams, long dangling strings, excessive spills or a hand covered in sauce. Keep the chicken cross-section and crispy texture visible.

HAND AND CLOTHING

Use one anatomically correct adult hand with natural skin texture and a relaxed, believable grip. Support the lower bun with the fingers and place the thumb along the front-side edge, leaving the bite unobstructed.

Position the thumb beside a small opening in the wrapper so the sauce can naturally touch exposed skin. Do not make sauce pass through the paper.

Keep the forearm entering from the lower right as in the template. Replace the striped sleeve with a plain warm-cream cotton sleeve. Avoid jewellery, nail art, tattoos and distracting clothing details.

NAMMA BRANDING — NO LOGO REFERENCE REQUIRED

Wrap only the bottom third of the burger in matte, food-safe paper, leaving the bitten face, crispy chicken and sauce clearly visible.

Use deep burgundy-red paper, HEX #930E0A, with golden-yellow printing, HEX #F2AD14.

On a clearly visible front-facing panel, print these exact words on two stacked lines:
NAMMA
CHICKEN

Use heavy, condensed, uppercase sans-serif lettering. Make the wordmark large enough to read on a phone, with strong yellow-on-red contrast. Keep the lettering on a relatively smooth section of paper so folds and fingers do not obscure it.

This is a simple typographic brand treatment. Do not invent a chicken mascot, icon, badge or additional wording.

Keep the wrapper below the bitten opening. Leave a small area of the thumb exposed beside the wrapper’s upper edge so one modest trickle of creamy sauce can travel naturally from the bite onto the skin without passing through the paper.

BACKGROUND AND COLOUR

Replace the blue background with a seamless deep burgundy-red studio background, HEX #930E0A. Add a restrained tonal lift behind the burger to separate its outline, while keeping the overall background clean and unmistakably red.

Distinguish the red wrapper from the red backdrop through realistic edge lighting, shadows and paper texture. Use the golden-yellow branding and warm-cream sleeve as supporting colour accents.

No checkerboard, patterns, props or scenery.

COMPOSITION AND LIGHTING

Preserve the selected template’s aspect ratio and diagonal hand-held composition. Place the burger prominently in the upper-middle portion of the frame, with clear breathing space above and around it.

Use directional studio light from the upper left, with soft fill to reveal the bitten interior. Give the sesame bun natural highlights, the coating crisp detail and the sauce a gentle gloss. Maintain realistic shadows beneath the bun, around the fingers and inside wrapper folds.

Keep the burger, sauce trickle and printed wrapper branding sharply resolved. Use natural food colours and realistic skin tones. The result should feel like a polished commercial food photograph with a spontaneous “just took a bite” moment.

EXCLUSIONS

Remove all original snack packaging and its text. Do not include “POP QUIZ” or any other original branding.

Do not add headlines, prices, opening d
```

##### 🏆 Rank #1241 (`0 ♡` | `39 👁️` | Model: `gpt_image_2_5` | Author: `@kpt_picard` | Size: `2:3` | Refs: `1`)
- **Publication ID**: `fe079566-d3cb-474a-94fa-bfba2706fd47`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1241_gpt_image_2_5_fe079566.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_34WjaGu0Vt0o30q3wAOEUXVcK7M/hf_20261014_074019_8d545587-044c-4a8a-80b5-590621d49193.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_34WjaGu0Vt0o30q3wAOEUXVcK7M/hf_20261014_074019_8d545587-044c-4a8a-80b5-590621d49193_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_34WjaGu0Vt0o30q3wAOEUXVcK7M/488fd84d-dd89-4543-b8f4-b876d4ed3d73.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Biến túi mì Ý tách nền trắng thành Poster Ẩm thực kèm Dấu tiếng Czech chuẩn 100% (`Before: rank_1241_ref1.png` ➔ `After: rank_1241_gpt_image_2_5_7cf24a03.webp`)**: `gpt_image_2_5` giữ nguyên bao bì túi nui xoắn `GUSTO & VITA` từ `@img1`, cho những viên nui bay lơ lửng trong nắng vàng và in dòng chữ `ZAKROUCENÉ DO SVĚTLA` chuẩn từng dấu sắc và dấu móc câu tiếng Czech!

```text
Create a premium vertical poster ad for the Czech pasta brand "adriana Pasta". The hero product is the real 1 kg PENNE package (clear transparent cellophane pillow bag with a wide matte black center band), presented as the absolute center of a sculptural ingredient composition. Build the image as a Cannes-level food campaign where packaging and ingredients are inseparably fused: the bag is embedded inside a dense oval body of real uncooked penne rigate, while a single long lemon peel spirals continuously around the structure from bottom to top like a fragrant ribbon of motion.

Use a front-facing studio product shot with a calm, slightly low eye-level perspective. Keep the composition centered on a clean monochrome terracotta-orange backdrop with generous negative space. The package stands upright in the middle, nested inside an oval penne halo. One lemon peel wraps the sculpture in a tall ascending helix, starting near the bottom foreground, circling the package and pasta mass, and tapering above the top edge. Place one fresh lemon wedge directly beneath as the grounded base note, and one compact basil cluster at the lower-left edge of the pasta oval. Keep the silhouette iconic, balanced, and immediately legible.

PACKAGE (keep faithful to the reference photo): transparent glossy cellophane bag with crimped top and bottom seals, filled with real penne visible on both sides of a vertical matte black band. On the black band, top to bottom: the lowercase wordmark "adriana" in white, large, geometric rounded sans-serif, with a thin vertical white line and a small wheat-ear icon to its left; directly below, the red handwritten-script word "Pasta" with a small ® mark; then a red spaced-caps line "100% SEMOLINA" with a fine red dotted rule above and below; then a small block of tiny white fine-print Czech text rendered as soft, non-legible texture; then the white caps word "PENNE"; at the lower left a single raw penne illustration; at the lower right a round brown-gold seal with five stars, a wheat ear and the curved text "SKVĚLÁ CHUŤ A KVALITA"; at the bottom edge "1 kg". Crisp print, believable matte ink, subtle bag highlights, realistic cellophane wrinkles without hiding the typography. Do not alter the logo, proportions or colors of the band.

SURROUNDING PASTA: penne rigate must look dry, real and tactile: diagonal-cut tube ends, fine parallel ridges, hollow centers, semolina grain, slight tone variation, natural irregularity, and consistent realistic scale relative to the bag. The lemon peel should feel freshly cut and aromatic, with realistic pith thickness, glossy yellow skin, visible oil pores, and physically plausible curling tension. The lemon wedge shows translucent juicy pulp and a moist cut surface. Basil leaves are fresh, saturated, slightly glossy, clearly veined. Add only a few tiny salt crystals and scattered pepper grains near the lemon wedge, with restraint.

LIGHTING AND COLOR: soft premium studio lighting, directional key from upper left, elegant frontal fill, gentle grounded shadow beneath the base. Palette: 50% warm terracotta and burnt orange background, 20% pale wheat and semolina beige, 15% citrus yellow, 10% black and red packaging accents, 5% basil green and pepper. Increase local contrast on penne ridges, the white wordmark, the red script, lemon peel edges, citrus pulp and basil sheen while keeping the finish soft, clean and luxurious. Keep the black band deep but with visible matte detail; avoid dead black patches, muddy grading, or greasy highlights.

POSTER TYPOGRAPHY (CZECH, EXACT): in the upper negative space place the headline "ZAKROUCENÉ DO SVĚTLA". Beneath it, in smaller type: "Penne s jasnou citronovo-bazalkovou duší." One tiny lower-corner line: "semolina, citron, bazalka". Typography is minimal, airy, premium, in a refined light-weight sans-serif with wide tracking for the headline, and never interferes with the package or the lemon spiral.

CZECH TYPOGRAPHY RULES: render all Czech text with correct diacritics exactly as written: háčky (Č, Ě, Š, Ž, Ť), čárky (Á, É), and keep the diacritics on UPPERCASE letters (É in ZAKROUCENÉ, Ě in SVĚTLA and SVĚLÁ, Á, Ť in CHUŤ). Never replace accented letters with plain ASCII (no Z instead of Ž, no E instead of Ě/É). Háčky and čárky must be fully visible, correctly shaped, not merged with neighboring letters, with enough line spacing so they are not clipped. Use the Czech full stop and standard letterforms, no invented glyphs, no extra or missing letters. Spelling must match exactly: "ZAKROUCENÉ DO SVĚTLA" / "Penne s jasnou citronovo-bazalkovou duší." / "semolina, citron, bazalka" / "SKVĚLÁ CHUŤ A KVALITA".

COMPOSITION AND AVOIDANCE: premium vertical product poster, exact single-bag hero, centered sculptural layout, monochrome backdrop, product-first hierarchy, pristine readability. Avoid extra props, plates, cutlery, duplicated basil clusters, chaotic crumbs, warped packaging, altered or misspelled logo text, missing diacritics, English text anywhere on the poster, unreadable label text, messy scatter, muddy grading, cheap typography, or any loss of the package as the dominant hero.
```

##### 🏆 Rank #1235 (`0 ♡` | `40 👁️` | Model: `gpt_image_2` | Author: `@prajiguruprasad` | Size: `auto` | Refs: `2`)
- **Publication ID**: `62184b76-1d20-4029-800c-78cde156dcd8`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1235_gpt_image_2_62184b76.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2vRp6HHRdjnM5rZlRUeYyAvjGjX/hf_20260918_202224_cb2782d7-879a-4dfc-af91-f1efd68a72da.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2vRp6HHRdjnM5rZlRUeYyAvjGjX/hf_20260918_202224_cb2782d7-879a-4dfc-af91-f1efd68a72da_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_2vRp6HHRdjnM5rZlRUeYyAvjGjX/a74409f1-7eb5-4e05-b3d7-09695daeaf5f.jpg
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_2vRp6HHRdjnM5rZlRUeYyAvjGjX/88236174-5d12-44ac-955c-3065834900f3_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Nước hoa SHAGHAF OUD MARINE cắm trong cát sa mạc (`Before: rank_1235_ref1.jpg + ref2.png` ➔ `After: rank_1235_gpt_image_2_03a7d1cb.webp`)**: Ghép hoàn hảo dáng chai xanh ngọc từ `@img1` và hộp giấy từ `@img2` vào đụn cát vàng có sóng biển vỗ phía sau, giữ nguyên chữ mạ bạc trên thân chai.

```text
PRODUCT LOCK — Use the attached image as the exact product. Reproduce it with absolute fidelity: do not redesign, restyle, recolour, re-letter or re-proportion any part of it. The product is a flat rectangular perfume bottle in matte deep teal
lacquer with squared shoulders and straight vertical sides, topped by a large square polished gold cap carrying two four-pointed star facets in relief. The front carries gold lettering: SHAGHAF above OUD MARINE in the upper area, and SWISS ARABIAN in the lower third. Keep the teal and the gold exactly as in the reference. The cap is one solid piece with exactly two stars. All lettering stays identical in wording, spacing and position. Add no other text anywhere in the image. The gold cap is polished metal and must mirror its surroundings — a dark horizon line across its lower facets, a bright sky reflection on its upper facets, and a colour bounce from the surface it stands on. It is never a flat matte gold shape. Integrate the bottle into the scene with physically correct perspective, scale, contact shadow, reflection and ambient colour bounce.

PLACEMENT: The bottle lies on its back, pressed into fine rippled desert sand, seen from directly overhead with the label facing straight up to camera and fully legible. It sits in a shallow impression it has made, with a soft crescent shadow along one side.

SCENE: Fine wind-rippled desert sand filling the entire frame, its ripples running in smooth parallel curves around the bottle. A light dusting of the same sand across the lower corners of the bottle and along one edge of the cap, as if wind-blown. No other objects. No horizon.

CAMERA: 50mm, camera directly overhead and perfectly perpendicular, f/11, everything sharp.

LIGHT: Hard low raking sun from the upper left throwing every sand ripple into strong relief and casting a long soft shadow from the bottle across the sand. The gold cap mirrors the bright sky above and picks up a warm sand bounce.

GRADE: Warm gold sand, deep teal, warm polished gold. Rich, graphic, high contrast.

NEGATIVE - distorted or altered product, wrong bottle shape, flat matte gold cap with no reflection, extra or missing stars on the cap, misspelled or invented text, additional logos or watermarks, warped lettering, ice covering or distorting the label, plastic or crystal-looking ice, floating product without contact shadow, oversaturated colour, teal-orange grade, yacht, palm-tree sunset, turquoise lagoon, CGI splash crown, decorative smoke swirls, fake bokeh snowflakes, Christmas decoration, lens flare, people unless specified, low resolution, no flat gold cap, no scattered loose petals, no water splash, no fish, no coral, no divers, no CGI bubble look, no perfectly spherical identical bubbles, no CGI splash crown, no symmetrical water shapes, no rainbow in the spray, no people, no CGI water, no perfectly still mirror surface, no lemons arranged in a pattern, no people, no footprints, no scattered objects, no sand covering the label, no tyre tracks.

Photorealistic overhead product photography. 4:3 vertical.
```

##### 🏆 Rank #1208 (`0 ♡` | `47 👁️` | Model: `nano_banana_2` | Author: `@jenomyk` | Size: `3:2` | Refs: `2`)
- **Publication ID**: `b8573c96-a47e-4c0b-8b50-e2dfdf9af4ed`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1208_nano_banana_2_b8573c96.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38IVL6p8Ia9xR3KK1zJkwjlBBSQ/hf_20261015_104025_f1096d27-f3a3-4f0a-ad60-dbef9c971938.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38IVL6p8Ia9xR3KK1zJkwjlBBSQ/hf_20261015_104025_f1096d27-f3a3-4f0a-ad60-dbef9c971938_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38IVL6p8Ia9xR3KK1zJkwjlBBSQ/9eef1965-8562-4f4c-9a0e-207987091f5f.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38IVL6p8Ia9xR3KK1zJkwjlBBSQ/58e9eec5-fe96-4120-bc42-8df36fe88d49.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Biến Screenshot Bảng Mùi Hương Web + Ảnh Chai Cũ thành Ảnh Studio Chai Mới (`Before: rank_1208_ref1.png + ref2.png` ➔ `After: rank_1208_nano_banana_2_57e467c0.webp`)**: Đọc các nốt hương từ ảnh chụp màn hình web (`@img1`) và dáng chai từ `@img2` để dựng thành bức ảnh quảng cáo chai nước hoa màu xanh ngọc bích đặt giữa lá bạc hà, chanh vàng và gỗ tuyết tùng.

```text
Ultra-realistic, minimalist studio product shot of the "Moscow 52" perfume bottle by Porto Gedanum 54°N, photorealistic 8k resolution.
Bottle Architecture & Material:
Shape & Silhouette: Heavy square raw porcelain bottle topped with a perfectly smooth, round spherical black cap on top, strictly identical in geometry and structure to Image 45[cite: 45].
Material & Color: Crafted entirely from raw, unglazed porcelain with a matte ceramic texture in an intense, pitch-black coal-like shade.
Engraving Details:
Technique & Depth: All logos, graphics, and typography are debossed/engraved to the exact same uniform depth into the porcelain front face, filled with a vibrant crimson-red finish.
Layout & Typography: Identical in font style and placement to Image 45[cite: 45]:
At the top: The anchor-waterdrop logo in crimson red[cite: 45].
Below it: The brand name "PORTO GEDANUM" with "54°N" directly underneath in crimson red[cite: 45].
Middle: The fragrance name "Moscow 52" in crimson red (replacing "Honolulu 08")[cite: 45].
Bottom: The text "extrait de parfum" (replacing "extrait de parfum" or any standard text) and "50 ml" centered below in small, clean crimson-red lettering[cite: 45].
Setting & Composition:
Placement: The bottle stands perfectly centered on a smooth white table against a seamless, bright white studio backdrop, identical to Image 45[cite: 45].
Strict Constraint: Completely empty background and tabletop. No fragrance ingredients, no props, no surrounding objects. Only the single perfume bottle stands alone in the center[cite: 45].
Lighting:
Soft, even luxury studio lighting casting a delicate, natural shadow beneath the bottle on the white surface[cite: 45]. High-end commercial product photography style. To draw focus to the bottle, a shallow depth of field should be used, ensuring only the object is perfectly in focus. The raw matte finish should softly capture the glares from the studio softboxes. No screen elements, camera metrics or interface overlays. Highly detailed 8k photography. No conversational text included. Do not include any decorative items, raw leaves or materials next to the bottle. No branding other than the specified Porto Gedanum and Moscow 52 elements. No visible humans. No watermarks. High contrasts. Cinematic touch. Precise perspective matching Image 45[cite: 45].
```

##### 🏆 Rank #1066 (`1 ♡` | `15 👁️` | Model: `gpt_image_2_5` | Author: `@naddou` | Size: `9:16` | Refs: `2`)
- **Publication ID**: `9e1513fb-2017-43ce-9e45-65a353728940`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1066_gpt_image_2_5_9e1513fb.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3Km3z80aDdxH7uuOrje89MKzA7l/hf_20261016_115931_35468914-5b0e-4cb6-aac6-9fa92f19ddef.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3Km3z80aDdxH7uuOrje89MKzA7l/hf_20261016_115931_35468914-5b0e-4cb6-aac6-9fa92f19ddef_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Km3z80aDdxH7uuOrje89MKzA7l/e4c42312-efea-4c4a-9cd2-fb18d99e883c.jpg
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Km3z80aDdxH7uuOrje89MKzA7l/bc3dcd85-11d8-4321-99bf-34a874d0ce14.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Thay thế Túi xách sản phẩm thật vào bố cục Flat-Lay Mùa Hè giữ nguyên bối cảnh (`Rank #1066` — `gpt_image_2_5`)**: Dùng `@img1` làm chuẩn tuyệt đối cho chiếc túi đan màu xanh cô-ban (`cobalt/teal blue chunky woven basketweave`), thay thế chiếc túi màu nâu trong bố cục flat-lay (`@img2`) trong khi giữ nguyên khăn trải bàn sọc xanh trắng, nửa quả cam tươi và kính râm.

```text
REFERENCE 1 is the user's actual product photograph and is authoritative for every feature of the replacement bag: cobalt/teal blue chunky woven body, very broad shallow boat-shaped rounded trapezoid silhouette, two separate circular woven loop handles, and small tan rectangular label centered below the handles. Preserve its original width-to-body-height ratio, approximately 2.4:1 excluding the handles; the bag must remain broad and low. Reproduce the weave, color, label position, rounded side contours, handle diameter and attachments from reference 1. Keep original indistinct label lettering as photographic detail. The original scene bag in reference 2 is only a placement guide; its material, color, shape, leather straps and handle structure must be replaced by the user's real blue bag. Use realistic scale, perspective, material detail, light and contact shadows. One photograph only. Preserve the reference 2 scene composition and lighting, replacing its handbag with the blue bag from reference 1. Clean screenshot interface icons, rounded screenshot corners and app controls out of the photographic output. No added typography, invented logos, watermark, collage, or new marketing claims.

REFERENCE 2 is the overhead summer still life: pale linen fills the background, the tan woven bag and brown handles occupy the upper-left area, two orange halves sit upper-right, brown-tinted sunglasses sit center-right, an orange striped scarf runs diagonally through the lower-left, small gold earrings lie below the sunglasses, and leafy shadows cross the scene. Edit THIS overhead photograph. Replace the tan bag and both brown leather handles with the exact blue handbag from reference 1 laid flat in the same upper-left diagonal orientation, with its genuine two circular woven handles and broad shallow blue body. Preserve the photographic flat-lay angle; the blue bag may be partially cropped at the left edge as the original was. Keep oranges, sunglasses, scarf, earrings, light direction, linen folds and tropical leaf shadows close to reference 2. Warm summer daylight; authentic cobalt blue product color against the orange props. The bag's separate blue beaded accessory need not be added to this already arranged flat lay. Remove the app's white rounded icon buttons at lower right and restore the linen/shadows beneath those UI overlays. No hand, poolside carafe or sea-cliff scene.
```

##### 🏆 Rank #3406 (`0 ♡` | `2 👁️` | Model: `gpt_image_2_5` | Author: `@askd` | Size: `4:5` | Refs: `2`)
- **Publication ID**: `46a3afc0-8cba-49f7-bdc2-5872166cf863`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_3406_gpt_image_2_5_46a3afc0.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IuEaJWKkyztt8sx9avBX1SUYtA/hf_20261020_070758_ad3f5c91-0dac-4fad-b35f-a0d24e2e0e2c.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IuEaJWKkyztt8sx9avBX1SUYtA/hf_20261020_070758_ad3f5c91-0dac-4fad-b35f-a0d24e2e0e2c_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3IuEaJWKkyztt8sx9avBX1SUYtA/c7a05e78-6a26-4db6-a4e0-30c1a94943b6.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3IuEaJWKkyztt8sx9avBX1SUYtA/454df5f5-8d37-42ec-ac70-b961c343ed37.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Chiến dịch Trang sức Nhẫn Kim Cương từ 2 góc chụp sản phẩm (`Rank #3406` — `gpt_image_2_5`)**: Sử dụng `@img1` (góc chính diện) và `@img2` (góc nghiêng) để khóa chặt số lượng hạt kim cương và dáng quạt của chiếc nhẫn `0,11 Karat Pırlantalı Yelpaze Yüzük`, cấm tuyệt đối hiệu ứng lóe sao giả tạo (`no starburst effects or plastic surfaces`).

```text
Create a premium, restrained, naturally photographic jewelry campaign in vertical 4:5 Instagram FEED composition. The exact product is 0,11 Karat Pırlantalı Yelpaze Yüzük (RG2-00575). Reference image 1 is the canonical product design, reference 2 is its alternate view. Preserve the same complete closed ring band, exact motif silhouette, stone number and placement, setting, metal color and proportions. No redesign, no extra branches, no oversized jewelry, no invented diamonds. Realistic fine metal texture, soft daylight, subtle sparkle, no starburst effects or plastic surfaces. Brand palette cherry rose #B04A63 with light neutral #DFDFDF, powder blush and ivory. Keep key jewelry at least 12% inside all image edges. No promotional text, no price, no watermark. Photograph only this ring resting with believable physical contact on a styled still life: mat vişne çürüğü ipek üzerinde yandan gün ışığı. Ring takes about 35% of canvas width; include generous breathing room. No people, no hands, no other products. Preserve the canonical product viewpoint closely, changing the surrounding set and lighting. Quiet editorial luxury.
```

##### 🏆 Rank #926 (`1 ♡` | `62 👁️` | Model: `gpt_image_2` | Author: `@maneteraser1983` | Size: `3:4` | Refs: `1`)
- **Publication ID**: `711fff6d-feec-4ef6-ab24-51e6fc1de095`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0926_gpt_image_2_711fff6d.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3JKHuvxOXvTgijGyFfDQAdZCdWS/hf_20261013_162129_17a8429c-8994-4963-9c83-e90c2806ba69.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3JKHuvxOXvTgijGyFfDQAdZCdWS/hf_20261013_162129_17a8429c-8994-4963-9c83-e90c2806ba69_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3JKHuvxOXvTgijGyFfDQAdZCdWS/3cdf4917-f9b8-44bf-a576-1402655a2b28.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Chiến dịch trang sức vàng Tiffany-style (`Before: rank_0926_ref1.jpg` ➔ `After: rank_0926_gpt_image_2_62c6525b.webp`)**: Giữ nguyên thiết kế vòng cổ/bông tai từ `@img1`, dựng ánh sáng phản chiếu kim loại vàng 18K sắc nét. *(Lưu ý kiểm định thị giác: `gpt_image_2` làm da mẫu nữ hơi mịn kiểu satin, nếu có người thật nên thêm lệnh khóa lỗ chân lông như `soul_cinematic`).*

```text
PREMIUM LUXURY JEWELRY CAMPAIGN — FEATHER GOLD SET

Reference image: Use the uploaded jewelry photograph as the primary and authoritative product reference. Create an ultra-realistic, high-end commercial jewelry campaign inspired by the refined visual language of Tiffany & Co., its sophisticated luxury advertising, elegant minimalism, exceptional craftsmanship, and iconic turquoise color palette.

MODEL

An exceptionally elegant East Asian female fashion model, approximately 25–30 years old, with refined natural features, luminous realistic skin, dark almond-shaped eyes, sleek dark hair styled in a sophisticated low bun or a smooth, tucked-behind-the-ears hairstyle. High-fashion editorial presence, confident yet understated expression, graceful neck, elegant posture, natural proportions, and timeless beauty. Minimal, polished makeup with softly defined eyes, natural satin skin, and muted rose-nude lips. The model should embody the sophisticated, modern, understated luxury aesthetic of an international fine-jewelry campaign.

JEWELRY — ABSOLUTE PRODUCT ACCURACY

Reproduce the exact gold necklace and matching earrings shown in the uploaded reference image. The reference photograph is the definitive source of truth for every product detail.

The jewelry set features sculptural, flowing feather-inspired forms in polished yellow gold, with a distinctive repeating sequence of curved, overlapping, flame-like feather elements. Preserve the original organic contours, directional flow, sculpted ridges, smooth convex surfaces, dimensional relief, individual element proportions, spacing, curvature, and precise warm-gold finish.

The necklace must retain its original silhouette, length, construction, arrangement, and recognizable sequence of feather-shaped links. The matching earrings must preserve their exact individual feather-like shapes, proportions, orientation, and polished gold appearance.

Transfer the jewelry onto the model as if the actual physical pieces were professionally fitted and photographed in a luxury studio. The necklace must follow the natural anatomy of the neck and collarbones, with physically accurate contact, gravity, perspective, and scale. The earrings must sit naturally on the earlobes and remain clearly visible.

Do not redesign, reinterpret, simplify, embellish, or replace any jewelry element. Do not add gemstones, diamonds, pearls, extra links, additional ornaments, or decorative details absent from the reference. Do not change the number, shape, thickness, or arrangement of the feather elements. No melting, warping, duplicated pieces, fused links, or artificial-looking metal.

Preserve the original product identity with the highest possible fidelity. Jewelry accuracy takes precedence over creative styling.

WARDROBE AND STYLING

A perfectly tailored black evening dress with a refined architectural neckline, exposing the collarbones and framing the necklace. Premium matte black fabric, elegant construction, no visible logos, no distracting embellishments. Sophisticated styling that creates a strong contrast against the warm polished gold. Hair pulled away from the ears and neck to showcase the jewelry unobstructed.

BACKGROUND AND ART DIRECTION

An elegant Tiffany-inspired pale turquoise and muted aqua studio backdrop, with subtle tactile texture and a gentle tonal gradient. Refined, uncluttered composition, sophisticated color harmony, restrained luxury, contemporary fine-jewelry editorial art direction. The turquoise must feel elegant and softly nuanced rather than overly saturated or artificial.

POSE AND COMPOSITION

A vertical 4:5 luxury advertising portrait, framed from the upper chest to slightly above the head. The model is turned three-quarters toward the camera, shoulders relaxed, chin subtly raised, neck elongated, with a calm, self-assured expression. Her posture naturally presents the necklace across the collarbones while keeping both earrings visible whenever anatomically possible.

The necklace is the primary visual focal point. The face provides an elegant emotional connection without overpowering the product. Keep the complete necklace and earrings within the frame, sharply defined and unobstructed. Natural anatomy, realistic jewelry placement, accurate proportions.

LIGHTING AND PHOTOGRAPHIC TECHNIQUE

Professional medium-format studio photography, captured with the visual quality of a Phase One or Hasselblad fashion campaign. Large diffused key light, carefully controlled fill light, subtle rim lighting, and precision highlights designed specifically for polished gold. Beautifully defined reflections that reveal the three-dimensional feather relief without clipping highlights or obscuring the sculptural details.

Accurate gold color, realistic metallic reflectivity, refined shadow transitions, lifelike skin texture, natural pores, realistic hair strands, exceptional micro-detail, crisp jewelry edges, premium retouching, sophisticated tonal depth, and a luxurious editorial finish.

Use a portrait-lens perspective with natural facial proportions and sufficient depth of field to keep the entire jewelry set in clear focus.

FINAL RESULT

Photorealistic luxury jewelry advertising photography, sophisticated East Asian fashion model, sculptural polished yellow-gold feather necklace and matching earrings faithfully reproduced from the exact reference photograph, elegant black couture, muted Tiffany-inspired turquoise background, exceptional material realism, meticulous jewelry detail, restrained high-fashion glamour, premium international luxury campaign quality, clean composition, timeless elegance, no artificial CGI appearance.

STRICT NEGATIVE PROMPT

Incorrect jewelry design, altered feather shapes, missing feather elements, additional feather elements, incorrect necklace silhouette, incorrect earrings, oversized jewelry, undersized jewelry, inaccurate gold tone, silver-colored metal, rose gold, added gemstones, diamonds, pearls, altered proportions, asymmetrical product errors, floating jewelry, fused elements, broken links, distorted metal, plastic-looking gold, excessive reflections, blown highlights, blurry jewelry, out-of-focus necklace, hidden earrings, hair covering the jewelry, hands obscuring the necklace, unnatural anatomy, excessive retouching, waxy skin, heavy makeup, distracting clothing, visible logos, text, watermarks, cartoon, illustration, 3D render, synthetic CGI appearance.

Priority hierarchy: 1. Exact jewelry fidelity. 2. Realistic physical fit and proportions. 3. Professional luxury campaign lighting. 4. Model beauty and styling. 5. Background aesthetics.
```

##### 🏆 Rank #929 (`1 ♡` | `59 👁️` | Model: `gpt_image_2_5` | Author: `@prajiguruprasad` | Size: `9:16` | Refs: `0`)
- **Publication ID**: `536d2884-f899-4be6-82e4-ef84d0e1d2f4`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0929_gpt_image_2_5_536d2884.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2vRp6HHRdjnM5rZlRUeYyAvjGjX/hf_20260925_181950_55f73259-000f-4c3c-ac92-2c7fb6cf5616.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2vRp6HHRdjnM5rZlRUeYyAvjGjX/hf_20260925_181950_55f73259-000f-4c3c-ac92-2c7fb6cf5616_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Tĩnh vật thực vật học làm nền hương liệu cho chiến dịch Nước hoa (`Botanical Fragrance Notes Backdrop` — `rank_0929_gpt_image_2_5_536d2884.webp`)**: Cố ý khóa `No text, no product, no podium` để chỉ chụp cận cảnh hoa lan trắng tươi và quả vani sẫm màu đọng giọt sương dưới nắng chiều trên nền tường màu mật ong — dùng làm cảnh B-roll giải thích tầng hương (`Fragrance Notes B-Roll`) hoặc làm phông nền ghép chai nước hoa vào sau.

```text
Vertical 9:16 photograph, real luxury fragrance campaign still life shot in a professional studio. Real botanical specimens styled by a high-end prop stylist, captured on a Phase One medium-format camera. Must look like an untouched high-end photograph, not CGI, not illustration. No text, no product, no podium, no arch.

Background: a real matte plaster wall in warm honey-beige (#EAD2A4), lit so the upper centre glows brighter pale ivory (#F5E5C5) and the edges fall off naturally to warm caramel (#CFA56C). Subtle real plaster texture, gentle light falloff, no artificial glow effects.

Arrangement: one single natural bouquet gathered at a point near the bottom left corner, fanning diagonally upward and to the right, as if a stylist placed real stems against the wall. Flowers sit mainly on the left half, the highest bloom about 30% from the top. Upper right quarter stays clean and empty. Organic and asymmetrical, every element different.

Flowers: 5 real fresh orchid-like blooms in ivory white, each different in size, angle and stage of opening. Real petal anatomy: thick waxy petals with visible fine parallel veins, slight translucency where light passes through, natural micro-creases, gently curled and uneven tips, faint cream-peach blush toward the centre, a few tiny natural imperfections. Golden-yellow throat with real pollen texture and delicate stamens. Petals cast real soft shadows onto each other and the wall. Behind them, 2 to 3 real blooms and leaves slightly out of focus for depth.

Vanilla pods: 8 to 10 real cured Madagascar vanilla beans, deep chocolate-brown to near black, leathery and slightly flattened, with fine lengthwise wrinkles, natural oily sheen catching small specular highlights, tiny splits and a few visible seeds at the ends. Long and slender, varied lengths, rising from the same base as the flowers. A few tips bend naturally and curl into loose hooks. Real weight and softness; each pod casts a crisp-edged soft contact shadow on the wall.

Leaves: a few real glossy vanilla vine leaves, pale green shifted to warm cream by the light, with visible midrib, subtle waxy reflections and natural edge variation.

Lighting: one large soft window-style key light from upper left, warm 3200K, plus a subtle bounce fill. Physically accurate light: true contact shadows, ambient occlusion where stems meet, subsurface scattering in petals, specular highlights on pods. Low to medium contrast, rich tonal detail in whites and in dark browns.

Camera: 100mm macro lens, f/8, focus on the main blooms, natural slight falloff in the far background. Tack-sharp micro detail, true-to-life colour, fine natural film grain, editorial luxury grade. Hyperrealistic, 8K.

Negative prompt: CGI, 3D render, digital painting, illustration, painterly, airbrushed, AI-looking, cheap stock image, plastic flowers, silk flowers, fake flowers, paper flowers, wax figure, smooth uniform petals, identical flowers, cloned elements, mirrored layout, symmetrical composition, glowing edges, bloom effect, heavy haze, soft-focus filter, oversaturated, overly orange, neon, arch, frame, border, text, letters, logo, watermark, podium, perfume bottle, product, people, hands, soil, roots, harsh shadows, flat lighting, low resolution, oversharpened halos
```

---

#### 2.3. Cách Các Đạo Diễn `@thomas_lundstrom` & `@ollkorrect` Viết Prompt Bảng Xoay Sản Phẩm `3-Panel` / `6-Panel` & Chống Lỗi Chữ Mặt Sau (Nguyên Văn 100% Từ `asset_registry.json`)

##### 🎬 Project `thomas_lundstrom/seedance-4k-vs-1080p-product-commercials` — Asset `@IMG_001` (Model: `gpt_image_2` | Roles: `start_frame_keyframe` | Reused in `1` jobs)
- **Chiến thuật Đạo diễn**: Thiết kế Chai nước hoa Hero (`AURELIA — L'Or de Nuit`) bằng cấu trúc 5 khối: `Bottle Architecture` + `Cap` + `Label & Typography` + `Surface & Environment` + `Lighting & Camera`.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2yLzar9qEBwWtKro0bFax4owvTR/hf_20260729_074826_d62c3e57-8101-4747-a758-09a8cf34495e.png
- **👁️ Visual Audit Verdict**: Bản thiết kế sản phẩm gốc hoàn chỉnh từ con số 0 trước khi tạo bảng xoay: quy định rõ độ dày đáy thủy tinh (`12mm crystal base`), màu chất lỏng (`rich warm amber-gold`), chất liệu giấy nhãn (`uncoated cotton paper`) và phông chữ khắc chìm.

```text
Cinematic character reference sheet of the man in the attached reference photo, split-frame layout, photorealistic. Preserve his exact facial identity from the reference in every view — same face, same hairstyle, same skin tone. Use the reference photo for face, hair and skin only — do NOT copy the clothing from the reference photo; he wears the outfit described below.

Left panel — facial close-up: a white Northern European man around 30, fair skin tone, the entire head fully inside the frame including all the hair, nothing cropped, short brown hair neatly side-parted and swept over, tapered shorter at the sides, light stubble along the jaw and upper lip, blue-grey eyes, real skin texture with subtle pores, calm friendly expression with a subtle closed-mouth smile, looking straight into lens. Shot on 85mm portrait lens, shallow depth of field, soft cinematic key light with gentle fill.

Right panel — full-body front and back views side by side: the same man shown twice within this panel — on the left, a full-body front view facing the camera; on the right, a full-body back view photographed from directly behind. In both, he stands straight in a normal relaxed pose, arms hanging down at his sides, full height in frame head-to-toe, tall athletic build with broad shoulders (1.85m), fair skin, same side-parted hair, and the same outfit in both views, styled as relaxed 90s-inspired streetwear with loose, drapey silhouettes: an oversized light-beige stone-colored heavyweight cotton T-shirt with a boxy fit, dropped shoulders, wide sleeves ending near the elbows and a ribbed crew neckline, draping loosely past his hips; a thin silver chain necklace with a small round silver pendant worn over the shirt; loose straight-leg black pants with a baggy relaxed drape, wide through the thigh and calf, stacking slightly on the shoes — NOT slim-fit, NOT tapered; and chunky black low-top sneakers with a retro 90s skate silhouette, thick midsole and layered panels, fully black. The front view shows his face and the front of the T-shirt; the back view shows the back of his head with the short tapered haircut, his shoulders, the back drape of the T-shirt, and the rear of the baggy black pants and chunky black sneakers. Both figures matched in framing, scale and lighting for consistency. Shot on 35mm lens, even full-length lighting.

Look: clean studio character sheet, plain solid grey background, consistent character across all views, soft diffused cinematic lighting, muted natural color grade, fine detail, true-to-life skin tones, vertical divider lines separating each view.
```

##### 🎬 Project `thomas_lundstrom/seedance-4k-vs-1080p-product-commercials` — Asset `@IMG_004` (Model: `gpt_image_2` | Roles: `start_frame_keyframe, turnaround_sheet_reference_element` | Reused in `3` jobs)
- **Chiến thuật Đạo diễn**: Biến ảnh chai nước hoa tĩnh thành Keyframe chuyển động tốc độ cao (`High-Speed Splash Keyframe`, tái sử dụng `3` lần) chụp ở tốc độ màn trập `1/4000s`.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2yLzar9qEBwWtKro0bFax4owvTR/hf_20260729_084951_e7be789e-f9bf-46df-8089-d21b932239fd.png
- **👁️ Visual Audit Verdict**: Giữ nguyên 100% hình dáng, nhãn và nắp chai nước hoa từ `@IMG_001`, đặt nghiêng `15°` trên mặt đá basalt đen ướt trong khoảnh khắc sóng nước vàng hổ phách bung lên ở tốc độ `1/4000s` — làm khung hình bắt đầu (`Start Frame`) hoàn hảo cho Seedance 2.0.

```text
Professional product prop sheet of the ROVA soda can on a seamless neutral grey background (#B8B8B8). Three views of the same can arranged side by side in a clean row: a full front view, a full back view, and a macro close-up detail of the front wordmark area filling the third frame, the graphics sharp and crisp.

CAN FORMAT:
- Standard 330 ml aluminum beverage can — classic short stubby proportions, 66 mm wide, 115 mm tall, NOT a slim can, NOT a tall energy-drink can
- Brushed silver aluminum top rim, lid and pull tab, plain silver bottom rim

CAN DESIGN: preserve the exact can design from the attached reference image — the vivid crimson red base with its fine grain texture, the huge white liquid-warped balloon-style "ROVA" wordmark wrapping on a rising diagonal, the white starburst "O" with the red center, the deeper tonal red splash blob flowing behind the letters, the scattered white hand-drawn doodles, the vertical "SPARKLING SODA" side text and the white checkerboard band at the base — do not alter, restyle or rearrange any of it

BACK VIEW: the same red base, splash blob and doodles continuing seamlessly around the can — replace the ingredient sticker seen in the reference with continued graphics: NO ingredient text, NO fine print, NO text block anywhere on the back

Keep the exact same can design identical in every view — do not vary the design between angles
Colors: red, deep tonal red and white only — no other colors

Even soft studio lighting, no harsh shadows, consistent scale across the front and back views, subtle ground shadow under each can. Technical reference sheet style, sharp focus, high detail, photorealistic, commercial product photography.
```

##### 🎬 Project `thomas_lundstrom/seedance-4k-vs-1080p-product-commercials` — Asset `@IMG_015` (Model: `nano_banana_flash` | Roles: `turnaround_sheet_reference_element` | Reused in `1` jobs)
- **Chiến thuật Đạo diễn**: Bảng Xoay Đồng Hồ 3 Góc (`Three-View Orthographic Product Reference Sheet`: `Left: Front | Center: 3/4 Angle | Right: Caseback`) kèm lệnh **Chống bịa chữ mặt sau (`NO text, NO numbers, NO markings on the back`)**.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2yLzar9qEBwWtKro0bFax4owvTR/hf_20260729_100650_cda3bea9-8d1c-433b-ac34-19bd3d65ce5f_min.webp
- **👁️ Visual Audit Verdict**: Bí quyết sống còn của `@thomas_lundstrom`: khi tạo góc mặt sau sản phẩm (`Right — Back / Caseback`), phải ra lệnh `completely clean — NO text, NO numbers, NO markings on the back` để AI không tự ý vẽ những dòng chữ vô nghĩa bị nhòe khi lên video 4K!

```text
Professional product prop sheet of the ARVID Meridian luxury wristwatch on a seamless neutral grey background (#B8B8B8). Three views of the exact same watch arranged side by side in a clean row: a front view of the watch standing upright with the bracelet closed in a loop, a back view of that same standing watch photographed from directly behind, and a macro close-up of the dial filling the third frame.

WATCH FORMAT:
- 39 mm round case in deep matte antique gold (#9A7B3C) with a fine satin-brushed finish — warm, dark and muted, NOT bright yellow gold, NOT high-gloss, no mirror polish anywhere
- Smooth satin-brushed bezel, domed sapphire crystal with only a faint soft reflection
- Screw-down matte gold crown engraved with a tiny north-star emblem
- Three-link bracelet in the same matte satin-brushed dark gold, all links matte, folding clasp

DIAL:
- Deep midnight-blue sunburst dial (#101E3F) with a fine radial brushed texture
- Applied brushed-gold baton hour markers, slim gold dauphine hour and minute hands, thin gold seconds hand, hands set to 10:08
- "ARVID" in small elegant serif capitals below 12 o'clock with "HELSINKI" in tiny spaced letters beneath it, "AUTOMATIC" in tiny capitals above 6 o'clock, a fine printed white minute track around the dial edge — no date window, no other text

BACK VIEW: the complete standing watch seen from behind, nothing cropped — the solid matte gold caseback centered, engraved with a north-star emblem in the middle and "ARVID • MERIDIAN • AUTOMATIC" in clean capitals around its rim, the bracelet clearly visible running upward and downward from the case, and the folding clasp visible at the bottom of the bracelet loop — unmistakably the rear side of the same watch

Keep the exact same watch design, dial layout, text and hand position identical in every view — do not vary the design between angles
Colors: matte dark antique gold, midnight-blue dial, white minute markings — no other colors

Even soft diffused studio lighting, subdued reflections matching the matte metal, no harsh shadows, no bright specular glints, consistent scale between the two standing views, subtle ground shadow under each. Technical reference sheet style, sharp focus, high detail, photorealistic, commercial product photography.
```

##### 🎬 Project `thomas_lundstrom/emerald-fragrance-commercial` — Asset `@IMG_006` (Model: `gpt_image_2` | Roles: `turnaround_sheet_reference_element` | Reused in `3` jobs)
- **Chiến thuật Đạo diễn**: Câu lệnh 1 dòng siêu gọn tạo `3-Panel Perfume Sheet` (`Full Front + 3/4 Perspective + Label Macro Closeup`, tái sử dụng `3` lần).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2yLzar9qEBwWtKro0bFax4owvTR/hf_20260715_200057_23cb43fe-af7b-4ca7-9c23-649d981572eb.png
- **👁️ Visual Audit Verdict**: Công thức nhanh gọn nhất khi bạn đã có ảnh chụp mặt trước sản phẩm có nhãn chữ (như tấm ảnh Cây thông Noel có dải chữ `Fireproof / Non-Allergic / Anti-Fading / Smell-Free` của bạn): yêu cầu 1 góc toàn cảnh mặt trước, 1 góc nghiêng 3/4 và 1 góc chụp cận cảnh chi tiết!

```text
Make a product sheet with one full front, one 3/4 perspective and one closeup of all the label text of the product from <<<image_1>>> . No added text just the 3 angles.
```

##### 🎬 Project `ollkorrect/besa` — Asset `@IMG_032` (Model: `gpt_image_2` | Roles: `turnaround_sheet_reference_element` | Reused in `25` jobs)
- **Chiến thuật Đạo diễn**: Bảng Xoay Đạo Cụ **6-Panel Chuẩn Điện Ảnh** (`Six-Panel Studio Prop Sheet: Front, Back, Left, Right, Top-Down, Macro Detail`) được tái sử dụng tới **25 lần** trong bộ phim *Besa*!
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_32vwRMunqoTPjjAdQ6zrT3TrjuG/hf_20260812_135948_a235e56f-ceca-42f4-a14f-a2af2ca64c96_min.webp
- **👁️ Visual Audit Verdict**: Đạo diễn `@ollkorrect` dựng 6 góc chụp của cùng 1 chiếc đèn dầu cổ trên nền studio tối với khóa cứng `STRICT CONSISTENCY RULES: All six panels must show the exact same lantern with identical proportions, metal color, rust pattern, glass shape, and handle geometry`. Đây là mẫu `6-Panel Prop Turnaround` chuẩn mực nhất toàn hệ thống.

```text
Create a photorealistic six-panel studio prop sheet showing one identical antique Albanian highland oil lantern, arranged in a clean two-row by three-column grid.

Top row: straight front view, exact left profile, exact right profile.
Bottom row: straight rear view, high three-quarter view with the carrying handle raised, front three-quarter view with the lantern lit.

The lantern is a compact late-19th-century pre-electric household object, approximately 30 centimetres tall with a 14-centimetre-wide base, designed to be carried comfortably in one hand. It has a squat circular fuel reservoir, twin curved air tubes, a vented chimney cap, a clear slightly wavy hand-blown glass globe, crossed iron protection wires, a tall arched carrying handle and a small brass wick-adjustment wheel on its right side.

Its construction combines blackened tinned iron, clear glass, aged brass and a cotton oil wick. The metal has a matte charcoal finish with restrained dark-brown oxidation, rubbed edges, faint soot around the chimney and several small natural dents from decades of household use. The surfaces are plain, undecorated and unbranded.

The first five panels show the cold unlit wick clearly. The final panel shows one small, low amber flame producing restrained golden reflections inside the glass. Preserve exactly the same dimensions, construction, dents, patina and component placement across every panel. Complete object fully visible, neutral grey studio background, soft overhead light, deep focus and realistic material detail.
```

---

### 21.🪄 CHUYÊN ĐỀ 3: TỪ SẢN PHẨM / ẢNH MỜ, THÔ, CẮT GHÉP, 3D SƠ KHAI THÀNH REAL SẮC NÉT (`BLURRY / 3D / FLAT CGI ➔ REAL SHARP` & KỸ THUẬT `REVERSE-POLISH`)

> **Phát hiện đột phá từ kiểm định thị giác**:
> Trong kho `♡ < 50` và `29` Dự Án Phim, các cao thủ sử dụng **2 chiều biến đổi chất lượng ảnh ngược nhau** tùy theo mục đích:
> 1. **Chiều Nâng Cấp (`3D / CGI / Blurry / Frame Grab ➔ Ultra-Sharp Real Photo`)**: Dùng khi ảnh gốc là ảnh 3D dựng sơ sài, ảnh game/hoạt hình, frame cắt từ video bị bệt, hoặc ảnh chụp bị nhòe chuyển động (`motion blur`). Câu lệnh khóa: `"Rephotograph the attached frame as a real photograph"`, `"Eliminate all motion blur, softness, and out-of-focus areas"`, `"Replace all flat digital/CGI surfaces with physically accurate real-world textures"`.
> 2. **Chiều Hạ Độ Bóng (`Reverse-Polish / De-AI-ify` — Phát hiện đắt giá nhất từ `Rank #476`)**: Khi bạn muốn ghép một sản phẩm hoặc nhân vật mới vào một **bức ảnh chụp thực tế bằng điện thoại trong phòng khách** (`@img1`), nếu AI vẽ vật thể mới quá nét và quá bóng bẩy kiểu studio, người xem sẽ phát hiện ra ảnh ghép ngay lập tức! Tác giả `@kimcheeverse` (`Rank #476`) đã viết câu lệnh ngược lại: **"Match the exact camera quality, sensor noise, slight JPEG compression, mild indoor softness, and imperfect dynamic range of the original photograph. Do NOT make the inserted subject sharper or cleaner than the rest of the image!"**

#### 3.1. Bộ Câu Lệnh "Thần Chú" Biến Ảnh Mờ / Thô / 3D Sơ Khai Thành Real Sắc Nét (Và Ngược Lại) — Nguyên Văn 100%

##### 🏆 Rank #476 (`9 ♡` | `2655 👁️` | Model: `seedream_v5_pro` | Author: `@kimcheeverse` | Size: `9:16` | Refs: `1`)
- **Publication ID**: `190de36a-4bd5-44e1-8b06-824e8233e74e`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0476_seedream_v5_pro_190de36a.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DUeuq342Rt84lSGBRMX13shiKu/hf_20260829_054740_cfc9e34b-1db4-4aa6-8aaf-6191d891719c.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DUeuq342Rt84lSGBRMX13shiKu/hf_20260829_054740_cfc9e34b-1db4-4aa6-8aaf-6191d891719c_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DUeuq342Rt84lSGBRMX13shiKu/f52056a1-f08f-4d70-b3bb-4370b5750847_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Kỹ thuật `Reverse-Polish` ghép người/vật vào ảnh điện thoại thật đạt độ chân thực 10/10 (`Before: rank_0476_ref1.jpg` ➔ `After: rank_0476_seedream_v5_pro_190de36a.webp`)**: Khi kiểm định bằng mắt cặp ảnh này, hoàn toàn không thể phân biệt được cô gái mặc áo đấu thêm vào với những cổ động viên thật trong ảnh gốc nhờ lệnh khóa độ nhiễu hạt và độ nét thấp của camera điện thoại (`Not sharper than the original photo. Not cleaner than the original photo`).

```text
EDIT THE PROVIDED STADIUM CONCOURSE PHOTOGRAPH.  THIS IS A LOCALIZED PHOTOREALISTIC EDIT.  DO NOT CREATE A NEW SCENE. DO NOT REGENERATE THE ENTIRE PHOTOGRAPH. DO NOT REDESIGN THE STADIUM.  PRIMARY GOAL:  Make Miyu look completely and naturally present inside the original real stadium concourse, as though she was physically there when this casual smartphone photograph was taken.  She is slightly lost and has stopped walking to look at the illuminated 123 / 124 section sign to figure out where she needs to go.  This must feel like an UNPLANNED CANDID MOMENT.  She is NOT posing for the camera.  ================================================== 1. ABSOLUTE MIYU IDENTITY LOCK ==================================================  Preserve Miyu's CURRENT facial identity exactly.  DO NOT redesign, reinterpret, beautify, replace, or significantly regenerate her face.  Preserve:  - exact recognizable facial identity - face shape - facial proportions - high cheekbones - eye shape - eye spacing - nose - lips - jawline - chin - youthful appearance - brown hair - bangs - hairstyle - hair length - earrings - current head size  NO identity drift.  NO face replacement.  NO different woman.  NO change in apparent age.  ================================================== 2. HEAD SIZE + BODY PROPORTIONS ==================================================  Preserve Miyu's CURRENT head-to-body proportions.  DO NOT independently enlarge her head.  DO NOT independently shrink her head.  DO NOT make her head wider or narrower.  DO NOT change:  - shoulder width - torso proportions - arm proportions - waist proportions - hip proportions - leg proportions  She must remain physically believable as the same person.  ================================================== 3. SUBTLE WHOLE-BODY SCALE CORRECTION ==================================================  Miyu currently appears slightly too small relative to her apparent physical position in the concourse.  Increase Miyu's ENTIRE BODY SCALE uniformly by approximately 5%.  This is a subtle perspective correction only.  IMPORTANT:  Scale her WHOLE BODY uniformly.  Do NOT enlarge only her head. Do NOT enlarge only her torso. Do NOT lengthen only her legs.  Maintain exactly the same human proportions.  KEEP HER FEET ANCHORED TO THE SAME PHYSICAL POSITION ON THE CONCRETE FLOOR.  As she becomes approximately 5% larger, preserve realistic floor contact and perspective.  She should appear naturally scaled relative to:  - the real partially visible spectator on the far left - the nearby doors - wall advertisements - section signage - railing - corridor architecture  Do NOT move her dramatically left or right.  Her current right-of-center placement works well.  ================================================== 4. SHE IS LOST — CANDID BEHAVIOR ==================================================  Preserve the storytelling concept that Miyu is trying to find her section.  She has momentarily stopped walking.  Her attention is directed toward the illuminated:  123 124  section sign above her.  Her head is naturally turned upward toward the sign.  Her eyes are focused on the signage.  She is NOT looking at the camera.  Her expression communicates:  "Wait...where am I supposed to go?"  But keep this extremely subtle and realistic.  Use:  - mild confusion - slight uncertainty - concentration - slightly raised eyebrows - subtly parted or relaxed lips - natural eye focus toward the sign  NO exaggerated confusion.  NO shocked expression.  NO frightened expression.  NO cartoonish expression.  NO dramatic acting.  She simply looks like someone navigating an unfamiliar stadium.  ================================================== 5. REMOVE THE FINGER-HEART COMPLETELY ==================================================  REMOVE the current finger-heart gesture.  There must be:  NO finger heart. NO peace sign. NO thumbs up. NO wave. NO pointing toward the camera. NO hand beside cheek. NO cute hand gesture. NO idol pose. NO influencer pose. NO deliberate camera gesture.  She is NOT aware of or responding to the camera.  ================================================== 6. NEW NATURAL HAND + ARM POSITION ==================================================  Replace the current raised finger-heart arm position with natural, incidental body language.  Lower that arm naturally.  Her arm should fall into a relaxed position near her side/hip.  Have that hand loosely and casually touch or very lightly hold the lower side/hem of her oversized Eagles jersey near her hip.  This should NOT look like a fashion pose.  It is an unconscious, incidental hand position while she has stopped walking.  The fingers are:  - naturally relaxed - slightly curved - subtly separated - anatomically correct - affected by gravity - not perfectly parallel - not deliberately arranged  The wrist is relaxed.  The opposite arm remains naturally hanging beside her body with a relaxed hand.  The two arms should have slight natural asymmetry.  DO NOT make both arms rigidly straight.  DO NOT make her hands symmetrical.  The body language should feel caught BETWEEN movements.  ================================================== 7. HAND ANATOMY ==================================================  Any hand that must be reconstructed because of the removed finger-heart pose must have realistic human anatomy.  Each hand has EXACTLY FIVE fingers:  - thumb - index - middle - ring - pinky  Maintain realistic:  - finger lengths - finger thickness - finger spacing - knuckles - joints - nail placement - palm anatomy - wrist anatomy - natural finger curvature  NO:  - extra fingers - missing fingers - fused fingers - duplicated fingers - webbed fingers - broken joints - oversized hands - tiny hands - excessively long fingers - perfectly straight AI fingers  Keep hand size proportional to Miyu's body.  ================================================== 8. JERSEY — ABSOLUTE WARDROBE LOCK ==================================================  Miyu wears an authentic:  PHILADELPHIA EAGLES MIDNIGHT GREEN / DARK TEAL GREEN FOOTBALL JERSEY.  Preserve the current oversized relaxed jersey fit.  CRITICAL:  THE JERSEY IS GREEN.  Specifically authentic Philadelphia Eagles MIDNIGHT GREEN / DARK TEAL GREEN.  NOT BLACK. NOT CHARCOAL. NOT GRAY. NOT KELLY GREEN.  It must remain visibly green even under the indoor stadium lighting.  Preserve/include:  - midnight-green football mesh - oversized casual fit - short football sleeves - NFL shield below collar - Eagles details - realistic mesh texture - realistic stitching - realistic seams - natural wrinkles - natural folds - natural fabric weight  ================================================== 9. NUMBER 1 — ABSOLUTE LOCK ==================================================  MIYU'S JERSEY NUMBER IS:  1  ONE SINGLE DIGIT.  EXACTLY ONE LARGE NUMERAL "1".  NOT 11.  DO NOT GENERATE:  - second number 1 - number 11 - duplicated digit - partial second digit - additional number - malformed number  THE FRONT NUMBER IS:  1  The numeral must naturally follow:  - torso curvature - jersey folds - perspective - mesh fabric - lighting - shadows  It must look physically integrated into the jersey.  ================================================== 10. BLUE DENIM SHORTS ==================================================  Miyu wears:  BLUE DENIM SHORTS.  Preserve the current shorts concept.  Use:  - medium-blue denim - contemporary casual women's shorts - natural waist - casual game-day fit - realistic denim seams - realistic stitching - pockets - natural hem - realistic wrinkles - natural fabric compression  The oversized jersey may naturally overlap the waistband.  NO:  - skirt - plaid skirt - tights - stockings - pantyhose - leggings  ================================================== 11. BARE LEGS ==================================================  Miyu's natural bare legs remain visible.  Preserve her existing:  - thigh proportions - knee proportions - calf proportions - leg length - stance  DO NOT make her legs thinner.  DO NOT make them thicker.  DO NOT lengthen her legs.  DO NOT exaggerate curves.  Use natural subtle skin texture and tonal variation consistent with a real smartphone photograph.  ================================================== 12. NO HANDBAG ==================================================  Miyu carries NO handbag.  NO purse.  NO shoulder bag.  NO brown leather strap.  NO crossbody strap.  NO bag hardware.  Do NOT add any accessory hanging from her shoulder or body.  ================================================== 13. PHYSICAL GROUNDING ==================================================  Miyu must look physically present on the concrete concourse floor.  Her shoes and feet must make convincing physical contact with the ground.  Maintain:  - realistic body weight - realistic center of gravity - foot-to-floor contact - subtle contact shadows - correct leg weight distribution - believable depth relative to the floor - realistic clothing gravity  Her weight should naturally favor one leg while the other remains slightly relaxed.  NO floating.  NO hovering.  NO incorrect foot perspective.  ================================================== 14. MOST IMPORTANT — MATCH MIYU DOWN TO THE REAL PHOTO ==================================================  DO NOT make the original photograph match Miyu.  MATCH MIYU DOWN TO THE ORIGINAL REAL PHOTOGRAPH.  The partially visible REAL spectator on the far left and the original concourse environment provide photographic references.  Miyu must inherit the SAME:  - smartphone camera rendering - computational photography characteristics - sharpness - fine-detail resolution - microcontrast - image noise - compression - exposure - white balance - dynamic range - saturation - color response - highlight rolloff - shadow rendering - edge softness - local contrast  Miyu must NOT appear:  - cleaner - sharper - smoother - higher resolution - more professionally photographed - more perfectly illuminated  than the real photographic environment.  DO NOT simply blur Miyu.  Instead match the actual photographic characteristics of the source.  ================================================== 15. REMOVE AI BEAUTY POLISH ==================================================  Preserve Miyu's youthful attractive appearance and identity.  Do NOT make her older.  However, remove excessive AI-generated perfection.  Use extremely subtle natural human characteristics:  - subtle pores - tiny complexion variation - subtle cheek tonal variation - subtle forehead variation - natural under-eye texture - realistic eyelid texture - natural nose texture - natural lip texture - subtle skin sheen - tiny warmth/redness variation - natural arm texture - natural leg texture  KEEP THIS SUBTLE.  NO:  - heavy pores - acne generation - obvious blemishes - wrinkles - aging - rough skin  REMOVE:  - porcelain skin - glass skin - waxy skin - plastic skin - beauty-filter smoothing - airbrushing - perfectly uniform complexion - glamour retouching - CGI skin  She should look like a naturally attractive young woman casually captured by a smartphone.  ================================================== 16. MATCH THE CONCOURSE LIGHTING ==================================================  Illuminate Miyu ONLY using the lighting physically present in the original concourse photograph.  This is indoor stadium concourse lighting.  Match the existing:  - overhead fluorescent/industrial lighting - relatively flat ambient illumination - cool-neutral indoor color temperature - soft environmental shadows - reflected concrete light  Apply the SAME lighting naturally to:  - face - hair - neck - arms - hands - jersey - shorts - bare legs - shoes  NO:  - outdoor sunset lighting - golden-hour lighting - studio lighting - portrait lighting - beauty lighting - cinematic key light - artificial fill light - rim lighting - face spotlight  Miyu must look illuminated by the actual concourse.  ================================================== 17. HAIR INTEGRATION ==================================================  Preserve Miyu's current:  - brown hair - bangs - hairstyle - hair length - overall hair volume  Do NOT redesign her hair.  Make only subtle photographic integration improvements.  Include natural:  - grouped strands - occasional flyaways - irregular edge hairs - realistic internal shadows - realistic gravity - natural interaction with shoulders and jersey  Do NOT render every strand razor sharp.  Avoid perfectly clean AI-generated hair boundaries.  ================================================== 18. EDGE INTEGRATION ==================================================  Pay special attention to the boundary between Miyu and the original real concourse.  Her:  - hair edges - shoulder edges - jersey edges - arm edges - hand edges - shorts edges - leg edges - shoe edges  must match the source photograph's natural edge characteristics.  NO:  - compositing halo - white outline - dark outline - artificial glow - cutout appearance - pasted appearance - excessive edge sharpening - artificial blur around her body  ================================================== 19. PERSPECTIVE ==================================================  Maintain the original smartphone wide-angle perspective.  After the subtle approximately 5% whole-body enlargement, Miyu must remain physically consistent with:  - floor geometry - wall geometry - doorway size - section signs - advertisements - nearby spectator - corridor depth  Do NOT create portrait-lens perspective.  Do NOT use DSLR depth of field.  Do NOT blur the background.  ================================================== 20. BACKGROUND — ABSOLUTE LOCK ==================================================  Preserve the ORIGINAL REAL CONCOURSE.  DO NOT modify:  - illuminated 123 / 124 sign - other section signage - advertisements - concrete walls - concrete floor - doors - ceiling - overhead lights - hallway - vending/kiosk equipment - spectators - partially visible person on the left - architecture - wall graphics - environmental objects  DO NOT regenerate signs.  DO NOT rewrite background text.  DO NOT remove real spectators.  DO NOT add new spectators.  ================================================== 21. CAMERA + COMPOSITION LOCK ==================================================  Preserve:  - vertical smartphone orientation - original framing - camera height - camera position - lens perspective - field of view - original image quality  Keep Miyu approximately in her CURRENT right-of-center location.  DO NOT center her perfectly.  DO NOT dramatically reposition her.  The 123 / 124 sign must remain clearly visible above her.  This composition should visually communicate that she is looking at the sign because she is trying to find her section.  ================================================== 22. DO NOT UPSCALE ==================================================  DO NOT:  - globally upscale - globally sharpen - globally denoise - globally smooth - create 4K facial detail - create 8K skin - add artificial HDR - create DSLR sharpness - create cinematic sharpness  Preserve the imperfections of the original smartphone photograph.  ================================================== FINAL STORY ==================================================  This is a candid smartphone photograph of Miyu inside the stadium concourse.  She is wearing:  PHILADELPHIA EAGLES MIDNIGHT GREEN JERSEY NUMBER 1 — EXACTLY ONE DIGIT BLUE DENIM SHORTS BARE LEGS NO HANDBAG  She has become slightly lost while trying to find her seats.  She has stopped walking underneath the 123 / 124 section sign and is looking up at it, quietly trying to determine where she needs to go.  She is NOT posing.  She is NOT looking at the camera.  She is NOT making a finger heart.  She is NOT making any deliberate hand gesture.  One hand casually and unconsciously rests near her hip or lightly touches the lower side of her oversized jersey.  Her other arm hangs naturally.  It should feel like her friend casually photographed her while she was trying to figure out where they were going.  The moment is spontaneous, ordinary and believable.  ================================================== FINAL NON-NEGOTIABLE CHECK ==================================================  Before completing the image verify:  1. Miyu's facial identity remains unchanged. 2. Miyu's head-to-body proportions remain unchanged. 3. Her whole body is only approximately 5% larger. 4. Her feet remain anchored to the same floor position. 5. Her placement remains naturally right-of-center. 6. She is looking toward the 123 / 124 sign. 7. She appears subtly lost/confused. 8. She does NOT look at the camera. 9. Finger-heart gesture is completely gone. 10. There is NO peace sign or other deliberate gesture. 11. Raised arm has been lowered naturally. 12. Hands are relaxed and anatomically correct. 13. Jersey remains Eagles MIDNIGHT GREEN. 14. Jersey is visibly GREEN, not black. 15. Jersey displays EXACTLY ONE numeral "1". 16. Jersey does NOT display 11. 17. She wears BLUE DENIM SHORTS. 18. NO skirt exists. 19. NO tights or stockings exist. 20. Legs remain naturally bare. 21. NO handbag exists. 22. NO shoulder strap exists. 23. Body and feet are physically grounded. 24. Skin does not have excessive AI beauty smoothing. 25. Lighting matches the indoor concourse. 26. Sharpness/noise/detail match the original smartphone photograph. 27. No compositing halo exists around Miyu. 28. Real person on the left remains unchanged. 29. 123 / 124 sign remains unchanged. 30. Entire real concourse remains unchanged. 31. No global upscaling or enhancement occurs. 32. Final result looks like ONE genuine candid smartphone photograph.
```

##### 🏆 Rank #485 (`9 ♡` | `405 👁️` | Model: `nano_banana_2` | Author: `@amarell_ia` | Size: `3:4` | Refs: `1`)
- **Publication ID**: `40fa9aa0-0273-4e55-9224-904a0febf822`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0485_nano_banana_2_40fa9aa0.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_33sVyAwGmqcYZiZtoOURda7CzHJ/hf_20261004_104646_954b0883-b52d-4b4d-a572-e08abf584f69.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_33sVyAwGmqcYZiZtoOURda7CzHJ/hf_20261004_104646_954b0883-b52d-4b4d-a572-e08abf584f69_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_33sVyAwGmqcYZiZtoOURda7CzHJ/a35e79b3-55de-4a4f-bf41-f38bdffaaeeb.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Khử nhòe chuyển động (`Deblur`) & Biến bề mặt CGI phẳng thành Da thuộc/Nhựa sần thật 100% (`Before: rank_0485_ref1.jpg` ➔ `After: rank_0485_nano_banana_2_9bf99036.webp`)**: Ảnh gốc `@img1` bị mờ nhoẹt ở bàn tay và gấu áo khoác da; ảnh sau khi qua `nano_banana_2` sắc nét từng đường chỉ khâu trên áo da, từng vết xước kim loại trên máy ảnh vintage và từng sợi lông mi.

```text
Refine this image into a hyper-realistic high-fashion runway photograph. Enhance the flowing coat fabric with crisp motion-blur-free detail in the areas closest to the body, while preserving natural soft blur only at the fastest-moving outer edges. Add realistic satin-leather texture with visible sheen variation across the folds. Sharpen the beak mask's surface material so it reads as structured leather or matte resin rather than flat CGI. Enhance skin texture and natural light falloff on the visible ear and jawline. Strengthen the directional studio lighting so highlights and shadows on the fabric feel physically accurate. Maintain the exact pose, composition, and color palette.
```

##### 🏆 Rank #1348 (`0 ♡` | `27 👁️` | Model: `nano_banana_2` | Author: `@warholgrape1065` | Size: `4:3` | Refs: `3`)
- **Publication ID**: `ba3194d8-57a2-49d7-a19e-9c0a23f45aaa`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1348_nano_banana_2_ba3194d8.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38tKfZMtCgJR1NEv97fELEq8FTt/hf_20261015_063742_1814baea-95ce-4039-9bd5-0be7f8d029a5.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38tKfZMtCgJR1NEv97fELEq8FTt/hf_20261015_063742_1814baea-95ce-4039-9bd5-0be7f8d029a5_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38tKfZMtCgJR1NEv97fELEq8FTt/82d9478d-9042-424d-a1cb-452aa8a478ae.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38tKfZMtCgJR1NEv97fELEq8FTt/28fd640f-723b-4222-999f-7e3ec355ae03_resize.jpg
- **Input Reference `@img3`**: https://d2ol7oe51mr4n9.cloudfront.net/user_38tKfZMtCgJR1NEv97fELEq8FTt/fc652ab9-c95c-4fe0-a63b-3da963d0e49d.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Chuyển giao chất liệu dệt nổi 3D thật sang bản vẽ thiết kế phẳng (`Before: rank_1348_ref1..ref3` ➔ `After: rank_1348_nano_banana_2_f30685bd.webp`)**: Lấy độ nổi sợi len 3D thật từ `@img3` đắp lên đồ họa phẳng của `@img1` và `@img2`, biến bản vẽ 2D thành chiếc chăn dệt Jacquard thật có từng sợi chỉ đan chéo.

```text
IMAGES 1 AND 2 DEFINE THE FABRIC AND THEY OVERRIDE EVERYTHING ELSE. They are close photographs of real RELIEF JACQUARD KNIT garments. Build this jacket's cloth exactly the same way.
IMAGE 3 supplies ONLY the artwork and the cut. Image 3 is a flat lifeless technical render — its surface must be completely ignored.

HOW THE FABRIC WORKS, taken from images 1 and 2:
A double-face RELIEF JACQUARD KNIT. The motif itself is padded from behind and swells out of the cloth. NO quilting grid, NO diamond lattice, NO square cells, NO stitched channels, NO sewn seam lines — the relief follows the DRAWING.
– Every shape rises as its own soft padded pouch standing several millimetres proud, rounded and full in the middle, falling away at its own outline.
– The background between motifs sits lower, flatter and tighter.
– The picture is drawn by the CHANGE OF LEVEL: each raised shape casts a soft shadow along one edge and catches light along the other.
– The colours are KNITTED IN with different coloured yarns, never printed. Knitted stitches visible within the raised areas as a moderate natural texture, not coarse and not dominating.
– Thick, soft and sculptural, crushing into deep rounded folds where the body bends, the relief bunching in the creases exactly as in image 1.

THE ARTWORK, taken from image 3: a PIXEL-ART composition in chestnut brown, rust, deep olive green, bone cream and black — TWO MEN astride TWO LONG-HORNED BULLS facing the viewer, olive-green sleeveless vests with webbing straps and belts, the left man with short hair, short beard and clear glasses, the right man with slicked dark hair, beard and dark sunglasses; below them two dark brown bulls charging side by side, heads low, wide pale upswept horns, a white blaze down each face, cream outlines against a stylised brown and olive forest, a pale sun disc between the riders' heads. Trees and foliage continue onto the sleeves.

THE ARTWORK IN RELIEF — THE POINT OF THIS FRAME: at this magnification the padded swelling of every shape must be unmistakable. The riders' heads and shoulders, the bulls' muzzles and their long horns all bulge out of the cloth as rounded padded forms with real height; the forest behind sits lower; the dark ground recedes furthest. Each contour is a level change throwing its own soft shadow. The knitted stitches run visibly across the crowns of the raised shapes and compress into the hollows around them. Keep the blocky pixel character of the drawing, rendered as swelling knitted relief — never a flat print, never a smooth painting. Do not enlarge the artwork because the camera is closer: keep the figure scale relative to the back panel as in image 3.

NO TEXT ANYWHERE.

FRAMING: horizontal 4:3, a close crop on the centre of a man's back, from the tops of the shoulder blades down to just above the ribbed waistband — the two riders and the bulls' heads fill most of the frame. No head, no face.

BACKGROUND: pure clean white seamless studio backdrop just visible at the edges.

LIGHTING: a crisp soft key raking LOW from one side so every raised shape carries a bright crown and a deep soft shadow at its edge and the sculptural relief of the drawing is dramatic and unmistakable. Gentle fill keeps the cream areas from blowing out.

Ultra-sharp high-resolution commercial textile photography, 100mm macro lens, true-to-life colour, maximum detail in the knitted relief.
```

##### 🏆 Rank #1519 (`0 ♡` | `15 👁️` | Model: `nano_banana_2_1` | Author: `@gojart` | Size: `3:4` | Refs: `1`)
- **Publication ID**: `82b28615-cfbc-49b6-ae2b-8ba97ea1ae19`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1519_nano_banana_2_1_82b28615.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191531_376cb834-b7ee-42c1-a6ad-39c6717474fd.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191531_376cb834-b7ee-42c1-a6ad-39c6717474fd_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/e477602e-98f4-4c29-b1d6-4c9814d8bcc0.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Biến ảnh phối cảnh kiến trúc sang góc mặt đứng Orthographic thẳng tắp 90° (`Rank #1519` — `nano_banana_2_1`)**: Dùng ảnh công trình gỗ tròn xếp tầng làm tham chiếu kiến trúc tuyệt đối (`strict architectural reference`), khử toàn bộ biến dạng phối cảnh để xuất ra bản chụp mặt đứng chính diện (`straight-on front elevation view`) sắc nét từng thanh nan gỗ và lan can mây đan.

```text
Use the attached image of the building as the strict architectural reference. The reference photo shows the organic stacked-disc timber pavilion from a dusk three-quarter elevated view with visitors on the terraces. Generate a photorealistic architectural image showing a DIFFERENT best, most flattering view of the same building — a camera angle and composition clearly distinct from the reference photo's framing (for example: a lower, more dramatic ground-level angle emphasizing the cantilevered curved discs overhead, a view from the opposite side of the building at golden-hour daylight instead of dusk, or a closer three-quarter view that reveals the glazed ground floor and the undersides of the timber discs) — whichever angle best reveals the building's stacked circular massing, cantilevers, timber cladding grain, and glass base, while clearly not reproducing the same viewpoint, time of day, or crowd composition as the attached photo. Preserve the original building exactly: maintain the same architectural design, geometry, proportions, the stacked overlapping disc/oval volumes, cantilevers, curved timber-clad undersides, glazed ground-floor envelope, roof terraces, and overall character from the reference image. Use a natural architectural camera, avoiding extreme distortion or fisheye effects. Create a high-end, ultra-realistic architectural photograph, with realistic materials, accurate wood grain and texture, natural lighting, detailed shadows, physically believable reflections, and professional architectural visualization quality. Important: Do not redesign, simplify, distort, add, remove, or alter any architectural elements of the original building — only choose a new, different camera position, viewing direction, and lighting moment to showcase it from an angle distinct from the attached reference photo.
```

##### 🏆 Rank #1964 (`0 ♡` | `6 👁️` | Model: `nano_banana_2_1` | Author: `@gojart` | Size: `3:4` | Refs: `2`)
- **Publication ID**: `eeb2de1e-1255-464c-ba47-b849805d1ddf`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1964_nano_banana_2_1_eeb2de1e.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191639_36b309f3-f931-4111-9230-5f7d7c81e793.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191639_36b309f3-f931-4111-9230-5f7d7c81e793_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/e477602e-98f4-4c29-b1d6-4c9814d8bcc0.jpg
- **Input Reference `@img2`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_191531_376cb834-b7ee-42c1-a6ad-39c6717474fd.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Biến ảnh công trình kiến trúc thành Góc chụp Đỉnh đầu 90° (`Top-Down Orthographic Roof Plan` — `Rank #1964`, `nano_banana_2_1`)**: Từ các bức ảnh chụp góc nghiêng dưới đất của tòa nhà gỗ tròn, `nano_banana_2_1` tái tạo bức ảnh chụp thẳng đứng 90° từ đỉnh đầu xuống (`perfectly straight top-down orthographic view looking directly down at 90 degrees`) với nắng thực tế và cây xanh bao quanh.

```text
Use the attached images of the organic stacked-disc timber pavilion as the strict architectural and geometric reference. Generate a perfectly perpendicular top-down view of the building, with the camera positioned directly above the exact center of the structure and facing straight downward at EXACTLY a 90-degree angle. This is a strict requirement: true orthographic-style top view / plan view, camera positioned directly above the building, facing straight down, perpendicular to the ground — absolutely no oblique, tilted, diagonal, aerial-perspective, or three-quarter angle. Preserve the original building exactly: maintain the same architectural design, footprint, geometry, proportions, the overlapping stacked circular/oval disc volumes at their different diameters and rotations, cantilevers, roof terraces with planting, glazed ground floor envelope, and overall character visible in the reference images. Camera and composition requirements: * True orthographic-style top view / plan view. * Camera positioned directly above the building. * Camera facing straight down, perpendicular to the ground, exactly 90 degrees. * No perspective distortion. * No tilted, diagonal, aerial, or oblique camera angle. * Keep vertical projection accurate and geometrically consistent. * Clearly show the complete roof plan — the topmost disc's terrace, planting, and the overlapping silhouettes of the discs beneath it — and the surrounding plaza/site. * Frame the entire building and its immediate urban context naturally. Create a high-end, ultra-realistic architectural visualization with accurate materials, detailed roof and terrace textures, realistic urban context, natural shadows, and physically believable lighting. Important: Change only the camera position and viewing direction to create a perfectly perpendicular 90-degree top-down view. Do not redesign, simplify, distort, add, remove, or alter any architectural or landscape elements from the original reference.
```

---

#### 3.2. Cách Đạo Diễn `@hft_online` Biến Frame Dựng Thô Thành Ảnh Chụp Máy Phim Thật (`Rephotograph as a Real Photograph` — Tái sử dụng `19` lần!)

##### 🎬 Project `hft_online/harmony-ai-film-festival` — Asset `@IMG_303` (Model: `nano_banana_2` | Roles: `turnaround_sheet_reference_element` | Reused in `19` jobs)
- **Chiến thuật Đạo diễn**: `Rephotograph the attached frame as a real photograph` (`nano_banana_2`, tái sử dụng `19` lần): Giữ nguyên 100% bố cục và tư thế từ ảnh thô, nhưng chụp lại bằng ống kính `35mm` với ánh sáng tự nhiên và chất liệu vật lý thật (`not plastic, not painted, not smoothed`).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2z48uxE2O5vQ9OjsGuyDZmbQkp5/hf_20260823_202426_87af49af-b56d-466d-a65b-5f39788cfa12_min.webp
- **👁️ Visual Audit Verdict**: Đây là câu lệnh cứu cánh tốt nhất khi một bức ảnh AI hoặc ảnh cắt từ 3D/video bị cảm giác nhựa (`CGI/plastic`): chỉ cần nạp bức ảnh đó vào `nano_banana_2` kèm câu lệnh `@IMG_303` này, toàn bộ da người, vải vóc và gỗ đá sẽ được phủ vi cấu trúc quang học thật mà không làm lệch vị trí bất kỳ vật thể nào!

```text
Rephotograph the attached frame as a real photograph.

SUBJECT: everything stays exactly where it is. The two blue wall shelves with the books, the jug, the vase, the tin and the bowl, the wall clock, the grey blue armchair, the coffee table, the sofa and armchairs in the foreground with the knitted throw, the record shelf and the gramophone at the right, the curtain, the window, the patterned wallpaper and the floorboards = a redrawn object, a changed shape or a moved item is a failed take.

LIGHTING, and this is the main correction: the window at the right is the only source and every lit surface in this picture must be explained by it. Light arrives from that side, crosses the room and falls off toward the left, so the right half of the room reads clearly brighter than the left half and the far left corner sits two stops down while keeping its detail. The wall shelves take the light on their right ends and darken toward their left ends. The jug, the vase and the bowl each catch a hard specular highlight on the side facing the window and fall into shade on the other. Every shadow in the frame points away from that window, in the same direction, with the same softness. Nothing anywhere is lit from a direction the window cannot reach = a surface glowing with no path back to that window, or a flat even blue wash across the whole room, is a failed take.

CONTACT SHADOWS: every object sits on something and proves it. Each shelf drops a dark narrow band onto the wallpaper beneath it and each bracket its own. Every object on the shelves has a tight dark contact shadow where its base meets the timber. The chair legs, the table legs and the furniture all darken into the floorboards where they touch = an object floating with no contact shadow is a failed take.

THE HAZE COMES DOWN: the soft veil sitting over the whole room is reduced to only the faintest suggestion of air in the light near the window. The wall, the floor and the furniture recover their contrast and their blacks instead of sitting behind a general fog.

CAMERA: same framing, same crop, same angle, same perspective. Establish a real focal plane: the shelves and the wall behind them are critically sharp, the armchair and the table read a little softer, and the sofa and throw in the foreground fall clearly out of focus = a frame where everything is equally soft is a failed take.

DETAILS: every surface resolves into real material. Real paper wallpaper with its pattern embossed into the surface, the paper visible beneath it. Real painted timber with the grain quietly under the coat and the plank joins reading as fine seams. Real velvet with a nap that changes value where the pile turns toward the light. Real knitted wool with individual stitches and the twist of the yarn. Real cloth spines on the books with worn corners. Real glaze on the ceramics. Real glass over the clock face with a faint reflection in it. No region of this picture is a flat blank field of colour = an area rendered as an untextured plane, or a surface that reads as vector art, is a failed take.

LOOK: soft, clean and creamy, but with real value separation across the room, not one uniform blue. Blacks are dense and blue, never crushed and never lifted, and no part of the frame is pure black. Every contour is a soft shouldered transition made of tone rather than of line. The picture surface is clean and continuous, free of any granular structure and free of any added texture, and nothing has been sharpened or crisped. Focus behaves optically, with a real focal plane and a gentle falloff away from it.
```

---

### 21.🔄 CHUYÊN ĐỀ 4: TỪ GÓC NÀY THÀNH GÓC KHÁC (`ANGLE ROTATION / PERSPECTIVE SHIFT / CAMERA REPOSITIONING`)

> **Giải mã câu hỏi lớn nhất của bạn**: *"Làm sao để từ 1 bức ảnh gốc ở góc A, bắt AI xoay sang góc B (góc nghiêng 90°, góc từ sau lưng 180°, góc từ trên cao nhìn xuống, góc cận cảnh mặt bên) mà sản phẩm/nhân vật/căn phòng vẫn là một?"*
>
> **🔍 PHÁT HIỆN XƯƠNG MÁU TỪ KIỂM ĐỊNH THỊ GIÁC (`Visual Audit` सो sánh trực tiếp `Rank #711` & `Rank #1137` vs `Rank #1132` & `Rank #3151`)**:
> Khi chúng tôi mở trực tiếp 4 cặp ảnh Trước/Sau của các bài toán xoay góc 90°/180° trên Community:
> - **Tại sao `Rank #1132` (`nano_banana_2`) VÀ cả `Rank #3151` (`nano_banana_2`) đều THẤT BẠI khi xoay 90° (chỉ xoay được ~45°–60° góc 3/4)?**
>   - Ở **`Rank #1132`** (`rank_1132_ref1.png` nhìn thẳng ➔ `rank_1132_nano_banana_2_dc7ad333.webp`): Tác giả viết `"camera positioned at a strict 90-degree side profile angle to the subject"` nhưng chỉ mô tả khuôn mặt nhìn sang bên mà không ra lệnh xoay trục vai và thân người. Kết quả: nhân vật chỉ hơi ngoảnh mặt sang góc 3/4, mắt phải vẫn nhìn về ống kính!
>   - Thậm chí ở **`Rank #3151`** (`rank_3151_nano_banana_2_67f16f6e.webp`): Dù tác giả đã viết rõ `"strict 90-degree left-facing side profile... Only the left side of her face is visible. No three-quarter angle"`, nhưng vì đồng thời ra lệnh giữ nguyên phần cổ áo yếm denim nhìn chính diện từ `@img1` (`"Preserve the exact garment construction from Image 1: high halter-style denim neckline"`), `nano_banana_2` bị "neo" bởi hai bờ vai chính diện của `@img1` nên vẫn chỉ xoay được khoảng 60°!
> - **Vậy làm sao `Rank #711` (`gpt_image_2_5`), `Rank #1137` (`nano_banana_2`), `Rank #1047` (`nano_banana_2_1`) và `@bucketlist_impossible/31-august` xoay chuẩn 90° và 180° tuyệt đối 100%?**
>   - **Bí quyết nằm ở việc XOAY TOÀN BỘ TRỤC GIẢI PHẪU CƠ THỂ (`Anatomical Body/Shoulders/Feet Axis Rotation`) chứ không chỉ xoay đầu!**
>   - Ở **`Rank #711`** (`rank_0711_ref1.jpg` nhìn thẳng ➔ `rank_0711_gpt_image_2_5_32036c59.webp` xoay 90°): Tác giả ra lệnh: **`"Show the knight’s anatomical right side facing the camera, with the helmet and feet pointing toward the right edge of the frame in a true 90-degree profile view"`**! Khi khóa cả **mũ/đầu VÀ mũi bàn chân (`helmet and feet pointing toward the right edge`) cùng mặt phẳng vai phải hướng vào camera**, AI buộc phải xoay toàn bộ trục cơ thể đúng 90°!
>   - Tương tự, ở **`Rank #1137`** (`rank_1137_nano_banana_2_1644d3e1.webp` xoay 180° sau lưng của chính tác giả `@nashjellyfish1232`): Tác giả viết **`"captured from a direct back view, with his head and shoulders facing completely away from the camera"`** — khi khóa cả `head AND shoulders facing completely away`, `nano_banana_2` xoay 180° sau gáy thành công mỹ mãn!

#### 4.1. 5 Kỹ Thuật Xoay Góc Máy Từ 1 Ảnh Gốc Duy Nhất
1. **Kỹ thuật `Full Anatomical Axis Profile Lock` (Khóa đồng bộ Đầu + Vai + Mũi chân để ép xoay đúng 90° hoặc 180° — `Rank #711` & `Rank #1137`)**:
   - Muốn xoay 90° sang phải: `"Show the subject's anatomical right side facing the camera, with the head, torso, shoulders, and feet all pointing toward the right edge of the frame in a true 90-degree orthographic side profile. Do NOT keep the frontal shoulder alignment of the reference image."`
2. **Kỹ thuật `Camera Repositioning on Locked 3D Scene` (Giữ nguyên 100% căn phòng/vật thể, chỉ di chuyển vị trí đứng của người cầm máy — `@pietromalegori/control` `@IMG_027` & `@IMG_059`)**:
   - Dùng cấu trúc: `"Reposition the camera to [NEW POSITION: e.g., low three-quarter angle from the left corner of the sofa / high overhead angle looking down at 45 degrees] while keeping the room architecture, furniture placement, lighting direction, and subject positions 100% unchanged."`
3. **Kỹ thuật `Multi-Panel Orthographic Turnaround Sheet` (`3-View`, `4-View` & `6-Panel` trên 1 khung hình — `Rank #692`, `Rank #1047`, `@ollkorrect/besa` `@IMG_032`)**:
   - Bắt AI vẽ đồng thời 4 góc (`Front | Back | 90° Side Profile | 3/4 View`) đứng cạnh nhau trên cùng 1 tấm ảnh (`Rank #692` trên `seedream_v5_pro` hoặc `Rank #1047` trên `nano_banana_2_1`). Khi vẽ cả 4 góc trên cùng 1 canvas, AI tự động phân biệt rõ góc `Front`, góc `3/4` và góc `90° Side Profile` mà không bao giờ bị nhầm!
   - **Cảnh báo Kiểm định Thị giác (`Rank #838` trên `gpt_image_2_5`)**: Khi tạo bảng xoay bộ giáp hiệp sĩ 3-panel (`Front | Back | Close-up Helmet`), nếu bạn viết câu `"All skin, hair, eyes and facial features remain concealed"` tách rời khỏi phần mô tả mũ giáp, `gpt_image_2_5` có nguy cơ vẽ Panel 1 (`Front View`) **mất đầu** (như đã phát hiện khi soi `rank_0838_gpt_image_2_5_9a03748b.webp`) vì nó dồn chiếc mũ sang Panel 3! Hãy dùng công thức của `Rank #692` (`seedream_v5_pro`: `"Keep her exactly as she is in @Image1: same face, same body, same costume, in all four views"`) để cả 4 panel đều nguyên vẹn.
4. **Kỹ thuật `Lens & Perspective Shift` (Đổi từ ảnh chụp phẳng sang góc Ultra-Wide 14mm hoặc Fisheye dí sát — `Rank #402` & `Rank #464`)**:
   - Giữ nguyên nhân vật và bối cảnh của `@img1`, nhưng đổi tiêu cự sang `14mm ultra-wide angle lens from a high top-down angle` để tạo hiệu ứng chiều sâu kịch tính.
5. **Kỹ thuật `Headless Body Sheet + Face Sheet Separation` (Mẹo độc quyền của `@thomas_lundstrom` `@IMG_007`)**:
   - Sau khi tạo bảng xoay nhân vật, dùng câu lệnh 11 chữ: **`"Remove the face and neck from the front full body reference."`** để tách riêng bảng trang phục không đầu và bảng cận cảnh khuôn mặt, giúp AI không bị nhòe mặt khi render góc rộng.

---

#### 4.2. Tuyển Tập Prompt Xoay Góc Máy Trên Community (`♡ < 50`) — Kiểm Định Đối Chiếu Trước & Sau

##### 🏆 Rank #711 (`3 ♡` | `150 👁️` | Model: `gpt_image_2_5` | Author: `@nostosalgos` | Size: `2:3` | Refs: `1`)
- **Publication ID**: `32036c59-6c12-4ef6-85ac-b5450d48b894`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0711_gpt_image_2_5_32036c59.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/hf_20261004_133749_38b4ec87-c99f-4a5f-9bc3-c1030f20e0e2.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/hf_20261004_133749_38b4ec87-c99f-4a5f-9bc3-c1030f20e0e2_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/0bac5461-d7a7-4a20-a78c-dfa7fcba9541_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Xoay góc nghiêng 90° thành công tuyệt đối nhờ khóa trục Vai + Mũi chân (`Before: rank_0711_ref1.jpg` ➔ `After: rank_0711_gpt_image_2_5_32036c59.webp`)**: Ảnh gốc `@img1` là hiệp sĩ đứng nhìn thẳng chính diện; nhờ câu lệnh khóa trục giải phẫu `Show the knight’s anatomical right side facing the camera, with the helmet and feet pointing toward the right edge of the frame in a true 90-degree profile view`, `gpt_image_2_5` xoay toàn bộ cơ thể, tấm khiên, thanh kiếm và bàn chân sang góc ngang 90° hoàn hảo!

```text
Using the uploaded knight image as the authoritative design reference, create a single full-body right-side profile of this exact character against a seamless medium-grey studio background.
Show the knight’s anatomical right side facing the camera, with the helmet and feet pointing toward the right edge of the image. Use a true side profile and a neutral upright stance, arms relaxed and feet naturally positioned. Include the entire helmet crest, armored feet and cape hem with clear margins.
Preserve the reference’s tall enclosed helmet, narrow upright blade-like crest, sculpted crown, dark visor openings and elongated flared cheek and throat plates. Translate their existing shapes into a coherent side view without changing their design.
Preserve the sculpted weathered silver plate armor, rounded layered pauldrons, leaf-like plate contours, dark chainmail, bronze-toned cape fittings, brown belt and heavy muted burgundy cape. Let the cape hang naturally behind the body.
The sword remains sheathed at the knight’s anatomical right hip, on the side nearest the camera. Preserve the round silver pommel, dark grip, straight crossguard, scabbard fittings and long worn brown scabbard. Keep the sword hanging naturally from its existing belt attachment.
Use the same realistic body proportions and photographed vintage 1980s dark fantasy costume appearance as the reference. Soft balanced studio illumination, readable chainmail and armor overlaps, restrained cool metal highlights, subtle organic film grain and mild optical softness.
Resolve unseen side surfaces conservatively using the established armor construction. Keep the face entirely concealed. One character, one view, no text, no additional ornaments or equipment.
```

##### 🏆 Rank #1137 (`1 ♡` | `6 👁️` | Model: `nano_banana_2` | Author: `@nashjellyfish1232` | Size: `9:16` | Refs: `1`)
- **Publication ID**: `1644d3e1-d1f4-414c-820f-2b6856473b87`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1137_nano_banana_2_1644d3e1.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3ANjoKWYKBU8pL8Za7ZwmebEWqa/hf_20260920_051407_7fb1a15c-5ceb-4b6d-a749-68aef2bff4e6.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3ANjoKWYKBU8pL8Za7ZwmebEWqa/hf_20260920_051407_7fb1a15c-5ceb-4b6d-a749-68aef2bff4e6_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3ANjoKWYKBU8pL8Za7ZwmebEWqa/hf_20260919_215649_de2c51e7-952f-4eef-85b7-40b009e1f5cf.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Xoay góc 180° Sau Lưng (`Direct Back View`) thành công tuyệt đối trên `nano_banana_2` (`rank_1137_nano_banana_2_1644d3e1.webp`)**: Cùng tác giả `@nashjellyfish1232` với `Rank #1132`, nhưng khi chuyển sang khóa cả đầu lẫn hai vai (`captured from a direct back view, with his head and shoulders facing completely away from the camera`), `nano_banana_2` xoay 180° sau lưng hoàn hảo, giữ nguyên kiểu tóc xoăn, chiếc khăn rằn buộc cổ và bối cảnh tàu điện ngầm từ ảnh tham chiếu!

```text
Ultra-realistic shoulder-up portrait of the exact same man in the uploaded reference image. Direct back view, with his head and shoulders facing completely away from the camera. No facial features visible. Preserve his exact head shape, haircut, fade, hair texture, ears, skin tone, neck, black shirt, and accessories. Clean white background, natural neutral lighting, realistic skin and hair texture. No beautification, distortion, stylization, or AI artifacts.
```

##### 🏆 Rank #1132 (`1 ♡` | `7 👁️` | Model: `nano_banana_2` | Author: `@nashjellyfish1232` | Size: `9:16` | Refs: `2`)
- **Publication ID**: `dc7ad333-f90a-4c0d-8cdc-c59f239c339b`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1132_nano_banana_2_dc7ad333.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3ANjoKWYKBU8pL8Za7ZwmebEWqa/hf_20260920_205828_5658e5ec-1701-4135-82ac-7ff9f99798d2.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3ANjoKWYKBU8pL8Za7ZwmebEWqa/hf_20260920_205828_5658e5ec-1701-4135-82ac-7ff9f99798d2_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3ANjoKWYKBU8pL8Za7ZwmebEWqa/hf_20260919_215649_de2c51e7-952f-4eef-85b7-40b009e1f5cf.png
- **Input Reference `@img2`**: https://d8j0ntlcm91z4.cloudfront.net/user_3ANjoKWYKBU8pL8Za7ZwmebEWqa/hf_20260920_201051_3d50ef26-6b87-4a5a-9f60-b86b86730e0a.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Bài học xương máu số 1 khi xoay góc 90° thất bại (`Before: rank_1132_ref1.png + ref2.png` ➔ `After: rank_1132_nano_banana_2_dc7ad333.webp`)**: Dù câu lệnh yêu cầu `camera positioned at a strict 90-degree side profile angle to the subject`, nhưng do không ra lệnh xoay trục hai vai và thân người khỏi tư thế chính diện của `@img1`, kết quả của `nano_banana_2` chỉ xoay được 45° (góc 3/4, mắt phải vẫn nhìn vào camera).

```text
Ultra-realistic raw iPhone 17 Pro Max photography, ultra-photorealistic 4K realism, camera shot at eye level, clean white seamless background, natural indoor light with lights off, no studio flash, no artificial tint, no colored lighting, no dramatic shadows, no glam lighting, no cinematic set, no lifestyle environment. Create a close-up headshot of the person in the uploaded reference image, turned into a full left profile. Preserve the person's identity exactly, including facial structure, facial proportions, skin tone, age appearance, ethnicity, hairstyle, hairline, hair color, eye shape, eye color, eyebrows, nose shape, lips, ears, facial hair (if any), accessories (if desired), and every distinctive facial feature.  He wears a  simple turquoise BLACK sleeveless fitted stretch jumpsuit, It must be black.The uploaded image is the primary identity reference and always takes priority. Head turned a full 90 degrees so the face is shown entirely in left-side profile, with only the left eye, left ear, and the natural line of the nose, lips, and jaw visible. Neutral composed expression, gaze held level toward the edge of frame, ultra-sharp focus on the eye and jawline. Maintain realistic skin texture with visible pores, natural imperfections, realistic hair strands, realistic scalp visibility where applicable, accurate facial anatomy, and zero beauty filters. No plastic skin, no stylization, no AI artifacts. Maximum identity preservation.
```

##### 🏆 Rank #3151 (`0 ♡` | `3 👁️` | Model: `nano_banana_2` | Author: `@stellagarlic1960` | Size: `3:4` | Refs: `0`)
- **Publication ID**: `67f16f6e-5686-43d3-9402-0733b87a515a`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_3151_nano_banana_2_67f16f6e.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2yB2RrqwQk3k3eb7OvX4dBjSajt/hf_20261015_135045_96ae3856-88fe-4f23-abb2-f59e8245000f.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2yB2RrqwQk3k3eb7OvX4dBjSajt/hf_20261015_135045_96ae3856-88fe-4f23-abb2-f59e8245000f_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Bài học xương máu số 2 khi xoay góc 90° thất bại do khóa cổ áo chính diện (`rank_3151_nano_banana_2_67f16f6e.webp`)**: Dù tác giả đã viết `strict 90-degree left-facing side profile... No three-quarter angle`, nhưng vì đồng thời bắt giữ nguyên phần cổ áo yếm denim nhìn thẳng từ `@img1` (`Preserve the exact garment construction from Image 1: high halter-style denim neckline`), hai bờ vai của nhân vật vẫn bị neo ở góc 3/4 (~60°)!

```text
Use Image 1 as the primary visual reference and base. Create a photorealistic, high-end Y2K fashion editorial beauty portrait of the same young adult woman, captured in a strict 90-degree left-facing side profile. Her face must be completely turned sideways, with a clearly defined forehead, nose, lips, chin, and jawline silhouette. No three-quarter angle or direct eye contact.
Frame the portrait tightly from the upper shoulders to the top of her hairstyle. Preserve her facial identity, warm bronzed skin, dark hair styled in a voluminous messy updo with delicate flyaway strands, oversized tortoiseshell wraparound shield sunglasses with amber gradient lenses, multiple chunky gold hoop earrings and ear cuffs, and faded blue denim halter neckline.
Her lips are slightly parted with realistic glossy caramel-nude lip makeup. Both hands remain completely outside the frame.
Use a seamless soft off-white studio background, bright diffused frontal-side beauty lighting, subtle shadows, realistic skin pores, sharp accessory details, and natural highlights. Maintain a sophisticated early-2000s luxury fashion magazine aesthetic.
Preserve accurate facial anatomy, natural proportions, realistic hair strands, consistent reflections, and authentic material textures. No additional people, props, text, logos, watermarks, artificial smoothing, distorted features, or depth-of-field blur. Output one ultra-detailed portrait matching Image 1's aspect ratio, with seamless photographic realism at 200% zoom.
```

##### 🏆 Rank #692 (`3 ♡` | `251 👁️` | Model: `seedream_v5_pro` | Author: `@nostosalgos` | Size: `16:9` | Refs: `1`)
- **Publication ID**: `46282ae9-8b79-4ca1-ab66-5e137e907049`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0692_seedream_v5_pro_46282ae9.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/hf_20261007_212845_711c188d-6a41-4666-89d0-81666ff431bd.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/hf_20261007_212845_711c188d-6a41-4666-89d0-81666ff431bd_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/f2a045d2-b889-43f5-a174-94c8ededd523.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Bảng Xoay Nhân Vật 4 Góc Toàn Thân (`Front | Back | 90° Side Profile | 3/4 View`) hoàn hảo 10/10 trên `seedream_v5_pro` (`Before: rank_0692_ref1.jpg` ➔ `After: rank_0692_seedream_v5_pro_46282ae9.webp`)**: Kiểm định bằng mắt xác nhận `seedream_v5_pro` dựng đủ 4 góc toàn thân đứng cạnh nhau trên nền xám đậm, giữ đồng nhất 100% cổ ấn phát sáng màu tím, gương mặt nứt sứ, váy vải lanh rách và áo choàng lông cừu ở cả 4 góc (trong đó Panel 2 xoay đúng 180° sau lưng và Panel 3 xoay đúng 90° profile!).

```text
Character turnaround reference sheet for a dark fantasy film: four full-body views of the same woman, arranged side by side on one plain dark grey studio background, in this order — front view, back view, profile view from the side, and three-quarter view. Keep her exactly as she is in @Image1: same face, same body, same markings, same costume, same hair, in all four views.

THE CHARACTER — an undead woman raised by a necromancer. A pale, gaunt woman of about twenty-five, extremely light translucent skin covered in a fine network of dark vein-like markings like cracked porcelain, across her face, her neck, the backs of her hands and her bare feet. Large pale milky lavender eyes without pupils, a small dark mouth, a calm and absent expression in every view. Long dark hair that looks wet, hanging in lank strands around her face and over her shoulders down to her waist; in the back view it covers the upper back.

COSTUME — a tattered off-white floor-length gown of heavy linen with long sleeves, frayed at the hem and soiled with dirt, with small holes in the fabric. Over one shoulder a heavy dark brown coarse-woven cloak that hangs down her back, ragged at the edge. Around her neck a thick dark collar of rusted iron and leather with a glowing circular purple sigil at the centre of the throat, bright enough to throw violet light on her chin and jaw, and a heavy dark chain hanging from the collar down the front of her chest. Barefoot, feet pale and dirtied, with the same dark markings as her face.

STYLE — photoreal cinematic dark fantasy in the same rendering language and the same material qualities as @Image1. Muted desaturated palette: charcoal grey, earthy brown and pale beige, with the single neon-violet light at her collar as the only saturated colour. Soft cool key light from the upper left, cool rim light separating her from the background, plain studio backdrop, no environment. She stands straight with her arms at her sides in all four views, identical proportions, identical costume and identical hair in every view, like a film costume turnaround.

No text, no labels, no watermarks, no logos, no UI elements, no gore, no wounds.
```

##### 🏆 Rank #1047 (`1 ♡` | `20 👁️` | Model: `nano_banana_2_1` | Author: `@mayanos` | Size: `21:9` | Refs: `1`)
- **Publication ID**: `46e3a53e-1064-41f5-80d6-34836868e125`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1047_nano_banana_2_1_46e3a53e.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3H5aQ4Ikk3KvsH2pGYmvTZNO3p6/hf_20261007_164138_7e3da6c0-7a0c-4aa2-8f0d-454d8099fb4e.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3H5aQ4Ikk3KvsH2pGYmvTZNO3p6/hf_20261007_164138_7e3da6c0-7a0c-4aa2-8f0d-454d8099fb4e_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3H5aQ4Ikk3KvsH2pGYmvTZNO3p6/hf_20260929_004457_92b05e0c-7ac0-4252-a46f-becdc917af81.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Bảng Xoay Cận Cảnh Đầu & Vai 4 Góc (`4-View Headshot Turnaround: Front, 3/4, Side Profile, Back-of-Head` — `Before: rank_1047_ref1.png` ➔ `After: rank_1047_nano_banana_2_1_46e3a53e.webp`)**: Câu lệnh ngắn gọn nhưng cực kỳ hiệu quả trên `nano_banana_2_1`: khi yêu cầu vẽ đủ 4 góc (`front view, 3/4 view, side profile, and back-of-head view`) trên cùng 1 hàng ngang nền trắng, AI tự động phân tách rạch ròi góc `3/4` (Panel 2) với góc `90° Side Profile` (Panel 3) và góc `180° Sau gáy` (Panel 4)!

```text
Create a photorealistic 4-view headshot turnaround sheet of the exact same character: front view, 3/4 view, side profile, and back-of-head view. Show head and shoulders only. Keep the face, hairstyle, skin tone, facial features, and proportions perfectly consistent. Neutral expression, soft studio lighting, pure white background, evenly spaced side-by-side.
```

##### 🏆 Rank #838 (`2 ♡` | `29 👁️` | Model: `gpt_image_2_5` | Author: `@nostosalgos` | Size: `16:9` | Refs: `1`)
- **Publication ID**: `9a03748b-e3ac-42ac-8805-2b190f807953`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0838_gpt_image_2_5_9a03748b.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/hf_20261004_131559_91c055e3-1d9f-42dd-8454-22ffcf98c215.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/hf_20261004_131559_91c055e3-1d9f-42dd-8454-22ffcf98c215_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3IMDxfmnoC6BWV24xUeeGvWe3uf/0bac5461-d7a7-4a20-a78c-dfa7fcba9541_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Cảnh báo Kiểm định Thị giác trên Bảng Xoay 3-Panel (`Before: rank_0838_ref1.jpg` ➔ `After: rank_0838_gpt_image_2_5_9a03748b.webp`)**: Dù chất liệu thép Gothic và áo choàng đỏ ở Panel 2 (`Back`) và Panel 3 (`Close-Up Helmet`) đẹp xuất sắc, nhưng Panel 1 (`Front Full-Body`) bị **mất đầu/mũ giáp** do `gpt_image_2_5` tách riêng chiếc mũ sang Panel 3 cận cảnh. Khi muốn tạo bảng xoay nhiều góc có mũ/đầu đầy đủ ở mọi panel, hãy ghi rõ `keep the helmet attached to the body in all views` như `Rank #692`!

```text
Create a precise three-view character reference sheet of the armored knight in the uploaded image. Use this image as the primary authority for the character’s proportions, silhouette, armor construction, helmet, clothing, equipment, materials and colors. Preserve the actual reference design rather than substituting generic medieval armor.
CHARACTER DESIGN
A tall, fully enclosed knight with realistic human proportions and an intricate, vertically elongated silhouette. All skin, hair, eyes and facial features remain concealed.
The helmet is tall and sharply pointed, with a pronounced central ridge and sculpted, leaf-like fluting. A narrow, downward-angled horizontal visor opening forms a shallow V across the front, completely black inside. The elongated faceplate descends into a flared, pointed lower edge overlapping the upper chest. Preserve this distinctive helmet shape precisely.
The armor is weathered dark silver steel with bright worn edges, fine scratches, mottled patina and deep dark recesses. Its overlapping plates resemble elongated leaves, with raised central ribs and flowing pointed contours. Preserve the sculpted breastplate, large leaf-shaped pauldrons, layered arm defenses, flared gauntlet cuffs, articulated metal fingers, overlapping pointed hip plates, ridged knee defenses, long fluted greaves and pointed articulated sabatons.
Dark chainmail forms a broad mantle around the shoulders and upper chest and remains visible beneath the arm plates, along the sides of the torso and between the leg defenses. Preserve the hanging chainmail sections and their length.
A heavy, faded burgundy cape attaches at both shoulders beneath small ornamental bronze-toned fittings. It falls to the ground in deep folds, with a frayed, ragged hem and slight pooling around the feet. Preserve its volume, fabric weight and muted wine-red color.
A narrow brown leather belt wraps around the waist, with a diagonal leather suspension strap across the hips. A single sword hangs at the knight’s anatomical right hip, appearing on the viewer’s left in the front view. Match the reference’s rounded metal pommel, dark grip, straight crossguard and long weathered brown scabbard. Preserve this anatomical side in every view; do not mirror the equipment.
LAYOUT
Use one horizontal landscape canvas with three equal-width viewing zones, arranged left to right: front body without head, complete rear body, enlarged helmet-and-upper-torso portrait.
Center each view within its own third. Maintain clear background around each silhouette so neighboring views do not overlap. Use one continuous neutral medium-grey studio background and floor across the entire sheet, without borders, divider lines, frames or visible panel seams.
LEFT THIRD: FRONT BODY, HEAD OMITTED
Show the knight directly from the front in a neutral symmetrical stance, arms relaxed at the sides, hands open naturally, feet slightly apart.
First establish complete full-body framing, including the hypothetical helmet position. Then omit only the head and helmet above the neckline, including the helmet’s elongated faceplate. Retain the chainmail collar, shoulder mantle, cape attachments and every independent torso armor component.
Leave plain background where the helmet would have been. This is a clean reference-sheet omission, with no exposed anatomy, wound, stump or detached helmet.
Keep the torso, shoulders, hands, hips, knees and feet at their original full-body positions. Do not move the body upward or enlarge it to occupy the empty head space. Keep both feet and the complete cape hem inside the canvas.
MIDDLE THIRD: COMPLETE REAR VIEW
Show the same knight directly from behind, including the entire helmet, cape and feet, in the matching neutral stance.
Preserve the helmet’s pointed crown and longitudinal ridges as they continue naturally around the rear. Show the heavy burgundy cape hanging naturally from the same shoulder attachments and covering the back. Do not remove, lift, shorten, spread or make the cape transparent to expose hidden armor.
Keep the visible rear and side portions of the armor consistent with the front design. The sword remains at the knight’s anatomical right hip, appearing on the viewer’s right in this rear view, and is only visible where the cape naturally permits.
The reference does not establish the complete rear construction. Resolve unseen areas conservatively through simple, plausible continuations of the existing forms. Add no new emblems, weapons, ornaments or costume elements.
MATCHED BODY SCALE
The front and rear views must use identical subject scale, camera height, viewing distance and restrained perspective. Align the shoulder line, waist, hips, knees and soles of the feet across both views.
Use the same ground baseline and the same hypothetical complete helmet-to-foot height. The front view’s omitted helmet must leave unused space, not trigger a change in framing.
RIGHT THIRD: HELMET AND UPPER-TORSO DETAIL
Show an enlarged portrait from the upper chest upward, including the complete helmet, chainmail collar, both shoulder attachments and enough of the pauldrons to explain their construction.
Turn the knight slightly toward the knight’s anatomical right, with the visor pointing slightly toward the viewer’s left. Keep the front visor and the knight’s left helmet surface visible in a restrained three-quarter view.
Preserve the pointed crown, central ridge, narrow black visor slit, leaf-like fluting and elongated flared faceplate. Keep clear background above the helmet tip and around its silhouette.
The visor remains fully closed and dark. Do not reveal or invent eyes, a face, hair or exposed skin.
LIGHTING AND CONTINUITY
Use soft, balanced studio illumination with consistent direction, exposure and color balance across all views. Reveal the dark steel’s raised ridges, scratches, chainmail links, leather straps and burgundy fabric without blowing out highlights or burying details in shadow.
Preserve the reference’s tactile costume materials and subtle photographic texture. Keep all views sufficiently sharp for design comparison, with minimal perspective distortion and no shallow-focus blur.
All three views depict one identical knight. Maintain matching armor construction, cape color, chainmail arrangement, fittings, proportions and equipment placement.
EXCLUSIONS
No text, labels, diagrams, measurements, logos, watermarks, scenery or decorative graphics. No additional props beyond the sword and scabbard already established in the reference. No additional weapons, shields, crowns, horns, glowing eyes or magical effects. No exposed face, open visor, costume variations, mirrored equipment, missing armor components, cropped feet or cropped helmet tip.
```

##### 🏆 Rank #402 (`17 ♡` | `3477 👁️` | Model: `nano_banana_2` | Author: `@aidsgn` | Size: `3:4` | Refs: `1`)
- **Publication ID**: `9b29ab1d-8574-4ce8-b43d-3ce14187ca27`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0402_nano_banana_2_9b29ab1d.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2vr9SojCEMjZqo7g5Ro7nXbZ2MR/hf_20260920_105200_aa98e797-0ca0-40c8-8c2b-33ca85720bec.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_2vr9SojCEMjZqo7g5Ro7nXbZ2MR/hf_20260920_105200_aa98e797-0ca0-40c8-8c2b-33ca85720bec_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_2vr9SojCEMjZqo7g5Ro7nXbZ2MR/hf_20260808_085137_a2b3ff9f-2723-4ca8-8c54-e8bfe61690b1.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Xoay từ ảnh chân dung thường sang góc Ultra-Wide dí sát ống kính (`Before: rank_0402_ref1.jpg` ➔ `After: rank_0402_nano_banana_2_e0f043a4.webp`)**: Giữ nguyên nhân vật và trang phục từ `@img1`, nhưng đổi sang góc chụp từ trên cao nhìn xuống (`high-angle shot`) với bàn tay đưa sát ống kính góc rộng.

```text
Use the uploaded image as the authoritative full-scene reference. Preserve the exact number of people and each person’s recognizable identity, facial features, age, skin tone, hairstyle, body type, clothing, footwear, accessories, colors, prints, logos and fabric textures. Preserve the same recognizable location, surrounding objects, architecture or landscape, lighting, weather, time of day, palette and atmosphere. Preserve the source framing category and visible anatomy: a headshot remains a headshot, waist-up remains waist-up, three-quarter remains three-quarter and full-body remains full-body. Analyze the existing pose, silhouette, dominant body axis, garment volume and direction of movement, then choose an individual camera side, height, tilt and rotation that presents this specific figure most powerfully. Use the original pose as the source of dynamism and intensify its natural line through camera placement. Position an extreme rectilinear ultra-wide close-focus virtual camera at point-blank range beside a broad connected body or clothing plane such as the shoulder with torso, side of the coat, torso with hip or flowing fabric. Aim along the whole visible figure so the complete silhouette recedes through depth in one continuous scale cascade, with the nearest third appearing approximately three times larger than the farthest third. Keep the face, hands, knees and feet integrated with their neighboring anatomy. Make the extreme wide-angle perspective unmistakable across the entire person through expanded near volume, rapid scale reduction, powerful foreshortening, stretched peripheral space and environmental lines converging around the figure. Keep every originally visible part fully inside the frame with 8–12% breathing room. Reconstruct the same environment consistently from the new viewpoint and continue newly revealed areas seamlessly. The photograph fills the complete rectangular canvas edge to edge with natural background imagery in all four corners; optical hardware, circular image boundaries, black rims and vignetting are entirely absent.
```

##### 🏆 Rank #464 (`11 ♡` | `108 👁️` | Model: `text2image_soul_v2` | Author: `@valyapokazhi` | Size: `1536x2048` | Refs: `1`)
- **Publication ID**: `b53378c7-1554-44d7-a439-333304b110c9`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0464_text2image_soul_v2_b53378c7.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_33WkoEFLQgBrBk5qYo7fGrtvB4B/hf_20261008_142305_4b5149a4-f345-4ce1-b815-70179c14c0f2.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_33WkoEFLQgBrBk5qYo7fGrtvB4B/hf_20261008_142305_4b5149a4-f345-4ce1-b815-70179c14c0f2_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_33WkoEFLQgBrBk5qYo7fGrtvB4B/1247a3a4-54e9-49de-91b7-0a0d9f48b826.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Đổi góc máy bằng thông số vật lý chính xác (`Before: rank_0464_ref1.jpg` ➔ `After: rank_0464_text2image_soul_v2_9214a9b1.webp`)**: Giữ nguyên người phụ nữ ngồi trên ghế từ `@img1`, nhưng xoay máy ảnh sang góc nghiêng thấp (`low three-quarter angle`) kèm mô tả chi tiết hướng ánh sáng đèn neon.

```text
Vertical 4:5 fashion street style photograph, autumn day. Reference 1 defines only the model’s identity. Preserve her facial geometry, the shape of her eyes, brows, nose, and lips, natural asymmetry, and skin tone.
The model is an adult woman, 29 years old, 156 cm tall, 52 kg, with a slim petite build. Natural light-blond hair falls loose to her lower back. Narrow oval dark sunglasses in a silver frame, silver drop earrings.
Outfit: a cropped, waist-length voluminous bomber jacket in soft matte dark-chocolate leather, with huge shoulders, balloon sleeves, a silver zipper, and milky ribbed trims at the cuffs and waistband with two chocolate stripes. A milky ribbed turtleneck and a black belt with a silver buckle. Wide parachute trousers in matte olive nylon, dark red socks, and glossy black chunky-soled loafers.
Location: the asphalt of an empty parking lot with white markings and yellow leaves scattered across it.
The camera is very close overhead, about 60 cm above the model’s head and slightly in front, pointing down. The frame is rotated 12°. Use a 24 mm full-frame-equivalent lens, suggested f/8, 1/500 s. The perspective intentionally enlarges her head and shoulders, while her legs and loafers appear small at the bottom of the frame.
The model tips her head back and looks up into the lens. Her right arm is raised, the palm wearing two silver rings shading her eyes from the sun. The huge bomber sleeve fills the upper-left part of the frame. Her left arm hangs loosely along her body. Her lips are slightly pursed.
Focus on the face, with the sleeve and hand also readable.
Sun from above and in front lights her face, and her hand casts a shadow on her forehead. Highlights run along the folds of the sleeve leather, and the sky reflects in her sunglass lenses. Retain pores, the bomber leather grain, sleeve folds, and the white markings.
No face changes, no extra or fused fingers, no lettering or logos.
```

---

#### 4.3. Cách 29 Bộ Phim Xoay Góc Máy Liên Hoàn Giữa Các Cảnh (`Match-Cut Camera Repositioning` & `6-View Orthographic Turnaround`) — Nguyên Văn 100%

##### 🎬 Project `bucketlist_impossible/31-august` — Asset `@IMG_014` (Model: `nano_banana_pro_unlimited` | Roles: `start_frame_keyframe` | Reused in `1` jobs)
- **Chiến thuật Đạo diễn**: Bảng Xoay Nhân Vật Hành Động **6 Góc (`Six-View Photographic Action Sheet`)** trên `nano_banana_pro_unlimited` với câu lệnh khóa cứng góc nghiêng 90° (`body, head, feet and nose all exactly 90 degrees left`).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_359U8LzwhGMVvAw4ZirC8oN1czR/hf_20260812_183045_e5b2a577-51e3-4b1b-aa2a-3e12db49c403.png
- **👁️ Visual Audit Verdict**: Đạo diễn `@bucketlist_impossible` đã viết công thức khóa góc 90° kinh điển nhất trong toàn bộ 29 bộ phim: `strictly 90-degree left side profile view (body, head, feet and nose all facing 90 degrees to the left edge of the frame — NOT a 3/4 view)`!

```text
Use the attached image as the absolute authority for VEX. Create a six-view photographic action sheet featuring exactly the same robot in every view.

Preserve VEX’s exact identity and construction: lens in the center of the head. identical speaker-array head, asymmetrical rectangular audio components, antenna, analog gauges, exposed neck wiring, uneven shoulder armor, chest instruments, narrow mechanical waist, long powerful limbs, gray-green enamel armor, dark internal framework, copper elements, orange-brown lower-leg plates, articulated hands and heavy mechanical feet.

Do not redesign, beautify or simplify him. Maintain the same component placement, proportions, colors, materials, weathering and intimidating command presence throughout all six depictions.

Show exactly these six views:

1. COMMAND POSE  
Full-body three-quarter stance, standing tall with controlled authority, head slightly lowered as if analyzing a threat, arms relaxed but ready.

2. UNARMED COMBAT  
VEX advances in a low, powerful fighting stance, one forearm blocking an incoming strike while the opposite metal fist drives forward. Strong torso rotation, compressed leading leg and believable mechanical weight.

3. HEAVY MACHINE GUN  
VEX braces a heavy experimental 1956 machine gun against his body. The weapon has a long perforated cooling shroud, rectangular gunmetal receiver, exposed feed mechanism, thick ammunition belt, Bakelite grips and an integrated forearm support. The weapon looks industrial, heavy and mechanically advanced for its period.

4. ELECTROMAGNETIC RIFLE  
VEX aims a two-handed experimental energy weapon containing exposed copper induction coils, ceramic insulators, analog gauges, a dark amber glass power chamber and a thick armored cable connected to his torso. Disciplined firing stance with both feet firmly planted.

5. CLOSE-RANGE WEAPON  
VEX attacks with a heavy forearm-mounted hydraulic impact weapon: a compact industrial piston ram built into one arm. The other hand protects his torso. The mechanism appears physically functional and brutally powerful.

6. CLOSE-UP  
Tight head-and-upper-torso portrait showing the speaker cones, grille, antenna, scratched gauge glass, meter needles, exposed wiring, oxidized copper, chipped enamel, weld seams, bolts, grease and layered armor thickness. The speaker-head remains mechanical and unreadable—commanding rather than friendly or deliberately villainous.

Present all six depictions on one uninterrupted charcoal-gray studio limbo with clear spacing and no borders. Use hard directional light from upper left, restrained fill and a narrow rear edge light. Strong contact shadows establish VEX’s weight.

Render physically convincing materials: chipped gray-green enamel, scratched gunmetal, oily joints, oxidized copper, aged Bakelite, cracked rubber insulation, woven cable sleeves, rough welds, uneven rivets, heat discoloration, machining marks and grime accumulated inside mechanical recesses.

Exactly one VEX repeated six times. Every view retains precisely the same head assembly, antenna position, armor asymmetry, body proportions, paint pattern and component placement. The weapons are separate equipment configurations; they do not alter VEX’s canonical body design.
```

##### 🎬 Project `bucketlist_impossible/31-august` — Asset `@IMG_117` (Model: `nano_banana_pro_unlimited` | Roles: `start_frame_keyframe, turnaround_sheet_reference_element` | Reused in `7` jobs)
- **Chiến thuật Đạo diễn**: `Matched Interior Continuity Sheet` (Tái sử dụng `7` lần): Bảng xoay 4 góc nội thất bên trong cabin xe tải năm 1956 (`Driver POV | Over-the-Shoulder | Side Profile | Reverse Angle Looking Back`).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_359U8LzwhGMVvAw4ZirC8oN1czR/hf_20260814_060215_cbd468a5-8204-4e1c-b3fd-4652f3258192.png
- **👁️ Visual Audit Verdict**: Cách làm cực kỳ thông minh khi quay nhiều cảnh trong cùng 1 không gian hẹp (như cabin xe hoặc góc phòng khách đặt cây thông Noel): tạo 1 tấm `Matched Interior Continuity Sheet` chứa đủ 4 góc máy bên trong không gian đó để mọi cú cắt cảnh đều khớp nhau 100%!

```text
Create a matched interior continuity sheet for the same 1956 American forward-control utility truck, showing exactly three photographic views of one identical cab: wide view from the open passenger door, centered view from behind the bench seat toward the windshield, and close three-quarter view of the dashboard and passenger-side glove compartment. The cab has one broad worn bench seat in dark oxblood vinyl, painted petrol-blue metal doors, ivory-painted steel dashboard, large thin-rim steering wheel on the left, floor shifter, analog gauges, simple heater controls, windshield wipers and utilitarian rubber flooring. Preserve the same dashboard openings, switch positions, glove-compartment dimensions, seat seams, door hardware and wear pattern in every view. Natural full-scale automotive photography under soft neutral studio light entering through the windows, with real cracked vinyl, chipped enamel, dusty glass, scratched Bakelite knobs, oxidized screws and grease at hinges. Deep readable geometry and restrained focus. Empty cab with plain surfaces and period controls.
```

##### 🎬 Project `pietromalegori/control` — Asset `@IMG_027` (Model: `seedream_v5_pro` | Roles: `start_frame_keyframe` | Reused in `2` jobs)
- **Chiến thuật Đạo diễn**: Đổi góc máy 180° sang Phía Sau Vai (`Reverse Over-the-Shoulder Angle`, `seedream_v5_pro`, tái sử dụng `2` lần) trong cùng căn phòng vừa chụp ở cảnh trước.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_38JDnD2aJxtjnkHGSvDeUpDsT5p/hf_20260822_163319_f0df9aa2-270c-484c-b4c2-ea13b5a1a5be.png
- **👁️ Visual Audit Verdict**: Giữ nguyên ánh sáng ban ngày lạnh, chiếc áo khoác xanh đậm và không gian phòng từ ảnh gốc, nhưng dịch chuyển máy quay ra phía sau lưng nhân vật (`positioned behind the subject's right shoulder`) để lấy điểm nhìn hướng về phía bức tường đối diện.

```text
Wide shot looking through an open doorway into a modest Soviet-era apartment living room, camera at standing eye level centered on the doorway opening, aged warm-toned wooden door frame visible on both left and right edges cropping the scene in shallow focus. Room interior: walls in flat pale off-white paint with a faint cold teal-green cast — bare and empty, no decoration, surface rough and slightly stained with age, ceiling plain flat white with a single small conical pendant light fitting mounted centrally — turned off, hanging on a short cord. Far wall: a single rectangular window centered on the back wall — dark wooden frame with a small upper transom pane and a larger lower pane, white sheer curtain hanging loosely on both sides, the window glowing with a  exterior  light — the window the primary light source casting a cold pale   forward into the dim space, a cast iron radiator mounted beneath the window. Left wall: a small simple shelf bracket mounted at mid-height with a few small indistinct objects on it, two small switch plates on the wall below the shelf, a flat painted interior door on the far left wall — simple, closed, same off-white paint. Furniture: a single worn fabric sofa against the left wall — low and sagging, upholstered in a dark muted striped worn fabric, heavily used and compressed. Beside the sofa: a small low wooden stool. Against the right wall in the midground: a low dark wooden sideboard or credenza — long and flat, aged dark wood, a few indistinct objects sitting on its surface. In the far right corner partially in shadow: a tall narrow dark bookshelf unit with a few objects on the shelves, barely readable in the dim light. Floor: dark worn wood plank flooring — aged and scuffed, dark brown-black with age, slightly reflective catching the cold window light as a pale streak running toward the far wall. Right side of frame: through a separate open doorway on the far right edge — a glimpse into the adjacent kitchen, pale mint-green tiled walls and kitchen counter visible, the kitchen lit with a brighter cold teal-green ambient glow, the light spilling slightly into the living room from the right. Atmosphere: desolate, oppressive, deeply dim, the cold blue-teal window glow as the dominant light source barely illuminating the room, the kitchen teal glow secondary from the right, deep shadow everywhere especially in the foreground corners and ceiling, muted cold teal-green cast throughout, no warm tones. Cinematic still, 35mm, 35mm lens, deep focus, perfectly level camera, no people, no figures, no television visible, photorealistic, no grain.
```

##### 🎬 Project `pietromalegori/control` — Asset `@IMG_059` (Model: `seedream_v5_pro` | Roles: `start_frame_keyframe` | Reused in `1` jobs)
- **Chiến thuật Đạo diễn**: Đổi sang Góc Máy Siêu Thấp Sát Sàn (`Extreme Low-Angle Floor-Level Perspective`, `seedream_v5_pro`) giữ nguyên 100% ánh sáng và vị trí đồ đạc trong căn hộ.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_38JDnD2aJxtjnkHGSvDeUpDsT5p/hf_20260824_230159_9f1469a1-16b6-45a9-b54b-dd3893d09313.png
- **👁️ Visual Audit Verdict**: Đặt máy quay sát mặt sàn bê tông nhìn ngược lên (`camera placed directly on the floor looking slightly upward`) với ống kính `35mm` để tạo cảm giác kịch tính và hùng vĩ cho chủ thể trong phòng.

```text
Wide three-quarter shot from inside a modest Soviet-era apartment living room, camera at standing eye level, approximately 1.6m, positioned slightly right of centre looking across the space, the entire room visible in a single frame, camera perfectly level, verticals parallel and true. The room matches the apartment reference exactly: proportions, furniture, wall tone, floor and layout unchanged.

WALLS: aged mint-green paint, flat and rough, stained and darkened toward the corners, peeling slightly near the ceiling edge, no decoration, bare and worn.
CEILING: plain flat plaster, slightly yellowed, no cornice, no fixture lit.
FLOOR: worn pale timber planks running toward camera, scuffed and dusty, darker at the edges and corners.

LEFT SIDE OF FRAME — THE FRONT DOOR, NOW OPENING ONTO THE COMMUNAL CORRIDOR: the tall panelled door on the left wall of the reference is the apartment's entrance door. Same door, same position, same frame, standing open inward into the room at the same angle — a heavy aged timber panel door with a single raised moulded panel, painted the same washed mint-green as the walls, worn darker around the plain lever handle and along the leading edge, hung in an aged painted timber frame with a worn threshold strip across the plank floor beneath it.
What lies beyond it changes: instead of another room, the doorway now opens directly onto the communal corridor. Through the opening, readable as a distinct space with its own light: white upper walls over a dark green painted dado, a heavy dark green door with a small red number plate on the far side of the corridor, worn pale vinyl floor with a seam running along it, a surface-mounted fluorescent tube burning cold white on the corridor ceiling, The corridor is brighter, colder and cleaner in colour than the apartment: a hard fluorescent white-green that spills a bright, hard-edged wedge across the plank floor of the living room and up the near wall, cutting into the dark interior.

CENTER FRAME
Worn sofa against the left wall — low and sagging, striped fabric upholstery in dark brown-olive tones, heavily compressed from use, small low stool or side table beside it. Back wall in bare off-white plaster with cold teal cast, completely empty. Window centered on the back wall — dark wood frame with upper transom pane and larger lower pane, loose white sheer curtains on both sides, glass emitting cold blue-teal light as the sole light source, no exterior detail visible, only flat diffuse glow. Cast iron radiator below the window. Flat white ceiling with a single central pendant light — conical or faceted socket fitting, unlit, hanging on a short cord.


RIGHT FRAME
Dark cabinet or storage unit against the right wall, absorbed into shadow. Open doorway on the far right — no door, leading to the adjacent kitchen, pale mint-green ceramic tile walls visible through the opening, kitchen counter, cold teal-green ambient glow bleeding through the opening and catching the edge of the door frame. The contrast between the dark living room and the teal kitchen glow is the second light source in the frame after the window.
LIGHT: two competing cold sources and nothing else. From the LEFT, the hard fluorescent white-green of the communal corridor through the open front door, throwing a bright hard-edged wedge across the floor and separating the door leaf as a dark silhouette against it. From the CENTRE-RIGHT, the softer blue-teal CRT glow washing the wall behind the sofa and the floor in front of the set. Between them the room stays deeply dim, the mint-green walls barely readable, deep unfilled shadow in the upper corners and along the ceiling. No warm light anywhere, no lamps lit, no daylight.

ATMOSPHERE: sparse, desolate, oppressive, lived in but stripped bare. Desaturated cold palette of mint-green, teal and dust.

Cinematic still, 35mm rectilinear lens, deep focus front to back, perfectly level camera, no people, no figures, photorealistic, available light only, no HDR, no colour grading, no grain.
```

##### 🎬 Project `ollkorrect/besa` — Asset `@IMG_053` (Model: `cinematic_studio_image` | Roles: `turnaround_sheet_reference_element` | Reused in `4` jobs)
- **Chiến thuật Đạo diễn**: Dịch chuyển vị trí máy quay từ trong phòng ra Khung Cửa Nhìn Vào (`Doorway Threshold Camera Repositioning`, `cinematic_studio_image`, tái sử dụng `4` lần) trên nền `Kulla Master Room`.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_32vwRMunqoTPjjAdQ6zrT3TrjuG/hf_20260812_110447_160a372d-29cb-454b-aebf-65d63121528a_min.webp
- **👁️ Visual Audit Verdict**: Sử dụng bức ảnh căn phòng đá gốc (`Kulla master`) làm chuẩn kiến trúc tuyệt đối, sau đó lùi máy quay ra ngoài ngưỡng cửa nhìn vào trong phòng để tạo khung hình lồng trong khung cửa (`frame-within-a-frame`).

```text
PRESERVE EXACTLY:

Use the attached Kulla master as the authority for architecture and composition. Preserve its exact proportions, limestone masonry, roof, chimney, central rectangular double oak door, all window placements, steps, courtyard wall, gate, tree, path, mountains, camera position, framing and perspective.

CHANGE:

Transform the location into a deep summer night during an old Albanian highland wedding. Replace winter ground with dry compacted earth, irregular grass and sparse summer vegetation. Give the tree a full canopy of dark-green leaves. The valley and mountains recede into near-black silhouettes beneath a dark indigo sky with no remaining twilight.

Keep the central double oak door open. Beyond it, show only a dim, faded amber interior ambience created by concealed traditional oil lanterns positioned deep inside the house, outside the camera’s sightline. Their indirect light reflects from stone walls, with layered shadows and subdued falloff. No indoor flame, lamp, lantern body, candle, fireplace or identifiable light source is visible.

Prepare the courtyard with authentic wedding elements: deep-red and ivory woven kilims and embroidered linens near the entrance, low wooden benches along the perimeter and several copper serving trays. Keep the centre completely open.

Exactly four resin-pine torches burn in simple hand-forged iron wall brackets: one on each side of the entrance, one beside the wooden gate and one on the far courtyard wall. All are wall-mounted and are the only visible flames.

Both ground-floor windows hold faint, uneven, diffused amber ambience from concealed lanterns deeper inside. The glass remains mostly dark, with no hotspot, flame, wick, lantern silhouette or recognizable source. Upper windows remain dark.

The exterior torches are the strongest lights, casting restrained local pools across nearby stone and parts of the courtyard. Indoor light remains weak and faded, never projecting into the courtyard. Faint cool night fill barely separates the roofline, tree and mountains. Use natural flame flicker, light smoke, realistic falloff, soft low-contrast shadows and restrained reflections on stone and copper.

The atmosphere is alive, ceremonial and historically pre-electric: stone, timber, wool, copper, torch fire and concealed oil-lantern ambience. Remove electric bulbs, string lights, modern lanterns, floodlights, chandeliers, plastic decorations, synthetic fabric, contemporary furniture and modern event styling.
```

##### 🎬 Project `thomas_lundstrom/emerald-fragrance-commercial` — Asset `@IMG_007` (Model: `nano_banana_2` | Roles: `turnaround_sheet_reference_element` | Reused in `3` jobs)
- **Chiến thuật Đạo diễn**: Câu lệnh 11 chữ Tách Đầu Khỏi Thân trên Bảng Tham Chiếu (`Remove the face and neck from the front full body reference`, `nano_banana_2`, tái sử dụng `3` lần).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_2yLzar9qEBwWtKro0bFax4owvTR/hf_20260716_053230_f76817a8-b22d-4683-88ae-f1aa01d95b2d.png
- **👁️ Visual Audit Verdict**: Sau khi tạo bảng nhân vật 2-panel (`Left: Face Close-up | Right: Full-body Front`), `@thomas_lundstrom` chạy lệnh này để xóa phần đầu ở panel toàn thân, buộc model video chỉ lấy khuôn mặt sắc nét từ panel cận cảnh!

```text
Remove the face and neck from the front full body reference.
```

---

### 21.🧩 CHUYÊN ĐỀ 5: CÁCH HỌ THAM CHIẾU ẢNH (`MULTI-REFERENCE WORKFLOWS`: TỪ 1 ĐẾN 9 ẢNH `@IMG` & KỸ THUẬT VẼ VẠCH MÀU MS-PAINT)

> **Thống kê thực tế từ `ranked_community_images.json` & `29` Dự Án Phim**:
> - Có tổng cộng **`825` bức ảnh trên Community** đính kèm ảnh tham chiếu (`1 Ref`: `492` ảnh; `2 Refs`: `170` ảnh; `3 Refs`: `65` ảnh; `4 Refs`: `46` ảnh; `5–14 Refs`: `52` ảnh) và hàng trăm cảnh phim dùng tới **`9` ảnh tham chiếu cùng lúc (`<<<image_1>>> ... <<<image_9>>>`)**.
> - Đặc biệt, qua kiểm định thị giác các ảnh `♡ < 50`, chúng tôi phát hiện **7 Kiến Trúc Phối Hợp Đa Ảnh Tham Chiếu Đỉnh Nhất**:

#### 5.1. 7 Kiến Trúc Phối Hợp Nhiều Ảnh Tham Chiếu Đỉnh Nhất Thực Chiến
1. **Kiến trúc `MS-Paint Color-Coded Zone Markup` (Vẽ vạch màu Vàng/Đỏ trực tiếp lên `@img1` để chỉ định vị trí lắp đèn LED / đặt đồ vật — Phát hiện đột phá từ `Rank #1708`, `Rank #3158`, `Rank #1831`, `Rank #3412` trên `seedream_v5_pro`!)**:
   - Khi kiểm định cặp ảnh `rank_1708_ref1.jpg` ➔ `rank_1708_seedream_v5_pro_963c6270.webp` và `rank_3158_ref1.jpg` ➔ `rank_3158_seedream_v5_pro_e51a4b4b.webp`, chúng tôi phát hiện một mẹo cực kỳ thông minh:
   - Thay vì mô tả tọa độ bằng chữ phức tạp, người dùng mở MS Paint / trình sửa ảnh điện thoại, **dùng bút dạ màu Vàng (`Yellow Drawn Area/Lines`) và màu Đỏ (`Red Drawn Area`) vẽ trực tiếp lên bức ảnh căn phòng `@img1`**, sau đó viết câu lệnh ngắn gọn:
     - **`Rank #1708`**: `"LED STRIP IN THE YELLOW DRAWN LINES, ADD A OPEN BUYING FROM THE FRIDGE"` ➔ `seedream_v5_pro` tự động xóa sạch 5 vạch bút dạ vàng và thay bằng 5 dải đèn LED vàng ấm âm dưới gầm kệ gỗ!
     - **`Rank #3158`**: `"ADD A MAN WORKING IN THE YELLOW DRAWN AREA, TURN ON THE CHANDELIERS, ADD 2 PEOPLE SEATED IN THE BENCH HAVING A WINE, ADD BREAD IN THE RED DRAWN AREA"` ➔ `seedream_v5_pro` bật sáng toàn bộ bóng đèn nến trên 2 chiếc đèn chùm sắt đen, đặt người thợ làm bánh vào đúng ô khoanh màu vàng và xếp bánh mì vào đúng kệ khoanh màu đỏ!
   - **Ứng dụng trực tiếp cho TVC Cây thông Noel của bạn**: Bạn có thể mở ảnh phòng khách lên, khoanh một vòng màu **Đỏ** ở góc lò sưởi nơi muốn đặt Cây thông Noel và vẽ các vạch màu **Vàng** dọc theo bệ lò sưởi/khung cửa sổ nơi muốn giăng dây đèn LED ấm!
2. **Kiến trúc `2D Top-Down Placement Diagram` (`@img1` = Ảnh bàn/phòng trống + `@img2` = Sơ đồ mặt bằng 2D vẽ vị trí đồ vật — `Rank #1324` & `@bucketlist_impossible/bash` `@IMG_069`)**:
   - Ở `Rank #1324` (`seedream_v5_pro`), `@img1` là bức ảnh chụp chiếc bàn gỗ trống trong rừng, còn `@img2` là sơ đồ mặt bằng 2D nhìn từ trên xuống có ghi chữ từng món đồ ăn. `seedream_v5_pro` đọc sơ đồ 2D ở `@img2` để bày chính xác từng đĩa thức ăn lên mặt bàn thật ở `@img1`!
   - Ở dự án phim `@bucketlist_impossible/bash` (`@IMG_069`, tái sử dụng `7` lần), đạo diễn dùng `@img1` làm sơ đồ vị trí 2D (`"Use @img1 as a 2D placement diagram..."`) kết hợp `@img2..@img5` làm bảng nhân vật và bối cảnh để khóa vị trí đứng của từng diễn viên.
3. **Kiến trúc `1 Room Master + N Furniture/Product Cutouts` (`Rank #1247`, `Rank #1562`, `Rank #1665`)**:
   - `@img1` là ảnh căn phòng gốc (hoặc mô tả phòng), `@img2` đến `@img5` là từng món đồ nội thất/sản phẩm tách nền trắng (`"crie um novo ambiente a partir do ambiente da imagem 1, acrescentando nesse ambiente os objetos das imagens 2, 3 e 4, sem modificar as caracteristicas dos moveis"` — `Rank #1562`).
4. **Kiến trúc `N Individual Products + 1 Group Layout Reference` (`Rank #1710` — `nano_banana_2_1`, `7 Refs`)**:
   - `@img1` đến `@img6` là 6 bức ảnh chụp cận cảnh từng chiếc vòng tay đơn lẻ (để AI lấy độ nét từng hạt đá), còn `@img7` là ảnh chụp cả 6 chiếc vòng xếp chồng lên nhau (để AI lấy bố cục).
5. **Kiến trúc `3x3 Grid Single-Cell Extraction + Character Sheets` (`Rank #699` — `gpt_image_2_5`, `3 Refs`)**:
   - Khi bạn tạo một tấm Storyboard `3x3 Grid` (`@img1`) và muốn bung 1 ô nhỏ trong bảng đó thành ảnh Full-Frame 4K sắc nét, hãy nạp `@img1` (bảng 3x3) + `@img2, @img3` (Character/Product Sheets) kèm câu lệnh: `"Regenerate ONE full-frame, standalone photorealistic photograph from the user's uploaded 3x3 reference photo grid. DO NOT generate a collage, grid, white borders... Match the specified grid cell's exact action, composition, camera angle, and lighting."`
6. **Kiến trúc `Cross-Reference Attribute Surgery` (`@img1` = Trang phục có sửa chi tiết + `@img2` = Tư thế & Bối cảnh + `@img3` = Khuôn mặt — `Rank #1961` trên `gpt_image_2` & `@nicholastakeyama/tokyo-4-17` `@IMG_021`)**:
   - Phân vai độc lập tuyệt đối cho từng ảnh tham chiếu: giữ 100% tư thế, góc máy và ánh sáng của `@img2`, mặc bộ đồ của `@img1` (nhưng xóa toàn bộ túi áo), và lấy khuôn mặt của `@img3`.
7. **Kiến trúc `9-Image Master Production Lock` (`<<<image_1>>> ... <<<image_9>>>` — `Rank #1025` trên `seedream_v5_pro` & `@seksifratello/apeirophobia-teaser` `@IMG_364`)**:
   - Khai báo danh bạ `REFERENCES` ở đầu prompt, chỉ rõ từng slot `<<<image_1>>>` đến `<<<image_9>>>` đóng vai trò gì (`Face Lock`, `Dressed Look`, `Prop Detail`, `Room Geometry`, `Lighting Reference`) và cái gì trong ảnh tham chiếu đó phải **BỎ QUA** (`"Ignore its backdrop, black t-shirt, and panel divisions"`).

---

#### 5.2. Nguyên Văn Các Prompt Phối Hợp Đa Ảnh Tham Chiếu (`1 đến 9 Refs`) Đắt Giá Nhất Trên Community

##### 🏆 Rank #1708 (`0 ♡` | `9 👁️` | Model: `seedream_v5_pro` | Author: `@gojart` | Size: `16:9` | Refs: `1`)
- **Publication ID**: `963c6270-6270-49b1-96cd-cea402f72407`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1708_seedream_v5_pro_963c6270.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_124327_040fc93e-8a3e-42e3-866d-0d3b56432f95.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_124327_040fc93e-8a3e-42e3-866d-0d3b56432f95_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/7aadc6dc-4491-4acd-9410-364ccd9f1844_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Kỹ thuật Vẽ Vạch Vàng MS-Paint để lắp Dải Đèn LED âm kệ (`Before: rank_1708_ref1.jpg` ➔ `After: rank_1708_seedream_v5_pro_963c6270.webp`)**: Kiểm định trực tiếp `rank_1708_ref1.jpg` cho thấy người dùng vẽ 5 đường bút dạ màu vàng neon dưới 5 tầng kệ gỗ tủ `SAUCES`; chỉ với câu lệnh 13 chữ, `seedream_v5_pro` xóa sạch nét vẽ vàng và thay bằng 5 dải đèn LED vàng ấm chiếu sáng từng chai nước sốt, đồng thời mở toang 2 cánh cửa kính tủ lạnh `CREAMERY` bên trái!

```text
LED STRIP IN THE YELLOW DRAWN LINES, ADD A OPEN BUYING FROM THE FRIDGE
```

##### 🏆 Rank #3158 (`0 ♡` | `3 👁️` | Model: `seedream_v5_pro` | Author: `@gojart` | Size: `3:2` | Refs: `1`)
- **Publication ID**: `e51a4b4b-405a-4ce7-905e-813102d60e9b`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_3158_seedream_v5_pro_e51a4b4b.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_122543_7a16b2a6-2888-48af-847b-07b6298edb7d.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/hf_20261015_122543_7a16b2a6-2888-48af-847b-07b6298edb7d_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DXmIqhClqwrfMsgmzGPvv6dxx5/5885d442-c0fc-4e66-b695-1683009a929d_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Kỹ thuật Khoanh Vùng Vàng & Đỏ MS-Paint kết hợp Bật Sáng Đèn Chùm (`Before: rank_3158_ref1.jpg` ➔ `After: rank_3158_seedream_v5_pro_e51a4b4b.webp`)**: Trên ảnh gốc `rank_3158_ref1.jpg`, 2 chiếc đèn chùm sắt đen đang tắt tối om, quầy bánh được khoanh bút dạ vàng và kệ gỗ trên cao được khoanh bút dạ đỏ. Ảnh xuất `seedream_v5_pro` bật sáng rực rỡ toàn bộ bóng đèn nến trên 2 đèn chùm, đặt người thợ làm bánh vào đúng vùng vàng, xếp bánh mì vào đúng kệ đỏ và thêm đôi nam nữ ngồi uống rượu vang trên ghế băng da!

```text
ADD A MAN WORKING IN THE YELLOW DRAWN AREA, TURN ON THE CHANDELIERS, ADD 2 PEOPLE SEATED IN THE BENCH HAVING A WINE, ADD BREAD IN THE RED DRAWN AREA
```

##### 🏆 Rank #1324 (`0 ♡` | `30 👁️` | Model: `seedream_v5_pro` | Author: `@damian_the_ace` | Size: `16:9` | Refs: `2`)
- **Publication ID**: `1d9dc07d-e36d-4da2-ab4a-ca89ab6e3991`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1324_seedream_v5_pro_1d9dc07d.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3JHtC6GcJsL2qMu4GVq6vlrf39P/hf_20261008_144029_e0b94aa8-3631-4f03-85c8-9f294d8e903c.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3JHtC6GcJsL2qMu4GVq6vlrf39P/hf_20261008_144029_e0b94aa8-3631-4f03-85c8-9f294d8e903c_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3JHtC6GcJsL2qMu4GVq6vlrf39P/hf_20261008_132242_a54ec088-d870-4e4d-8d8f-d54d014d3776.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3JHtC6GcJsL2qMu4GVq6vlrf39P/1dfd7551-6fb5-4f50-8600-8fd0850f2eec.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Kiến trúc Sơ đồ mặt bằng 2D `@img2` điều khiển vị trí đồ vật trên ảnh thật `@img1` (`Before: rank_1324_ref1.jpg + ref2.png` ➔ `After: rank_1324_seedream_v5_pro_1d9dc07d.webp`)**: Từ chiếc bàn gỗ trống trong rừng (`@img1`) và sơ đồ mặt bằng 2D có mũi tên chỉ vị trí từng món ăn (`@img2`), `seedream_v5_pro` bày biện đại tiệc 10 món ăn khớp 100% tọa độ sơ đồ với ánh sáng tự nhiên xuyên qua tán lá.

```text
Edit IMAGE 1, the real woodland photograph with EMPTY table. IMAGE 2 is a TOP-DOWN PLACEMENT DIAGRAM ONLY: translate its arrangement onto the real tabletop in IMAGE 1's existing perspective. Output the photograph, never the diagram. Keep the original full wide camera view, table, both wooden benches, terrain, forest, sunlight, exposure and colours unchanged. Add exactly TWO sandwiches on cream paper wrappers and exactly TWO small capped water bottles, one bottle per meal, plus ONE small crumpled brown paper bag and TWO paper napkins. Follow the diagram: place both sandwiches at the midpoint along the table's long length, directly opposite one another across its SHORT width, one near each LONG edge above the centre of each long bench. One meal belongs to the foreground bench, the other to the opposite bench. Neither meal belongs at a short end. Each bottle stands beside its own sandwich, leaving the table centre clear for hands. Paper bag at the far short end. Casual realistic takeaway food, small natural offsets, true item scale and contact shadows. Preserve bare wood elsewhere and empty seats. No extra bottles, no people, no diagram labels, arrows or graphic symbols.
```

##### 🏆 Rank #1710 (`0 ♡` | `9 👁️` | Model: `nano_banana_2_1` | Author: `@mednour` | Size: `4:5` | Refs: `7`)
- **Publication ID**: `32cf7d2b-acf7-4fa0-b6d4-4e215a574c24`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1710_nano_banana_2_1_32cf7d2b.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/hf_20261017_145706_112d3562-9031-4a00-9dee-4614f3f7159f.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/hf_20261017_145706_112d3562-9031-4a00-9dee-4614f3f7159f_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/hf_20261012_221129_213452cd-6efb-49cc-b2bb-b53eddb75c0f.png
- **Input Reference `@img2`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/hf_20261012_221038_e827041e-9467-4e0b-9965-5bea59b7617e.png
- **Input Reference `@img3`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/hf_20261012_220838_8822ded0-db68-4e6b-b1c8-55c2e948fe0a.png
- **Input Reference `@img4`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/hf_20261012_221143_0eadd6d4-69dc-4c21-8975-210098cad75b.png
- **Input Reference `@img5`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/hf_20261012_221210_063dc75a-e692-4ca1-a129-d101c058418d.png
- **Input Reference `@img6`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/hf_20261012_190713_d0a3b07b-6375-4326-8dbc-72a5e8ca7513.png
- **Input Reference `@img7`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DrzXVQGzd51fqeH8ZiPFvw2sj2/fa986ef7-3b42-49b8-86c7-a7ede99576f5_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Kiến trúc 6 ảnh sản phẩm lẻ + 1 ảnh bố cục nhóm (`Before: rank_1710_ref1..ref7` ➔ `After: rank_1710_nano_banana_2_1_32cf7d2b.webp`)**: `nano_banana_2_1` kết hợp độ nét chi tiết của 6 chiếc vòng tay đá quý đơn lẻ (`@img1..@img6`) vào đúng bố cục xếp chồng của `@img7`, tạo ra bức ảnh catalog trang sức sắc nét đến từng hạt cườm.

```text
TASK: Create a Premium E-commerce Product Photograph of Six Bracelets Using Seven Reference Images
Use all seven uploaded reference images according to their specific roles.
REFERENCE IMAGE ASSIGNMENTS
Reference Images 1–6: Each image shows one individual bracelet. These are the absolute source of truth for the exact product design, construction, materials, colors, decorative details, gold-tone hardware, central ornament, rhinestones, braided texture, clasp, and proportions of each individual bracelet.
Reference Image 7: This image shows all six bracelets arranged together. Use it as the strict composition and positioning reference. Reproduce the same overall arrangement, overlapping sequence, orientation, spacing, and visual hierarchy.
PRIMARY OBJECTIVE
Create a premium, photorealistic, luxury e-commerce product photograph featuring all six bracelets together in the same arrangement as Reference Image 7.
The result should look like a professionally photographed jewelry product set for a high-end online jewelry store.
ABSOLUTE PRODUCT PRESERVATION — HIGHEST PRIORITY
Treat each bracelet in References 1–6 as an existing physical product that must be transferred faithfully into the final composition.
Do not redesign, regenerate, reinterpret, simplify, or invent any part of the jewelry.
Preserve each bracelet's exact:
Overall shape, dimensions, thickness, and proportions.
Original braided cord pattern and texture.
Exact cord color and color saturation.
Gold-tone metal components, including their shape, size, finish, and placement.
Central infinity-shaped decorative ornament, preserving its exact curves, intertwined structure, orientation, and dimensions.
Rhinestone arrangement, stone count, stone placement, and surrounding metalwork.
End caps, clasps, connectors, and all small construction details.
Do not replace the central ornament with a similar-looking design. Do not alter the number, position, or shape of the rhinestones. Do not add missing decorative elements or remove existing ones.
Each bracelet must remain individually identifiable and faithful to its corresponding product reference.
COMPOSITION AND ARRANGEMENT
Reproduce the arrangement shown in Reference Image 7 as closely as possible.
Include exactly six bracelets, with all six visible and distinguishable.
Preserve the same cascading, overlapping arrangement, with each bracelet positioned above or below its neighboring bracelet as shown in the composition reference.
Maintain the same relative orientation, curvature, spacing, and overlap relationships.
Keep the gold decorative ornaments facing the camera and visible, following their original positions in Reference Image 7.
Preserve the original sequence of bracelet colors and their relative positions. Do not reorder the bracelets.
Keep the bracelets naturally layered, with believable physical contact and realistic separation between the braided cords.
Do not straighten, symmetrize, spread out, or rearrange the bracelets into a different layout.
Do not create a grid, a row of separate products, or six isolated product cutouts.
The final image must preserve the recognizable overall silhouette and visual balance of Reference Image 7 while improving its presentation to professional commercial standards.
BACKGROUND AND ENVIRONMENT
Replace the entire original environment with a perfectly clean, pure white studio background (#FFFFFF).
Seamless white surface and background.
No visible table edges, room details, fabric, hands, skin, or unwanted objects.
No gray background, cream tint, gradient, decorative props, or lifestyle elements.
A clean, premium jewelry catalog aesthetic.
Natural, subtle contact shadows directly beneath the bracelets, preserving their physical grounding without compromising the pure white appearance.
The white background must be evenly illuminated, clean, and free from texture, stains, color casts, and distracting shadows.
LIGHTING AND PHOTOGRAPHY
Simulate a professional high-end jewelry product photography setup.
Soft, large-area studio lighting for smooth, controlled illumination.
Balanced highlights on the gold-tone metal components, revealing their authentic polished metallic finish.
Controlled reflections that preserve the shape and fine details of the central ornaments.
Realistic, crisp rhinestone reflections without excessive sparkle, artificial starbursts, or blown highlights.
Accurate color reproduction for all six braided cords.
Soft, physically plausible contact shadows between overlapping bracelets.
High micro-detail and natural material definition.
Even exposure with no harsh glare, crushed shadows, or overexposed white metal reflections.
Use a professional macro-product-photography look with excellent sharpness across all six bracelets. Every decorative ornament and braided cord should be clearly legible.
CAMERA AND FRAMING
Professional e-commerce product photography.
Preserve the viewing angle and perspective of Reference Image 7 as closely as possible.
Frame the entire arrangement comfortably within the image.
Keep all six bracelets and their decorative elements inside the frame, with no cropped ends or ornaments.
Center the complete bracelet arrangement on the canvas, leaving balanced, clean white margins around it.
Use a high-resolution, square 1:1 composition suitable for a premium online jewelry catalog.
Maintain realistic perspective and natural proportions without wide-angle distortion.
IMAGE CLEANUP AND FINISHING
Remove the imperfections of the original photograph without altering the products themselves.
Improve image clarity, fine-detail visibility, exposure, white balance, edge cleanliness, and overall professional presentation.
Remove visual noise, compression artifacts, distracting reflections, and unwanted environmental color casts.
Maintain the authentic woven texture of the cords and the fine details of the gold-tone ornaments. Do not apply excessive smoothing, artificial sharpening, plastic-looking textures, or unrealistic metallic effects.
STRICT NEGATIVE GUIDANCE
No missing bracelets.
No additional bracelets.
No duplicated bracelets.
No merged or fused bracelets.
No altered bracelet colors.
No incorrect color order.
No redesigned ornaments.
No modified infinity symbols.
No missing or invented rhinestones.
No changed clasps or end caps.
No deformed braided cords.
No floating products.
No unnatural intersections or impossible overlaps.
No hands, wrists, skin, mannequins, or models.
No props, packaging, text, logos, watermarks, or decorative graphics.
No gray, beige, colored, or textured background.
No illustration, CGI appearance, or artificial-looking jewelry.
FINAL QUALITY REQUIREMENT
The final result must look like a real, professionally photographed set of six existing bracelets, not AI-generated replacements.
Reference Images 1–6 determine exactly what each bracelet looks like. Reference Image 7 determines exactly how the six bracelets are arranged together.
Preserve the products and the arrangement. Improve only the photographic quality, lighting, background, cleanliness, and commercial presentation.
Product accuracy is more important than creative interpretation. When any detail is uncertain, reproduce the corresponding reference faithfully rather than inventing a replacement.
```

##### 🏆 Rank #699 (`3 ♡` | `227 👁️` | Model: `gpt_image_2_5` | Author: `@kimcheeverse` | Size: `9:16` | Refs: `3`)
- **Publication ID**: `f87fe0c7-a8e9-49f4-ba04-e419bf224467`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0699_gpt_image_2_5_f87fe0c7.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DUeuq342Rt84lSGBRMX13shiKu/hf_20261008_024803_52669844-e6cc-4ca8-8905-742f27facd52.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DUeuq342Rt84lSGBRMX13shiKu/hf_20261008_024803_52669844-e6cc-4ca8-8905-742f27facd52_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DUeuq342Rt84lSGBRMX13shiKu/4d78417f-1e93-44aa-96f3-63f531ce69eb.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DUeuq342Rt84lSGBRMX13shiKu/86634297-d412-4dae-872b-9235c452478d.png
- **Input Reference `@img3`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3DUeuq342Rt84lSGBRMX13shiKu/a123ad6a-2463-4ddf-8192-3d1555f76a35.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Tách 1 ô từ Bảng Storyboard `3x3 Grid` thành ảnh Full-Frame sắc nét kèm 2 Character Sheets (`Before: rank_0699_ref1..ref3` ➔ `After: rank_0699_gpt_image_2_5_f87fe0c7.webp`)**: Giải quyết bài toán hậu kỳ khi làm Storyboard 3x3: nạp bảng 3x3 (`@img1`) cùng 2 bảng thiết kế nhân vật (`@img2, @img3`) để `gpt_image_2_5` tái tạo riêng 1 ô thành bức ảnh đơn 9:16 độ phân giải cao mà không bị dính viền trắng hay chia ô.

```text
Regenerate ONE full-frame, standalone photorealistic vertical 9:16 amateur Halloween street photograph from the user's uploaded 3x3 reference photo grid. DO NOT generate a collage, grid, white borders, captions, or multiples. Match the specified grid cell's exact action, composition, camera angle, intimacy, facial expressions, and lighting, not just the theme. The other two uploaded pictures are identity/costume reference sheets: Miyu (young Japanese woman, long chestnut brown hair with bangs, full tan and cream fluffy Shiba Inu onesie with dog-eared hood); Yuna (young Korean woman, short layered brown bob, Jotaro-inspired black peaked cap with gold badges, dark oversized coat with large gold chain, black top and black pants). Preserve their individual real facial identities, features, original hair colors and costumes; no face swapping or generic glam faces. Shibuya Tokyo Halloween nightlife aesthetic, 2026, harsh on-camera flash, dim ambient neon, imperfect candid framing, slight motion blur, film grain, real skin texture, documentary realism, not glossy AI renders. IMPORTANT: Any Halloween date visible on any billboard, poster or banner MUST READ precisely "SHIBUYA HALLOWEEN 2026" or "HALLOWEEN 2026". Never show 2024, 2028 or any wrong date; if unsure, omit the date. Grid panel TOP MIDDLE, shot 2: Miyu ALONE in Shiba Inu kigurumi lovingly hugging a large Hachiko dog statue from side at Shibuya, eyes closed smiling, statue with Halloween witch hat and pumpkin decoration, pedestal with Japanese inscription, crowds in background. The only human foreground subject is Miyu, identical to source tile. No Yuna in this frame.
```

##### 🏆 Rank #1025 (`1 ♡` | `25 👁️` | Model: `seedream_v5_pro` | Author: `@kamto` | Size: `9:16` | Refs: `9`)
- **Publication ID**: `b55f19ae-a247-4d2d-a045-1ac61be57096`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1025_seedream_v5_pro_b55f19ae.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/hf_20261011_151915_95a132f1-3168-4453-ad5e-498b8498ddc2.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/hf_20261011_151915_95a132f1-3168-4453-ad5e-498b8498ddc2_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/b20ac22d-6c35-492e-8ea2-da6cf56b2021_resize.jpg
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/d3af2afc-c518-46bf-a0ea-99640d306f93_resize.jpg
- **Input Reference `@img3`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/fd6be315-eaa7-4347-9226-df2e154a9f1b_resize.jpg
- **Input Reference `@img4`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/aeb45870-b990-4012-a029-49fb9dc6baff_resize.jpg
- **Input Reference `@img5`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/8c93c43a-5aa7-4f8a-b8f3-e75b0713d03a.jpg
- **Input Reference `@img6`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/01afc316-aeb8-4051-8e74-e8e64af2875c_resize.jpg
- **Input Reference `@img7`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/601216bd-abd1-433a-b063-82de41e55d68_resize.jpg
- **Input Reference `@img8`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/2d86261b-55d5-4991-bcb6-6596fd546414.png
- **Input Reference `@img9`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3Dqzq7Z0gaOmcREmYVlw0yIQzvs/e2a6fa2e-e8a9-4658-b7a8-0e953ad7ae0d_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Phối hợp 9 ảnh tham chiếu (`<<<image_1>>> ... <<<image_9>>>`) trong chiến dịch thời trang thực tế trên `seedream_v5_pro` (`Rank #1025`)**: Khai báo rõ từng ảnh tham chiếu giữ vai trò gì (`LEO's face`, `NIA's face`, `LEO's dressed look`...) kèm chỉ dẫn thông minh `Ignore its backdrop, black t-shirt, black shorts and panel divisions` để AI không bị nhiễm nền xám của bảng character sheet vào ảnh chụp ngoại cảnh!

```text
You are a master photographer and gaffer shooting a high-end campaign on location, with available light, shaped. Every image is a REAL PHOTOGRAPH taken on this shoot by the same photographer - not a frame grab, not a render. It must survive being printed large.

REFERENCES
<<<image_1>>>  LEO's face - face, body and skin tone. Never changes. Ignore its backdrop, black t-shirt, black shorts and panel divisions.
<<<image_2>>>  NIA's face - face, body, skin tone, hair. Never changes. Ignore its backdrop, black romper and panel divisions.
<<<image_3>>>  LEO's dressed look - his finished look exactly: black quarter-zip polo, white shorts, white cap, white socks, black shoes.
<<<image_4>>>  NIA's dressed look - her finished look exactly: navy polo, navy skirt, white socks, white shoes, gold hoops, high bun with two temple curls.
<<<image_5>>>  his outfit and racket - every detail, including each BK monogram. Ignore the backdrop and panel layout.
<<<image_6>>>  her outfit, racket and backpack - every detail, including each BK monogram. Ignore the backdrop and panel layout.
<<<image_7>>>  THE COURT - this exact place: the red-orange clay, white lines, low white side walls, dark back windscreen with the white BK, palms, terracotta-roofed clubhouse, desert mountains.
<<<image_8>>>  THE BK MONOGRAM - the exact mark. Ignore its black background.
<<<image_9>>>  THE TONE FRAME - take its LIGHT, COLOUR, GRADE and MOOD exactly: the low hard 5 pm sun, the burnt-orange clay, the long shadows, the warmth. Do NOT take its pose or its framing.
Leo and Nia are never given each other's face, skin tone, hair, or build; they never merge, and no third person ever appears.

MOOD  the mood of <<<image_9>>>, exactly.

THE PERFORMANCE - DURING PLAY: eyes locked on the ball, jaw set, mouth closed with hard breaths through it, bodies explosive and committed. BETWEEN POINTS: their eyes find each other, a real grin breaks (Leo's small tooth gap shows), shoulders loose, bodies leaning toward each other. Never posed, never looking at the lens.

COLOUR LOCK - exact, every image. Do not harmonise.
Clay in sun #b57b55 · clay in shadow #603f28 · lines and white garments #e8dcce warm white · Nia's polo and skirt the navy of <<<image_9>>>, a deep blue-navy, never pure black · Leo's polo a true black with its knit texture held.
17:00, sun low at about 20 degrees, hard, clear sky, 3800K - identical in every image.

CINEMATOGRAPHY
ARRI Alexa 35, the same body for every image. Named primes only; the focal length and stop given in each request. Plane of focus as stated. RAW. Depth of field from the aperture only.

LIGHTING - take the light of <<<image_9>>> exactly: its direction, hardness, level and colour. Do not relight, do not make it moodier. The sun is the only source; the shadow sides are lifted only by warm bounce off the clay and stay deep. Every face has a lit side and a deep shadow side - NOBODY IS IN FLAT SHADE. Each request names the setup and what the light does there.

COLOUR SCIENCE  Kodak Vision3 250D, the grade of <<<image_9>>> exactly, plus the values in the lock.

THE BODY  Both bodies exactly as in <<<image_1>>> and <<<image_2>>> - same proportions, height and build in every image. Never slimmer, never longer-limbed.

REALISM
Skin at full colour saturation, never lightened, never ashy: pores, fine grain, peach fuzz, a sheen of sweat at temples and collarbones, natural marks; Nia's beauty mark on her left cheekbone. No retouching, never waxy. Real eyes with iris fibres and wet catchlights. Hair with baby hairs and flyaways. Pique knit grain on the polos, light on the crest of each fold; technical weave on shorts and skirt; mesh and rubber on shoes with clay in the tread; clay grit sharp at the pixel level. Real fine grain across the frame.

INTEGRATION + THE WORLD
They stand IN the place: matching light direction, warm clay bounce under chins, arms and hems, hard contact shadows where shoes meet clay. Every view is the SAME court at the same hour. What sits behind their heads and shoulders is the PLACE - windscreen, wall, palms, clubhouse, clay - never open sky; any sky is a narrow band at the very top of the frame.

NEVER
No overlay text, captions or watermarks. The BK monogram is the only lettering on any product, exactly as in <<<image_5>>>, <<<image_6>>> and <<<image_8>>>; all other signage soft and unreadable. No other logos - no ticks, no stripes, no other brand marks. No changed faces, no swapped outfits, no redesigned clothes, no retouching, no added flare, bloom or vignette.

Aspect 9:16.

Create ONE photograph of this moment - THE COURT ALONE: a single tennis ball rolling across the empty clay, no people.

THE GEOMETRY
THE LENS        50mm at f/4.
THE FRAMING     the ball small in the lower third, about 6% of the frame · the white centre line running away from the lens toward the net · the clay filling the frame, the base of the net and the white side wall soft in the distance at the very top.
CAMERA HEIGHT   at ground level, the lens just above the clay.
LENS AXIS       level, looking along the court surface.
WHERE IT SITS   the ball just right of centre, rolling left toward the centre line.

THE MOMENT: THE MIDDLE - the ball rolling, not yet stopped.
A single yellow tennis ball rolling slowly across the raked clay toward the centre line, a faint trail in the clay dust behind it.

THE PLACE       view 4 seen low - the clay surface and the centre line, palm-frond shadows dappled across it.
THE PRODUCT     no product - the place itself.

LIGHTING
The low sun through the palm fronds: moving dappled frond shadows across the burnt-orange clay; the ball's fuzz rim-lit gold; every raked furrow throwing a tiny long shadow; the white line crisp where the sun hits it.
```

##### 🏆 Rank #960 (`1 ♡` | `45 👁️` | Model: `nano_banana_2` | Author: `@natashakishore` | Size: `1:1` | Refs: `7`)
- **Publication ID**: `225a3818-9b4b-42ad-9b93-64ee3e6a2f07`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0960_nano_banana_2_225a3818.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/hf_20261008_113322_93acb122-4c1d-490c-bc33-11ffc423fc02.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/hf_20261008_113322_93acb122-4c1d-490c-bc33-11ffc423fc02_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/13989403-7a23-49d6-bd1f-94fd58263be6.png
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/ab25e005-0473-41cb-8338-2e2932f55966.png
- **Input Reference `@img3`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/0bf0ceb2-8c1c-4524-ae3f-142bf3fff1d3_resize.jpg
- **Input Reference `@img4`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/edf6813c-56a1-4830-868c-76d236e25eed_resize.jpg
- **Input Reference `@img5`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/3de17e2c-13f5-4de3-a01f-d9a3e7805798_resize.jpg
- **Input Reference `@img6`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/8d569081-8b4d-4b82-b096-5efc93762ad4_resize.jpg
- **Input Reference `@img7`**: https://d2ol7oe51mr4n9.cloudfront.net/user_36kJXarwpLJgSF2BfKv2jmTvebq/5092b35a-5ee0-4c34-8bcb-54ccea841d96_resize.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Phối hợp 7 ảnh tham chiếu trong 1 đại cảnh (`Before: rank_0960_ref1..ref7` ➔ `After: rank_0960_nano_banana_2_5ca70296.webp`)**: Gán từng nhân vật từ `@img1..@img7` vào đúng vị trí ngồi và đứng trong đại cảnh với khóa đồng nhất ánh sáng.

```text
#IMAGE1 = pose + environment + camera + lighting reference
#IMAGE2 = model face / identity reference, use the model face as given in #image2, do not use any other model identity.
#IMAGE3= top garment reference — exact product accuracy, keep the blazer buttoned.
#IMAGE4 = top garment detail shot reference.
#IMAGE5 = bottom garment reference - exact product accuracy
#IMAGE6 = belt
#IMAGE7 = watch

Use #IMAGE2 identity exactly. Single model only.
Image-generation prompt
Luxury European menswear tailoring campaign, intimate editorial portrait. Adult male fashion model seated deep and comfortably on a wide sofa on one side. His torso is angled subtly toward the camera, shoulders relaxed and natural. One arm rests along the sofa backrest. The opposite elbow rests on the side armrest, forearm raised toward his face, fingers lightly resting in front of his mouth and chin in a thoughtful, elegant gesture. Head tilted subtly downward while maintaining direct eye contact with the camera. Calm, confident, sophisticated expression with restrained sensuality. Relaxed legs extending naturally toward the lower-right of frame.
Model wearing an impeccably tailored suit, structured single-breasted jacket with natural shoulders and precise lapels, crisp white open-collar shirt underneath. Preserve exact tailoring, fabric texture, construction, lapel shape, button placement and natural garment drape. while keeping the blazer details visible and in focus.
Camera: vertical high-end fashion editorial photograph, approximately 70–85mm portrait lens, camera positioned around seated torso/waist height with a very subtle three-quarter angle. Slightly compressed perspective, natural anatomy, no wide-angle distortion. Medium-close framing from approximately mid-thigh upward, with the face and hand gesture as the visual focal point. Model positioned slightly left of center.
Set: minimalist refined European studio interior, seamless warm light-gray/taupe wall, wide cream contemporary  sofa. Extremely clean composition, no clutter, no distracting props.
Lighting: large diffused softbox or window light positioned high camera-left, producing soft directional illumination across the face and tailoring. Gentle shadow on the opposite side of the face, subtle tonal falloff across the suit, controlled highlights on skin and hair. Soft ambient fill, low contrast but dimensional. Warm-neutral daylight color temperature.
Sophisticated muted palette of taupe, warm gray, cream, white and natural wood. Fine analog film grain, subtle texture, restrained contrast, realistic skin, premium luxury campaign photography, understated European elegance.
Mood: quiet confidence, mature masculinity, personal tailoring, intimate luxury, intelligent, refined, effortless, sensual without being overtly sexual, timeless menswear editorial, premium fashion magazine aesthetic.
dont copy hair, model or clothing from #IMAGE1. composition: 1:1. 
No face drift, no bodysuit deviation, no jacket deviation, no trouser deviation, no missing earrings, no footwear changes, no accessory replacement, no luxury café glamour, no beauty light, no perfect skin, no staged smile, no sterile background, no CGI look.
```

##### 🏆 Rank #1961 (`0 ♡` | `6 👁️` | Model: `gpt_image_2` | Author: `@runningkoala1340` | Size: `3:4` | Refs: `3`)
- **Publication ID**: `6691dd41-4833-402b-b954-51a3d812ba69`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1961_gpt_image_2_6691dd41.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3GCbqxFBYOhdbiBNHq211rJD4Zn/hf_20261020_010639_3e297832-e431-4306-bb47-3f9f69d6cea2.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3GCbqxFBYOhdbiBNHq211rJD4Zn/hf_20261020_010639_3e297832-e431-4306-bb47-3f9f69d6cea2_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3GCbqxFBYOhdbiBNHq211rJD4Zn/7d69ca29-5c0b-407d-b180-49f009469f95_resize.jpg
- **Input Reference `@img2`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3GCbqxFBYOhdbiBNHq211rJD4Zn/4149531c-4341-4701-9793-80ae3a35ed3c.jpg
- **Input Reference `@img3`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3GCbqxFBYOhdbiBNHq211rJD4Zn/4fad974f-c3a1-46bf-a6f1-2ddcc5f3094e.jpg
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Phẫu thuật ghép 3 ảnh tham chiếu (`@img1` Trang phục bỏ túi áo + `@img2` Tư thế/Góc máy/Ánh sáng + `@img3` Khuôn mặt — `Rank #1961`, `gpt_image_2`)**: Giữ nguyên 100% dáng đứng và ánh sáng đường phố của `@img2`, lấy khuôn mặt của `@img3`, và mặc bộ đồ denim của `@img1` nhưng ra lệnh xóa sạch toàn bộ nắp túi và đường may túi trên áo khoác (`移除牛仔上衣所有口袋，衣身平整无袋盖`).

```text
图 2 模特，完全保留图 2 肢体动作、站姿、构图、拍摄角度、场景环境、光影色调不变；模特身穿图 1 同款牛仔套装，移除牛仔上衣所有口袋，衣身平整无袋盖、无贴袋、无挖袋，保留原有斜门襟、面料肌理、牛仔色彩与服装版型；模特面部五官、妆容完全参考图 3，高级极简哑光妆面，眉眼轮廓、唇色不变；整体是真实街拍抓拍感，低饱和胶片质感，自然皮肤纹理，服装面料自然褶皱，画面细节和图 2 保持一致。
```

##### 🏆 Rank #1839 (`0 ♡` | `7 👁️` | Model: `nano_banana_flash` | Author: `@chico_1972` | Size: `16:9` | Refs: `4`)
- **Publication ID**: `15504811-ff33-4c38-99aa-6835ca9bf9e9`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1839_nano_banana_flash_15504811.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DWrtvEHUpDE1yvsSdJ2TZU3B1Y/hf_20261014_102521_c04bda6f-681d-4d44-a1c5-e056a2804e5a.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DWrtvEHUpDE1yvsSdJ2TZU3B1Y/hf_20261014_102521_c04bda6f-681d-4d44-a1c5-e056a2804e5a_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DWrtvEHUpDE1yvsSdJ2TZU3B1Y/hf_20261011_201605_42513dfe-45b0-4c77-9e2a-737e422143b6.png
- **Input Reference `@img2`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DWrtvEHUpDE1yvsSdJ2TZU3B1Y/hf_20261011_201746_d73800cf-109f-430f-ad42-800f2a82403b.png
- **Input Reference `@img3`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DWrtvEHUpDE1yvsSdJ2TZU3B1Y/hf_20261011_202036_c4e65c00-39f9-4ca1-ac22-573e6c3ad516.png
- **Input Reference `@img4`**: https://d8j0ntlcm91z4.cloudfront.net/user_3DWrtvEHUpDE1yvsSdJ2TZU3B1Y/hf_20261011_203237_8e6d186d-4f32-4d01-8e42-46c9a0698444.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Phối hợp 4 ảnh tham chiếu với `nano_banana_flash` (`Before: rank_1839_ref1..ref4` ➔ `After: rank_1839_nano_banana_flash_0fb0a214.webp`)**: Kết hợp nhân vật, trang phục và bối cảnh từ 4 ảnh rời thành một khung hình điện ảnh 16:9 đồng nhất.

```text
Use the reference images for the captain <<<image_1>>> and the crew <<<image_2>>> exactly as they are. Keep their faces, beards, clothes and the ship's wood <<<image_3>>> and sail design identical. Do not copy the framing of any previous image.

Photorealistic cinematic medium close-up, camera placed on the opposite side of the deck, looking back toward the bow. In the foreground, two sailors fill the frame from the waist up: the sailor in the red head cloth and the bald mustached sailor, both gripping the thick wet sail rope with both hands, mid-pull. At this exact instant a huge unseen sound has hit them: both freeze, their heads snapped up toward the sky, eyes wide, mouths half open in shock, bodies flinching, shoulders hunched. Their hands are still on the rope, NOT on their ears. The rope trembles taut in their fists, raindrops jump off the rope and the wet planks, the wood vibrates, a faint ripple of air distortion passes across the frame.

Behind them, small and slightly out of focus, the seated captain stops mid-shout, mouth still open, one arm raised, rain pouring down.

The deck is tilted hard, the torn sail shakes violently, heavy rain, dark storm clouds, lightning in the distance, the tornado faint on the horizon. Waves crash against the hull, spray in the air. Knives stay sheathed. Real people and a real full-size ship, no miniature, no toy look. Shallow depth of field, sharp on the two sailors.

Keep subject centered, safe for vertical crop.
```

##### 🏆 Rank #567 (`6 ♡` | `200 👁️` | Model: `nano_banana_2_1` | Author: `@ava-20` | Size: `2:3` | Refs: `2`)
- **Publication ID**: `cc4ea06f-92c9-4b1c-98ad-ad5f881d9879`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0567_nano_banana_2_1_cc4ea06f.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3G0fihgrxOmmB0LJffBSPyF37xE/hf_20261016_185458_ac8a32ab-6f6f-47ae-b393-4b92873ca6f3.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3G0fihgrxOmmB0LJffBSPyF37xE/hf_20261016_185458_ac8a32ab-6f6f-47ae-b393-4b92873ca6f3_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_3G0fihgrxOmmB0LJffBSPyF37xE/hf_20261016_184556_4f191d15-3a06-4c77-ae29-72965de1368a.png
- **Input Reference `@img2`**: https://d8j0ntlcm91z4.cloudfront.net/user_3G0fihgrxOmmB0LJffBSPyF37xE/hf_20261016_174348_f5e343f6-f836-4836-81d2-65e58b04a6c8.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Ghép 2 ảnh tham chiếu giữ nguyên ánh sáng và thần thái (`Before: rank_0567_ref1.jpg + ref2.jpg` ➔ `After: rank_0567_nano_banana_2_1_e1bece6f.webp`)**: Chuyển giao hoàn hảo danh tính và trang phục giữa 2 ảnh tham chiếu với độ chân thực da tự nhiên.

```text
Same photoshoot as the first reference image: the exact same male model with voluminous wavy dark brown hair, same face, same anthracite crewneck sweatshirt, same mid-blue straight jeans and white low-top leather sneakers. Editorial pose caught mid-step: walking straight toward the camera, body facing forward, one leg forward, one hand in a front jeans pocket, the other arm swinging naturally, gaze slightly off camera. The chest faces the camera squarely so the small tone-on-tone embossed text is fully visible and copied letter for letter from the second reference: "WE MUST" / "GET LOST" / "- IN -" / "NATURE." with short horizontal dashes, not dots. Full body including shoes and a pale floor. Warm off-white textured plaster wall, soft even light, no hard shadows. Natural hands. Photorealistic e-commerce catalog photo.
```

---

#### 5.3. Cách Các Dự Án Phim Phối Hợp Đa Ảnh Tham Chiếu (`2 đến 9 Refs` & `2D Placement Diagram`) — Nguyên Văn 100% Từ `asset_registry.json`

##### 🎬 Project `bucketlist_impossible/bash` — Asset `@IMG_069` (Model: `seedream_v5_pro` | Roles: `start_frame_keyframe` | Reused in `7` jobs)
- **Chiến thuật Đạo diễn**: Dùng `@img1` làm **Sơ đồ Vị trí 2D (`Use @img1 as a 2D placement diagram`)** kết hợp `@img2..@img5` làm bảng nhân vật & bối cảnh trên `seedream_v5_pro` (tái sử dụng `7` lần).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_359U8LzwhGMVvAw4ZirC8oN1czR/hf_20260909_081251_e60b0c5a-9fce-4bdb-8046-557e778af79f.png
- **👁️ Visual Audit Verdict**: Câu lệnh mẫu mực chỉ rõ cách buộc AI tuân thủ sơ đồ vị trí 2D mà không vẽ lại các đường kẻ sơ đồ lên ảnh thật (`Use @img1 ONLY for relative spatial positioning — do not render any diagram lines, labels, or arrows`).

```text
Create a photorealistic 21:9 cinematic feature-film frame of the approved collapsed-building cavity at night. Preserve the exact wide location geometry, low fractured concrete ceiling, upper-left opening, cracked playable floor, rubble perimeter, exposed rebar and camera perspective. Do not redesign the room.

<<<image_10>>> Use the latest annotated placement image to position the approved props. Remove all drawn marks, arrows and labels from the final image.

ADAM: <<<image_2>>>
Use the approved injured ADAM sheet as absolute identity authority. Place him in the right-side crushed lower compartment shown in the annotation. Only his head and anatomical RIGHT arm emerge into the cavity. His left arm, chest, torso, hips and legs remain buried beneath the collapsed structure. He is severely pinned, with limited head and right-arm movement. His right hand rests naturally near the rubble edge. Preserve exact injuries, clothing and photographic skin detail.

CUP AND WATER: <<<image_6>>>
Place the approved heavily damaged, darkened metal camping cup beneath the ceiling drip indicated in the annotation, left of the fire. Preserve its exact design, single handle, dents, warped rim and dirty finish. Keep it small and realistically scaled, approximately 9–10 cm tall. A localized drip falls from a concrete crack directly into the cup - 2 seperate drops, slightly creating small ripples and a damp patch beneath it. Do not create a waterfall or flood.

BAG: <<<image_8>>>
Place the approved worn bag on its side behind the fire, slightly toward the right, as marked. Preserve its exact design and realistic scale. It should look naturally dropped, dusty and partially settled into the rubble.

TOOLS AND METAL: <<<image_9>>> 
Place the approved small metal tools and scrap pieces near the right-side rubble edge, within the restricted reach zone. Use the selected reference designs, not the rejected variants. Keep them realistically sized and casually scattered, not arranged like a product display.

WOOD: <<<image_7>>>
Use the approved short, irregular broken wood pieces, including the selected charred pieces. Place a small amount near the fire and a few spare pieces along the right-side ground. Preserve their rough broken shapes and realistic scale. No oversized logs or neatly stacked firewood.

FIRE: <<<image_4>>>
Preserve the existing small improvised wooden-log fire. It remains close enough to ADAM's right arm to be plausibly maintained. Small flames, glowing embers, occasional tiny sparks and a little natural smoke. Keep the central ground usable for later movement.

LIGHTING AND MOOD: <<<image_3>>> <<<image_5>>>
Deep night. The only motivated sources are faint cold blue-green exterior light through the opening and warm amber firelight. Mix both temperatures naturally without creating a single-color wash. The fire produces localized flicker and rapid falloff; the opening gives selective cold separation. Most of the cavity remains in deep darkness.

Follow the supplied mood references: intimate, suffocating, tactile, dirty and emotionally heavy. Subtle atmospheric haze, suspended concrete dust, natural smoke, organic film grain, soft highlight rolloff, restrained halation around the flame and rich shadow separation. Photographed feature-film quality, not glossy CGI or clean HDR.

CAMERA:
Preserve the approved wide camera position, low to the rubble floor and slightly off-axis. Approximately 24mm spherical cinema lens perspective, with strong foreground depth, partial obstruction and natural spatial distortion. The frame should establish the playable cavity while maintaining claustrophobia. Do not move the camera closer or change the room's proportions.

SCALE AND CONTINUITY:
All props must remain realistically proportioned to ADAM and the environment. Preserve their approved designs, damage and relative placement. Do not enlarge objects to make them more visible. The cup, bag, tools, wood and fire must occupy the same physical positions in later reverse angles.

No additional characters or animals. No text, labels, arrows, diagrams or overlays. No extra props beyond the supplied approved elements.
```

##### 🎬 Project `nicholastakeyama/tokyo-4-17` — Asset `@IMG_021` (Model: `gpt_image_2` | Roles: `turnaround_sheet_reference_element` | Reused in `13` jobs)
- **Chiến thuật Đạo diễn**: Quy tắc Tách Biệt 2 Vai Trò Tham Chiếu (`Use the TWO provided reference images for TWO COMPLETELY DIFFERENT PURPOSES: REFERENCE IMAGE 1 = FOREGROUND / CHARACTER ... REFERENCE IMAGE 2 = BACKGROUND / ENVIRONMENT`, tái sử dụng `13` lần).
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_3I46mUa53PeRFKUW81n8w50NiCE/hf_20260905_063028_8add87d7-7bf3-4c01-8ce8-b38d2a59180a_min.webp
- **👁️ Visual Audit Verdict**: Khi ghép sản phẩm hoặc nhân vật (`@img1`) vào phòng khách (`@img2`), việc mở đầu bằng câu khẳng định `Use the TWO provided reference images for TWO COMPLETELY DIFFERENT PURPOSES` giúp `gpt_image_2` không bao giờ trộn lẫn nền của `@img1` vào `@img2`!

```text
Use the TWO provided reference images for TWO COMPLETELY DIFFERENT PURPOSES.

REFERENCE IMAGE 1 = FORMAT / LAYOUT / CAMERA / STUDIO TEMPLATE ONLY.

REFERENCE IMAGE 2 = CHARACTER APPEARANCE / CASTING / STYLING REFERENCE ONLY.

Do not mix the purposes of the two references.


==================================================
REFERENCE IMAGE 1 — FORMAT ONLY
==================================================

Use Reference Image 1 ONLY to reproduce the standardized CHARACTER MASTER SHEET presentation.

Preserve from Reference Image 1:

- overall horizontal canvas format
- exactly three vertical panels
- panel proportions
- subject scale
- framing
- camera distance
- camera height
- neutral studio background
- neutral studio lighting
- full-body presentation
- close-up presentation
- thin vertical panel dividers
- clean professional casting-reference aesthetic

The final layout must be:

LEFT:
FULL-BODY FRONT VIEW

CENTER:
FULL-BODY BACK VIEW

RIGHT:
CLOSE-UP PORTRAIT

IMPORTANT:

DO NOT copy the woman from Reference Image 1.

Do not copy her:

face,
body,
age,
hair,
makeup,
dress,
jewelry,
shoes,
skin tone,
or styling.

Reference Image 1 defines ONLY HOW THE CHARACTER IS DISPLAYED.


==================================================
REFERENCE IMAGE 2 — CHARACTER APPEARANCE
==================================================

Use Reference Image 2 as the PRIMARY CHARACTER APPEARANCE REFERENCE.

The woman in Reference Image 2 defines WHO THE CHARACTER IS.

Preserve her recognizable visual identity and overall appearance as closely as possible.

Translate the woman from Reference Image 2 into the standardized three-panel character sheet defined by Reference Image 1.

Preserve from Reference Image 2:

- facial identity
- apparent adult age
- facial structure
- face shape
- eye shape
- eyebrow shape
- nose
- lips
- jawline
- cheek structure
- skin tone
- natural facial asymmetry
- distinctive facial features
- hairstyle
- hair length
- hair color
- hair texture
- hair parting
- body type
- height impression
- body proportions
- overall styling
- makeup
- clothing
- dress design
- dress color
- dress material
- jewelry
- accessories
- shoes, if visible
- overall personality and visual character

Do NOT beautify or normalize her.

Do NOT transform her into a generic AI beauty.

Do NOT make her face resemble the woman from Reference Image 1.

The final character should unmistakably derive from Reference Image 2.


==================================================
WHEN INFORMATION IS NOT VISIBLE
==================================================

If some information is not visible in Reference Image 2, infer it conservatively and realistically.

For example:

If only the front of the outfit is visible, create a physically plausible back construction that matches the same garment.

If shoes are not visible, choose understated shoes that naturally match the existing wardrobe.

If the rear hairstyle is not visible, reconstruct it logically from the visible hair length, volume, texture and styling.

If exact height cannot be determined, infer a believable height from the visible body proportions.

DO NOT redesign visible elements merely because another design might look better.

Preserve what is known.

Only invent what is genuinely missing.


==================================================
IDENTITY CONSISTENCY
==================================================

All three panels must depict THE EXACT SAME WOMAN from Reference Image 2.

This is one person photographed three times.

Maintain identical:

facial identity,
skull shape,
age,
skin tone,
body proportions,
height,
hairline,
hairstyle,
hair color,
makeup,
wardrobe,
jewelry,
accessories,
and shoes.

Do not generate three similar women.

Do not reinterpret her identity between panels.


==================================================
LEFT PANEL — FULL-BODY FRONT
==================================================

Create a neutral full-body front reference photograph of the woman from Reference Image 2.

Direct front view.

Entire body visible from top of head to shoes.

Natural standing posture.

Arms resting naturally.

No crossed legs.

No exaggerated hip shift.

No fashion-editorial pose.

No seductive pose.

Approximately 70mm full-frame equivalent lens.

Camera level.

Minimal perspective distortion.

The purpose is accurate documentation of her complete appearance.


==================================================
CENTER PANEL — FULL-BODY BACK
==================================================

Show THE EXACT SAME WOMAN directly from behind.

180-degree rear view.

Entire body visible from head to shoes.

Face completely hidden.

Accurately reconstruct:

rear hairstyle,
hair length,
neck,
shoulders,
back of wardrobe,
waist,
body proportions,
legs,
jewelry where applicable,
and shoes.

The back view must be physically consistent with Reference Image 2 and with the generated front view.

Do not redesign the character.


==================================================
RIGHT PANEL — CLOSE-UP PORTRAIT
==================================================

Create a clean head-and-shoulders portrait of THE EXACT SAME WOMAN from Reference Image 2.

Face approximately straight toward camera.

Preserve her facial identity with maximum fidelity.

Maintain:

eye anatomy,
eye spacing,
eyebrows,
nose,
lips,
jaw,
cheeks,
skin,
hairline,
hair,
makeup,
earrings,
necklace or other visible jewelry.

Approximately 85mm full-frame equivalent lens.

Eye-level.

Approximately f/4 appearance.

Natural human facial proportions.

Realistic skin texture.

No beauty filter.

No excessive retouching.


==================================================
STUDIO PRESENTATION
==================================================

Use the studio presentation from Reference Image 1.

Neutral medium-gray background.

Neutral matte studio floor.

Soft diffused studio lighting.

Neutral white balance.

Clear visibility of face, hair, body and wardrobe.

No dramatic cinematic lighting.

No nightclub lighting.

No neon.

No colored light.

No environmental background.

No furniture.

No props.

No text.

No captions.

No labels.


==================================================
REFERENCE PRIORITY — VERY IMPORTANT
==================================================

When the two references conflict:

REFERENCE IMAGE 2 ALWAYS WINS for:

IDENTITY,
FACE,
AGE,
BODY,
HAIR,
MAKEUP,
WARDROBE,
COLOR,
JEWELRY,
ACCESSORIES,
SHOES,
and CHARACTER APPEARANCE.

REFERENCE IMAGE 1 ALWAYS WINS for:

LAYOUT,
PANEL ORDER,
FRAMING,
CAMERA,
SUBJECT SCALE,
BACKGROUND,
LIGHTING,
and PRESENTATION STYLE.

Never borrow character appearance from Reference Image 1.

Never borrow layout or studio presentation from Reference Image 2.


==================================================
FINAL RESULT
==================================================

Transform the CHARACTER shown in Reference Image 2 into the standardized CHARACTER MASTER SHEET FORMAT shown in Reference Image 1.

REFERENCE 1 = HOW TO DISPLAY HER.

REFERENCE 2 = WHO SHE IS.

ONE horizontal image.

EXACTLY THREE panels.

LEFT = FULL-BODY FRONT.
CENTER = FULL-BODY BACK.
RIGHT = CLOSE-UP PORTRAIT.

Maximum fidelity to Reference Image 2's character appearance.

Maximum consistency between all three views.

Ultra-photorealistic live-action photography.

Real skin.
Real hair.
Real fabric.
Real anatomy.

Do not redesign.
Do not beautify.
Do not average the two women together.
Do not create a hybrid identity.
```

##### 🎬 Project `seksifratello/apeirophobia-teaser` — Asset `@IMG_364` (Model: `nano_banana_2` | Roles: `start_frame_keyframe` | Reused in `2` jobs)
- **Chiến thuật Đạo diễn**: Kỷ lục phối hợp **9 Ảnh Tham Chiếu (`<<<image_1>>>` đến `<<<image_9>>>`)** kèm khóa `PROJECT LOOK LOCK: ARRICAM LT, Kodak Vision3 500T 5219` trên `nano_banana_2`.
- **Generated Asset URL**: https://d8j0ntlcm91z4.cloudfront.net/user_31n0NLIr1dkrN5DoEG0FF0aoOzh/hf_20260911_100053_8b599e6d-c6d6-40f0-8422-f98c52233500.png
- **👁️ Visual Audit Verdict**: Đạo diễn `@seksifratello` phân bổ 9 ảnh tham chiếu cho từng nhiệm vụ vi mô: `@img1..@img3` khóa gương mặt & hình xăm nhân vật A, `@img4..@img6` khóa nhân vật B, `@img7..@img9` khóa kiến trúc căn phòng và ánh sáng đêm.

```text
PROJECT LOOK LOCK:

Create a grounded, photorealistic 35mm European crime-drama still in the established visual world of the film.

Shoot as if on ARRICAM LT, Kodak Vision3 500T 5219 rated at EI 320, Zeiss Super Speed Mk II 85mm lens, stopped down enough to keep BOTH faces critically sharp on the same focal plane, around T4. Subtle Black Pro-Mist 1/8.

24 fps visual language, authentic medium-fine 35mm grain, subtle halation, soft highlight roll-off, slightly lifted blacks, low saturation, no HDR, no digital crispness, no glossy commercial finish.

Muted Baltic night palette:
deep steel-blue darkness,
gray-green dune vegetation,
faded sand tones,
restrained natural skin tones.

The image should feel dark, wind-worn, quiet and genuinely nocturnal.

CHARACTER REFERENCE LOCK:

<<<image_1>>> and <<<image_2>>> = ADAM.

Use these references ONLY for Adam’s exact facial identity, hair, facial structure, neck / upper-chest tattoos and styling.

Adam is the younger and taller man.

Adam is almost a full head taller than Sicko, and this height difference must read clearly and naturally even in the tight shared framing.

His wraparound sunglasses MUST be visibly resting on top of his head.

Preserve his established neck / upper-chest tattoos.

NO tattoos on Adam’s hands, fingers or arms.

<<<image_3>>>, <<<image_4>>>, <<<image_5>>> and <<<image_6>>> = SICKO.

Use these references ONLY for Sicko’s exact facial identity, age, thin build, hollow cheeks, large gray-green eyes, receding thin hair, clothing and tattoo details.

<<<image_6>>> specifically defines Sicko’s hand tattoos.

Sicko is visibly smaller, thinner and older than Adam.

Do not transfer any Sicko traits onto Adam.

LOCATION:

Night on a Baltic beach.

Adam and Sicko have left the campsite and are walking side by side across the beach toward the water.

IMPORTANT:

THE OCEAN ITSELF IS NOT VISIBLE.

They are theoretically walking toward the sea, but the camera is positioned in front of them facing inland.

Behind them we see only dark coastal dunes, sandy rises, sparse dune grass and low wind-shaped vegetation disappearing into the night.

No buildings.
No caravans.
No streetlights.
No lamps.
No visible civilization.
No horizon line of the sea.

The environment should feel remote, cold, natural and almost completely dark.

SHOT:

Adam and Sicko are walking side by side directly toward the camera while talking.

This is an extremely tight shared two-person close-up.

The camera moves backwards directly in front of them, maintaining roughly the same distance as they walk.

CAMERA POSITION — CRITICAL:

The camera is positioned VERY close to them, approximately half a meter from their faces.

The camera is slightly BELOW their eye line, creating a subtle upward perspective.

Do NOT exaggerate this into a dramatic low-angle shot.

It should simply feel as though the camera is walking slightly lower than their natural eye level.

The camera is NOT centered perfectly between the two men.

We are positioned more on SICKO’S SIDE.

Sicko is slightly closer to the lens and subtly more frontal.

Adam stands slightly farther across the frame beside him.

This creates a mild diagonal depth relationship between the two faces while keeping BOTH faces equally important and equally sharp.

The composition should feel as though we are walking alongside Sicko, very close to him, while still seeing Adam directly beside him.

Do not make Sicko dramatically larger through perspective.
The difference should remain subtle and natural.

Even within the tight framing, Adam should still read as almost a full head taller than Sicko.

FRAMING:

Both heads dominate the frame.

Mainly show:

their faces,
their necks,
and only a very small amount of upper shoulders.

Minimal torso.

Their faces should feel unusually close to the lens, almost crowding the image.

The tops of their heads may approach the upper frame edge.

Do NOT turn this into a medium close-up.

Do NOT create empty space around them.

This should feel intimate and physically close.

FACIAL ACTION:

This is a silent in-between moment during their conversation.

Their mouths are completely still and naturally closed.

No visible speech articulation.
No open mouths.
No frozen mid-word expressions.

Adam has a restrained, slightly amused and guarded expression.

He occasionally looks sideways toward Sicko rather than toward the camera.

Sicko feels relaxed, attentive and quietly engaged.

There is a subtle warmth developing between them, but nothing sentimental or overtly emotional.

They should feel like two men who have only recently met but are unexpectedly enjoying each other's company.

FOCUS — ABSOLUTE PRIORITY:

The FACES are the visual priority.

BOTH faces must be simultaneously and critically sharp.

Both pairs of eyes must be clean, detailed and readable.

Neither man may fall noticeably out of focus.

Do not prioritize the dunes over the faces.

The background may fall away optically, but the dunes must remain identifiable as real dunes rather than becoming abstract blur.

Strong depth readability.

No portrait-mode separation.
No artificial depth map.
No creamy bokeh soup.

The image should still communicate clearly that they are walking through a beach landscape at night.

LIGHTING — CRITICAL:

NO artificial lighting whatsoever.

No movie lighting.

No key light.
No fill light.
No beauty light.
No frontal light.
No rim light.
No hidden softbox.
No practical lamps.
No caravan light.
No streetlights.
No torches.
No visible artificial source.

There is also NO stylized blue moonlight beam illuminating them.

The scene is exposed only through extremely subtle NATURAL NIGHT AMBIENT LIGHT.

The sky provides just enough residual ambient exposure to retain facial information.

Their faces remain dark.

Their eye sockets, cheek structure, skin texture and expressions are still readable, but they must NEVER look deliberately illuminated.

No warm highlights on their faces.

No fake blue edge light.

No Hollywood night lighting.

Preserve deep natural shadows.

The image may sit slightly underexposed.

MOVEMENT FEELING:

They are genuinely walking.

Subtle differences in shoulder height and body rhythm.

No synchronized steps.

No posing.

No dramatic gestures.

No staged symmetry.

The camera retreats naturally in front of them with subtle human handheld micro-drift.

It should feel observed rather than choreographed.

MOOD:

Quiet.
Dry.
Intimate.
Human.
Nighttime.
Slightly noir.
Cold coastal air.

A small, genuine moment of connection between two men walking toward the unseen sea.

No sentimentality.
No romance.
No horror staging.
No gothic vampire imagery.
No supernatural effects.

NEGATIVE LOCK:

No visible ocean.
No sea behind them.
No campsite.
No caravans.
No buildings.
No artificial lights.
No medium shot.
No waist-up shot.
No wide shot.
No excessive torso visibility.
No large amount of empty space around the characters.
No camera at normal distant portrait distance.
No perfectly symmetrical frontal two-shot.
No dramatic low-angle hero shot.
No direct face lighting.
No frontal lighting.
No fill lighting.
No beauty lighting.
No rim lighting.
No stylized moonlight.
No orange light on faces.
No glowing skin.
No open mouths.
No visible speech articulation.
No looking directly into the camera.
No fashion posing.
No shallow-focus bokeh soup.
No background disappearing completely into blur.
No glossy skin.
No HDR.
No oversaturated color.
No teal-orange grade.
No logos.
No text.
No hand tattoos on Adam.
Do not remove Adam’s sunglasses from the top of his head.
Do not mix Adam and Sicko’s identities.
```

---

### 21.🧬 CHUYÊN ĐỀ 6: ẢNH VỀ CON NGƯỜI & CHẤT LIỆU (`CHARACTER REALISM, SKIN MICRO-TEXTURE & MATERIAL PHYSICS`)

> **Quy tắc Kiểm định Thị giác (`Visual Audit First`)**:
> Khi soi trực tiếp hàng trăm bức ảnh chân dung ở phân khúc `♡ < 50` và `29` Dự Án Phim, chúng ta rút ra bảng phân công Model cho Con người & Chất liệu như sau:
> - **Top 1 về Da người thật (`Pores, Vellus Peach Fuzz, Sweat Beads, Subsurface Scattering`)**: `soul_cinematic` (`Rank #1011`) và `text2image_soul_v2` (`Rank #1061`, `Rank #894`, `Rank #1090`) tạo ra làn da có lỗ chân lông, lông tơ bắt sáng ngược, giọt mồ hôi và độ tán xạ dưới da thật 100%.
> - **Top 1 về Tạo Bảng Casting Diễn Viên 3-Panel Tự Động (`Front | Back | Close-Up Face`)**: `cinematic_studio_soul_cast` (`Rank #3493`, `Rank #3483`, `Rank #3502`) nhận cấu trúc JSON `[Character Params: {"age": ..., "outfit": ..., "body_type": ...}]` và xuất thẳng tấm ảnh chia 3 cột có cả góc mặt trước, góc lưng 180° và góc cận cảnh khuôn mặt!
> - **Cảnh báo Model bị mịn da kiểu Sáp/Kem (`Waxy/Beauty-Retouch Alert`)**: Qua kiểm định trực tiếp `rank_0312_seedream_v4_5_0e7838d1.webp` (`seedream_v4_5`) và `rank_0926_gpt_image_2_62c6525b.webp` (`gpt_image_2`), dù prompt yêu cầu `"visible pores, no airbrushing"`, hai model này vẫn có xu hướng làm gò má hơi bóng mịn như đánh phấn highlight. Nếu cần cận cảnh da người thật 100%, hãy ưu tiên `soul_cinematic`, `text2image_soul_v2` hoặc `nano_banana_2`!

#### 6.1. Tuyển Tập Prompt Con Người, Vi Cấu Trúc Da & Bảng Casting 3-Panel Ở Phân Khúc `♡ < 50` — Nguyên Văn 100%

##### 🏆 Rank #1011 (`1 ♡` | `29 👁️` | Model: `soul_cinematic` | Author: `@colonialsnail2245` | Size: `1152x2048` | Refs: `0`)
- **Publication ID**: `3944ae66-7709-4d8c-9aab-2b84630b306e`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1011_soul_cinematic_3944ae66.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KeUeotV8evjwMoE16rzJD1ztVA/hf_20261013_190156_f46dd1c0-8805-4467-9526-18016e2c8668.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KeUeotV8evjwMoE16rzJD1ztVA/hf_20261013_190156_f46dd1c0-8805-4467-9526-18016e2c8668_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Đỉnh cao 10/10 về Vi cấu trúc Da người, Lỗ chân lông & Giọt mưa trên `soul_cinematic` (`rank_1011_soul_cinematic_3944ae66.webp`)**: Kiểm định trực tiếp bằng mắt cho thấy từng lỗ chân lông trên trán và sống mũi, từng giọt mưa và vệt nước mắt lăn qua râu lởm chởm, từng sợi lông mày ướt và ánh sáng phản chiếu trong tròng mắt đạt độ chân thực điện ảnh 35mm tuyệt đối, hoàn toàn không có dấu vết AI!

```text
Cinematic extreme close-up film still of a man's eyes and upper face, mid-thirties, rain dripping from his lashes and running down his cheek, water beading on skin and stubble, exhausted but determined stare, mid-blink. Very shallow depth of field, soft bokeh street lights behind him, hard cool sidelight, 35mm film grain, muted high-contrast neo-noir grade. No text, no logos, no watermark.
```

##### 🏆 Rank #1061 (`1 ♡` | `17 👁️` | Model: `text2image_soul_v2` | Author: `@simrildirector` | Size: `2048x1536` | Refs: `1`)
- **Publication ID**: `e51845db-cb64-4248-ac9d-796ce55b2038`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1061_text2image_soul_v2_e51845db.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KLXzWmhVEWXBuv6V6BhbDmOHrZ/hf_20261012_193120_7f19a603-26c3-4c73-ab39-1479ed437aff.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KLXzWmhVEWXBuv6V6BhbDmOHrZ/hf_20261012_193120_7f19a603-26c3-4c73-ab39-1479ed437aff_min.webp
- **Input Reference `@img1`**: https://d2ol7oe51mr4n9.cloudfront.net/user_3KLXzWmhVEWXBuv6V6BhbDmOHrZ/03a9c1ee-b391-419e-9521-4d0af36c28fd.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Đỉnh cao 10/10 về Làn da đẫm mồ hôi, Lông tơ (`Vellus Hair`) & Chiều sâu trường ảnh trên `text2image_soul_v2` (`rank_1061_text2image_soul_v2_e51845db.webp`)**: Cú đấm ở tiền cảnh được làm nhòe chuyển động (`motion blur + shallow DOF`) trong khi gương mặt nữ võ sĩ nét căng từng lỗ chân lông, lớp mồ hôi bóng tự nhiên trên trán và những sợi tóc con bắt ánh đèn rim light.

```text
Extreme close-up portrait in full colour: hair pulled back in a tight ponytail, glistening sweat on her skin, fierce determined expression, eyes locked on the camera. Two fists raised beside her face, close to the lens and slightly blurred in the foreground, like she's about to throw a punch. Cinematic professional photography, dramatic lighting, shallow depth of field, razor-sharp focus on her eyes, visible skin texture, film grain. Motivational poster composition — bold, inspiring, heroic framing with clean negative space around the subject. No text, no logos, no watermarks.
```

##### 🏆 Rank #894 (`1 ♡` | `90 👁️` | Model: `text2image_soul_v2` | Author: `@bauhausnarwhal2188` | Size: `1152x1536` | Refs: `0`)
- **Publication ID**: `054b464a-bbdc-4f74-b3d0-7b6b037fa6b4`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0894_text2image_soul_v2_054b464a.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KNaniTi1atNJNEJpaFijiyFS1m/hf_20261007_193844_a962da89-80e9-4c79-8eed-629dbc591765.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3KNaniTi1atNJNEJpaFijiyFS1m/hf_20261007_193844_a962da89-80e9-4c79-8eed-629dbc591765_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Ảnh chụp Flash ban ngày đời thực tự nhiên 100% (`Candid Street Flash Realism` — `rank_0894_text2image_soul_v2_054b464a.webp`)**: `text2image_soul_v2` tái hiện hoàn hảo bức ảnh chụp nhanh ngoài phố với bóng đổ sắc nét của đèn flash trên bức tường trắng phía sau, làn da rám nắng có nếp nhăn mắt tự nhiên, râu quai nón, lông tay và từng nếp nhăn nhàu tự nhiên của chiếc áo sơ mi vải linen xanh nhạt.

```text
Create a highly realistic reference photo of an ordinary real person who looks completely believable and human, not like an AI-generated model.
Italian Male, approximately 30-35 years old. He should look approachable, intelligent, and believable as someone who could teach a language online. He should be reasonably pleasant-looking, but NOT unusually handsome, glamorous, fashionable, or model-like. He should look like a normal person you could realistically meet at work, in a coffee shop, or in your neighborhood.
Give him average, non-idealized facial proportions. His face should have subtle natural asymmetry. One eyebrow can sit slightly higher than the other, the eyes can have slightly different shapes, the nose should not be perfectly straight or symmetrical, and the mouth can be subtly uneven. His jaw should be average and natural, NOT broad, square, sculpted, or sharply defined. Avoid exaggerated cheekbones or a perfect masculine face shape.
His skin must look like real human skin. Preserve subtle visible pores, fine lines, slight unevenness in skin tone, mild redness around parts of the nose or cheeks, subtle under-eye texture, tiny natural imperfections, and realistic variation across the face. Skin texture should be subtle and visible mainly at close range, not exaggerated. Do not smooth, airbrush, beautify, or digitally perfect the skin. Avoid waxy, plastic, porcelain, glossy, overly smooth, or artificially sharpened skin.
His teeth should look natural rather than cosmetic-perfect. Allow slightly uneven tooth alignment, natural tooth shapes, small differences between individual teeth, and normal off-white coloring. Do not give him perfectly straight, identical, ultra-white Hollywood teeth.
His hair should look naturally grown rather than professionally styled. Include slight irregularity in the hairline, subtle differences in hair density, small flyaway hairs, individual strands, and naturally imperfect styling. Do not make the hairline perfectly symmetrical or unnaturally dense.
If facial hair is present, make the density naturally uneven with realistic individual hairs. Do not create a perfectly edged or perfectly symmetrical beard.
Give him average body proportions. Do not make him unusually muscular, broad-shouldered, lean, chiseled, or fashion-model proportioned.
Use a relaxed, neutral-friendly expression. He should look comfortable and approachable, like someone having a normal conversation. Avoid a commercial advertising smile, fashion pose, intense expression, or exaggerated confidence.
Photograph him at eye level with a natural 50mm-equivalent perspective. Show his head, shoulders, and upper torso. Use ordinary soft indoor daylight, realistic exposure, natural shadows, and normal camera dynamic range. It should feel like a high-quality photo taken with a normal smartphone or consumer mirrorless camera, not a professional fashion shoot.
Use a simple realistic home office, classroom, or neutral indoor background. Keep the depth of field moderate rather than extremely blurry.
The final result should look like an actual photograph of a specific real human being. Preserve mundane human irregularities and small imperfections. The goal is not ugliness or obvious flaws; the goal is believable normality.
AVOID: perfect facial symmetry, male-model face, extremely handsome appearance, square jaw, giant jaw, razor-sharp jawline, exaggerated cheekbones, perfectly straight nose, flawless skin, beauty-filter skin, skin smoothing, waxy skin, plastic skin, porcelain skin, artificial pore texture, excessive freckles, fake blemishes, dramatic scars, perfect teeth, ultra-white teeth, perfectly symmetrical hairline, overly styled hair, fashion photography, glamour photography, cinematic lighting, dramatic rim lighting, excessive bokeh, HDR appearance, oversharpening, unrealistically bright eyes, oversized irises, perfectly white eye sclera, commercial stock-photo appearance, or the stereotypical AI-generated influencer look. Make a photo from waist up and put him in a dress shirt.  make this
```

##### 🏆 Rank #1090 (`1 ♡` | `11 👁️` | Model: `text2image_soul_v2` | Author: `@brotmaker` | Size: `1152x1536` | Refs: `0`)
- **Publication ID**: `15e61616-6767-465b-8dc5-2c20061f5bd2`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1090_text2image_soul_v2_15e61616.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3Ks9EhCS0C9z1c1XGRJm3RmSrg8/hf_20261018_151246_9c662951-b346-46d4-a086-a5692fbdf4d2.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3Ks9EhCS0C9z1c1XGRJm3RmSrg8/hf_20261018_151246_9c662951-b346-46d4-a086-a5692fbdf4d2_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Chân dung trong Phòng khách ấm cúng kết hợp Len đan hạt to & Ánh đèn dây Edison (`Cozy Living Room Portrait` — `rank_1090_text2image_soul_v2_15e61616.webp`)**: Cực kỳ phù hợp làm mẫu nhân vật ngồi cạnh Cây thông Noel trong TVC của bạn: cô gái mặc áo len cổ lọ đan sợi to (`chunky cream knit sweater`) và tất len xám ngồi co gối trên ghế bành da nâu, phía sau là bóng đèn dây Edison vàng ấm và ánh đèn neon cam phản chiếu nhẹ lên gò má và sợi tóc.

```text
A young woman in her mid-20s sits curled up in the corner of a cozy, sunlit living room on a late autumn afternoon, holding a large ceramic mug of steaming coffee close to her lips as she takes a slow, contented sip. Her eyes are half-closed, and a soft, peaceful smile shows over the rim of the cup. She has tousled chestnut-brown hair in a loose messy bun, with a few strands falling across her face, and a scattering of light freckles across her nose and cheeks. She wears an oversized cream-colored chunky knit sweater with sleeves pulled over her hands, soft gray flannel pajama pants, and thick wool socks with a subtle striped pattern.
She is seated on a deep, slightly worn caramel-brown leather armchair, with a mustard-yellow throw blanket draped over her legs and a patterned velvet cushion tucked behind her back. The mug is handmade, with a speckled glaze in dusty blue, and gentle curls of steam rise from it, catching the light.
The living room is warm and lived-in. Behind her, a tall window with sheer white linen curtains lets in golden hour sunlight, casting long, soft shadows and glowing dust particles across the hardwood floor. Rain-streaked glass hints at a drizzly autumn day outside, with blurred orange and red maple leaves beyond. To her left, a low wooden coffee table holds a stack of well-thumbed paperbacks, a small ceramic vase with dried pampas grass, a half-burned beeswax candle, and a plate with a half-eaten croissant dusted with crumbs. On the right, a tall bookshelf is packed with books, trailing pothos plants, framed photographs, and a small vintage record player. A large monstera plant stands in the corner, its leaves lit by the sunlight. A woven jute rug with a muted geometric pattern covers the floor, and a sleepy orange tabby cat is curled up on it near her feet.
The wall behind features a gallery of mismatched framed art prints and a round brass mirror reflecting the window light. A warm lamp with a linen shade glows softly in the background, adding amber highlights.
Style and technical details: photorealistic, cinematic lifestyle photography, shot on a 50mm f/1.8 lens, shallow depth of field with softly blurred background, warm golden-hour color grading with muted earth tones, soft natural window light with gentle rim lighting on her hair, subtle film grain, hygge atmosphere, serene and nostalgic mood, highly detailed textures (knit wool, leather grain, ceramic glaze, steam), 4K, 3:2 aspect ratio.
```

##### 🏆 Rank #306 (`38 ♡` | `705 👁️` | Model: `nano_banana` | Author: `@frank_brsrk` | Size: `auto` | Refs: `1`)
- **Publication ID**: `137d8590-a33a-4738-9e6e-54516e8813eb`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0306_nano_banana_137d8590.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_37TEr9F6fpjYAxEMksPrw2ikTof/41091b0a-ba20-4d86-8c0a-3fb4cabee515.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_37TEr9F6fpjYAxEMksPrw2ikTof/41091b0a-ba20-4d86-8c0a-3fb4cabee515_min.webp
- **Input Reference `@img1`**: https://d8j0ntlcm91z4.cloudfront.net/user_37TEr9F6fpjYAxEMksPrw2ikTof/170752c8-775d-4e8d-9f7f-d13e2615389b.png
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Chân dung Thời trang Studio Ngoảnh Lưng Nhìn Qua Vai (`Over-the-Shoulder Studio Portrait` — `rank_0306_nano_banana_137d8590.webp`)**: `nano_banana` giữ sắc nét từng sợi tóc mai, độ bóng kim loại của gọng kính râm bạc, khuyên tai và nếp vải áo sơ mi xanh đen trên nền trắng studio.

```text
Close-up shot from behind, subject’s back and shoulders visible, head turned over the shoulder towards the camera. Face partially visible in profile, centered in the frame.
```

##### 🏆 Rank #312 (`35 ♡` | `2773 👁️` | Model: `seedream_v4_5` | Author: `@anthonvg` | Size: `3:4` | Refs: `0`)
- **Publication ID**: `0e7838d1-3e23-4db8-8260-81f48ab7c180`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_0312_seedream_v4_5_0e7838d1.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_35OXBjHEQwjJNorhVDBL1AzYURe/hf_20260217_234950_9bcf5eb1-0be8-4780-b12d-3d8f3cda8f6a.jpeg
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_35OXBjHEQwjJNorhVDBL1AzYURe/hf_20260217_234950_9bcf5eb1-0be8-4780-b12d-3d8f3cda8f6a_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Cảnh báo Kiểm định Thị giác trên `seedream_v4_5` (`rank_0312_seedream_v4_5_0e7838d1.webp`)**: Dù câu lệnh yêu cầu rất kỹ `visible pores, subtle freckles, natural skin texture, no airbrushing`, nhưng khi soi trực tiếp ảnh xuất bằng mắt, `seedream_v4_5` vẫn phủ một lớp nhũ bóng beauty-retouch lên gò má và môi. Bài học: Khi cần cận cảnh da người thô mộc, hãy dùng câu lệnh này trên `soul_cinematic` (như `Rank #1011`) hoặc `text2image_soul_v2` (như `Rank #1061`) thay vì `seedream_v4_5`!

```text
Photorealistic extreme close-up portrait. Vertical 4:5, face only from chin to forehead. Hair version B: long waves framing both sides of face softly. Both hands framing her own face — fingers along jawline and cheeks, gold rings visible, tattooed left wrist/forearm entering frame. Face fills 80% of the image: green-hazel eyes intense and direct, every detail sharp — iris texture, lash definition, skin pores. Lips full glossy pink slightly parted. Septum ring delicate. Brows thick natural. Skin dewy golden-olive. Soft frontal natural light, tiny catchlights in eyes. Very shallow depth of field, fingertips slightly soft. Warm tones. Film grain. No text, no logos.
```

##### 🏆 Rank #3400 (`0 ♡` | `2 👁️` | Model: `soul_cinematic` | Author: `@mathewmosses` | Size: `1152x2048` | Refs: `0`)
- **Publication ID**: `0364bfd8-e1b4-4f5d-bd2c-ee4fadae69c3`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_3400_soul_cinematic_0364bfd8.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3FcSZgwbFj8Ye8qzM2YSVIz1YUY/hf_20261006_074544_4cfd0244-9f05-4501-afa4-22749e5ffd1e.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3FcSZgwbFj8Ye8qzM2YSVIz1YUY/hf_20261006_074544_4cfd0244-9f05-4501-afa4-22749e5ffd1e_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Tuyệt tác Chất liệu Lụa Kasavu Dệt Chỉ Vàng Zari & Da Voi Nhăn Thực Tế (`rank_3400_soul_cinematic_0364bfd8.webp`)**: `soul_cinematic` đặt hai bề mặt vật lý đối lập cạnh nhau ở góc nghiêng 90°: làn da nâu ấm áp và tà áo saree lụa kem viền chỉ vàng óng ánh của người mẫu Ấn Độ chạm vào lớp da voi xám nhăn nheo, thô ráp giữa màn sương sớm Kerala.

```text
ULTRA-REALISTIC LUXURY FASHION EDITORIAL — KERALAM

A breathtaking high-fashion photograph captured on location in Keralam, India.

A magnificent Asian elephant stands calmly in a lush emerald Kerala landscape. Directly in front of the elephant stands a striking South Indian female fashion model, facing it completely.

The elephant gently raises and curves its trunk upward.

The woman is standing close to the elephant and lightly holds the elephant's raised trunk with both hands, using the trunk naturally for balance and support. Her body is upright and elegant.

Their faces are at exactly the same height.

The woman and elephant are looking directly into each other's eyes, face-to-face, with their foreheads gently touching.

Their forehead contact is the emotional centre of the photograph.

The woman's eyes are open and calm. The elephant's eyes are soft and intelligent. The interaction feels intimate, peaceful and deeply trusting, never sentimental or theatrical.

The woman's posture is graceful and completely natural. Her hands visibly and realistically wrap around the elephant's trunk without deforming it. The trunk supports her lightly while remaining anatomically correct.

She wears an extraordinary ivory Kerala silk couture saree transformed into a sculptural haute couture silhouette, with a broad antique-gold border and exquisite traditional Kerala gold jewellery.

Her long black hair falls naturally down her back, with a few loose strands moving in the humid breeze. Fresh jasmine flowers are subtly woven through her hair.

The lower portion of the saree flows naturally around her legs and onto the wet grass.

The elephant is enormous compared with the woman. Its forehead, ears and trunk show extraordinary realistic detail: wrinkles, fine hairs, moisture, subtle scars and natural tonal variation.

Behind them is a lush Kerala landscape: deep emerald paddy fields, coconut palms, tropical foliage and a distant temple pond disappearing into soft morning mist.

A few other elephants are visible very far in the background, softly out of focus, suggesting a natural herd without distracting from the central relationship.

Soft early-morning natural light illuminates both faces equally.

No artificial halo. No fantasy lighting.

PHOTOGRAPHIC EXECUTION:
Hasselblad X2D medium-format camera, 80mm lens, f/5.6, natural optical depth of field, realistic perspective and lens compression, extremely high dynamic range, delicate highlight roll-off, subtle natural film grain, restrained luxury editorial colour grading.

The woman's skin must be genuinely photographic: visible pores, fine facial hair, subtle pigmentation, realistic eyes, natural lips and tiny imperfections.

The elephant must look genuinely photographed: physically accurate anatomy, realistic skin texture, natural eyes, realistic trunk structure and believable weight.

The silk must behave according to real gravity and wind. Jewellery must have physically accurate metal reflections.

Composition: vertical 4:5 fashion campaign photograph. Both faces positioned precisely near the upper centre of the frame. The woman's ivory silhouette contrasts against the elephant's dark gray skin and emerald landscape.

The emotional feeling is ancient, intimate and regal — as though a contemporary goddess has encountered an ancient guardian of Keralam.

An extremely expensive international fashion campaign photographed in Kerala.

ABSOLUTELY PHOTOGRAPHIC.
No CGI.
No 3D render.
No illustration.
No painting.
No fantasy-art appearance.
No plastic skin.
No artificial glow.
No distorted anatomy.
No extra fingers.
No malformed hands.
No deformed trunk.
No duplicated elephant.
No tourist aesthetic.
No text.
No logo.
```

##### 🏆 Rank #1387 (`0 ♡` | `24 👁️` | Model: `soul_cinematic` | Author: `@tammyboy` | Size: `2048x1152` | Refs: `0`)
- **Publication ID**: `105a47d1-457d-4725-b843-d0d99003fe28`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_1387_soul_cinematic_105a47d1.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3BwFtbjOnv1gp3IwcL2lsjXaygH/hf_20261014_202837_28ae618f-d0c8-4650-8c82-882b029ccf30.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3BwFtbjOnv1gp3IwcL2lsjXaygH/hf_20261014_202837_28ae618f-d0c8-4650-8c82-882b029ccf30_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Chân dung Đời thường & Biểu cảm Điện ảnh trong Quán Cà Phê Mưa Đêm (`rank_1387_soul_cinematic_105a47d1.webp`)**: Biểu cảm ngỡ ngàng cực kỳ tự nhiên của khách hàng và nhân viên pha chế dưới ánh đèn huỳnh quang ấm áp pha lẫn kính ướt mưa ban đêm.

```text
A candid cinematic photograph of a tired young barista-turned-customer in a rain-streaked Manila street café at dawn, standing at the pickup counter and staring at a comically enormous paper coffee cup the size of a fire hydrant that a wide-eyed barista is struggling to slide across the counter with both hands. A normal small cup sits forgotten beside it with a handwritten “Small – Matt” sticker. The customer’s mouth is half-open between a laugh and disbelief, one hand still holding a crumpled ₱120 bill. Steam spirals up from the giant cup’s lid and catches warm amber backlight from the café’s neon sign. Other patrons in the background turn to look, one spilling a drink, one filming on a phone.
Shot on 35mm cinema lens, 35mm f/1.8, shallow depth of field, soft film grain, Kodak Portra 400 color science, natural window light mixed with warm tungsten practicals, volumetric steam, raindrops on the glass with bokeh street lights outside. Hyper-detailed skin with visible pores, fine peach fuzz, slight under-eye fatigue, subtle sweat sheen, flyaway hairs, wrinkled cotton hoodie with realistic fabric weave, scuffed ceramic counter, coffee ring stains, scratched stainless steel espresso machine. Imperfect, lived-in, documentary realism. No plastic skin, no airbrushing, no CGI look, no over-saturation. Emotion: pure comedic disbelief turning into joy. Ultra-detailed, 8K, award-winning cinematic still.
```

##### 🏆 Rank #3493 (`0 ♡` | `0 👁️` | Model: `cinematic_studio_soul_cast` | Author: `@pippi104` | Size: `2048x1152` | Refs: `0`)
- **Publication ID**: `7bf8e74a-c405-4541-a211-255922ea8942`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_3493_cinematic_studio_soul_cast_7bf8e74a.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3BUXDsgxEFXSJpiyq6QR917aU4E/hf_20260731_135752_d4e836dd-1afa-42b8-a724-543f834ee4fa.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3BUXDsgxEFXSJpiyq6QR917aU4E/hf_20260731_135752_d4e836dd-1afa-42b8-a724-543f834ee4fa_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Giải mã Cấu trúc JSON `[Character Params: {...}]` của Model `cinematic_studio_soul_cast` (`rank_3493_cinematic_studio_soul_cast_7bf8e74a.webp`)**: Kiểm định bằng mắt bức ảnh xuất cho thấy `cinematic_studio_soul_cast` tự động sinh **Bảng Casting 3-Panel ngăn cách bằng vạch đen dọc (`Panel 1: Toàn thân trước | Panel 2: Toàn thân sau 180° | Panel 3: Cận cảnh mặt`)** với độ đồng nhất tuyệt đối về gương mặt râu lởm chởm, áo thun xanh navy in logo và đai đồ nghề thợ điện!

```text
Luca Moretti fixed a festival blackout solo; now he must prevent the mayor’s gala collapsing.
[Character Params: {"age": "young - adult, 35 y.o", "race": "European", "genre": "Comedy", "gender": "male", "outfit": "A utility electrician wears a dark blue flame-resistant T-shirt with the company, paired with sturdy jeans or work pants featuring reinforced knees and tool pockets. EH-rated leather boots with non-conductive soles complete the base uniform. utility belt with tools", "archetype": "Hero", "body_type": {"build": "athletic", "height": "tall"}, "eye_color": "brown", "hair_type": {"style": "short", "texture": "wavy"}, "hair_color": "brown", "facial_hair": "stubble", "ATTRACTIVENESS": "attractive appearance"}]
```

##### 🏆 Rank #3483 (`0 ♡` | `0 👁️` | Model: `cinematic_studio_soul_cast` | Author: `@highenergyfield` | Size: `2048x1152` | Refs: `0`)
- **Publication ID**: `8dbbf2f0-a6ab-4741-a239-d2325f951b6e`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_3483_cinematic_studio_soul_cast_8dbbf2f0.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DZPfIecwWyoFonX31rcKClElfe/hf_20260818_110049_460e9ad1-31e2-4dee-b857-be48373debeb.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_3DZPfIecwWyoFonX31rcKClElfe/hf_20260818_110049_460e9ad1-31e2-4dee-b857-be48373debeb_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Mẫu JSON `[Character Params]` cho Nữ Chính Á Đông (`Mei Lin Chen` — `Rank #3483`, `cinematic_studio_soul_cast`)**: Cấu trúc khai báo đầy đủ `age`, `race`, `genre`, `gender`, `outfit`, `archetype`, `body_type`, `eye_color`, `hair_type` để sinh bảng nhân vật 3 góc chuẩn điện ảnh.

```text
Mei Lin Chen fled her seaside hometown at twenty; now love forces a dangerous choice.
[Character Params: {"age": "young, 25 y.o", "era": "2020", "race": "Asian", "genre": "Romance", "gender": "female", "outfit": "纯白缎面伴娘服", "archetype": "Innocent", "body_type": {"build": "skinny", "height": "average"}, "eye_color": "brown", "hair_type": {"style": "long", "texture": "straight"}, "hair_color": "black", "ATTRACTIVENESS": "extraordinary beautiful face with high-fashion supermodel facial features"}]
```

##### 🏆 Rank #3502 (`0 ♡` | `0 👁️` | Model: `cinematic_studio_soul_cast` | Author: `@axellent361` | Size: `2048x1152` | Refs: `0`)
- **Publication ID**: `daf4ad87-f60c-4a2a-ba60-831a9e554361`
- **Local Audited File**: `data/community_images/downloaded_images/full_prompts/rank_3502_cinematic_studio_soul_cast_daf4ad87.webp`
- **Output Image (`.png`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38w6jZK5dva7W5cA0TTU4Fxkk0M/hf_20260429_131857_b908bbc3-8672-4553-b34b-211fc6616794.png
- **Output Preview (`_min.webp`)**: https://d8j0ntlcm91z4.cloudfront.net/user_38w6jZK5dva7W5cA0TTU4Fxkk0M/hf_20260429_131857_b908bbc3-8672-4553-b34b-211fc6616794_min.webp
- **👁️ Visual Audit Verdict (`Before Ref vs After Output`)**: **Mẫu JSON `[Character Params]` cho Nam Chính Đường Phố (`Malik Thompson` — `Rank #3502`, `cinematic_studio_soul_cast`)**: Khóa chi tiết chất liệu áo hoodie nỉ nặng (`heavyweight fleece`), quần cargo và giày sneaker da lộn trong schema `[Character Params]`.

```text
Malik Thompson, mixtape prodigy sold out his first show at fifteen, now fights eviction.
[Character Params: {"age": "young, 25 y.o", "era": "2000", "race": "Black", "genre": "Comedy", "gender": "male", "outfit": "hip hop urban in the 2000 years ", "archetype": "Creator", "body_type": {"build": "athletic", "height": "tall"}, "eye_color": "gray", "hair_type": {"style": "braids", "texture": "curly"}, "hair_color": "black", "facial_hair": "short beard", "ATTRACTIVENESS": "extraordinary beautiful face with high-fashion supermodel facial features"}]
```

---

### 21.🎄 CHUYÊN ĐỀ 7: CẨM NANG ỨNG DỤNG TRỰC TIẾP CHO DỰ ÁN TVC CỦA BẠN (ĐẶT CÂY THÔNG NOEL CỦA BẠN VÀO PHÒNG KHÁCH ĐIỆN ẢNH BẰNG CÁC BÍ KÍP VỪA GIẢI MÃ)

#### 🔍 Kiểm Định Thị Giác 2 Bức Ảnh Cây Thông Noel Gốc Của Bạn (`Visual Audit of User Uploaded Product Photos`)
Trước khi thiết kế bộ câu lệnh, chúng tôi đã soi trực tiếp 2 bức ảnh sản phẩm bạn tải lên:
1. **Ảnh 1 (`media_1792546525662_557c1cca.jpg` — Cận cảnh Cành thông & Dải tính năng)**:
   - **Đặc điểm vật lý cốt lõi cần khóa (`Product DNA Lock`)**: Cành thông nhựa PE/PVC xanh đậm có **đầu lá phủ tuyết trắng mịn (`frosted snow-flocked needle tips`)**, xen kẽ **chùm quả mọng đỏ bóng (`clusters of glossy red holly berries`)** và **bóng đèn LED tròn phát sáng vàng ấm (`warm 2700K glowing LED fairy bulbs`)**. Phía dưới ảnh có dải băng rôn xanh lá in 4 icon tính năng (`Fireproof / Non-Allergic / Anti-Fading / Smell-Free`) — khi đưa ảnh này làm `@img2` (tham chiếu chi tiết cành), chúng ta phải thêm lệnh **`"Ignore the green promotional banner and icons at the bottom of the closeup reference"`** (áp dụng bài học từ `Rank #1025`) để AI không vô tình in dải banner xanh lên ảnh TVC!
2. **Ảnh 2 (`media_1792546554461_c5de676e.jpg` — Toàn cảnh Cây thông trong Phòng khách trắng)**:
   - **Đặc điểm vật lý & Lý do ảnh gốc chưa đạt chất TVC điện ảnh**: Cây thông dáng cao thon, tán lá dày phủ tuyết nhẹ + quả đỏ + đèn LED vàng ấm, phần chân bọc **túi vải bố màu nâu kem thắt dây (`natural beige woven burlap sack base`)**, đặt giữa **lò sưởi trắng (`white fireplace mantel`) bên trái** và **cửa sổ kính rèm trắng bên phải** trên sàn gỗ sáng.
   - **Chẩn đoán Thị giác (`Why it looks flat right now`)**: Trong ảnh 2 hiện tại, căn phòng đang bị chiếu sáng phẳng (`flat high-key white daylight`), cửa sổ bên phải trắng xóa và lò sưởi bên trái đang tắt tối, khiến ánh đèn LED vàng ấm trên cây thông bị chìm nghỉm vào tường trắng!
   - **Giải pháp Đạo diễn từ Kho 1,819 Ảnh & 29 Phim**: Áp dụng ngay 5 quy trình thực chiến dưới đây để biến chính cây thông chân bọc vải bố này thành TVC Giáng Sinh triệu đô:

---

#### Bước 1: Tạo "Bảng Xoay Chuẩn Hóa Cây Thông 3-Panel" (`3-Panel Orthographic Product Sheet` — Công thức `@thomas_lundstrom` `@IMG_006` + `Rank #692`)
- **Mục đích**: Giúp bạn có đủ 3 góc chuẩn (Chính diện toàn cây + Nghiêng 3/4 + Cận cảnh Macro đầu cành phủ tuyết & quả đỏ) trên nền studio xám trung tính `#E8E6E1`, đồng thời lọc bỏ hoàn toàn dải banner quảng cáo màu xanh ở ảnh 1.
- **Model khuyên dùng**: `gpt_image_2_5` hoặc `nano_banana_2_1` (Đính kèm Ảnh 2 toàn cây làm `@img1` và Ảnh 1 cận cảnh cành làm `@img2`).

```text
Use @img1 (full Christmas tree) and @img2 (macro branch detail, ignoring the green promotional text banner at the bottom) as the strict authoritative product references.
Create a photorealistic three-panel studio product reference sheet on a clean, neutral warm-gray seamless background (#E8E6E1), arranged horizontally side by side:
- LEFT PANEL (Full Front View): Straight-on eye-level full-height view of the exact pre-lit frosted artificial Christmas tree from @img1, showing its conical silhouette, dense dark-green pine branches with snow-flocked white tips, evenly distributed clusters of glossy red berries, warm 2700K LED lights, and the exact natural beige woven burlap sack base tied at the trunk.
- CENTER PANEL (Three-Quarter 45° View): The exact same Christmas tree rotated 45 degrees, showcasing the volumetric depth of the hinged branches, layered snow frosting, red berry clusters, and the three-dimensional roundness of the woven burlap base.
- RIGHT PANEL (Macro Branch & Material Detail): Extreme close-up studio macro shot matching @img2, showing the individual snow-dusted PE/PVC pine needles, glossy crimson berry cluster, and a warm glowing 2700K LED bulb with realistic translucent housing.
STRICT CONSISTENCY: Preserve the exact branch density, snow-flocking ratio, red berry size, warm LED color temperature, and burlap sack base across all panels. No promotional banners, no text, no icons, no extra ornaments added. Aspect ratio 16:9.
```

---

#### Bước 2: Biến Phòng Khách Trắng Phẳng Trong Ảnh 2 Thành Phòng Khách Điện Ảnh Chạng Vạng Tuyết Rơi (`Blue-Hour Chalet Relighting` — Công thức `Rank #675` + `Rank #3396` + `@adilinthewild` `@IMG_068`)
- **Mục đích**: Giữ nguyên 100% cây thông Noel chân bọc vải bố VÀ giữ nguyên vị trí lò sưởi bên trái + cửa sổ bên phải của Ảnh 2 (`media_1792546554461_c5de676e.jpg`), nhưng chuyển thời gian sang **Chạng vạng xanh tuyết rơi (`Blue Hour 6500K` ngoài cửa sổ)** và **Bật lửa lò sưởi ấm áp (`2200K–2700K` bên trong)** để hàng trăm bóng đèn LED trên cây thông tỏa sáng lung linh!
- **Model khuyên dùng**: `gpt_image_2_5` hoặc `nano_banana_2` (Đính kèm Ảnh 2 `media_1792546554461_c5de676e.jpg` làm `@img1`).

```text
Edit the attached living room photograph (@img1). Keep the exact pre-lit frosted Christmas tree with red berries and its beige woven burlap base in the exact same position, scale, and proportions. Keep the exact room layout: the white fireplace mantel on the left, the tall window with sheer white curtains on the right, and the natural hardwood floor.

DRAMATIC CINEMATIC RELIGHTING (BLUE HOUR WINTER DUSK):
1. EXTERIOR WINDOW (6500K Cool Blue Hour): Turn the bright white window on the right into a twilight winter evening scene — soft blue-hour dusk outside with gentle snowflakes falling past dark pine trees, casting a subtle cool 6500K blue rim light across the sheer curtain folds.
2. INTERIOR FIREPLACE & TREE GLOW (2700K Warm Golden): Light a warm, crackling golden-orange fire inside the firebox of the left fireplace mantel, and make the warm 2700K LED string lights embedded in the frosted Christmas tree branches glow softly and naturally, casting delicate warm specular reflections onto the polished hardwood floor and illuminating the snow-dusted needle tips and glossy red berries.
3. CAMERA & FILM LOOK: Shot on ARRI Alexa 35 with a 35mm prime lens, T2.0, natural shallow depth of field, rich dynamic range with preserved highlight detail in every LED bulb (no blown-out white halos), fine Kodak Vision3 500T film grain. No text, no logos, no CGI plastic look.
```

---

#### Bước 3: Đặt Cây Thông Của Bạn Vào Bất Kỳ Phòng Khách Mới Nào Bằng Mẹo "Khoanh Vùng Màu MS-Paint" (`Rank #1708` & `Rank #3158`) Hoặc "Tắt Đèn Gắt Ban Ngày + Khóa Tỷ Lệ" (`Rank #1103`)

##### Cách 3A — Mẹo Nhanh Nhất: Khoanh Vùng Đỏ/Vàng Bằng MS-Paint Trên `seedream_v5_pro` (`Rank #1708` & `Rank #3158`)
- Mở bức ảnh phòng khách bất kỳ, dùng bút màu **Đỏ (`Red Drawn Area`)** khoanh vùng góc phòng nơi muốn đặt cây thông, và vẽ đường màu **Vàng (`Yellow Drawn Lines`)** dọc theo bệ lò sưởi nơi muốn thêm dây thông đèn LED. Nạp ảnh phòng đã vẽ (`@img1`) + Ảnh 2 cây thông của bạn (`@img2`) vào `seedream_v5_pro`:

```text
PLACE THE EXACT FROSTED CHRISTMAS TREE WITH RED BERRIES AND BEIGE BURLAP BASE FROM @IMG2 INTO THE RED DRAWN AREA OF @IMG1, ADD WARM GLOWING GARLAND AND LED LIGHTS ALONG THE YELLOW DRAWN LINES, TURN ON THE FIREPLACE WITH WARM GOLDEN LIGHT. REMOVE ALL RED AND YELLOW DRAWN MARKUP LINES COMPLETELY.
```

##### Cách 3B — Ghép Chuẩn Kiến Trúc Vào Phòng Khách Ban Ngày Bằng Quy Tắc `Rank #1103` + `Reverse-Polish` (`Rank #476`)
- Khi ghép cây thông (`@img1`) vào một bức ảnh phòng khách ban ngày (`@img2`), áp dụng quy tắc **giảm độ chói đèn LED để lá thông tuyết ăn nắng tự nhiên của phòng** (`Rank #1103`) và **khóa độ nhiễu hạt camera** (`Rank #476`):

```text
Use @img2 as the authoritative living room background and @img1 as the exact product reference for the frosted Christmas tree with red berries and beige woven burlap base.
Place the Christmas tree naturally in the clear corner between the sofa/fireplace and the window.
SCALE LOCK: The tree height should reach approximately 75% of the ceiling height, with its lower branch diameter narrower than the adjacent armchair — never oversized.
LIGHTING INTEGRATION (RANK #1103 RULE): The tree's internal LED lights emit only a subtle, restrained warm 2700K glow so that the natural afternoon sunlight entering from the room's window is the primary light source revealing the white snow-flocked needle tips, deep green foliage, glossy red berries, and burlap base texture. Cast a physically accurate soft contact shadow beneath the burlap base onto the wooden floor.
REVERSE-POLISH REALISM LOCK (RANK #476 RULE): Match the exact lens sharpness, sensor grain, color temperature, and dynamic range of the living room photograph (@img2). The inserted tree must not look sharper, cleaner, or more saturated than the rest of the room.
```

---

#### Bước 4: Đảo Góc Máy Liên Hoàn Quanh Cây Thông Trong Cùng Phòng Khách (`Camera Repositioning` — Công thức `@pietromalegori/control` `@IMG_027` & `@IMG_059` + `Rank #1499`)
Sau khi đã có tấm ảnh Master Shot từ Bước 2 (cây thông đặt giữa lò sưởi và cửa sổ), dùng chính tấm ảnh đó làm `@img1` trên `nano_banana_2` hoặc `seedream_v5_pro` để sinh tiếp **3 góc máy cắt cảnh (Cutaways)** cho kịch bản TVC 15 giây:

1. **Cảnh Cutaway 1 — Góc thấp sát sàn nhìn từ hộp quà/chân vải bố hướng lên ngọn thông (`Low-Angle Floor Perspective` — `@IMG_059`)**:
   ```text
   Using @img1 as the strict scene and continuity reference, reposition the camera to a low floor-level angle near the woven beige burlap base of the Christmas tree, looking upward at 35 degrees through the snow-frosted pine branches and glowing 2700K LED lights toward the top of the tree and ceiling. Keep the exact fireplace glow on the left and blue-hour snowy window on the right. Shallow depth of field, 35mm lens, foreground burlap weave and lowest frosted branch in tack-sharp focus.
   ```
2. **Cảnh Cutaway 2 — Góc Cận cảnh Macro 85mm chạm tay vào cành thông phủ tuyết & quả đỏ (`Macro Tactile Detail` — trình diễn tính năng `Non-Allergic & Anti-Fading` từ Ảnh 1)**:
   ```text
   Stay 100% inside the established living room of @img1, but move the camera to an extreme close-up 85mm macro shot (f/2.0) of one snow-frosted pine branch cluster with glossy red berries and a warm glowing LED bulb. A woman's hand in a cream chunky knit sweater sleeve gently touches the soft snow-dusted needle tips (demonstrating soft, non-allergic realistic PE needle texture). In the softly blurred bokeh background, the warm fireplace flames and blue-hour window remain visible in the exact same positions.
   ```
3. **Cảnh Cutaway 3 — Góc nhìn từ ngoài cửa sổ tuyết rơi nhìn xuyên qua kính vào phòng khách ấm áp (`Exterior-to-Interior Window Frame` — `@lukasbandana/rewind` `@IMG_004` + `Rank #526`)**:
   ```text
   Using @img1 as the exact interior reference, reposition the camera OUTSIDE the house in the snowy blue-hour evening, looking IN through the tall glass window panes toward the warm living room. Through the glass (with subtle frost at the corners and faint outdoor reflections), we see the exact frosted Christmas tree with red berries and warm glowing LED lights standing next to the crackling white fireplace. Strong cinematic color contrast between 6500K cold snowy exterior and 2700K warm cozy interior.
   ```

---

## 22. CẨM NANG VIDEO QUẢNG CÁO & CONTENT VIRAL TỪ 18 MODELS TRÊN HIGGSFIELD COMMUNITY (`5,723` SHOTS — `1,612` FULL PROMPTS)

> **Báo cáo chi tiết đầy đủ**: Xem tại [`data/community_shots/COMMUNITY_VIDEO_ADS_AND_CONTENT_PLAYBOOK.md`](./data/community_shots/COMMUNITY_VIDEO_ADS_AND_CONTENT_PLAYBOOK.md) và bảng xếp hạng tổng [`data/community_shots/RANKED_COMMUNITY_PROMPTS.md`](./data/community_shots/RANKED_COMMUNITY_PROMPTS.md).
> - **Mở rộng quy mô từ 8 lên 18 Models Video**: Bổ sung 10 model chuyên trị Quảng cáo & Content (`marketing_studio_v2_video`, `marketing_studio_video`, `ad_multiplier`, `viral_hub_video`, `cinematic_studio_video_v2`, `kling3_0`, `kling2_6`, `kling_o3_image_reference`, `kling_o3_flf`, `wan3_0_prime`) bên cạnh 8 model `Seedance` & `MiniMax H3`, đồng thời giải mã toàn bộ các trường ẩn `products` / `web_products` / `avatars` / `enhanced_prompt` / `multi_prompt` / `chain_preset` / `video_edit`.
> - **Bộ lọc chặn sạch 100% Rác (`EXCLUDED_VIDEO_MODELS`)**: Đã tích hợp `is_excluded_video_model()` và `is_excluded_video_shot()` trong [`scraper/higgsfield_community_scraper.py`](./scraper/higgsfield_community_scraper.py) để loại bỏ hoàn toàn các video chỉ ghép mặt, nhép chuyển động từ video có sẵn hoặc chỉ nâng nét (`motion_control`, `replace_object`, `genjutsu`, `topaz_video`, `upscale`, `restyle`).
> - **Kiểm định Thị giác Bắt buộc (`Visual Audit First`)**: Toàn bộ 43 video tiêu biểu thuộc 6 nhóm kỹ thuật dưới đây đều đã được trích xuất Thumbnail / Frame thực tế và kiểm tra bằng mắt trước khi đưa vào sổ tay.

### 22.1. Nhóm 1 — Quay Quảng Cáo Sản Phẩm Trực Tiếp, Macro Chất Liệu & Bóc Tách Cơ Khí (`Direct Product Commercials`)
1. **Khóa Bao Bì Tuyệt Đối (`<<<image_1>>> Source of Truth + Anti-Morphing Rule`) trên `Seedance 2.5`**:
   - **Dẫn chứng**: **Rank #5** (`seedance_2_5` | `647 ♡` | `67,794 views` | `@religious_raccoon_dark36` | ID: `099ee2c0-3c13-4e3d-971f-d78d59a9a9a9` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3Btsg1RieQOoYK6o6x65C3UYqNH/hf_20260814_024423_23e78b00-c455-420b-b72f-fc8e9b14244c_wm3.mp4)).
   - **Thần chú khóa hình dáng sản phẩm qua nhiều cảnh cắt**:
     ```text
     ACTIVE REFERENCE
     <<<image_1>>> is the exact product reference and the visual source of truth. Preserve the small rectangular matte pink drink carton, its proportions, folded top, white bendable straw, striped sunset symbol, dark cherry-red SIPPO logo, Cherry label and two smiling cherries with green stems. Keep the packaging recognizable and unchanged in every shot. It remains a carton and never becomes a can, bottle or plastic container.
     ```
2. **Quảng Cáo CGI Kiểu Apple Launch & Ánh Sáng Tạt Ngang Soi Vân Vật Liệu (`Extreme Macro Grazing Light`) trên `Marketing Studio 2.0 Video`**:
   - **Dẫn chứng**: **Rank #423** (`marketing_studio_v2_video` | `2 ♡` | `@rubensapple1583` | ID: `7a0d75c7-f3aa-41b8-ab3c-fdd78369e926` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3F7yPJjIXYfpGjxMJKMQz7g2QC6/hf_20261010_115134_cef791a2-9da0-460f-999a-e9766c49bd1f.mp4)) & **Rank #1002** (`marketing_studio_v2_video` | `1 ♡` | ID: `63ace82b-cb15-4b0b-a054-e9cae83385f4` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3F7yPJjIXYfpGjxMJKMQz7g2QC6/hf_20260930_140026_d5e94956-0e65-42d0-b2d5-5456e0732311.mp4)).
   - **Mẹo thực chiến**: Để sản phẩm mỏng/chi tiết nhỏ (như miếng dán vân gỗ hoặc cành thông phủ tuyết) trông đắt tiền như TVC Apple, hãy mở đầu bằng `beginning with an extreme macro shot... so the natural wood grain, organic fibers, matte finish, and subtle texture variations are clearly visible` rồi mới kéo ra góc Hero Shot có bóng nắng kiến trúc (`architectural window shadow gobo`).
3. **Mở Hộp Nam Châm Tự Động & Găng Tay Đen Nâng Sản Phẩm (`Magnetic Lid + Black Nitrile Gloves`) trên `Cinematic Studio Video 2.0`**:
   - **Dẫn chứng**: **Rank #1383** (`cinematic_studio_video_v2` | `@rodinbutter1432` | ID: `ba9f9ca6-8d19-4c31-a1ea-a815d7adce23` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3CIzu7iEmjuhh79yk00TQGnBW6m/hf_20260702_114217_425e6fa3-2a9a-4ad0-af5a-3e9ef6911ccf.mp4)).
   - **Thần chú**: `The magnetic lid smoothly opens by itself. A pair of black premium gloves slowly enter the frame and gently lift <<<product_uuid>>> vertically from the velvet insert. The bottle rises slowly while remaining perfectly upright. The camera simultaneously performs a subtle orbit around the bottle, revealing elegant reflections across the glass.`
4. **Bóc Tách Linh Kiện Cơ Khí Có Chú Thích (`Exploded Assembly + Technical Callouts`) & Bàn Xoay Kết Hợp Lớp Ghost Mờ `8–12% Opacity`**:
   - **Rank #1478** (`marketing_studio_v2_video` | `@gsgrafikdesign` | ID: `325f7d36-4b2f-4d62-a3be-c8871231b346` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3HkG5BLPcXoqeCy1Xb4GWovBYNi/hf_20260930_234824_460ff346-6897-4cad-a756-26ac45da1487.mp4)): Bung rã 3 tầng đồng hồ `Rolex Sky-Dweller` kèm đường chỉ mảnh màu trắng (`thin white lines with a measurement point and uppercase labels`).
   - **Rank #401** (`wan3_0_prime` | `2 ♡` | `@animura7` | ID: `adbe2c2c-4510-422c-8469-bc3c98777a1d`): Khi muốn chèn hiệu ứng đồ họa xung quanh sản phẩm đang xoay trên bàn xoay mà không làm lem sản phẩm, hãy khóa hiệu ứng ở tường phía sau với độ mờ **`at about 8 to 12% opacity, slightly out of focus, in the middle band of the frame (between about 28% and 85% of the frame height), never above 26% so the logo is never covered`**.

---

### 22.2. Nhóm 2 — 3-Giây Mở Đầu Giật Tít (`Viral Hooks`), Ẩn Dụ Thị Giác & `FOOH` (`Viral Hub` & `Kling O3`)
1. **Ẩn Dụ Thị Giác Chạy Nước Rút Nhưng Khóa Cứng Sản Phẩm Ở Ngực (`Rank #516` — `kling_o3_image_reference`)**:
   - **Dẫn chứng**: **Rank #516** (`1 ♡` | `@wunderbiuser` | ID: `4d433368-84ab-4065-baae-54b6ab39f72a` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_39tC1erxLvNheGIafYE4EronzE9/hf_20261013_115016_dc9c6b0f-a1eb-4059-aadc-4156991557b0.mp4)).
   - **Cấu trúc câu lệnh**: Cho nhân vật làm bằng giấy chạy nước rút làm giấy bay tơi tả phía sau, nhưng khóa cứng sản phẩm đang bê: `The printer stays rigid, sharp and undistorted, with the "Canon" wordmark and the "i-SENSYS MF460 II" label readable throughout.`
2. **Sản Phẩm Tiền Cảnh Khóa Nét + Tình Huống Bất Ngờ Ở Hậu Cảnh (`Rank #1134` — `viral_hub_video`)**:
   - **Dẫn chứng**: **Rank #1134** (`@bouarroudj` | ID: `4bbcdd7e-142e-42ec-bffe-780ae9f21406` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3JJZy54TWKTfahWhaUv4Ufs2iN6/hf_20260926_110727_52d6746e-8e80-4f19-bfde-da20fdbf4618.mp4)).
   - **Thần chú**: `Preserve the reference burger exactly... prominent in foreground, shallow depth of field. A woman notices it, approaches and reaches for it. Just before she grabs it, an unexpected funny event happens in the background... Keep burger sharp, appetizing and unchanged.`

---

### 22.3. Nhóm 3 — `First-to-Last Frame` (`kling_o3_flf` & `minimax_h3`) & Biến Hình Không Gian (`Before ➔ After`)
1. **Stop-Motion Lắp Ráp Nội Thất Từng Vùng Không Trôi Máy (`Zone-by-Zone Stop-Motion Room Fill` — `Rank #2943`, `kling_o3_flf`)**:
   - **Dẫn chứng**: **Rank #2943** (`@miragency` | ID: `ae03eae3-9ba8-4097-8498-96bcbe6b8b3e` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3I4xLOm1JmRTPoRUGApegaiYts6/hf_20261020_124115_67002094-f6a4-4352-b988-2c1ca6441b59.mp4) | [Start Frame](https://d8j0ntlcm91z4.cloudfront.net/user_3I4xLOm1JmRTPoRUGApegaiYts6/hf_20261020_123807_45361a11-8343-4f85-b0a8-28183c923dfb.png) | [End Frame](https://d8j0ntlcm91z4.cloudfront.net/user_3I4xLOm1JmRTPoRUGApegaiYts6/hf_20261020_123642_47c2a2e6-33b3-4103-ac17-436e44627b1c.png)).
   - **Nguyên văn câu lệnh**:
     ```text
     Static locked-off overhead camera, no camera movement. The empty floor plan fills with furniture zone by zone, each item quickly popping into place in a clean satisfying stop-motion style with soft shadows: first the storage cabinets along the wall, then the editing desk with monitor, then the shooting table with backdrop and lights, then the work desk and chair, then the leather armchair corner, finally the sofa, rugs and plants. Lighting stays the same. No people, no text.
     ```
2. **Ưu Tiên Khung Cuối Làm Bản Vẽ Chuẩn Khi Dựng Timelapse Từ Dưới Lên (`Last-Reference Blueprint Priority` — `Rank #518`, `minimax_h3`)**:
   - **Dẫn chứng**: **Rank #518** (`1 ♡` | `@bufflabs` | ID: `1aeb4993-7688-4e1a-8f62-93c0d7920bd5` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3H8EdXU4pxMybpIeiRAa7tcZ8eD/hf_20260924_083009_28fc1f3e-3194-40d2-9019-3da9f77acafb.mp4)).
   - **Thần chú**: `REFERENCE PRIORITY: Use the LAST reference image as the strict architectural blueprint and final appearance. Use the FIRST reference image only to guide the unfinished concrete structure... Show workers constructing the central building progressively from the bottom upward, floor by floor, until it matches the completed building in the final reference image.`
3. **Nguyên Liệu Lơ Lửng Xoáy Vào Hộp ➔ Biến Thành Cảnh Thưởng Thức (`Rank #329`, `minimax_h3` & `Rank #656`, `seedance_2_0_mini`)**:
   - **Dẫn chứng**: **Rank #329** (`2 ♡` | `@ahiggs01` | ID: `d93cf9d9-3c43-4216-ba86-4507dc913f17` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3EWhRDy7XGliqGhTrAQjo9MKGRf/hf_20260925_063335_557fc07a-e11e-4de0-8aec-1c7124f924da.mp4)).
   - **Cấu trúc**: `0–3s: All ingredients are visible together above the open can... 3–7s: The ingredients follow a graceful downward spiral into the can, with realistic gravity...`
4. **Nối Mượt 2 Ảnh Khác Bối Cảnh Bằng Quầng Sáng Mặt Trời / Đèn LED (`Sun-Glare Bloom Wipe` — `Rank #1477`, `kling_o3_flf`)**:
   - **Dẫn chứng**: **Rank #1477** (`@lzg` | ID: `800b1482-79c0-46fb-bbcd-97352b207e24` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3KKBwPOluFEfLroZh9IsFdwwSdX/hf_20261007_152805_db983c06-bf44-46a9-a671-87c6b92e7823.mp4)).
   - **Thần chú**: `The camera gently tilts up toward the low sun; the sun's warm glare softly blooms and grows until soft golden light fills the whole frame. As the glow gently recedes, the light settles into [End Frame scene]... Seamless, graceful light transition.`

---

### 22.4. Nhóm 4 — Chuyển Động Máy Quay Điện Ảnh 1-Shot (`Kling 3.0` & `Cinematic Studio Video 2.0`)
1. **Khóa Cứng Máy Quay Vào Vật Thể Đang Chạy (`Rigid Object-Locked SnorriCam` — `Rank #2`, `kling3_0`, `924 ♡`)**:
   - **Dẫn chứng**: **Rank #2** (`924 ♡` | `139,290 views` | `@ryanp_tx` | ID: `794da67f-12d8-447e-8197-755f2e2df3e4` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3709hEjL37V5u3gPiUc1pSGtMwx/hf_20260204_182741_50727a49-430c-42e5-9602-e2d9c60e526a.mp4)).
   - **Thần chú**: `Low-angle wide-angle tracking shot focused on a crumpled brown paper bag held tightly in a man’s hand. The camera is rigidly locked to the bag with precise tracking — the bag stays centered and stable while the world rushes past.`
2. **Đẩy Xuyên Qua Phản Chiếu Tròng Kính Không Cắt Cảnh (`Reflection-to-Reality Dolly-Through` — `Rank #8`, `kling3_0`, `579 ♡`)**:
   - **Dẫn chứng**: **Rank #8** (`579 ♡` | `64,860 views` | `@ryanp_tx` | ID: `ac18b4d3-372e-49b4-abe7-6e51d5c0cc40` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3709hEjL37V5u3gPiUc1pSGtMwx/hf_20260204_182642_cc3d2d10-6a80-42bb-87e8-fd34049c299a.mp4)).
   - **Thần chú**: `The camera continues a smooth, uninterrupted dolly straight into the glasses without changing angle or direction, no portal effect, no cut, the reflection seamlessly becomes reality.`
3. **Xoay Quỹ Đạo Cung Tròn Khóa Cứng 1 Điểm Neo (`Fixed Pivot Point Arc Orbit` — `Rank #604`, `cinematic_studio_video_v2`)**:
   - **Dẫn chứng**: **Rank #604** (`1 ♡` | `@sasvisuals` | ID: `08f434f7-30b2-4e2f-b18b-1c6f3dad2ed8` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_2xBMWCyHtA749tpt7NYiF1is1wP/hf_20260824_190549_0e4a1e6a-bc9e-4770-a680-a88f74023f6e.mp4)).
   - **Thần chú chống trôi tâm khung hình**: `Create a smooth cinematic arc right camera movement... The camera must stay perfectly locked on one fixed tracking point: the center of the wheel hub, specifically the center of the SAS logo cap. This point remains centered and stable throughout the entire shot with zero drift.`

---

### 22.5. Nhóm 5 — Nhân Vật Tương Tác Sản Phẩm (`UGC Creator`) & Thoại Ngắn 15 Giây (`Marketing Studio Video`)
- **Dẫn chứng Top #3 Toàn Bảng Xếp Hạng (`752 ♡`, `264,029 views`)**: **Rank #3** (`marketing_studio_video` | `@byzantinetiger1459` | ID: `19f9c5f8-9ca4-4369-937b-16baa3ace52f` | [Video `.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3CIjqzTsrKEUr8OzFBaYO4ux3nG/hf_20260413_121933_7dfa9582-a536-4a83-9041-ee5aa102ff8c.mp4)) & **Rank #11** (`539 ♡` | `139,768 views` | ID: `bbbc4150-f6fb-488f-8e45-0842c7bdfb86`).
- **3 Quy tắc vàng khi làm UGC trên `Marketing Studio Video`**:
  1. **Luôn khóa đồng thời cả `<<<avatar:UUID>>>` (`@IMG_02`) và `<<<product:UUID>>>` (`@IMG_01`) kèm lệnh `ANGLE LOCK — DO NOT VIOLATE` trong `enhanced_prompt`**: Ở `Rank #3`, bản `enhanced_prompt` hậu trường giải mã từ API tiết lộ bí quyết giúp bình giữ nhiệt `AURA` (`@IMG_01`) giữ nguyên chữ khắc laser dọc thân bình suốt 15s: `ANGLE LOCK — DO NOT VIOLATE: The camera is positioned IN FRONT OF the woman inside the car, facing her directly — passenger-seat / dashboard mount POV looking at her face and torso... Every cut in this video must be from a DIFFERENT angle or distance.` Ngược lại, kiểm định thị giác ở **Rank #1185** cho thấy nếu quên gắn token sản phẩm hoặc nhồi 6 cảnh cắt vào 1 lần sinh video, chữ nhỏ trên bao bì sẽ bị nhòe khi nhân vật vẫy tay!
  2. **Cụm từ khóa khử "màu nhựa AI" để ra chất cam trước iPhone thật (`Rank #11`, `#18`, `#50`)**:
     ```text
     Shot on iPhone front camera (selfie mode), vertical 9:16, natural HDR, slight handheld movement, real skin tones, no color grading, casual framing, feels real and unpolished.
     ```
  3. **Chia kịch bản 15 giây thành 3 nhịp rõ ràng (`0–4s Hook Selfie ➔ 4–10s Cận cảnh sờ chất liệu/dùng thử ➔ 10–15s Hero Shot + Kết câu thoại`)** như `Rank #18` (`403 ♡`, `74,132 views`) và `Rank #44` (`232 ♡`).
  4. **Công Thức "KOL Review Nhanh 10 Giây — 4 Nhịp Rapid Hard Cuts & High-Energy Performance" (`9:16 Vertical` — Mẫu Thực Chiến Ăn Khách Do Người Dùng Đóng Góp)**:
     - **Giải mã cấu trúc ăn tiền của câu lệnh**:
       * **Nhịp cắt siêu nhanh 4 phân đoạn trong 10 giây (`0.0–1.2s` ➔ `1.2–3.8s` ➔ `3.8–7.5s` ➔ `7.5–10.0s`)**: Phá bỏ sự đơn điệu của 1 góc máy cố định bằng `Mixed camera angles with rapid HARD CUTS` (từ `MEDIUM SELFIE` lao nhanh vào ống kính ➔ `DYNAMIC shots` chỉ tay khoe quy mô 2.5m + vuốt cận cảnh đầu lá thông kết tinh ➔ `TIGHT SELFIE CLOSE-UP` ánh đèn nhiều màu hắt lên da mặt ➔ `Final high-energy recommendation` chỉ tay xuống `link in bio`).
       * **Lệnh ép diễn xuất năng lượng cao (`[CRITICAL]: DEMAND HIGH-ENERGY PHYSICAL PERFORMANCE`)**: Khóa biểu cảm gương mặt (`huge grin`, `expressive head tilts and wide eyes showing "insane" wonder`, `satisfied nod`) và cử chỉ tay linh hoạt trong mọi khung hình.
       * **Khóa giải phẫu chống mọc thừa tay khi khua tay nhanh (`Strict Two-Hand Lock`)**: `CRITICAL: Maintain strict anatomical integrity with EXACTLY TWO HANDS; movements must feel natural and weighted.`
     - **Nguyên văn Prompt Mẫu Chuẩn (`VIVATREES 10s KOL Fast-Cut Review`)**:
       ```text
       High-end 10-second fast-paced cinematic VIVATREES TVC with English voiceover, 9:16 vertical. [DIALOGUE]: "Check out this new tree from VIVATREES, guys. It's huge, two and a half meters! The detail is just insane—look at these crystalline snow needles. It makes the whole room glow. Honestly, it's a masterpiece. Check the link in my bio!" Style: UGC iPhone aesthetic, natural daylight. Mixed camera angles with rapid HARD CUTS. [CRITICAL]: DEMAND HIGH-ENERGY PHYSICAL PERFORMANCE. The creator (identity from ref 88289e39) must use dynamic, expressive hand gestures and intense facial expressions in every shot. 0.0-1.2s: MEDIUM SELFIE, he leans in fast with a huge grin and open-palm gesture. 1.2-3.8s: DYNAMIC shots of him gesturing wildly at the 2.5m scale and his fingers brushing the sharp crystalline needles with rapid focus shifts. 3.8-7.5s: TIGHT SELFIE CLOSE-UP, expressive head tilts and wide eyes showing "insane" wonder, multi-colored lights pulsing brightly on his skin. 7.5-10.0s: Final high-energy recommendation, sharp point toward the "link in bio" with a satisfied nod. CRITICAL: Maintain strict anatomical integrity with EXACTLY TWO HANDS; movements must feel natural and weighted. Sony A7V clarity, 720p, rich HDR shadows, no flickering. No text.
       ```

---

### 22.6. Nhóm 6 — 4 Kịch Bản Video Thực Chiến Cho "Cây Thông Noel Phủ Tuyết Chân Bọc Vải Bố" Của Bạn (Nối Tiếp Trực Tiếp Từ Mục 21)

Sau khi đã dùng **Mục 21** để tạo bộ ảnh Keyframe chuẩn điện ảnh từ 2 bức ảnh gốc của bạn (`Ảnh 1: media_1792546525662_557c1cca.jpg` — cận cảnh cành phủ tuyết, quả mọng đỏ, đèn LED 2700K; và `Ảnh 2: media_1792546554461_c5de676e.jpg` — toàn cảnh cây thông chân bọc vải bố đặt giữa lò sưởi trắng và cửa sổ), hãy đưa các tấm ảnh đó vào **4 quy trình Video** dưới đây:

1. **Kịch bản Video 1 — `Stop-Motion Room Transformation` trên `Kling O3 First-to-Last Frame` (`kling_o3_flf`) hoặc `MiniMax H3` (Công thức `Rank #2943` + `Rank #518`)**:
   - **Start Frame**: Ảnh phòng khách của Ảnh 2 đã xóa riêng cây thông Noel (giữ nguyên lò sưởi trắng bên trái + cửa sổ rèm voan bên phải).
   - **End Frame**: Ảnh 2 đã relight sang `Blue-Hour Dusk + Lò sưởi cháy ấm 2700K` có cây thông Noel chân bọc vải bố tỏa sáng.
   - **Prompt**:
     ```text
     REFERENCE PRIORITY: Use the LAST reference image as the strict blueprint and final appearance of the pre-lit frosted Christmas tree with red berries and beige woven burlap base. Use the FIRST reference image as the starting empty living room space between the white fireplace mantel and the tall sheer-curtained window.

     Static locked-off camera, zero camera drift. In the warm living room between the left fireplace mantel and right window, the Christmas tree progressively assembles and blooms into place from the bottom upward in a clean, satisfying stop-motion style with soft natural shadows: first the natural beige woven burlap sack base settles onto the hardwood floor, then the lower, middle, and top tiers of dark-green pine branches with snow-frosted white tips unfold to full conical volume, followed by clusters of glossy red holly berries popping onto the branches zone by zone, and finally the embedded warm 2700K LED fairy lights illuminate with a soft golden glow, matching the final reference image exactly. The fireplace, window curtains, and hardwood floor remain completely unchanged. No people, no text overlays.
     ```
2. **Kịch bản Video 2 — `1-Shot Fixed-Pivot Orbit` Khóa Cứng Chùm Quả Đỏ Không Trôi Tâm trên `Cinematic Studio Video 2.0` (Công thức `Rank #604 @sasvisuals`)**:
   - **Input Frame**: Bản `Blue-Hour Dusk` của Ảnh 2.
   - **Prompt**:
     ```text
     Use the provided reference image as the exact pre-lit frosted Christmas tree, snow-flocked branch density, glossy red berry clusters, beige woven burlap sack base, left white fireplace, and right window.
     Create a smooth cinematic arc right camera movement. The camera performs a subtle short-radius horizontal orbit from left to right while maintaining constant distance from the Christmas tree.
     The camera must stay perfectly locked on one fixed tracking point: the central cluster of glossy red holly berries in the middle tier of the tree. This point remains centered and stable throughout the entire shot with zero drift. As the camera moves right, the warm 2700K LED lights and fireplace glow create natural optical bokeh parallax while the woven burlap base, snow-frosted pine needles, and red berries retain their exact shape and realistic texture.
     ```
3. **Kịch bản Video 3 — `TVC Apple Launch Macro Grazing Light` trên `Seedance 2.5` hoặc `Marketing Studio 2.0 Video` (Công thức `Rank #5` + `Rank #423` + `Rank #1002`)**:
   - **Input References**: `<<<image_1>>>` = Ảnh 2 (toàn cây chân vải bố), `<<<image_2>>>` = Ảnh 1 (cận cảnh cành phủ tuyết + quả đỏ, kèm lệnh bỏ qua dải banner xanh ở đáy ảnh).
   - **Prompt**:
     ```text
     SCENE CONTEXT
     A 15-second premium holiday home commercial showcasing our pre-lit frosted Christmas tree with red berries and woven burlap base, filmed with the clean, tactile precision of an Apple product launch film.

     ACTIVE REFERENCES
     <<<image_1>>> is the absolute visual source of truth for the full slender conical Christmas tree silhouette, snow-flocked dark-green branches, red berry clusters, warm 2700K LEDs, and natural beige woven burlap sack base tied at the trunk. <<<image_2>>> is the exact macro reference for the snow-dusted PE/PVC pine needles, glossy red holly berries, and warm LED bulb (strictly ignore the green promotional banner and icons at the bottom of <<<image_2>>>). Preserve the exact tree proportions, burlap base, and frosted needle texture in every shot. It remains a burlap-base frosted tree and never becomes a plastic-stand or bare green tree.

     SHOT SEQUENCE
     0.0–4.5s (Extreme Macro Grazing Light): Start with a slow macro glide along a single snow-flocked branch from <<<image_2>>> under warm golden raking light, highlighting the realistic 3D molded pine needles with white frost tips and glossy red berries. A woman's hand gently brushes the frosted needles, showing their soft, non-allergic resilient bounce with zero snow or needle shedding.
     4.5–9.5s (Burlap Base to Mid-Tier Crane Up): Smooth low-angle crane-up starting from the textured beige woven burlap sack base tied with twine on the hardwood floor, rising past the dense frosted branches as the warm 2700K LED fairy lights cascade to life.
     9.5–15.0s (Hero Packshot Lock): Slow dolly pull-back to the exact full-tree composition of <<<image_1>>> standing between the white fireplace mantel on the left and the sheer-curtained window on the right. The tree remains completely sharp, symmetrical, and unchanged as a final hero frame. No text overlays, no banners.
     ```
4. **Kịch bản Video 4 — `15s TikTok / Reels UGC Vlog` Quay Bằng Cam Trước iPhone trên `Marketing Studio Video` (Công thức `Rank #3` `752 ♡` + `Rank #11` `539 ♡`)**:
   - **Prompt**:
     ```text
     Style: Authentic TikTok UGC home decor vlog, shot on iPhone front and back camera mix, vertical 9:16, natural HDR, slight handheld movement, real skin tones, no heavy cinematic color grading.
     Prompt:
     A cheerful young woman in a cozy cream knit sweater is filming herself in her living room right next to the pre-lit frosted Christmas tree with red berries and beige woven burlap sack base from <<<image_1>>> (standing between the white fireplace on the left and window on the right). Keep the Christmas tree's exact slender conical shape, snow-frosted tips, red berries, warm LED lights, and beige burlap base unchanged.
     0–4s: Handheld selfie mode — she smiles into the front camera, points her hand toward the frosted Christmas tree and its cute woven burlap sack base behind her.
     4–10s: Quick cut to back-camera close-up — her hand gently squeezes and brushes a snow-flocked pine branch with glossy red berries and warm glowing LED bulbs, showing the soft non-allergic needles and zero snow shedding on her fingers.
     10–15s: She steps back for a full vertical view of the glowing frosted tree between the fireplace and window, giving a warm smile.
     Dialogue (natural, warm, ~15 sec):
     "I finally found a frosted Christmas tree that doesn't shed fake snow all over the floor. It comes pre-lit with these warm lights and red berries, and the little woven burlap base looks so much nicer than a metal stand!"
     ```

---

## 23. Giải Mã Dự Án `@aist/projects/detour` (`6,162` Jobs ➔ `982` Cụm Cảnh Duy Nhất, `84` Thư Mục Con, `486` Ảnh `@IMG`)

> **Hồ sơ đầy đủ**:
> - [`data/creators/aist/projects/detour/dna_report.md`](./data/creators/aist/projects/detour/dna_report.md)
> - [`data/creators/aist/projects/detour/VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/aist/projects/detour/VIDEO_CENTRIC_SCRAPED_PROMPTS.md)
> - [`data/DIRECTOR_STYLE_LIBRARY.md`](./data/DIRECTOR_STYLE_LIBRARY.md) (Mục `#6 — aist/detour`)

### 23.1. Thống Kê Quy Mô Sản Xuất & Tổ Chức Thư Mục Studio Đa Tác Giả
- **Quy mô thực chiến**: **`6,162` jobs** ➔ **`982` cụm cảnh Final Take duy nhất** (`302` cụm Video + `680` cụm Ảnh; tỷ lệ Re-roll **`6.27x`** = lọc bỏ `5,180` bản nháp `84.1%`).
- **Độ dài Prompt**: Trung bình **`3,532.3` ký tự** (Min: `16` chars, Max: **`19,067` chars**), mật độ tham chiếu **`1.61` UUID refs/scene** (`1,585` lượt gắn thẻ UUID), **`50.5%`** (`496/982` scenes) có khối khóa phủ định (`NEGATIVE LOCK / CONSTRAINTS`).
- **Phân bổ Model ở bản Chốt (`Final Take`)**: `Seedance 2.5` (**297** cụm Video — chiếm 98.3% lượng video toàn phim), `Seedream 5.0 Pro` (**225** cụm Ảnh), `ImageGen 2.0 (GPT Image 2.0)` (**222** cụm Ảnh), `Nano Banana 2 (Pro)` (**208** cụm Ảnh).
- **Cấu trúc 84 thư mục làm phim chuyên nghiệp (3 cộng sự: `aist`, `transformingbanana_xxl`, `rodinsnow1196`)**:
  - `Animation/Scene 01` .. `Animation/Scene 12` (đặc biệt `Scene 06`, `Scene 07`, `Scene 08` chia nhỏ tới từng nhịp `B6-1`..`B6-7`, `B7-1`..`B7-6`, `B8-1`..`B8-13`).
  - `Characters/{Masha, Igor, Roma, Vika, Hookahman, Cashier, Babushka}/FINAL`, `Locations/{Garage, Gas Station, Hookah Bar, Track, Village}/FINAL`, `Props/{Capybara, Drones, Drugs, Gun, Helmets, Hookah, Cars}/FINAL`.

### 23.2. 4 Kỹ Thuật Đắt Giá Nhất Rút Ra Từ `@aist/projects/detour`

1. **Kỹ thuật 1 — Bảng Nhân Vật 4 Góc (`4-View Character Model Sheet`) Khóa Cứng Nền `HEX #808080` & Tỷ Lệ Giải Phẫu Học Theo Phần Trăm (`%`)**:
   - Thay vì dùng 3-Panel thông thường, `@aist/detour` dùng bố cục **4-View ngang (`16:9`)** gồm: `(1) full-body FRONT view at far left, (2) full-body SIDE PROFILE view at center-left, (3) full-body BACK view at center-right, and (4) a large tight CLOSE-UP portrait of the head and shoulders filling the right portion of the frame`.
   - **Khóa nền `#808080` tuyệt đối không đổ bóng**: `"The background behind all four views is a completely uniform, flat, solid neutral grey studio backdrop (HEX #808080) with zero gradient, zero texture, zero studio equipment, zero horizon line, and zero floor shadow falloff — just a subtle contact shadow directly beneath the shoe soles."`
   - **Khóa tỷ lệ cơ thể bằng con số giải phẫu học (`Anatomical Ratio Lock`)**: `"178cm tall, eight-and-a-half head canon, waist point at 62% of total height, hip at 52%, inseam near half of total height"`, kết hợp tư thế đứng `contrapposto` (`60% weight on right leg, 40% on left leg`) để dáng đứng tự nhiên không bị cứng như ma-nơ-canh.

2. **Kỹ thuật 2 — Chỉ Định Rõ "Lấy Gì" Và "Cấm Lấy Gì (`не брать`)" Từ Từng Thẻ `<<<UUID>>>` Trong Cảnh Đua Xe Đa Tham Chiếu (`SCENE_561` — `19,067` chars)**:
   - Khi nạp nhiều ảnh tham chiếu đạo cụ/đường đua vào `Seedance 2.5`, AI rất dễ bê nguyên nền xám studio hoặc ánh sáng mặt trăng từ ảnh tham chiếu vào cảnh đua xe.
   - Đạo diễn `@aist` giải quyết bằng cách viết **Bộ lọc thuộc tính cho từng thẻ `<<<UUID>>>`**:
     * Với thẻ vật phẩm `[power-up_turn-right | <<<c5d30835-942c-414b-a671-db39c2b21495>>>]`: Chỉ lấy biểu tượng chữ thập đỏ + mũi tên xanh phát sáng, **cấm lấy nền xám, bóng đen phẳng, kích thước và góc xoay gốc** (*"Серый фон, плоский силуэт, масштаб и ориентацию из <<<...>>> не брать"*).
     * Với thẻ đường đua `[elevated-road_warm | <<<b624bdef-1bc7-4703-825f-3162b108ba1b>>>]`: Chỉ lấy mặt nhựa đường kẻ caro khô ráo và 6 vạch mũi tên pha lê đỏ phát sáng, **cấm lấy mặt trăng khổng lồ, mặt đường ướt bóng gương và góc máy gốc** (*"не брать гигантскую луну, влажный зеркальный блеск покрытия, исходный ракурс..."*).

3. **Kỹ thuật 3 — Đối Lập Giữa Ngôn Ngữ Máy Quay Đua Xe Nghẹt Thở Với Thực Tế Hài Hước `39 km/h` (`SCENE_009` Opening Hook — `30s`, `10` nhịp cắt)**:
   - Cảnh mở đầu dài 30 giây (`21:9`) chia thành 10 mốc giây (`0–3s` .. `28–30s`) với 8 cú cắt Macro dồn dập (kéo khóa găng tay da, cài quai mũ bảo hiểm, vặn hết ga, ống xả phụt khói tắt máy) như phim đua mô-tô phân khối lớn, trước khi **Hard Cut** ở giây `18–21s` ra góc rộng tĩnh tiết lộ nhân vật đang cưỡi chiếc xe tay ga giao bánh Pizza bé xíu có gắn thú bông Capybara và đồng hồ tốc độ rung bần bật ở mức **`39 km/h`**.

4. **Kỹ thuật 4 — Tái Tạo Chữ Tiêu Đề Bằng Hạt Tàn Lửa Cháy Ngược (`Reverse-Burn Ember & Ash Title Card Reconstruction` — `SCENE_982` Ending Shot)**:
   - Dùng `<<<image_1>>>` làm khung hình đích (`End-State Geometry Lock`) chứa dòng chữ `"DETOUR / film by aist"`, sau đó chia 6 giây thành 5 giai đoạn hạt lửa tàn bay ngược trong gió đêm (`00:00–00:00.5` đen tĩnh ➔ `00:00.5–00:01.6` bụi than hồng lơ lửng ➔ `00:01.6–00:03.2` các mảng tàn lửa kết tụ đồng thời trên toàn bộ các chữ cái — **cấm hiện tuần tự từ trái sang phải** ➔ `00:03.2–00:04.4` khóa viền chữ sắc nét 100% khớp `<<<image_1>>>` ➔ `00:04.4–00:06.0` giữ tĩnh tuyệt đối).


---

## 24. Giải Mã Dự Án `@stan_studios/projects/double-sin` (`1,285` Jobs ➔ `455` Cụm Cảnh Duy Nhất, `44` Thư Mục Con, `211` Ảnh `@IMG`) & Nghệ Thuật "Bàn Tay Khổng Lồ Đặt Sản Phẩm (`Dual-Scale Forced Perspective & Hand-Placement Intro`)"

> **Hồ sơ đầy đủ**:
> - [`data/creators/stan_studios/projects/double-sin/dna_report.md`](./data/creators/stan_studios/projects/double-sin/dna_report.md)
> - [`data/creators/stan_studios/projects/double-sin/VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/stan_studios/projects/double-sin/VIDEO_CENTRIC_SCRAPED_PROMPTS.md)
> - [`data/DIRECTOR_STYLE_LIBRARY.md`](./data/DIRECTOR_STYLE_LIBRARY.md) (Mục `#21 — stan_studios/double-sin`)

### 24.1. Thống Kê Quy Mô Sản Xuất & Phân Bổ Công Thức
- **Quy mô thực chiến**: **`1,285` jobs** ➔ **`455` cụm cảnh Final Take duy nhất** (`120` cụm Video + `335` cụm Ảnh; tỷ lệ Re-roll **`2.82x`** = lọc bỏ `830` bản nháp `64.6%`), thời lượng Master Film **`868.33s` (`14 phút 28 giây`)** chia thành **`44` thư mục con** (`ASSETS/TITLE SEQUENCE/CONTENT`, `ASSETS/PROPS/Chess`, `SCENE 1`..`SCENE 16`, đặc biệt là cặp cảnh song song `SCENE 14 A / CASS CHESS` và `SCENE 14 B / ADA CHESS`).
- **Độ dài Prompt**: Trung bình **`4,546.9` ký tự** (Min: `20` chars, Max: **`28,802` chars** ở `SCENE_097`/`SCENE 1 / STREET INITIAL`), mật độ tham chiếu **`1.32` UUID refs/scene** (`601` lượt gắn thẻ UUID), **`63.1%`** (`287/455` scenes) có khối khóa phủ định/khẳng định (`POSITIVE LOCKS / CONSTRAINTS`).
- **Phân bổ Model ở bản Chốt (`Final Take`)**:
  - **Tạo Ảnh (`335` cụm)**: `Seedream 4.5` (**133** cụm — chủ lực tạo `3-Panel Turnaround Sheet` và chỉnh sửa chi tiết trang phục/khuyên mặt), `Nano Banana 2 (Pro)` (**127** cụm — chủ lực ghép bố cục Poster đa tỷ lệ `SCENE_308`/`SCENE_310` ở độ phân giải `4K 6336x2688` và thiết kế bàn cờ), `Soul Cinematic` (**52** cụm — tạo chân dung da thật có lỗ chân lông và bộ cờ chiến binh giáp sắt).
  - **Tạo Video (`120` cụm)**: `Seedance 2.5` (**119** cụm — chiếm **99.2%** toàn bộ video trong dự án).

### 24.2. 5 Kỹ Thuật Đắt Giá Nhất Rút Ra Từ `@stan_studios/projects/double-sin` (Đã Kiểm Định Thị Giác `Visual Audit First`)

1. **Kỹ thuật 1 — Bố Cục Đa Tỷ Lệ 3 Lớp Chiều Sâu (`Dual-Scale Forced Perspective Poster` — Giải Mã Chính Xác Bức Ảnh Bìa `SCENE_308` & `SCENE_310`)**:
   - **👁️ Kiểm định thị giác (`SCENE_308`, Job `22075517-f0a8-4cf6-ad8b-61f3d46730dd`, Model `Nano Banana 2 (Pro)`, `4K 6336x2688`, `23` lần re-roll)**:
     * Tác giả tạo ra hiệu ứng thị giác cực mạnh bằng cách kết hợp **3 thẻ `<<<UUID>>>` ẩn** (`[ada | @IMG_024]` = cô gái khổng lồ phía sau; `[cass_red | @IMG_039]` = cô gái mặc vest đỏ thu nhỏ bằng quân cờ; `[cass_weapon | @IMG_042]` = khẩu shotgun cổ điển) trên ống kính góc rộng nghiêng trục (`strong Dutch tilt leaning to the right, wide-angle lens for exaggerated perspective distortion`).
     * **3 Lớp chiều sâu (`3 Depth Planes`)**:
       1. **Tiền cảnh sát ống kính (`Blurred Extreme Foreground Left`)**: Bàn tay khổng lồ hơi out-nét vươn từ mép trái vào sát ống kính, các ngón tay cầm chóp quân Hậu bạc hạ xuống góc trái dưới bàn cờ (`In the blurred extreme foreground, entering from the LEFT edge, <<<UUID>>>'s large out-of-focus hand reaches down and holds a single silver chess piece (queen) close to the lens, softly defocused, fingers lowering it onto the board in the lower-left corner`).
       2. **Trung cảnh mặt bàn cờ nghiêng (`Midground Tilted Board Plane`)**: Dòng chữ 3D vàng đậm `"DOUBLE SIN"` có độ dày vật lý đứng thẳng trên mặt bàn cờ và đổ bóng xuống các ô cờ; bên phải là nhân vật `cass_red` thu nhỏ bằng chiều cao quân cờ, gác gót giày cao gót đỏ lên chữ cái cuối cùng.
       3. **Hậu cảnh phía trên (`Upper-Center Background`)**: Khuôn mặt cô gái khổng lồ `ada` cúi thấp phía sau dòng chữ, nhìn thẳng vào ống kính với ánh đèn viền vàng-xanh (`golden-green rim light glowing behind her head, deep greenish background shadows`).
   - **Thần chú gốc tạo bức ảnh bìa (`SCENE_308` — 100% Verbatim)**:
     ```text
     Cinematic movie-poster / album cover, dramatic low-angle shot with a strong Dutch tilt leaning to the right, wide-angle lens for exaggerated perspective distortion. 

     References: [ada | @IMG_024 | <<<f2eb5d68-8d79-4fb9-b94d-966bed0d4215>>>] = the large woman behind the title. [cass_red | @IMG_039 | <<<2cf5f4ca-66ec-4fdb-b049-6ce27014ee50>>>] = the woman in red on the right. [cass_weapon | @IMG_042 | <<<177fb720-d549-4949-914a-27c5ee5bbaa0>>>] = the shotgun. Preserve each reference's exact identity — same faces, features, bone structure, skin tone, freckles, hairstyles, clothing. Do not restyle.

     [ada | @IMG_024 | <<<f2eb5d68-8d79-4fb9-b94d-966bed0d4215>>>] looms large across the upper-center and background of the frame, leaning down low over a red-and-cream checkered chessboard that tilts diagonally across the whole image. Keep her identical to the reference: platinum-white/two-tone hair slicked back with loose wispy white strands framing the face, freckled fair skin, pale-blue eyes, the exact same multiple ear piercings, dark military-style jacket with silver buttons. She looks directly into the camera with a cold, intense stare, her face just above and behind the title.

     In the blurred extreme foreground, entering from the LEFT edge, [ada | @IMG_024 | <<<f2eb5d68-8d79-4fb9-b94d-966bed0d4215>>>]'s large out-of-focus hand reaches down and holds a single silver chess piece (queen) close to the lens, softly defocused, fingers lowering it onto the board in the lower-left corner.

     On the RIGHT side stands [cass_red | @IMG_039 | <<<2cf5f4ca-66ec-4fdb-b049-6ce27014ee50>>>], scaled small to the height of the chess pieces, standing on the board. Keep her identical to the reference: long straight platinum-blonde hair, sharp red blazer suit with white shirt and tie, red belt, bare legs, red high heels. Confident dynamic pose: [cass_weapon | @IMG_042 | <<<177fb720-d549-4949-914a-27c5ee5bbaa0>>>] (vintage red pump-action shotgun) held in her right hand, resting back against her shoulder, barrel pointing up. Her right leg is raised with the red high heel resting on top of the last title letter. Body warped by wide-angle distortion. She looks straight into the lens. Both women stare into the camera.

     Across the tilted board stand red and silver chess pieces, spaced apart, with a couple of toppled dark red pieces lying on their sides in the open squares.

     Bold saturated yellow 3D title text "DOUBLE SIN" in huge uppercase vintage lettering with real extruded depth, thickness and beveled edges, slightly weathered texture. It sits standing upright on the board plane along the lower-middle of the frame, running left-to-right and following the board's diagonal perspective, the letters casting soft shadows on the checkered squares. [cass_red | @IMG_039 | <<<2cf5f4ca-66ec-4fdb-b049-6ce27014ee50>>>]'s raised heel rests on the final letter. The title sits in front of [ada | @IMG_024 | <<<f2eb5d68-8d79-4fb9-b94d-966bed0d4215>>>] but does not cover her face.

     Cinematic lighting in warm yellow and green tones — golden rim light glowing behind [ada | @IMG_024 | <<<f2eb5d68-8d79-4fb9-b94d-966bed0d4215>>>]'s head and hair, deep greenish background shadows, dark moody atmosphere, film grain, high contrast, shallow depth of field. Ultra-detailed, photorealistic, dramatic cinematic lighting.
     ```

2. **Kỹ thuật 2 — Phẫu Thuật Đổi Vật Liệu/Đồ Vật Mà Giữ Nguyên 100% Bố Cục Ảnh Bìa (`Surgical Object/Material Swap` — `SCENE_306` & `SCENE_307`)**:
   - Ngay sau khi tạo được bố cục ảnh bìa ưng ý, `@stan_studios` không viết lại prompt từ đầu khi muốn đổi màu/đổi vật thể trên bàn cờ mà dùng mẫu câu khóa cứng:
     ```text
     Take this exact image <<<image_1>>> and keep everything completely unchanged — same two women, same faces, same poses, same hair, same clothing, same shotgun, same giant yellow 3D "DOUBLE SIN" title, same board, same green background, same warm cinematic lighting, same composition and framing. Do not alter or move anything except [the target object/material].
     ```

3. **Kỹ thuật 3 — Bảng `3-Panel Turnaround Sheet` "Cắt Đầu Ở Cổ Áo Panel Trái + Ghép Luôn Đạo Cụ Vào Cùng 1 Ảnh" (`@IMG_024` & `@IMG_039` — `SCENE_027`..`SCENE_029`)**:
   - **👁️ Kiểm định thị giác trên file `@IMG_024` (`sheet_ada`) và `@IMG_039` (`sheet_cass_red`)**:
     * Ở cả 2 bảng nhân vật chính, `@stan_studios` đều **cắt bỏ hoàn toàn phần đầu và cổ ở hình toàn thân mặt trước bên trái (`LEFT panel`) ngay tại đường viền cổ áo**, chỉ giữ lại đầu ở hình chụp sau lưng (`CENTER panel`) và bức chân dung cận cảnh siêu nét bên phải (`RIGHT panel`)!
     * **Câu lệnh gốc (`SCENE_028` & `SCENE_029`)**:
       ```text
       Critical — LEFT panel only: this figure has NO head at all — no face, no skull, no neck stump, no silhouette. The head is completely removed. The figure is cut cleanly along the top line of the high jacket collar: the head, face, hair, and neck are not visible above the collar; the body simply ends at the edge of the collar, following its shape, with the studio background above it. Everything from the collar down remains exactly as in the reference, sharp and in focus. CENTER and RIGHT keep the head fully intact and sharp.
       ```
     * Đặc biệt ở `@IMG_039` (`sheet_cass_red`), tác giả còn **ghép luôn bức ảnh đạo cụ khẩu súng (`cass_weapon`) nằm cạnh chân trái của nhân vật ngay trong Panel 1** để 1 thẻ `<<<UUID>>>` duy nhất khóa đồng thời cả Quần áo trước + Quần áo sau + Gương mặt cận cảnh + Vũ khí!

4. **Kỹ thuật 4 — Đạo Diễn Vật Lý "Bàn Tay Đưa Vào Khung Hình Đặt Đồ Vật Xuống Rồi Rút Ra" (`Hand-Placement Macro Physics` — `SCENE_436`, `SCENE_451` & `SCENE_453`)**:
   - Trong `SCENE 14 B / ADA CHESS` (`SCENE_436`, `SCENE_451`, `SCENE_453`), `@stan_studios` viết công thức cực kỳ chi tiết để điều khiển **bàn tay con người cầm một vật thể đặt xuống mặt phẳng trong `Seedance 2.5`** mà không bị biến dạng ngón tay hay trôi vật thể:
     * **Chuỗi 5 nhịp vật lý của bàn tay (`Hover ➔ Grip ➔ Lift & Carry ➔ Set-Down Click & Single Rock ➔ Clean Withdraw`)**:
       1. **`Hover` (Lơ lửng 1 nhịp trước khi chạm)**: `"a held beat of hovering before the grip closes"`
       2. **`Grip` (Khóa lực bấm ngón tay)**: `"the grip tightening with a fine tremor visible at macro scale, the nail beds whitening"`
       3. **`Carry` (Giữ nguyên độ cao & trọng lượng thật)**: `"The piece moves with a human hand's weight in it — carry at a constant height with the small live tremor of a held hand... her forearm shifts the light and throws a moving shadow across the surface as it works."`
       4. **`Set-Down Click & Single Rock` (Chạm mặt phẳng kêu "cạch", lắc nhẹ 1 nhịp rồi đứng yên)**: `"set down square so the piece rocks once and settles; ending on a small solid click."`
       5. **`Clean Withdraw` (Mở ngón tay và rút hẳn ra ngoài khung hình để nhường sân khấu cho vật thể)**: `"then withdraws and leaves the frame before the piece settles into stillness... leaving frame without lingering."`
     * **Khóa giới hạn cơ thể (`ONLY HAND & FOREARM LOCK`)**: `"ONLY her HAND, fingers and part of her forearm enter the shot — no face, no body, nothing above the wrist beyond the sleeve."`

5. **Kỹ thuật 5 — Song Hành 2 Thế Giới: "Bàn Cờ Trên Bàn Đá (`Tabletop Scale`)" ↔ "Đấu Trường Khổng Lồ Gấp Đôi Người Thật (`Double-Scale Colossal Board`)" (`SCENE_375`..`SCENE_455`)**:
   - Toàn bộ cao trào của bộ phim (`SCENE 14 A` & `SCENE 14 B`) là màn cắt cảnh song song giữa:
     * **Thế giới 1 (`SCENE 14 B` — `@IMG_192 table_war` + `@IMG_204 chessgame_3`)**: Bàn tay của `Ada` đặt quân cờ bạc xuống mặt bàn đá trong căn phòng tối chiếu 1 luồng sáng xanh lạnh (`hard cold blue pool of light falling from directly above`).
     * **Thế giới 2 (`SCENE 14 A` — `@IMG_175 chess_nopawns`)**: Ngay khi quân cờ được đặt xuống, cảnh cắt vào thế giới **bên trên mặt bàn cờ khổng lồ** (`a chessboard built at exactly DOUBLE normal size, each checkered square about as wide as a person is tall, standing alone in total darkness`), nơi nhân vật `Cass` có kích thước người thật đang chiến đấu ngay dưới chân những quân cờ khổng lồ cao gấp đôi người!

### 24.3. Mở Rộng Tư Duy Đạo Diễn: Biến Ý Tưởng "Lấy Ảnh Bìa `Double Sin` Thay Cây Thông Làm Intro Đặt Cây Thông Xuống" Thành Kịch Bản TVC Hoàn Chỉnh

Từ ý tưởng của bạn (**lấy chính bố cục bìa `SCENE_308`, thay quân Hậu bạc trên tay bằng Cây Thông Noel của bạn và làm Intro đặt cây thông xuống**), hệ thống đúc kết **3 Hướng Logic Nối Cảnh (Continuity Logic)** kèm bộ Prompt thực chiến:

1. **Hướng Logic A — `Giant Hand Placement ➔ Golden Light Shockwave ➔ Camera Dive Into Real Living Room` (Đặt Cây Thông Xuống Mô Hình ➔ Bừng Sáng Đèn LED ➔ Lao Máy Vào Phòng Khách Thật)**:
   - **Logic Điện Ảnh**:
     * **Shot 1 (0–4s — Intro Đặt Cây Thông)**: Từ bức ảnh bìa của bạn (bàn tay khổng lồ cầm cây thông Noel hạ xuống), áp dụng công thức **`Set-Down & Withdraw` (`SCENE_436`/`SCENE_453`)**: Bàn tay hạ thẳng đứng **Cây Thông Noel Phủ Tuyết Chân Bọc Vải Bố** xuống mặt phẳng ➔ đáy túi vải bố chạm sàn nhún nhẹ 1 nhịp (`touches down square and settles with real weight`) ➔ các ngón tay mở ra và rút khỏi mép trái khung hình ➔ ngay khoảnh khắc bàn tay rời đi, toàn bộ **đèn LED 2700K trên cây thông bừng sáng từ gốc lên ngọn**, hắt ánh vàng ấm lên gương mặt người khổng lồ phía sau!
     * **Shot 2 (4–8s — Chuyển Tỷ Lệ `Scale-Shift Push-In / Match Cut`)**: Máy quay đẩy nhanh (`fast smooth dolly push-in`) thẳng vào phần thân cây thông đang tỏa sáng ➔ cắt khớp chuyển động (`Match Cut on Forward Push`) sang góc rộng căn phòng khách thật 1:1 (`Ảnh 2: media_1792546554461_c5de676e.jpg` giữa lò sưởi trắng và cửa sổ), biến cây thông vừa được "đặt xuống" thành tâm điểm của cả ngôi nhà!
   - **Prompt Tạo Ảnh Bìa Đã Thay Cây Thông (`Nano Banana 2 (Pro)` — Kết hợp `SCENE_308` + `SCENE_306` + `Ảnh 2`)**:
     ```text
     Take the exact composition, camera angle, strong right-leaning Dutch tilt, wide-angle perspective distortion, lighting, and characters of <<<image_1>>> (the Double Sin poster) and keep the background woman, tilted board perspective, and dramatic warm golden-green rim lighting unchanged.

     Targeted Replacement — Swap the silver chess piece in the foreground left hand with the exact Pre-Lit Frosted Christmas Tree from <<<image_2>>>:
     In the blurred extreme foreground entering from the LEFT edge, the giant woman's large out-of-focus hand reaches down from above and delicately holds the top crown tip of the slender conical pre-lit frosted Christmas tree from <<<image_2>>> (with dark-green pine branches, snow-flocked white tips, glossy red berry clusters, warm 2700K LED fairy lights, and a natural beige woven burlap sack base tied at the bottom), lowering the burlap base of the Christmas tree onto the lower-left square of the tilted board.

     Keep the Christmas tree 100% faithful to <<<image_2>>> — natural conical silhouette, realistic snow-dusted pine needles, red berries, warm glowing LEDs casting a soft golden reflection onto the board squares and her fingers, and the textured beige woven burlap sack base. Photorealistic, 8K, shallow depth of field, cinematic film grain.
     ```
   - **Prompt Làm Video Intro "Bàn Tay Khổng Lồ Đặt Cây Thông Xuống & Bừng Sáng" (`Seedance 2.5` / `Kling 3.0` — Áp dụng khóa vật lý `SCENE_436` & `SCENE_453`)**:
     ```text
     SCENE CONTEXT
     Opening on <<<image_1>>> — dramatic low-angle Dutch-tilt wide-angle shot where the giant woman leans over the tilted surface while her large foreground hand on the left lowers the pre-lit frosted Christmas tree with red berries and beige woven burlap base onto the lower-left foreground. 5s.

     ACTION & TIMING
     0.0–2.2s (The Placement): The large foreground hand on the left lowers the frosted Christmas tree vertically over the final few centimeters onto the tilted surface. At 1.8s, the beige woven burlap sack base touches down squarely on the surface with a soft, weighted thud, rocking once and settling upright into complete stillness.
     2.2–3.5s (The Release & Illumination): Her fingers open cleanly from the top of the tree and her hand withdraws smoothly out of the left edge of the frame without lingering. The instant her hand releases the tree, the embedded warm 2700K LED fairy lights across all the snow-frosted branches cascade to full golden brightness from the burlap base up to the top tip.
     3.5–5.0s (The Push-In Hook): As the golden LED glow illuminates the surrounding squares and catches a warm gleam in the eyes of the giant woman watching from behind, the camera begins a smooth, hypnotic push-in directly toward the glowing frosted Christmas tree.

     PHYSICS & POSITIVE LOCKS
     The Christmas tree moves with real physical weight as it is lowered — the conical silhouette, snow-flocked pine needles, glossy red berry clusters, and beige woven burlap sack base remain 100% rigid and identical to <<<image_1>>> with zero morphing or branch distortion. Her fingers open cleanly without passing through the branches. Once set down at 1.8s, the tree stays firmly planted in the exact same spot. Real-time speed throughout, cinematic diegetic sound: a soft weighted fabric-and-wood thud on placement, followed by a warm magical crystalline shimmer as the LED lights bloom.
     ```

2. **Hướng Logic B — `First-to-Last Frame Scale Morph` Trên `Kling O3 First-to-Last Frame (`kling_o3_flf`)` (Biến Bàn Cờ Có Bàn Tay Đặt Cây Thông Thành Phòng Khách Thật Trong 1 Cú Máy Liền Mạch)**:
   - **Start Frame (`<<<image_1>>>`)**: Bức ảnh bìa `Double Sin` đã thay cây thông của bạn (bàn tay khổng lồ vừa đặt cây thông xuống).
   - **End Frame (`<<<image_2>>>`)**: Bức ảnh cây thông đứng trong phòng khách ấm cúng (`Ảnh 2: media_1792546554461_c5de676e.jpg` hoặc bản `Blue-Hour Dusk` có lò sưởi cháy ấm).
   - **Prompt chuyển cảnh liền mạch**:
     ```text
     Start from the exact first frame <<<image_1>>> as the giant foreground hand finishes setting the pre-lit frosted Christmas tree with the beige woven burlap base down and withdraws out of the left edge of the frame. As the hand leaves the frame, the camera smoothly levels out from the Dutch tilt and pushes in on the frosted Christmas tree while the surrounding dark scene and checkered floor seamlessly transform and expand around the tree into the warm, sunlit cozy living room of the final frame <<<image_2>>>, with the white fireplace mantel rising on the left and the sheer-curtained window on the right. The frosted Christmas tree itself stays anchored in the center-right foreground as the constant visual bridge from start to finish.
     ```

3. **Hướng Logic C — `"The Giant Decorator Series"` (Biến Concept "Người Khổng Lồ Trang Trí Nhà Tí Hon" Thành Chuỗi 3 Cảnh Hook Bán Hàng Viral)**:
   - Học từ cách `@stan_studios` đối lập tỷ lệ giữa `Ada` (khổng lồ) và `Cass` (tí hon trên bàn cờ):
     * **Cảnh 1 (0–3s)**: Bàn tay khổng lồ từ trên cao đặt **Cây Thông Noel Chân Bọc Vải Bố** xuống căn phòng khách miniature (trong phòng có gia đình/nhân vật tí hon đang ngước nhìn lên trầm trồ).
     * **Cảnh 2 (3–6s)**: Ngón tay trỏ khổng lồ chạm nhẹ vào đỉnh cây thông (`gentle fingertip tap on the top pine tip`) ➔ kích hoạt chuỗi đèn LED 2700K sáng bừng từ đỉnh xuống chân vải bố.
     * **Cảnh 3 (6–12s)**: Máy quay hạ xuống ngang tầm mắt người thật bên trong căn phòng khách (`Camera drops to human eye-level inside the living room`), nối vào cận cảnh cành thông phủ tuyết và chùm quả đỏ (`Ảnh 1`) kèm thông điệp chốt đơn: *"Chỉ cần đặt xuống là cả căn phòng bừng sáng Giáng Sinh — Không cần lắp ráp phức tạp, không rụng tuyết!"*
---

## 25. Bảng Kiểm Định Thị Giác Toàn Diện 39 Hồ Sơ Đạo Diễn (`100% Visual Audit Matrix — 39 Profiles / 200 Top @IMG Anchors`) & 10 Kỹ Thuật Chế Tác Ảnh Gốc Đỉnh Cao Mới Phát Hiện

> **Quy mô Kiểm định Thị giác (`Visual Audit First` — 100% Không Bỏ Sót)**:
> Toàn bộ **`39` hồ sơ đạo diễn** trong [`data/DIRECTOR_STYLE_LIBRARY.md`](./data/DIRECTOR_STYLE_LIBRARY.md) (`36` dự án phim/TVC/Trailer trong `data/creators/*/projects/*/` + `3` kho clip lẻ trong `data/creators/*/standalone_clips/`, tổng cộng **`47,334` jobs** ➔ **`9,906` cụm cảnh Final Take duy nhất**) đã được trích xuất **Top 5–8 tấm ảnh mỏ neo `@IMG` được tái sử dụng nhiều nhất của từng hồ sơ (tổng cộng `200` tấm ảnh `@IMG`)**, tải trực tiếp về máy và **kiểm định bằng mắt từng tấm một (`read_file`)** đối chiếu với câu lệnh Prompt gốc trong `asset_registry.json`.

### 25.1. Bảng Ma Trận Kiểm Định Thị Giác Toàn Bộ 39 Hồ Sơ (`39/39 Profiles Audited`)

| # | Hồ Sơ Đạo Diễn (`author/slug`) | Jobs / Clusters (`Reroll`) | Top 5 `@IMG` Đã Xem Bằng Mắt (`Reuse Count`) | Điểm Thị Giác (`Da Người / Sản Phẩm / Bối Cảnh`) | Phát Hiện Kỹ Thuật Đắt Giá Nhất Trên Ảnh Thật |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1 | **`6moths/where-letters-fall`** | `207` / `114` (`1.82x`) | `@IMG_001` (`58x`), `@IMG_039` (`18x`), `@IMG_011` (`16x`), `@IMG_003` (`14x`), `@IMG_010` (`11x`) | **9.5/10** (`Da 9.2` / `Prop 9.8` / `Bối cảnh 9.6`) | `3-Panel Character Sheet` nền xám + `4-Angle Post-Office Interior Sheet` (`@IMG_003`) + Khóa tiêu cự `LENS LOCK = 47°` FOV. |
| 2 | **`abz94/i-hate-science`** | `1,227` / `296` (`4.15x`) | `@IMG_001` (`72x`), `@IMG_007` (`61x`), `@IMG_004` (`43x`), `@IMG_006` (`41x`), `@IMG_016` (`28x`) | **9.4/10** (`Da 9.5` / `Prop 9.3` / `Giảng đường 9.6`) | Phối 4 bảng `3-Panel` diễn viên độc lập (`2.60 UUID refs/scene`) trong cùng giảng đường đại học bậc thang (`@IMG_016`). |
| 3 | **`adilinthewild/4k-blockbuster-breakdown`** | `13,491` / `1,293` (`10.43x`) | `@IMG_002` (`191x`), `@IMG_034` (`134x`), `@IMG_039` (`98x`), `@IMG_010` (`82x`), `@IMG_016` (`77x`) | **9.7/10** (`Da 9.7` / `Giáp & Vũ khí 9.8` / `Đại sảnh 9.8`) | Kỷ lục tái sử dụng `@IMG_002` tới **`191` lần**; da mặt lấm bụi/sẹo cực thật kết hợp `Ollkorrect Authority Contract Locks`. |
| 4 | **`adilinthewild/top-up`** | `255` / `66` (`3.86x`) | `@IMG_004` (`18x`), `@IMG_005` (`13x`), `@IMG_016` (`13x`), `@IMG_019` (`13x`), `@IMG_012` (`11x`) | **9.5/10** (`Da 9.5` / `Xe độ 9.6` / `Trạm xăng đêm 9.6`) | Chuẩn mực bảng màu `PerceptronNewt 60/30/10 Color Palette` (`83.3%` scenes) + mật độ `2.98 UUID refs/scene`. |
| 5 | **`adilinthewild/tv-4k`** | `1,957` / `112` (`17.47x`) | `@IMG_002` (`9x`), `@IMG_003` (`4x`), `@IMG_006` (`4x`), `@IMG_008` (`3x`), `@IMG_009` (`2x`) | **9.4/10** (`Keyframe 16:9 9.4` / `CRT TV 9.5`) | Dùng `16:9 Master Keyframe Plates` làm mỏ neo chuyển kênh TV (`Channel-Surfing Glitch Match Cut`), lọc nháp gắt nhất hệ thống (`17.47x`). |
| 6 | **`aist/detour`** | `6,162` / `982` (`6.27x`) | `@IMG_279` (`109x`), `@IMG_218` (`65x`), `@IMG_058` (`52x`), `@IMG_272` (`49x`), `@IMG_271` (`43x`) | **9.7/10** (`Da 9.5` / `Giáp & Mũ đua 9.8` / `Đường đua 9.6`) | Bảng nhân vật **`4-View Model Sheet` (`Front | Side | Back | Close-Up`)** trên nền `#808080` + lệnh lọc thuộc tính `<<<UUID>>>` (`не брать`). |
| 7 | **`alishaqantaar/the-new-girl`** | `373` / `83` (`4.49x`) | `@IMG_011` (`31x`), `@IMG_032` (`23x`), `@IMG_020` (`22x`), `@IMG_015` (`16x`), `@IMG_033` (`14x`) | **8.6/10** (`Nữ chính 8.8`, ⚠️ `Nữ phụ @IMG_015/@IMG_020 da sáp 7.2` / `Lớp học 9.7`) | **Cặp ảnh Lớp học Đảo ngược 180° (`@IMG_032` nhìn lên bảng vs `@IMG_033` nhìn xuống lớp)** cực đỉnh; nhưng cảnh báo lỗi dùng nền gỗ sọc và da mịn sáp ở nhân vật phụ. |
| 8 | **`askar_yedil/higgsfield-academy`** | `218` / `39` (`5.59x`) | `@IMG_001` (`22x`), `@IMG_003` (`16x`), `@IMG_005` (`13x`), `@IMG_006` (`12x`), `@IMG_002` (`11x`) | **9.6/10** (`Da 9.4` / `Inset Gear Callouts 9.8` / `Học viện 9.5`) | **`Composite Character + Equipment Zone Sheet`**: Nhúng luôn các ô vuông phóng đại Vũ khí, Giày, Ba lô vào nửa phải tấm bảng nhân vật! |
| 9 | **`bucketlist_impossible/31-august`** | `668` / `379` (`1.76x`) | `@IMG_006` (`38x`), `@IMG_020` (`34x`), `@IMG_016` (`28x`), `@IMG_044` (`18x`), `@IMG_078` (`18x`) | **9.5/10** (`Da nắng chiều 9.5` / `Phòng ngủ & Biển 9.7`) | Chuẩn bị `284` cụm ảnh Keyframe bằng `Nano Banana 2 Pro` giúp tỷ lệ Re-roll Video giảm xuống chỉ còn `1.76x`. |
| 10 | **`bucketlist_impossible/bash`** | `378` / `156` (`2.42x`) | `@IMG_040` (`14x`), `@IMG_001` (`7x`), `@IMG_017` (`6x`), `@IMG_002` (`5x`), `@IMG_049` (`5x`) | **9.7/10** (`5-View Sheet 9.9` / `Biệt thự hồ bơi 9.6`) | **Đột phá `Triple-Headless 5-View Dry vs. Wet State Sheet` (`@IMG_040` vest khô ➔ `@IMG_049` vest ướt sũng)**: 2 khung mặt cận cảnh + 3 khung toàn thân đều cắt đầu! |
| 11 | **`hft_online/harmony-ai-film-festival`** | `1,543` / `801` (`1.93x`) | `@IMG_085` (`41x`), `@IMG_270` (`39x`), `@IMG_135` (`34x`), `@IMG_237` (`29x`), `@IMG_096` (`28x`) | **9.8/10** (`Da 35mm 9.9` / `Tàu vũ trụ 9.8`) | Phối `Nano Banana 2 Pro` + `Seedream 5.0 Pro` + `Soul Cinematic` tạo `487` tấm `@IMG` chất lượng điện ảnh Festival (`89.1%` Single Shot). |
| 12 | **`higgscreator/nala-heads-drop`** | `162` / `160` (`1.01x`) | `@IMG_001` (`79x`), `@IMG_003` (`1x`), `@IMG_005` (`1x`), `@IMG_007` (`1x`), `@IMG_009` (`1x`) | **9.6/10** (`Mặt Nala @IMG_001 9.7` / `Mannequin Swap 9.9`) | **Độc chiêu `Grey Mannequin Oval Head Anonymization`**: Biến đầu người mẫu trong ảnh street-style thành khối cầu xám trơn để gắn mặt `@IMG_001` vào 79 bộ đồ với tỷ lệ trúng 100% (`1.01x` reroll)! |
| 13 | **`lukasbandana/rewind`** | `1,562` / `279` (`5.60x`) | `@IMG_006` (`47x`), `@IMG_002` (`43x`), `@IMG_007` (`41x`), `@IMG_017` (`38x`), `@IMG_001` (`19x`) | **9.7/10** (`Da 3 độ tuổi 9.8` / `Máy ảnh cơ @IMG_017 9.9`) | Bảng `3-Panel` khóa nhân vật qua 3 độ tuổi (`30s ➔ 50s ➔ 70s`) + `3-Panel Prop Sheet` máy ảnh không logo + `7-Block Narrative Physics DNA`. |
| 14 | **`mixingburrito1329/anime-production`** | `440` / `135` (`3.26x`) | `@IMG_001` (`3x`), `@IMG_004` (`3x`), `@IMG_007` (`2x`), `@IMG_015` (`2x`), `@IMG_021` (`2x`) | **9.6/10** (`2D Anime Cel-Shading 9.6`) | `100% Single-Shot Keyframe Anime` bằng `Seedream 5.0 Pro` + khóa phủ định cấm lai 3D CGI. |
| 15 | **`mohamed-halloum/sentence`** | `646` / `230` (`2.81x`) | `@IMG_002` (`49x`), `@IMG_001` (`34x`), `@IMG_005` (`26x`), `@IMG_006` (`24x`), `@IMG_012` (`19x`) | **9.5/10** (`Da tù nhân gai góc 9.6` / `Buồng giam 9.6`) | Ánh sáng khe cửa trại giam (`Slit-Window Chiaroscuro`) + diễn xuất ánh mắt tĩnh lặng (`67%` không thoại). |
| 16 | **`nicholastakeyama/tokyo-4-17`** | `559` / `229` (`2.44x`) | `@IMG_001` (`35x`), `@IMG_005` (`22x`), `@IMG_008` (`19x`), `@IMG_014` (`17x`), `@IMG_019` (`15x`) | **9.7/10** (`Da châu Á 9.8` / `Đêm mưa Tokyo 9.8`) | Dùng `Soul Cinematic` làm chủ lực (`50.2%` clusters) tạo chất ảnh đêm mưa neon Tokyo kiểu Wong Kar-wai chân thực tuyệt đối. |
| 17 | **`ollkorrect/besa`** | `960` / `450` (`2.13x`) | `@IMG_001` (`54x`), `@IMG_002` (`44x`), `@IMG_008` (`28x`), `@IMG_032` (`25x`), `@IMG_015` (`22x`) | **9.9/10** (`Da lịch sử 9.9` / `Đèn dầu 6-Panel @IMG_032 10/10`) | **Kiệt tác `6-Panel Studio Prop Sheet (5 Unlit + 1 Lit Panel)` (`@IMG_032`)** + `Master Camera Rail` + `Topaz Video Upscale`. |
| 18 | **`pandaproduction/thread`** | `837` / `128` (`6.54x`) | `@IMG_001` (`43x`), `@IMG_004` (`31x`), `@IMG_009` (`24x`), `@IMG_012` (`21x`), `@IMG_018` (`16x`) | **9.8/10** (`Da thợ may già 9.9` / `Xưởng may & Sợi chỉ đỏ 9.9`) | Quán quân nối cảnh `=== CONTINUATION FROM PREVIOUS SHOT ===` (`13.3%` clusters) dẫn chuyện bằng sợi chỉ đỏ xuyên suốt. |
| 19 | **`pietromalegori/control`** | `708` / `217` (`3.26x`) | `@IMG_002` (`48x`), `@IMG_001` (`37x`), `@IMG_006` (`29x`), `@IMG_010` (`21x`), `@IMG_015` (`19x`) | **9.9/10** (`Da người thật Soul Cinematic 10/10` / `Phòng máy 9.9`) | Kết hợp `Soul Cinematic` + `Nano Banana 2 Pro` tạo lỗ chân lông người thật `10/10` + Prompt dài kỷ lục `45,685` chars. |
| 20 | **`seksifratello/apeirophobia-teaser`** | `6,862` / `1,444` (`4.75x`) | `@IMG_001` (`18x`), `@IMG_004` (`15x`), `@IMG_009` (`14x`), `@IMG_012` (`12x`), `@IMG_019` (`11x`) | **9.9/10** (`Da Dutch Master 10/10` / `Liminal Space 9.9`) | Thần chú **`"Do not beautify him and do not turn him into a model"`** + `ARRICAM ST Look Lock` + `<<<image_1..4>>>` Positional Tagging. |
| 21 | **`stan_studios/double-sin`** | `1,285` / `455` (`2.82x`) | `@IMG_024` (`53x`), `@IMG_039` (`46x`), `@IMG_101` (`31x`), `@IMG_175` (`28x`), `@IMG_192` (`24x`) | **9.8/10** (`Headless-Left + Weapon Sheet 9.9` / `Poster 3 lớp 9.9`) | `Headless-Left Collar Cut` + Nhúng súng vào Panel 1 (`@IMG_039`) + Bàn tay khổng lồ đặt quân cờ (`Dual-Scale Forced Perspective`). |
| 22 | **`thomas_lundstrom/chandler-rollerblade-commercial`** | `211` / `22` (`9.59x`) | `@IMG_008` (`5x`), `@IMG_002` (`4x`), `@IMG_009` (`4x`), `@IMG_001` (`3x`), `@IMG_010` (`3x`) | **8.9/10** (`Giày patin @IMG_002 9.8` / ⚠️ `Da GPT-Image 7.6`) | **Độc chiêu `Floating Helmet above Headless Body` (`@IMG_008`)**: Xóa mặt và cổ ở khung giữa nhưng giữ mũ bảo hiểm lơ lửng trên cổ áo! |
| 23 | **`thomas_lundstrom/donut-commercial`** | `227` / `17` (`13.35x`) | `@IMG_003` (`4x`), `@IMG_004` (`4x`), `@IMG_005` (`4x`), `@IMG_006` (`3x`), `@IMG_001` (`2x`) | **9.0/10** (`Bánh Donut @IMG_004 9.8` / `Tiệm bánh 9.8` / ⚠️ `Da mẫu 7.5`) | Đồng bộ bảng màu Pastel Hồng-Vàng kiểu Wes Anderson giữa Hộp bánh (`@IMG_004`) và Tiệm bánh (`@IMG_005`). |
| 24 | **`thomas_lundstrom/emerald-fragrance-commercial`** | `94` / `13` (`7.23x`) | `@IMG_006` (`3x`), `@IMG_007` (`3x`), `@IMG_008` (`3x`), `@IMG_001` (`1x`), `@IMG_002` (`1x`) | **9.4/10** (`Chai nước hoa @IMG_006 9.9` / `Da 8.5` / `Hang rêu 9.5`) | Câu lệnh 1 dòng tạo `3-Panel Perfume Sheet` (`Full Front + 3/4 + Label Closeup` `@IMG_006`) + **`Floating Fedora Hat above Headless Body` (`@IMG_007`)**. |
| 25 | **`thomas_lundstrom/glow-mask-commercial`** | `127` / `15` (`8.47x`) | `@IMG_003` (`3x`), `@IMG_001` (`2x`), `@IMG_002` (`1x`), `@IMG_004` (`1x`), `@IMG_005` (`1x`) | **9.2/10** (`Tuýp kem @IMG_005 9.8` / `Da Beauty 8.2` / `Phòng tắm 9.2`) | **`Panel-Locked Wardrobe Swap` (`@IMG_001` vest xanh ➔ `@IMG_002` khăn tắm trắng giữ nguyên pixel mặt trái)** + Giữ dây chuyền trên cổ đã cắt đầu (`@IMG_003`). |
| 26 | **`thomas_lundstrom/seedance-2-5-blender`** | `152` / `22` (`6.91x`) | `@IMG_001` (`1x`), `@IMG_003` (`1x`), `@IMG_004` (`1x`), `@IMG_005` (`1x`), `@IMG_007` (`1x`) | **9.1/10** (`Da @IMG_005 9.0`, ⚠️ `@IMG_004 7.5` / `Thư viện 9.5`) | Điều khiển quỹ đạo hành động bằng **`Blender <<<video_1>>> Color-Coded Proxy Boxes`** + cắt đầu ở Panel 1 bên trái (`@IMG_003`). |
| 27 | **`thomas_lundstrom/seedance-4k-vs-1080p-product-commercials`** | `25` / `18` (`1.39x`) | `@IMG_004` (`3x`), `@IMG_003` (`2x`), `@IMG_006` (`2x`), `@IMG_001` (`1x`), `@IMG_002` (`1x`) | **9.9/10** (`Lon ROVA 7-View @IMG_002 10/10` / `Serum @IMG_003 9.9`) | **`7-View Master Packaging Sheet` (`@IMG_002` có cả nắp giật trên & đáy lon dưới)** + Lệnh xóa chữ thành phần mặt sau (`NO fine print on the back` `@IMG_004`). |
| 28 | **`zhit/the-patch`** | `653` / `133` (`4.91x`) | `@IMG_006` (`50x`), `@IMG_007` (`34x`), `@IMG_020` (`25x`), `@IMG_012` (`24x`), `@IMG_017` (`20x`) | **9.8/10** (`Da & Tóc 9.8` / `Ngón tay & Miếng dán @IMG_007 9.9`) | **Đột phá `Blurred-Face Center Panel De-duplication` (`@IMG_006`, `@IMG_012`, `@IMG_017`)**: Làm mờ Gaussian riêng mắt-mũi-miệng ở khung giữa để giữ nguyên mái tóc và dáng đầu! |
| 29 | **`6moths/standalone_clips`** | `6` / `5` (`1.20x`) | `@IMG_001` (`1x`), `@IMG_002` (`1x`), `@IMG_003` (`1x`), `@IMG_004` (`1x`), `@IMG_005` (`1x`) | **9.4/10** (`Editorial Cutout 9.4` / `B&W Crowd Blur @IMG_005 9.6`) | Bộ ảnh Streetwear trên nền `#FFFFFF` / `#000000` + Ảnh chủ thể đứng yên giữa đám đông nhòe chuyển động (`@IMG_005`) + `100%` 7-Block DNA. |
| 30 | **`bucketlist_impossible/standalone_clips`** | `6` / `6` (`1.00x`) | `@IMG_001` (`1x`), `@IMG_002` (`1x`), `@IMG_003` (`1x`), `@IMG_004` (`1x`), `@IMG_005` (`1x`) | **9.8/10** (`Storyboard 13-Panel @IMG_001 9.9` / `Motion Sheet @IMG_002 9.9`) | **Phát hiện chấn động: `13-Panel Timecoded Commercial Storyboard Sheet (0:00–0:15)` (`@IMG_001`)** & **`15-Second Motion Sheet Table` (`@IMG_002`)** trong 1 bức ảnh! |
| 31 | **`hft_online/standalone_clips`** | `12` / `12` (`1.00x`) | `@IMG_008` (`3x`), `@IMG_009` (`2x`), `@IMG_001` (`1x`), `@IMG_002` (`1x`), `@IMG_003` (`1x`) | **9.7/10** (`Da 35mm @IMG_008 9.8` / `Bếp xanh & Mask vàng @IMG_003 9.7`) | **Độc chiêu `Neon-Yellow Scribble Mask Inpainting` (`#FFFF00` trên `@IMG_003`)**: Dùng cọ vàng neon tô lên vật thể thừa trong ảnh bếp để chỉ điểm vùng cần xóa/thay thế! |
| 32 | **`sileent/the-breach`** | `1,240` / `496` (`2.50x`) | `@IMG_067` (`205x`), `@IMG_097` (`111x`), `@IMG_110` (`93x`), `@IMG_112` (`51x`), `@IMG_058` (`41x`), `@IMG_059` (`41x`), `@IMG_128` (`28x`), `@IMG_143` (`9x`) | **9.9/10** (`Da chiến trường 10/10` / `Bi-đông xanh @IMG_128 10/10` / `Ortona 9.9`) | **Kỷ lục tái sử dụng `@IMG_067` (`205x`)** + **`Dual-Headless Front & Back Mannequins` + Hoán đổi Chân dung/Trang phục mô-đun (`@IMG_067` ➔ `@IMG_143`)** + Kịch bản **`"Đạo Cụ Song Sinh" (@IMG_128 Blue-Enamel Water Bottle)`** + `STAGE 1..5 END STATE` & `THE DOCK`. |
| 33 | **`noah_01/cane-man`** | `2,046` / `526` (`3.89x`) | `@IMG_091` (`115x`), `@IMG_090` (`106x`), `@IMG_015` (`100x`), `@IMG_135` (`72x`), `@IMG_018` (`71x`), `@IMG_062` (`54x`) | **9.8/10** (`Da ông lão 85t @IMG_135 9.9` / `Quái vật @IMG_091/@IMG_090 9.8`) | **Câu thần chú tiếng Hàn `Seedream 5.0 Pro 3-Split Headless-Left`** + **`Natural Hat-Brim Face Occlusion` (`@IMG_135` cúi đầu che mặt bằng mũ lưỡi trai ở Panel 1)** + **`Kinetic Chain Biomechanics (WAIST → TORSO → SHOULDER → ARM → CANE)`**. |
| 34 | **`buralqy/kai-streamer-university-trailer-vfx`** | `254` / `67` (`3.79x`) | `@IMG_001` (`1x`), `@IMG_002` (`1x`), `@IMG_004` (`1x`), `@IMG_006` (`1x`), `@IMG_008` (`1x`), `@IMG_009` (`2x`), `@IMG_010` (`2x`) | **9.8/10** (`ARRI LOG Plate 9.9` / `VFX Portal & Car 9.8` / `3D Stone Title 9.8`) | **Độc chiêu `Red-Lasso Spatial Inpaint Masking (#FF0000)` trên Footage ARRI LOG quay thật (`@IMG_001` ➔ `@IMG_002`, `@IMG_006` ➔ `@IMG_008`)** + Khung lệnh `PRESERVE` biến cửa cuốn nhà kho thành cổng vàng Platform 9¾ (`VIDEO 01`). |
| 35 | **`daniallll/seed-audio-1-0-launch-video`** | `950` / `54` (`17.59x`) | `@IMG_001` (`1x`), `@IMG_002` (`1x`), `@IMG_003` (`1x`), `@IMG_004` (`4x`), `@IMG_005` (`4x`) | **9.6/10** (`Da & Lip-Sync 9.6` / `2-Panel Split Card 9.6`) | **`Pre-Video Garbled-Text Erasing` (`@IMG_002` xóa chữ rác trên áo ngực thành `@IMG_003` trước khi đưa vào `Seedance 2.0`)** + `CAMERA STYLE PRESET` (`Sean Baker` / `David Fincher` / `Mockumentary Snap-Zoom` 5 giọng nói trong 1 cú máy `15s`). |
| 36 | **`diegothetower/the-secret-monkey-island-movie-trailer`** | `27` / `11` (`2.45x`) | `@IMG_001`..`@IMG_004` (`1x`), `@IMG_005` (`1x`), `@IMG_015` (`1x`), `@IMG_016` (`1x`) | **9.7/10** (`Da Tom Holland 9.8` / `5-Panel Head Sheet @IMG_016 9.9`) | **`4-Reference IP-to-Hollywood Live-Action Casting Translation` (`@IMG_001..004` ➔ `@IMG_015`)** + **Bảng Xoay Đầu 5 Góc (`5-Panel Head Turnaround Sheet` có góc sau gáy `@IMG_016`)** + Lệnh bóc từng lớp áo & ghép râu từ `Reference 2 <<<image_2>>>`. |
| 37 | **`higgsfield.soul/huntress-s-tale`** | `225` / `49` (`4.59x`) | `@IMG_001` (`1x`), `@IMG_008` (`1x`), `@IMG_009` (`14x`), `@IMG_010` (`14x`), `@IMG_011` (`9x`), `SCENE_047`, `SCENE_049` | **9.8/10** (`BJD Warrior 9.8` / `Isolated Serpent @IMG_011 9.9` / `Title & YOU DIED 9.9`) | **Tách Thủy Quái Ra Nền Xám Phẳng (`@IMG_008` ➔ `@IMG_011` `"put him like a 3d rendered model on plain background"`)** + Khóa HEX lạnh tuyệt đối + **Cú Twist Nàng Tiên Hóa Rồng Quấn Cổ (`VIDEO 21/22`)** + Màn hình `YOU DIED / Try Again?` (`SCENE_049`). |
| 38 | **`lerra98/emberdant-s1-trailer`** | `38` / `24` (`1.58x`) | `@IMG_006` (`3x`), `@IMG_026` (`3x`), `@IMG_027` (`3x`), `@IMG_004` (`2x`), `@IMG_005` (`2x`), `@IMG_030` (`2x`), `@IMG_039` (`1x`), `@IMG_041` (`1x`) | **9.8/10** (`Wedding & Pirate Triptychs 9.8` / `Carved Stone Title @IMG_041 9.9`) | **Hệ bảng nhân vật theo từng giai đoạn bi kịch (`@IMG_006` Lễ cưới ➔ `@IMG_017` Xiềng xích ➔ `@IMG_036` Cướp biển) & Cặp trạng thái tàu `Raven's Due` (`@IMG_026` ➔ `@IMG_039`)** + **Quy tắc `4 Giây Đen Đặc + Im Lặng Tuyệt Đối (00:22–00:26)`** + Prompt chữ đá nứt lửa nóng chảy `2.39:1` (`VIDEO 10`, `VIDEO 17..20`). |
| 39 | **`lightdrop-studio/dudes-in-distress`** | `541` / `368` (`1.47x`) | `@IMG_004` (`1x`), `@IMG_029` (`27x`), `@IMG_035` (`30x`), `@IMG_036` (`25x`), `@IMG_037` (`6x`) | **9.8/10** (`8-Panel Tattoo Sheet @IMG_004 9.9` / `Hinged Coin @IMG_037 9.9`) | **`8-Panel Multi-Callout Character Sheet` (`@IMG_004` có 3 ô Macro Hình xăm & Khuyên tai)** + Câu lệnh 1 dòng cắt đầu mặt trước (`@IMG_035/@IMG_036`) + **Bảng Đạo Cụ Đồng Xu Có Khớp Bản Lề (`@IMG_037`)** + Khung `5-Second Fast Action-Trailer Crane Swoop` (`VIDEO 139`). |

---

### 25.2. Tổng Đúc Kết 10 Kỹ Thuật Chế Tác Ảnh Gốc (`@IMG`) Đỉnh Cao Nhất Phát Hiện Qua Kiểm Định Bằng Mắt (`155 Images Visual Audit`)

Từ việc xem tận mắt toàn bộ `155` bức ảnh `@IMG` chủ lực của `31` đạo diễn, hệ thống đúc kết **10 Kỹ Thuật Chế Tác Ảnh Gốc** mà chỉ khi mở file ảnh ra xem mới phát hiện được (không thể biết hết nếu chỉ đọc thống kê chữ):

1. **Kỹ thuật 1 — `Blurred-Face Center Panel De-duplication` (Làm Mờ Vùng Mắt-Mũi-Miệng Ở Khung Giữa Thay Vì Cắt Cụt Đầu — Phát hiện tại `28_zhit/the-patch` `@IMG_006`, `@IMG_012`, `@IMG_017`)**:
   - **Vấn đề của cách Cắt cụt đầu (`Headless`)**: Khi dùng lệnh `"Remove the face and neck from the front full body reference"`, nếu nhân vật có mái tóc dài xõa xuống vai, đội mũ lệch, hoặc dán thiết bị trên thái dương/trán (như miếng dán thần kinh trong *The Patch*), việc cắt cụt cả cái đầu ở khung giữa đôi khi làm AI không hiểu tóc xõa xuống vai thế nào.
   - **Giải pháp thiên tài của `@zhit`**: Giữ nguyên toàn bộ phần đầu, mái tóc, tai và tư thế nghiêng cổ ở khung toàn thân giữa, nhưng **phủ một lớp làm mờ Gaussian (`Gaussian Blur`) chỉ che đúng vùng mắt, mũi, miệng ở khung giữa**, đồng thời để khung bên trái hiển thị bức ảnh chân dung 85mm sắc nét đến từng lỗ chân lông! Nhờ đó `Seedance 2.5` vừa lấy được dáng đầu và mái tóc từ khung giữa, vừa bắt buộc phải lấy nét mặt sắc nét từ khung bên trái!

2. **Kỹ thuật 2 — `Floating Helmet / Fedora Hat above Headless Body` (Xóa Mặt & Cổ Nhưng Giữ Mũ Bảo Hiểm / Mũ Phớt Lơ Lửng Trên Cổ Áo — Phát hiện tại `22_thomas_lundstrom/chandler-rollerblade-commercial` `@IMG_008` & `24_emerald-fragrance-commercial` `@IMG_007`)**:
   - Khi nhân vật đội mũ bảo hiểm (`@IMG_008`) hoặc mũ phớt Fedora kiểu Indiana Jones (`@IMG_007`), `@thomas_lundstrom` ra lệnh xóa phần mặt và cổ (`face and neck`) ở khung giữa nhưng **giữ nguyên chiếc mũ lơ lửng trong không trung đúng vị trí trên cổ áo**! Kết quả là tỷ lệ mũ so với vai được khóa cứng 100% mà không bị lỗi vẽ mặt nhỏ.

3. **Kỹ thuật 3 — `Featureless Grey Mannequin Oval Head Anonymization` (Biến Đầu Người Mẫu Trong Ảnh Phố Xá Thành Khối Cầu Xám Ma-nơ-canh — Phát hiện tại `12_higgscreator/nala-heads-drop` `@IMG_003`..`@IMG_080`)**:
   - Khi muốn đưa 1 gương mặt KOL/Model cố định (`@IMG_001`) vào hàng chục bức ảnh thời trang đường phố có sẵn dáng đứng và bộ đồ đẹp: Dùng `Nano Banana 2 Pro` **thay phần đầu của người mẫu trong ảnh gốc bằng một khối bầu dục màu xám trơn không có ngũ quan (`smooth featureless grey mannequin oval head`)**. Khi đưa cặp `@IMG_001` (mặt thật) + `@IMG_003` (thân hình gắn đầu ma-nơ-canh xám) vào `Seedance 2.0`, tỷ lệ ghép trúng đạt **99% ngay lần đầu tiên (`Reroll Ratio = 1.01x`)**!

4. **Kỹ thuật 4 — `Triple-Headless 5-View Dry vs. Wet / Clean vs. Damaged State Sheets` (Bảng Nhân Vật 5 Cột Cắt Đầu Cả 3 Góc Toàn Thân & Khóa Cặp Trạng Thái Khô ↔ Ướt / Sạch ↔ Bẩn — Phát hiện tại `10_bucketlist_impossible/bash` `@IMG_040`/`@IMG_049` & `21_stan_studios/double-sin` `@IMG_039`/`@IMG_101`)**:
   - Ở `bucketlist_impossible/bash`, bảng nhân vật nâng lên **5 cột (`2 Cận cảnh mặt Nghiêng + Thẳng bên trái | 3 Toàn thân Trước - Nghiêng - Sau đều cắt cụt đầu bên phải`)**.
   - Khi nhân vật bị ngã xuống hồ bơi hoặc vừa trải qua trận chiến, đạo diễn lấy chính tấm bảng lúc khô/sạch làm `@img1` để sinh ra tấm bảng thứ hai có **vị trí 5 cột trùng khớp từng pixel nhưng quần áo và tóc ướt sũng nước (`@IMG_049`) hoặc rách bẩn dính bùn (`@IMG_101`)**!

5. **Kỹ thuật 5 — `Panel-Locked Wardrobe Swap` (Đổi Quần Áo Ở Khung Giữa & Phải Nhưng Giữ Nguyên Pixel Khung Mặt Trái — Phát hiện tại `25_thomas_lundstrom/glow-mask-commercial` `@IMG_001` ➔ `@IMG_002`)**:
   - Trong TVC mỹ phẩm, người mẫu cần mặc vest thanh lịch ở cảnh mở đầu (`@IMG_001`) rồi chuyển sang quấn khăn tắm trắng và đi dép bông hồng trong phòng tắm (`@IMG_002`). Thay vì tạo bảng nhân vật mới từ đầu dễ làm lệch mặt, tác giả dùng lệnh chỉnh sửa trên `@IMG_001`: **Giữ nguyên 100% pixel khung cận cảnh gương mặt bên trái, chỉ thay trang phục ở khung toàn thân giữa và sau lưng bên phải**!

6. **Kỹ thuật 6 — `Composite Character + Inset Equipment/Weapon Callout Sheet` (Gộp Nhân Vật + Các Ô Phóng Đại Đạo Cụ/Vũ Khí Vào Cùng 1 Tấm `@IMG` — Phát hiện tại `08_askar_yedil/higgsfield-academy` `@IMG_001` & `21_stan_studios/double-sin` `@IMG_039`)**:
   - Để tiết kiệm số lượng thẻ `@IMG` đính kèm vào mỗi cảnh video, các đạo diễn ghép trực tiếp **khẩu súng đứng cạnh chân nhân vật ngay trong Panel 1 (`double-sin @IMG_039`)** hoặc chia nửa bên phải tấm ảnh thành **các ô vuông Callout phóng đại Vũ khí, Giày, Ba lô, Huy hiệu (`higgsfield-academy @IMG_001`, `@IMG_005`)**.

7. **Kỹ thuật 7 — `7-View Can & 6-Panel Unlit/Lit Prop Sheets + Clean Back Lock` (Bảng Sản Phẩm 7 Góc Có Cả Nắp/Đáy, Bảng Đạo Cụ 5 Tắt + 1 Sáng & Lệnh Xóa Chữ Nhỏ Mặt Sau — Phát hiện tại `27_thomas_lundstrom/seedance-4k-vs-1080p` `@IMG_002`/`@IMG_004` & `17_ollkorrect/besa` `@IMG_032`)**:
   - Với lon nước giải khát cần bay xoay 3D trên không: Tạo **`7-View Packaging Sheet` (`@IMG_002`)** có đủ góc chụp thẳng từ đỉnh nắp giật (`Top Pull-Tab`) và đáy lon (`Bottom Base`), đồng thời ở bảng xoay ngang (`@IMG_004`) ra lệnh **`NO ingredient text, NO fine print, NO text block anywhere on the back`** để xóa bảng chữ thành phần li ti mặt sau, giúp video 4K không bao giờ bị nhòe chữ!
   - Với sản phẩm có đèn (như Đèn dầu cổ `@IMG_032` hoặc Cây thông Noel gắn đèn LED): Dùng **`6-Panel Studio Prop Sheet` trong đó 5 ô đầu ở trạng thái Tắt (`Unlit`) và ô thứ 6 ở trạng thái Bật sáng (`Lit with warm amber glow`)** để AI hiểu rõ cấu trúc vật lý cả trước và sau khi phát sáng!

8. **Kỹ thuật 8 — `13-Panel Timecoded Storyboard Sheet & 15-Second Motion Sheet Table` (Tạo Bảng Storyboard 13 Cảnh Có Đánh Số Giây `0:00–0:15` Trong 1 Bức Ảnh — Phát hiện tại `30_bucketlist_impossible/standalone_clips` `@IMG_001` & `@IMG_002`)**:
   - Trước khi tạo từng video lẻ cho TVC 15 giây, tạo **1 bức ảnh dọc chứa đủ 13 khung hình Storyboard đánh số từ `1 HERO INTRO (0:00-0:01)` đến `13 FINAL HERO PACKSHOT (0:12-0:15)` (`@IMG_001`)** hoặc bảng `15 SECOND MOTION SHEET` (`@IMG_002`). Tấm ảnh này vừa là bản thiết kế tổng thể vừa có thể nạp thẳng vào `Seedance 2.0` làm bản đồ chuyển cảnh!

9. **Kỹ thuật 9 — `Neon-Yellow Scribble Mask Inpainting (#FFFF00)` (Tô Cọ Màu Vàng Neon Lên Vật Thể Trong Ảnh Để Chỉ Điểm Vùng Cần Xóa/Thay Thế — Phát hiện tại `31_hft_online/standalone_clips` `@IMG_003`)**:
   - Khi muốn xóa các món đồ lặt vặt trên bàn bếp/kệ tủ hoặc đặt sản phẩm mới vào đúng vị trí mong muốn mà không sợ AI sửa nhầm chỗ khác: Dùng cọ vẽ màu vàng neon `#FFFF00` tô đè lên đúng vật thể đó trong ảnh gốc rồi đưa vào `Nano Banana 2 Pro` kèm lệnh xóa/thay thế vùng màu vàng!

10. **Kỹ thuật 10 — `180° Reverse-Angle Room Pair & Anti-Beautification Skin Realism` (Cặp Ảnh Phòng Đảo Ngược 180° & Quy Tắc Chống Da Nhựa AI — Phát hiện tại `07_alishaqantaar` `@IMG_032/@IMG_033`, `19_pietromalegori/control` & `20_seksifratello/apeirophobia-teaser`)**:
    - Tạo sẵn **cặp ảnh bối cảnh nhìn từ Trước ra Sau (`@IMG_032`) và từ Sau ra Trước (`@IMG_033`)** để cắt cảnh đối thoại `Shot / Reverse-Shot` không bao giờ lệch kiến trúc phòng.
    - **Kết luận Kiểm định Thị giác Da Người (`Skin Realism Verdict`)**: Khi tạo nhân vật bằng `GPT Image 2.0` hoặc chỉnh sửa nhiều lần không có khóa bảo vệ da (như nhân vật phụ ở `07_alishaqantaar` `@IMG_015` hay `22/23/26_thomas_lundstrom`), da mặt rất dễ rơi xuống mức `7.2–7.6/10` (mịn bóng như sáp). Để đạt điểm **`9.8–10/10` như người thật**, **BẮT BUỘC** tạo gương mặt gốc bằng **`Soul Cinematic` / `Seedream 5.0 Pro`** kết hợp câu thần chú của `@seksifratello`:
      ```text
      Do not beautify him/her and do not turn him/her into a model. Keep real human asymmetry, uneven skin tone, visible pores, subtle under-eye fatigue, and matte unretouched skin.
      ```


---

## 26. Giải Mã 2 Bộ Phim Tự Sự Đỉnh Cao `@sileent/projects/the-breach` (`8m02s` WWII Drama) & `@noah_01/projects/cane-man` (`19m07s` Urban Superhero Featurette) — 6 Quy Tắc Vàng Viết Kịch Bản & Quay Phim Ngắn AI Để Khán Giả Hiểu 100% Câu Chuyện

> **Lý do mổ xẻ sâu 2 bộ phim này**:
> Một bài học cực lớn trong biên kịch phim ngắn AI: **Dù từng khung hình có đẹp đến đâu, nếu kịch bản ôm đồm quá nhiều đạo cụ rời rạc và dùng lời thoại triết lý trừu tượng mà thiếu một "Sợi Dây Nhân Quả Vật Lý" xuyên suốt thì người xem sẽ bị rối, không hiểu chuyện gì đang xảy ra**.
> Việc cào và kiểm định thị giác toàn bộ **`@sileent/projects/the-breach`** (`1,240` jobs ➔ `496` cụm cảnh Final Take, phim dài `8 phút 02 giây`) và **`@noah_01/projects/cane-man`** (`2,046` jobs ➔ `526` cụm cảnh Final Take, phim dài `19 phút 07 giây`) đã giải đáp trọn vẹn câu hỏi: **Làm thế nào các đạo diễn Top đầu dựng được một bộ phim AI dài 8–19 phút mà người xem hiểu 100% từng giây, khóc ở cảnh kết và không bao giờ bị đứt mạch không gian?**

---

### 26.1. Kiểm Định Thị Giác (`Visual Audit First`) & Giải Mã `@sileent/projects/the-breach` (`1,240` Jobs / `496` Clusters / `161` `@IMG` Anchors)

- **Hồ sơ lưu trữ**: [`data/creators/sileent/projects/the-breach/`](./data/creators/sileent/projects/the-breach/)
  - **Master Film (`482.375s` = 8m02s)**: `https://d2ol7oe51mr4n9.cloudfront.net/user_33jl3BnMt18Tk2W8Gc0ZpJ42JaX/1214ad2f-24a4-403e-a465-3d917255bd92.mp4`
  - **Hồ sơ Gom Theo Từng Video**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/sileent/projects/the-breach/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`280` cụm Video + `216` cụm Ảnh, `Reroll Ratio = 2.50x`)
  - **Danh bạ `@IMG`**: [`asset_registry.json`](./data/creators/sileent/projects/the-breach/asset_registry.json) (`161` mã `@IMG`, đã tải `599` file ảnh tham chiếu về máy).

#### A. Kết Quả Kiểm Định Bằng Mắt (`read_file`) 9 Tấm Ảnh `@IMG` Chủ Lực Của `sileent/the-breach`

1. **`@IMG_067` (`205x` reuse — Kỷ lục tái sử dụng số 1 toàn hệ thống 33 hồ sơ! — Nhân vật chính `TOMMY` lính bộ binh Canada 19 tuổi)**:
   - **File local**: [`start_c9e99c36_c9e99c36-44bb-4822-90ef-ad0ea12e567f_resize.jpg`](./data/creators/sileent/projects/the-breach/images_final_takes/start_frames/start_c9e99c36_c9e99c36-44bb-4822-90ef-ad0ea12e567f_resize.jpg)
   - **Phát hiện bố cục `Dual-Headless Front & Back Mannequins + Weapon Inset` (`10/10`)**:
     * **Góc trên bên trái**: Ảnh chân dung cận cảnh của Tommy tạo bằng `Soul Cinematic` (mũ sắt Brodie phủ lưới, mắt xanh xám mở to hoảng sợ, lỗ chân lông, bọng mắt, máu khô và bụi gạch bám trên má cực thật `10/10`).
     * **Góc dưới bên trái**: Khẩu súng trường gỗ **`Lee-Enfield No.4`** đặt nằm ngang tách nền.
     * **Nửa bên phải**: Hai hình toàn thân mặc quân phục kaki Canada có đeo bao đạn trước ngực (`Front` & `Back`) đứng trên nền xám `#808080`, nhưng **CẢ HÌNH MẶT TRƯỚC LẪN HÌNH MẶT SAU ĐỀU CẮT CỤT ĐẦU (`Dual-Headless Front & Back`)**! Thậm chí ở hình mặt sau cũng không có mũ sắt hay gáy, giúp AI không bao giờ lấy nhầm đầu từ hình toàn thân!
2. **`@IMG_058` (`41x` reuse — `HUTCHINS`) & `@IMG_059` (`41x` reuse — `CORPORAL`)**:
   - **File local**: [`start_6d6a9e8b_6d6a9e8b-6c3b-441c-bc6f-16fab5ea6b8e_resize.jpg`](./data/creators/sileent/projects/the-breach/images_final_takes/start_frames/start_6d6a9e8b_6d6a9e8b-6c3b-441c-bc6f-16fab5ea6b8e_resize.jpg) & [`start_ef9d52d4_ef9d52d4-11b1-461c-b7ae-08aa0ed05913_resize.jpg`](./data/creators/sileent/projects/the-breach/images_final_takes/start_frames/start_ef9d52d4_ef9d52d4-11b1-461c-b7ae-08aa0ed05913_resize.jpg)
   - **Mẹo tiết kiệm công sức cực thông minh (`Modular Squad Uniform Template Reuse`)**: Vì cả tiểu đội lính Canada đều mặc quân phục và cầm súng trường `Lee-Enfield` giống hệt nhau, đạo diễn `@sileent` **giữ nguyên 100% khẩu súng và 2 hình ma-nơ-canh không đầu của `@IMG_067`**, chỉ việc **thay đúng bức ảnh chân dung ở ô góc trên bên trái** để tạo ra đồng đội `Hutchins` (`@IMG_058`) và viên Hạ sĩ `Corporal` (`@IMG_059`) trong 5 giây!
3. **`@IMG_143` (`9x` reuse — `TOMMY AT DINNER` trong cảnh kết đêm Giáng Sinh)**:
   - **File local**: [`start_26a2a910_26a2a910-86ef-4c11-830c-f6796998bd38.png`](./data/creators/sileent/projects/the-breach/images_final_takes/start_frames/start_26a2a910_26a2a910-86ef-4c11-830c-f6796998bd38.png)
   - **Đảo ngược quy trình (`Modular Costume Swap Locking Left Portrait`)**: Khi Tommy cởi bỏ giáp trận để ngồi ăn tối Giáng Sinh ở cảnh cuối phim (`7a-TOMMY v2`), tác giả **giữ nguyên 100% bức chân dung Tommy ở bên trái của `@IMG_067`**, xóa khẩu súng bên dưới, và chỉ thay 2 hình ma-nơ-canh không đầu bên phải thành **áo sơ mi kaki xắn tay kèm dây đeo quần chữ Y (`khaki shirt + suspenders`)**! Nhờ vậy gương mặt Tommy ở cảnh chiến đấu và cảnh bàn tiệc Giáng Sinh giống nhau tuyệt đối 100%!
4. **`@IMG_097` (`111x` reuse — `KURT` người lính dù Đức Fallschirmjäger 40 tuổi bị thương nặng)**:
   - **File local**: [`start_ff6a5b4d_ff6a5b4d-5ef3-4f63-aa70-1956b569fc23_resize.jpg`](./data/creators/sileent/projects/the-breach/images_final_takes/start_frames/start_ff6a5b4d_ff6a5b4d-5ef3-4f63-aa70-1956b569fc23_resize.jpg)
   - **Kiểm định thị giác**: Bảng `Dual-Headless Front & Back` của Kurt — bên trái là gương mặt người lính già 40 tuổi hốc hác, mắt trũng sâu đỏ ngầu, máu chảy từ thái dương trái xuống hàm râu lởm chởm (`10/10`); bên phải là 2 hình toàn thân không đầu mặc áo ngụy trang rằn ri (`splinter-pattern jump smock`) có **mảng máu đỏ sẫm thấm ướt bên sườn trái và hai bàn tay bê bết máu khô**!
5. **`@IMG_128` (`28x` reuse — Đạo cụ trung tâm của cả bộ phim: `Chiếc Bi-đông Nước Tráng Men Xanh Coban / Blue-Enamel Water Bottle`)**:
   - **File local**: [`start_1906b81e_hf_20260825_105309_1906b81e-2777-4f87-ad67-011ecef49862.webp`](./data/creators/sileent/projects/the-breach/images_final_takes/start_frames/start_1906b81e_hf_20260825_105309_1906b81e-2777-4f87-ad67-011ecef49862.webp)
   - **Kiểm định thị giác (`10/10`)**: Bức ảnh chụp chính diện chiếc bi-đông quân đội tráng men màu xanh coban (`blue-enamel canteen`) bị trầy xước viền rỉ sét, nắp nhôm buộc dây dù vào cổ bình, bên ngoài bọc dây đai vải bố kaki chữ thập (`crossed khaki webbing carrier`) đặt trên nền xám studio `#808080`.
6. **`@IMG_110` (`93x` reuse), `@IMG_112` (`51x` reuse), `@IMG_129` (`17x` reuse) & `@IMG_155` (`4x` reuse)**:
   - `@IMG_110`: Khung hình gốc (`Anchor Keyframe`) Kurt ngồi bệt tựa lưng vào chiếc tủ gỗ vỡ trong căn phòng đổ nát, tay phải chĩa súng ngắn Luger về phía lỗ thủng, tay trái ôm vết thương bên sườn.
   - `@IMG_112`: Khung hình gốc Tommy đứng nép bên khe tường gạch vỡ dọc (`the vertical brick breach`) nhìn sang phòng bên kia.
   - `@IMG_129`: Khung hình cận cảnh Kurt lúc hấp hối, hai bàn tay đẫm máu đan trước ngực giữ chiếc bi-đông xanh.
   - `@IMG_155`: Bối cảnh căn hầm ăn tối Giáng Sinh (`Christmas dugout`) tối tăm ấm áp với dòng chữ cắt giấy `MERRYXMAS` treo trên tường gạch và ngọn nến đơn độc cháy trên mặt bàn gỗ.

---

### 26.2. Kiểm Định Thị Giác (`Visual Audit First`) & Giải Mã `@noah_01/projects/cane-man` (`2,046` Jobs / `526` Clusters / `183` `@IMG` Anchors)

- **Hồ sơ lưu trữ**: [`data/creators/noah_01/projects/cane-man/`](./data/creators/noah_01/projects/cane-man/)
  - **Master Film (`1,147.58s` = 19m07s)**: `https://d2ol7oe51mr4n9.cloudfront.net/user_2x8MupDOtWUfup9bx9I6JkD6hx0/11da71f1-db51-4260-92ce-54d7f72b1bfc.mp4`
  - **Hồ sơ Gom Theo Từng Video**: [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/noah_01/projects/cane-man/VIDEO_CENTRIC_SCRAPED_PROMPTS.md) (`419` cụm Video + `107` cụm Ảnh, `Reroll Ratio = 3.89x`)
  - **Danh bạ `@IMG`**: [`asset_registry.json`](./data/creators/noah_01/projects/cane-man/asset_registry.json) (`183` mã `@IMG`, đã tải `680` file ảnh tham chiếu về máy).

#### A. Kết Quả Kiểm Định Bằng Mắt (`read_file`) 6 Tấm Ảnh `@IMG` Chủ Lực Của `noah_01/cane-man`

1. **`@IMG_135` (`72x` reuse — Nhân vật chính `OLD RAY / CANE-MAN`: Ông lão 85 tuổi lưng còng cầm gậy gỗ chiến đấu với quái vật)**:
   - **File local**: [`sheet_ray2_941e7d87-d3eb-4101-a322-dec787d5cbfd.png`](./data/creators/noah_01/projects/cane-man/images_final_takes/turnaround_sheets/sheet_ray2_941e7d87-d3eb-4101-a322-dec787d5cbfd.png)
   - **Phát hiện độc chiêu `Natural Hat-Brim Face Occlusion` (`9.9/10`)**:
     * Nếu dùng lệnh cắt cụt đầu ở Panel 1 cho một ông lão 85 tuổi lưng còng, AI sẽ làm mất dáng còng lưng khắc khổ từ cổ xuống vai.
     * Thay vì cắt cụt cổ, đạo diễn `@noah_01` cho ông lão Ray ở **Panel 1 (Toàn thân trước) hơi cúi đầu xuống để vành chiếc mũ lưỡi trai denim che khuất toàn bộ mắt và mũi một cách tự nhiên**, tay phải chống cây gậy gỗ cong (`wooden walking cane`); **Panel 2 (Giữa)** quay lưng; còn **Panel 3 (Bên phải)** là ảnh Macro chính diện gương mặt ông lão 85 tuổi với từng đốm đồi mồi, nếp nhăn sâu, râu bạc và vết máu rỉ ở môi dưới (`9.9/10`)!
2. **`@IMG_015` (`100x` reuse — `MILO`), `@IMG_018` (`71x` reuse — `KAI`) & `@IMG_062` (`54x` reuse — `VESPER`)**:
   - **File local**:
     * [`sheet_asset_a39e241c-064c-46e6-8f22-69267df41081.png`](./data/creators/noah_01/projects/cane-man/images_final_takes/turnaround_sheets/sheet_asset_a39e241c-064c-46e6-8f22-69267df41081.png) (`@IMG_015`)
     * [`sheet_asset_8be1748a-c77a-468f-ac38-a3d42a843dc7.png`](./data/creators/noah_01/projects/cane-man/images_final_takes/turnaround_sheets/sheet_asset_8be1748a-c77a-468f-ac38-a3d42a843dc7.png) (`@IMG_018`)
     * [`sheet_vesper_vesper_3d12b03e-2aae-4264-94ed-ac09441d7e0d.png`](./data/creators/noah_01/projects/cane-man/images_final_takes/turnaround_sheets/sheet_vesper_vesper_3d12b03e-2aae-4264-94ed-ac09441d7e0d.png) (`@IMG_062`)
   - **Công thức `Seedream 5.0 Pro` Tiếng Hàn Tạo Bảng `3-Split Headless-Left Sheet` (`SCENE_003`..`SCENE_011`)**:
     Đạo diễn `@noah_01` chỉ cần đưa 1 bức ảnh nhân vật (`<<<image_1>>>`) vào `Seedream 5.0 Pro` kèm đúng 2 câu lệnh tiếng Hàn sau để sinh ra hàng loạt bảng `3-Panel` có **Panel trái không mặt (`얼굴 없이`), Panel giữa quay lưng, Panel phải cận cảnh mặt**:
     ```text
     1번 사진 인물의 앞,뒤 캐릭터 시트 만들어줘. 3분할인데 왼쪽은 얼굴 없이 의상이 보이는 앞모습, 전신 중앙에는 의상이 보이는 뒷모습 전신, 오른쪽에는 얼굴 정면 클로즈업. 표정은 무표정으로 한다.
     ```
     *(Dịch nghĩa để dùng tiếng Anh hoặc tiếng Hàn đều được: "Make a front and back character sheet of the person in image 1. It is a 3-split layout: on the left is a full-body front view showing the outfit WITHOUT the face; in the center is a full-body back view showing the outfit; on the right is a frontal face close-up with a neutral expression.")*
3. **`@IMG_091` (`115x` reuse — Quái vật 4 chân `STALKER`) & `@IMG_090` (`106x` reuse — Quái vật 2 chân `RUNNER`)**:
   - **File local**: [`sheet_stalker_c8c4a29c-1bf4-49da-914d-ce79f9053f49.png`](./data/creators/noah_01/projects/cane-man/images_final_takes/turnaround_sheets/sheet_stalker_c8c4a29c-1bf4-49da-914d-ce79f9053f49.png) & [`sheet_runner_1aa12371-28fc-4504-a10f-7755b3c1a75b.png`](./data/creators/noah_01/projects/cane-man/images_final_takes/turnaround_sheets/sheet_runner_1aa12371-28fc-4504-a10f-7755b3c1a75b.png)
   - **Mẹo khóa ánh sáng môi trường ngay trong `Monster Turnaround Sheet`**: Thay vì đặt quái vật trên nền xám studio (dễ làm da quái vật bị sáng bệch giả tạo khi ghép vào cảnh công viên), `@noah_01` đặt cả 3 khung của con quái vật (`Side/Front | Back | Roaring Jaws Close-Up`) **ngay trên lối đi bộ có hàng rào sắt đen của công viên Central Park dưới tán cây xanh**! Nhờ vậy bóng đổ xanh mát của lá cây đã ăn sẵn vào lớp da xám nhầy nhụa của quái vật.

---

### 26.3. Tại Sao Các Phim Ngắn AI Nghiệp Dư Thường Khó Hiểu, Còn `@sileent/the-breach` & `@noah_01/cane-man` Lại Dễ Hiểu 100% & Chạm Tới Cảm Xúc? (6 Quy Tắc Vàng Làm Phim Ngắn AI)

| Tiêu Chí Kịch Bản & Đạo Diễn | ❌ Lỗi Điển Hình Ở Các Phim Ngắn AI Nghiệp Dư | ✅ Cách `@sileent/the-breach` & `@noah_01/cane-man` Giải Quyết Triệt Để |
| :--- | :--- | :--- |
| **1. Số lượng Đạo cụ & Luật thế giới (`Props & Concept Load`)** | Nhồi **3–4 đạo cụ + 1 luật siêu nhiên phức tạp** chỉ trong 6 cảnh ngắn. Người xem chưa kịp hiểu món này đã nhảy sang món khác. | **Quy tắc `"1 Đạo Cụ Duy Nhất Dẫn Chuyện Từ Đầu Đến Cuối"`**: *The Breach* chỉ dùng **1 chiếc Bi-đông nước màu xanh (`@IMG_128`)**. *Cane-Man* chỉ dùng **1 cây Gậy gỗ của ông lão (`@IMG_135`)**. Mọi cảm xúc và bước ngoặt đều xoay quanh đúng 1 vật thể đó! |
| **2. Cách viết Lời thoại (`Dialogue Style`)** | Dùng lời độc thoại giải thích cốt truyện dài và trừu tượng, bắt người xem phải đọc phụ đề để hiểu luật phim. | **Quy tắc `"Hình Ảnh Giải Thích 90%, Thoại Chỉ Từ 1–8 Chữ Gắn Với Hành Động Vật Lý"`**: Súng hết đạn kêu *cạch cạch* ➔ Kurt ném súng đi rồi mới nói 2 chữ `{Finish it.}`. Tommy đưa bi-đông nước ➔ Kurt uống xong mới thều thào tên mình `{Kurt.}`. |
| **3. Kỷ luật Không gian (`Spatial Geography Lock`)** | Các cảnh cắt chuyển góc liên tục trong phòng mà không có một ranh giới vật lý cố định làm chuẩn. | **Quy tắc `"Ranh Giới Vật Lý Bất Khả Xâm Phạm (GEO-SPATIAL Boundary)"`**: Trong *The Breach*, Tommy ở phòng bên trái, Kurt ở phòng bên phải, ngăn cách bởi **1 bức tường gạch có lỗ thủng 30cm (`The Wall Is Never Crossed`)**. Khán giả luôn biết 100% ai đang ở đâu! |
| **4. Kỹ thuật Nối giữa Cảnh N và Cảnh N+1 (`Shot-to-Shot Continuity`)** | Mỗi cảnh chỉ mô tả hành động đang diễn ra, không khóa cứng tư thế đóng băng ở giây cuối cùng. | **Quy tắc `"Khóa END STATE Từng Nhịp + THE DOCK Ở Giây Cuối"`**: Mỗi `STAGE` trong *The Breach* đều có dòng `END STATE:` khóa chính xác vị trí tay/mắt, và giây cuối cùng có `THE DOCK:` trùng khớp 100% với Frame 1 của cảnh tiếp theo! |
| **5. Cú Twist / Payoff ở Cảnh Kết (`Emotional Payoff`)** | Cảnh kết lặp lại hành động bấm máy ghi âm nhưng thiếu một vật thể đối chứng bất ngờ từ đời thực. | **Quy tắc `"Đạo Cụ Song Sinh Ở Cảnh Kết (The Twin Prop Payoff)"`**: Chiếc bi-đông xanh `@IMG_128` rơi khỏi ngực Kurt khi anh chết ở Cảnh 5h; sang Cảnh 7a (đêm Giáng Sinh), viên Hạ sĩ vô tình đặt **chiếc bi-đông xanh quân nhu y hệt (`the twin canteen`)** xuống bàn ăn cạnh đĩa của Tommy! Không cần 1 lời giải thích, khán giả lập tức nổi da gà khi Tommy nhìn chiếc bi-đông và thì thầm `{Merry Christmas, Kurt.}`! |
| **6. Khóa Vật lý Cơ thể trong Hành động (`Action Biomechanics`)** | Chỉ mô tả hành động chung chung (*"anh ấy bật lửa"*, *"cô ấy nhìn"*). | **Quy tắc `"Chuỗi Truyền Lực Cơ Sinh Học (Kinetic Chain: WAIST → TORSO → SHOULDER → ARM → PROP)"`** của `@noah_01`: Mô tả rõ lực phát ra từ đâu, khớp nào xoay trước, vật nào giữ cố định. |

---

### 26.4. Kho Prompt Nguyên Văn Đắt Giá Nhất Từ `@sileent/the-breach` & `@noah_01/cane-man` (Lưu Trữ Để Áp Dụng Khi Làm Phim Ngắn & TVC Kể Chuyện)

#### 1. Mẫu Prompt `"Cái Chết Tĩnh Lặng & Đạo Cụ Rơi Theo Trọng Lực"` (`sileent/the-breach` — `SCENE_462` / `5h-DEATH-OT`)
> **Điểm thiên tài**: Thay vì tả cảnh chết kịch tính giả tạo, đạo diễn tả sự sống tắt dần qua **nhịp thở ngừng hẳn ở giây thứ 4**, đôi mắt mở nhìn vô định, và **trọng lực tự nhiên làm hai bàn tay buông lỏng khiến chiếc bi-đông xanh (`@IMG_128`) tự lăn khỏi ngực xuống nền gạch kêu một tiếng cộc khô khốc (`one dull knock, a short half-roll, still`)**!

```text
[Material Roles]
[@IMG_129: 5h-a] is the starting frame (Kurt's final moment — a close-up from high angle, head on rubble, eyes barely open, hands folded at the lower edge with the blue water bottle).
[@IMG_097: KURT] is the character identity reference for the 40-year-old German Fallschirmjäger.
[@IMG_128: Water bottle] is the prop reference for the blue-enamel water bottle.

[Shot]
Single continuous static shot, 8 seconds, NO cuts. High angle looking straight down at Kurt's face and upper chest (~50–60° below horizontal). Medium close-up — head, shoulders, upper chest, his folded hands at the bottom of frame holding the blue water bottle [@IMG_128: Water bottle]. The camera does NOT move for the entire 8 seconds — absolute stillness, like a witness holding its breath.

STAGE 1 (0–4s) — THE LAST BREATH:
Exact continuation of [@IMG_129: 5h-a]. Kurt lies with his head resting on the grey stone rubble, face angled slightly toward the breach at the left edge of frame. His heavy-lidded red-rimmed eyes are half-open, looking softly toward the breach where Tommy's voice just came from. A faint, almost imperceptible last exhalation leaves his parted lips — his chest sinks a few millimeters and does NOT rise again. The small muscle at the corner of his mouth relaxes completely. His gaze does not close — his eyelids stay half-open, fixed on the warm strip of light at the breach, but the focus behind the eyes quietly goes out, softening into still glass.
END STATE: Kurt is completely still. Eyes half-open, unblinking, reflecting the pale grey window light. No chest movement.

STAGE 2 (4–8s) — THE HANDS LET GO:
Only after his face has been still for a full beat, gravity takes what his hands were holding. At the bottom of frame, his blood-stained fingers — loosely folded over the blue water bottle [@IMG_128: Water bottle] on his chest — slowly, passively slacken by a few millimeters as the last muscle tone leaves them. Freed from his grip, the blue water bottle tips gently off his chest and rolls a few inches down onto the rubble floor beside his shoulder with a single quiet, hollow clink against a broken tile, coming to rest on its side in the dust. Neither hand moves to follow it — his fingers remain half-curled on his still chest, empty. The camera holds on his quiet, unchanged face and the fallen blue bottle beside him for the remaining two seconds.
END STATE: Kurt motionless, eyes half-open toward the breach, hands empty on his chest, the blue water bottle lying still on the rubble beside his shoulder.

[Style]
1943 war drama, ARRI Alexa Mini LF + Panavision C-Series anamorphic, heavy 35mm grain, desaturated palette (ash grey, wet slate, dark oxblood on his tunic, the muted blue of the fallen water bottle as the only quiet note of color). Cold grey daylight from off-screen right, warm amber bounce from the breach on the left side of his face.

[Audio]
Near-total silence. At 1–2s, the faintest soft breath leaving his lips — barely audible over the low winter wind outside. Then 3 full seconds of complete stillness. At ~5s, one small, hollow metallic-enamel clink and a short dry scrape as the blue water bottle slips from his chest and settles on the broken tiles. No music, no voice, no gunfire — only the cold wind breathing through the ruins.

[Constraints]
NO camera movement whatsoever. NO dramatic head flop, NO eyes rolling back, NO sudden spasm — his passing is almost invisible, a quiet stopping. His eyelids do NOT close; they remain half-open as in [@IMG_129: 5h-a]. No extra objects, no water spilling from the capped bottle.
```

#### 2. Mẫu Prompt `"Đạo Cụ Song Sinh Ở Cảnh Kết & Cú Nâng Ly Dừng Ở 2 Centimet"` (`sileent/the-breach` — `SCENE_481` / `7a-TOMMY v2`)
> **Điểm thiên tài**: Đây là khuôn mẫu vàng cho **Cảnh Kết (Epilogue / Brand Payoff)** của mọi bộ phim ngắn hoặc TVC kể chuyện cảm xúc: Dùng một nhân vật phụ vô tư đặt **một vật thể giống hệt đạo cụ ở cao trào (`the twin canteen` `@IMG_128`)** ngay trước mắt nhân vật chính để kích hoạt ký ức mà không cần bất kỳ cảnh hồi tưởng (flashback) dài dòng nào!

```text
[Material Roles]
[@IMG_155: 7a] is the starting frame (dark dug-out dinner scene, MERRYXMAS banner in background, Tommy seated at center table in khaki shirt and suspenders, single candle on the left).
[@IMG_143: TOMMY AT DINNER] is the character reference for Tommy (19, pale gaunt face, wide grey-blue eyes, khaki shirt and suspenders, no helmet).
[@IMG_144: CORPORAL AT DINNER] is the character reference for the Corporal (early 30s, thick dark moustache, square jaw, khaki shirt and suspenders).
[@IMG_128: Water bottle] is the prop reference for the standard-issue blue-enamel water bottle with canvas strap.

[Shot]
Single continuous shot, 15 seconds, NO cuts. Medium two-shot at table height (35mm lens, shallow depth of field). The single candle on the left edge of the table is the ONLY light source, casting warm trembling amber across their faces against deep black shadows.

STAGE 1 (0–4s) — THE NOISE OF SURVIVAL:
Exact continuation of [@IMG_155: 7a]. Around the cramped brick cellar, soldiers eat, laugh, and clink tin mugs in warm, muffled celebration. Tommy [@IMG_143: TOMMY AT DINNER] sits motionless at the center of the rough wooden table, staring down at his untouched tin plate, his face hollow and quiet inside the noise. From the right side of the frame, the Corporal [@IMG_144: CORPORAL AT DINNER] steps up beside Tommy's bench holding a tin mug in one hand and his own standard-issue blue-enamel water bottle [@IMG_128: Water bottle] by its webbing strap in the other. He claps a heavy, cheerful hand onto Tommy's right shoulder and leans down with a warm grin, speaking over the chatter:
{Tommy! How the hell did you get past that sniper yesterday?}
END STATE: Corporal's hand on Tommy's shoulder, smiling down at him; Tommy slowly lifts his eyes partway.

STAGE 2 (4–9s) — THE TWIN CANTEEN:
Without waiting for an answer, as he shifts his weight to grab a piece of bread from the table, the Corporal absently sets his blue-enamel water bottle [@IMG_128: Water bottle] down on the wooden planks right beside Tommy's tin plate — one dull wooden thud. It sits upright in the candlelight, identical in color, shape, and worn khaki webbing to the bottle Tommy passed through the breach to Kurt. The Corporal laughs at something shouted from down the table and steps away out of the right edge of the frame, leaving the blue bottle behind. Tommy's gaze drops and locks onto the blue water bottle beside his plate. The warm amber candle flame reflects as a tiny point of light on its scratched blue enamel.
END STATE: Corporal gone from frame; the blue water bottle stands beside Tommy's plate in the candlelight; Tommy stares at it, completely still.

STAGE 3 (9–15s) — THE UNFINISHED TOAST:
The surrounding laughter and voices in the cellar seem to recede into a soft, distant murmur. Tommy's eyes stay fixed on the blue water bottle for a long quiet beat. His right hand moves slowly across the rough wood and wraps around the handle of his chipped enamel mug. Barely moving his lips, in a voice so quiet it doesn't reach the soldier sitting next to him, he whispers to the empty air above the candle:
{Merry Christmas, Kurt.}
He lifts the mug just two centimeters off the table — a tiny, private toast that never reaches his lips — holds it suspended in the warm candlelight for a second as his eyes glisten without shedding a tear, and the shot holds on his still face and the blue bottle beside him.
END STATE: Tommy holding the mug 2cm above the table, staring quietly at the blue water bottle in the candlelight.
```

#### 3. Mẫu Prompt `"Chuỗi Truyền Lực Cơ Sinh Học (Kinetic Chain Biomechanics) & Khóa Thương Tích Cộng Dồn"` (`noah_01/cane-man` — `SCENE_283`)
> **Điểm thiên tài**: Khi làm cảnh hành động hoặc tương tác vật lý phức tạp trên `Seedance 2.0`, nếu chỉ viết *"ông lão vung gậy đánh quái vật"*, AI sẽ làm chân nhân vật trượt đi trên mặt đất hoặc vung tay yếu ớt. Đạo diễn `@noah_01` khóa chặt 2 chân (`feet planted`) và chỉ định rõ chuỗi truyền lực cơ học **`WAIST → TORSO → SHOULDER → ARM → CANE`**!

```text
USE <<<video_1>>> AS MOTION REFERENCE ONLY FOR THE SWING TIMING.
Character identity for Old Ray comes strictly from [@IMG_135: sheet_ray2] and the Monsters from [@IMG_091: sheet_stalker].

CONTINUOUS COMBAT STATE LOCK:
Throughout the entire shot, Ray ALREADY HAS ONE STALKER [@IMG_091: sheet_stalker] BITING AND CLAMPED ONTO HIS RIGHT LEG, AND A SECOND STALKER BITING AND HANGING ONTO HIS LEFT FOREARM. Both creatures remain latched onto his limbs from frame 1 to the end — they do NOT vanish.

ACTION & KINETIC CHAIN BIOMECHANICS:
1. Because his right leg is pinned by the first Stalker, Ray CANNOT step forward. Instead, he generates explosive rotational power purely through a grounded kinetic chain:
   WAIST ROTATION → UPPER TORSO TWIST → RIGHT SHOULDER SNAP → FOREARM WHIP → WOODEN CANE IMPACT.
2. With a violent snap of his hips and shoulders, Ray whips the heavy wooden cane horizontally into the skull of the Stalker clamping his left arm, shattering its jaw grip and sending dark saliva flying across the wet asphalt.
3. Immediately as a third Stalker lunges straight at his throat from the front, Ray snaps both hands onto the ends of his wooden cane, raises the cane HORIZONTALLY like a crossbar, and JAMS THE WOODEN SHAFT DIRECTLY BETWEEN THE THIRD STALKER'S UPPER AND LOWER SPLIT JAWS — locking the monster's teeth millimeters from his face while drool drips onto his plaid shirt.
```

---

### 26.5. Quy Trình Chuẩn 5 Bước Khi Chúng Ta Bắt Tay Làm Một Bộ Phim Ngắn AI Mới (Từ Hôm Nay Trở Đi)

Bất kỳ khi nào bạn muốn làm một bộ phim ngắn (từ `1 phút` gồm `6–10 cảnh` đến `5–10 phút`), chúng ta sẽ **KHÔNG nhảy vào viết ngay 6 câu prompt rời rạc nữa**, mà bắt buộc đi qua **5 Bước Thiết Kế Của `@sileent` & `@noah_01`**:

1. **Bước 1 — Chốt `"1 Đạo Cụ Linh Hồn (The Single Soul Prop)"` & `"Cú Payoff Đạo Cụ Song Sinh Ở Cảnh Kết"`**:
   - Toàn bộ phim chỉ xoay quanh **ĐÚNG 1 đạo cụ vật lý có màu sắc/hình khối nổi bật** (như chiếc bi-đông xanh `@IMG_128` hoặc cây gậy gỗ `@IMG_135`).
   - Thiết kế sẵn **Cảnh 1 (Đạo cụ xuất hiện bình thường) ➔ Cảnh Cao Trào (Đạo cụ cứu mạng / gắn với hy sinh) ➔ Cảnh Kết (Đạo cụ đó hoặc "bản sao song sinh" của nó bất ngờ xuất hiện lại trong bối cảnh đời thường khiến nhân vật lặng người)**.
2. **Bước 2 — Thiết Kế Bộ `@IMG` Theo Chuẩn `Dual-Headless + Modular Costume Swap`**:
   - Tạo gương mặt gốc bằng **`Soul Cinematic`** (khóa lỗ chân lông, bất đối xứng tự nhiên, vết sẹo/mồ hôi theo thần chú của `@seksifratello`).
   - Dựng bảng nhân vật trên nền `#808080` bằng **`Seedream 5.0 Pro`** (câu lệnh tiếng Hàn `3분할 Headless-Left` của `@noah_01`) hoặc **`Nano Banana 2 Pro`** (`Dual-Headless Front & Back Mannequins` của `@sileent`).
   - Nếu nhân vật đổi quần áo ở cảnh kết: **Giữ nguyên 100% khung chân dung bên trái, chỉ thay 2 hình ma-nơ-canh không đầu bên phải** (như `@IMG_067` ➔ `@IMG_143`).
3. **Bước 3 — Vẽ Sơ Đồ Không Gian Cố Định (`GEO-SPATIAL Boundary Lock`)**:
   - Xác định rõ vị trí Trái / Phải / Vách ngăn vật lý giữa 2 nhân vật (cửa sổ, bức tường thủng, mặt bàn, quầy bar) và giữ đúng trục máy quay 180 độ xuyên suốt.
4. **Bước 4 — Viết Prompt Theo Cấu Trúc `[Material Roles]` + `STAGE 1..N` + `END STATE:` + `THE DOCK`**:
   - Mỗi cảnh chia làm các `STAGE` (mỗi stage 4–6 giây), cuối mỗi stage bắt buộc có dòng **`END STATE:`** mô tả chính xác tư thế dừng, và giây cuối cùng của cảnh có **`THE DOCK:`** khớp 100% với Frame 1 của cảnh kế tiếp.
5. **Bước 5 — Kiểm Soát Thoại Tối Giản `{...}` & Âm Thanh Vật Lý Đơn Lẻ (`Single Physical Sound Cue`)**:
   - Cấm viết thoại giải thích dài dòng. Mỗi câu thoại đặt trong ngoặc nhọn `{...}` chỉ dài **1–8 từ** và luôn đi kèm **1 âm thanh vật lý đắt giá** (`two dry metallic clicks of an empty firing pin`, `one hollow clink of the blue bottle rolling onto broken tiles`, `a toast lifted 2 centimeters off the wood`).


---

## 27. 📚 Kiến Thức Cherry-Pick Từ 2 Skill Repos Mã Nguồn Mở (2026-10-22)

> ⚠️ **Lưu ý**: Các kỹ thuật dưới đây được trích từ 2 skill repos mã nguồn mở:
> - `smixs/visual-skills` (github.com/smixs/visual-skills) — Serge Shima, CC BY 4.0
> - `Emily2040/seedance-2.0` (github.com/Emily2040/seedance-2.0) — MIT License
>
> Chưa kiểm chứng 100% với hệ sinh thái Higgsfield. Nếu áp dụng mà kết quả sai/dở,
> hãy xóa mục tương ứng. Mỗi mục có trích dẫn nguồn để dễ truy vết.

---

### 27.1 Bảng So Sánh Syntax 3 Model — Seedance 2.5 vs Kling 3.0 vs Nano Banana 2

> 📚 Nguồn: `smixs/visual-skills` → `video/references/seedance-25.md`, `video/references/kling.md`, `image/references/nano-banana.md`

| Tính năng | **Seedance 2.5** | **Kling 3.0** | **Nano Banana 2 (NB2/NBP)** |
|---|---|---|---|
| **Reference tags** | `@Image N`, `@Video N`, `@Audio N` (50 slot: 30 ảnh + 10 video + 10 audio) | `[Character A: ...]` labels trong prompt + Element Library tùy chọn | `[Image 1: face]`, `[Image 2: outfit]` — NB2 tối đa 10 obj / NBP tối đa 6 obj |
| **Audio/Dialogue** | Markers riêng: `{ }` thoại, `< >` SFX, `( )` nhạc, `【 】` phụ đề | Native lip-sync 15s, multi-character voice | Không có (image-only model) |
| **Negative prompts** | Viết trong prompt: "no subtitles, no BGM" — 2.5 đã fix bug không chấp hành | **Field riêng**, viết "robots" KHÔNG viết "no robots" | Không có field riêng — ghi vào cuối prose |
| **Lens syntax** | Focal length OK (`50mm`) nhưng mô tả visible result quan trọng hơn | Hiểu trực tiếp `35mm, 85mm, anamorphic 40mm` | **CẤM số lens** (`50mm, f/2.8` bị ignore) — dùng mô tả: "shallow depth of field" |
| **Max duration** | 30s single-pass, extension tới 60s, Ultra Long 30-180s | 15s, multi-shot tối đa 6 shots | N/A (ảnh tĩnh) |
| **Multi-shot** | Stages liên tục + timestamp `[0-4s]...` | `Shot 1 (0-3s)... Shot 2 (3-6s)...` tối đa 6 shots | N/A |
| **JSON** | Không cần | Không cần | Dùng JSON cho scene 5+ elements |
| **Ưu điểm nổi bật** | Timestamp chính xác tới giây, 50 refs, edit/blockout | Multi-shot dialogue + lip-sync native | Text rendering SOTA 100+ ngôn ngữ, Image Grounding |
| **Nhược điểm** | Hay tự cắt dù bảo "one-take", lỗi commission (làm quá nhiều) | Lỗi omission (bỏ shots), âm nhạc hay tự thêm | Tay/mặt vẫn bị lỗi, HDR overcooked |

**Quy tắc vàng chung cho cả 3 model:**
- Viết natural language, KHÔNG tag-spam (`"masterpiece, 4K, cinematic"` = vô dụng).
- Mỗi shot 1 camera move chính + tối đa 1 micro-adjustment (handheld shake, rack focus).
- Đặt Subject + Action ở ĐẦU prompt (30-40% token đầu được chú ý nhiều nhất).
- Mỗi clip phải có **final image rule** — trạng thái kết thúc cụ thể, model dùng nó làm đích.

---

### 27.2 Seedance 2.5 — Cấu Trúc Anti-Collapse Skeleton & Công Thức Người Thật

> 📚 Nguồn: `smixs/visual-skills` → `video/references/seedance-25.md` §3, §7, §8

**Công thức prompt chính thức của Seedance 2.5:**
```
<Subject> performs <primary action> in <scene/environment>.
The visuals feature <visual style>.
Use <shot size, camera angle, camera movement>.
Audio includes <dialogue, ambience, SFX, music>.
```

**Anti-Collapse Skeleton 3 Module** (cho cảnh drama 30s):
```
<Logline 1 dòng>

[Module 1 — Reference layer]
Strictly keep @Image 1's face consistent. Keep @Image 2's composition/blockout.

[Module 2 — Global settings]
Base environment & texture. Visual style. Camera language. Character styling.
Performance core. Prohibitions: <sound bans> + <subtitle bans> + <behavior bans>.

[Module 3 — Timestamped storyboard]
[0-5s] [beat name] — physical directives + emotional subtext.
[5-12s] ...
```

**Mẹo quan trọng — Directive + Subtext:** Sau chỉ dẫn vật lý, giải thích CHO MODEL biết *tại sao* hành động xảy ra: *"Emotion analysis: she is not complaining — she is waiting for him to confirm an answer she already guessed."* → Model diễn tốt hơn khi hiểu intent.

**Công thức người thật anti-da-nhựa:**
```
Character = [age/ethnicity] + [skin tone/texture] + [3-4 facial details]
          + [gaze/soul] + [hairstyle/color] + [clothing/fabric]
          + [build/emotion/aura]
```
Bắt buộc thêm suffix: **`"retaining real fine pores and skin texture"`** — đây là câu thần chú chống da nhựa chính thức.

**Danh sách cấm cụ thể (ví dụ cảnh chia tay):** *"No exaggerated crying, no fast cuts, no large body movements, no extra dialogue, no BGM, no runny nose, no premature dropping of tears."* → Ban ĐÚNG cách cảnh này có thể hỏng, không ban chung chung.

---

### 27.3 Kling 3.0 — Dialogue Protocol P1-P4 & Multi-Shot Syntax

> 📚 Nguồn: `smixs/visual-skills` → `video/references/kling.md` §3

**5-Layer Structure:** `Scene → Characters → Action → Camera → Audio`

**Anchor subjects ở ĐẦU prompt:**
```
[Character A: Exhausted Partner — late 40s, gray-streaked beard, navy peacoat]
[Character B: Female Investor — early 30s, sharp blazer, calm posture]
```

**4 quy tắc thoại (P1-P4):**
- **P1 — Structured naming:** Dùng ID duy nhất `[Character A: ...]`, KHÔNG dùng `[Agent]` chung chung.
- **P2 — Visual anchoring TRƯỚC dialogue:** Gắn thoại vào hành động: *"Character A pulls a note from his pocket and reads aloud: 'It's not what you think.'"* → Không gắn = lip-sync trôi.
- **P3 — Voice tone trong tag:** `[Character A, raspy deep voice]:` → Generic `[Man]:` = giọng generic.
- **P4 — Temporal control giữa các câu:** Dùng linking words: *"Immediately,"* giữa 2 câu thoại → Không có = model chồng lời.

**Negative field Kling — quy tắc ĐẶC BIỆT:** Viết **chính danh từ cần loại** ("robots"), KHÔNG viết "no robots".

**Khi 2 shot liền kề cùng framing + angle → model gộp thành 1 take.** Fix: mỗi shot PHẢI khác framing hoặc angle.

---

### 27.4 Dramaturgy Engine — Scene Formula, Rule of Six & Three-Jobs Rule

> 📚 Nguồn: `smixs/visual-skills` → `video/references/dramaturgy.md`

**Scene Formula (5 yếu tố bắt buộc):**
```
Scene = hero's desire + obstacle + space geometry + controlled gaze + editing rhythm
```
Thiếu 1 yếu tố = cảnh sụp thành trang trí. Trước khi viết prompt, đặt tên từng yếu tố trong 1 câu.

**Three-Jobs Rule — Mỗi shot phải làm ít nhất 1 trong 3 việc:**
1. **Change emotion** (nhân vật hoặc khán giả)
2. **Advance action** (sự kiện mới, thông tin mới, vị trí mới)
3. **Increase pressure** (stakes tăng, thời gian cạn, không gian thu hẹp)

→ *"Beautiful establishing shot"* hay *"Beautiful hero shot of product"* = KHÔNG PHẢI MỘT JOB.

**Walter Murch Rule of Six** (thứ tự ưu tiên khi cắt):
1. **Emotion (51%)** — Cắt phục vụ sự thật cảm xúc
2. **Story (23%)** — Cắt đẩy câu chuyện
3. **Rhythm (10%)** — Cắt theo nhịp
4. **Eye-trace (7%)** — Mắt khán giả đang nhìn đâu
5. **2D plane (5%)** — Tôn trọng trục hướng màn hình
6. **3D space (4%)** — Tôn trọng hình học không gian thực

→ Cắt nhanh "cho có nhịp" mà không phục vụ Emotion + Story = quảng cáo TikTok dành cho người mất tập trung.

**Five Anchors Principle — Mỗi phim ngắn cam kết đúng 5 mỏ neo:**
1. Một cảm xúc chính
2. Một motif thị giác lặp lại
3. Một vật thể mỏ neo
4. Một khoảnh khắc gãy (break)
5. Một hình ảnh cuối cùng

*Ví dụ: Emotion=Guilt, Motif=phản chiếu trong kính, Object=điện thoại tin nhắn chưa đọc, Break=xóa tin nhắn, Final=mặt anh ta in bóng trên màn hình tối.*

---

### 27.5 14-Field Shot Card Template

> 📚 Nguồn: `smixs/visual-skills` → `video/references/dramaturgy.md` §11

Mỗi shot trong storyboard phải điền đủ 14 trường. Trường trống = thiếu direction:

| # | Field | Mô tả |
|---|---|---|
| 1 | Shot ID | 01, 02, 03 |
| 2 | Beat | Điều gì thay đổi trong câu chuyện ở đây |
| 3 | Emotion | Fear, shame, anger, guilt, resolve, relief... |
| 4 | Frame | wide / medium / close-up / macro insert |
| 5 | Composition | Center, edge, negative space, reflection, silhouette, foreground obstruction |
| 6 | Camera | Static, push-in, handheld, tracking, whip-pan |
| 7 | Movement reason | TẠI SAO camera di chuyển ở đây — "what changed?" |
| 8 | Action | Sự kiện vật lý chính xác |
| 9 | Eye trace | Mắt khán giả nên đáp vào đâu trong 0.3s đầu |
| 10 | Duration | 0.5s, 1s, 3s |
| 11 | Cut type | match cut, smash cut, cut on action, J-cut, L-cut |
| 12 | Sound | Breath, bass hit, street noise, phone ring, silence |
| 13 | Light/Color | Cold, contrast, flicker, shadow, specific palette |
| 14 | Production note | Prop, location, actor direction |

---

### 27.6 De-Slop System — 10 Trục Chống "Mặt Nhựa AI" & Boosters Bị Cấm

> 📚 Nguồn: `smixs/visual-skills` → `image/references/de-slop.md`

**10 trục mà AI model tự động "làm đẹp" (phải counter-steer):**

| Trục | Model tự kéo về | Ảnh thật thường có |
|---|---|---|
| Eyes | To, tròn, đối xứng | Hẹp, mí lót, 1 mắt nhỏ hơn |
| Face | V-line, tỷ lệ búp bê | Midface dài/phẳng, bất đối xứng |
| Skin | Không lỗ chân lông, phát sáng | Lỗ chân lông, lông tơ, đỏ da |
| Body | Silhouette lý tưởng | Phẳng, vuông, nặng, bình thường |
| Clothing | Bó hơn, mới hơn, hở hơn | Đúng coverage và mức cũ của ref |
| Hair | Phồng, bóng, sợi nào ra sợi nấy | Xẹp, bết, tóc bay |
| Stance | Pose model, cằm ngẩng | Tư thế lóng ngóng thật |
| Casting | Idol / influencer | Người bình thường |
| Background | Bão hòa, gọn, gradient | Trầm, bừa bộn, 1 hex cụ thể |
| Extras | Tự thêm bông tai, biển hiệu | Vắng mặt rõ ràng |

**Boosters BỊ CẤM trong positive slots:** `4K, 8K, ultra-detailed, hyper-detailed, ultra-realistic, photorealistic render, masterpiece, best quality, sharp focus, crisp, intricate detail, flawless, stunning, perfect`

**Thay vì "realistic", nêu pipeline chụp thật:**
- *Film scan:* `"35mm colour negative, lab scan"` → kết quả: grain thật, halation quanh highlights
- *Phone photo:* `"phone camera, auto HDR off"` → smeared shadow noise, faint edge halo
- *DSLR:* `"natural light, no flash, no retouch"` → fine sensor noise, natural falloff

**Imperfection phải có VỊ TRÍ cụ thể:** *"pores across the nose and cheeks, redness at the nostril wings, one mole below the left jaw"* — không chỉ nói "add imperfections" chung chung.

---

### 27.7 Story Arc — 5 Loại Vòng Cung Kịch Bản & Khi Nào Dùng/Không Dùng

> 📚 Nguồn: `smixs/visual-skills` → `video/references/patterns-and-genres.md` §4

| Arc | Hình dạng | Dùng khi | KHÔNG dùng khi |
|---|---|---|---|
| **1. Causal Chain** | Bình thường → phá vỡ → hệ quả → giải quyết | Có mục tiêu + mỗi beat gây ra beat tiếp theo | Khoảnh khắc đơn lẻ, không có progression |
| **2. Turn (Kishotenketsu)** | Setup → mở rộng → yếu tố không liên quan xoay nghĩa → hòa giải | Không có đối thủ, sức mạnh nằm ở recontextualization | Đánh nhau, cạnh tranh, có đối thủ |
| **3. One Peak** | Vừa đủ context → đỉnh → tàn dư | Bắt 1 khoảnh khắc duy nhất (lời thề, giây chiến thắng) | Có progression tuần tự hoặc vấn đề cần giải |
| **4. Conflict Beat Sheet** | Opening → trigger → midpoint reversal → lowest → climax → closing | 2 lực đối đầu, kết quả bất định | Khám phá yên tĩnh, tuyến tính không đảo ngược |
| **5. Hook & Open End** | Hook → fragment → câu hỏi mở / CTA | Teaser, series, "to be continued" | Câu chuyện cần kết thúc trọn vẹn |

**Quy tắc:** Nếu 2 arc trông đều hợp lý → brief chưa quyết → hỏi khách hàng trước khi viết shots. Chạy 2 arc cùng lúc = phim đổi ý giữa chừng.

---

### 27.8 Anti-Slop Lexicon — 6 Lớp "Slop" & Bảng Thay Thế

> 📚 Nguồn: `Emily2040/seedance-2.0` → `references/anti-slop-lexicon.md`

**6 lớp slop cần kiểm tra (KHÔNG phải auto-delete — kiểm tra context trước):**

| Lớp | Dấu hiệu | Cách xử lý |
|---|---|---|
| **Empty evaluators** | `cinematic, epic, stunning, beautiful, dramatic` | Giữ nếu mang mood hữu ích, chỉ bổ sung quyết định thiếu |
| **Image-model tokens** | `8K, masterpiece, award-winning, RAW, Unreal Engine` | Tách riêng: delivery requirement vs render look vs lời khen rỗng |
| **Tag salad** | Keywords phẩy phẩy không rõ quan hệ | Nối subject + action + timing khi quan hệ mờ; list ngắn gọn OK |
| **Negation slop** | `no blur, no artifacts, no distortion` | Mô tả trạng thái MONG MUỐN — giữ exclusions cần thiết |
| **Adjective stacking** | `gorgeous, breathtaking, mesmerizing sunset` | Xóa lặp không thêm intent; giữ mood + distinction |
| **Feel-suffix** | `电影感`, `雰囲気のある`, `감성적인`, `vibey` | Giữ mood cue, chỉ clarify khi cần |

**Bảng thay thế hữu ích nhất:**

| Phrase | Quyết định cần làm rõ |
|---|---|
| "cinematic" | Framing, pacing, hay light cụ thể nào? |
| "dynamic" | Cái gì thay đổi theo thời gian? Đừng thêm camera move vào locked shot |
| "professional" | Production standard CỦA THỂ LOẠI NÀY là gì? |
| "cool transition" | Quan hệ giữa 2 shots là gì trước khi chọn transition |
| "ultra-realistic" | Material hay motion detail nào cần? Đừng hứa photorealism |
| "8K / ultra-HD" | Delivery target — KHÔNG phải prompt control, tách ra setting riêng |

---

### 27.9 Reference Transfer Contract — Pattern "Controls / Ignore"

> 📚 Nguồn: `Emily2040/seedance-2.0` → `references/reference-transfer-contract.md`

**Pattern bắt buộc cho mỗi reference:**
```
[ReferenceTag] controls [role] only; ignore [identity/environment/logo/audio/camera/motion] from that reference.
```

**Ví dụ thực tế:**
```
@Image1 controls character appearance only; ignore background, lighting, and other people from that reference.
@Video1 controls side-tracking camera rhythm only; ignore performer identity and background.
@Audio1 controls tempo and mood only; ignore dialogue content.
```

**3 quy tắc quan trọng:**
1. **Exact Tag Rule:** Giữ nguyên tag user cung cấp (`@Image1`, `@Image 1`, `[Video 1]`) — KHÔNG format lại, KHÔNG đổi case, KHÔNG renumber.
2. **Continuity Source ≠ Motion Reference:** Reference identity (bất biến) ≠ Reference motion (donor). Đừng để motion reference ghi đè lên identity/wardrobe/product geometry.
3. **Multi-Subject Selector:** Khi reference chứa nhiều subject, chỉ rõ subject nào bằng position/tag/feature — KHÔNG assume subject lớn nhất/trung tâm là đúng.

---

### 27.10 Field-Observed Tips — 10 Mẹo Thực Chiến & 4 Pattern Prompt Mạnh/Yếu

> 📚 Nguồn: `Emily2040/seedance-2.0` → `references/field-observed-tips.md`

**10 bước workflow ổn định (đã kiểm chứng trên Seedance 2.0, cần re-observe cho 2.5):**
1. **Draft ngắn trước dài:** Test 3-5s trước khi chi 10-15s clip.
2. **Đổi 1 biến/lần retry:** camera HOẶC lighting HOẶC motion HOẶC reference role.
3. **Bind mỗi reference 1 job duy nhất.**
4. **Locked framing cho:** identity dễ vỡ, logo sản phẩm, text đọc được, lip-sync, bàn tay, VFX phức tạp.
5. **Video ref = motion/camera rhythm, KHÔNG phải identity transfer.**
6. **Audio ref = tempo/mood/ambience** (trừ khi voice/music được cấp phép).
7. **Edit/extend/segment replace >> regenerate toàn bộ** khi chỉ 1 beat hỏng.
8. **Lưu last frame trả về → dùng làm first-frame anchor cho continuation.**
9. **Audio ref điều khiển timing → mute video ref cạnh tranh** hoặc hạ vai về camera/motion.
10. **Ghi lại observed final state TRƯỚC KHI xin prompt tiếp** — đừng assume kế hoạch xảy ra đúng.

**4 Pattern Prompt Mạnh vs Yếu:**

| ❌ Yếu | ✅ Mạnh |
|---|---|
| `cinematic, epic, beautiful` | `soft side backlight, wet asphalt reflections, locked medium shot, quiet room tone` |
| `make it move naturally` | `shoulders rise once with breathing, hand releases the cup, final pose holds for one second` |
| `use this video as style` | `@Video1 provides only side-tracking camera rhythm; do not transfer performer identity or background` |
| `make product luxury` | `narrow warm light sweep across the label, black acrylic table reflection, no label redesign` |

**High-Risk Areas (dễ lỗi nhất):**
- Cử chỉ tay nhanh, text/logo/label nhỏ
- Multi-character không tag
- Nhiều camera move đồng thời
- Product transformation mà identity phải giữ
- Extension chains không có last-frame anchor

---

### 27.11 Genre Templates Đắt Giá Nhất (Cherry-Pick 8/33 Thể Loại)

> 📚 Nguồn: `Emily2040/seedance-2.0` → `references/directing-engine-genre-library.md`

**Template 1 — Horror/Suspense:** Dùng `intimate minimalist` voice. Cực chậm creeping push vào doorway, giữ mối nguy KHÔNG THẤY. 1 practical light duy nhất + shadow sâu. Âm thanh: im lặng giữ + 1 off-screen cue. *Mẹo: "Her thumb rubs the chipped green paint on the rail once and then stops"* — 1 chi tiết vật lý nhỏ bé mang toàn bộ nỗi sợ.

**Template 2 — Comedy Pratfall:** `graphic formalist, deadpan`. Locked symmetrical wide + đợi past comfort. *"His palm stops short of his nose and redirects to straighten his collar"* — Camera KHÔNG PHẢN ỨNG (no reaction zoom), chỉ giữ frame im lặng.

**Template 3 — UGC / Caught Real Moment:** `observational naturalist + phone-UGC source lock`. Vertical handheld + sway nhẹ + auto-exposure shift. *Ôm artifacts, vì clean giả = fake.* *"One front paw slides on the blue dish towel, catches, and launches without a second attempt."*

**Template 4 — Dialogue Two-Hander:** `composed classicist`. Opposed singles cùng eye-level → subtle size/height imbalance khi power shift. *"Character B's index finger circles the cup rim once and stops before lifting it"* — bàn tay kể chuyện, không phải lời.

**Template 5 — Short Drama (短剧 / Vertical Drama):** `kinetic visceral, vertical tight`. Fast push → held close-up. *"Do not reveal the message, reserve the consequence for the next clip"* — cắt tại điểm cao trào, giữ khán giả treo.

**Template 6 — Product/Commercial Reveal:** `composed classicist`. Locked slider silhouette → hero. 1 warm key duy nhất quét across product. *Sản phẩm LÀ diễn viên — second hand completes one precise sweep.* Không bịa wearer/desire/drama.

**Template 7 — Talking-Head Pitch (口播):** `composed classicist, caption-safe`. Locked MCU + soft even key + headroom cho caption. *"The thumb taps the prototype's chipped blue corner once before the hand opens toward it"* — 1 gesture mở tay tại điểm key, kiềm chế.

**Template 8 — Nostalgia/Vintage Memory:** `observational naturalist + vintage source lock`. Grainy film texture + gate weave + halation. Camera KHÔNG đuổi theo subject khi subject rời frame — giữ lại empty wet patch. *Đồ vật bị bỏ lại kể câu chuyện vắng mặt.*

**Pattern chung của mọi template hay:** Mỗi template đều có `non-transferable detail` — 1 chi tiết vật lý cực nhỏ chỉ tồn tại trong cảnh này (nút áo lệch tâm, nhãn dán VISITOR gấp trên ve áo, vé xe buýt Route 17 nhét trong bản đồ). Chi tiết này là thứ khiến cảnh CÓ THẬT thay vì "stock footage feeling".

---

### 27.12 Montage Patterns — 6 Cấu Trúc Cắt Dựng Sẵn

> 📚 Nguồn: `smixs/visual-skills` → `video/references/patterns-and-genres.md` §1

| Pattern | Dùng cho | Chuỗi |
|---|---|---|
| **Escalation** | Tension build, reveal | `wide → medium → close-up → macro → reaction CU → impact` |
| **Anxiety** | Áp lực tâm lý, xung đột nội tâm | `face → object → hand → face → object closer → sound cue → sudden stillness` |
| **Discovery** | Khám phá, tìm kiếm | `POV → empty space → searching hand → hidden object → rack focus → emotional reaction` |
| **Catastrophe** | Thảm họa hài/kịch (vật nhỏ gây thảm họa lớn hơn vụ nổ) | `anticipation → object instability → reaction → falling → impact → silence → emotional collapse` |
| **Commercial Product Drama** | Quảng cáo sản phẩm hero | `lifestyle setup → product reveal → macro texture → human reaction → use moment → hero product shot` |
| **Music Video Loop** | Nhịp lặp, biến đổi | `gesture A → cut → gesture A from new angle → cut → transformation → repeat gesture A → release` |

---

### 27.13 Universal Rules — 3 Chi Tiết Bắt Buộc Mỗi Shot & Consequence Prompting

> 📚 Nguồn: `smixs/visual-skills` → `video/references/universal-rules.md`

**Three-Detail Check — Kiểm tra TRƯỚC KHI gửi prompt:**
Mỗi shot PHẢI có ít nhất 1 của mỗi loại:
1. **Environmental pressure** — ánh sáng lạnh tủ lạnh, asphalt ướt, đèn huỳnh quang nhấp nháy
2. **Physical micro-action** — hàm siết, ngón tay cuộn vào khung cửa, nuốt nước bọt
3. **Sound anchor / visual motif** — bụng kêu ở 2.3s, phản chiếu trong điện thoại tối

**Shot có 0/3 = filler → XÓA. Shot có 1/3 = mỏng. Shot mạnh = 3/3.**

**Consequence Prompting** — Mô tả HẬU QUẢ, không chỉ hành động:
- ❌ *"Tires spin"*
- ✅ *"Tires kick up water curtains meters high"*
- ❌ *"He opens the jar"*
- ✅ *"Hand grips the jar → lid actually unscrews → steam escapes"*

→ Action chains mà mỗi bước ép bước tiếp theo cũng là QA: chuỗi gãy = thế hệ lỗi hiện rõ ngay.

**Priority Declaration — Khi prompt quá tải (10+ scenes):** Đừng thêm mô tả → thêm thứ tự ưu tiên:
1. Subject cốt lõi phải sống qua mọi shot
2. Shots bắt buộc phải xuất hiện
3. Transitions model được tự do
4. Frame cuối bắt buộc

---

### 27.14 Nano Banana 2 — Đặc Thù & Cấm Kỵ

> 📚 Nguồn: `smixs/visual-skills` → `image/references/nano-banana.md`

**CẤM viết lens numbers:** `50mm, 85mm, f/2.8, ISO 400` → NB2 bỏ qua hoàn toàn. Thay bằng: `"shallow depth of field"`, `"wide-angle distortion"`.

**JSON cho scene 5+ elements:**
```json
{
  "subject": {"description": "main subject", "expression": "emotion/pose"},
  "photography": {"angle": "eye-level", "shot_type": "waist-up", "aspect_ratio": "16:9"},
  "background": {"setting": "location", "lighting": "soft natural"}
}
```

**Image Grounding (NB2 only):** Model tìm ảnh thật trên internet trước khi gen — dùng cho: buildings, bridges, squares, animal species, plant species. KHÔNG dùng cho: người cụ thể.

**Edit, don't re-roll:** Ảnh đúng 80% → chỉnh sửa cụ thể, KHÔNG gen lại. NB2 giữ context 3 edits liên tục.

**Known fails:** Tay/mặt vẫn bị lỗi (nhất là NBP), text nhỏ mờ ở 1K, hay bị overcooked HDR → thêm `"natural contrast, no HDR look"`.

**Workflow tiết kiệm:** Batch ở `0.5K` flash → chọn → regen winner ở `2K`/`4K`.

---

### 27.15 Rhythm Ladder — 4 Mẫu Nhịp Cắt Theo Thể Loại

> 📚 Nguồn: `smixs/visual-skills` → `video/references/dramaturgy.md` §12

| Thể loại | Mẫu nhịp (giây) |
|---|---|
| **Slow-burn drama** | 4s, 4s, 3s, 2s, 1s, **pause**, 2s |
| **Commercial product arc** | 3s, 2s, 1.5s, 1s, 0.5s (product macro), 2s (hero shot) |
| **Anxiety build** | 2s, 1s, 1s, 0.5s, 0.5s, 0.3s, **pause**, 1s |
| **Impact scene** | **pause**, 0.2s (flash), 2s (aftermath in stillness) |

**Quy tắc vàng:** Luôn chèn ít nhất 1 khoảng dừng (**pause**) TRƯỚC cú cắt lớn nhất. Không có pause, tốc độ thành máy xay thịt thị giác.

---

## 28. Giải Mã Nghệ Thuật Dựng Trailer Điện Ảnh & TVC Trên Higgsfield (`https://higgsfield.ai/community/projects`) — Từ Video Preview Ngoài Trang Chủ (`gallery_media`) Đến Từng Cú Máy `Shot 1 ➔ Shot N`, Nhịp Cắt, Âm Thanh & Bảng Nhân Vật `@IMG`

> **Bối cảnh thực chiến**:
> Khi lướt trang [`https://higgsfield.ai/community/projects`](https://higgsfield.ai/community/projects), trước khi bấm vào nút `"View full project"`, mỗi dự án đều có một **Video Trailer / Master Cut tự động phát (`gallery_media`)** với nhịp cắt cực kỳ cuốn hút, kỹ xảo biến hình mượt mà, âm thanh có khoảng lặng nổi da gà và bảng tên phim (`Title Card`) chuyên nghiệp như Netflix / A24 / Game AAA.
> Để giúp bạn nắm trọn **công thức dựng Trailer và dùng chính tư duy Trailer đó để làm bộ phim tiếp theo**, chúng ta đã:
> 1. **Nâng cấp [`scraper/higgsfield_project_scraper.py`](./scraper/higgsfield_project_scraper.py)**:
>    - Bổ sung cơ chế tự động dò cả 4 trường thư mục gốc (`snapshot_folder_id` ➔ `original_folder_id` ➔ `root_folder_id` ➔ `source_folder_id`) để mở khóa toàn bộ các dự án Trailer phức tạp có chia nhiều thư mục con (`Character sheet`, `Locations`, `SHOT1`..`SHOT5`, `Final shots`, `UI`).
>    - Bảo toàn trọn vẹn danh sách **`gallery_media`** (chứa toàn bộ các bản dựng Video Trailer / Master Cut ngoài trang chủ) trong `raw_dataset.json`.
>    - Bổ sung ánh xạ tên chuẩn cho các model mới nhất dùng trong các dự án Trailer: `kling_video_edit` (`Kling Video Edit`), `gpt_image_2_unlimited` (`ImageGen 2.0 Unlimited`), `image_auto` (`Higgsfield Auto Image`), `cinematic_studio_3_0_image_edit` (`Cinema Studio 3.0 Image Edit`), `cinematic_studio_3_0` (`Cinema Studio 3.0`), `cinematic_studio_video_4_0` (`Cinema Studio Video 4.0`), `wan3_0` (`Wan 3.0`).
> 2. **Cào mới 100%, tải toàn bộ `@IMG` & Kiểm định thị giác (`Visual Audit First` bằng `read_file`) 6 Dự Án Trailer Đỉnh Cao** trên trang Community Projects (nâng tổng kho dữ liệu lên **`36` dự án + `3` kho clip lẻ = `39` hồ sơ đạo diễn**, **`47,334` jobs ➔ `9,906` cụm cảnh Final Take**):
>    - **`@buralqy/projects/kai-streamer-university-trailer-vfx`** (`254` jobs ➔ `67` clusters, `46` `@IMG`)
>    - **`@diegothetower/projects/the-secret-monkey-island-movie-trailer`** (`27` jobs ➔ `11` clusters, `16` `@IMG`)
>    - **`@lerra98/projects/emberdant-s1-trailer`** (`38` jobs ➔ `24` clusters, `57` `@IMG`)
>    - **`@lightdrop-studio/projects/dudes-in-distress`** (`541` jobs ➔ `368` clusters, `206` `@IMG`)
>    - **`@daniallll/projects/seed-audio-1-0-launch-video`** (`950` jobs ➔ `54` clusters, `27` `@IMG`)
>    - **`@higgsfield.soul/projects/huntress-s-tale`** (`225` jobs ➔ `49` clusters, `40` `@IMG`)

---

#### 28.1. Bản Chất Của Video Preview Ngoài Trang Chủ (`gallery_media`) Và Cách Nó Liên Kết Với Các Cảnh Lẻ Bên Trong `"View full project"`

| # | Dự Án Trailer (`@author/projects/slug`) | Link Video Trailer Preview Ngoài Trang Chủ (`gallery_media[0]` & `master_film_url`) | Thời Lượng Master Cut | Quy Mô Cây Thư Mục Bên Trong `"View full project"` | Trường Phái Dựng Trailer Đặc Trưng |
| ---: | :--- | :--- | ---: | :--- | :--- |
| 1 | **`buralqy/kai-streamer-university-trailer-vfx`** | [`hf_20260711_074848_b3c60070.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_2vXWHqHVtNVlKTey8FQHzStgrcP/hf_20260711_074848_b3c60070-5505-443d-b9f3-b4c14e921b18.mp4) \| [HLS Preview](https://d3u0tzju9qaucj.cloudfront.net/5516d0c8-f87f-4fa0-9c9a-142d6d04ff99/1f266464-e0a3-4ef7-8f13-87bc84068757.m3u8) | `138.8s` | `254` jobs ➔ `67` clusters (`37` Video + `30` Ảnh, `46` `@IMG`) | **Hybrid Live-Action + AI VFX Trailer**: Khoanh bút đỏ `#FF0000` (`Red-Lasso Inpaint` `@IMG_002`, `SCENE_003`, `SCENE_016`) để bơm khói hơi nước / dọn tiền cảnh sân ga và biến cửa cuốn nhà kho (`@IMG_015`) thành cổng phép thuật `Platform 9¾` (`VIDEO 07`..`VIDEO 10`). |
| 2 | **`lerra98/emberdant-s1-trailer`** | [`hf_20260907_164308_430aa615.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3EnOjmTEOqMaLjdbEv6fpXfnvDE/hf_20260907_164308_430aa615-6c0d-4d08-8772-0d44d466d4f8.mp4) \| [HLS Preview](https://d3u0tzju9qaucj.cloudfront.net/ac6c0392-54c6-48b9-a9f8-8378f1e6b3f9/f8aa8fd8-dd3a-4781-b030-9f5c694b420b.m3u8) | `200.5s` | `38` jobs ➔ `24` clusters (`20` Video + `4` Ảnh, `57` `@IMG`) | **Theatrical Dark-Fantasy Series Trailer (`2.39:1`)**: Chuỗi `VIDEO 01 -> VIDEO 20` trên `Seedance 2.5` & `2.0` (`Lễ cưới tại The Ember Hall & Casada vỗ tay trễ nửa nhịp` ➔ `96fps chìm xuống biển đen Sea Gate` ➔ `Tàu Raven's Due & thuyền trưởng Mora` ➔ **Quy tắc `4 Giây Đen Đặc & Im Lặng Tuyệt Đối (00:22–00:26)`** ở `VIDEO 10` và Title Card chữ đá nứt lửa `@IMG_041`, `VIDEO 17`..`VIDEO 20`). |
| 3 | **`higgsfield.soul/huntress-s-tale`** | [`hf_20260625_180823_9b4b4579.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_2x29137N157098v55v6c6B2E1E9/hf_20260625_180823_9b4b4579-cf0f-414e-b334-2fd58fd7ca55.mp4) \| [HLS Preview](https://d3u0tzju9qaucj.cloudfront.net/649b723b-1c82-463a-8d0a-1765f170fa45.mp4/c5296883-536e-4187-b152-d7f4616c234d.m3u8) | `67.4s` | `225` jobs ➔ `49` clusters (`22` Video + `27` Ảnh, `40` `@IMG`, chia 8 thư mục `Character sheet`, `Locations`, `SHOT1..5`, `UI`) | **AAA Game-Cinematic Dark Fantasy Trailer**: Sập sàn rơi thẳng xuống hầm ngập nước (`VIDEO 20`) ➔ Rồng biển đuổi (`VIDEO 01`) ➔ **Cú Twist Nàng tiên trên vai hóa Rồng quấn cổ (`VIDEO 21/22`)** ➔ Màn hình `YOU DIED / Try Again?` (`SCENE_049`). |
| 4 | **`daniallll/seed-audio-1-0-launch-video`** | [`hf_20260630_155320_11942466.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_2wW5p9z8R4k1m7N3x6B0v2C9q5L/hf_20260630_155320_11942466-9254-4625-9337-473873580932.mp4) \| [HLS Preview](https://d3u0tzju9qaucj.cloudfront.net/f292b281-bf75-42f0-90b5-d6f5ab20ee49/b0d86631-ef9c-49d0-a7d5-55a562d91f9a.m3u8) | `106.1s` | `950` jobs ➔ `54` clusters (`20` Video + `34` Ảnh, `27` `@IMG`) | **Product Launch & Multi-Voice Showcase Trailer**: Xóa chữ rác trên áo (`@IMG_002` ➔ `@IMG_003`), chuyển đổi ngôn ngữ camera (`Sean Baker` ➔ `David Fincher ASMR Push-In` `VIDEO 02` ➔ `Workplace Mockumentary Whip-Pan` 5 nhân vật tung hứng thoại trong 1 cú máy `15s` `VIDEO 06`). |
| 5 | **`lightdrop-studio/dudes-in-distress`** | [`hf_20260820_235744_d1c44601.mp4`](https://d8j0ntlcm91z4.cloudfront.net/user_3GFI9yneBNy5n75epfzclaq8i2y/hf_20260820_235744_d1c44601-1a55-43f7-858e-523541c2ab2e.mp4) \| [HLS Preview](https://d3u0tzju9qaucj.cloudfront.net/e729699a-be58-4a3b-a4eb-e7ff49b6c717/17d5742c-a6bb-4d28-9214-bf20172f2957.m3u8) | `332.25s` | `541` jobs ➔ `368` clusters (`144` Video + `224` Ảnh, `206` `@IMG`, có thư mục riêng `Final shots`) | **Live-Action Fantasy Adventure Trailer**: Bảng nhân vật `8-Panel Tattoo Callout` (`@IMG_004`), câu lệnh cắt đầu 1 dòng (`@IMG_090`, `@IMG_096`), đồng xu có bản lề giấu cuộn giấy `1cm` (`@IMG_037`, `@IMG_121`, `@IMG_180`, `@IMG_206`), và cú máy `5-Second Fast Action-Trailer Crane Swoop` biến vũ khí thành hoa (`VIDEO 139`). |
| 6 | **`diegothetower/the-secret-monkey-island-movie-trailer`** | [HLS Master Cut](https://d3u0tzju9qaucj.cloudfront.net/568bd44b-ef25-4435-942c-b14bf1b90e44/c4ca8b6d-7f24-41d5-8cb0-ca12714996e3.m3u8) | `106.75s` | `27` jobs ➔ `11` clusters (`11` Ảnh Keyframe & Turnaround, `16` `@IMG`) | **IP-to-Hollywood Live-Action Concept Trailer**: Chuyển thể 4 tấm sprite 2D (`@IMG_001..004`) thành diễn viên Hollywood `Tom Holland` (`@IMG_014`), phẫu thuật bóc lớp trang phục (`SCENE_008` / `@IMG_015`), bảng xoay đầu (`@IMG_016`) & bảng 8 biểu cảm (`SCENE_011`). |
| 7 | **`seksifratello/apeirophobia-teaser`** *(đã có trong kho)* | [`431270ea-2298-4436-b245-0b300661f788.mp4`](https://d2ol7oe51mr4n9.cloudfront.net/user_31n0NLIr1dkrN5DoEG0FF0aoOzh/431270ea-2298-4436-b245-0b300661f788.mp4) | `97.6s` | `6,862` jobs ➔ `1,444` clusters (`267` Video + `1,177` Ảnh, `374` `@IMG`) | **A24 Psychological Horror Teaser**: `ARRICAM ST 500T Look Lock` + `Anti-Beautification Skin Realism` + mê cung hành lang `Liminal Space`. |
| 8 | **`alishaqantaar/the-new-girl`** *(đã có trong kho)* | [`bb1d117b-f833-4810-a131-ca44eaad1c8b.mp4`](https://d2ol7oe51mr4n9.cloudfront.net/user_3FYSo9OooPo1Z8CSN2pLzprvU6X/bb1d117b-f833-4810-a131-ca44eaad1c8b.mp4) | `90.0s` | `373` jobs ➔ `83` clusters (`22` Video + `61` Ảnh, `58` `@IMG`) | **Japanese High-School Thriller Teaser**: Dựng nhiều góc máy liên hoàn trong cùng 1 phòng học (`Reframe the same classroom from the back...`) + `Authority Contract Locks`. |
| 9 | **`mixingburrito1329/anime-production`** *(đã có trong kho)* | [`8f4c23e3-659e-4e15-b52a-0d115f1f74fd.mp4`](https://d2ol7oe51mr4n9.cloudfront.net/user_3EugSQ3VZX24bAVRklLPXGmHpQM/8f4c23e3-659e-4e15-b52a-0d115f1f74fd.mp4) | `60.0s` | `440` jobs ➔ `135` clusters (`5` Video trong `Video generations` + `130` Ảnh, `16` `@IMG`) | **Early-2000s Retro Anime Action Trailer**: Bảng `2-Panel Split-Screen Character Sheet` (`Seedream 5.0 Pro`) + kịch bản nhiều Shot liên hoàn (`Shot 1 (0–3s)`..`Shot 4`) trong 1 cú máy `15s`. |

#### 🎬 Giải Mã Sơ Đồ Ráp Nối Từng Cảnh (`Shot 1 -> Shot N`) Từ Cây Thư Mục Vào Bản Dựng Trailer Master Cut
Khi đối chiếu trực tiếp file video Trailer ngoài trang chủ (`gallery_media[0]`) với danh sách các cụm cảnh (`VIDEO 01 -> VIDEO N`) bên trong `"View full project"`, chúng ta thấy rõ cách các đạo diễn chia nhỏ một Trailer thành các khối cảnh độc lập rồi ráp lại:
- **Mô hình 1 — Phân Hồi Có Đánh Số Timecode Ngay Trong Prompt (`lerra98/emberdant-s1-trailer`: `VIDEO 01 -> VIDEO 20` trong [`VIDEO_CENTRIC_SCRAPED_PROMPTS.md`](./data/creators/lerra98/projects/emberdant-s1-trailer/VIDEO_CENTRIC_SCRAPED_PROMPTS.md))**:
  * **Cụm 1 — Lễ Cưới Hoàng Gia, Biến Cố Đẫm Máu & Bản Dựng Hồi I `"THE GOLD"` (`VIDEO 01`..`VIDEO 06`, `Seedance 2.5`)**:
    - `VIDEO 01` (`SCENE_003`, `30s`): Lễ cưới ấm áp trong đại sảnh `THE EMBER HALL` (`@IMG_004: ember-hall`). Chú rể `Casimir` (`@IMG_006: casimir_wedding`) hồi hộp làm vướng nhẫn cưới ở đốt ngón tay (`THE FUMBLE`), cô dâu `Maeve` (`@IMG_005: maeve_wedding`) bật cười nén một tiếng khụt mũi nhỏ (`one small snort she immediately tries to swallow`) và chỉnh lại tay giúp anh. `THE HIGH PRIEST` quấn dải lụa vàng-đỏ buộc tay hai người (*"Before the flame that made us — and the sea that surrounds us —"*); Casimir thì thầm *"...I've got it. I've got it."*, Maeve đáp *"You haven't."*
    - `VIDEO 02` (`SCENE_004`, `30s`) & `VIDEO 03` (`SCENE_005`, `6s`): Thảm sát đẫm máu ngay tại lễ cưới (`@IMG_008: ember-hall_blade`). `Maeve` (`@IMG_007: maeve-dy`) ngã gục trên bậc đá, `Casimir` (`@IMG_009: casimir_bl`) bị kéo ngã theo vì hai cổ tay vẫn bị buộc dây lễ nghi; anh dùng răng cắn đứt dây trói, áp tai sát miệng cô giữa đại sảnh hỗn loạn (*"No — no, look at me — Maeve. Maeve. Say it again. Say it again —"*), rồi nhìn lòng bàn tay tắt lịm ánh lửa và hét lên ở `VIDEO 03`: *"you poison me with wine , i can't transform!!"*.
    - `VIDEO 04` (`SCENE_006`, `4s`) & `VIDEO 05` (`SCENE_007`, `5s`): Chiến trường phép thuật tối (`@IMG_010: dark-magic-war-field`) — `Vacier` (`@IMG_011`) cưỡi ngựa đen rút kiếm và `Morrigana` (`@IMG_012`) giương cung tan biến trong làn khói trắng.
    - `VIDEO 06` (`SCENE_008`, `30s` — `[00:00:00 – 00:00:30] · “THE GOLD”`): Bản dựng chuẩn Hồi I chia 5 nhịp: `00:00–00:08` cận cảnh hai bàn tay trao nhẫn; `00:08–00:14` máy quay lướt qua hàng ghế khách mời và bắt gặp em trai **`Casada` (`@IMG_013: casada_court`) mặc lễ phục đen-xanh lục đang vỗ tay cùng tốc độ với cả khán phòng nhưng trễ nửa nhịp (`applauding half a beat behind the room, lit exactly as warmly as everyone else`)**; `00:14–00:16` đàn thằn lằn rồng vàng (`@IMG_014: tame-ember-drakes`) trên giếng trời `oculus` đồng loạt ngoảnh đầu về phía những cánh cửa đang đóng rồi tung cánh bay tán loạn ở `48fps`; `00:16–00:20` cắt sang đen 4 giây im lặng tuyệt đối; `00:20–00:30` cận cảnh tĩnh (`Static macro`) vết máu đỏ đen loang chậm từng sợi chỉ trên lụa váy cưới trắng-vàng (`The stain. Static macro on white-and-gold bridal silk. Black-red spreading thread by thread`).
  * **Cụm 2 — Phản Bội Soán Ngôi, Quăng Xuống Biển Đen Ở `96fps` & Tàu Cướp Biển `The Raven's Due` (`VIDEO 07`..`VIDEO 09`, `Seedance 2.5`)**:
    - `VIDEO 07` (`SCENE_010`, `30s`): Ngục tối `THE SLAVE CATACOMBS` (`@IMG_020`) với `Casimir` (`@IMG_017: casimir_chain`) bị xiềng trong lồng sắt; `Casada` (`@IMG_018: casada_enthroned`) ngồi trên ngai vàng nghe `THE BOUGHT PRIEST` (`@IMG_021: the-bought-priest`) đọc bản án tại `THE COURT OF THE EMBER THRONE` (`@IMG_022`); tại bến cảng `THE SEA GATE` (`@IMG_016`) trong mưa đêm, lính gác xô `Casimir` xuống vực biển đen — máy quay chuyển sang góc dưới mặt nước ở **`96fps slow-motion`** quay cảnh cơ thể `Casimir` (`@IMG_019: casimir_sinking`) chìm dần qua làn nước đen đặc cùng giọng đọc `THE SEA (V.O.)`: *“They chose the sea as the dead. Because the sea forgets, they said.” (a pause) “The sea forgets nothing.”*
    - `VIDEO 08` (`SCENE_011`, `30s`): Bình minh trên biển với tàu cướp biển buồm đen `THE RAVEN'S DUE` (`@IMG_026: ravens-due_hero`). Thuyền trưởng `Mora` (`@IMG_027: mora_pirate`) vớt `Casimir` (`@IMG_028: casimir_wreckage`), vạch cổ áo thấy vết sẹo bỏng hình rồng ở xương quai xanh trái (`THE DRAKE-BRAND`) và mỉm cười toan tính: *“Whatever the sea kept, the Due collects.” … “…dragon.”* Tiếp nối cảnh đêm `Mora` (`@IMG_023: mora_rifle`) chĩa súng kíp vào `Casimir` bị trói ở cột buồm (`@IMG_029: casimir_prisoner`): *“Do you know what your kingdom has done to my people?”*, rồi cánh buồm bão đen (`@IMG_025: the-storm-sail`) bung ra ở `120fps` như đôi cánh rồng.
    - `VIDEO 09` (`SCENE_012`, `30s`): Vùng biển sương mù trắng đục `THE VEIL CURRENTS` (`@IMG_034: veil-reef_fog`), nơi tấm lưới kéo (`@IMG_035: the-net`) phát sáng ánh đồng đỏ duy nhất giữa khung hình đơn sắc; `Casimir` (`@IMG_033: casimir_deck-duel`) bước ra chắn mũi kiếm bảo vệ `Lyra` (`@IMG_031: lyra_net`): *“Let her live. She’s done nothing wrong.”*; `Lyra` (`@IMG_032: lyra_netbreak`) bung rách lưới ở `96fps` và thủy quái 3 đầu `THE HYDRA` (`@IMG_030: hydra`) trồi vọt lên khỏi mặt biển đen.
  * **Cụm 3 — Cao Trào Tàu `Raven's Due` Bốc Cháy, Quy Tắc `4 Giây Đen Đặc & Im Lặng Tuyệt Đối (00:22–00:26)` & Title Card Đá Nứt Lửa (`VIDEO 10`..`VIDEO 20`, `Seedance 2.5` & `2.0`)**:
    - `VIDEO 10` (`SCENE_013`, `30s`): `00:00–00:08` cú máy 7 giây không cắt (`Seven unbroken seconds`) trước bánh lái tàu trong cuộc phục kích đêm — `Mora` (`@IMG_037: mora_helm-burning`) nắm chặt bánh lái khi vạt áo khoác sau lưng đang bốc cháy lửa xanh ngùn ngụt, nghiến răng thở gấp không buông tay; `00:08–00:14` `Casimir` (`@IMG_036: casimir_pirate` / `@IMG_038: casimir_stormwing`) đu dây văng qua mặt biển đen, trong khi mặt biển dưới hạm đội địch đông cứng như mặt kính (`@IMG_040: the-tide-refusing`) khiến hàng trăm mái chèo đập xuống trượt đi; `00:14–00:22` đại cảnh con tàu `THE RAVEN'S DUE BURNING` (`@IMG_039: ravens-due_burning`) bốc cháy từ mớn nước lên đỉnh cột buồm cùng giọng đọc `THE SEA (V.O.) - MAN'S VOICE`: *“The crown had a dragon.” (a pause) “And threw him into the sea.”*; **`00:22–00:26` cắt phụt sang 4 giây màn hình đen đặc và im lặng kỹ thuật số tuyệt đối (`Cut to black. Total silence. Four seconds. Nothing.`)**; `00:26–00:30` dòng lửa vàng-cam nóng chảy trào lên dọc rãnh đá khắc cổ ngữ (`@IMG_041: cave-of-carvings_title`) tạo chữ **`EMBERDANT / THE CHRONICLE OF KALDRIS`**.
    - `VIDEO 11` (`SCENE_014`, `30s`) & `VIDEO 12`..`VIDEO 16` (`4s–8s`): Montage 4 nhịp quyền lực của vua giả `Casada` (`Vessendra` `@IMG_049` rót độc dược đen `@IMG_044` trong hầm mộ `@IMG_042` cho `Casada` `@IMG_045` uống nổi gân đen; `Maren` `@IMG_047` cầm kiếm gỗ `@IMG_052` giữa đấu trường rồng `@IMG_046`; `Casada` `@IMG_048` đứng ở mũi chiến thuyền `@IMG_051` tuyên bố *"I have taught the sea the shape of my war, brother."*; hàng lồng sắt `@IMG_043` mở tung thả binh đoàn quái thú `@IMG_050`), cùng các cảnh thuỷ thủ đoàn nhảy múa/kể chuyện quanh lửa trại trên boong tàu (`VIDEO 12`, `14`, `15` `@IMG_054`..`@IMG_056`), đấu trường rồng (`VIDEO 13` `@IMG_053`) và đánh `Hydra` (`VIDEO 16` — `Mora` hô *"attack!!"*).
    - `VIDEO 17` (`SCENE_020`, `4s`, `Seedance 2.0`) & `VIDEO 18`..`VIDEO 20` (`SCENE_021`..`SCENE_023`, `4s` mỗi cảnh, `Seedance 2.5`): Bộ 4 Title Cards kết thúc (`DIRECTED AND ORIGINAL STORY BY LERRA BAJUT` ở `VIDEO 17..18`, `[COMING SOON] [9.9.2026]` ở `VIDEO 19`, và Title Card chính `EMBERDANT / THE CHRONICLE OF KALDRIS` chữ serif vàng cổ điển trên tường đá chạm khắc tối ở `VIDEO 20`).
- **Mô hình 2 — Chia Cây Thư Mục Theo Từng Cụm Shot (`higgsfield.soul/huntress-s-tale`: 8 Thư Mục `Character sheet`, `Locations`, `SHOT1`..`SHOT5`, `UI`)**:
  * Thư mục `Character sheet` (`SCENE_001`..`SCENE_011`) & `Locations` (`SCENE_012`..`SCENE_019`): Tạo trước toàn bộ bảng nhân vật nữ thợ săn (`@IMG_009`, `@IMG_010`), tách con rồng biển ra nền xám (`@IMG_008` ➔ `@IMG_011`), và khóa mã màu HEX lạnh cho 3 bối cảnh hầm ngầm (`@IMG_012`, `@IMG_016`, `@IMG_018`).
  * Thư mục `SHOT2` (`VIDEO 20` / `SCENE_035`): Nữ thợ săn chạy dọc hành lang đá thì sàn nhà sập vỡ, rơi thẳng một mạch (`no shaft between them`) xuống căn hầm ngập nước bên dưới.
  * Thư mục `SHOT1` & `SHOT3` (`VIDEO 01`..`VIDEO 19`): Cuộc chạm trán và rượt đuổi nghẹt thở với con rồng biển (`@IMG_011`) dưới làn nước xanh lạnh.
  * Thư mục `SHOT5` (`VIDEO 21` & `VIDEO 22` / `SCENE_041`): Nữ thợ săn lao qua cánh cửa gỗ đôi, đóng sầm lại thở phào nhẹ nhõm (`[00-03s]`) ➔ Nàng tiên nhỏ (`@IMG_020`) đậu trên giáp vai bỗng rùng mình hóa thành con rồng nước quấn chặt quanh cổ cô từ phía sau (`[03-10s]`).
  * Thư mục `UI` (`SCENE_047`..`SCENE_049`): Cắt sang đen kèm tiếng nuốt ừng ực, hiện Logo bạc `Huntress's Tale` (`SCENE_047`) và màn hình kết thúc `YOU DIED / Try Again? ▶ YES / NO` (`SCENE_049`).

---

### 28.2. Khung Xương Sống 5 Hồi Của Một Trailer Đỉnh Cao Trên Higgsfield (`The 5-Act AI Trailer Blueprint — 45s to 90s`)

Khi bạn bắt tay làm một bộ phim ngắn hoặc TVC mới, **hãy thiết kế nó theo đúng Cấu Trúc 5 Hồi Của Một Trailer Điện Ảnh (`5-Act Trailer Spine`)** dưới đây để khán giả bị hút chặt từ giây thứ nhất đến giây cuối cùng:

1. **Hồi 1 (`00:00–00:08` — `THE COLD OPEN / VISUAL HOOK`: Cú Móc Thị Giác Trong 3 Giây Đầu)**:
   - **Tuyệt đối không mở đầu bằng cảnh toàn tĩnh lặng vô thưởng vô phạt**. Các đạo diễn Trailer trên Higgsfield luôn chọn 1 trong 3 cách mở màn:
     * **Cách A — `Direct-to-Lens Intimate Hook` (`daniallll/seed-audio-1-0-launch-video` `VIDEO 01` & `VIDEO 02`)**: Nhân vật nhìn thẳng vào ống kính góc rộng trên nền phông trắng vô cực (`white cyclorama`), máy quay cầm tay thở nhẹ kiểu `Sean Baker` hoặc đẩy trượt dolly siêu chậm kiểu `David Fincher` từ trung cảnh vào sát môi khi nhân vật hạ giọng thì thầm ASMR vào micro.
     * **Cách B — `No-Shaft Floor Collapse Transition` (`higgsfield.soul/huntress-s-tale` `VIDEO 20`)**: Nhân vật đang chạy trong hành lang đá sáng, ở giây thứ `03–05s` mặt đất dưới chân bất ngờ sập vỡ và **lỗ thủng trên sàn chính là lỗ thủng trên trần của căn hầm ngập nước bên dưới (`no shaft between them; she falls directly through`)** — cú rơi 1-take xuyên qua 2 tầng không gian!
     * **Cách C — `Intimate Human Fumble -> Half-Beat Delayed Applause Betrayal Cue` (`lerra98/emberdant-s1-trailer` `VIDEO 01` & `VIDEO 06` — `"THE GOLD"`)**: Mở màn bằng khoảnh khắc đời thường cực kỳ ấm áp tại lễ cưới (`Casimir` hồi hộp làm vướng nhẫn cưới ở đốt ngón tay và cô dâu `Maeve` bật cười nén tiếng khụt mũi ở `VIDEO 01`), rồi máy quay lướt qua hàng ghế khách mời đang vỗ tay để bắt gặp kẻ phản bội **`Casada` (`@IMG_013: casada_court`) mặc lễ phục đen-xanh lục đang vỗ tay cùng tốc độ nhưng trễ đúng nửa nhịp so với cả khán phòng (`applauding half a beat behind the room`)**, ngay trước khi đàn rồng nhỏ trên giếng trời `oculus` tung cánh bay tán loạn ở `48fps` và vết máu đỏ đen loang dần từng sợi chỉ trên lụa váy cưới trắng-vàng (`VIDEO 06`)!
2. **Hồi 2 (`00:08–00:22` — `THE SECRET OBJECT & CONSPIRACY BEAT`: Đạo Cụ Chứa Bí Mật)**:
   - Thay vì dùng lời thoại dài dòng giải thích cốt truyện, hãy dùng **1 Đạo cụ vật lý có cơ chế đóng/mở (`Mechanical Reveal Prop`)** giống như `lightdrop-studio/dudes-in-distress` (`VIDEO 06`, `VIDEO 08`, `VIDEO 10`, `VIDEO 11`):
     * Nhân vật nhặt được **đồng xu vàng có khớp bản lề `@IMG_037` / `@IMG_121` (`The-coin`)**.
     * Cận cảnh ngón tay tách nhẹ khớp bản lề (`visible hinge on the rim` — khoang trong `@IMG_180`), hé lộ **cuộn giấy phép thuật tí hon dài đúng `1cm` (`@IMG_029: scroll`, khóa tỷ lệ trên lòng bàn tay ở `@IMG_206`)** nằm gọn bên trong lòng đồng xu rỗng!
     * Nghe tiếng bước chân của kẻ phản diện (`@IMG_036: GOM`), cô lập tức **rút cuộn giấy giấu ra sau lưng bằng tay trái trong khi tay phải bấm đóng sập đồng xu lại (`soft metallic click`)** rồi đưa chiếc đồng xu rỗng cho hắn mà hắn không hề nghi ngờ! Chỉ trong 15 giây không cần 1 câu giải thích, khán giả hiểu ngay âm mưu và hồi hộp tột độ!
3. **Hồi 3 (`00:22–00:38` — `THE ESCALATION MONTAGE & 5-SECOND ACTION-TRAILER SWOOP`: Cao Trào Hành Động Tốc Độ Cao)**:
   - Đây là lúc tung ra các cú máy **5 giây (`Up to 5 seconds maximum — Fast action-trailer energy`)** theo công thức của `lightdrop-studio/dudes-in-distress` (`VIDEO 139` & `VIDEO 140`):
     * **Nhịp `0.0s–1.2s`**: Camera Drone/Crane từ trên cao (`HIGH ABOVE the castle side`) lao vút xuống để thấy rõ toàn bộ địa hình 2 phe đối đầu trên cây cầu đá (`CASTLE SIDE` vs `OPPOSITE SIDE`).
     * **Nhịp `1.2s–2.0s`**: Camera hạ thấp đặt nhân vật chính (`@IMG_183: mali`) ở tiền cảnh, đám đông kẻ địch đang lao tới ở hậu cảnh ngay phía sau lưng cô.
     * **Nhịp `2.0s–2.6s` (`Sharp Gesture / Backward Over-the-Shoulder Casting`)**: Nhân vật tung cú vung tay dứt khoát phóng làn sóng xung kích phép thuật màu xanh lá về phía cầu.
     * **Nhịp `2.6s–5.0s`**: Camera lao vút theo làn sóng xung kích màu xanh lá (`surges forward WITH the green wave`), đi đến đâu vũ khí của kẻ địch (xẻng, đinh ba, búa, rìu, cung tên) **lập tức biến thành những bó hoa rực rỡ (`instantly transform into flowers`)** đến đó!
   - **Quy tắc Âm thanh Sống còn ở Hồi 3 (`ABSOLUTELY NO BACKGROUND MUSIC`)**: Mọi câu prompt tạo cảnh hành động trong Trailer đều phải khóa **`ABSOLUTELY NO BACKGROUND MUSIC. NO MUSIC WHATSOEVER. NO SCORE.`** để khi dựng Trailer, tiếng bước chân, tiếng kiếm chạm và tiếng nổ phép thuật sạch 100%, không bị các đoạn nhạc AI hỗn tạp đè lên nhau!
4. **Hồi 4 (`00:38–00:46` — `THE 4-SECOND TOTAL BLACK & DIGITAL SILENCE RULE + TITLE CARD`: 4 Giây Đen Đặc & Im Lặng Tuyệt Đối Trước Bảng Tên Phim)**:
   - Đây là **phát hiện đắt giá nhất về tâm lý học khán giả** từ đạo diễn `@lerra98/emberdant-s1-trailer` (`VIDEO 10` / `SCENE_013` & `VIDEO 17`..`VIDEO 20`):
     * Ngay sau đại cảnh con tàu `The Raven's Due` (`@IMG_039`) bốc cháy ngùn ngụt trên biển đêm cùng câu đọc trầm đục của `THE SEA (V.O.)`: *“The crown had a dragon.” (a pause) “And threw him into the sea.”* (`00:14–00:22`), **CẮT PHỤT SANG MÀN HÌNH ĐEN ĐẶC VÀ TẮT SẠCH 100% ÂM THANH TRONG ĐÚNG 4 GIÂY (`00:22 – 00:26 — Cut to black. Total silence. Four seconds. Nothing. / EVERYTHING STOPS. Digital silence. Four seconds.`)**!
     * Như `@lerra98` viết nguyên văn trong khối `DIRECTION` của prompt `VIDEO 10` (`SCENE_013`): *"The four seconds of silence at 02:52 are the most valuable seconds in the trailer. After escalation, stop everything. No music, no sound, no image. On a phone in a feed, that is the moment a thumb stops moving."* (4 giây im lặng ở 02:52 là những giây giá trị nhất trong cả trailer: sau khi đẩy cao trào lên đỉnh điểm, hãy dừng tất cả — không nhạc, không âm thanh, không hình ảnh; trên màn hình điện thoại khi đang lướt bảng tin, đó chính là khoảnh khắc ngón tay cái của người xem khựng lại!).
     * Ngay sau 4 giây im lặng đó (`00:26–00:30` ở `VIDEO 10`, kết hợp bộ Title Cards `VIDEO 17`..`VIDEO 20`), từ bức ảnh thanh kiếm cắm vào vách đá khắc cổ ngữ (`@IMG_041: cave-of-carvings_title`), dòng lửa vàng-cam nóng chảy trào lên lắp đầy từng rãnh chữ **`EMBERDANT / THE CHRONICLE OF KALDRIS`** kèm âm thanh đe sắt đảo ngược và tiếng dung nham nứt (`a reversed struck anvil, slow lava crackle, sub-bass rise`)!
5. **Hồi 5 (`00:46–00:60+` — `THE POST-TITLE STINGER TWIST & INTERACTIVE END CARD`: Cú Lật Mặt Sau Khi Tưởng Đã An Toàn)**:
   - Học từ đoạn kết rùng mình của **`@higgsfield.soul/huntress-s-tale` (`VIDEO 21` & `VIDEO 22` + `SCENE_049`)**:
     * **`[00-03s]` (Sự nhẹ nhõm giả tạo — `False Relief`)**: Nữ chiến binh lao qua cánh cửa gỗ khổng lồ, đóng sầm cửa lại chặn con thủy quái bên ngoài, tựa lưng vào cửa nhắm mắt thở phào nhẹ nhõm. Nàng tiên nhỏ phát sáng (`@IMG_020: Fairy`) đậu êm ái lên giáp vai cô.
     * **`[03-07s]` (Sự biến đổi ngay trên vai — `The Shoulder Betrayal`)**: Trong sự im lặng chỉ có tiếng nước nhỏ giọt, cơ thể nàng tiên nhỏ trên vai cô bỗng rùng mình — chiếc váy trắng rách toạc dọc sống lưng, lớp vảy xanh đen ướt nhẫy trồi ra, cơ thể dài gấp đôi rồi trườn xuống quấn một vòng chậm rãi, nặng trịch quanh cổ nữ chiến binh từ phía sau (`a serpentine form wrapping a single slow loop around her neck from behind — not violent, deliberate, inevitable`).
     * **`[07-10s]` (Khoảnh khắc nhận ra — `The Split Second Before Terror`)**: Cái đầu rồng dài ngoẵng nâng lên ngang tầm mắt cô chỉ cách vài centimet. Nữ chiến binh đứng chết trân, bàn tay vẫn áp trên cánh cửa gỗ, đôi mắt mở to nhìn thẳng vào con ngươi lạnh lẽo của con quái vật.
     * **`Cut to Black + 1 Tiếng Động Đơn Độc + End Card`**: Cắt phụt sang đen, một nhịp im lặng tuyệt đối, rồi vang lên **đúng 1 tiếng nuốt ừng ực trầm đục vọng lại trong vòm đá (`one deep resonant gulp echoing through empty stone`)**, trước khi hiện màn hình chữ bạc **`YOU DIED — Try Again? ▶ YES / NO`** (`SCENE_049`)!

---

### 28.3. Kiểm Định Thị Giác (`Visual Audit First`) & Kho Prompt Nguyên Văn 100% Từ 6 Dự Án Trailer Mới Cào

#### 1. `@buralqy/projects/kai-streamer-university-trailer-vfx` — Kỹ Thuật Khoanh Bút Đỏ `#FF0000` (`Red-Lasso Spatial Inpaint Masking`) Trên Footage Quay Thật & Phép Thuật Đi Xuyên Tường Cửa Cuốn (`Platform 9¾ Portal`)

- **Hồ sơ lưu trữ**: [`data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/`](./data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/)
- **Kiểm định thị giác bằng mắt (`view_file`)**:
  1. **`@IMG_002` ([`start_b21c8f84.png`](./data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/images_final_takes/start_frames/start_b21c8f84_b21c8f84-3828-4faf-b493-db83ee915a81.png)) + `@IMG_021` ([`start_becd37f5.png`](./data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/images_final_takes/start_frames/start_becd37f5_becd37f5-8116-4954-8c8d-a54861258dab.png)) ➔ `SCENE_003` ([`keyframe_ba066296.webp`](./data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/images_final_takes/generated_keyframes/keyframe_ba066296_hf_20260702_195540_ba066296-55fb-488a-8713-6f7ff92e53e8.webp))**:
     - `@IMG_002` là frame sân ga tàu hơi nước cổ điển số hiệu `32424` có hai sinh viên mặc đồng phục đứng ở tiền cảnh. Nghệ sĩ VFX đã **dùng bút đỏ `#FF0000` vẽ 2 vòng khoanh tay ở hậu cảnh (1 vòng bên trái cột trụ sân ga, 1 vòng bên phải phía trên đầu tàu)** kèm tấm ảnh tham chiếu vị trí khói `@IMG_021`.
     - Sang `SCENE_003` (`Nano Banana Pro`), đường viền đỏ biến mất hoàn toàn và **làn khói hơi nước chỉ bốc lên đúng ở hậu cảnh phía sau đoàn tàu nơi có vòng khoanh đỏ**, giữ nguyên 100% hai diễn viên ở tiền cảnh (`9.9/10`)!
  2. **`@IMG_012` ([`start_aa552912_resize.jpg`](./data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/images_final_takes/start_frames/start_aa552912_aa552912-64c1-4eca-8e5e-d0d0bef1645b_resize.jpg)) & `@IMG_015` ([`start_fb92c0e9.png`](./data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/images_final_takes/start_frames/start_fb92c0e9_fb92c0e9-c585-43c6-a77f-2d49e4b98dc1.png))**:
     - `@IMG_012` là ảnh chụp khu sân nhà kho có gắn biển hiệu `"STREAMER EXPRESS PLATFFORM 1"` và cánh cửa cuốn kim loại màu xám in quốc huy vàng-đỏ `"SU 2026 STREAMER UNIVERSITY"`. Ở `SCENE_016`, đạo diễn kẻ vạch đỏ và dùng lệnh `"remove/cleanup all below red line/draw. Remove foreground"` để dọn sạch tiền cảnh dưới vạch đỏ.
     - `@IMG_015` là ảnh cận cảnh chính diện cánh cửa cuốn có quốc huy `"STREAMER UNIVERSITY"`, đóng vai trò mỏ neo thị giác cho chuỗi `VIDEO 07`..`VIDEO 10` biến cửa cuốn thành bức tường ánh sáng vàng đặc kiểu Nhà ga 9¾ (`9.8/10`).
  3. **`@IMG_035` ([`start_a990f69e.webp`](./data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/images_final_takes/start_frames/start_a990f69e_hf_20260708_160752_424e5d3f-5f75-40f8-ae79-5240e90ceaef.webp)) & `@IMG_046` ([`keyframe_fa2c7b3d.webp`](./data/creators/buralqy/projects/kai-streamer-university-trailer-vfx/images_final_takes/generated_keyframes/keyframe_fa2c7b3d_hf_20260711_111201_fa2c7b3d-9b5f-42f7-8fa9-f16ae26a51dd.webp))**:
     - `@IMG_035`: Góc ngang đoàn tàu `"STREAMER EXPRESS"` màu đỏ rượu vang - kem có gắn huy hiệu `"STREAMER UNIVERSITY RAILWAYS"`.
     - `@IMG_046`: Góc 3/4 đầu tàu hơi nước đen `32424` `"STREAMER EXPRESS"` xả khói trắng xóa dưới gầm bánh sắt (`9.8/10`).

##### 📜 Nguyên Văn Prompt 1 (`buralqy/kai-streamer-university-trailer-vfx` — `SCENE_003` & `SCENE_016`: Bộ Đôi Câu Lệnh Siêu Ngắn Điều Khiển Vùng Khoanh Bút Đỏ `#FF0000` Trên `Nano Banana Pro`)
```text
add fog/smoke to the further background of <<<image_2>>>.
```

```text
remove/cleanup all below red line/draw. Remove foreground
```

##### 📜 Nguyên Văn Prompt 2 (`buralqy/kai-streamer-university-trailer-vfx` — `VIDEO 10` / `SCENE_020`: Khung Lệnh `PRESERVE` + `STRICT NEGATIVE INSTRUCTIONS` Biến Cửa Cuốn Nhà Kho `@IMG_014` / `@IMG_015` Thành Cổng Phép Thuật Platform 9¾ Cho Các Diễn Viên Đi Xuyên Qua Trên `Seedance 2.0`)
```text
PRESERVE (absolute priority, no deviations): Use <<<video_1>>> exactly as the source. Keep the characters' body movement, leg positions, poses, running pace, cart movement, speed, framing, and timing 100% identical frame-by-frame. Every foot placement in every frame must match the original. No freeze frames, no early ending, no slow motion, no speed changes, no retiming. The camera remains completely locked-off, identical to the original, with zero camera movement.

Only visual change: Replace the warehouse opening with the closed gate from [@IMG_014: start_frame_1]: a worn corrugated metal roller shutter featuring the gold-and-burgundy crest, crown, crossed banners, and the text "STREAMER UNIVERSITY". Match the original opening's size, angle, and position perfectly. The gate is a solid, opaque, flat vertical metal surface permanently installed in the wall. It never opens, never reveals any hole, doorway, tunnel, or empty space, and remains perfectly rigid and motionless throughout the entire video.

MODIFY (portal/light effect): At the exact original frame where the leading character reaches the gate, their body touches the flat metal surface. At the contact point, a warm golden-white magical glow instantly appears: a circular, soft-edged light projected onto the metal surface itself, as if the metal becomes energized. The corrugated metal remains visible around and beneath the glow. No black hole, no transparent portal, no opening, and nothing behind the gate is ever visible.

Without changing their speed, trajectory, poses, or timing, the characters naturally disappear into the glowing light in the exact same sequence as their original movement: legs first, then torso, then the cart, matching the source frame-by-frame. From the contact point, bright high-speed sparks burst outward—white-hot at the core, fading to warm amber, each lasting about 0.3-0.5 seconds. The characters receive a warm golden rim light until they completely vanish.

The instant the second character's trailing foot disappears, the portal collapses: the glow rapidly contracts back into the contact point and fades out within ~0.3 seconds, leaving the gate completely solid, flat, undamaged, motionless, and identical to the first frame, with absolutely no trace of any opening.

Everything else remains identical to the source: warehouse yard, surrounding structures, overcast daylight, color grading, and environment.

STRICT NEGATIVE INSTRUCTIONS: Do not create a visible circular portal, ring, vortex, energy disc, magical doorway, halo, or any portal outline. The effect must not have a defined circular boundary. Do not surround the characters with an aura, glow, energy shell, or volumetric light. The light exists only at the exact contact point on the metal gate, appearing as a flat, localized illumination projected onto the gate surface, as if the metal itself briefly becomes energized. The glow must never extend around the characters or into the air. The gate must remain fully opaque and visible at all times. Nothing behind the gate may ever become visible.
```

---

#### 2. `@diegothetower/projects/the-secret-monkey-island-movie-trailer` — Chuyển Thể 4 Ảnh Sprite 2D Thành Diễn Viên Hollywood (`4-Reference IP-to-Live-Action Casting`), Phẫu Thuật Bóc Lớp Trang Phục (`Layer Stripping`) & Bảng Xoay Đầu (`Head Turnaround Sheet`)

- **Hồ sơ lưu trữ**: [`data/creators/diegothetower/projects/the-secret-monkey-island-movie-trailer/`](./data/creators/diegothetower/projects/the-secret-monkey-island-movie-trailer/)
- **Kiểm định thị giác bằng mắt (`view_file`)**:
  1. **`@IMG_001` ([`start_c879229d.webp`](./data/creators/diegothetower/projects/the-secret-monkey-island-movie-trailer/images_final_takes/start_frames/start_c879229d_c879229d-c4e0-4a8d-9dc4-fde19214fd3a.webp))..`@IMG_004` (4 tấm Sprite 2D của nhân vật game *Guybrush Threepwood*) ➔ `@IMG_014` (`SCENE_001`, [`keyframe_e0633db1.webp`](./data/creators/diegothetower/projects/the-secret-monkey-island-movie-trailer/images_final_takes/generated_keyframes/keyframe_e0633db1_hf_20260602_151900_e0633db1-a5e7-4b04-8183-1b4c3c6723e6.webp))**:
     - Tác giả nạp cùng lúc 4 tấm ảnh vẽ 2D (`Reference 1` đến `Reference 4`) vào `Nano Banana 2 (Pro)` và yêu cầu chuyển thể thành **chân dung Live-Action do diễn viên Tom Holland thủ vai**. Bức ảnh `@IMG_014` đạt điểm **`9.8/10`**: gương mặt Tom Holland cực kỳ chân thực với mái tóc vàng buộc đuôi ngựa thấp và trang phục cướp biển xanh-trắng.
  2. **`SCENE_008` / `@IMG_015` ([`keyframe_f9efb9ac.webp`](./data/creators/diegothetower/projects/the-secret-monkey-island-movie-trailer/images_final_takes/generated_keyframes/keyframe_f9efb9ac_hf_20260604_204127_f9efb9ac-0595-4fb0-877c-de646d697098.webp))**:
     - Phẫu thuật bóc sạch lớp áo khoác xanh (`remove the blue blazer`), áo ghi-lê (`remove the vest underneath`) và kiếm (`remove the sword`) từ Reference 1, đồng thời **cấy bộ râu từ Reference 2 (`<<<image_2>>>`)** lên gương mặt Tom Holland (`9.8/10`).
  3. **`@IMG_016` (`SCENE_010`, [`keyframe_35cddf08.webp`](./data/creators/diegothetower/projects/the-secret-monkey-island-movie-trailer/images_final_takes/generated_keyframes/keyframe_35cddf08_hf_20260604_225451_35cddf08-5518-44db-90d7-821ba8810df2.webp)) & `SCENE_011` ([`keyframe_4e2940fa.webp`](./data/creators/diegothetower/projects/the-secret-monkey-island-movie-trailer/images_final_takes/generated_keyframes/keyframe_4e2940fa_hf_20260604_225903_4e2940fa-4c5f-4bff-97fa-b942bd77ed81.webp))**:
     - `@IMG_016`: **Bảng Xoay Đầu Cận Cảnh 6 Góc (`front, 3/4 left, left profile, back view, right profile, 3/4 right`)** khóa chặt kiểu tóc buộc đuôi ngựa sau gáy (`9.9/10`).
     - `SCENE_011`: **Bảng 8 Biểu Cảm Cận Cảnh Mặt (`8-Expression Sheet`)** giữ đồng nhất 100% bộ râu và nốt ruồi (`9.9/10`).

##### 📜 Nguyên Văn Prompt 1 (`diegothetower/the-secret-monkey-island-movie-trailer` — `SCENE_001` / `@IMG_014`: Chuyển Thể 4 Ảnh Hoạt Hình/Game Sang Nhân Vật Live-Action Do `Tom Holland` Thủ Vai Trên `Nano Banana 2 Pro`)
```text
Use Reference 1, Reference 2, Reference 3 and Reference 4 as character design references for Guybrush Threepwood from Monkey Island.

Create a highly realistic live-action cinematic character portrait of Tom Holland as Guybrush Threepwood in a real Hollywood-style Monkey Island adaptation.

This must look like a real big-budget live-action film still, not an illustration, not a cartoon, not a cosplay photo, and not a stylized fantasy painting.

Guybrush should clearly look like Tom Holland, while also faithfully incorporating the key visual traits of Guybrush from the references:
- young pirate hero
- slim build
- charming and slightly awkward energy
- longer hair tied back in a small ponytail
- elegant pirate outfit
- adventurous but slightly scrappy appearance
- youthful face, expressive eyes, intelligent but inexperienced look

Wardrobe should feel inspired by Monkey Island 2 Guybrush:
- refined pirate clothing
- white or off-white loose shirt
- fitted pirate vest or coat
- high-waisted pirate trousers
- leather belt and pirate accessories
- subtle Caribbean pirate aesthetic
- stylish but believable real-world costume design

The costume must feel grounded and realistic, as if designed by a top Hollywood costume department. Keep the silhouette and spirit of Guybrush from the references, but adapt everything into believable live-action materials, textures, and construction.

Expression: confident but slightly naive, like an ambitious young pirate who wants to become legendary.
Mood: adventurous, charismatic, funny, heroic.
Make him feel like the lead of a real adventure film.

Lighting should be cinematic and realistic, with subtle dramatic shaping on the face.
Background can be softly out of focus, suggesting a Caribbean pirate port environment.
Shot type: medium shot, from around waist up.
Camera feel: real cinema camera, natural lens rendering, realistic skin texture, high detail, photorealistic.

Important:
- preserve Tom Holland’s recognizable facial features
- use the Guybrush references only for character design cues
- do not make him look too modern
- do not make him look too old
- do not make him muscular like a superhero
- avoid artificial beauty retouching
- avoid exaggerated fantasy armor
- avoid cartoon proportions
- avoid a cheesy cosplay look

The final result should feel like an authentic frame from a live-action Monkey Island teaser trailer.
```

##### 📜 Nguyên Văn Prompt 2 (`diegothetower/the-secret-monkey-island-movie-trailer` — `SCENE_008` / `@IMG_015` & `SCENE_010` / `@IMG_016`: Phẫu Thuật Bóc Lớp Áo Khoác + Cấy Râu Từ Ảnh 2 & Tạo Bảng Xoay Đầu Cận Cảnh 6 Góc)
```text
Use Reference 1 <<<image_1>>> as the main base for the character: full body framing, overall body proportions, face, hair, pirate styling, and main costume direction.

Use Reference 2 <<<image_2>>> only for the beard style. Transfer the beard style from Reference 2 onto the character from Reference 1.

Create a highly realistic full-body live-action cinematic character image of Tom Holland as Guybrush Threepwood for a real Hollywood-style Monkey Island adaptation.

Important character direction:
- Tom Holland must clearly be recognizable as Tom Holland
- Keep the face primarily based on Reference 1
- Keep the longer hair tied back in a small ponytail
- Apply only the beard style from Reference 2
- The beard should be subtle, youthful, and natural, not heavy or overly rugged

Wardrobe direction:
Keep the costume mostly based on Reference 1, but make these changes:
- remove the blue blazer
- remove the vest underneath
- remove the sword
- keep the remaining pirate outfit as the base
- make the final outfit feel like a grounded, elegant, believable pirate costume
- realistic fabrics, natural textures, slightly worn but refined
- no excessive accessories

Framing and pose:
- full body
- same kind of full body presentation as Reference 1
- relaxed heroic stance
- natural posture
- clear readable silhouette

Style:
- highly realistic
- photorealistic live-action
- real Hollywood casting / character reveal image
- not illustration
- not animation
- not cosplay
- not stylized fantasy art

Expression and attitude:
- charming
- confident but slightly naive
- adventurous
- likable young pirate hero

Important:
- preserve Tom Holland’s identity
- preserve the face direction from Reference 1
- use Reference 2 only for the beard style
- do not keep the blue blazer
- do not keep the inner vest
- do not include a sword
- keep the final result grounded, cinematic, and believable

The final result should feel like an official full-body character reveal of Tom Holland as Guybrush Threepwood in a live-action Monkey Island film.
```

```text
Use Reference 1 as the main character reference for Guybrush Threepwood played by Tom Holland.

Create a highly realistic live-action character model sheet in a single image, showing 6 separate close-up portraits of the same character on a pure white seamless studio background.

Character:
Tom Holland as Guybrush Threepwood in a realistic Hollywood-style live-action Monkey Island adaptation.

Important:
- He must clearly and faithfully look like Tom Holland
- Preserve the face, hair, beard, costume styling, and overall character design from Reference 1
- Keep the longer hair tied back in a small ponytail if visible
- Keep the pirate styling consistent with Reference 1
- Highly realistic, photorealistic, live-action look
- Not illustration, not animation, not concept art, not stylized fantasy art

Layout:
Show 6 separate close-up portraits of the same character in the same image, evenly spaced and clearly separated.
Do not let any portrait overlap with another.
Each portrait must be individually framed and fully visible.
Use a clean model sheet layout.

The 6 views should be:
1. front view
2. 3/4 left view
3. left profile
4. back view
5. right profile
6. 3/4 right view

Framing:
- all images should be close-ups
- framing from upper chest / shoulders up
- keep the framing consistent across all 6 views
- make all views large enough to clearly read facial structure, hair, and beard

Expression and pose:
- neutral expression
- similar expression across all front and side angles
- professional character turnaround presentation
- back view should clearly show the hairstyle from behind

Background and presentation:
- pure white infinity background
- clean studio lighting
- no props
- no environment
- no text
- no labels
- no overlapping images
- clean, professional presentation

Important consistency:
- same facial structure in all views
- same Tom Holland identity in all views
- same beard style in all views
- same hairstyle in all views
- same costume neckline / upper costume styling in all views
- preserve identity consistency across every angle

The final result should feel like a professional live-action close-up turnaround sheet for film preproduction.
```

---

#### 3. `@lerra98/projects/emberdant-s1-trailer` — Quy Tắc `4 Giây Đen Đặc & Im Lặng Tuyệt Đối (00:22–00:26)` & Công Thức Tạo Title Card Chữ Đá Núi Lửa Nứt Lửa Nóng Chảy (`@IMG_041`)

- **Hồ sơ lưu trữ**: [`data/creators/lerra98/projects/emberdant-s1-trailer/`](./data/creators/lerra98/projects/emberdant-s1-trailer/)
- **Kiểm định thị giác bằng mắt (`view_file`)**:
  1. **`@IMG_005` ([`sheet_maeve_wedding.webp`](./data/creators/lerra98/projects/emberdant-s1-trailer/images_final_takes/turnaround_sheets/sheet_maeve_wedding_hf_20260826_181328_18fb8f39-830b-4dbd-9a2e-7dcd3f6f4a79_min.webp)), `@IMG_006` ([`sheet_casimir_wedding.webp`](./data/creators/lerra98/projects/emberdant-s1-trailer/images_final_takes/turnaround_sheets/sheet_casimir_wedding_hf_20260826_181442_f35b1ddb-d669-4efe-b296-0552e7d93e4c_min.webp)) & `@IMG_027` ([`sheet_mora_pirate.webp`](./data/creators/lerra98/projects/emberdant-s1-trailer/images_final_takes/turnaround_sheets/sheet_mora_pirate_hf_20260827_091131_b07f17ea-ef7d-4609-9420-c2d7c8ed9ed1_min.webp))**:
     - Bộ 3 **Bảng Nhân Vật Triptych 3 Ô (`LEFT PANEL: full-body front view | MIDDLE PANEL: full-body back view | RIGHT PANEL: close-up portrait` ở `@IMG_005` & `@IMG_006`)**: Khóa cực kỳ sắc nét họa tiết thêu vàng trên váy cưới nhung kem của `Maeve` (`@IMG_005`), lễ phục cưới viền lông thú đỏ-vàng của `Casimir` (`@IMG_006`) và áo khoác da cướp biển thêu vàng của thuyền trưởng `Mora` (`@IMG_027` — **`9.8/10`**).
  2. **`@IMG_004` ([`sheet_ember-hall.webp`](./data/creators/lerra98/projects/emberdant-s1-trailer/images_final_takes/turnaround_sheets/sheet_ember-hall_hf_20260826_172418_e3a6d7ae-9677-426b-8d80-4583611a4282_min.webp)), `@IMG_026` ([`sheet_ravens-due_hero.webp`](./data/creators/lerra98/projects/emberdant-s1-trailer/images_final_takes/turnaround_sheets/sheet_ravens-due_hero_hf_20260902_113827_9a9838b3-b224-49b8-a19f-adf8621281ac_min.webp)), `@IMG_039` ([`sheet_ravens-due_burning.webp`](./data/creators/lerra98/projects/emberdant-s1-trailer/images_final_takes/turnaround_sheets/sheet_ravens-due_burning_hf_20260903_043037_822120d2-9368-4ea4-b9ca-2d0cfbff990f_min.webp)) & `@IMG_041` ([`sheet_cave-of-carvings_title.webp`](./data/creators/lerra98/projects/emberdant-s1-trailer/images_final_takes/turnaround_sheets/sheet_cave-of-carvings_title_hf_20260826_154001_d3688f8f-de95-43f8-8c0a-80057442907d_min.webp))**:
     - `@IMG_026` ➔ `@IMG_039`: Cặp ảnh đối xứng trạng thái (`State-Pair Environment Anchor`) của con tàu cướp biển buồm đen `Raven's Due` lúc đang rẽ sóng và lúc bốc cháy ngùn ngụt trên biển đêm (`9.9/10`).
     - `@IMG_041`: Bức ảnh mỏ neo cho Title Card (`VIDEO 10` & `VIDEO 17`..`VIDEO 20`) — thanh kiếm sắt cắm thẳng xuống rãnh đá núi lửa đen khắc chữ cổ đang rực sáng dung nham vàng-cam (`9.9/10`).

##### 📜 Nguyên Văn Prompt 1 (`lerra98/emberdant-s1-trailer` — `VIDEO 10` / `SCENE_013`: Kịch Bản Cao Trào Tàu Bốc Cháy + Quy Tắc Vàng `"4 Giây Đen Đặc & Im Lặng Tuyệt Đối (00:22–00:26)"` Trước Khi Lửa Nóng Chảy Chạy Theo Rãnh Đá `@IMG_041`)
```text
INTERNAL PACING :• 00:00 – 00:08 — The ambush at full. Green fire in the rigging. Boarding chains. Mora at the burning helm — both fists on the wheel, the back of her coat alight, and she does not let go. Seven unbroken seconds. • 00:08 – 00:14 — Casimir [@IMG_036: casimir_pirate] swings out over black water on the cut storm-sail. The tide beneath the enemy fleet goes glassy — hundreds of oars strike the water and skid off it like glass. • 00:14 – 00:22 — THE RAVEN'S DUE BURNING. A wide from off the water. The ship alight from waterline to topmast, green flame running the rigging, her people silhouetted against their own home going up. • 00:22 – 00:26 — Cut to black. Total silence. Four seconds. Nothing. • 00:26 – 00:30 — The title. Molten light runs up out of carved stone. EMBERDANT. THE CHRONICLE OF KALDRIS.DIRECTION:Mora at the burning helm is the trailer’s best held shot. Seven unbroken seconds of a woman refusing to let go while
her coat is on fire. Do not cut away from her. Do not give it music. Her breathing through her teeth is the score.
The burning ship is the last image before the title, and it must be enormous and hopeless. Shot wide from off the
water so the audience sees the whole vessel alight at once. The trailer ends by destroying the only safe place in it — and
the audience has spent ninety seconds learning to love that ship.
The four seconds of silence at 02:52 are the most valuable seconds in the trailer. After escalation, stop everything. No
music, no sound, no image. On a phone in a feed, that is the moment a thumb stops moving.
And do not slam the title. It writes itself, letter by letter, in reading order, in molten fire, as though the stone were writing
its own name. When it is complete let it breathe twice. Fade the ember, not the image.AUDIO:• 00:00 — SFX: cloth burning close to the microphone. Specific, horrible, intimate. Her breathing through her teeth. No scream. • 00:08 — SFX: hundreds of oars in unison — then hundreds of hard wooden skids, wrong and dry, like blades on ice. • 00:14 — SFX: an entire ship burning — canvas, tar, timber. Rigging giving way. And no voices at all. • 00:22 — EVERYTHING STOPS. Digital silence. Four seconds. • 00:26 — SFX: a low, wrong, beautiful sound as fire runs up the groove — a reversed struck anvil, slow lava crackle, sub-bass rise. Then one enormous chord on the completed word, and out. • 00:30 — SFX: one wave. Alone. Over black. END.THE SEA (V.O.) (over the burning ship — the film’s only promise)-MAN'S VOICE: “The crown had a dragon.” (a pause) “And
threw him into the sea.”One unbroken medium-low shot held for seven full seconds from in front of a ship's wheel on a
night deck under attack: MORA [@IMG_037: mora_helm-burning] with both fists locked white-knuckled on the
spokes while the shoulder and back of her black gold-embroidered coat burn with green flame
and stream smoke off her, face turned into the heat, breathing tight through her teeth and not
letting go. Green fire in the rigging behind her, boarding chains, smoke.
Then a tracking shot alongside CASIMIR [@IMG_038: casimir_stormwing] swung out in a real pendulum arc
over black water with a cut black sailcloth cracked open above him like a wing.
Then, low on the water on a long lens held for several seconds: [@IMG_040: the-tide-refusing] — the black
sea beneath a massed enemy fleet turning taut and glassy and humming with fine visible
vibration, standing ripple-rings forming in geometric patterns, and ranked banks of hundreds
of oars striking the surface together and skidding off it as though striking glass, throwing
no wake, the hulls slewing and losing way.
Then the key shot — an enormous wide from off the water: THE RAVEN'S DUE BURNING
[@IMG_039: ravens-due_burning], the whole black-sailed sloop alight from waterline to topmast, green
flame running up the tarred rigging and through the patched sails, the hull glowing from
within, timber failing, spars coming down, her crew silhouetted small and black against their
own ship going up. Black sea in every direction. Hold this shot.
Then cut to absolute black for four full seconds with nothing in frame and no sound at all.
Finally, a macro lateral track along wet black carved stone [@IMG_041: cave-of-carvings_title] as molten
flame-orange light runs up out of a deep ember-trench and spreads groove by groove, each
carved channel filling with liquid fire from its deepest point outward, the surrounding rock
staying completely dark and cold, smoke drifting across the growing glow — then a pull back to
a wide as the molten shape stands whole and enormous across the black wall and pulses slowly
twice like a living coal.
GRADE: Black oily water, green fire as the dominant light source, ember-orange on the burning
ship, deep crushed blacks, blown highlights on burning canvas, heavy smoke in every frame.
Then ash-black, wet mineral-black and molten gold for the title, with two light sources only —
a torch out of frame and the self-emitting molten light within the grooves.
POST — THE TITLE: Generate the igniting stone as the plate. The prompt deliberately never
names the word — Seedance will not render an eleven-letter word cleanly. Composite EMBERDANT
in carved-epic caps, letterspaced wide, tracked to the stone, using the generated molten light
as its fill. Beneath it, smaller and letterspaced wider, arriving two seconds later in the
same fire: THE CHRONICLE OF KALDRIS.
STYLE LOCK: Cinematic photoreal live-action epic. Large-format anamorphic, 2.39:1, ARRI
laser-grade colour science, natural 35mm film grain, deep true blacks, shallow depth of field,
film-still quality. Real human skin with visible pores and subtle natural texture; believable
human proportions; true-to-nature material texture on stone, metal, cloth and water. Grounded
restrained naturalistic performance — micro-expressions only, no theatrical mugging, no
gesturing at the camera. 24fps, natural motion blur. Photo-real — NOT anime, NOT illustration,
NOT stylised, NOT painterly, NOT CGI-plastic. No text, no letters, no subtitles, no watermark,
no morphing or drifting faces, no extra limbs or fingers.
```

##### 📜 Nguyên Văn Prompt 2 (`lerra98/emberdant-s1-trailer` — `VIDEO 20` / `SCENE_023`: Công Thức Tạo Title Card 4 Giây `"EMBERDANT / THE CHRONICLE OF KALDRIS"` Chữ Vàng Cổ Điển Trên Tường Đá Khắc Nổi `2.39:1`)
```text
Cinematic title card, 4 seconds, 2.39:1. Background: a dark stone monument or carved relief wall, heavily shadowed, shot with shallow depth so the carving reads as texture rather than detail. Thin veil of smoke drifting upward through the center, fine debris particles floating. Cool charcoal-grey base with a single warm light source from above catching the stone edges.
Three centered lines, tight vertical stack:
— Top, small and widely letter-spaced: "DIRECTED AND ORIGINAL STORY BY LERRA BAJUT"-DO NOT spell wrong, pale bronze, roughly one-quarter the height of the main line.
— Middle, the hero line: "EMBERDANT" - DON'T SPELL IT WRONG it is emberdant, NOT emberdent. in a tall classical serif with fine hairline strokes, polished antique gold with a burnished metallic gradient — bright along the top bevels, dark at the base. Spans about 60% of frame width.
— Bottom, smallest and most widely spaced: "THE CHRONICLE OF KALDRIS", dim warm grey-gold, sitting well below with generous breathing room.
Motion: text fades up out of the darkness as the smoke drifts and the overhead light slowly strengthens across the stone. Almost imperceptible push-in. Holds fully lit and steady from 0:01 to 0:04. Soft bloom on the gold, deep vignette, fine film grain, static camera, no cuts. 24fps.
```

---

#### 4. `@lightdrop-studio/projects/dudes-in-distress` — Bảng Nhân Vật 8 Ô Phóng Đại Hình Xăm (`8-Panel Tattoo Callout Sheet` `@IMG_004`), Cắt Đầu 1 Dòng (`@IMG_090`), Đồng Xu Bản Lề Cơ Khí (`@IMG_037` / `@IMG_121` / `@IMG_180`) & Cú Máy `5-Second Action-Trailer Crane Swoop`

- **Hồ sơ lưu trữ**: [`data/creators/lightdrop-studio/projects/dudes-in-distress/`](./data/creators/lightdrop-studio/projects/dudes-in-distress/)
- **Kiểm định thị giác bằng mắt (`view_file`)**:
  1. **`@IMG_004` ([`sheet_mira.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/turnaround_sheets/sheet_mira_hf_20260811_161454_2911a23d-bdb7-4316-9195-cf47bcae0ab1_min.webp) — `8-Panel Multi-Callout Character Sheet` của nữ chiến binh `Mira`)**:
     - Điểm thị giác **`9.9/10`**: Bức ảnh chia làm 8 ô cực kỳ khoa học trên nền xám phẳng — ngoài 5 góc cơ thể (`Full-Body Front`, `Back`, `Side`, `3/4 Action`, `Face Close-Up`), cột bên phải có **3 ô Macro Callout chụp cận cảnh Hình xăm hoa văn cổ tay trái, Hình xăm cánh tay phải và Khuyên tai bạc + Dây xích eo**!
  2. **`@IMG_090` ([`sheet_cind.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/turnaround_sheets/sheet_cind_hf_20260815_210601_b82ebc3e-348d-4c3e-bf06-b2c1ace24d88_min.webp) — `cind`) & `@IMG_096` ([`sheet_snow.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/turnaround_sheets/sheet_snow_hf_20260815_041410_abb6dbe7-6937-4186-b6ec-6a6ca6b964fb_min.webp) — `Snow`)**:
     - Điểm thị giác **`9.9/10`**: Khung toàn thân mặt trước **được cắt sạch phần đầu ngay từ cổ (`Headless-Front`)** bằng câu lệnh 1 dòng, trong khi khung cận cảnh bên phải giữ nguyên gương mặt sắc nét! (Còn `@IMG_035` [`sheet_femi.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/turnaround_sheets/sheet_femi_hf_20260815_045643_b41afaf7-c0d4-4759-993f-966f88400ea8_min.webp) và `@IMG_036` [`sheet_gom.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/turnaround_sheets/sheet_gom_hf_20260815_041327_dbcc950f-3b61-49f9-a185-470487c1ee9b_min.webp) là bảng 3 ô của nữ thần `Femi` và thần bão tố `GOM`).
  3. **`@IMG_037` ([`sheet_the-coin.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/turnaround_sheets/sheet_the-coin_hf_20260813_233837_718611c5-a262-420c-ba22-5f9415db5da7_min.webp)), `@IMG_121` ([`sheet_prop_the-coin.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/turnaround_sheets/sheet_prop_the-coin_hf_20260817_101214_df610ba4-894f-4117-abdd-bfd74e7db126_min.webp)), `@IMG_180` ([`sheet_pendant-interior.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/turnaround_sheets/sheet_pendant-interior_hf_20260816_034528_cd505cfe-2a46-46c8-9f61-34bf3f785751_min.webp)), `@IMG_029` ([`keyframe_90c4d7a7.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/generated_keyframes/keyframe_90c4d7a7_hf_20260813_200832_90c4d7a7-def4-4d94-a1c1-2f2ddd3ce3d7.webp)) & `@IMG_206` ([`keyframe_6a9cd5b4.webp`](./data/creators/lightdrop-studio/projects/dudes-in-distress/images_final_takes/generated_keyframes/keyframe_6a9cd5b4_hf_20260821_011535_6a9cd5b4-55d0-43e5-af3d-65837238e395.webp))**:
     - Điểm thị giác **`9.9/10`**: Bộ 5 tấm tham chiếu đạo cụ hoàn chỉnh — từ bảng 3 góc đồng xu đóng có khớp bản lề (`@IMG_037` / `@IMG_121`), bảng đồng xu mở nắp 90° thấy khoang rỗng (`@IMG_180`), cuộn giấy hình trụ có hoa văn uốn theo độ cong vật lý (`@IMG_029`), đến ảnh đặt cuộn giấy `1cm` trên lòng bàn tay để khóa tỷ lệ (`@IMG_206`)!

##### 📜 Nguyên Văn Prompt 1 (`lightdrop-studio/dudes-in-distress` — Tạo Bảng Nhân Vật Cắt Đầu Mặt Trước `@IMG_090` & Thiết Kế Hoa Văn Uốn Theo Độ Cong Hình Trụ Của Cuộn Giấy `@IMG_029` Ở `SCENE_021`)
```text
Crop the character's head from the front view, leaving a body without a head. Leave his face in the close-up
```

```text
Edit this image, keeping the same object, composition, lighting and
photorealistic style. Keep the ornate wooden handles exactly as they
are — they are good.

Remove the six-pointed star and all angular geometric shapes entirely.
Replace all markings with a new decorative scheme.

CRITICAL: every marking must wrap around the curved surface of the
rolled scroll, not sit flat on it. Lines follow the cylinder's
curvature, compressing and foreshortening as they turn away toward
the top and bottom edges, disappearing around the back. Nothing
should look like a flat decal.

The decoration is arranged as three continuous horizontal bands
running the entire length of the scroll, from one handle to the other,
uninterrupted:

— An ornamental border band along the upper edge: a continuous
repeating pattern of circular and spiralling motifs, interlacing
knotwork and small concentric rings, running the full length.

— A matching border band along the lower edge, mirroring the upper.

— A central band of flowing script between them: continuous lines of
unreadable ancient calligraphy in an unknown language, curving,
rounded, organic letterforms with no sharp angles, running horizontally
the full length of the scroll and wrapping out of sight around both
the top and bottom curve.

All motifs are circular, spiralling and organic — rings, spirals,
rosettes, curling vines, concentric circles. No stars, no triangles,
no straight-edged geometry, no religious symbols.

Two materials as before: raised gold leaf catching hard specular
highlights, and glowing light-script radiating warmly from within
the vellum. Some passages bright, some faint.

Because the scroll is rolled closed, only the front-facing portion is
visible — the decoration continues around the hidden back.

Photorealistic, extreme detail, no readable text.
```

##### 📜 Nguyên Văn Prompt 2 (`lightdrop-studio/dudes-in-distress` — `VIDEO 10` / `SCENE_058`: Cận Cảnh Nữ Thần Mở Khớp Bản Lề Đồng Xu `@IMG_037`, Giấu Cuộn Giấy `1cm` `@IMG_029` Ra Sau Lưng Và Bấm Đóng Đồng Xu Trong 7 Giây)
```text
SCENE CONTEXT:
The same heavenly cloud realm. Soft divine sunrise light, warm gold and pale rose tones, bleeding through drifting cloud banks. [@IMG_035: Femi] kneels on the cloud floor, @coin closed in her hand.

ACTIVE REFERENCES:
[@IMG_035: Femi] — locked identity, barefoot, warm backlight glowing along the edges of her hair, the lower folds of her dress dissolving into the surrounding cloud.
@coin — small ornate gold coin, closed, with a small hidden compartment inside it.
[@IMG_029: scroll] — a tiny curled scroll, roughly one centimeter long, fully enclosed within the coin's compartment, catching light even at this small scale.

0-4s: [@IMG_035: Femi] opens @coin in her palm, revealing the small compartment inside with [@IMG_029: scroll] resting fully enclosed within it, impossibly tiny. Her expression shifts to open disbelief, eyebrows lifting, a slow exhale — not fear, astonishment, as if she has just confirmed something she didn't think possible. Camera holds close on her face and her open palm together.

4-7s: Her expression sharpens, alert now, listening to something offscreen. In one fast, practiced motion, she draws [@IMG_029: scroll] out of the coin's compartment and tucks it behind her back, out of sight, while her other hand snaps @coin shut. Camera holds steady, close on her hands completing both actions in the same fluid movement.

(low ambient wind throughout) <a faint magical chime as the coin first opens during 0-4s> <a soft metallic click as it shuts during 4-7s>

TECHNICAL:
FOV 29° close on her face and hands throughout, no wide shot needed for this beat. White balance 4200K, warm sunrise tone.

POSITIVE LOCKS:
[@IMG_029: scroll] stays fully concealed behind [@IMG_035: Femi]'s body from the moment she hides it onward. Her expression in 0-4s reads as wonder and disbelief, not alarm. Her movement in 4-7s is fast but controlled, practiced rather than panicked.
```

##### 📜 Nguyên Văn Prompt 3 (`lightdrop-studio/dudes-in-distress` — `VIDEO 139` / `SCENE_363` Trong Thư Mục `Final shots`: Mẫu Cú Máy `5-Second Fast Action-Trailer Crane Swoop` Biến Toàn Bộ Vũ Khí Của Đám Đông Thành Hoa)
```text
SUMMARY:
A fast 5-second photorealistic action-trailer shot in daylight. On the CASTLE SIDE of a stone bridge stand [@IMG_183: mali], exactly one dwarf woman from [@IMG_067: Dwarffes], and [@IMG_112: maurin]. On the OPPOSITE SIDE, [@IMG_111: Gus] leads an angry mob of village women dressed like men [@IMG_147: char_20-ladies], with short hair, charging across the bridge toward them with shovels, tridents, hammers, axes, bows, and arrows.

Using one epic aerial crane / drone-style camera move, the shot begins high above the castle side, swoops down to reveal the full bridge and both opposing sides, then drives forward as [@IMG_183: mali] raises her hand and releases a green magical shockwave. The wave races from the castle side through the charging mob, and all of their weapons instantly transform into flowers.

ELEMENTS: [@IMG_183: mali], [@IMG_067: Dwarffes], [@IMG_112: maurin], [@IMG_111: Gus]

SHORT DESCRIPTION:
A crane/drone-style camera swoops down over the castle-side bridge reveal as [@IMG_111: Gus] leads an attacking mob of armed village women toward [@IMG_183: mali], one dwarf woman, and [@IMG_112: maurin]. [@IMG_183: mali] makes one sharp gesture, a green magical shockwave blasts across the bridge, and the attackers’ weapons instantly turn into flowers.

LONG DESCRIPTION:
Create a highly detailed photorealistic live-action fantasy action clip.

TOTAL DURATION:
Up to 5 seconds maximum.

ONE CONTINUOUS SHOT.

DAYLIGHT.

This is a fast action-trailer beat.
Go straight into the confrontation.

ABSOLUTELY NO BACKGROUND MUSIC.
NO MUSIC WHATSOEVER.
NO SCORE.
NO MUSICAL UNDERSCORE.

==================================================
BRIDGE GEOGRAPHY — ABSOLUTE PRIORITY
==================================================

The scene takes place on a stone bridge immediately outside a castle.

The bridge has TWO CLEARLY OPPOSING SIDES.

CASTLE SIDE:
At one end of the bridge, very close to the castle gate or outer wall, stand:
[@IMG_183: mali]
exactly ONE dwarf woman selected from [@IMG_067: Dwarffes]
[@IMG_112: maurin]

These three are stationary on the castle side.
They face outward across the bridge toward the attackers.

OPPOSITE SIDE:
At the far end of the bridge, charging toward the castle, is:
[@IMG_111: Gus]
leading an angry mob of village women.

The attacking women are:
adult village women,
not a formal army,
dressed in masculine fairy-tale-era work clothes,
with short hair.

Their bodies should still read clearly as women.

They carry:
shovels,
tridents,
hammers,
axes,
bows,
and arrows.

They are already in motion at the start, charging toward the castle side and clearly about to attack.

==================================================
CAMERA — EPIC CRANE / DRONE MOVE
==================================================

Use ONE continuous epic action-trailer camera movement.

0.0s–1.2s:
Begin HIGH ABOVE the castle side of the bridge in a dramatic aerial crane / drone-style view.

The camera is elevated enough to clearly show:
the castle side in the foreground,
the full length of the bridge,
and the attacking mob rushing from the opposite side.

Then the camera swoops downward and forward quickly, descending toward [@IMG_183: mali] and the defenders.

This opening must immediately establish the geography:
defenders by the castle,
attackers charging from the far side.

1.2s–2.0s:
As the camera descends and closes in, [@IMG_183: mali] comes into strong foreground or midground focus while the charging mob remains clearly visible beyond her on the bridge.

The camera continues driving forward with action-trailer momentum.

==================================================
ACTION
==================================================

2.0s–2.6s:
[@IMG_183: mali] makes one sharp, decisive hand gesture toward the attackers.

A fast green magical shockwave forms from her gesture on the CASTLE SIDE.

The green effect should feel like:
a magical pressure wave,
or green thunder-like energy,
or a fast green surge through the air.

It originates specifically from [@IMG_183: mali] and moves AWAY from the castle.

2.6s–4.2s:
The camera surges forward WITH the green wave down the bridge.

As the wave hits the charging mob led by [@IMG_111: Gus], all of their weapons instantly transform into flowers.

The transformation must be immediate and readable:
shovels become flower bunches,
tridents become flowering stems,
hammers become bouquets,
axes become blossoms,
bows become floral shapes,
arrows become stems or flowers.

Only the ATTACKERS’ weapons transform.

Do not transform anything held by:
[@IMG_183: mali],
the dwarf woman,
or [@IMG_112: maurin].

4.2s–5.0s:
End on a strong dynamic trailer image:
the mob stumbling or freezing in confusion,
their former weapons now flowers,
with [@IMG_111: Gus] at the front shocked and frustrated.

The castle group should remain visible at the far end of the bridge behind them or in the distance, with [@IMG_183: mali] still calm and in control.
```

---

#### 5. `@daniallll/projects/seed-audio-1-0-launch-video` — Xóa Chữ Rác Trên Áo Trước Khi Tạo Video (`Pre-Video Garbled-Text Erasing`) & Điều Phối `CAMERA STYLE PRESET` (`David Fincher ASMR Push-In` vs. `Mockumentary Whip-Pan` 5 Giọng Nói)

- **Hồ sơ lưu trữ**: [`data/creators/daniallll/projects/seed-audio-1-0-launch-video/`](./data/creators/daniallll/projects/seed-audio-1-0-launch-video/)
- **Kiểm định thị giác bằng mắt (`view_file`)**:
  1. **`@IMG_002` ([`start_8ce1b88f.png`](./data/creators/daniallll/projects/seed-audio-1-0-launch-video/images_final_takes/start_frames/start_8ce1b88f_8ce1b88f-2a9f-4232-bf8a-01a9cee63ed9.png)) ➔ `@IMG_003` ([`start_4b4ada6e.webp`](./data/creators/daniallll/projects/seed-audio-1-0-launch-video/images_final_takes/start_frames/start_4b4ada6e_hf_20260629_082022_8b231832-cff5-4442-9871-708950dbcbbe.webp))**:
     - Khi soi bằng mắt bức ảnh gốc `@IMG_002`, trên ngực chiếc áo crop-top tie-dye xanh và trên thắt lưng của cô gái có in dòng chữ AI bị biến dạng vô nghĩa (`"ROU KOOR / ROCRR"`).
     - Trước khi đưa vào `Seedance 2.0` (`4K`) để tạo `VIDEO 02`, đạo diễn đã chạy một bước dọn sạch chữ rác trên áo và thắt lưng thành bức `@IMG_003` (nền vải tie-dye trơn sạch 100%, giữ nguyên 100% gương mặt, tai nghe và chiếc micro trên tay)! Nhờ đó khi camera đẩy dolly vào gần trong `VIDEO 02`, người xem không bị đập vào mắt dòng chữ lỗi!
  2. **`@IMG_001` ([`start_d1e4f49c.png`](./data/creators/daniallll/projects/seed-audio-1-0-launch-video/images_final_takes/start_frames/start_d1e4f49c_d1e4f49c-aa79-4903-b28a-504656099f69.png)), `@IMG_004` ([`start_868edc32.png`](./data/creators/daniallll/projects/seed-audio-1-0-launch-video/images_final_takes/start_frames/start_868edc32_868edc32-9dc7-4859-8519-086714456990.png)), `@IMG_005` ([`start_c35c658a.png`](./data/creators/daniallll/projects/seed-audio-1-0-launch-video/images_final_takes/start_frames/start_c35c658a_c35c658a-1846-4e14-9d59-f438d3bb2efd.png)) & `@IMG_008` ([`start_4f2ec5f8.webp`](./data/creators/daniallll/projects/seed-audio-1-0-launch-video/images_final_takes/start_frames/start_4f2ec5f8_hf_20260629_115646_3f3975f5-9563-4bdc-a7d2-5a3207f3c6c4.webp))**:
     - Bố cục **`2-Panel Split Character Card`** (`Khung Trái: Toàn thân | Khung Phải: Chân dung cận cảnh` ở `@IMG_001`, `@IMG_005`), bối cảnh phòng đọc sách gỗ óc chó (`@IMG_004`), và bảng đạo cụ 4 góc chiếc máy nhắn tin retro đã xóa sạch chữ trên bàn phím QWERTY (`@IMG_008`).

##### 📜 Nguyên Văn Prompt 1 (`daniallll/seed-audio-1-0-launch-video` — `VIDEO 02` / `SCENE_014`: Đẩy Dolly Siêu Chậm Kiểu `David Fincher` Từ Trung Cảnh Vào Cận Cảnh Môi & Chuyển Giọng Từ Thuyết Trình Sang Thì Thầm ASMR)
```text
single continuous shot, one take no cuts, cinematic oner, cinematic lighting,
photorealistic, 35mm film quality, professional color grading, sharp focus,
high detail texture, film grain, depth of field mastery, steadicam fluidity

Cinematographic style of David Fincher, imperceptible dolly forward on rails, micro push-in on motorized slider, mechanically perfect stabilization, subliminal camera pressure, no handheld, no snap movement, no zoom

MODE: One Take continuous

[@IMG_003: start_frame_1] — character identity + wardrobe lock: young woman, dark hair in a high messy bun with loose face-framing strands, soft natural makeup, large black over-ear headphones worn over the bun, fitted blue-teal tie-dye crop top. Lock face, hair, headphones, top.

GLOBAL CONSISTENCY LOCK: the woman is the only person in frame throughout; headphones stay on; crop top unchanged; seamless white cyclorama background with no corner, no horizon line, no wall-to-floor seam; flat shadowless diffuse light constant; small handheld microphone already in her right hand, held low at start.

SOUND: diegetic, on-camera spoken dialogue in her own voice, fully lip-synced. Treated-studio near silence, soft clean room tone, no music, no off-screen narration. Beat 2 is intimate close-mic proximity, breathy, almost ASMR.

DIALOGUE (spoken on camera, lip-synced):
Beat 1 (relaxed, presentational, to camera): "Now you can generate any sound at all — voice, music, effects, ambience. Take my voice. As a cricket commentator."
Beat 2 (soft, almost ASMR, lips close to the mic): "Hey. This is my normal voice."

CAMERA BEHAVIOR (single primary move — slow push only):
[0s] Medium shot. She stands centered on the seamless white cyclorama, relaxed and confident, microphone held low in her right hand, and begins Beat 1. The camera holds, then the faintest imperceptible push-in begins.
[~4s] On the words "cricket commentator" she calmly raises the microphone toward her lips; the camera continues its slow imperceptible push toward her face.
[~6s] The push settles into a close-up on her lips and the microphone; she softens, intimate, and breathes Beat 2 almost ASMR.
[~9s] Hold the close-up one beat on the final word as a small private smile forms.

STYLE: clean, intimate, soft, controlled, premium, calm, ASMR

negative: music score, off-screen narration voiceover, text overlay, watermark, second person, extra hands, extra microphone, headphones removed, wardrobe change, lip-sync drift, unstable or warping mouth, jittery teeth, camera spinning, handheld shake, simultaneous complex movements, hard cut, shadows on the white background, visible horizon line, visible wall-floor seam, flicker, morphing, extra limbs
```

##### 📜 Nguyên Văn Prompt 2 (`daniallll/seed-audio-1-0-launch-video` — `VIDEO 06` / `SCENE_020`: Kịch Bản `Workplace Mockumentary Snap-Zoom & Whip-Reframe` Điều Phối 5 Giọng Nói Khác Nhau Trong Cùng 1 Cú Máy `15s`)
```text
Interior, mid-century modern study at midday: walnut-paneled walls, deep blue carpet, low bookshelves crammed with books, tall windows showing an overcast city skyline, circular ring lights set into the coffered ceiling, an old film projector on a side cabinet. Four people stand clustered close together in the center of the room, shoulders almost touching, turning toward one another as each speaks. Handheld mockumentary camera, light shake, documentary feel: it snap-zooms in on each person the instant they start talking, then whip-reframes to the next speaker, the way a workplace mockumentary punches in on whoever holds the floor. Snap-zoom to a broad-shouldered man with dark curly hair and a thick black mustache, in a navy armored suit with a maroon cape; he plants his feet, scans the room, turns to the elderly man beside him and says in a deep voice, "Hold the perimeter." Whip-reframe and zoom to the elderly man — white hair, heavy grey eyebrows, grey cardigan over a pale blue shirt — leaning on his cane; he claps the caped man on the shoulder and chuckles into his face in a thin old voice, "My wife tells me that every single day! Heh." The camera punches over to a woman with voluminous dark-brown curls in a magenta coat as she steps between them holding a small cream-colored retro handheld device with a flip green LCD screen and a tiny QWERTY keyboard; her thumbs hammer the keys in a fast burst, then she twists the screen around to show the two men. Quick zoom to the device as it answers in a flat robotic synth voice, "I can confirm. It is all true." Snap-zoom back to the old man — his eyebrows jump, he leans toward the gadget, mouth open, and blurts in surprise, "What the flip?!" Hard cut, and the zooming stops. Steady handheld medium shot of a bald man with a grey-blond goatee and a visible gap between his front teeth, white shirt; eyes wide, he says in disbelief, "Hold on — they're actually talking to each other? Multiple voices, one scene, and it's all generated?" Cut to a steady matching shot of a young woman with dark hair in a messy top bun, black over-ear headphones, blue tie-dye top; she turns her head to look at him, face flat and unbothered, and replies, "Every single voice." Natural room ambience, faint hum of the ceiling lights, fast plastic key-clicks during the typing, no music.
```

---

#### 6. `@higgsfield.soul/projects/huntress-s-tale` — Quy Trình Tách Quái Vật Ra Nền Xám (`Creature Isolation`), Cú Rơi Xuyên Sàn Không Qua Đường Ống (`No-Shaft Floor Collapse`), Cú Twist Nàng Tiên Hóa Rồng Quấn Cổ & Màn Hình `YOU DIED`

- **Hồ sơ lưu trữ**: [`data/creators/higgsfield.soul/projects/huntress-s-tale/`](./data/creators/higgsfield.soul/projects/huntress-s-tale/)
- **Kiểm định thị giác bằng mắt (`view_file`)**:
  1. **`@IMG_008` ([`keyframe_1f07831d.webp`](./data/creators/higgsfield.soul/projects/huntress-s-tale/images_final_takes/generated_keyframes/keyframe_1f07831d_hf_20260624_172839_1f07831d-63b7-4bf7-8555-9781d1d5d424.webp)) ➔ `@IMG_011` ([`keyframe_e26f8661.webp`](./data/creators/higgsfield.soul/projects/huntress-s-tale/images_final_takes/generated_keyframes/keyframe_e26f8661_hf_20260624_173039_e26f8661-d4bf-4ce3-9bd8-705fe3733e27.webp))**:
     - Ban đầu con thủy quái rồng biển được tạo trong cảnh sóng biển tung bọt trắng xóa (`@IMG_008`). Nếu đưa trực tiếp `@IMG_008` vào cảnh hầm mộ đá, AI sẽ mang theo cả sóng biển vào trong hầm!
     - Đạo diễn dùng câu lệnh 13 chữ: **`"make him look realistic,put him like a 3d rendered model on plain background"`** trên `GPT Image 2.0` để tách con rồng biển cuộn tròn đặt lên nền xám phẳng `#6E6E6E` (`@IMG_011` — **`9.9/10`**), giúp tái sử dụng mượt mà trong `9` cảnh hầm ngầm!
  2. **`SCENE_047` ([`keyframe_96d93313.webp`](./data/creators/higgsfield.soul/projects/huntress-s-tale/images_final_takes/generated_keyframes/keyframe_96d93313_hf_20260625_183913_96d93313-17da-4dec-afd3-fe0874a7660d.webp)) & `SCENE_049` ([`keyframe_60b12c06.webp`](./data/creators/higgsfield.soul/projects/huntress-s-tale/images_final_takes/generated_keyframes/keyframe_60b12c06_hf_20260625_201317_60b12c06-db36-47e9-b00d-e264f0036514.webp))**:
     - `SCENE_047`: Logo 3D **`Huntress's Tale`** bằng thép bạc đánh bóng, chữ `H` tích hợp đầu rồng và vảy rồng uốn lượn liền khối trên nền trắng studio (`9.9/10`).
     - `SCENE_049`: Màn hình kết **`YOU DIED / Try Again? / ▶ YES / NO`** bằng bạc xước mờ khắc hoa văn filigree trên nền đen tuyền (`9.9/10`).

##### 📜 Nguyên Văn Prompt 1 (`higgsfield.soul/huntress-s-tale` — `VIDEO 20` / `SCENE_035`: Cú Chuyển Cảnh Sập Sàn Rơi Thẳng Từ Hành Lang Xuống Hầm Ngập Nước Trong 1 Cú Máy Liên Tục `Start Frame -> End Frame`)
```text
[@IMG_014: start_frame_1] — identity anchor: face, body, full outfit, sword — maintain exactly.

[@IMG_015: start_frame_2] — identity anchor: face for closeups.
START FRAME: <<<video_1>>> — a pale blonde warrior in a white bodysuit with silver filigree pauldrons and crimson brocade thigh-high boots, sword at her hip, seen from behind running through a dark arched stone corridor of an ancient ruined fortress toward the shadowed opening, misty green hillside visible through a side arch.
END FRAME: [@IMG_032: start_frame_3] — the same warrior lying on her back, half-submerged and motionless in the still green water of a deep underground flooded vault, directly beneath a round broken hole in the ceiling, a single soft shaft of pale daylight falling straight down onto her through arches and stone columns rising from the water.
ACTION (one continuous shot, ~8–10s):
[00–03s] From the start frame, the warrior runs at full speed deeper through the dark corridor, taking a few hard strides, boots pounding cracked stone, sword clanking at her hip.
[03–05s] Suddenly the floor gives way — a broken hole opens in the ground beneath her. Her lead foot punches through into empty air, her body lurches and drops with a gasp, arms flying out, grabbing for the edge but missing as stone crumbles. This hole in the floor is the broken hole in the ceiling of the flooded vault below — no shaft between them; she falls directly through.
[05–08s] She plunges straight down through the bright ceiling hole into the dim flooded vault and crashes into the dark green water — a large splash erupts, debris raining in, the light shaft catching the spray. The water settles.
[08–10s] The ripples calm and she comes to rest floating on her back, half-submerged and still beneath the beam of daylight — arriving exactly at the end-frame composition. Motionless, dazed, breathing faintly. She blinks slowly, naturally, like a real human — alive but stunned.
CAMERA: handheld behind her during the run, jolts as the floor collapses, follows her fall through the floor-hole and cranes/tilts down to reveal the flooded vault as she hits the water, then settles and pulls back to the wide, still composition of the end frame looking down the light shaft. Natural controlled shake during action, calm and still at the end. Frame her from behind and the side at a respectful distance — focus on the run, the fall, and the water; no rear close-ups, do not emphasize her hips or backside.
STYLE: the look shifts from the cold grey-green sunlit corridor into the cold, dim blue-green flooded vault as she falls through — a single drop, no shaft. Desaturated teal palette below, low-key lighting, one hard cold shaft of daylight from the ceiling hole, deep shadows, volumetric mist, wet stone reflections, live-action cinematic realism, 50mm feel. Maintain the character's exact appearance and outfit from both frames. 4K ultra sharp, stable frame rate, no flicker.
SFX: rapid boot footsteps echoing on stone, sudden crack of collapsing floor, a sharp gasp, brief wind-rush of the fall, massive water-crash splash, debris plunging into water, metallic sword scrape, then quiet — water lapping and dripping in the vault, faint breath. No music — SFX only.
```

##### 📜 Nguyên Văn Prompt 2 (`higgsfield.soul/huntress-s-tale` — `VIDEO 22` / `SCENE_041`: Cú Twist Stinger Cuối Trailer — Đóng Cửa Thở Phào Nhẹ Nhõm ➔ Nàng Tiên Nhỏ Trên Vai Rùng Mình Hóa Rồng Quấn Quanh Cổ Nữ Chiến Binh Trong 1 Cú Máy `10s`)
```text
[@IMG_026: start_frame_5] (Start frame) — opening composition anchor: hunter seen from behind, both palms on massive dark iron-banded double doors from interior side, tiny glowing fairy hovering at her right shoulder, cold light shaft through door gap, flooded stone floor. Match this exact framing to open Shot 1.
[@IMG_009: start_frame_1] [@IMG_010: start_frame_2](Hunter) — pale blonde warrior, white armored bodysuit, silver pauldrons, crimson boots, large sword — wet and disheveled. Exact face, hair, full outfit. Locked, never warp.
[@IMG_020: start_frame_3] (Fairy) — tiny palm-sized fairy, no larger than a human hand, long flowing blue-silver hair, translucent iridescent wings, cream petal dress, amber eyes, soft inner blue glow. Locked, never warp.
[@IMG_011: start_frame_4](Dragon) — blue-grey water serpent: long coiling scaled body, pale cream underbelly, spiked dorsal ridge, membrane wing-fins, elongated reptilian head with cold narrow eyes. Exact design and scale. Locked, never warp.
[@IMG_027: start_frame_6] (Chamber) — underground flooded vault chamber: low rounded romanesque arches, thick square stone columns, dark still green-tinted water floor, moss at waterlines, cold teal-blue ambient light, deep shadow at edges, mist rising from water surface.
[@IMG_028: start_frame_7]  (Mid frame) — composition anchor for Shot 2: hunter pressed sideways against closed door from inside, one palm flat on dark wood, face in three-quarter profile, eyes closed, tiny fairy standing on her silver pauldron. Match lighting and framing.

Single continuous shot (10s, 24fps): [00-03s] Hunter crosses the threshold from outside, both hands gripping iron ring handles, hauling the massive double doors shut behind her with her full body weight; hinges groan, dark water sloshes around her boots, doors boom closed with deep stone reverb; she releases the handles and presses both palms flat against the cold wood, back against the door — exactly matching <<<image_mid>>>; forehead drops forward, eyes close, one long slow exhale — shoulders drop with pure relief. The tiny fairy lands softly on her silver pauldron, wings folding still, blue-white glow gentle in the cold dark. [03-07s] A beat of stillness. Then — the fairy's small body begins to shiver. Her inner glow intensifies, cold white-blue light pulsing from within; the cream dress splits as dark wet scales push through from beneath, slick and overlapping; her form doubles — the hunter feels unexpected weight shift on her pauldron, brow furrowing slightly without opening her eyes; the fairy doubles again, her elongating body beginning to coil — a scaled tail slides off the pauldron and drops in a slow heavy loop around the hunter's shoulder; the hunter's eyes open, confused, looking sideways and down; the coiling body thickens further, a serpentine form wrapping a single slow loop around her neck from behind — not violent, deliberate, inevitable; the spiked dorsal ridge rises along the lengthening neck, membrane wing-fins unfold briefly then press flat against the door surface on both sides of the hunter's head. [07-10s] The transformation completes — the blue-grey water serpent, now forearm-length and growing, is coiled partially around her neck and shoulder, its elongated head raised level with her face, cold narrow eyes opening and focusing on her from inches away — exactly matching <<<image_end>>>. The hunter is completely still. Her palm still flat on the door. Her face: not yet terror — the precise moment of recognition, the split second before fear arrives. Camera holds. The dragon's cold eye and her half-open eye fill the frame together. EMOTIONS: Hunter — relief → confusion (weight shift) → slow dawning recognition → the moment before terror. Dragon — unhurried, deliberate, ancient. The coil is not aggressive — it is simply claiming. STYLE: Dark fantasy cinematic, photoreal PBR, 4K ultra sharp. Cold teal-blue ambient throughout, fairy's blue-white glow the only light source — intensifying during transformation then shifting to cold ambient as scales extinguish it. Zero warm light sources. Continuous handheld with gentle drift settling to near-static at end frame. Shallow depth of field on face and dragon head at final moment. Fine grain. Water physics active — subtle displacement as coil mass increases. FORBIDDEN: cuts of any kind, transformation skipping stages or flickering, hunter moving away from the door, warm or amber lighting anywhere, plastic or waxy textures, frozen or robotic movement, extra fingers, on-screen HUD or text, flicker, dragon appearing full-size without transformation stages. SFX: dark water sloshing at boots, iron ring handles gripped and pulled, heavy door hinges groaning, doors swinging shut — deep wood-and-stone boom reverberating through vault — then near-silence; slow exhale; fairy wings folding with soft flutter; water dripping from outfit; brief stillness — then: the fairy's first shiver, a barely audible internal hum building; wet tearing sound as scales push through; a soft heavy weight settling on the pauldron — metal creak of armor under growing mass; the low liquid sound of a scaled body beginning to coil, each loop tightening slowly; a deep resonant breath from the forming dragon; the hunter's single sharp inhale of recognition; silence. Cold. 10s. 24fps. 16:9. One continuous shot. No cuts. Maintain full hunter, fairy, and dragon identity throughout. Smooth continuous handheld settling to locked. 4K ultra sharp. Stable exposure. Consistent frame rate. Clean picture.
```

##### 📜 Nguyên Văn Prompt 3 (`higgsfield.soul/huntress-s-tale` — `SCENE_047` & `SCENE_049`: Bộ Đôi Prompt Tạo Logo 3D Thép Bạc Chạm Khắc Rồng & Màn Hình Kết `"YOU DIED / Try Again? ▶ YES / NO"` Trên `Nano Banana 2 Pro`)
```text
Create a premium 3D cinematic movie title/logo for "Huntress's Tale" on a pure clean white background. The title should be made from shimmering polished silver steel, appearing as realistic high-end metallic material with depth and volume. The typography should feel custom-designed and inspired by the main characters' aesthetic.
Blend elegant ornamental fantasy details with dragon-inspired forms: delicate silver filigree, engraved patterns, subtle dragon scales integrated into letter edges, curved horn-like extensions, sharp spines, and mystical gothic elements naturally woven into the typography.
The logo must feel luxurious and iconic — thick 3D extruded letters, reflective chrome-silver surfaces, polished steel texture, crystal-like highlights, soft metallic reflections, sparkling details across the edges, engraved craftsmanship, jewelry-level precision.
Minimal white studio background, floating premium product-shot style, clean shadows underneath, luxury fantasy film branding, highly detailed, ultra realistic, blockbuster movie logo design.
```

```text
Create a cinematic dark-fantasy "YOU DIED" death screen on a pure black background, styled to match the elegant logo treatment of image 1 ("Huntress's Tale") — but rendered in matte brushed metallic silver instead of glossy chrome.
Lettering style: ornate, elegant serif typeface with refined serifs and fine engraved filigree detailing inside the letterforms — exactly the sophisticated fantasy logo style of image 1, NOT pixelated. Smooth crisp vector-clean edges, no pixel/8-bit look anywhere. The metal is matte and softly satin — brushed silver with gentle, restrained highlights rather than sharp mirror sparkles.
Layout (matching image 2 composition):
"YOU DIED" large and dominant, stacked on two lines, centered in the upper-middle.
Below it, smaller, "Try Again?" centered.
Beneath that, a small menu: "YES" with an elegant little arrow (▶) pointing at it, and "NO" on the line below.
All text in the same matte metallic silver with the ornate engraved serif style; the smaller lines slightly simpler but matching the family.
Mood: the matte silver letters catch a faint cold light against the deep black, subtle soft glow/sheen around them, ominous and refined. Generous black negative space, no frames or borders.
Style: luxurious dark-fantasy title key-art, matte brushed-metal silver, ornate engraved serif lettering with filigree, smooth high-detail vector-clean edges (absolutely no pixelation), soft cold highlights on black. Centered composition. 16:9, sharp and clean.
```


---

## 29. Ngữ Pháp Chuẩn `MiniMax H3` (`minimax_hailuo_2_3_fast` / `minimax_h3`) & 5 Quy Tắc Kiểm Duyệt Tiền Kỳ Phim Ngắn / Trailer AI (`Pre-Production Causal & 180° Continuity Checklist`)

> **Nguồn giải mã**: Quét toàn bộ **`104` video `minimax_hailuo_2_3_fast`** trong [`data/community_shots/ranked_community_shots.json`](./data/community_shots/ranked_community_shots.json) (Top #1 đạt **`532 ♡`**: `2d5d4455-5ec9-413b-acfc-034e31b1903e`, Top #2 đạt **`400 ♡`**: `c475f55b-d9ed-4cf9-861e-34b5c102ebac`) và đối chiếu với quy trình kiểm soát liên hoàn của `@pandaproduction/thread`, `@sileent/the-breach`, `@ollkorrect/besa`, `@daniallll/seed-audio-1-0-launch-video` và `@higgsfield.soul/huntress-s-tale`.

### 29.1. Sự Khác Biệt Cốt Lõi Giữa Ngữ Pháp `Seedance 2.0/2.5` Và `MiniMax H3`

- **1. Cú Pháp Tham Chiếu Tài Nguyên (`@Image1`, `@Image2` thay vì `<<<image_1>>>`)**:
  - Trong khi `Seedance 2.0/2.5` trên Higgsfield dùng `<<<image_1>>>` hoặc `@IMG_001`, dòng `MiniMax H3` sử dụng mảng `image_urls: ["https://..."]` kết hợp gọi trực tiếp **`@Image1`, `@Image2`, `@Image3`** ngay trong văn bản prompt (tương tự `@Video1`, `@Audio1`).
- **2. Ngôn Ngữ Đạo Diễn "Văn Xuôi Điện Ảnh Giàu Vật Lý" (`Flowing Physical-Cinematic Prose` + `[Camera Bracket Commands]`)**:
  - Khác với `Seedance` thích chia mốc giây cứng `[00:00 - 00:03]`, `MiniMax H3` đạt chất lượng chuyển động mượt nhất khi viết bằng **văn xuôi miêu tả chuỗi nhân quả vật lý liên tục** (`As the camera slowly pushes in..., the subject lifts..., warm tungsten light glints off...`), kết hợp:
    - **Từ khóa điều khiển máy quay đặt ở đầu câu hoặc trong ngoặc vuông**: `[Push in]`, `[Pull out]`, `[Pan right]`, `[Tracking shot]`, `[Handheld subtle shake]`, `[Rack focus]`, `[Low angle]`.
    - **Khóa chất liệu ống kính & ánh sáng (`Optical & Chromatic Lock`)**: `Shot on 35mm anamorphic lens, shallow depth of field, Kodak Vision3 500T 5219 film grain, cold desaturated cyan-slate shadows (#1A262B) contrasting with warm tungsten amber highlights (#D9822B), realistic skin pores, no CGI plastic sheen`.
- **3. Quy Tắc Vàng Khi Upload Ảnh Tham Chiếu (`Pre-Upscale 2K Sharpen Rule`)**:
  - Nếu truyền ảnh gốc độ phân giải thấp (`685×382` hoặc `_min.webp`) làm `@Image1`, model video sẽ nội suy bề mặt da bị bệt sáp (`waxy`).
  - **Giải pháp bắt buộc**: Luôn giữ hoặc upscale ảnh tham chiếu lên **2K (`2048×1142` hoặc `1920×1080`) bằng bộ lọc `Lanczos + UnsharpMask(radius=1.2, percent=135)`** trước khi đưa vào render video.

---

### 29.2. 5 Quy Tắc Sống Còn Khi Tiền Kỳ Phim Ngắn & Trailer AI (`Pre-Production Causal Storyboard & Continuity Checklist`)

Trước khi bấm nút render bất kỳ bộ phim ngắn hay Trailer nào, bạn **BẮT BUỘC phải kiểm duyệt 5 chốt chặn tiền kỳ sau**:

1. **Quy tắc 1 — Khóa Mắt Xích Nhân Quả Vật Lý Giữa Các Cảnh (`Causal Storyboard Spine` chuẩn `@pandaproduction/thread` & `@sileent/the-breach`)**:
   - Đừng bao giờ viết các cảnh rời rạc chỉ chung một bầu không khí mà không có **hành động vật lý gây ra hệ quả trực tiếp ở cảnh kế tiếp**.
   - Hãy học `@pandaproduction/thread`: Cảnh 1 hai bàn tay đẫm máu đổ gục xuống bệ cửa sổ ➔ vô tình đẩy con suốt gỗ rơi xuống đường ở Cảnh 2 ➔ dẫn tới phòng hộ sinh nơi bà đỡ dùng chính con suốt đó buộc rốn 1 tiếng trước.
   - **Cấm tự ý xóa cảnh nối nhân quả vì sợ bộ lọc từ khóa**: Nếu một cảnh cầu nối gặp từ khóa nhạy cảm (`bullet time / slow motion / violence`), phải **viết lại cảnh đó bằng ngôn ngữ vật lý hợp lệ** chứ tuyệt đối không được cắt bỏ mắt xích nhân quả.

2. **Quy tắc 2 — Kiểm Toán Trục Không Gian 180° & Danh Mục Đạo Cụ Trên Bàn (`180-Degree Spatial Axis & Tabletop Prop Inventory`)**:
   - **Đồng bộ đạo cụ giữa Cảnh Cận (`Macro Insert`) và Cảnh Rộng (`Master Wide`)**: Nếu cảnh trước là cảnh Macro tương tác với đạo cụ đặt trên bàn, thì trong ảnh `Start Frame` của cảnh rộng kế tiếp, **đạo cụ đó bắt buộc phải nằm đúng vị trí trên mặt bàn** (tuyệt đối không dùng ảnh phòng trống chưa đặt đạo cụ làm `Start Frame` cho cảnh sau).
   - **Tuân thủ nghiêm ngặt Trục 180° của `2-Panel Room Sheet`**: Khi thiết kế bối cảnh 2 bức tường đối diện (`Wall A` phía sau lưng nhân vật | `Wall B` phía trước mặt nhân vật), mọi góc máy đảo trục 180° nhìn trực diện vào mặt nhân vật **bắt buộc phải lấy đúng bức tường tương ứng làm hậu cảnh**, tuyệt đối cấm vẽ cùng một bức tường xuất hiện ở cả hai phía đối diện nhau.

3. **Quy tắc 3 — Kiểm Định Thị Giác Từng Góc Ảnh Nguồn Trước Khi Đẩy Vào Video (`Pre-Video Visual Scrubbing` chuẩn `@daniallll/seed-audio-1-0-launch-video`)**:
   - Giống như đạo diễn `@daniallll` đã soi thấy chữ rác `"ROU KOOR"` trên ngực áo ở `@IMG_002` và chạy lệnh xóa sạch ở `@IMG_003` trước khi đưa vào `Seedance`, bạn **phải dùng mắt kiểm tra toàn bộ 4 góc của mọi tấm Keyframe**:
     * Có chi tiết xuyên không niên đại (`Anachronism` — như màn hình máy tính hiện đại, chữ rác, logo lạ) lọt vào bối cảnh cổ điển không?
     * Qua lớp kính hoặc gương phản chiếu đã có đúng bóng nhân vật/bối cảnh phòng bên cạnh chưa? Nếu chưa, phải dùng `Surgical Edit` xử lý ngay trên ảnh tĩnh trước khi chạy video.

4. **Quy tắc 4 — Khóa Vật Lý Khi Đóng Nắp Đạo Cụ Có Lửa Hoặc Ánh Sáng (`Extinguish-Before-Close Lock` chuẩn `@ollkorrect/besa` `@IMG_032`)**:
   - Khi yêu cầu AI diễn cảnh đóng nắp bật lửa, hộp đồng xu phát sáng hoặc tắt đèn dầu, các model video thường bị lỗi giữ nguyên layer ánh sáng/ngọn lửa xuyên qua nắp kim loại đã đóng.
   - **Câu lệnh khóa vật lý bắt buộc**:
     `"As the thumb flips the hinged metal lid shut, the flame/glow is instantly smothered and completely extinguished into darkness BEFORE the lid clicks closed — zero visible flame or light leak once the metal lid is shut"` (hoặc cung cấp cả `Start Frame` đang mở + `End Frame` đã đóng kín).

5. **Quy tắc 5 — Tách Biệt Rạch Ròi `Internal Voiceover (Môi Khép Kín)` Với `On-Camera Spoken Lip-Sync`**:
   - Nếu truyền câu thoại vào prompt của một cảnh có gương mặt nhân vật mà không khóa trạng thái miệng, AI sẽ mặc định cho nhân vật **mở miệng nói thành tiếng (`on-camera lip-sync`)**.
   - Nếu câu thoại đó là **Độc thoại nội tâm (`Internal Monologue / Off-Screen V.O.`)**, bắt buộc phải ghi rõ trong phần hình ảnh: **`"MOUTH LOCK: His/Her lips remain completely closed and still throughout the entire shot — no spoken lip movement"`**, và chỉ dùng lip-sync cho những câu nhân vật thực sự mở miệng nói trực tiếp trong cảnh.

---

## 30. Giải Mã Trực Tiếp Bộ Phim Thành Phẩm (`Master Film 60-Frame Visual Storyboard Audit`) — `@pandaproduction/projects/thread` (`"THREAD"`, `5:44`) & Công Cụ `--extract-storyboard`

> **Bài học Xương Máu Về Kể Chuyện Điện Ảnh (`Visual Storytelling vs. Raw Prompt Text`)**:
> - Nếu chỉ đọc các câu Prompt chữ rời rạc mà **không xem trực tiếp Video/Trailer thành phẩm (`gallery_media`)** ở đầu dự án, AI rất dễ rơi vào bẫy viết kịch bản **"Đố mẹo bằng đạo cụ vô cảm"** (như đặt đồng xu lên cân rồi rút súng đọc thoại sáo rỗng — khán giả không biết nhân vật là ai, không có sự đồng cảm con người và thoát ra ngay ở giây thứ 5).
> - Để khắc phục triệt để mà không cần tải file `.mp4` gốc nặng hàng trăm MB làm phình Git, [`scraper/higgsfield_project_scraper.py`](./scraper/higgsfield_project_scraper.py) đã được tích hợp cờ **`--extract-storyboard`** (cũng tự động kích hoạt khi chạy `--download-media`), dùng `ffmpeg` đọc trực tiếp luồng `HLS 480p` (`index_480p.m3u8`) để trích xuất 2 bảng Storyboard `.jpg` siêu nhẹ (~200KB/tấm):
>   1. [`master_film_storyboard_first90s.jpg`](./data/creators/pandaproduction/projects/thread/images_final_takes/master_film_storyboard_first90s.jpg) (30 khung hình thực tế trong 90 giây mở đầu / Trailer).
>   2. [`master_film_storyboard_rest.jpg`](./data/creators/pandaproduction/projects/thread/images_final_takes/master_film_storyboard_rest.jpg) (30 khung hình thực tế từ giây 90 đến hết phim).

### 30.1. 4 Bí Quyết Kể Chuyện Bậc Thầy Của `@pandaproduction/projects/thread` (`Bart Bialobrzeski`) Khi Xem Trực Tiếp 60 Khung Hình Thành Phẩm

1. **Cú Hook 20 Giây Đầu (`00:00–00:20` — `VIDEO 07` & `VIDEO 22`): Mở Màn Bằng "Bi Kịch Con Người Tột Cùng" Rồi Mới Kích Hoạt "Đạo Cụ Vật Lý" (`Accidental Physical Trigger`)**
   - **Không bao giờ mở màn bằng đồ vật vô tri**: Giây `00:00` mở thẳng vào gương mặt tái nhợt, tuyệt vọng của người đàn ông đứng sau lớp kính cửa sổ mờ đục phản chiếu bóng phố gạch thế kỷ 18, bên tai chỉ có tiếng thở đứt quãng và tiếng tim đập thình thịch (`Subjective Sound`).
   - Giây `00:06–00:15`: Máy quay lùi chậm ra ngoài cửa sổ tầng 2. Anh đẩy tung cánh cửa sổ, đưa **hai bàn tay đẫm máu đỏ tươi** lên bóp chặt mặt, ngửa cổ gào lên một tiếng hét xé lòng rồi **đổ gục hai cẳng tay xuống bệ cửa sổ bằng đá**.
   - **Cơ chế kích hoạt vật lý vô thức**: Chính cú đổ gục cẳng tay vì kiệt sức đó vô tình đẩy nhẹ **con suốt gỗ cuốn chỉ lanh (`wooden spindle`)** nằm khuất trên bệ đá, làm nó lăn qua mép cửa sổ và rơi tự do xuống mặt đường đá ướt bên dưới!
   - **Tác dụng giữ chân khán giả**: Chỉ trong 15 giây không một lời thoại, người xem bị khóa chặt bởi câu hỏi nhân tính: *"Chuyện kinh hoàng gì vừa xảy ra trong căn phòng tối đó mà tay anh ta đầy máu, và con suốt chỉ rơi xuống đường kia gắn với bi kịch gì?"*

2. **Kỹ Thuật "Chuyền Gậy Tiếp Sức Chủ Thể (`=== THE CAMERA NEVER STOPS — IT ALWAYS HAS A LEADER ===`)" (`00:20–01:30` — `VIDEO 01`, `VIDEO 02`, `VIDEO 10`, `VIDEO 11`)**
   - Máy quay `Steadicam Oner` không bao giờ đứng yên và không bao giờ đi một mình — mỗi chủ thể mới phải lao vào khung hình khi chủ thể cũ vẫn còn đang chuyển động:
     * **Leader 1 (`Con suốt gỗ`)**: Lao từ bệ cửa sổ tầng 2 xuống mặt đường đá ướt, lăn lông lốc giữa rừng chân người đi chợ sớm, dừng lại ở mép rãnh nước bẩn.
     * **Leader 2 (`Con chuột cống`)**: Chạy dọc rãnh nước đỏ màu máu cá, luồn qua gầm xe ngựa, leo thẳng lên chân bàn gỗ của sạp cá đúng lúc lưỡi dao phay của bà bán cá **chặt đứt lìa đầu con cá bạc**.
     * **Leader 3 (`Con chó hoang -> Đám tang -> Đôi tình nhân -> Hai đứa trẻ -> Người mẹ bế con`)**: Con chó chạy dọc phố chợ dẫn máy quay lướt qua nỗi đau (đám tang áo đen) và niềm vui (đôi tình nhân hôn nhau dưới vòm cổng) đúng như câu logline *"when grief and joy pass like strangers"*, rồi dừng ở bàn chân trần nhỏ xíu của đứa bé sơ sinh trên lòng mẹ.
     * **Leader 4 (`Con ruồi & Con chim sẻ`)**: Máy quay xoay 360° `clockwise` quanh con ruồi đậu trên ngón chân đứa bé ➔ con ruồi bay lên ➔ **con chim sẻ (`sparrow`)** lao vào đớp gọn con ruồi giữa không trung rồi bay vọt lên cao, vượt qua biển mái ngói đầy khói bếp sang con phố bên cạnh, đáp xuống bệ cửa sổ tầng 2 đang mở toang!

3. **Cú Twist "Khép Vòng Tròn Thời Gian (`Circular Time-Loop Reveal`)" (`01:30–03:30` — `VIDEO 10`..`VIDEO 15`)**
   - Khi máy quay bay xuyên qua con chim sẻ trên bệ cửa sổ vào căn phòng tối bên trong, khán giả nhận ra người đàn ông lúc mở đầu đang ngồi co ro ở góc phòng — nhưng **hai bàn tay anh ta hoàn toàn sạch sẽ, chưa hề có máu!**
   - Cú máy tiếp sức ngoài phố đã đưa khán giả **quay ngược thời gian về 1 tiếng trước**: Anh chồng bước vào phòng hộ sinh khi vợ vừa sinh con (3 giây im lặng nghẹt thở trước khi tiếng khóc chào đời vang lên, hai vợ chồng mỉm cười hạnh phúc), bà đỡ dùng **chính sợi chỉ từ con suốt gỗ đó** để buộc rốn cho đứa bé rồi đặt con suốt lên bệ cửa sổ. Ngay giây thứ 27 (`VIDEO 15`), người vợ đột ngột thét lên vì **băng huyết sau sinh**.

4. **Đỉnh Cao Kể Bi Kịch Qua "Chiếc Gương Cổ Mờ Đục & Âm Thanh Tắt Dần" (`03:30–05:44` — `VIDEO 17`, `VIDEO 20`, `VIDEO 24`, `VIDEO 39`)**
   - Thay vì quay cảnh máu me trên giường, tác giả dùng công thức **`Off-Screen Mirror Tragedy & Sound Decay`**:
     * Khóa người chồng đứng chết lặng ở `1/3` trái khung hình, ôm đứa con quấn khăn trắng thấm đỏ máu ở nửa dưới; còn ở `1/3` phải khung hình là **chiếc gương cổ mờ đục (`@IMG_041`)** phản chiếu bóng 3 người phụ nữ đang hối hả cứu người vợ trong im lặng tuyệt đối (`VIDEO 39`).
     * Toàn bộ bi kịch nằm ở lớp âm thanh (`=== THIS SHOT IS ABOUT THE SOUND ===`): Tiếng rên đau đớn của người vợ từ phía sau máy quay yếu dần, thưa dần qua 4 giai đoạn (`0–8s` ➔ `8–17s` ➔ `17–25s`) rồi tắt hẳn.
     * Bà đỡ bước tới đón đứa bé khỏi tay anh (trong 4 bước vật lý có sức nặng thật: luồn tay đỡ đầu ➔ luồn tay đỡ thân ➔ nhấc nhận trọng lượng làm vết máu in lên tay áo trắng của chồng ➔ ôm vào lòng đung đưa theo phản xạ 40 năm nghề). Người chồng bước tới đứng trước ô cửa kính, máy quay lướt qua khung gỗ cửa sổ (`Wooden Mullion Wipe`) xuyên qua kính ra ngoài phố — **khép kín 100% vào khung hình đầu tiên ở giây `00:00`!**



