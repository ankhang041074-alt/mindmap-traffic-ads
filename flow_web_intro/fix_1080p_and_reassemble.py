import asyncio
import glob
import os
import shutil
import websockets

import assemble_web_intros
from download_1080p_winners import DL_TMP, HD_DIR, probe_video
from download_remaining_1080p import extract_mid_frame_rgb_mean, mean_abs_diff
from gen_batch_images import get_flow_ws_url
from gen_video_shot1 import VIDEOS_DIR, FlowVideoCDP


async def download_1080p_strict(flow, card, expected_key, ref_sigs, timeout_s=90):
    os.makedirs(DL_TMP, exist_ok=True)
    for f in glob.glob(os.path.join(DL_TMP, "*")):
        os.remove(f)
    try:
        await flow.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP, "eventsEnabled": True})
    except Exception:
        await flow.call("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": DL_TMP})

    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.4)

    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": card["cx"], "y": card["cy"]})
    await asyncio.sleep(0.7)

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
        print(f"  No more_vert button found near {card}")
        return False

    await flow.trusted_click(more_btn["cx"], more_btn["cy"])
    await asyncio.sleep(0.6)

    dl_item = await flow.js("""
    (() => {
        const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('Tải xuống'));
        if (!m) return null;
        const r = m.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    if not dl_item:
        return False

    await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": dl_item["cx"], "y": dl_item["cy"]})
    await asyncio.sleep(0.8)

    rect_1080 = await flow.js("""
    (() => {
        const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('1080p'));
        if (!m) return null;
        const r = m.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    if not rect_1080:
        return False

    await flow.trusted_click(rect_1080["cx"], rect_1080["cy"])
    print(f"  Triggered 1080p upscale for {expected_key}, waiting up to {timeout_s}s...")

    for _ in range(timeout_s):
        await asyncio.sleep(1.0)
        files = glob.glob(os.path.join(DL_TMP, "*"))
        mp4s = [f for f in files if f.endswith(".mp4") and not f.endswith(".crdownload") and os.path.getsize(f) > 200_000]
        cr = [f for f in files if f.endswith(".crdownload")]
        if mp4s and not cr:
            cand = mp4s[0]
            sig = extract_mid_frame_rgb_mean(cand)
            diffs = {k: round(mean_abs_diff(sig, v), 2) for k, v in ref_sigs.items()}
            best = min(diffs, key=diffs.get)
            print(f"  Downloaded candidate: best={best} diffs={diffs}")
            if best == expected_key and diffs[best] < 5.0:
                out_mp4 = os.path.join(HD_DIR, f"{expected_key}_1080p.mp4")
                shutil.move(cand, out_mp4)
                info = probe_video(out_mp4)
                print(f"  VERIFIED {expected_key}_1080p.mp4: {info['width']}x{info['height']} ({os.path.getsize(out_mp4):,} bytes)")
                return True
            else:
                print(f"  Discarding stale download belonging to {best} while waiting for {expected_key}...")
                os.remove(cand)
    return False


async def fix_hd_folder():
    ref_sigs = {
        k: extract_mid_frame_rgb_mean(os.path.join(VIDEOS_DIR, f"{k}.mp4"))
        for k in ["shot1_v1", "shot2_v1", "shot3_v1", "shot4_v2"]
    }

    print("=== Auditing Existing Files in hd_1080p by Visual RGB Signature ===")
    staged = {}
    for path in sorted(glob.glob(os.path.join(HD_DIR, "*.mp4"))):
        sig = extract_mid_frame_rgb_mean(path)
        diffs = {k: round(mean_abs_diff(sig, v), 2) for k, v in ref_sigs.items()}
        best = min(diffs, key=diffs.get)
        print(f"  {os.path.basename(path)} -> true_identity={best} (diff={diffs[best]}, all={diffs})")
        if diffs[best] < 5.0:
            tmp_stage = os.path.join(HD_DIR, f"__verified_{best}_1080p.mp4")
            shutil.move(path, tmp_stage)
            staged[best] = tmp_stage
        else:
            os.remove(path)

    for k, tmp_stage in staged.items():
        final_p = os.path.join(HD_DIR, f"{k}_1080p.mp4")
        shutil.move(tmp_stage, final_p)
        print(f"  Confirmed {os.path.basename(final_p)} ({os.path.getsize(final_p):,} bytes)")

    missing = [k for k in ["shot1_v1", "shot2_v1", "shot3_v1", "shot4_v2"] if not os.path.exists(os.path.join(HD_DIR, f"{k}_1080p.mp4"))]
    print(f"Missing native 1080p clips: {missing}")

    if "shot1_v1" in missing:
        ws_url = get_flow_ws_url()
        async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
            flow = FlowVideoCDP(ws)
            await flow.call("Page.enable")
            # Scroll to top first, then scroll down +270px so Row 2 Left (shot1_v1) sits cleanly at (x=248, y~347)
            await flow.call("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": 480, "y": 400, "deltaX": 0, "deltaY": -1500})
            await asyncio.sleep(0.8)
            await flow.call("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": 480, "y": 400, "deltaX": 0, "deltaY": 271})
            await asyncio.sleep(1.0)

            card_shot1 = {"x": 248, "y": 346, "w": 452, "h": 254, "cx": 474, "cy": 460}
            await download_1080p_strict(flow, card_shot1, "shot1_v1", ref_sigs, timeout_s=90)

            # Scroll back to top & dismiss toast
            await flow.call("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": 480, "y": 400, "deltaX": 0, "deltaY": -1500})
            await asyncio.sleep(0.7)
            await flow.js("""
            (() => {
                const b = Array.from(document.querySelectorAll('button')).find(el => (el.innerText || '').trim() === 'Đóng');
                if (b) b.click();
            })()
            """)
            await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 120, "y": 500})
            await asyncio.sleep(0.6)
            await flow.shot("25_final_project_overview_clean.jpg")

    shutil.rmtree(DL_TMP, ignore_errors=True)


def main():
    asyncio.run(fix_hd_folder())
    print("\n=== Re-Assembling Verified 1920x1080 16:9 Web Intro Masters ===")
    assemble_web_intros.main()


if __name__ == "__main__":
    main()
