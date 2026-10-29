import asyncio
import os
import websockets

from gen_batch_images import get_flow_ws_url
from gen_video_shot1 import VIDEOS_DIR, FlowVideoCDP
from download_1080p_winners import HD_DIR, try_download_1080p
import subprocess


def extract_mid_frame_rgb_mean(video_path):
    tmp_a = video_path + "_chk.ppm"
    subprocess.run(
        ["/opt/homebrew/bin/ffmpeg", "-y", "-ss", "2.0", "-i", video_path,
         "-frames:v", "1", "-vf", "scale=32:18", tmp_a],
        capture_output=True, check=True
    )
    with open(tmp_a, "rb") as f:
        data = f.read()[-32 * 18 * 3:]
    os.remove(tmp_a)
    return list(data)


def mean_abs_diff(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


async def main():
    ref_sigs = {
        k: extract_mid_frame_rgb_mean(os.path.join(VIDEOS_DIR, f"{k}.mp4"))
        for k in ["shot1_v1", "shot2_v1", "shot3_v1", "shot4_v2"]
    }

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")

        # Scroll to very top of current All Media view (do NOT re-click active tab so grid stays hydrated)
        await flow.call("Input.dispatchMouseEvent", {
            "type": "mouseWheel", "x": 480, "y": 400, "deltaX": 0, "deltaY": -1200
        })
        await asyncio.sleep(0.8)

        # Exact verified card boxes from 25_final_project_overview_clean.jpg (1200x940 viewport):
        exact_targets = [
            ("shot3_v1", {"x": 248, "y": 346, "w": 452, "h": 254, "cx": 474, "cy": 460}),
            ("shot2_v1", {"x": 716, "y": 346, "w": 452, "h": 254, "cx": 942, "cy": 460}),
            ("shot1_v1", {"x": 248, "y": 617, "w": 452, "h": 254, "cx": 474, "cy": 655}),
        ]

        for name, card in exact_targets:
            out_path = os.path.join(HD_DIR, f"{name}_1080p.mp4")
            if os.path.exists(out_path) and os.path.getsize(out_path) > 500_000:
                print(f"Already have {name}_1080p.mp4, skipping.")
                continue
            print(f"\nTriggering native Flow 1080p upscale for {name} at ({card['cx']},{card['cy']})...")
            ok = await try_download_1080p(flow, card, out_path)
            print(f"  Result for {name}: {ok}")
            if ok:
                sig = extract_mid_frame_rgb_mean(out_path)
                diffs = {k: round(mean_abs_diff(sig, v), 2) for k, v in ref_sigs.items()}
                best = min(diffs, key=diffs.get)
                print(f"  Visual RGB verification: best_match={best} (expected {name}) diffs={diffs}")
            # Dismiss toast if present
            await flow.js("""
            (() => {
                const b = Array.from(document.querySelectorAll('button')).find(el => (el.innerText || '').trim() === 'Đóng');
                if (b) b.click();
            })()
            """)
            await asyncio.sleep(0.5)

        # Move mouse to neutral sidebar margin so no hover overlay remains, capture final clean screenshot
        await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 120, "y": 500})
        await asyncio.sleep(0.8)
        await flow.shot("25_final_project_overview_clean.jpg")


if __name__ == "__main__":
    asyncio.run(main())
