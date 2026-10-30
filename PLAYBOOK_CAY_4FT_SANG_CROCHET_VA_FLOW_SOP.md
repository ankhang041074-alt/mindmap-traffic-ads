# Sổ Tay Thực Chiến: Đúc Kết Làm Cây `4ft`, Cách Áp Dụng Sang `Crochet` / Sản Phẩm Mới & SOP Thao Tác Ngầm Google Flow

> [!IMPORTANT]
> Tài liệu này đóng gói trọn vẹn **kinh nghiệm xương máu từ 2 SKU Cây `4ft` hôm nay** (`40 ảnh 2K 16:9` + `40 video Veo 3.1 4s`), giải đáp chi tiết **cách mang công thức "1 Ảnh Tách Nền Trắng -> Plate `2K` + Macro `1K`" sang đồ `Crochet` và các sản phẩm khác**, cùng **quy trình thao tác Google Flow chạy ngầm trên AdsPower** mà không cần up full hình/video nặng làm rối GitHub.

---

## 1. Lưu Ý Xương Máu Khi Làm Sản Phẩm Cây `4ft` (Đúc Kết Từ 2 SKU Hôm Nay)

Hôm nay chúng ta đã hoàn thành trọn vẹn 2 mã cây trên Project Flow `dfcf77a5-5374-4678-9f80-1c5ea7b5c305`:
1. **SKU #1 ([`cedar_4ft_10s/`](./cedar_4ft_10s)):** Cây Cedar `4ft` (`~1.20m`) chậu vuông đen cao vát đáy (`S01..S20` + `V01..V20`).
2. **SKU #2 ([`barrel_cedar_20/`](./barrel_cedar_20)):** Cây Cedar `4ft+` (`~1.25m–1.30m`) chậu thùng gỗ 3 đai sắt đen (`B01..B20` + `VB01..VB20` + xuất gộp `1080p`).

Dưới đây là **5 lỗi thực tế đã phát hiện khi soi QA và công thức khóa chết vĩnh viễn**:

| Ca lỗi thực tế hôm nay | Nguyên nhân gốc | Công thức xử lý dứt điểm (đã đóng gói vào Toolkit) |
| :--- | :--- | :--- |
| **1. Cây `4ft` bị biến thành cây khổng lồ `8ft` chạm trần hoặc bonsai `60cm`** *(Ca `B15` phòng ăn & `B20` phòng khách biển)* | Dùng Plate `55%–70%` cho bối cảnh đại cảnh thấy trọn trần nhà `3.2m`, hoặc dùng Plate `36%` quá nhỏ làm chìm cây | Áp đúng **Ma trận `% chiều cao Plate`**: Đại cảnh trần cao thấy trọn bàn ăn dùng **`36%`** (`PLATE_07`); Phòng khách rộng nhìn ra biển dùng mức **Goldilocks `56%`** (`PLATE_08`) + neo lưng ghế sofa `78cm` cao tới `~60%` cây; Cửa chính `2.4m` dùng **`52%`** (ngọn cây cao hơn tay nắm cửa `~18cm`). |
| **2. Nội thất khổng lồ bên cạnh "nuốt" mất bề ngang cây** *(Ca `B19` Cabana hồ bơi)* | Đặt cột gỗ to hoặc tay vịn ghế daybed dày sát rạt ngay cạnh chậu thùng gỗ ở tiền cảnh | Dùng Plate Hero **`76%`** (`PLATE_09`), bắt buộc ghi trong prompt: **đẩy sofa/daybed lùi ra sau `1.2m–1.4m`**, khóa mặt đệm ngồi ngang đai sắt giữa của chậu và lưng tựa chỉ cao tới `48%–55%` thân cây. |
| **3. AI tự vẽ lại tán lá dẹt mảnh thành chùm lá thông xù nhọn** *(Ca `B16` phòng đọc sách)* | Ảnh gốc `1024x1024` có quá nhiều viền trắng (`65%`), AI không nhìn rõ đầu lá; cộng thêm bóng nắng đen vắt ngang tán cây | **Bắt buộc kèm tấm `REF_2_CLOSEUP_1024` (zoom `1.65x` sát nhánh lá + thân chậu)** + câu khóa `STRICT_CUTOUT_LOCK` (`treat ... as an untouched locked foreground photograph cutout`) + thả nắng xiên lên tường/kệ phía sau nhưng giữ **ánh sáng tự nhiên sạch và đều quanh cây (`even, clean natural daylight around the plant`)**. |
| **4. Video `Veo 3.1` tự mọc thêm cây thứ 3 từ rìa khung hình** *(Ca `VB02` hiên Farmhouse)* | Mép ngoài cùng bên trái ảnh tĩnh `B02` có lấp ló một vệt lá mờ; khi chạy `lateral truck` (trượt ngang mở biên), `Veo 3.1` suy diễn vệt lá đó thành cây mới | Khi rìa trái/phải ảnh có chi tiết cắt dở, **cấm dùng `lateral truck`**. Đổi ngay sang **`forward diagonal camera push-in`** (đẩy máy tiến xiên vào tâm cửa) để cắt bỏ rìa biên ra khỏi màn hình ngay giây đầu tiên. |
| **5. Video `Veo 3.1` lộ thanh ray sắt đen ở mép dưới hoặc đứng im như ảnh JPEG** | Viết chữ `slider / gimbal / dolly / rig` (lộ thiết bị) hoặc `100% still / motionless / hold steady / 5%` (đóng băng khung hình) | Bộ lọc [`guardrails.py`](./flow_sku_tvc_toolkit/guardrails.py) tự động chặn trước khi chạy. Luôn viết: `Continuous, clearly visible 4-second [35mm/50mm] [forward camera push-in / lateral camera truck-right] ... so the softly blurred [vật tiền cảnh] sweeps visibly ... in rich 3D optical parallax`. |

