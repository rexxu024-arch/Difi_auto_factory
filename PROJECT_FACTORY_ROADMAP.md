# OpenClaw Factory Roadmap

Timezone: America/New_York

## Roles

- Rex: Commander. Owns business intent, final risk calls, spend approvals, and strategic pivots.
- Gemini: Strategy advisor. Provides market framing, buyer psychology, product portfolio critique, and summarizes Rex's broader intent when available.
- Codex: Executive operator. Owns repo memory, implementation, QA gates, local files, Printify/eBay/Etsy execution, automation, and durable handoffs.

Gemini output is advisory input, not an execution authority. Codex may use Gemini's recommendations, but must filter them through repo state, account-risk rules, cost constraints, and Rex's explicit instructions.

## Memory Rules

- Repo files are the durable source of truth.
- Do not rely on chat history as the only memory.
- Before deadline work, update `CURRENT_TASK.md`.
- After each batch, update `PROGRESS_LOG.md`.
- Before leaving a thread, write a handoff checkpoint.
- Gemini summaries should be saved under `Gemini_Advisor/` before they influence recurring automation.

## Phase 1: Minimum Viable Factory, 3-5 Days

Goal: start learning from real market signals without damaging account health.

- Slow eBay public publishing after Akamai/CDN errors.
- Read Seller Hub performance on a schedule.
- Build Etsy brand shell.
- Launch 20-30 curated Etsy listings.
- Unify Printify/eBay/Etsy tracking tables.
- Create basic performance log.
- Mark promising DNA.
- Continue only low-risk, audited small-batch listing work.

## Phase 2: Stable Learning Factory, 7-12 Days

Goal: first reliable semi-automatic money machine.

- Reconcile eBay, Etsy, and Printify states.
- Automatically capture views, clicks, favorites, orders, promoted status, and listing health.
- Diagnose exposure, click, and conversion problems.
- Suggest or apply title, description, tag, image-order, and price changes within safe bounds.
- Pick winner DNA.
- Generate variations from winner DNA.
- Run MJ harvest, asset build, QA, Printify upload, and platform-specific copy.
- Add local or Vision QA gates.
- Publish in cooled, small batches.
- Generate morning reports and anomaly stops.

## Phase 3: Near Unattended Factory, 2-4 Weeks

Goal: stable automated product research, production, and learning loop.

- Market research: eBay/Etsy trends, keyword demand, competitor pricing, visual winners.
- Community response research: Reddit, Pinterest, TikTok, Google Trends where useful.
- Audience mapping: buyer personas, room styles, gifting occasions, collection themes.
- Ad experiments: Etsy Ads, eBay Promoted Listings Standard 2%, controlled A/B tests.
- Customer support assistant: classify messages, draft replies, flag order issues.
- Winner DNA lifecycle: expand, cap, refresh, retire.
- Failure handling: isolate bad assets, retry, downgrade, or hold.

## Current Guardrails

- Do not rapidly publish while eBay Developer/Seller Hub shows Akamai `Zero size object` instability.
- Use Promoted Listings Standard / General only, fixed 2.0%, never suggested rates or Priority/PPC, once advertising setup is stable and approved at action time.
- Sticker count remains capped below 100 until the custom cover/U image issue is proven fixed.
- Poster and Acrylic can use official Printify mockups only when Production_Design matches local source and product type is correct.
- Buyer-facing descriptions must clarify that the main product image represents the item received and additional images are concept/detail references.
- For Etsy, use the existing shop unless there is hidden account risk. Start with curated Poster/Acrylic-heavy selection, not a 200-listing dump.

## Gemini Advisor Cadence

- Morning: Codex writes an overnight report and sends/saves it for Gemini review when available.
- Evening: Gemini can advise on product direction, audience, pricing, and ad hypotheses.
- Major decisions: use Gemini as a second-opinion source for Etsy launch mix, ad tests, and winner DNA expansion.
- Do not send API keys, payment details, buyer private data, or sensitive account information to Gemini.

## 2026-05-05 04:45:18 -04:00 Two-Day Low-Bandwidth Execution Lane
Until Rex confirms Ethernet/low-latency network is active, Codex should prioritize:
1. Local data and text: listing copy candidates, Etsy tags, price/margin matrix, registry/action buckets.
2. Local image QA: gallery derivation, EXIF/metadata checks, file naming, design-to-production hash audits.
3. Code hardening: resilient HTTP retry, checkpointable queues, safe suspend/resume on transient errors.
4. Reports: morning report, Gemini advisor queue, unified performance logs.

Suspend or keep single-item only:
- Bulk MJ / Discord jobs.
- Bulk Printify uploads or publishes.
- Broad eBay/Etsy writes.
- Repeated OAuth refresh attempts.

Default action: if network_guard reports pause/conservative, keep working locally instead of waiting on network.
