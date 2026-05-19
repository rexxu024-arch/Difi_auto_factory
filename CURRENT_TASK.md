# Current Task - 3-Day Revenue Priority Override

Updated: 2026-05-16 America/New_York
Priority: P0
Protocol: Rex 3-Day Revenue Ordering

Mission:
- For the next three days, execute in this order unless a hard guard blocks a lane:
  1. Adobe Stock product production first. Assets must meet Rex quality standards: commercial-useful, macro/material depth, no low-res drafts, no cheap flat texture spam, proper metadata/AI disclosure, and no Etsy/eBay/First Audit brand leakage.
  2. Sticker liquidation into Etsy digital material bundles second. Use retired/high-res U assets as designer-resource packs, not Sticker POD. Package ZIPs within Etsy limits, use Etsy-native title/description, and make buyer expectations explicit.
  3. Daily Etsy/eBay listing drip third. Keep reasonable daily quantity, no Sticker POD expansion, prioritize quality POD and controlled experiments under fee/account/QA guards.
- If Adobe is blocked by visual QA/source quality, do not publish weak assets. Improve source/DNA/metadata first.
- If Sticker bundle publishing is blocked, continue packaging, preview sheets, metadata, and market evidence work without spending.
- If marketplaces are blocked, continue local prep and Adobe/Project Mirror/Premium DNA work.

Current execution status:
- Market evidence gate is now mandatory for revenue products: `modules/market_research_gate.py`, `Reports/Market_Evidence_Gate_latest.md`.
- Adobe Stock contributor account is ready from Rex side, but first batch must be rebuilt to the higher-quality macro/material standard before upload.
- Sticker bundle builder exists and produces ZIP/preview/metadata outputs under `Release/Digital_Warehouse/` and `Database/Sticker_Liquidation/`.
- Sticker liquidation pack size is locked: small style packs use 20 images each; the mega vault uses 50 images. Do not revert to the old 30/100 plan unless Rex explicitly approves after a file-size and buyer-expectation review.
- Adobe Stock upload-ready packs are neutral 50-file folders: `adobe_stock_factory/upload_ready/batch_###_[material_hint]`. Do not split new upload packs by date. The folder hint is for local reference only; each Adobe file keeps its own title/keywords/category.
- Adobe Stock upload resume rule: each confirmed uploaded file receives `_uploaded`; the folder receives `_completed` only after every real image in that batch is uploaded. If a batch folder is not `_completed`, the next upload-prep run must resume that same folder before creating any new batch. Stop after the day's 50-file target or when all staged files are uploaded.
- Adobe Stock repetition guard: after roughly 150 images in one material/theme family, reduce same-family output unless the next run adds a clear new element, lighting treatment, camera distance, surface use case, or hybrid material direction. Avoid flooding Adobe with near-duplicate stock.
- Etsy/eBay daily drip remains active but lower than Adobe + Sticker bundle work for this 3-day window.
- Codex participation rule: for the next 2-3 weeks, every `continue monthly tasks` / heartbeat wake is a chat-model supervised work turn. The local long-shift loop may execute deterministic arms, but Codex must own prioritization, QA/risk judgment, blocker isolation, and cross-project progress. Do not stop after one small script if higher-value work remains.

---

# Previous Current Task - V15.5 Dual-Track Purge And Studio Gift Pivot

Updated: 2026-05-13 11:50 -04:00 America/New_York
Priority: P0
Protocol: V15.5 Great Purge / Executive Gift Pivot

Mission:
- Stop low-price blind volume and clean active marketplace dead weight.
- Move sub-USD-15 low-value digital/sticker/planner/printable assets out of active sale when API data supports the decision; zero-signal non-POD experiments are also purge candidates.
- Keep actions reversible and logged.
- Shift public production toward 3-5/day high-quality Acrylic / Poster / executive-gift listings with strong mockups.
- Build V15.5 weaponized folders for selected premium assets under `Release/[SKU-intent]/`.

