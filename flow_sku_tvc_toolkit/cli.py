"""
Unified CLI for Flow Exact-SKU TVC Toolkit.

Usage examples:
  python3 -m flow_sku_tvc_toolkit list-presets
  python3 -m flow_sku_tvc_toolkit init-sku --slug crochet_tulip --preset crochet_decor --project-id dfcf77a5-5374-4678-9f80-1c5ea7b5c305
  python3 -m flow_sku_tvc_toolkit isolate-white --input raw_photo.jpg --output products/crochet_tulip/raw_white.jpg --preset crochet_decor --project-id dfcf77a5-5374-4678-9f80-1c5ea7b5c305
  python3 -m flow_sku_tvc_toolkit build-plates --input products/crochet_tulip/raw_white.jpg --config products/crochet_tulip/sku_project.json
  python3 -m flow_sku_tvc_toolkit validate --config products/crochet_tulip/sku_project.json
  python3 -m flow_sku_tvc_toolkit run-images --config products/crochet_tulip/sku_project.json --phase check1
  python3 -m flow_sku_tvc_toolkit map-uuids --config products/crochet_tulip/sku_project.json
  python3 -m flow_sku_tvc_toolkit run-videos --config products/crochet_tulip/sku_project.json --phase all
  python3 -m flow_sku_tvc_toolkit download-1080p --config products/crochet_tulip/sku_project.json --out-dir ~/Downloads/crochet_tulip
"""

import argparse
import asyncio
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .guardrails import validate_sku_config
from .plate_engine import build_sku_plates_from_image
from .presets import PRESETS, get_preset, list_presets


