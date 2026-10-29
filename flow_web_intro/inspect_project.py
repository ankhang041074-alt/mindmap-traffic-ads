import asyncio
import base64
import json
import os
import urllib.request
import websockets

OUT_DIR = "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro"
SCREENSHOT_DIR = os.path.join(OUT_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

TARGET_PROJECT_URL = "https://flow.google.com/project/e77d4088-8126-4cb4-8d09-edec09be18ff"


def get_flow_ws_url():
    with urllib.request.urlopen("http://127.0.0.1:52602/json/list") as resp:
        tabs = json.loads(resp.read().decode("utf-8"))
    for tab in tabs:
        if tab.get("type") == "page" and "flow.google" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"], tab["url"], tab["title"]
    for tab in tabs:
        if tab.get("type") == "page" and not tab.get("url", "").startswith("chrome://"):
            return tab["webSocketDebuggerUrl"], tab["url"], tab["title"]
    raise RuntimeError("No suitable page tab found in AdsPower CDP")


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


async def main():
    ws_url, cur_url, title = get_flow_ws_url()
    print(f"Found tab: title={title!r}, url={cur_url!r}")
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        msg_id = 1
        await cdp_call(ws, "Page.enable", msg_id=msg_id); msg_id += 1
        await cdp_call(ws, "Runtime.enable", msg_id=msg_id); msg_id += 1

        if "e77d4088-8126-4cb4-8d09-edec09be18ff" not in cur_url:
            print(f"Navigating to {TARGET_PROJECT_URL}...")
            await cdp_call(ws, "Page.navigate", {"url": TARGET_PROJECT_URL}, msg_id=msg_id); msg_id += 1
            await asyncio.sleep(6)

        # Capture screenshot
        shot = await cdp_call(ws, "Page.captureScreenshot", {"format": "jpeg", "quality": 85}, msg_id=msg_id); msg_id += 1
        shot_path = os.path.join(SCREENSHOT_DIR, "01_initial_project_state.jpg")
        with open(shot_path, "wb") as f:
            f.write(base64.b64decode(shot["data"]))
        print("Saved screenshot to:", shot_path)

        # Inspect interactive DOM elements and existing assets
        js_inspect = """
        (() => {
            const rectObj = (el) => {
                const r = el.getBoundingClientRect();
                return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)};
            };
            const buttons = Array.from(document.querySelectorAll('button, [role="button"], [role="tab"], [role="combobox"], [role="option"], [role="menuitem"]'))
                .map(el => ({
                    tag: el.tagName,
                    role: el.getAttribute('role'),
                    ariaLabel: el.getAttribute('aria-label'),
                    text: (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 120),
                    disabled: el.disabled || el.getAttribute('aria-disabled'),
                    selected: el.getAttribute('aria-selected') || el.getAttribute('data-state'),
                    rect: rectObj(el)
                }))
                .filter(b => b.rect.w > 0 && b.rect.h > 0);

            const inputs = Array.from(document.querySelectorAll('textarea, input, [contenteditable="true"]'))
                .map(el => ({
                    tag: el.tagName,
                    type: el.getAttribute('type'),
                    placeholder: el.getAttribute('placeholder'),
                    ariaLabel: el.getAttribute('aria-label'),
                    contentEditable: el.getAttribute('contenteditable'),
                    value: (el.value || el.innerText || '').slice(0, 200),
                    rect: rectObj(el)
                }));

            const videos = Array.from(document.querySelectorAll('video')).map(v => ({
                src: v.currentSrc || v.src,
                poster: v.poster,
                duration: v.duration,
                w: v.videoWidth,
                h: v.videoHeight,
                rect: rectObj(v)
            }));

            const images = Array.from(document.querySelectorAll('img')).map(img => ({
                src: (img.currentSrc || img.src || '').slice(0, 250),
                alt: img.alt,
                naturalW: img.naturalWidth,
                naturalH: img.naturalHeight,
                rect: rectObj(img)
            })).filter(i => i.rect.w > 20 && i.rect.h > 20);

            return {
                url: location.href,
                title: document.title,
                viewport: {w: window.innerWidth, h: window.innerHeight},
                buttons,
                inputs,
                videos,
                images
            };
        })()
        """
        res = await cdp_call(ws, "Runtime.evaluate", {"expression": js_inspect, "returnByValue": True}, msg_id=msg_id); msg_id += 1
        dom_info = res["result"]["value"]
        dump_path = os.path.join(OUT_DIR, "dom_initial.json")
        with open(dump_path, "w", encoding="utf-8") as f:
            json.dump(dom_info, f, ensure_ascii=False, indent=2)
        print(f"Viewport: {dom_info['viewport']}")
        print(f"Buttons: {len(dom_info['buttons'])}, Inputs: {len(dom_info['inputs'])}, Videos: {len(dom_info['videos'])}, Images: {len(dom_info['images'])}")
        for b in dom_info["buttons"]:
            print(f"  BTN [{b['rect']['x']},{b['rect']['y']} {b['rect']['w']}x{b['rect']['h']}] text={b['text']!r} aria={b['ariaLabel']!r} role={b['role']!r} state={b['selected']!r}")
        for inp in dom_info["inputs"]:
            print(f"  INP [{inp['rect']['x']},{inp['rect']['y']} {inp['rect']['w']}x{inp['rect']['h']}] tag={inp['tag']} type={inp['type']} placeholder={inp['placeholder']!r} aria={inp['ariaLabel']!r}")


if __name__ == "__main__":
    asyncio.run(main())