---

## 2. Áp Dụng Quy Trình "Tách Nền Trắng -> Plate `2K` + Macro `1K`" Sang `Crochet` & Sản Phẩm Khác Có Ổn Không?

### Câu trả lời ngắn gọn: **CỰC KỲ ỔN — Và với đồ `Crochet` (len móc thủ công), kỹ thuật này còn giải quyết đúng bài toán khó nhất của AI!**
- Khi tạo ảnh/video đồ Crochet bằng cách thông thường, AI gần như luôn mắc 3 bệnh: **(1) biến mũi móc đơn/kép (`crochet`) thành gân áo len đan kim (`knitting`)**, **(2) làm chảy sợi cotton thành cục bông xù CGI**, và **(3) tự đổi số lượng cánh hoa / viền sò**.
- Khi dùng **Combo Khóa Khuôn Kép (`2K 16:9 Cutout Plate` + `1K Macro Stitch Ref`)**, `Nano Banana Pro` bị khóa cứng **100% từng mũi móc thật của bạn** trên nền `#FFFFFF` và chỉ vẽ mặt bàn gỗ, nắng sớm, ly sứ bokeh xung quanh!

### Tuy nhiên, khi chuyển từ Cây `4ft` (`125cm` đặt sàn) sang `Crochet` (`8cm – 45cm` đặt bàn/kệ), BẮT BUỘC đổi 5 điểm sau:

*(Toàn bộ 5 điểm này đã được cài sẵn thành các Preset `crochet_coaster`, `crochet_decor`, `crochet_bag` trong [`flow_sku_tvc_toolkit/presets.py`](./flow_sku_tvc_toolkit/presets.py)):*

