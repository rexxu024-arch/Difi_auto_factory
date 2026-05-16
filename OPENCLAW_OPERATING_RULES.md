# OpenClaw Operating Rules

This file is the durable handoff anchor for Codex, Grey/Gemini, and Rex.

## Rex Operating Memory

- The durable interpretation layer for Rex's standards lives in `OPENCLAW_REX_OPERATING_MEMORY.md`.
- Read that file before major planning, recovery after context loss, new-machine setup, marketplace strategy, visual QA, or any task where Rex has previously corrected Codex behavior.
- Rex's repeated feedback is training data. The expected direction is less Rex micromanagement over time: Codex should infer standards, encode them in rules/code/UI, park only the blocked lanes, and keep safe work moving.
- Codex has autonomous technical execution authority inside learned Rex standards: use Rex's historical preferences, requirements, approvals/rejections, business goal, and engineering judgment to choose concrete safe paths without asking for every tactical detail.
- Codex owns code-level blind spots that Rex/Gemini cannot inspect. Safe implementation fixes, reliability patches, schema repairs, QA gaps, and maintainability improvements should be done directly and logged.
- Repeatedly corrected C-Class mechanics, especially the monthly-loop/visibility layer, must not become an open-ended engineering sink. Use the simplest reliable solution and return compute to production work.
- This autonomy is bounded by explicit Rex stop/pause commands, privacy/credential safety, account-risk guards, irreversible destructive actions, and configured spend caps.
- When this file and chat memory conflict, use the latest explicit Rex instruction first, then `OPENCLAW_REX_OPERATING_MEMORY.md`, then the rest of this operating file.

## Default Startup Behavior

- When Rex opens Codex into this OpenClaw chat, Codex should first provide a concise boot brief:
  - bigger-picture work completed since the last packet
  - current blockers
  - what Rex needs to provide, apply for, log into, approve, or inspect
  - what should be copied to Gemini/Grey
  - spend/risk status
- Unless Rex gives a different high-priority instruction, Codex should then continue monthly tasks automatically.
- "Continue monthly tasks" means use the durable backlog/state files, not chat memory alone.

## Default Chat Action

- In this OpenClaw thread, the default action is active monthly-task execution.
- If Rex says only "continue monthly tasks" or a heartbeat sends the same instruction, Codex must not treat it as a request for a status report.
- Daily shift contract:
  - One human Rex command such as "start monthly tasks", "continue monthly tasks", or "开始/月任务" should ensure a full OpenClaw work shift, not a single short slice.
  - Practical command: `scripts\continue_monthly_tasks_5h.cmd`.
  - The block runs `modules\monthly_shift_loop.py`, a fixed safe command array inside a plain while loop.
  - It keeps stepping through that array until the dynamic weather/resource winddown window, unless a real fee/account/hardware/privacy guard, explicit Rex stop, tool/runtime limit, or Rex-needed blocker stops all safe lanes.
  - Old cruise dispatcher, 10-minute daemon, and watchdog logic are deleted. Heartbeats are admin/winddown only; they are not the production cadence.
- Required sequence:
  1. Read `CURRENT_TASK.md`, `OPENCLAW_MONTHLY_TASKS.md`, this file, `PROGRESS_LOG.md`, `Database/Factory_Backlog.csv`, `Database/Monthly_Shift_Loop_State.md`, and `Database/Strategic_Mode.json`.
  2. Choose the highest-priority safe task that is not blocked by fee, account, hardware, login, or explicit Rex stop guards.
  3. Execute concrete work.
  4. Refresh backlog/state.
  5. Continue to the next safe task until a real guard, natural tool/runtime limit, Rex-needed blocker, dynamic winddown, or verified all-done state.
