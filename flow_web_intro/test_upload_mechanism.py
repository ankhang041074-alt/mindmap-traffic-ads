import asyncio
import base64
import json
import os
import urllib.request
import websockets

OUT_DIR = "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro"
SCREENSHOT_DIR = os.path.join(OUT_DIR, "screenshots")
REF_DIR = "/Users/dudumac5/.gemini/antigravity/brain/b5518d8f-8b2d-4488-85b7-420814826233"

TEST_FILE = os.path.join(REF_DIR, "PROD1_STYLE_A_POPUP_MUG_CLEAN.jpg")


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

    async def wait_event(self, event_name, timeout=5.0):
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            for i, ev in enumerate(self.events):
                if ev.get("method") == event_name:
                    return self.events.pop(i)
            try:
                raw = await asyncio.wait_for(self.ws.recv(), timeout=0.3)
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

    async def click(self, predicate_js):
        expr = f"""
        (() => {{
            const els = Array.from(document.querySelectorAll('button, [role="button"], [role="menuitem"], [role="option"]'))
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
        await cdp.call("Page.setInterceptFileChooserDialog", {"enabled": True})

        try:
            # Click top '+' button ("Trình đơn thêm nội dung nghe nhìn")
            await cdp.click("aria === 'Trình đơn thêm nội dung nghe nhìn'")
            await asyncio.sleep(0.6)
            # Click 'Tải lên' menuitem
            await cdp.click("el.getAttribute('role') === 'menuitem' && text.includes('Tải lên')")
            ev = await cdp.wait_event("Page.fileChooserOpened", timeout=5.0)
            print("FileChooser event:", ev)
            if ev and "params" in ev and "backendNodeId" in ev["params"]:
                await cdp.call("DOM.setFileInputFiles", {
                    "files": [TEST_FILE],
                    "backendNodeId": ev["params"]["backendNodeId"]
                })
                print("Successfully setFileInputFiles:", TEST_FILE)
                await asyncio.sleep(5.0)
                await cdp.shot("15_after_upload_test.jpg")
            else:
                print("No backendNodeId in fileChooserOpened! Checking <input type=file> in DOM...")
                doc = await cdp.call("DOM.getDocument", {"depth": -1})
                print("DOM root nodeId:", doc["root"]["nodeId"])
        finally:
            await cdp.call("Page.setInterceptFileChooserDialog", {"enabled": False})


if __name__ == "__main__":
    asyncio.run(main())
