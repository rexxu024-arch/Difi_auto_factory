# OpenClaw Monthly Tasks

Last updated: 2026-05-09 ET

This file is the durable monthly-task contract. When Rex says "continue monthly tasks", or when the heartbeat wakes this chat, Codex itself should read this file, `CURRENT_TASK.md`, `OPENCLAW_OPERATING_RULES.md`, `PROGRESS_LOG.md`, `Database/Strategic_Mode.json`, `Database/Factory_Backlog.csv`, and the latest local state files, then directly execute a supervised task drain. Local scripts are tools, not the owner of the shift.

Automation policy:
- Old 10-minute worker/daemon/dispatcher logic is not the production model for the current phase.
- `continue monthly tasks` maps to Codex-in-chat reading the durable task files and executing a long supervised drain across eligible tasks.
- Heartbeats exist to wake Codex back into the thread when the chat would otherwise go idle. They are not a substitute for Codex judgment.
- Active raw logs use a 7-day retention window. The watchdog runs `modules\log_retention_archive.py`; it backs up and archives old raw detail, then keeps the active `PROGRESS_LOG.md` focused on progress bars, risk anchors, and the last seven days of raw work.

## Execution Contract - Codex Is The Active Worker

- Current-stage rule: Codex in this thread is the primary worker. Do not replace Codex judgment with daemon health reports while major monthly tasks remain open.
- 95% supervision rule: until a lane is proven stable, assume Codex must actively supervise it. Local scripts may execute only deterministic, repeatedly validated, low-risk work without active Codex judgment.
- Trusted-script threshold: a lane is trusted only after it has dry-run/readback evidence, produces measurable state changes, has guard coverage, and does not require aesthetic, pricing, platform-risk, account, or strategy judgment.
- If a script hits an untrusted decision, repeated no-op, new marketplace warning, fee ambiguity, login/OAuth issue, or API/schema failure, it must mark `CODEX_NEEDED` and stop that lane. Do not count that as healthy autonomous progress.
- HUD rule: the local dashboard is for visibility. It does not mean Codex is absent or that a background script has permission to make judgment calls.
- AI-delegation rule: if Codex attention must be freed later, judgment can be delegated only to an explicit low-cost AI reviewer with budget guards and saved responses. Do not replace Codex judgment with ordinary scripts.
- "Continue monthly tasks" means: pick the highest-priority safe task, execute it, refresh backlog/state, then immediately pick the next task until a real guard stops work, the 05:30 ET winddown window begins, or all eligible tasks are verified complete.
- Daily shift rule: one Rex "start/continue monthly tasks" command should produce a long Codex-supervised work block, not a short script and not a passive daemon check.
- Heartbeat role: wake Codex, read the durable task list, execute supervised progress, then report useful progress. It must not become a passive health rhythm.
- Default-chat rule: this thread treats "continue monthly tasks" as an execution command, not a reporting command. The expected result is concrete state change, not unchanged health counters.
- Loop rule: after each task, move to the next command in the fixed safe array. If a command has no work, it logs and the loop continues instead of stopping.
- Do not spend cycles on cosmetic automation complexity while core production, QA, marketplace experiments, or private showcase gaps remain open.
- Backlog sufficiency rule: monthly-task files must always contain enough actionable tasks for at least one full work session. If the eligible queue becomes thin, add the next concrete tasks from the business plan before idling.
- Two-day runway warning rule: if the executable monthly backlog is estimated to contain two days or less of meaningful work, Codex must notify Rex and create/update the Gemini packet before the queue actually empties. Use `py modules\monthly_task_runway_monitor.py`; it writes `Database/Monthly_Task_Runway_State.json`, `Review_Packets/Rex_Monthly_Task_Runway_latest.md`, and `Review_Packets/Gemini_Bridge/MONTHLY_TASK_RUNWAY_ALERT_latest.md`.
- Reporting is not progress unless it directly unlocks a decision, records a blocker, or closes a task. Default to building, QA, packaging, API-safe diagnostics, or market experiment preparation.
- Log cleanup is not production work. It is allowed as tiny maintenance only because it prevents context bloat; it must not touch assets, databases, CSV queues, marketplace state, credentials, or anything not explicitly classified as a log/archive.
- Rex-action blocker reporting rule: permissions, account eligibility, OAuth/app approval, billing, login/security warnings, and marketplace account settings that likely require Rex must be captured in the 05:30 ET Gemini/Grey web-thread report and the Rex action packet the same morning. Do not let these blockers sit silently across days; if they block a cash-flow lane, write the exact URL/page, observed error, and the smallest Rex action needed.
- Current implementation rule: automation is for memory, guardrails, repetitive verified chores, and waking the chat. When Rex leaves Codex open, Codex-in-thread remains the primary executor. Do not replace real execution with a health report, daemon status, or unchanged counters.
- Network watchdog rule: during normal monthly-task loops, periodically run `py modules\network_path_monitor.py --expected-alias "Ethernet 3"`. It should quietly log current default route, Ethernet link speed, and Wi-Fi state. Notify Rex only if active network path stops being `Ethernet 3`, Ethernet drops below Up/1 Gbps, or repeated alerts appear.
- 48-hour network sampling rule: from 2026-05-13 12:19 ET to 2026-05-15 12:19 ET, Windows Task Scheduler runs `OpenClaw Network Path Sampler` every 10 minutes. Do not notify Rex on normal samples. Use `py modules\network_path_summary.py --expected-alias "Ethernet 3"` to decide whether the Ethernet adapter is likely unstable.
- Continuity proof: use local state files only as evidence of what happened, not as proof that Codex can disengage. If state shows no meaningful progress, Codex must directly pick and run the next safe task.
- SSD infrastructure rule: Rex bought a PNY 1TB SSD, expected in about one week from 2026-05-13. Until it arrives, keep C: pressure low by avoiding duplicate raw assets. Run `py modules\ssd_migration_plan.py` as a planning-only task. When the drive arrives, migrate heavy asset folders (`Output`, `Release`, `First_Audit_Release`, harvest folders, Adobe Stock batches) to the SSD with checksum verification and NTFS junctions, while keeping `.env`, browser profiles, active databases, `.git`, source code, and `.venv` on the internal disk unless benchmarking proves otherwise.

