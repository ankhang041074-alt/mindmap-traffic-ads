import asyncio
import json
import os
import websockets

from gen_batch_images import FlowCDP, OUT_DIR, get_flow_ws_url


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        await flow.call("Page.enable")

        # Click 'Video' filter on left sidebar
        await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Left sidebar Video")
        await asyncio.sleep(0.8)

        # Hover over the first video card (around x=330, y=220) to see if <video> mounts!
        await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": 330, "y": 220})
        await asyncio.sleep(1.2)
        hover_vids = await flow.js("""
        Array.from(document.querySelectorAll('video')).map(v => ({src: v.currentSrc || v.src || '', w: v.videoWidth, h: v.videoHeight}))
        """)
        print("After hover -> videos:", hover_vids)

        # Also check clicking more_vert -> hover/click 'download Tải xuống'
        more_btns = await flow.js("""
        Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]')).map(b => {
            const r = b.getBoundingClientRect();
            return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2), w: r.width};
        }).filter(b => b.w > 0 && b.cy > 70 && b.cy < 400)
        """)
        if more_btns:
            await flow.trusted_click(more_btns[0]["cx"], more_btns[0]["cy"])
            await asyncio.sleep(0.5)
            dl_item = await flow.js("""
            (() => {
                const m = Array.from(document.querySelectorAll('[role="menuitem"]')).find(e => (e.innerText || '').includes('Tải xuống'));
                if (!m) return null;
                const r = m.getBoundingClientRect();
                return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2), hasPopup: m.getAttribute('aria-haspopup')};
            })()
            """)
            print("Download menuitem:", dl_item)
            if dl_item:
                await flow.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": dl_item["cx"], "y": dl_item["cy"]})
                await asyncio.sleep(0.6)
                sub_items = await flow.js("""
                Array.from(document.querySelectorAll('[role="menuitem"]')).map(m => (m.innerText || '').trim().replace(/\\s+/g, ' '))
                """)
                print("After hovering Tải xuống -> all menuitems:", sub_items)
            await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
            await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
            await asyncio.sleep(0.3)

        # Return to All media
        await flow.find_and_trusted_click("text.includes('Tất cả nội dung') && r.x < 240", "All media")
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