Current execution:
- Monthly shift runner is now hard-routed through `scripts\continue_monthly_tasks_5h.cmd` -> `modules\monthly_shift_loop.py`. This bypasses the old cruise dispatcher. It is a primitive fixed-queue while loop: execute command, log, refresh trigger, move to next command, repeat until the current weather/hardware duty deadline. There is no 5-hour default cap and no fixed 05:30/06:00 stop when heat data says otherwise. It must not stop merely because one command has no immediate new work.
- Steer conversation rule: unless Rex explicitly says stop, pause, wait, or shut down, any side answer must be followed by returning to the monthly shift loop. Answering Rex is not a completion condition.
- Etsy conservative first wave moved 4 listings inactive.
- Etsy hard purge then moved the remaining low-price active download archive inactive by official Etsy API. Current active state is 57 physical listings, 0 active downloads, 0 active listings under $15.
- Reconciliation file: `Database/V155_Etsy_Hard_Purge_Reconciliation.json`.
- eBay purge candidate-only map built: `Database/V155_eBay_Purge_Candidates.csv`; no eBay listings ended until exact live item-level traffic/end path is verified.
- First V15.5 weaponized folder created: `Release/OC-V155-001-Executive-Jade-Desk-Gift`.
- First Audit V5 private review pack exists at `First_Audit_Release/V5_Zones1_3`; focused Top 4 packet exists at `Review_Packets/First_Audit_V5_Zones1_3_TOP4_CONTACT_SHEET.jpg`.
- First Audit V5 Top 4 second-pass Relaxed grids are harvested at `Review_Packets/First_Audit_V5_Top4_Refinement_GRID_CONTACT_SHEET.jpg`. Fast/Upscale remains locked until Rex selects a quadrant.
- 48-hour Ethernet stability sampling is active via Windows Task Scheduler. Current early samples are clean on `Ethernet 3` / 1 Gbps. Summary: `Reports/Network_Path_48h_Sampling_Report.md`.
- Tomorrow 03:05 ET continuity probe is scheduled to test whether the monthly-task loop sustains work for roughly one hour without Rex nudging it.

Next execution:
1. Rex visual review when available: inspect `Review_Packets/First_Audit_V5_Top4_Refinement_GRID_CONTACT_SHEET.jpg`; best current automatic pick is `OC-NYC-MUSEUM-020-R1` top-left, but do not upscale without Rex.
2. Continue V15.5 daily release prep: acrylic/poster only, no Sticker expansion.
3. Turn the first weaponized folder into a Printify-ready private/public candidate only after mockup and cost guard are rechecked.
4. Improve eBay purge/readback path before ending any eBay live listings.
5. Keep normal monthly work moving while the network sampler runs in the background; only interrupt Rex if `Network_Path_Alerts.csv` records active path falling off Ethernet or Ethernet stops being gigabit.

Project Mirror routing:
- Routine POD and low-price experiments can use prior OpenClaw DNA plus light Premium Mentor blending.
- Mid-tier Poster/Acrylic should mix existing OpenClaw DNA with `Database/Premium_Mentor_Hub.csv`.
- First Audit, cousin-demo work, $128 acrylic, $149 bundle, and $295 anchor products require source-derived Premium DNA and an A/B/C comparison before upscale or public/private finalization.
- Current seed report: `Review_Packets/Project_Mirror/PREMIUM_DNA_EXTRACTION_V1.md`.
- Current A/B/C matrix: `Database/Premium_DNA_AB_Comparison.csv`.

---

# Previous Task - The First Audit: 001 Studio Series

Updated: 2026-05-11 20:10 -04:00 America/New_York
Priority: P0
Protocol: V13.0 high-atlier studio pivot

Mission:
- Build "THE FIRST AUDIT: 001" as the first cold-gallery OpenClaw Design Studio series.
- Stop treating premium visuals as low-price public marketplace inventory.
- Physically separate Etsy from Studio:
  - Etsy becomes a digital resource archive / warehouse for low-price designer materials.
  - Studio becomes a New York atelier for physical acrylic relics and archival studio prints.
- Studio carriers are restricted to optical acrylic blocks, archival studio prints, and premium framed posters.
- Studio banned carriers: mugs, notebooks, phone cases, and other cheap merch.
- Pricing firmware is locked to integer steps:
  - $48 entrance studio print.
  - $128 core optical acrylic relic.
  - $295 anchor masterwork acrylic / limited object.
- Top 1% visual assets must receive THE FIRST AUDIT audit IDs and remain out of Etsy archive placement.

Current generated deliverables:
- Database/First_Audit_001_Asset_Manifest.csv
- Database/First_Audit_001_State.json
- Database/First_Audit_001_Blocklist.csv
- Database/First_Audit_001_Guard_Audit.csv
- Review_Packets/First_Audit_001/THE_FIRST_AUDIT_001_LOOKBOOK.md
- Review_Packets/First_Audit_001/THE_FIRST_AUDIT_001_LOOKBOOK.pdf
- Review_Packets/First_Audit_001/THE_FIRST_AUDIT_001_CONTACT_SHEET.jpg
- Review_Packets/First_Audit_001/FIRST_AUDIT_GUARD_REPORT.md
- Review_Packets/First_Audit_001/FIRST_AUDIT_EXTENSION_SPEC_SHEETS.md
- Database/First_Audit_001_Extension_Specs.csv

Next execution:
1. Rex visual review: inspect `Review_Packets/First_Audit_001/THE_FIRST_AUDIT_001_CONTACT_SHEET.jpg` and the PDF prototype.
2. Codex preflight rule: run `py modules/first_audit_guard.py` before any public Etsy/eBay/Printify queue publish involving premium assets. Public queue leak count must be 0. Publish scripts can also call `risk_guard.assert_no_first_audit_public_assets(...)` before writing public marketplace payloads.
3. Codex next safe task: create Etsy archive rename/retirement packet and mark premium assets as `KEEP_OUT_OF_ETSY_ARCHIVE` in local mapping before any shop rename/UI work.
4. Codex next production task: continue filling First Audit from 9 selected units toward 12-15 stronger candidates, prioritizing acrylic relics and gallery-grade prints.
5. Codex must not publish these to eBay/Etsy; this is private Studio inventory and Printify-backed fulfillment.

---

# Previous Task - Operation Shock and Awe Final MVP

Started: 2026-05-09 11:20 -04:00 America/New_York
Priority: P0
Deadline: 14-day private showcase sprint

Mission:
- Build 30 high-net-worth private-client showcase concepts for OpenClaw Design Studio.
- Current active phase: Zone 2 / Battlefield 2, 10 cultural-arbitrage concepts for partner-demo review.
- Quality standard is stricter than public marketplace production: these 30 demos are partner-recruitment showcase assets, not quantity output. Every unit must earn its place by improving quality, user-story fit, cultural story, material illusion, and Printify feasibility.
- Do not continue dispatching prompts just to show activity. Spend extra time/API only when it measurably improves concept strength, visual accuracy, premium feel, or private-sales usefulness.
- Use Printify as the fulfillment backend, but do not sync this packet to eBay/Etsy.
- Focus on official, verified Printify formats only. User/Grey codes are treated as intent labels until verified against Printify Catalog API.
- Create Printify private draft-ready products after images pass QA.
- Printify private titles/descriptions should be personality-led and private-sales friendly, not SEO template copy.
- Do not generate eBay/Etsy public listing title/description copy for this packet.
- Do not connect China image APIs in Phase 1.
- Avoid direct IP infringement and avoid hardcore eastern mythology that Midjourney may render cheaply.
- Final MVP output format per unit:
  - Block A: Midjourney Master Prompt.
  - Block B: Broker's Hook, 1-2 casual private-channel sentences for WeChat/朋友圈.
  - Block C: Studio Spec Sheet, dense official authority copy with cultural anchor, material illusion, spatial recommendation, and objection handling.
  - Block D: Printify Production Vector with verified blueprint/provider/variant/cost/RRP.

