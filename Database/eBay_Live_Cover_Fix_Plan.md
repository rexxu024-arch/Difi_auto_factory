# eBay Live Cover Fix Plan

Generated: 2026-05-05 22:46 America/New_York

## Current Finding

- Local `Cover_Mockup.png` files are present and correct for the audited Sticker listings.
- Printify product JSON can contain the correct cover at image index 0, but many products also expose a second `is_default=true` image.
- Live eBay active listings can show only the single U images in the variation photo set, with the local 4pc cover missing from the visible buyer gallery.
- A title/description-only sync cannot repair this. A Printify `images=true` publish attempt on `Sticker-Zen-0025` did not repair the live eBay gallery.
- Official Printify API docs confirm product mockup `images` are read-only in the product update model, so ordinary API product PUT is not a reliable repair path for existing mockup-image defaults. Reference: https://developers.printify.com/API-Doc-RREdits.html

## Affected Listings

- Audited published listings with eBay item ids: 99.
- Latest per-SKU results:
  - Correct live cover: 2.
  - Live main image matched a single U/detail image: 49.
  - Ambiguous but mostly acceptable single-image Poster/Acrylic cases: 48.
- Sticker result: 45/47 published Sticker rows show a single U image rather than the 4pc local cover.
- Non-sticker high-confidence review rows: 2 Poster, 2 Acrylic.
- Fix queue: `Database/eBay_Online_Cover_Fix_Queue.csv`.

## Immediate Guardrail

- `modules/printify_publish_scheduler.py` now blocks new publish attempts when Printify reports anything other than exactly one selected default image.
- Sticker expansion remains paused until the default-image / eBay-variation-photo issue is repaired.

## Repair Direction

1. Restore or create a deterministic image editor path:
   - Preferred: Printify UI mockup library once Chrome profile is logged back into Printify.
   - Fallback: create replacement listings from the same local assets with the fixed default-image gate, verify the live buyer cover, then retire the old inventory-managed listing.
2. For Sticker listings, the buyer-facing first image should be the local `Cover_Mockup.png` showing the 4pc set.
3. U images should stay as supporting detail images.
4. After any repair, run `modules/ebay_online_cover_audit.py --ids <SKU>` and compare against local files before marking the row fixed.

## Do Not Do

- Do not blindly click `Revise it` after opening the eBay editor.
- Do not rely on Printify API `images` order/default mutation; product mockup images are effectively read-only for this purpose.
- Do not continue broad publishing while `Printify_Image_Default_Audit.csv` reports duplicate default images.