def _load_config(config_path: str) -> Tuple[Dict[str, Any], str]:
    abs_path = os.path.abspath(config_path)
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"Config file not found: {abs_path}")
    with open(abs_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data, os.path.dirname(abs_path)


def _build_starter_config(slug: str, prefix: str, preset_name: str, project_id: str) -> Dict[str, Any]:
    preset = get_preset(preset_name)
    first_plate = f"{prefix}_{preset.plates[0].suffix}.jpg"
    macro_ref = f"{prefix}_REF_2_CLOSEUP_1024.jpg"

    is_pair = len(preset.plates[0].placements) >= 2
    lock_header = preset.pair_cutout_lock_header if is_pair else preset.single_cutout_lock_header

    if preset_name.startswith("crochet"):
        sample_scene_tail = (
            "an 85mm live-action Kodak Vision3 250D sunlit artisan tabletop scene: the handmade crochet piece rests naturally "
            "on a warm solid European white-oak table beside a 9.5cm matte cream ceramic coffee mug positioned slightly behind to lock true tabletop scale, "
            "softly blurred foreground linen napkin corner bottom-left for 3D depth, warm morning side-window golden sunbeams across the wood grain, "
            "even clean natural daylight preserving every cotton crochet stitch, soft realistic yarn contact shadow on the oak surface, zero text."
        )
        sample_video_prompt = (
            "Continuous, clearly visible 4-second 85mm gentle forward diagonal camera push-in across the sunlit solid white-oak table "
            "with natural 3D optical depth perspective while all tabletop objects, the ceramic mug, linen napkin, and handmade crochet piece "
            "remain 100% stationary anchored on the oak surface. Warm morning window sunbeams softly illuminate the wood grain "
            "while preserving the exact solid shape, crisp interlocking milk-cotton crochet yarn stitches, and true colors of the crochet item. "
            "No people, no camera equipment, zero morphing, zero text."
        )
    else:
        sample_scene_tail = (
            "a 50mm live-action Kodak Vision3 250D sunlit architectural interior scene with natural scale-locking furniture "
            "set on the same floor plane, warm afternoon diagonal window sunbeams on the plaster wall behind, "
            "even clean natural daylight around the product, realistic floor contact shadow underneath the base, zero text."
        )
        sample_video_prompt = (
            "Continuous, clearly visible 4-second 50mm gentle forward camera push-in across the sunlit room "
            "with natural 3D architectural perspective while all furniture, architectural elements, and the product "
            "remain 100% stationary anchored to the floor. Warm afternoon window sunbeams illuminate the subtle plaster wall texture "
            "while preserving the exact solid shape, proportions, and surface texture of the product. "
            "No people, no camera equipment, zero morphing, zero text."
        )

    return {
        "slug": slug,
        "prefix": prefix,
        "preset": preset.name,
        "project_id": project_id,
        "notes_vi": f"Dự án SKU '{slug}' ({preset.label_vi}). Chỉ commit file JSON cấu hình & UUID; ảnh plates_2k/ và qa/ lưu local.",
        "exclude_uuids": [],
        "scenes": [
            {
                "key": "S01_HERO_SAMPLE_SCENE",
                "refs": [first_plate, macro_ref],
                "prompt": lock_header + sample_scene_tail,
            }
        ],
        "videos": [
            {
                "key": "V01_HERO_SAMPLE_4S",
                "scene_key": "S01_HERO_SAMPLE_SCENE",
                "prompt": sample_video_prompt,
            }
        ],
    }


def cmd_list_presets(_args: argparse.Namespace) -> int:
    print("=== DANH SÁCH PRESET TỶ LỆ VẬT LÝ & KHÓA KHUÔN (FLOW SKU TVC TOOLKIT) ===")
    for p in list_presets():
        print(f"\n[{p.name}] — {p.label_vi}")
        print(f"  * Tỷ lệ thực tế : {p.physical_size_note_vi}")
        print(f"  * Ống kính chuẩn: {p.recommended_lens}")
        print(f"  * Vật neo tỷ lệ : {p.scale_anchors_vi}")
        print(f"  * Số Plate 2K   : {len(p.plates)} tấm ({', '.join(pt.suffix for pt in p.plates)})")
    return 0


def cmd_init_sku(args: argparse.Namespace) -> int:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", args.slug.strip()).strip("_").lower()
    if not slug:
        raise ValueError("--slug must contain alphanumeric characters.")
    prefix = (args.prefix or slug).strip().upper()
    prefix = re.sub(r"[^A-Z0-9_]+", "_", prefix).strip("_")

    out_dir = os.path.abspath(args.out_dir or os.path.join("products", slug))
    os.makedirs(out_dir, exist_ok=True)
    cfg_path = os.path.join(out_dir, "sku_project.json")
    if os.path.exists(cfg_path) and not args.force:
        raise FileExistsError(f"Config already exists: {cfg_path} (pass --force to overwrite)")

    cfg = _build_starter_config(slug=slug, prefix=prefix, preset_name=args.preset, project_id=args.project_id)
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

    print(f"Created lightweight SKU project config -> {cfg_path}")
    print(f"  Preset : {args.preset}")
    print(f"  Prefix : {prefix}")
    print(f"  Next   : python3 -m flow_sku_tvc_toolkit build-plates --input <ANH_NEN_TRANG.jpg> --config {cfg_path}")
    return 0


def cmd_build_plates(args: argparse.Namespace) -> int:
    if args.config:
        cfg, proj_dir = _load_config(args.config)
        out_dir = os.path.abspath(args.out_dir or proj_dir)
        prefix = args.prefix or cfg["prefix"]
        preset_name = args.preset or cfg["preset"]
    else:
        if not (args.out_dir and args.prefix and args.preset):
            raise ValueError("Provide either --config OR all of (--out-dir, --prefix, --preset).")
        out_dir = os.path.abspath(args.out_dir)
        prefix = args.prefix
        preset_name = args.preset

    manifest = build_sku_plates_from_image(
        input_path=os.path.abspath(args.input),
        out_dir=out_dir,
        prefix=prefix,
        preset_name=preset_name,
        bg_threshold=args.bg_threshold,
        max_chroma=args.max_chroma,
        allow_nonwhite_bg=args.allow_nonwhite_bg,
        auto_split_twin_pair=not args.no_split_twin_pair,
    )
    print(f"Generated {len(manifest['clean_refs'])} clean refs + {len(manifest['plates_2k'])} 2K 16:9 plates in {out_dir}")
    print(f"  Cutout bbox : {manifest['cutout_stats']['tight_bbox']} (aspect W/H = {manifest['cutout_stats']['aspect_ratio_w_over_h']})")
    for rname in manifest["clean_refs"]:
        print(f"  [REF 1K]   clean_refs/{rname}")
    for pt in manifest["plates_2k"]:
        print(f"  [PLATE 2K] plates_2k/{pt['filename']} — {pt['description_vi']}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    cfg, proj_dir = _load_config(args.config)
    errs = validate_sku_config(cfg, project_dir=proj_dir, require_local_plates=args.check_files)
    if errs:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(
        f"VALIDATION PASSED: slug={cfg['slug']!r}, preset={cfg['preset']!r}, "
        f"scenes={len(cfg.get('scenes', []))}, videos={len(cfg.get('videos', []))}"
    )
    return 0


def cmd_isolate_white(args: argparse.Namespace) -> int:
    from .flow_cdp import isolate_white_on_flow

    asyncio.run(
        isolate_white_on_flow(
            input_image_path=args.input,
            output_white_path=args.output,
            project_id=args.project_id,
            preset_name=args.preset,
            custom_prompt=args.prompt or "",
            port=args.port,
        )
    )
    return 0


def cmd_run_images(args: argparse.Namespace) -> int:
    from .flow_cdp import run_images_pipeline

    cfg, proj_dir = _load_config(args.config)
    asyncio.run(
        run_images_pipeline(
            config=cfg,
            project_dir=proj_dir,
            phase=args.phase,
            start_index=args.start_index,
            only_key=args.only_key,
            port=args.port,
        )
    )
    return 0


def cmd_map_uuids(args: argparse.Namespace) -> int:
    from .flow_cdp import map_scene_uuids_pipeline

    cfg, proj_dir = _load_config(args.config)
    asyncio.run(
        map_scene_uuids_pipeline(
            config=cfg,
            project_dir=proj_dir,
            port=args.port,
            only_key=args.only_key,
            force_remap=args.force_remap,
        )
    )
    return 0


def cmd_run_videos(args: argparse.Namespace) -> int:
    from .flow_cdp import run_videos_pipeline

    cfg, proj_dir = _load_config(args.config)
    asyncio.run(
        run_videos_pipeline(
            config=cfg,
            project_dir=proj_dir,
            phase=args.phase,
            start_index=args.start_index,
            only_key=args.only_key,
            port=args.port,
        )
    )
    return 0


def cmd_download_1080p(args: argparse.Namespace) -> int:
    from .flow_cdp import download_and_merge_1080p_pipeline, resolve_video_card_indices_by_start_frame

    cfg, proj_dir = _load_config(args.config)
    videos = cfg.get("videos", [])
    if not videos:
        raise ValueError("No videos defined in SKU config.")

    custom_map = cfg.get("video_card_indices")
    uuid_path = os.path.join(proj_dir, f"{cfg['slug']}_scene_uuids.json")
    if custom_map:
        pairs = [(int(item["card_index"]), str(item["slug"])) for item in custom_map]
    elif os.path.isfile(uuid_path) or all((v.get("uuid") or "").strip() for v in videos):
        print("Auto-resolving Video-tab card indices by start-frame visual match (handles out-of-order re-renders)...")
        pairs = asyncio.run(
            resolve_video_card_indices_by_start_frame(
                config=cfg,
                project_dir=proj_dir,
                port=args.port,
            )
        )
    else:
        n = len(videos)
        pairs = [((n - 1) - i, f"{i + 1:02d}_{v['key']}") for i, v in enumerate(videos)]

    out_dir = os.path.abspath(os.path.expanduser(args.out_dir or os.path.join(proj_dir, "renders_1080p")))
    master_name = args.master_name or f"{cfg['slug'].upper()}_MASTER_1080p.mp4"
    asyncio.run(
        download_and_merge_1080p_pipeline(
            project_id=cfg["project_id"],
            card_index_to_slug=pairs,
            target_dir=out_dir,
            master_filename=master_name,
            port=args.port,
        )
    )
    return 0


def cmd_audit_videos(args: argparse.Namespace) -> int:
    from .flow_cdp import (
        audit_videos_2zone_in_browser,
        resolve_video_card_indices_by_start_frame,
    )

    cfg, proj_dir = _load_config(args.config)
    videos = cfg.get("videos", [])
    if not videos:
        raise ValueError("No videos defined in SKU config.")

    custom_map = cfg.get("video_card_indices")
    uuid_path = os.path.join(proj_dir, f"{cfg['slug']}_scene_uuids.json")
    if custom_map:
        pairs = [(int(item["card_index"]), str(item["slug"])) for item in custom_map]
    elif os.path.isfile(uuid_path) or all((v.get("uuid") or "").strip() for v in videos):
        pairs = asyncio.run(
            resolve_video_card_indices_by_start_frame(
                config=cfg,
                project_dir=proj_dir,
                port=args.port,
            )
        )
    else:
        n = len(videos)
        pairs = [((n - 1) - i, f"{i + 1:02d}_{v['key']}") for i, v in enumerate(videos)]

    out_json = args.out_json or os.path.join(proj_dir, "qa", "video_2zone_audit.json")
    results = asyncio.run(
        audit_videos_2zone_in_browser(
            project_id=cfg["project_id"],
            card_index_to_slug=pairs,
            out_json_path=out_json,
            port=args.port,
        )
    )
    failed = [r for r in results if not r.get("ok")]
    if failed:
        print(f"AUDIT FAILED on {len(failed)}/{len(results)} video(s). Saved report -> {out_json}", file=sys.stderr)
        return 1
    print(f"AUDIT PASSED on all {len(results)} video(s). Saved report -> {out_json}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python3 -m flow_sku_tvc_toolkit",
        description="Flow Exact-SKU TVC Toolkit (Cutout Plate Engine + Silent AdsPower CDP Runner)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp_list = sub.add_parser("list-presets", help="Show calibrated physical scale presets (tree_4ft, crochet, etc.)")
    sp_list.set_defaults(func=cmd_list_presets)

    sp_init = sub.add_parser("init-sku", help="Create a lightweight SKU project config JSON (Git-friendly, 0 heavy images)")
    sp_init.add_argument("--slug", required=True, help="Short folder slug, e.g. crochet_tulip_pot")
    sp_init.add_argument("--prefix", default="", help="Optional uppercase plate prefix, e.g. TULIP")
    sp_init.add_argument("--preset", choices=sorted(PRESETS.keys()), default="crochet_decor")
    sp_init.add_argument("--project-id", required=True, help="Google Flow project UUID")
    sp_init.add_argument("--out-dir", default="", help="Target folder (defaults to products/<slug>)")
    sp_init.add_argument("--force", action="store_true", help="Overwrite existing sku_project.json")
    sp_init.set_defaults(func=cmd_init_sku)

    sp_iso = sub.add_parser("isolate-white", help="Silently isolate a raw messy-background photo onto pure #FFFFFF on Flow (1:1)")
    sp_iso.add_argument("--input", required=True, help="Raw product photo path")
    sp_iso.add_argument("--output", required=True, help="Output clean #FFFFFF 1024x1024 JPG path")
    sp_iso.add_argument("--project-id", required=True, help="Google Flow project UUID")
    sp_iso.add_argument("--preset", choices=sorted(PRESETS.keys()), default="crochet_decor")
    sp_iso.add_argument("--prompt", default="", help="Optional custom isolation prompt")
    sp_iso.add_argument("--port", type=int, default=None, help="Optional explicit AdsPower CDP port")
    sp_iso.set_defaults(func=cmd_isolate_white)

    sp_plates = sub.add_parser("build-plates", help="Generate 1K clean/macro refs + 2K 16:9 #FFFFFF plates from 1 white-bg/PNG photo")
    sp_plates.add_argument("--input", required=True, help="Clean white-background JPG/PNG or transparent PNG")
    sp_plates.add_argument("--config", default="", help="Path to sku_project.json")
    sp_plates.add_argument("--out-dir", default="", help="Output SKU directory (if --config omitted)")
    sp_plates.add_argument("--prefix", default="", help="Filename prefix (if --config omitted)")
    sp_plates.add_argument("--preset", choices=sorted(PRESETS.keys()), default="", help="Category preset (if --config omitted)")
    sp_plates.add_argument("--bg-threshold", type=int, default=240, help="Near-white border flood min RGB threshold (default 240)")
    sp_plates.add_argument("--max-chroma", type=int, default=18, help="Max RGB channel spread for studio white border (default 18)")
    sp_plates.add_argument("--allow-nonwhite-bg", action="store_true", help="Bypass <2%% white-border safety guard")
    sp_plates.add_argument("--no-split-twin-pair", action="store_true", help="Keep side-by-side twin pairs together as 1 SKU cutout")
    sp_plates.set_defaults(func=cmd_build_plates)

    sp_val = sub.add_parser("validate", help="Offline guardrail check on all image & Veo 4s prompts in sku_project.json")
    sp_val.add_argument("--config", required=True, help="Path to sku_project.json")
    sp_val.add_argument("--check-files", action="store_true", help="Also verify local plates_2k/ and clean_refs/ exist")
    sp_val.set_defaults(func=cmd_validate)

    sp_img = sub.add_parser("run-images", help="Silently upload plates & generate 16:9 Nano Banana Pro scenes on Flow")
    sp_img.add_argument("--config", required=True)
    sp_img.add_argument("--phase", choices=["check1", "rest", "slice", "all", "only"], default="check1")
    sp_img.add_argument("--start-index", type=int, default=0)
    sp_img.add_argument("--only-key", default="")
    sp_img.add_argument("--port", type=int, default=None)
    sp_img.set_defaults(func=cmd_run_images)

    sp_map = sub.add_parser("map-uuids", help="Map generated Flow images 1-to-1 to scene keys via CDK virtual scroll")
    sp_map.add_argument("--config", required=True)
    sp_map.add_argument("--only-key", default="", help="Update only scene(s) matching this key substring after a single-scene re-render")
    sp_map.add_argument("--force-remap", action="store_true", help="Allow full newest-first overwrite even when extra re-rendered images exist")
    sp_map.add_argument("--port", type=int, default=None)
    sp_map.set_defaults(func=cmd_map_uuids)

    sp_vid = sub.add_parser("run-videos", help="Silently generate 4s Veo 3.1 - Fast 16:9 clips on Flow")
    sp_vid.add_argument("--config", required=True)
    sp_vid.add_argument("--phase", choices=["all", "slice", "only", "qa-only"], default="all")
    sp_vid.add_argument("--start-index", type=int, default=0)
    sp_vid.add_argument("--only-key", default="")
    sp_vid.add_argument("--port", type=int, default=None)
    sp_vid.set_defaults(func=cmd_run_videos)

    sp_dl = sub.add_parser("download-1080p", help="Silently upscale/download 1080p clips from Flow Video tab & merge Master MP4")
    sp_dl.add_argument("--config", required=True)
    sp_dl.add_argument("--out-dir", default="", help="Output folder (e.g. ~/Downloads/SKU_1080p)")
    sp_dl.add_argument("--master-name", default="", help="Merged master MP4 filename")
    sp_dl.add_argument("--port", type=int, default=None)
    sp_dl.set_defaults(func=cmd_download_1080p)

    sp_aud = sub.add_parser("audit-videos", help="In-browser 2-Zone HTML5 <video> scrub QA (0 .mp4 downloads; catches frozen camera & sliding props)")
    sp_aud.add_argument("--config", required=True)
    sp_aud.add_argument("--out-json", default="", help="Optional output JSON report path (defaults to qa/video_2zone_audit.json)")
    sp_aud.add_argument("--port", type=int, default=None)
    sp_aud.set_defaults(func=cmd_audit_videos)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
