"""
Pillow Plate & Macro Reference Engine (Zero-Distortion + Border-Flood White Cutout).

Converts 1 single product photo (white/studio background JPG/PNG or transparent PNG)
into:
- <PREFIX>_REF_1_SINGLE_CLEAN.jpg (1024x1024 pure #FFFFFF master ref)
- <PREFIX>_REF_2_CLOSEUP_1024.jpg (1024x1024 ~1.65x-1.85x macro detail ref, 0% distortion)
- <PREFIX>_PLATE_01..._16x9.jpg (2560x1440 2K 16:9 #FFFFFF plates calibrated by category preset)
- plate_manifest.json (lightweight metadata safe to commit to Git without bulky images)
"""

from collections import deque
import json
import os
import statistics
from typing import Any, Dict, Iterable, List, Optional, Tuple
from PIL import Image, ImageChops, ImageOps, ImageStat

from .presets import CategoryPreset, PlacementSpec, get_preset


def _extract_alpha_channel_if_transparent(img: Image.Image) -> Optional[Image.Image]:
    """Return an 'L' alpha mask ONLY if the image genuinely has transparent pixels (<250)."""
    has_transparency = (
        img.mode in ("RGBA", "LA")
        or (img.mode == "P" and "transparency" in img.info)
    )
    if not has_transparency:
        return None
    alpha = img.convert("RGBA").getchannel("A")
    extrema = alpha.getextrema()
    if extrema and extrema[0] < 250:
        return alpha
    return None


def composite_to_rgb_white(img: Image.Image) -> Tuple[Image.Image, bool]:
    """Convert any PIL image mode to RGB, compositing genuine alpha transparency onto pure #FFFFFF."""
    img = ImageOps.exif_transpose(img)
    alpha = _extract_alpha_channel_if_transparent(img)
    has_mode_alpha = (
        img.mode in ("RGBA", "LA")
        or (img.mode == "P" and "transparency" in img.info)
    )
    if has_mode_alpha:
        rgba = img.convert("RGBA")
        white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        composited = Image.alpha_composite(white_bg, rgba).convert("RGB")
        return composited, alpha is not None
    return img.convert("RGB"), False


