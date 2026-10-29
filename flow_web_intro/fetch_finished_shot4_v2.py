import asyncio
import hashlib
import os
import websockets

from finish_videos_2_3_4 import (
    VIDEOS_DIR,
    build_and_copy_sheet,
    download_card_mp4_robust,
    get_finished_16x9_video_cards,
)
from gen_batch_images import get_flow_ws_url
from gen_video_shot1 import FlowVideoCDP


def md5_file(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


async def main():
    v1_md5 = md5_file(os.path.join(VIDEOS_DIR, "shot4_v1.mp4"))
    print("shot4_v1 md5:", v1_md5)

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")
        await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
        await asyncio.sleep(1.0)

        for step in range(30):
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
            await asyncio.sleep(0.4)
            pct = await flow.js("""
            Array.from(document.querySelectorAll('div, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => /^\\d+%$/.test(t))
            """)
            cards = await get_finished_16x9_video_cards(flow)
            print(f"  [check {step*3}s] pct={pct}, visible_16x9={len(cards)}")
            if not pct and cards:
                out_mp4 = os.path.join(VIDEOS_DIR, "shot4_v2.mp4")
                await download_card_mp4_robust(flow, cards[0], out_mp4, res_choice="720p")
                new_md5 = md5_file(out_mp4)
                print("Downloaded top card md5:", new_md5)
                if new_md5 != v1_md5:
                    build_and_copy_sheet("shot4_v2", out_mp4)
                    print("SUCCESS: Fresh shot4_v2 downloaded and audited!")
                    return
                print("Top card was still shot4_v1, waiting 4s...")
            await asyncio.sleep(3.0)


if __name__ == "__main__":
    asyncio.run(main())
