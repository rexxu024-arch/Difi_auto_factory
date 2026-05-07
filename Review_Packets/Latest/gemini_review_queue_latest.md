# Gemini Advisor Review Queue

Generated: 2026-05-07 09:31 -0400 America/New_York

Rex is Commander, Gemini is Strategy Advisor, Codex is Executive Operator.

Please review the current OpenClaw plan as a strategy advisor. Do not request API keys, account secrets, payment data, buyer private data, or direct account actions.

## Report Summary

# OpenClaw Morning Report

Generated: 2026-05-07 09:31 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 161
- Published through Printify/eBay tracking: 145
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 53, ready 0
- Poster: stable 45, published 45, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-07 02:13:19 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 282
- Etsy digital printable upload queue: 20 listings, max file 3.42MB, under 20MB limit: True
- Etsy digital previews: 20 listings x 3 preview images
- Etsy digital final upload packet: 20 listings, QA bad=0, missing=0
- Etsy digital bundle concepts: 3
- Etsy Digital gray queue rows: 30
- Etsy Digital live listings: 10
- Etsy Digital confirmed listing-fee spend: $2.00
- Etsy Digital public audit active/readable: 10
- Etsy legacy listings retired/deleted: 2
- eBay cover QA rows: 14

## Unified Registry Buckets

- Etsy_Draft_Prepared: 4
- Fix_Gallery_First: 1
- Hold: 165
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 43
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 16

## eBay Traffic Experiment

- A_TITLE_INTENT_REWRITE: 18
- B_COVER_QA_PRIORITY: 14
- C_HOLDOUT_CONTROL: 12

## eBay Traffic Diagnosis

- Poster/Acrylic currently show more early movement than Sticker.: 1
- Promoted Listings Standard 2% is active but is not enough alone.: 1
- Sticker live cover/gallery mismatch is a primary blocker.: 1
- Title rewrite experiment has not produced a clear Sticker lift yet.: 1

## Live Cover Integrity

- Live eBay cover audit AMBIGUOUS: 48
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 59
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 33
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 12
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 6
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- eBay Promoted Listings Standard / General 2% is the only approved active ad mode; do not use Priority/PPC or suggested ad rates.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.


## Questions for Gemini

1. Given the first 10 Etsy Digital listings are live, what early signal should decide whether to spend the next $2 gray cell?
2. If the first 10 get 0 views after indexing, which search-intent variable should be changed first: title/category angle, product format, or visual theme?
3. Which three visual DNA themes should be expanded first if Etsy impressions appear but clicks remain low?
4. What ad test would you run first with a $3-5/day Etsy Ads budget after 48-72 hours of organic data?
5. Which product language sounds too mass-generated and should be softened before launch?

## Codex Action Filter

- Adopted:
- Deferred:
- Rejected:
- Requires Rex confirmation:
