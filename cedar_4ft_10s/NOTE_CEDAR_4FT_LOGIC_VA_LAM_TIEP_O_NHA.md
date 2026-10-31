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
1. Ở máy nhà, mở Terminal tại thư mục repo `wonderful-lavoisier` và kéo code + ảnh gốc `1K` nền trắng nhẹ (`clean_refs/`) + bảng UUID về (các bộ `plates_2k/` nặng không đẩy lên GitHub để tránh rối repo; khi cần tái tạo chỉ mất 2 giây bằng `python3 -m flow_sku_tvc_toolkit build-plates ...`, còn các tấm đã upload sẵn trên Project Flow sẽ được lấy trực tiếp từ thư viện mây Flow):
   ```bash
   git pull
   ```
2. Mở AdsPower profile `flow veo` → vào Project Flow `https://flow.google.com/project/dfcf77a5-5374-4678-9f80-1c5ea7b5c305` (nếu mở bằng Chrome/máy phụ bị hỏi login thì dùng `python3 flow_web_intro/home_helper.py --force-cloud-cookie` hoặc `--inject-session flow_web_intro/flow_session.json`).
3. Nhắn cho AI trong Antigravity ở nhà đọc ngay file `cedar_4ft_10s/NOTE_CEDAR_4FT_LOGIC_VA_LAM_TIEP_O_NHA.md` và `PLAYBOOK_CAY_4FT_SANG_CROCHET_VA_FLOW_SOP.md` rồi ra lệnh:
   > *"Đọc file `cedar_4ft_10s/NOTE_CEDAR_4FT_LOGIC_VA_LAM_TIEP_O_NHA.md`, dùng đúng các tấm Plate đã có trên Project Flow (hoặc chạy `flow_sku_tvc_toolkit`) cùng logic Combo khóa khuôn + Video 4s Dynamic Parallax để chạy ngầm tiếp các bối cảnh mới trên AdsPower cho tôi."*


---

## 4. Danh Mục 20 Bối Cảnh Đã Hoàn Tất Chuẩn 100% SKU Trên Project Flow (`S01 → S20`)

### Lô 1 (`S01 → S10` — Đã Xong 10 Ảnh `16:9` + 10 Video `4s`)
- `S01` (`3d63c790-7d60-4f2d-bce6-05114ca84031`) — Hiên cửa chính gỗ óc chó `2.45m` & tường gạch kem (2 cây = `1/2` cửa)
- `S02` (`5d275a3e-f828-4419-854f-a70ae267077a`) — Hiên biệt thự Mỹ gỗ trắng Hamptons góc xiên `3/4` (2 cây chiều sâu)
- `S03` (`4f63712c-37c9-433d-8457-a47e3672cf34`) — Cửa đôi kính khung thép đen sân hiên đá Travertine (2 cây cận trung)
- `S04` (`65f2c152-5db9-4ca7-8996-7dfd76b2ce9e`) — Sân hiên có mái ghế bành mây gỗ Teak & vườn nắng sớm (1 cây phải)
- `S05` (`e89c5d87-3173-42d1-85ae-4a4edd69bb76`) — Lò sưởi đá vôi Pháp trần cao `3.4m` & gương vòm đồng (2 cây ngang kệ `1.22m`)
- `S06` (`56d84fb5-e098-432f-89ad-3c2b54ae048c`) — Sảnh Foyer bàn Console gỗ sồi `85cm` & tranh lớn (2 cây đối xứng)
- `S07` (`d81a1ece-9b49-4d8f-8576-510de683db46`) — Phòng khách tủ gỗ rãnh, rèm linen & ly gốm mờ bokeh (1 cây trái)
- `S08` (`7a13b09d-c6cd-4dac-8732-d828f3a5429f`) — Phòng đọc sách bàn gỗ óc chó & kệ sách vòm vữa ấm (1 cây trái)
- `S09` (`7ef37782-5c33-4d76-972c-49b87d27735b`) — Cầu thang gỗ sồi bay & vách kính sát trần nhìn ra vườn (1 cây phải)
- `S10` (`ebc19d89-96d5-431c-bf48-65672b2852ec`) — Phòng ăn trần cao tủ Buffet gỗ sồi & nắng ban mai (1 cây đại cảnh)