## Active Concrete Queue

This queue must stay populated. When one item is completed or blocked, refresh `Database/Factory_Backlog.csv`, append the result to `PROGRESS_LOG.md`, and move to the next safe item.

## 3-Day Revenue Priority Override - 2026-05-16 to 2026-05-19 ET

Rex's current ordering is mandatory for the next three days:

1. **Adobe Stock production first.**
   - Build only commercially useful, high-quality stock materials/backgrounds.
   - Reject flat, low-resolution, generic, or visually worthless drafts.
   - Use macro/material DNA, correct resolution, metadata/IP QA, AI disclosure, and separation from Etsy/eBay/First Audit branding.
   - The target is a credible first upload-ready pilot, then a daily baseline of about 50 QA-passed stock assets once quality is proven.
2. **Sticker liquidation as Etsy digital material bundles second.**
   - Use former Sticker POD assets as internal source material and digital resource bundles.
   - Do not expand Sticker POD.
   - Package U/upscaled high-quality assets into Etsy-safe ZIP parts, generate preview images, and use Etsy-native title/description based on market evidence.
3. **Daily Etsy/eBay listing drip third.**
   - Continue reasonable daily listing/experiment cadence under account, fee, QA, and marketplace guards.
   - Etsy/eBay remain testing grounds, but do not let routine drip crowd out Adobe production during this three-day window.

If a higher lane is blocked by a real guard, move to the next lane; do not idle or rerun reports.

## V15.5 Dual-Track Purge And Studio Gift Pivot

Updated: 2026-05-13 ET

Current doctrine:
- Stop low-price blind volume. Sticker expansion is closed, and low-value Digital only survives when it is useful market-signal inventory.
- Clean algorithmic dead weight: Etsy/eBay low-value assets below USD 15, especially digital/sticker/planner/printable patterns, should be moved out of active sale when API evidence supports it. Zero-signal non-POD experiments are purge candidates even when exact 48-hour counters are unavailable.
- Use reversible actions first: inactive/draft/end with durable logs, not destructive local deletion.
- Public release cadence is now 3-5 high-quality listings/day maximum, focused on optical acrylic blocks, framed/premium posters, and executive-gift user stories.
- Each new premium public item needs strong mockups and no repeated-gallery risk. No bare white/transparent-only uploads for premium POD.
- Pricing matrix:
  - Entrance / business gift: USD 48-98.
  - Bundle / matched executive desk set: USD 149.
  - Anchor / waitlist object: USD 250+ and deliberately scarce.
