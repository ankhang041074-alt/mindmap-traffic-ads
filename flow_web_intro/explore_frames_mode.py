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


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        msg_id = 1
        # Click 'Khung hình' inside the open Video settings popup
        res = await js_click(ws, "text.includes('Khung hình')", msg_id); msg_id += 1
        if res == "NOT_FOUND":
            await js_click(ws, "aria === 'Điều kiện kích hoạt cài đặt'", msg_id); msg_id += 1
            await asyncio.sleep(0.5)
            await js_click(ws, "text.includes('Video') && r.y > 450 && r.y < 650", msg_id); msg_id += 1
            await asyncio.sleep(0.5)
            await js_click(ws, "text.includes('Khung hình')", msg_id); msg_id += 1
        await asyncio.sleep(0.7)
        await save_shot(ws, "10_frames_mode_settings.jpg", msg_id); msg_id += 1

        # Check models available in Khung hình mode
        await js_click(ws, "(text.includes('Omni') || text.includes('Veo')) && r.y > 500 && r.y < 760", msg_id); msg_id += 1
        await asyncio.sleep(0.6)
        await save_shot(ws, "11_frames_mode_models.jpg", msg_id); msg_id += 1

        # Close dropdown & settings by clicking 'Điều kiện kích hoạt cài đặt' or outside
        await js_click(ws, "aria === 'Điều kiện kích hoạt cài đặt'", msg_id); msg_id += 1
        await asyncio.sleep(0.6)
        await save_shot(ws, "12_frames_prompt_bar.jpg", msg_id); msg_id += 1

        # Dump prompt bar buttons & file inputs
        js = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"], input'))
                .map(el => {
                    const r = el.getBoundingClientRect();
                    return {
                        tag: el.tagName,
                        type: el.getAttribute('type'),
                        role: el.getAttribute('role'),
                        aria: el.getAttribute('aria-label'),
                        text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 100),
                        x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
                    };
                })
                .filter(b => b.type === 'file' || (b.w > 0 && b.h > 0 && b.y > 700));
            return btns;
        })()
        """
        btns = await js_eval(ws, js, msg_id); msg_id += 1
        print("=== FRAMES PROMPT BAR ELEMENTS ===")
        for b in btns:
            print(" ", b)


if __name__ == "__main__":
    asyncio.run(main())
