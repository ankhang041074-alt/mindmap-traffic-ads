# SỔ TAY RIÊNG DỰ ÁN: CÂY GIẢ CEDAR `4FT` (`16:9` TVC ĐA BỐI CẢNH — VỀ NHÀ LÀM TIẾP)

## 1. Thông Tin Dự Án & Đường Dẫn Nhanh
- **Sản phẩm:** Cây giả Cedar nhựa PE đúc 2 tông xanh kèm chậu vuông đen cao vát đáy (`Chậu + Tán lá = 4ft ≈ 1.20m`, cao đúng `1/2` cánh cửa chính `2.4m` / ngang mặt kệ lò sưởi `1.22m` / cao hơn mặt tủ `80cm` khoảng `40cm`).
- **Link Project Google Flow đang chạy (AdsPower profile `flow veo`):**
  👉 `https://flow.google.com/project/dfcf77a5-5374-4678-9f80-1c5ea7b5c305`
- **Project dựng Fast-Cut `10s` (`"10s内包含多个场景"`):** Conversation `35e7c62f-5e89-4172-b621-9835d23f7591`
- **Thư mục mã nguồn & tài nguyên chuẩn trong Repo (`git pull` về nhà là có đủ 100%):**
  - `cedar_4ft_10s/clean_refs/CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg` — Ảnh gốc `1024x1024` sạch chữ (dùng để khóa chi tiết cận cảnh lá đúc PE & khấc miệng chậu vuông âm).
  - `cedar_4ft_10s/batch40_plates/` — **6 tấm Plate `2K 16:9` (`2560x1440`) nền trắng `#FFFFFF`** đã đặt sẵn ảnh cây thật nguyên bản đúng vị trí & tỷ lệ `4ft`:
    1. `PLATE_01_PAIR_HALFDOOR_45PCT_16x9.jpg` — 2 cây đối xứng `44.5%` khung hình (dùng cho cửa chính cao `2.45m`, lò sưởi trần cao `3.4m`).
    2. `PLATE_02_PAIR_MEDIUM_HERO_56PCT_16x9.jpg` — 2 cây cận trung `50mm` (`56%` khung hình, dùng cho bàn Console sảnh Foyer, cửa kính đôi sân hiên).
    3. `PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg` — 2 cây đặt lệch tầng góc xiên `3/4` (tạo chiều sâu kiến trúc 3D cho hiên nhà / bậc thềm).
    4. `PLATE_04_SINGLE_HERO_LEFT_68PCT_16x9.jpg` — 1 cây Hero lớn bên trái (`68%` khung hình, dùng cho phòng khách rèm linen, phòng đọc sách).
    5. `PLATE_05_SINGLE_HERO_RIGHT_66PCT_16x9.jpg` — 1 cây Hero lớn bên phải (`66%` khung hình, dùng cho cầu thang kính vườn, sân hiên ghế mây).
    6. `PLATE_06_SINGLE_WIDE_ROOM_50PCT_16x9.jpg` — 1 cây đại cảnh phòng rộng (`50%` khung hình, dùng cho phòng ăn nắng sớm, phòng khách lớn).
  - `cedar_4ft_10s/run_batch10_silent_flow.py` — Script tạo hàng loạt ảnh `16:9` chạy ngầm trên AdsPower (`0` nhảy cửa sổ).
  - `cedar_4ft_10s/run_batch10_veo4s_silent.py` — Script tạo hàng loạt video `4 giây` (`Veo 3.1 - Fast`) chạy ngầm trên AdsPower.

---

## 2. LOGIC CỐT LÕI ĐÃ KIỂM CHỨNG THÀNH CÔNG (Đọc 1 Phút Hiểu Trọn Bí Quyết)

### A. Bí Quyết Tạo Ảnh `16:9` Chuẩn `100%` Sản Phẩm Gốc + Nắng Điện Ảnh TVC (`Nano Banana Pro`)
1. **Không cắt ghép thủ công, cũng không quăng ảnh vuông `1:1` cho AI tự vẽ lại cây:**
   - Luôn đính kèm **CẶP KHÓA KÉP (2 file)** vào `+ Thành phần`:
     * **File 1:** `1` trong `6` tấm `PLATE_0X_..._16x9.jpg` (khóa cứng tọa độ đứng, dáng phình bầu cây và tỷ lệ thật `4ft`).
     * **File 2:** `CEDAR_REF_1_SINGLE_4FT_CLEAN.jpg` (`1024x1024`, khóa độ nét từng cọng lá đúc PE 2 màu & khấc miệng chậu vuông đen).
