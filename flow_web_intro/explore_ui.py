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


async def get_visible_buttons(ws, msg_id):
    js = """
    (() => {
        return Array.from(document.querySelectorAll('button, [role="button"], [role="menuitem"], [role="option"], [role="tab"]'))
            .map(el => {
                const r = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    role: el.getAttribute('role'),
                    aria: el.getAttribute('aria-label'),
                    text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 100),
                    x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
                };
            })
            .filter(b => b.w > 0 && b.h > 0 && b.y >= 0 && b.y <= window.innerHeight);
    })()
    """
    res = await cdp_call(ws, "Runtime.evaluate", {"expression": js, "returnByValue": True}, msg_id=msg_id)
    return res["result"]["value"]


async def click_xy(ws, x, y, msg_id):
    await cdp_call(ws, "Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1}, msg_id=msg_id); msg_id += 1
    await cdp_call(ws, "Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1}, msg_id=msg_id); msg_id += 1
    return msg_id


async def save_shot(ws, name, msg_id):
    shot = await cdp_call(ws, "Page.captureScreenshot", {"format": "jpeg", "quality": 85}, msg_id=msg_id)
    path = os.path.join(SCREENSHOT_DIR, name)
    with open(path, "wb") as f:
        f.write(base64.b64decode(shot["data"]))
    print("Saved:", path)


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        msg_id = 1
        btns = await get_visible_buttons(ws, msg_id); msg_id += 1
        print("=== VISIBLE BUTTONS INITIAL ===")
        for b in btns:
            if b["x"] < 250 or b["x"] > 780 or b["y"] < 70:
                print(f"  [{b['x']},{b['y']} {b['w']}x{b['h']}] text={b['text']!r} aria={b['aria']!r} role={b['role']!r}")

        # 1. Click top '+' menu ("Trình đơn thêm nội dung nghe nhìn" at x=859+20=879, y=18+20=38)
        for b in btns:
            if b["aria"] == "Trình đơn thêm nội dung nghe nhìn":
                cx, cy = b["x"] + b["w"] // 2, b["y"] + b["h"] // 2
                print(f"\nClicking top '+' menu at ({cx}, {cy})...")
                msg_id = await click_xy(ws, cx, cy, msg_id)
                await asyncio.sleep(1.0)
                await save_shot(ws, "02_top_plus_menu.jpg", msg_id); msg_id += 1
                btns2 = await get_visible_buttons(ws, msg_id); msg_id += 1
                for b2 in btns2:
                    if b2["role"] in ("menuitem", "option") or b2["y"] < 350 and b2["x"] > 650:
                        print(f"  MENU [{b2['x']},{b2['y']} {b2['w']}x{b2['h']}] text={b2['text']!r} aria={b2['aria']!r} role={b2['role']!r}")
                # Press Escape to close menu
                await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
                await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
                await asyncio.sleep(0.5)
                break

        # 2. Click 'tune' ("Cài đặt" in prompt box at [1103, 873]) to see settings
        for b in btns:
            if b["aria"] == "Cài đặt" and b["y"] > 800:
                cx, cy = b["x"] + b["w"] // 2, b["y"] + b["h"] // 2
                print(f"\nClicking bottom 'tune' settings at ({cx}, {cy})...")
                msg_id = await click_xy(ws, cx, cy, msg_id)
                await asyncio.sleep(1.0)
                await save_shot(ws, "03_agent_tune_menu.jpg", msg_id); msg_id += 1
                btns3 = await get_visible_buttons(ws, msg_id); msg_id += 1
                for b3 in btns3:
                    if b3["x"] > 700 and b3["y"] > 400:
                        print(f"  TUNE [{b3['x']},{b3['y']} {b3['w']}x{b3['h']}] text={b3['text']!r} aria={b3['aria']!r} role={b3['role']!r}")
                await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
                await cdp_call(ws, "Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"}, msg_id=msg_id); msg_id += 1
                await asyncio.sleep(0.5)
                break


if __name__ == "__main__":
    asyncio.run(main())
