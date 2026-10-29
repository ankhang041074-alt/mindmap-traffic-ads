import asyncio
import json
import os
import shutil
import urllib.request

import download_remaining_1080p
import assemble_web_intros
from gen_video_shot1 import VIDEOS_DIR


def main():
    print("=== STEP 1: Download Remaining Native Flow 1080p Upscales ===")
    asyncio.run(download_remaining_1080p.main())

    print("\n=== STEP 2: Assemble 16:9 1920x1080 Web Intro Master Deliverables & 2fps Contact Sheets ===")
    assemble_web_intros.main()

    print("\n=== STEP 3: Cleanup Empty Temp Download Folders & Verify Live Browser Health ===")
    for sub in ["dl_tmp", "dl_1080p"]:
        p = os.path.join(VIDEOS_DIR, sub)
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
            print(f"  Removed temporary dir: {p}")

    from home_helper import list_cdp_tabs
    cdp_base, tabs = list_cdp_tabs()
    flow_tabs = [t for t in tabs if "e77d4088-8126-4cb4-8d09-edec09be18ff" in t.get("url", "")]
    print(f"  Live AdsPower Flow Project Tab Alive ({cdp_base}): {len(flow_tabs) > 0} (total tabs={len(tabs)})")
    if flow_tabs:
        print(f"  Tab Title: {flow_tabs[0].get('title')} | URL: {flow_tabs[0].get('url')}")


if __name__ == "__main__":
    main()
