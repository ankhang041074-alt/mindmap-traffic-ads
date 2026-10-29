import asyncio
import base64
import glob
import json
import os
import shutil
import websockets

from download_1080p_winners import DL_TMP, HD_DIR, probe_video
from download_remaining_1080p import extract_mid_frame_rgb_mean, mean_abs_diff
from fix_1080p_and_reassemble import download_1080p_strict
from gen_batch_images import FRAMES_DIR, MANIFEST_PATH, get_flow_ws_url
from gen_video_shot1 import VIDEOS_DIR, FlowVideoCDP


async def clear_composer_strict(flow):
    await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
    await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
    await asyncio.sleep(0.35)
    for _ in range(3):
        removed = await flow.js("""
        (() => {
            let n = 0;
            const clearAll = document.querySelector('button[aria-label="Xoá câu lệnh"]');
            if (clearAll && clearAll.getBoundingClientRect().width > 0) {
                clearAll.click();
                n++;
            }
            const chips = Array.from(document.querySelectorAll('button[aria-label="Thành phần"]'));
            for (const c of chips) {
                if (c.getBoundingClientRect().width > 0) {
                    c.click();
                    n++;
                }
            }
            const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
            if (el && (el.innerText || '').trim().length > 0) {
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
            }
            return document.querySelectorAll('button[aria-label="Thành phần"]').length;
        })()
        """)
        await asyncio.sleep(0.35)
        if removed == 0:
            break


async def attach_single_ingredient_verified(flow, identifier):
    """Attach strictly ONE verified ingredient (by UUID or filename) and confirm preview matches before adding."""
    await flow.find_and_trusted_click("aria === 'Thêm thành phần vào ô nhập câu lệnh'", "open '+' modal")
    await asyncio.sleep(0.9)

    # Check if already previewed on right pane!
    async def check_preview_and_option():
        return await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(identifier)};
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            let targetOpt = null;
            for (const el of opts) {{
                const txt = (el.innerText || '').trim();
                const src = el.querySelector('img')?.src || '';
                if (txt.includes(idStr) || src.includes(idStr)) {{
                    targetOpt = {{
                        txt: txt.replace(/\\s+/g, ' ').slice(0, 60),
                        uuid: src.split('?')[0].split('/').pop()
                    }};
                    break;
                }}
            }}
            const addBtn = Array.from(document.querySelectorAll('button')).find(
                b => (b.innerText || '').trim() === 'Thêm vào câu lệnh' && b.getBoundingClientRect().width > 0
            );
            const bigImgs = Array.from(document.querySelectorAll('img')).filter(i => {{
                const r = i.getBoundingClientRect();
                return r.width > 170 && r.height > 100 && (i.src || '').includes('flow-content.google/image/');
            }}).map(i => (i.src || '').split('?')[0]);
            return {{targetOpt, hasAddBtn: Boolean(addBtn), bigImgs}};
        }})()
        """)

    st = await check_preview_and_option()
    if not st["targetOpt"]:
        # Use search input inside modal
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
            await flow.js("""
            (() => {
                const inp = document.querySelector('[aria-label="Tìm kiếm thành phần"]');
                if (inp) { inp.select(); }
            })()
            """)
            q = identifier.replace(".jpg", "")
            await flow.call("Input.insertText", {"text": q})
            await asyncio.sleep(0.9)
            st = await check_preview_and_option()

    if not st["targetOpt"]:
        raise RuntimeError(f"Ingredient {identifier!r} not found in modal options!")

    target_uuid = st["targetOpt"]["uuid"]
    already_previewed = any(target_uuid in u for u in st["bigImgs"]) and st["hasAddBtn"]
    print(f"  Modal state for {identifier!r} (uuid={target_uuid[:10]}): already_previewed={already_previewed}, bigImgs={[u[-10:] for u in st['bigImgs']]}")

    if not already_previewed:
        # Scroll option to center and click its thumbnail image
        rect = await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(identifier)};
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const txt = (el.innerText || '').trim();
                const img = el.querySelector('img');
                const src = img?.src || '';
                if (txt.includes(idStr) || src.includes(idStr)) {{
                    el.scrollIntoView({{block: 'center'}});
                    const r = (img || el).getBoundingClientRect();
                    return {{cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)}};
                }}
            }}
            return null;
        }})()
        """)
        await asyncio.sleep(0.35)
        # Re-read rect after scroll settles
        rect = await flow.js(f"""
        (() => {{
            const idStr = {json.dumps(identifier)};
            const opts = Array.from(document.querySelectorAll('[role="option"]'));
            for (const el of opts) {{
                const txt = (el.innerText || '').trim();
                const img = el.querySelector('img');
                const src = img?.src || '';
                if (txt.includes(idStr) || src.includes(idStr)) {{
                    const r = (img || el).getBoundingClientRect();
                    return {{cx: Math.round(r.x + r.width / 2), cy: Math.round(r.y + r.height / 2)}};
                }}
            }}
            return null;
        }})()
        """)
        await flow.trusted_click(rect["cx"], rect["cy"])
        await asyncio.sleep(0.6)
        st2 = await check_preview_and_option()
        if not st2["hasAddBtn"] or not any(target_uuid in u for u in st2["bigImgs"]):
            # Click option container center once more if first click only focused list
            await flow.trusted_click(rect["cx"] + 40, rect["cy"])
            await asyncio.sleep(0.6)
            st2 = await check_preview_and_option()
        print(f"  After click preview check: hasAddBtn={st2['hasAddBtn']}, bigImgs={[u[-10:] for u in st2['bigImgs']]}")
        if not any(target_uuid in u for u in st2["bigImgs"]):
            raise RuntimeError(f"Preview UUID mismatch for {identifier!r}: expected {target_uuid}, got {st2['bigImgs']}")

    await flow.find_and_trusted_click("text === 'Thêm vào câu lệnh'", "Thêm vào câu lệnh")
    await asyncio.sleep(0.6)
    chip_count = await flow.js("document.querySelectorAll('button[aria-label=\"Thành phần\"]').length")
    print(f"  Attached {identifier!r} cleanly (composer chip_count={chip_count})")