2. **Cấu trúc Prompt `Edit Background Only` (Tuyệt đối KHÔNG dùng từ mô tả thực vật gây méo cây):**
   - **CẤM DÙNG:** `cedar`, `pine`, `topiary`, `slender pot`, `teardrop`, `chartreuse` (các từ này khiến AI tự vẽ mới cây thông lá kim nhọn và kéo ốm chậu).
   - **KHUÔN MẪU MỞ ĐẦU CỐ ĐỊNH:**
     > `Edit this 16:9 product photograph (using the second 1024x1024 reference image for close-up molded leaf and matte-black square planter detail): keep [the / BOTH] potted artificial plant[s] and [its / their] matte-black tapered square planter[s] 100% pixel-identical to the 16:9 plate in exact position, height, pot width-to-height proportions, snug recessed square top rim, plump symmetrical rounded-cone outer contour, and dense two-tone green molded plastic leaf texture — DO NOT slim the pot[s], DO NOT pinch the waist above the pot rim, and DO NOT redraw or alter the leaves into spiky pine needles. Replace ONLY the pure white background with [mô tả bối cảnh 35mm-50mm Kodak Vision3 250D + vật neo tỷ lệ 4ft + tiền cảnh mờ bokeh + nắng xiên chiều trên tường + ánh sáng tự nhiên trung thực trên cây + bóng đổ dưới đáy chậu, zero text].`

---

### B. Bí Quyết Tạo Video `4 Giây` (`Veo 3.1 - Fast` · `Khung hình Bắt đầu` · `16:9`) Mượt Mà, Không Đứng Im, Không Lộ Thiết Bị
Qua thực chiến QA trực tiếp 10 clip trên Flow, đây là **3 Luật Sống Còn** cho video `4 giây`:
1. **CẤM ghi tên thiết bị quay phim (`slider`, `gimbal`, `dolly`, `tripod`, `rig`):**
   - Ghi chữ `slider` hoặc `gimbal` khiến `Veo 3.1` vẽ lộ thanh sắt/chân máy màu đen thò vào mép dưới khung hình!
   - **Thay bằng:** `Continuous, clearly visible 4-second forward camera push-in` hoặc `Continuous, clearly visible 4-second lateral camera truck-left / truck-right` + chốt cuối câu: `No people, no camera equipment, zero morphing, zero text.`
2. **CẤM ghi các từ "đóng băng máy quay" (`100% still`, `motionless`, `hold steady`, `5%`, `6%`):**
   - Ghi `motionless / 100% still / hold steady` làm `Veo 3.1` khóa cứng luôn cả khung hình khiến video đứng im y như ảnh tĩnh!
   - **Cách viết đúng để máy di chuyển 3D rõ nét mà cây giả vẫn chuẩn form:**
     * Tả rõ **vật thể tiền cảnh trượt qua màn hình**: *"so the foreground sofa / coffee table and ceramic mug sweeps visibly across the bottom foreground in strong 3D optical parallax, moving smoothly from a wide view to a closer medium shot..."*
     * Cho thêm chuyển động vi mô của môi trường thật (*rèm voan khẽ thở nhẹ `sheer linen curtains breathe very softly`, hạt nắng bụi mịn `subtle golden dust motes drift in the sunbeams`, hoặc bóng nắng lá cây / lá vườn xa phía sau khẽ lung linh*).
     * Khóa dáng sản phẩm bằng cụm từ hình học thay vì từ đóng băng: *"...while preserving the exact solid shape, matte-black square planter geometry, and dense two-tone green molded foliage of the plant."*
3. **Khi chạy tự động trên AdsPower (CDP):**
   - Tuyệt đối **KHÔNG** gọi `Page.bringToFront` (để trình duyệt không nhảy đè lên màn hình). Chỉ gọi `Emulation.setFocusEmulationEnabled({"enabled": True})`.
   - Sau mỗi lần bấm nút `Bắt đầu tạo` ở chế độ Video, chờ ~`4–5 giây` cho ô `Bắt đầu` tự reset trống rồi mới gán tấm ảnh tiếp theo.

---

## 3. Các Bước Về Nhà Mở Máy Làm Tiếp (Nhân Lên `30–40` Cảnh Tiếp Theo)
1. Ở máy nhà, mở Terminal tại thư mục repo `wonderful-lavoisier` và kéo code + bộ Plate `2K` mới nhất về:
   ```bash
   git pull
   ```
2. Mở AdsPower profile `flow veo` → vào Project Flow `https://flow.google.com/project/dfcf77a5-5374-4678-9f80-1c5ea7b5c305` (nếu bị hỏi login thì dùng `python3 flow_web_intro/home_helper.py import` như hướng dẫn cũ).
3. Nhắn cho AI trong Antigravity ở nhà đọc ngay file `cedar_4ft_10s/NOTE_CEDAR_4FT_LOGIC_VA_LAM_TIEP_O_NHA.md` này rồi ra lệnh:
   > *"Đọc file `cedar_4ft_10s/NOTE_CEDAR_4FT_LOGIC_VA_LAM_TIEP_O_NHA.md`, dùng đúng 6 tấm `batch40_plates` và logic Combo khóa khuôn + Video 4s Dynamic Parallax để chạy ngầm tiếp 20–30 bối cảnh mới trên AdsPower cho tôi."*