Current deliverables:
- Review_Packets/OPERATION_SHOCK_AND_AWE_V5_ZONE2_CONCEPTS_20260509.md
- Database/Shock_And_Awe_V5_Zone2_Printify_Private_Queue.csv
- Review_Packets/OPERATION_SHOCK_AND_AWE_V5_BLUEPRINT_RND_20260509.md
- Database/Shock_And_Awe_Blueprint_RnD.csv
- Database/Strategic_Mode.json
- Each V5 Zone 2 row includes a private DM pitch so Rex or the partner can test interest directly in WeChat/private traffic.
- Private showcase sales logic: the product is the fulfillment object, but the real offer is story, identity signal, cultural depth, room aura, and social talking value.
- Zone 2 first 10 visual demo units now have harvested images, visual QA decisions, final selections, Printify production files, and Printify private draft products.
- Zone 2 final review packet: Review_Packets/OPERATION_SHOCK_AND_AWE_V5_ZONE2_FINAL_PACKET_20260509.md.

Parallel monthly task contract:
- Durable list: OPENCLAW_MONTHLY_TASKS.md.
- Etsy public listing engine is authorized under the fee guard, with normal cap USD 50 and absolute ceiling USD 60.
- Fee guard semantics: paid listing actions are allowed inside the configured budget; stop only for cap overflow, ambiguous/duplicate spend, account risk, QA failure, or reconciliation failure.
- Etsy quality pivot: keep a limited Digital test pool for market sensing, but do not let Digital become the main low-quality volume engine. Prioritize high-quality Printify-backed POD listings that pass design QA, product-fit QA, pricing guard, and Etsy-style title/tag/description standards.
- eBay must run a 3-day experiment loop instead of passively waiting on 0-view listings.
- Daily marketplace drip is a standing task: if fee/account/QA guards are green, each workday should safely publish or adjust a small Etsy/eBay experimental batch until Rex's cap is reached. Etsy prefers official API/Printify-backed POD plus selected digital tests; eBay prefers Poster/Acrylic/high-value experiments. Do not expand Sticker inventory.
- Current implementation anchor: Etsy paid listing actions are allowed under the $50 normal / $60 hard cap; `monthly_shift_loop.py` includes a one-listing guarded `etsy_pod_publish_drip` command. eBay live publish remains blocked until shipping/source readback is clean, so eBay daily work is prep/diagnosis/experiment planning rather than risky live publish.
- Automation must keep moving toward a self-operating factory, reducing Codex hand-driving over time.
- Pricing rule: low-value traffic items must not lose money but can run low margin for reviews; mid-tier items balance profit and conversion; high-value/private-showcase items keep premium margin and test acceptance in small batches. Always include Printify production, shipping, marketplace/payment fees, listing fees, and ads before deciding price.
- Reasoning setting reminder: OpenClaw core work should run on the strongest available Codex reasoning setting by default. Only deterministic local batch chores should use medium/low, and any downgrade must return to high reasoning before strategy, QA, pricing, publish, or account-risk work.
- Operating-window rule: after Rex opens/boots Codex, continue monthly tasks until the current weather/resource duty deadline unless Rex explicitly stops/pauses or all eligible work is verified complete. Heat, hardware state, and Rex's current operating plan decide the actual stop/downshift time. The historical 05:30/06:00 window is only a legacy default when weather/thermal data is unavailable and the machine is otherwise healthy; it must never override an abnormal-heat deadline. Heartbeats are wakeup/visibility prompts, not the main worker.
- Thermal routing update: hot-but-not-dangerous periods run low-power lanes instead of idling. Heavy image/MJ/upscale/browser-write lanes are deferred unless Rex explicitly says AC/fan cooling is on; use `scripts\set_thermal_override.ps1 -Mode on -Hours N` for that window. CPU/memory hard guards remain active even with AC override.
- Instruction triage rule: Rex may send several tasks or corrections in a row. Sort them by business impact, urgency, risk, and dependencies; do not blindly execute every sentence immediately. Preserve deferred tasks in durable backlog/state files so earlier work is not forgotten.
- Event trigger rule: task completion writes `Database/OpenClaw_Next_Action.trigger.json`; local scripts use this as the next-action marker. Codex heartbeat automation must wake this chat for supervised work when the chat has gone idle; it is not a substitute for Codex judgment.
- Progress visibility rule: produce a concrete hourly brief while OpenClaw is active. Use `modules/hourly_progress_brief.py` and report counters such as Etsy 42/250 live, V7 4/60 upload-ready, Shock & Awe 10/30 final, eBay zero-view ratio, current blocker, and next safe action.
- Gemini web-thread rule: when Codex posts a packet to the `Codex 自动化矩阵升级计划` thread, it must later capture Gemini's complete reply and save it locally. If the immediate reply is empty/incomplete, create a follow-up task rather than treating sync as finished.
- Routine review/report/Gemini-sync is locked to the 05:30 ET winddown window. During normal work hours, prioritize concrete monthly task execution over summaries unless Rex explicitly asks for a report or a fatal risk appears.
- Gemini API supervision is a separate every-few-hours advisor lane. It must not be confused with the monthly-task continuation loop and must not stop or replace actual task execution.