async def generate_image_strict(flow, key_name, ingredients, prompt):
    print(f"\n=== STRICT GENERATING {key_name} ===")
    await flow.find_and_trusted_click("text.includes('Tất cả nội dung') && r.x < 240", "All media tab")
    await asyncio.sleep(0.8)
    await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
    await asyncio.sleep(0.4)
    await flow.ensure_image_16x9_pro()
    await clear_composer_strict(flow)

    before_imgs = await flow.js("""
    Array.from(document.querySelectorAll('img'))
        .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth, nh: i.naturalHeight}))
        .filter(i => i.src.includes('flow-content.google/image/'))
    """)
    before_uuids = {im["src"].split("?")[0] for im in before_imgs}

    for ing in ingredients:
        await attach_single_ingredient_verified(flow, ing)

    ed_rect = await flow.js("""
    (() => {
        const el = document.querySelector('[aria-label="Bạn muốn tạo những gì?"], [aria-label="Bạn muốn tạo gì?"], [contenteditable="true"]');
        const r = el.getBoundingClientRect();
        return {cx: Math.round(r.x + r.width/2), cy: Math.round(r.y + r.height/2)};
    })()
    """)
    await flow.trusted_click(ed_rect["cx"], ed_rect["cy"])
    await asyncio.sleep(0.2)
    await flow.call("Input.insertText", {"text": prompt})
    await asyncio.sleep(0.5)

    btns = await flow.js("""
    Array.from(document.querySelectorAll('[aria-label="Bắt đầu tạo"]')).map(el => {
        const r = el.getBoundingClientRect();
        const cx = Math.round(r.x + r.width / 2);
        const cy = Math.round(r.y + r.height / 2);
        const topEl = document.elementFromPoint(cx, cy);
        const hit = Boolean(topEl && (el === topEl || el.contains(topEl)));
        return {cx, cy, hit, disabled: el.disabled};
    })
    """)
    target = next((b for b in btns if b["hit"] and not b["disabled"]), None)
    if not target:
        raise RuntimeError(f"Submit button not enabled for {key_name}: {btns}")
    await flow.trusted_click(target["cx"], target["cy"])
    print(f"  Submitted {key_name}, polling...")

    new_img = None
    for step in range(45):
        await asyncio.sleep(2.0)
        await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0 && !el.closest('[role=\"dialog\"]')) el.scrollTop = 0; });")
        cur_imgs = await flow.js("""
        Array.from(document.querySelectorAll('img'))
            .map(i => ({src: i.currentSrc || i.src || '', nw: i.naturalWidth, nh: i.naturalHeight}))
            .filter(i => i.src.includes('flow-content.google/image/'))
        """)
        for im in cur_imgs:
            base = im["src"].split("?")[0]
            if base not in before_uuids and im["nw"] >= 1000:
                new_img = im
                break
        pct = await flow.js("""
        Array.from(document.querySelectorAll('div, span'))
            .map(e => (e.innerText || '').trim())
            .filter(t => /^\\d+%$/.test(t))
        """)
        print(f"    [{(step+1)*2}s] progress={pct}, found={bool(new_img)}")
        if new_img:
            break

    if not new_img:
        raise RuntimeError(f"Timeout waiting for {key_name}")

    b64 = await flow.js(f"""
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
    out_file = os.path.join(FRAMES_DIR, f"{key_name}.jpg")
    with open(out_file, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"  SAVED {key_name}: {new_img['nw']}x{new_img['nh']} -> {out_file}")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    manifest[key_name] = {
        "uuid": new_img["src"].split("?")[0].split("/")[-1],
        "base_url": new_img["src"].split("?")[0],
        "full_url": new_img["src"],
        "width": new_img["nw"],
        "height": new_img["nh"],
        "local_path": out_file,
    }
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return manifest[key_name]


async def main():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    ref_sigs = {
        k: extract_mid_frame_rgb_mean(os.path.join(VIDEOS_DIR, f"{k}.mp4"))
        for k in ["shot1_v1", "shot2_v1", "shot3_v1", "shot4_v1", "shot4_v2"]
        if os.path.exists(os.path.join(VIDEOS_DIR, f"{k}.mp4"))
    }

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=80 * 1024 * 1024) as ws:
        flow = FlowVideoCDP(ws)
        await flow.call("Page.enable")

        # 1. Export native Flow 1080p for shot4_v2 (top-left card in Video tab: x=248, y=82, w=452, h=254)
        shot4_hd = os.path.join(HD_DIR, "shot4_v2_1080p.mp4")
        if not os.path.exists(shot4_hd):
            print("=== Step 1: Exporting Native Google Flow 1080p for shot4_v2 ===")
            await flow.find_and_trusted_click("text.includes('videocam') && text.includes('Video') && r.x < 240", "Video tab")
            await asyncio.sleep(1.2)
            await flow.js("window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop > 0) el.scrollTop = 0; });")
            await asyncio.sleep(0.6)
            top_left_card = {"x": 248, "y": 82, "w": 452, "h": 254, "cx": 474, "cy": 209}
            ok = await download_1080p_strict(flow, top_left_card, "shot4_v2", ref_sigs, timeout_s=95)
            print(f"  shot4_v2 native 1080p download result: {ok}")

        shot1_end_uuid = manifest["shot1_end"].get("uuid") or manifest["shot1_end"]["base_url"].split("/")[-1]

        # 2. Generate shot1_start_v2 strictly from shot1_end ONLY (ZERO center-pad daisies, EXACT 4 white daisy stems!)
        prompt_shot1_start_v2 = (
            "16:9 widescreen surgical pre-drop state edit of this exact 16:9 sunlit cafe breakfast table reference image. "
            "PRESERVE 100% IDENTICAL CAMERA, FRAMING, BACKGROUND, TABLETOP, AND LIGHTING FROM THE REFERENCE IMAGE: "
            "exact same 16:9 camera angle, focal length, glossy cream-stone tabletop, glass jar of chamomile flowers on the far left, wooden chair and flaky croissant on white scalloped plate on the far right, and exact same warm morning window sunbeams. "
            "CHANGE ONLY TWO PHYSICAL STATES FOR THE PRE-DROP MOMENT: "
            "1) Lift the exact same cream-white ceramic hot tea mug straight vertically upward by 3.5 cm so its base hovers 3.5 cm in mid-air directly above the center of the green crochet coaster, held gently from the right side by a clean manicured female right hand gripping ONLY the mug handle, poised to lower it straight down onto the coaster. "
            "2) Unfold the matcha-green crochet coaster into its completely FLAT 0-degree resting state on the glossy table surface while keeping STRICT 1:1 TOPOLOGY WITH THE REFERENCE COASTER: "
            "the round matcha-green crochet center pad with light pastel-green scalloped border is 100% PLAIN SOLID GREEN CROCHET YARN WITH ZERO FLOWERS ON THE CENTER PAD (completely empty clean green crochet center pad, NO white flowers on top of the pad!), "
            "and unfold ONLY the EXACT 4 thin green crochet yarn stems (each with one tiny green crochet leaf and one SMALL dainty ~2.2cm white crochet daisy with yellow center, positioned at front-left 8 o'clock, back-left 10 o'clock, front-right 4 o'clock, and back-right 2 o'clock) so those exact 4 daisy stems lie COMPLETELY FLAT horizontally at 0 degrees resting directly on the tabletop radiating outward from the pastel-green rim (NOT standing upright, NOT floating, strictly 4 small miniature crochet daisies outside the rim and 0 flowers on the center pad). "
            "85mm commercial macro lens, crisp cotton yarn stitches, NO text, NO logos, NO watermarks."
        )
        await generate_image_strict(flow, "shot1_start_v2", [shot1_end_uuid], prompt_shot1_start_v2)

        # 3. Generate shot5_end (Product 1 Style A Matcha-Green 4-Daisy Coaster + Clear Iced Matcha Latte Glass)
        prompt_shot5_end = (
            "16:9 widescreen commercial product hero photograph of the exact handmade matcha-green crochet coaster with light pastel-green scalloped border and 4 miniature white crochet daisy stems from the reference image, holding a clear cylindrical glass cup of layered iced green matcha milk latte (white milk bottom layer, vibrant ceremonial matcha green top layer with ice cubes) on a sunlit pale birch-wood cafe desk. "
            "PRESERVE 100% IDENTICAL CROCHET COASTER GEOMETRY AND MINIATURE DAISY SCALE FROM THE REFERENCE: "
            "round matcha-green crochet yarn center pad (plain solid green center pad under the glass) with light pastel-green scalloped crochet border, and EXACTLY 4 thin green crochet yarn stems (each with one tiny green crochet leaf and one SMALL dainty ~2.2cm 6-petal white crochet daisy with tiny yellow yarn center — strictly small miniature crochet daisies matching the reference 1:1, NEVER giant or oversized petals) standing VERTICALLY UPRIGHT at 90 degrees from the coaster rim at 8 o'clock, 10 o'clock, 4 o'clock, and 2 o'clock hugging the lower-middle sides of the clear iced matcha latte glass (~60% up the glass height), plus the 2 subtle low green yarn loops at left and right rim. "
            "Compose as a clean airy 16:9 horizontal website hero banner at a 25-degree tabletop angle on a sunlit pale Scandinavian birch wooden table with soft morning window sunbeams, an open linen-bound book softly blurred on the far left, and a small ceramic saucer with a matcha macaron softly blurred on the far right. "
            "85mm commercial macro lens, razor-sharp cotton crochet stitches, NO hands, NO text, NO logos, NO watermarks."
        )
        await generate_image_strict(flow, "shot5_end", ["PROD1_STYLE_A_POPUP_MUG_CLEAN.jpg"], prompt_shot5_end)

        # 4. Generate shot6_end (Product 2 Dual-Coaster 16:9 Scene from PROD2_IMG_01.jpg)
        prompt_shot6_end = (
            "16:9 widescreen commercial product hero photograph expanding the exact dual handmade crochet flower coaster scene from the reference image into a balanced 16:9 horizontal website banner on the exact warm sunlit oak dining table in a cozy sunlit cottage living room. "
            "PRESERVE 100% IDENTICAL PRODUCT DETAILS AND MINIATURE FLOWER PROPORTIONS FROM THE REFERENCE IMAGE: "
            "1) On the left-center of the 16:9 frame: the dark soil-brown crochet center pad with bright lime-green ruffled grass border holding the exact hand-painted cream-and-blue floral ceramic mug (with handle on the right), surrounded by the exact 2-tier miniature ~3cm yellow crochet sunflowers with dark brown yarn centers on thin green crochet stems standing VERTICALLY UPRIGHT at 90 degrees (2 tall side sunflower stems at 9 o'clock and 3 o'clock reaching mug rim height + 2 shorter front sunflower stems at 7 o'clock and 5 o'clock reaching halfway up the mug, strictly miniature scale matching the reference 1:1, NEVER oversized petals). "
            "2) On the right-center of the 16:9 frame beside it on the wooden table: the companion round moss-green spiral crochet coaster with cream-white scalloped border lying open flat with its 6 thin green crochet stems, sage leaves, and small compact ~2.2cm red and pink crochet rosebuds resting flat on the oak table. "
            "Soft bokeh stone fireplace and sunlit cottage windows in the background, folded linen napkin and small plate of cookies on the far right edge, warm morning sunlight. "
            "85mm commercial macro lens, crisp handmade yarn stitches, NO hands, NO text, NO logos, NO watermarks."
        )
        await generate_image_strict(flow, "shot6_end", ["PROD2_IMG_01.jpg"], prompt_shot6_end)
        await clear_composer_strict(flow)

    shutil.rmtree(DL_TMP, ignore_errors=True)
    print("\n=== Completed Strict Step 1: shot4_v2_1080p + shot1_start_v2 + shot5_end + shot6_end ===")


if __name__ == "__main__":
    asyncio.run(main())
