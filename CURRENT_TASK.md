# Current Task - OpenClaw Factory Phase 1 Day 1

Started: 2026-05-03 22:43 -04:00 America/New_York

Operating timezone:
- Use New York / Eastern time for all future project logs, checkpoints, and handoffs.

Operating roles:
- Rex is Commander.
- Gemini is Strategy Advisor.
- Codex is Executive Operator.
- Durable route is saved in `PROJECT_FACTORY_ROADMAP.md`.

Browser/resource hygiene:
- After finishing a browser-based task, close related working tabs automatically.
- Keep only the 1-2 project tabs needed for the next active task.
- Do not close unrelated/private user tabs unless Rex explicitly asks.
- Prefer API/local scripts over repeated browser refresh loops when possible.

Current execution order:
1. Pause rapid public eBay publishing after Akamai/zero-size-object instability.
2. Build Phase 1 data foundation: eBay read-only performance log, unified listing records, and DNA signal fields.
3. Keep Etsy shop setup in waiting mode until Rex says the Etsy shop is ready. Prepare data/assets only; do not debug Etsy storefront, publish Etsy listings, or edit Etsy shop settings.
4. Keep Printify production available but avoid shop-front design changes until Rex updates the Printify storefront.
5. Continue QA-first production, eBay read-only monitoring, performance logging, and report automation.
6. Save morning/Gemini advisor report templates so Gemini can act as strategy advisor and Codex can filter recommendations.

Guardrails:
- Do not publish new eBay/Etsy listings in this phase unless explicitly resumed.
- Do not interact with Etsy shop setup until Rex gives the signal that the Etsy shop is ready.
- Do not activate paid advertising without final action-time confirmation. Exception already completed on 2026-05-04: Rex confirmed eBay Promoted Listings Standard / General fixed 2.0%; Seller Hub campaign now covers 99 identifiable OpenClaw listings after external-id refresh.
- Do not touch payment settings, orders, or buyer messages without confirmation.
- Sticker expansion remains paused until the Cover/U image selection bug is fixed.

## 2026-05-04 20:22 -04:00 Etsy Brand Shell Current State
- Use Edge for Etsy site operations by default; Chrome has Etsy site data cleared and may have OAuth issues.
- Do not edit Etsy shop settings until Rex selects one of the numbered brand options.
- Current complete local design options: 02 Quiet Relic Studio, 03 Scholar Grove Atelier, 04 Lumen Relic Gallery.

## 2026-05-04 23:20 -04:00 Network Guard Rule
- Until Rex confirms the latency issue is resolved, every large continuous task must run network preflight first: py modules\network_guard.py.
- Use conservative execution by default: max_parallel=1, batch_size=1-3, shorter independent jobs, checkpoint after each unit.
- For MJ/Discord, avoid large simultaneous prompt batches; for Printify/Etsy/eBay, avoid broad bulk writes and prefer recoverable single-item batches.

## 2026-05-05 00:24:12 -04:00 Low-Bandwidth / 2.4GHz Default Protocol
- Until Rex confirms wired/low-latency network is ready, choose low-dependency local work first.
- Suspended by default: bulk image uploads, broad Printify/eBay/Etsy writes, frequent OAuth refresh attempts, large MJ batches.
- Allowed: local code hardening, data normalization, listing text/tag/price generation, image metadata cleanup, mockup/gallery derivation, QA audit scripts, report builders.
- If network is needed, run network_guard first and use max_parallel=1, batch_size=1 unless the guard is clearly healthy.

## 2026-05-05 08:41:18 -04:00 Current Local-Only Work + Product R&D Branch
- Network guard currently reports pause, so no bulk online writes.
- Continue local monthly factory tasks: copy candidates, unpublished-draft copy application, market signal/action queue, report refresh.
- New branch after local queue: investigate new Printify blueprint candidates for eBay/Etsy using official Printify catalog/API when network permits; score by product fit, margin, upload complexity, mockup reliability, buyer demand, and account-risk diversification.
- Do not develop/publish new product type at scale until blueprint/provider/variant/print-area/cost/shipping are verified from official sources.

## 2026-05-05 10:50:06 -04:00 Blueprint Provider/Variant Probe
- Continue difficult R&D branch: query official Printify provider/variant/cost/print-area data for top blueprint candidates one-by-one with checkpointed output.
- Weak-network rule remains active: single blueprint at a time, short retries, write partial CSV after every successful query.

## 2026-05-05 13:18:11 -04:00 Etsy Digital Product R&D
- New branch: evaluate Etsy digital products that fit current OpenClaw pipeline and revenue goal.
- Prioritize: instant download / low-support / high asset reuse / clear buyer expectation / Etsy policy compliant.
- Custom pet/family portrait ideas are allowed by Etsy when seller-designed/AI-disclosed, but likely higher support and saturation; evaluate but do not default to them first.

