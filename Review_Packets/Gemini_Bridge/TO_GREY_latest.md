You are Grey, Rex's strategic advisor for OpenClaw.

Strict output requirement:
- Return concise Markdown plus a JSON block.
- The JSON block must include a top-level `tasks` array.
- Each task should include: title, priority, lane, rationale, command, risk.
- Do not request secrets. Do not recommend PPC/Priority ads. Do not recommend spending beyond caps.

## Constitution
# Grey Context Constitution

## Role Split
- Rex is the business commander and requirement engineer.
- Grey/Gemini is the strategic advisor: direction, risk critique, market logic, and summary pressure tests.
- Codex is the execution officer and head engineer: code, QA, automation, local state, and safe operations.

## Current Mainline Priority
- Printify / eBay / Etsy POD factory is the active project.
- Fallback projects are R&D only until the POD factory is stable or Rex explicitly activates them.

## Business Goal
- Build a reliable semi-automatic money printer with low manual Rex intervention.
- Prioritize real traffic, low error rate, no account damage, and no loss-making products.

## Marketplace Guardrails
- eBay ads: Promoted Listings Standard / General only, fixed 2.0%; no Priority/PPC and no suggested-rate chasing.
- Etsy spend cap before signal: $2 per batch, $6 daily gray cap, $40-$60 early test ceiling, 200 listing experiment pool.
- Do not modify payment/billing settings, generate orders, or touch private credentials beyond reading project env/config.

## Browser Rule
- Marketplace/account UI must use dedicated Edge CDP 9223 only.
- Do not use Rex's daily Chrome for Etsy, Printify, eBay, Seller Hub, or account data gathering.
- Gemini Web strategic sync must use the existing Gemini chat thread named `Codex 自动化矩阵升级计划` only. API bridge traffic remains file/API based; web chat sync is low-frequency and advisory.

## Product / QA Standards
- Printify production design must match local Production_Design through visual QA.
- Cover Gate: live buyer-page image must be verified before retiring old listings or scaling.
- Official Printify default mockups are allowed and often preferred for buyer context.
- Sticker custom U gallery mismatch is a blocker.
- Poster/Acrylic use full-image designs, not sticker cut logic.

## Strategy Notes
- Ads alone have not solved eBay 0-view; cover integrity, SEO intent, category fit, and product-market fit matter more.
- Poster/Acrylic showed better early signal than Sticker.
- Use Quiet Luxury, Smoky Jade, Reading Nook, Meditation Room, Study Room, Collector Shelf, and Deep Work intent language when suitable.


## Daily Sitrep
[DAILY_SITREP_SYNC]
Timestamp: 2026-05-09 01:50:53 -0400
System_Status: NORMAL

1. Cash-Flow Fortress:
- eBay: latest snapshot 2026-05-08 08:09:29 -0400; 0-view 44; nonzero 6; General ads 50.
- Etsy Mirror: live digital 10; confirmed spend $2.20; public audit 10.
- Printify QA: Cover Gate retired/replaced 49; gallery custom-risk 22; gallery exact-duplicate n/a; gallery OK 127.

2. The Syndicate:
- Stock / FTP distribution: deferred; Printify/POD factory remains active priority.

3. Roadblocks:
- eBay 0-view remains high; ads alone are not enough.
- Gallery Integrity is the active publish blocker: repeated/risky buyer-facing image galleries must be repaired or isolated before scaling.
- Etsy API approval remains separate from Printify/Etsy UI operations; listing-fee cap still applies.


## Latest Morning Report
# OpenClaw Morning Report

Generated: 2026-05-09 01:50 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 121
- Published through Printify/eBay tracking: 121
- Ready for Printify: 47

## Product Counts

- Acrylic: stable 42, published 42, ready 0
- Poster: stable 34, published 34, ready 0
- Sticker: stable 45, published 45, ready 47

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 116
- Acrylic: 42
- Poster: 32
- Sticker: 42

