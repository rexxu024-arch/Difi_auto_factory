# Gemini Advisor Review Queue

Generated: 2026-05-06 10:46 -0400 America/New_York

Rex is Commander, Gemini is Strategy Advisor, Codex is Executive Operator.

Please review the current OpenClaw plan as a strategy advisor. Do not request API keys, account secrets, payment data, buyer private data, or direct account actions.

## Report Summary

# OpenClaw Morning Report

Generated: 2026-05-06 10:46 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 161
- Published through Printify/eBay tracking: 112
- Ready for Printify: 50

## Product Counts

- Acrylic: stable 53, published 26, ready 0
- Poster: stable 32, published 26, ready 4
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
- Unified registry rows bucketed: 240
- Etsy digital printable upload queue: 20 listings, max file 3.42MB, under 20MB limit: True
- Etsy digital previews: 20 listings x 3 preview images
- Etsy digital final upload packet: 20 listings, QA bad=0, missing=0
- Etsy digital bundle concepts: 3
- eBay cover QA rows: 14

## Unified Registry Buckets

- Etsy_Draft_Prepared: 29
- Hold: 62
- Published_Has_View_Monitor: 8
- Published_Zero_View_Copy_Ad_Review: 42
- Ready_For_Printify_When_Network_OK: 50
- Stable_Draft_Publish_When_Scheduled: 49

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
- Live eBay cover audit LIKELY_COVER: 2
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 49
- Live cover fix queue rows: 49
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Cover replacement queue WAIT_SOURCE_REPAIR_RESULT: 45
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog BLOCKED: 1
- Backlog BLOCKED_BY_COVER_GATE: 1
- Backlog READY: 5
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog WAIT_COVER_GATE: 2
- Backlog WAIT_PRINTIFY_LOGIN: 1
- Backlog WAIT_SOURCE_REPAIR_RESULT: 1
- Backlog WAIT_USER_OR_API_APPROVAL: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / BLOCKED: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P95 supervisor:cover_gate / WAIT_PRINTIFY_LOGIN: Repair one Printify source cover, then live-audit eBay before scaling.
- P92 image_integrity / BLOCKED_BY_COVER_GATE: Clear Printify default-image CHECK rows before publish resumes

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- fallback: 1
- image_integrity: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Until wired/low-latency network is confirmed, prefer local low-bandwidth tasks and single-item network probes.
- No Etsy publish until Rex confirms listing-fee spend.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- New publish is blocked when Printify exposes multiple default images for a product.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.


## Questions for Gemini

1. Given the current low-view eBay signal, which buyer persona should the first Etsy launch prioritize?
2. For a 30-listing Etsy relaunch, is the Poster/Acrylic-heavy mix commercially sensible, or should Sticker/digital printable be emphasized sooner?
3. Which three visual DNA themes should be expanded first if Etsy impressions appear but clicks remain low?
4. What ad test would you run first with a $3-5/day Etsy Ads budget after 48-72 hours of organic data?
5. Which product language sounds too mass-generated and should be softened before launch?

## Codex Action Filter

- Adopted:
- Deferred:
- Rejected:
- Requires Rex confirmation:
