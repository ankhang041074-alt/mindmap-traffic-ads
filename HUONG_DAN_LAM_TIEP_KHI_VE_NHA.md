# 🏠 HƯỚNG DẪN LÀM TIẾP VEO 3 (GOOGLE FLOW + ADSPOWER) KHI VỀ NHÀ

> **Link Project Google Flow đang làm dở (đã lưu sẵn toàn bộ ảnh `16:9` & video `1080p` trên Cloud):**
> 👉 **https://flow.google.com/project/e77d4088-8126-4cb4-8d09-edec09be18ff**

---

## ⏰ PHẦN 1: TRƯỚC KHI RỜI CÔNG TY LÚC 17H (CHỈ MẤT 10 GIÂY!)

Trước khi gập/tắt máy ở công ty, bạn làm đúng **1 thao tác** này để AdsPower đẩy phiên đăng nhập mới nhất lên đám mây:
1. Mở ứng dụng **AdsPower Global** trên máy công ty.
2. Ở dòng profile **`flow veo`**, bấm nút **`Close` (`Đóng`)** (hoặc tắt cửa sổ trình duyệt `SunBrowser` của profile đó).
3. **Đợi 5–10 giây** cho nút chuyển lại thành **`Open` (`Mở`)** (lúc này AdsPower đã đồng bộ xong toàn bộ Cookie phiên Google Flow Ultra lên Cloud). Sau đó tắt máy đi về thoải mái!

*(Lưu ý bảo mật: Toàn bộ file nhạy cảm `flow_session.json` và `flow_cookies_adspower.json` đã được khóa trong `.gitignore`, **tuyệt đối không bao giờ bị đẩy lên GitHub**).*

---

## 🚀 PHẦN 2: KHI VỀ TỚI NHÀ — 3 BƯỚC MỞ LẠI ĐÚNG CHỖ ĐANG LÀM DỞ

### Bước 1: Mở lại trình duyệt `flow veo` trên AdsPower ở máy nhà
1. Trên máy ở nhà, tải và mở **AdsPower Global** -> đăng nhập **cùng tài khoản AdsPower** bạn dùng ở công ty.
2. Bạn sẽ thấy sẵn profile **`flow veo`** (cấu hình `macOS / MacIntel` + Cookie đã đồng bộ sẵn từ công ty).
3. Bấm nút **`Open` (`Mở`)** -> trình duyệt `SunBrowser` hiện lên là **đã đăng nhập sẵn Google Flow Ultra**, không bị Google bắt xác minh thiết bị lạ hay hỏi mã OTP.

### Bước 2: Kéo toàn bộ code, ảnh sạch `0% chữ` & video `1080p` từ GitHub về máy nhà
Toàn bộ thư mục [`flow_web_intro/`](./flow_web_intro) đã được đẩy đồng bộ lên **cả 2 repo GitHub của bạn** (`video-prompt-v2` và `mindmap-traffic-ads`) để ở nhà bạn đang mở repo nào cũng có đủ 100%:

- **Nếu máy nhà đã có sẵn thư mục repo:**
  ```bash
  git pull origin main
  ```
- **Nếu máy nhà chưa tải repo về:**
  ```bash
  git clone https://github.com/ankhang041074-alt/video-prompt-v2.git
  cd video-prompt-v2
  ```
  *(Hoặc repo thứ 2: `git clone https://github.com/ankhang041074-alt/mindmap-traffic-ads.git`)*

### Bước 3: Chạy 1 lệnh tự động bắt cổng AdsPower tại nhà & mở đúng Project Veo 3
*(Ở công ty cổng CDP của AdsPower là `52602`, nhưng khi về nhà mỗi lần mở AdsPower nó sẽ cấp một cổng ngẫu nhiên khác. Script `home_helper.py` sẽ **tự động tìm cổng mới** trên cả Mac & Windows mà bạn không cần chỉnh bất kỳ dòng code nào!)*

```bash
python3 flow_web_intro/home_helper.py --check --open-project
```

Khi màn hình hiện **`🎉 TẤT CẢ SẴN SÀNG!`** là máy ở nhà đã nối thông hoàn toàn với cửa sổ AdsPower đang mở!

*(Tùy chọn: nếu muốn lưu thêm 1 bản `flow_session.json` dự phòng cho Playwright Cách 2 ngay tại máy nhà, chạy thêm:)*
```bash
python3 flow_web_intro/home_helper.py --export-session
```

