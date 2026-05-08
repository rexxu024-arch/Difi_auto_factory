# OpenClaw Morning Report

Generated: 2026-05-07 22:21 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 139
- Published through Printify/eBay tracking: 126
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 42, published 42, ready 0
- Poster: stable 35, published 35, ready 0
- Sticker: stable 62, published 49, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-07 18:02:39 -0400
- Rows read: 44
- 0-view rows in snapshot: 40
- Rows with at least 1 view: 4
- General promoted rows in snapshot: 44

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 299
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

- Etsy_Draft_Prepared: 14
- Fix_Gallery_First: 1
- Hold: 194
- Published_Zero_View_Copy_Ad_Review: 28
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 16

## eBay Traffic Experiment

- A_TITLE_INTENT_REWRITE: 18
- B_COVER_QA_PRIORITY: 14
- C_HOLDOUT_CONTROL: 12

## eBay Traffic Diagnosis

- Cover Gate is cleared; the current blocker is traffic/product-market fit.: 1
- Poster/Acrylic currently show more early movement than Sticker.: 1
- Promoted Listings Standard 2% is active but is not enough alone.: 1
- Repeated or risky gallery images can suppress buyer trust and marketplace quality scoring.: 1
- Title rewrite experiment has not produced a clear Sticker lift yet.: 1

## Live Cover Integrity

- Live eBay cover audit AMBIGUOUS: 48
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 78
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 49
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38
- Printify gallery duplicate audit rows: 146
- Printify gallery duplicate audit CHECK_CUSTOM_GALLERY_REPEATS_RISK: 22
- Printify gallery duplicate audit OK: 124
- eBay live gallery duplicate audit rows: 25
- eBay live gallery duplicate audit CHECK_LIVE_PRIMARY_DUPLICATE_REVIEW: 3
- eBay live gallery duplicate audit OK_DOM_DUPLICATE_ONLY: 22

## Factory Backlog

- Backlog READY: 5
- Backlog READY_AFTER_IMAGE_QA: 2
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog WAIT_NETWORK: 1

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P72 production / READY_AFTER_IMAGE_QA: Resume Ready_for_Printify uploads in audited single-item batches
- P70 supervisor:publish / WAIT_NETWORK: Publish small cooled batch if network guard is healthy.
- P68 publish / READY_AFTER_IMAGE_QA: Publish small cooled batch after default-image and live-cover spot audit

Lane counts:
- control: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- supervisor:copy_experiment: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:publish: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- eBay Promoted Listings Standard / General 2% is the only approved active ad mode; do not use Priority/PPC or suggested ad rates.
- Sticker and non-sticker expansion remain paused until gallery duplicate risk is repaired or isolated.
- Multiple Printify official/default mockups are allowed only when they are visually distinct; publish is blocked by missing custom design/cover, live buyer-page mismatch, zero default image, or repeated selected gallery images.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.
