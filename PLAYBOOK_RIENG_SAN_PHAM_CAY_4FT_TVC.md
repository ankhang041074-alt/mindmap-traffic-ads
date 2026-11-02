# Sổ Tay Đạo Diễn & Lưu Ý Riêng Cho Dòng Sản Phẩm Cây Đặt Sàn (`4ft` / `1.20m – 1.30m`)

> [!IMPORTANT]
> **Mục đích tài liệu này:** Lưu trữ tách biệt **toàn bộ quy tắc tỷ lệ vật lý, phối cảnh kiến trúc, góc đặt chậu và bài học hậu kỳ** dành riêng cho **nhóm sản phẩm Cây cảnh / Cây giả đặt sàn (`tree_4ft`)** — đúc kết qua 3 lô sản xuất thực tế (`cedar_4ft_10s`, `barrel_cedar_20`, `products/cedar_sqpot_batch3_20`) — để **không bị lẫn lộn** khi chuyển sang làm các dòng sản phẩm khác (như `Crochet`, đồ gốm để bàn, phụ kiện nhỏ), đồng thời sẵn sàng tái sử dụng chuẩn `100%` bất cứ khi nào quay lại làm SKU cây mới.

---

## 1. Hồ Sơ 4 Lô Sản Phẩm Cây Đã Triển Khai

| Lô / Thư mục | Đặc điểm vật lý SKU Cây | Quy mô | Điểm nhấn kỹ thuật đã khóa |
| :--- | :--- | :---: | :--- |
| **Lô 1:** [`cedar_4ft_10s/`](./cedar_4ft_10s) | Cây tùng lá đúc PE 2 tông xanh `4ft`, **chậu vuông đen cao vát đáy** | `20 Ảnh` + `20 Video 4s` | Auto-split tách 1 cây chuẩn từ ảnh 2-pack; chuẩn hóa vật neo cửa chính `2.4m` & kệ `85cm` |
| **Lô 2:** [`barrel_cedar_20/`](./barrel_cedar_20) (`ATF-9422`) | Cây tùng `4ft+` tán lá dẹt mảnh, **chậu thùng gỗ xám nâu 3 đai sắt đen** | `20 Ảnh` + `20 Video 4s` | Khóa ảnh cận `REF_2_CLOSEUP_1024` (`1.65x`) chống vẽ lại lá thông nhọn (`B16`); khóa `56%` phòng biển (`B20`) & lùi ghế daybed hồ bơi `1.3m` (`B19`) |
| **Lô 3:** [`products/cedar_sqpot_batch3_20/`](./products/cedar_sqpot_batch3_20) | Cây tùng PE 2 tông xanh `4ft`, **chậu vuông đen cao vát đáy** (20 bối cảnh kiến trúc mới `S21..S40`) | `20 Ảnh` + `20 Video 4s` | Khóa 4 bài học đạo diễn nâng cao: **Cấm hạt cát vàng ảo**, **Đặt xéo bám đúng đường chân tường `3/4`**, **Cấm mức `36%` làm cây teo nhỏ**, **Cấm ghế tiền cảnh tự chạy băng chuyền** |
| **Lô 4:** [`products/cedar_roundpot_20/`](./products/cedar_roundpot_20) | Cây lá đúc PE 2 tông xanh `4ft` tán rộng, lộ gốc gỗ nâu `~5cm`, **chậu nhựa tròn trụ đen mờ nhỏ gọn `5in x 5.5in`** (`R01..R20`) | `20 Ảnh` + `20 Video 4s` | Khóa **Cấm cửa tự mở / cửa kính tự trượt (`Poltergeist Doors`)**, **Cấm 2 cây tự chạy lại gần nhau trên sàn (`Sliding Trees`)**, **Nắng ôm viền lá (`Optical Sunlight Rim-Wrap`)**, và **Cấm ghép `PLATE_03` đặt xéo với cổng vòm chính diện (`R03`)** |

