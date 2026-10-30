import asyncio
import json
import os
import sys
import urllib.request
import websockets

sys.path.insert(0, "/Users/dudumac5/Documents/antigravity/wonderful-lavoisier/flow_web_intro")
from gen_batch_images import FlowCDP
from run_barrel20_images_silent import (
    OUT_DIR,
    PORT,
    PROJECT_ID,
    SCENES_20,
    UUID_CACHE_PATH,
    exit_edit_view_if_needed,
    open_ingredient_modal,
)

SCENE_UUIDS_PATH = os.path.join(OUT_DIR, "barrel20_scene_uuids.json")

# Known SKU #1 generated UUIDs (to exclude cleanly)
SKU1_UUIDS = {
    "3d63c790-7d60-4f2d-bce6-05114ca84031",
    "d81a1ece-9b49-4d8f-8576-510de683db46",
    "e89c5d87-3173-42d1-85ae-4a4edd69bb76",
    "5d275a3e-f828-4419-854f-a70ae267077a",
    "7a13b09d-c6cd-4dac-8732-d828f3a5429f",
    "65f2c152-5db9-4ca7-8996-7dfd76b2ce9e",
    "7ef37782-5c33-4d76-972c-49b87d27735b",
    "4f63712c-37c9-433d-8457-a47e3672cf34",
    "56d84fb5-e098-432f-89ad-3c2b54ae048c",
    "ebc19d89-96d5-431c-bf48-65672b2852ec",
    "94476b2c-f110-4c1a-9c08-ee3d514ccc6c",
    "72972fcc-5a93-464b-8324-399a9185d9d2",
    "7cf09a22-e08a-4bb0-9634-ef73a6450557",
    "80fe0aac-30fb-4d56-9fc3-8cd36fdeeba0",
    "c8560aa3-3ce7-401f-831e-7cee9e229b90",
    "88270262-e787-4d12-809c-1c3fb0a01be9",
    "255b13ff-e051-4f6b-8fc6-5de808f483de",
    "357a083b-bb15-4391-8461-42c738a6d409",
    "03731287-04a9-477e-a037-843e39e6cdf2",
    "2a636fef-0562-4470-ad3d-8ff399015f8f",
}


async def main():
    plate_uuids = set()
    if os.path.exists(UUID_CACHE_PATH):
        with open(UUID_CACHE_PATH, "r") as f:
            plate_uuids = set(json.load(f).values())

    tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list").read())
    t = next((x for x in tabs if PROJECT_ID in (x.get("url") or "")), None)
    if not t:
        raise RuntimeError(f"Flow tab for project {PROJECT_ID} not found!")

    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=30 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        await flow.call("Page.enable")
        await flow.call("DOM.enable")
        await flow.call("Emulation.setFocusEmulationEnabled", {"enabled": True})

        await exit_edit_view_if_needed(flow)
        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(0.35)

        # Scan strict newest-first list in '+' ingredient picker
        await open_ingredient_modal(flow)
        await flow.js("""
        (() => {
            const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
            if (vp) vp.scrollTop = 0;
        })()
        """)
        await asyncio.sleep(0.4)

        ordered = []
        seen = set()
        for _ in range(25):
            items = await flow.js("""
            Array.from(document.querySelectorAll('[role="option"]'))
                .map(el => ({
                    top: el.getBoundingClientRect().top,
                    txt: (el.innerText || '').trim().replace(/\\s+/g, ' '),
                    uuid: (el.querySelector('img')?.src || '').split('?')[0].split('/').pop()
                }))
                .sort((a, b) => a.top - b.top)
            """)
            for it in items:
                u = it["uuid"]
                if not u or u in seen:
                    continue
                seen.add(u)
                ordered.append(it)
            if len(ordered) >= 35:
                break
            moved = await flow.js("""
            (() => {
                const vp = document.querySelector('cdk-virtual-scroll-viewport[role="listbox"]') || document.querySelector('cdk-virtual-scroll-viewport');
                if (!vp) return false;
                const prev = vp.scrollTop;
                vp.scrollTop += 260;
                return vp.scrollTop > prev;
            })()
            """)
            if not moved:
                break
            await asyncio.sleep(0.28)

        await flow.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape"})
        await flow.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape"})
        await asyncio.sleep(0.3)

        filtered = [
            it for it in ordered
            if it["uuid"] not in plate_uuids
            and it["uuid"] not in SKU1_UUIDS
            and "BARREL_PLATE_" not in it["txt"]
            and "BARREL_REF_" not in it["txt"]
            and "PLATE_0" not in it["txt"]
            and "CEDAR_REF_" not in it["txt"]
        ]

        print(f"Found {len(filtered)} new generated Barrel SKU images (expected 20):")
        for idx, it in enumerate(filtered[:22]):
            print(f"  [{idx:02d}] {it['uuid']} | {it['txt'][:95]}")

        if len(filtered) < 20:
            raise RuntimeError(f"Expected 20 generated barrel images, found only {len(filtered)}!")

        # Newest-first: filtered[0] == B20, filtered[19] == B01
        newest_20 = filtered[:20]
        oldest_to_newest = list(reversed(newest_20))

        mapping = {}
        print("\n=== MAPPED 1-TO-1 SCENE -> FLOW IMAGE UUID ===")
        for sc, it in zip(SCENES_20, oldest_to_newest):
            mapping[sc["key"]] = it["uuid"]
            print(f"  {sc['key']:42s} -> {it['uuid']} | caption={it['txt'][:65]}")

        with open(SCENE_UUIDS_PATH, "w") as f:
            json.dump(mapping, f, indent=2)
        print(f"\nSaved 20 exact scene UUIDs to {SCENE_UUIDS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