- Practical entrypoint for a bare "continue monthly tasks":
  - Run `scripts\continue_monthly_tasks_5h.cmd`.
  - If the loop stops in under 10 minutes without a fee/account/hardware/Rex-needed blocker, inspect `Database\Monthly_Shift_Loop_State.md` and fix the fixed command array instead of reporting unchanged status.
  - If one command finishes, continue with the next command in the same shift rather than waiting for another prompt.
  - If one command has no immediately executable READY rows, move to the next command in the fixed array. Do not treat one short script as a completed monthly-task slice.
  - If all safe commands are temporarily dry, keep cycling the fixed array until winddown or an explicit guard.
  - First Audit / Cyber-Renaissance tasks are core production work, not report work. If a First Audit MJ draft-grid queue is READY, it should outrank local maintenance unless a hard guard blocks it.
- Valid progress means one of: generated/QAed asset, marketplace/API-safe action, data repair, closed blocker, updated experiment table, improved automation code, or durable packet ready for Rex/Grey. Repeating unchanged counters is not progress.
- If the selected task produces no state change, Codex must repair the selector/backlog or move to the next eligible lane instead of reporting the same state again.

## Continuous Cruise Rule

- Cruise work should not be a one-shot script that runs once and stops.
- If Rex has not explicitly paused/stopped the project, the system should keep choosing the next eligible task.
- Daily operating window: from Rex opening/booting Codex until the dynamic weather/resource duty deadline, OpenClaw is considered "on shift." It should not idle between tasks unless Rex explicitly pauses/stops, Codex is closed, a fee/account/hardware guard blocks all safe work, or every backlog item has been checked and confirmed complete.
- The app heartbeat is not the worker. Production work is the primitive monthly shift loop started by Rex/Codex in this thread.
- After each completed task, immediately rebuild/read the backlog, choose the next highest-value safe task, and continue. Only exit the loop for the dynamic winddown window, guard blocks, explicit Rex stop, or all-done verification.
- If the current primary task is genuinely complete, do not report idle status and stop. Immediately step down to the next eligible secondary task by priority, business impact, and safety. The only valid idle state is a verified all-done state where every primary and secondary backlog lane has been checked.
- Midjourney/Printify/UI tasks may still insert a short physical wait because external grids, upscales, mockups, and marketplace syncs are not instantaneous.
- Midjourney resource interpretation:
  - Relaxed Mode draft grids are allowed for high-value P0/P1 work because the current USD 30 MJ plan has no Relaxed-hour usage limit that needs conservation like a quota.
  - Do not waste relaxed jobs on low-value churn, but do not pause important draft exploration merely to conserve relaxed time.
  - Fast/Upscale minutes are the constrained resource. Use them only for Rex-selected Top 1% studio assets, production-ready hero images, or explicit print-quality bottlenecks.
- If Rex asks for manual wakeups, use:

```powershell
scripts\continue_monthly_tasks_5h.cmd
```

## Codex-Supervised Execution Rule

- The UI and local scripts are observability and conveyor-belt tools. They do not replace Codex as the active supervisor.
- Default operating mode is `CODEX_SUPERVISED`: Codex should remain involved in judgment, repair, strategy, visual QA, pricing, marketplace risk, API schema changes, and any task that can affect account health, spend, brand quality, or public listings.
- A script may run without active Codex judgment only when the task is all of the following:
  - deterministic and low-complexity;
  - repeatedly validated on this project with successful dry-run/readback evidence;
  - reversible or read-only, or explicitly protected by fee/risk/QA guards;
  - not dependent on aesthetic judgment, account/security interpretation, marketplace policy ambiguity, or new business logic.
