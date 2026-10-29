import glob
import json
import os
import shutil
import subprocess
import tempfile

from contact_sheet import BRAIN_DIR, build_2fps_contact_sheet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
HD_DIR = os.path.join(VIDEOS_DIR, "hd_1080p")
DELIV_DIR = os.path.join(BASE_DIR, "deliverables")
os.makedirs(DELIV_DIR, exist_ok=True)
FFPROBE_BIN = shutil.which("ffprobe") or FFPROBE_BIN
FFMPEG_BIN = shutil.which("ffmpeg") or FFMPEG_BIN


def ffprobe_full(path):
    res = subprocess.run(
        [FFPROBE_BIN, "-v", "error",
         "-show_entries", "format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate,pix_fmt,channels,sample_rate",
         "-of", "json", path],
        capture_output=True, text=True, check=True
    )
    return json.loads(res.stdout)


def has_audio_stream(path):
    info = ffprobe_full(path)
    return any(s.get("codec_type") == "audio" for s in info.get("streams", []))


def pick_best_source(clip_key):
    """Prefer native Google Flow 1080p AI upscale if available and valid, else 720p original."""
    hd_path = os.path.join(HD_DIR, f"{clip_key}_1080p.mp4")
    sd_path = os.path.join(VIDEOS_DIR, f"{clip_key}.mp4")
    if os.path.exists(hd_path) and os.path.getsize(hd_path) > 500_000:
        info = ffprobe_full(hd_path)
        v_streams = [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
        if v_streams and int(v_streams[0]["width"]) == 1920:
            return hd_path, sd_path, True
    return sd_path, sd_path, False


def prepare_normalized_segment(video_src, audio_src, start_s, end_s, out_seg_path):
    """
    Trim [start_s, end_s] and standardize to:
      - Video: 1920x1080 (native Flow 1080p; Lanczos fallback if needed), 30fps, yuv420p, SAR 1:1, libx264 CRF 15
      - Audio: 48kHz stereo AAC with sub-bass rumble filter (110Hz-12kHz), gentle 4:1 foley leveling,
               -9 dBFS peak ceiling (eliminates +1.8 dB / -1.5 dB glass spikes), and 60ms/80ms smooth edge fades
    """
    dur = round(end_s - start_s, 3)
    fade_out_st = max(0.0, round(dur - 0.08, 3))

    vf = "scale=1920:1080:flags=lanczos,setsar=1,fps=30,format=yuv420p"
    af = (
        "aresample=48000,"
        "aformat=sample_fmts=fltp:channel_layouts=stereo,"
        "highpass=f=110,"
        "lowpass=f=12000,"
        "acompressor=threshold=-20dB:ratio=4:attack=5:release=60,"
        "alimiter=limit=0.35:level=false,"
        f"afade=t=in:st=0:d=0.06,afade=t=out:st={fade_out_st}:d=0.08"
    )

    if has_audio_stream(video_src):
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", f"{start_s:.3f}", "-t", f"{dur:.3f}", "-i", video_src,
            "-vf", vf, "-af", af,
            "-c:v", "libx264", "-preset", "slow", "-crf", "15",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            out_seg_path
        ]
    elif has_audio_stream(audio_src):
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", f"{start_s:.3f}", "-t", f"{dur:.3f}", "-i", video_src,
            "-ss", f"{start_s:.3f}", "-t", f"{dur:.3f}", "-i", audio_src,
            "-map", "0:v:0", "-map", "1:a:0",
            "-vf", vf, "-af", af,
            "-c:v", "libx264", "-preset", "slow", "-crf", "15",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            out_seg_path
        ]
    else:
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", f"{start_s:.3f}", "-t", f"{dur:.3f}", "-i", video_src,
            "-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-map", "0:v:0", "-map", "1:a:0",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "slow", "-crf", "15",
            "-c:a", "aac", "-b:a", "192k", "-shortest",
            out_seg_path
        ]
    subprocess.run(cmd, check=True, capture_output=True)