Verified Printify correction:
- User/Grey target codes 107, 118, 211, and 1 did not resolve as official Printify blueprints in the current API.
- User/Grey target codes 518 and 11 resolve to apparel, not the intended acrylic/canvas/mug targets.
- Current production anchors for Zone 2 are official Printify blueprints 1471 Photo Block, 1236 Framed Paper Posters, and 1936 Canvas Art Wraps.

Next execution:
1. Rex should visually spot-check the Zone 2 final packet/contact sheets when convenient. Do not wait idly for this review.
2. Prepare Zone 1 and Zone 3 concept sheets using the same quality gate, but avoid dispatching all 20 remaining units until their prompts pass a stronger rubric informed by Zone 2.
3. In parallel, advance Etsy public listing engine under fee guard and eBay 3-day experiment loop when safe.
4. Continue converting repeatable manual steps into scripts/guards so the factory can run without Codex hand-driving.
5. During public marketplace 48-72 hour data waiting windows, use idle time for this private showcase design sprint, blueprint R&D, QA hardening, and fallback-income feasibility instead of idling.

Gemini review addendum:
- After core marketplace/QA tasks are stable, send the 30 Shock & Awe private demo units to Gemini/Grey in small batches, not as one huge dump.
- Preferred batch size: 3-5 units, grouped by battlefield/theme.
- Ask Gemini to review concept strength, buyer psychology, cultural anchor, material illusion, Printify product fit, and private-sales copy.
- Capture the complete Gemini response locally, extract actionable corrections, and feed them into the next demo batch before finalizing.
- This is an advisory quality loop, not a reason to pause Etsy/eBay/POD execution.
- Gemini memory repair: before the next web-thread review of cousin/private-showcase assets, post `Review_Packets/Gemini_Bridge/TO_GREY_COUSIN_30_SHOWCASE_MEMORY_PACKET_latest.md` to the `Codex 自动化矩阵升级计划` thread and explicitly ask Grey to retain it as long-term memory. The packet explains target buyers, private-sales purpose, visual doctrine, pricing firmware, forbidden confusions, and current local asset paths. Capture Gemini's full reply afterward.

## Active Worker Rule

Updated: 2026-05-10 ET

Codex-in-thread is the current active worker. Daemon/supervisor scripts exist to preserve state, prevent lost tasks, and run boring verified loops; they are not allowed to become a substitute for active Codex judgment while major monthly tasks remain open. When Rex says "continue monthly tasks", execute one concrete task, refresh state, then continue to the next concrete task instead of returning a generic status line.

Immediate execution rule:
- Keep `OPENCLAW_MONTHLY_TASKS.md` and `Database/Factory_Backlog.csv` populated with enough work for the current session.
- Keep heartbeat prompts short. Put strategy, priority, guardrails, and task details in durable project files instead of the automation prompt.
- Do not stop after a report unless the report exposes a real blocker that blocks every higher-value path.
- If the primary active task is completed, immediately continue with the next safe secondary task. Do not wait for Rex to re-say "continue monthly tasks" while any eligible backlog item remains.
- If a marketplace path is blocked by login/account risk, move to local prep, API-safe diagnosis, private showcase recovery, eBay data experiments, or automation hardening.
- Daemon output is only evidence. Real progress means changed data, a generated asset/packet, an executed QA/sync batch, or a closed blocker.