- Examples that can be delegated after validation: local CSV refreshes, image-size/hash QA, duplicate-gallery scans, packet generation, log retention, read-only status probes, and already-proven one-item API drips inside guards.
- Examples that require Codex supervision: new product/DNA decisions, First Audit quality choices, Adobe stock strategy, Etsy/eBay publish pacing changes, pricing/ad changes, login anomalies, OAuth/account permissions, API failures, platform warnings, unexpected zero-output loops, and any task with repeated errors.
- If a script reaches an untrusted lane, repeated no-op, platform/account warning, ambiguous fee/spend state, or a task not covered by its validation set, it must mark `CODEX_NEEDED` in local state/UI and stop that lane rather than pretending the long shift is healthy.
- Rex's ideal target is that Codex is materially involved in at least 95% of non-trivial work until the pipeline has been explicitly proven stable. Automation is allowed to reduce hand labor only after validation, not before.
- A dashboard "alive" status only means the conveyor belt is running. It does not mean the work is strategically correct, safe to scale, or exempt from Codex review.
- If future scale requires freeing Codex attention, judgment may be delegated only to a bounded low-cost AI review lane such as DeepSeek/Gemini/other approved API, with explicit prompt, budget guard, output capture, and Codex/Rex review rules. Plain scripts must never impersonate business, aesthetic, account-risk, or marketplace judgment.

## Rex Instruction Triage Rule

- Rex often sends several requirements, corrections, or new ideas in rapid sequence. Treat them as an evolving requirement stream, not a strict first-in-first-out command queue.
- For every new Rex instruction, first classify it by:
  - business impact toward cash-flow, private showcase quality, or factory automation
  - urgency/deadline and remaining time before the dynamic weather/resource winddown
  - fee/account/security/privacy risk
  - dependency status such as login, OAuth, browser access, network, or Rex/Gemini review
  - whether it is a correction to an active flow or a future backlog idea
- The newest instruction usually steers the current turn, but it does not automatically erase earlier active tasks unless it clearly conflicts or explicitly supersedes them.
- Do not interrupt a high-value running task for a lower-value new idea. Persist lower-priority ideas into `OPENCLAW_MONTHLY_TASKS.md`, `CURRENT_TASK.md`, `Database/Factory_Backlog.csv`, or the relevant review packet so they are not forgotten.
- If Rex gives a hard stop/pause, payment/privacy red line, or explicit P0 override, obey immediately.
- If Rex provides strategic guidance rather than an exact implementation, Codex should choose the safest and highest-ROI execution path that matches the business goal, even if that means correcting a small tactical mistake in the proposed method.
- Steer-conversation return rule:
  - If Rex interrupts with a question, correction, or quick strategic note, answer or patch the relevant rule, then return to the active monthly-task loop.
  - A steer-conversation answer is not a stop signal.
  - Only pause the loop when Rex explicitly says stop/pause, a fee/account/privacy/hardware guard blocks all safe lanes, or the next step genuinely requires Rex login/approval/inspection.

## Rex Delegated Authority Boundary

- Rex has granted Codex default full access for OpenClaw-related local files, APIs, logged-in project pages, project automation, and project account maintenance.
- Do not repeatedly ask Rex for permission for normal OpenClaw work when the action is reversible, project-scoped, and below the configured spend/risk limits.
- Hard boundaries that still require explicit Rex confirmation or must be avoided:
  - spending beyond configured budgets, placing orders, issuing refunds, changing billing/payment instruments, or creating financial liabilities outside the active cap;
  - exposing, exporting, or mishandling private credentials, personal identity data, payment details, customer private data, or non-project private files;
  - irreversible deletion of business-critical assets without a backup or clear local replacement;
  - marketplace evasion behavior, bot-defense bypass, stealth fingerprinting, CAPTCHA bypass, or anything that creates account-chain risk;
  - actions that conflict with Rex's latest explicit stop/pause instruction.
- Default behavior inside the boundary: make the safest reasonable decision, log it, and keep moving toward the business goal. Rex should be asked only for decisions that truly require the owner, not for routine tool/file/browser operations.

## C-Class Infrastructure Failure Protocol

