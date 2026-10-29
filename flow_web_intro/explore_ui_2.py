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


async def dump_visible(ws, msg_id):
    js = """
    (() => {
        return Array.from(document.querySelectorAll('button, [role="button"], [role="menuitem"], [role="option"], [role="tab"], [role="radio"], [role="switch"], input'))
            .map(el => {
                const r = el.getBoundingClientRect();
                return {
                    tag: el.tagName,
                    type: el.getAttribute('type'),
                    role: el.getAttribute('role'),
                    aria: el.getAttribute('aria-label'),
                    state: el.getAttribute('data-state') || el.getAttribute('aria-checked') || el.getAttribute('aria-selected') || el.getAttribute('aria-expanded'),
                    text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 100),
                    x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
                };
            })
            .filter(b => (b.w > 0 && b.h > 0 && b.y >= 0 && b.y <= window.innerHeight) || b.type === 'file');
    })()
    """
    res = await cdp_call(ws, "Runtime.evaluate", {"expression": js, "returnByValue": True}, msg_id=msg_id)
    return res["result"]["value"]


async def js_click_aria(ws, aria_label, msg_id, min_y=0):
    js = f"""
    (() => {{
        const els = Array.from(document.querySelectorAll('button, [role="button"]'))
            .filter(el => el.getAttribute('aria-label') === {json.dumps(aria_label)} && el.getBoundingClientRect().y >= {min_y});
        if (!els.length) return 'NOT_FOUND';
        const el = els[els.length - 1];
        el.dispatchEvent(new PointerEvent('pointerdown', {{bubbles: true}}));
        el.dispatchEvent(new MouseEvent('mousedown', {{bubbles: true}}));
        el.dispatchEvent(new PointerEvent('pointerup', {{bubbles: true}}));
        el.dispatchEvent(new MouseEvent('mouseup', {{bubbles: true}}));
        el.click();
        return 'CLICKED at ' + JSON.stringify(el.getBoundingClientRect());
    }})()
    """
    res = await cdp_call(ws, "Runtime.evaluate", {"expression": js, "returnByValue": True}, msg_id=msg_id)
    print(f"Click {aria_label!r}:", res["result"]["value"])


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        msg_id = 1
        # Close right agent panel ('Đóng')
        await js_click_aria(ws, "Đóng", msg_id, min_y=50); msg_id += 1
        await asyncio.sleep(1.2)
        await save_shot(ws, "04_after_close_agent.jpg", msg_id); msg_id += 1
        els = await dump_visible(ws, msg_id); msg_id += 1
        print("=== AFTER CLOSING AGENT PANEL ===")
        for e in els:
            if e["y"] > 700 or e["type"] == "file" or e["y"] < 70:
                print(f"  [{e['x']},{e['y']} {e['w']}x{e['h']}] tag={e['tag']} type={e['type']} role={e['role']} state={e['state']} text={e['text']!r} aria={e['aria']!r}")

        # Now click bottom 'Cài đặt' (tune button) in the prompt bar!
        await js_click_aria(ws, "Cài đặt", msg_id, min_y=700); msg_id += 1
        await asyncio.sleep(1.0)
        await save_shot(ws, "05_bottom_prompt_settings.jpg", msg_id); msg_id += 1
        els2 = await dump_visible(ws, msg_id); msg_id += 1
        print("=== AFTER CLICKING BOTTOM PROMPT SETTINGS ===")
        for e in els2:
            if e["y"] > 450 or e["role"] in ("menuitem", "option", "tab", "radio", "switch"):
                print(f"  [{e['x']},{e['y']} {e['w']}x{e['h']}] tag={e['tag']} role={e['role']} state={e['state']} text={e['text']!r} aria={e['aria']!r}")


if __name__ == "__main__":
    asyncio.run(main())