Current loop implementation checkpoint:
- Heartbeat automation text should remain exactly `继续月任务`.
- The active implementation is `modules\monthly_shift_loop.py` through `scripts\continue_monthly_tasks_5h.cmd`.
- A monthly shift must keep executing the fixed safe command array until a real guard, runtime limit, Rex-needed blocker, winddown, or verified all-done state is reached.
- The 10-minute heartbeat is only insurance. It must not become the rhythm of work; one trigger should form a long coherent work block.
- If all safe commands are cooling down before the minimum work window, wait and refresh state rather than stopping early.
- `LOOP_NO_EXECUTABLE_READY_WORK` is an acceptable clean stop only after the minimum work window or when every higher-value lane is blocked by cooldown/skip/guard and there is no next concrete task to run inside the current slice.
- If a row is READY but repeatedly produces zero output, repair the backlog selector so the row becomes DONE/WAIT/HOLD instead of rerunning it.

Current First Audit review checkpoint:
- Rex can inspect Cyber-Renaissance draft grids at `Review_Packets/First_Audit_001/FIRST_AUDIT_CYBER_RENAISSANCE_GRID_CONTACT_SHEET.jpg`.
- Detailed grid notes are at `Review_Packets/First_Audit_001/FIRST_AUDIT_CYBER_RENAISSANCE_GRID_REVIEW.md`.
- Raw draft grids are in `Output/First_Audit/Cyber_Renaissance/`.
- No MJ upscale or final `First_Audit_Release` hero folder until Rex selects Top 1% candidates.

## P99 Future Roadmap Note

Rex added V10.0 long-term evolution as a future-only roadmap: RAG memory, adversarial agents, and sandboxed self-healing. This is not a current build task. Include a concise feasibility audit in the next Daily Grey SitRep, then keep current execution focused on P0/P1/P2 production, QA, and marketplace learning.

## 2026-05-10 eBay API Root-Cause Branch

Gemini free-tier supervision and eBay API audit both indicate the short-term money-printer bottleneck is not only visual DNA. Current eBay zero-view products show platform-surface issues that must be fixed before further scaling:

- buyer-facing shipping is not free/clean in API output;
- brand is still `eBay_product_rex`;
- some snippets are thin;
- some galleries are too short or duplicated;
- some Acrylic products need category review.

Current files:
- `Reports/eBay_API_Inventory_Category_Audit.md`
- `Database/eBay_API_Inventory_Category_Audit.csv`
- `Reports/eBay_API_Repair_Plan.md`
- `Database/eBay_API_Repair_Plan.csv`

Next safe action:
1. Do not blindly publish more of the same gallery/brand/shipping setup.
2. Build a small eBay repair experiment: 5 repaired products vs 5 unchanged controls.
3. Repair order: gallery gate first, then free-shipping price/brand/snippet, then category review.
4. Use paid Gemini only if the repair experiment would spend, scale, or change account-risk posture.

## V7 Genesis Correction - Etsy Darwinian Lab

User clarified on 2026-05-09 ET: the new V7 six-pool batch is NOT the cousin/partner recruitment demo. It is an Etsy public-market experiment line for traffic validation. Treat it as Track B, separate from Track A private high-net-worth demo products.

Execution rules:
- Build six Etsy-native digital product pools, 10 listings each.
- Copy/SEO/tags must follow Etsy behavior, not eBay style. Emphasize giftability, craft use case, room/persona, printable/download clarity, and 13 useful tags.
- Do not publish until assets, QA, metadata, duplicate checks, and Etsy fee guard pass.
- Track 14-day results and apply kill/scale rules.

## Etsy Login Anomaly Safety Freeze

Updated: 2026-05-10 09:45 -04:00 America/New_York

Etsy showed the red sign-in error page again during/after high-volume UI work. Treat this as account-risk evidence, not a normal login failure.

Temporary rule:
- Freeze Etsy UI writes, login retry loops, and paid publish actions.
- Keep preparing Etsy-native listings locally.
- Allow read-only Etsy checks and official API/OAuth diagnostics.
- Resume publishing only after official Etsy Open API OAuth is stable and a small reconciled batch confirms listing id, media, fee, and active state.

## Bulk Publish Preflight Rule

Updated: 2026-05-10 09:50 -04:00 America/New_York