---

## 2. Năm Quy Tắc Sống Còn Dành Riêng Cho Sản Phẩm Cây Đặt Sàn (`tree_4ft`)

### Quy tắc 1: Ngưỡng sàn chiều cao tối thiểu trên khung `16:9` là `46% – 50%` (CẤM TUYỆT ĐỐI mức `36%`)
- **Bài học thực tế (`B20` Lô 2 & `S35` Lô 3):** Khi đặt 1 cây đơn ở mức `36%` chiều cao khung hình `16:9`, diện tích cây chỉ chiếm chưa tới `2.5%` toàn màn hình. Dù phòng ăn dầm gỗ sồi và nắng xiên đẹp như tạp chí kiến trúc, sản phẩm lập tức bị lọt thỏm thành đồ decor phụ và nhìn chỉ cao như cây `90cm` (`3ft`).
- **Chuẩn đã khóa trong [`TREE_4FT_PRESET`](./flow_sku_tvc_toolkit/presets.py):**
  - **Đại cảnh phòng rộng trần dầm gỗ `3.3m` (`PLATE_07`):** Tối thiểu **`50%`** (`bottom_margin = 6.0%`). Phía trên ngọn cây vẫn còn nguyên **`44%` khoảng không trần** để khoe trọn dầm gỗ sồi và cửa vòm nắng xiên, nhưng cây đĩnh đạc làm chủ khung hình.
  - **Trung-đại cảnh phòng khách view biển / hồ (`PLATE_08`):** **`56%`** (`Goldilocks coastal scale`).
  - **Cận trung Hero 1 cây (`PLATE_04`, `PLATE_05`, `PLATE_09`):** **`70% – 76%`**.
  - **Cặp 2 cây đối xứng cửa chính `2.4m` (`PLATE_01`) / Bàn console `85cm` (`PLATE_02`):** **`52%`** và **`62%`**.

### Quy tắc 2: Vật neo nội thất đặt cạnh cây bắt buộc nằm CÙNG MẶT PHẲNG CHIỀU SÂU với chậu
- **Lỗi phối cảnh đánh lừa mắt (`S35`):** Nếu kê một chiếc tủ buffet gỗ (`85cm`) chạy dọc tiến sát về phía ống kính ở góc phải, mặt tủ gần ống kính sẽ phình cao lên ngang ngửa cái cây đứng lùi ở góc sau — làm mắt người tưởng cây chỉ cao hơn mặt tủ `10–15cm` (tức cây cao có `~95cm`).
- **Cách đặt chuẩn đạo diễn:**
  - Tủ buffet / kệ console `80–85cm` đặt cạnh cây bắt buộc **kê ngang trên cùng mặt phẳng sàn (`y_base` ngang nhau)** với đáy chậu cây → Khi đó tủ chỉ cao bằng **`~65% – 68%`** tổng chiều cao cây, ngọn cây **vọt cao hơn mặt tủ rõ `~40cm`** (khóa cứng cảm giác cây cao `1.25m / 4ft`).
  - Cửa chính `2.40m–2.45m`: Tay nắm cửa (`1.05m`) luôn phải nằm **thấp hơn ngọn cây `~15–18cm`** (cây cao đúng `1/2` cánh cửa).
  - Bệ lò sưởi (`1.15m–1.20m`): Mặt kệ đá ngang bằng hoặc thấp hơn ngọn cây một chút.
  - Không đặt lưng ghế sofa hay ghế daybed khổng lồ chắn sát góc dưới tiền cảnh nuốt mất `15–20%` khung hình; mọi ghế lớn phải **lùi ra sau chậu cây `1.2m – 1.4m`**.

