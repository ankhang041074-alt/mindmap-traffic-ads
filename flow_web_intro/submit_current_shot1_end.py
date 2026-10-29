import asyncio
import base64
import json
import os
import urllib.request
import websockets

OUT_DIR = "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro"
SCREENSHOT_DIR = os.path.join(OUT_DIR, "screenshots")
FRAMES_DIR = os.path.join(OUT_DIR, "frames")


def get_flow_ws_url():
    with urllib.request.urlopen("http://127.0.0.1:52602/json/list") as resp:
        tabs = json.loads(resp.read().decode("utf-8"))
    for tab in tabs:
        if tab.get("type") == "page" and "flow.google" in tab.get("url", ""):
            return tab["webSocketDebuggerUrl"]
    raise RuntimeError("No flow.google tab found")


async def cdp_call(ws, method, params=None, mid=1):
    payload = {"id": mid, "method": method}
    if params:
        payload["params"] = params
    await ws.send(json.dumps(payload))
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if data.get("id") == mid:
            if "error" in data:
                raise RuntimeError(f"CDP error {method}: {data['error']}")
            return data.get("result", {})


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        mid = 1

        async def js(expr):
            nonlocal mid
            res = await cdp_call(ws, "Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True}, mid)
            mid += 1
            return res.get("result", {}).get("value")

        before_imgs = await js("""
        Array.from(document.querySelectorAll('img'))
            .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth, nh: i.naturalHeight}))
            .filter(i => i.src.includes('flow-content.google/image/'))
        """)
        before_uuids = {im["src"].split("?")[0] for im in before_imgs}
        print("Before image count:", len(before_uuids))

        # Inspect ALL 'Bắt đầu tạo' buttons and pick the visible hit-testable one
        btns = await js("""
        Array.from(document.querySelectorAll('[aria-label="Bắt đầu tạo"]')).map(el => {
            const r = el.getBoundingClientRect();
            const cx = Math.round(r.x + r.width / 2);
            const cy = Math.round(r.y + r.height / 2);
            const topEl = document.elementFromPoint(cx, cy);
            const hit = Boolean(topEl && (el === topEl || el.contains(topEl)));
            return {cx, cy, w: Math.round(r.width), h: Math.round(r.height), hit, disabled: el.disabled};
        })
        """)
        print("Submit buttons:", btns)
        target = next((b for b in btns if b["hit"] and not b["disabled"]), None)
        if not target:
            raise RuntimeError("No visible enabled submit button!")

        print(f"Trusted clicking visible submit button at ({target['cx']}, {target['cy']})...")
        await cdp_call(ws, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": target["cx"], "y": target["cy"]}, mid); mid += 1
        await cdp_call(ws, "Input.dispatchMouseEvent", {"type": "mousePressed", "x": target["cx"], "y": target["cy"], "button": "left", "clickCount": 1}, mid); mid += 1
        await cdp_call(ws, "Input.dispatchMouseEvent", {"type": "mouseReleased", "x": target["cx"], "y": target["cy"], "button": "left", "clickCount": 1}, mid); mid += 1

        new_img = None
        for step in range(40):
            await asyncio.sleep(2.0)
            cur_imgs = await js("""
            Array.from(document.querySelectorAll('img'))
                .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth, nh: i.naturalHeight}))
                .filter(i => i.src.includes('flow-content.google/image/'))
            """)
            for im in cur_imgs:
                base = im["src"].split("?")[0]
                if base not in before_uuids and im["nw"] >= 800:
                    new_img = im
                    break
            pct = await js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            print(f"  [{(step+1)*2}s] progress={pct}, found={bool(new_img)}")
            if new_img:
                break

        shot = await cdp_call(ws, "Page.captureScreenshot", {"format": "jpeg", "quality": 85}, mid); mid += 1
        with open(os.path.join(SCREENSHOT_DIR, "21_shot1_end_completed.jpg"), "wb") as f:
            f.write(base64.b64decode(shot["data"]))

        if not new_img:
            raise RuntimeError("Timed out waiting for Shot 1 END_FRAME")

        print(f"SUCCESS! Shot 1 END_FRAME: {new_img['nw']}x{new_img['nh']} -> {new_img['src'][:90]}")
        b64 = await js(f"""
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
        out_file = os.path.join(FRAMES_DIR, "shot1_end.jpg")
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(b64))
        print("Saved full-res Shot 1 END_FRAME:", out_file)

        meta_path = os.path.join(FRAMES_DIR, "frames_manifest.json")
        manifest = {}
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                manifest = json.load(f)
        manifest["shot1_end"] = {
            "base_url": new_img["src"].split("?")[0],
            "full_url": new_img["src"],
            "width": new_img["nw"],
            "height": new_img["nh"],
            "local_path": out_file,
        }
        with open(meta_path, "w") as f:
            json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