| Hạng mục | Cây Cảnh `4ft` (`tree_4ft`) | Đồ Len Móc `Crochet` (`crochet_coaster` / `crochet_decor` / `crochet_bag`) |
| :--- | :--- | :--- |
| **1. Xử lý ảnh gốc trước khi dựng Plate** | Ảnh hãng thường có sẵn nền trắng (chỉ cần xóa chữ) | Ảnh chụp đồ len thủ công thường chụp trên mặt bàn gỗ/vải. **Bước 0:** Chạy lệnh `isolate-white` (dùng `Nano Banana Pro 1:1` tách sang nền trắng `#FFFFFF`) hoặc tách PNG trong suốt trước, sau đó `plate_engine.py` sẽ tự chạy thuật toán **Border-Flood** khử sạch viền xám studio thành `#FFFFFF` mà **không làm mất màu len trắng/kem bên trong**. |
| **2. Bẫy "Sản phẩm màu trắng/kem chạm nền `#FFFFFF`"** | Lá cây xanh đậm nên tách biệt hoàn toàn với nền trắng `#FFFFFF` | Hoa cúc trắng, thỏ len trắng, viền kem (`#F5EFE6`) rất gần màu nền `#FFFFFF`. **Quy tắc bắt buộc:** Khi outpaint bối cảnh cho len sáng màu, **KHÔNG tả mặt bàn màu trắng sáng loá** — hãy đặt lên **bàn gỗ óc chó (`walnut`), gỗ sồi ấm (`warm white-oak`), đá travertine kem ấm hoặc khăn linen màu be/xanh sage** kèm nắng xiên nhẹ (`warm golden rim-light`) để viền sợi len nổi khối 3D sắc lẹm! |
| **3. Tiêu cự ống kính & Khoảng hở đáy (`bottom_margin`)** | `35mm–50mm` ngang tầm mắt; đáy chậu sát sàn (`bottom_margin = 4.5%–6%`) | **`85mm–100mm Macro Tabletop f/2.8`** (xóa phông kem mịn); **nâng đáy sản phẩm lên `11%–18%` (`bottom_margin`)** để lộ rõ mặt bàn gỗ/khăn trải bàn ở tiền cảnh ngay trước chân sản phẩm (giúp bóng đổ tiếp xúc dưới đáy sợi len bám thật vào mặt bàn). |
| **4. Vật neo khóa tỷ lệ thật (`Scale Anchors`)** | Cửa chính `2.4m`, tay nắm cửa, lò sưởi `1.15m`, lưng sofa `78cm` | **Ly gốm cà phê / tách trà (`9cm–9.5cm`)**, tách espresso (`6.5cm`), hộp AirPods (`5.5cm`), cuốn sổ tay bìa vải `A5`, thìa đồng nhỏ đặt lùi nhẹ phía sau. |
| **5. Bộ từ cấm & Chế độ Video `Veo 3.1`** | Cấm `cedar, pine, topiary, slender...` · Dùng Video **1-Frame `Bắt đầu` (`4s 3D-Parallax`)** | **CẤM TUYỆT ĐỐI chữ `knitted / knitting` (len đan), `felt` (vải nỉ), `fuzzy wool`, `cartoon`, `CGI`** · Tả đúng: `handcrafted tight milk-cotton crochet yarn stitches, crisp interlocking crochet loops`.<br>• **Đồ Crochet tĩnh** (chậu hoa len, thú bông Amigurumi, túi len): Dùng **1-Frame `Bắt đầu` (`4s 3D-Parallax`)** y hệt làm cây hôm nay.<br>• **Đồ Crochet biến hình cơ học** (đế lót ly phẳng -> đặt ly xuống bật cuống hoa dựng `90°` như bộ [`flow_web_intro/`](./flow_web_intro)): Dùng **2-Frame (`Bắt đầu` + `Kết thúc`)** (Toolkit hỗ trợ sẵn trường `end_scene_key`!). |

---

## 3. SOP Thao Tác Google Flow Chạy Ngầm Như Hôm Nay (`AdsPower Silent CDP`)

Toàn bộ thao tác hôm nay đã được đóng gói thành công cụ dòng lệnh thống nhất [`flow_sku_tvc_toolkit/`](./flow_sku_tvc_toolkit). Hệ thống tự động dò cổng CDP của AdsPower `SunBrowser` đang mở (không sợ đổi port khi tắt mở máy) và **chạy ngầm 100% bằng `Emulation.setFocusEmulationEnabled(true)` — không bao giờ nhảy cửa sổ đè màn hình làm việc**.

