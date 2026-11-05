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

from .guardrails import audit_project_images_cutout, validate_sku_config
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
            "a 50mm live-action Kodak Vision3 250D sunlit architectural interior scene: positioned flush along the same flat floor depth plane "
            "behind the product is natural scale-locking furniture (82cm oak console or bench styled with lived-in ceramic vase, books, and woven baskets) "
            "beneath a sunlit window with sheer linen curtains casting warm diagonal sunbeams across the wall, floor, and outer product edges, "
            "realistic floor contact shadow directly underneath the base, zero text."
        )
        sample_video_prompt = (
            "Continuous, clearly visible 4-second 50mm gentle low-horizon forward 3D camera push-in across the sunlit room "
            "in rich 3D optical parallax (maintaining a locked level horizon without zooming in close, keeping the entire product "
            "from floor base to top tip 100% uncut and visible head-to-toe inside the frame from 0s to 4s) while all furniture, "
            "architectural elements, and the product remain 100% stationary anchored to the floor. Warm window sunbeams gleam softly "
            "across the room while preserving the exact solid shape, proportions, and surface texture of the product. "
            "No people, no camera equipment, zero fade-out, zero morphing, zero text."
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
    eff_phase = "only" if args.only_key else args.phase
    asyncio.run(
        run_images_pipeline(
            config=cfg,
            project_dir=proj_dir,
            phase=eff_phase,
            start_index=args.start_index,
            only_key=args.only_key,
            port=args.port,
        )
    )
    if getattr(args, "auto_audit", True):
        print("\n=== [AUTO-AUDIT EYE] HẬU KIỂM ẢNH SAU KHI TẠO (ADVISORY) ===")
        audit_and_record_scenes(
            config=cfg,
            project_dir=proj_dir,
            only_key=args.only_key,
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
    eff_root = os.path.abspath(getattr(args, "repo_root", "") or os.getcwd())
    eff_slug = _resolve_brain_project_slug(cfg, eff_root)
    try:
        from analyzer.gate_ledger import get_gate_status

        for vd in cfg.get("videos", []):
            vkey = str(vd.get("key") or "")
            if args.only_key and args.only_key not in vkey:
                continue
            skey = str(vd.get("scene_key") or "").strip()
            if not skey:
                continue
            g_stat = get_gate_status(eff_slug, skey, repo_root=eff_root)
            if g_stat and g_stat.get("verdict") == "fail" and not g_stat.get("override_reason"):
                print(
                    f"⚠️ [ADVISORY EYE WARNING] Video {vkey!r} dùng start-frame {skey!r} đang có verdict='fail' "
                    f"(L1={g_stat.get('cutout_l1')}, defects={g_stat.get('blocking_defects')}) chưa có override_reason.\n"
                    f"   💡 Hệ thống vẫn cho chạy (không chặn cứng). Nếu cố ý giữ ảnh này, hãy ghi chú: "
                    f"python3 -m analyzer.gate_ledger override --project-slug {eff_slug} --scene-key {skey} --reason \"...\""
                )
    except Exception:
        pass

    eff_phase = "only" if args.only_key else args.phase
    asyncio.run(
        run_videos_pipeline(
            config=cfg,
            project_dir=proj_dir,
            phase=eff_phase,
            start_index=args.start_index,
            only_key=args.only_key,
            port=args.port,
        )
    )
    if getattr(args, "auto_audit", True):
        print("\n=== [AUTO-FFMPEG-16F-GRID & 2-ZONE AUDIT] XUẤT LƯỚI 16 KHUNG HÌNH TỪ LUỒNG 720p (0s CHỜ 1080p) ===")
        try:
            audit_args = argparse.Namespace(
                config=args.config,
                out_json=os.path.join(proj_dir, "qa", "video_2zone_audit.json"),
                port=args.port,
            )
            cmd_audit_videos(audit_args)
        except Exception as exc:
            print(f"⚠️ [ADVISORY VIDEO AUDIT WARNING] {exc}")
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


def cmd_audit_images(args: argparse.Namespace) -> int:
    cfg, proj_dir = _load_config(args.config)
    results = audit_project_images_cutout(
        config=cfg,
        project_dir=proj_dir,
        scenes_dir=args.scenes_dir or None,
        only_key=args.only_key,
        max_cutout_l1=args.max_cutout_l1,
        max_halo_fattening_pct=args.max_fattening_pct,
    )
    out_json = args.out_json or os.path.join(proj_dir, "qa", "image_cutout_audit.json")
    os.makedirs(os.path.dirname(os.path.abspath(out_json)), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    for r in results:
        status = "PASS" if r.get("ok") else f"FAIL ({r.get('verdict')})"
        print(
            f"  [{status}] {r['key']} | cutout_l1={r.get('cutout_rgb_l1', 'N/A')} | "
            f"fattening={r.get('halo_fattening_pct', 'N/A')}% | {r.get('reason', '')}"
        )

    failed = [r for r in results if not r.get("ok")]
    if failed:
        print(f"IMAGE AUDIT FAILED on {len(failed)}/{len(results)} scene(s). Saved -> {out_json}", file=sys.stderr)
        return 1
    print(f"IMAGE AUDIT PASSED on all {len(results)} scene(s). Saved -> {out_json}")
    return 0


def _resolve_brain_project_slug(config: Dict[str, Any], repo_root: str) -> str:
    explicit = str(config.get("project_slug") or "").strip()
    if explicit:
        return explicit
    raw_slug = str(config.get("slug") or "").strip()
    products_data = os.path.join(repo_root, "data", "products")
    if raw_slug and os.path.isdir(products_data):
        norm_raw = re.sub(r"[^a-z0-9]+", "", raw_slug.lower())
        for entry in sorted(os.listdir(products_data)):
            norm_entry = re.sub(r"[^a-z0-9]+", "", entry.lower())
            if norm_raw and (norm_raw in norm_entry or norm_entry in norm_raw):
                return entry
            tokens = [t for t in re.split(r"[^a-z0-9]+", raw_slug.lower()) if len(t) >= 4]
            if tokens and all(t in norm_entry for t in tokens[:2]):
                return entry
    return raw_slug or "general"


def audit_and_record_scenes(
    config: Dict[str, Any],
    project_dir: str,
    project_slug: Optional[str] = None,
    repo_root: Optional[str] = None,
    scenes_dir: Optional[str] = None,
    only_key: str = "",
) -> List[Dict[str, Any]]:
    """
    Run `verify_rendered_image_contract` + `record_gate_result` across all rendered scenes in `config`,
    persist advisory verdicts (`pass` / `warn` / `fail` / `no_ref`) into `gate_ledger.json`, and save
    `qa/image_gate_audit.json`.
    """
    import glob
    from analyzer.gate_ledger import record_gate_result
    from analyzer.plate_resolver import resolve_local_plate
    from analyzer.post_render_image_gate import verify_rendered_image_contract

    eff_root = os.path.abspath(repo_root or os.getcwd())
    eff_slug = project_slug or _resolve_brain_project_slug(config, eff_root)
    sdir = scenes_dir or os.path.join(project_dir, "qa", "scenes_fullres")
    pdir = os.path.join(project_dir, "plates_2k")

    uuid_map: Dict[str, str] = {}
    slug = config.get("slug", "")
    if slug:
        upath = os.path.join(project_dir, f"{slug}_scene_uuids.json")
        if os.path.isfile(upath):
            try:
                with open(upath, "r", encoding="utf-8") as f:
                    uuid_map = json.load(f)
            except Exception:
                uuid_map = {}

    recorded: List[Dict[str, Any]] = []
    for sc in config.get("scenes", []):
        skey = str(sc.get("key") or "").strip()
        if not skey or (only_key and only_key not in skey):
            continue
        refs = list(sc.get("refs") or [])
        plate_name = str(refs[0]).strip() if refs else ""
        plate_path: Optional[str] = None
        if plate_name:
            cand_p = os.path.join(pdir, plate_name)
            if os.path.isfile(cand_p):
                plate_path = os.path.abspath(cand_p)
        if not plate_path:
            plate_path = resolve_local_plate(refs + [skey], eff_root, eff_slug)

        scene_path = str(sc.get("rendered_path") or "").strip()
        if scene_path and not os.path.isabs(scene_path):
            scene_path = os.path.join(project_dir, scene_path)
        if not scene_path or not os.path.isfile(scene_path):
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
            continue

        gate_rep = verify_rendered_image_contract(
            rendered_image_path=scene_path,
            project_slug=eff_slug,
            ref_image_path=plate_path,
            prompt_text=str(sc.get("prompt") or ""),
            repo_root=eff_root,
        )
        entry = record_gate_result(
            project_slug=eff_slug,
            scene_key=skey,
            gate_report=gate_rep,
            plate_path=plate_path,
            media_ref=str(uuid_map.get(skey) or ""),
            repo_root=eff_root,
        )
        recorded.append(entry)
        v_up = str(entry.get("verdict") or "pass").upper()
        print(
            f"  [{v_up}] {skey} | plate={os.path.basename(plate_path) if plate_path else 'None'} | "
            f"cutout_l1={entry.get('cutout_l1')} | defects={entry.get('blocking_defects', [])}"
        )

    out_json = os.path.join(project_dir, "qa", "image_gate_audit.json")
    os.makedirs(os.path.dirname(os.path.abspath(out_json)), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(recorded, f, indent=2, ensure_ascii=False)
    return recorded


def plan_scenes(
    config: Dict[str, Any],
    project_slug: str,
    brief_lines: Sequence[str],
    closeup_ref: str = "",
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fill `config["scenes"]` and `config["videos"]` from short brief lines (`KEY | PLATE_FILENAME | brief`)
    using `run_project_director_stage` (Brain).
    - Preserves any existing scene or video entry with `"locked": true` untouched.
    - Prints an advisory warning if any generated prompt exceeds 300 words.
    """
    from analyzer.project_director_loop import run_project_director_stage

    eff_root = os.path.abspath(repo_root or os.getcwd())
    prefix = str(config.get("prefix") or config.get("slug") or "SKU").upper()
    default_closeup = closeup_ref.strip() or f"{prefix}_REF_2_CLOSEUP_1024.jpg"

    existing_scenes_by_key: Dict[str, Dict[str, Any]] = {
        str(s.get("key")): dict(s) for s in (config.get("scenes") or []) if s.get("key")
    }
    existing_videos_by_skey: Dict[str, Dict[str, Any]] = {
        str(v.get("scene_key")): dict(v) for v in (config.get("videos") or []) if v.get("scene_key")
    }

    new_scenes: List[Dict[str, Any]] = []
    new_videos: List[Dict[str, Any]] = []

    for idx, raw_line in enumerate(brief_lines):
        line = str(raw_line or "").strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            raise ValueError(
                f"Invalid brief line {line!r}; expected 'SCENE_KEY | PLATE_FILENAME | scene_brief'."
            )
        skey, plate_file, scene_brief = parts[0], parts[1], "|".join(parts[2:]).strip()

        existing_sc = existing_scenes_by_key.get(skey)
        if existing_sc and existing_sc.get("locked") is True:
            new_scenes.append(existing_sc)
            existing_vd = existing_videos_by_skey.get(skey)
            if existing_vd:
                new_videos.append(existing_vd)
            continue

        img_res = run_project_director_stage(
            project_slug=project_slug,
            scene_brief=scene_brief,
            media_type="image",
            shot_id=skey,
            camera_recipe_index=idx,
            repo_root=eff_root,
        )
        img_prompt = str(img_res.get("final_prompt") or "").strip()
        wc_img = len(img_prompt.split())
        if wc_img > 300:
            print(
                f"⚠️ [ADVISORY WORD-COUNT WARNING] Scene {skey!r} prompt has {wc_img} words (> 300 words). "
                "Consider trimming if Nano Banana Pro dilutes attention."
            )

        refs = [plate_file]
        if default_closeup and default_closeup not in refs:
            refs.append(default_closeup)

        sc_entry: Dict[str, Any] = {
            "key": skey,
            "refs": refs,
            "scene_brief": scene_brief,
            "prompt": img_prompt,
        }
        new_scenes.append(sc_entry)

        existing_vd = existing_videos_by_skey.get(skey)
        if existing_vd and existing_vd.get("locked") is True:
            new_videos.append(existing_vd)
        else:
            vid_res = run_project_director_stage(
                project_slug=project_slug,
                scene_brief=scene_brief,
                media_type="video",
                shot_id=f"V_{skey}",
                camera_recipe_index=idx,
                repo_root=eff_root,
            )
            vid_prompt = str(vid_res.get("final_prompt") or "").strip()
            new_videos.append(
                {
                    "key": f"V_{skey}_4S",
                    "scene_key": skey,
                    "prompt": vid_prompt,
                }
            )

    config["project_slug"] = project_slug
    config["scenes"] = new_scenes
    config["videos"] = new_videos
    return config


def cmd_plan_scenes(args: argparse.Namespace) -> int:
    cfg, _ = _load_config(args.config)
    eff_root = os.path.abspath(args.repo_root or os.getcwd())
    eff_slug = args.project_slug or _resolve_brain_project_slug(cfg, eff_root)
    with open(os.path.abspath(args.briefs), "r", encoding="utf-8") as bf:
        lines = bf.readlines()
    updated = plan_scenes(
        config=cfg,
        project_slug=eff_slug,
        brief_lines=lines,
        closeup_ref=args.closeup or "",
        repo_root=eff_root,
    )
    with open(os.path.abspath(args.config), "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
    print(
        f"✅ [BRAIN PLAN-SCENES] Updated {len(updated.get('scenes', []))} scene(s) and "
        f"{len(updated.get('videos', []))} video(s) in {args.config} (project_slug={eff_slug!r})."
    )
    return 0


def save_formula_from_config(
    config: Dict[str, Any],
    key: str,
    note: str = "",
    project_slug: Optional[str] = None,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Save a winning scene or video prompt from `config` directly into `data/prompt_vault.json`
    via `save_prompt_to_vault()` WITHOUT mutating `project_lock.json`.
    """
    from analyzer.project_director_loop import save_prompt_to_vault

    eff_root = os.path.abspath(repo_root or os.getcwd())
    eff_slug = project_slug or _resolve_brain_project_slug(config, eff_root)
    target_key = str(key or "").strip()

    for sc in config.get("scenes", []):
        if str(sc.get("key")) == target_key:
            brief = str(sc.get("scene_brief") or note or target_key)
            return save_prompt_to_vault(
                project_slug=eff_slug,
                shot_id=target_key,
                full_prompt=str(sc.get("prompt") or ""),
                media_type="image",
                origin_track="agent_bespoke",
                scene_brief=brief,
                human_approved=True,
                repo_root=eff_root,
            )

    for vd in config.get("videos", []):
        if str(vd.get("key")) == target_key:
            brief = str(note or vd.get("scene_key") or target_key)
            return save_prompt_to_vault(
                project_slug=eff_slug,
                shot_id=target_key,
                full_prompt=str(vd.get("prompt") or ""),
                media_type="video",
                origin_track="agent_bespoke",
                scene_brief=brief,
                human_approved=True,
                repo_root=eff_root,
            )

    raise KeyError(f"Key {target_key!r} not found in config['scenes'] or config['videos'].")


def cmd_save_formula(args: argparse.Namespace) -> int:
    cfg, _ = _load_config(args.config)
    res = save_formula_from_config(
        config=cfg,
        key=args.key,
        note=args.note or "",
        project_slug=args.project_slug or None,
        repo_root=args.repo_root or None,
    )
    entry = res.get("entry") or {}
    print(
        f"✅ [SAVE-FORMULA -> PROMPT VAULT] Saved {entry.get('entry_id')} "
        f"(project={entry.get('project_slug')}, media={entry.get('media_type')}) -> {res.get('vault_json_path')}"
    )
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
    sp_img.add_argument(
        "--auto-audit",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Automatically run post-render image gate audit after generating images (default: True)",
    )
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
    sp_vid.add_argument("--repo-root", default="", help="Optional repo root for gate_ledger lookup")
    sp_vid.add_argument(
        "--auto-audit",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Automatically extract 16-frame 4x4 ffmpeg grids & run 2-zone audit from 720p stream after run-videos (default: True)",
    )
    sp_vid.set_defaults(func=cmd_run_videos)

    sp_plan = sub.add_parser("plan-scenes", help="Auto-generate image & video prompts in sku_project.json from short briefs via Brain")
    sp_plan.add_argument("--config", required=True, help="Path to sku_project.json")
    sp_plan.add_argument("--project-slug", default="", help="Project lock slug in data/products/<slug>")
    sp_plan.add_argument("--briefs", required=True, help="Text file with 'KEY | PLATE_FILE | brief' per line")
    sp_plan.add_argument("--closeup", default="", help="Optional 1K closeup ref filename")
    sp_plan.add_argument("--repo-root", default="", help="Optional repository root path")
    sp_plan.set_defaults(func=cmd_plan_scenes)

    sp_save = sub.add_parser("save-formula", help="Save a winning scene/video prompt from sku_project.json into data/prompt_vault.json")
    sp_save.add_argument("--config", required=True, help="Path to sku_project.json")
    sp_save.add_argument("--key", required=True, help="Scene key or video key to save")
    sp_save.add_argument("--note", default="", help="Optional note/scene_brief description")
    sp_save.add_argument("--project-slug", default="", help="Optional explicit project_slug")
    sp_save.add_argument("--repo-root", default="", help="Optional repository root path")
    sp_save.set_defaults(func=cmd_save_formula)

    sp_dl = sub.add_parser("download-1080p", help="Silently upscale/download 1080p clips from Flow Video tab & merge Master MP4")
    sp_dl.add_argument("--config", required=True)
    sp_dl.add_argument("--out-dir", default="", help="Output folder (e.g. ~/Downloads/SKU_1080p)")
    sp_dl.add_argument("--master-name", default="", help="Merged master MP4 filename")
    sp_dl.add_argument("--port", type=int, default=None)
    sp_dl.set_defaults(func=cmd_download_1080p)

    sp_aud_img = sub.add_parser("audit-images", help="Offline Stage-2 Cutout & Silhouette Fattening QA against 2K white plates")
    sp_aud_img.add_argument("--config", required=True)
    sp_aud_img.add_argument("--scenes-dir", default="", help="Optional custom scenes directory (defaults to qa/scenes_fullres)")
    sp_aud_img.add_argument("--only-key", default="", help="Filter scenes by key substring")
    sp_aud_img.add_argument("--max-cutout-l1", type=float, default=58.0, help="Max allowed RGB L1 inside cutout mask (default 58.0)")
    sp_aud_img.add_argument("--max-fattening-pct", type=float, default=9.0, help="Max allowed outer halo foliage spill %% (default 9.0)")
    sp_aud_img.add_argument("--out-json", default="", help="Optional output JSON report path (defaults to qa/image_cutout_audit.json)")
    sp_aud_img.set_defaults(func=cmd_audit_images)

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