### Lô 2 (`S11 → S20` — Đã Xong 10 Ảnh `16:9` Đón Nắng Thực Tế Mới Nhất)
- `S11` (`94476b2c-f110-4c1a-9c08-ee3d514ccc6c`) — Hiên vòm đá vôi biệt thự Santa Barbara & cửa đôi gỗ sồi `2.45m` nắng chiều bóng lá (2 cây = `1/2` cửa)
- `S12` (`72972fcc-5a93-464b-8324-399a9185d9d2`) — Phòng kính Sunroom ngập nắng sớm & bệ ghế băng cửa sổ gỗ sồi `50cm` (1 cây Hero trái)
- `S13` (`7cf09a22-e08a-4bb0-9634-ef73a6450557`) — Hành lang cột đá sân trong biệt thự nhìn ra hồ bơi xanh ngọc nắng vàng góc `3/4` (2 cây lệch tầng)
- `S14` (`80fe0aac-30fb-4d56-9fc3-8cd36fdeeba0`) — Góc Đảo bếp đá cẩm thạch Calacatta & gỗ sồi rãnh `90cm` cạnh cửa kính trượt ra sân vườn (1 cây Hero phải)
- `S15` (`c8560aa3-3ce7-401f-831e-7cee9e229b90`) — Cổng vòm thông phòng ốp phào chỉ `95cm` mở ra phòng khách ngập nắng phía sau (2 cây cận trung)
- `S16` (`88270262-e787-4d12-809c-1c3fb0a01be9`) — Góc thư giãn Phòng ngủ Master rèm voan cửa ban công nắng sớm & ghế bành vải linen `72cm` (1 cây Hero trái)
- `S17` (`255b13ff-e051-4f6b-8fc6-5de808f483de`) — Sân vườn đá Châu Âu đối xứng hai bên cửa sổ vòm gỗ sồi & bóng nắng đốm lá cây (2 cây cận trung)
- `S18` (`357a083b-bb15-4391-8461-42c738a6d409`) — Góc khô ráo cạnh cửa sổ nắng trong phòng tắm Master Organic Spa & bồn tắm đá trắng `60cm` (1 cây Hero phải)
- `S19` (`03731287-04a9-477e-a037-843e39e6cdf2`) — Ban công Penthouse sàn gỗ Teak lan can đá kính `1.10m` nắng hoàng hôn vàng rực góc `3/4` (2 cây chiều sâu)
- `S20` (`2a636fef-0562-4470-ad3d-8ff399015f8f`) — Phòng khách đồi ven biển Malibu California trần xà gỗ nhìn ra biển nắng cuối chiều (1 cây đại cảnh)


---

## 5. Sản Phẩm SKU #2 — Cây Giả Cedar `4ft+` Chậu Thùng Gỗ 3 Đai Sắt Đen (`B01 → B20`: Đã Xong 20 Ảnh `16:9` + 20 Video `4s` `VB01 → VB20`)

### A. Tài Nguyên Chuẩn Trong Thư Mục `barrel_cedar_20/`
- **Tỷ lệ vật lý chuẩn xác nhận từ video hãng `ATF-9421,9422.mp4`:** `~4ft+` (`~1.25m–1.30m`), ngọn nhọn cao **nhỉnh hơn tay nắm cửa chính ~15–20cm** và cao hơn mặt kệ lò sưởi ~12cm.
- **2 Ảnh tham chiếu `1K` sạch nền trắng (`1024x1024`) đã lưu trong Git (`barrel_cedar_20/clean_refs/`):**
  - `BARREL_REF_1_SINGLE_CLEAN.jpg` — Ảnh tổng thể toàn cây nền trắng sạch.
  - `BARREL_REF_2_CLOSEUP_LEAF_BARREL_1024.jpg` — Ảnh Macro đặc tả lá dẹp `flat-fan lacy foliage` + thùng gỗ 3 đai sắt đen (dùng để khóa chi tiết lá & vân gỗ `Dual-Lock` cho các cảnh đại cảnh `B15`, `B16`, `B19`, `B20`).