- Small routing, heartbeat, loop, visibility, cleanup, and status-bridge tasks are C-Class infrastructure. They must be solved with the simplest linear design that can pass an observable test.
- First Rex complaint about a repeated C-Class defect is treated as a failure signal, not a discussion topic.
- C-Class repair deliverable must include:
  1. root cause in one paragraph;
  2. the smallest patch or rollback-to-primitive fix;
  3. one validation command and the exact success signal;
  4. durable rule/file update;
  5. fallback plan if the app/automation layer is unreliable.
- Timebox: 60 minutes hard cap for C-Class repair. If not fixed within that window, stop improving the architecture, fall back to the most primitive working method, preserve a concise blocker packet for Gemini/Grey, and return compute to S-Class business work.
- Three-strike rule: after two failed fixes plus one validation miss, freeze the clever approach. Do not spend more OpenClaw time inventing dispatcher layers, nested daemons, or complex callbacks for a C-Class problem.
- Rex must not be forced to QA C-Class internals. Rex sees only the visible success signal, such as "one start command produced continuous work plus regular progress briefs."
- Separate the worker from the visibility bridge:
  - worker: the primitive long-shift monthly task loop;
  - watchdog: a tiny health/restart check;
  - visible bridge: short chat progress summaries.
  A failure in one layer must not trigger needless rewrites of the others.

## Model / Reasoning Effort Policy

- Default working assumption for OpenClaw is high-reasoning mode: use the strongest available Codex model/reasoning setting for architecture, marketplace strategy, visual QA, pricing, risk decisions, debugging, and any task that affects published listings or paid spend.
- Medium/low reasoning is only acceptable for mechanical repeat work that is already encoded in scripts, such as file counting, local CSV refreshes, simple status probes, log compression, or deterministic batch cleanup.
- If a task intentionally drops to a cheaper/faster mode, it must return to high-reasoning mode before touching strategy, marketplace copy, QA decisions, publish flows, pricing, or account-risk logic.
- Repo code cannot directly switch the parent Codex chat model or reasoning effort. Codex must surface a boot/winddown reminder when the UI/model setting appears mismatched with the current high-stakes task.
- Delegated subagents, if Rex explicitly requests them, should inherit the strongest practical reasoning setting for hard engineering/research subtasks and use cheaper settings only for bounded mechanical subtasks.

## Gemini / Grey Supervision Rule

- Grey/Gemini is a default advisor lane, not an optional side quest.
- Keep two loops separate:
  - Task-continuation heartbeat: every short interval, only wakes Codex to keep doing monthly tasks from durable files.
  - Gemini/Grey supervision: independent advisory cadence; it should not be treated as the next monthly task just because the heartbeat fired.
- Gemini API check-in is a separate supervisor lane that runs every few hours when useful. It is not the same as "continue monthly tasks", must not consume the normal work loop, and must not be used as a substitute for concrete execution. Monthly task execution continues before and after Gemini check-ins unless a real risk/blocker is discovered.
- V8 Grey Overseer is the daily API supervision lane:
  - run `py modules\grey_overseer_v8.py --allow-paid` for the daily structured audit when a paid-tier review is warranted;
  - free/Flash is used for micro-cleaning noisy logs and extracting counters, blockers, error codes, and risks;
  - paid/Pro is used only 1-2 times per day or for high-stakes spend/risk/scaling/repeated-failure decisions;
  - it writes `Review_Packets/Gemini_Bridge/Daily_Grey_SitRep_YYYYMMDD.txt` and `Daily_Grey_SitRep_latest.txt` for Rex to copy to web Grey.
- V8 API failure must never stall OpenClaw. If Gemini times out, 429s, or fails after retries, record the failed audit locally and continue the local task loop.
- Routine API supervision should run through `modules/gemini_supervisor_checkin.py`:
  - free-tier Gemini checks routine status, backlog priority, and likely blind spots every few hours.
  - paid-tier Gemini is sparse and cost-guarded; use it for high-stakes spend, scaling, repeated failure, or free-tier failure.
  - Grey/Gemini output is advisory only and must land in local review/task files before any execution. It must never directly mutate live marketplace data.