def concat_segments_to_master(segments_spec, out_mp4, also_muted_mp4=None):
    """
    segments_spec: list of (clip_key, start_s, end_s)
    Concatenates normalized segments and layers a continuous warm -53 dBFS room-ambience bed
    underneath so Veo's mid-clip -120 dBFS digital audio truncations never produce dead vacuum dropouts.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        seg_files = []
        for idx, (clip_key, s_t, e_t) in enumerate(segments_spec):
            v_src, a_src, _ = pick_best_source(clip_key)
            seg_path = os.path.join(tmpdir, f"seg_{idx:02d}.mp4")
            prepare_normalized_segment(v_src, a_src, s_t, e_t, seg_path)
            seg_files.append(seg_path)

        n = len(seg_files)
        inputs = []
        filter_parts = []
        for idx, sf in enumerate(seg_files):
            inputs.extend(["-i", sf])
            filter_parts.append(f"[{idx}:v:0][{idx}:a:0]")

        total_dur = round(sum(e_t - s_t for _, s_t, e_t in segments_spec), 3)
        inputs.extend([
            "-f", "lavfi",
            "-i", f"anoisesrc=c=pink:r=48000:a=0.025:d={total_dur:.3f}",
        ])
        bed_idx = n
        master_fade_out = max(0.0, round(total_dur - 0.20, 3))
        filter_complex = (
            "".join(filter_parts)
            + f"concat=n={n}:v=1:a=1[vcat][acat];"
            + f"[{bed_idx}:a:0]highpass=f=120,lowpass=f=4200,"
            + "aformat=sample_fmts=fltp:channel_layouts=stereo[abed];"
            + "[acat][abed]amix=inputs=2:duration=first:dropout_transition=0:weights=1 1:normalize=0,"
            + "alimiter=limit=0.38:level=false,"
            + f"afade=t=in:st=0:d=0.12,afade=t=out:st={master_fade_out}:d=0.20[aout]"
        )

        cmd = [
            FFMPEG_BIN, "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "[vcat]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "slow", "-crf", "15",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            out_mp4
        ]
        subprocess.run(cmd, check=True, capture_output=True)

        if also_muted_mp4:
            subprocess.run(
                [FFMPEG_BIN, "-y", "-i", out_mp4, "-c:v", "copy", "-an", "-movflags", "+faststart", also_muted_mp4],
                check=True, capture_output=True
            )


def main():
    print("=== Checking Best Sources (Native Flow 1080p vs 720p) ===")
    source_report = {}
    clip_keys = ["shot1_v2", "shot2_v1", "shot3_v1", "shot4_v2", "shot5_v1", "shot6_v1"]
    for k in clip_keys:
        v_src, a_src, is_1080 = pick_best_source(k)
        info = ffprobe_full(v_src)
        vs = next(s for s in info["streams"] if s["codec_type"] == "video")
        source_report[k] = {
            "video_src": v_src,
            "native_flow_1080p": is_1080,
            "width": vs["width"],
            "height": vs["height"],
            "has_audio": has_audio_stream(v_src),
        }
        print(f"  {k}: {vs['width']}x{vs['height']} native_1080p={is_1080} audio={source_report[k]['has_audio']} ({os.path.basename(v_src)})")

    masters = [
        (
            "WEB_INTRO_15S_MULTI_PRODUCT_16x9.mp4",
            "WEB_INTRO_15S_MULTI_PRODUCT_16x9_MUTED.mp4",
            [
                ("shot1_v2", 0.00, 3.10),  # 3.10s: Cream Hot Tea Mug -> 4 White Daisies pop up 90° (topology-clean v2!)
                ("shot2_v1", 0.00, 3.05),  # 3.05s: Mustard Coffee Mug -> 2-Tier Yellow Sunflowers pop up 90°
                ("shot5_v1", 0.00, 3.00),  # 3.00s: Clear Iced Matcha Latte Glass -> 4 White Daisies pop up 90°
                ("shot3_v1", 0.00, 3.15),  # 3.15s: Clear Iced Milk Latte Glass -> 6 Red & Pink Rosebuds pop up 90°
                ("shot4_v2", 0.00, 2.75),  # 2.75s: White AirPods Case -> White Daisy 3D Storage Basket pops up 90°
            ],
            True,
        ),
        (
            "WEB_INTRO_10S_FASTCUT_16x9.mp4",
            "WEB_INTRO_10S_FASTCUT_16x9_MUTED.mp4",
            [
                ("shot1_v2", 0.15, 2.65),  # 2.50s: Cream Tea Mug descent + touchdown -> crisp 4-daisy 90° snap -> steaming hero
                ("shot2_v1", 0.25, 2.75),  # 2.50s: Mustard Mug descent + touchdown -> 2-tier sunflower 90° snap -> hero
                ("shot3_v1", 0.35, 2.85),  # 2.50s: Iced Latte descent + touchdown -> 6 red/pink rosebud 90° snap -> 0.30s hands-free hero
                ("shot4_v2", 0.20, 2.70),  # 2.50s: AirPods placement -> 3D daisy basket 90° snap -> hero
            ],
            True,
        ),
        (
            "WEB_INTRO_PRODUCT1_DAISY_16x9.mp4",
            "WEB_INTRO_PRODUCT1_DAISY_16x9_MUTED.mp4",
            [
                ("shot1_v2", 0.00, 3.90),  # 3.90s: Cream Hot Tea Mug -> 4 White Daisies pop up 90°
                ("shot5_v1", 0.00, 3.50),  # 3.50s: Clear Iced Matcha Latte Glass -> 4 White Daisies pop up 90° (clean before 3.58s jump)
                ("shot4_v2", 0.00, 3.85),  # 3.85s: White AirPods Case -> White Daisy 3D Basket pops up 90° (11.25s total)
            ],
            True,
        ),
        (
            "WEB_INTRO_PRODUCT2_SUNFLOWER_ROSE_16x9.mp4",
            "WEB_INTRO_PRODUCT2_SUNFLOWER_ROSE_16x9_MUTED.mp4",
            [
                ("shot2_v1", 0.00, 3.33),  # 3.33s: Mustard Coffee Mug -> 2-Tier Yellow Sunflowers pop up 90° (clean before 3.37s micro-pop)
                ("shot3_v1", 0.00, 3.85),  # 3.85s: Clear Iced Milk Latte Glass -> 6 Red & Pink Rosebuds pop up 90°
                ("shot6_v1", 0.00, 3.34),  # 3.34s: Blue-Floral Ceramic Mug -> Dual Sunflower & Rose Coasters pop up 90° (10.52s total)
            ],
            True,
        ),
    ]

    manifest = {"sources": source_report, "deliverables": []}

    for fname, muted_fname, spec, make_sheet in masters:
        out_path = os.path.join(DELIV_DIR, fname)
        muted_path = os.path.join(DELIV_DIR, muted_fname) if muted_fname else None
        print(f"\nAssembling {fname}...")
        concat_segments_to_master(spec, out_path, also_muted_mp4=muted_path)

        # Copy deliverable(s) to brain artifact directory as well
        brain_mp4 = os.path.join(BRAIN_DIR, fname)
        shutil.copy2(out_path, brain_mp4)
        brain_muted_mp4 = None
        if muted_path:
            brain_muted_mp4 = os.path.join(BRAIN_DIR, muted_fname)
            shutil.copy2(muted_path, brain_muted_mp4)

        info = ffprobe_full(out_path)
        vs = next(s for s in info["streams"] if s["codec_type"] == "video")
        a_streams = [s for s in info["streams"] if s["codec_type"] == "audio"]
        dur = float(info["format"]["duration"])
        sz = int(info["format"]["size"])
        print(f"  -> {fname}: {vs['width']}x{vs['height']} {vs['codec_name']} {vs['pix_fmt']} dur={dur:.2f}s audio_streams={len(a_streams)} size={sz:,} bytes")

        sheet_path = None
        brain_sheet = None
        if make_sheet:
            sheet_path = out_path.replace(".mp4", "_contact_2fps.jpg")
            build_2fps_contact_sheet(out_path, sheet_path, cols=5)
            brain_sheet = os.path.join(BRAIN_DIR, os.path.basename(sheet_path))
            shutil.copy2(sheet_path, brain_sheet)

        manifest["deliverables"].append({
            "filename": fname,
            "path": out_path,
            "brain_path": brain_mp4,
            "muted_path": muted_path,
            "brain_muted_path": brain_muted_mp4,
            "width": int(vs["width"]),
            "height": int(vs["height"]),
            "duration_sec": round(dur, 3),
            "size_bytes": sz,
            "pix_fmt": vs["pix_fmt"],
            "has_audio": len(a_streams) > 0,
            "contact_sheet_2fps": sheet_path,
            "brain_contact_sheet_2fps": brain_sheet,
        })

    manifest_path = os.path.join(DELIV_DIR, "deliverables_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nSaved deliverables manifest: {manifest_path}")


if __name__ == "__main__":
    main()