def _maybe_isolate_first_twin_unit(
    cleaned_full: Image.Image,
    fg_mask: bytearray,
    tight_bbox: Tuple[int, int, int, int],
) -> Optional[Tuple[Tuple[int, int, int, int], int]]:
    """
    Detect 'Set of 2 / 3 / 4' side-by-side identical twin product listing photos on white background.
    Returns (first_unit_tight_bbox, pack_count) ONLY when:
      1. [x0..x1) splits cleanly into 2..4 horizontal foreground islands separated by near-empty
         vertical corridors (>= max(6px, 1.5% of total bbox width) where each column has at most
         <= max(2px, 1.5% of bbox height) sparse touching leaf tips or JPEG dust),
      2. Every island matches island 0 in width (±8%), height (±6%), and top/bottom alignment (±6%),
         and occupies substantial vertical fill (>20%) so hollow frames/rings never split,
      3. Every sibling island matches island 0 photometrically on a 24x36 RGB template (mean L1 <= 16/255,
         allowing direct or horizontal-mirror symmetry).
    Single products and multi-piece unequal sets (e.g. teapot + small cup) return None untouched.
    """
    w, _h = cleaned_full.size
    bx0, by0, bx1, by1 = tight_bbox
    total_w = bx1 - bx0
    total_h = by1 - by0
    if total_w < 64 or total_h < 32:
        return None

    col_fg_count = [0] * total_w
    for y in range(by0, by1):
        row_off = y * w
        for dx in range(total_w):
            if fg_mask[row_off + bx0 + dx]:
                col_fg_count[dx] += 1

    max_corridor_fg_px = max(2, round(total_h * 0.015))
    col_has_fg = [cnt > max_corridor_fg_px for cnt in col_fg_count]

    min_gap = max(6, round(total_w * 0.015))
    raw_runs: List[Tuple[int, int]] = []
    idx = 0
    while idx < total_w:
        if not col_has_fg[idx]:
            idx += 1
            continue
        start = idx
        while idx < total_w and col_has_fg[idx]:
            idx += 1
        raw_runs.append((bx0 + start, bx0 + idx))

    if len(raw_runs) < 2:
        return None

    # Merge tiny sub-threshold column gaps (e.g. thin airy leaf gaps) while keeping true full-corridor splits
    merged: List[Tuple[int, int]] = [raw_runs[0]]
    for rx0, rx1 in raw_runs[1:]:
        prev_x0, prev_x1 = merged[-1]
        if (rx0 - prev_x1) < min_gap:
            merged[-1] = (prev_x0, rx1)
        else:
            merged.append((rx0, rx1))

    if not (2 <= len(merged) <= 4):
        return None

    island_boxes: List[Tuple[int, int, int, int]] = []
    for i_idx, (ix0, ix1) in enumerate(merged):
        # Expand island bounds up to the minimum-density midpoint of adjacent corridors so untrimmed outer tips stay intact
        left_bound = bx0 if i_idx == 0 else (merged[i_idx - 1][1] + ix0) // 2
        right_bound = bx1 if i_idx == len(merged) - 1 else (ix1 + merged[i_idx + 1][0]) // 2
        if i_idx == 0 and len(merged) > 1:
            corr_start = ix1 - bx0
            corr_end = merged[1][0] - bx0
            if corr_end > corr_start:
                min_cnt = min(col_fg_count[corr_start:corr_end])
                # Pick rightmost zero/min column closest to midpoint so unit 0 keeps all its own outer leaf tips
                best_dx = min(
                    range(corr_start, corr_end),
                    key=lambda d: (col_fg_count[d], abs(d - (corr_start + corr_end) // 2)),
                )
                right_bound = bx0 + best_dx

        actual_x0 = right_bound
        actual_x1 = left_bound - 1
        iy0 = by1
        iy1 = by0 - 1
        fg_area = 0
        for y in range(by0, by1):
            row_off = y * w
            row_hit = False
            for x in range(left_bound, right_bound):
                if fg_mask[row_off + x]:
                    fg_area += 1
                    row_hit = True
                    if x < actual_x0:
                        actual_x0 = x
                    if x > actual_x1:
                        actual_x1 = x
            if row_hit:
                if y < iy0:
                    iy0 = y
                if y > iy1:
                    iy1 = y
        if iy1 < iy0 or actual_x1 < actual_x0:
            return None
        iw = (actual_x1 + 1) - actual_x0
        ih = (iy1 + 1) - iy0
        if iw < 24 or ih < 24:
            return None
        if fg_area / float(iw * ih) < 0.20:
            return None
        island_boxes.append((actual_x0, iy0, actual_x1 + 1, iy1 + 1))

    x0_0, y0_0, x1_0, y1_0 = island_boxes[0]
    w0 = x1_0 - x0_0
    h0 = y1_0 - y0_0
    thumb0 = cleaned_full.crop((x0_0, y0_0, x1_0, y1_0)).resize((24, 36), Image.Resampling.BILINEAR)

    for ix0, iy0, ix1, iy1 in island_boxes[1:]:
        iw = ix1 - ix0
        ih = iy1 - iy0
        if abs(iw - w0) / float(max(iw, w0)) > 0.08:
            return None
        if abs(ih - h0) / float(max(ih, h0)) > 0.06:
            return None
        if abs(iy0 - y0_0) / float(h0) > 0.06 or abs(iy1 - y1_0) / float(h0) > 0.06:
            return None

        thumb_i = cleaned_full.crop((ix0, iy0, ix1, iy1)).resize((24, 36), Image.Resampling.BILINEAR)
        l1_direct = sum(ImageStat.Stat(ImageChops.difference(thumb0, thumb_i)).mean) / 3.0
        l1_mirror = sum(ImageStat.Stat(ImageChops.difference(thumb0, ImageOps.mirror(thumb_i))).mean) / 3.0
        if min(l1_direct, l1_mirror) > 16.0:
            return None

    return island_boxes[0], len(island_boxes)


def extract_clean_white_cutout(
    img: Image.Image,
    bg_threshold: int = 240,
    max_chroma: int = 18,
    pad_px: int = 4,
    allow_nonwhite_bg: bool = False,
    bg_tolerance: int = 12,
    max_step: int = 5,
    alpha_threshold: int = 12,
    auto_split_twin_pair: bool = True,
) -> Tuple[Image.Image, Tuple[int, int, int, int], Dict[str, Any]]:
    """
    Extract a zero-seam #FFFFFF-backed product cutout while preserving white/ivory/cream details:
    1. If the input has genuine alpha transparency (e.g. PNG cutout of a pure-white crochet bunny/daisy),
       use the alpha mask directly (`alpha > alpha_threshold`) so opaque white/cream yarn touching the
       outer contour is NEVER eaten by RGB flood-fill.
    2. Otherwise, measure the median studio-white color along the 4 image borders and run a
       gradient-step-gated (`max_step`) + border-color-bounded (`bg_tolerance`) 4-border BFS flood-fill,
       normalizing outer studio grey (#F0F0F0..#FEFEFE) to pure #FFFFFF while stopping cleanly at
       ivory/cream/off-white crochet petal boundaries and preserving all enclosed white pixels.
    3. When `auto_split_twin_pair=True`, automatically isolates 1 single unit if the source image is a
       'Set of 2/3/4' side-by-side identical twin product listing photo separated by pure white background.
    """
    transposed = ImageOps.exif_transpose(img)
    alpha_mask = _extract_alpha_channel_if_transparent(transposed)
    rgb, had_alpha = composite_to_rgb_white(transposed)
    w, h = rgb.size
    if w < 16 or h < 16:
        raise ValueError(f"Input image is too small ({w}x{h}); expected at least 16x16.")

    raw = bytearray(rgb.tobytes())
    total_px = w * h
    fg_mask = bytearray(total_px)

    if had_alpha and alpha_mask is not None:
        a_bytes = alpha_mask.tobytes()
        min_x, min_y = w, h
        max_x, max_y = -1, -1
        bg_count = 0
        for idx in range(total_px):
            if a_bytes[idx] <= alpha_threshold:
                bg_count += 1
                off = idx * 3
                raw[off] = 255
                raw[off + 1] = 255
                raw[off + 2] = 255
            else:
                fg_mask[idx] = 1
                y, x = divmod(idx, w)
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y

        if max_x < 0:
            raise ValueError(
                "Input image is completely blank/white — no product foreground pixels detected."
            )
        flooded_ratio = bg_count / float(total_px)
    else:
        # Precompute candidate near-white mask (1 = candidate studio white, 0 = clearly colored/dark)
        cand = bytearray(total_px)
        for i in range(total_px):
            off = i * 3
            r = raw[off]
            g = raw[off + 1]
            b = raw[off + 2]
            mn = r if r < g else g
            if b < mn:
                mn = b
            if mn >= bg_threshold:
                mx = r if r > g else g
                if b > mx:
                    mx = b
                if (mx - mn) <= max_chroma:
                    cand[i] = 1

        border_indices = []
        for x in range(w):
            border_indices.append(x)
            border_indices.append((h - 1) * w + x)
        for y in range(1, h - 1):
            row = y * w
            border_indices.append(row)
            border_indices.append(row + w - 1)

        border_white_indices = [idx for idx in border_indices if cand[idx]]
        visited = bytearray(total_px)

        if border_white_indices:
            bg_r = int(statistics.median(raw[idx * 3] for idx in border_white_indices))
            bg_g = int(statistics.median(raw[idx * 3 + 1] for idx in border_white_indices))
            bg_b = int(statistics.median(raw[idx * 3 + 2] for idx in border_white_indices))

            def within_bg_tol(idx: int) -> bool:
                off = idx * 3
                return (
                    abs(raw[off] - bg_r) <= bg_tolerance
                    and abs(raw[off + 1] - bg_g) <= bg_tolerance
                    and abs(raw[off + 2] - bg_b) <= bg_tolerance
                )

            def step_ok(cur_idx: int, nb_idx: int) -> bool:
                o1 = cur_idx * 3
                o2 = nb_idx * 3
                return (
                    abs(raw[o1] - raw[o2]) <= max_step
                    and abs(raw[o1 + 1] - raw[o2 + 1]) <= max_step
                    and abs(raw[o1 + 2] - raw[o2 + 2]) <= max_step
                )

            q: deque[int] = deque()
            for idx in border_white_indices:
                if not visited[idx] and within_bg_tol(idx):
                    visited[idx] = 1
                    q.append(idx)

            while q:
                cur = q.popleft()
                x = cur % w
                if x > 0:
                    nb = cur - 1
                    if cand[nb] and not visited[nb] and within_bg_tol(nb) and step_ok(cur, nb):
                        visited[nb] = 1
                        q.append(nb)
                if x + 1 < w:
                    nb = cur + 1
                    if cand[nb] and not visited[nb] and within_bg_tol(nb) and step_ok(cur, nb):
                        visited[nb] = 1
                        q.append(nb)
                nb_up = cur - w
                if nb_up >= 0 and cand[nb_up] and not visited[nb_up] and within_bg_tol(nb_up) and step_ok(cur, nb_up):
                    visited[nb_up] = 1
                    q.append(nb_up)
                nb_dn = cur + w
                if nb_dn < total_px and cand[nb_dn] and not visited[nb_dn] and within_bg_tol(nb_dn) and step_ok(cur, nb_dn):
                    visited[nb_dn] = 1
                    q.append(nb_dn)

        flooded_count = sum(visited)
        if flooded_count >= total_px:
            raise ValueError(
                "Input image is completely blank/white — no product foreground pixels detected."
            )

        flooded_ratio = flooded_count / float(total_px)
        if flooded_ratio < 0.02 and not allow_nonwhite_bg:
            raise ValueError(
                f"Ảnh đầu vào chưa có nền trắng (#FFFFFF) hoặc nền PNG trong suốt "
                f"(chỉ {flooded_ratio * 100:.2f}% viền ngoài là nền trắng).\n"
                f"👉 Cách xử lý chuẩn: Chạy 'python3 -m flow_sku_tvc_toolkit isolate-white ...' "
                f"để tách sản phẩm sang nền trắng tinh #FFFFFF (hoặc truyền ảnh PNG đã tách nền) trước khi dựng Plate 2K."
            )

        min_x, min_y = w, h
        max_x, max_y = -1, -1
        for idx in range(total_px):
            if visited[idx]:
                off = idx * 3
                raw[off] = 255
                raw[off + 1] = 255
                raw[off + 2] = 255
            else:
                fg_mask[idx] = 1
                y, x = divmod(idx, w)
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y

    cleaned_full = Image.frombytes("RGB", (w, h), bytes(raw))
    tight_x0, tight_y0, tight_x1, tight_y1 = min_x, min_y, max_x + 1, max_y + 1
    twin_pack_count = 1

    if auto_split_twin_pair:
        twin_res = _maybe_isolate_first_twin_unit(
            cleaned_full,
            fg_mask,
            (tight_x0, tight_y0, tight_x1, tight_y1),
        )
        if twin_res is not None:
            (tight_x0, tight_y0, tight_x1, tight_y1), twin_pack_count = twin_res
            # Whiten everything outside the isolated single unit so padded margins stay 100% pure #FFFFFF
            isolated_canvas = Image.new("RGB", (w, h), (255, 255, 255))
            unit_patch = cleaned_full.crop((tight_x0, tight_y0, tight_x1, tight_y1))
            isolated_canvas.paste(unit_patch, (tight_x0, tight_y0))
            cleaned_full = isolated_canvas

    x0 = max(0, tight_x0 - pad_px)
    y0 = max(0, tight_y0 - pad_px)
    x1 = min(w, tight_x1 + pad_px)
    y1 = min(h, tight_y1 + pad_px)
    crop = cleaned_full.crop((x0, y0, x1, y1))

    stats = {
        "source_size": [w, h],
        "had_alpha": had_alpha,
        "flooded_bg_ratio": round(flooded_ratio, 4),
        "auto_split_twin_pack_count": twin_pack_count,
        "tight_bbox": [tight_x0, tight_y0, tight_x1, tight_y1],
        "padded_bbox": [x0, y0, x1, y1],
        "cutout_size": [crop.width, crop.height],
        "aspect_ratio_w_over_h": round(crop.width / float(crop.height), 6),
    }
    return crop, (x0, y0, x1, y1), stats


def _resize_preserve_aspect(
    crop: Image.Image,
    max_w: int,
    max_h: int,
) -> Image.Image:
    """Resize crop using LANCZOS to fit inside (max_w, max_h) with 0.0% aspect distortion."""
    cw, ch = crop.size
    scale = min(max_w / float(cw), max_h / float(ch))
    target_w = max(1, round(cw * scale))
    target_h = max(1, round(ch * scale))
    return crop.resize((target_w, target_h), Image.Resampling.LANCZOS)


def build_ref_1_clean_square(
    cutout_crop: Image.Image,
    canvas_size: int = 1024,
    max_fill: float = 0.86,
) -> Image.Image:
    """Place the clean cutout centered on a 1024x1024 #FFFFFF canvas with 0% distortion."""
    canvas = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    limit = max(16, round(canvas_size * max_fill))
    fitted = _resize_preserve_aspect(cutout_crop, limit, limit)
    px = (canvas_size - fitted.width) // 2
    py = (canvas_size - fitted.height) // 2
    canvas.paste(fitted, (px, py))
    return canvas


def build_ref_2_macro_square(
    cutout_crop: Image.Image,
    focus_box: Tuple[float, float, float, float] = (0.16, 0.28, 0.84, 0.98),
    canvas_size: int = 1024,
    max_fill: float = 0.94,
) -> Image.Image:
    """
    Build the 1024x1024 close-up macro reference (1.6x–1.9x zoom on foliage/yarn stitches + planter/base)
    preserving 100% true pixel aspect ratio (never stretching non-square crops).
    """
    cw, ch = cutout_crop.size
    fx0, fy0, fx1, fy1 = focus_box
    rx0 = max(0, min(cw - 1, round(cw * fx0)))
    ry0 = max(0, min(ch - 1, round(ch * fy0)))
    rx1 = max(rx0 + 1, min(cw, round(cw * fx1)))
    ry1 = max(ry0 + 1, min(ch, round(ch * fy1)))

    sub = cutout_crop.crop((rx0, ry0, rx1, ry1))
    canvas = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    limit = max(16, round(canvas_size * max_fill))
    fitted = _resize_preserve_aspect(sub, limit, limit)
    px = (canvas_size - fitted.width) // 2
    py = (canvas_size - fitted.height) // 2
    canvas.paste(fitted, (px, py))
    return canvas


def render_plate_2k(
    cutout_crop: Image.Image,
    placements: Iterable[PlacementSpec],
    canvas_w: int = 2560,
    canvas_h: int = 1440,
) -> Image.Image:
    """
    Render one 2560x1440 (2K 16:9) pure #FFFFFF plate placing 1 or more locked product
    cutouts at exact physical % heights & coordinates with 0.0% aspect distortion.
    """
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    cw, ch = cutout_crop.size

    for spec in placements:
        target_h = max(1, round(canvas_h * spec.height_pct))
        target_w = max(1, round(cw * (target_h / float(ch))))
        max_w_px = max(1, round(canvas_w * spec.max_width_pct))
        if target_w > max_w_px:
            target_w = max_w_px
            target_h = max(1, round(ch * (target_w / float(cw))))

        resized = cutout_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        paste_x = round(canvas_w * spec.center_x_pct - target_w / 2.0)
        paste_y = round(canvas_h * (1.0 - spec.bottom_margin_pct) - target_h)

        paste_x = max(0, min(canvas_w - target_w, paste_x))
        paste_y = max(0, min(canvas_h - target_h, paste_y))
        canvas.paste(resized, (paste_x, paste_y))

    return canvas


def build_sku_plates_from_image(
    input_path: str,
    out_dir: str,
    prefix: str,
    preset_name: str = "tree_4ft",
    bg_threshold: int = 240,
    max_chroma: int = 18,
    allow_nonwhite_bg: bool = False,
    auto_split_twin_pair: bool = True,
    jpeg_quality: int = 95,
) -> Dict[str, Any]:
    """
    End-to-end local asset builder from 1 source image:
      out_dir/clean_refs/<PREFIX>_REF_1_SINGLE_CLEAN.jpg
      out_dir/clean_refs/<PREFIX>_REF_2_CLOSEUP_1024.jpg
      out_dir/plates_2k/<PREFIX>_<PLATE_SUFFIX>.jpg
      out_dir/plate_manifest.json
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input SKU image not found: {input_path}")

    clean_prefix = prefix.strip().upper().rstrip("_")
    if not clean_prefix:
        raise ValueError("prefix must be a non-empty identifier (e.g. 'CROCHET_TULIP').")

    preset: CategoryPreset = get_preset(preset_name)
    refs_dir = os.path.join(out_dir, "clean_refs")
    plates_dir = os.path.join(out_dir, "plates_2k")
    os.makedirs(refs_dir, exist_ok=True)
    os.makedirs(plates_dir, exist_ok=True)

    with Image.open(input_path) as src_im:
        cutout_crop, bbox, stats = extract_clean_white_cutout(
            src_im,
            bg_threshold=bg_threshold,
            max_chroma=max_chroma,
            allow_nonwhite_bg=allow_nonwhite_bg,
            auto_split_twin_pair=auto_split_twin_pair,
        )

    ref1_name = f"{clean_prefix}_REF_1_SINGLE_CLEAN.jpg"
    ref2_name = f"{clean_prefix}_REF_2_CLOSEUP_1024.jpg"
    ref1_path = os.path.join(refs_dir, ref1_name)
    ref2_path = os.path.join(refs_dir, ref2_name)

    ref1_im = build_ref_1_clean_square(cutout_crop, canvas_size=1024)
    ref2_im = build_ref_2_macro_square(cutout_crop, focus_box=preset.macro_focus_box, canvas_size=1024)
    ref1_im.save(ref1_path, format="JPEG", quality=jpeg_quality, subsampling=0)
    ref2_im.save(ref2_path, format="JPEG", quality=jpeg_quality, subsampling=0)

    generated_plates = []
    for pt in preset.plates:
        fname = f"{clean_prefix}_{pt.suffix}.jpg"
        fpath = os.path.join(plates_dir, fname)
        plate_im = render_plate_2k(cutout_crop, pt.placements, canvas_w=2560, canvas_h=1440)
        plate_im.save(fpath, format="JPEG", quality=jpeg_quality, subsampling=0)
        generated_plates.append(
            {
                "code": pt.code,
                "filename": fname,
                "description_vi": pt.description_vi,
                "count": len(pt.placements),
                "heights_pct": [p.height_pct for p in pt.placements],
            }
        )

    manifest = {
        "prefix": clean_prefix,
        "preset": preset.name,
        "preset_label_vi": preset.label_vi,
        "source_image": os.path.basename(input_path),
        "cutout_stats": stats,
        "clean_refs": [ref1_name, ref2_name],
        "plates_2k": generated_plates,
    }
    manifest_path = os.path.join(out_dir, "plate_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return manifest
