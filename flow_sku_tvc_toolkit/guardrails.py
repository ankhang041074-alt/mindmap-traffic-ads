"""
Compile-time & pre-flight prompt guardrails for Nano Banana Pro (16:9 Images)
and Veo 3.1 - Fast (4s 3D-Parallax / 2-Frame Videos).
"""

import os
import re
from typing import Any, Dict, List, Sequence

from .presets import get_preset

FORBIDDEN_VIDEO_EQUIPMENT_SUBSTRINGS = (
    "slider",
    "gimbal",
    "dolly",
    "tripod",
    "steadicam",
    "crane",
)

FORBIDDEN_VIDEO_EQUIPMENT_REGEXES = (
    r"\brig\b",
)

FORBIDDEN_VIDEO_FREEZE_SUBSTRINGS = (
    "100% still",
    "stay still",
    "remain still",
    "motionless",
    "hold steady",
    "5%",
    "6%",
    "frozen",
    "no zoom-in",
    "constant viewing distance",
    "~10 percent",
    "10 percent closer",
)

FORBIDDEN_VIDEO_FREEZE_REGEXES = (
    r"\bstatic\b",
)

# Prevents Veo 3.1 - Fast from spawning fake self-luminous golden sand/glitter overlays in dark shadow zones.
# Note: 'shimmer' / 'sparkling water' remain allowed for natural lake/pool water ripples.
FORBIDDEN_VIDEO_PARTICLE_SUBSTRINGS = (
    "dust mote",
    "dust motes",
    "golden dust",
    "floating dust",
    "bokeh particles",
    "golden particles",
)

FORBIDDEN_VIDEO_PARTICLE_REGEXES = (
    r"\bglitter(?:ing|y)?\b",
    r"\bsparkles?\b",
)

# Prevents Veo 3.1 - Fast from locking the camera still and driving foreground furniture/props across the floor
# like a conveyor belt (e.g. 'foreground oak bench sweeps leftward', 'velvet chair glides outward').
FORBIDDEN_VIDEO_PROP_MOTION_REGEXES = (
    r"\b(?:chair|bench|ottoman|sofa|table|handrail|balustrade|napkin|book|holder|sprig|carafe|pitcher|vanity|plinth|tray|ledge|rim|armrest|backrest)\b[^.;]{0,65}\b(?:sweeps|glides|slides|moves)\b",
)

# Prevents Veo 3.1 - Fast from opening/swinging/pivoting/sliding background doors, gates, casements, or glass panels
# by themselves ('poltergeist doors'), which ruins product TVC realism.
FORBIDDEN_VIDEO_DOOR_MOTION_REGEXES = (
    r"(?<!\bno\s)(?<!\bzero\s)(?<!\bwithout\s)\b(?:door|doors|gate|gates|casement|casements|shoji)\b[^.;]{0,65}\b(?:swings?|pivots?|opens?|slides?|glides?)\b",
    r"\b(?:doors?|gates?|casements?)\s+(?:swing|swings|swinging|pivot|pivots|pivoting|open|opens|opening|slide|slides|sliding)\b",
)

# Prevents Veo 3.1 - Fast from tilting/panning upward during a forward push-in, which chops off the bottom
# of the planters near the lower frame edge (unless explicitly negated with 'no' / 'without' / 'zero').
FORBIDDEN_VIDEO_UPWARD_TILT_REGEXES = (
    r"(?<!\bno\s)(?<!\bzero\s)(?<!\bwithout\s)(?<!\bnot\s)(?<!\bor\s)\b(?:tilts?\s+up(?:ward)?|tilting\s+up(?:ward)?|pans?\s+up(?:ward)?|panning\s+up(?:ward)?)\b",
)

# Prevents pairing the staggered diagonal 2-tree plate (PLATE_03_PAIR_DIAGONAL_3Q: left y=8%, right y=21.5%)
# with frontal architectural portals/archways/gates/consoles/mantels. Nano Banana Pro renders portals/archways
# in 1-point frontal symmetry (horizontal wall seam at y~22%), which leaves the near-left pot stranded 2m out
# in the middle of the courtyard while only the right pot sits against the pillar.
FORBIDDEN_DIAGONAL_PLATE_FRONTAL_REGEXES = (
    r"\b(?:archway|portal|gate|gates|portico|mantel|fireplace|console|alcove|bookcase)\b",
)