- First Audit / Studio assets are physically separated from Etsy Archive. Premium Top 1% assets must not be cheap public-market inventory.

Standing commands:
- `py modules\v155_purge_and_release.py --policy hard --max-price 15 --min-age-hours 48` audits low-value Etsy active listings under the current hard purge rule.
- `py modules\v155_purge_and_release.py --apply --policy hard --max-apply 120 --max-price 15 --min-age-hours 48` performs the reversible Etsy inactive move after audit.
- Output packet: `Reports/V155_Great_Purge_And_First_Release.md`.
- Current state: Etsy V15.5 hard purge is complete; active inventory is physical-only, with 0 active downloads and 0 active listings below USD 15. eBay purge is candidate-only until the live item-level performance and safe ending path are verified.
- First V15.5 release folder: `Release/OC-V155-001-Executive-Jade-Desk-Gift`.

0.5. Etsy/eBay public-market experiment doctrine: treat both stores as active testing grounds for finding OpenClaw's traffic code, not as static catalogs. Be bold with product type, design DNA, title angle, pricing, ads, and bundle format experiments, but every experiment must preserve cost guardrails, account-risk pacing, QA, and measurable readback. Digital products remain a limited Etsy sensing pool; the stronger direction is high-quality Printify-backed POD that Codex judges fit the platform and buyer use case. Sticker expansion is frozen unless a narrow no-loss review/reputation test is explicitly useful.
0.6. Daily marketplace drip: every active workday, before lower-value maintenance/reporting, attempt one safe public-market experiment cycle when guards allow it. Etsy may publish a small API/Printify-backed batch under the $50 normal / $60 hard cap; eBay may publish or adjust a small Poster/Acrylic/high-value experiment batch under gallery/cover/price/ad guards. If a platform warning, login anomaly, fee cap, duplicate gallery, First Audit leak, or external-id ambiguity appears, stop that lane and switch to local prep or the other marketplace. Do not expand Sticker inventory.

0. V13 The First Audit studio pivot: maintain a physical wall between Etsy Archive and OpenClaw Design Studio. Premium Top 1% visuals belong to `THE FIRST AUDIT: 001` and must not be diluted into cheap marketplace SEO inventory. Build lookbook, audit manifest, archive-retirement packet, and Studio-only Printify draft readiness before any public-platform use.
0.1. Cyber-Renaissance First Audit expansion: use the 21 concept queue in `Database/First_Audit_Cyber_Renaissance_Draft_Queue.csv` to generate Midjourney draft grids only. Absolutely no automatic upscale. Convert concepts into `Database/First_Audit_Cyber_Renaissance_MJ_Dispatch_Queue.csv`, dispatch initial grids in controlled batches, harvest/QA, and only after Rex marks a Top 1% candidate build the final one-folder release under `First_Audit_Release/[ä½œå“ç¼–å·_ä¸­æ–‡ä»£å·]/`.
0.2. Midjourney resource rule: the USD 30 MJ plan has no Relaxed-hour usage limit that we need to conserve like a quota, so draft grids may use Relaxed Mode when they materially advance P0/P1 work. Do not abuse Relaxed for low-value churn, but do not block important draft exploration just to "save relaxed". The scarce resource is Fast/Upscale time. Fast/Upscale is reserved for Rex-selected Top 1% studio assets, production-ready marketplace heroes, or explicit print-quality needs; routine draft grids must not auto-upscale.
1. Shock & Awe private showcase recovery: execute the 6-gap recovery queue without using the raw Discord interaction path; use verified UI submission or a newly captured safe dispatch path, then harvest, QA, and create private Printify drafts.
1.1. MJ identity-locked scene experiment: run the 9 prompts in `Database/MJ_Identity_Locked_Scene_Experiment.csv` through a verified MJ path, then QA whether the product itself stayed unchanged. Only promote a parameter set into the mockup generator if it preserves product identity across Poster/Acrylic/Digital samples.
2. eBay zero-view recovery: turn dry-run SEO/intent plans into a controlled local workbook patch, then sync only a small API-safe batch through Printify/eBay and measure 48-72h impact.
3. eBay gallery integrity: identify repeated/gallery-risk listings and choose between Printify rebuild, Seller Hub supervised repair, or retire/replace. Do not publish more public products with unresolved gallery-source ambiguity.
4. Etsy public engine while account risk is frozen: continue local package building, QA, metadata, tag/title/description, fee ledger, and API/OAuth diagnostics; no Etsy UI writes or paid publish until the login anomaly clears.
5. Gemini/Grey supervision: run API check-ins on real decisions and parse tasks into local queues; daily web-thread sync belongs in winddown, not in the middle of core production.
6. Marketplace performance loop: every 3 days refresh eBay data, compare experiment groups, mark losers, and feed winners into DNA/variation generation.
7. Automation hardening: convert repeated proven manual steps into small scripts with rollback, fee guard, risk guard, and QA gates. Do not overbuild broad daemons while high-value tasks remain open.