---

## 📦 PHẦN 3: BẢN ĐỒ TÀI NGUYÊN ĐÃ HOÀN TẤT TRONG `flow_web_intro/`

Tất cả đã được đóng gói sẵn trên GitHub để bạn dùng ngay hoặc dựng tiếp:

1. **`flow_web_intro/deliverables/` — 8 File Video Thành Phẩm Web Intro `16:9` Full HD (`1920x1080`):**
   - `WEB_INTRO_15S_MULTI_PRODUCT_16x9.mp4` (`15.17s` — Tổng hợp 5 loại ly & hộp AirPods trên cả 2 sản phẩm) + bản `_MUTED.mp4`
   - `WEB_INTRO_10S_FASTCUT_16x9.mp4` (`10.07s` — Fast-cut `4 × 2.5s` tốc độ cao cho Hero Banner Web) + bản `_MUTED.mp4`
   - `WEB_INTRO_PRODUCT1_DAISY_16x9.mp4` (`11.30s` — Riêng SP1 Đế hoa cúc trắng: Ly sứ trà nóng + Ly Matcha đá + Giỏ 3D đựng AirPods) + bản `_MUTED.mp4`
   - `WEB_INTRO_PRODUCT2_SUNFLOWER_ROSE_16x9.mp4` (`10.57s` — Riêng SP2 Hướng dương 2 tầng & Hoa hồng 6 nụ: Ly sứ vàng + Ly Latte đá + Bàn đôi phòng khách) + bản `_MUTED.mp4`
   *(Các file `*_MUTED.mp4` đã gỡ luồng âm thanh `-an` và bật `+faststart` để nhúng thẳng vào thẻ `<video autoplay muted loop playsinline>` trên Header Website).*

2. **`flow_web_intro/videos/hd_1080p/` — 6 Cảnh Gốc Native `1080p` Xuất Từ Google Flow Veo 3.1:**
   - `shot1_v2_1080p.mp4`: SP1 Hoa cúc trắng (`4` cuống) + Ly sứ trắng trà nóng
   - `shot2_v1_1080p.mp4`: SP2 Hướng dương 2 tầng (`2` cao chạm miệng ly + `2` thấp phía trước) + Ly sứ vàng
   - `shot3_v1_1080p.mp4`: SP2 Hoa hồng viền kem (`6` nụ đỏ/hồng xen kẽ) + Ly thủy tinh Latte đá
   - `shot4_v2_1080p.mp4`: SP1 Giỏ hoa cúc 3D đa năng + Hộp AirPods trắng
   - `shot5_v1_1080p.mp4`: SP1 Hoa cúc trắng (`4` cuống) + Ly thủy tinh Matcha Latte đá
   - `shot6_v1_1080p.mp4`: SP2 Bàn đôi phòng khách (Ly gốm hoa lam bật hoa hướng dương bên cạnh đế hoa hồng mở phẳng)

3. **`flow_web_intro/clean_product_refs/` — Bộ Ảnh Gốc 2 Sản Phẩm Thật Đã Xóa Sạch 100% Chữ (`0% Text`):**
   - `PRODUCT_1_AND_2_REAL_REFERENCE_ATLAS.jpg` (Bảng đối chiếu 6 góc chuẩn của cả 2 sản phẩm)
   - `PROD1_STYLE_A_POPUP_MUG_CLEAN.jpg`, `PROD1_AIRPODS_BASKET_CLEAN.jpg`, `IMG_01_CLEAN_NO_TEXT.jpg`
   - `PROD2_STYLE_C_SUNFLOWER_MUG_CLEAN.jpg`, `PROD2_STYLE_B_ROSE_FLAT_ISOLATED.jpg`, `PROD2_IMG_01.jpg`

4. **`flow_web_intro/frames/` — Toàn Bộ Cặp Ảnh `16:9` `START_FRAME` (`Bắt đầu`) & `END_FRAME` (`Kết thúc`)** đã khóa tỷ lệ hoa thật.

5. **`flow_web_intro/contact_sheets/` — Bảng Kiểm Định Pháp Y `0.5s` (`2fps`)** của cả 4 video thành phẩm.

---