# Prevents single-tree plates from placing a deep receding hallway/corridor vanishing point behind the cutout
# (unless negated with 'no' / 'zero' / 'without'), which visually dwarfs the architecture and makes a 4ft plant look 7ft tall.
FORBIDDEN_SINGLE_TREE_HALLWAY_REGEXES = (
    r"(?<!\bno\s)(?<!\bzero\s)(?<!\bwithout\s)\b(?:receding\s+(?:side\s+)?(?:hallway|corridor)|deep\s+(?:hallway|corridor))\b",
)


def evaluate_cutout_silhouette_fidelity(
    plate_img: Any,
    scene_img: Any,
    max_cutout_l1: float = 58.0,
    max_halo_fattening_pct: float = 9.0,
) -> Dict[str, Any]:
    """
    Quantitative Stage-2 Image QA Gate comparing a generated 16:9 scene image against its 2K white plate:
      1. Extracts the exact product cutout mask (non-white pixels on the 2K plate).
      2. Measures mean RGB L1 difference inside the cutout mask (`cutout_rgb_l1`) to verify the product
         remained at its exact 2D canvas coordinates and was not shifted, shrunk, or replaced.
      3. Measures `halo_fattening_pct` inside a 4px..36px outer ring around the upper 82% of the product
         silhouette to catch Nano Banana Pro puffing out / widening / fattening the foliage beyond the plate.
    """
    from PIL import Image, ImageFilter

    p_rgb = plate_img.convert("RGB")
    s_rgb = scene_img.convert("RGB").resize(p_rgb.size, Image.Resampling.LANCZOS)
    w, h = p_rgb.size
    p_px = p_rgb.load()
    s_px = s_rgb.load()

    mask = Image.new("L", (w, h), 0)
    m_px = mask.load()
    min_y, max_y = h, 0
    for y in range(h):
        for x in range(w):
            r, g, b = p_px[x, y]
            if r < 242 or g < 242 or b < 242:
                m_px[x, y] = 255
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y

    if max_y <= min_y:
        return {
            "ok": False,
            "verdict": "EMPTY_PLATE_MASK",
            "cutout_rgb_l1": 999.0,
            "halo_fattening_pct": 100.0,
            "reason": "Plate image contains no non-white product cutout pixels.",
        }

    dil_inner = mask.filter(ImageFilter.MaxFilter(9))
    dil_outer = dil_inner.filter(ImageFilter.MaxFilter(29))
    di_px = dil_inner.load()
    do_px = dil_outer.load()

    foliage_cutoff_y = int(min_y + 0.82 * (max_y - min_y))
    inside_diff_sum = 0.0
    inside_count = 0
    halo_green_count = 0
    halo_total_count = 0

    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if m_px[x, y] > 0:
                pr, pg, pb = p_px[x, y]
                sr, sg, sb = s_px[x, y]
                inside_diff_sum += (abs(pr - sr) + abs(pg - sg) + abs(pb - sb)) / 3.0
                inside_count += 1
            elif do_px[x, y] > 0 and di_px[x, y] == 0 and y < foliage_cutoff_y:
                sr, sg, sb = s_px[x, y]
                halo_total_count += 1
                if sg > sr + 12 and sg > sb + 10 and 25 < sg < 190:
                    halo_green_count += 1

    cutout_l1 = round(inside_diff_sum / max(1, inside_count), 2)
    fattening_pct = round(100.0 * halo_green_count / max(1, halo_total_count), 2)

    if cutout_l1 > max_cutout_l1:
        return {
            "ok": False,
            "verdict": "CUTOUT_SHIFTED_OR_ALTERED",
            "cutout_rgb_l1": cutout_l1,
            "halo_fattening_pct": fattening_pct,
            "reason": (
                f"Core cutout RGB L1 drift {cutout_l1:.2f} exceeds {max_cutout_l1:.1f} "
                f"(product shifted, resized, or redrawn away from 2D plate coordinates)."
            ),
        }

    if fattening_pct > max_halo_fattening_pct:
        return {
            "ok": False,
            "verdict": "SILHOUETTE_FATTENED",
            "cutout_rgb_l1": cutout_l1,
            "halo_fattening_pct": fattening_pct,
            "reason": (
                f"Outer silhouette halo foliage spill {fattening_pct:.2f}% exceeds {max_halo_fattening_pct:.1f}% "
                f"(AI puffed out / widened the plant beyond the locked plate contour)."
            ),
        }

    return {
        "ok": True,
        "verdict": "OK",
        "cutout_rgb_l1": cutout_l1,
        "halo_fattening_pct": fattening_pct,
        "reason": f"Cutout locked (cutout_rgb_l1={cutout_l1:.2f}, halo_fattening_pct={fattening_pct:.2f}%).",
    }


def classify_two_zone_video_motion(
    bg_seg_l1: Sequence[float],
    fg_seg_l1: Sequence[float],
    bg_e2e_l1: float,
    fg_e2e_l1: float,
    wall_e2e_l1: float = -1.0,
    center_e2e_l1: float = -1.0,
) -> Dict[str, Any]:
    """
    Evaluate multi-zone in-browser HTML5 <video> scrub metrics (no .mp4 download needed):
      - Top 65% zone (bg_*): measures 3D camera ego-motion against background walls/architecture.
      - Bottom 35% zone (fg_*): measures lower floor/tabletop & foreground planter displacement.
      - Optional wall_e2e_l1 vs center_e2e_l1: compares outer architectural wall strips against the
        center doorway/hearth zone to catch self-opening doors ('poltergeist doors') or sliding trees.

    Catches four distinct Veo failure modes:
      1. FROZEN_VIDEO: Camera and architecture barely move (still JPEG clip or only water ripples).
      2. CONVEYOR_PROP_OR_SLIDING_TREES: Background walls/hearth barely move while foreground pots or props
         slide across the floor toward/away from each other.
      3. POLTERGEIST_DOOR_CAMERA_STATIC: Outer architectural walls stay static while a center door swings open.
    """
    bg_mean = sum(bg_seg_l1) / float(len(bg_seg_l1)) if bg_seg_l1 else 0.0
    fg_mean = sum(fg_seg_l1) / float(len(fg_seg_l1)) if fg_seg_l1 else 0.0
    fg_to_bg_e2e_ratio = fg_e2e_l1 / max(bg_e2e_l1, 0.5)
    fg_to_bg_seg_ratio = fg_mean / max(bg_mean, 0.5)

    if (bg_e2e_l1 < 5.0 and fg_e2e_l1 < 6.5 and bg_mean < 3.0) or (
        bg_e2e_l1 < 11.5 and fg_e2e_l1 < 12.5 and bg_mean < 6.0
    ):
        return {
            "verdict": "FROZEN_VIDEO",
            "ok": False,
            "reason": (
                f"Camera and architecture are nearly static (bg_e2e_l1={bg_e2e_l1:.2f}, "
                f"fg_e2e_l1={fg_e2e_l1:.2f}, bg_seg_mean={bg_mean:.2f})."
            ),
            "fg_to_bg_e2e_ratio": round(fg_to_bg_e2e_ratio, 2),
        }

    if (
        (bg_e2e_l1 < 8.5 and fg_e2e_l1 >= 12.0 and fg_to_bg_e2e_ratio >= 2.3)
        or (bg_mean < 4.5 and fg_mean >= 10.0 and fg_to_bg_seg_ratio >= 2.5)
        or (fg_e2e_l1 >= 35.0 and fg_to_bg_e2e_ratio >= 1.85)
    ):
        return {
            "verdict": "CONVEYOR_PROP_CAMERA_FROZEN",
            "ok": False,
            "reason": (
                f"Background architecture is too static relative to foreground displacement — "
                f"trees or foreground props are sliding across the floor "
                f"(bg_e2e_l1={bg_e2e_l1:.2f} vs fg_e2e_l1={fg_e2e_l1:.2f}, ratio={fg_to_bg_e2e_ratio:.2f}x)."
            ),
            "fg_to_bg_e2e_ratio": round(fg_to_bg_e2e_ratio, 2),
        }

    if wall_e2e_l1 >= 0.0 and center_e2e_l1 >= 0.0:
        center_to_wall_ratio = center_e2e_l1 / max(wall_e2e_l1, 0.5)
        if wall_e2e_l1 < 11.0 and center_e2e_l1 >= 22.0 and center_to_wall_ratio >= 2.1:
            return {
                "verdict": "POLTERGEIST_DOOR_CAMERA_STATIC",
                "ok": False,
                "reason": (
                    f"Outer architectural walls are static (wall_e2e_l1={wall_e2e_l1:.2f}) while center "
                    f"doorway/panel moves by itself (center_e2e_l1={center_e2e_l1:.2f}, ratio={center_to_wall_ratio:.2f}x)."
                ),
                "fg_to_bg_e2e_ratio": round(fg_to_bg_e2e_ratio, 2),
            }

    return {
        "verdict": "OK",
        "ok": True,
        "reason": (
            f"True 3D camera motion verified across background architecture "
            f"(bg_e2e_l1={bg_e2e_l1:.2f}, fg_e2e_l1={fg_e2e_l1:.2f})."
        ),
        "fg_to_bg_e2e_ratio": round(fg_to_bg_e2e_ratio, 2),
    }


