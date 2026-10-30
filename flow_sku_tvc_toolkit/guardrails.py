"""
Compile-time & pre-flight prompt guardrails for Nano Banana Pro (16:9 Images)
and Veo 3.1 - Fast (4s 3D-Parallax / 2-Frame Videos).
"""

import os
import re
from typing import Any, Dict, List

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

    return errors
