import asyncio
import json
import websockets

from gen_batch_images import FlowCDP, get_flow_ws_url


async def main():
    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        await flow.call("Page.enable")

        # Check account credit info by clicking ULTRA pill
        await flow.find_and_trusted_click("aria === 'Thông tin về tài khoản'", "ULTRA badge")
        await asyncio.sleep(0.7)
        acc_text = await flow.js("""
        Array.from(document.querySelectorAll('[role="dialog"], [role="menu"], div'))
            .map(e => (e.innerText || '').trim())
            .filter(t => t.includes('tín dụng') || t.includes('ULTRA'))
            .slice(0, 5)
        """)
        print("Account credit info:", acc_text)
        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(0.4)

        # Open manual settings -> Video -> Khung hình -> 16:9 -> 4 giây -> x1 and check Veo 3.1 Fast vs Quality
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "settings pill")
        await asyncio.sleep(0.5)
        await flow.find_and_trusted_click("text.includes('Video') && r.y > 450 && r.y < 750", "Video tab")
        await asyncio.sleep(0.4)
        await flow.find_and_trusted_click("text.includes('Khung hình')", "Khung hình")
        await asyncio.sleep(0.3)
        await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text.includes('16:9')", "16:9")
        await asyncio.sleep(0.3)
        await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === '4 giây'", "4 giây")
        await asyncio.sleep(0.3)
        await flow.find_and_trusted_click("el.getAttribute('role') === 'radio' && text === 'x1'", "x1")
        await asyncio.sleep(0.4)
        fast_cost = await flow.js("""
        Array.from(document.querySelectorAll('div, span, p'))
            .map(e => (e.innerText || '').trim())
            .filter(t => t.includes('Quá trình tạo sẽ tốn'))
        """)
        print("Veo 3.1 - Fast (4s, 16:9, x1) cost:", fast_cost)

        # Switch to Veo 3.1 - Quality and check cost
        await flow.find_and_trusted_click("(text.includes('Veo') || text.includes('Omni')) && r.y > 500 && r.y < 780", "model dropdown")
        await asyncio.sleep(0.4)
        await flow.find_and_trusted_click("el.getAttribute('role') === 'menuitem' && text.includes('Veo 3.1 - Quality')", "Veo 3.1 - Quality")
        await asyncio.sleep(0.4)
        qual_cost = await flow.js("""
        Array.from(document.querySelectorAll('div, span, p'))
            .map(e => (e.innerText || '').trim())
            .filter(t => t.includes('Quá trình tạo sẽ tốn'))
        """)
        print("Veo 3.1 - Quality (4s, 16:9, x1) cost:", qual_cost)

        # Close settings
        await flow.find_and_trusted_click("aria === 'Điều kiện kích hoạt cài đặt'", "close settings")


if __name__ == "__main__":
    asyncio.run(main())