### Bước 0 — Mở AdsPower & Kiểm Tra Danh Sách Preset
Mở profile `flow veo` trong AdsPower (đứng sẵn ở Project Google Flow bạn muốn chạy), sau đó xem các Preset tỷ lệ vật lý có sẵn:
```bash
python3 -m flow_sku_tvc_toolkit list-presets
```

### Bước 1 — Tạo Khung Dự Án Nhẹ Cho Sản Phẩm Mới (`0` Rác, Chỉ Sinh 1 File JSON)
Ví dụ tạo dự án cho chậu hoa Tulip len móc (`crochet_decor`) hoặc cây mới (`tree_4ft`):
```bash
python3 -m flow_sku_tvc_toolkit init-sku \
  --slug crochet_tulip_pot \
  --prefix TULIP \
  --preset crochet_decor \
  --project-id dfcf77a5-5374-4678-9f80-1c5ea7b5c305
```
*(Lệnh này tạo file cấu hình nhẹ `products/crochet_tulip_pot/sku_project.json`. Bạn có thể xem file mẫu hoàn chỉnh cho Crochet tại [`flow_sku_tvc_toolkit/examples/crochet_sunflower_pot_sample.json`](./flow_sku_tvc_toolkit/examples/crochet_sunflower_pot_sample.json)).*

### Bước 2 — Tách Nền Trắng `#FFFFFF` (Nếu Ảnh Gốc Nền Rối) & Sinh Bộ Plate `2K 16:9` + Macro `1K`
- **Nếu ảnh chụp trên bàn gỗ / nền chưa trắng:** Chạy lệnh tách nền trắng tinh `1:1` ngầm trên Google Flow trước:
  ```bash
  python3 -m flow_sku_tvc_toolkit isolate-white \
    --input ~/Downloads/anh_goc_chup_ban.jpg \
    --output products/crochet_tulip_pot/source_white.jpg \
    --preset crochet_decor \
    --project-id dfcf77a5-5374-4678-9f80-1c5ea7b5c305
  ```
- **Từ 1 tấm ảnh nền trắng (hoặc PNG đã tách nền), sinh tự động trọn bộ `REF_1`, `REF_2_CLOSEUP_1024` và toàn bộ `Plate 2K 16:9` (`2560x1440`):**
  ```bash
  python3 -m flow_sku_tvc_toolkit build-plates \
    --input products/crochet_tulip_pot/source_white.jpg \
    --config products/crochet_tulip_pot/sku_project.json
  ```

### Bước 3 — Kiểm Duyệt Từ Cấm (`0` Tốn Credit) & Render Thử Ảnh Số 1 (`check1`)
```bash
# Quét lỗi từ cấm (slider, gimbal, still, cedar, pine, knitted...) & kiểm tra đủ file Plate:
python3 -m flow_sku_tvc_toolkit validate --config products/crochet_tulip_pot/sku_project.json --check-files

# Upload ngầm bộ Plate lên Flow & render thử đúng 1 ảnh đầu tiên để soi tỷ lệ:
python3 -m flow_sku_tvc_toolkit run-images --config products/crochet_tulip_pot/sku_project.json --phase check1
```