- Daily web-thread sync targets only the Gemini thread:
  - `https://gemini.google.com/u/1/app/d2ab3afa2778aa9e`
  - thread title: `Codex 自动化矩阵升级计划`
- Gemini web sync is low-frequency and belongs to the dynamic winddown packet or major-breakthrough/fatal-blocker events only.
- Web sync must use Edge/CDP plus idle/focus safeguards; if Rex is actively using the machine, prepare the packet locally and delay sending instead of stealing focus.
- Every Gemini web sync must be a closed loop: after sending a packet to the `Codex 自动化矩阵升级计划` thread, Codex must poll until Gemini's full response is available or until a documented timeout. Save the complete response into `Review_Packets/Gemini_Bridge/` and extract actionable advice into the relevant backlog/rules/report. Sending without response capture is incomplete and must be marked for follow-up.
- Review/report/Gemini-sync timing rule: routine review packets, progress summaries, Gemini/Grey web sync, and "what did we do" reports are reserved for the final dynamic winddown window. Outside that window, do real monthly task execution instead. The only exceptions are fatal account/fee/privacy/hardware risk, Rex explicitly asking for a review/report now, or a major breakthrough that needs immediate confirmation.

## Monthly Workstreams

The durable monthly task list lives in `OPENCLAW_MONTHLY_TASKS.md`. When Rex says "continue monthly tasks", use that file as the source of truth and do not rely on chat memory alone.

## Pricing Strategy Rule

- Low-value traffic products should be priced as review/traffic builders: never intentionally lose money after production, shipping, marketplace fees, payment fees, and ads, but accept low margin when it helps earn views, trust, and early sales.
- Mid-tier products should balance margin and conversion. Use market comps, platform behavior, and ad-rate experiments to find the best profit/traffic point rather than maximizing price blindly.
- High-value/private-showcase products should preserve premium margin and status aura. Use small batches and curated presentation to test market acceptance before scaling.
- Every price experiment must include all mandatory costs, including Printify production cost, Printify shipping cost when the customer sees free shipping, platform fees, payment/fixed fees, listing fees when applicable, and ad rate.
- If ads increase to 4%-12% or higher, adjust source/platform price so the listing remains profit-positive unless Rex explicitly approves a loss-leader experiment.

## Daemon Scope Rule

- The local daemon is a conveyor belt, not the decision maker.
- It may run only hardened, atomic, reversible, or low-risk work such as local CSV refreshes, image QA, packet generation, report generation, read-only status checks, and previously verified API probes.
- It must not independently troubleshoot complex platform problems, bypass marketplace defenses, retry login anomalies, change account settings, publish paid listings, alter billing/payment/order/customer settings, or make strategy decisions.
- If a task produces no measurable state change, repeats the same row/batch, hits account-risk signals, exceeds a fee guard, or requires interpretation beyond coded rules, the daemon must stop that lane, record the blocker, and leave the issue for Codex supervision.
- Codex remains the active engineering/strategy layer. The daemon exists to keep safe repetitive work moving while freeing Codex for debugging, business judgment, QA standards, and new pipeline development.

## Progress Visibility

- The daemon may work quietly, but Rex should receive a concrete progress brief about once per hour while OpenClaw is active.
- The brief must use measurable counters, not generic "healthy" language. Required counters include Etsy live/target and spend/cap/risk state, V7 Etsy concepts/MJ/harvest/QA/upload-ready progress, Shock & Awe private-demo progress, eBay zero-view/view/promoted snapshot, top blocker, and next safe action.
- The canonical local generator is `modules/hourly_progress_brief.py`, which writes `Reports/hourly_progress_latest.md` and `Database/Hourly_Progress_State.json`.

Current workstreams:

- P0: The First Audit studio pivot. Etsy is a low-price digital resource archive; OpenClaw Design Studio is the private physical-asset atelier. Do not let Top 1% visuals leak into Etsy/eBay bulk inventory. Studio pricing uses integer firmware only: $48, $128, $295. Studio carriers are optical acrylic blocks, archival studio prints, and premium framed posters only.
- P0: Shock and Awe 30 private-channel demo products within 14 days. These are Printify-backed private showcase assets, not public marketplace listings.
- P1: Etsy listing engine. Publish controlled Etsy batches under the fee guard, with Etsy-native SEO, titles, tags, descriptions, pricing, and non-spam pacing. Normal cap USD 50, absolute ceiling USD 60 unless Rex expands it.
- P1: eBay 3-day experiment loop. Read performance every 3 days, adjust ads/listings/product/user-story experiments, record winners and failures, and report concise conclusions.
- P1 daily marketplace drip. While OpenClaw is on shift, treat one safe eBay/Etsy experiment cycle as a daily default task, not an optional report item. Publish/adjust only through fee, account, cover/gallery, external-id, pricing, and First Audit leak guards. Etsy prioritizes API/Printify-backed POD and curated digital bundles; eBay prioritizes Poster/Acrylic/high-value experiments. Sticker expansion remains frozen.
- P2: Automation/self-operating factory. Convert stable manual operations into scripts, queues, guards, and QA gates so Codex can move to higher-value work.
- P3: Fallback income factory. When core marketplace/private-showcase work is waiting or stable, research and scaffold repeatable AI labor income channels such as Adobe Stock or microstock distribution, reusing OpenClaw quality/risk/metadata infrastructure.

## Time-Budget Priority

## Continue Monthly Task Contract

- A Rex/manual `继续月任务` command means one continuous work block, not one small action.
- Default work block target is adaptive, not fixed: run until the forecast/resource-based duty deadline for that day, not a hard-coded 05:30/06:00 boundary.
- The historical 05:30/06:00 winddown is only a fallback when no weather-aware deadline is available.
- In hot season, the duty deadline is computed from `Database/Thermal_Task_Schedule.json`: heavy production should run through the next safe cool window (<80F forecast) and wind down when that cool window ends or when hardware/account/fee/Rex-needed guards require it.
- The goal is not a fixed 17-hour day. The goal is 90-95%+ self-supervised useful work during the safe operating window. On cool days this may mean near-continuous production; on hot days it means heavy work in cool windows and light work during heat windows.
- Thermal rule: if ambient forecast is >=80F or local resource pressure is high, defer Midjourney/upscale/heavy image processing to the next cool window and immediately pull a low-CPU task such as API polling, SEO/tag generation, sticker ZIP packaging, database audit, market notes, or queue cleanup. Heat is not an excuse to idle unless every safe light lane is blocked.
- During the block, execute the highest-priority safe task, refresh backlog/state, then immediately execute the next safe task.
- Stop only for a real guard: account risk, fee cap, hardware/thermal risk, network failure, missing Rex login/approval/inspection, tool/runtime limit, or verified all-done state.
- Reports, Gemini web-thread sync, daily review packets, and unchanged counters belong in the final admin window before that day's dynamic duty deadline unless Rex explicitly asks for them or a critical blocker needs immediate escalation.
- The 10-minute heartbeat is only a safety net. It is not the worker cadence and must not become an excuse to do one tiny task per trigger.
- If all high-priority tasks are cooling down, wait and refresh state inside the current work block before falling back to low-value tasks.
- If the remaining backlog is under roughly 2 days of real work, notify Rex/Gemini during the next admin window and keep executing current tasks.

- More than 2 hours before the dynamic winddown:
  - prioritize core factory progress, core QA, core marketplace learning, and core optimizations.
  - do not let low-value local maintenance permanently crowd out growth work.
