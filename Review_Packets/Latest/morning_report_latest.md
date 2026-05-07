# OpenClaw Morning Report

Generated: 2026-05-06 17:07 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 165
- Published through Printify/eBay tracking: 146
- Ready for Printify: 47

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 36, published 36, ready 1
- Sticker: stable 76, published 60, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 50
- Acrylic: 16
- Poster: 28
- Sticker: 6

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 01:23:31 -0400
- Rows read: 50
- 0-view rows in snapshot: 42
- Rows with at least 1 view: 8
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 96
- Unified registry rows bucketed: 255
- Etsy digital printable upload queue: 20 listings, max file 3.42MB, under 20MB limit: True
- Etsy digital previews: 20 listings x 3 preview images
- Etsy digital final upload packet: 20 listings, QA bad=0, missing=0
- Etsy digital bundle concepts: 3
- eBay cover QA rows: 14

## Unified Registry Buckets

- Etsy_Draft_Prepared: 32
- Fix_Gallery_First: 1
- Hold: 120
- Published_Has_View_Monitor: 8
- Published_Zero_View_Copy_Ad_Review: 28
- Ready_For_Printify_When_Network_OK: 47
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 36
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 31
- Cover replacement queue REPLACEMENT_PUBLISHED_LIVE_PASS: 14
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 7
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2
- Backlog WAIT_USER_OR_API_APPROVAL: 2

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
- supervisor:read_only_market: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Until wired/low-latency network is confirmed, prefer local low-bandwidth tasks and single-item network probes.
- No Etsy publish until Rex confirms listing-fee spend.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.