def validate_image_prompt(prompt: str, preset_name: str = "tree_4ft", scene_key: str = "") -> List[str]:
    """Return a list of violation descriptions (empty list if clean)."""
    errors: List[str] = []
    if not prompt or not prompt.strip():
        return [f"[{scene_key or 'image'}] Image prompt is empty."]

    preset = get_preset(preset_name)
    low = prompt.lower()
    tag = f"[{scene_key}] " if scene_key else ""

    for sub in preset.forbidden_image_substrings:
        if sub in low:
            errors.append(
                f"{tag}Forbidden category term {sub!r} found in image prompt (causes SKU shape/material drift)."
            )
    for rx in preset.forbidden_image_regexes:
        if re.search(rx, low):
            errors.append(
                f"{tag}Forbidden category pattern {rx!r} matched in image prompt (causes SKU shape/material drift)."
            )
    return errors


def validate_video_prompt(prompt: str, preset_name: str = "tree_4ft", video_key: str = "") -> List[str]:
    """Return a list of violation descriptions for Veo 3.1 4s video prompts."""
    errors: List[str] = []
    if not prompt or not prompt.strip():
        return [f"[{video_key or 'video'}] Video prompt is empty."]

    preset = get_preset(preset_name)
    low = prompt.lower()
    tag = f"[{video_key}] " if video_key else ""

    for sub in FORBIDDEN_VIDEO_EQUIPMENT_SUBSTRINGS:
        if sub in low:
            errors.append(
                f"{tag}Forbidden camera-gear word {sub!r} in Veo prompt (causes Veo 3.1 to render black metal rails/rigs in frame)."
            )
    for rx in FORBIDDEN_VIDEO_EQUIPMENT_REGEXES:
        if re.search(rx, low):
            errors.append(
                f"{tag}Forbidden camera-gear pattern {rx!r} in Veo prompt (causes Veo 3.1 to render camera hardware in frame)."
            )

    for sub in FORBIDDEN_VIDEO_FREEZE_SUBSTRINGS:
        if sub in low:
            errors.append(
                f"{tag}Forbidden freeze word {sub!r} in Veo prompt (causes Veo 3.1 to freeze the entire 4s clip like a still JPEG)."
            )
    for rx in FORBIDDEN_VIDEO_FREEZE_REGEXES:
        if re.search(rx, low):
            errors.append(
                f"{tag}Forbidden freeze pattern {rx!r} in Veo prompt (causes Veo 3.1 to freeze camera motion)."
            )

    for sub in FORBIDDEN_VIDEO_PARTICLE_SUBSTRINGS:
        if sub in low:
            errors.append(
                f"{tag}Forbidden fake-particle phrase {sub!r} in Veo prompt "
                f"(causes Veo 3.1 to spawn fake golden sand/glitter overlays even in dark shadow zones)."
            )
    for rx in FORBIDDEN_VIDEO_PARTICLE_REGEXES:
        if re.search(rx, low):
            errors.append(
                f"{tag}Forbidden fake-particle pattern {rx!r} in Veo prompt "
                f"(causes Veo 3.1 to spawn artificial glitter/sparkle overlays)."
            )

    for rx in FORBIDDEN_VIDEO_PROP_MOTION_REGEXES:
        m = re.search(rx, low)
        if m:
            errors.append(
                f"{tag}Forbidden foreground-prop motion clause {m.group(0)!r} in Veo prompt "
                f"(assigning sweeps/glides/slides to furniture/props makes Veo freeze the camera and drive the prop across the floor; "
                f"describe ONLY 3D camera motion and state that all furniture/props remain stationary anchored in place)."
            )

    for rx in FORBIDDEN_VIDEO_DOOR_MOTION_REGEXES:
        m = re.search(rx, low)
        if m:
            errors.append(
                f"{tag}Forbidden self-opening/sliding door clause {m.group(0)!r} in Veo prompt "
                f"(causes spooky poltergeist door opening/sliding in product TVC; all doors, gates, casements, and sliding panels "
                f"must remain 100% locked motionless in their initial state)."
            )

    for rx in FORBIDDEN_VIDEO_UPWARD_TILT_REGEXES:
        m = re.search(rx, low)
        if m:
            errors.append(
                f"{tag}Forbidden upward camera tilt/pan clause {m.group(0)!r} in Veo prompt "
                f"(tilting upward during a forward push-in chops off the bottom of the planters near the lower frame border; "
                f"maintain a level or slightly downward-angled horizon)."
            )

    for sub in preset.forbidden_image_substrings:
        if sub in low:
            errors.append(
                f"{tag}Forbidden SKU drift term {sub!r} in Veo prompt."
            )
    for rx in preset.forbidden_image_regexes:
        if re.search(rx, low):
            errors.append(
                f"{tag}Forbidden SKU drift pattern {rx!r} in Veo prompt."
            )
    return errors