## Performance Snapshot

- Latest eBay snapshot: 2026-05-08 08:09:29 -0400
- Rows read: 50
- 0-view rows in snapshot: 44
- Rows with at least 1 view: 6
- General promoted rows in snapshot: 50

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
- Etsy Digital confirmed listing-fee spend: $2.20
- Etsy Digital public audit active/readable: 10
- Etsy legacy listings retired/deleted: 2
- eBay cover QA rows: 14

## Unified Registry Buckets

- Etsy_Draft_Prepared: 89
- Fix_Gallery_First: 1
- Hold: 136
- Published_Zero_View_Copy_Ad_Review: 26
- Ready_For_Printify_When_Network_OK: 47

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
- Live eBay cover audit LIKELY_COVER: 14
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 78
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 51
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 49
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38
- Printify gallery duplicate audit rows: 149
- Printify gallery duplicate audit CHECK_CUSTOM_GALLERY_REPEATS_RISK: 22
- Printify gallery duplicate audit OK: 127
- eBay live gallery duplicate audit rows: 27
- eBay live gallery duplicate audit CHECK_LIVE_PRIMARY_DUPLICATE_REVIEW: 3
- eBay live gallery duplicate audit OK: 1
- eBay live gallery duplicate audit OK_DOM_DUPLICATE_ONLY: 23

## Factory Backlog

- Backlog READY: 6
- Backlog READY_AFTER_IMAGE_QA: 1
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog WAIT_NETWORK: 1

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P72 production / READY_AFTER_IMAGE_QA: Resume Ready_for_Printify uploads in audited single-item batches
- P70 supervisor:publish / WAIT_NETWORK: Publish small cooled batch if network guard is healthy.
- P65 supervisor:read_only_market / READY: Refresh eBay Seller Hub performance snapshot.

Lane counts:
- control: 1
- etsy: 1
- market_learning: 1
- production: 1
- r_and_d: 1
- supervisor:copy_experiment: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:publish: 1
- supervisor:read_only_market: 1

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


