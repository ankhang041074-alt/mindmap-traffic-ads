import asyncio
import json
import os
import websockets

from gen_batch_images import FlowCDP, MANIFEST_PATH, get_flow_ws_url


async def main():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    shot2_end_uuid = manifest["shot2_end"]["uuid"]
    shot3_end_uuid = manifest["shot3_end"]["uuid"]
    shot4_end_uuid = manifest["shot4_end"]["uuid"]

    jobs = [
        (
            "shot2_start",
            [shot2_end_uuid],
            (
                "16:9 widescreen surgical pre-drop state edit of the reference 16:9 sunlit oak desk image. "
                "PRESERVE 100% IDENTICAL CAMERA, FRAMING, BACKGROUND, AND LIGHTING FROM THE REFERENCE IMAGE: exact same 16:9 camera angle, focal length, sunlit honey-oak wooden desk grain, white ceramic plant pot on woven rattan mat on the left, closed cream linen notebook on the right, and exact same warm morning window sunbeams. "
                "CHANGE ONLY TWO PHYSICAL STATES FOR THE PRE-DROP MOMENT: "
                "1) Lift the exact same glossy mustard-yellow ceramic coffee mug straight vertically upward by 4 cm so its base hovers 4 cm in mid-air directly above the center of the brown-and-green crochet coaster, held gently from the right side by a clean manicured female right hand gripping the yellow mug handle, poised to set it down onto the coaster. "
                "2) Unfold the crochet sunflower coaster into its completely FLAT 0-degree resting state on the wooden desk surface: the dark soil-brown crochet pad with bright lime-green ruffled crochet grass border lies flat on the oak tabletop, and all thin green crochet yarn stems with small green crochet leaves and SMALL ~3cm yellow crochet sunflowers with dark brown yarn centers lie COMPLETELY FLAT horizontally at 0 degrees resting directly on the wooden desk radiating outward around the lime-green coaster rim (NOT standing upright, NOT floating in air, strictly small miniature crochet sunflowers matching the reference scale, NEVER oversized petals). "
                "85mm commercial macro lens, crisp cotton yarn stitches, NO text, NO logos, NO watermarks."
            ),
        ),
        (
            "shot3_start",
            [shot3_end_uuid, "PROD2_STYLE_B_ROSE_FLAT_ISOLATED.jpg"],
            (
                "16:9 widescreen surgical pre-drop state edit of the first 16:9 walnut table reference image, using the second reference image strictly for the flat unfolded state of the green-and-cream crochet rosebud coaster. "
                "PRESERVE 100% IDENTICAL CAMERA, FRAMING, BACKGROUND, AND LIGHTING FROM THE FIRST 16:9 IMAGE: exact same 16:9 camera angle, focal length, warm sunlit walnut wooden tabletop, blurred cozy fireplace living room background, blurred green plant leaves in bottom-left corner, and folded striped linen napkin with plate of butter cookies on the far right. "
                "CHANGE ONLY TWO PHYSICAL STATES FOR THE PRE-DROP MOMENT: "
                "1) Lift the exact same clear cylindrical glass cup of layered iced milk latte straight vertically upward by 4 cm so its glass bottom hovers 4 cm in mid-air directly above the center of the green crochet coaster, held lightly from the upper-right by a clean manicured female right hand gripping the upper rim/side of the glass without blocking the front view of the coaster below. "
                "2) Unfold the moss-green spiral crochet coaster with cream-white scalloped border into its completely FLAT 0-degree resting state on the walnut tabletop (matching the second reference image 1:1): the round moss-green pad with cream scalloped border lies flat on the wood, and all 6 thin green crochet yarn stems with veined sage-green crochet leaves and SMALL tight spherical ~2.2cm crochet rosebuds (alternating crimson-red and dusty-pink) lie COMPLETELY FLAT horizontally at 0 degrees resting directly on the wooden table surface radiating outward around the cream border (NOT standing upright, NOT floating in mid-air, strictly small compact crochet rosebuds, NEVER giant open roses). "
                "85mm commercial macro lens, crisp cotton yarn stitches, NO text, NO logos, NO watermarks."
            ),
        ),
        (
            "shot4_start",
            [shot4_end_uuid, "IMG_01_CLEAN_NO_TEXT.jpg"],
            (
                "16:9 widescreen surgical pre-drop state edit of the first 16:9 sunlit light-oak desk corner reference image, using the second reference image strictly for the flat unfolded state of the matcha-green crochet white daisy coaster. "
                "PRESERVE 100% IDENTICAL CAMERA, FRAMING, BACKGROUND, AND LIGHTING FROM THE FIRST 16:9 IMAGE: exact same 38-degree elevated 16:9 camera angle, focal length, sunlit minimalist light-oak desk corner, and exact same warm morning window leaf shadows. "
                "CHANGE ONLY TWO PHYSICAL STATES FOR THE PRE-DROP MOMENT: "
                "1) Lift the exact same smooth glossy white wireless earbuds charging case straight vertically upward by 4 cm so it hovers 4 cm in mid-air directly above the center of the matcha-green crochet coaster, held lightly from the upper-right by a clean manicured female right hand (thumb and fingertips gently holding the top edges of the white case, poised to place it down onto the green pad). "
                "2) Flatten the matcha-green crochet daisy coaster into its completely FLAT 0-degree unfolded resting state on the light-oak desk surface (matching the second reference image): the round matcha-green crochet pad with light pastel-green scalloped border lies flat on the wooden desk (showing 3 tiny flat white crochet daisies sewn on the green pad), and all 6 thin 2.5mm green crochet yarn stems with tiny green crochet leaves and SMALL dainty 2.2cm 5-petal white crochet daisies with yellow centers lie COMPLETELY FLAT horizontally at 0 degrees resting directly on the wooden tabletop radiating outward around the coaster rim (NOT standing upright, NOT curled into a basket yet, strictly miniature crochet daisies, NEVER large petals). "
                "85mm commercial macro lens, razor-sharp cotton crochet stitches, NO text, NO logos, NO watermarks."
            ),
        ),
    ]

    ws_url = get_flow_ws_url()
    async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
        flow = FlowCDP(ws)
        await flow.call("Page.enable")
        for key_name, ingredients, prompt in jobs:
            await flow.generate_image(key_name, ingredients, prompt)
            await asyncio.sleep(1.0)


if __name__ == "__main__":
    asyncio.run(main())
