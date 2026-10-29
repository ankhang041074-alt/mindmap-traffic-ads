import glob
import os
import shutil
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_OFFICE_BRAIN = "/Users/dudumac5/.gemini/antigravity/brain/b5518d8f-8b2d-4488-85b7-420814826233"
BRAIN_DIR = _OFFICE_BRAIN if os.path.isdir(_OFFICE_BRAIN) else os.path.join(_BASE_DIR, "contact_sheets")
os.makedirs(BRAIN_DIR, exist_ok=True)
FFMPEG_BIN = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"


def build_2fps_contact_sheet(mp4_path, out_jpg, cols=4):
    with tempfile.TemporaryDirectory() as tmpdir:
        pattern = os.path.join(tmpdir, "f_%03d.jpg")
        subprocess.run(
            [FFMPEG_BIN, "-y", "-i", mp4_path, "-vf", "fps=2,scale=512:-1", "-q:v", "2", pattern],
            check=True, capture_output=True
        )
        frame_files = sorted(glob.glob(os.path.join(tmpdir, "f_*.jpg")))
        if not frame_files:
            raise RuntimeError(f"No frames extracted from {mp4_path}")

        imgs = [Image.open(f).convert("RGB") for f in frame_files]
        fw, fh = imgs[0].size
        rows = (len(imgs) + cols - 1) // cols
        pad = 8
        header_h = 34
        canvas_w = cols * fw + (cols + 1) * pad
        canvas_h = header_h + rows * fh + (rows + 1) * pad
        canvas = Image.new("RGB", (canvas_w, canvas_h), (18, 18, 22))
        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        except Exception:
            font = ImageFont.load_default()

        title = f"2fps (0.5s) Forensic Audit: {os.path.basename(mp4_path)} ({len(imgs)} frames)"
        draw.text((pad, 8), title, fill=(255, 230, 120), font=font)

        for idx, im in enumerate(imgs):
            r = idx // cols
            c = idx % cols
            x = pad + c * (fw + pad)
            y = header_h + pad + r * (fh + pad)
            canvas.paste(im, (x, y))
            t_sec = idx * 0.5
            label = f"{t_sec:.1f}s (f{idx+1})"
            draw.rectangle([x + 6, y + 6, x + 118, y + 32], fill=(0, 0, 0))
            draw.text((x + 12, y + 9), label, fill=(255, 255, 255), font=font)

        canvas.save(out_jpg, quality=92)
        print(f"Saved 2fps contact sheet ({len(imgs)} frames): {out_jpg}")


if __name__ == "__main__":
    mp4 = sys.argv[1] if len(sys.argv) > 1 else "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro/videos/shot1_v1.mp4"
    out_local = mp4.replace(".mp4", "_contact_2fps.jpg")
    build_2fps_contact_sheet(mp4, out_local)
    brain_copy = os.path.join(BRAIN_DIR, f"flow_16x9_{os.path.basename(out_local)}")
    shutil.copy2(out_local, brain_copy)
    print("Copied to brain dir:", brain_copy)