## 🤖 PHẦN 4: CÂU LỆNH COPY-PASTE GỬI CHO AI TẠI NHÀ ĐỂ LÀM TIẾP NGAY (KHÔNG SỢ AI HIỂU SAI)

Khi về nhà, sau khi bạn mở profile `flow veo` trong AdsPower và `git pull`, bạn chỉ cần **copy nguyên đoạn dưới đây** gửi cho AI (Antigravity / Claude / Cursor) là AI sẽ nắm 100% ngữ cảnh và làm tiếp ngay mà không lặp lại bất kỳ lỗi cũ nào:

```text
Tôi đã mở sẵn trình duyệt AdsPower (profile "flow veo" đã login Google Flow Ultra) trên máy nhà và đã git pull repo mới nhất.
Hãy đọc ngay file HUONG_DAN_LAM_TIEP_KHI_VE_NHA.md và chạy `python3 flow_web_intro/home_helper.py --check --open-project` để tự động bắt cổng CDP của AdsPower (TUYỆT ĐỐI KHÔNG đóng trình duyệt AdsPower của tôi).

Chúng ta đang làm trực tiếp trên project Google Flow: https://flow.google.com/project/e77d4088-8126-4cb4-8d09-edec09be18ff
Phần Web Intro 16:9 ngang đã làm xong trong `flow_web_intro/deliverables/`. Bây giờ hãy đọc kỹ ảnh đối chiếu sản phẩm thật trong `flow_web_intro/clean_product_refs/PRODUCT_1_AND_2_REAL_REFERENCE_ATLAS.jpg` và các script trong `flow_web_intro/` (như `review_fix_keyframes_step1.py`, `review_fix_keyframes_step2.py`, `review_gen_videos_step3.py`, `assemble_web_intros.py`) để làm tiếp cho tôi:
[GHI YÊU CẦU TIẾP THEO CỦA BẠN Ở ĐÂY — VÍ DỤ: "Làm bản 9:16 dọc TikTok/Reels đặt nhiều loại ly khác nhau bật hoa dậy" HOẶC "Chỉnh lại thứ tự cắt / thêm chữ intro cho bản 16:9"]

Lưu ý bắt buộc giữ đúng quy tắc vật lý Reverse Surgical END_FRAME -> START_FRAME Lock:
1. Không bao giờ để cánh hoa quá to biến dạng (phải khớp đúng tỷ lệ hoa len móc mini thật trong clean_product_refs/).
2. Không để hoa bay lơ lửng CGI chậm; khi đặt ly chạm đế len thì cuống hoa bật dựng đứng 90° gọn gàng (tâm đế cúc Style A trơn 0 bông hoa ở giữa, 4 cuống cúc quanh viền; mẫu hướng dương Style C có 2 hoa bên cao chạm miệng ly + 2 hoa trước thấp ngang thân ly; mẫu hoa hồng Style B đế xanh viền kem có 6 nụ đỏ/hồng).
```

---

## 🛠️ PHẦN 5: XỬ LÝ NHANH 4 TÌNH HUỐNG HAY GẶP KHI CHUYỂN MÁY VỀ NHÀ

| Tình huống tại nhà | Cách xử lý trong 10 giây |
| :--- | :--- |
| **1. Chạy `home_helper.py` báo `Không tìm thấy trình duyệt AdsPower đang mở`** | Mở app **AdsPower Global** -> bấm nút **`Open` (`Mở`)** ở dòng `flow veo`, đợi cửa sổ `SunBrowser` bật lên rồi chạy lại lệnh. |
| **2. Máy ở nhà báo thiếu thư viện Python (`No module named 'websockets'` hoặc `'PIL'`)** | Chạy: `pip3 install websockets pillow` |
| **3. Máy ở nhà chưa cài `ffmpeg` (khi cần cắt ghép lại MP4 bằng `assemble_web_intros.py`)** | Trên Mac: `brew install ffmpeg` <br> Trên Windows: `winget install Gyan.FFmpeg` |
| **4. Muốn sửa điểm cắt giây (trim) hoặc đổi thứ tự cảnh của 4 video `16:9` mà không cần tốn credit tạo lại** | Chỉnh thông số giây trong hàm `main()` của [`flow_web_intro/assemble_web_intros.py`](./flow_web_intro/assemble_web_intros.py) rồi chạy: <br> `python3 flow_web_intro/assemble_web_intros.py && python3 flow_web_intro/verify_all_deliverables.py` |
