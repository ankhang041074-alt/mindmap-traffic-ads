import asyncio
import json
import os
import websockets

from gen_batch_images import MANIFEST_PATH, get_flow_ws_url
from gen_video_shot1 import FlowVideoCDP
from review_fix_keyframes_step1 import clear_composer_strict, generate_image_strict
import review_fix_keyframes_step1 as step1


async def select_asset_in_open_flow_menu(flow, identifier, search_query=None):
    """
    Works for BOTH '+' ingredient menu and 'Bắt đầu' / 'Kết thúc' frame slot menu!
    Clears any prior search filter with real keyboard input, checks top 15 items, and uses search_query if needed.
    """
    if isinstance(identifier, (tuple, list)):
        identifier, search_query = identifier[0], identifier[1]

    # Clear search box cleanly with trusted click + selectAll + Backspace if non-empty
    sbox = await flow.js("""
    (() => {
        const inp = document.querySelector('[aria-label="Tìm kiếm thành phần"]');
        if (!inp || !inp.value) return null;
        const r = inp.getBoundingClientRect();
        return {cx: Math.round(r.x + 80), cy: Math.round(r.y + r.height / 2), val: inp.value};
    })()
    """)
    if sbox:
        await flow.trusted_click(sbox["cx"], sbox["cy"])
        await asyncio.sleep(0.15)
        await flow.js("document.querySelector('[aria-label=\"Tìm kiếm thành phần\"]')?.select()")
        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Backspace", "code": "Backspace"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Backspace", "code": "Backspace"})
        await asyncio.sleep(0.5)

    async def inspect_menu():
        return await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(identifier)};
            const listbox = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
            if (!listbox) return {{noListbox: true}};
            const menuRoot = listbox.closest('flow-add-menu-asset-list')?.parentElement || listbox.parentElement?.parentElement;
            const opts = Array.from(listbox.querySelectorAll('[role="option"]'));
            let targetOpt = null;
            for (const el of opts) {{
                const txt = (el.innerText || '').trim();
                const src = el.querySelector('img')?.src || '';
                if (txt.includes(idStr) || src.includes(idStr)) {{
                    const r = el.getBoundingClientRect();
                    targetOpt = {{
                        txt: txt.replace(/\\s+/g, ' ').slice(0, 60),
                        uuid: src.split('?')[0].split('/').pop(),
                        cx: Math.round(r.x + r.width / 2),
                        cy: Math.round(r.y + r.height / 2),
                        y: r.y,
                        h: r.height
                    }};
                    break;
                }}
            }}
            const previewImgs = menuRoot ? Array.from(menuRoot.querySelectorAll('img'))
                .filter(i => !i.closest('[role="option"]') && (i.src || '').includes('flow-content.google/image/'))
                .map(i => (i.src || '').split('?')[0]) : [];
            const addBtn = Array.from(document.querySelectorAll('button')).find(
                b => (b.innerText || '').trim() === 'Thêm vào câu lệnh' && b.getBoundingClientRect().width > 0
            );
            return {{
                noListbox: false,
                targetOpt,
                previewImgs,
                hasAddBtn: Boolean(addBtn),
            }};
        }})()
        """)

    st = await inspect_menu()
    if st.get("noListbox"):
        raise RuntimeError("Asset picker listbox did not open!")

    # If not in top visible 15 items, search via Tìm kiếm thành phần!
    q = search_query or (identifier.replace(".jpg", "") if "." in identifier else None)
    if not st["targetOpt"] and q:
        srect = await flow.js("""
        (() => {
            const inp = document.querySelector('[aria-label="Tìm kiếm thành phần"]');
            if (!inp) return null;
            const r = inp.getBoundingClientRect();
            return {cx: Math.round(r.x + 80), cy: Math.round(r.y + r.height / 2)};
        })()
        """)
        if srect:
            await flow.trusted_click(srect["cx"], srect["cy"])
            await asyncio.sleep(0.2)
            await flow.js("document.querySelector('[aria-label=\"Tìm kiếm thành phần\"]')?.select()")
            await flow.call("Input.insertText", {"text": q})
            await asyncio.sleep(0.8)
            st = await inspect_menu()

    if not st["targetOpt"]:
        raise RuntimeError(f"Asset {identifier!r} (search={q!r}) not found in listbox!")

    target_uuid = st["targetOpt"]["uuid"]
    already_previewed = bool(st["previewImgs"]) and any(target_uuid in u for u in st["previewImgs"]) and st["hasAddBtn"]
    print(f"  Menu check {identifier!r} (uuid={target_uuid[:10]}): already_previewed={already_previewed}, preview={[u[-10:] for u in st['previewImgs']]}")

    if not already_previewed:
        # Ensure option is comfortably inside listbox visible bounds before clicking
        await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(identifier)};
            const lb = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"], [role="listbox"]');
            const opts = Array.from(lb.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const txt = (el.innerText || '').trim();
                const src = el.querySelector('img')?.src || '';
                if (txt.includes(idStr) || src.includes(idStr)) {{
                    el.scrollIntoView({{block: 'nearest'}});
                    return true;
                }}
            }}
            return false;
        }})()
        """)
        await asyncio.sleep(0.3)
        st = await inspect_menu()
        opt = st["targetOpt"]
        await flow.trusted_click(opt["cx"], opt["cy"])
        await asyncio.sleep(0.55)
        st2 = await inspect_menu()
        print(f"  After click preview: hasAddBtn={st2['hasAddBtn']}, preview={[u[-10:] for u in st2['previewImgs']]}")
        if not any(target_uuid in u for u in st2["previewImgs"]):
            raise RuntimeError(f"Right-pane preview UUID mismatch! Expected {target_uuid}, got {st2['previewImgs']}")

    await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
    await asyncio.sleep(0.6)
    return target_uuid


