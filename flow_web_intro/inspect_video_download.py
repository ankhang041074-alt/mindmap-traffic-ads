import asyncio
import json
import websockets

from gen_batch_images import FlowCDP, get_flow_ws_url


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        await flow.call("Page.enable")

        # Close ULTRA account dialog if open
        await flow.js("""
        (() => {
            const closeBtns = Array.from(document.querySelectorAll('button'))
                .filter(b => (b.innerText || '').trim() === 'close' || b.getAttribute('aria-label') === 'Đóng');
            for (const b of closeBtns) b.click();
        })()
        """)
        await asyncio.sleep(0.5)

        # Inspect video elements & video cards in DOM
        info = await flow.js("""
        (() => {
            const vids = Array.from(document.querySelectorAll('video')).map(v => ({
                src: v.currentSrc || v.src || '',
                poster: v.poster || '',
                w: v.videoWidth,
                h: v.videoHeight
            }));
            const playBtns = Array.from(document.querySelectorAll('button'))
                .filter(b => (b.innerText || '').includes('play_circle'))
                .slice(0, 5)
                .map(b => {
                    const card = b.closest('[data-testid], [class*="card"], div');
                    const r = b.getBoundingClientRect();
                    return {
                        aria: b.getAttribute('aria-label'),
                        text: (b.innerText || '').trim().slice(0, 80),
                        x: Math.round(r.x), y: Math.round(r.y)
                    };
                });
            return {vids, playBtns};
        })()
        """)
        print("Videos in DOM:", json.dumps(info["vids"][:5], indent=2))
        print("Play buttons in DOM:", json.dumps(info["playBtns"], indent=2))

        # Switch to Video tab on left sidebar briefly or scroll down to inspect one video card's more_vert menu
        await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Left sidebar Video filter")
        await asyncio.sleep(1.0)
        vids_tab = await flow.js("""
        (() => {
            const vids = Array.from(document.querySelectorAll('video')).map(v => ({
                src: v.currentSrc || v.src || '',
                poster: v.poster || ''
            }));
            const moreBtns = Array.from(document.querySelectorAll('button[aria-label="Tuỳ chọn khác"]')).map(b => {
                const r = b.getBoundingClientRect();
                return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2), w: r.width, h: r.height};
            }).filter(b => b.w > 0 && b.cy > 70 && b.cy < 600);
            return {vids: vids.slice(0, 5), moreBtns: moreBtns.slice(0, 3)};
        })()
        """)
        print("In Video filter -> vids:", json.dumps(vids_tab["vids"], indent=2))
        print("In Video filter -> moreBtns:", vids_tab["moreBtns"])

        if vids_tab["moreBtns"]:
            mb = vids_tab["moreBtns"][0]
            await flow.trusted_click(mb["cx"], mb["cy"])
            await asyncio.sleep(0.6)
            menu_items = await flow.js("""
            Array.from(document.querySelectorAll('[role="menuitem"]')).map(m => ({
                text: (m.innerText || '').trim().replace(/\\s+/g, ' '),
                aria: m.getAttribute('aria-label')
            }))
            """)
            print("Video card more_vert menu items:", menu_items)
            await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
            await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
            await asyncio.sleep(0.3)

        # Return to 'Tất cả nội dung nghe nhìn'
        await flow.find_and_trusted_click("text.includes('Tất cả nội dung') && r.x < 240", "Left sidebar All media")
        await asyncio.sleep(0.6)


if __name__ == "__main__":
    asyncio.run(main())
