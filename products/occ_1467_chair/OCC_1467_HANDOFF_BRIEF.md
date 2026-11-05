# Handoff & Quy Chuẩn Sản Xuất TVC Ghế Bập Bênh Xếp Gọn Đỏ `OCC-1467` (Crimson Red & Silver-Grey Mesh)

## 1. Đường Dẫn Nguồn Ảnh Gốc & Video Giải Phẫu Thực Tế
- **3 Thư mục ảnh gốc (`OCC-1467`)**:
  - `/Users/dudumac5/Downloads/IMAGE/OCC-1464-1467 VER 1/OCC-1467` (`Main-1.jpg` studio góc 3/4 nền trắng, `Main-2.jpg` kích thước & gấp gọn, `Main-4.jpg` chính diện + ngang 90 độ, `Main-5.jpg` mặt sau lưng ghế, `Main-8.jpg` 4 bước gấp gọn).
  - `/Users/dudumac5/Downloads/IMAGE/OCC-1464-1467 VER 2/OCC-1467`
  - `/Users/dudumac5/Downloads/IMAGE/OCC-1464-1467 VER 3/OCC-1467`
- **Video giải phẫu thực tế & Các frame `1080p` đã trích xuất sẵn**:
  - Video gốc: `/Users/dudumac5/Downloads/OCC-1465(PROMO)(DEMO).mp4`
  - Bộ ảnh giải phẫu `1080p` đã trích xuất sẵn trong workspace: `products/occ_1467_chair/demo_anatomy_refs/`
    * `hi_03s.jpg`: Góc `Rear-3/4` người ngồi ngả lưng đan tay sau gáy bập bênh thực tế (thấy rõ mặt lưới xám hơi xuyên sáng, dải đỏ đỉnh lưng có 2 đinh tán bạc, dây đỏ chéo khung chữ X sau, túi cốc đỏ bên phải và 2 trụ lò xo đen).
    * `hi_07s.jpg`: Hình thái thực tế khi gấp gọn `4.9"` xách ngang 1 tay bằng quai vải đỏ (2 trụ lò xo đen có tem vàng chĩa ngang, túi cốc đỏ rủ ở cạnh dưới).
    * `hi_15s.jpg` & `hi_16s.jpg`: Cận cảnh mặt ghế đỏ Crimson `#B12233` + 2 đường chỉ viền trắng dọc (`two crisp white vertical piping lines`) + tấm lưới xám thoáng khí bán trong suốt (`#A1A0A5`).
    * `hi_20s.jpg`: Cận cảnh túi đựng cốc vải đỏ viền xám gắn ở trụ trước bên phải + tem vàng trên thanh chéo chữ X.
    * `hi_29s.jpg`: Cận cảnh cơ cấu bập bênh dưới đất: thanh đế ngắn nằm ngang phẳng cố định sát mặt đất + khớp chữ U màu đen bắt ốc bạc + trụ lò xo hình trụ đen thẳng đứng (tem vàng `ROTATION PROHIBITED`) + ống khung chữ L nhún ép lên đỉnh trụ lò xo.
- **Tham khảo cấu hình & bộ Plate mẫu từ mã xanh `OCC-1464`**:
  - `products/occ_1464_chair/sku_project.json`

---

## 2. 6 Luật Cứng Bắt Buộc Khi Làm Ảnh & Video Cho `OCC-1467`
1. **Quy trình 2 bước bắt buộc (`Chụp Diện Rộng & Check Kỹ Chi Tiết Sản Phẩm ➔ Mới Chạy Video`)**:
   - Mỗi lần tạo ảnh xong trên Google Flow, bắt buộc chụp ảnh diện rộng (`qa_..._img_page1.jpg`) và tải ảnh full-res kiểm tra kỹ 100% chi tiết ghế:
     * **Tựa lưng mặt trước**: Phải lộ rõ **dải vải đỏ ngang bản rộng trên đỉnh lưng (`#B12233`) + 2 đường viền trắng dọc + tấm lưới xám (`#A1A0A5`)** (kể cả khi có người ngồi góc 3/4, không để lưng người che khuất hoàn toàn làm AI tự bịa lưng ghế 1 màu đỏ trơn khi nhún).
     * **Tựa lưng mặt sau (`Rear View`)**: Đủ dải vải đỏ đỉnh lưng có 2 đinh tán bạc, lưới xám giữa lưng, dây vải đỏ chéo dưới khung chữ X sau.
     * **Khung gầm & chân đế**: Khung chữ X liền mạch (không có thanh sắt gãy thừa), túi đựng cốc đỏ bên hông phải, và **thanh đế ngang thẳng nằm phẳng sát đất + khớp chữ U đen + ống chữ L + trụ lò xo đen thẳng đứng có tem vàng** (tuyệt đối cấm chân cong bập bênh truyền thống).
     * **Logic đạo cụ hợp lý**: Ngồi 1 mình chỉ có đúng **1 ly nước/bình nước** đặt trong túi đựng cốc bên phải (khóa rõ trong prompt video để AI không tự sinh thêm ly nước thứ 2 trên tay kia).
2. **Cấu trúc chuẩn 1 Concept TVC (`7 Shots · Khóa Cứng 8 Giây/Shot`)**:
   - **2–3 Cảnh Có Nhân Vật Ngồi Chill / Trò Chuyện & Đung Đưa Bập Bênh Nhẹ (`Rocking Shots`)**:
     * Shot 1 (Hook): Nhóm 2–3 người bạn ngồi trò chuyện vui vẻ và **đung đưa bập bênh nhẹ nhàng**.
     * Shot 2 (Rear-3/4 View): Góc quay từ phía sau lưng ghế (`Rear View` chuẩn `Main-5.jpg` & `hi_03s.jpg`) ngắm cảnh đẹp và **đung đưa bập bênh êm ái**.
     * Shot 3 (Couple / Solo Chill): Đôi bạn hoặc 1 người ngồi thư giãn ngắm cảnh và **đung đưa bập bênh nhẹ**.
   - **1 Cảnh Cận Cảnh Chi Tiết Sản Phẩm (`Close-Up Camera Pan · Ghế Đứng Im 100%`)**:
     * Ghế không người, đứng im 100%, máy quay `85mm` lia mượt dọc thân ghế từ lưng lưới xám viền trắng qua tay vịn bọc đệm đỏ, túi đựng cốc đỏ và khung chữ X + trụ lò xo đen.
   - **2 Cảnh Bối Cảnh Sản Phẩm Không Người Theo Logic Mới (`Rule-of-Thirds 1/3–2/3 Environmental Showcase + 3D Orbital Parallax Glide`)**:
     * **CẤM** đặt 2 ghế đối xứng phẳng trái–phải chiếm kín khung hình + camera zoom thẳng chậm.
     * **BẮT BUỘC** đặt ghế ở góc `3/4` lệch 1 bên khung hình (`1/3`) kèm đạo cụ đời sống (bàn trà gỗ, bình giữ nhiệt, tách cà phê, đèn lồng...) và mở rộng `2/3` khung hình cho bối cảnh 3 lớp chiều sâu; trong video, ghế đứng vững 100% trên sàn còn **máy quay trượt vòng cung 3D (`3D orbital parallax arc / lateral tracking glide`)** vừa tôn bối cảnh vừa khoe dáng ghế 3D.
   - **1 Cảnh Chót Xếp Gọn Mang Đi (`Folded Carry Outro`)**:
     * Nhân vật một tay xách ngang chiếc ghế gấp gọn `4.9"` bằng quai vải đỏ (`chuẩn Main-3.jpg / hi_07s.jpg`) bước đi tự nhiên.