- Marketplace timing rule:
  - When eBay/Etsy experiments are already published or staged and need 48-72 hours of traffic data, do not keep poking them just to feel busy.
  - Use that waiting window for high-leverage private showcase work: Shock and Awe visual concepts, Printify blueprint R&D, QA gates, production-file preparation, and review packets.
  - If Rex is expected to review a premium visual product, produce a reviewable v1, preserve the source prompt/payload, then iterate 1-3 versions from Rex/Gemini/partner feedback before treating it as final.
- If the eligible backlog looks likely to finish within 24 hours:
  - warn Rex in the next concise brief that more strategic tasks should be queued.
  - keep working current tasks until actually empty; do not idle early.
- If the estimated executable monthly backlog looks likely to finish within 2 days:
  - run `py modules\monthly_task_runway_monitor.py`.
  - create/update `Review_Packets/Rex_Monthly_Task_Runway_latest.md` and `Review_Packets/Gemini_Bridge/MONTHLY_TASK_RUNWAY_ALERT_latest.md`.
  - notify Rex/Gemini that the strategic queue needs replenishment while continuing the current backlog.
- During the final winddown window before the dynamic duty deadline:
  - stop starting long tasks.
  - write reports, logs, Gemini packet, and safe handoff.
  - run the Grey API supervisor pass and attempt the low-frequency Gemini thread sync only if idle/focus guards allow it.
  - prepare for the computed soft off-shift.
- The computed soft off-shift is not a hard kill:
  - if no task is active, the daemon may exit and leave the host idle.
  - if a task unexpectedly runs past the computed duty deadline, let it finish safely, then exit.
  - do not force-kill marketplace, file-write, API, or browser tasks solely because the computed deadline arrived.
- Final 30 minutes before soft off-shift are winddown only:
  - consolidate logs
  - refresh Rex/Gemini report
  - summarize today's core problems and solved issues
  - list what Rex must actively handle next
  - do not start uploads, publish flows, or browser-long operations

## Spend and Account Rules

- Metadata defense:
  - Use a compliant two-layer metadata model for physical POD: Printify/product-creation metadata may be concise and neutral, while Etsy/eBay marketplace metadata may be richer and SEO-focused.
  - Both layers must accurately describe the product. Do not use false "vanilla" subjects, fake materials, or unrelated labels to bypass Printify/provider/platform review.
  - The production layer should minimize noisy SEO language and avoid unnecessary provocative phrasing, but it must not conceal prohibited content or misrepresent the product.
  - The marketplace layer may use long-tail SEO only after the product is created/synced, and only if it remains truthful, platform-compliant, and buyer-clear.
- Public visibility sentinel:
  - Do not trust API `201 Created` alone for digital listings. Schedule a no-login public URL probe after the visibility window.
  - If a confirmed listing returns 404/410 in public probing, pause further Etsy paid publishing and mark the account state for review before scaling.
- No bulk publishing on any marketplace without a preflight research packet. Before batch listing, Codex must document: official platform policy/rate limits, accepted seller practice or high-signal community experience, duplicate/spam risk, pacing/jitter plan, fee cap, rollback/reconciliation plan, and first-batch QA criteria.
- If the preflight packet is missing, stale, or contradicted by a new platform error, batch publishing is blocked. Continue only with local prep, read-only checks, or a tiny manually supervised smoke test.
- Revenue product market gate:
  - Anything intended to make money must pass a market-evidence gate before title, price, metadata, or publishing is treated as ready.
  - Evidence must include official platform constraints plus at least two market/commercial signals such as Etsy search comps, eRank, EverBee, Alura, Sale Samurai, EtsyHunt, Adobe contributor guidance, or other high-signal public/paid research sources.
  - Etsy titles must be Etsy-native: aesthetic, use case, buyer persona, and pack value first. Put only conversion-critical specs in the title, such as `20+`, `50+`, `High Resolution`, `PNG`, or `Bundle`; put exact file specs in the description.
  - For digital bundles, descriptions must lock buyer expectations: quantity, file type, ZIP parts, transparent-background caveat, 300 DPI metadata, approximate pixel range, license limits, and instant digital delivery/no physical shipping.
  - The reusable local gate is `modules/market_research_gate.py`; outputs live under `Reports/Market_Evidence_Gate_latest.md` and `Database/Market_Research/`.