- **9 tấm Plate `2K 16:9` (`2560x1440`) nền trắng `#FFFFFF` đã upload lên Project Flow (`barrel_cedar_20/barrel_plate_uuids.json`):**
  1. `BARREL_PLATE_01_PAIR_DOOR_52PCT_16x9.jpg` (`52%` khung hình — 2 cây đối xứng cửa chính `2.4m` / lò sưởi)
  2. `BARREL_PLATE_02_PAIR_MEDIUM_62PCT_16x9.jpg` (`62%` khung hình — 2 cây cận trung `50mm`)
  3. `BARREL_PLATE_03_PAIR_DIAGONAL_3Q_16x9.jpg` (2 cây lệch tầng góc xiên `3/4`: trái `64%`, phải `51%`)
  4. `BARREL_PLATE_04_SINGLE_HERO_LEFT_72PCT_16x9.jpg` (`72%` khung hình — 1 cây Hero bên trái)
  5. `BARREL_PLATE_05_SINGLE_HERO_RIGHT_70PCT_16x9.jpg` (`70%` khung hình — 1 cây Hero bên phải)
  6. `BARREL_PLATE_06_SINGLE_WIDE_55PCT_16x9.jpg` (`55%` khung hình — 1 cây đại cảnh phòng rộng trần cao)
  7. `BARREL_PLATE_07_SINGLE_WIDE_RIGHT_36PCT_16x9.jpg` (`36%` khung hình — 1 cây đại cảnh trần cao `B15` chuẩn tỷ lệ `4ft` cạnh tủ Buffet `85cm`)
  8. `BARREL_PLATE_08_SINGLE_COASTAL_RIGHT_56PCT_16x9.jpg` (`56%` khung hình — 1 cây đại cảnh phòng khách biển `B20` chuẩn tỷ lệ `4ft`)
  9. `BARREL_PLATE_09_SINGLE_HERO_RIGHT_76PCT_16x9.jpg` (`76%` khung hình — 1 cây Hero tiền cảnh hồ bơi `B19`)
- **Bộ Script tự động chạy ngầm + map UUID chuẩn 1-1 + tải/ghép Master `1080p`:**
  - `barrel_cedar_20/run_barrel20_images_silent.py` — Tạo 20 ảnh `16:9` (`Nano Banana Pro`) chạy ngầm.
  - `barrel_cedar_20/map_barrel20_uuids.py` — Quét danh sách cuộn ảo lấy chính xác 20 UUID lưu vào `barrel_cedar_20/barrel20_scene_uuids.json`.
  - `barrel_cedar_20/run_barrel20_veo4s_silent.py` — Tạo 20 video `4 giây` (`Veo 3.1 - Fast`) kèm cầu nối `img[data-media-id] <-> /asb/` chống trượt token sau khi reload trình duyệt.
  - `barrel_cedar_20/download_and_merge_atf_9422_1080p.py` — Tự động upscale/tải `1080p` (`1920x1080`), kiểm định SHA-256 + `ffprobe` và nối file Master `+faststart`.

