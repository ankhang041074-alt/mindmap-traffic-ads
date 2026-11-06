# Handoff Brief — `ATF-9462` (`4ft` / `122cm` Artificial Cedar Pine Tree in Rimmed Black Pot)

- **Google Flow Project URL**: `https://flow.google.com/project/7e3df0de-fb44-4860-945f-f1a7bfbfd70b`
- **Project ID**: `7e3df0de-fb44-4860-945f-f1a7bfbfd70b`
- **Config File**: [`products/atf_9462_cedar_4ft/sku_project.json`](./sku_project.json)
- **Plate UUIDs**: [`products/atf_9462_cedar_4ft/atf_9462_cedar_4ft_plate_uuids.json`](./atf_9462_cedar_4ft_plate_uuids.json)
- **Scene UUIDs**: [`products/atf_9462_cedar_4ft/atf_9462_cedar_4ft_scene_uuids.json`](./atf_9462_cedar_4ft_scene_uuids.json)

---

## 1. Bộ 4 Cảnh & Video Chuẩn Nhất Cuối Cùng (`S45`–`S48` & `V45`–`V48` — Đã Xử Lý `"颜色不够绿 / 太暗了"`)

Được tạo bằng **`🍌 Nano Banana Pro`** trên **100% ảnh Plate gốc chưa chỉnh sửa Python** (`PLATE_01`, `PLATE_06`, `PLATE_07`, `PLATE_08` + `ATF9462_REF_2_CLOSEUP_1024.jpg`) với mệnh đề **`CRITICAL FOLIAGE EXPOSURE LIFT (+1.5 EV BRIGHTNESS & LUSH GREEN TRANSLUCENCY)`** (và `+1.2 EV NATURAL SUNLIT GREEN` cho `S47`):

| Scene Key | Video Key | Plate Gốc | Scene Media UUID (Flow) | 2-Zone Motion (`bg` / `fg`) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `S45_PRO_EXACT_LIMESTONE_TERRACE_ARCHED_WINDOW_OLIVE_PAIR` | `V45_PRO_EXACT_LIMESTONE_TERRACE_ARCHED_WINDOW_OLIVE_PAIR` | `PLATE_01_PORCH_PAIR_52PCT.png` | `507ac7f9-0ef9-4450-b450-d2fcecacc5e2` | `bg=53.49` / `fg=38.65` | **PASS** |
| `S46_PRO_EXACT_SUNLIT_BAY_WINDOW_SEAT_HERO_LEFT` | `V46_PRO_EXACT_SUNLIT_BAY_WINDOW_SEAT_HERO_LEFT` | `PLATE_06_LEFT_HERO_70PCT.png` | `dac3119e-b615-4e11-bfcd-e60e3a7deab9` | `bg=49.10` / `fg=54.20` | **PASS** |
| `S47_PRO_EXACT_OAK_STAIRCASE_GARDEN_WINDOW_HERO_RIGHT` | `V47_PRO_EXACT_OAK_STAIRCASE_GARDEN_WINDOW_HERO_RIGHT` | `PLATE_07_RIGHT_HERO_70PCT.png` | `cf9c1048-8c98-403b-972b-c8f4cc2c1e0e` | `bg=61.20` / `fg=65.24` | **PASS** |
| `S48_PRO_EXACT_FLUTED_OAK_CONSOLE_ARCH_MIRROR_SUNBEAM_PAIR` | `V48_PRO_EXACT_FLUTED_OAK_CONSOLE_ARCH_MIRROR_SUNBEAM_PAIR` | `PLATE_08_PAIR_MEDIUM_58PCT.png` | `7206ca42-0d0b-49a8-b210-cc1f62b1f83e` | `bg=30.66` / `fg=48.50` | **PASS** |

---

## 2. Lưu Ý Kỹ Thuật Quan Trọng Khi Làm Tiếp Ở Nhà

1. **Khóa Model `🍌 Nano Banana Pro`**:
   - Hàm [`ensure_image_mode`](../../flow_sku_tvc_toolkit/flow_cdp.py) đã được sửa để luôn tìm và chuyển về **`🍌 Nano Banana Pro`** kể cả khi thanh công cụ nằm sát đáy màn hình (`y >= 1100`). Tuyệt đối không để rơi về `Nano Banana 2.1` (sẽ làm cây tối thui hoặc vẽ nền giả).
2. **Không dùng Python chỉnh màu Plate gốc**:
   - Chỉ dùng Plate gốc trong `products/atf_9462_cedar_4ft/plates_2k/` kèm `clean_refs/ATF9462_REF_2_CLOSEUP_1024.jpg` và mệnh đề `+1.5 EV BRIGHTNESS & LUSH GREEN TRANSLUCENCY` / `+1.2 EV NATURAL SUNLIT GREEN` trong prompt.
3. **Lệnh chạy nhanh ở nhà**:
   ```bash
   # Tạo ảnh (4 ảnh / 1 wave, không tải ảnh 2K về máy)
   python3 -m flow_sku_tvc_toolkit render-images --config products/atf_9462_cedar_4ft/sku_project.json --only S45,S46,S47,S48

   # Tạo video (4 video / 1 wave)
   python3 -m flow_sku_tvc_toolkit render-videos --config products/atf_9462_cedar_4ft/sku_project.json --only V45,V46,V47,V48

   # Kiểm định video + xuất lưới 16 khung hình ffmpeg (qa/video_grids/*_16f_grid.jpg)
   python3 -m flow_sku_tvc_toolkit audit-videos --config products/atf_9462_cedar_4ft/sku_project.json --only V45,V46,V47,V48
   ```