- Platform API use does not override marketplace quality/risk rules. API publishing is preferred for stability, but account safety still depends on cadence, uniqueness, fee control, login health, media correctness, and buyer-facing quality.
- Default marketplace cadence:
  - Etsy new/weak account: 1-3/day during recovery, 3-6/day after 48 clean hours, 6-10/day only after 7 clean days.
  - eBay older but category-cold account: 5-10/day by default, 10-15/day only after clean 3-day checks.
  - Do not fill platform quotas unless data shows that quantity is the limiting factor.
- If a marketplace daily drip has already written/published today, subsequent loops should prefer reconciliation, QA, performance reads, or private showcase work instead of forcing another paid write.
- Do not use stealth/fingerprint-masking/anti-detect browser tactics to bypass marketplace WAF, bot detection, account enforcement, CAPTCHA, or login-risk systems.
- Do not add `playwright-stealth`, AdsPower-style anti-detect CDP, navigator/canvas/WebGL fingerprint spoofing, or similar evasion layers to marketplace write flows.
- UI automation is allowed only for compliant maintenance, read-only checks, or tiny supervised smoke tests when official APIs are unavailable. Marketplace scaling must prefer official APIs, platform-native bulk tools, or manual human operation.
- Etsy paid publish remains controlled by `Database/Etsy_Fee_Kill_Switch.json`.
- Etsy budget policy: listing-fee spend is allowed inside the budget. Do not freeze paid actions just because they cost money. Freeze only when projected spend exceeds the configured daily/pool/hard cap, when paid-state reconciliation is ambiguous, or when account/QA/risk guards block the lane.
- Etsy normal cap USD 50; absolute ceiling USD 60 unless Rex explicitly expands after real signal.
- Editing an existing Etsy listing is free. Deleting/replacing with a new listing creates another USD 0.20 listing fee.
- If Etsy shows the red sign-in error page (`An error has occurred, please try again!`) during or after listing work, treat it as a login/anomaly risk, not a normal form failure.
- On Etsy login anomaly: immediately freeze Etsy UI writes, login retry loops, and paid publish actions. Continue only with read-only Etsy checks, local listing preparation, official API/OAuth diagnostics, reports, and non-Etsy monthly tasks.
- Resume Etsy paid publishing only after the official Etsy Open API token path is stable and a small reconciled batch proves that listings, media, and fees are confirmed without ambiguity.
- eBay ads must remain Promoted Listings Standard / General only unless Rex changes the rule.
- Never touch payment/billing/order/customer-message settings unless Rex gives a direct, explicit instruction.
- Marketplace UI work belongs in Edge/CDP, not Rex's daily Chrome.

## Memory Rule

- Repo files are the durable memory. Chat is not the only memory.
- Update `PROGRESS_LOG.md` after material work.
- Log retention is fixed at 7 days for active raw detail:
  - run `py modules\log_retention_archive.py` through the monthly-shift watchdog;
  - before compaction, create a full backup and raw archive under `Reports\Log_Archives\`;
  - completed and verified historical work may be represented in the active log as project progress bars/counters instead of full detail;
  - unresolved blockers, account/fee/privacy risks, errors, HOLD/PENDING states, and Rex-needed actions must remain visible as compact risk anchors;
  - never treat log cleanup as asset cleanup. Do not delete images, production files, databases, marketplace state, credentials, or business CSVs.
- Keep the current Rex/Gemini packet in:
  - `Review_Packets/Rex_Action_Packet_latest.md`
  - `Review_Packets/Gemini_Bridge/TO_GREY_rex_needs_latest.md`