### B. Danh Sách 20 Ảnh `16:9` & 20 Video `4s` Chậu Thùng Gỗ Đai Đen Trên Project Flow (`B01 → B20` / `VB01 → VB20`)
#### Nhóm 10 Cảnh Đôi (`2 Cây` — `B01 → B10` + `VB01 → VB10`)
- `B01` / `VB01` (`6db60962-6415-4f60-8eb5-9e7d4b0e0adc`) — Hiên cửa xám than `2.4m` tay nắm đồng & cột đá vôi kem (2 cây cao hơn tay nắm ~18cm)
- `B02` / `VB02` (`b79f4640-6f8c-4dd6-9480-1f45c2ec382b`) — Hiên Farmhouse Mỹ vách gỗ trắng `board-and-batten` & cửa gỗ sồi kính góc xiên `3/4`
- `B03` / `VB03` (`c4943dff-0e78-4809-b4a6-0d28cdf55d05`) — Phòng khách trần cao `3.3m` lò sưởi đá vôi chạm khắc & gương vòm đồng cổ
- `B04` / `VB04` (`dc6353ce-f24f-4054-869f-f829945e28d5`) — Cửa đôi kính khung thép đen & sân đá phiến tự nhiên nắng chiều
- `B05` / `VB05` (`c464825d-04db-47cb-af20-db42f90ff9ed`) — Sân trong Villa Địa Trung Hải đài phun nước đá & vòm ô-liu góc xiên `3/4`
- `B06` / `VB06` (`7cfd4143-d2cf-4275-b8cb-153506086a44`) — Sảnh Foyer bàn Console gỗ sồi tự nhiên `85cm` & tranh linen tối giản
- `B07` / `VB07` (`738d4df5-4d78-4ee0-81df-9ef226dc63df`) — Vòm đá vôi dinh thự Châu Âu & cửa đôi gỗ óc chó `2.45m` bóng nắng đốm lá
- `B08` / `VB08` (`a1ec88a7-8f1d-4326-aab1-818bc07e5f67`) — Sân vườn đá Napa Valley & cửa sổ vòm gỗ sồi cạnh ghế sắt tiền cảnh
- `B09` / `VB09` (`5c0e6841-b2a9-46ee-a1d7-44e3a1edbb5e`) — Sàn gỗ Teak giàn Pergola nắng chiều vườn sau góc xiên `3/4`
- `B10` / `VB10` (`280418e1-6063-4c53-8fbb-193b61070b93`) — Cổng vòm nội thất phào chỉ cổ điển `90cm` mở ra phòng khách ngập nắng

#### Nhóm 10 Cảnh Đơn Hero & Đại Cảnh (`1 Cây` — `B11 → B20` + `VB11 → VB20`)
- `B11` / `VB11` (`94bd79f0-ec26-434c-a49d-b16244374267`) — Hiên vườn có mái ghế bành gỗ Teak đan mây & vườn nắng sớm (1 cây Hero phải)
- `B12` / `VB12` (`07ca3cea-54d5-42f9-ac07-6cc00088d4db`) — Phòng khách tủ gỗ sồi rãnh `80cm`, rèm voan linen & ly gốm thủ công (1 cây Hero trái)
- `B13` / `VB13` (`d6b74296-6f95-4ec4-8758-8f004aacdcf9`) — Phòng kính Sunroom bệ ghế cửa sổ gỗ sồi `50cm` & sàn gạch Terracotta (1 cây Hero trái)
- `B14` / `VB14` (`97d7f5d6-a835-48d6-9f74-529ae38c8d6d`) — Góc đảo bếp đá Marble Calacatta & gỗ sồi rãnh cạnh cửa kính sân vườn (1 cây Hero phải)
- `B15` / `VB15` (`89fd32b4-b711-471d-88ad-7b6b01748713`) — Phòng ăn trần cao tủ Buffet gỗ sồi `85cm` & bàn ăn nắng ban mai (1 cây đại cảnh `PLATE_07` chuẩn `4ft`)
- `B16` / `VB16` (`8c5ae9c1-5afd-4a59-ac02-fe88e604d098`) — Phòng đọc sách bàn gỗ óc chó, sổ da & kệ sách vòm vữa đất sét (1 cây Hero trái khóa `REF_2` lá dẹp)
- `B19` / `VB19` & `B17..B20` theo thứ tự:
  - `B17` / `VB17` (`2c384643-3ea0-4a76-83be-3448d470258b`) — Cầu thang gỗ sồi lan can sắt đen & vách kính sát trần nhìn ra vườn (1 cây Hero phải)
  - `B18` / `VB18` (`da276718-80a1-49c8-9839-021b8c26f20b`) — Góc thư giãn Phòng ngủ Master rèm voan ban công & ghế bành linen (1 cây Hero trái)
  - `B19` / `VB19` (`6a6f121c-f7b4-4bfd-ac72-25eee72808c5`) — Cabana hồ bơi Resort đá Travertine & sofa Daybed gỗ Teak (1 cây Hero tiền cảnh phải `PLATE_09` khóa `REF_2`)
  - `B20` / `VB20` (`2df175d4-9486-46d6-9140-bf9043b8a131`) — Phòng khách đồi ven biển California trần xà gỗ sồi & cửa kính đại dương (1 cây đại cảnh `PLATE_08` chuẩn `4ft`)