Gemini check-in separation:
- The 5-hour monthly work block is not a Gemini supervisor trigger.
- Gemini free/paid checks are advisory tasks on their own cadence. They should not preempt private showcase recovery, Etsy/eBay production learning, or QA work unless there is a high-risk spend/account/scaling decision.
- Routine backlog continuation should usually pick the highest-value concrete production/QA/market task before any advisor-only task.

V8.1 defense tasks:
- For Printify physical POD creation, use the compliant two-layer metadata guard in `modules/metadata_defense.py`. Internal Printify metadata should be concise and accurate; public marketplace SEO can be richer but must not misrepresent or bypass review.
- For Etsy API-created digital listings, run `modules/etsy_shadowban_sentinel.py` after the visibility window. A public 404/410 pauses further paid Etsy publishing until reviewed.
- Grey/Gemini SitRep failures must be recorded locally and must not stall marketplace-safe or local monthly tasks.
8. Fallback income research only after P0/P1 are not actively blocked: Adobe Stock/microstock feasibility, reusable metadata, QA, and submission scaffolds.

## P0 - Adobe Stock / Sweatshop First Submission Sprint

Updated: 2026-05-15 ET

MJ account-risk update, 2026-05-19 ET:
- Midjourney/Discord page showed a 5-day temporary block message tied to suspected third-party tools or scripting.
- Until Rex clears this state, all raw Discord API dispatch and automated Discord/MJ UI submission are hard-frozen.
- Adobe Stock production must continue through existing local assets, metadata QA, duplicate guards, upload ledgers, local non-MJ processing, and future manually/approved generation paths only.
- Do not treat a 204 Discord interaction as success. No MJ job is considered submitted unless there is a safe, visible, policy-compliant confirmation path.

Strategic shift:
- Cousin/First Audit review moved to early June, so First Audit is no longer the immediate top workload.
- Adobe Stock / sweatshop becomes the current P1 cashflow infrastructure lane until the first high-quality submission batch is ready.
- Goal for tomorrow: prepare and submit, or be ready to submit, the first high-quality Adobe Stock material/background batch.
- Daily target after the pilot is accepted by QA: 50 QA-passed, commercially safe stock images/day, with metadata and AI disclosure prepared.