## Current Backlog CSV
﻿Priority,Lane,Task,Status,Blocker,Command,Done_When,Risk,Network_Need,Owner
100,control,Run local supervisor maintenance cycle,READY,None,py modules\factory_supervisor.py --execute-local --skip-network,"Factory_Autopilot_State, action queue, QA, traffic diagnosis, morning report, and Gemini queue refresh with 0 failures.",low,local,Codex
100,supervisor:local,"Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.",READY,Safe low-bandwidth maintenance keeps the factory state current while account/image writes are paused.,py modules\factory_supervisor.py --execute-local --skip-network,Supervisor action remains present until its status is completed or superseded.,low,no,Codex
72,production,Resume Ready_for_Printify uploads in audited single-item batches,READY_AFTER_IMAGE_QA,"47 local rows are ready; Cover Gate is cleared, so proceed only through single-item upload plus production-design/default-image audit.",py modules\printify_full_pipeline.py --limit 1,A new single item reaches stable mockup state and passes selected-count/default-count audit.,high,Printify UI/API,Codex
70,supervisor:publish,Publish small cooled batch if network guard is healthy.,WAIT_NETWORK,Stable=121 published=121 ready=47; network=unknown.,py modules\printify_publish_scheduler.py --limit 3 --min-delay 180 --max-delay 420,Supervisor action remains present until its status is completed or superseded.,high,yes,Codex
65,supervisor:read_only_market,Refresh eBay Seller Hub performance snapshot.,READY,Performance data is stale or absent; this is read-only but browser/network dependent. Resource guard says conservative: temperature sensor DENIED_OR_UNAVAILABLE; using CPU/memory proxy; memory elevated 84.2%,py modules\ebay_sellerhub_snapshot.py,Supervisor action remains present until its status is completed or superseded.,low,yes,Codex
63,supervisor:production_design_qa,Run a tiny Printify production-design audit before any larger online batch.,READY,This checks whether Printify front print-area art visually matches local Production_Design files; keep it small under weak Wi-Fi. Resource guard says conservative: temperature sensor DENIED_OR_UNAVAILABLE; using CPU/memory proxy; memory elevated 84.2%,py modules\printify_design_audit.py --limit 2 --sleep-seconds 1,Supervisor action remains present until its status is completed or superseded.,low,yes,Codex
62,market_learning,Keep eBay traffic diagnosis current and avoid ad-only conclusions,READY,5 current traffic hypotheses generated.,py modules\ebay_traffic_diagnosis.py,Traffic report identifies exposure/click/conversion blockers from snapshots and cover queues.,low,local,Codex
56,etsy,Monitor first 10 Etsy Digital listings before spending more,READY_MONITOR,Live=10 ready=0 confirmed_spend=$2.20.,py modules\etsy_live_audit.py --limit 10,Morning readout has active/readable status plus views/favorites when available; do not scale until signal or Rex resumes.,low,Etsy public/UI read,Codex
55,supervisor:etsy,Monitor Etsy Digital first gray batch before spending more listing fees.,READY_MONITOR,Live=10 ready=0 confirmed_spend=$2.20; hold scale until first traffic readout. Resource guard says conservative: temperature sensor DENIED_OR_UNAVAILABLE; using CPU/memory proxy; memory elevated 84.2%,py modules\etsy_live_audit.py --limit 10,Supervisor action remains present until its status is completed or superseded.,low,yes,Codex
50,supervisor:copy_experiment,Continue low-bandwidth SEO/title/description experiment analysis.,READY,Ads alone did not move zero-view listings; controlled copy/image experiments are the next learning loop.,py modules\ebay_experiment_report.py,Supervisor action remains present until its status is completed or superseded.,low,no,Codex
46,r_and_d,Validate next product candidates with official Printify blueprint/provider/variant data,READY_FOR_SCHOLAR_REVIEW,5 next blueprint candidates are documented.,py modules\product_blueprint_next_plan.py,"Canvas, framed poster, notebook, mug, and metal candidates have enough data for Scholar review before development.",low,local,Codex


## Recent Progress Tail
ed 10 new Track A low-competition intent rewrites focused on Acrylic/Poster, not Sticker. All 10 synced successfully with no image changes and no listing-fee spend.
- Generated `Review_Packets/PRINTIFY_SOURCE_GALLERY_RISK_20260508.md`: 22 Printify source-gallery debt rows, all `P2_SOURCE_DEBT`; no current `P1_LIVE_VISIBLE` duplicate fire.
- Refreshed multi-track experiment and monitor reports. Latest decision: keep 2% ads as baseline, but treat product-market fit, long-tail intent, and gallery trust as the growth levers.
- Etsy Digital remains capped: 10 live/readable, total confirmed spend $2, today $0, API still pending/inactive.

## 2026-05-08 09:31:00 -04:00 Forty-Minute Monthly Task Block
- Applied Rex's Gemini Web routing rule: low-frequency Gemini Web sync must use the existing `Codex 自动化矩阵升级计划` thread only; API bridge remains file/API based and advisory.
- Resource optimization succeeded: closed idle Edge automation tabs/session after account UI work; CPU dropped from about 100% to about 25% and memory freed to roughly 4.8GB. Chrome was not touched.
- Read latest Grey/Gemini API feedback: recommendation remains SEO intent monitoring, Etsy Digital read-only monitoring, Poster/Acrylic priority, and no Sticker scale until the gallery path is safe.
- Etsy live audit: first 10 listings remain `ACTIVE_READABLE`; no additional Etsy spend.
- Printify production-design audit: Poster 4/4 and Acrylic 4/4 visual matches, no mismatches.
- Local factory supervisor refreshed QA, unified registry, market queue, eBay traffic diagnosis, gallery duplicate audit, blueprint plan, Etsy API status, backlog, morning/Gemini reports. One expected failure: Printify login guard could not reach Edge CDP because Edge had been deliberately closed for resource cleanup.
- eBay diagnosis remains unchanged: 2% General ads are active but not enough alone; current blocker is traffic/product-market fit plus gallery/source trust, not Cover Gate.
- Gemini free API follow-up attempt returned HTTP 503 high demand; no retry loop was started. `TO_GREY_latest.md` is ready for the next low-demand retry.

