import asyncio
import base64
import json
import os
import urllib.request
import websockets

from home_helper import get_flow_ws_url

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(OUT_DIR, "screenshots")
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)
MANIFEST_PATH = os.path.join(FRAMES_DIR, "frames_manifest.json")


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
            raw = await asyncio.wait_for(self.ws.recv(), timeout=25.0)
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

    async def trusted_click(self, x, y):
        await self.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        await self.call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        await self.call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

    async def find_and_trusted_click(self, predicate_js, desc="element"):
        rect = await self.js(f"""
        (() => {{
            const els = Array.from(document.querySelectorAll('button, [role="button"], [role="radio"], [role="menuitem"], [role="option"], [role="tab"]'))
                .filter(el => {{
                    const r = el.getBoundingClientRect();
                    if (r.width <= 0 || r.height <= 0) return false;
                    const cx = Math.round(r.x + r.width / 2);
                    const cy = Math.round(r.y + r.height / 2);
                    if (cx < 0 || cy < 0 || cx > window.innerWidth || cy > window.innerHeight) return false;
                    const text = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                    const aria = el.getAttribute('aria-label') || '';
                    const imgSrc = el.querySelector('img')?.src || '';
                    return ({predicate_js});
                }});
            if (!els.length) return null;
            // Pick the hit-testable one if possible, else last matching
            for (const el of els) {{
                const r = el.getBoundingClientRect();
                const cx = Math.round(r.x + r.width / 2);
                const cy = Math.round(r.y + r.height / 2);
                const topEl = document.elementFromPoint(cx, cy);
                if (topEl && (el === topEl || el.contains(topEl) || topEl.contains(el))) {{
                    return {{cx, cy, text: (el.innerText || '').trim().slice(0, 60), aria: el.getAttribute('aria-label')}};
                }}
            }}
            const el = els[0];
            const r = el.getBoundingClientRect();
            return {{cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2), text: (el.innerText || '').trim().slice(0, 60), aria: el.getAttribute('aria-label')}};
        }})()
        """)
        if not rect:
            raise RuntimeError(f"Could not find {desc}: {predicate_js}")
        await self.trusted_click(rect["cx"], rect["cy"])
        return rect

    async def shot(self, name):
        res = await self.call("Page.captureScreenshot", {"format": "jpeg", "quality": 85})
        path = os.path.join(SCREENSHOT_DIR, name)
        with open(path, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("  Saved screenshot:", path)

    async def ensure_image_16x9_pro(self):
        pill = await self.js("(document.querySelector('[aria-label=\"Điều kiện kích hoạt cài đặt\"]')?.innerText || '').trim()")
        if "Nano Banana Pro" not in pill or "crop_16_9" not in pill or "x1" not in pill:
            await self.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "settings pill")
            await asyncio.sleep(0.5)
            await self.find_and_trusted_click("text.includes('Hình ảnh') && r.y > 450", "Hình ảnh tab")
            await asyncio.sleep(0.4)
            await self.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('16:9')", "16:9 radio")
            await asyncio.sleep(0.3)
            await self.find_and_trusted_click("text.includes('Nano Banana') && r.y > 500 && r.y < 780", "model dropdown")
            await asyncio.sleep(0.4)
            await self.find_and_trusted_click("el.getAttribute('role') === 'menuitem' && text.includes('Nano Banana Pro')", "Nano Banana Pro")
            await asyncio.sleep(0.3)
            await self.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === 'x1'", "x1 radio")
            await asyncio.sleep(0.3)
            await self.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "close settings")
            await asyncio.sleep(0.4)

    async def attach_ingredient(self, identifier):
        """identifier can be a filename substring (e.g. 'IMG_01_CLEAN_NO_TEXT.jpg') or an image UUID substring."""
        await self.find_and_trusted_click("aria === 'Thêm thành phần vào ô nhập câu lệnh'", "add ingredient '+'")
        await asyncio.sleep(0.9)

        # Scroll modal list if needed or search if not immediately visible
        found = await self.js(f"""
        (() => {{
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const text = (el.innerText || '').trim();
                const imgSrc = el.querySelector('img')?.src || '';
                if (text.includes({json.dumps(identifier)}) || imgSrc.includes({json.dumps(identifier)})) {{
                    el.scrollIntoView({{block: 'center'}});
                    return true;
                }}
            }}
            return false;
        }})()
        """)
        if not found:
            # Type in search box 'Tìm kiếm thành phần'
            srect = await self.js("""
            (() => {
                const inp = document.querySelector('[aria-label="Tìm kiếm thành phần"]');
                if (!inp) return null;
                const r = inp.getBoundingClientRect();
                return {cx: Math.round(r.x + 60), cy: Math.round(r.y + r.height/2)};
            })()
            """)
            if srect:
                await self.trusted_click(srect["cx"], srect["cy"])
                await asyncio.sleep(0.2)
                await self.call("Input.insertText", {"text": identifier.replace(".jpg", "")})
                await asyncio.sleep(0.7)

        await asyncio.sleep(0.3)
        opt = await self.find_and_trusted_click(
            f"el.getAttribute('role') === 'option' && (text.includes({json.dumps(identifier)}) || imgSrc.includes({json.dumps(identifier)}))",
            f"option {identifier}"
        )
        print(f"  Selected ingredient {identifier!r}: {opt['text']!r}")
        await asyncio.sleep(0.5)
        await self.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
        await asyncio.sleep(0.6)

    async def generate_image(self, key_name, ingredients, prompt):
        print(f"\n=== GENERATING {key_name} ===")
        await self.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
        await asyncio.sleep(0.4)
        await self.ensure_image_16x9_pro()

        before_imgs = await self.js("""
        Array.from(document.querySelectorAll('img'))
            .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth, nh: i.naturalHeight}))
            .filter(i => i.src.includes('flow-content.google/image/'))
        """)
        before_uuids = {im["src"].split("?")[0] for im in before_imgs}

        for ing in ingredients:
            await self.attach_ingredient(ing)

        # Enter prompt text
        ed_rect = await self.js("""
        (() => {
            const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
            const r = el.getBoundingClientRect();
            return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
        })()
        """)
        await self.trusted_click(ed_rect["cx"], ed_rect["cy"])
        await asyncio.sleep(0.2)
        await self.call("Input.insertText", {"text": prompt})
        await asyncio.sleep(0.5)

        # Trusted click on visible hit-tested submit button
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
            await self.shot(f"err_{key_name}_no_submit.jpg")
            raise RuntimeError(f"Submit button not enabled for {key_name}: {btns}")
        await self.trusted_click(target["cx"], target["cy"])
        print(f"  Submitted {key_name} at ({target['cx']}, {target['cy']}), polling...")

        new_img = None
        for step in range(45):
            await asyncio.sleep(2.0)
            await self.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
            cur_imgs = await self.js("""
            Array.from(document.querySelectorAll('img'))
                .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth, nh: i.naturalHeight}))
                .filter(i => i.src.includes('flow-content.google/image/'))
            """)
            for im in cur_imgs:
                base = im["src"].split("?")[0]
                if base not in before_uuids and im["nw"] >= 1000:
                    new_img = im
                    break
            pct = await self.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            print(f"    [{(step+1)*2}s] progress={pct}, found={bool(new_img)}")
            if new_img:
                break

        if not new_img:
            await self.shot(f"err_{key_name}_timeout.jpg")
            raise RuntimeError(f"Timeout waiting for {key_name}")

        b64 = await self.js(f"""
        (async () => {{
            const resp = await fetch({json.dumps(new_img['src'])});
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
        out_file = os.path.join(FRAMES_DIR, f"{key_name}.jpg")
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f"  SAVED {key_name}: {new_img['nw']}x{new_img['nh']} -> {out_file}")

        manifest = {}
        if os.path.exists(MANIFEST_PATH):
            with open(MANIFEST_PATH) as f:
                manifest = json.load(f)
        manifest[key_name] = {
            "uuid": new_img["src"].split("?")[0].split("/")[-1],
            "base_url": new_img["src"].split("?")[0],
            "full_url": new_img["src"],
            "width": new_img["nw"],
            "height": new_img["nh"],
            "local_path": out_file,
        }
        with open(MANIFEST_PATH, "w") as f:
            json.dump(manifest, f, indent=2)
        return manifest[key_name]


async def main():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    shot1_end_uuid = manifest["shot1_end"]["base_url"].split("/")[-1]

    jobs = [
        (
            "shot1_start",
            [shot1_end_uuid, "IMG_01_CLEAN_NO_TEXT.jpg"],
            (
                "16:9 widescreen surgical pre-drop state edit of the first 16:9 cafe table reference image, using the second reference image strictly for the flat unfolded state of the green crochet daisy coaster. "
                "PRESERVE 100% IDENTICAL CAMERA, FRAMING, BACKGROUND, AND LIGHTING FROM THE FIRST 16:9 IMAGE: exact same 16:9 camera angle, focal length, glossy cream-stone breakfast tabletop, glass jar of chamomiles on the left, wooden chair and flaky croissant on white scalloped plate on the right, and exact same warm morning window sunbeams. "
                "CHANGE ONLY TWO PHYSICAL STATES FOR THE PRE-DROP MOMENT: "
                "1) Lift the exact same cream-white ceramic tea mug straight vertically upward by 4 cm so its base hovers 4 cm in mid-air directly above the center of the green crochet coaster, held gently from the right side by a clean manicured female right hand gripping the mug handle, poised to lower it onto the coaster. "
                "2) Unfold the green crochet daisy coaster into its completely FLAT 0-degree resting state on the glossy table surface (matching the second reference image): the round matcha-green crochet pad with pastel-green scalloped border lies flat on the table (with 3 tiny flat white crochet daisies sewn on the green pad), and all 6 thin 2.5mm green crochet yarn stems with tiny green leaves and SMALL dainty 2.2cm 5-petal white crochet daisies lie COMPLETELY FLAT horizontally at 0 degrees resting directly on the tabletop radiating outward around the coaster rim (NOT standing upright, NOT floating in mid-air, strictly small miniature crochet daisies, NEVER large petals). "
                "85mm commercial macro lens, crisp cotton yarn stitches, NO text, NO logos, NO watermarks."
            ),
        ),
        (
            "shot2_end",
            ["PROD2_STYLE_C_SUNFLOWER_MUG_CLEAN.jpg"],
            (
                "16:9 widescreen commercial product hero photograph expanding the exact handmade crochet sunflower coaster and mustard-yellow ceramic coffee mug from the reference image onto a warm sunlit natural oak desk. "
                "PRESERVE 100% IDENTICAL PRODUCT DETAILS AND 2-TIER MINIATURE SCALE FROM THE REFERENCE: the dark soil-brown crochet yarn center pad with bright lime-green ruffled crochet grass border, the glossy mustard-yellow ceramic mug with handle on the right sitting centered on the brown pad, and the exact 2-tier miniature yellow crochet sunflowers with dark brown yarn centers on thin green crochet yarn stems with small green crochet leaves standing vertically upright at 90 degrees around the mug: 2 tall side sunflower stems on the left (9 o'clock) and right (3 o'clock) reaching mug rim height, plus 2 shorter front sunflower stems reaching halfway (50%) up the mug height (each crochet sunflower head strictly small ~3cm diameter matching the reference 1:1, NEVER giant or oversized petals). "
                "Compose as a clean 16:9 horizontal website hero banner at a 25-degree tabletop angle on a sunlit honey-oak wooden desk with airy negative space: a small white ceramic pot with green leafy plant and woven rattan mat softly blurred on the far left, a closed cream linen notebook on the far right, warm golden morning window sunbeams. "
                "85mm commercial macro lens, crisp handmade yarn stitches, NO hands, NO text, NO logos, NO watermarks."
            ),
        ),
        (
            "shot3_end",
            ["PROD2_STYLE_B_ROSE_FLAT_ISOLATED.jpg", "PROD2_IMG_01.jpg"],
            (
                "16:9 widescreen commercial product hero photograph of the exact handmade olive-green crochet coaster with cream-white scalloped border and 6 miniature crochet rosebud stems from the reference images, shown in its 3D POPPED-UP UPRIGHT STATE holding a clear cylindrical glass cup of layered iced milk latte on a sunlit walnut afternoon-tea table. "
                "PRESERVE 100% IDENTICAL CROCHET COASTER MATERIALS AND MINIATURE ROSEBUD SCALE FROM THE REFERENCES: round moss-green spiral crochet yarn center pad with cream-white scalloped crochet border, and exactly 6 thin green crochet yarn stems (each with one small veined sage-green crochet leaf and one SMALL tight spherical ~2.2cm crochet rosebud alternating crimson-red and dusty-pink, strictly small compact crochet rosebuds like the reference, NEVER giant open roses) standing VERTICALLY UPRIGHT at 90 degrees from the cream border hugging the lower half of the clear glass iced latte cup (reaching ~55% up the glass height). "
                "Compose as a clean 16:9 horizontal website hero banner at a 25-degree tabletop angle on a warm sunlit walnut wooden table in a cozy sunlit living room with soft bokeh fireplace/window background on the left and a folded striped linen napkin with a small plate of butter cookies on the far right. "
                "85mm commercial macro lens, crisp cotton yarn stitches, NO hands, NO text, NO logos, NO watermarks."
            ),
        ),
        (
            "shot4_end",
            ["PROD1_AIRPODS_BASKET_CLEAN.jpg", "PROD1_STYLE_A_POPUP_MUG_CLEAN.jpg"],
            (
                "16:9 widescreen commercial macro hero photograph upgrading the exact handmade matcha-green crochet white daisy coaster holding a smooth glossy white wireless earbuds charging case (matching the first reference image 1:1, using the second reference image for crisp crochet yarn stitch detail) on a clean sunlit minimalist cream-oak vanity desk. "
                "PRESERVE 100% IDENTICAL PRODUCT PROPORTIONS AND MINIATURE DAISY SCALE FROM THE FIRST REFERENCE: a clean smooth glossy white rounded rectangular wireless earbuds case (~4.5cm x 5.4cm, zero logos, zero text) resting snugly in the center of the round matcha-green crochet yarn pad whose light pastel-green scalloped border curls slightly upward (~25 degrees) into a cozy shallow nest, while 6 thin 2.5mm green crochet yarn stems with tiny green crochet leaves stand upright at 85-90 degrees around the rim, each topped with a SMALL dainty 2.2cm 5-petal white crochet daisy with tiny yellow center (plus 3 tiny white crochet daisies nestled along the inner rim, strictly miniature scale matching the reference, NEVER oversized flowers). "
                "Compose as a clean 16:9 horizontal website hero shot at a 38-degree elevated tabletop angle on a bright sunlit cream-white minimalist desk with soft morning window leaf shadows and warm airy negative space on left and right. "
                "85mm commercial macro lens, razor-sharp cotton crochet stitches, NO hands, NO text, NO logos, NO watermarks."
            ),
        ),
    ]

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        await flow.call("Page.enable")
        for key_name, ingredients, prompt in jobs:
            await flow.generate_image(key_name, ingredients, prompt)
            await asyncio.sleep(1.0)


if __name__ == "__main__":
    asyncio.run(main())
