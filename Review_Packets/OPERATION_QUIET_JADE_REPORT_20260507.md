# Operation Quiet Jade Report - 2026-05-07 01:36 EDT

## Objective

Rex/Grey strategy: stop relying on generic crowded terms and push the live zero-view eBay set toward higher-intent buyer language:

- Smoky Jade
- Quiet Luxury Apartment Decor
- Deep Work Visuals
- Reading Nook / Scholar Room / Wabi Sabi

## Scope

Targeted the latest zero-view active eBay set from `Database/Performance_Log.csv`.

- Total modified: 42
- Poster: 16
- Acrylic: 17
- Sticker: 9

Pricing guard:

- Poster: held at `$34.99`
- Acrylic: held at `$89.99` because `$29.99-$34.99` would violate cost + shipping + fee guardrails
- Sticker: held at `$11.99` as review/trust-friendly low-ticket products

## Execution

Local source of truth updated:

- `Database/eBay_listing.xlsx`
- rollback: `Database/eBay_Quiet_Jade_Rollback.csv`
- plan: `Database/eBay_Quiet_Jade_Pivot.csv`
- Printify verification: `Database/eBay_Quiet_Jade_Verify.csv`
- Printify sync log: `Database/eBay_Quiet_Jade_Sync_Log.csv`
- eBay UI fallback log: `Database/eBay_UI_Title_Revise_Log.csv`

Printify API path:

- Updated title, description, and enabled variant price.
- Published only title/description/variants.
- `images=false`, `shipping_template=false`, no buyer/payment/order fields touched.
- Result: 42/42 Printify API readback OK.

eBay UI fallback:

- Seller Hub initially showed only 25/42 title changes.
- 17 stuck rows were revised through the dedicated Edge CDP profile using title-only Seller Hub revise pages.
- Final Seller Hub active snapshot: 42/42 target titles visible, 42/42 prices match.

## Quality Notes

- eBay title length preserved at 75-79 characters.
- Removed direct use of known crowded phrase patterns such as `Zen Poster` and `Green Canvas`.
- Buyer-facing description note retained:
  Main image is the physical product customers receive; extra gallery images are concept/detail/reference views, not extra products or selectable variations.
- No image order, Printify mockup, payment, order, shipping policy, or PPC/Priority ad setting was modified.

## Next Readout

Check the next 24-48 hours for:

- impressions/views lift compared with prior zero-view baseline
- whether Poster/Acrylic continue outperforming Sticker
- whether Quiet Jade terms generate any watch/favorite/buyer-page movement

If still 0-view after 48 hours, treat this as an eBay account/search-surface issue rather than a pure copy issue and pivot more effort to Etsy/digital and higher-demand product-category tests.
