import asyncio
import base64
import json
import os
import urllib.request
import websockets

OUT_DIR = "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro"
SCREENSHOT_DIR = os.path.join(OUT_DIR, "screenshots")


def get_flow_ws_url():
    with urllib.request.urlopen("http://127.0.0.1:52602/json/list") as resp:
        tabs = json.loads(resp.read().decode("utf-8"))
    for tab in tabs:
        if tab.get("type") == "page" and "flow.google" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    raise RuntimeError("No flow.google tab found")


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

    async def js(self, expr):
        res = await self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return res.get("result", {}).get("value")

    async def click(self, predicate_js):
        expr = f"""
        (() => {{
            const els = Array.from(document.querySelectorAll('button, [role="button"], [role="radio"], [role="menuitem"], [role="option"], [role="tab"]'))
                .filter(el => {{
                    const r = el.getBoundingClientRect();
                    const text = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                    const aria = el.getAttribute('aria-label') || '';
                    return r.width > 0 && r.height > 0 && ({predicate_js});
                }});
            if (!els.length) return 'NOT_FOUND';
            const el = els[0];
            el.dispatchEvent(new PointerEvent('pointerdown', {{bubbles: true}}));
            el.dispatchEvent(new MouseEvent('mousedown', {{bubbles: true}}));
            el.dispatchEvent(new PointerEvent('pointerup', {{bubbles: true}}));
            el.dispatchEvent(new MouseEvent('mouseup', {{bubbles: true}}));
            el.click();
            return 'CLICKED: ' + ((el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ')) + ' | aria=' + el.getAttribute('aria-label');
        }})()
        """
        val = await self.js(expr)
        print(val)
        return val

    async def shot(self, name):
        res = await self.call("Page.captureScreenshot", {"format": "jpeg", "quality": 85})
        path = os.path.join(SCREENSHOT_DIR, name)
        with open(path, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("Saved:", path)


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        cdp = CDPClient(ws)
        await cdp.call("Page.enable")
        await cdp.call("DOM.enable")

        # 1. Open manual settings and check Veo 3.1 - Fast & Veo 3.1 - Quality options
        await cdp.click("aria === 'Điều kiện kích hoạt cài đặt'")
        await asyncio.sleep(0.5)
        await cdp.click("(text.includes('Omni') || text.includes('Veo')) && r.y > 500 && r.y < 760")
        await asyncio.sleep(0.5)
        await cdp.click("role === 'menuitem' && text.includes('Veo 3.1 - Fast')") if False else None
        # Note: role is accessible via el.getAttribute('role')
        await cdp.click("el.getAttribute('role') === 'menuitem' && text.includes('Veo 3.1 - Fast')")
        await asyncio.sleep(0.6)
        await cdp.click("el.getAttribute('role') === 'radio' && text === 'x1'")
        await asyncio.sleep(0.4)
        await cdp.shot("13_veo31_fast_settings.jpg")

        # Close settings
        await cdp.click("aria === 'Điều kiện kích hoạt cài đặt'")
        await asyncio.sleep(0.5)

        # 2. Check what happens when clicking 'Bắt đầu' (First Frame slot)!
        await cdp.click("text === 'Bắt đầu' && r.y > 700")
        await asyncio.sleep(0.8)
        await cdp.shot("14_first_frame_picker.jpg")
        picker_els = await cdp.js("""
        (() => {
            return Array.from(document.querySelectorAll('button, [role="button"], [role="menuitem"], [role="option"], input'))
                .map(el => {
                    const r = el.getBoundingClientRect();
                    return {
                        tag: el.tagName,
                        type: el.getAttribute('type'),
                        role: el.getAttribute('role'),
                        aria: el.getAttribute('aria-label'),
                        text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 80),
                        x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
                    };
                })
                .filter(e => e.type === 'file' || (e.w > 0 && e.h > 0 && e.y > 300 && e.y < 850));
        })()
        """)
        print("=== FIRST FRAME PICKER ELEMENTS ===")
        for e in picker_els[:35]:
            print(" ", e)

        # Close picker with Escape
        await cdp.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await cdp.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
