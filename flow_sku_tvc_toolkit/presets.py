"""
Calibrated physical scale matrices, macro crop windows, prompt locks, and
category-specific guardrails for Trees (4ft floor-standing), Crochet products
(coasters, plush/potted decor, bags), and general physical SKUs.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class PlacementSpec:
    """Single product cutout placement on a 2560x1440 (#FFFFFF) 16:9 plate."""
    height_pct: float
    center_x_pct: float
    bottom_margin_pct: float = 0.055
    max_width_pct: float = 0.46


@dataclass(frozen=True)
class PlateTemplate:
    """Definition of one 2K 16:9 plate layout within a category preset."""
    code: str
    suffix: str
    description_vi: str
    placements: Tuple[PlacementSpec, ...]


@dataclass(frozen=True)
class CategoryPreset:
    """Complete physical & prompt configuration for a product category."""
    name: str
    label_vi: str
    physical_size_note_vi: str
    recommended_lens: str
    scale_anchors_vi: str
    # Relative crop window (x0, y0, x1, y1) inside tight product bbox for REF_2_CLOSEUP_1024
    macro_focus_box: Tuple[float, float, float, float]
    plates: Tuple[PlateTemplate, ...]
    single_cutout_lock_header: str
    pair_cutout_lock_header: str
    white_isolation_prompt: str
    forbidden_image_substrings: Tuple[str, ...]
    forbidden_image_regexes: Tuple[str, ...]


TREE_4FT_PRESET = CategoryPreset(
    name="tree_4ft",
    label_vi="Cây cảnh / Cây giả đặt sàn ~4ft (1.20m – 1.30m)",
    physical_size_note_vi="Cao ~1.20m–1.30m (chậu + tán): ngang 1/2 cửa chính 2.4m (cao hơn tay nắm cửa ~15–18cm), ngang mặt kệ lò sưởi 1.15m–1.22m, vượt lưng sofa 78cm khoảng 45–50cm.",
    recommended_lens="35mm–50mm architectural cinema lens (Kodak Vision3 250D)",
    scale_anchors_vi="Cửa chính 2.4m–2.45m, tay nắm cửa (~1.05m), bệ lò sưởi (1.15m–1.22m), bàn console/tủ buffet (85cm), lưng sofa (78cm).",
    macro_focus_box=(0.16, 0.28, 0.84, 0.98),
    plates=(
        PlateTemplate(
            code="01",
            suffix="PLATE_01_PAIR_DOOR_52PCT_16x9",
            description_vi="2 cây đối xứng cửa chính 2.4m / lò sưởi trần cao 3.3m (52% chiều cao khung)",
            placements=(
                PlacementSpec(height_pct=0.52, center_x_pct=0.29, bottom_margin_pct=0.055, max_width_pct=0.34),
                PlacementSpec(height_pct=0.52, center_x_pct=0.71, bottom_margin_pct=0.055, max_width_pct=0.34),
            ),
        ),
        PlateTemplate(
            code="02",
            suffix="PLATE_02_PAIR_MEDIUM_62PCT_16x9",
            description_vi="2 cây đối xứng cận trung 50mm: bàn Console 85cm, cửa đôi Pháp, cổng vòm (62%)",
            placements=(
                PlacementSpec(height_pct=0.62, center_x_pct=0.27, bottom_margin_pct=0.050, max_width_pct=0.36),
                PlacementSpec(height_pct=0.62, center_x_pct=0.73, bottom_margin_pct=0.050, max_width_pct=0.36),
            ),
        ),
        PlateTemplate(
            code="03",
            suffix="PLATE_03_PAIR_DIAGONAL_3Q_16x9",
            description_vi=(
                "2 cây đặt xéo bám dọc theo cùng đường chân tường/hành lang góc 3/4 "
                "(cây gần trái 60% đáy 5.5%, cây xa phải 46% đáy nâng xéo lên 20.5% theo điểm tụ — "
                "kẹp 2 bên lối mở bậc thềm/cửa Pháp để cả 2 cùng sát tường và bằng nhau 4ft trong không gian 3D, không trôi ra giữa lối đi)"
            ),
            placements=(
                PlacementSpec(height_pct=0.60, center_x_pct=0.28, bottom_margin_pct=0.055, max_width_pct=0.36),
                PlacementSpec(height_pct=0.46, center_x_pct=0.70, bottom_margin_pct=0.205, max_width_pct=0.30),
            ),
        ),
        PlateTemplate(
            code="04",
            suffix="PLATE_04_SINGLE_HERO_LEFT_72PCT_16x9",
            description_vi="1 cây Hero bên trái 50mm: phòng khách, phòng đọc sách, sunroom (72%)",
            placements=(
                PlacementSpec(height_pct=0.72, center_x_pct=0.29, bottom_margin_pct=0.050, max_width_pct=0.42),
            ),
        ),
        PlateTemplate(
            code="05",
            suffix="PLATE_05_SINGLE_HERO_RIGHT_70PCT_16x9",
            description_vi="1 cây Hero bên phải 50mm: hiên nhà, đảo bếp, cầu thang kính (70%)",
            placements=(
                PlacementSpec(height_pct=0.70, center_x_pct=0.71, bottom_margin_pct=0.050, max_width_pct=0.42),
            ),
        ),
        PlateTemplate(
            code="06",
            suffix="PLATE_06_SINGLE_WIDE_55PCT_16x9",
            description_vi="1 cây trung-đại cảnh bên trái: phòng rộng có nội thất trung cảnh (55%)",
            placements=(
                PlacementSpec(height_pct=0.55, center_x_pct=0.30, bottom_margin_pct=0.060, max_width_pct=0.36),
            ),
        ),
        PlateTemplate(
            code="07",
            suffix="PLATE_07_SINGLE_WIDE_RIGHT_50PCT_16x9",
            description_vi=(
                "1 cây đại cảnh nắng kiến trúc 35mm-50mm trần dầm gỗ cao 3.3m thấy trọn bàn ăn & cửa vòm "
                "(ngưỡng sàn tối thiểu 50% để cây chuẩn 4ft nổi bật vượt tủ buffet 85cm ~40cm, cấm dùng 36% gây teo nhỏ cây)"
            ),
            placements=(
                PlacementSpec(height_pct=0.50, center_x_pct=0.73, bottom_margin_pct=0.060, max_width_pct=0.34),
            ),
        ),
        PlateTemplate(
            code="08",
            suffix="PLATE_08_SINGLE_COASTAL_RIGHT_56PCT_16x9",
            description_vi="1 cây Goldilocks 56% bên phải: phòng khách rộng nhìn ra biển / vườn lớn",
            placements=(
                PlacementSpec(height_pct=0.56, center_x_pct=0.72, bottom_margin_pct=0.055, max_width_pct=0.36),
            ),
        ),
        PlateTemplate(
            code="09",
            suffix="PLATE_09_SINGLE_HERO_RIGHT_76PCT_16x9",
            description_vi="1 cây Hero cận nổi khối tiền cảnh bên phải (hồ bơi / daybed lùi sau 1.3m, 76%)",
            placements=(
                PlacementSpec(height_pct=0.76, center_x_pct=0.71, bottom_margin_pct=0.045, max_width_pct=0.44),
            ),
        ),
    ),
    single_cutout_lock_header=(
        "Edit this 16:9 product photograph (using the second 1024x1024 close-up reference image for exact foliage sprig and planter material detail): "
        "treat the potted plant and planter in the 16:9 plate as an untouched locked foreground photograph cutout — "
        "keep every single leaf sprig, outer branch contour, full foliage width, and full planter geometry 100% pixel-identical to the 16:9 plate "
        "without shrinking, narrowing, clumping, thickening, or redrawing any leaf or planter pixels. "
        "Outpaint ONLY the pure white background with "
    ),
    pair_cutout_lock_header=(
        "Edit this 16:9 product photograph (using the second 1024x1024 close-up reference image for exact foliage sprig and planter material detail): "
        "keep BOTH potted plants and their planters 100% pixel-identical to the 16:9 plate in exact position, height, planter proportions, "
        "outer silhouette contour, and leaf texture — DO NOT alter the planters, DO NOT widen or slim the silhouettes, and DO NOT redraw the leaves. "
        "Outpaint ONLY the pure white background with "
    ),
    white_isolation_prompt=(
        "Clean studio product isolation: keep ONLY this exact potted plant and its planter 100% identical in every leaf sprig, branch tip, silhouette, "
        "color, and planter detail. Remove all background scenery, floor, props, text, and watermarks, placing the untouched product centered on a "
        "pure solid #FFFFFF white background with crisp natural edges and zero shadow clipping, zero text."
    ),
    forbidden_image_substrings=(
        "cedar", "topiary", "slender", "teardrop", "chartreuse",
        "conifer", "spruce", "cypress", "juniper", "spiky needles",
    ),
    forbidden_image_regexes=(r"\bpine\b",),
)


CROCHET_COASTER_PRESET = CategoryPreset(
    name="crochet_coaster",
    label_vi="Đồ len móc Crochet mini đặt bàn / Đế lót ly hoa / Phụ kiện nhỏ (8cm – 15cm)",
    physical_size_note_vi="Đường kính / chiều cao 8cm–15cm đặt trên mặt bàn (tabletop): nâng đáy lên 14%–18% khung hình để lộ mặt bàn gỗ/đá tiền cảnh, dùng ống kính 85mm–100mm Macro f/2.8.",
    recommended_lens="85mm–100mm macro tabletop cinema lens, f/2.8 shallow depth of field (Kodak Vision3 250D)",
    scale_anchors_vi="Ly sứ gốm / tách trà (cao 9cm–9.5cm, miệng 8.5cm), tách espresso (6.5cm), hộp AirPods (5.5cm), thìa đồng nhỏ, cuốn sổ tay A5 trên mặt bàn gỗ ấm.",
    macro_focus_box=(0.14, 0.14, 0.86, 0.86),
    plates=(
        PlateTemplate(
            code="01",
            suffix="PLATE_01_SINGLE_TABLETOP_LEFT_44PCT_16x9",
            description_vi="1 sản phẩm Crochet Hero bên trái mặt bàn (44% cao, đáy nâng 15% lộ tiền cảnh bàn gỗ)",
            placements=(
                PlacementSpec(height_pct=0.44, center_x_pct=0.33, bottom_margin_pct=0.15, max_width_pct=0.38),
            ),
        ),
        PlateTemplate(
            code="02",
            suffix="PLATE_02_SINGLE_TABLETOP_RIGHT_44PCT_16x9",
            description_vi="1 sản phẩm Crochet Hero bên phải mặt bàn (44% cao, đáy nâng 15%)",
            placements=(
                PlacementSpec(height_pct=0.44, center_x_pct=0.67, bottom_margin_pct=0.15, max_width_pct=0.38),
            ),
        ),
        PlateTemplate(
            code="03",
            suffix="PLATE_03_SINGLE_MACRO_CENTER_52PCT_16x9",
            description_vi="1 sản phẩm Crochet cận Macro trung tâm (52% cao, khoe trọn từng mũi móc sợi cotton)",
            placements=(
                PlacementSpec(height_pct=0.52, center_x_pct=0.48, bottom_margin_pct=0.14, max_width_pct=0.44),
            ),
        ),
        PlateTemplate(
            code="04",
            suffix="PLATE_04_PAIR_TABLETOP_38PCT_16x9",
            description_vi="2 sản phẩm Crochet đặt cạnh nhau lệch chiều sâu nhẹ trên bàn trà (40% & 35%)",
            placements=(
                PlacementSpec(height_pct=0.40, center_x_pct=0.32, bottom_margin_pct=0.14, max_width_pct=0.33),
                PlacementSpec(height_pct=0.35, center_x_pct=0.69, bottom_margin_pct=0.20, max_width_pct=0.30),
            ),
        ),
        PlateTemplate(
            code="05",
            suffix="PLATE_05_SINGLE_WIDE_TEA_SETTING_32PCT_16x9",
            description_vi="1 sản phẩm Crochet trong bố cục khay trà / bàn cà phê sáng sớm rộng (32%)",
            placements=(
                PlacementSpec(height_pct=0.32, center_x_pct=0.64, bottom_margin_pct=0.16, max_width_pct=0.30),
            ),
        ),
    ),
    single_cutout_lock_header=(
        "Edit this 16:9 tabletop product photograph (using the second 1024x1024 macro close-up reference image for exact handcrafted milk-cotton crochet yarn stitches, "
        "interlocking crochet loop geometry, petal/edge stitch count, and yarn fiber twist): "
        "treat the handmade crochet item in the 16:9 plate as an untouched locked foreground photograph cutout — "
        "keep every single crochet stitch loop, scalloped yarn border, exact petal/motif count, yarn color, and outer contour 100% pixel-identical to the 16:9 plate "
        "without resizing, melting stitches, turning crochet loops into sweater knit ribs, or adding fuzzy stray wool hairs. "
        "Outpaint ONLY the pure white background with "
    ),
    pair_cutout_lock_header=(
        "Edit this 16:9 tabletop product photograph (using the second 1024x1024 macro close-up reference image for exact handcrafted milk-cotton crochet yarn stitches "
        "and interlocking loop detail): keep BOTH handmade crochet items 100% pixel-identical to the 16:9 plate in exact position, scale, stitch count, "
        "yarn loop texture, and outer contour without altering or blurring any yarn pixels. "
        "Outpaint ONLY the pure white background with "
    ),
    white_isolation_prompt=(
        "Clean studio tabletop product isolation: keep ONLY this exact handmade crochet product 100% identical in every single crochet yarn stitch, "
        "loop count, petal/border shape, yarn twist, and true color (preserving cream and off-white yarn tones without over-brightening). "
        "Remove the table surface, props, hands, shadows, text overlays, and watermarks, placing the untouched crochet item centered on a "
        "pure solid #FFFFFF white background, zero text."
    ),
    forbidden_image_substrings=(
        "woollen fuzz", "fuzzy wool", "oversized petals", "giant flower",
        "3d render", "cartoon", "plastic toy", "frayed yarn", "messy yarn",
    ),
    forbidden_image_regexes=(r"\bknitted\b", r"\bknitting\b", r"\bfelt\b", r"\bcgi\b"),
)


CROCHET_DECOR_PRESET = CategoryPreset(
    name="crochet_decor",
    label_vi="Chậu hoa len Crochet / Thú bông Amigurumi / Giỏ hoa len để bàn & kệ (15cm – 32cm)",
    physical_size_note_vi="Cao 15cm–32cm đặt trên bàn làm việc, bệ cửa sổ, kệ gỗ, bàn trà: cao gấp 1.8x–2.8x ly sứ 9.5cm hoặc ngang chồng sách bìa cứng.",
    recommended_lens="50mm–85mm lifestyle tabletop & interior close-medium lens (Kodak Vision3 250D)",
    scale_anchors_vi="Ly gốm cà phê (9.5cm), chồng sách nghệ thuật nằm ngang (8cm–12cm), khung ảnh để bàn (18cm), đèn bàn gốm, bệ cửa sổ gỗ sồi.",
    macro_focus_box=(0.15, 0.20, 0.85, 0.94),
    plates=(
        PlateTemplate(
            code="01",
            suffix="PLATE_01_SINGLE_HERO_LEFT_62PCT_16x9",
            description_vi="1 sản phẩm Crochet 3D Hero bên trái bàn gỗ / bệ cửa sổ (62% cao, đáy nâng 11%)",
            placements=(
                PlacementSpec(height_pct=0.62, center_x_pct=0.30, bottom_margin_pct=0.11, max_width_pct=0.40),
            ),
        ),
        PlateTemplate(
            code="02",
            suffix="PLATE_02_SINGLE_HERO_RIGHT_60PCT_16x9",
            description_vi="1 sản phẩm Crochet 3D Hero bên phải kệ sách / bàn trà (60% cao, đáy nâng 11%)",
            placements=(
                PlacementSpec(height_pct=0.60, center_x_pct=0.70, bottom_margin_pct=0.11, max_width_pct=0.40),
            ),
        ),
        PlateTemplate(
            code="03",
            suffix="PLATE_03_SINGLE_CLOSE_HERO_68PCT_16x9",
            description_vi="1 sản phẩm Crochet 3D cận rõ mũi móc & chậu/đế (68% cao, đáy nâng 10%)",
            placements=(
                PlacementSpec(height_pct=0.68, center_x_pct=0.33, bottom_margin_pct=0.10, max_width_pct=0.44),
            ),
        ),
        PlateTemplate(
            code="04",
            suffix="PLATE_04_PAIR_SHELF_52PCT_16x9",
            description_vi="2 sản phẩm Crochet 3D đặt đôi trên bàn console / kệ gỗ (52% cao, đáy nâng 12%)",
            placements=(
                PlacementSpec(height_pct=0.52, center_x_pct=0.30, bottom_margin_pct=0.12, max_width_pct=0.35),
                PlacementSpec(height_pct=0.52, center_x_pct=0.70, bottom_margin_pct=0.12, max_width_pct=0.35),
            ),
        ),
        PlateTemplate(
            code="05",
            suffix="PLATE_05_SINGLE_WIDE_DESK_45PCT_16x9",
            description_vi="1 sản phẩm Crochet 3D trung cảnh góc bàn làm việc / bàn ăn nắng sớm (45% cao)",
            placements=(
                PlacementSpec(height_pct=0.45, center_x_pct=0.69, bottom_margin_pct=0.13, max_width_pct=0.34),
            ),
        ),
    ),
    single_cutout_lock_header=CROCHET_COASTER_PRESET.single_cutout_lock_header,
    pair_cutout_lock_header=CROCHET_COASTER_PRESET.pair_cutout_lock_header,
    white_isolation_prompt=CROCHET_COASTER_PRESET.white_isolation_prompt,
    forbidden_image_substrings=CROCHET_COASTER_PRESET.forbidden_image_substrings,
    forbidden_image_regexes=CROCHET_COASTER_PRESET.forbidden_image_regexes,
)


CROCHET_BAG_PRESET = CategoryPreset(
    name="crochet_bag",
    label_vi="Túi xách len Crochet / Gối tựa len / Phụ kiện thời trang thủ công (30cm – 45cm)",
    physical_size_note_vi="Cao 30cm–45cm (gồm quai): đặt trên ghế gỗ/mây, băng ghế sofa linen, bàn cà phê sân vườn.",
    recommended_lens="50mm–85mm natural lifestyle lens (Kodak Vision3 250D)",
    scale_anchors_vi="Mặt ghế bành mây/gỗ Teak, đệm sofa linen, tách latte gốm đặt cạnh trên bàn, cuốn tạp chí khổ A4, mũ cói.",
    macro_focus_box=(0.16, 0.24, 0.84, 0.92),
    plates=(
        PlateTemplate(
            code="01",
            suffix="PLATE_01_SINGLE_HERO_LEFT_66PCT_16x9",
            description_vi="1 túi/gối Crochet Hero bên trái trên ghế/bàn (66% cao, đáy nâng 10%)",
            placements=(
                PlacementSpec(height_pct=0.66, center_x_pct=0.31, bottom_margin_pct=0.10, max_width_pct=0.42),
            ),
        ),
        PlateTemplate(
            code="02",
            suffix="PLATE_02_SINGLE_HERO_RIGHT_66PCT_16x9",
            description_vi="1 túi/gối Crochet Hero bên phải trên băng ghế gỗ / sofa (66% cao, đáy nâng 10%)",
            placements=(
                PlacementSpec(height_pct=0.66, center_x_pct=0.69, bottom_margin_pct=0.10, max_width_pct=0.42),
            ),
        ),
        PlateTemplate(
            code="03",
            suffix="PLATE_03_SINGLE_MEDIUM_52PCT_16x9",
            description_vi="1 túi/gối Crochet trung cảnh 50mm trong góc phòng/hiên nắng (52% cao, đáy nâng 11%)",
            placements=(
                PlacementSpec(height_pct=0.52, center_x_pct=0.68, bottom_margin_pct=0.11, max_width_pct=0.36),
            ),
        ),
    ),
    single_cutout_lock_header=CROCHET_COASTER_PRESET.single_cutout_lock_header,
    pair_cutout_lock_header=CROCHET_COASTER_PRESET.pair_cutout_lock_header,
    white_isolation_prompt=CROCHET_COASTER_PRESET.white_isolation_prompt,
    forbidden_image_substrings=CROCHET_COASTER_PRESET.forbidden_image_substrings,
    forbidden_image_regexes=CROCHET_COASTER_PRESET.forbidden_image_regexes,
)


GENERIC_DECOR_PRESET = CategoryPreset(
    name="generic_decor",
    label_vi="Sản phẩm Decor / Gia dụng / Thủ công tổng quát",
    physical_size_note_vi="Tùy chỉnh vật neo kiến trúc hoặc mặt bàn theo kích thước thật (cm) của sản phẩm.",
    recommended_lens="50mm natural cinema lens (Kodak Vision3 250D)",
    scale_anchors_vi="Luôn neo kích thước thật bằng 1–2 đồ vật quen thuộc có chiều cao cụ thể (cm/m) đặt cạnh sản phẩm.",
    macro_focus_box=(0.16, 0.20, 0.84, 0.92),
    plates=(
        PlateTemplate(
            code="01",
            suffix="PLATE_01_SINGLE_HERO_LEFT_64PCT_16x9",
            description_vi="1 sản phẩm Hero bên trái (64% cao, đáy nâng 10%)",
            placements=(
                PlacementSpec(height_pct=0.64, center_x_pct=0.31, bottom_margin_pct=0.10, max_width_pct=0.42),
            ),
        ),
        PlateTemplate(
            code="02",
            suffix="PLATE_02_SINGLE_HERO_RIGHT_64PCT_16x9",
            description_vi="1 sản phẩm Hero bên phải (64% cao, đáy nâng 10%)",
            placements=(
                PlacementSpec(height_pct=0.64, center_x_pct=0.69, bottom_margin_pct=0.10, max_width_pct=0.42),
            ),
        ),
        PlateTemplate(
            code="03",
            suffix="PLATE_03_PAIR_SYMMETRIC_54PCT_16x9",
            description_vi="2 sản phẩm đối xứng trái/phải (54% cao, đáy nâng 10%)",
            placements=(
                PlacementSpec(height_pct=0.54, center_x_pct=0.29, bottom_margin_pct=0.10, max_width_pct=0.36),
                PlacementSpec(height_pct=0.54, center_x_pct=0.71, bottom_margin_pct=0.10, max_width_pct=0.36),
            ),
        ),
        PlateTemplate(
            code="04",
            suffix="PLATE_04_SINGLE_WIDE_46PCT_16x9",
            description_vi="1 sản phẩm trung-đại cảnh (46% cao, đáy nâng 12%)",
            placements=(
                PlacementSpec(height_pct=0.46, center_x_pct=0.69, bottom_margin_pct=0.12, max_width_pct=0.34),
            ),
        ),
    ),
    single_cutout_lock_header=(
        "Edit this 16:9 product photograph (using the second 1024x1024 close-up reference image for exact surface texture and material detail): "
        "treat the product in the 16:9 plate as an untouched locked foreground photograph cutout — "
        "keep every detail, proportion, color, and outer contour 100% pixel-identical to the 16:9 plate without resizing or redrawing any product pixels. "
        "Outpaint ONLY the pure white background with "
    ),
    pair_cutout_lock_header=(
        "Edit this 16:9 product photograph (using the second 1024x1024 close-up reference image for exact surface texture and material detail): "
        "keep BOTH products 100% pixel-identical to the 16:9 plate in exact position, scale, color, and contour without redrawing any product pixels. "
        "Outpaint ONLY the pure white background with "
    ),
    white_isolation_prompt=(
        "Clean studio product isolation: keep ONLY this exact product 100% identical in every detail, texture, proportion, and true color. "
        "Remove all background clutter, props, text, and watermarks, placing the untouched product centered on a pure solid #FFFFFF white background, zero text."
    ),
    forbidden_image_substrings=(),
    forbidden_image_regexes=(),
)


PRESETS: Dict[str, CategoryPreset] = {
    p.name: p
    for p in (
        TREE_4FT_PRESET,
        CROCHET_COASTER_PRESET,
        CROCHET_DECOR_PRESET,
        CROCHET_BAG_PRESET,
        GENERIC_DECOR_PRESET,
    )
}


def get_preset(name: str) -> CategoryPreset:
    if name not in PRESETS:
        valid = ", ".join(sorted(PRESETS.keys()))
        raise KeyError(f"Unknown preset {name!r}. Valid presets: {valid}")
    return PRESETS[name]


def list_presets() -> List[CategoryPreset]:
    return list(PRESETS.values())
