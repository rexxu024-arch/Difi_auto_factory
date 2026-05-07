# OpenClaw Operations Manual

Last updated: 2026-05-06 America/New_York

This file is the fast recovery map for Rex, Codex, or another AI/operator after a broken thread, power loss, or new-device setup.

## Project Rule

Printify remains the main production and marketplace push system. eBay/Etsy APIs should be added narrowly for analytics, ads, health checks, metadata experiments, and reconciliation. Do not create a second full listing engine unless a verified blocker forces it.

## Fast Recovery

If the thread breaks, read `START_HERE_OPENCLAW.md` first. It is the short handoff map for Rex, Codex, Gemini, or another AI/operator.

## Image And Mockup Policy

- Do not treat Printify official mockups/default images as an error by default. They help buyers understand the physical product context.
- For Sticker, the custom cover should show the actual 4-piece sticker set when possible.
- For Poster and Acrylic, the production image is one full print surface. Do not use die-cut or sticker-splitting logic.
- The must-pass gate is production-design correctness and buyer-facing honesty: the printed design must match the local production image, and the listing description must clarify that additional images are concept/detail/reference views unless the listing explicitly offers variations.
- Future R&D may generate premium Midjourney scene/mockups from the real production image, but those images require QA before replacing or supplementing Printify's official mockups.

## Roles

- Rex: Commander and final business/risk owner.
- Gemini: Strategy advisor.
- Codex: Executive operator and factory debugger.

## New Device Setup

1. Clone the repo:

```powershell
git clone https://github.com/rexxu024-arch/Difi_auto_factory.git C:\AIprojects\openclaw_difi
cd C:\AIprojects\openclaw_difi
```

2. Create `.env` from Rex's private credential source. Never commit `.env`.

Required keys used by the current factory:

- `Printify_API_KEY`
- `Printify_EBAY_SHOP_ID`
- `Printify_ETSY_SHOP_ID`
- `PRINTIFY_LOGIN_EMAIL=rexxu024@gmail.com`
- `DISCORD_TOKEN`
- `GUILD_ID`
- `CHANNEL_ID`
- `DEEPSEEK_API_KEY`
- `CLAUDE_API_KEY`
- `Etsy_Key_string`
- `Etsy_shared_secret`

3. Install dependencies:

```powershell
npm run setup:win
```

If npm is not available:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

4. Start or reuse the dedicated Edge remote-debug profile for marketplace UI tasks:

```powershell
npm run browser:edge
```

5. Run the factory preflight:

```powershell
npm run doctor
```

## Main Commands

```powershell
npm run local
```

Refreshes safe local maintenance: QA, registry, market queue, cover decisions, replacement queue, title queue, traffic report, backlog, morning report, and Gemini queue.

```powershell
npm run doctor
```

Runs network-aware supervisor and writes:

- `Database/Factory_Autopilot_State.json`
- `Database/Factory_Autopilot_Action_Queue.csv`
- `Database/Factory_Autopilot_Action_Queue.md`

```powershell
npm run printify:login
```

Checks/recover Printify login in the Chrome CDP profile. It only allows Google account `rexxu024@gmail.com`. If Google asks for a password or a different account, it stops.

```powershell
npm run printify:cover-repair
```

Runs exactly one source-cover repair, then live eBay cover audit. Do not scale until one SKU becomes `LIVE_COVER_FIXED` or confirms replacement-listing fallback.

```powershell
npm run printify:design-audit
```

Checks whether Printify front print-area image matches local `Production_Design.png` visually and by dimensions.

```powershell
npm run etsy:api-status
```

Checks whether Etsy API key has become active. As of the latest check, it is still pending/inactive.

```powershell
npm run system:resources
```

Samples CPU, memory, GPU counter availability, battery/power, and thermal sensor availability, then writes the current resource allocation decision.

```powershell
npm run system:resources:watch
```

Runs the resource allocator as a lightweight monitor. It writes:

- `Database/System_Resource_Policy.json`
- `Database/System_Resource_State.json`
- `Database/System_Resource_Allocation.csv`

Resource decisions are `RUN`, `RUN_CONSERVATIVE`, `DEFER_TO_NIGHT`, or `PAUSE_COOLDOWN`. Factory supervisor now includes this resource strategy in its state.

```powershell
npm run hardware:heartbeat
```

Samples CPU, memory, GPU counter availability, battery/power, fan probe, and thermal sensor availability. Writes:

- `Database/Hardware_Heartbeat_State.json`
- `Database/Hardware_Heartbeat.csv`

```powershell
npm run grunt:seed
npm run grunt:queue
npm run grunt:dry
npm run grunt:once
```