### Quy tắc 3: Đặt đôi (`2 cây`) ở góc xiên `3/4` — Bắt buộc bám đúng Đường Chân Tường & Có Lý Do Kiến Trúc
- **Bài học thực tế (`S25` lan can hồ & `S22` cổng sắt Tuscan):**
  1. **Không để cây xa trôi ra giữa lối đi hành lang:** Nếu hai đáy chậu đặt gần như ngang nhau (`5.0%` và `8.2%`) nhưng bối cảnh là dải lan can đá hút chéo sâu lên `~22%` khung hình, cây trái sẽ kê sát lan can còn cây phải bị trôi thò ra chắn giữa đường đi `~1.5m` — ngoài đời không ai đặt chậu cây giữa lối đi như vậy.
     - **Chuẩn tọa độ [`PLATE_03_PAIR_DIAGONAL_3Q_16x9`](./flow_sku_tvc_toolkit/presets.py):** Cây gần trái `height = 60%, bottom_margin = 5.5%`; cây xa phải nâng đáy xéo hẳn lên **`bottom_margin = 20.5%`**, thu chiều cao theo điểm tụ đường chân trời `1.30m` về **`height = 46%`** → Cả 2 đáy chậu cùng trượt xéo bám sát mép chân tường/lan can `15–20cm` và trong không gian 3D đều đọc đúng `4ft` bằng nhau.
  2. **Phải có điểm mở kiến trúc ở giữa 2 cây:** Tuyệt đối không đặt 2 cây chơ vơ cách nhau vài mét dọc một đoạn lan can đặc trống không. Ở giữa cặp 2 cây bắt buộc phải là **lối bậc tam cấp mở xuống vườn/bến hồ, cổng vòm, cửa đôi kính Pháp, lò sưởi hoặc bàn console**.
  3. **CẤM TUYỆT ĐỐI ghép `PLATE_03` đặt xéo với Cổng Vòm / Cửa Đôi / Lò Sưởi / Bàn Console chính diện (`Bài học thực tế R03 Lô 4`):**
     - **Nguyên nhân gốc rễ ở Bước Ảnh (`Stage 2`):** Khi dùng `PLATE_03_PAIR_DIAGONAL_3Q` (cây trái đặt thấp ở `bottom_margin = 7.5%–8.0%`, cây phải nâng cao lên `bottom_margin = 20.5%–21.5%`) nhưng trong prompt lại yêu cầu vẽ **`open carved stone archway portal` (cổng vòm đá dẫn vào hành lang)**, model `Nano Banana Pro` sẽ ưu tiên vẽ **cổng vòm chính diện 1 điểm tụ (`mặt tường nằm ngang thẳng mặt ở y ≈ 22%`)**. Hậu quả là chỉ có cây bên phải (`y = 21.5%`) đứng sát trụ cổng, còn **cây bên trái (`y = 8.0%`) bị lòi tuốt ra giữa sân đá cách cổng tới 2 mét** — tạo ra bố cục đặt xéo vô lý ngay trước cổng chính diện.
     - **Quy tắc bắt buộc kiểm duyệt ngay ở Bước Tạo Ảnh (`Stage-2 Wall-Seam Collinearity Gate`) trước khi tạo Video:**
       1. **Khóa ở Code (`guardrails.py`):** Mọi bối cảnh có **cổng vòm (`archway / portal / gate / portico`), cửa chính, lò sưởi (`mantel / fireplace`), bàn `console`, kệ sách (`bookcase / alcove`)** bắt buộc phải dùng **Plate đôi đối xứng ngang [`PLATE_01_PAIR_DOOR_52PCT_16x9`](./flow_sku_tvc_toolkit/presets.py) hoặc [`PLATE_02_PAIR_MEDIUM_62PCT_16x9`](./flow_sku_tvc_toolkit/presets.py)** (`bottom_margin = 7.5%–8.0%` bằng nhau cả 2 bên) để 2 chậu cây đứng đối xứng ôm sát 2 trụ cổng. Chỉ dùng `PLATE_03_PAIR_DIAGONAL_3Q` cho dải lan can đá thấp chạy xiên liên tục (`continuous low balustrade railing / coastal steps` như `R06`).
       2. **Khóa ở Bước Kiểm Duyệt Ảnh (`Stage 2`):** Ngay khi ảnh vừa tạo xong, bắt buộc kiểm tra **Đường chân tường (`wall-to-floor seam`) có đi qua sát đáy của CẢ 2 chậu cây (cùng cách chân tường `15–18cm`) hay không**. Nếu 1 chậu sát trụ cổng còn 1 chậu trôi ra giữa sân → **Xoá ảnh và tạo lại ngay ở Bước Ảnh**, tuyệt đối không đưa ảnh sai bố cục sang Bước Video làm tốn lượt render video!
  4. **Lưu ý riêng giữa Chậu Vuông vs Chậu Tròn:**
     - Với **Chậu Tròn / Thùng Gỗ tròn (`barrel_cedar_20`)**: Xoay góc tường xiên `15°–20°` vẫn tự nhiên vì miệng tròn không lộ góc cạnh đáy.
     - Với **Chậu Vuông (`cedar_sqpot`)**: Vì ảnh cutout 2D đã cố định góc xoay mặt trước của chậu vuông, **ưu tiên đặt cặp 2 cây ở mặt tiền chính diện hoặc xiên rất nhẹ (`<= 5°`)** để cạnh đáy chậu vuông luôn song song mạch gạch lát sàn. Còn với các bối cảnh **hành lang / lan can hút chéo sâu `3/4`**, dùng **1 cây Hero đặt gọn vào góc trụ đầu hành lang (`PLATE_04 / 05 / 08`)** là chân thật `100%` ngoài đời!