---

## 6. Lô 3 SKU #1 — Cây Giả `4ft` Lá Đúc PE 2 Tông Xanh Chậu Vuông Đen Cao Vát Đáy (`S21 → S40` & `V21 → V40`: 20 Ảnh `16:9` + 20 Video `4s`)

### A. Cấu Hình Chuẩn Hóa Trên `flow_sku_tvc_toolkit` (`products/cedar_sqpot_batch3_20/`)
- **Tự động tách 1 cây chuẩn từ ảnh Listing `Set of 2`:** `plate_engine.py` tự nhận diện ảnh đôi đồng kích thước trên nền `#FFFFFF` và tách riêng 1 cây sạch (`416x1024`, `W/H = 0.40625`) để dựng trọn bộ **9 tấm Plate `2K 16:9` (`SQPOT3_PLATE_01..09`)** + **Ảnh Macro `1.65x` (`SQPOT3_REF_2_CLOSEUP_1024.jpg`)** khóa khấc miệng chậu vuông âm & cọng lá đúc PE 2 tông xanh.
- **File cấu hình & bảng khóa 20 UUID vĩnh viễn lưu gọn trong Git:**
  - `products/cedar_sqpot_batch3_20/sku_project.json` — Trọn bộ 20 bối cảnh kiến trúc/nội thất mới (`S21 → S40`) + 20 kịch bản chuyển động máy 3D-Parallax `4 giây` (`V21 → V40`) + danh sách `exclude_uuids` cách ly toàn bộ tài nguyên cũ trên Project Flow.
  - `products/cedar_sqpot_batch3_20/cedar_sqpot_batch3_20_scene_uuids.json` — 20 UUID `data-media-id` chuẩn 1-1 cho `S21 → S40`.
  - `products/cedar_sqpot_batch3_20/cedar_sqpot_batch3_20_plate_uuids.json` — Token 10 tấm Plate & Macro `SQPOT3_*` đã upload sẵn trên Project Flow.

### B. Danh Sách 20 Ảnh `16:9` & 20 Video `4s` Mới Nhất Trên Project Flow (`S21 → S40` / `V21 → V40`)

#### Nhóm 10 Cảnh Đôi (`2 Cây` — `S21 → S30` + `V21 → V30`)
- `S21` / `V21` (`23460d2f-3988-441d-bd00-e5b482079f3a`) — Mặt tiền dinh thự Georgian cửa đôi đen satin `2.4m` tay gõ đồng & cột đá vôi rãnh (`PLATE_01` `52%`)
- `S22` / `V22` (`08aeac9a-4b9c-4a6d-bfeb-97f99bf3d972`) — Cổng sắt mỹ thuật kính vòm sân trong Villa Tuscany đá Travertine & bậc thềm nắng chiều góc `3/4` cân bằng `60%/56%` đồng cỡ `4ft` (`PLATE_03B`)
- `S23` / `V23` (`8facbd9d-41ed-4ea7-861b-e6105fcfe46c`) — Sảnh biệt thự hiện đại cửa trục xoay Pivot đồng sẫm & kính sọc kiến trúc `2.45m` (`PLATE_01` `52%`)
- `S24` / `V24` (`d6587f20-8cb3-4a03-b550-cd6c9d500d00`) — Phòng khách hiện đại lò sưởi đá Roman Travertine rãnh cao `1.18m` & đôn vải linen (`PLATE_02` `62%`)
- `S25` / `V25` (`cf869a1f-27f9-4b21-9bc3-b982ff2e372b`) — Sân hiên lan can con tiện đá vôi `1.00m` biệt thự ven hồ nước xanh ngọc núi tuyết góc `3/4` cân bằng `60%/56%` đồng cỡ `4ft` (`PLATE_03B`)
- `S26` / `V26` (`77397d83-7177-4f63-94cd-91fa438561b3`) — Sảnh khách sạn Boutique 5 sao tường vữa Marmorino & bàn Console đá Travertine chân đồng `85cm` (`PLATE_02` `62%`)
- `S27` / `V27` (`dc6751d8-652d-43dd-9745-be4b0d20b5ac`) — Nhà kính Orangery dinh thự Châu Âu cửa đôi vòm thép đen chia ô kính `2.45m` (`PLATE_01` `52%`)
- `S28` / `V28` (`4b1a1f00-40eb-4590-8b36-a3946e0e8af7`) — Phòng ăn sang trọng cửa đôi kính khung đồng hầm rượu phát sáng ấm & sàn gỗ xương cá (`PLATE_02` `62%`)
- `S29` / `V29` (`dad27022-42da-4de1-b4fb-ee742ec5e3b1`) — Sân thượng Montecito California lò sưởi ngoài trời vữa trắng dầm gỗ sồi `1.18m` dưới giàn Pergola nắng sọc (`PLATE_01` `52%`)
- `S30` / `V30` (`11292166-35de-4d99-ae5d-d76497805bba`) — Tiền sảnh thang máy riêng Penthouse cửa đồng Champagne, vách gỗ sồi rãnh & đá cẩm thạch (`PLATE_02` `62%`)

