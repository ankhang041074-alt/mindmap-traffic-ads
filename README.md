# Hệ Thống Sản Xuất Ảnh `2K 16:9` & Video TVC `4s` Chuẩn `100%` SKU Trên Google Flow (AdsPower Silent CDP)

Repository này đóng gói trọn bộ **công cụ tự động hóa (`flow_sku_tvc_toolkit`)**, **kiến trúc Khóa Khuôn Kép (`2K 16:9 Cutout Plate` + `1K Macro Ref`)**, và **sổ tay lưu ý thực chiến** để từ **1 tấm ảnh sản phẩm gốc duy nhất** sản xuất hàng loạt ảnh bối cảnh điện ảnh (`Nano Banana Pro`) & video `3D-Parallax 4 giây` (`Veo 3.1 - Fast`) chạy ngầm 100% trên AdsPower — áp dụng cho **Cây cảnh `4ft`, Đồ len móc `Crochet`, và các dòng sản phẩm Decor/Thủ công mới** mà **không phải up full bộ ảnh/video nặng làm rối GitHub**.

---

## 1. Bản Đồ Điều Hướng Nhanh (Đọc Đúng File Cần Tìm Trong 10 Giây)

### A. Sổ Tay & Quy Trình Cốt Lõi (Đọc Đầu Tiên Khi Làm Sản Phẩm Mới)
1. **[`PLAYBOOK_CAY_4FT_SANG_CROCHET_VA_FLOW_SOP.md`](./PLAYBOOK_CAY_4FT_SANG_CROCHET_VA_FLOW_SOP.md)** — **Sổ tay thực chiến quan trọng nhất**:
   - Đúc kết 5 bài học xương máu từ 2 SKU Cây `4ft` (`B15`, `B16`, `B19`, `B20`, `VB02`).
   - Hướng dẫn chi tiết **5 điểm phải đổi khi áp dụng quy trình tách nền trắng -> Plate `2K` sang đồ `Crochet` (`8cm–45cm`)** và các sản phẩm đặt bàn/kệ.
   - SOP thao tác ngầm Google Flow từng bước từ ảnh gốc đến xuất gộp `1080p`.
2. **[`MASTER_LOGIC_GOOGLE_FLOW_EXACT_SKU_TVC_TOOL.md`](./MASTER_LOGIC_GOOGLE_FLOW_EXACT_SKU_TVC_TOOL.md)** — Kiến trúc kỹ thuật chuyên sâu 4 tầng của hệ thống (Sơ đồ luồng, Ma trận tỷ lệ vật lý, Thuật toán chống trôi cuộn ảo `CDK Virtual Scroll`, Tương thích kép URL `/asb/` & `flow-content`, tự tắt nút `'Tác nhân'`).
3. **[`HUONG_DAN_LAM_TIEP_KHI_VE_NHA.md`](./HUONG_DAN_LAM_TIEP_KHI_VE_NHA.md)** — Quy tắc chống văng phiên đăng nhập Google Flow trên AdsPower khi chuyển đổi giữa máy Công ty <-> máy Nhà (`home_helper.py`).

---

### B. Bộ Toolkit Chuẩn Dùng Chung Cho Mọi Sản Phẩm Mới (`Crochet`, `Cây`, `Decor`)
- **[`flow_sku_tvc_toolkit/`](./flow_sku_tvc_toolkit)** — CLI đóng gói gọn toàn bộ quy trình:
  - [`presets.py`](./flow_sku_tvc_toolkit/presets.py): Ma trận `% chiều cao khung`, khoảng nâng đáy `bottom_margin`, khung cắt Macro `1024x1024` và bộ khóa `STRICT_CUTOUT_LOCK` cho `tree_4ft`, `crochet_coaster`, `crochet_decor`, `crochet_bag`, `generic_decor`.
  - [`plate_engine.py`](./flow_sku_tvc_toolkit/plate_engine.py): Thuật toán `Pillow` **Border-Flood** tự khử viền xám studio thành `#FFFFFF` tuyệt đối (bảo toàn 100% chi tiết len trắng/kem bên trong sản phẩm) và sinh bộ Plate `2560x1440` sai số tỷ lệ `0.0%`.
  - [`guardrails.py`](./flow_sku_tvc_toolkit/guardrails.py): Bộ chặn tự động từ cấm làm méo cây (`cedar, pine, topiary...`), từ làm sai mũi móc len (`knitted, knitting, felt, CGI...`), từ làm `Veo 3.1` lộ thanh sắt (`slider, gimbal, dolly, rig...`) hoặc đứng im (`still, motionless, frozen, 5%...`).
  - [`flow_cdp.py`](./flow_sku_tvc_toolkit/flow_cdp.py) & [`cli.py`](./flow_sku_tvc_toolkit/cli.py): Động cơ CDP chạy ngầm tuyệt đối (`Emulation.setFocusEmulationEnabled(true)`, `0` gọi `Page.bringToFront`) cho cả 5 khâu: `isolate-white` -> `run-images` -> `map-uuids` -> `run-videos` -> `download-1080p`.
  - [`examples/crochet_sunflower_pot_sample.json`](./flow_sku_tvc_toolkit/examples/crochet_sunflower_pot_sample.json): Cấu hình mẫu chuẩn cho sản phẩm **Crochet**.