Execution rules:
- Adobe assets must be separated from Etsy/eBay brand assets and from First Audit private assets.
- Stock assets are high-quality commercial material/background bricks, not finished OpenClaw studio products.
- Use Adobe-specific mentor/product files only. Do not pollute Printify/Etsy/eBay Production_Line or Mentor_Hub.
- Maintain quality comparable to normal OpenClaw visual work, but simplify commercial use so it cannot be confused with Etsy/eBay premium products.
- Generate title and keyword metadata suitable for stock search, including Created using AI disclosure where required.
- Before upload: run image QA, duplicate/IP risk scan, metadata QA, and keep a local submission manifest.
- Upload packaging rule: stage Adobe files in neutral 50-file folders under `adobe_stock_factory/upload_ready/batch_###_[material_hint]`, not date-based folders. The material hint is only local archive/reference context; Adobe metadata remains per-file title/keywords/category. Source dates may remain only in manifests.
- Upload resume rule: after Adobe confirms files were accepted, run `py modules/adobe_stock_mark_batch_uploaded.py --folder batch_###... --files ...` or `--limit N` so only confirmed local staged filenames receive `_uploaded`. The batch folder receives `_completed` only after every real upload image in that folder is `_uploaded`. If an upload-ready batch is not `_completed`, every future upload-prep pass must resume that incomplete folder before creating a new 50-file batch.
- Repetition guard: once a material/theme family approaches roughly 150 staged/submitted images, reduce same-family production unless the next run adds clear new value through hybrid material, lighting, camera distance, usage context, or pattern variation. This prevents low-quality duplicate flooding and keeps the stock line useful.

Standing next actions:
- Build/refresh Adobe mentor DNA and production queues.
- Generate/QA first 25-50 pilot images.
- Prepare CSV/metadata and upload checklist for Adobe Contributor.
- Keep first upload conservative and review rejection/acceptance feedback before scaling.
## P0 - Private Showcase: Shock and Awe 30 Demo Products

Goal: within 14 days, produce 30 top-tier private-channel showcase products to impress Rex's partner and prove OpenClaw can sell status, story, material illusion, and cultural confidence, not just images.

Rules:
- This is not eBay/Etsy public listing work.
- Use Printify as the fulfillment backend, but do not sync this packet to public marketplaces unless Rex explicitly converts a design into a marketplace product.
- Quality beats volume. Spend extra time/API only when it improves visual accuracy, cultural leverage, product fit, or private-sales usefulness.
- Every finished unit needs Midjourney prompt, broker hook, studio spec sheet, Printify production vector, image QA, and private fulfillment readiness.
- Current first battlefield: Zone 2 / Epic Mythology, Cyber-Fusion, Cultural Assassin, 10 units already queued/submitted to Midjourney. Next step is harvest, visual QA, iteration, and Printify-private draft preparation.
- Gemini/Grey critique loop: once a small set of demo units is materially ready, send 3-5 units at a time to the Gemini thread `Codex è‡ªåŠ¨åŒ–çŸ©é˜µå‡çº§è®¡åˆ’` for second-opinion review. Capture the full reply locally, extract only actionable corrections, and apply them to later units. Do not let this advisory loop replace production work or become a report-only task.
- Gemini memory repair: before the next web-thread critique, send `Review_Packets/Gemini_Bridge/TO_GREY_COUSIN_30_SHOWCASE_MEMORY_PACKET_latest.md` to the `Codex è‡ªåŠ¨åŒ–çŸ©é˜µå‡çº§è®¡åˆ’` thread so Grey remembers that the 30-unit cousin showcase is a private high-net-worth Studio demo line, not Etsy/eBay/Adobe public inventory. Ask Grey to retain the strategic context, then capture the full response locally.

## P1 - Etsy Public Listing Engine

Goal: start Etsy as the main public testing battlefield and use a controlled paid listing pool to find market signal.

Rules:
- Publish Etsy listings only within the fee guard.
- Normal spend cap: USD 50.
- Absolute ceiling: USD 60 unless Rex explicitly expands the budget after real signal.
- Budget semantics: paid Etsy listing actions are allowed while projected spend remains under the configured caps and account/QA/reconciliation guards pass. The fee guard is a budget throttle, not a blanket paid-action freeze.
- New-shop pacing strategy: treat Etsy as a weak/new account until it shows stable signal. Start with official API recovery probes and slow drip publishing, not quota-filling.
- Etsy cadence ladder:
  - First 48 hours after any login/payment/API anomaly: 1-3 listings/day, API-only, one listing per probe, reconcile active state/media/files/fee before continuing.
  - After 48 hours clean: 3-6 listings/day, spread across 12-18 hours with varied product pools and no UI batch work.
  - After 7 clean days with no red login error, payment warning, or listing suppression: 6-10 listings/day maximum unless Rex approves a new scale packet.