#### Nhóm 10 Cảnh Đơn Hero & Đại Cảnh (`1 Cây` — `S31 → S40` + `V31 → V40`)
- `S31` / `V31` (`7cc2af5f-e98c-496a-bcfd-a2843f697679`) — Phòng nhạc Salon ngập nắng rèm voan cao & đàn Đại dương cầm Grand Piano lùi hậu cảnh `1.4m` (`PLATE_04` `72%` trái)
- `S32` / `V32` (`c07b522c-3f59-4e77-beae-2f20eb4f2392`) — Poolhouse Cabana đá Travertine hồ bơi vô cực & giường nghỉ gỗ Teak lùi hậu cảnh `1.35m` (`PLATE_09` `76%` phải)
- `S33` / `V33` (`b78f69b3-e533-42a1-a231-d7a84fa931d9`) — Góc ăn sáng Breakfast Nook ghế băng vòng cung gỗ sồi rãnh bọc Bouclé & bàn tròn đá Travertine (`PLATE_04` `72%` trái)
- `S34` / `V34` (`eb701e7f-4e31-4fe0-90d3-ea782e9ebad4`) — Hành lang gỗ Hinoki phong cách Japandi mở cửa trượt ra vườn sỏi trắng thiền & bồn đá nước (`PLATE_05` `70%` phải)
- `S35` / `V35` (`06567b61-f4c6-4e6d-b69d-df625851431d`) — Đại cảnh phòng ăn & khách trần xà gỗ sồi cao `3.3m`, bàn ăn dài `2.6m` & tủ Sideboard rãnh `85cm` (`PLATE_07` `36%` phải)
- `S36` / `V36` (`91933026-b81b-4025-9d18-5161d3a1591b`) — Phòng Lounge thư viện ghế bành da bò Cognac `76cm` & hệ kệ gỗ sồi trưng bày sách nghệ thuật (`PLATE_04` `72%` trái)
- `S37` / `V37` (`e64cb883-4cf1-4360-b805-05d0c2cba273`) — Phòng thay đồ Master Dressing Suite tủ áo gỗ sồi rãnh, gương vòm đồng & ghế đôn Bouclé `46cm` (`PLATE_05` `70%` phải)
- `S38` / `V38` (`5b47ac76-1bc3-48f2-b3d3-2b14385383e1`) — Hành lang vòm đá cổ Provence Pháp ghế đá chạm `48cm` mở ra vườn hoa Oải hương & Ô-liu nắng vàng (`PLATE_06` `55%` trái)
- `S39` / `V39` (`1354fa6a-f9b9-4b85-b4a5-3b55aefec7fb`) — Phòng khách biệt thự ven hồ núi hiện đại mở trọn cửa kính trượt ra sàn gỗ & mặt hồ lấp lánh (`PLATE_08` `56%` phải)
- `S40` / `V40` (`aef8080a-6555-44c1-b699-c479d300d140`) — Sảnh thông tầng Atrium cầu thang xoắn ốc điêu khắc vữa trắng Venetian & bậc gỗ sồi đón nắng giếng trời (`PLATE_05` `70%` phải)

