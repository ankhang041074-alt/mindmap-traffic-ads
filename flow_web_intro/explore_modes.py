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


async def cdp_call(ws, method, params=None, msg_id=1):
    payload = {"id": msg_id, "method": method}
    if params:
        payload["params"] = params
    await ws.send(json.dumps(payload))
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if data.get("id") == msg_id:
            if "error" in data:
                raise RuntimeError(f"CDP error for {method}: {data['error']}")
            return data.get("result", {})


async def save_shot(ws, name, msg_id):
    shot = await cdp_call(ws, "Page.captureScreenshot", {"format": "jpeg", "quality": 85}, msg_id=msg_id)
    path = os.path.join(SCREENSHOT_DIR, name)
    with open(path, "wb") as f:
        f.write(base64.b64decode(shot["data"]))
    print("Saved:", path)


async def js_eval(ws, expr, msg_id):
    res = await cdp_call(ws, "Runtime.evaluate", {"expression": expr, "returnByValue": True}, msg_id=msg_id)
    return res.get("result", {}).get("value")


async def js_click_element(ws, predicate_js, msg_id):
    js = f"""
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
    val = await js_eval(ws, js, msg_id)
    print(val)
    return val


async def dump_visible(ws, msg_id):
    js = """
    (() => {
        return Array.from(document.querySelectorAll('button, [role="button"], [role="menuitem"], [role="option"], [role="tab"], [role="radio"]'))
            .map(el => {
                const r = el.getBoundingClientRect();
                return {
                    role: el.getAttribute('role'),
                    aria: el.getAttribute('aria-label'),
                    state: el.getAttribute('data-state') || el.getAttribute('aria-checked') || el.getAttribute('aria-selected'),
                    text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 100),
                    x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
                };
            })
            .filter(b => b.w > 0 && b.h > 0 && b.y >= 0 && b.y <= window.innerHeight);
    })()
    """
    return await js_eval(ws, js, msg_id)


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        msg_id = 1
        # 1. Inspect Image models dropdown
        await js_click_element(ws, "aria.includes('quá trình tạo hình ảnh')", msg_id); msg_id += 1
        await asyncio.sleep(0.7)
        els = await dump_visible(ws, msg_id); msg_id += 1
        print("=== IMAGE MODELS ===")
        for e in els:
            if e["role"] in ("option", "menuitem") or (e["x"] > 800 and 300 < e["y"] < 800):
                print(" ", e)
        await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
        await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
        await asyncio.sleep(0.5)

        # 2. Inspect Video models dropdown
        await js_click_element(ws, "aria.includes('tính năng tạo video')", msg_id); msg_id += 1
        await asyncio.sleep(0.7)
        els = await dump_visible(ws, msg_id); msg_id += 1
        print("=== VIDEO MODELS ===")
        for e in els:
            if e["role"] in ("option", "menuitem") or (e["x"] > 800 and 400 < e["y"] < 900):
                print(" ", e)
        await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
        await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
        await asyncio.sleep(0.5)

        # 3. Click 16:9 for Image (y around 362) and 16:9 for Video (y around 545), then click 'Lưu'
        await js_click_element(ws, "text.includes('16:9') && r.y > 300 && r.y < 420", msg_id); msg_id += 1
        await asyncio.sleep(0.3)
        await js_click_element(ws, "text.includes('16:9') && r.y > 500 && r.y < 600", msg_id); msg_id += 1
        await asyncio.sleep(0.3)
        await js_click_element(ws, "text === 'Lưu'", msg_id); msg_id += 1
        await asyncio.sleep(1.0)

        # Close right agent panel if open
        await js_click_element(ws, "aria === 'Đóng' && r.x > 1000", msg_id); msg_id += 1
        await asyncio.sleep(0.8)

        # 4. Now click 'Tác nhân' mode selector button in the bottom prompt bar!
        await js_click_element(ws, "text === 'Tác nhân' && r.y > 750", msg_id); msg_id += 1
        await asyncio.sleep(0.8)
        await save_shot(ws, "06_mode_selector_popup.jpg", msg_id); msg_id += 1
        els = await dump_visible(ws, msg_id); msg_id += 1
        print("=== MODE SELECTOR POPUP ===")
        for e in els:
            if e["y"] > 500 or e["role"] in ("menuitem", "option", "tab", "radio"):
                print(" ", e)


if __name__ == "__main__":
    asyncio.run(main())
