import ast
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from PIL import Image, ImageDraw

from flow_sku_tvc_toolkit.cli import main as cli_main
from flow_sku_tvc_toolkit.guardrails import (
    validate_image_prompt,
    validate_sku_config,
    validate_video_prompt,
)
from flow_sku_tvc_toolkit.plate_engine import (
     PlacementSpec,
    build_sku_plates_from_image,
    extract_clean_white_cutout,
    render_plate_2k,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestPlateEngineAndWhiteCutout(unittest.TestCase):
    def test_border_flood_whitens_studio_grey_and_preserves_internal_white_crochet(self):
        # Outer background is slightly off-white studio grey (246, 246, 248)
        im = Image.new("RGB", (300, 300), (246, 246, 248))
        draw = ImageDraw.Draw(im)
        # Colored crochet yarn border ring enclosing pure white & cream center petals
        draw.ellipse((70, 70, 230, 230), fill=(185, 92, 65))
        draw.ellipse((100, 100, 200, 200), fill=(255, 255, 255))
        draw.ellipse((125, 125, 175, 175), fill=(250, 246, 236))

        crop, bbox, stats = extract_clean_white_cutout(im, pad_px=4)
        # Tight bbox must wrap (70..231)
        self.assertEqual(stats["tight_bbox"], [70, 70, 231, 231])
        # Corner of padded crop was studio grey (246,246,248) -> must now be exact pure #FFFFFF
        self.assertEqual(crop.getpixel((0, 0)), (255, 255, 255))
        # Center of crop corresponds to enclosed cream/white petals -> must remain untouched!
        cx, cy = crop.width // 2, crop.height // 2
        self.assertEqual(crop.getpixel((cx, cy)), (250, 246, 236))
        self.assertEqual(crop.getpixel((cx, cy - 32)), (255, 255, 255))

    def test_transparent_rgba_white_crochet_bunny_preserves_outer_white_body(self):
        # Regression test: opaque white/ivory crochet amigurumi on transparent PNG must NOT be eaten to its dark eyes
        im = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse((90, 60, 210, 250), fill=(252, 250, 246, 255))
        d.ellipse((130, 110, 140, 120), fill=(35, 30, 28, 255))
        d.ellipse((160, 110, 170, 120), fill=(35, 30, 28, 255))

        crop, _bbox, stats = extract_clean_white_cutout(im, pad_px=4)
        self.assertTrue(stats["had_alpha"])
        self.assertEqual(stats["tight_bbox"], [90, 60, 211, 251])
        self.assertEqual(crop.getpixel((0, 0)), (255, 255, 255))
        # Mid-body ivory yarn pixel must remain intact (252, 250, 246), not erased to (255, 255, 255)
        self.assertEqual(crop.getpixel((crop.width // 2, crop.height - 30)), (252, 250, 246))

    def test_rgb_ivory_crochet_daisy_on_studio_white_preserves_outer_cream_petals(self):
        # Regression test: unenclosed ivory/cream crochet petals touching studio white (#FCFCFC) must NOT be amputated
        im = Image.new("RGB", (400, 400), (252, 252, 252))
        d = ImageDraw.Draw(im)
        for box in ((140, 50, 260, 190), (140, 210, 260, 350), (50, 140, 190, 260), (210, 140, 350, 260)):
            d.ellipse(box, fill=(248, 245, 241))
        d.ellipse((150, 150, 250, 250), fill=(225, 175, 45))

        crop, _bbox, stats = extract_clean_white_cutout(im, pad_px=4)
        self.assertEqual(stats["tight_bbox"], [50, 50, 351, 351])
        self.assertEqual(crop.getpixel((0, 0)), (255, 255, 255))
        # Top petal pixel at original (200, 90) -> inside padded crop at (200 - 46, 90 - 46) = (154, 44)
        self.assertEqual(crop.getpixel((154, 44)), (248, 245, 241))

    def test_exif_orientation_6_phone_photo_is_transposed_upright(self):
        # Raw stored dimensions are landscape 320x200 with a horizontal bar (40..280, 70..130),
        # tagged with EXIF Orientation=6 (90 deg CW) so upright view is tall portrait (W=61, H=241).
        raw = Image.new("RGB", (320, 200), (255, 255, 255))
        d = ImageDraw.Draw(raw)
        d.rectangle((40, 70, 280, 130), fill=(60, 130, 80))
        exif = raw.getexif()
        exif[0x0112] = 6  # Orientation: Rotate 90 CW

        with tempfile.TemporaryDirectory() as tmp:
            src_jpg = os.path.join(tmp, "phone_exif6.jpg")
            raw.save(src_jpg, "JPEG", quality=98, exif=exif.tobytes())
            manifest = build_sku_plates_from_image(
                input_path=src_jpg,
                out_dir=os.path.join(tmp, "out"),
                prefix="EXIFTEST",
                preset_name="crochet_decor",
            )
            # Upright cutout must be tall (aspect W/H < 0.40), NOT sideways (> 2.5)!
            self.assertLess(manifest["cutout_stats"]["aspect_ratio_w_over_h"], 0.40)

    def test_transparent_rgba_png_cutout(self):
        im = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.rectangle((60, 40, 179, 199), fill=(48, 120, 72, 255))

        crop, _bbox, stats = extract_clean_white_cutout(im, pad_px=2)
        self.assertTrue(stats["had_alpha"])
        self.assertEqual(stats["tight_bbox"], [60, 40, 180, 200])
        self.assertEqual(crop.getpixel((0, 0)), (255, 255, 255))

    def test_blank_and_tiny_images_raise_value_error(self):
        blank = Image.new("RGB", (128, 128), (255, 255, 255))
        with self.assertRaisesRegex(ValueError, "completely blank/white"):
            extract_clean_white_cutout(blank)

        tiny = Image.new("RGB", (8, 8), (255, 255, 255))
        with self.assertRaisesRegex(ValueError, "too small"):
            extract_clean_white_cutout(tiny)

    def test_nonwhite_raw_desk_photo_rejected_with_isolate_white_guidance(self):
        raw_crochet = os.path.join(
            REPO_ROOT,
            "flow_web_intro",
            "clean_product_refs",
            "PROD2_STYLE_B_ROSE_FLAT_ISOLATED.jpg",
        )
        self.assertTrue(os.path.isfile(raw_crochet))
        with Image.open(raw_crochet) as im:
            with self.assertRaisesRegex(ValueError, "isolate-white"):
                extract_clean_white_cutout(im)

    def test_real_barrel_tree_generates_9_2k_plates_and_macro_zero_distortion(self):
        real_barrel = os.path.join(
            REPO_ROOT,
            "barrel_cedar_20",
            "clean_refs",
            "BARREL_REF_1_SINGLE_CLEAN.jpg",
        )
        self.assertTrue(os.path.isfile(real_barrel))
        with tempfile.TemporaryDirectory() as tmp:
            manifest = build_sku_plates_from_image(
                input_path=real_barrel,
                out_dir=tmp,
                prefix="TESTBARREL",
                preset_name="tree_4ft",
            )
            self.assertEqual(len(manifest["clean_refs"]), 2)
            self.assertEqual(len(manifest["plates_2k"]), 9)

            for rname in manifest["clean_refs"]:
                rpath = os.path.join(tmp, "clean_refs", rname)
                with Image.open(rpath) as rim:
                    self.assertEqual(rim.size, (1024, 1024))

            for pt in manifest["plates_2k"]:
                ppath = os.path.join(tmp, "plates_2k", pt["filename"])
                with Image.open(ppath) as pim:
                    self.assertEqual(pim.size, (2560, 1440))
                    # Verify pure white outer corners
                    for corner in ((0, 0), (2559, 0), (0, 1439), (2559, 1439)):
                        px = pim.getpixel(corner)
                        self.assertTrue(all(c >= 253 for c in px), f"Non-white corner {px} in {pt['filename']}")

    def test_wide_flat_crochet_coaster_respects_max_width_cap_and_aspect_lock(self):
        # Wide flat coaster cutout: W=500, H=200 (ratio 2.50)
        coaster = Image.new("RGB", (500, 200), (195, 70, 90))
        spec = PlacementSpec(height_pct=0.52, center_x_pct=0.50, bottom_margin_pct=0.15, max_width_pct=0.38)
        plate = render_plate_2k(coaster, [spec], canvas_w=2560, canvas_h=1440)
        self.assertEqual(plate.size, (2560, 1440))

        # Find bounding box of non-white pixels on rendered plate
        _, _bbox, stats = extract_clean_white_cutout(plate, pad_px=0)
        rw = stats["tight_bbox"][2] - stats["tight_bbox"][0]
        rh = stats["tight_bbox"][3] - stats["tight_bbox"][1]
        # Must be capped at 2560 * 0.38 = 973px width, height = round(973 / 2.5) = 389px
        self.assertLessEqual(rw, round(2560 * 0.38) + 1)
        self.assertAlmostEqual(rw / float(rh), 2.5, delta=0.02)

    def test_twin_pair_listing_photo_auto_isolates_single_unit_without_splitting_unequal_sets(self):
        pair_photo = os.path.join(
            REPO_ROOT,
            "cedar_4ft_10s",
            "clean_refs",
            "CEDAR_REF_2_PAIR_4FT_CLEAN.jpg",
        )
        self.assertTrue(os.path.isfile(pair_photo))
        with Image.open(pair_photo) as im:
            crop, _bbox, stats = extract_clean_white_cutout(im)
        self.assertEqual(stats["auto_split_twin_pack_count"], 2)
        self.assertAlmostEqual(stats["aspect_ratio_w_over_h"], 0.408, delta=0.03)
        self.assertEqual(crop.getpixel((crop.width - 1, crop.height // 2)), (255, 255, 255))

        # Unequal multi-piece set (large teapot + small cup separated by white corridor) must NOT split
        unequal = Image.new("RGB", (500, 360), (255, 255, 255))
        d = ImageDraw.Draw(unequal)
        d.rectangle((50, 60, 230, 300), fill=(150, 95, 70))
        d.rectangle((300, 190, 410, 300), fill=(70, 120, 155))
        _c2, _b2, stats2 = extract_clean_white_cutout(unequal)
        self.assertEqual(stats2["auto_split_twin_pack_count"], 1)
        self.assertEqual(stats2["tight_bbox"], [50, 60, 411, 301])

        # Twin pair with sparse touching leaf sprigs (3px green bridge across middle corridor) MUST still isolate 1 unit
        with Image.open(pair_photo) as im_touch:
            touching = im_touch.convert("RGB")
        dt = ImageDraw.Draw(touching)
        dt.rectangle((490, 520, 540, 523), fill=(48, 92, 40))
        crop_touch, _bt, stats_touch = extract_clean_white_cutout(touching)
        self.assertEqual(stats_touch["auto_split_twin_pack_count"], 2)
        self.assertAlmostEqual(stats_touch["aspect_ratio_w_over_h"], 0.408, delta=0.03)
        self.assertEqual(crop_touch.getpixel((crop_touch.width - 1, 521)), (255, 255, 255))

        # Hollow rectangular picture frame / ring must NEVER split in half
        frame = Image.new("RGB", (400, 500), (255, 255, 255))
        df = ImageDraw.Draw(frame)
        df.rectangle((60, 50, 340, 450), outline=(45, 45, 45), width=22)
        _cf, _bf, stats_frame = extract_clean_white_cutout(frame)
        self.assertEqual(stats_frame["auto_split_twin_pack_count"], 1)
        self.assertEqual(stats_frame["tight_bbox"], [60, 50, 341, 451])

        # Explicit opt-out (auto_split_twin_pair=False) keeps genuine 2-piece pair SKUs together
        with Image.open(pair_photo) as im_keep:
            _ck, _bk, stats_keep = extract_clean_white_cutout(im_keep, auto_split_twin_pair=False)
        self.assertEqual(stats_keep["auto_split_twin_pack_count"], 1)
        self.assertGreater(stats_keep["aspect_ratio_w_over_h"], 0.75)


class TestPromptGuardrailsAndCLI(unittest.TestCase):
    def test_guardrails_block_forbidden_words_and_allow_safe_substrings(self):
        # Safe words containing 'rig' or 'pine' substrings ('truck-right', 'bright', 'upright', 'alpine')
        clean_veo = (
            "Continuous, clearly visible 4-second 85mm lateral camera truck-right across the bright oak table "
            "past the upright ceramic mug while preserving handcrafted milk-cotton crochet yarn stitches."
        )
        self.assertEqual(validate_video_prompt(clean_veo, preset_name="crochet_decor"), [])

        # Forbidden camera equipment & freeze words
        bad_veo = "Smooth 4s slider and camera rig shot, plant stays 100% still and motionless (5% push)."
        errs_veo = validate_video_prompt(bad_veo, preset_name="tree_4ft")
        self.assertGreaterEqual(len(errs_veo), 4)

        # Forbidden tree words
        self.assertTrue(validate_image_prompt("A green cedar pine topiary in pot", preset_name="tree_4ft"))

        # Forbidden crochet words ('knitted' turns crochet loops into sweater knit ribs!)
        self.assertTrue(validate_image_prompt("A cute knitted felt flower pot CGI", preset_name="crochet_decor"))
        self.assertEqual(
            validate_image_prompt(
                "Handcrafted tight milk-cotton crochet yarn stitches on warm oak table",
                preset_name="crochet_decor",
            ),
            [],
        )

    def test_guardrails_reject_video_missing_both_scene_key_and_uuid(self):
        bad_cfg = {
            "slug": "test_vid",
            "prefix": "TVID",
            "preset": "crochet_decor",
            "project_id": "dfcf77a5-5374-4678-9f80-1c5ea7b5c305",
            "scenes": [],
            "videos": [
                {
                    "key": "V01_ORPHAN",
                    "prompt": "Continuous 4-second 85mm lateral camera truck-right across warm oak table.",
                }
            ],
        }
        errs = validate_sku_config(bad_cfg)
        self.assertTrue(any("must specify either 'scene_key' or explicit 'uuid'" in e for e in errs), errs)

        bad_cfg2 = dict(bad_cfg)
        bad_cfg2["videos"] = [
            {
                "key": "V01_DANGLING_SCENE",
                "scene_key": "NON_EXISTENT_SCENE",
                "prompt": "Continuous 4-second 85mm lateral camera truck-right across warm oak table.",
            }
        ]
        errs2 = validate_sku_config(bad_cfg2)
        self.assertTrue(any("unknown scene_key" in e for e in errs2), errs2)

    def test_guardrails_validate_video_card_indices_and_cli_no_split_flag(self):
        cfg = {
            "slug": "test_order",
            "prefix": "TORD",
            "preset": "tree_4ft",
            "project_id": "dfcf77a5-5374-4678-9f80-1c5ea7b5c305",
            "scenes": [],
            "videos": [
                {"key": "V01", "uuid": "11111111-1111-1111-1111-111111111111", "prompt": "Continuous 4-second lateral camera truck-right."},
                {"key": "V02", "uuid": "22222222-2222-2222-2222-222222222222", "prompt": "Continuous 4-second lateral camera truck-left."},
            ],
            "video_card_indices": [
                {"card_index": 0, "slug": "01_V01"},
                {"card_index": 0, "slug": "02_V02"},
            ],
        }
        errs = validate_sku_config(cfg)
        self.assertTrue(any("Duplicate card_index 0" in e for e in errs), errs)

        cfg["video_card_indices"] = [
            {"card_index": 1, "slug": "01_V01"},
            {"card_index": 0, "slug": "02_V02"},
        ]
        self.assertEqual(validate_sku_config(cfg), [])

        pair_photo = os.path.join(REPO_ROOT, "cedar_4ft_10s", "clean_refs", "CEDAR_REF_2_PAIR_4FT_CLEAN.jpg")
        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = cli_main([
                    "build-plates",
                    "--input", pair_photo,
                    "--out-dir", tmp,
                    "--prefix", "KEEPPAIR",
                    "--preset", "tree_4ft",
                    "--no-split-twin-pair",
                ])
            self.assertEqual(rc, 0)
            with open(os.path.join(tmp, "plate_manifest.json"), "r", encoding="utf-8") as f:
                mf = json.load(f)
            self.assertEqual(mf["cutout_stats"]["auto_split_twin_pack_count"], 1)

    def test_crochet_sample_config_and_cli_workflow(self):
        sample_cfg = os.path.join(
            REPO_ROOT,
            "flow_sku_tvc_toolkit",
            "examples",
            "crochet_sunflower_pot_sample.json",
        )
        with open(sample_cfg, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(validate_sku_config(data), [])

        with tempfile.TemporaryDirectory() as tmp:
            # Create synthetic white-bg crochet source image
            src_img = os.path.join(tmp, "crochet_src.png")
            im = Image.new("RGB", (600, 600), (255, 255, 255))
            d = ImageDraw.Draw(im)
            d.rectangle((220, 320, 380, 500), fill=(175, 125, 85))  # pot
            d.ellipse((190, 120, 410, 340), fill=(235, 180, 40))    # sunflower
            im.save(src_img)

            sku_dir = os.path.join(tmp, "crochet_test_sku")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc0 = cli_main(["list-presets"])
                rc1 = cli_main([
                    "init-sku",
                    "--slug", "crochet_test_sku",
                    "--prefix", "CTEST",
                    "--preset", "crochet_decor",
                    "--project-id", "dfcf77a5-5374-4678-9f80-1c5ea7b5c305",
                    "--out-dir", sku_dir,
                ])
                cfg_path = os.path.join(sku_dir, "sku_project.json")
                rc2 = cli_main([
                    "build-plates",
                    "--input", src_img,
                    "--config", cfg_path,
                ])
                rc3 = cli_main([
                    "validate",
                    "--config", cfg_path,
                    "--check-files",
                ])
            self.assertEqual((rc0, rc1, rc2, rc3), (0, 0, 0, 0))
            self.assertTrue(os.path.isfile(os.path.join(sku_dir, "plate_manifest.json")))


class TestRepoPortabilityAndSilentCDPInvariants(unittest.TestCase):
    def test_flow_cdp_token_bridging_vietnamese_picker_regex_and_zero_import_side_effects(self):
        from flow_sku_tvc_toolkit.cli import build_parser
        from flow_sku_tvc_toolkit.flow_cdp import UPLOADED_EXT_RE, _token_matches_set

        # Verify importing flow_cdp does NOT create stray flow_web_intro/videos/dl_1080p directory
        stray_dir = os.path.join(REPO_ROOT, "flow_web_intro", "videos", "dl_1080p")
        self.assertFalse(os.path.exists(stray_dir), f"Import side-effect created {stray_dir}")

        # Verify Vietnamese Flow picker text ('<filename>.jpg Hình ảnh') is caught as an uploaded asset
        self.assertIsNotNone(UPLOADED_EXT_RE.search("image raw_crochet_desk.jpg Hình ảnh"))
        self.assertIsNotNone(UPLOADED_EXT_RE.search("BARREL_PLATE_04_SINGLE_HERO_LEFT_72PCT_16x9.png Hình ảnh"))
        self.assertIsNotNone(UPLOADED_EXT_RE.search("photo_clean.webp Hình ảnh"))
        self.assertIsNone(
            UPLOADED_EXT_RE.search("image Replace only the solid pure white background with an 85mm tabletop Hình ảnh")
        )

        # Verify 174-char /asb/ picker tokens match both 48-char cached plate tokens AND bridged 36-char UUIDs
        full_asb = (
            "ANqvLOZwEKmhz6Fx4Z50wc-xGqWYxQ9l9JWDZ6N2yShv5n37F19-3e7s7-m22-3N6G7B_yO4f6D052"
            "e1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        )
        short_48 = full_asb[:48]
        perm_uuid = "8c5ae9c1-5afd-4a59-ac02-fe88e604d098"
        self.assertTrue(_token_matches_set(full_asb, {short_48}))
        self.assertTrue(_token_matches_set(full_asb, {perm_uuid}, asb_to_uuid={short_48: perm_uuid}))
        self.assertFalse(_token_matches_set(full_asb, {"deadbeef-0000-4000-8000-000000000000"}, asb_to_uuid={short_48: perm_uuid}))

        # Verify CLI map-uuids supports --only-key and --force-remap
        parsed = build_parser().parse_args(["map-uuids", "--config", "sku_project.json", "--only-key", "B16", "--force-remap"])
        self.assertEqual(parsed.only_key, "B16")
        self.assertTrue(parsed.force_remap)

        # Verify _decode_and_normalize_flow_image_bytes handles WebP + RGBA PNG bytes and rejects tiny error payloads
        from flow_sku_tvc_toolkit.flow_cdp import _decode_and_normalize_flow_image_bytes

        webp_buf = io.BytesIO()
        Image.new("RGBA", (512, 512), (245, 210, 120, 255)).save(webp_buf, "WEBP")
        norm_rgb = _decode_and_normalize_flow_image_bytes(webp_buf.getvalue())
        self.assertEqual(norm_rgb.mode, "RGB")
        self.assertEqual(norm_rgb.size, (512, 512))

        tiny_buf = io.BytesIO()
        Image.new("RGB", (64, 64), (255, 255, 255)).save(tiny_buf, "JPEG")
        with self.assertRaisesRegex(RuntimeError, "too small"):
            _decode_and_normalize_flow_image_bytes(tiny_buf.getvalue())

    def test_no_bring_to_front_and_no_hardcoded_user_paths_in_packaged_python(self):
        target_files = [
            os.path.join(REPO_ROOT, "flow_sku_tvc_toolkit", "__init__.py"),
            os.path.join(REPO_ROOT, "flow_sku_tvc_toolkit", "presets.py"),
            os.path.join(REPO_ROOT, "flow_sku_tvc_toolkit", "plate_engine.py"),
            os.path.join(REPO_ROOT, "flow_sku_tvc_toolkit", "guardrails.py"),
            os.path.join(REPO_ROOT, "flow_sku_tvc_toolkit", "flow_cdp.py"),
            os.path.join(REPO_ROOT, "flow_sku_tvc_toolkit", "cli.py"),
            os.path.join(REPO_ROOT, "barrel_cedar_20", "run_barrel20_images_silent.py"),
            os.path.join(REPO_ROOT, "barrel_cedar_20", "map_barrel20_uuids.py"),
            os.path.join(REPO_ROOT, "barrel_cedar_20", "run_barrel20_veo4s_silent.py"),
            os.path.join(REPO_ROOT, "barrel_cedar_20", "download_and_merge_atf_9422_1080p.py"),
            os.path.join(REPO_ROOT, "cedar_4ft_10s", "run_batch10_silent_flow.py"),
            os.path.join(REPO_ROOT, "cedar_4ft_10s", "run_batch10_veo4s_silent.py"),
        ]
        for fpath in target_files:
            self.assertTrue(os.path.isfile(fpath), f"Missing {fpath}")
            with open(fpath, "r", encoding="utf-8") as f:
                src = f.read()
            # Must parse cleanly as valid Python AST
            tree = ast.parse(src, filename=fpath)
            self.assertNotIn("/Users/dudumac5", src, f"Hardcoded user path in {fpath}")

            # Ensure Page.bringToFront is NEVER invoked in any string literal argument to call()
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    self.assertNotEqual(
                        node.value.strip(),
                        "Page.bringToFront",
                        f"Forbidden Page.bringToFront call found in {fpath}",
                    )

    def test_checked_in_product_configs_and_uuid_maps_are_valid(self):
        batch3_dir = os.path.join(REPO_ROOT, "products", "cedar_sqpot_batch3_20")
        cfg_path = os.path.join(batch3_dir, "sku_project.json")
        uuid_path = os.path.join(batch3_dir, "cedar_sqpot_batch3_20_scene_uuids.json")
        self.assertTrue(os.path.isfile(cfg_path))
        self.assertTrue(os.path.isfile(uuid_path))

        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        with open(uuid_path, "r", encoding="utf-8") as f:
            uuid_map = json.load(f)

        self.assertEqual(validate_sku_config(cfg, project_dir=batch3_dir, require_local_plates=False), [])
        self.assertEqual(len(cfg["scenes"]), 20)
        self.assertEqual(len(cfg["videos"]), 20)
        self.assertEqual(len(uuid_map), 20)
        self.assertEqual(len(set(uuid_map.values())), 20)

        excluded = set(cfg.get("exclude_uuids", []))
        for sc in cfg["scenes"]:
            uid = uuid_map.get(sc["key"], "")
            self.assertRegex(uid, r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
            self.assertNotIn(uid, excluded)


if __name__ == "__main__":
    unittest.main()