### Quy tắc 4: Lộ trọn `100%` thân & đáy chậu trên sàn (Không đè đôn/ghế tiền cảnh, không zoom cắt đáy chậu)
- **Ở khâu tạo Ảnh (`Nano Banana Pro`):** Tuyệt đối không để đôn vải (`ottoman`), ghế gỗ hay mép bàn tiền cảnh che ngang phần thân dưới của chậu cây (như lỗi đôn che nửa chậu trái ở `S24`). Toàn bộ 4 cạnh chậu từ miệng xuống chân đế tiếp sàn + bóng đổ tiếp xúc (`contact shadow`) phải lộ rõ `100%`.
- **Ở khâu tạo Video (`Veo 3.1 - Fast`):** Khi 2 chậu cây đặt ở `bottom_margin = 5.0% – 5.5%` (khá gần mép dưới), không dùng lệnh `push-in closer` quá gắt làm khung hình cắt cụt đáy chậu ở giây thứ 3–4 (như các bản nháp đã xoá của `V23`, `V30`). Luôn ghi rõ: `keeping the entire planters from top rim to bottom floor base completely visible head-to-toe inside the frame`.

### Quy tắc 5: Khóa từ vựng hình thái lá cây & Ánh sáng TVC sạch tự nhiên
- **Từ cấm làm biến dạng giống cây (`TREE_4FT_PRESET`):** `cedar`, `pine`, `topiary`, `slender`, `teardrop`, `chartreuse`, `conifer`, `spruce`, `cypress`, `juniper`, `spiky needles`. Luôn dùng mô tả hình thái học thật của lá kèm ảnh `REF_2_CLOSEUP_1024`: `two-tone green fine feathery flat-fan molded leaf sprigs, airy outer branchlet tips`.
- **Ánh sáng & Chuyển động TVC thật (`Veo 3.1 - Fast`):**
  - **CẤM vĩnh viễn hạt cát vàng / kim tuyến bay ảo:** Không bao giờ viết `dust mote`, `dust motes`, `golden dust`, `floating dust`, `glitter`, `sparkle`, `bokeh particles` (vì `Veo 3.1` sẽ đẻ ra hạt cát vàng tự phát sáng bay ra từ cả gầm cầu thang tối hoặc làm ố vàng ngọn cây như `V40, V31, V26`). Thay bằng: luồng nắng tự nhiên chiếu xiên trên tường/sàn, bóng lá cây ngoài sân khẽ đung đưa, rèm voan khẽ thở nhẹ, hoặc mặt nước hồ lấp lánh (`shimmer`).
  - **CẤM gán động từ chuyển động cho bàn ghế tiền cảnh:** Không bao giờ viết `foreground bench/ottoman/chair sweeps or glides...` (vì `Veo 3.1` sẽ giữ camera đứng im rồi cho cái ghế tự bò ngang qua phòng như `V30, V24`). Luôn khóa cứng: `all furniture, architectural elements, and both potted plants remain 100% stationary anchored to the floor while ONLY the 3D camera moves smoothly`.
  - **CẤM tuyệt đối Cửa Tự Mở / Cửa Kính Lùa Tự Trượt (`Poltergeist Doors`):**
    * Đang quay TVC sản phẩm cây cảnh chứ không phải intro bước vào nhà — việc cánh cửa đôi tự động xoay mở hoặc cửa kính lùa tự trượt ngang rất rợn người và phi thực tế.
    * **Từ khâu tạo Ảnh (`Nano Banana Pro`):** Không dùng cánh cửa đôi khép hờ hoặc khung cửa kính lùa sát cây; thay bằng **vòm đá mở (`open stone archway`), tường phào chỉ/lò sưởi, kệ sách âm tường, đài phun nước tường đá, cửa sổ khung cố định trên bệ tường đá (`fixed picture window above stone knee-wall`), hoặc hiên cột đá mở (`open-air colonnade verandah`)**.
    * **Từ khâu tạo Video (`Veo 3.1 - Fast`):** Bộ lọc `FORBIDDEN_VIDEO_DOOR_MOTION_REGEXES` trong `guardrails.py` chặn mọi câu lệnh mở/xoay/trượt cửa; đồng thời không nhắc từ `door / doors / sliding / casement / shoji` trong prompt video để `Veo 3.1` không tự kích hoạt hiệu ứng mở cửa.
  - **CẤM tuyệt đối 2 Chậu Cây Tự Chạy Lại Gần / Ra Xa Nhau Trên Sàn (`Sliding Trees`) & Công Thức Nắng Ôm Viền Lá (`Optical Sunlight Rim-Wrap`):**
    * Khi nâng lề sàn dưới đáy chậu lên **`7.5%–8.0%`** (thay vì `4.5%–5.0%` sát mép dưới khung `16:9`), cây vừa đứng lùi sát chân tường tự nhiên hơn (`15–18cm`), vừa có đủ khoảng sàn đệm phía dưới để khi `Veo 3.1` thực hiện cú đẩy camera tiến 3D góc thấp (`low-horizon 3D forward camera push-in`), toàn bộ căn phòng và 2 chậu cây phóng đại đồng bộ đúng luật phối cảnh 3D mà **không bao giờ bị cắt đáy chậu hay ép 2 chậu cây tự trượt trên sàn**.
    * Cấm tuyệt đối các cụm từ mâu thuẫn phối cảnh như `"no zoom-in"`, `"constant viewing distance"`, `"~10 percent"` trong prompt video (đã đưa vào `FORBIDDEN_VIDEO_FREEZE_SUBSTRINGS`).
    * Khi tạo ảnh tĩnh (`Nano Banana Pro`), cho phép ánh nắng môi trường ôm nhẹ vào đầu lá xanh non (`allowing warm directional sunlight to naturally wrap the outer fresh spring-green branchlet tips with crisp optical rim-light highlights, natural leaf-to-leaf micro-shadow depth, and floor bounce light`) để cây có chi tiết sắc nét và hòa quyện ánh sáng thật 100% mà vẫn giữ nguyên dáng lá PE và chậu gốc.
