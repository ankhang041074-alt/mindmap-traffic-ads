import asyncio
import base64
import json
import os
import websockets

from gen_batch_images import FlowCDP, MANIFEST_PATH, OUT_DIR, SCREENSHOT_DIR, get_flow_ws_url

VIDEOS_DIR = os.path.join(OUT_DIR, "videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)
VIDEO_MANIFEST_PATH = os.path.join(VIDEOS_DIR, "videos_manifest.json")


class FlowVideoCDP(FlowCDP):
    async def ensure_video_frames_mode(self, model_name="Veo 3.1 - Fast", duration_label="4 giây"):
        # Close any stray popovers
        await self.js("""
        (() => {
            const closeBtns = Array.from(document.querySelectorAll('button'))
                .filter(b => b.getAttribute('aria-label') === 'Đóng' && b.getBoundingClientRect().width > 0);
            for (const b of closeBtns) b.click();
        })()
        """)
        await asyncio.sleep(0.4)

        # Ensure manual mode (Tác nhân OFF)
        has_manual = await self.js("Boolean(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]'))")
        if not has_manual:
            await self.find_and_trusted_click("text === 'Tác nhân' && r.y > 700", "toggle Tác nhân off")
            await asyncio.sleep(0.6)

        await self.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "open settings")
        await asyncio.sleep(0.5)
        await self.find_and_trusted_click("text.includes('Video') && r.y > 400 && r.y < 700", "Video tab")
        await asyncio.sleep(0.4)
        await self.find_and_trusted_click("text.includes('Khung hình')", "Khung hình mode")
        await asyncio.sleep(0.4)
        await self.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('16:9')", "16:9 aspect ratio")
        await asyncio.sleep(0.3)

        # Open model selector inside Video settings
        await self.find_and_trusted_click("(text.includes('Veo') || text.includes('Omni')) && r.y > 500 && r.y < 780", "Video model dropdown")
        await asyncio.sleep(0.4)
        await self.find_and_trusted_click(f"el.getAttribute('role') === 'menuitem' && text.includes({json.dumps(model_name)})", f"Model {model_name}")
        await asyncio.sleep(0.4)

        await self.find_and_trusted_click(f"el.getAttribute('role') === 'radio' && text === {json.dumps(duration_label)}", f"Duration {duration_label}")
        await asyncio.sleep(0.3)
        await self.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === 'x1'", "x1 count")
        await asyncio.sleep(0.3)

        await self.shot("22_video_settings_configured.jpg")
        # Close settings popup
        await self.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "close settings")
        await asyncio.sleep(0.5)

    async def set_frame_slot(self, slot_label, image_uuid):
        """slot_label is 'Bắt đầu' or 'Kết thúc'."""
        await self.find_and_trusted_click(f"text.includes({json.dumps(slot_label)}) && r.y > 650", f"Slot {slot_label}")
        await asyncio.sleep(0.9)

        # Scroll option with image_uuid into view
        found = await self.js(f"""
        (() => {{
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const imgSrc = el.querySelector('img')?.src || '';
                if (imgSrc.includes({json.dumps(image_uuid)})) {{
                    el.scrollIntoView({{block: 'center'}});
                    return true;
                }}
            }}
            return false;
        }})()
        """)
        if not found:
            # Switch to 'Hình ảnh' tab inside modal just in case
            await self.find_and_trusted_click("el.getAttribute('role') === 'tab' && text.includes('Hình ảnh')", "Modal Hình ảnh tab")
            await asyncio.sleep(0.6)
            await self.js(f"""
            (() => {{
                const opts = Array.from(document.querySelectorAll('[role="option"]'));
                for (const el of opts) {{
                    const imgSrc = el.querySelector('img')?.src || '';
                    if (imgSrc.includes({json.dumps(image_uuid)})) {{
                        el.scrollIntoView({{block: 'center'}});
                        return true;
                    }}
                }}
                return false;
            }})()
            """)

        await asyncio.sleep(0.3)
        opt = await self.find_and_trusted_click(
            f"el.getAttribute('role') === 'option' && imgSrc.includes({json.dumps(image_uuid)})",
            f"Frame option {image_uuid}"
        )
        print(f"  [{slot_label}] selected {image_uuid[:12]}...: {opt['text']!r}")
        await asyncio.sleep(0.5)
        await self.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
        await asyncio.sleep(0.6)

    async def get_video_cards_in_video_tab(self):
        await self.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Left sidebar Video tab")
        await asyncio.sleep(0.8)
        await self.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.4)
        cards = await self.js("""
        (() => {
            // Find all card images or play buttons in the main grid (x > 240)
            const imgs = Array.from(document.querySelectorAll('img'))
                .filter(i => {
                    const r = i.getBoundingClientRect();
                    return r.x > 240 && r.width > 120 && r.height > 80 && r.y > 60 && r.y < 600;
                })
                .map(i => {
                    const r = i.getBoundingClientRect();
                    return {
                        thumb: (i.currentSrc || i.src || '').split('?')[0],
                        cx: Math.round(r.x + r.width / 2),
                        cy: Math.round(r.y + r.height / 2),
                        w: Math.round(r.width),
                        h: Math.round(r.height)
                    };
                });
            return imgs;
        })()
        """)
        return cards

    async def generate_flf_video(self, clip_key, start_uuid, end_uuid, prompt, model_name="Veo 3.1 - Fast", duration_label="4 giây"):
        print(f"\n=== GENERATING VIDEO {clip_key} ({model_name}, {duration_label}, 16:9) ===")
        # Record existing top video thumbnails in Video tab first
        before_cards = await self.get_video_cards_in_video_tab()
        before_thumbs = {c["thumb"] for c in before_cards}
        print(f"  Before top video cards visible: {len(before_thumbs)}")

        # Switch back to All media so our generated images are in view / accessible
        await self.find_and_trusted_click("text.includes('Tất cả nội dung') && r.x < 240", "Left sidebar All media")
        await asyncio.sleep(0.6)

        await self.ensure_video_frames_mode(model_name=model_name, duration_label=duration_label)

        # Clear any existing frames/text if present
        await self.js("""
        (() => {
            const rmBtns = Array.from(document.querySelectorAll('button')).filter(b => {
                const r = b.getBoundingClientRect();
                const aria = (b.getAttribute('aria-label') || '').toLowerCase();
                const txt = (b.innerText || '').trim();
                return r.y > 640 && r.x > 250 && r.x < 550 && (aria.includes('xoá') || aria.includes('xóa') || txt === 'close');
            });
            for (const b of rmBtns) b.click();
        })()
        """)
        await asyncio.sleep(0.3)

        await self.set_frame_slot("Bắt đầu", start_uuid)
        await self.set_frame_slot("Kết thúc", end_uuid)

        # Enter motion prompt
        ed_rect = await self.js("""
        (() => {
            const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
            const r = el.getBoundingClientRect();
            return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
        })()
        """)
        await self.trusted_click(ed_rect["cx"], ed_rect["cy"])
        await asyncio.sleep(0.2)
        await self.js("""
        (() => {
            const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
            if (el) {
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
            }
        })()
        """)
        await asyncio.sleep(0.15)
        await self.call("Input.insertText", {"text": prompt})
        await asyncio.sleep(0.5)
        await self.shot(f"before_{clip_key}.jpg")

        # Click submit button
        btns = await self.js("""
        Array.from(document.querySelectorAll('[aria-label="Bắt đầu tạo"]')).map(el => {
            const r = el.getBoundingClientRect();
            const cx = Math.round(r.x + r.width / 2);
            const cy = Math.round(r.y + r.height / 2);
            const topEl = document.elementFromPoint(cx, cy);
            const hit = Boolean(topEl && (el === topEl || el.contains(topEl)));
            return {cx, cy, hit, disabled: el.disabled};
        })
        """)
        target = next((b for b in btns if b["hit"] and not b["disabled"]), None)
        if not target:
            raise RuntimeError(f"Submit button not enabled for {clip_key}: {btns}")
        await self.trusted_click(target["cx"], target["cy"])
        print(f"  Submitted {clip_key}! Switching to Video tab to monitor completion...")
        await asyncio.sleep(1.5)

        await self.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Left sidebar Video tab")
        await asyncio.sleep(1.0)

        new_card = None
        for step in range(60):
            await asyncio.sleep(3.0)
            await self.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
            pct = await self.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            cur_cards = await self.js("""
            Array.from(document.querySelectorAll('img'))
                .filter(i => {
                    const r = i.getBoundingClientRect();
                    return r.x > 240 && r.width > 120 && r.height > 80 && r.y > 60 && r.y < 500;
                })
                .map(i => {
                    const r = i.getBoundingClientRect();
                    return {
                        thumb: (i.currentSrc || i.src || '').split('?')[0],
                        cx: Math.round(r.x + r.width / 2),
                        cy: Math.round(r.y + r.height / 2),
                        w: Math.round(r.width),
                        h: Math.round(r.height)
                    };
                })
            """)
            for c in cur_cards:
                if c["thumb"] and c["thumb"] not in before_thumbs:
                    new_card = c
                    break
            print(f"    [{(step+1)*3}s] progress={pct}, new_card={bool(new_card)}")
            if new_card and not pct:
                break

        await self.shot(f"after_{clip_key}.jpg")
        if not new_card:
            raise RuntimeError(f"Timed out waiting for video {clip_key}!")

        # Hover over the new card to mount <video> element and fetch its .mp4!
        print(f"  Hovering new 16:9 video card at ({new_card['cx']}, {new_card['cy']}) ({new_card['w']}x{new_card['h']})...")
        await self.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": new_card["cx"], "y": new_card["cy"]})
        vid_src = None
        for _ in range(15):
            await asyncio.sleep(0.6)
            vids = await self.js("""
            Array.from(document.querySelectorAll('video')).map(v => ({
                src: v.currentSrc || v.src || '',
                w: v.videoWidth,
                h: v.videoHeight
            })).filter(v => v.src.startsWith('http'))
            """)
            if vids:
                vid_src = vids[0]["src"]
                print(f"  Mounted <video>: {vids[0]['w']}x{vids[0]['h']} src={vid_src[:90]}...")
                break

        if not vid_src:
            raise RuntimeError(f"Could not mount <video> on hover for {clip_key}")

        b64 = await self.js(f"""
        (async () => {{
            const resp = await fetch({json.dumps(vid_src)});
            const buf = await resp.arrayBuffer();
            let binary = '';
            const bytes = new Uint8Array(buf);
            const chunk = 0x8000;
            for (let i = 0; i < bytes.length; i += chunk) {{
                binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
            }}
            return btoa(binary);
        }})()
        """)
        out_mp4 = os.path.join(VIDEOS_DIR, f"{clip_key}.mp4")
        with open(out_mp4, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  DOWNLOADED {clip_key}.mp4 ({os.path.getsize(out_mp4)} bytes) -> {out_mp4}")

        vman = {}
        if os.path.exists(VIDEO_MANIFEST_PATH):
            with open(VIDEO_MANIFEST_PATH) as f:
                vman = json.load(f)
        vman[clip_key] = {
            "thumb": new_card["thumb"],
            "video_url": vid_src,
            "local_path": out_mp4,
            "model": model_name,
            "duration": duration_label,
        }
        with open(VIDEO_MANIFEST_PATH, "w") as f:
            json.dump(vman, f, indent=2)
        return out_mp4


async def main():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    s1_start = manifest["shot1_start"].get("uuid") or manifest["shot1_start"]["base_url"].split("/")[-1]
    s1_end = manifest["shot1_end"].get("uuid") or manifest["shot1_end"]["base_url"].split("/")[-1]

    prompt_shot1 = (
        "Locked-off static tripod 16:9 commercial macro shot with zero camera movement. "
        "0.0s to 0.8s: The woman's right hand smoothly lowers the steaming cream ceramic tea mug straight down 4 cm until the mug base presses firmly onto the center of the flat matcha-green crochet daisy coaster pad. "
        "0.8s to 1.1s: Triggered instantly by the weight of the mug pressing the internal drawstring mechanism of the coaster, all 6 thin green crochet yarn stems hinge crisply and rapidly upward 90 degrees around their fixed rim anchor points in one fast elastic spring pop-up snap (pivoting strictly from the coaster border while remaining physically attached to the crochet rim at all times, zero floating petals, zero slow levitation), hugging the lower half of the mug with small dainty white crochet daisies. "
        "1.1s to 2.0s: Her fingers gently release the mug handle and her hand withdraws smoothly out of frame to the right. "
        "2.0s to 4.0s: Completely settled, motionless hero tea mug hugged by upright miniature white crochet daisies on the sunlit breakfast table as soft tea steam rises gently. Subtle natural foley of ceramic mug touching soft cotton yarn and a crisp light yarn spring snap, quiet morning room ambience, no voice, no music, no text."
    )

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")
        await flow.generate_flf_video("shot1_v1", s1_start, s1_end, prompt_shot1, model_name="Veo 3.1 - Fast", duration_label="4 giây")


if __name__ == "__main__":
    asyncio.run(main())