Before any future bulk publish to Etsy, eBay, Printify-connected marketplace, Adobe Stock, microstock, Pinterest, or another platform, create a preflight research packet first. It must cover official policy/rate limits, seller best practices, duplicate/spam risk, pacing, fee cap, reconciliation, and rollback. Without that packet, batch publish is blocked.

## UI Automation Safety Rule

Updated: 2026-05-10 10:00 -04:00 America/New_York

Do not adopt stealth/fingerprint-masking/anti-detect tactics for marketplace writes. No `playwright-stealth`, AdsPower-style CDP, webdriver spoofing, canvas/WebGL spoofing, or CAPTCHA/WAF bypass. If Etsy API is blocked, continue local packaging, read-only audits, official OAuth diagnostics, or tiny supervised smoke tests; do not resume UI batch publishing through evasion.

## Sticker Expansion Freeze - 2026-05-11 ET

Rex stopped further Sticker expansion. Reason: eBay sticker market is too price-competitive and low-margin; existing stickers can remain for data/review learning, but do not spend more automation time producing additional Sticker listings unless Rex explicitly reopens the line.

Priority shift:
1. Poster / Acrylic / higher-margin POD products.
2. Etsy digital bundles and market-test pools under fee/risk guard.
3. Shock & Awe private high-end showcase.
4. eBay experiments should favor better product-market fit, pricing, gallery, and higher-value categories rather than more stickers.

## Adobe Stock Account Ready - 2026-05-14 ET

Rex confirmed Adobe Stock contributor account, PayPal, and W-9 are ready. Treat Adobe Stock as a low-risk P3 fallback income line, but keep it behind P0/P1 unless marketplace work is waiting on review/data/platform pacing.

Current state:
- Local-only scaffold exists: `Review_Packets/Adobe_Stock_Passive_Fortress_Scaffold.md`.
- Pilot queue exists: `Database/Adobe_Stock_Pilot_Queue.csv`.
- Draft Adobe CSV exists: `Database/Adobe_Stock_Upload_Metadata_DRAFT.csv`.
- Execution packet exists: `Review_Packets/Adobe_Stock_Pilot_Execution_Packet.md`.
- Contributor upload entry confirmed by Rex: https://contributor.stock.adobe.com/en/uploads?upload=1
- Contributor upload page visually verified by Rex screenshot on 2026-05-14 ET; account access appears ready for manual/web upload after QA.
- Project organization decision: keep Adobe Stock as an isolated subproject inside OpenClaw for now at `adobe_stock_factory/`. It reuses OpenClaw generation/QA modules but keeps public metadata and generated stock assets separated from Etsy/eBay/First Audit language. Generated Adobe assets stay out of git under ignored subfolders.

Rules:
- Internal codename must never appear in public metadata, filenames, CSV upload rows, or Adobe-facing text.
- Adobe line produces stock-safe textures/backgrounds/material fields, not First Audit hero art and not Etsy/eBay/private-client products.
- Quality bar should match regular Etsy/eBay products in craft, resolution, cleanliness, and commercial usefulness, but the product logic must be simpler: Adobe outputs are reusable source materials, not finished OpenClaw-style narrative products.
- Public-facing Adobe assets must not create any obvious bridge to the Etsy/eBay stores: no shared SKU language, no First Audit/atelier/private-sales wording, no marketplace title phrasing, no distinctive product mockup story, and no shop-adjacent brand vocabulary.
- If discovered by the same buyer, the desired perception is: Adobe Stock has premium raw materials; Etsy/eBay has more sophisticated, curated, productized designs built from a higher-order design process.
- Data isolation rule: Adobe may read or imitate Etsy/eBay workflow logic, but all Adobe queue/status/metadata/QA data must remain in Adobe-namespaced files. It must never write to Mentor Hub, Production Line, Etsy/eBay performance stores, Printify backups, or First Audit release data. `modules/adobe_stock_isolation.py` enforces this on Adobe scripts.
- Upload is blocked until image QA, duplicate QA, AI disclosure, and metadata validation pass.
- First safe execution path: generate 5-10 Relaxed draft backgrounds, QA them locally, then prepare a tiny pilot upload batch.

