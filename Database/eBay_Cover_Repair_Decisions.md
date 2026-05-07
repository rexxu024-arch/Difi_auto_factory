# eBay Cover Repair Decisions

Generated: 2026-05-07 00:06:18 America/New_York

## Learned Rule

- eBay Reports cannot revise variation pictures for these Printify-synced inventory-managed listings. The failed result returned: Items that are managed by Inventory do not allow Add/Delete variation pictures.
- The current safe path is source repair in Printify, followed by a Printify re-sync and live eBay cover audit.
- If source re-sync still cannot change a live Inventory-managed listing, create a correct replacement listing and retire the bad listing after verification.

## Counts

- NON_STICKER_REVIEW_REQUIRED: 4
- RETIRED_REPLACED_DONE: 33
- SOURCE_REPAIR_REQUIRED: 12

## Product Types

- Acrylic: 2
- Poster: 2
- Sticker: 45

CSV: `C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv`
