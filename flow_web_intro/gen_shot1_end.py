import asyncio
import base64
import json
import os
import urllib.request
import websockets

OUT_DIR = "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro"
SCREENSHOT_DIR = os.path.join(OUT_DIR, "screenshots")
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)


def get_flow_ws_url():
    with urllib.request.urlopen("http://127.0.0.1:52602/json/list") as resp:
        tabs = json.loads(resp.read().decode("utf-8"))
    for tab in tabs:
        if tab.get("type") == "page" and "flow.google" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    raise RuntimeError("No flow.google tab found")


class FlowCDP:
    def __init__(self, ws):
        self.ws = ws
        self.msg_id = 1

    async def call(self, method, params=None):
        mid = self.msg_id
        self.msg_id += 1
        payload = {"id": mid, "method": method}
        if params:
            payload["params"] = params
        await self.ws.send(json.dumps(payload))
        while True:
            raw = await self.ws.recv()
            data = json.loads(raw)
            if data.get("id") == mid:
                if "error" in data:
                    raise RuntimeError(f"CDP error {method}: {data['error']}")
                return data.get("result", {})

    async def js(self, expr):
        res = await self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in res:
            raise RuntimeError(f"JS exception: {res['exceptionDetails']}")
        return res.get("result", {}).get("value")

    async def mouse_click(self, x, y):
        await self.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        await self.call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        await self.call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

    async def click_js(self, predicate_js):
        expr = f"""
        (() => {{
            const els = Array.from(document.querySelectorAll('button, [role="button"], [role="radio"], [role="menuitem"], [role="option"], [role="tab"]'))
                .filter(el => {{
                    const r = el.getBoundingClientRect();
                    const text = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                    const aria = el.getAttribute('aria-label') || '';
                    return r.width > 0 && r.height > 0 && ({predicate_js});
                }});
            if (!els.length) return null;
            const el = els[0];
            el.dispatchEvent(new PointerEvent('pointerdown', {{bubbles: true}}));
            el.dispatchEvent(new MouseEvent('mousedown', {{bubbles: true}}));
            el.dispatchEvent(new PointerEvent('pointerup', {{bubbles: true}}));
            el.dispatchEvent(new MouseEvent('mouseup', {{bubbles: true}}));
            el.click();
            const r = el.getBoundingClientRect();
            return {{text: (el.innerText || '').trim().slice(0, 60), aria: el.getAttribute('aria-label'), x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)}};
        }})()
        """
        return await self.js(expr)

    async def shot(self, name):
        res = await self.call("Page.captureScreenshot", {"format": "jpeg", "quality": 85})
        path = os.path.join(SCREENSHOT_DIR, name)
        with open(path, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("Saved screenshot:", path)

    async def ensure_manual_image_16x9(self):
        # Make sure Agent mode is off (check if 'Điều kiện kích hoạt cài đặt' exists)
        has_manual = await self.js("Boolean(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]'))")
        if not has_manual:
            await self.click_js("aria === 'Đóng' && r.x > 1000")
            await asyncio.sleep(0.5)
            await self.click_js("text === 'Tác nhân' && r.y > 700")
            await asyncio.sleep(0.6)

        btn_text = await self.js("(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]')?.innerText || '').trim()")
        print("Current mode pill:", btn_text)
        if "Nano Banana Pro" not in btn_text or "crop_16_9" not in btn_text or "x1" not in btn_text:
            await self.click_js("aria === 'Điều kiện kích hoạt cài đặt'")
            await asyncio.sleep(0.5)
            await self.click_js("text.includes('Hình ảnh') && r.y > 450 && r.y < 750")
            await asyncio.sleep(0.4)
            await self.click_js("el.getAttribute('role') === 'radio' && text.includes('16:9')")
            await asyncio.sleep(0.3)
            await self.click_js("text.includes('Nano Banana') && r.y > 500 && r.y < 780")
            await asyncio.sleep(0.4)
            await self.click_js("el.getAttribute('role') === 'menuitem' && text.includes('Nano Banana Pro')")
            await asyncio.sleep(0.3)
            await self.click_js("el.getAttribute('role') === 'radio' && text === 'x1'")
            await asyncio.sleep(0.3)
            await self.click_js("aria === 'Điều kiện kích hoạt cài đặt'")
            await asyncio.sleep(0.4)

    async def clear_prompt_box(self):
        # Remove any existing attached ingredient chips inside the bottom prompt container
        removed = await self.js("""
        (() => {
            let count = 0;
            const btns = Array.from(document.querySelectorAll('button'))
                .filter(b => {
                    const r = b.getBoundingClientRect();
                    const aria = (b.getAttribute('aria-label') || '').toLowerCase();
                    const txt = (b.innerText || '').trim();
                    return r.y > 700 && (aria.includes('xoá') || aria.includes('xóa') || aria.includes('remove') || txt === 'close' || txt === 'cancel');
                });
            for (const b of btns) { b.click(); count++; }
            return count;
        })()
        """)
        if removed:
            print(f"Removed {removed} old chips")
            await asyncio.sleep(0.3)

        # Focus prompt editor and select-all + delete
        rect = await self.js("""
        (() => {
            const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {x: Math.round(r.x + 20), y: Math.round(r.y + r.height/2)};
        })()
        """)
        if rect:
            await self.mouse_click(rect["x"], rect["y"])
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
            await asyncio.sleep(0.2)

    async def attach_ingredient_by_name(self, name_substr):
        await self.click_js("aria === 'Thêm thành phần vào ô nhập câu lệnh'")
        await asyncio.sleep(0.8)
        opt = await self.click_js(f"el.getAttribute('role') === 'option' && text.includes({json.dumps(name_substr)})")
        if not opt:
            raise RuntimeError(f"Option containing {name_substr!r} not found in ingredient picker!")
        print("Selected option:", opt)
        await asyncio.sleep(0.5)
        add_btn = await self.click_js("text === 'Thêm vào câu lệnh'")
        if not add_btn:
            raise RuntimeError("Could not click 'Thêm vào câu lệnh'")
        await asyncio.sleep(0.6)

    async def enter_prompt_and_submit(self, prompt_text):
        rect = await self.js("""
        (() => {
            const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
            const r = el.getBoundingClientRect();
            return {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)};
        })()
        """)
        await self.mouse_click(rect["x"], rect["y"])
        await asyncio.sleep(0.2)
        await self.call("Input.insertText", {"text": prompt_text})
        await asyncio.sleep(0.5)

    async def get_all_image_urls(self):
        return await self.js("""
        (() => {
            return Array.from(document.querySelectorAll('img'))
                .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth, nh: i.naturalHeight}))
                .filter(i => i.src.includes('flow-content.google/image/'));
        })()
        """)

    async def download_url_in_browser(self, url, out_path):
        b64 = await self.js(f"""
        (async () => {{
            const resp = await fetch({json.dumps(url)});
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
        raw = base64.b64decode(b64)
        with open(out_path, "wb") as f:
            f.write(raw)
        print(f"Downloaded {len(raw)} bytes -> {out_path}")


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        await flow.call("Page.enable")
        # Scroll grid to top so newly created cards are immediately rendered in DOM
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.5)

        await flow.ensure_manual_image_16x9()
        await flow.clear_prompt_box()

        before_imgs = await flow.get_all_image_urls()
        before_uuids = {im["src"].split("?")[0] for im in before_imgs}
        print("Existing image count:", len(before_uuids))

        await flow.attach_ingredient_by_name("PROD1_STYLE_A_POPUP_MUG_CLEAN.jpg")

        prompt = (
            "16:9 widescreen commercial product hero photograph expanding the exact handmade crochet daisy coaster and cream ceramic tea mug from the reference image onto a sunlit morning cafe table. "
            "PRESERVE 100% IDENTICAL PRODUCT DETAILS AND MINIATURE SCALE FROM THE REFERENCE: the round matcha-green crochet yarn coaster pad with light pastel-green scalloped crochet rim, the smooth cream-white ceramic mug with handle on the right filled with warm amber tea and delicate rising steam, and the 6 thin 2.5mm green crochet yarn stems with tiny green crochet leaves standing vertically upright at 90 degrees hugging the lower half of the mug, each stem topped with a SMALL dainty 2.2cm 5-petal white crochet daisy with tiny yellow center (reach only 55% up the mug height, strictly small miniature crochet flowers exactly like the reference, NEVER large or oversized petals). "
            "Compose as a clean 16:9 horizontal website hero banner shot at a 25-degree tabletop angle on a glossy cream-stone breakfast table with generous airy negative space: a small glass jar of fresh chamomiles softly blurred near the sunlit window on the far left, a flaky golden croissant on a white scalloped plate on the far right, warm morning sunbeams and soft window shadows. "
            "85mm commercial macro lens, crisp handmade cotton yarn stitches, NO hands, NO text, NO logos, NO watermarks."
        )
        await flow.enter_prompt_and_submit(prompt)
        await flow.shot("19_before_submit_shot1_end.jpg")

        # Click submit button
        sub = await flow.click_js("aria === 'Bắt đầu tạo'")
        print("Clicked submit:", sub)

        # Poll for new image UUID
        new_img = None
        for step in range(45):
            await asyncio.sleep(2.0)
            cur_imgs = await flow.get_all_image_urls()
            for im in cur_imgs:
                base = im["src"].split("?")[0]
                if base not in before_uuids and im["nw"] >= 800:
                    new_img = im
                    break
            pct = await flow.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            print(f"  [{(step+1)*2}s] progress={pct}, found={bool(new_img)}")
            if new_img:
                break

        await flow.shot("20_after_shot1_end.jpg")
        if not new_img:
            raise RuntimeError("Timed out waiting for Shot 1 END_FRAME!")

        print("NEW IMAGE:", new_img["nw"], "x", new_img["nh"], new_img["src"][:100])
        out_file = os.path.join(FRAMES_DIR, "shot1_end.jpg")
        await flow.download_url_in_browser(new_img["src"], out_file)

        # Save metadata
        meta_path = os.path.join(FRAMES_DIR, "frames_manifest.json")
        manifest = {}
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                manifest = json.load(f)
        manifest["shot1_end"] = {
            "base_url": new_img["src"].split("?")[0],
            "full_url": new_img["src"],
            "width": new_img["nw"],
            "height": new_img["nh"],
            "local_path": out_file,
        }
        with open(meta_path, "w") as f:
            json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