- Do not spend the 200-listing Etsy test pool quickly. Use it as a 3-5 week Darwinian experiment budget so Etsy can learn the shop gradually and so OpenClaw can observe which pools earn views/favorites/orders.
- Avoid spam-like frequency. Use controlled batches, varied timing, varied product pools, and Etsy-native copy.
- Etsy copy must be Etsy-native: artistic, warm, giftable, decor/persona/room-use focused, with proper 13-tag strategy where applicable.
- Sticker liquidation digital bundles are fixed at 20-image small packs and a 50-image mega vault. Specs belong mainly in the description; titles may mention only buyer-critical value such as `20+`, `50+`, `High Resolution`, `PNG`, or `Bundle`.
- Titles, tags, descriptions, pricing, product photos, and digital/physical distinction must be checked before publish.
- Etsy image-count rule from Seller Hub: listings with too few photos get search-visibility improvement warnings. Digital products should not ship with a single preview only; build at least 4-6 preview images when possible (cover, content preview, usage context, detail zoom, file/dimension note). POD listings should keep official Printify mockups plus design/close-up images without duplicating the same image repeatedly.
- Usage-scene image rule: scene/mockup images must preserve the exact product identity. Do not let Midjourney reinterpret the product. Use the original production/cover image as a high-weight locked image reference; keep subject shape/pattern/color/proportion unchanged, and only vary room context, camera, lighting, crop, and styling. Default MJ scene prompt should use low chaos/stylize, strong identity language (`preserve exact product design, no redesign, no pattern changes`), and the highest practical image weight. If identity drift is visible, mark HOLD instead of using the scene image.
- If an existing Etsy listing is edited, there is no new listing fee. If it is deleted/replaced with a new listing, the new listing spends another USD 0.20.
- Keep experiment data so winners can be scaled and losers can be stopped.
- Default next move when Etsy paid publishing is blocked or not due: keep building/QAing V7 digital products locally, run API read/status checks, and prepare the next one-per-pool batch; do not keep retrying UI login.
- Daily action: if paid/API guards are green and the shop has not already received today's safe batch, publish or prepare the next 1-3 Etsy listings from the highest-quality POD/digital queue, then reconcile listing id, media count, fee ledger, public visibility, and source-product mapping before any further Etsy write.
- Implementation anchor: the long-shift loop includes `etsy_pod_publish_drip`, which attempts one guarded Printify-to-Etsy POD publish per pass. This is allowed while projected spend stays under the configured cap and account/QA/reconciliation guards pass; it must not be treated as frozen merely because it spends the normal Etsy listing fee.

## P1 - eBay 3-Day Experiment Loop

Goal: stop waiting passively on low-traffic listings. Every 3 days, read performance, adjust experiments, and record results.

Rules:
- Account context: eBay is a 4-year old store with 34 positive reviews and prior secondhand sales, but POD/AI wall-art/sticker products are a new category for the account. Treat the account as stronger than Etsy but still category-cold.
- eBay cadence ladder:
  - Current default: 5-10 listings/day when publishing is needed, not one large burst.
  - If three days pass with no warning, no duplicate/search-manipulation risk, and gallery/cover audits are clean: test 10-15 listings/day.
  - Do not publish 50-100/day just to use free quota; previous 0-view data shows that traffic fit and gallery/title/category quality are the bottleneck.
- New listings must be materially distinct by product type, buyer intent, image set, title angle, and category/user story. Do not mass-publish near-duplicates.
- Capture views, impressions/clicks when available, promoted status, listing age, product type, title strategy, cover/gallery status, and price/ad settings.
- Analyze whether the problem is product type, title/SEO, category, price, gallery quality, account weight, ad rate, or traffic fit.
- Adjust experiments with controlled changes: ad rate groups, title/description variants, product type mix, new user stories, or relisting/replacement where justified.
- Winners get scaled. Weak listings are marked. If a listing stays dead for 1-2 weeks after several adjustments, record it for deletion or let the matured policy decide.
- Report concise conclusions to Rex/Gemini.
- Daily action: if eBay has safe quota and no account/gallery/cover warning, push a small Poster/Acrylic/high-value experiment batch or apply one controlled ad/title/price/category experiment. Do not publish new Stickers. Every action must update the experiment table so the next 3-day read can compare variants rather than guessing.
- Current implementation anchor: eBay daily publishing remains blocked until the shipping/source readback path is clean. While blocked, the daily loop should continue eBay traffic diagnosis, candidate prep, price/ad/title planning, and Seller Hub/API capability notes instead of forcing risky live publish.