## 2026-05-08 21:57:00 -04:00 One-Shot Night Shift Runner Armed
- Rex requested roughly 10 hours of monthly tasks until the next 06:00 ET shutdown. Actual available window from current time is about 8 hours, ending with 05:30 winddown and 05:50 stop.
- Added `modules/night_shift_runner.py` as a bounded one-shot loop for the current logged-in session only. It does not change startup/login/reboot behavior.
- Trial cycle passed: memory guard, resource allocator, local factory supervisor, multi-track monitor, eBay experiment report, eBay traffic diagnosis, and backlog refresh all completed. CPU after trial was about 43%, memory about 70%.
- Night runner strategy: before 23:00 ET, prioritize local/read-only/report work; after 23:00 ET, allow Edge read-only Seller Hub snapshots and very small Printify metadata syncs only if guards pass. No Etsy paid listings, no PPC/Priority ads, no order/payment/customer-message actions.
- Logs/state: `Database/Night_Shift_Run_Log.csv` and `Database/Night_Shift_State.json`.

## 2026-05-08 22:15:00 -04:00 Night Shift Fill-Work Rule Added
- Rex clarified that if the expected night workload finishes early, the factory should not idle; it should automatically add safe monthly tasks until the winddown window.
- Stopped the first night-runner instance during its sleep window and upgraded `modules/night_shift_runner.py`.
- New fill-work behavior: shorter default loop interval (`900s`), Grunt queue seed/one-shot execution, Quality Floor scans, morning report refresh, Daily Sitrep preparation, and Grey prepare-only packets.
- Online writes remain guarded: only tiny metadata syncs after 23:00 ET, no paid Etsy spend, no PPC/Priority, no account/payment/order/customer-message actions.

## 2026-05-08 23:35:00 -04:00 Autonomous Continuation Reinforced
- Rex reminded that monthly tasks should continue without repeated prompts. Added durable rule: after any interruption, if no explicit stop/pause exists and guards are green, advance the highest-priority backlog item or safe local/report/QA work automatically.
- Night shift runner is healthy at cycle 4 and continues toward 05:30 winddown / 05:50 stop.
- Memory pressure cleanup closed idle Edge automation processes and Phone Link helpers, not Chrome. Memory improved from about 85.8% used to about 72.4%, CPU from about 56% to about 25%.

## 2026-05-08 23:52:00 -04:00 Monthly Task Continuation Checkpoint
- Night shift runner is active and completed Track A metadata sync small batch at 23:49 (`limit=3`, jittered, no images, no fees).
- Gemini/Grey API follow-up succeeded and produced 5 advisory tasks. Advice aligns with current route: Track A SEO intent, read-only Seller Hub refresh, Etsy live audit, Poster/Acrylic QA, and gallery debt prep.
- Refused to run Grey's suggested `printify_full_pipeline --limit 1` blindly because all 47 Ready_for_Printify rows are Sticker; Sticker expansion remains frozen until create-time gallery is safe.
- Added one manual production-design audit (`printify_design_audit_20260508_235120.csv`): 5/5 visual matches, no mismatches.
- Runner remains responsible for the next Seller Hub read-only snapshot on the next eligible cycle.