### Bước 4 — Chạy Hàng Loạt Các Ảnh Còn Lại, Khóa UUID & Xuất Hàng Loạt Video `Veo 3.1 4s`
```bash
# 1. Chạy ngầm toàn bộ các ảnh còn lại (3 ảnh / wave, tự bấm Retry nếu gặp thẻ 'Không thành công'):
python3 -m flow_sku_tvc_toolkit run-images --config products/crochet_tulip_pot/sku_project.json --phase rest

# 2. Quét danh sách cuộn ảo CDK khóa chính xác 1-1 Scene Key -> UUID vào file JSON:
python3 -m flow_sku_tvc_toolkit map-uuids --config products/crochet_tulip_pot/sku_project.json

# 3. Chạy ngầm toàn bộ dàn Video 4s Veo 3.1 - Fast (2 video / wave, tự căn tâm chống trôi cuộn ảo):
python3 -m flow_sku_tvc_toolkit run-videos --config products/crochet_tulip_pot/sku_project.json --phase all
```
*(Nếu soi QA muốn sửa lẻ đúng 1 ảnh hoặc 1 video nào đó, chỉ cần sửa prompt cảnh đó trong `sku_project.json` và chạy `run-images --phase only --only-key <MÃ_CẢNH>` — công cụ sẽ tự động cập nhật đúng UUID mới của riêng cảnh đó vào `<slug>_scene_uuids.json` mà không làm xô lệch các cảnh còn lại, hoặc dùng `map-uuids --only-key <MÃ_CẢNH>`, sau đó chạy `run-videos --phase only --only-key <MÃ_CẢNH>` y như cách fix lẻ `B16`, `B19`, `B20`, `VB02` hôm nay!).*

### Bước 5 — Tự Động Upscale / Tải Trọn Bộ `1080p` & Ghép File Master MP4
```bash
python3 -m flow_sku_tvc_toolkit download-1080p \
  --config products/crochet_tulip_pot/sku_project.json \
  --out-dir ~/Downloads/CROCHET_TULIP_1080P
```

---

## 4. Quy Tắc Giữ GitHub Không Bao Giờ Bị Rối & Câu Lệnh Giao Việc Nhanh Cho AI

### 4.1. Cái gì lưu lên GitHub vs Cái gì nằm ở Máy Local? (Đã khóa tự động bằng [`.gitignore`](./.gitignore))
- **Đẩy lên GitHub (Siêu nhẹ, chỉ vài KB, đọc phát hiểu ngay):**
  - Toàn bộ bộ công cụ [`flow_sku_tvc_toolkit/`](./flow_sku_tvc_toolkit), sổ tay `.md`, file cấu hình `products/<ten_sp>/sku_project.json`, `plate_manifest.json`, và bảng ánh xạ `*_scene_uuids.json`.
- **Tự động chặn KHÔNG đẩy lên GitHub (`.gitignore` đã khóa sẵn):**
  - Toàn bộ ảnh chụp màn hình kiểm tra `qa_*.jpg`, thư mục `qa/`, thư mục tạm `_dl_*`, file video `.mp4` render nặng, và toàn bộ thư mục `products/*/plates_2k/`, `products/*/clean_refs/` của hàng chục sản phẩm sau này (vì chỉ cần 1 ảnh gốc chạy `build-plates` 1 giây là sinh lại đủ 100%).

### 4.2. Câu Lệnh Mẫu Copy-Paste Giao Việc Cho AI Khi Làm Sản Phẩm Mới (Crochet / Cây / Decor)
> *"Đọc kỹ `PLAYBOOK_CAY_4FT_SANG_CROCHET_VA_FLOW_SOP.md` và `MASTER_LOGIC_GOOGLE_FLOW_EXACT_SKU_TVC_TOOL.md`. Tôi có 1 ảnh sản phẩm mới tại `<ĐƯỜNG_DẪN_ẢNH>` (loại sản phẩm: `<Crochet / Cây / Decor>`, kích thước thật: `<XX cm>`). Hãy dùng `flow_sku_tvc_toolkit` tách nền trắng `#FFFFFF` (nếu cần), dựng bộ Plate `2K 16:9` + `Macro 1K` đúng Preset, viết 20 bối cảnh `Kodak Vision3 250D` + 20 chuyển động `Veo 3.1 4s 3D-Parallax` tuân thủ tuyệt đối `guardrails.py`, chạy ngầm `check1` trên AdsPower để tôi duyệt tỷ lệ trước rồi mới chạy hết lô. Tuyệt đối không gọi `Page.bringToFront` và không commit full bộ ảnh render/QA lên GitHub."*