## P2 - Automation and Self-Operating Factory

Goal: reduce Codex manual labor over time. The pipeline should become runnable mostly by code, with Codex observing, debugging, and improving instead of hand-driving each item.

Rules:
- Each repeated manual step should become a script, guard, queue, or QA gate when stable.
- Critical checks include fee guard, risk guard, cover/gallery gate, design-image match gate, Printify production-file integrity, Etsy/eBay metadata style, and account-health pacing.
- Gemini/Grey supervision is part of the default factory loop:
  - run routine free-tier API advisor check-ins every few hours;
  - run `py modules\grey_overseer_v8.py --allow-paid` for the daily structured V8 audit when a paid-tier review is warranted;
  - use paid-tier Gemini only for high-stakes spend/risk/scaling/repeated-failure reviews or free-tier failure;
  - parse Grey output into local review queues before acting;
  - update the Gemini thread `Codex è‡ªåŠ¨åŒ–çŸ©é˜µå‡çº§è®¡åˆ’` during the 05:30 ET winddown when idle/focus guards permit;
- Once a flow is stable, move Codex attention to higher-value projects: Etsy digital products, private-channel showcase, visual asset factory, and future fallback income engines.
- Keep durable logs, compact reports, and Gemini/Grey action packets current so context can be recovered after thread/browser/power failure.

## P2 - Project Mirror / Reference-Derived Aesthetic DNA

Goal: raise Mentor Hub from generic prompt invention to reference-derived premium taste. Project Mirror converts carefully selected real-world references into original OpenClaw material, lighting, composition, and buyer-intent DNA without copying source images.

Rules:
- Use source images for DNA extraction only. Do not redistribute reference images or treat them as marketplace assets.
- Prioritize three high-value lanes: NYC Luxury, European Dark Academia, and Imperial Kintsugi.
- Reject Pinterest spam, low-resolution assets, obvious AI renders, direct IP, and anything that would drag the brand back into cheap generic decor.
- Distilled output must become Mentor-Hub-compatible DNA: physical material parameters, light distribution matrix, composition rules, purchase-intent word cluster, and negative prompt cluster.
- Build A/B tests against the old Claude-only prompt logic before promoting any reference-derived DNA into production.

Current files:
- `Database/Aesthetic_DNA_Pool_Index.csv`
- `Database/Aesthetic_DNA_Source_Candidates.csv`
- `Database/Aesthetic_DNA_Distillation_Schema.csv`
- `Review_Packets/Project_Mirror/PROJECT_MIRROR_DNA_PIPELINE.md`
- `Database/Project_Mirror_State.json`
- `Database/Premium_DNA_Source_Queue.csv`
- `Database/Premium_Mentor_Hub.csv`
- `Database/Premium_DNA_AB_Comparison.csv`
- `Review_Packets/Project_Mirror/PREMIUM_DNA_EXTRACTION_V1.md`

Next safe action:
- Fill accepted source URLs and local references in the pool index, then build the first vision/LLM distillation script. Keep this behind P0/P1 marketplace execution, but use it whenever marketplace work is waiting on data, platform pacing, or Rex review.

Tier-routing rule:
- Low/known product lanes may use existing OpenClaw DNA plus Codex curation when the goal is cheap market sensing or daily POD drip.
- Mid-tier public POD should mix existing OpenClaw DNA with the new Premium Mentor Hub material/lighting rules.
- First Audit, cousin-demo assets, $128 acrylics, $149 bundles, and $295 anchors require source-derived premium DNA and Codex/Rex visual review before upscale or publish.
- Use A/B/C comparison before promoting a DNA family:
  - A = old imagination / existing OpenClaw prompt logic.
  - B = source-derived Vision/API distillation from top visual references.
  - C = Codex/Rex-standard curation based on prior feedback and product fit.
