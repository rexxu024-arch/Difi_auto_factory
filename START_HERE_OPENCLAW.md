# OpenClaw Start Here

Last updated: 2026-05-06 America/New_York

Use this file first after power loss, thread corruption, or moving the factory to a new device. It is intentionally short; deeper details live in `OPERATIONS_MANUAL.md`, `CURRENT_TASK.md`, `PROGRESS_LOG.md`, and `RECOVERY_STATE.json`.

## Operator Roles

- Rex: commander and final business/risk owner.
- Gemini: strategy advisor.
- Codex: execution operator, code debugger, and automation builder.

## Current Business Goal

Build a Printify-first POD factory that can create, QA, publish, monitor, and improve high-quality eBay/Etsy listings with minimal Rex intervention. The near-term marketplace mix is Sticker, Poster, and Acrylic, with Sticker capped when live cover quality or spam risk becomes the bottleneck.

The execution rule is not "more listings at any cost." The rule is stable production, correct buyer-facing images, clean SEO copy, small controlled publish batches, and feedback loops that discover winner DNA.

## Non-Negotiable Rules

- Durable memory lives in repo files, not chat.
- Before deadline work, update `CURRENT_TASK.md`.
- After each batch, update `PROGRESS_LOG.md`.
- Before leaving a thread, write a handoff checkpoint.
- Use New York time for logs.
- Printify remains the main production and marketplace push system.
- eBay/Etsy APIs are support layers for analytics, ads, health checks, metadata experiments, and reconciliation.
- Do not build a second full listing engine unless a verified blocker forces it.
- Do not touch payment settings, orders, buyer messages, or purchases without explicit confirmation.
- Rex has granted default full access for routine OpenClaw project work: files, project account navigation, API debugging, browser automation, QA, report writing, and scripts. Do not repeatedly ask for permission unless a hard red line is involved.
- Use only the Printify Google account `rexxu024@gmail.com`.
- Keep browser tabs minimal; prefer scripts/APIs over manual browser loops.
- Use the dedicated Edge automation profile on CDP port 9223 for marketplace UI work. Do not interfere with Rex's daily Chrome unless explicitly requested.

## Current Image Policy

For Sticker:

- The buyer-facing cover should show the actual 4-piece 6x6 sticker set when possible.
- First-pass Printify/eBay publishing should use the Cover image only as custom marketplace art, plus Printify official product mockups. Do not push U1-U4 as initial marketplace gallery images; live eBay audits showed eBay can choose a single U/detail image as the main cover.
- U1-U4 should remain local QA/detail/reference assets. Add them later only through a separate, audited gallery path.
- Listing descriptions must say the main/product mockup image shows the product received and any supplemental detail/concept images are visual references.

For Poster and Acrylic:

- These are full-surface printed products. Do not use sticker-style cutout or die-cut logic.
- The production design must match the local production image.
- Printify official default/mockup images are allowed and useful because they show the product context.
- Do not delete or fail a product only because Printify exposes multiple default mockups.
- Future R&D: generate premium MJ scene/mockups from the real production image, then pass Vision/manual QA before replacing or supplementing official mockups.

## Recovery Commands

Install/setup on a new machine:

```powershell
git clone https://github.com/rexxu024-arch/Difi_auto_factory.git C:\AIprojects\openclaw_difi
cd C:\AIprojects\openclaw_difi
npm run setup:win
```

Start or reuse the dedicated Edge remote-debug profile for marketplace UI work:

```powershell
npm run browser:edge
```

Run safe local maintenance:

```powershell
npm run local
```

Run network-aware preflight:

```powershell
npm run doctor
```

Check Printify login:

```powershell
npm run printify:login:dry
```

Repair one known cover issue only:

```powershell
npm run printify:cover-repair -- --ids Sticker-Academia-0005 --limit 1 --post-sync-wait 120
```

Audit production design mapping:

```powershell
npm run printify:design-audit
```

Check Etsy API approval:

```powershell
npm run etsy:api-status
```

## Key Files

- `OPERATIONS_MANUAL.md`: full recovery manual and command list.
- `CURRENT_TASK.md`: current priorities and guardrails.
- `PROGRESS_LOG.md`: chronological batch progress.
- `RECOVERY_STATE.json`: machine-readable state snapshot.
- `PROJECT_OPERATING_PROTOCOL.md`: standing operating protocol.
- `PROJECT_FACTORY_ROADMAP.md`: 3-5 day, 7-12 day, 2-4 week automation roadmap.
- `Database/Factory_Backlog.md`: next actions sorted by priority.
- `Reports/`: generated morning reports.
- `Gemini_Advisor/`: summaries for Gemini strategy review.
- `Review_Packets/OPENCLAW_GEMINI_BRIEF.md`: current copy/paste brief for Gemini or another advisor. Use this before older timestamped reports.

## Current Known Blockers

- Some eBay live listings show a single U/detail image instead of the intended cover. Fix path is source repair through Printify, then live eBay buyer-page audit. If source repair cannot sync through inventory-managed variation images, create replacement listings and retire bad ones.
- Etsy API app is still pending/inactive until Etsy approves the key. Etsy UI login works through the dedicated Edge profile; first Etsy Digital gray batch is live: 10 listings, $2.00 confirmed spend.
- Wired LAN was restored on 2026-05-06. Low-bandwidth mode is lifted unless a new network guard check fails. If network quality becomes poor again, fall back to local QA, copy optimization, pricing, registry, and reports instead of bulk upload/publish.

## What To Do Next After Recovery

1. Run `npm run local`.
2. Read `Database/Factory_Backlog.md`.
3. Check `Database/eBay_Cover_Repair_Decisions.md`.
4. If Printify login is valid, repair exactly one cover SKU and inspect live eBay result.
5. Only expand batches after one repair proves stable.
6. For Etsy Digital, read traffic on the first 10 live listings before spending more unless Rex explicitly resumes the next gray cell.
7. Keep Git checkpointing safe code/docs/database state; never commit `.env`, browser profiles, cache, or temporary screenshots.