def validate_sku_config(
    config: Dict[str, Any],
    project_dir: str = "",
    require_local_plates: bool = False,
) -> List[str]:
    """Validate an entire SKU JSON configuration (scenes, refs, videos, guardrails)."""
    errors: List[str] = []
    for req_field in ("slug", "prefix", "preset", "project_id"):
        if not config.get(req_field):
            errors.append(f"Missing required top-level field {req_field!r} in SKU config.")

    preset_name = config.get("preset", "generic_decor")
    try:
        get_preset(preset_name)
    except KeyError as exc:
        errors.append(str(exc))
        return errors

    scenes = config.get("scenes", [])
    videos = config.get("videos", [])
    scene_keys = set()

    for idx, sc in enumerate(scenes):
        skey = sc.get("key") or f"scene_{idx}"
        if skey in scene_keys:
            errors.append(f"Duplicate scene key {skey!r}.")
        scene_keys.add(skey)

        refs = sc.get("refs") or []
        if len(refs) < 2:
            errors.append(
                f"[{skey}] Dual-Lock requires at least 2 ingredient refs ([2K_16x9_Plate, 1024_Macro_Ref]), got {refs!r}."
            )

        if require_local_plates and project_dir:
            for rf in refs:
                p1 = os.path.join(project_dir, "plates_2k", rf)
                p2 = os.path.join(project_dir, "clean_refs", rf)
                if not (os.path.isfile(p1) or os.path.isfile(p2)):
                    errors.append(f"[{skey}] Missing local ingredient file {rf!r} in plates_2k/ or clean_refs/.")

        scene_prompt = sc.get("prompt", "")
        if any("PLATE_03_PAIR_DIAGONAL_3Q" in rf.upper() for rf in refs):
            low_sp = scene_prompt.lower()
            for rx in FORBIDDEN_DIAGONAL_PLATE_FRONTAL_REGEXES:
                m = re.search(rx, low_sp)
                if m:
                    errors.append(
                        f"[{skey}] Diagonal staggered plate ('PLATE_03_PAIR_DIAGONAL_3Q') cannot be paired with "
                        f"frontal portal/archway/gate/console term {m.group(0)!r} in image prompt "
                        f"(Nano Banana Pro renders portals/archways with a horizontal 1-point-perspective wall seam, "
                        f"stranding the near-left tree 2m out in the courtyard; use symmetric PLATE_01 or PLATE_02 instead)."
                    )

        if any("SINGLE_" in rf.upper() for rf in refs):
            low_sp = scene_prompt.lower()
            for rx in FORBIDDEN_SINGLE_TREE_HALLWAY_REGEXES:
                m = re.search(rx, low_sp)
                if m:
                    errors.append(
                        f"[{skey}] Single-tree plate cannot be paired with un-negated receding hallway/corridor term "
                        f"{m.group(0)!r} in image prompt (draws a deep vanishing point behind the cutout that makes "
                        f"a 4ft plant look 7ft tall; use a continuous flat front-facing wall plane behind the plant)."
                    )

        errors.extend(validate_image_prompt(scene_prompt, preset_name=preset_name, scene_key=skey))

    video_keys = set()
    for idx, vd in enumerate(videos):
        vkey = vd.get("key") or f"video_{idx}"
        if vkey in video_keys:
            errors.append(f"Duplicate video key {vkey!r}.")
        video_keys.add(vkey)

        skey = (vd.get("scene_key") or "").strip()
        explicit_uuid = (vd.get("uuid") or "").strip()
        if not skey and not explicit_uuid:
            errors.append(f"[{vkey}] Video entry must specify either 'scene_key' or explicit 'uuid'.")
        elif skey and skey not in scene_keys and not explicit_uuid:
            errors.append(f"[{vkey}] References unknown scene_key {skey!r}.")
        end_skey = (vd.get("end_scene_key") or "").strip()
        end_uuid = (vd.get("end_uuid") or "").strip()
        if end_skey and end_skey not in scene_keys and not end_uuid:
            errors.append(f"[{vkey}] References unknown end_scene_key {end_skey!r}.")

        errors.extend(validate_video_prompt(vd.get("prompt", ""), preset_name=preset_name, video_key=vkey))

    custom_indices = config.get("video_card_indices")
    if custom_indices is not None:
        if not isinstance(custom_indices, list) or not (1 <= len(custom_indices) <= len(videos)):
            errors.append(
                f"video_card_indices must be a non-empty list of length <= {len(videos)} matching rendered 'videos', "
                f"got {len(custom_indices) if isinstance(custom_indices, list) else type(custom_indices).__name__}."
            )
        else:
            seen_cidx = set()
            seen_cslugs = set()
            for item in custom_indices:
                if not isinstance(item, dict) or "card_index" not in item or not item.get("slug"):
                    errors.append(f"Invalid video_card_indices entry {item!r}; expected {{'card_index': int, 'slug': str}}.")
                    continue
                cidx = item["card_index"]
                cslug = str(item["slug"]).strip()
                if not isinstance(cidx, int) or isinstance(cidx, bool) or cidx < 0:
                    errors.append(f"video_card_indices card_index must be a non-negative integer, got {cidx!r}.")
                elif cidx in seen_cidx:
                    errors.append(f"Duplicate card_index {cidx} in video_card_indices.")
                else:
                    seen_cidx.add(cidx)
                if cslug in seen_cslugs:
                    errors.append(f"Duplicate slug {cslug!r} in video_card_indices.")
                seen_cslugs.add(cslug)

    return errors