## 2026-05-08 21:48:52 -04:00 Cruise Heartbeat Cooldown Activated
- Checked git/worktree first; the workspace already had many untracked Database/Review_Packets artifacts, and heartbeat work left them untouched.
- Repo npm heartbeat/cooldown/resource/memory scripts were attempted, but `.venv\Scripts\python.exe`, PyManager `python`, and `py` all failed with `Access is denied` before module execution.
- PowerShell fallback resource sampling succeeded, but final CPU resample was unstable up to 99.4%; memory stayed workable around 63.3% used / 4.3GB free; thermal/fan/power sensors remain denied or unavailable.
- Refreshed hardware heartbeat, cooldown, memory guard, system resource, and Grunt state/log files with cooldown active until 22:10 ET. No Edge/Chrome tabs were inspected or closed.
- Attempted one low-risk `npm run grunt:dry`; it was blocked by the same Python access failure. Live Grunt work and any second Grunt attempt were skipped; no payment, billing, order, or customer-message settings were touched.

## 2026-05-09 00:58:00 -04:00 Daily Rex/Gemini Action Packet Automated
- Converted the existing one-shot Etsy morning heartbeat into a daily `OpenClaw Daily Rex/Gemini Action Packet` at 08:30 ET.
- Added `daily_rex_support_packet.py` into `night_shift_runner.py` normal cycles and winddown so Rex/Grey needs are refreshed before shutdown.
- Current packet outputs are centralized in `Review_Packets/Rex_Action_Packet_latest.md` and `Review_Packets/Gemini_Bridge/TO_GREY_rex_needs_latest.md`.

## 2026-05-09 01:00:00 -04:00 Etsy Printify External Poller Added
- Added `modules/etsy_printify_external_poll.py` as a no-spend/no-republish reconciler for Printify Etsy publishes whose external id has not backfilled.
- Wired the poller into `night_shift_runner.py` every other cycle.
- First poll: `Poster-Academia-0011` remains `PUBLISHED_EXTERNAL_PENDING` at age about 6 minutes, so no duplicate publish was attempted.

## 2026-05-09 01:05:00 -04:00 Etsy Shop Shell Task Preserved
- Added a durable backlog task to apply the Option 02 / Quiet Relic Studio Etsy shop shell before scaling Etsy listings.
- Updated Rex/Gemini daily packet to include the storefront shell as an action item and to point at the existing banner/icon/copy sources.

## 2026-05-09 01:35:00 -04:00 Etsy Shop Shell Applied Through Edge
- Confirmed Etsy Shop Manager is logged in through Edge CDP 9223.
- Applied Option 02 / Quiet Relic Studio shell copy:
  - announcement, physical buyer note, digital buyer note, tagline, about headline/body.
- Uploaded and saved the Option 02 shop logo.
- Shop name change to `QuietRelicStudio` did not verify; Etsy's custom input remained in Save/Cancel state and the visible shop name stayed `DriveFuel`. Left as a tracked follow-up rather than blocking monthly Etsy work.
- No paid listings, ads, orders, payment settings, or customer messages were touched.

## 2026-05-09 01:44:00 -04:00 Etsy Monthly Task Continuation
- Etsy app key probe still passes as `API_KEY_ACTIVE`.
- OAuth PKCE Edge bridge was implemented and tested, but Etsy authorization lands on `https://www.etsy.com/error.php` before the localhost callback. No token was stored and no live data was changed.
- Retried OAuth with a minimal scope set; same Etsy `error.php`, so this is likely app redirect/app authorization configuration rather than listing code.
- Printify Etsy external poll: `Poster-Academia-0011` still pending external id at age about 42 minutes; no duplicate publish attempted.
- Etsy live read-only audit: 10 known active listings remain `ACTIVE_READABLE`.
- Next digital batch selector refreshed 29 ready no-spend candidates; projected fee if published would be `$5.80`, but no new spend was triggered.


## Question / Decision Request
Review current state. Identify the next 3-7 highest ROI actions, risks, and any strategic correction. Keep Printify/POD as mainline.