Runs the OpenClaw Grunt Engine background-task layer. The Grunt Engine owns portable local work that does not need Rex decisions: hardware heartbeat, local supervisor refresh, quality-floor scans, market/SEO report refreshes, and rest-window maintenance planning.

It writes:

- `Database/Grunt_Task_Queue.jsonl`
- `Database/Grunt_Engine_State.json`
- `Database/Grunt_Engine_Run_Log.csv`
- `Database/Grunt_Maintenance_Plan.json`

Rest-window disruptive actions such as restart, battery cycling, and disk optimization are planned only and are not executed unattended.

```powershell
py modules\ebay_quiet_jade_pivot.py --prepare --apply-local --limit 42
py modules\ebay_quiet_jade_pivot.py --sync-printify --limit 42
```

Runs Operation Quiet Jade style metadata pivots for active eBay listings using local workbook + Printify API. This path updates title, description, and enabled variant price only; it does not publish images or shipping templates.

```powershell
py modules\ebay_ui_title_revise.py --ids <ID1,ID2> --cdp-port 9223
```

Title-only Seller Hub fallback for rows where Printify metadata updates do not propagate to eBay. Use dedicated Edge CDP profile only.

```powershell
py modules\etsy_digital_ui_publisher.py --limit 1
```

Publishes the next approved Etsy Digital gray-test listing through the dedicated Edge profile. Use only when `Database\Etsy_Fee_Kill_Switch.json` and `Database\Account_Risk_State.json` allow it.

## Current Blocking State

The primary blocker is live eBay image integrity:

- Many Sticker live pages show one U/detail image as buyer-facing main image instead of the intended 4pc cover.
- Printify product `images` are read-only in ordinary API update flow, so source repair currently requires Printify UI in CDP profile.
- Public publish remains blocked until one source repair or replacement listing path passes live eBay audit.

Current next command after Printify login is available:

```powershell
py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120
```

## Important Files

- `CURRENT_TASK.md`: current operating rules and active priorities.
- `PROGRESS_LOG.md`: chronological completed work.
- `RECOVERY_STATE.json`: compact machine-readable recovery state.
- `PROJECT_OPERATING_PROTOCOL.md`: standing permissions and guardrails.
- `PROJECT_FACTORY_ROADMAP.md`: 3-5 day, 7-12 day, and 2-4 week plan.
- `Database/Factory_Backlog.md`: sortable task backlog.
- `Database/Factory_Autopilot_Action_Queue.md`: current supervisor actions.
- `Database/System_Resource_State.json`: current hardware/resource guard state.
- `Review_Packets/AI_LABOR_FACTORY_KERNEL_AND_HARDWARE_PLAN.md`: portable AI labor kernel and 24-hour laptop protection plan.
- `Reports/latest morning_report_*.md`: latest human-facing summary.
- `Gemini_Advisor/latest gemini_review_queue_*.md`: strategy advisor packet.

## Account/API Boundaries

Allowed without repeated confirmation:

- Project files under this repo.
- Project account navigation, local file edits, API debugging, browser automation, QA checks, report writing, and script changes related to OpenClaw.
- Printify status/audit/draft repair/listing preparation.
- eBay/Etsy Seller Hub read-only inspection.
- Printify/eBay/Etsy local data reconciliation.
- Small recoverable probes that do not create orders, touch payments, or exceed an approved fee cap.

Pause or ask before:

- Payments, orders, purchases, subscriptions, billing settings.
- Buyer messages.
- Etsy listing-fee-triggering publishes beyond the current written cap.
- Broad public eBay/Etsy publishing if supervisor flags cover/network/account risk.

## Marketplace Strategy Memory

- eBay: 2% Promoted Listings Standard/General only. No Priority/PPC. Ignore suggested ad rate.
- Etsy: existing shop is now usable through Edge UI. First Digital gray batch is live: 10 listings, $2.00 spend. Do not bulk dump; read traffic before spending more unless Rex explicitly resumes the next gray cell.
- Product creation and mockups remain Printify-first.
- eBay/Etsy APIs are support layers, not a replacement for Printify unless the image/variation blocker forces it.

## Git Checkpoint Automation

Codex has an active automation:

- Name: `Openclaw Git Checkpoint Push`
- Cadence: every 2 hours
- Target: `origin main`
- Rule: stage only safe project code and durable deliverable data; never commit `.env`, browser profiles, caches, screenshots, or uncertain secrets.

If checking manually:

```powershell
git status
git remote -v
```

## Handoff Template

Before ending a thread, write this into `PROGRESS_LOG.md`:

```markdown
## YYYY-MM-DD HH:MM -04:00 Handoff Checkpoint
handoff checkpoint: <current blocker>, <next safe command>, <do-not-do rules>.
```
