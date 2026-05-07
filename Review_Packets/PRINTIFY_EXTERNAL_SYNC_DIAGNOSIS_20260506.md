# Printify External Sync Diagnosis - 2026-05-06

Generated: 2026-05-06 20:18:56  America/New_York

## Finding

`Poster-Academia-0038` through `Poster-Academia-0042` were previously marked as `Printify_Published_Mockups8`, but Printify product JSON still has `external = null` and the local workbook has no `eBay_Item_ID`. They are not confirmed eBay live listings.

## Action Taken

- Synced `Poster-Academia-0037` and recovered its eBay external id: `406909473606`.
- Corrected `Poster-Academia-0038` through `0042` to `Printify_PublishExternalPending_Mockups8`.
- Retried `Poster-Academia-0038` once via Printify publish API; response was 200, but external id remained missing.
- Updated `printify_publish_scheduler.py` so external-pending rows are not retried by default. Manual retry now requires `--retry-pending`.
- Updated scheduler accounting so ?published? means external eBay id confirmed, not merely Printify API returned 200.

## Interpretation

This is a sales-channel publish-route issue, not an asset/QA issue. The products exist in Printify with 8 selected mockups and correct variants, but eBay item creation was not confirmed. Continue asset creation and QA, but do not count these rows as live eBay inventory until `external.id` appears.

## Next Safe Path

1. Continue reading external ids with `printify_external_sync.py`.
2. Do not retry Printify `publish.json` blindly.
3. When eBay API access is approved, create/revise marketplace listings directly and call Printify `publishing_succeeded.json` only after the marketplace id is real.
4. If API is still blocked but browser login is stable, use dedicated automation Edge/Printify UI for a small one-listing publish proof before scaling.

## Official Reference Notes

Printify?s docs describe `publish.json` as a publish event/trigger and show that `external` is set by the sales channel using the `publishing_succeeded` endpoint. This supports treating missing `external.id` as not confirmed live inventory.



## Additional Proof - 2026-05-06 20:45:54 America/New_York

A fresh cover-only replacement draft `Sticker-Zen-0044-FIX1` was created and passed Printify production/design QA:

- Product ID: `69fbdfc9f60a24b6d1035f8b`
- Selected official mockups: 3
- Custom U/detail gallery images: 0
- Production visual match: PASS

Then `printify_publish_scheduler.py` called Printify `publish.json` once. HTTP returned 200, but `external.id` remained missing. The scheduler correctly kept `external_confirmed=0`.

This proves the blocker is not Poster-specific and not image-specific. It is the marketplace sales-channel publish route. Do not continue relying on Printify API publish for eBay live creation until eBay API or a verified UI publish path is available.
