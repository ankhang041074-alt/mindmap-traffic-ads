import asyncio
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import websockets

OUT_DIR_LOCAL = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(OUT_DIR_LOCAL)
sys.path.insert(0, OUT_DIR_LOCAL)
sys.path.insert(0, os.path.join(REPO_ROOT, "flow_web_intro"))
from gen_batch_images import FlowCDP
from home_helper import discover_cdp_http_url
from run_barrel20_images_silent import OUT_DIR, PORT, PROJECT_ID
from run_barrel20_veo4s_silent import exit_edit_view_if_needed

TARGET_ROOT = os.environ.get("ATF9422_OUT_DIR") or os.path.expanduser("~/Downloads/ATF-9422")
CLIPS_DIR = os.path.join(TARGET_ROOT, "20_clips_le_1080p")
DL_TMP = os.path.join(OUT_DIR, "_dl_1080p_tmp")
MASTER_MP4 = os.path.join(TARGET_ROOT, "ATF-9422_1080p.mp4")

FFMPEG = "/opt/homebrew/bin/ffmpeg" if os.path.exists("/opt/homebrew/bin/ffmpeg") else "ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe" if os.path.exists("/opt/homebrew/bin/ffprobe") else "ffprobe"

# Exact verified Video-tab 2-column grid indices (0 = newest .. 22 = oldest of the 23 barrel clips)
# Indices {3: VB20_old, 8: VB15_old, 21: VB02_old} are intentionally skipped!
CARD_INDEX_TO_SCENE = [
    (22, "01_B01_Porch_Charcoal_Door_Pair"),
    (0,  "02_B02_Porch_Farmhouse_3Q_Pair"),
    (20, "03_B03_Living_Limestone_Fireplace_Pair"),
    (19, "04_B04_Patio_Black_French_Doors_Pair"),
    (18, "05_B05_Courtyard_Stone_Fountain_3Q_Pair"),
    (17, "06_B06_Foyer_White_Oak_Console_Pair"),
    (16, "07_B07_Porch_Limestone_Arch_Walnut_Doors_Pair"),
    (15, "08_B08_Courtyard_Arched_Oak_Window_Pair"),
    (14, "09_B09_Terrace_Pergola_Teak_Deck_3Q_Pair"),
    (13, "10_B10_Gallery_Arched_Portal_Wainscoting_Pair"),
    (12, "11_B11_Verandah_Teak_Rattan_Lounge_Single"),
    (11, "12_B12_Living_Fluted_Oak_Credenza_Single"),
    (10, "13_B13_Sunroom_Oak_Window_Bench_Single"),
    (9,  "14_B14_Kitchen_Marble_Oak_Island_Single"),
    (1,  "15_B15_Dining_Oak_Sideboard_True4ft_Single"),
    (7,  "16_B16_Study_Walnut_Desk_Arched_Shelves_Single"),
    (6,  "17_B17_Staircase_Oak_Iron_Garden_Glass_Single"),
    (5,  "18_B18_Bedroom_Balcony_Linen_Curtains_Single"),
    (4,  "19_B19_Pool_Cabana_Travertine_Daybed_Single"),
    (2,  "20_B20_Coastal_Great_Room_Ocean_True4ft_Single"),
]


def probe_video(path):
    res = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,duration,r_frame_rate", "-of", "json", path],
        capture_output=True, text=True, check=True,
    )
    return json.loads(res.stdout)["streams"][0]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


async def switch_to_video_tab(flow):
    await exit_edit_view_if_needed(flow)
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)
    vid_tab = await flow.js("""
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="tab"]')).filter(b => {
            const r = b.getBoundingClientRect();
            const txt = (b.innerText || '').trim();
            return r.width > 0 && r.x < 260 && r.y > 60 && r.y < 260 && txt.includes('Video');
        });
        if (!btns.length) return null;
        const r = btns[0].getBoundingClientRect();
        return {cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)};
    })()
    """)
    if vid_tab:
        await flow.trusted_click(vid_tab["cx"], vid_tab["cy"])
        await asyncio.sleep(1.0)