def audit_project_images_cutout(
    config: Dict[str, Any],
    project_dir: str,
    scenes_dir: Optional[str] = None,
    only_key: str = "",
    max_cutout_l1: float = 58.0,
    max_halo_fattening_pct: float = 9.0,
) -> List[Dict[str, Any]]:
    """
    Offline Stage-2 Image QA Auditor: checks every rendered scene image in `qa/scenes_fullres/`
    against its corresponding 2K 16:9 plate in `plates_2k/` using `evaluate_cutout_silhouette_fidelity`.
    Supports both `<KEY>.jpg` and `<KEY>__<8char_uuid>.jpg` filenames in `qa/scenes_fullres/`.
    """
    import glob
    import json
    from PIL import Image

    sdir = scenes_dir or os.path.join(project_dir, "qa", "scenes_fullres")
    pdir = os.path.join(project_dir, "plates_2k")
    uuid_map: Dict[str, str] = {}
    slug = config.get("slug", "")
    if slug:
        upath = os.path.join(project_dir, f"{slug}_scene_uuids.json")
        if os.path.isfile(upath):
            with open(upath, "r", encoding="utf-8") as f:
                uuid_map = json.load(f)

    results: List[Dict[str, Any]] = []

    for sc in config.get("scenes", []):
        skey = sc.get("key", "")
        if only_key and only_key not in skey:
            continue
        refs = sc.get("refs") or []
        plate_name = refs[0] if refs else ""
        plate_path = os.path.join(pdir, plate_name)

        scene_path = os.path.join(sdir, f"{skey}.jpg")
        if not os.path.isfile(scene_path):
            uid8 = (uuid_map.get(skey) or "")[:8]
            if uid8:
                cand = os.path.join(sdir, f"{skey}__{uid8}.jpg")
                if os.path.isfile(cand):
                    scene_path = cand
            if not os.path.isfile(scene_path):
                matches = sorted(glob.glob(os.path.join(sdir, f"{skey}__*.jpg")), key=os.path.getmtime, reverse=True)
                if matches:
                    scene_path = matches[0]

        if not os.path.isfile(scene_path):
            results.append(
                {
                    "key": skey,
                    "plate": plate_name,
                    "ok": False,
                    "verdict": "MISSING_SCENE_IMAGE",
                    "reason": f"Scene image not found at {scene_path}",
                }
            )
            continue
        if not os.path.isfile(plate_path):
            results.append(
                {
                    "key": skey,
                    "plate": plate_name,
                    "ok": False,
                    "verdict": "MISSING_PLATE_IMAGE",
                    "reason": f"2K plate not found at {plate_path}",
                }
            )
            continue

        with Image.open(plate_path) as pim, Image.open(scene_path) as sim:
            res = evaluate_cutout_silhouette_fidelity(
                plate_img=pim,
                scene_img=sim,
                max_cutout_l1=max_cutout_l1,
                max_halo_fattening_pct=max_halo_fattening_pct,
            )
        res["key"] = skey
        res["plate"] = plate_name
        res["scene_file"] = os.path.basename(scene_path)
        results.append(res)

    return results


