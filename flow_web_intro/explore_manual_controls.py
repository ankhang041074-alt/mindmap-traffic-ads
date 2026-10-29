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


async def js_click(ws, predicate_js, msg_id):
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


async def dump_popup(ws, msg_id):
    js = """
    (() => {
        return Array.from(document.querySelectorAll('button, [role="button"], [role="menuitem"], [role="option"], [role="tab"], [role="radio"], input'))
            .map(el => {
                const r = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    type: el.getAttribute('type'),
                    role: el.getAttribute('role'),
                    aria: el.getAttribute('aria-label'),
                    state: el.getAttribute('data-state') || el.getAttribute('aria-checked') || el.getAttribute('aria-selected'),
                    text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 100),
                    x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
                };
            })
            .filter(b => b.type === 'file' || (b.w > 0 && b.h > 0 && b.y > 400));
    })()
    """
    return await js_eval(ws, js, msg_id)


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        msg_id = 1
        # 1. Click 'Điều kiện kích hoạt cài đặt'
        await js_click(ws, "aria === 'Điều kiện kích hoạt cài đặt'", msg_id); msg_id += 1
        await asyncio.sleep(0.8)
        await save_shot(ws, "07_manual_settings_image.jpg", msg_id); msg_id += 1
        els = await dump_popup(ws, msg_id); msg_id += 1
        print("=== MANUAL SETTINGS (IMAGE) ===")
        for e in els:
            if e["role"] or e["y"] > 500:
                print(" ", e)

        # 2. Switch to Video tab inside manual settings!
        await js_click(ws, "(text.includes('Video') || text.includes('videocam')) && r.y > 450 && r.y < 850", msg_id); msg_id += 1
        await asyncio.sleep(0.8)
        await save_shot(ws, "08_manual_settings_video.jpg", msg_id); msg_id += 1
        els2 = await dump_popup(ws, msg_id); msg_id += 1
        print("=== MANUAL SETTINGS (VIDEO) ===")
        for e in els2:
            if e["role"] or e["y"] > 500:
                print(" ", e)

        # Close settings popup
        await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
        await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
        await asyncio.sleep(0.6)
        await save_shot(ws, "09_video_prompt_bar.jpg", msg_id); msg_id += 1
        els3 = await dump_popup(ws, msg_id); msg_id += 1
        print("=== VIDEO PROMPT BAR ===")
        for e in els3:
            if e["y"] > 740 or e["type"] == "file":
                print(" ", e)


if __name__ == "__main__":
    asyncio.run(main())