async def attach_single_ingredient_cdk(flow, identifier):
    await flow.find_and_trusted_click("aria === 'Thêm thành phần vào ô nhập câu lệnh'", "open '+' modal")
    await asyncio.sleep(0.8)
    target_uuid = await select_asset_in_open_flow_menu(flow, identifier)
    chip_count = await flow.js("document.querySelectorAll('button[aria-label=\"Thành phần\"]').length")
    print(f"  VERIFIED attached {identifier!r} (uuid={target_uuid[:10]}), composer chip_count={chip_count}")


step1.attach_single_ingredient_verified = attach_single_ingredient_cdk


async def main():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    shot1_end_uuid = manifest["shot1_end"].get("uuid") or manifest["shot1_end"]["base_url"].split("/")[-1]
    shot5_end_uuid = manifest["shot5_end"]["uuid"]
    shot6_end_uuid = manifest["shot6_end"]["uuid"]

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")

        # 1. Regenerate shot1_start_v2 strictly from shot1_end (5212e1d7)
        prompt_shot1_start_v2 = (
            "16:9 widescreen surgical pre-drop state edit of this exact 16:9 sunlit cafe breakfast table reference image. "
            "PRESERVE 100% IDENTICAL CAMERA, FRAMING, BACKGROUND, TABLETOP, AND LIGHTING FROM THE REFERENCE IMAGE: "
            "exact same 16:9 camera angle, focal length, glossy cream-stone breakfast tabletop, glass jar with twine ribbon and white chamomile flowers on the far left, wooden chair with plaid throw and golden flaky croissant on white scalloped plate on the far right, and exact same warm morning window sunbeams. "
            "CHANGE ONLY TWO PHYSICAL STATES FOR THE PRE-DROP MOMENT: "
            "1) Lift the exact same cream-white ceramic hot tea mug straight vertically upward by 3.5 cm so its base hovers 3.5 cm in mid-air directly above the center of the matcha-green crochet coaster, held gently from the right side by a clean manicured female right hand gripping ONLY the mug handle, poised to lower it straight down onto the coaster. "
            "2) Unfold the matcha-green crochet coaster into its completely FLAT 0-degree resting state on the glossy cream-stone tabletop while keeping STRICT 1:1 TOPOLOGY WITH THE REFERENCE COASTER: "
            "the round matcha-green crochet center pad with light pastel-green ruffled/scalloped crochet border is 100% PLAIN SOLID MATCHA-GREEN CROCHET YARN WITH ZERO FLOWERS ON THE CENTER PAD (completely empty plain green crochet center pad, NO white flowers on top of the pad!), "
            "and unfold ONLY the EXACT 4 thin green crochet yarn stems (each with one tiny green crochet leaf and one SMALL dainty ~2.2cm 6-petal white crochet daisy with yellow center, anchored at front-left 8 o'clock, back-left 10 o'clock, front-right 4 o'clock, and back-right 2 o'clock) so those exact 4 daisy stems lie COMPLETELY FLAT horizontally at 0 degrees resting directly on the glossy tabletop radiating outward from the pastel-green rim (NOT standing upright, NOT floating, strictly 4 miniature crochet daisies outside the rim and 0 flowers on the center pad). "
            "85mm commercial macro lens, crisp cotton yarn stitches, NO text, NO logos, NO watermarks."
        )
        await generate_image_strict(flow, "shot1_start_v2", [(shot1_end_uuid, "Crochet daisy coaster and mug")], prompt_shot1_start_v2)

        # 2. Generate shot5_start strictly from shot5_end
        prompt_shot5_start = (
            "16:9 widescreen surgical pre-drop state edit of this exact 16:9 sunlit pale birch-wood cafe table reference image. "
            "PRESERVE 100% IDENTICAL CAMERA, FRAMING, BACKGROUND, TABLETOP, AND LIGHTING FROM THE REFERENCE IMAGE: "
            "exact same 16:9 camera angle, focal length, sunlit pale Scandinavian birch wooden tabletop, open linen-bound book on the far left, wooden chair back in soft background, small ceramic saucer with green matcha macaron on the far right, and exact same warm morning sunbeams. "
            "CHANGE ONLY TWO PHYSICAL STATES FOR THE PRE-DROP MOMENT: "
            "1) Lift the exact same clear cylindrical glass cup of layered iced green matcha milk latte straight vertically upward by 3.5 cm so its glass bottom hovers 3.5 cm in mid-air directly above the center of the matcha-green crochet coaster, held lightly from the upper-right by a clean manicured female right hand gently gripping the upper rim/side of the glass without blocking the view of the coaster below. "
            "2) Unfold the matcha-green crochet coaster into its completely FLAT 0-degree resting state on the birch wooden table while keeping STRICT 1:1 TOPOLOGY WITH THE REFERENCE COASTER: "
            "the round matcha-green crochet center pad with light pastel-green ruffled/scalloped crochet border is 100% PLAIN SOLID MATCHA-GREEN CROCHET YARN WITH ZERO FLOWERS ON THE CENTER PAD (completely empty plain green crochet center pad, NO white flowers on top of the pad!), "
            "and unfold ONLY the EXACT 4 thin green crochet yarn stems (each with one tiny green crochet leaf and one SMALL dainty ~2.2cm 6-petal white crochet daisy with yellow center, anchored at front-left 8 o'clock, back-left 10 o'clock, front-right 4 o'clock, and back-right 2 o'clock) so those exact 4 daisy stems lie COMPLETELY FLAT horizontally at 0 degrees resting directly on the wooden table radiating outward from the pastel-green rim (NOT standing upright, NOT floating, strictly 4 miniature crochet daisies outside the rim and 0 flowers on the center pad). "
            "85mm commercial macro lens, razor-sharp cotton crochet stitches, NO text, NO logos, NO watermarks."
        )
        await generate_image_strict(flow, "shot5_start", [(shot5_end_uuid, "Crochet coaster holding matcha")], prompt_shot5_start)

        # 3. Generate shot6_start strictly from shot6_end
        prompt_shot6_start = (
            "16:9 widescreen surgical pre-drop state edit of this exact 16:9 sunlit oak dining table dual-coaster reference image. "
            "PRESERVE 100% IDENTICAL CAMERA, FRAMING, BACKGROUND, RIGHT-SIDE ROSEBUD COASTER, AND LIGHTING FROM THE REFERENCE IMAGE: "
            "exact same 16:9 camera angle, warm sunlit oak wooden tabletop, blurred stone fireplace and sunlit armchair/windows in the background, blurred green leaves in bottom-left corner, plate of cookies on linen napkin on the far right, AND keep the right-side moss-green & cream-border crochet coaster with 6 red and pink rosebuds 100% IDENTICAL and untouched on the table. "
            "CHANGE ONLY THE LEFT-SIDE SUNFLOWER COASTER AND BLUE-FLORAL CERAMIC MUG FOR THE PRE-DROP MOMENT: "
            "1) Lift the exact hand-painted cream-and-blue floral ceramic mug straight vertically upward by 3.5 cm so its base hovers 3.5 cm in mid-air directly above the center of the left dark soil-brown crochet coaster, held gently from the upper-right by a clean manicured female right hand gripping ONLY the ceramic mug handle, poised to set it straight down onto the brown pad. "
            "2) Unfold the left dark soil-brown crochet pad with bright lime-green ruffled grass border into its completely FLAT 0-degree resting state on the oak table: the dark soil-brown crochet center pad is completely empty and flat, and its 4 thin green crochet yarn stems with green crochet leaves and SMALL ~3cm yellow crochet sunflowers with dark brown yarn centers (anchored at 9 o'clock, 7 o'clock, 5 o'clock, and 3 o'clock) lie COMPLETELY FLAT horizontally at 0 degrees resting directly on the wooden tabletop radiating outward from the lime-green grass border (NOT standing upright, NOT floating, strictly miniature crochet sunflowers matching the reference scale). "
            "85mm commercial macro lens, crisp handmade yarn stitches, NO text, NO logos, NO watermarks."
        )
        await generate_image_strict(flow, "shot6_start", [(shot6_end_uuid, "Crochet flower coasters on table")], prompt_shot6_start)
        await clear_composer_strict(flow)

    print("\n=== Completed Step 2: shot1_start_v2 + shot5_start + shot6_start ===")


if __name__ == "__main__":
    asyncio.run(main())