def extract_16f_video_grid(
    mp4_source: Any,
    out_grid_path: str,
    fps: int = 4,
    cols: int = 4,
    rows: int = 4,
    tile_width: int = 420,
) -> str:
    """
    Generate a single lightweight 16-frame (`4x4` at `4fps` = every `0.25s`) storyboard JPEG
    from either a file path (`str`) or in-memory `bytes` (`pipe:0`) in ~0.12s using `ffmpeg`.
    """
    import shutil
    import subprocess

    ff = shutil.which("ffmpeg") or "ffmpeg"
    abs_out = os.path.abspath(out_grid_path)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)
    vf_filter = f"fps={fps},scale={tile_width}:-1,tile={cols}x{rows}:padding=4:margin=4:color=black"

    if isinstance(mp4_source, (bytes, bytearray)):
        cmd = [
            ff,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            "pipe:0",
            "-vf",
            vf_filter,
            "-frames:v",
            "1",
            "-update",
            "1",
            "-q:v",
            "5",
            abs_out,
        ]
        subprocess.run(cmd, input=bytes(mp4_source), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    else:
        cmd = [
            ff,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            os.path.abspath(str(mp4_source)),
            "-vf",
            vf_filter,
            "-frames:v",
            "1",
            "-update",
            "1",
            "-q:v",
            "5",
            abs_out,
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return abs_out