## 2026-05-05 13:26:00 -04:00 Etsy Digital Product Pilot Design
- Network guard is in pause mode because Printify latency is high; stay local/low-bandwidth.
- Build a digital-product roadmap and first pilot package strategy without Etsy uploads.
- Official constraints to respect: digital listings must be seller-made/designed, AI-assisted work must be disclosed, instant-download listings support up to 5 files with 20MB max each.
- Product priority to test: printable wall art packs, personalized bookplate/ex-libris downloads, then custom pet portrait after a QA/revision workflow exists.

## 2026-05-05 14:22:00 -04:00 Modem-Proximity Network Stress Test
- Rex moved laptop near the modem; run higher-traffic stability checks before resuming broad online work.
- Sequence: network_guard baseline, HTTPS download stress, account endpoint read-only probes.
- Only if stable: resume one small recoverable online batch; avoid publish/account writes until test data is healthy.

## 2026-05-05 17:52:00 -04:00 eBay Traffic Recovery Experiment
- General 2% ads did not materially change zero-view state; treat ads as amplifier, not root fix.
- Build an A/B/C experiment for active Sticker listings: title/search-intent rewrite, cover/gallery fix priority, and holdout control.
- Preserve rollback data before changing local workbook; online sync only after a small low-risk batch or confirmed network stability.
- Product language priority: buyer-intent terms first (4pc vinyl sticker set, laptop, water bottle, journal, waterproof-style use case), aesthetic words second.

## 2026-05-05 18:38:00 -04:00 Continue Low-Bandwidth Monthly Tasks
- Do not idle while network remains unstable.
- Continue local-first work: Etsy digital printable pack expansion, Etsy metadata, eBay cover QA contact sheets, performance experiment tracking scaffolds, and report refresh.
- Online operations remain small JSON only; defer high-bandwidth image uploads and broad marketplace writes.

## 2026-05-06 00:40:00 -04:00 Live Cover Repair Gate
- Sticker expansion remains paused.
- Seller Hub Reports cannot repair existing Printify-synced variation pictures because eBay treats them as Inventory-managed listings.
- The next executable repair path is source repair: log into the Chrome remote-debug Printify profile, re-upload/select mockups so each product has exactly one Cover default, publish/sync from Printify, then run live eBay cover audit.
- If source re-sync cannot update existing live inventory-managed listings, the fallback is replacement listings: create correct listings with the fixed source image logic, verify live cover, then retire the bad old listing after verification.
- New publish scheduler must continue to block products with duplicate Printify default images.
- Durable decision files: `Database/eBay_Cover_Repair_Decisions.csv` and `Database/eBay_Cover_Repair_Decisions.md`.

## 2026-05-06 01:08:00 -04:00 Automation-First Supervisor
- Codex is a temporary debugger/operator, not the permanent factory worker.
- Recurring work must be converted into scripts, queues, guards, and reports.
- Added factory supervisor target: `py modules\factory_supervisor.py --execute-local --skip-network`.
- Supervisor owns local maintenance, cover-gate state, network strategy, read-only market refresh recommendations, and publish blocking.
- Upload/full-pipeline code must reject any product whose selected Printify images do not have exactly one default image.

## 2026-05-06 08:10:00 -04:00 API Integration Scope Rule
- Maximize the existing Printify API/workflow first; do not build a second full listing engine unless forced by a verified blocker.
- eBay API, once available, should be added narrowly: performance reads, Promoted Listings Standard 2% state, item health checks, lightweight metadata experiments, and reconciliation.
- Product creation, production design upload, mockup generation, and platform push remain Printify-owned by default.
- Any eBay/Etsy API result must write back into the existing database/supervisor files instead of creating a separate source of truth.

## 2026-05-06 14:55:00 -04:00 Wired Network Restored + Sticker Cover Gate Resolution
- Ethernet is active through `Ethernet 3` at 1Gbps; Wi-Fi is disconnected. Multi-endpoint checks showed 0% packet loss and about 5-8ms latency; 50MB download test was about 214 Mbps.
- Low-bandwidth mode is lifted for online batches, but account-risk throttles still apply.
- Sticker main-image bug root cause: sending U1-U4 as Printify/eBay listing gallery images lets eBay pick a single U/detail image as the buyer-facing cover.
- New Sticker rule: publish/replace with Cover-only custom art plus Printify official mockups. Keep U1-U4 locally for QA/detail/reference; do not push them as first-pass eBay gallery images.
- Verified live eBay results: `Sticker-Academia-0005-FIX2`, `0006-FIX1`, `0007-FIX1`, `0008-FIX1`, and the next 10 replacement listings use official cover mockups and pass live buyer-page cover audit.
- Old bad listings are queued in `Database/eBay_Retire_Queue.csv`; do not create many more duplicates until a safe end-listing path is confirmed.

## 2026-05-06 15:20:00 -04:00 Full Throughput Mode Restored
- Rex confirmed the wired asset/network setup is good enough to stop worrying about Wi-Fi instability.
- Default execution mode returns to high-throughput online work: Printify publishing, live buyer-page audits, and API reads may run without low-bandwidth deferral.
- Account-risk gates remain active: do not use PPC/Priority ads, do not touch payment/order/buyer-message settings, and do not create many duplicate Sticker replacements before old bad listings have a verified retirement path.