- B+C is mandatory for top-tier assets. A+C is acceptable only for routine POD and low-risk tests.

## P3 - Fallback Income Factory / AI Labor Channels

Goal: after the Printify/Etsy/eBay core engine is stable enough, start building a low-marginal-cost fallback income line that can repeatedly turn AI labor into real revenue.

Candidate tracks:
- Adobe Stock or similar microstock pipeline: large-scale generation of high-quality, commercially safe images with metadata, QA, and submission automation.
- Multi-node stock distribution: reuse metadata and assets across Adobe Stock, Freepik, Shutterstock, Wirestock, or other suitable platforms where terms allow.
- Other repeatable AI labor channels that can produce practical income without high platform risk or heavy manual customer service.

Rules:
- This is not allowed to displace active P0/P1 work until the main Printify/Etsy/eBay tasks are no longer blocked by missing Rex input or time-sensitive execution.
- Reuse OpenClaw modules where possible: prompt DNA, image QA, risk guard, metadata builder, queueing, report packets, and spend/rate-limit guards.
- Before committing to a new platform, produce a cold engineering/business feasibility report: time-to-deploy, expected payout delay, content acceptance risk, account-ban risk, IP/commercial-safety constraints, and required human setup.
- Favor boring, repeatable, compliant labor over flashy but fragile hacks.

## P99 - Future V10 Digital Twin / RAG / Multi-Agent Evolution

Status: backlog only. This is a future feasibility audit after the first Printify/Etsy/eBay engine is stable and producing recurring cash flow. It must not consume current production bandwidth, marketplace publish time, or Midjourney/Printify execution slots.

Scope:
- Evaluate a RAG long-term memory layer for V-series protocols, error logs, Rex standards, and platform lessons.
- Evaluate adversarial red/blue agent review for high-risk decisions before spend, publish, or account-risk actions.
- Evaluate a self-healing loop in an isolated sandbox for code patches after API/tool failures.
- Evaluate Phase 1 low-cost stabilizers: SQLite for durable local Product ID/log/SEO persistence, Photoroom or Remove.bg API for post-MJ background removal and Printify template composition, and Notion API for daily SitRep / high-end asset-library sync.
- Evaluate V10+ expansion tools: ChromaDB / FAISS for local RAG memory, CrewAI / LangGraph for red-blue multi-agent review, and Stripe API for a future direct private-sales payment surface.

Current rule:
- Do not implement the V10 stack now.
- Merge only a compact feasibility note into the monthly comprehensive report or daily Grey SitRep appendix when the system is otherwise idle; do not run live API onboarding or paid trials during production windows.
- Keep V10 lower priority than P0 private showcase, P1 Etsy/eBay marketplace learning, P2 QA/automation hardening, and P3 fallback-income feasibility.

## Scheduling Guidance

- If more than 2 hours remain before winddown, prioritize P0/P1 core progress and core optimizations.
- If less than 2 hours remain, prioritize QA, reports, Gemini/Grey packet, logs, and handoff cleanup.
- If marketplace tests are waiting for 48-72 hour data, use that waiting window for P0 private showcase work, blueprint R&D, QA gates, and automation hardening.
- Do not idle just because one path is blocked by login, UI, API approval, or platform delay. Move to the next safe high-value task.
- If P0/P1/P2 are all waiting on external platform data or Rex input, advance P3 feasibility and scaffolding so the machine keeps creating future earning options.

## Weak-Network / Platform-Blocked Fallback

When Discord, Adobe Contributor, Etsy, eBay, Printify, or Gemini are unavailable, switch to the local-only work map instead of idling. The canonical packet is:

- `Review_Packets/Network_Restricted_Task_Map.md`

Allowed local fallback lanes include Adobe metadata QA, old-training salvage with Rex/sharpness/duplicate filters, sticker ZIP packaging, marketplace lifecycle planning, First Audit folder hygiene, local contact sheets, and git-safe cleanup planning.

Do not run Adobe upload, Discord/Midjourney dispatch, marketplace publish/write, or bulk browser UI actions when login/captcha/network/account guards are dirty.

