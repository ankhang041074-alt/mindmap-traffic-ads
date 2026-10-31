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


def classify_two_zone_video_motion(
    bg_seg_l1: Sequence[float],
    fg_seg_l1: Sequence[float],
    bg_e2e_l1: float,
    fg_e2e_l1: float,
) -> Dict[str, Any]:
    """
    Evaluate 2-zone in-browser HTML5 <video> scrub metrics (no .mp4 download needed):
      - Top 65% zone (bg_*): measures true 3D camera ego-motion against background walls/architecture.
      - Bottom 35% zone (fg_*): measures lower floor/tabletop & foreground prop displacement.

    Catches two distinct Veo failure modes:
      1. FROZEN_VIDEO: Both background and foreground barely move (still JPEG clip).
      2. CONVEYOR_PROP_CAMERA_FROZEN: Background walls/doors barely move while a foreground
         chair/bench/ottoman slides across the lower frame (tricking global L1 motion metrics).
    """
    bg_mean = sum(bg_seg_l1) / float(len(bg_seg_l1)) if bg_seg_l1 else 0.0
    fg_mean = sum(fg_seg_l1) / float(len(fg_seg_l1)) if fg_seg_l1 else 0.0
    fg_to_bg_e2e_ratio = fg_e2e_l1 / max(bg_e2e_l1, 0.5)
    fg_to_bg_seg_ratio = fg_mean / max(bg_mean, 0.5)

    if bg_e2e_l1 < 5.0 and fg_e2e_l1 < 6.5 and bg_mean < 3.0:
        return {
            "verdict": "FROZEN_VIDEO",
            "ok": False,
            "reason": (
                f"Camera and scene are nearly frozen (bg_e2e_l1={bg_e2e_l1:.2f}, "
                f"fg_e2e_l1={fg_e2e_l1:.2f}, bg_seg_mean={bg_mean:.2f})."
            ),
            "fg_to_bg_e2e_ratio": round(fg_to_bg_e2e_ratio, 2),
        }

    if (bg_e2e_l1 < 8.5 and fg_e2e_l1 >= 12.0 and fg_to_bg_e2e_ratio >= 2.3) or (
        bg_mean < 4.5 and fg_mean >= 10.0 and fg_to_bg_seg_ratio >= 2.5
    ):
        return {
            "verdict": "CONVEYOR_PROP_CAMERA_FROZEN",
            "ok": False,
            "reason": (
                f"Camera/background is stationary while foreground prop slides across frame "
                f"(bg_e2e_l1={bg_e2e_l1:.2f} vs fg_e2e_l1={fg_e2e_l1:.2f}, ratio={fg_to_bg_e2e_ratio:.2f}x)."
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

        errors.extend(validate_image_prompt(sc.get("prompt", ""), preset_name=preset_name, scene_key=skey))

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
        if not isinstance(custom_indices, list) or len(custom_indices) != len(videos):
            errors.append(
                f"video_card_indices must be a list of length {len(videos)} matching 'videos', "
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
