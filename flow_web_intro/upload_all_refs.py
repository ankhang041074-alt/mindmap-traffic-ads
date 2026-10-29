import asyncio
import base64
import json
import os
import urllib.request
import websockets

from home_helper import get_flow_ws_url

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(OUT_DIR, "screenshots")
REF_DIR = os.path.join(OUT_DIR, "clean_product_refs")

FILES_TO_UPLOAD = [
    os.path.join(REF_DIR, "IMG_01_CLEAN_NO_TEXT.jpg"),
    os.path.join(REF_DIR, "PROD1_AIRPODS_BASKET_CLEAN.jpg"),
    os.path.join(REF_DIR, "PROD2_STYLE_C_SUNFLOWER_MUG_CLEAN.jpg"),
    os.path.join(REF_DIR, "PROD2_STYLE_C_SUNFLOWER_EMPTY_BASKET_CLEAN.jpg"),
    os.path.join(REF_DIR, "PROD2_STYLE_B_ROSE_FLAT_ISOLATED.jpg"),
    os.path.join(REF_DIR, "PROD2_IMG_01.jpg"),
]


class CDPClient:
    def __init__(self, ws):
        self.ws = ws
        self.msg_id = 1
        self.events = []

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
            if "id" not in data:
                self.events.append(data)
                continue
            if data["id"] == mid:
                if "error" in data:
                    raise RuntimeError(f"CDP error {method}: {data['error']}")
                return data.get("result", {})

    async def wait_event(self, event_name, timeout=5.0):
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            for i, ev in enumerate(self.events):
                if ev.get("method") == event_name:
                    return self.events.pop(i)
            try:
                raw = await asyncio.wait_for(self.ws.recv(), timeout=0.25)
                data = json.loads(raw)
                if "id" not in data:
                    if data.get("method") == event_name:
                        return data
                    self.events.append(data)
            except asyncio.TimeoutError:
                pass
        return None

    async def js(self, expr):
        res = await self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return res.get("result", {}).get("value")

    async def mouse_click(self, x, y):
        await self.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        await self.call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        await self.call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

    async def shot(self, name):
        res = await self.call("Page.captureScreenshot", {"format": "jpeg", "quality": 85})
        path = os.path.join(SCREENSHOT_DIR, name)
        with open(path, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("Saved:", path)


async def main():
    for f in FILES_TO_UPLOAD:
        assert os.path.exists(f), f"Missing {f}"

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        cdp = CDPClient(ws)
        await cdp.call("Page.enable")
        await cdp.call("DOM.enable")
        await cdp.call("Page.setInterceptFileChooserDialog", {"enabled": True})

        try:
            rect = await cdp.js("""
            (() => {
                const el = document.querySelector('[aria-label="Trình đơn thêm nội dung nghe nhìn"]');
                const r = el.getBoundingClientRect();
                return {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)};
            })()
            """)
            await cdp.mouse_click(rect["x"], rect["y"])
            await asyncio.sleep(0.6)

            item_rect = await cdp.js("""
            (() => {
                const els = Array.from(document.querySelectorAll('[role="menuitem"]'))
                    .filter(el => (el.innerText || '').includes('Tải lên'));
                const r = els[0].getBoundingClientRect();
                return {x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)};
            })()
            """)
            await cdp.mouse_click(item_rect["x"], item_rect["y"])
            ev = await cdp.wait_event("Page.fileChooserOpened", timeout=5.0)
            if not ev:
                raise RuntimeError("No fileChooserOpened event!")
            await cdp.call("DOM.setFileInputFiles", {
                "files": FILES_TO_UPLOAD,
                "backendNodeId": ev["params"]["backendNodeId"]
            })
            print(f"Queued {len(FILES_TO_UPLOAD)} files for upload! Waiting for completion...")

            for attempt in range(25):
                await asyncio.sleep(2.0)
                top_cards = await cdp.js("""
                (() => {
                    return Array.from(document.querySelectorAll('button'))
                        .map(b => b.getAttribute('aria-label') || '')
                        .filter(a => a.includes('CLEAN') || a.includes('PROD') || a.includes('IMG_01'))
                        .slice(0, 15);
                })()
                """)
                pct_texts = await cdp.js("""
                (() => {
                    return Array.from(document.querySelectorAll('div, span'))
                        .map(e => (e.innerText || '').trim())
                        .filter(t => /^\\d+%$/.test(t));
                })()
                """)
                print(f"  [{attempt*2}s] in-progress={pct_texts}, uploaded_labels={top_cards}")
                if len(top_cards) >= 7 and not pct_texts:
                    break

            await cdp.shot("16_all_refs_uploaded.jpg")
        finally:
            await cdp.call("Page.setInterceptFileChooserDialog", {"enabled": False})


if __name__ == "__main__":
    asyncio.run(main())