---

### C. Hồ Sơ Lưu Trữ Các Dự Án Sản Phẩm Đã Triển Khai
1. **[`barrel_cedar_20/`](./barrel_cedar_20)** — **SKU Cây #2: Cây Cedar `4ft+` Chậu Thùng Gỗ 3 Đai Sắt Đen (`ATF-9422`)**
   - 20 kịch bản ảnh `16:9` (`B01..B20`), bảng ánh xạ [`barrel20_scene_uuids.json`](./barrel_cedar_20/barrel20_scene_uuids.json), 20 kịch bản video `4s` (`VB01..VB20`) và script tải/ghép `1080p` [`download_and_merge_atf_9422_1080p.py`](./barrel_cedar_20/download_and_merge_atf_9422_1080p.py).
2. **[`cedar_4ft_10s/`](./cedar_4ft_10s)** — **SKU Cây #1: Cây Cedar `4ft` Chậu Vuông Đen Cao Vát Đáy**
   - 20 kịch bản ảnh & video (`S01..S20` / `V01..V20`) và ghi chú dự án [`NOTE_CEDAR_4FT_LOGIC_VA_LAM_TIEP_O_NHA.md`](./cedar_4ft_10s/NOTE_CEDAR_4FT_LOGIC_VA_LAM_TIEP_O_NHA.md).
3. **[`flow_web_intro/`](./flow_web_intro)** — **Dự Án Crochet Đế Lót Ly Hoa Bật Mở 3D (`2-Frame Reverse Surgical Start -> End`)** & lõi kết nối CDP [`gen_batch_images.py`](./flow_web_intro/gen_batch_images.py), [`home_helper.py`](./flow_web_intro/home_helper.py).

---

## 2. Quy Trình 5 Lệnh Chạy Một Sản Phẩm Mới (Gọn Nhẹ, Không Up Full Hình Lên Git)

```bash
# 1. Tạo file cấu hình JSON nhẹ cho sản phẩm mới trong products/<slug>/
python3 -m flow_sku_tvc_toolkit init-sku \
  --slug crochet_tulip_pot --prefix TULIP --preset crochet_decor \
  --project-id dfcf77a5-5374-4678-9f80-1c5ea7b5c305

# 2. (Tùy chọn nếu ảnh gốc chụp bàn gỗ chưa tách nền trắng) Tách sang nền trắng #FFFFFF trên Flow:
python3 -m flow_sku_tvc_toolkit isolate-white \
  --input ~/Downloads/anh_goc.jpg --output products/crochet_tulip_pot/white.jpg \
  --preset crochet_decor --project-id dfcf77a5-5374-4678-9f80-1c5ea7b5c305

# 3. Sinh bộ REF_1, REF_2_CLOSEUP_1024 & toàn bộ Plate 2K 16:9 (#FFFFFF) tại máy local:
python3 -m flow_sku_tvc_toolkit build-plates \
  --input products/crochet_tulip_pot/white.jpg \
  --config products/crochet_tulip_pot/sku_project.json

# 4. Kiểm duyệt prompt & chạy ngầm trên AdsPower (test 1 ảnh -> chạy nốt -> map UUID -> chạy Video 4s):
python3 -m flow_sku_tvc_toolkit validate --config products/crochet_tulip_pot/sku_project.json --check-files
python3 -m flow_sku_tvc_toolkit run-images --config products/crochet_tulip_pot/sku_project.json --phase check1
python3 -m flow_sku_tvc_toolkit run-images --config products/crochet_tulip_pot/sku_project.json --phase rest
python3 -m flow_sku_tvc_toolkit map-uuids --config products/crochet_tulip_pot/sku_project.json
python3 -m flow_sku_tvc_toolkit run-videos --config products/crochet_tulip_pot/sku_project.json --phase all

# 5. Tự động tải 1080p từ tab Video & nối thành file Master MP4:
python3 -m flow_sku_tvc_toolkit download-1080p \
  --config products/crochet_tulip_pot/sku_project.json --out-dir ~/Downloads/TULIP_1080P
```

---

## 3. Chính Sách Giữ Repo Sạch Gọn (`.gitignore`)

Để làm hàng chục sản phẩm sau này mà repo không bao giờ phình dung lượng hay rối mắt:
- **Lưu trên GitHub:** Mã nguồn `.py`, tài liệu lưu ý `.md`, cấu hình kịch bản `sku_project.json`, `plate_manifest.json`, và bảng `*_scene_uuids.json`.
- **Tự động bỏ qua ở Local (`.gitignore`):** Ảnh chụp màn hình `qa_*.jpg`, thư mục `qa/`, thư mục tải tạm `_dl_*`, video `.mp4` xuất ra, các script nháp `fix_*.py` / `retry_*.py`, và thư mục ảnh sinh tự động `products/*/plates_2k/`, `products/*/clean_refs/`.