async def scroll_to_card_exact(flow, card_idx):
    row = card_idx // 2
    col = card_idx % 2
    target_sy = max(0, round(row * 270.25 - 100))
    await flow.js(f"""
    (() => {{
        for (const el of Array.from(document.querySelectorAll('*'))) {{
            if (el.scrollHeight > el.clientHeight + 200 && el.getBoundingClientRect().width > 500) {{
                el.scrollTop = {target_sy};
            }}
        }}
    }})()
    """)
    await asyncio.sleep(0.55)
    card = await flow.js(f"""
    (() => {{
        const sc = Array.from(document.querySelectorAll('*')).find(el => el.scrollTop > 0 && el.getBoundingClientRect().width > 500);
        const actualSy = sc ? sc.scrollTop : 0;
        const expX = {248 if col == 0 else 716};
        const expY = 76 + {row} * 270.25 - actualSy;
        const media = Array.from(document.querySelectorAll('img, video')).filter(m => {{
            const r = m.getBoundingClientRect();
            return Math.abs(r.x - expX) < 30 && Math.abs(r.y - expY) < 45 && r.width > 400;
        }});
        if (!media.length) return null;
        const r = media[0].getBoundingClientRect();
        return {{
            x: Math.round(r.x),
            y: Math.round(r.y),
            w: Math.round(r.width),
            h: Math.round(r.height),
            cx: Math.round(r.x + r.width / 2),
            cy: Math.round(r.y + Math.min(r.height / 2, 110)),
        }};
    }})()
    """)
    return card


async def download_one_1080p(flow, card_idx, out_mp4, seen_hashes):
    for attempt in range(1, 4):
        for f in glob.glob(os.path.join(DL_TMP, "*")):
            try:
                os.remove(f)
            except OSError:
                pass

        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(0.35)

        # Dismiss any floating toast 'Đóng' button so it never overlaps
        await flow.js("""
        (() => {
            const b = Array.from(document.querySelectorAll('button')).find(el => (el.innerText || '').trim() === 'Đóng');
            if (b) b.click();
        })()
        """)

        card = await scroll_to_card_exact(flow, card_idx)
        if not card:
            print(f"    [attempt {attempt}] Card #{card_idx} not found at expected grid slot, refreshing Video tab...")
            await switch_to_video_tab(flow)
            continue

        # Move away then hover card center to reveal 'Tuỳ chọn khác'
        await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 110, "y": 320})
        await asyncio.sleep(0.2)
        await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": card["cx"], "y": card["cy"]})
        await asyncio.sleep(0.65)

        more_btn = await flow.js(f"""
        (() => {{
            const btns = Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]'))
                .map(b => {{
                    const r = b.getBoundingClientRect();
                    return {{cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2), x: r.x, y: r.y, w: r.width}};
                }})
                .filter(b => b.w > 0 && b.x >= {card['x'] - 20} && b.x <= {card['x'] + card['w'] + 20} && b.y >= {card['y'] - 20} && b.y <= {card['y'] + card['h'] + 20});
            return btns[0] || null;
        }})()
        """)
        if not more_btn:
            print(f"    [attempt {attempt}] 'Tuỳ chọn khác' not visible on hover at {card}")
            continue

        await flow.trusted_click(more_btn["cx"], more_btn["cy"])
        await asyncio.sleep(0.55)

        dl_item = await flow.js("""
        (() => {
            const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('Tải xuống'));
            if (!m) return null;
            const r = m.getBoundingClientRect();
            return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
        })()
        """)
        if not dl_item:
            print(f"    [attempt {attempt}] 'Tải xuống' menuitem not found")
            continue

        await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": dl_item["cx"], "y": dl_item["cy"]})
        await asyncio.sleep(0.75)

        rect_1080 = await flow.js("""
        (() => {
            const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('1080p'));
            if (!m) return null;
            const r = m.getBoundingClientRect();
            return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
        })()
        """)
        if not rect_1080:
            print(f"    [attempt {attempt}] '1080p' submenu item not found")
            continue

        await flow.trusted_click(rect_1080["cx"], rect_1080["cy"])
        print(f"    ⏳ Triggered 1080p upscale/download for card #{card_idx} (attempt {attempt}), waiting up to 80s...")

        for _ in range(80):
            await asyncio.sleep(1.0)
            files = glob.glob(os.path.join(DL_TMP, "*"))
            mp4s = [f for f in files if f.endswith(".mp4") and not f.endswith(".crdownload") and os.path.getsize(f) > 200_000]
            cr = [f for f in files if f.endswith(".crdownload")]
            if mp4s and not cr:
                cand = mp4s[0]
                h = sha256_file(cand)
                if h in seen_hashes:
                    print("    ⚠️ Discarding duplicate stale download hash, continuing wait...")
                    os.remove(cand)
                    continue
                info = probe_video(cand)
                w, ht = int(info["width"]), int(info["height"])
                if w < 1900 or ht < 1060:
                    print(f"    ⚠️ Got {w}x{ht} instead of 1080p, retrying...")
                    os.remove(cand)
                    break
                seen_hashes.add(h)
                shutil.move(cand, out_mp4)
                print(f"    ✅ Saved {os.path.basename(out_mp4)} ({w}x{ht}, {float(info.get('duration', 4.0)):.2f}s, {os.path.getsize(out_mp4)/1024/1024:.2f} MB)")
                return True
    raise RuntimeError(f"Failed to download 1080p clip for card #{card_idx} -> {out_mp4}")


