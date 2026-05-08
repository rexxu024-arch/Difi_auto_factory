# Multi-Track Experiment Plan

Generated: 2026-05-07 23:45:37 -0400

## Guardrails Now Active
- 165 experiment slots are split equally: 55 low-competition niche, 55 high-volume value, 55 digital pure-profit.
- Etsy fee kill switch is active: $2/batch, $6/day. Confirmed Etsy spend today: $0.00.
- Image QA is active. `SHADOW_CLIPPING`, `LOW_RESOLUTION`, and `HIGHLIGHT_CLIPPING` are hard HOLD states.
- Sticker Cover Gate remains active: cover-safe official mockups only for marketplace publishing.
- eBay ads remain General / Promoted Listings Standard fixed 2%, never Priority/PPC.

## Track A - Low-Competition Niche
Objective: Force non-zero traffic through long-tail room-use and buyer-scene terms.

| ID | Action | Intent | QA | Price |
|---|---|---|---|---|
| Acrylic-Zen-0003 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | reading nook decor | READY | $89.99 |
| Poster-Academia-0023 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | home library wall art | READY | $34.99 |
| Acrylic-Zen-0005 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | tea room accent | READY | $89.99 |
| Acrylic-Grimdark-0001 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | dark study room decor | READY | $89.99 |
| Acrylic-Grimdark-0032 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | collector shelf object | READY | $89.99 |
| Acrylic-Grimdark-0031 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | smoky jade relic | READY | $89.99 |
| Acrylic-Grimdark-0017 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | gothic shelf decor | READY | $89.99 |
| Acrylic-Grimdark-0009 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | moody desk display | READY | $89.99 |

## Track B - High-Volume Value
Objective: Test broad-volume value terms with Rex-grade visuals and safe pricing.

| ID | Action | Intent | QA | Price |
|---|---|---|---|---|
| Poster-Academia-0003-FIX1 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | wall art poster | READY | $29.99-$34.99 |
| Poster-Academia-0020 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | gallery wall decor | READY | $29.99-$34.99 |
| Poster-Zen-0005 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | apartment wall art | READY | $29.99-$34.99 |
| Poster-Academia-0008 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | poster print | READY | $29.99-$34.99 |
| Acrylic-Grimdark-0016 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | office decor | READY | $79.99-$89.99 |
| Acrylic-Grimdark-0081-FIX1 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | acrylic photo block | READY | $79.99-$89.99 |
| Acrylic-Grimdark-0008 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | desk display | READY | $79.99-$89.99 |
| Acrylic-Grimdark-0037 | COPY_OR_PRICE_EXPERIMENT_ON_EXISTING_LISTING | shelf decor | READY | $79.99-$89.99 |

## Track C - Digital Pure Profit
Objective: Use zero-production-cost Etsy digital downloads to test SEO templates cheaply.

| ID | Action | Intent | QA | Price |
|---|---|---|---|---|
| Poster-Academia-0008 | NEXT_ETSY_GRAY_BATCH_UNDER_FEE_CAP | book lover gift | READY | $6.99 |
| Poster-Academia-0010 | NEXT_ETSY_GRAY_BATCH_UNDER_FEE_CAP | reading nook printable | READY | $6.99 |
| Poster-Academia-0014 | NEXT_ETSY_GRAY_BATCH_UNDER_FEE_CAP | instant download gift | READY | $6.99 |
| Poster-Academia-0030 | NEXT_ETSY_GRAY_BATCH_UNDER_FEE_CAP | book lover gift | READY | $6.99 |
| Poster-Academia-0026 | NEXT_ETSY_GRAY_BATCH_UNDER_FEE_CAP | reading nook printable | READY | $6.99 |
| Poster-Academia-0027 | NEXT_ETSY_GRAY_BATCH_UNDER_FEE_CAP | instant download gift | READY | $6.99 |
| Poster-Academia-0028 | NEXT_ETSY_GRAY_BATCH_UNDER_FEE_CAP | book lover gift | READY | $6.99 |
| Poster-Academia-0084 | MONITOR_LIVE_DIGITAL_TRAFFIC | reading nook printable | READY | $6.99 |

## QA Hold Pool
- HOLD rows are excluded from the 165 experiment capacity and written as `QA_HOLD_POOL`.
- HOLD count in this run: 60.

## Executed Experiment Batches
- Synced `A_LOW_COMPETITION_NICHE` copy rows: 5

Latest copy-monitor report, when present: `Review_Packets/MULTI_TRACK_COPY_MONITOR_20260507.md`.

## Next Operator Move
1. Do not spend additional Etsy listing fees until the next gray cell is selected from Track C and the fee ledger is reconciled.
2. Use Track A first if eBay remains a 0-view channel: the goal is non-zero search entry, not immediate conversion.
3. Use Track B only after the cover/product image is clean, because broad-volume terms punish weak thumbnails faster.
4. If Track C first paid cells remain 0 views, stop fee spend and rewrite SEO using the Buyer Persona vs Room Use result split.

## References
- Etsy fees: https://www.etsy.com/legal/fees/
- Etsy Seller Handbook / marketplace insight workflow: https://www.etsy.com/seller-handbook
- eBay Promoted Listings Standard: https://www.ebay.com/sellercenter/ebay-for-business/marketing/promoted-listings-standard
