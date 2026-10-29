import json
import os
import re
import subprocess
import wave
import numpy as np

from assemble_web_intros import DELIV_DIR, ffprobe_full
from contact_sheet import BRAIN_DIR


def check_audio_levels(mp4_path):
    res = subprocess.run(
        [( __import__("shutil").which("ffmpeg") or "/opt/homebrew/bin/ffmpeg" ), "-i", mp4_path, "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True
    )
    mean_m = re.search(r"mean_volume:\s*([-\d.]+)\s*dB", res.stderr)
    max_m = re.search(r"max_volume:\s*([-\d.]+)\s*dB", res.stderr)
    return (
        float(mean_m.group(1)) if mean_m else None,
        float(max_m.group(1)) if max_m else None,
    )


def check_windowed_rms_continuity(mp4_path, win_sec=0.25):
    tmp_wav = "/tmp/_verify_master_audio.wav"
    subprocess.run(
        [( __import__("shutil").which("ffmpeg") or "/opt/homebrew/bin/ffmpeg" ), "-y", "-i", mp4_path, "-vn", "-ac", "1", "-ar", "48000", tmp_wav],
        capture_output=True, check=True
    )
    with wave.open(tmp_wav, "rb") as wf:
        sr = wf.getframerate()
        n = wf.getnframes()
        samples = np.frombuffer(wf.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    step = int(sr * win_sec)
    # Exclude the first/last 0.15s master fade-in/out ramps when checking mid-video dropout floor
    inner = samples[int(sr * 0.15): max(int(sr * 0.30), len(samples) - int(sr * 0.22))]
    rms_dbs = []
    for start in range(0, len(inner) - step + 1, step):
        chunk = inner[start:start + step]
        rms = float(np.sqrt(np.mean(chunk * chunk)) + 1e-12)
        rms_dbs.append(round(20.0 * np.log10(rms), 1))
    peak_db = round(20.0 * np.log10(float(np.max(np.abs(samples))) + 1e-12), 2)
    return min(rms_dbs), max(rms_dbs), peak_db


def main():
    manifest_path = os.path.join(DELIV_DIR, "deliverables_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print("=== 1. Native Google Flow 1080p Source Audit (6/6 Clips) ===")
    for k, src in manifest["sources"].items():
        assert src["native_flow_1080p"] is True, f"{k} is NOT native Flow 1080p!"
        assert int(src["width"]) == 1920 and int(src["height"]) == 1080, f"{k} bad resolution!"
        print(f"  [PASS] {k}: {src['width']}x{src['height']} native_flow_1080p=True ({os.path.basename(src['video_src'])})")

    print("\n=== 2. Full Stream + Windowed Audio Continuity + Brain Sync Audit Across All 8 MP4 Deliverables ===")
    mp4_files = sorted(f for f in os.listdir(DELIV_DIR) if f.endswith(".mp4"))
    assert len(mp4_files) == 8, f"Expected 8 MP4 deliverables, found {len(mp4_files)}: {mp4_files}"

    for fname in mp4_files:
        p = os.path.join(DELIV_DIR, fname)
        bp = os.path.join(BRAIN_DIR, fname)
        assert os.path.exists(bp) and os.path.getsize(bp) == os.path.getsize(p), f"Brain copy mismatch for {fname}"

        info = ffprobe_full(p)
        vs = next(s for s in info["streams"] if s["codec_type"] == "video")
        a_streams = [s for s in info["streams"] if s["codec_type"] == "audio"]
        dur = float(info["format"]["duration"])
        sz = int(info["format"]["size"])
        assert int(vs["width"]) == 1920 and int(vs["height"]) == 1080, f"Resolution mismatch in {fname}"
        assert vs["pix_fmt"] == "yuv420p" and vs["r_frame_rate"] == "30/1", f"Format mismatch in {fname}"

        if fname.endswith("_MUTED.mp4"):
            assert len(a_streams) == 0, f"Muted file {fname} unexpectedly has audio stream!"
            aud_str = "muted (-an, 0 audio streams)"
        else:
            assert len(a_streams) == 1, f"Audio master {fname} missing audio stream!"
            mean_db, max_db = check_audio_levels(p)
            min_win_rms, max_win_rms, peak_db = check_windowed_rms_continuity(p)
            assert min_win_rms > -65.0, f"Audio dropout detected in {fname}: min 0.25s RMS = {min_win_rms} dBFS"
            assert peak_db <= -1.0, f"Audio peak too hot in {fname}: peak = {peak_db} dBFS"
            sheet_name = fname.replace(".mp4", "_contact_2fps.jpg")
            assert os.path.exists(os.path.join(DELIV_DIR, sheet_name)), f"Missing contact sheet {sheet_name}"
            assert os.path.exists(os.path.join(BRAIN_DIR, sheet_name)), f"Missing brain contact sheet {sheet_name}"
            aud_str = (
                f"aac {a_streams[0].get('sample_rate')}Hz ch={a_streams[0].get('channels')} "
                f"mean={mean_db}dB max={max_db}dB | 0.25s_rms=[{min_win_rms}, {max_win_rms}]dBFS"
            )
        print(
            f"  [PASS] {fname}: {vs['width']}x{vs['height']} {vs['codec_name']} {vs['pix_fmt']} "
            f"fps={vs['r_frame_rate']} dur={dur:.2f}s size={sz:,}B | {aud_str}"
        )

    print("\nALL 8 MP4 DELIVERABLES + 4 CONTACT SHEETS + 6/6 NATIVE 1080P SOURCES PASSED DEEP VERIFICATION!")


if __name__ == "__main__":
    main()