def extract_vb02_contact_sheet(vb02_mp4, out_jpg):
    subprocess.run(
        [
            FFMPEG, "-y", "-i", vb02_mp4,
            "-vf", "fps=1.25,scale=640:360,tile=5x1",
            "-frames:v", "1", "-q:v", "3", out_jpg,
        ],
        check=True, capture_output=True,
    )
    print("Saved VB02_v2 5-frame QA strip:", out_jpg)


def merge_20_clips_into_single_1080p_mp4(clip_paths, out_master_mp4):
    concat_txt = os.path.join(DL_TMP, "concat_20.txt")
    os.makedirs(DL_TMP, exist_ok=True)
    with open(concat_txt, "w") as f:
        for p in clip_paths:
            esc = p.replace("'", "'\\''")
            f.write(f"file '{esc}'\n")

    res = subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", "-movflags", "+faststart", out_master_mp4],
        capture_output=True, text=True,
    )
    ok_copy = False
    if res.returncode == 0 and os.path.exists(out_master_mp4):
        info = probe_video(out_master_mp4)
        dur = float(info.get("duration", 0))
        if int(info["width"]) == 1920 and int(info["height"]) == 1080 and 78.0 <= dur <= 82.5:
            ok_copy = True
            print(f"✅ Lossless 1080p master merged: {out_master_mp4} ({info['width']}x{info['height']}, {dur:.2f}s, {os.path.getsize(out_master_mp4)/1024/1024:.2f} MB)")

    if not ok_copy:
        print("Encoding high-bitrate CRF 16 1080p master for uniform timebase...")
        subprocess.run(
            [
                FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
                "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out_master_mp4,
            ],
            check=True, capture_output=True,
        )
        info = probe_video(out_master_mp4)
        dur = float(info.get("duration", 0))
        print(f"✅ High-bitrate 1080p master merged: {out_master_mp4} ({info['width']}x{info['height']}, {dur:.2f}s, {os.path.getsize(out_master_mp4)/1024/1024:.2f} MB)")


async def main():
    os.makedirs(TARGET_ROOT, exist_ok=True)
    os.makedirs(CLIPS_DIR, exist_ok=True)
    os.makedirs(DL_TMP, exist_ok=True)

    seen_hashes = set()
    for existing in sorted(glob.glob(os.path.join(CLIPS_DIR, "*.mp4"))):
        try:
            inf = probe_video(existing)
            if int(inf["width"]) >= 1900 and int(inf["height"]) >= 1060:
                seen_hashes.add(sha256_file(existing))
        except Exception:
            pass

    cdp_base = discover_cdp_http_url()
    tabs = json.loads(urllib.request.urlopen(f"{cdp_base}/json/list").read())
    t = next((x for x in tabs if PROJECT_ID in (x.get("url") or "")), None)
    if not t:
        raise RuntimeError(f"Flow tab for project {PROJECT_ID} not found on {cdp_base}!")

    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=40 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        # Silent background focus emulation ONLY — NEVER call Page.bringToFront!
        await flow.call("Page.enable")
        await flow.call("DOM.enable")
        await flow.call("Emulation.setFocusEmulationEnabled", {"enabled": True})
        try:
            await flow.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP, "eventsEnabled": True})
        except Exception:
            await flow.call("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP})

        await switch_to_video_tab(flow)

        ordered_clip_paths = []
        for card_idx, slug in CARD_INDEX_TO_SCENE:
            out_mp4 = os.path.join(CLIPS_DIR, f"{slug}_1080p.mp4")
            ordered_clip_paths.append(out_mp4)
            if os.path.exists(out_mp4):
                try:
                    inf = probe_video(out_mp4)
                    if int(inf["width"]) == 1920 and int(inf["height"]) == 1080:
                        print(f"⏩ Already verified 1080p: {os.path.basename(out_mp4)}")
                        continue
                except Exception:
                    os.remove(out_mp4)

            print(f"\n[{slug}] Downloading Video-tab card #{card_idx} in 1080p...")
            await download_one_1080p(flow, card_idx, out_mp4, seen_hashes)

        await flow.js("Array.from(document.querySelectorAll('*')).forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")

    extract_vb02_contact_sheet(ordered_clip_paths[1], os.path.join(OUT_DIR, "qa_vb02_v2_5frames.jpg"))
    merge_20_clips_into_single_1080p_mp4(ordered_clip_paths, MASTER_MP4)
    shutil.rmtree(DL_TMP, ignore_errors=True)
    print("\n🎉 ALL 20 1080p VIDEOS DOWNLOADED & MERGED INTO:", MASTER_MP4)


if __name__ == "__main__":
    asyncio.run(main())
