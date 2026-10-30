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
        _, bbox, stats = extract_clean_white_cutout(plate, pad_px=0)
        rw = stats["tight_bbox"][2] - stats["tight_bbox"][0]
        rh = stats["tight_bbox"][3] - stats["tight_bbox"][1]
        # Must be capped at 2560 * 0.38 = 973px width, height = round(973 / 2.5) = 389px
        self.assertLessEqual(rw, round(2560 * 0.38) + 1)
        self.assertAlmostEqual(rw / float(rh), 2.5, delta=0.02)


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


if __name__ == "__main__":
    unittest.main()