3. **Mỗi Concept TVC thay đổi bối cảnh đồng bộ mới + Tạo bảng Nhân vật mới (`@CHAR_Sheet` 3 khung da thật) với phối đồ mới**.
4. **Chạy ngầm 100% qua `init_silent_flow_session` (Zero Focus Stealing)**.
5. **LUẬT CỨNG #7 (KINH NGHIỆM THỰC CHIẾN TẠO ẢNH & VIDEO ĐUNG ĐƯA `OCC-1467` ĐÃ KIỂM CHỨNG)**:
   - **Tạo ảnh 2 người ngồi trò chuyện (`RED_LAKE03`, `RED_LAKE09`, `RED_LAKE10`)**:
     * Muốn đổi vị trí mới độc đáo trên khung `16:9`, hãy tạo Plate cắt sẵn lệch phải `2/3` (`OCC1467_PLATE_09_PAIR_RIGHT_TERRACE_16x9.jpg`) hoặc lệch trái `2/3` (`OCC1467_PLATE_10_PAIR_LEFT_STREAM_16x9.jpg`).
     * Trong prompt tạo ảnh, **TUYỆT ĐỐI CẤM** viết `"turned in 3/4 profile"` (vì Nano Banana Pro sẽ xoay ngang cả 2 chiếc ghế và tự vẽ lại chân ghế cong sai mẫu). **BẮT BUỘC** viết:
       > `"keep BOTH chairs at their exact 52% identical low-back director-chair height and exact 2D canvas coordinates with 100% UNCHANGED frames, do NOT rotate or redraw the chairs: seat two happy friends facing forward in the two chairs while turning their heads toward each other to chat warmly (never looking at the camera) ... both sitting comfortably with the wide crimson-red top header band, two white vertical piping lines, and silver-grey mesh backrest panel clearly visible around their shoulders"`
   - **Tạo ảnh 1 người ngồi bên phải quay mặt sang trái (`RED_LAKE01`)**:
     * Bắt buộc dùng Plate đã lật chiều ghế sang trái `OCC1467_PLATE_01B_SINGLE_RIGHT_FACING_LEFT_58PCT_16x9.jpg` (tuyệt đối không ép nhân vật ngồi ngược chiều với Plate gốc làm AI lật ngược phần lưng ghế nhưng để lại chân chữ L bị hếch).
   - **Tạo ảnh xách ghế xếp gọn (`Folded Carry Outro` — `RED_LAKE08`)**:
     * Bắt buộc dùng duy nhất ref `OCC1467_REF_5_FOLDED_CARRY_S4_1024.jpg` (cắt riêng `STEP 4` từ `Main-8.jpg`, bỏ `STEP 3` cạnh ngang hẹp) để chiếc ghế gấp có đúng kích thước khung chữ nhật bản rộng (`80cm × 65cm`, kéo dài từ ngang hông xuống sát cổ chân), tuyệt đối không bị biến thành thanh hẹp.
   - **Prompt Video đung đưa nhẹ (`V_RED_BEACH01..03`, `V_RED_LAKE02`, `V_RED_LAKE09`, `V_RED_LAKE10`) — Giải mã 3 lý do vì sao `V_RED_BEACH02` cử động nhún đúng 100% cơ học**:
     1. **Tư thế 2 bàn chân trong Ảnh gốc (`Both Feet Planted on the Ground — NO Crossed Lifted Leg`)**: Ở `RED_BEACH02` (và các nhân vật nam trong `RED_BEACH01`, `RED_BEACH03`, `RED_LAKE03`), **cả 2 bàn chân đều đặt chạm sàn** (`both feet resting naturally on the ground, legs uncrossed`). Ngược lại, khi nhân vật nữ **vắt chéo chân làm 1 bàn chân nhấc bổng lơ lửng trên không** (do bắt chước cô gái vắt chân trong ảnh ref `OCC1467_COUPLE_CAMP_TALK_REF.jpg`), Veo 3.1 thấy bàn chân lơ lửng nên hiểu nhầm là đang đạp bập bênh ngửa cả khung đế ghế lên! Do đó khi tạo ảnh người ngồi, nên ghi rõ `"with both feet resting naturally on the ground (legs uncrossed)"`.
     2. **Chủ ngữ hành động trong Prompt Video là "Người ngả lưng nhẹ" (`Person leans gently` — Tuyệt đối KHÔNG nhắc chữ `spring / hinge / bottom bar` trong prompt video)**:
        - Công thức chuẩn Vàng của `V_RED_BEACH02`:
          > `"the [man/woman] seated in the chair leans gently and rhythmically back and forth in an effortless, soothing rocking motion"`
        - Khi chủ ngữ là **người ngồi ngả lưng nhẹ nhàng** và **không nhắc một chữ nào đến lò xo hay chân sắt** trong prompt video, Veo 3.1 mặc định coi phần chân đế sát đất là vật tĩnh cố định và chỉ cho phần thân trên + lưng ghế nhún nhẹ theo khớp chữ L. Ngược lại, hễ nhắc `"spring"`, `"hinge"`, `"bottom bar"` vào prompt video là Veo 3.1 lập tức cố làm chuyển động/uốn cong các thanh sắt dưới đất.
     3. **Bóng nắng đen sát mặt sàn (`Hard Solar Contact Shadow`)**: Thanh đế ngang dưới cùng có vệt bóng đổ đen sắc nét chạm sát mặt sàn giúp Veo 3.1 "dán chặt" thanh đế ngang vào mặt đất, chỉ cho phần khung chữ L phía trên nhún.
   - **Với cảnh cận cảnh / bối cảnh ghế trống không người (`V_RED_BEACH04`, `V_RED_LAKE04..07`)**:
     * Khóa cứng `"The empty chair remains 100% stationary and firmly planted..."` và dùng chuyển động máy quay `3D orbital push-in and lateral arc` trong `1 single continuous 8-second shot` (`NO cuts, NO cross-dissolves`).

---

## 3. Trạng Thái 2 Bộ TVC Đã Hoàn Thành Trên Google Flow (`project_id = 1d71c3d4-623e-4656-8d1e-915fbe5e59bd`)
- **TVC #1 — Concept Bờ Biển & Đầm Phá Gỗ Tuyết Tùng (`products/occ_1467_chair/sku_project.json`)**:
  - 7 Ảnh (`RED_BEACH01..07`) + 7 Video `8 giây` (`V_RED_BEACH01..07`): Đã hoàn thành 100% (bao gồm bản sửa `RED_BEACH06` thuyền gỗ thật `5.5m` tỷ lệ `1:1` + camera trượt vòng cung 3D).
- **TVC #2 — Concept Hồ Tuyết Sơn & Trại Gỗ Tùng Mùa Thu Bắc Mỹ (`products/occ_1467_chair/sku_project_tvc2_lake.json`)**:
  - Nhân vật mới `@CHAR_2`: `products/occ_1467_chair/clean_refs/OCC1467_CHAR_2_SHEET.jpg` (`5b954b64-31c5-45e6-8d9d-0db8d5b6f25f`).
  - 10 Ảnh (`RED_LAKE01..10`) đã kiểm duyệt 100% trong `products/occ_1467_chair/occ_1467_chair_tvc2_lake_scene_uuids.json` & lưu bản full-res trong `products/occ_1467_chair/verified_scenes/`.
  - 10 Video `8 giây` (`V_RED_LAKE01..10`) đã chạy trên Google Flow project `https://flow.google.com/project/1d71c3d4-623e-4656-8d1e-915fbe5e59bd`.
