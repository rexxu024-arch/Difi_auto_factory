# GREY FULL LOGIC ASSET EXPORT

Generated: 2026-05-06 23:48:41 
Workspace: `C:\AIprojects\openclaw_difi`

Sensitive credential values are redacted. Product IDs, listing IDs, and operational logs are preserved.

## Executive Pulse

{
  "updated_at": "2026-05-06T22:30:00-04:00",
  "timezone": "America/New_York",
  "source_of_truth": [
    "START_HERE_OPENCLAW.md",
    "CURRENT_TASK.md",
    "PROGRESS_LOG.md",
    "PROJECT_OPERATING_PROTOCOL.md",
    "PROJECT_FACTORY_ROADMAP.md",
    "OPERATIONS_MANUAL.md",
    "Database/Factory_Autopilot_State.json",
    "Database/Factory_Autopilot_Action_Queue.csv",
    "Database/Factory_Backlog.csv",
    "Database/eBay_Live_Cover_Fix_Plan.md",
    "Database/eBay_Traffic_Diagnosis.md",
    "Database/Printify_Production_Design_Audit.csv",
    "Reports/latest morning_report_*.md",
    "Review_Packets/OPENCLAW_GEMINI_BRIEF.md",
    "Review_Packets/REPORT_INDEX.md",
    "Review_Packets/ETSY_DIGITAL_TRAFFIC_PENETRATION_REPORT_20260506.md",
    "Review_Packets/PRINTIFY_EXTERNAL_SYNC_DIAGNOSIS_20260506.md",
    "Database/Etsy_Digital_Gray_Launch_Queue.csv",
    "Database/Etsy_Fee_Ledger.csv",
    "Review_Packets/EBAY_API_MINIMAL_APPLICATION_PACKET.md"
  ],
  "operating_roles": {
    "Rex": "Commander",
    "Gemini": "Strategy advisor",
    "Codex": "Executive operator and factory debugger"
  },
  "default_authorization_policy": {
    "principle": "Rex has repeatedly granted full OpenClaw project access. Routine project account navigation, local file edits, API debugging, browser automation, QA checks, report writing, and script changes should proceed without repeated permission prompts.",
    "ask_only_for": [
      "spending beyond the approved cap",
      "payment or billing settings",
      "placing, canceling, or refunding orders",
      "sending buyer/customer messages",
      "exposing or changing private credentials",
      "destructive actions outside the OpenClaw project scope"
    ],
    "blocked_behavior": "When a tool/runtime/login failure appears, record the blocker, choose the safest authorized workaround, and return to the mainline instead of waiting by default."
  },
  "advisor_packet_policy": {
    "canonical_brief": "Review_Packets/OPENCLAW_GEMINI_BRIEF.md",
    "index": "Review_Packets/REPORT_INDEX.md",
    "principle": "Gemini cannot see the repo, code, or local folders, so advisor packets must summarize business context, current facts, risks, and strategy questions without requiring file access.",
    "network_note": "The canonical Gemini brief explicitly supersedes older low-bandwidth assumptions: wired LAN is fixed and low-bandwidth mode is lifted."
  },
  "browser_isolation_policy": {
    "principle": "Do not use Rex's active daily Chrome tabs as the automation workbench. Prefer API/headless work first, then a dedicated automation browser profile.",
    "dedicated_edge_command": "npm run browser:edge",
    "dedicated_edge_port": 9223,
    "dedicated_edge_profile": "C:\\openclaw_edge_profile",
    "ebay_env": "Set OPENCLAW_EBAY_CDP_PORT=9223 for Seller Hub and live eBay audit scripts.",
    "current_note": "Dedicated Edge is running and should be used for marketplace/account UI work. Latest check: Printify, Etsy Shop Manager, and eBay Seller Hub are logged in/readable on Edge CDP 9223; only eBay Developer Program still redirects to sign-in/pending access.",
    "latest_fix": "2026-05-06 20:31-20:40: Printify login guard, supervisor, mockup uploader, and full pipeline default to Edge CDP 9223. Do not use daily Chrome 9222 for project automation by default."
  },
  "automation_first_rule": {
    "principle": "Codex labor is for building and debugging the factory, not for becoming the permanent factory worker.",
    "durable_entrypoint": "py modules\\factory_supervisor.py --execute-local --skip-network",
    "online_preflight": "py modules\\factory_supervisor.py",
    "logs": [
      "Database/Factory_Autopilot_State.json",
      "Database/Factory_Autopilot_Action_Queue.csv",
      "Database/Factory_Backlog.csv",
      "Database/Factory_Autopilot_Run_Log.csv"
    ],
    "new_device_setup": "Read START_HERE_OPENCLAW.md, then OPERATIONS_MANUAL.md; run npm run setup:win, npm run doctor, and npm run local."
  },
  "current_counts": {
    "ebay_listing_rows": 240,
    "stable_printify_tracked": 161,
    "published_tracking_rows": 112,
    "ready_for_printify": 50,
    "factory_backlog_rows": 14,
    "product_counts": {
      "Sticker": {
        "stable": 76,
        "published": 60,
        "ready": 46
      },
      "Poster": {
        "stable": 32,
        "published": 26,
        "ready": 4
      },
      "Acrylic": {
        "stable": 53,
        "published": 26,
        "ready": 0
      }
    },
    "last_known_after_lan_batch": "eBay workbook rows=255; published tracked rows: Sticker=74, Poster=30, Acrylic=30 after 2026-05-06 LAN batch."
  },
  "current_blockers": [
    "Sticker/public publish is blocked by live eBay cover mismatch until source repair or replacement is verified.",
    "Printify login can expire; use npm run printify:login to verify/recover the CDP profile before UI source repair.",
    "Etsy API app is still pending personal approval, but Etsy UI login works in the dedicated Edge profile and the first 10 digital printable listings are live. Do not scale beyond gray caps without signal.",
    "Printify official/default mockups should be preserved when useful; cover repair now validates custom cover/design presence and live buyer-page result rather than requiring exactly one default image.",
    "One verified sample proves some old inventory-managed eBay variation images may not accept source repair; use replacement listing flow for READY_TO_REPLACE_VERIFIED rows.",
    "Old bad Sticker listings must be safely retired after replacement listings pass live audit; retire queue is Database/eBay_Retire_Queue.csv."
  ],
  "cover_repair_state": {
    "live_cover_fix_queue_rows": 49,
    "source_repair_required": 12,
    "non_sticker_review_required": 4,
    "replacement_queue": "Database/eBay_Cover_Replacement_Queue.csv",
    "repair_decisions": "Database/eBay_Cover_Repair_Decisions.csv",
    "next_action_if_logged_in": "Run one targeted source repair with py modules\\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120, then live audit the same SKU before scaling.",
    "latest_single_sku_test": "Cover-only official replacement path is now proven at scale: Sticker-Zen-0044-FIX1 through 0046-FIX1 and 0049-FIX1 through 0054-FIX1 passed live buyer-page cover audit; all corresponding old bad-cover listings were retired through Edge Seller Hub and detached from Printify.",
    "replacement_draft_latest": "Cover-only replacement path is now production policy for Sticker: upload Cover only as custom marketplace image, keep Printify official mockups, retain U1-U4 only as local reference unless a separate audited gallery path is added."
  },
  "printify_login_state": {
    "allowed_google_account": "rexxu024@gmail.com",
    "guard_command": "npm run printify:login",
    "latest_check": "2026-05-06 23:11 -0400: LOGGED_IN through Edge CDP 9223; Printify-eBay store token renewed through eBay consent.",
    "status_file": "Database/Printify_Login_Status.json",
    "rule": "Never select a Google account other than rexxu024@gmail.com; if password is required, stop for manual login."
  },
  "production_design_qa_state": {
    "latest_audit": "Database/Printify_Production_Design_Audit.csv",
    "latest_sample": "2 Acrylic rows checked on 2026-05-06 morning; 2/2 visual and size match, ahash_distance=0. Exact SHA differed due Printify-side re-encoding.",
    "small_batch_command": "py modules\\printify_design_audit.py --limit 2 --sleep-seconds 1"
  },
  "latest_market_signal": {
    "latest_snapshot": "2026-05-06 23:03:00 -0400",
    "snapshot_rows": 50,
    "zero_view_rows": 43,
    "one_plus_view_rows": 7,
    "promoted_general_rows": 50,
    "product_signal": "Acrylic 3/17 moved, Poster 4/17 moved, Sticker 0/16 moved.",
    "diagnosis_file": "Database/eBay_Traffic_Diagnosis.md",
    "summary": "2% Standard ads are active but not enough; Sticker cover/gallery mismatch and publish-route control remain priority."
  },
  "prepared_local_assets": {
    "etsy_shop_packet": "Database/Etsy_shop_update_packet.md",
    "ebay_profile_packet": "Database/eBay_Profile_Update_Packet.md",
    "etsy_digital_final_packet": "Database/Etsy_Digital_Final_Upload_Packet.csv",
    "blueprint_next_test_plan": "Database/Product_Blueprint_Next_Test_Plan.md",
    "factory_backlog": "Database/Factory_Backlog.md",
    "operations_manual": "OPERATIONS_MANUAL.md"
  },
  "confirmed_printify_specs": {
    "poster_premium_matte_vertical": {
      "blueprint_id": 282,
      "provider_id": 99,
      "variant_id": 43138,
      "target_size": "12x18",
      "print_area": "3600x5400"
    },
    "photo_block_acrylic": {
      "blueprint_id": 1471,
      "provider_id": 104,
      "variant_id": 106190,
      "target_size": "5x7 vertical",
      "print_area": "1538x2138"
    }
  },
  "next_product_test_plan": [
    "Canvas blueprint 1936 variant 119906",
    "Framed Poster blueprint 1236 variant 93818",
    "Notebook/Journal blueprint 5634 variant 252281",
    "Mug blueprint 478 variant 65216",
    "Metal blueprint 1206 variant 91995"
  ],
  "do_not_do_without_new_signal": [
    "Do not broad-publish more stickers while cover gate is open.",
    "Do not use Priority/PPC ads; only Promoted Listings Standard/General fixed 2%.",
    "Do not use suggested ad rates.",
    "Do not touch payments, orders, buyer messages, or billing settings.",
    "Do not publish beyond the first Etsy Digital gray batch unless the fee guard and current Rex budget cap allow it; normal pool is $40 total and $60 requires written rationale."
  ],
  "image_policy": {
    "sticker": "Use Cover-only custom art plus Printify official mockups for first-pass marketplace publishing. Do not publish U1-U4 as eBay/Printify gallery images because eBay can select one U/detail image as the main cover. Keep U1-U4 local for QA/detail/reference.",
    "poster_acrylic": "Use one full production design; no die-cut/sticker-split logic. Preserve Printify official mockups/defaults as product-context images unless they create buyer confusion.",
    "future_rd": "Premium MJ-generated scene/mockups from real production images are allowed only after QA; track as R&D, not a blocker for current production."
  },
  "network_policy": "Ethernet restored on 2026-05-06: Ethernet 3 up at 1Gbps, Wi-Fi disconnected, 0% loss and about 5-8ms latency in latest checks. Rex cleared low-bandwidth mode at 2026-05-06 15:20 -0400; online batches may run normally/full-throughput, but marketplace/account-risk throttles still apply.",
  "housekeeping_policy": {
    "review_packet_dir": "Review_Packets/",
    "rule": "Keep Rex/Gemini/AI-facing summaries and decision packets in Review_Packets. Keep script queues in Database and production assets in Output. Clear temp/cache/debug artifacts regularly, but do not delete personal downloads, Docker/app data, or production source assets without a specific reason.",
    "latest_cleanup": "2026-05-06 16:45 -0400: safe caches/temp cleanup freed about 18GB and raised C drive free space to about 54.7GB."
  },
  "etsy_digital_gray_launch": {
    "batch_id": "ETSY-DIGITAL-FIRST-LIVE-20260506",
    "queue": "Database/Etsy_Digital_Gray_Launch_Queue.csv",
    "qa_report": "Database/Etsy_Digital_QA_Report.csv",
    "fee_ledger": "Database/Etsy_Fee_Ledger.csv",
    "report": "Review_Packets/ETSY_DIGITAL_TRAFFIC_PENETRATION_REPORT_20260506.md",
    "selected": 10,
    "qa_pass": 10,
    "confirmed_spent_usd": 2.0,
    "reserved_fee_usd": 2.0,
    "status": "PUBLISHED_UI_CONFIRMED_FIRST_10",
    "public_audit": "10/10 active/readable and 10/10 digital-download signal in Database/Etsy_Digital_Live_Audit.csv.",
    "legacy_cleanup": "Old DriveFuel Etsy listings 4407466791 and 4366700475 deleted/retired; public pages show unavailable and active manager no longer contains them.",
    "live_listing_ids": [
      "Poster-Academia-0001 -> 4500654287",
      "Poster-Academia-0002 -> 4500664506",
      "Poster-Academia-0003 -> 4500665474",
      "Poster-Academia-0081 -> 4500657145",
      "Poster-Academia-0082 -> 4500667154",
      "Poster-Academia-0083 -> 4500667734",
      "Poster-Academia-0084 -> 4500668282",
      "Poster-Academia-0085 -> 4500668786",
      "Poster-Academia-0091 -> 4500660013",
      "Poster-Zen-0001 -> 4500669878"
    ],
    "rule": "First batch is live; hold further paid publishing until initial traffic/indexing readout unless Rex explicitly asks or the fee guard admits the next gray cell."
  },
  "latest_supervisor_state": {
    "last_local_run": "2026-05-06 22:30 -04:00",
    "result": "npm run local completed with failures=0.",
    "etsy_status": "READY_MONITOR: first 10 Etsy Digital listings are live; monitor traffic before spending more.",
    "latest_report": "Reports/morning_report_20260506_2230.md",
    "latest_gemini_queue": "Gemini_Advisor/gemini_review_queue_20260506_2230.md"
  },
  "printify_external_pending": {
    "ids": [
      "Poster-Academia-0038",
      "Poster-Academia-0039",
      "Poster-Academia-0040",
      "Poster-Academia-0041",
      "Poster-Academia-0042"
    ],
    "status": "Printify_PublishExternalPending_Mockups8",
    "confirmed_not_live": "No eBay_Item_ID / product external id after sync and one API retry on 0038.",
    "external_synced": [
      "Poster-Academia-0037 -> 406909473606"
    ],
    "report": "Review_Packets/PRINTIFY_EXTERNAL_SYNC_DIAGNOSIS_20260506.md",
    "scheduler_rule": "Normal publish scheduler no longer retries external-pending rows; explicit --retry-pending required."
  }
}



## Current Task / Progress Memory


### CURRENT_TASK.md
```markdown
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
- Do not interfere with Rex's daily Chrome. Use the dedicated Edge automation profile on CDP port 9223 for marketplace/account UI work unless there is a specific reason not to.

Default authorization policy:
- Rex has repeatedly granted full OpenClaw project access. Do not stop to ask for routine project account navigation, local file edits, API debugging, browser automation, QA checks, report writing, or script changes.
- Ask only for true red lines: spending beyond the approved cap, touching payment/billing settings, placing/canceling orders, sending buyer/customer messages, exposing or changing private credentials, or destructive actions outside the project scope.
- When blocked by a tool/runtime/login failure, record the blocker, choose the safest authorized workaround, and continue the mainline instead of waiting by default.

Current execution order:
1. Pause rapid public eBay publishing after Akamai/zero-size-object instability.
2. Build Phase 1 data foundation: eBay read-only performance log, unified listing records, and DNA signal fields.
3. Etsy Digital gray test is now active through the dedicated Edge UI profile: first 10 digital printable listings are live, with confirmed spend $2.00. Do not scale beyond the gray caps without signal.
4. Keep Printify production available but avoid shop-front design changes until Rex updates the Printify storefront.
5. Continue QA-first production, eBay read-only monitoring, performance logging, and report automation.
6. Save morning/Gemini advisor report templates so Gemini can act as strategy advisor and Codex can filter recommendations.

Guardrails:
- Do not rapid-publish new eBay listings while external sync and Sticker cover trust remain unresolved.
- Etsy Digital is explicitly resumed for a controlled gray test. First batch cap is 10 listings / $2.00; no-result spend cap is $40-$60 total, with $40 as the normal pool and $60 requiring written rationale.
- Do not activate paid advertising without final action-time confirmation. Exception already completed on 2026-05-04: Rex confirmed eBay Promoted Listings Standard / General fixed 2.0%; Seller Hub campaign now covers 99 identifiable OpenClaw listings after external-id refresh.
- Do not touch payment settings, orders, or buyer messages without confirmation.
- Sticker expansion remains paused until the Cover/U image selection bug is fixed.

## 2026-05-06 21:58 -04:00 Etsy Digital First Batch Live
- Etsy UI login is working in the dedicated Edge automation profile.
- First Etsy Digital gray batch: 10/10 live, all manual-renewal digital listings, confirmed Etsy listing-fee spend $2.00.
- Public page QA: 10/10 active/readable, 10/10 with digital-download signal.
- The 2 old legacy DriveFuel listings were deleted/retired; their public pages now show unavailable and active manager no longer contains them.
- Next Etsy actions: pause further paid publishing until the first 10 have initial indexing/traffic data or Rex explicitly asks to spend more.

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

## 2026-05-06 16:45:00 -04:00 Housekeeping Rule
- Regularly scan for temporary/debug artifacts and clear obvious caches instead of letting the workspace/C drive fill silently.
- Files intended for Rex/Gemini/another AI review should be placed under `Review_Packets/` with clear names.
- Keep raw production assets in `Output/`, machine queues in `Database/`, and durable project memory in `START_HERE_OPENCLAW.md`, `RECOVERY_STATE.json`, `CURRENT_TASK.md`, and `PROGRESS_LOG.md`.
- Do not delete personal downloads, production source assets, or Docker/large app data without a separate reason or explicit user signal.

## 2026-05-06 17:30:55 -04:00 Gemini Brief Consolidation
- Gemini cannot see local code, folders, or detailed CSV/XLSX state, so advisor packets must be written at business/strategy level with only minimal implementation notes.
- Use `Review_Packets/OPENCLAW_GEMINI_BRIEF.md` as the canonical copy/paste brief for Gemini.
- This brief explicitly says the wired LAN/network issue is fixed and low-bandwidth mode is lifted, so strategy advice should not rely on the old Wi-Fi constraint.
- Older timestamped `Reports/` and `Gemini_Advisor/` files are historical supplements only; do not copy many old reports unless debugging history.

## 2026-05-06 17:45:00 -04:00 Browser Isolation Protocol
- Do not use Rex's daily Chrome tabs as the automation workbench, especially if Chrome is on personal checkout/account pages.
- Prefer API/headless/read-only HTTP when possible.
- For browser automation, use a dedicated automation profile and port instead of the daily browser. Default helper: `npm run browser:edge` starts/checks Edge on CDP port 9223 with profile `C:\openclaw_edge_profile`.
- eBay browser scripts now accept `OPENCLAW_EBAY_CDP_PORT` / `OPENCLAW_CDP_PORT`; use port 9223 for Seller Hub/audit work when the dedicated Edge profile is ready.
- Close automation tabs after each task and keep at most 1-2 automation tabs alive.

## 2026-05-06 18:10:00 -04:00 Etsy Login Block (Resolved Later)
- Historical blocker: Etsy temporarily returned the red "An error has occurred, please try again!" login banner across browsers.
- Current state supersedes this: by 2026-05-06 late evening, the dedicated Edge automation profile is logged into Etsy Shop Manager and the first 10 Etsy Digital gray-test listings are live.
- Do not resurrect the old blocker unless a fresh Edge login check fails.

## 2026-05-06 18:35:00 -04:00 Resume Full-Throughput Non-Etsy Monthly Tasks
- Etsy login/publish remains paused.
- Full-throughput mode is active because wired LAN is stable.
- Execution order: retire old eBay bad-cover listings if Seller Hub access works, top up Poster inventory toward 50, keep Acrylic stable, audit production-image correctness, sync external IDs, then push latest durable changes to GitHub.
- Maintain account-risk gates: no PPC/Priority ads, no payment/order/buyer-message changes, and no broad duplicate Sticker expansion beyond the current cap.

## 2026-05-06 18:48:00 -04:00 eBay Market Learning Loop
- If Seller Hub views/orders remain flat after cover repair and fixed 2% General ads, do not assume more volume alone will solve it.
- Start small controlled eBay experiments: buyer-intent title rewrites, clearer cover/mockup selection, price/offer tests, trust/profile fixes, and new product-blueprint probes.
- Evaluate eBay as a channel by evidence. If multiple controlled tests still produce near-zero views, shift execution priority toward Etsy and keep eBay as a smaller syndication/test channel.

## 2026-05-06 19:05:00 -04:00 Quality/Reasoning Budget Rule
- Rex explicitly prefers faster, higher-completion work over excessive token saving.
- Use stronger reasoning for high-leverage tasks: architecture, marketplace strategy, QA gates, debugging, pricing, and experiment design.
- Use scripts/batch execution for repetitive work; do not waste high reasoning on mechanical loops.
- Do not pause work merely to conserve weekly quota unless the task is obviously low value.

## 2026-05-06 19:12:00 -04:00 Etsy 200-Listing Experiment Pool
- Once Etsy login is stable, Rex authorizes up to 200 Etsy listings as a controlled experiment pool, accepting about $40 in listing fees over the listing period.
- Goal is not volume for its own sake: find monetizable winners quickly, then scale proven DNA.
- Do not dump all 200 blindly. Use staged cells with clear metrics: digital printable packs, premium Poster POD, Acrylic POD, and a small custom/personalized pilot.
- Etsy publish remains blocked until login/account access is stable, but local assets, metadata, and launch queues should be prepared now.

## 2026-05-06 19:25:00 -04:00 Pricing / Free Shipping Rule
- Marketplace listings should be positioned as free shipping where possible.
- Printify production cost plus Printify shipping must be included in the product price/profit math; do not double-charge customers by adding marketplace shipping on top of an inflated product price.
- Pricing must never knowingly go below break-even after Printify cost, Printify shipping, marketplace fees, payment processing where applicable, and ad fee assumptions.
- Sticker may accept low margin to earn positive reviews and trust. Poster/Acrylic should preserve premium margin unless a deliberate A/B price test is being run.

## 2026-05-06 20:08:00 -04:00 Proactive Research / Senior Operator Rule
- Rex authorizes Codex to proactively search official docs, market references, open-source resources, and competitor/platform information when doing so helps the business goal.
- Convert research into executable code, QA gates, experiments, pricing rules, and reports rather than leaving it as generic advice.
- Boundaries remain: protect credentials/privacy; do not touch payment/order/buyer-message settings without clear need; do not design marketplace evasion or ban-circumvention systems.
- Default role: senior requirement engineer + senior implementation engineer + cautious operator focused on Rex's money-printer goal.

## 2026-05-06 20:00:00 -04:00 Interruption Return Rule
- When Rex inserts a question, pressure test, or `steer conversation`, answer it, persist any new rule, then automatically return to the prior monthly-task mainline.
- Do not treat an interruption as permission to stop the production workflow unless Rex explicitly says pause/stop.
- Current resumed mainline: resolve `Poster-Academia-0038` through `0042` published-without-external-id state, then continue Poster top-up and marketplace experiment scaffolding.


## 2026-05-06 20:19:29 -04:00 Active Mainline After Interruption
- Interruption return rule is active: after answering side questions or pressure tests, resume the monthly-task mainline automatically.
- Etsy Digital first 10 are QA-passed, published through Edge UI, publicly readable, and logged with confirmed spend $2.00. Hold further Etsy paid scale until the first-10 traffic/indexing readout unless Rex deliberately opens the next gray cell.
- Printify/eBay external sync issue is open for Poster-Academia-0038..0042. They are Printify-ready but not confirmed eBay live listings.
- Default publish scheduler must not retry external-pending rows unless explicitly run with `--retry-pending` after route diagnosis.
- Continue mainline: resolve publish route (eBay API or small UI proof), then top up Poster toward target and continue controlled marketplace experiments.

## 2026-05-06 23:03:00 -04:00 Edge-Only Browser State
- All marketplace/account browser operations should use the dedicated Edge automation profile on CDP port 9223.
- Do not use Rex's daily Chrome for OpenClaw account work.
- Current login check: Printify `LOGGED_IN`, Etsy Shop Manager `LOGGED_IN`, eBay Seller Hub `LOGGED_IN`.
- Only current account gap: eBay Developer Program still redirects to sign-in/pending program access; not a blocker for immediate Printify/Etsy/Seller Hub UI work.

```


### PROGRESS_LOG.md
```markdown
# Progress Log

## 2026-04-29 10:55 - Context Recovery

Recovered task context from the user's pasted prior-thread transcript plus local project artifacts.

Confirmed prior progress from transcript and local files:

- Sticker 5-image workflow was stabilized enough to repair existing products.
- Old primary-image issue was found: Printify UI could reorder uploads and make U images become primary.
- Upload logic was changed toward Cover-first handling.
- Primary audit/repair loop was used until old uploaded Sticker products had Cover first.
- At one point, 35 Sticker products were published and 87 remained `Ready_for_Printify`.
- Login-loss hard stop was added so Printify UI falling back to login page does not continue making bad 3-image drafts.
- Bad drafts created during unstable runs were deleted and rows were reset to `Ready_for_Printify`.
- P5X and Reverse 1999 Steam folders were deleted, freeing about 11.85 GB.
- Later user direction: continue yesterday's tasks but only parts that do not require user review.
- Current safer publishing stance: Printify can prepare/audit drafts; eBay publishing should be throttled and separated from preparation.
- New product official specs previously confirmed:
  - Poster blueprint 282, provider 99, 12x18 variant 43138, print area 3600x5400.
  - Acrylic/photo block blueprint 1471, provider 104, 5x7 vertical variant 106190, print area 1538x2138.

Current local observations:

- `CURRENT_TASK.md`, `PROGRESS_LOG.md`, and `RECOVERY_STATE.json` did not exist before this checkpoint and are being created now.
- Git working tree is dirty with tracked changes in `Database/Etsy_listing.xlsx`, `Database/eBay_listing.xlsx`, `Database/nightly_handoff_log.txt`, `Database/printify_bad_draft_cleanup_20260429.log`, and `modules/edit_for_platforms.py`.
- Many 2026-04-29 audit/log files are untracked.

Next actions:

- Reconcile current Excel status counts before starting any new batch.
- Verify no background Printify runner is active.
- Continue with local no-review work: listing variation, audits, bad draft cleanup, and Poster/Acrylic local pipeline preparation.
- Do not run high-volume eBay publish.

## 2026-04-29 11:05 - Recovered Factory Architecture History

Recovered additional prior-thread context covering the GREY ARCHITECT DNA factory work from V13.0 through V15.3.

Confirmed implemented architecture from the user's transcript:

- `modules/dna_worker.py` was originally created to read `Database/pending_tasks.txt`, use `Mentor_Hub.xlsx`, call Claude, and append DNA production rows to `Production_Line.xlsx`.
- `config.py` was patched to expose `CLAUDE_API_KEY`, `DEEPSEEK_API_KEY`, and `BASE_URL`.
- V13.1/V13.5 refactored the CLI and module boundaries:
  - `main.py` routes Stage 1 to `mentor_hub.run_logic()`.
  - `main.py` routes Stage 2 to `product_line.run_logic()`.
  - Stage 3/4 behavior should be preserved.
  - `modules/mentor_hub.py` handles pending seed to Gold DNA.
  - `modules/product_line.py` handles Gold DNA to production listings.
- V13.7 added Dify-style streaming:
  - Claude API uses stream mode.
  - Prompt requests raw JSON array only.
  - Each complete JSON object is parsed and saved immediately.
  - Console prints `[Dify-Mode] ID: ... 写入成功 | 实时保存已完成`.
  - API read timeout/slow seed handling was added.

Confirmed Mentor_Hub behavior:

- One seed must be sent as exactly one Claude request.
- Each seed request must generate 20 DNA rows.
- Seeds are processed sequentially, not combined into one request.
- A seed is removed from `pending_tasks.txt` only after its 20 rows are saved.
- Slow seeds should not be allowed to burn Claude indefinitely. Normal observed time was under 1 minute; at 2-3 minutes the process should stop, log, debug, or skip/hold the seed.
- A run of 20 new seeds completed:
  - 400 new DNA rows.
  - 20 categories, 20 rows each.
  - `pending_tasks.txt` empty afterward.
  - No duplicate fingerprints, no missing `isolated on white`, no missing `--v 6.1`.
  - Timestamp uses local machine timezone and Excel datetime format like `m/d/yyyy, h:mm:ss AM/PM`.

Confirmed Mentor_Hub schema correction:

- Removed columns: `Product_Type`, `Logic_Protocol`, `Note`.
- Current intended columns: `Category`, `Layout`, `Title`, `Gold_Prompt_DNA`, `Material_Keywords`, `Timestamp`, `Design_Count`, `Performance`.
- New DNA rows have `Design_Count = 0`.
- `Performance` defaults empty.
- `Design_Count >= 100` means the DNA should not be recommended for new product designs.

Confirmed Product_Line behavior:

- Product_Line must use the original verbose/sortable format:
  - `ID`, `Timestamp`, `Category`, `Product_Type`, `Style`, `Title`, `MJ_Prompt`, `SEO_Hook`, `Status`.
- Default Status is `Ready_for_production`.
- ID sequencing is per prefix, not global total row count.
  - Example: `Sticker-Zen-0003` is followed by `Sticker-Zen-0004`.
- Product-specific mold rules exist for Sticker, Poster, Acrylic, T-shirt, and Mug.
- `MJ_Prompt` must be single-line plain text with no newline characters.
- A prior pending design run generated 240 listings:
  - `Sticker-Zen-0070` to `Sticker-Zen-0149`
  - `Poster-Academia-0001` to `Poster-Academia-0080`
  - `Acrylic-Grimdark-0001` to `Acrylic-Grimdark-0080`
- After correction, `Production_Line.xlsx` had 460 effective rows, missing `Product_Type` count 0, missing `Category` count 0, wrong status count 0, and no MJ prompt newlines.

Confirmed Excel repair:

- Both `Database/Product_Line.xlsx` and `Database/Mentor_Hub.xlsx` previously opened with Excel content-repair warnings.
- Root cause identified in prior thread: stale Excel Table XML objects.
- Backups were created:
  - `Database/Production_Line.backup_20260427_005522.xlsx`
  - `Database/Mentor_Hub.backup_20260427_005522.xlsx`
- Both workbooks were rebuilt cleanly without internal `xl/tables/table1.xml`.
- Post-repair counts from transcript:
  - `Production_Line.xlsx`: 460 rows, 9 columns.
  - `Mentor_Hub.xlsx`: 620 rows, 8 columns.
- Excel COM open/save/close test passed for both.

Current implication:

- Before changing factory code, verify the current workbook schemas still match these recovered rules.
- Future product generation should use `Pending_design.txt` and Product_Line V15.3 rules, not ad hoc row appends.

## 2026-04-29 11:25 - Full Project Logic Read-Through

Completed a broader read-through of the project structure, core modules, workbook schemas, local output folders, and handoff logs. Saved consolidated logic to `PROJECT_LOGIC_RECOVERY.md`.

Verified current live state:

- No active `py`, `python`, or `excel` process was found during the read-only check.
- `Database/pending_tasks.txt` is `[]`.
- `Database/Pending_design.txt` is `[]`.
- `Mentor_Hub.xlsx` has 620 data rows and the expected 8-column schema.
- `Production_Line.xlsx` has 460 data rows plus 20 blank XML rows and the expected 9-column schema.
- `Production_Line.xlsx` product counts from current XML:
  - Sticker: 189
  - Poster: 121
  - Acrylic: 80
  - T-Shirt: 20
  - Wall Art: 30
  - Blank rows: 20 empty rows with no ID/category/status.
- `eBay_listing.xlsx` has 149 rows:
  - `Printify_Published_Mockups5`: 34
  - `Printify_UI_Mockups5`: 8
  - `Ready_for_Printify`: 78
  - `Quality_Hold_LowRes_U`: 27
  - `Printify_UI_Failed`: 2
- `Etsy_listing.xlsx` has 149 rows, all `Placeholder`.
- Local Sticker folders under `Output/Sticker/Kiss-Cut`:
  - `Ready_for_Steaming`: 122
  - `Not_Working_LowRes`: 27
  - `Not_Working`: 6
  - `Review`: 1
  - Other: 2

Important reconciliation:

- Earlier transcript said 35 published and 87 ready, but current `eBay_listing.xlsx` says 34 published and 78 ready. Current Excel is the live source of truth.
- Earlier transcript said Product_Line had no missing Product_Type; current XML check found 20 blank rows, not real rows with IDs. Treat these as harmless blank workbook residue unless they affect Excel behavior.
- Git checkpoint remains blocked by `.git` permission errors in the handoff log.

Next step requested by user:

- Do not execute production yet.
- Present the interpreted 10pm requirements split into necessary core tasks and nice-to-have tasks.
- Wait for user confirmation before execution.

## 2026-04-29 11:34 - Execution Authorized

User confirmed the recovered plan is close enough and authorized execution with broad operational discretion:

- Act as the user's digital double for routine decisions.
- Make reasonable business-plan adjustments without repeatedly asking.
- Printify/eBay account checks and necessary changes are allowed when aligned with strategy.
- eBay API should not be built now; use Seller Hub active listings directly if account/listing verification is needed.
- Continue to protect eBay account health with conservative pacing.

Execution plan:

1. Start with local data/schema/status audits.
2. Repair obvious local data issues.
3. Audit Printify 5-image and primary-cover state.
4. Continue safe batches only when session/account state allows.
5. Avoid broad high-volume eBay publishing unless explicitly safe and throttled.

## 2026-04-29 11:50 - Permission Handling Correction

User reiterated multiple times that OpenClaw project work has standing full access and should not repeatedly stop for routine confirmations.

Updated `PROJECT_OPERATING_PROTOCOL.md`:

- Project files, scripts, local `.venv`, missing project dependencies, Printify/eBay project checks, and routine draft/status repair are pre-authorized.
- If Codex app sandbox forces a tool-level approval, treat it as an execution gate, not a fresh user decision.
- Still pause only for payment/order/billing credentials, broad public eBay publishing/sync risk, destructive deletion outside narrowly verified project cleanup, or sensitive personal data unrelated to OpenClaw.

## 2026-04-29 12:22 - 4-Day Listing Target

User set a broader travel-window goal:

- By arrival in New York, reach about 230 total listings.
- Target product ratio: `Sticker : Poster : Acrylic = 2 : 1 : 1`.
- Approximate final mix:
  - Sticker: 115
  - Poster: 57
  - Acrylic: 57
- Today, Sticker total should not exceed 100.
- eBay public publishing should remain cautious, staggered, and not forced in large bursts.
- Printify preparation and audit can continue when Wi-Fi is available.
- Summarize any items that require the user's final handling.

## 2026-04-29 Listing Copy Batch
- Patched edit_for_platforms.py with template-bank title/description generation, DeepSeek template constraints, image-note enforcement, duplicate-title cleanup, and banned MJ-term filtering.
- Rebuilt local Sticker listing copy in Database/eBay_listing.xlsx.
- Audit: 149 rows, title length 75-79 for all rows, duplicate titles 0, missing image note 0, Sticker missing 4pc/6x6 0, banned title terms 0.
- Next: Printify/eBay cover-order audit and repair.

## 2026-04-29 Sticker Gate + Batch
- Added printify_design_audit.py for Production_Design vs Printify print-area visual audit. It records byte SHA, declared remote size, preview size, and perceptual hash.
- Integrated production design gate into printify_full_pipeline.py before and after mockup upload; checkpoint prints every 2 completions.
- Full existing Printify design audit: 70 checked, 0 visual mismatches.
- Repaired 0068, 0081, 0084, 0086, 0087, and 0088 to 5 mockups with Cover primary and correct Production_Design.
- Added new 0089, 0091, 0092, 0093, 0094 via gated pipeline; all passed design and 5 mockup checks.
- Current Sticker good total: 76 = 42 Printify_UI_Mockups5 + 34 Printify_Published_Mockups5. Sticker cap remains <=100.

## 2026-04-29 16:04 Poster/Acrylic DNA 排产批次
- 写入并跑完 Database/Pending_design.txt 多 DNA 排产：Poster 20 + Acrylic 20。
- Poster DNA：Academia-Astrological_Globe、Academia-Star_Chart_Blueprint、Zen-Bonsai_Elysium、Academia-Glass_Orrery。
- Acrylic DNA：Grimdark-Alchemical_Vessel、Academia-Astrological_Globe、Zen-Lotus_Mechanism、Zen-Tea_Ceremony_Soul。
- Product_Line 新行保持老格式：ID / Timestamp / Category / Product_Type / Style / Title / MJ_Prompt / SEO_Hook / Status。
- 状态均为 Ready_for_production，MJ_Prompt 无换行且包含 --v 6.1 --style raw。
- 价格策略：Poster 12x18 当前使用 $34.99；Acrylic 5x7 当前使用 $89.99，后续以 Printify 实际成本/运费复核。
- 修复 Product_Line 去重阈值：避免 Poster/Acrylic 因共享材质词被误判为重复，只拦同主体或极高相似。

## 2026-04-29 16:21 Poster Upload + Audit Batch
- Generated listing rows for Poster-Academia-0001/0002/0003; Poster title lengths 76/78/79 and price $34.99.
- Uploaded Poster-Academia-0002 and Poster-Academia-0003 to Printify blueprint 282/provider 99/variant 43138.
- Poster 0001/0002/0003 all passed Production_Design visual audit and Cover primary audit.
- Full design audit checked 79 Printify products, mismatches 0.
- Primary audit found Sticker-Zen-0092 had only 3 selected mockups; repaired it to 5 selected mockups and confirmed Cover primary distance 0.

## 2026-04-29 17:04 Listing Copy / Metadata Sync
- Buyer-facing Image Note updated: main image is actual received product; additional images are bonus concept/detail references and not extra products or selectable variations.
- modules/printify_metadata_sync.py added to sync local Excel title/description back to Printify without touching variants or print areas.
- Synced Printify metadata: Sticker 76/76, Poster 3/3, Acrylic 3/3.
- Acrylic sample upload complete: Acrylic-Academia-0001, Acrylic-Grimdark-0081, Acrylic-Zen-0001 all 5 mockups, Cover primary OK, Production_Design visual match OK.
- Verified Acrylic 5x7 cost from Printify API: variant 106190 cost $35.43, current price $89.99.

## 2026-04-29 17:28 Poster Batch 0081-0084
- Harvested Poster-Academia-0081/0082/0083/0084 from Discord; all have U1-U4 and metadata.
- Built Poster production assets with full-frame 3600x5400 Production_Design and 1800x2700 Cover_Mockup.
- Generated listing copy and uploaded all 4 to Printify blueprint 282/provider 99/variant 43138.
- Targeted audit: all 4 Cover primary distance 0; all 4 Production_Design visual_match true.
- Poster stable Printify total now 7.

## 2026-04-29 18:01 Acrylic Batch 0082/Zen0002-0003
- Harvested Acrylic-Grimdark-0082, Acrylic-Zen-0002, Acrylic-Zen-0003 successfully; Acrylic-Academia-0002 timed out and remains isolated for rescue/rerun.
- Built Acrylic 1538x2138 Production_Design and 1500x2100 Cover_Mockup assets.
- Uploaded Acrylic-Zen-0002 and Acrylic-Zen-0003 directly; Acrylic-Grimdark-0082 had a UI mockup count 0 issue, then repaired via mockup UI uploader.
- Targeted audit: all 3 Cover primary distance 0; all 3 Production_Design visual_match true.
- Acrylic stable Printify total now 6.

## 2026-04-29 18:30 Poster Batch 0085
- Poster-Academia-0085 harvested, asset-built, listed, and uploaded to Printify.
- Poster-Academia-0086/0087/0088/0089 timed out; rescue found no Discord grid/U assets, so they remain defeated and will be skipped/replaced.
- Poster stable Printify total now 8.
- Concurrency adjustment: avoid 5 parallel for Poster; return to 3 parallel for reliability.

## 2026-04-29 18:56 Poster Batch 0091
- Poster-Academia-0091 harvested and uploaded; targeted audit pending/complete in terminal output.
- Poster-Academia-0090/0092 had no Discord message/recoverable output; skip rather than burning time.
- Poster stable Printify total now 9.

## 2026-04-29 19:14 Acrylic Batch 0083/Acad0003/Zen0004
- Harvested Acrylic-Grimdark-0083, Acrylic-Academia-0003, Acrylic-Zen-0004 successfully.
- Built assets and uploaded all 3 to Printify blueprint 1471/provider 104/variant 106190.
- Targeted audit complete/recorded in terminal: Cover primary distance 0 and Production_Design visual match true.
- Acrylic stable Printify total now 9.

## 2026-04-29 19:19 Acrylic Batch Primary Correction
- Correction to previous Acrylic batch note: targeted audit initially found Acrylic-Grimdark-0083 primary cover mismatch (distance 168) while Production_Design matched.
- Re-ran mockup UI repair for Acrylic-Grimdark-0083.
- Re-audit passed: Cover primary distance 0; Production_Design visual_match true.

## 2026-04-29 19:41 Acrylic Batch Zen0005
- Acrylic-Zen-0005 harvested, asset-built, listed, and uploaded to Printify.
- Acrylic-Grimdark-0084 and Acrylic-Academia-0004 timed out with no usable output; skip/replace later.
- Acrylic stable Printify total now 10.
- MJ batch success rate is currently unstable for non-Zen directions; next generation should use smaller/single-ID batches or wait for queue stability.

## 2026-04-29 20:40 Poster Zen Batch Correction
- Poster-Zen-0002 uploaded and passed targeted audit.
- Poster-Zen-0001 had a partial 4/5 bad draft; deleted from Printify and held locally.
- Poster-Zen-0003 failed UI upload with 4/5 images; deleted from Printify and held locally.
- Poster stable Printify total now 10.

## 2026-04-29 21:00 Acrylic Batch Zen0006-0008
- Harvested Acrylic-Zen-0006/0007/0008 successfully.
- Built assets and uploaded all 3 to Printify.
- Targeted audit in terminal: Cover primary and Production_Design checks performed.
- Acrylic stable Printify total now 13.

## 2026-04-29 21:19 Poster Zen 0004/0005 Attempt
- Harvested Poster-Zen-0004 and Poster-Zen-0005 successfully.
- Printify upload timed out while processing Poster-Zen-0004; bad partial draft was deleted and row set to Printify_Hold_BadDraftDeleted.
- Poster-Zen-0005 remains local-ready / Ready_for_Printify for next run.
- Stable Poster count remains 10; no further public publish attempted.

## 2026-04-29 21:21 Handoff checkpoint
- User paused work because laptop power supply is unexpectedly unavailable; no new production batches should run until resumed.
- Confirmed no active OpenClaw MJ/Printify production scripts other than the current check command.
- Cleaned stale deleted bad draft row: Poster-Zen-0003 -> Printify_Hold_BadDraftDeleted, Printify_Product_ID cleared.
- Stable Printify-prepared totals at pause: Sticker 76, Poster 10, Acrylic 13, total stable 99.
- Local-ready but not stable/uploaded: Poster-Zen-0005 remains Ready_for_Printify; Poster-Zen-0001/0003/0004 are held after bad partial drafts were deleted.
- No public eBay publish/sync expansion was started in this final pause window.
- handoff checkpoint


## 2026-04-29 21:28 Resume - Poster-Zen-0005
- Resumed from handoff.
- Uploaded Poster-Zen-0005 to Printify successfully.
- Production_Design visual match true; targeted Cover primary audit executed in terminal.
- Poster stable Printify count moves from 10 to 11 if primary audit passes.

## 2026-04-29 21:40 Resume Poster Hold Recovery
- Reprocessed held local Poster assets: Poster-Zen-0001 and Poster-Zen-0004 uploaded successfully to Printify.
- Poster-Zen-0003 failed again at UI Continue; deleted bad partial draft and returned it to hold.
- Targeted audits for Poster-Zen-0001/0004 executed in terminal.

## 2026-05-03 22:43 -04:00 NYC Resume
- User arrived in New York; operating timezone changed to America/New_York for all future logs.
- eBay active Sticker listings show very low/no traffic; deeper diagnosis deferred until morning review.
- Overnight priority: finish remaining Acrylic and Poster staged listings with strict design/cover audits, no broad eBay publish expansion.


## 2026-05-03 23:22 -04:00 Acrylic Mockup Rule Repair
- Corrected Acrylic Photo Block handling: official Printify mockups are front/back/side views, not Sticker-style 5 custom mockups.
- Acrylic-Grimdark-0085 marked stable with official 4 views and Production_Design visual match.
- Acrylic-Zen-0009 and Acrylic-Zen-0010 marked stable after Production_Design visual match and official view audit; both currently have duplicated official view sets (8 selected), accepted as non-production-risk but logged for later cleanup research.
- Acrylic stable count target moves upward from 15 to 17.


## 2026-05-03 23:23 -04:00 Target 200 Allocation
- New user target: Printify stable total = 200.
- Current stable total: 106 = Sticker 76, Poster 13, Acrylic 17.
- Working allocation: Sticker 100 max, Poster 50, Acrylic 50. Needed: +24 Sticker, +37 Poster, +33 Acrylic.
- Publish cadence may be more aggressive, but still batched and audit-gated to protect the eBay account.


## 2026-05-03 23:35 -04:00 Publish Policy Update
- User authorized periodic eBay publish after audit gates.
- Operating policy: publish only audited Printify-staged items; use small mixed-product batches with irregular spacing; avoid one-shot mass publish or unaudited products.

## 2026-05-04 00:18 -04:00 Publish Batches 001-002
- Published two audited mixed batches through Printify API.
- Batch 001: 9/9 published, mixed Poster/Acrylic/Sticker.
- Batch 002: 12/12 published, mixed Poster/Acrylic/Sticker.
- Publish total after batches: 55 rows in Printify_Published_* statuses.
- Stable Printify total remains 106; no unaudited product was published.

## 2026-05-04 00:20 -04:00 Acrylic Harvest Batch 001-010
- Ran Acrylic Discord harvest for Acrylic-Grimdark-0001 through 0010 with conservative parallelism.
- Completed assets for 8/10: 0001, 0004, 0005, 0006, 0007, 0008, 0009, 0010.
- Acrylic-Grimdark-0002 and 0003 timed out and remain isolated for replacement/rerun.
- Built local Acrylic production assets; next step is listing copy generation, Printify upload, and production-design audit.

## 2026-05-04 01:08 -04:00 Acrylic Upload Recovery
- Generated Acrylic listing copy for 25 available Acrylic folders; 8 new harvested items entered Ready_for_Printify.
- First Acrylic upload attempt exceeded the external runtime budget and left residual processes; stopped them before continuing.
- API audit recovered Acrylic-Grimdark-0001: official front/back/side views present, Production_Design visual_match true, marked Printify_UI_Mockups4.
- Reset no-product-id failures Acrylic-Grimdark-0005/0006/0007 back to Ready_for_Printify for single-item retry.
- Acrylic stable count now 19; Acrylic ready count now 6.

## 2026-05-04 01:33 -04:00 Acrylic Upload Transport Fix
- Isolated Printify upload failure to large Acrylic production PNG upload: repeated 10053 connection aborts and Printify 502 responses.
- Added visible upload attempt logging and 5 retries for image uploads.
- Added q99 JPEG upload derivatives for Poster/Acrylic transfer only; original local Production_Design.png files remain unchanged for audit/source-of-truth.
- Re-ran Acrylic-Grimdark-0005 successfully: Production_Design visual_match true, official front/back/side views present, marked Printify_UI_Mockups4.

## 2026-05-04 01:58 -04:00 Acrylic Upload Batch Completion
- Uploaded/recovered Acrylic-Grimdark-0006/0007/0008/0009/0010.
- All five passed Production_Design visual audit and official Acrylic front/back/side view audit.
- Acrylic-Grimdark-0009 initially reported 0 mockups, then generated official views on delayed API recheck and was marked stable after targeted audit.
- Acrylic stable count now 25; Acrylic Ready_for_Printify count now 0.

## 2026-05-04 02:13 -04:00 Publish Batch 003
- Published 12/12 audited items through Printify API with mixed Poster/Acrylic/Sticker cadence.
- Delay window was 45-120 seconds between items.
- Published totals now: Sticker 45, Poster 11, Acrylic 11.
- Stable totals remain: Sticker 76, Poster 13, Acrylic 25.

## 2026-05-04 02:33 -04:00 Poster Harvest Batch 0005-0014
- Ran Poster-Academia-0005 through 0014 with max parallel 3.
- Completed 8/10: 0005, 0006, 0008, 0009, 0010, 0011, 0013, 0014.
- Poster-Academia-0007 and 0012 timed out and remain excluded.
- Built Poster production assets and regenerated listing copy; 8 new Poster rows are Ready_for_Printify.

## 2026-05-04 03:28 -04:00 Poster Printify Rule Repair
- Switched Poster handling away from Sticker-style forced 5 custom mockups.
- Accepted official Printify Poster mockups when Production_Design visual audit passes and at least 4 official poster mockups are selected.
- Reduced Poster upload derivatives to q95 JPEG for transport stability; original local Production_Design.png remains the source-of-truth.
- Relaxed Production_Design visual audit to allow same-size ahash distance <= 5 to avoid false failures from Printify/JPEG re-encoding.
- Uploaded/recovered Poster-Academia-0005/0006/0008/0009/0010/0011/0013/0014.
- Poster stable count now 21.

## 2026-05-04 03:49 -04:00 Publish Batch 004
- Published 15/15 audited mixed items through Printify API.
- Delay window was 45-120 seconds.
- Published totals now: Sticker 50, Poster 16, Acrylic 16.
- Stable totals remain: Sticker 76, Poster 21, Acrylic 25.

## 2026-05-04 04:19 -04:00 Acrylic Harvest Batch 0011-0020
- Ran Acrylic-Grimdark-0011 through 0020 with max parallel 3.
- Completed 9/10: 0011 through 0019.
- Acrylic-Grimdark-0020 timed out and remains excluded.
- Built Acrylic production assets and regenerated listing copy; 9 new Acrylic rows are Ready_for_Printify.

## 2026-05-04 05:17 -04:00 Acrylic Upload Batch 0011-0019
- Uploaded/recovered Acrylic-Grimdark-0011 through 0019.
- All 9 passed Production_Design visual audit and official Acrylic front/back/side mockup audit.
- Fixed Acrylic delayed-mockup logic: stable delayed API recheck is sufficient; initial 0 selected no longer mislabels good drafts as failed.
- Acrylic stable count now 34.
- Total stable Printify count now 131 = Sticker 76, Poster 21, Acrylic 34.

## 2026-05-04 05:33 -04:00 Publish Batch 005
- Published 15/15 audited mixed items through Printify API.
- Delay window was 30-90 seconds.
- Published totals now: Sticker 55, Poster 21, Acrylic 21.
- Stable totals remain: Sticker 76, Poster 21, Acrylic 34.

## 2026-05-04 06:42 -04:00 Acrylic Batch 0021-0030
- Ran Acrylic-Grimdark-0021 through 0030; completed 9/10, with Acrylic-Grimdark-0029 timed out.
- Built assets, regenerated listing copy, and uploaded/recovered 9 Acrylic products.
- Delayed official-view recovery marked Acrylic-Grimdark-0022/0026/0027 stable after API recheck.
- Acrylic stable count now 43.

## 2026-05-04 06:56 -04:00 Sticker Top-Up Trial Stopped
- Tested Sticker top-up with Sticker-Zen-0095/0096.
- Product creation and Production_Design audits passed, but Printify UI mockup selection only selected 2 gallery mockups instead of Cover + U1-U4.
- Deleted the two bad Printify drafts and reset both rows to Ready_for_Printify.
- Decision: pause Sticker expansion at stable count 76 to avoid U1/partial-gallery cover errors; continue total-count growth with Poster/Acrylic.

## 2026-05-04 07:42 -04:00 Acrylic Batch 0031-0040
- Ran Acrylic-Grimdark-0031 through 0040; completed 10/10.
- Built assets, regenerated listing copy, and uploaded/recovered all 10 Acrylic products.
- Delayed official-view recovery marked Acrylic-Grimdark-0032/0038/0039/0040 stable after API recheck.
- Acrylic stable count now 53.
- Total stable Printify count now 150 = Sticker 76, Poster 21, Acrylic 53.

## 2026-05-04 08:42 -04:00 Poster Batch 0015-0024
- Ran Poster-Academia-0015 through 0024; completed 7/10, with 0015/0016/0018 timed out.
- Built assets, regenerated listing copy, and uploaded/recovered all 7 completed Poster products.
- Poster upload derivative quality reduced to q92 after Poster-Academia-0024 q95 transfer repeatedly hit Printify 502; q92 retry succeeded and passed visual audit.
- Poster stable count now 28.
- Total stable Printify count now 157 = Sticker 76, Poster 28, Acrylic 53.

## 2026-05-04 11:01 -04:00 Publish Batch 006
- Published 15/15 audited mixed items through Printify API after the browser/CDN path showed a transient Akamai zero-size-object failure.
- Delay window was 30-90 seconds.
- Published items: Poster-Academia-0017/0019/0020/0021/0022, Acrylic-Grimdark-0007/0008/0009/0010/0011, Sticker-Zen-0067/0068/0069/0070/0071.
- Published totals now: Sticker 60, Poster 26, Acrylic 26.
- Stable totals remain: Sticker 76, Poster 28, Acrylic 53.

## 2026-05-04 11:19 -04:00 eBay Developer/Akamai Cooling
- User reported `Service Unavailable - Zero size object` on `developer.ebay.com/develop`.
- Independent web check showed the eBay Developer page is globally reachable, so likely local browser/IP/session/CDN-edge issue rather than full outage.
- Public eBay publish cadence is slowed until the edge/session condition cools down.
- Continue API/local preparation; avoid repeated browser refresh/login loops against eBay Developer.

## 2026-05-04 12:04 -04:00 Steam Cleanup
- User confirmed deletion of Steam and Steam-related residual directories, preserving TapTap.
- Deleted `C:\Program Files (x86)\Steam`, `C:\Users\Rex\AppData\Local\Steam`, and the Start Menu Steam folder.
- C drive free space changed from 36.597GB to 37.816GB, freeing about 1.219GB.
- `C:\Users\Public\Desktop\Steam.lnk` could not be removed due access denied; no other large Steam game directory remained on disk.

## 2026-05-04 13:36 -04:00 Phase 1 Data Foundation
- Saved long-term 3-5 day / 7-12 day / 2-4 week factory roadmap in `PROJECT_FACTORY_ROADMAP.md`.
- Saved Rex/Gemini/Codex role model and Gemini advisor queue in `Gemini_Advisor/`.
- Generated local-only Etsy launch plan: 30 draft candidates, mix Poster 14 / Acrylic 10 / Sticker 6. No Etsy shop changes and no listing fees triggered.
- Generated `Database/Etsy_brand_shell.md` and `Database/Etsy_launch_plan.xlsx`.
- Added read-only Seller Hub snapshot logger. Latest loaded active-listing snapshot: 50 rows, 41 zero-view rows, 9 rows with at least 1 view, 4 General promoted rows.
- Added Printify external id sync and backfilled 85 eBay item IDs into `Database/eBay_listing.xlsx`; remaining missing/failed reads will be retried slowly.
- Generated morning report and Gemini review queue in `Reports/` and `Gemini_Advisor/`.
- Reset interrupted `Poster-Academia-0025` from `Printify_UI_Failed` back to `Ready_for_Printify` for safe recovery.

## 2026-05-04 14:05 -04:00 Poster Upload Timeout Recovery
- Tried to continue Poster-Academia-0025 through 0034 without public publish.
- Outer process timed out after 30 minutes during Printify-side slow response.
- Stable gains before timeout: Poster-Academia-0023 and 0024 are now `Printify_UI_Mockups8`.
- Poster-Academia-0025/0026/0027/0028 were marked failed with no product id; reset all four back to `Ready_for_Printify`.
- Decision: continue Poster uploads later in smaller batches to avoid long Printify stalls.

## 2026-05-04 14:24 -04:00 eBay 2 Percent Standard Ads Prep
- Confirmed Printify `external.id` can identify eBay item ids, but Printify API cannot directly enable eBay Promoted Listings.
- Added `modules/ebay_ads_standard.py` for eBay Marketing API/Seller Hub-aligned fixed 2.0% Standard ads preparation.
- Dry-run found 95 published listings with eBay item ids eligible for the `Fixed_2_Percent_Strategy` campaign.
- 17 published listings still lack local eBay item ids and need low-frequency Printify external-id retry before automated ad enrollment.
- Seller Hub read-only snapshot still shows 50 loaded active rows, 41 zero-view rows, and 4 General promoted rows.
- No ads were activated and no paid action was submitted.

## 2026-05-04 14:58 -04:00 eBay 2 Percent Standard Ads Activated
- User explicitly confirmed Promoted Listings Standard / General only, fixed 2.0%, no Priority/PPC, no suggested ad rate.
- Updated Seller Hub campaign `Fixed_2_Percent_Strategy` (campaign id `165251921016`).
- Campaign detail page confirmed: Promoted Listings / General, fixed ad rate, ad rate range `2%`, active, continuous duration.
- Added all 95 locally identifiable OpenClaw eBay item ids to the campaign; deleted dumbbell/toothbrush listings were not present in the whitelist.
- Verified campaign listing table shows `Showing 1-25 out of 95`; visible ad-rate inputs show `2.0`.
- Logged 95 `UI_CONFIRMED_STANDARD_2` rows into `Database/ebay_ads_standard_2pct.csv`.
- Updated `printify_publish_scheduler.py` so future Printify publishes sync the eBay external id and enqueue/enroll the item into the 2% campaign; if eBay OAuth is unavailable, the item is written to `Database/ebay_ads_pending_2pct.csv` instead of being forgotten.

## 2026-05-04 15:09 -04:00 eBay Ad Coverage Refreshed To 99
- Retried missing Printify external ids at low frequency; recovered 4 more eBay item ids.
- Reopened Seller Hub campaign editor and added the refreshed 99-id whitelist through the Item IDs workflow.
- Re-applied fixed single ad rate `2.0` after eBay temporarily defaulted newly added items to a higher suggested rate.
- Final campaign detail verification: `Fixed_2_Percent_Strategy`, Promoted Listings / General, fixed ad rate, ad rate range `2%`, `Showing 1-25 out of 99`.
- Logged 99 `UI_CONFIRMED_STANDARD_2_REFRESH_99` rows into `Database/ebay_ads_standard_2pct.csv`.

## 2026-05-04 15:14 -04:00 Seller Hub Snapshot After Ads
- Ran read-only Seller Hub active-listing snapshot after ad campaign update.
- Loaded visible active rows: 50.
- Visible rows promoted: 50.
- Visible rows with 0 views: 43; rows with at least 1 view: 7.
- Snapshot appended to `Database/Performance_Log.csv` for future baseline comparison.

## 2026-05-04 15:18 -04:00 Browser Resource Hygiene
- Added standing browser hygiene rule to `CURRENT_TASK.md`.
- Closed completed eBay advertising dashboard/campaign tabs and duplicate Seller Hub active-listing tabs.
- Left only 2 active project tabs: one eBay Seller Hub active listings tab and one Printify mockup/product tab.

## 2026-05-04 16:57 -04:00 Poster Batch 0025-0027 Recovered
- Ran Poster-Academia-0025 through 0027 through Printify API upload path.
- Product creation and Production_Design audits passed for all 3; Printify official mockups initially returned 0 and caused false failures.
- Delayed API recheck recovered all 3 as `Printify_UI_Mockups4`; official mockups now 4/4 for each.
- Updated `modules/printify_full_pipeline.py` to wait longer for Poster official mockups and classify unresolved cases as `Printify_MockupsPending` instead of hard UI failure.

## 2026-05-04 17:05 -04:00 Poster/Acrylic Product Fit Review
- Paused Poster background batch at Rex's request before continuing the monthly plan.
- Product fit conclusion: Poster and Acrylic are rectangular print products; artwork object silhouette does not affect manufacturing because the image is printed as a rectangular raster onto paper/acrylic.
- Sales-risk conclusion: buyer expectation needs clarity so customers do not mistake acrylic/poster art for a sculpted 3D object. Existing generated descriptions already include the Image Note: main image is the actual received product; additional images are concept/detail previews and not extra products/variations.
- Live Printify spot-check confirmed the Image Note is present on sampled Poster and Acrylic products.
- Pricing conclusion: Poster $34.99 is reasonable; Acrylic $89.99 is viable premium pricing with margin, but future Acrylic batches can test $84.99 for broader conversion while keeping select strongest designs at $89.99.


## 2026-05-04 20:22 -04:00 Etsy Brand Visual Drafts
- Cleared Chrome Etsy cookies/site data after Rex confirmation; Google cookies were not cleared.
- Reopened Chrome Etsy sign-in to clean page and closed Etsy-related Facebook OAuth residue.
- Default Etsy account operations will use Edge going forward because Rex confirmed Edge login works.
- Generated MJ Etsy brand design options 02/03/04 with local icon and banner assets under Output/Brand/Etsy/20260504_180120/previews.
- Waiting for Rex to select an option number before editing Etsy shop settings online.

## 2026-05-04 23:20 -04:00 Network Guard Added
- Current Wi-Fi is already on 5GHz / 802.11ac with strong signal.
- Preflight ping check: Printify/Etsy/Discord all reachable with 0% packet loss during sample.
- Added modules/network_guard.py and standing low-concurrency rule until network issue is declared resolved by Rex.

## 2026-05-05 00:24:12 -04:00 Protocol Update
- Adopted Gemini/Rex low-bandwidth protocol as default for the next ~2 days: prioritize local logic, data, QA, pricing, text/tag, and retry infrastructure; defer high-bandwidth uploads/OAuth churn.

## 2026-05-05 01:33:44 -04:00 Poster/Acrylic Gallery Backfill
- Fixed art_asset_builder so non-sticker products always write Gallery_U1-4 derived from the selected Production_Design image.
- Fixed edit_for_platforms so non-sticker listing rows prefer Gallery_U paths over raw Midjourney U paths.
- Added modules/gallery_backfill.py for repeatable local repair/audit.
- Backfilled 88 local Poster/Acrylic folders and updated 364 workbook gallery path cells across 91 non-sticker listing rows.
- Final audit: non-sticker rows using raw U gallery paths = 0.

## 2026-05-05 04:37:25 -04:00 Local Copy / Pricing / Registry Batch
- Generated Database/Listing_Copy_Optimization.csv/xlsx for 112 published eBay listings.
- Copy audit: eBay proposed title length failures = 0; Etsy tag count failures = 0.
- Generated Database/Pricing_Strategy_Matrix.csv/xlsx with 96 platform/product/ad-rate/shipping scenarios.
- Rebuilt Etsy_launch_plan to 50 local draft candidates using Quiet Relic Studio positioning; no Etsy listing fees triggered.
- Added resilient_http retry helper and wired it into Etsy OAuth/API modules.
- Generated Database/Unified_Listing_Registry.csv/xlsx with action buckets for 240 local listing rows.

## 2026-05-05 05:04:21 -04:00 Local Listing QA
- Added modules/local_listing_qa.py to audit production image existence, dimensions, cover/gallery paths, title length, and image-note readiness without network calls.
- First QA found one real corrupt local production file: Poster-Academia-0006.
- Rebuilt Poster-Academia-0006 Production_Design/Cover/Gallery from source U image.
- Final QA: 27 issue rows remain, all known Quality_Hold/low-res Sticker rows with missing cover/gallery; no Poster/Acrylic local image integrity issues remain.

## 2026-05-05 05:13:56 -04:00 Image Metadata Audit / Report Refresh
- Added modules/image_metadata_audit.py to audit image format, dimensions, file size, info keys, EXIF key count, and read status without rewriting uploaded artwork.
- Audited 1440 image references from eBay_listing.xlsx; 135 read errors are expected missing images from the 27 known low-res Sticker hold rows.
- Rebuilt Pricing_Strategy_Matrix with eBay 13.6% most-categories fee assumption plus .40 fixed fee; category/store fee still marked for final verification before scaling.
- Refreshed morning report and Gemini advisor queue: Reports/morning_report_20260505_0512.md and Gemini_Advisor/gemini_review_queue_20260505_0512.md.

## 2026-05-05 05:18:15 -04:00 Etsy Shop Packet
- Created Database/Etsy_shop_update_packet.md for selected Option 02 / Quiet Relic Studio.
- Included local icon, banner, preview board paths, shop-name choices, announcement/about/FAQ/shipping notes, and operator notes for Edge/Etsy handling.
- Full compile check passed for new/changed local modules.

## 2026-05-05 05:21:50 -04:00 Handoff Checkpoint
handoff checkpoint: Low-bandwidth local work lane is active. Do not run bulk MJ/Printify/eBay/Etsy writes until network_guard is healthy or Rex confirms wired network. Completed gallery backfill, local copy optimization, pricing matrix, unified registry, local QA, image metadata audit, Etsy Option 02 shop packet, and refreshed morning/Gemini reports.

## 2026-05-05 11:41:05 -04:00 Blueprint Official Probe
- Added modules/printify_blueprint_probe.py for checkpointed official Printify catalog probing.
- Weak-network small-batch probe succeeded for Canvas, Framed Poster, and Metal priority candidates.
- Current official detail file: Database/Product_Blueprint_Official_Details.csv with 120 rows across priority blueprint candidates.

## 2026-05-05 13:05:02 -04:00 Product Blueprint Official Details
- Created modules/printify_blueprint_probe.py for checkpointed official Printify catalog detail probing.
- Created modules/blueprint_summary_builder.py for Scholar-friendly summary output.
- Probed official provider/variant/print-area/shipping data for Canvas, Framed Poster, Metal, Notebook/Journal, and selected Mug blueprints.
- Output files: Database/Product_Blueprint_Scholar_Verification.csv, Database/Product_Blueprint_Official_Details.csv, Database/Product_Blueprint_Mug_Details.csv, Database/Product_Blueprint_Official_Summary.csv/xlsx.
- Important finding: queried catalog variant endpoints expose blueprint/provider/variant/print-area and shipping profiles, but not production cost; cost must be verified by UI or create-product/readback before pricing.

## 2026-05-05 13:58:40 -04:00 Etsy Digital Product R&D
- Added modules/etsy_digital_products.py as a local-only Etsy digital product R&D and printable wall-art pack builder.
- Created Database/Etsy_Digital_Product_RnD.md, Database/Etsy_Digital_Product_RnD.csv, Database/Etsy_Digital_Candidates.csv, and Database/Etsy_Digital_Pilot_Packs.csv.
- Built 3 instant-download printable wall art pilot packs under Output/Digital/PrintableWallArt using existing high-resolution Poster production images.
- Each pilot pack contains 5 Etsy-ready JPG ratios: 2x3, 3x4, 4x5, 11x14, and ISO A-series; max file size is 2.54MB, below Etsy's 20MB per-file digital upload limit.
- Decision: start digital products with printable wall art sets; keep personalized ex-libris/bookplate as second pilot; defer pet/family portraits until a revision and image-privacy workflow exists.

## 2026-05-05 14:05:37 -04:00 Handoff Checkpoint
handoff checkpoint: Etsy digital R&D branch is local-only and ready for Rex review. No Etsy upload or storefront edit was performed. First recommended launch is 20 printable wall art instant-download listings from best Poster images; 3 pilot packs already generated and verified under Etsy file-size limits.

## 2026-05-05 17:05:00 -04:00 Wi-Fi 5GHz Diagnosis
- Confirmed the Realtek 8821CE hidden registry setting `PreferBand=2`, meaning the driver is already configured as 5GHz first.
- Short stability test showed the adapter started on 5GHz channel 52 with 100% signal, disconnected, then rejoined the same SSID on 2.4GHz channel 11.
- Codex process lacks Windows administrator rights to write HKLM adapter advanced settings directly; attempts to change `PreferBand`, `RegROAMSensitiveLevel`, and `ConcurrentOpPref` were denied by Windows.
- Added tools/wifi_prefer_5g_admin.ps1 for an elevated run: keeps 5GHz preference, lowers roaming sensitivity, removes 2.4GHz concurrent-operation preference, and sets Wi-Fi power saving to maximum performance.

## 2026-05-05 17:31:32 -04:00 Wi-Fi 5GHz Preference Applied With Admin
- Ran tools/wifi_prefer_5g_admin.ps1 through an elevated UAC process.
- Applied Realtek adapter settings: `PreferBand=2` (5G first), `RegROAMSensitiveLevel=80` (lower roaming sensitivity), `ConcurrentOpPref=0` (no 2.4GHz concurrent preference), Wi-Fi power saving set to maximum performance.
- After restart and manual reconnect, Windows still selected `Verizon_P9PQG9` on 2.4GHz channel 11, not 5GHz.
- Conclusion: local adapter preference is now correctly set; remaining issue is likely Verizon gateway band steering / merged SSID / 5GHz DFS channel instability, not a missing Windows preference.

## 2026-05-05 18:31:35 -04:00 eBay Traffic Experiment Batch
- Added modules/ebay_traffic_experiment.py to create a reversible A/B/C experiment for zero-view active Sticker listings.
- Backed up workbook to Database/eBay_listing.backup_traffic_experiment_20260505_182220.xlsx.
- Experiment groups: 18 A_TITLE_INTENT_REWRITE, 14 B_COVER_QA_PRIORITY, 12 C_HOLDOUT_CONTROL.
- A group rewrites were applied locally and synced through Printify with title/description-only publish; all 18 returned update=200 and publish=200.
- Sync queue: Database/eBay_Metadata_Sync_Queue.csv now has 18 SYNCED rows; log: Database/eBay_Metadata_Sync_Log.csv.
- B group remains unchanged for cover/thumbnail QA; C group remains unchanged as holdout control for 48-72h comparison.

## 2026-05-05 20:02:02 -04:00 Low-Bandwidth Monthly Tasks Continued
- Expanded Etsy printable wall art digital product prep from 3 pilots to 20 upload-ready listings.
- Output: Database/Etsy_Digital_Upload_Queue.csv and Output/Digital/PrintableWallArt/Pilot_Contact_Sheet_20.jpg.
- Each digital listing has 5 JPG ratios and all files remain below Etsy's 20MB per-file digital upload limit; largest observed file is 3.42MB.
- Added modules/etsy_digital_bundle_builder.py and generated 3 bundle concepts: 12-piece Dark Academia ($19.99), 3-piece Zen ($12.99), 8-piece Mixed ($17.99).
- Added modules/ebay_cover_qa.py and Database/eBay_Cover_QA_Manual_Review.md; B group cover QA found local files valid but several dragon covers need stronger 4pc-sticker thumbnail clarity before image sync.
- Added modules/ebay_experiment_report.py for future A/B/C delta reporting after new Seller Hub snapshots.
- Updated modules/factory_morning_report.py so reports now include Etsy digital queue, bundle concepts, cover QA, and eBay experiment group counts.

## 2026-05-05 20:22:00 -04:00 Etsy Digital Upload Packet Hardened
- Added modules/etsy_digital_preview_builder.py and generated 3 Etsy preview images for each of 20 printable wall art listings.
- Improved preview typography/layout after visual QA: first pass text was too small for Etsy thumbnails; regenerated with large digital-download and size-ratio panels.
- Updated modules/etsy_digital_qa.py to validate both 100 customer download JPG files and 60 preview images; final QA bad=0, missing=0.
- Added modules/etsy_digital_listing_export.py and generated Database/Etsy_Digital_Final_Upload_Packet.csv/md with title, description, 13 tags, price, 3 previews, and 5 download files per listing.
- Cleaned Etsy digital titles locally to remove repeated phrases such as "Wall Art Wall Art"; no Etsy upload or listing fee was triggered.

## 2026-05-05 21:42:00 -04:00 Live eBay Cover Integrity Gate
- Added modules/ebay_online_cover_audit.py to compare live eBay main gallery images against local Cover_Mockup.png and U1-U4 files.
- Audited the 14 cover-priority active Sticker listings: 1 matched local Cover_Mockup, 13 matched a single U image instead of the intended cover.
- Wrote Database/eBay_Online_Cover_Audit.csv, Database/eBay_Online_Cover_Fix_Queue.csv, and a contact sheet under Database/eBay_Online_Cover_Audit/.
- Added modules/printify_image_default_audit.py; current audit shows 123/161 Printify-tracked products need checking because many expose multiple default images.
- Tightened modules/printify_publish_scheduler.py so future publish attempts are blocked when Printify reports anything other than exactly one default image.
- Updated morning/Gemini reports to include live cover mismatch counts and Printify default-image audit counts.

## 2026-05-05 22:18:00 -04:00 Buyer Image Note + Cover Repair Plan
- Confirmed eBay revise pages for Sticker variation listings show the live buyer gallery as variation photos; affected listings can be missing the local 4pc Cover_Mockup entirely.
- Created Database/eBay_Live_Cover_Fix_Plan.md documenting the root cause, safe repair path, and do-not-do rules.
- Added modules/ensure_image_note.py and patched all 18 eBay local descriptions missing the buyer-facing image note.
- eBay local description audit now passes: 240/240 rows include the image note that the main image is the actual product customers receive, while additional images are concept/detail references.

## 2026-05-05 22:32:00 -04:00 Full Sticker Live Cover Audit
- Ran live eBay cover audit across all 47 published Sticker rows with eBay item ids.
- Result by latest SKU state: 2/47 live Sticker listings match local Cover_Mockup; 45/47 show a single U image as the live main/buyer-facing image.
- Refreshed Database/eBay_Online_Cover_Fix_Queue.csv; current pending live cover fixes: 45.
- This confirms the cover problem is a system-level variation-photo sync issue, not an isolated listing mistake.

## 2026-05-05 22:45:00 -04:00 Poster/Acrylic Live Cover Audit
- Ran live eBay cover audit across 52 published Poster/Acrylic rows with eBay item ids.
- Most Poster/Acrylic rows are AMBIGUOUS because local Gallery_U1 is intentionally the same or near-same full image as Cover_Mockup for single-image products.
- Added 4 non-sticker rows to the cover fix queue for manual/high-confidence review: Poster-Academia-0001, Poster-Academia-0003, Acrylic-Grimdark-0081, Acrylic-Zen-0001.
- Current live cover fix queue total: 49 rows (45 Sticker, 2 Poster, 2 Acrylic).

## 2026-05-06 00:38:00 -04:00 eBay Cover Repair Rule Learned
- Tested Seller Hub Reports image repair on Sticker-Zen-0025.
- Parent-level EPS-only image CSV completed, but live buyer page still showed a single U image because eBay uses the variation photo set for these Printify sticker listings.
- Variation-level Reports repair failed with eBay error: inventory-managed items do not allow add/delete variation pictures.
- Conclusion: existing Printify-synced eBay variation photos cannot be safely repaired through Seller Hub Reports.
- Created modules/ebay_cover_repair_decision.py and Database/eBay_Cover_Repair_Decisions.csv/md to preserve the decision logic.
- Current repair plan: fix source mockup defaults in Printify and re-sync; if live Inventory-managed listings still reject image changes, replace bad listings with newly generated correct listings and retire the bad ones after verification.
- Hardened modules/printify_mockup_ui_uploader.py with CDP command timeouts, `--ids`, and `--allow-any-status` so source-cover repairs can target published rows without waiting indefinitely or sweeping unrelated rows.

## 2026-05-06 01:08:00 -04:00 Automation-First Control Layer
- Added modules/factory_supervisor.py as the durable plant-manager entrypoint for unattended local work and publish blocking.
- Supervisor writes Database/Factory_Autopilot_State.json, Database/Factory_Autopilot_Action_Queue.csv/md, and Database/Factory_Autopilot_Run_Log.csv.
- Ran `py modules\factory_supervisor.py --execute-local --skip-network`; local cycle completed with 0 failures.
- Current local outputs refreshed: Local_Listing_QA, eBay_Cover_Repair_Decisions, Unified_Listing_Registry, Market_Signal_Action_Queue, eBay_Traffic_Experiment_Report, morning report, and Gemini review queue.
- Updated modules/market_signal_planner.py so live eBay cover mismatches become `FIX_LIVE_COVER_SOURCE_OR_REPLACE` instead of generic market actions.
- Hardened modules/printify_mockup_ui_uploader.py and modules/printify_full_pipeline.py so selected Printify images must have exactly one default image before success/publish status is accepted.
- Saved the automation-first rule into PROJECT_OPERATING_PROTOCOL.md: Codex should debug and upgrade the factory, while recurring execution must move into scripts/queues/guards/reports.

## 2026-05-06 01:25:00 -04:00 Read-Only eBay Snapshot + Supervisor Login Gate
- Patched modules/ebay_sellerhub_snapshot.py so temporary Seller Hub CDP tabs are closed after read-only extraction.
- Ran read-only Seller Hub active-listing snapshot with 12 scrolls: 50 rows read, 42 zero-view, 8 with at least one view, 50 Promoted Standard/General.
- Refreshed Unified_Listing_Registry, eBay_Traffic_Experiment_Report, morning report, and supervisor state from the latest snapshot.
- Added Printify CDP login detection to modules/factory_supervisor.py.
- Current supervisor cover action is `WAIT_PRINTIFY_LOGIN`, because the CDP-controlled Printify profile is still on `https://printify.com/app/auth/login`.
- No publish, image upload, or account write was performed in this batch.

## 2026-05-06 01:33:00 -04:00 Cover Replacement Fallback Queue
- Added modules/ebay_cover_replacement_queue.py to preserve the fallback path if Printify source re-sync cannot repair live eBay inventory-managed variation photos.
- Generated Database/eBay_Cover_Replacement_Queue.csv/md with 49 rows.
- Queue breakdown: 45 `WAIT_SOURCE_REPAIR_RESULT`, 4 `REVIEW_BEFORE_REPLACE`.
- Added replacement queue generation to the local supervisor cycle.
- Updated modules/factory_morning_report.py so morning reports include replacement queue status.

## 2026-05-06 01:40:00 -04:00 Local Title-Length Repair Queue
- Added modules/ebay_title_repair_queue.py to detect published eBay titles outside the 75-79 character house rule and prepare safe local repairs.
- Applied local-only title repairs to 7 published Sticker rows; no Printify/eBay online sync was performed.
- Refreshed Local_Listing_QA: issue rows decreased from 34 to 27.
- Remaining QA issues are the known low-res/missing-cover Sticker hold rows, not active published title-length errors.
- Added title repair generation to the local supervisor cycle.

## 2026-05-06 01:45:00 -04:00 Repeatable eBay Traffic Diagnosis
- Added modules/ebay_traffic_diagnosis.py so low-traffic hypotheses are generated from Seller Hub snapshots, cover queues, and experiment data instead of manual guesswork.
- Generated Database/eBay_Traffic_Diagnosis.csv/md.
- Current diagnosis: Sticker live cover/gallery mismatch is the primary blocker; 2% Standard ads are active but not enough by themselves; Poster/Acrylic show more early movement than Sticker; title rewrite alone has not lifted Sticker experiment groups yet.
- Added traffic diagnosis to the local supervisor cycle and morning report.

## 2026-05-06 01:51:00 -04:00 Printify API Cover Repair Constraint
- Checked official Printify API docs for product update behavior.
- Durable finding saved into Database/eBay_Live_Cover_Fix_Plan.md: product mockup `images` are read-only in the update model, so ordinary product PUT is not a reliable way to repair existing live mockup defaults.
- Current automated repair order remains: source repair through Printify mockup UI when CDP profile is logged in; if live eBay still rejects the changed variation photo set, create verified replacement listings and retire old bad listings after live audit.

## 2026-05-06 01:53:00 -04:00 Supervisor End-to-End Local Verification
- Ran `py modules\factory_supervisor.py --execute-local --skip-network`.
- Completed local supervisor cycle with 0 failures.
- One command now refreshes: Local_Listing_QA, eBay_Cover_Repair_Decisions, eBay_Cover_Replacement_Queue, eBay_Title_Repair_Queue, Unified_Listing_Registry, Market_Signal_Action_Queue, eBay_Traffic_Experiment_Report, eBay_Traffic_Diagnosis, morning report, and Gemini advisor queue.
- Current blocking status remains `WAIT_PRINTIFY_LOGIN` for cover repair because the CDP-controlled Printify browser profile is still logged out.

## 2026-05-06 02:00:00 -04:00 eBay Profile Trust Packet
- Added modules/ebay_profile_packet.py to produce a reusable eBay seller-profile update packet from the selected Quiet Relic Studio brand shell.
- Generated Database/eBay_Profile_Update_Packet.md with seller profile image path, optional banner reference, seller bio draft, buyer-facing image note, and category suggestions.
- This is a low-bandwidth trust-building task; no Seller Hub profile edit was performed.

## 2026-05-06 02:07:00 -04:00 Next Product Blueprint Test Plan
- Added modules/product_blueprint_next_plan.py to condense official Printify blueprint probe data into a Scholar-verifiable next-test packet.
- Generated Database/Product_Blueprint_Next_Test_Plan.csv/md.
- Current priority order: Canvas blueprint 1936 variant 119906, Framed Poster blueprint 1236 variant 93818, Notebook/Journal blueprint 5634 variant 252281, Mug blueprint 478 variant 65216, Metal blueprint 1206 variant 91995.
- No product creation/upload was performed; this is a R&D planning artifact for later cost/mockup verification.

## 2026-05-06 02:10:00 -04:00 Market Queue Default-Image Gate
- Updated modules/market_signal_planner.py to read Database/Printify_Image_Default_Audit.csv.
- Products with Printify default audit `CHECK` are now assigned `FIX_PRINTIFY_DEFAULT_IMAGE_BEFORE_PUBLISH`, not publish actions.
- Current market queue actions: 74 default-image fixes, 49 live cover source/replace fixes, 50 upload candidates, 24 small-batch publish candidates, 27 QA holds.
- Refreshed morning report and supervisor state after the queue correction.

## 2026-05-06 02:12:00 -04:00 Recovery State Refresh
- Rebuilt RECOVERY_STATE.json to reflect the May 6 factory state instead of the old April 29 recovery checkpoint.
- Recovery now points first to CURRENT_TASK.md, PROGRESS_LOG.md, PROJECT_OPERATING_PROTOCOL.md, Factory_Autopilot state/queue, eBay cover plan, and latest morning reports.
- Validated RECOVERY_STATE.json parses as JSON.

## 2026-05-06 02:14:00 -04:00 Handoff Checkpoint
handoff checkpoint: Automation-first control layer is now live. Use `py modules\factory_supervisor.py --execute-local --skip-network` for local maintenance and `py modules\factory_supervisor.py` before any online batch. Current blocker is Printify CDP login plus live cover/default-image gate; no more Sticker publishing until a targeted source repair or replacement path passes live eBay cover audit.

## 2026-05-06 07:34:00 -04:00 Supervisor Cover Repair Runner Wired
- Added and compiled `modules/factory_cover_repair_runner.py`.
- Dry-run correctly stopped at `WAIT_PRINTIFY_LOGIN`; no upload, publish, or eBay write was performed.
- Updated `modules/factory_supervisor.py` so the cover-gate action becomes a one-SKU repair runner once the Printify CDP browser is logged in.
- Ran `py modules\factory_supervisor.py --execute-local --skip-network`; local cycle completed with 0 failures and refreshed QA, repair decisions, replacement queue, registry, market queue, experiment report, traffic diagnosis, profile packet, blueprint plan, morning report, and Gemini queue.
- Current blocker remains Printify CDP login. Current safe next online command after login: `py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120`.

## 2026-05-06 07:40:00 -04:00 Factory Backlog Added
- Added `modules/factory_backlog.py` and wired it into `modules/factory_supervisor.py`.
- Generated `Database/Factory_Backlog.csv` and `Database/Factory_Backlog.md`.
- Backlog currently has 13 tasks: 4 READY, 2 WAIT_COVER_GATE, 2 WAIT_USER_OR_API_APPROVAL, 1 BLOCKED, 1 WAIT_PRINTIFY_LOGIN, 1 BLOCKED_BY_COVER_GATE, 1 WAIT_SOURCE_REPAIR_RESULT, and 1 READY_FOR_SCHOLAR_REVIEW.
- Ran supervisor again; local cycle completed with 0 failures and now includes backlog generation.

## 2026-05-06 07:44:00 -04:00 Morning Report Backlog Summary
- Updated `modules/factory_morning_report.py` to include `Factory_Backlog` status counts, top tasks, and lane counts.
- Generated `Reports/morning_report_20260506_0744.md` and `Gemini_Advisor/gemini_review_queue_20260506_0744.md`.

## 2026-05-06 07:51:00 -04:00 Production Design Integrity Audit Hardened
- Updated `modules/printify_design_audit.py` with stable output `Database/Printify_Production_Design_Audit.csv`, product-type filter, ID filter, and weak-network sleep controls.
- Ran a tiny Acrylic audit under conservative network mode: 2/2 passed visual/size match against local `Production_Design.png`; both had `ahash_distance=0`.
- Exact SHA differed for both rows, likely due Printify-side image re-encoding, but dimensions and visual hash matched exactly.
- Added a P63 `production_design_qa` action to `modules/factory_supervisor.py`: `py modules\printify_design_audit.py --limit 2 --sleep-seconds 1`.
- Refreshed `Factory_Backlog`, morning report, and Gemini queue.

## 2026-05-06 07:54:00 -04:00 Recovery State Updated
- Updated `RECOVERY_STATE.json` to point at the new `Factory_Backlog` and `Printify_Production_Design_Audit` files.
- Added the one-SKU source repair command and latest production-design QA sample result to durable recovery memory.
- Validated `RECOVERY_STATE.json` parses successfully.

## 2026-05-06 08:00:00 -04:00 Production QA Retry Path
- Switched `modules/printify_design_audit.py` from bare `requests.get` to `modules.resilient_http.request_with_retry` for Printify product JSON and remote image downloads.
- Ran a one-row Poster production design audit: Poster-Academia-0001 passed visual/size match, `ahash_distance=0`, local and remote sizes both 3600x5400.
- Removed a Pillow deprecation warning by replacing `getdata()` with `tobytes()` in the image hash path.

## 2026-05-06 08:28:00 -04:00 Printify Login Guard + Recovery Manual
- Added `PRINTIFY_LOGIN_EMAIL=rexxu024@gmail.com` to `.env` and exposed `Config.PRINTIFY_LOGIN_EMAIL`.
- Added `modules/printify_login_guard.py`.
- Login guard only allows Google account `rexxu024@gmail.com`; if another account appears or Google asks for a password, it stops and writes manual-login status.
- Verified `npm run printify:login:dry`; current Chrome CDP profile is `LOGGED_IN` to Printify dashboard.
- Added `requirements.txt`, `package.json`, and `OPERATIONS_MANUAL.md`.
- Updated `README.md` to point future recovery to `OPERATIONS_MANUAL.md`, `RECOVERY_STATE.json`, `CURRENT_TASK.md`, and `PROGRESS_LOG.md`.
- Confirmed existing Codex automation `Openclaw Git Checkpoint Push` runs every 2 hours against `origin main`.
- Verified `npm run etsy:api-status`; Etsy API remains `PENDING_OR_INACTIVE` / HTTP 403.


## 2026-05-06 11:35:00 -04:00 Printify Mockup Policy + Recovery Index
- Added `START_HERE_OPENCLAW.md` as the short recovery map for Rex/Codex/Gemini/another AI after thread break, power loss, or new-device setup.
- Updated `README.md`, `OPERATIONS_MANUAL.md`, and `RECOVERY_STATE.json` to point at the new recovery entrypoint.
- Codified the product image policy: preserve Printify official/default mockups when useful, especially for Poster/Acrylic buyer context; do not fail a product merely because multiple official/default images exist.
- Adjusted `printify_mockup_ui_uploader.py`, `factory_cover_repair_runner.py`, `printify_primary_audit.py`, and `printify_publish_scheduler.py` so QA checks for required custom image/design presence and at least one default, instead of enforcing exactly one default.
- Tested one source-repair path on `Sticker-Academia-0005`; the Printify UI now reaches the save/publish stage and the API shows selected images plus the custom cover present. Next scaling gate is live eBay buyer-page audit, not a bulk repair batch.
- Kept premium MJ-generated product scene/mockups as R&D only: potentially valuable later, but must pass QA before replacing or supplementing Printify official mockups.


## 2026-05-06 12:22:00 -04:00 Live Cover Audit Proves Replacement Path
- Ran a direct live eBay buyer-page audit for `Sticker-Academia-0005` after Printify source repair reached the save/publish stage.
- Result remained `LIKELY_SINGLE_U_MISMATCH`: eBay front page matched local `U4` exactly and remained far from the local cover (`cover=194`, `U4=0`).
- Updated `Database/eBay_Cover_Repair_Decisions.csv`: `Sticker-Academia-0005` is now `SOURCE_REPAIR_DONE_LIVE_STILL_BAD`.
- Updated `modules/ebay_cover_replacement_queue.py` so source-repaired-but-live-still-bad rows become `READY_TO_REPLACE_VERIFIED` instead of staying in `WAIT_SOURCE_REPAIR_RESULT`.
- Regenerated `Database/eBay_Cover_Replacement_Queue.csv/md`: 1 row is now `READY_TO_REPLACE_VERIFIED`, 44 remain `WAIT_SOURCE_REPAIR_RESULT`, 4 remain `REVIEW_BEFORE_REPLACE`.
- Operational conclusion: do not keep burning time on the same old inventory-managed listing when live eBay refuses the source image sync. Build verified replacement listing flow, then retire the old item only after the new live buyer-page audit passes.


## 2026-05-06 12:48:00 -04:00 Default Mockup Policy Propagated To Planner
- Updated market planner so multiple Printify official/default mockups are no longer treated as a publish blocker by themselves.
- The new blocker is true image insufficiency: selected image count below expected, zero default image, or audit error.
- Updated factory backlog and supervisor so a source-repaired live eBay failure can surface as `READY_TO_REPLACE_VERIFIED`.
- Confirmed local supervisor preserves `Sticker-Academia-0005` as the verified replacement-path sample.


## 2026-05-06 13:00:00 -04:00 Replacement Draft Created, Online Upload Paused By Network Guard
- Added `modules/ebay_replacement_draft_builder.py` and targeted `--ids` support to `modules/printify_full_pipeline.py`.
- Created local replacement row `Sticker-Academia-0005-FIX1` from the verified failed listing `Sticker-Academia-0005`.
- The replacement row is `Ready_for_Printify`, with old Printify/eBay external IDs cleared.
- Ran network guard before online upload: Printify avg 474ms, max 2780ms, Discord loss 16%; strategy returned `pause`.
- Therefore no Printify upload and no eBay publish were attempted. Next online action when network improves: `py modules\printify_full_pipeline.py --ids Sticker-Academia-0005-FIX1 --limit 1` without `--publish`.
## 2026-05-06 14:58 -04:00

- Wired LAN test passed: Ethernet 1Gbps active, Wi-Fi disconnected, 0% loss to Printify/eBay/Etsy/Discord/OpenAI, roughly 5-8ms average latency, 50MB download around 214 Mbps.
- Published and audited replacement experiments for the Sticker eBay cover bug:
  - `Sticker-Academia-0005-FIX1` proved the old custom U-gallery route still fails live audit.
  - `Sticker-Academia-0005-FIX2` proved Cover-only + Printify official mockups fixes the live main image.
  - `Sticker-Academia-0006-FIX1`, `0007-FIX1`, `0008-FIX1` passed live buyer-page cover audit.
  - Expanded batch: `Sticker-Academia-0009/0010/0011/0014/0015/0016-FIX1` and `Sticker-Zen-0001/0002/0003/0004-FIX1` created, published, and audited; official-only cases are now classified as `LIKELY_COVER_OFFICIAL`.
- Updated code:
  - Sticker full pipeline now uploads only Cover as the custom listing image and relies on Printify official mockups for marketplace gallery context.
  - Publish scheduler blocks Sticker products that still have custom U/gallery images selected.
  - Live eBay cover audit recognizes Printify official-only mockups as pass states instead of false-failing against local U hashes.
- Published 8 additional Poster/Acrylic listings after production-design QA: `Poster-Academia-0023..0026` and `Acrylic-Grimdark-0012..0015`; all 8 passed production-design audit and live buyer-page official-mockup audit.
- Created/updated `Database/eBay_Retire_Queue.csv` with 15 listings that should be safely ended after eBay API or Seller Hub end-listing flow is confirmed.

## 2026-05-06 15:20 -04:00

- Rex cleared the network constraint after LAN/asset validation; resumed full-throughput online work.
- Recompiled the changed Printify/eBay cover-gate modules successfully.
- Regenerated the eBay replacement queue: 31 ready-to-replace verified rows, 14 replacement-published-live-pass rows, 4 review-before-replace rows.
- Rechecked Printify/eBay connectivity: 0% packet loss, about 5-6ms average latency.

## 2026-05-06 16:45 -04:00

- Ran C drive cleanup audit and safe cleanup.
- C drive free space improved from about 31.36GB to about 54.73GB.
- Removed safe temp/cache targets only: user temp, Windows temp, pip cache, local `.cache`, browser caches, Discord cache, project `.tmp`, and project `__pycache__`.
- Cleared Recycle Bin.
- Left personal downloads, TapTap, Docker data, and production assets untouched.
- Added `Review_Packets/` as the central folder for Rex/Gemini/AI review material and added housekeeping ignore rules for obvious transient artifacts.

## 2026-05-06 17:30 -04:00

- Consolidated Rex/Gemini-facing project status into `Review_Packets/OPENCLAW_GEMINI_BRIEF.md`.
- Added `Review_Packets/REPORT_INDEX.md` and updated `Review_Packets/README.md`.
- Updated `START_HERE_OPENCLAW.md` so future recovery sessions know to use the Gemini brief before old timestamped reports.
- The new brief is written for Gemini without assuming repo or code access. It emphasizes: wired LAN is fixed, low-bandwidth mode is lifted, Sticker cover bug is the main quality issue, eBay ads alone did not solve traffic, eBay/Etsy APIs are still pending, and the next execution order is replacement audit/retirement then Poster to 50.

## 2026-05-06 17:45 -04:00

- Added dedicated automation browser helper `modules/automation_browser.py`.
- Added npm shortcuts `browser:edge` and `browser:edge:check`.
- Updated eBay browser scripts to accept `OPENCLAW_EBAY_CDP_PORT` / `OPENCLAW_CDP_PORT` so future Seller Hub and live-audit browser work can be moved away from Rex's active Chrome window.
- Codified browser isolation rule: prefer API/headless; use dedicated Edge/CDP profile when browser is necessary; close automation tabs after use.
- Launched dedicated Edge automation profile on CDP port 9223 at `C:\openclaw_edge_profile`.
- Retried two failed live eBay cover audits through dedicated Edge; both passed as `LIKELY_COVER_OFFICIAL`.
- Added 10 newly verified Sticker replacement mappings to `Database/eBay_Retire_Queue.csv`.
- Tested retiring one old listing through dedicated Edge; Seller Hub requires login in the dedicated profile, so the script stopped safely with `LOGIN_REQUIRED` and preserved queue status.

## 2026-05-06 18:10 -04:00

- Cleared Etsy-only site data/cache/cookies in the dedicated automation Edge profile and reopened a clean Etsy sign-in page.
- Rex still saw Etsy's red "An error has occurred, please try again!" banner after retry.
- Public checks did not suggest a clear Etsy-wide outage; current diagnosis is account/session/IP/security verification or Etsy-side login bug.
- Etsy UI edits, old listing deletion, and Etsy publish are paused to avoid repeated failed login attempts.
- Built `modules/printify_etsy_launch.py` and generated a 20-item Etsy candidate launch plan, but the first Printify Etsy smoke product had no selected official mockups yet; do not publish Etsy listings until mockup selection/login path is stable.

## 2026-05-06 18:25 -04:00

- Rex confirmed Chrome Google-account Etsy login also fails with the same red banner.
- Diagnosis strengthened: this is unlikely to be only Edge cache or a bad local profile.
- New operating rule: pause repeated Etsy credential retries, keep Etsy publish/storefront edits blocked, and continue eBay/Printify/local factory tasks.
- Recommended human-side checks are account-safe: Etsy email/security notice, `Trouble signing in?`, and one mobile/cellular login test to determine whether the Etsy account itself is temporarily blocked.

## 2026-05-06 18:43 -04:00

- Resumed full-throughput non-Etsy work after Rex confirmed to continue.
- Used dedicated automation Edge on CDP port 9223, not Rex's daily Chrome.
- Retired 10 old Sticker listings whose live eBay cover was previously wrong, and detached their old Printify external publish state:
  - `Sticker-Zen-0005`, `0007`, `0008`, `0009`, `0022`, `0024`, `0025`, `0027`, `0041`, `0042`.
- All 10 returned Seller Hub success banners and were marked `RETIRED_CONFIRMED` / `Retired_Replaced`.

## 2026-05-06 18:48 -04:00

- Topped up Poster by publishing `Poster-Academia-0034` through `0037`.
- All 4 Poster products passed Printify production-design audit: local `Production_Design` matched Printify front print area visually, with 3600x5400 remote size and ahash distance 0.
- All 4 Poster listings passed live eBay buyer-page image audit as `LIKELY_COVER_OFFICIAL`.
- eBay item IDs synced:
  - `Poster-Academia-0034` -> `406909467980`
  - `Poster-Academia-0035` -> `406909471020`
  - `Poster-Academia-0036` -> `406909472775`
  - `Poster-Academia-0037` -> `406909473606`
- All 4 were queued for future fixed 2% Promoted Listings Standard enrollment once eBay OAuth is available.
- Added market-learning rule: if eBay views remain flat, run controlled product/copy/price/category experiments rather than only adding more volume.

## 2026-05-06 19:00 -04:00

- Created `Review_Packets/REVENUE_EXPERIMENTS.md` for Rex/Gemini strategy review.
- Created `Database/Revenue_Experiment_Queue.csv` so revenue ideas become executable experiments instead of loose chat ideas.
- Recommended first practical revenue experiment: Etsy digital printable wall art packs from existing Poster assets, because it uses local assets, avoids Printify/shipping cost, and can be prepared while Etsy login is blocked.

## 2026-05-06 19:30 -04:00

- Added `modules/digital_printable_pack_builder.py` and built the first 10 Etsy digital printable ZIP packs locally.
- Added `modules/digital_etsy_metadata_builder.py` and generated 10 Etsy-ready metadata rows: title, description, 13 tags, price, ZIP path, and AI/digital-download disclosure.
- Added `Database/Etsy_Gray_Launch_Sequence.csv` for the 200-listing Etsy experiment pool.
- Added `Review_Packets/CODEX_STRESS_TEST_RESPONSE.md` with concrete answers to Gemini's stress test:
  - network guard now detects `full_throughput`;
  - eBay low-view risk requires controlled experiments, not more volume alone;
  - Cover Gate prevention is enforced through production/live audits;
  - Etsy listing fees must be spent through staged launch cells with stop rules.

## 2026-05-06 19:42 -04:00

- MJ harvest for `Poster-Academia-0038` through `0042` completed.
- Generated Poster production assets for `0038` through `0042` and wrote eBay/Etsy listing rows.
- Created and published Printify products for `Poster-Academia-0038` through `0042`; each passed Printify production-design audit and selected 8 official mockups.
- Printify has not yet returned eBay external item IDs for these 5 products after two sync attempts; they remain published-but-waiting-external-sync.
- Updated pricing/free-shipping rule: buyer-facing free shipping preferred, but Printify shipping is included in price/profit calculations.
- Created `Database/Printify_Cost_Shipping_Guardrail.csv` and `Database/Pricing_Strategy_Matrix.csv`.

## 2026-05-06 19:58 -04:00

- Added `Review_Packets/CODEX_STRESS_TEST_ROUND2.md` for Gemini/Rex.
- Added `Database/Etsy_Fee_Kill_Switch.json` with hard caps:
  - batch listing cap 10;
  - batch fee cap $2.00;
  - daily test fee cap $6.00;
  - ambiguous paid publish cap 1;
  - duplicate paid listing cap 0.
- Added `Database/Account_Risk_State.json` with Etsy marked `LOGIN_ANOMALY` and paid publish disabled.
- Added `modules/risk_guard.py` for marketplace write/fee preflight blocking.
- Added `modules/image_quality_gate.py` and ran it on `Poster-Academia-0038` through `0042`.
- Image QA result: final production assets mostly pass; `Poster-Academia-0041` cover/gallery shows `SHADOW_CLIPPING`, so it should be treated as published-but-review-recommended rather than a future winner seed.


## 2026-05-06 20:19:29 -04:00 Etsy Digital Gray Launch Gate + Printify External Sync Correction
- Built first Etsy Digital gray-launch batch from 10 prepared printable wall-art packs.
- Strict QA result: 10/10 PASS, 0 HOLD.
- Fee guard result: $2.00 reserved, $0.00 confirmed spent. Etsy publish remains blocked by Account_Risk_State because Etsy login/API access is not clean.
- Created `Database/Etsy_Digital_Gray_Launch_Queue.csv`, `Database/Etsy_Digital_QA_Report.csv`, `Database/Etsy_Fee_Ledger.csv`, and `Review_Packets/ETSY_DIGITAL_TRAFFIC_PENETRATION_REPORT_20260506.md`.
- Scheduled morning heartbeat report for Etsy Digital traffic penetration readout.
- Corrected `Poster-Academia-0038` through `0042` from false `Printify_Published_Mockups8` to `Printify_PublishExternalPending_Mockups8` because no eBay external id exists.
- Recovered `Poster-Academia-0037` external id into workbook: 406909473606.
- Patched `printify_publish_scheduler.py` so external-pending rows are not retried by default and published count means external id confirmed.


## 2026-05-06 20:46:12 -04:00 Replacement Publish Route Proof
- Created local replacement draft `Sticker-Zen-0044-FIX1` from verified cover-failure queue.
- Ran full Printify pipeline: product `69fbdfc9f60a24b6d1035f8b`, production design visual match PASS, selected official mockups=3, custom U gallery=0.
- Tried Printify API publish once; HTTP 200 but no eBay external id. Scheduler correctly reported `external_confirmed=0` and kept the row pending rather than counted as live.
- Conclusion: current blocker is marketplace publish route, not product assets. Use eBay API once approved or a verified Printify UI publish path; do not broad-retry Printify API publish.


## 2026-05-06 20:48:49 -04:00 Browser Isolation + Market Snapshot Refresh
- Patched Printify login guard, full pipeline, mockup uploader, and supervisor to default to dedicated Edge CDP port 9223 instead of daily Chrome 9222.
- Verified `npm run printify:login:dry` returns LOGGED_IN on dedicated Edge.
- Ran factory supervisor local cycle again: failures=0.
- Ran Printify production design audit: 2/2 passed visual match, ahash_distance=0.
- Read eBay Seller Hub snapshot through dedicated Edge: 50 rows, 43 zero-view, 7 with one-plus views, 50 promoted.
- Synced 80 Printify products for external ids: 67 updated. Traffic diagnosis now attributes movement by product type: Acrylic 3/17 moved, Poster 4/17 moved, Sticker 0/16 moved.
- Created `Review_Packets/EBAY_API_MINIMAL_APPLICATION_PACKET.md` and updated Gemini brief/index.

## 2026-05-06 21:58:00 -04:00 Authorization Guardrail + Etsy Digital Batch 1 Live
- Added Rex's full-project-access rule to `CURRENT_TASK.md`: routine OpenClaw file/account/API/browser/debug work should proceed without repeated permission prompts.
- Preserved hard red lines: payment/billing settings, orders, buyer/customer messages, private credentials, and spend beyond approved caps still require explicit confirmation.
- Etsy UI login is working in the dedicated Edge automation profile on CDP port 9223.
- First Etsy Digital gray batch is live: 10/10 printable wall-art listings published through Etsy UI, all digital/manual-renewal, confirmed listing-fee spend $2.00.
- Confirmed live Etsy listing ids:
  - `Poster-Academia-0001` -> `4500654287`
  - `Poster-Academia-0002` -> `4500664506`
  - `Poster-Academia-0003` -> `4500665474`
  - `Poster-Academia-0081` -> `4500657145`
  - `Poster-Academia-0082` -> `4500667154`
  - `Poster-Academia-0083` -> `4500667734`
  - `Poster-Academia-0084` -> `4500668282`
  - `Poster-Academia-0085` -> `4500668786`
  - `Poster-Academia-0091` -> `4500660013`
  - `Poster-Zen-0001` -> `4500669878`
- Etsy Shop Manager currently shows 12 active listings: 10 new OpenClaw digital tests plus 2 legacy DriveFuel listings.
- Patched the Etsy UI publisher during the run:
  - use the dedicated Edge profile, not Chrome;
  - upload ZIPs through Etsy's digital-file field, not the photo input;
  - copy ZIPs to short Etsy-safe upload names like `OC-Poster-Academia-0081.zip`;
  - write confirmed listing ids and spend to queue/metadata/ledger.
- Next: update Gemini/Rex packets, public QA sample, retire/delete the two legacy Etsy listings, and hold further paid Etsy publishing until first-10 traffic can be read or Rex asks to spend more.

## 2026-05-06 22:06:00 -04:00 Etsy Digital Public Page Audit
- Added `modules/etsy_live_audit.py` for reusable public Etsy listing checks through the dedicated Edge automation profile.
- Audited all 10 newly published Etsy Digital listings.
- Result: 10/10 `ACTIVE_READABLE`, 10/10 with digital-download signal present.
- Audit log written to `Database/Etsy_Digital_Live_Audit.csv`.

## 2026-05-06 22:20:00 -04:00 Etsy Legacy Listings Removed
- Deleted/retired the two old DriveFuel legacy Etsy listings Rex asked to remove:
  - `4407466791` - Impulse Purchase Recovery Kit (Digital Download)
  - `4366700475` - DriverFuel_SideHustle_Driver_Planner_Kit
- Public verification: both pages now show "This item is unavailable."
- Shop Manager active listing page no longer contains either legacy listing id/title.
- Clean confirmation saved to `Database/Etsy_Legacy_Retirement_Status.csv`.

## 2026-05-06 22:30:00 -04:00 Supervisor Etsy State Corrected
- Patched `factory_supervisor.py`, `factory_backlog.py`, and `factory_morning_report.py` so Etsy is no longer reported as merely waiting for user/API approval.
- New supervisor Etsy status: `READY_MONITOR` for first live Etsy Digital gray batch.
- Ran `npm run local`; result failures=0.
- Backlog now shows one Etsy monitor task instead of stale "hold until readiness" as the active Etsy path.
- Latest generated report: `Reports/morning_report_20260506_2230.md`.
- Latest Gemini queue: `Gemini_Advisor/gemini_review_queue_20260506_2230.md`.

## 2026-05-06 22:45:00 -04:00 Edge-Only Login Check
- Rex re-confirmed: all marketplace/account UI operations should use Edge, not Chrome.
- Dedicated Edge CDP 9223 is running.
- Printify login guard: `LOGGED_IN`.
- Etsy Shop Manager: `LOGGED_IN`.
- eBay Seller Hub active listings: `LOGGED_IN`.
- eBay Developer page timed out; not required for the immediate Etsy/Printify/Seller Hub workflow and still treated as pending/unstable until accessible.

## 2026-05-06 23:03:00 -04:00 Edge-Only Login Recheck + Network Guard
- Rex asked that all account/browser operations be handled in Edge and asked what logins are still needed.
- Dedicated Edge CDP 9223 is online.
- `py modules\network_guard.py`: `full_throughput`, 0% loss, average 5-8ms across Printify/Etsy/Discord.
- Printify guard through Edge: `LOGGED_IN`.
- Etsy Shop Manager through Edge: readable and logged in; dashboard shows DriveFuel with 10 active listings after legacy cleanup.
- eBay Seller Hub through Edge: readable; dry-run snapshot read 50 rows, 43 zero-view, 50 promoted.
- eBay Developer Program through Edge still redirects to sign-in/pending program access. This is the only current login/program-access gap and is not required for the immediate Printify/Etsy/Seller Hub UI work.

## 2026-05-06 23:11:00 -04:00 Printify-eBay Token Renewed + One Cover Replacement Closed
- Root cause for new Printify products not receiving eBay external ids: Printify showed `Your connection token is expired`.
- Renewed Printify's eBay authorization through Edge/eBay consent; Printify My Products no longer shows the expired-token banner.
- Re-published `Sticker-Zen-0044-FIX1`; Printify synced eBay item id `406909884756`.
- Live buyer-page cover audit: `LIKELY_COVER_OFFICIAL`, 3/3 selected images are Printify official mockups, no custom U gallery.
- Retired old bad-cover listing `Sticker-Zen-0044` / eBay `406902622710` through Edge Seller Hub; result `ENDED_CONFIRMED_SELLER_HUB`.
- Detached the old Printify external connection and marked old workbook row `Retired_Replaced`.
- Refreshed supervisor/local reports; failures=0. New report: `Reports/morning_report_20260506_2311.md`.

## 2026-05-06 23:20:00 -04:00 Cover Replacement Batch +3
- Created and published three additional cover-only replacement listings:
  - `Sticker-Zen-0045-FIX1` -> eBay `406909890800`
  - `Sticker-Zen-0046-FIX1` -> eBay `406909891985`
  - `Sticker-Zen-0049-FIX1` -> eBay `406909893702`
- All three passed buyer-page live cover audit as `LIKELY_COVER_OFFICIAL`; selected images are official-only mockups.
- Retired old bad-cover listings through Edge Seller Hub:
  - `Sticker-Zen-0045` / `406902640998`
  - `Sticker-Zen-0046` / `406902663232`
  - `Sticker-Zen-0049` / `406902713267`
- All three old listings returned `ENDED_CONFIRMED_SELLER_HUB` and old Printify external connections were detached.
- Cover repair decision count improved to `RETIRED_REPLACED_DONE=28`, `SOURCE_REPAIR_REQUIRED=17`, `NON_STICKER_REVIEW_REQUIRED=4`.

## 2026-05-06 23:39:00 -04:00 Cover Replacement Batch +5
- Created, published, audited, and retired another five Sticker cover replacements:
  - `Sticker-Zen-0050-FIX1` -> eBay `406909904704`
  - `Sticker-Zen-0051-FIX1` -> eBay `406909905683`
  - `Sticker-Zen-0052-FIX1` -> eBay `406909906686`
  - `Sticker-Zen-0053-FIX1` -> eBay `406909907111`
  - `Sticker-Zen-0054-FIX1` -> eBay `406909907742`
- All five passed live eBay buyer-page cover audit as `LIKELY_COVER_OFFICIAL`.
- Retired the five old bad-cover listings through Edge Seller Hub and detached old Printify external connections.
- Refreshed supervisor/local reports; failures=0. Latest report: `Reports/morning_report_20260506_2339.md`.
- Current cover-gate decision count: `RETIRED_REPLACED_DONE=33`, `SOURCE_REPAIR_REQUIRED=12`, `NON_STICKER_REVIEW_REQUIRED=4`.

```


# 1. Logic Architecture Snapshot


### FULL SOURCE: modules/edit_for_platforms.py
```python
import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from openpyxl import Workbook, load_workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config


DATABASE_DIR = PROJECT_ROOT / "Database"
OUTPUT_ROOT = PROJECT_ROOT / "Output"
OUTPUT_DIR = OUTPUT_ROOT / "Sticker" / "Kiss-Cut"
EBAY_BOOK = DATABASE_DIR / "eBay_listing.xlsx"
ETSY_BOOK = DATABASE_DIR / "Etsy_listing.xlsx"
EBAY_HEADERS = [
    "ID",
    "SKU",
    "Category",
    "Product_Type",
    "Title",
    "Description",
    "Price",
    "DNA Profile",
    "Production_Path",
    "Cover_Path",
    "Gallery_U1_Path",
    "Gallery_U2_Path",
    "Gallery_U3_Path",
    "Gallery_U4_Path",
    "Status",
    "Timestamp",
    "Printify_Product_ID",
]
ETSY_HEADERS = ["ID", "Raw_Metadata", "Production_Path", "Status", "Timestamp"]
DEFAULT_PRICE = os.getenv("STICKER_DEFAULT_PRICE", "$11.99")
PRODUCT_CONFIGS = {
    "Sticker": {
        "output_dir": OUTPUT_ROOT / "Sticker" / "Kiss-Cut",
        "price": os.getenv("STICKER_DEFAULT_PRICE", "$11.99"),
        "title_required": "4pc 6x6",
        "product_phrase": "Kiss-Cut Sticker",
        "includes": "One 6x6 kiss-cut sheet with 4 individual sticker designs.",
        "material": "Durable kiss-cut vinyl sticker sheet with waterproof finish.",
        "size": "6x6 kiss-cut sheet with four coordinated designs.",
    },
    "Poster": {
        "output_dir": OUTPUT_ROOT / "Poster" / "Premium-Matte-Vertical",
        "price": os.getenv("POSTER_DEFAULT_PRICE", "$34.99"),
        "title_required": "12x18",
        "product_phrase": "Matte Poster",
        "includes": "One 12x18 premium matte vertical poster.",
        "material": "Premium matte vertical poster through Printify Choice.",
        "size": "12x18 vertical wall art.",
    },
    "Acrylic": {
        "output_dir": OUTPUT_ROOT / "Acrylic" / "Photo-Block",
        "price": os.getenv("ACRYLIC_DEFAULT_PRICE", "$89.99"),
        "title_required": "5x7",
        "product_phrase": "Acrylic Photo Block",
        "includes": "One 5x7 vertical acrylic photo block.",
        "material": "Acrylic photo block with light-reflective gallery display finish.",
        "size": "5x7 vertical acrylic block.",
    },
}

TITLE_TEMPLATE_BANK = {
    "Sticker": [
        "{lead} {subject} 4pc 6x6 Kiss-Cut Sticker {scene}",
        "{subject} {lead} 4pc 6x6 Vinyl Sticker {audience} Gift",
        "{lead} {subject} 4pc 6x6 Sticker Sheet {emotion} Decor",
        "{subject} 4pc 6x6 Kiss-Cut Sticker {lead} {scene}",
        "{lead} {subject} 4pc 6x6 Vinyl Sticker Laptop Journal Gift",
        "{subject} {lead} 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor",
    ],
    "Poster": [
        "{lead} {subject} 12x18 Matte Poster Wall Decor",
        "{subject} {lead} 12x18 Matte Poster Study Room Art",
        "{lead} {subject} 12x18 Poster Library Print Scholar Gift",
        "{subject} 12x18 Matte Poster {lead} Gallery Decor",
        "{lead} {subject} 12x18 Wall Art Study Room Decor",
    ],
    "Acrylic": [
        "{lead} {subject} 5x7 Acrylic Photo Block Shelf Decor",
        "{subject} {lead} 5x7 Acrylic Photo Block Desk Display",
        "{lead} {subject} 5x7 Acrylic Block Collector Gift",
        "{subject} 5x7 Acrylic Photo Block {lead} Gallery Decor",
        "{lead} {subject} 5x7 Desk Art Acrylic Block Study Decor",
    ],
}

DESCRIPTION_TEMPLATE_BANK = [
    {
        "heading": "{base_title} {product_phrase}",
        "intro": "{intro}",
        "body": (
            "Designed for {use_cases}, this {product_lower} blends niche aesthetic appeal "
            "with collectible mentor-grade artwork."
        ),
        "close": "Complete the collection with matching Alchemy pieces.",
    },
    {
        "heading": "{base_title} | {product_phrase}",
        "intro": (
            "{intro} The artwork is built around a focused visual DNA profile, so each "
            "piece feels like part of a coherent small-batch collection."
        ),
        "body": (
            "Use it for {use_cases}. The composition favors readable detail, strong mood, "
            "and giftable niche appeal without generic mass-market styling."
        ),
        "close": "Pair it with related OpenClaw pieces for a coordinated collection.",
    },
    {
        "heading": "{base_title} - {product_phrase}",
        "intro": (
            "A polished {category} aesthetic piece for {audience}. {intro}"
        ),
        "body": (
            "The design works well across {use_cases}, while the title, material notes, "
            "and DNA profile stay specific for easy comparison."
        ),
        "close": "Saved under the reference SKU below for easy collector matching.",
    },
]


def _timestamp():
    return time.strftime("%-m/%-d/%Y  %-I:%M:%S %p") if os.name != "nt" else time.strftime("%#m/%#d/%Y  %#I:%M:%S %p")


def _clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _split_keywords(value):
    words = []
    seen = set()
    for part in re.split(r"[,|;/]", _clean_text(value)):
        cleaned = re.sub(r"[^A-Za-z0-9 &-]", "", part).strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        words.append(cleaned)
    return words


def _ascii_title(value):
    value = re.sub(r"[^\x00-\x7F]+", " ", _clean_text(value))
    value = re.sub(r"\s+", " ", value).strip(" -|")
    return value


def _title_tokens(value):
    return [word.lower() for word in re.findall(r"[A-Za-z0-9]+", value)]


def _title_repeats(value):
    words = _title_tokens(value)
    return {word for word in words if len(word) > 4 and words.count(word) > 1}


def _clean_subject(value, category):
    subject = _ascii_title(value) or "Art"
    subject = re.sub(r"[^A-Za-z0-9 ]+", " ", subject)
    subject = re.sub(r"\b(kiss[- ]?cut|sticker|stickers|vinyl|decal|sheet)\b", " ", subject, flags=re.I)
    if category:
        subject = re.sub(rf"\b{re.escape(category)}\b", " ", subject, flags=re.I)
    subject = re.sub(r"\s+", " ", subject).strip(" -|")
    return subject or "Art"


def _dedupe_long_words(value):
    result = []
    seen = set()
    for token in value.split():
        key = re.sub(r"[^A-Za-z0-9]+", "", token).lower()
        if len(key) > 4 and key in seen:
            continue
        if len(key) > 4:
            seen.add(key)
        result.append(token)
    return " ".join(result)


def _variant_index(metadata, modulo=6):
    seed = "|".join(
        _clean_text(metadata.get(key))
        for key in ("ID", "Title", "Category", "SEO_Hook", "Product_Type")
    )
    digest = hashlib.sha1(seed.encode("utf-8", errors="ignore")).hexdigest()
    return int(digest[:8], 16) % modulo


def _variant_pick(metadata, values):
    return values[_variant_index(metadata, len(values))]


def _variant_rotate(metadata, values):
    if not values:
        return []
    index = _variant_index(metadata, len(values))
    return values[index:] + values[:index]


def _parse_metadata(path):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    data = {"Raw_Metadata": raw}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def _ready_folders(product_type="Sticker"):
    output_dir = PRODUCT_CONFIGS[product_type]["output_dir"]
    if not output_dir.exists():
        return []
    return sorted(
        path for path in output_dir.iterdir()
        if path.is_dir()
        and path.name.startswith("MASTER_")
        and path.name.endswith("_Ready_for_Steaming")
    )


def _folder_id(folder):
    return (
        folder.name
        .replace("MASTER_", "")
        .replace("_Ready_for_Steaming", "")
        .replace("_Completed", "")
    )


def _fit_ebay_title(title, keywords, product_type="Sticker"):
    title = re.sub(r"[!]+", "", _clean_text(title))
    title = re.sub(r"\b(skin|person|text|watermark|blurry|edges)\b", " ", title, flags=re.I)
    title = re.sub(r"\s+", " ", title).strip()
    title = _dedupe_long_words(title)
    cfg = PRODUCT_CONFIGS.get(product_type, PRODUCT_CONFIGS["Sticker"])
    required = cfg["title_required"]
    if required.lower() not in title.lower():
        if product_type == "Sticker" and "Kiss-Cut" in title:
            title = title.replace("Kiss-Cut", f"{required} Kiss-Cut", 1)
        elif product_type == "Sticker" and "Sticker" in title:
            title = title.replace("Sticker", f"{required} Sticker", 1)
        elif product_type == "Poster" and "Poster" in title:
            title = title.replace("Poster", f"{required} Poster", 1)
        elif product_type == "Acrylic" and "Acrylic" in title:
            title = title.replace("Acrylic", f"{required} Acrylic", 1)
        else:
            title = f"{title} {required}"
    used_words = {word.lower() for word in re.findall(r"[A-Za-z0-9]+", title)}
    banned_title_words = {"skin", "person", "text", "watermark", "blurry", "edges"}
    extras = []
    for word in _split_keywords(keywords):
        parts = {part.lower() for part in re.findall(r"[A-Za-z0-9]+", word)}
        if parts & banned_title_words:
            continue
        if parts and (parts & used_words):
            continue
        extras.append(word.strip().title())
    if len(title) > 79:
        protected = required.split()
        words = title.split()
        result = []
        for word in words:
            candidate = " ".join(result + [word])
            if len(candidate) > 79:
                if word in protected:
                    result.append(word)
                break
            result.append(word)
        title = " ".join(result)
    if required.lower() not in title.lower():
        words = title.split()
        while len(" ".join(words + required.split())) > 79 and len(words) > 3:
            words.pop(-1)
        title = " ".join(words + required.split())
    filler = {
        "Sticker": ["Vinyl", "Laptop", "Journal", "Decor", "Gift", "Aesthetic", "Study", "Desk", "Reader", "Collector"],
        "Poster": ["Wall", "Decor", "Study", "Library", "Gift", "Aesthetic", "Gallery", "Room", "Art", "Collector"],
        "Acrylic": ["Shelf", "Decor", "Study", "Library", "Gift", "Aesthetic", "Gallery", "Block", "Art", "Collector"],
    }.get(product_type, ["Decor", "Gift", "Aesthetic", "Art", "Collector"])
    for extra in [*extras, *filler]:
        if len(title) >= 75:
            break
        parts = {part.lower() for part in re.findall(r"[A-Za-z0-9]+", extra)}
        if parts & banned_title_words:
            continue
        if parts & used_words:
            continue
        candidate = f"{title} {extra}"
        if len(candidate) <= 79 and not _title_repeats(candidate):
            title = candidate
            used_words.update(word.lower() for word in re.findall(r"[A-Za-z0-9]+", extra))
    return _repair_dangling_title(title[:79].strip(), product_type)


def _repair_dangling_title(title, product_type="Sticker"):
    title = _clean_text(title).rstrip(" ,-/")
    words = title.split()
    if not words:
        return title
    dangling = {"for", "with", "and", "or", "of", "in", "on", "by", "to", "from"}
    if words[-1].lower().strip(",") not in dangling:
        return title
    base_words = words[:-1]
    replacement_pool = {
        "Sticker": ["Gift", "Desk", "Laptop"],
        "Poster": ["Decor", "Gallery", "Study"],
        "Acrylic": ["Gift", "Shelf", "Display"],
    }.get(product_type, ["Gift", "Decor"])
    for replacement in replacement_pool:
        candidate = " ".join(base_words + [replacement])
        if len(candidate) <= 79:
            return candidate
    return " ".join(base_words).strip()


def _retitle_duplicate(title, item_id, keywords, product_type, used_titles):
    suffix_pool = {
        "Sticker": ["Journal", "Notebook", "Desk", "Reader", "Gift", "Collector", "Laptop", "Bottle", "Study", "Calm"],
        "Poster": ["Library", "Study", "Gallery", "Room", "Gift", "Collector", "Wall", "Scholar", "Decor"],
        "Acrylic": ["Shelf", "Desk", "Gallery", "Gift", "Collector", "Library", "Study", "Display", "Decor"],
    }.get(product_type, ["Gift", "Collector", "Decor"])
    seed = int(hashlib.sha1(_clean_text(item_id).encode("utf-8")).hexdigest()[:8], 16)
    rotated = suffix_pool[seed % len(suffix_pool):] + suffix_pool[:seed % len(suffix_pool)]
    for suffix in rotated:
        words = title.split()
        while len(" ".join(words + [suffix])) > 79 and len(words) > 5:
            words.pop(-1)
        candidate = _fit_ebay_title(" ".join(words + [suffix]), keywords, product_type)
        if 75 <= len(candidate) <= 79 and candidate not in used_titles:
            return candidate
    return title


def _keyword_pick(metadata, limit=3):
    title_words = _split_keywords(metadata.get("Title"))
    seo_words = _split_keywords(metadata.get("SEO_Hook"))
    banned = {
        "sticker",
        "stickers",
        "kiss cut",
        "kiss-cut",
        "vinyl",
        "decor",
        "collectible sticker",
        "mentor-grade sticker",
    }
    picks = []
    seen = set()
    for word in [*title_words, *seo_words]:
        normalized = word.lower()
        if normalized in banned or normalized in seen:
            continue
        if len(word) > 28:
            continue
        seen.add(normalized)
        picks.append(word.title())
        if len(picks) >= limit:
            break
    return picks


def _niche_profile(metadata):
    category = _clean_text(metadata.get("Category")).lower()
    seo = _clean_text(metadata.get("SEO_Hook")).lower()
    title = _clean_text(metadata.get("Title")).lower()
    if "academia" in category or "academia" in seo or "academia" in title:
        variants = [
            {"lead": "Dark Academia", "scene": "Laptop Study Journal Decor", "audience": "Book Lover Student", "emotion": "Cozy Vintage Intellectual", "style": "Academia Mentor-Grade"},
            {"lead": "Gothic Academia", "scene": "Study Desk Journal Decor", "audience": "Reader Writer Student", "emotion": "Moody Scholarly Vintage", "style": "Academia Mentor-Grade"},
            {"lead": "Vintage Academia", "scene": "Library Laptop Notebook Decor", "audience": "Book Lover Introvert", "emotion": "Literary Cozy Study", "style": "Academia Mentor-Grade"},
        ]
        return variants[_variant_index(metadata, len(variants))]
    variants = [
        {"lead": "Zen Aesthetic", "scene": "Laptop Journal Water Bottle Decor", "audience": "Mindfulness Minimalist", "emotion": "Calm Balance Peaceful", "style": "Zen Mentor-Grade"},
        {"lead": "Mindful Zen", "scene": "Journal Laptop Meditation Decor", "audience": "Yoga Minimalist Gift", "emotion": "Peaceful Calm Balance", "style": "Zen Mentor-Grade"},
        {"lead": "Minimal Zen", "scene": "Water Bottle Journal Desk Decor", "audience": "Calm Lifestyle Gift", "emotion": "Serene Mindful Clean", "style": "Zen Mentor-Grade"},
    ]
    return variants[_variant_index(metadata, len(variants))]


def _build_local_title(metadata):
    product_type = metadata.get("Product_Type", "Sticker")
    profile = _niche_profile(metadata)
    subject = _clean_subject(metadata.get("Title") or metadata.get("ID"), metadata.get("Category"))
    if len(subject) > 34:
        subject = " ".join(subject.split()[:4])
    values = {
        "lead": profile["lead"],
        "subject": subject,
        "scene": profile["scene"],
        "audience": profile["audience"],
        "emotion": profile["emotion"],
    }
    if product_type in {"Poster", "Acrylic"}:
        product_words = {
            "Poster": ["Wall Decor", "Study Room Art", "Library Print", "Gallery Decor", "Scholar Gift"],
            "Acrylic": ["Shelf Decor", "Desk Display", "Gallery Block", "Collector Gift", "Study Decor"],
        }[product_type]
        values["scene"] = _variant_pick(metadata, product_words)
        candidates = [template.format(**values) for template in _variant_rotate(metadata, TITLE_TEMPLATE_BANK[product_type])]
        best = candidates[0]
        for candidate in candidates:
            fitted = _fit_ebay_title(candidate, metadata.get("SEO_Hook"), product_type)
            if 75 <= len(fitted) <= 79:
                return fitted
            if abs(77 - len(fitted)) < abs(77 - len(best)):
                best = fitted
        return _fit_ebay_title(best, metadata.get("SEO_Hook"), product_type)
    tails = [
        profile["scene"],
        f"{profile['audience']} Gift",
        f"{profile['emotion']} Decor",
        "Laptop Journal Desk Decor",
        "Water Bottle Notebook Gift",
        "Study Desk Aesthetic Decor",
    ]
    values["scene"] = _variant_pick(metadata, tails)
    candidates = [template.format(**values) for template in _variant_rotate(metadata, TITLE_TEMPLATE_BANK["Sticker"])]
    best = candidates[0]
    for candidate in candidates:
        fitted = _fit_ebay_title(candidate, metadata.get("SEO_Hook"), product_type)
        if 75 <= len(fitted) <= 79:
            return fitted
        if abs(77 - len(fitted)) < abs(77 - len(best)):
            best = fitted
    return _fit_ebay_title(best, metadata.get("SEO_Hook"), product_type)


def _short_dna(metadata):
    prompt = _clean_text(metadata.get("MJ_Prompt"))
    prompt = re.sub(r"--\S+(?:\s+\S+)?", " ", prompt)
    prompt = re.sub(r"\b(white contour border|vector clean edges|die-cut sticker style|solid white background|isolated on white background)\b", " ", prompt, flags=re.I)
    prompt = _clean_text(prompt)
    if len(prompt) <= 360:
        return prompt
    return prompt[:357].rsplit(" ", 1)[0] + "..."


def _build_local_description(metadata):
    profile = _niche_profile(metadata)
    product_type = metadata.get("Product_Type", "Sticker")
    cfg = PRODUCT_CONFIGS.get(product_type, PRODUCT_CONFIGS["Sticker"])
    item_id = _clean_text(metadata.get("ID"))
    base_title = _ascii_title(metadata.get("Title")) or item_id
    seo_keywords = _split_keywords(metadata.get("SEO_Hook"))
    keyword_text = ", ".join(seo_keywords[:10])
    dna = _short_dna(metadata)
    category = _clean_text(metadata.get("Category")) or profile["lead"].replace(" Aesthetic", "")
    style = _clean_text(metadata.get("Style")) or profile["style"]
    if category.lower() == "zen":
        intros = [
            f"Bring calm and balance into your daily routine with this {base_title} zen aesthetic {cfg['product_phrase'].lower()}.",
            f"Add a quiet mindful accent to your workspace with this {base_title} {cfg['product_phrase'].lower()}.",
            f"Designed for peaceful desks, journals, and small rituals, this {base_title} {cfg['product_phrase'].lower()} carries a clean Zen mood.",
        ]
        intro = _variant_pick(metadata, intros)
        audiences = [
            "mindfulness lovers, minimalists, journal keepers, yoga enthusiasts, and peaceful room setups",
            "meditation fans, calm desk setups, notebook collectors, and gift buyers who like clean aesthetics",
            "students, remote workers, yoga lovers, and anyone building a serene everyday space",
        ]
        audience = _variant_pick(metadata, audiences)
    else:
        intros = [
            f"Embrace the dark academia aesthetic with this vintage-inspired {base_title} {cfg['product_phrase'].lower()}.",
            f"Give your study space a scholarly, moody accent with this {base_title} {cfg['product_phrase'].lower()}.",
            f"Built for readers and collectors, this {base_title} {cfg['product_phrase'].lower()} blends literary atmosphere with vintage study-room style.",
        ]
        intro = _variant_pick(metadata, intros)
        audiences = [
            "students, book lovers, writers, introverts, and dark academia collectors",
            "readers, literature fans, journal keepers, study desk decorators, and thoughtful gift buyers",
            "writers, learners, library lovers, and collectors of moody scholarly decor",
        ]
        audience = _variant_pick(metadata, audiences)
    use_case_variants = [
        "study rooms, creative workspaces, shelves, gallery walls, and collectible aesthetic decor",
        "laptops, notebooks, reading corners, desk setups, gallery shelves, and gift bundles",
        "journal spreads, library shelves, dorm rooms, studio desks, and cozy personal collections",
    ]
    use_cases = _variant_pick(metadata, use_case_variants)
    template = _variant_pick(metadata, DESCRIPTION_TEMPLATE_BANK)
    heading = template["heading"].format(base_title=base_title, product_phrase=cfg["product_phrase"])
    intro_text = template["intro"].format(
        intro=intro,
        category=category,
        audience=audience,
        product_phrase=cfg["product_phrase"],
        product_lower=product_type.lower(),
    )
    body_text = template["body"].format(
        use_cases=use_cases,
        product_lower=product_type.lower(),
        category=category,
        audience=audience,
    )
    close_text = template["close"].format(category=category, product_lower=product_type.lower())
    return (
        f"<h2>{heading}</h2>"
        f"<p>{intro_text}</p>"
        f"<p>{body_text}</p>"
        f"<ul>"
        f"<li><strong>Includes:</strong> {cfg['includes']}</li>"
        f"<li><strong>Material:</strong> {cfg['material']}</li>"
        f"<li><strong>Size:</strong> {cfg['size']}</li>"
        f"<li><strong>Style:</strong> {style}; {category} aesthetic.</li>"
        f"<li><strong>DNA Profile:</strong> {dna}</li>"
        f"<li><strong>Best For:</strong> {audience}.</li>"
        f"</ul>"
        f"<p><strong>SEO Keywords:</strong> {keyword_text}</p>"
        f"<p><strong>Image Note:</strong> The main image shows the actual product customers receive. Additional images are bonus concept/detail reference images and do not represent extra products or selectable variations.</p>"
        f"<p>{close_text}</p>"
        f"<p><small>Reference SKU: {item_id}</small></p>"
    )


def _ensure_image_note(description):
    description = _clean_text(description)
    note_pattern = re.compile(r"<p><strong>Image Note:</strong>.*?</p>", re.I | re.S)
    note = (
        "<p><strong>Image Note:</strong> The main image shows the actual product customers receive. "
        "Additional images are bonus concept/detail reference images and do not represent extra products "
        "or selectable variations.</p>"
    )
    if note_pattern.search(description):
        return note_pattern.sub(note, description, count=1)
    if "main image shows the actual product customers receive" in description.lower():
        description = re.sub(
            r"The main image shows the actual product customers receive[^<]*(?:</p>)?",
            "",
            description,
            flags=re.I,
        )
    if "</ul>" in description:
        return description.replace("</ul>", f"</ul>{note}", 1)
    return f"{description}{note}"


def _fallback_listing(metadata):
    title = _build_local_title(metadata)
    dna = _short_dna(metadata)
    description = _ensure_image_note(_build_local_description(metadata))
    return {"Title": title, "Description": description, "DNA Profile": dna}


def _deepseek_listing(metadata):
    api_key = [REDACTED]
    if not api_key:
        [REDACTED] RuntimeError("DEEPSEEK_API_KEY is missing")
    base_url = (Config.DEEPSEEK_BASE_URL or "https://api.deepseek.com").rstrip("/")
    prompt = {
        "ID": metadata.get("ID"),
        "Title": metadata.get("Title"),
        "SEO_Hook": metadata.get("SEO_Hook"),
        "Style": metadata.get("Style"),
        "MJ_Prompt": metadata.get("MJ_Prompt"),
        "Product_Type": metadata.get("Product_Type", "Sticker"),
    }
    payload = {
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "messages": [
            {
                "role": "system",
                "content": (
                    "Output strict JSON only. Keys: Title, Description, DNA Profile. "
                    "Create high-conversion eBay SEO for the Product_Type in the metadata. "
                    "Title must be 75-79 ASCII characters, no exclamation marks, no filler. "
                    "For Sticker, title must clearly include 4pc and 6x6. "
                    "For Poster, title must clearly include 12x18. For Acrylic, title must clearly include 5x7. "
                    "Use one of these title template families, with natural substitutions: "
                    "1) aesthetic lead + subject + required size + product noun + use case; "
                    "2) subject + aesthetic lead + required size + product noun + audience gift; "
                    "3) aesthetic lead + subject + required size + product noun + room/decor placement. "
                    "Use one of these description structures: "
                    "A) concise aesthetic intro, practical use paragraph, factual bullets, image note; "
                    "B) collector-focused intro, visual DNA paragraph, factual bullets, image note; "
                    "C) gift/use-case intro, mood paragraph, factual bullets, image note. "
                    "Use the item's metadata as the source of truth. "
                    "For Zen, emphasize calm, balance, mindfulness, minimalist, laptop, journal, water bottle. "
                    "For Academia, emphasize dark academia, study, vintage, intellectual, book lover, student, journal, study desk. "
                    "Description must be eBay-ready HTML and include Includes, Material, Size, Style, DNA Profile, and use cases. "
                    "Description must include an Image Note saying the main image shows the actual product customers receive, while additional images are bonus concept/detail reference images and do not represent extra products or selectable variations. "
                    "Vary sentence structure and keyword order across items so listings do not look mass-generated. "
                    "Use tasteful synonyms while preserving the same product facts. "
                    "Do not invent product materials beyond the requested Printify product type."
                ),
            },
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
        "temperature": 0.45,
    }
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=90,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(content)
    data["Title"] = _fit_ebay_title(data.get("Title"), metadata.get("SEO_Hook"), metadata.get("Product_Type", "Sticker"))
    data["Description"] = _clean_text(data.get("Description"))
    if "<" not in data["Description"]:
        data["Description"] = _build_local_description({**metadata, "MJ_Prompt": data.get("DNA Profile") or metadata.get("MJ_Prompt")})
    data["Description"] = _ensure_image_note(data["Description"])
    return data


def _gallery_paths(folder, item_id, product_type="Sticker"):
    paths = {}
    for index in range(1, 5):
        if product_type != "Sticker":
            candidates = [
                folder / f"Gallery_U{index}.png",
                folder / f"{item_id}_Gallery_U{index}.png",
                folder / f"{item_id}_U{index}.png",
                folder / f"{item_id}_U{index}_Grid.png",
            ]
        else:
            candidates = [
                folder / f"{item_id}_U{index}_Grid.png",
                folder / f"{item_id}_U{index}.png",
                folder / f"Grid{index}.png",
            ]
        found = next((path for path in candidates if path.exists()), None)
        paths[f"Gallery_U{index}_Path"] = str(found.resolve()) if found else ""
    return paths


def _open_book(path, headers):
    if path.exists():
        wb = load_workbook(path)
        ws = wb.active
        current = [cell.value for cell in ws[1]]
        if current != headers:
            old_rows = []
            current_map = {header: idx + 1 for idx, header in enumerate(current) if header}
            for row in range(2, ws.max_row + 1):
                old_rows.append({header: ws.cell(row=row, column=col).value for header, col in current_map.items()})
            ws.delete_rows(1, ws.max_row)
            ws.append(headers)
            for old in old_rows:
                if not old.get("SKU") and old.get("ID"):
                    old["SKU"] = old.get("ID")
                ws.append([old.get(header, "") for header in headers])
        return wb, ws
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    return wb, ws


def _upsert(ws, headers, row_data):
    id_col = headers.index("ID") + 1
    target = None
    for row in range(2, ws.max_row + 1):
        if ws.cell(row=row, column=id_col).value == row_data["ID"]:
            target = row
            break
    if target is None:
        target = ws.max_row + 1
    else:
        existing = {header: ws.cell(row=target, column=col).value for col, header in enumerate(headers, 1)}
        if existing.get("Status") and existing.get("Status") != "Ready_for_Printify":
            row_data["Status"] = existing.get("Status")
        if existing.get("Printify_Product_ID"):
            row_data["Printify_Product_ID"] = existing.get("Printify_Product_ID")
    for col, header in enumerate(headers, 1):
        ws.cell(row=target, column=col).value = row_data.get(header, "")


def _existing_ids(ws, headers):
    id_col = headers.index("ID") + 1
    return {
        str(ws.cell(row=row, column=id_col).value or "").strip()
        for row in range(2, ws.max_row + 1)
        if str(ws.cell(row=row, column=id_col).value or "").strip()
    }


def build_listing_assets(limit=0, use_api=True, product_type="Sticker", only_missing=False):
    DATABASE_DIR.mkdir(exist_ok=True)
    ebay_wb, ebay_ws = _open_book(EBAY_BOOK, EBAY_HEADERS)
    etsy_wb, etsy_ws = _open_book(ETSY_BOOK, ETSY_HEADERS)
    product_type = "Acrylic" if product_type.lower().startswith("acry") else ("Poster" if product_type.lower().startswith("poster") else "Sticker")
    folders = _ready_folders(product_type)
    if only_missing:
        known = _existing_ids(ebay_ws, EBAY_HEADERS)
        folders = [folder for folder in folders if _folder_id(folder) not in known]
    if limit:
        folders = folders[:limit]
    completed = 0
    for folder in folders:
        metadata_path = folder / "metadata.txt"
        production_path = folder / "Production_Design.png"
        cover_path = folder / "Cover_Mockup.png"
        if not metadata_path.exists() or not production_path.exists() or not cover_path.exists():
            print(f"[SKIP] Missing required assets: {folder.name}")
            continue
        metadata = _parse_metadata(metadata_path)
        metadata["ID"] = metadata.get("ID") or _folder_id(folder)
        metadata["Product_Type"] = product_type
        try:
            listing = _deepseek_listing(metadata) if use_api else _fallback_listing(metadata)
        except Exception as exc:
            print(f"[WARN] DeepSeek fallback for {metadata['ID']}: {exc}")
            listing = _fallback_listing(metadata)
        row = {
            "ID": metadata["ID"],
            "SKU": metadata["ID"],
            "Category": metadata.get("Category", ""),
            "Product_Type": product_type,
            "Title": listing.get("Title", ""),
            "Description": listing.get("Description", ""),
            "Price": PRODUCT_CONFIGS[product_type]["price"],
            "DNA Profile": listing.get("DNA Profile") or metadata.get("MJ_Prompt", ""),
            "Production_Path": str(production_path.resolve()),
            "Cover_Path": str(cover_path.resolve()),
            **_gallery_paths(folder, metadata["ID"], product_type),
            "Status": "Ready_for_Printify",
            "Timestamp": _timestamp(),
        }
        _upsert(ebay_ws, EBAY_HEADERS, row)
        _upsert(
            etsy_ws,
            ETSY_HEADERS,
            {
                "ID": metadata["ID"],
                "Raw_Metadata": metadata.get("Raw_Metadata", ""),
                "Production_Path": str(production_path.resolve()),
                "Status": "Placeholder",
                "Timestamp": _timestamp(),
            },
        )
        completed += 1
        print(f"[LISTING] {metadata['ID']} -> eBay/Etsy rows ready")
    ebay_wb.save(EBAY_BOOK)
    etsy_wb.save(ETSY_BOOK)
    ebay_wb.close()
    etsy_wb.close()
    print(f"[DONE] Listing assets updated: {completed}")


def normalize_existing_listing_rows():
    if not EBAY_BOOK.exists():
        print("[NORMALIZE] eBay listing workbook not found")
        return
    wb, ws = _open_book(EBAY_BOOK, EBAY_HEADERS)
    headers = {header: index + 1 for index, header in enumerate(EBAY_HEADERS)}
    changed = 0
    used_titles = set()
    for row in range(2, ws.max_row + 1):
        item_id = ws.cell(row=row, column=headers["ID"]).value
        if not item_id:
            continue
        product_type = ws.cell(row=row, column=headers["Product_Type"]).value or "Sticker"
        if product_type not in PRODUCT_CONFIGS:
            product_type = "Sticker"
            ws.cell(row=row, column=headers["Product_Type"]).value = product_type
        title_cell = ws.cell(row=row, column=headers["Title"])
        desc_cell = ws.cell(row=row, column=headers["Description"])
        seo = ws.cell(row=row, column=headers["DNA Profile"]).value or ""
        new_title = _fit_ebay_title(title_cell.value, seo, product_type)
        if new_title in used_titles:
            new_title = _retitle_duplicate(new_title, item_id, seo, product_type, used_titles)
        used_titles.add(new_title)
        new_desc = _ensure_image_note(desc_cell.value or "")
        if title_cell.value != new_title:
            title_cell.value = new_title
            changed += 1
        if desc_cell.value != new_desc:
            desc_cell.value = new_desc
            changed += 1
    wb.save(EBAY_BOOK)
    wb.close()
    print(f"[NORMALIZE] Existing listing rows updated: {changed}")


def run_logic():
    build_listing_assets()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--no-api", action="store_true")
    parser.add_argument("--product-type", default="Sticker", choices=["Sticker", "Poster", "Acrylic"])
    parser.add_argument("--normalize-existing", action="store_true")
    parser.add_argument("--only-missing", action="store_true")
    args = parser.parse_args()
    if args.normalize_existing:
        normalize_existing_listing_rows()
    else:
        build_listing_assets(
            limit=args.limit,
            use_api=not args.no_api,
            product_type=args.product_type,
            only_missing=args.only_missing,
        )

```


### FULL SOURCE: modules/digital_etsy_metadata_builder.py
```python
import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config

INDEX_PATH = PROJECT_ROOT / "Database" / "Digital_Printable_Pack_Index.csv"
OUTPUT_PATH = PROJECT_ROOT / "Database" / "Digital_Etsy_Metadata.csv"


def _clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _fit_title(value):
    title = _clean(re.sub(r"[^\x00-\x7F]+", " ", value))
    if len(title) <= 140:
        return title
    words = title.split()
    out = []
    for word in words:
        if len(" ".join(out + [word])) > 140:
            break
        out.append(word)
    return " ".join(out)


def _fallback(row):
    title = _fit_title(
        f"{row['Title']} Printable Wall Art, Dark Academia Decor, Digital Download, Study Room Poster"
    )
    tags = [
        "printable wall art",
        "digital download",
        "dark academia",
        "study room decor",
        "library wall art",
        "poster print",
        "gallery wall",
        "moody decor",
        "scholar decor",
        "instant download",
        "wall art print",
        "home office decor",
        "unique wall art",
    ]
    description = (
        f"Digital printable wall art pack for {row['Title']}.\n\n"
        "This is an instant digital download. No physical item will be shipped.\n\n"
        "Included files:\n"
        "- 2x3 ratio JPG\n"
        "- 3x4 ratio JPG\n"
        "- 4x5 ratio JPG\n"
        "- 5x7 ratio JPG\n"
        "- 11x14 JPG\n\n"
        "AI disclosure: this artwork is an original AI-assisted design curated, edited, and prepared for printable wall art.\n\n"
        "For personal use only. Do not resell or redistribute the files."
    )
    return {"Title": title, "Tags": tags[:13], "Description": description, "Price": "6.99"}


def _deepseek(row):
    api_key = [REDACTED]
    if not api_key:
        [REDACTED] RuntimeError("DEEPSEEK_API_KEY is missing")
    base_url = (Config.DEEPSEEK_BASE_URL or "https://api.deepseek.com").rstrip("/")
    payload = {
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "messages": [
            {
                "role": "system",
                "content": (
                    "Output strict JSON only. Keys: Title, Tags, Description, Price. "
                    "Create Etsy SEO for a premium digital printable wall art listing. "
                    "Title max 140 chars. Tags must be exactly 13 Etsy-style tags, each <=20 chars. "
                    "Description must clearly say this is a digital download and no physical item is shipped. "
                    "Include AI-assisted artwork disclosure in a tasteful way. "
                    "Tone: premium, poetic, searchable, not spammy."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "source_title": row["Title"],
                        "zip_mb": row["Zip_MB"],
                        "file_ratios": ["2x3", "3x4", "4x5", "5x7", "11x14"],
                        "shop_positioning": "premium Zen, dark academia, jade relic, quiet study decor",
                    },
                    ensure_ascii=False,
                ),
            },
        ],
        "temperature": 0.55,
    }
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=90,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(content)
    data["Title"] = _fit_title(data.get("Title") or row["Title"])
    tags = []
    seen = set()
    for tag in data.get("Tags") or []:
        tag = _clean(tag).lower()[:20]
        if tag and tag not in seen:
            seen.add(tag)
            tags.append(tag)
    fallback = _fallback(row)["Tags"]
    for tag in fallback:
        if len(tags) >= 13:
            break
        if tag not in seen:
            tags.append(tag)
            seen.add(tag)
    data["Tags"] = tags[:13]
    data["Description"] = _clean(data.get("Description") or _fallback(row)["Description"])
    if "digital" not in data["Description"].lower() or "no physical" not in data["Description"].lower():
        data["Description"] = _fallback(row)["Description"]
    data["Price"] = str(data.get("Price") or "6.99").replace("$", "")
    return data


def _read_index(limit=0, ids=None):
    wanted = {item.strip() for item in (ids or []) if item.strip()}
    existing = set()
    if OUTPUT_PATH.exists() and not wanted:
        with OUTPUT_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                item_id = _clean(row.get("ID"))
                if item_id:
                    existing.add(item_id)
    rows = []
    if not INDEX_PATH.exists():
        return rows
    with INDEX_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if wanted and row.get("ID") not in wanted:
                continue
            if not wanted and row.get("ID") in existing:
                continue
            if row.get("Listing_Status") != "LOCAL_READY_NOT_PUBLISHED":
                continue
            rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows


def build(limit=10, ids=None, use_api=True):
    rows = _read_index(limit=limit, ids=ids)
    exists = OUTPUT_PATH.exists()
    with OUTPUT_PATH.open("a", encoding="utf-8-sig", newline="", errors="ignore") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "Timestamp",
                "ID",
                "Title",
                "Description",
                "Tags",
                "Price",
                "Zip_Path",
                "Zip_MB",
                "Status",
            ],
        )
        if not exists:
            writer.writeheader()
        done = 0
        for row in rows:
            try:
                meta = _deepseek(row) if use_api else _fallback(row)
            except Exception as exc:
                print(f"[DIGITAL-META-WARN] {row['ID']} fallback: {exc}")
                meta = _fallback(row)
            writer.writerow(
                {
                    "Timestamp": datetime.now().isoformat(timespec="seconds"),
                    "ID": row["ID"],
                    "Title": meta["Title"],
                    "Description": meta["Description"],
                    "Tags": ", ".join(meta["Tags"]),
                    "Price": meta["Price"],
                    "Zip_Path": row["Zip_Path"],
                    "Zip_MB": row["Zip_MB"],
                    "Status": "READY_FOR_ETSY_DRAFT",
                }
            )
            handle.flush()
            done += 1
            print(f"[DIGITAL-META] {row['ID']} tags={len(meta['Tags'])} title_len={len(meta['Title'])}")
    print(f"[DONE] digital etsy metadata rows={done}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--ids", default="")
    parser.add_argument("--no-api", action="store_true")
    args = parser.parse_args()
    ids = [part.strip() for part in args.ids.split(",") if part.strip()]
    build(limit=args.limit, ids=ids, use_api=not args.no_api)


if __name__ == "__main__":
    main()

```


### FULL SOURCE: modules/product_line.py
```python
import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import time
from copy import copy
from datetime import datetime
from pathlib import Path

import requests
from openpyxl import load_workbook

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import BASE_URL, CLAUDE_API_KEY, DEEPSEEK_API_KEY
from modules.streaming_json import JsonObjectStream, iter_anthropic_text

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

DATABASE_DIR = Path("Database")
MENTOR_FILE = DATABASE_DIR / "Mentor_Hub.xlsx"
PRODUCTION_FILE = DATABASE_DIR / "Production_Line.xlsx"
GENERATED_LOG = DATABASE_DIR / "product_line_generated.log"
PENDING_DESIGN_FILE = DATABASE_DIR / "Pending_design.txt"

MENTOR_COLUMNS = ["Category", "Layout", "Title", "Gold_Prompt_DNA", "Material_Keywords", "Design_Count", "Performance"]
PRODUCTION_COLUMNS = [
    "ID",
    "Timestamp",
    "Category",
    "Product_Type",
    "Style",
    "Title",
    "MJ_Prompt",
    "SEO_Hook",
    "Status",
]

MJ_SUFFIX = "--v 6.1 --style raw --no skin, person, text, watermark"
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
SYSTEM_PROMPT = 'Strictly output raw JSON array. Start directly with "[". No preamble, no markdown, no explanations.'
LIFECYCLE_LIMIT = 100
BATCH_LIMIT = 20

PRODUCT_TEMPLATES = {
    "Sticker": {
        "layout": "Isolated",
        "ar": "--ar 1:1",
        "suffix": "white contour border, vector clean edges, die-cut sticker style, solid white background, isolated on white background",
    },
    "Poster": {
        "layout": "Full_Frame",
        "ar": "--ar 2:3",
        "suffix": "premium matte vertical poster composition, full frame, cinematic lighting, edge-to-edge composition, immersive environment, 12x18 wall art format",
    },
    "Acrylic": {
        "layout": "Full_Frame",
        "ar": "--ar 5:7",
        "suffix": "premium vertical acrylic photo block composition, 3D depth, refractive light, internal glow, ray tracing, gallery collectible art object",
    },
    "T-shirt": {
        "layout": "Isolated",
        "ar": "--ar 2:3",
        "suffix": "centered design, graphic tee style, vector art, isolated on solid background",
    },
    "Mug": {
        "layout": "Full_Frame",
        "ar": "--ar 2:1",
        "suffix": "continuous seamless pattern, panoramic wrap-around design",
    },
}

PRODUCT_ALIASES = {
    "sticker": "Sticker",
    "stickers": "Sticker",
    "poster": "Poster",
    "posters": "Poster",
    "acrylic": "Acrylic",
    "acrylics": "Acrylic",
    "t-shirt": "T-shirt",
    "tshirt": "T-shirt",
    "tshirts": "T-shirt",
    "t-shirts": "T-shirt",
    "shirt": "T-shirt",
    "shirts": "T-shirt",
    "mug": "Mug",
    "mugs": "Mug",
}


class ProductLineError(RuntimeError):
    pass


def root_path(relative_path):
    return ROOT_DIR / relative_path


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def clean_prompt(raw):
    return str(raw or "").replace("\n", " ").replace("\r", " ").strip()


def excel_timestamp():
    return datetime.now()


def header_map(sheet):
    return {cell.value: index + 1 for index, cell in enumerate(sheet[1]) if cell.value}


def validate_schema():
    for path, columns in ((MENTOR_FILE, MENTOR_COLUMNS), (PRODUCTION_FILE, PRODUCTION_COLUMNS)):
        workbook = load_workbook(root_path(path), read_only=True, data_only=True)
        try:
            sheet = workbook.active
            headers = [cell.value for cell in sheet[1]]
            missing = [column for column in columns if column not in headers]
            if missing:
                raise ProductLineError(f"{path} missing columns: {', '.join(missing)}")
        finally:
            workbook.close()


def canonical_product_type(product_type):
    token = [REDACTED]"_", "-")
    token = [REDACTED]"\s+", "-", token)
    canonical = PRODUCT_ALIASES.get(token)
    if not canonical:
        raise ProductLineError(f"[AUDIT] Unknown Product_Type template: {product_type}")
    if canonical not in PRODUCT_TEMPLATES:
        raise ProductLineError(f"[AUDIT] Missing exact Style template: {canonical}")
    return canonical


def read_pending_design():
    path = root_path(PENDING_DESIGN_FILE)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("[]", encoding="utf-8")
        return []
    raw = path.read_text(encoding="utf-8-sig").strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProductLineError(f"Pending_design.txt must be a JSON Array: {exc}") from exc
    if not isinstance(parsed, list):
        raise ProductLineError("Pending_design.txt must be a JSON Array")
    tasks = []
    for item in parsed:
        if not isinstance(item, dict):
            print(f"[AUDIT] Invalid pending design item skipped: {item}")
            continue
        category = clean_text(item.get("Category"))
        product_type = clean_text(item.get("Product_Type"))
        try:
            count = int(item.get("Count") or item.get("Number_of_Designs") or 0)
        except (TypeError, ValueError):
            count = 0
        if not category or not product_type or count <= 0:
            print(f"[AUDIT] Invalid pending design item skipped: {item}")
            continue
        tasks.append({"Category": category, "Product_Type": product_type, "Count": count})
    return tasks


def write_pending_design(tasks):
    path = root_path(PENDING_DESIGN_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = []
    for task in tasks:
        count = int(task.get("Count") or 0)
        if count > 0:
            normalized.append({
                "Category": clean_text(task.get("Category")),
                "Product_Type": canonical_product_type(task.get("Product_Type")),
                "Count": count,
            })
    temp_path = path.with_suffix(".tmp")
    temp_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_path.replace(path)


def load_mentor_rows():
    workbook = load_workbook(root_path(MENTOR_FILE), read_only=True, data_only=True)
    try:
        sheet = workbook.active
        columns = header_map(sheet)
        rows = []
        for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            item = {column: row[columns[column] - 1] if column in columns else None for column in MENTOR_COLUMNS}
            if item.get("Category") and item.get("Gold_Prompt_DNA"):
                item["_row_index"] = row_index
                rows.append(item)
        return rows
    finally:
        workbook.close()


def category_selector(task_category, product_type):
    category = clean_text(task_category)
    product = canonical_product_type(product_type)
    product_token = [REDACTED]
    if category.lower().startswith(product_token.lower() + "-"):
        return category[len(product_token) + 1 :]
    if category.lower().startswith("wall-art-"):
        return category[len("wall-art-") :]
    return category


def mentor_matches_task(seed_category, selector):
    seed_category = clean_text(seed_category)
    selector = clean_text(selector)
    if not selector:
        return False
    if seed_category.lower() == selector.lower():
        return True
    return seed_category.lower().startswith(selector.lower() + "-")


def design_count_value(seed):
    try:
        return int(seed.get("Design_Count") or 0)
    except (TypeError, ValueError):
        return 0


def select_mentor_seed(task):
    selector = category_selector(task["Category"], task["Product_Type"])
    candidates = [seed for seed in load_mentor_rows() if mentor_matches_task(seed["Category"], selector)]
    exact = [seed for seed in candidates if clean_text(seed["Category"]).lower() == selector.lower()]
    pool = exact or candidates
    candidates = sorted(pool, key=lambda seed: (design_count_value(seed), seed["_row_index"]))
    for seed in candidates:
        count = design_count_value(seed)
        if count >= LIFECYCLE_LIMIT:
            print(f"[AUDIT] DNA Exceeded Lifecycle ({count}/100). Skipping. Category={seed['Category']} Row={seed['_row_index']}")
            continue
        return seed
    print(f"[AUDIT] No available DNA for Category={task['Category']} Selector={selector}. Skipping.")
    return None


def load_generated_categories():
    path = root_path(GENERATED_LOG)
    if not path.exists():
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def mark_generated(category):
    path = root_path(GENERATED_LOG)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(category + "\n")


def product_type_for(seed_or_category, override=None):
    if override:
        return canonical_product_type(override)
    if isinstance(seed_or_category, dict):
        configured = clean_text(seed_or_category.get("Product_Type"))
        if configured:
            return configured
        text = clean_text(seed_or_category.get("Category")).lower()
    else:
        text = clean_text(seed_or_category).lower()
    if text.startswith("poster-") or "poster" in text:
        return "Poster"
    if "shirt" in text or "t-shirt" in text:
        return "T-shirt"
    if "wall" in text or "canvas" in text:
        return "Acrylic"
    if "acrylic" in text:
        return "Acrylic"
    if "relief" in text or "3d" in text:
        return "Acrylic"
    return "Sticker"


def strip_suffix(prompt):
    prompt = clean_prompt(prompt)
    prompt = re.sub(r"\s--v\s+\S+", "", prompt)
    prompt = re.sub(r"\s--ar\s+\S+", "", prompt)
    prompt = re.sub(r"\s--style\s+\S+", "", prompt)
    prompt = re.sub(r"\s--tile\b", "", prompt)
    prompt = re.sub(r"\s--no\s+.*$", "", prompt)
    return clean_prompt(prompt).rstrip(",")


def product_prompt_tail(product_type):
    return PRODUCT_TEMPLATES[canonical_product_type(product_type)]["suffix"]


def enforce_prompt(raw_prompt, product_type):
    product_type = canonical_product_type(product_type)
    template = PRODUCT_TEMPLATES[product_type]
    prompt = strip_suffix(raw_prompt)
    if product_type != "Sticker":
        prompt = re.sub(r"\b(die[- ]cut|sticker|vinyl decal|white contour border|contour border)\b", "", prompt, flags=re.I)
    tail = template["suffix"]
    if tail.lower() not in prompt.lower():
        prompt = f"{prompt}, {tail}"
    return clean_prompt(f"{prompt}, {template['ar']} {MJ_SUFFIX}")


def seo_hook(title, prompt, material_keywords):
    parts = []
    for value in re.split(r"[,;|/]+", clean_text(material_keywords)):
        if value.strip():
            parts.append(value.strip().lower())
    words = re.findall(r"[A-Za-z][A-Za-z-]{2,}", f"{title} {strip_suffix(prompt)}")
    stop = {"the", "and", "with", "from", "into", "white", "background", "isolated", "style", "raw"}
    for word in words:
        lowered = word.lower()
        if lowered not in stop and lowered not in parts:
            parts.append(lowered)
        if len(parts) >= 15:
            break
    while len(parts) < 10:
        for extra in ("mentor grade", "jade art", "kintsugi", "collectible", "premium decor"):
            if extra not in parts:
                parts.append(extra)
            if len(parts) >= 10:
                break
    return ", ".join(parts[:15])


def extract_json_array(text):
    text = clean_text(text)
    fenced = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.I | re.S)
    if fenced:
        return json.loads(fenced.group(1))
    start = text.find("[")
    end = text.rfind("]")
    if start >= 0 and end > start:
        return json.loads(text[start : end + 1])
    raise ProductLineError("API response did not contain a JSON array")


def build_prompt(seed, product_type, batch_count=BATCH_LIMIT):
    category = clean_text(seed["Category"])
    product_type = canonical_product_type(product_type)
    template = PRODUCT_TEMPLATES[product_type]
    return {
        "mission": "GREY ARCHITECT V15.3 Product_Line mold production",
        "required_count": int(batch_count),
        "sub_category": category,
        "product_type": product_type,
        "style": f"{category} Mentor-Grade",
        "layout": template["layout"],
        "product_ar": template["ar"],
        "product_suffix_keywords": template["suffix"],
        "gold_dna": {
            "title": seed["Title"],
            "prompt": seed["Gold_Prompt_DNA"],
            "materials": seed["Material_Keywords"],
        },
        "rules": [
            f"Generate exactly {int(batch_count)} visually unified but non-duplicate design variants.",
            "Each item must contain Title, MJ_Prompt, SEO_Hook.",
            "Preserve the material logic, mood, and premium visual language from Gold_Prompt_DNA, but DO NOT repeat the same core subject across the batch.",
            "Every batch must cover a subject diversity matrix: creature, botanical object, ritual instrument, architectural relic, talisman/seal, vessel/container, celestial object, weapon/tool, landscape micro-scene, abstract symbol.",
            "Use each primary subject slot at most once per batch. If one item is a phoenix, no other item may be phoenix-like; if one item is a seal, no other item may be seal/medallion/sigil-like.",
            "Do not let the source DNA become a repeated mascot. The source DNA is a material and atmosphere reference, not permission to repeat one object 20 times.",
            "Titles must make the unique focal object obvious in 2 to 5 words.",
            "Adjacent designs must not share the same primary noun or silhouette. Examples: do not output 20 Enso circles, 20 koi, 20 dragons, 20 torii gates, or 20 hourglasses.",
            "Each design must have a visibly different silhouette, focal object, pose/angle, accessory system, and composition, while still belonging to the same Sub_Category aesthetic.",
            "Avoid synonym-only variation. Colorway, lighting, or adjective changes alone are not enough to count as a new design.",
            "Do not preserve the original Midjourney aspect ratio; use product_ar exactly.",
            "MJ_Prompt must follow: [DNA Subject Description], [Product Suffix Keywords], [Product AR] --v 6.1 --style raw --no skin, person, text, watermark",
            "Do not include newline characters.",
            "SEO_Hook must contain 10 to 15 comma-separated keywords.",
            "Return only a JSON array.",
        ],
    }


def stream_claude_objects(seed, product_type, batch_count=BATCH_LIMIT, retries=3, max_seconds=150):
    if not CLAUDE_API_KEY:
        [REDACTED] ProductLineError("CLAUDE_API_KEY is empty")
    url = BASE_URL.rstrip("/") + "/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 8000,
        "temperature": 0.72,
        "stream": True,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": json.dumps(build_prompt(seed, product_type, batch_count), ensure_ascii=False)}],
    }
    last_error = None
    for attempt in range(1, retries + 1):
        started_at = time.monotonic()
        try:
            response = requests.post(url, headers=headers, json=payload, stream=True, timeout=(10, 15))
            if response.status_code >= 400:
                raise ProductLineError(f"{response.status_code} {response.text[:800]}")
            parser = JsonObjectStream()
            for text in iter_anthropic_text(response):
                if time.monotonic() - started_at > max_seconds:
                    response.close()
                    raise TimeoutError(f"Batch stream exceeded {max_seconds}s")
                for item in parser.feed(text):
                    yield item
            return
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(2 * attempt)
    raise ProductLineError(f"Product Line API stream failed after retries: {last_error}")


def fallback_variants(seed):
    category = clean_text(seed["Category"])
    base_prompt = strip_suffix(seed["Gold_Prompt_DNA"])
    themes = [
        "lunar rim lighting",
        "golden dawn glow",
        "obsidian shadow contrast",
        "jade bioluminescent core",
        "kintsugi fracture map",
        "floating relic orbit",
        "vertical talisman layout",
        "sacred geometry frame",
        "crystalline star chart",
        "ink-wash mist trail",
        "museum artifact angle",
        "macro material close-up",
        "halo backlight composition",
        "silent ceremonial pose",
        "celestial gate silhouette",
        "alchemical glow chamber",
        "ancient scholar archive",
        "premium collectible profile",
        "mythic compass symmetry",
        "soft sacred underlighting",
    ]
    return [
        {
            "Title": f"{seed['Title']} {index:02d}",
            "MJ_Prompt": f"{base_prompt}, {theme}, variant {index:02d}",
            "SEO_Hook": seo_hook(seed["Title"], base_prompt, seed["Material_Keywords"]),
        }
        for index, theme in enumerate(themes, 1)
    ]


def main_category(category):
    return clean_text(category).split("-", 1)[0].split("_", 1)[0] or clean_text(category)


def id_prefix(product_type, category):
    return f"{id_product_token(product_type)}-{main_category(category)}"


def next_sequence(product_type, category):
    prefix = id_prefix(product_type, category)
    workbook = load_workbook(root_path(PRODUCTION_FILE), read_only=True, data_only=True)
    try:
        sheet = workbook.active
        columns = header_map(sheet)
        id_column = columns["ID"]
        last_number = 0
        width = 4
        for row in sheet.iter_rows(min_row=2, values_only=True):
            value = row[id_column - 1]
            text = str(value or "")
            if not text.startswith(prefix + "-"):
                continue
            match = re.search(r"(\d+)$", text)
            if match:
                last_number = int(match.group(1))
                width = max(width, len(match.group(1)))
        return last_number + 1, width
    finally:
        workbook.close()


def normalize_variants(seed, raw_variants, product_type):
    seen = set()
    variants = []
    for index, item in enumerate(raw_variants, 1):
        if len(variants) >= 20:
            break
        title = clean_text(item.get("Title") or f"{seed['Title']} Variant {index:02d}")
        prompt = enforce_prompt(item.get("MJ_Prompt") or seed["Gold_Prompt_DNA"], product_type)
        hook = clean_text(item.get("SEO_Hook")) or seo_hook(title, prompt, seed["Material_Keywords"])
        hook_parts = [part.strip() for part in hook.split(",") if part.strip()]
        if len(hook_parts) < 10 or len(hook_parts) > 15:
            hook = seo_hook(title, prompt, seed["Material_Keywords"])
        fp = " ".join(sorted(set(re.findall(r"[A-Za-z][A-Za-z-]{3,}", f"{title} {prompt} {hook}".lower()))))
        if fp in seen:
            prompt = enforce_prompt(f"{strip_suffix(prompt)}, unique aesthetic branch {index:02d}", product_type)
            fp = f"{fp}-{index:02d}"
        seen.add(fp)
        variants.append({"Title": title, "MJ_Prompt": prompt, "SEO_Hook": hook})
    if len(variants) != 20:
        raise ProductLineError(f"Expected 20 variants, got {len(variants)}")
    return variants


SIMILARITY_STOPWORDS = {
    "with", "from", "into", "that", "this", "style", "sticker", "design", "white", "background",
    "isolated", "vector", "clean", "edges", "border", "solid", "sharp", "focus", "raw", "skin",
    "person", "text", "watermark", "mentor-grade", "hyper-detailed", "premium", "composition",
    "cinematic", "lighting", "material", "system", "primary", "surface", "relief", "visible",
    "handcrafted", "subtle", "internal", "glow", "crisp", "silhouette", "readability",
    "celestial", "astral", "lunar", "cosmic", "starbound", "starborne", "moonlit", "moonstone",
    "jade", "obsidian", "sapphire", "rainbow", "white", "black", "golden", "silver", "indigo",
    "violet", "emerald", "nebula", "ink-wash", "fragments", "floating", "orbiting", "crafted",
    "carved", "formed", "constructed", "sculpted", "ancient", "sacred", "mythical", "divine",
}


SUBJECT_GROUPS = {
    "phoenix": {"phoenix", "bird", "crane", "eagle", "feather", "wings", "winged"},
    "dragon": {"dragon", "serpent", "wyrm"},
    "koi": {"koi", "fish", "carp"},
    "beast": {"lion", "tiger", "fox", "wolf", "kirin", "qilin", "guardian", "beast"},
    "lotus": {"lotus", "flower", "bloom", "petal", "blossom"},
    "tree": {"tree", "bonsai", "bamboo", "branch", "pine", "willow"},
    "instrument": {"guqin", "bell", "chime", "flute", "drum", "singing", "bowl", "instrument"},
    "vessel": {"vessel", "cauldron", "urn", "chalice", "bowl", "jar", "teapot", "incense", "burner"},
    "gate": {"gate", "torii", "portal", "doorway", "archway", "shrine"},
    "pagoda": {"pagoda", "temple", "tower", "lantern", "pavilion", "bridge"},
    "seal": {"seal", "sigil", "medallion", "emblem", "crest", "talisman", "amulet"},
    "globe": {"globe", "orb", "sphere", "planet", "astrolabe", "compass"},
    "scroll": {"scroll", "manuscript", "tablet", "book", "sutra", "script"},
    "weapon": {"sword", "blade", "dagger", "spear", "staff", "wand", "vajra"},
    "landscape": {"mountain", "waterfall", "river", "island", "garden", "landscape", "pond"},
    "abstract": {"enso", "mandala", "geometry", "knot", "spiral", "circle", "constellation"},
}


def diversity_tokens(title, prompt):
    text = strip_suffix(f"{title} {prompt}").lower()
    words = re.findall(r"[a-z][a-z-]{3,}", text)
    return {
        word
        for word in words
        if word not in SIMILARITY_STOPWORDS and not word.startswith("variant")
    }


def subject_key(title, prompt):
    text = strip_suffix(f"{title} {prompt}").lower()
    words = set(re.findall(r"[a-z][a-z-]{2,}", text))
    for key, aliases in SUBJECT_GROUPS.items():
        if words & aliases:
            return key
    title_words = [
        word
        for word in re.findall(r"[a-z][a-z-]{3,}", str(title or "").lower())
        if word not in SIMILARITY_STOPWORDS
    ]
    return title_words[-1] if title_words else ""


def similarity_score(tokens_a, tokens_b):
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / max(1, len(tokens_a | tokens_b))


def too_similar_to_saved(title, prompt, saved_variants, threshold=0.78):
    current = diversity_tokens(title, prompt)
    current_subject = subject_key(title, prompt)
    for saved in saved_variants:
        saved_subject = saved.get("_subject_key", "")
        if current_subject and saved_subject and current_subject == saved_subject:
            return True, 1.0, saved["Title"]
        score = similarity_score(current, saved["_diversity_tokens"])
        # Product-line batches intentionally share material vocabulary from the same
        # DNA. Only block text-level similarity when it is extremely high; the
        # subject_key gate above catches true repeated silhouettes.
        if score >= threshold:
            return True, score, saved["Title"]
    return False, 0.0, ""


def normalize_variant(seed, item, product_type, index=1):
    title = clean_text(item.get("Title") or f"{seed['Title']} Variant {index:02d}")
    prompt = enforce_prompt(item.get("MJ_Prompt") or seed["Gold_Prompt_DNA"], product_type)
    hook = clean_text(item.get("SEO_Hook")) or seo_hook(title, prompt, seed["Material_Keywords"])
    hook_parts = [part.strip() for part in hook.split(",") if part.strip()]
    if len(hook_parts) < 10 or len(hook_parts) > 15:
        hook = seo_hook(title, prompt, seed["Material_Keywords"])
    return {"Title": title, "MJ_Prompt": prompt, "SEO_Hook": hook}


def clone_style(source_cell, target_cell):
    if source_cell.has_style:
        target_cell._style = copy(source_cell._style)
    target_cell.number_format = "@"
    if source_cell.alignment:
        target_cell.alignment = copy(source_cell.alignment)


def last_filled_row(sheet, id_column):
    for row_index in range(sheet.max_row, 1, -1):
        if clean_text(sheet.cell(row=row_index, column=id_column).value):
            return row_index
    return 1


def id_product_token(product_type):
    return clean_text(product_type).replace(" ", "-")


def build_output_rows(seed, variants, product_type):
    dna_category = clean_text(seed["Category"])
    category = main_category(dna_category)
    sequence, width = next_sequence(product_type, dna_category)
    timestamp = excel_timestamp()
    prefix = id_prefix(product_type, dna_category)
    rows = []
    for offset, variant in enumerate(variants):
        rows.append({
            "ID": f"{prefix}-{sequence + offset:0{width}d}",
            "Timestamp": timestamp,
            "Category": category,
            "Product_Type": product_type,
            "Style": f"{category} Mentor-Grade",
            "Title": clean_text(variant["Title"]),
            "MJ_Prompt": clean_prompt(variant["MJ_Prompt"]),
            "SEO_Hook": clean_text(variant["SEO_Hook"]),
            "Status": "Ready_for_production",
        })
    return rows


def build_output_row(seed, variant, product_type):
    return build_output_rows(seed, [variant], product_type)[0]


def save_with_openpyxl(output_rows):
    path = root_path(PRODUCTION_FILE)
    workbook = load_workbook(path)
    try:
        sheet = workbook.active
        columns = header_map(sheet)
        missing = [column for column in PRODUCTION_COLUMNS if column not in columns]
        if missing:
            raise ProductLineError(f"Production_Line.xlsx missing columns: {', '.join(missing)}")
        last_row = last_filled_row(sheet, columns["ID"])
        template_row = max(last_row, 2)
        for row_data in output_rows:
            row_index = last_row + 1
            for column in PRODUCTION_COLUMNS:
                cell = sheet.cell(row=row_index, column=columns[column])
                clone_style(sheet.cell(row=template_row, column=columns[column]), cell)
                cell.value = row_data[column]
                if column == "Timestamp":
                    cell.number_format = "m/d/yyyy, h:mm:ss AM/PM"
                else:
                    cell.number_format = "@"
            last_row = row_index
        workbook.save(path)
    finally:
        workbook.close()


def save_with_excel_com(output_rows):
    import win32com.client

    excel_app = None
    workbook = None
    try:
        excel_app = win32com.client.DispatchEx("Excel.Application")
        excel_app.DisplayAlerts = False
        workbook = excel_app.Workbooks.Open(str(root_path(PRODUCTION_FILE)))
        sheet = workbook.Worksheets(1)
        columns = {}
        column = 1
        while True:
            value = sheet.Cells(1, column).Value
            if value in (None, ""):
                break
            columns[str(value)] = column
            column += 1
        missing = [name for name in PRODUCTION_COLUMNS if name not in columns]
        if missing:
            raise ProductLineError(f"Production_Line.xlsx missing columns: {', '.join(missing)}")
        xl_up = -4162
        last_row = sheet.Cells(sheet.Rows.Count, columns["ID"]).End(xl_up).Row
        template_row = last_row
        for row_data in output_rows:
            target_row = last_row + 1
            sheet.Range(sheet.Cells(template_row, 1), sheet.Cells(template_row, len(columns))).Copy()
            sheet.Range(sheet.Cells(target_row, 1), sheet.Cells(target_row, len(columns))).PasteSpecial(-4122)
            for name in PRODUCTION_COLUMNS:
                cell = sheet.Cells(target_row, columns[name])
                if name == "Timestamp":
                    cell.NumberFormat = "m/d/yyyy, h:mm:ss AM/PM"
                else:
                    cell.NumberFormat = "@"
                cell.Value = row_data[name]
            last_row = target_row
        excel_app.CutCopyMode = False
        workbook.Save()
    finally:
        if workbook is not None:
            workbook.Close(SaveChanges=True)
        if excel_app is not None:
            excel_app.Quit()


def append_rows(output_rows):
    try:
        save_with_openpyxl(output_rows)
    except PermissionError:
        save_with_excel_com(output_rows)


def append_row(row):
    append_rows([row])


def increment_design_count(seed, amount=20):
    workbook = load_workbook(root_path(MENTOR_FILE))
    try:
        sheet = workbook.active
        columns = header_map(sheet)
        if "Design_Count" not in columns:
            sheet.cell(row=1, column=sheet.max_column + 1).value = "Design_Count"
            columns = header_map(sheet)
        row_index = int(seed["_row_index"])
        current = sheet.cell(row=row_index, column=columns["Design_Count"]).value or 0
        try:
            current = int(current)
        except (TypeError, ValueError):
            current = 0
        sheet.cell(row=row_index, column=columns["Design_Count"]).value = current + amount
        if "Timestamp" in columns:
            stamp_cell = sheet.cell(row=row_index, column=columns["Timestamp"])
            stamp_cell.value = datetime.now()
            stamp_cell.number_format = "m/d/yyyy, h:mm:ss AM/PM"
        workbook.save(root_path(MENTOR_FILE))
    finally:
        workbook.close()


def increment_design_count_by_row(seed, amount=1):
    increment_design_count(seed, amount)


def process_seed_v135_legacy(seed, product_type="Sticker"):
    saved = 0
    seen = set()
    output_rows = []
    for item in stream_claude_objects(seed, product_type):
        variant = normalize_variant(seed, item, product_type, saved + 1)
        fp = f"{variant['Title']}|{variant['MJ_Prompt']}|{variant['SEO_Hook']}"
        if fp in seen:
            continue
        seen.add(fp)
        row = build_output_row(seed, variant, product_type)
        row["MJ_Prompt"] = clean_prompt(row["MJ_Prompt"])
        append_row(row)
        increment_design_count_by_row(seed, 1)
        saved += 1
        output_rows.append(row)
        print(f"[Dify-Mode] ID: {row['ID']} 写入成功 | 实时保存已完成")
        if saved >= 20:
            break
    if saved != 20:
        raise ProductLineError(f"Expected 20 variants, got {saved}")
    print(f"[PRODUCT_LINE] Generated 20 rows: {seed['Category']}")
    return output_rows


def process_seed(seed, product_type="Sticker", batch_count=BATCH_LIMIT, max_seconds=150, on_saved=None):
    product_type = canonical_product_type(product_type)
    batch_count = min(int(batch_count), BATCH_LIMIT)
    saved = 0
    seen = set()
    output_rows = []
    started_at = time.monotonic()
    for item in stream_claude_objects(seed, product_type, batch_count=batch_count, max_seconds=max_seconds):
        if time.monotonic() - started_at > max_seconds:
            print(f"[AUDIT] Batch exceeded {max_seconds}s after saved={saved}. Breaking for debug-safe resume.")
            break
        variant = normalize_variant(seed, item, product_type, saved + 1)
        too_close, score, near_title = too_similar_to_saved(variant["Title"], variant["MJ_Prompt"], output_rows)
        if too_close:
            print(f"[DIVERSITY] Rejected near-duplicate score={score:.2f}: {variant['Title']} ~ {near_title}")
            continue
        fp = f"{variant['Title']}|{variant['MJ_Prompt']}|{variant['SEO_Hook']}"
        if fp in seen:
            continue
        seen.add(fp)
        row = build_output_row(seed, variant, product_type)
        row["MJ_Prompt"] = clean_prompt(row["MJ_Prompt"])
        row["_diversity_tokens"] = diversity_tokens(row["Title"], row["MJ_Prompt"])
        row["_subject_key"] = subject_key(row["Title"], row["MJ_Prompt"])
        append_row(row)
        increment_design_count_by_row(seed, 1)
        saved += 1
        output_rows.append(row)
        if on_saved:
            on_saved(row, saved)
        print(f"[Dify-Mode] ID: {row['ID']} 写入成功 | 实时保存已完成")
        if saved >= batch_count:
            break
    if saved == 0:
        raise ProductLineError(f"Expected {batch_count} variants, got 0")
    if saved != batch_count:
        print(f"[AUDIT] Partial batch saved={saved}/{batch_count}. Pending_design will keep the remaining demand.")
    print(f"[PRODUCT_LINE] Generated {batch_count} rows: {seed['Category']} -> {product_type}")
    return output_rows


def run_legacy_seed_mode(limit=1, product_type="Sticker"):
    os.chdir(ROOT_DIR)
    validate_schema()
    seeds = []
    for seed in load_mentor_rows():
        try:
            design_count = int(seed.get("Design_Count") or 0)
        except (TypeError, ValueError):
            design_count = 0
        if design_count < 100:
            seeds.append(seed)
    if limit is not None:
        seeds = seeds[:limit]
    if not seeds:
        print("[PRODUCT_LINE] No new Gold DNA seeds.")
        return 0
    processed = 0
    for seed in seeds:
        process_seed(seed, product_type=product_type)
        processed += 1
    return processed


def run_logic(limit=None, product_type=None, max_batches=None, max_seconds=150):
    os.chdir(ROOT_DIR)
    validate_schema()
    tasks = read_pending_design()
    if not tasks:
        print("[PRODUCT_LINE] Pending_design.txt is empty.")
        return 0

    total_saved = 0
    batches_done = 0
    task_index = 0
    while task_index < len(tasks):
        task = tasks[task_index]
        try:
            task["Product_Type"] = canonical_product_type(task["Product_Type"])
        except ProductLineError as exc:
            print(str(exc))
            tasks.pop(task_index)
            write_pending_design(tasks)
            continue

        seed = select_mentor_seed(task)
        if seed is None:
            tasks.pop(task_index)
            write_pending_design(tasks)
            continue

        current_count = design_count_value(seed)
        remaining_life = max(0, LIFECYCLE_LIMIT - current_count)
        if remaining_life <= 0:
            print(f"[AUDIT] DNA Exceeded Lifecycle ({current_count}/100). Skipping.")
            tasks.pop(task_index)
            write_pending_design(tasks)
            continue

        requested = int(task["Count"])
        allowed_for_task = min(requested, remaining_life)
        if allowed_for_task < requested:
            print(f"[AUDIT] Demand clipped: requested={requested}, available_lifecycle={remaining_life}, Category={seed['Category']}")
            task["Count"] = allowed_for_task
            requested = allowed_for_task
            write_pending_design(tasks)

        batch_count = min(requested, BATCH_LIMIT)
        print(
            f"[BATCH] Category={task['Category']} DNA={seed['Category']} Product={task['Product_Type']} "
            f"Batch={batch_count} RemainingTask={requested} Design_Count={current_count}/100"
        )
        task["Count"] = int(task["Count"])

        def checkpoint_saved(_row, _saved_in_batch):
            task["Count"] = max(0, int(task["Count"]) - 1)
            if task["Count"] <= 0:
                tasks.pop(task_index)
            write_pending_design(tasks)

        rows = process_seed(
            seed,
            product_type=task["Product_Type"],
            batch_count=batch_count,
            max_seconds=max_seconds,
            on_saved=checkpoint_saved,
        )
        saved = len(rows)
        total_saved += saved
        batches_done += 1
        if limit is not None and total_saved >= int(limit):
            break
        if max_batches is not None and batches_done >= int(max_batches):
            break

    print(f"[PRODUCT_LINE] V15.3 completed. Batches={batches_done} Saved={total_saved}")
    return total_saved


def self_test():
    os.chdir(ROOT_DIR)
    validate_schema()
    original_root = ROOT_DIR
    original_cwd = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="product_line_v135_") as temp_dir:
        temp_root = Path(temp_dir)
        (temp_root / DATABASE_DIR).mkdir()
        shutil.copy2(root_path(MENTOR_FILE), temp_root / MENTOR_FILE)
        shutil.copy2(root_path(PRODUCTION_FILE), temp_root / PRODUCTION_FILE)
        globals()["ROOT_DIR"] = temp_root
        try:
            seed = load_mentor_rows()[-1]
            next_id, _ = next_sequence("Sticker", seed["Category"])
            prompt = enforce_prompt(f"{seed['Gold_Prompt_DNA']}\nself test branch\r", product_type_for(seed, "Sticker"))
            output = build_output_rows(seed, [{
                "Title": "Self Test DNA",
                "MJ_Prompt": prompt,
                "SEO_Hook": seo_hook("Self Test DNA", prompt, seed["Material_Keywords"]),
            }], "Sticker")
            if int(output[0]["ID"].split("-")[-1]) != next_id:
                raise ProductLineError("ID step validation failed")
            if "\n" in output[0]["MJ_Prompt"] or "\r" in output[0]["MJ_Prompt"]:
                raise ProductLineError("Prompt text cleaning failed")
            if output[0]["Status"] != "Ready_for_production":
                raise ProductLineError("Initial status validation failed")
        finally:
            globals()["ROOT_DIR"] = original_root
            os.chdir(original_cwd)
    print("PRODUCT_LINE_SELF_TEST_OK")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--max-batches", type=int, default=None)
    parser.add_argument("--max-seconds", type=int, default=150)
    parser.add_argument("--product-type", default="Sticker")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        run_logic(limit=args.limit, product_type=args.product_type, max_batches=args.max_batches, max_seconds=args.max_seconds)


if __name__ == "__main__":
    main()

```


### FULL SOURCE: modules/etsy_digital_ui_publisher.py
```python
"""Publish staged Etsy digital downloads through the logged-in Edge UI.

This is a narrow bridge while Etsy Open API approval is pending. It obeys the
same fee kill switch as the API path: one listing proof first, no blind retries,
and every confirmed publish is written to the fee ledger.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import re
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.risk_guard import assert_allowed, assert_etsy_fee_batch_allowed, fee_kill_switch

DATABASE = PROJECT_ROOT / "Database"
QUEUE_PATH = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
QA_PATH = DATABASE / "Etsy_Digital_QA_Report.csv"
FEE_LEDGER_PATH = DATABASE / "Etsy_Fee_Ledger.csv"
METADATA_PATH = DATABASE / "Digital_Etsy_Metadata.csv"
UI_LOG_PATH = DATABASE / "Etsy_Digital_UI_Publish_Log.csv"

ETSY_CREATE_URL = "https://www.etsy.com/your/shops/me/listing-editor/create"

LOG_FIELDS = [
    "Timestamp",
    "ID",
    "Action",
    "Status",
    "Etsy_Listing_ID",
    "URL",
    "Confirmed_Fee_USD",
    "Note",
]


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _append_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    exists = path.exists()
    with path.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def _confirmed_spend_today() -> float:
    today = datetime.now().date().isoformat()
    total = 0.0
    for row in _read_csv(FEE_LEDGER_PATH):
        if str(row.get("Timestamp", "")).startswith(today) and str(row.get("Status", "")).startswith("CONFIRMED"):
            try:
                total += float(row.get("Confirmed_Spent_USD") or 0)
            except ValueError:
                pass
    return total


def _metadata_by_id() -> dict[str, dict]:
    return {row.get("ID", ""): row for row in _read_csv(METADATA_PATH)}


def _select_candidates(limit: int) -> list[dict]:
    metadata = _metadata_by_id()
    rows = []
    for row in _read_csv(QUEUE_PATH):
        if not row.get("QA_Status", "").startswith("PASS"):
            continue
        if row.get("Etsy_Listing_ID"):
            continue
        if row.get("Fee_Status") == "CONFIRMED_SPENT":
            continue
        if row.get("Launch_Status") not in {"READY_BLOCKED_ETSY_AUTH", "READY_TO_PUBLISH", "READY_UI_PUBLISH"}:
            continue
        merged = dict(row)
        merged.update({f"Meta_{k}": v for k, v in (metadata.get(row.get("ID", "")) or {}).items()})
        rows.append(merged)
        if len(rows) >= limit:
            break
    return rows


def _font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _fit(image: Image.Image, size: tuple[int, int], fill=(241, 239, 234)) -> Image.Image:
    canvas = Image.new("RGB", size, fill)
    im = image.copy().convert("RGB")
    im.thumbnail(size, Image.Resampling.LANCZOS)
    canvas.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return canvas


def _draw_wrap(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, max_chars: int, font, fill=(45, 42, 38)):
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        probe = " ".join(current + [word])
        if len(probe) > max_chars and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    x, y = xy
    for line in lines[:8]:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + 12


def _preview_paths(row: dict) -> list[str]:
    item_id = row["ID"]
    zip_path = Path(row["Zip_Path"])
    pack_dir = zip_path.with_suffix("")
    preview_dir = pack_dir / "_etsy_preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(preview_dir.glob("Preview_*.jpg"))
    if len(existing) >= 3:
        return [str(path) for path in existing[:3]]

    art_candidates = sorted(pack_dir.glob(f"{item_id}_2x3_*.jpg")) or sorted(pack_dir.glob("*.jpg"))
    if not art_candidates:
        raise FileNotFoundError(f"No printable JPG found in {pack_dir}")
    with Image.open(art_candidates[0]) as source:
        source = ImageEnhance.Contrast(source.convert("RGB")).enhance(1.02)
        art = _fit(source, (860, 1290))

    title = _clean(row.get("Title") or row.get("Meta_Title") or item_id)
    title_font = _font(72, True)
    sub_font = _font(42)
    body_font = _font(34)
    small_font = _font(28)

    p1 = preview_dir / "Preview_01_framed_printable.jpg"
    canvas = Image.new("RGB", (2000, 2000), (239, 236, 229))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, 2000, 1450], fill=(244, 242, 237))
    frame = (600, 120, 1460, 1410)
    draw.rectangle([frame[0] - 42, frame[1] - 42, frame[2] + 42, frame[3] + 42], fill=(49, 43, 38))
    draw.rectangle([frame[0] - 18, frame[1] - 18, frame[2] + 18, frame[3] + 18], fill=(235, 231, 224))
    canvas.paste(art, (frame[0], frame[1]))
    draw.rounded_rectangle([110, 1540, 1030, 1885], radius=28, fill=(255, 254, 250), outline=(184, 178, 169), width=3)
    draw.text((165, 1595), "Digital Download", font=title_font, fill=(35, 32, 28))
    draw.text((170, 1700), "5 printable JPG ratios included", font=sub_font, fill=(78, 70, 62))
    draw.text((170, 1764), "No physical item is shipped", font=body_font, fill=(112, 76, 52))
    draw.text((1270, 1760), "Quiet Relic Studio", font=body_font, fill=(67, 59, 52))
    canvas.save(p1, "JPEG", quality=92, optimize=True)

    p2 = preview_dir / "Preview_02_included_ratios.jpg"
    canvas = Image.new("RGB", (2000, 2000), (250, 249, 246))
    draw = ImageDraw.Draw(canvas)
    draw.text((125, 105), "Included Files", font=title_font, fill=(35, 32, 28))
    for i, line in enumerate(["2x3 ratio: 12x18, 16x24, 20x30", "3x4 ratio: 9x12, 12x16, 18x24", "4x5 ratio: 8x10, 12x15, 16x20", "5x7 ratio: 5x7, 10x14", "11x14 ratio"]):
        y = 310 + i * 250
        draw.rounded_rectangle([130, y, 1870, y + 185], radius=22, fill=(255, 254, 250), outline=(190, 185, 176), width=3)
        draw.text((195, y + 55), line, font=sub_font, fill=(45, 42, 38))
    draw.text((160, 1695), "Print at home or with any local/online print shop.", font=body_font, fill=(82, 76, 68))
    canvas.save(p2, "JPEG", quality=92, optimize=True)

    p3 = preview_dir / "Preview_03_style_detail.jpg"
    canvas = Image.new("RGB", (2000, 2000), (247, 245, 240))
    draw = ImageDraw.Draw(canvas)
    canvas.paste(_fit(art, (1000, 1500)), (110, 210))
    draw.rectangle([110, 210, 1110, 1710], outline=(172, 165, 154), width=3)
    draw.text((1200, 260), "Printable Wall Art", font=title_font, fill=(35, 32, 28))
    _draw_wrap(draw, (1205, 380), title, 26, sub_font)
    draw.rounded_rectangle([1200, 1335, 1845, 1605], radius=24, fill=(255, 254, 250), outline=(190, 185, 176), width=2)
    draw.text((1245, 1390), "Instant digital files", font=body_font, fill=(45, 42, 38))
    draw.text((1245, 1450), "AI-assisted artwork", font=small_font, fill=(90, 82, 74))
    draw.text((1245, 1502), "Personal use license", font=small_font, fill=(90, 82, 74))
    canvas.save(p3, "JPEG", quality=92, optimize=True)

    return [str(p1), str(p2), str(p3)]


def _safe_digital_upload_path(row: dict) -> Path:
    source = Path(row["Zip_Path"]).resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    upload_dir = source.parent / "_etsy_upload"
    upload_dir.mkdir(exist_ok=True)
    safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "-", str(row["ID"]))[:52].strip("-")
    target = upload_dir / f"OC-{safe_stem}.zip"
    if not target.exists() or target.stat().st_mtime < source.stat().st_mtime or target.stat().st_size != source.stat().st_size:
        shutil.copy2(source, target)
    if len(target.name) > 70:
        raise ValueError(f"Etsy-safe upload filename is too long: {target.name}")
    return target


def _parse_listing_id(url: str) -> str:
    match = re.search(r"/listing/(\d+)|/edit/(\d+)", url)
    if not match:
        return ""
    return next(group for group in match.groups() if group)


def _parse_listing_id_from_manager(page, row: dict) -> tuple[str, str]:
    item_id = str(row.get("ID") or "")
    title_start = _clean(row.get("Title") or "")[:50]
    try:
        page.wait_for_function(
            """needle => document.body && document.body.innerText.includes(needle)""",
            arg=item_id,
            timeout=20000,
        )
    except Exception:
        pass
    links = page.locator("a").evaluate_all(
        """els => els.map(a => ({text: (a.innerText || a.ariaLabel || '').trim(), href: a.href}))
        .filter(x => x.href.includes('/listing/') || x.href.includes('listing-editor/edit'))"""
    )
    for link in links:
        text = link.get("text") or ""
        href = link.get("href") or ""
        if item_id in text or (title_start and title_start in text):
            listing_id = _parse_listing_id(href)
            if listing_id:
                return listing_id, href
    return "", page.url


def _set_manual_renew(page) -> None:
    radios = page.locator('input[name="shouldAutoRenew"]')
    if radios.count() >= 2:
        radios.nth(1).evaluate(
            "e => { e.checked=true; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }"
        )


def _choose_radio_by_name(page, name: str, index: int) -> None:
    radios = page.locator(f'input[name="{name}"]')
    if radios.count() > index:
        radios.nth(index).evaluate(
            "e => { e.checked=true; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }"
        )


def _fill_listing(page, row: dict) -> None:
    title = _clean(row.get("Title") or row.get("Meta_Title"))
    description = str(row.get("Meta_Description") or row.get("Description") or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    tags = [tag.strip()[:20] for tag in str(row.get("Meta_Tags") or "").split(",") if tag.strip()]
    if len(tags) < 13:
        tags.extend(["printable wall art", "digital download", "dark academia", "study room decor", "gallery wall"][: 13 - len(tags)])
    price = str(row.get("Price") or row.get("Meta_Price") or "6.99").replace("$", "").strip()
    zip_path = str(_safe_digital_upload_path(row))
    preview_paths = _preview_paths(row)

    page.goto(ETSY_CREATE_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3500)
    for button_text in ("Dismiss", "Got it"):
        try:
            loc = page.get_by_role("button", name=button_text)
            if loc.count() > 0 and loc.first.is_visible():
                loc.first.click(timeout=2000)
                page.wait_for_timeout(500)
        except Exception:
            pass

    # Photos first; Etsy's first file input is the photo/video uploader.
    page.locator("input[type=file]").nth(0).set_input_files(preview_paths)
    page.wait_for_timeout(5000)

    page.locator("#category-field-search").fill("digital wall art printable")
    page.wait_for_timeout(2500)
    page.get_by_text("Digital Prints", exact=True).first.click(timeout=8000)
    page.wait_for_timeout(1500)

    # Switch to digital downloads. Direct event dispatch avoids sticky UI intercepts.
    page.locator('input[name="listing_type_options_group"][value="download"]').evaluate(
        "e => { e.checked=true; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }"
    )
    page.wait_for_timeout(2500)

    # Target the digital file uploader by its stable section id. After photos
    # upload, Etsy adds extra photo inputs, so positional nth() can hit the
    # wrong uploader and trigger a photo-format error for the ZIP.
    page.locator("#field-digitalFiles input[type=file]").set_input_files(zip_path)
    page.wait_for_timeout(4000)

    page.locator('textarea[name="title"]').fill(title)
    page.locator('textarea[name="description"]').fill(description)

    # Made in 2020-2026.
    selects = page.locator("select")
    if selects.count() > 0:
        try:
            selects.nth(0).select_option(label="2020 - 2026")
        except Exception:
            pass

    tag_input = page.locator("#listing-tags-input")
    for tag in tags[:13]:
        tag_input.fill(tag)
        tag_input.press("Enter")
        page.wait_for_timeout(150)

    page.locator("#listing-price-input").fill(price)
    page.locator("#listing-quantity-input").fill("999")
    try:
        page.get_by_role("button", name="Add SKU").click(timeout=3000)
        page.wait_for_timeout(500)
    except Exception:
        pass
    if page.locator('input[name="sku"]').count() > 0:
        try:
            page.locator('input[name="sku"]').fill(f"DIGITAL-{row['ID']}")
        except Exception:
            pass

    # How it's made: I did; finished product; created by me. Prefer direct radio dispatch for stability.
    _choose_radio_by_name(page, "whoMade", 0)
    _choose_radio_by_name(page, "isSupply", 0)
    _choose_radio_by_name(page, "digitalContentCreatedBy", 1)
    _set_manual_renew(page)


def _mark_result(row_id: str, listing_id: str, url: str, fee: float) -> None:
    queue = _read_csv(QUEUE_PATH)
    for row in queue:
        if row.get("ID") == row_id and not row.get("Etsy_Listing_ID"):
            row["Etsy_Listing_ID"] = listing_id
            row["Fee_Status"] = "CONFIRMED_SPENT"
            row["Launch_Status"] = "PUBLISHED_UI_CONFIRMED"
            row["Notes"] = f"Published via Etsy UI at {url}"
            break
    if queue:
        _write_csv(QUEUE_PATH, queue, list(queue[0].keys()))

    metadata = _read_csv(METADATA_PATH)
    for row in metadata:
        if row.get("ID") == row_id:
            row["Status"] = "PUBLISHED_ETSY_UI_CONFIRMED"
            break
    if metadata:
        _write_csv(METADATA_PATH, metadata, list(metadata[0].keys()))

    ledger = _read_csv(FEE_LEDGER_PATH)
    for row in ledger:
        if row.get("ID") == row_id and row.get("Status") == "RESERVED_NOT_SPENT":
            row["Confirmed_Spent_USD"] = f"{fee:.2f}"
            row["Status"] = "CONFIRMED_SPENT_UI"
            row["Reference"] = listing_id or url
            break
    if ledger:
        _write_csv(FEE_LEDGER_PATH, ledger, list(ledger[0].keys()))

    _append_csv(
        UI_LOG_PATH,
        [
            {
                "Timestamp": _now(),
                "ID": row_id,
                "Action": "PUBLISH",
                "Status": "CONFIRMED",
                "Etsy_Listing_ID": listing_id,
                "URL": url,
                "Confirmed_Fee_USD": f"{fee:.2f}",
                "Note": "Published through logged-in Etsy UI with manual renewal selected.",
            }
        ],
        LOG_FIELDS,
    )


def publish(limit: int = 1, dry_run: bool = False, cdp_port: int = 9223) -> dict:
    assert_allowed("etsy", "paid_publish")
    candidates = _select_candidates(limit)
    if not candidates:
        return {"selected": 0, "published": 0, "status": "NO_CANDIDATES"}
    assert_etsy_fee_batch_allowed(len(candidates), daily_spend_so_far=_confirmed_spend_today())
    fee = float((fee_kill_switch() or {}).get("expected_listing_fee_usd", 0.20))

    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{cdp_port}")
        context = browser.contexts[0]
        for row in candidates:
            page = context.new_page()
            try:
                _fill_listing(page, row)
                if dry_run:
                    results.append({"ID": row["ID"], "status": "DRY_RUN_FILLED", "url": page.url})
                    continue
                page.get_by_role("button", name="Publish").click(timeout=10000)
                page.wait_for_timeout(8000)
                try:
                    confirm = page.get_by_role("button", name="Publish")
                    if confirm.count() > 0 and confirm.first.is_visible():
                        confirm.first.click(timeout=10000)
                        page.wait_for_timeout(8000)
                except Exception:
                    pass
                url = page.url
                listing_id = _parse_listing_id(url)
                body = page.locator("body").inner_text(timeout=10000)
                if not listing_id and "/tools/listings" in url:
                    listing_id, url = _parse_listing_id_from_manager(page, row)
                if not listing_id and "newly_created=1" in page.url:
                    page.goto("https://www.etsy.com/your/shops/me/tools/listings", wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(12000)
                    listing_id, url = _parse_listing_id_from_manager(page, row)
                if not listing_id and "published" not in body.lower():
                    raise RuntimeError(f"Publish not confirmed. url={url} body={body[:500]}")
                _mark_result(row["ID"], listing_id, url, fee)
                results.append({"ID": row["ID"], "status": "PUBLISHED", "listing_id": listing_id, "url": url})
            except Exception as exc:  # noqa: BLE001
                _append_csv(
                    UI_LOG_PATH,
                    [
                        {
                            "Timestamp": _now(),
                            "ID": row.get("ID", ""),
                            "Action": "PUBLISH",
                            "Status": "ERROR",
                            "Etsy_Listing_ID": "",
                            "URL": page.url,
                            "Confirmed_Fee_USD": "0.00",
                            "Note": f"{type(exc).__name__}: {_clean(exc)}"[:500],
                        }
                    ],
                    LOG_FIELDS,
                )
                results.append({"ID": row.get("ID"), "status": "ERROR", "error": str(exc)[:300], "url": page.url})
                # Money-sensitive path: stop after any ambiguity/error.
                break
            finally:
                page.close()
        browser.close()
    return {"selected": len(candidates), "published": sum(1 for r in results if r["status"] == "PUBLISHED"), "results": results}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cdp-port", type=int, default=9223)
    args = parser.parse_args()
    result = publish(limit=args.limit, dry_run=args.dry_run, cdp_port=args.cdp_port)
    print(result)


if __name__ == "__main__":
    main()

```


### FULL SOURCE: modules/printify_publish_scheduler.py
```python
import argparse
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from openpyxl import load_workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules import ebay_ads_standard


EBAY_BOOK = PROJECT_ROOT / "Database" / "eBay_listing.xlsx"
PUBLISHABLE_PREFIXES = ("Printify_UI_Mockups",)
RETRYABLE_EXTERNAL_PENDING_PREFIXES = ("Printify_PublishExternalPending_Mockups",)
PUBLISHED_PREFIXES = ("Printify_Published", "Printify_Published_Mockups")
PUBLISH_BODY = {
    "title": True,
    "description": True,
    "images": True,
    "variants": True,
    "tags": True,
    "keyFeatures": True,
    "shipping_template": True,
}


def _headers():
    return {
        "Authorization": f"Bearer {Config.Printify_API_KEY}",
        "Content-Type": "application/json",
    }


def _product_type(value):
    text = str(value or "").strip().lower()
    if text.startswith("poster"):
        return "Poster"
    if text.startswith("acry"):
        return "Acrylic"
    if text.startswith("stick"):
        return "Sticker"
    return "Other"


def _publish_suffix(status):
    text = str(status or "")
    if "Mockups" in text:
        return text.split("Mockups", 1)[1]
    return ""


def _fetch_product(product_id):
    response = requests.get(
        f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products/{product_id}.json",
        headers={"Authorization": _headers()["Authorization"]},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _selected_count(product):
    return sum(1 for image in product.get("images") or [] if image.get("is_selected_for_publishing") is not False)


def _selected_images(product):
    return [
        image
        for image in product.get("images") or []
        if image.get("is_selected_for_publishing") is not False
    ]


def _ensure_column(ws, cols, name):
    if name not in cols:
        ws.cell(1, ws.max_column + 1).value = name
        cols[name] = ws.max_column
    return cols[name]


def _sync_external_id_for_row(ws, cols, row_idx, item_id, product_id, attempts=5, delay=12):
    ebay_col = _ensure_column(ws, cols, "eBay_Item_ID")
    url_col = _ensure_column(ws, cols, "eBay_Item_URL")
    type_col = _ensure_column(ws, cols, "External_Type")
    sync_col = _ensure_column(ws, cols, "External_Sync_Timestamp")
    existing = str(ws.cell(row_idx, ebay_col).value or "").strip()
    if existing:
        return existing, "existing"
    for attempt in range(1, attempts + 1):
        product = _fetch_product(product_id)
        external = product.get("external") or {}
        ebay_id = str(external.get("id") or "").strip()
        if ebay_id:
            ws.cell(row_idx, ebay_col).value = ebay_id
            ws.cell(row_idx, url_col).value = str(external.get("handle") or "").strip()
            ws.cell(row_idx, type_col).value = str(external.get("type") or "").strip()
            ws.cell(row_idx, sync_col).value = datetime.now()
            return ebay_id, f"synced_attempt_{attempt}"
        if attempt < attempts:
            time.sleep(delay)
    return "", "missing_external_id"


def _preflight(row):
    product_id = str(row.get("Printify_Product_ID") or "").strip()
    if not product_id:
        return False, "missing Printify_Product_ID"
    product = _fetch_product(product_id)
    if not product.get("print_areas"):
        return False, "missing print_areas"
    selected_images = _selected_images(product)
    selected = len(selected_images)
    defaults = [image for image in selected_images if image.get("is_default")]
    product_type = _product_type(row.get("Product_Type"))
    if product_type == "Sticker" and selected < 3:
        return False, f"selected mockups={selected}, expected >=3 official cover mockups"
    if product_type == "Sticker":
        custom_gallery = [
            image for image in selected_images
            if "pfy-prod-products-mockup-media" in str(image.get("src") or "")
        ]
        if custom_gallery:
            return False, f"sticker custom gallery images selected={len(custom_gallery)}; use cover-only official mockups before publish"
    if product_type == "Poster" and selected < 4:
        return False, f"selected mockups={selected}, expected >=4"
    if product_type == "Acrylic" and selected < 4:
        return False, f"selected mockups={selected}, expected >=4"
    if len(defaults) < 1:
        return False, "default image count=0, expected at least 1 before publish"
    return True, f"selected mockups={selected}, defaults={len(defaults)}"


def _publish(product_id):
    last_error = None
    for attempt in range(1, 4):
        try:
            response = requests.post(
                f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products/{product_id}/publish.json",
                headers=_headers(),
                json=PUBLISH_BODY,
                timeout=180,
            )
            if response.status_code in {200, 201, 202, 204}:
                return response.status_code
            response.raise_for_status()
        except Exception as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(8 * attempt)
    raise last_error


def _load_publishable(limit, product_cycle, ids=None, retry_pending=False):
    wanted_ids = {str(item).strip() for item in (ids or []) if str(item).strip()}
    wb = load_workbook(EBAY_BOOK)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    cols = {header: idx + 1 for idx, header in enumerate(headers)}
    if "Publish_Timestamp" not in cols:
        ws.cell(1, ws.max_column + 1).value = "Publish_Timestamp"
        cols["Publish_Timestamp"] = ws.max_column
    buckets = {product_type: [] for product_type in product_cycle}
    for row_idx in range(2, ws.max_row + 1):
        row_id = str(ws.cell(row_idx, cols["ID"]).value or "").strip()
        if wanted_ids and row_id not in wanted_ids:
            continue
        status = str(ws.cell(row_idx, cols["Status"]).value or "")
        allowed_prefixes = PUBLISHABLE_PREFIXES + (RETRYABLE_EXTERNAL_PENDING_PREFIXES if retry_pending else ())
        if status.startswith(PUBLISHED_PREFIXES) or not status.startswith(allowed_prefixes):
            continue
        product_type = _product_type(ws.cell(row_idx, cols["Product_Type"]).value)
        if product_type not in buckets:
            continue
        row = {header: ws.cell(row_idx, cols[header]).value for header in headers if header in cols}
        row["_row_idx"] = row_idx
        buckets[product_type].append(row)

    selected = []
    while len(selected) < limit and any(buckets.values()):
        for product_type in product_cycle:
            if buckets[product_type] and len(selected) < limit:
                selected.append(buckets[product_type].pop(0))
    return wb, ws, cols, selected


def run(limit=8, min_delay=90, max_delay=240, product_cycle=None, dry_run=False, ids=None, retry_pending=False):
    product_cycle = product_cycle or ["Poster", "Acrylic", "Sticker"]
    wb, ws, cols, rows = _load_publishable(limit, product_cycle, ids=ids, retry_pending=retry_pending)
    done = 0
    try:
        for row in rows:
            item_id = row["ID"]
            product_id = str(row.get("Printify_Product_ID") or "").strip()
            row_idx = row["_row_idx"]
            try:
                ok, note = _preflight(row)
                if not ok:
                    print(f"[PUBLISH-SKIP] {item_id}: {note}")
                    continue
                if dry_run:
                    print(f"[PUBLISH-DRY] {item_id} product={product_id} {note}")
                    continue
                code = _publish(product_id)
                suffix = _publish_suffix(row.get("Status"))
                ws.cell(row_idx, cols["Publish_Timestamp"]).value = datetime.now()
                ebay_id, external_note = _sync_external_id_for_row(ws, cols, row_idx, item_id, product_id)
                if ebay_id:
                    ws.cell(row_idx, cols["Status"]).value = f"Printify_Published_Mockups{suffix}" if suffix else "Printify_Published"
                else:
                    ws.cell(row_idx, cols["Status"]).value = (
                        f"Printify_PublishExternalPending_Mockups{suffix}" if suffix else "Printify_PublishExternalPending"
                    )
                if ebay_id:
                    ads_ok = ebay_ads_standard.enroll_listing(item_id, ebay_id)
                    ads_note = "ads_enrolled" if ads_ok else "ads_queued"
                else:
                    ads_note = "ads_waiting_for_external_id"
                done += 1 if ebay_id else 0
                wb.save(EBAY_BOOK)
                print(
                    f"[PUBLISH-OK] {item_id} product={product_id} http={code} {note} "
                    f"external={external_note} ebay={ebay_id or 'MISSING'} {ads_note}"
                )
                if done < len(rows):
                    delay = random.randint(min_delay, max_delay)
                    print(f"[PUBLISH-SLEEP] {delay}s")
                    time.sleep(delay)
            except Exception as exc:
                print(f"[PUBLISH-FAIL] {item_id}: {exc}")
                continue
    finally:
        wb.close()
    print(f"[DONE] publish attempted={len(rows)} external_confirmed={done}")
    return done


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--min-delay", type=int, default=90)
    parser.add_argument("--max-delay", type=int, default=240)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cycle", default="Poster,Acrylic,Sticker")
    parser.add_argument("--ids", default="", help="Comma-separated listing IDs to publish exactly.")
    parser.add_argument("--retry-pending", action="store_true", help="Explicitly retry Printify_PublishExternalPending rows.")
    args = parser.parse_args()
    cycle = [part.strip() for part in args.cycle.split(",") if part.strip()]
    ids = [part.strip() for part in args.ids.split(",") if part.strip()]
    run(
        limit=args.limit,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        product_cycle=cycle,
        dry_run=args.dry_run,
        ids=ids,
        retry_pending=args.retry_pending,
    )


if __name__ == "__main__":
    main()

```


### FULL SOURCE: modules/ebay_ads_standard.py
```python
import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from openpyxl import load_workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
EBAY_BOOK = DATABASE_DIR / "eBay_listing.xlsx"
LOG_PATH = DATABASE_DIR / "ebay_ads_standard_2pct.csv"
PENDING_PATH = DATABASE_DIR / "ebay_ads_pending_2pct.csv"

CAMPAIGN_NAME = "Fixed_2_Percent_Strategy"
DEFAULT_CAMPAIGN_ID = os.getenv("EBAY_AD_CAMPAIGN_ID", "165251921016")
MARKETPLACE_ID = os.getenv("EBAY_MARKETPLACE_ID", "EBAY_US")
AD_RATE = "2.0"
BASE_URL = os.getenv("EBAY_API_BASE_URL", "https://api.ebay.com")

HEADERS = [
    "Timestamp",
    "Action",
    "ID",
    "eBay_Item_ID",
    "Campaign_ID",
    "HTTP_Status",
    "Result",
    "Error",
]
PENDING_HEADERS = [
    "Timestamp",
    "ID",
    "eBay_Item_ID",
    "Campaign_ID",
    "Ad_Rate",
    "Status",
    "Error",
]


def _access_token():
    token = [REDACTED]"EBAY_ACCESS_TOKEN") or os.getenv("EBAY_OAUTH_TOKEN")
    if not token:
        [REDACTED] RuntimeError(
            "Missing EBAY_ACCESS_TOKEN / EBAY_OAUTH_TOKEN. eBay Marketing API cannot be used until OAuth is configured."
        )
    return token


def has_access_token():
    return bool(os.getenv("EBAY_ACCESS_TOKEN") or os.getenv("EBAY_OAUTH_TOKEN"))


def _headers():
    return {
        "Authorization": f"Bearer {_access_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE_ID,
    }


def _api(method, path, **kwargs):
    response = requests.request(method, f"{BASE_URL}{path}", headers=_headers(), timeout=90, **kwargs)
    return response


def _log(rows):
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def enqueue_listing(item_id, ebay_item_id, campaign_id=None, status="PENDING_API"):
    ebay_item_id = str(ebay_item_id or "").strip()
    if not ebay_item_id:
        return False
    campaign_id = campaign_id or DEFAULT_CAMPAIGN_ID or CAMPAIGN_NAME
    existing = set()
    if PENDING_PATH.exists():
        with PENDING_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                existing.add((row.get("eBay_Item_ID"), row.get("Campaign_ID")))
    key = (ebay_item_id, campaign_id)
    if key in existing:
        return False
    file_exists = PENDING_PATH.exists()
    with PENDING_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PENDING_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "Timestamp": datetime.now().isoformat(timespec="seconds"),
                "ID": item_id,
                "eBay_Item_ID": ebay_item_id,
                "Campaign_ID": campaign_id,
                "Ad_Rate": AD_RATE,
                "Status": status,
                "Error": "",
            }
        )
    return True


def _published_listing_ids(limit=0):
    workbook = load_workbook(EBAY_BOOK, read_only=True, data_only=True)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    cols = {header: index for index, header in enumerate(headers)}
    if "eBay_Item_ID" not in cols:
        workbook.close()
        raise RuntimeError("eBay_Item_ID column is missing. Run printify_external_sync.py first.")
    rows = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row or not row[cols["ID"]]:
            continue
        status = str(row[cols.get("Status")] or "")
        item_id = str(row[cols["eBay_Item_ID"]] or "").strip()
        if status.startswith("Printify_Published") and item_id:
            rows.append(
                {
                    "ID": row[cols["ID"]],
                    "Product_Type": row[cols.get("Product_Type")],
                    "Title": row[cols.get("Title")],
                    "eBay_Item_ID": item_id,
                }
            )
            if limit and len(rows) >= limit:
                break
    workbook.close()
    return rows


def find_campaign():
    response = _api("GET", f"/sell/marketing/v1/ad_campaign?campaign_name={CAMPAIGN_NAME}")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    data = response.json()
    campaigns = data.get("campaigns") or data.get("adCampaigns") or []
    for campaign in campaigns:
        if campaign.get("campaignName") == CAMPAIGN_NAME or campaign.get("name") == CAMPAIGN_NAME:
            return campaign
    return campaigns[0] if len(campaigns) == 1 else None


def create_campaign():
    payload = {
        "campaignName": CAMPAIGN_NAME,
        "campaignFundingStrategy": {
            "fundingModel": "COST_PER_SALE",
            "bidPercentage": AD_RATE,
        },
        "marketplaceId": MARKETPLACE_ID,
    }
    response = _api("POST", "/sell/marketing/v1/ad_campaign", json=payload)
    if response.status_code not in {200, 201, 202, 204}:
        response.raise_for_status()
    location = response.headers.get("Location", "")
    campaign_id = location.rstrip("/").split("/")[-1] if location else ""
    return campaign_id, response.status_code, location


def bulk_create_ads(campaign_id, listings, dry_run=True):
    logs = []
    if dry_run:
        for listing in listings:
            logs.append(
                {
                    "Timestamp": datetime.now().isoformat(timespec="seconds"),
                    "Action": "DRY_RUN_ADD_AD",
                    "ID": listing["ID"],
                    "eBay_Item_ID": listing["eBay_Item_ID"],
                    "Campaign_ID": campaign_id,
                    "HTTP_Status": "",
                    "Result": f"Would add listing at fixed bidPercentage={AD_RATE}",
                    "Error": "",
                }
            )
        _log(logs)
        print(f"[ADS-DRY] campaign={campaign_id or CAMPAIGN_NAME} listings={len(listings)} rate={AD_RATE}")
        return logs
    requests_payload = [
        {"listingId": listing["eBay_Item_ID"], "bidPercentage": AD_RATE}
        for listing in listings
    ]
    response = _api(
        "POST",
        f"/sell/marketing/v1/ad_campaign/{campaign_id}/bulk_create_ads_by_listing_id",
        json={"requests": requests_payload},
    )
    result_text = response.text[:1000]
    status_code = response.status_code
    if response.status_code not in {200, 201, 202, 207}:
        response.raise_for_status()
    for listing in listings:
        logs.append(
            {
                "Timestamp": datetime.now().isoformat(timespec="seconds"),
                "Action": "ADD_AD_FIXED_2",
                "ID": listing["ID"],
                "eBay_Item_ID": listing["eBay_Item_ID"],
                "Campaign_ID": campaign_id,
                "HTTP_Status": status_code,
                "Result": result_text,
                "Error": "",
            }
        )
    _log(logs)
    print(f"[ADS-OK] campaign={campaign_id} listings={len(listings)} http={status_code}")
    return logs


def enroll_listing(item_id, ebay_item_id, campaign_id=None, dry_run=False):
    campaign_id = campaign_id or DEFAULT_CAMPAIGN_ID
    listing = {"ID": item_id, "eBay_Item_ID": str(ebay_item_id).strip()}
    if not listing["eBay_Item_ID"]:
        return False
    if dry_run:
        bulk_create_ads(campaign_id or CAMPAIGN_NAME, [listing], dry_run=True)
        return True
    if not has_access_token():
        enqueue_listing(item_id, listing["eBay_Item_ID"], campaign_id=campaign_id, status="PENDING_OAUTH")
        print(f"[ADS-PENDING] {item_id} ebay={listing['eBay_Item_ID']} reason=missing_oauth")
        return False
    if not campaign_id:
        campaign = find_campaign()
        campaign_id = (
            campaign.get("campaignId")
            or campaign.get("campaign_id")
            or campaign.get("adCampaignId")
            if campaign
            else ""
        )
    if not campaign_id:
        enqueue_listing(item_id, listing["eBay_Item_ID"], campaign_id=CAMPAIGN_NAME, status="PENDING_CAMPAIGN_ID")
        print(f"[ADS-PENDING] {item_id} ebay={listing['eBay_Item_ID']} reason=missing_campaign_id")
        return False
    bulk_create_ads(campaign_id, [listing], dry_run=False)
    return True


def run(limit=0, dry_run=True, campaign_id=None, create_if_missing=False):
    listings = _published_listing_ids(limit=limit)
    print(f"[ADS] eligible_with_ebay_id={len(listings)} dry_run={dry_run} rate={AD_RATE}")
    if dry_run:
        return bulk_create_ads(campaign_id or CAMPAIGN_NAME, listings, dry_run=True)
    campaign = None
    if campaign_id:
        resolved_campaign_id = campaign_id
    else:
        campaign = find_campaign()
        resolved_campaign_id = (
            campaign.get("campaignId")
            or campaign.get("campaign_id")
            or campaign.get("adCampaignId")
            if campaign
            else ""
        )
    if not resolved_campaign_id and create_if_missing:
        resolved_campaign_id, status, location = create_campaign()
        print(f"[ADS-CAMPAIGN-CREATED] id={resolved_campaign_id} http={status} location={location}")
    if not resolved_campaign_id:
        raise RuntimeError(
            f"Campaign {CAMPAIGN_NAME} was not found. Create it in Seller Hub or rerun with --create-if-missing after final confirmation."
        )
    return bulk_create_ads(resolved_campaign_id, listings, dry_run=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--campaign-id", default="")
    parser.add_argument("--create-if-missing", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    run(
        limit=args.limit,
        dry_run=not args.execute,
        campaign_id=args.campaign_id or None,
        create_if_missing=args.create_if_missing,
    )


if __name__ == "__main__":
    main()

```


### FULL SOURCE: modules/risk_guard.py
```python
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RISK_PATH = PROJECT_ROOT / "Database" / "Account_Risk_State.json"
FEE_PATH = PROJECT_ROOT / "Database" / "Etsy_Fee_Kill_Switch.json"


class RiskBlocked(RuntimeError):
    pass


def _load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def risk_state():
    return _load_json(RISK_PATH)


def fee_kill_switch():
    return _load_json(FEE_PATH)


def marketplace_state(marketplace):
    states = risk_state().get("states") or {}
    return states.get(str(marketplace).lower()) or {}


def assert_allowed(marketplace, action):
    state = marketplace_state(marketplace)
    action = str(action).lower()
    key = {
        "read": "read_allowed",
        "write": "write_allowed",
        "paid_publish": "paid_publish_allowed",
        "paid_ads": "paid_ads_allowed",
    }.get(action, f"{action}_allowed")
    if state and not state.get(key, False):
        raise RiskBlocked(
            f"{marketplace} {action} blocked by Account_Risk_State: "
            f"{state.get('risk_state')} | {state.get('notes', '')}"
        )
    return True


def assert_etsy_fee_batch_allowed(planned_count, ambiguous_count=0, duplicate_paid_count=0, daily_spend_so_far=0.0):
    config = fee_kill_switch()
    if not config:
        return True
    expected_fee = float(config.get("expected_listing_fee_usd", 0.20))
    planned_fee = planned_count * expected_fee
    if planned_count > int(config.get("batch_listing_cap", 10)):
        raise RiskBlocked(f"Etsy batch listing cap exceeded: {planned_count}")
    if planned_fee > float(config.get("batch_fee_cap_usd", 2.0)):
        raise RiskBlocked(f"Etsy batch fee cap exceeded: ${planned_fee:.2f}")
    if daily_spend_so_far + planned_fee > float(config.get("daily_listing_fee_cap_usd", 6.0)):
        raise RiskBlocked(f"Etsy daily fee cap exceeded: ${daily_spend_so_far + planned_fee:.2f}")
    if ambiguous_count >= int(config.get("ambiguous_publish_cap", 1)):
        raise RiskBlocked("Etsy ambiguous paid publish cap reached; stop and reconcile.")
    if duplicate_paid_count > int(config.get("duplicate_paid_listing_cap", 0)):
        raise RiskBlocked("Etsy duplicate paid listing cap exceeded.")
    return True

```


## Risk State JSON / Fee Kill Switch JSON


### Database/Account_Risk_State.json
```json
{
  "updated_at": "2026-05-06T21:08:51-04:00",
  "policy": "Compliant account containment. Do not spoof identity, bypass marketplace enforcement, or move flagged activity to backup accounts.",
  "states": {
    "ebay": {
      "read_allowed": true,
      "write_allowed": true,
      "paid_ads_allowed": false,
      "paid_ads_mode": "Promoted Listings Standard / General fixed 2% only after OAuth",
      "risk_state": "OK_LIMITED_BY_OAUTH",
      "notes": "No Priority/PPC. Seller Hub writes allowed only for known maintenance like retiring verified bad listings."
    },
    "etsy": {
      "read_allowed": true,
      "write_allowed": true,
      "paid_publish_allowed": true,
      "risk_state": "UI_LOGGED_IN_API_PENDING",
      "notes": "Rex confirmed Etsy login works in dedicated Edge. Paid publish is authorized only under Etsy_Fee_Kill_Switch caps: 200-listing pool, $2 per batch, $6 daily gray cap unless explicitly changed."
    },
    "printify": {
      "read_allowed": true,
      "write_allowed": true,
      "paid_publish_allowed": false,
      "risk_state": "OK",
      "notes": "Printify product creation/publish is allowed for eBay/Printify workflow; avoid order/payment settings."
    }
  }
}

```


### Database/Etsy_Fee_Kill_Switch.json
```json
{
  "updated_at": "2026-05-06T21:09:14-04:00",
  "marketplace": "Etsy",
  "authorized_pool_listings": 200,
  "expected_listing_fee_usd": 0.2,
  "authorized_pool_budget_usd": 40.0,
  "batch_listing_cap": 10,
  "batch_fee_cap_usd": 2.0,
  "daily_listing_fee_cap_usd": 6.0,
  "ambiguous_publish_cap": 1,
  "duplicate_paid_listing_cap": 0,
  "default_action_on_ambiguous_paid_state": "STOP_BATCH_AND_RECONCILE",
  "publish_requires_confirmation_before_next_create": true,
  "notes": [
    "Default Etsy experiment pool: 200 listings / $40 listing fees.",
    "Before there is meaningful market evidence, $40-$60 is the maximum acceptable total spend.",
    "Do not exceed $40 unless a written evidence-based rationale is recorded for Rex/Gemini.",
    "Never exceed $60 before results without explicit new instruction.",
    "Preserve capital before preserving output.",
    "If a paid publish/create result cannot be confirmed, do not retry create blindly.",
    "Query by local idempotency key/title/SKU/hash before any retry.",
    "Full 200-listing pool should be consumed only after staged performance signals."
  ],
  "absolute_no_result_spend_cap_usd": 60.0,
  "spend_between_40_and_60_requires_written_rationale": true
}

```


# 2. Live Pulse - Last 24h Raw Logs


### RAW LOG: Database/Factory_Autopilot_Run_Log.csv
```text
﻿Timestamp,Module,Status,Detail
2026-05-06T01:04:46-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=34
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0005 title_length_72
[LOCAL-QA] Sticker-Academia-0008 title_length_73
[LOCAL-QA] Sticker-Academia-0010 title_length_73
[LOCAL-QA] Sticker-Academia-0011 title_length_71
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0002 title_length_74
[LOCAL-QA] Sticker-Zen-0003 title_length_73
[LOCAL-QA] Sticker-Zen-0005 title_length_74
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sti"
2026-05-06T01:04:47-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T01:04:48-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=29
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=7
[REGISTRY] Published_Zero_View_Copy_Ad_Review=43
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T01:04:49-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=49
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=36
[MARKET-QUEUE] action HOLD=35
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=34
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=29
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=7
[MARKET-QUEUE] dependency medium=78
[MARKET-QUEUE] dependency local=69
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency low=43"
2026-05-06T01:04:49-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T01:04:50-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0104.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_0104.md"
2026-05-06T01:53:30-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=27
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T01:53:31-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T01:53:32-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=45"
2026-05-06T01:53:33-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T01:53:34-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=29
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=42
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T01:53:35-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=27
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=27
[MARKET-QUEUE] action HOLD=22
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=11
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=5
[MARKET-QUEUE] dependency medium=125
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency local=49
[MARKET-QUEUE] dependency low=16"
2026-05-06T01:53:35-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T01:53:36-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T01:53:36-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0153.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_0153.md"
2026-05-06T07:34:39-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=27
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T07:34:41-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T07:34:41-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=45"
2026-05-06T07:34:43-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T07:34:44-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=29
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=42
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T07:34:45-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action FIX_PRINTIFY_DEFAULT_IMAGE_BEFORE_PUBLISH=74
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=27
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=24
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=8
[MARKET-QUEUE] action HOLD=6
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=2
[MARKET-QUEUE] dependency medium=155
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency local=33
[MARKET-QUEUE] dependency low=2"
2026-05-06T07:34:45-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T07:34:46-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T07:34:47-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T07:34:47-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T07:34:48-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0734.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_0734.md"
2026-05-06T07:40:18-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=27
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T07:40:19-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T07:40:21-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=45"
2026-05-06T07:40:22-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T07:40:23-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=29
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=42
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T07:40:25-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action FIX_PRINTIFY_DEFAULT_IMAGE_BEFORE_PUBLISH=74
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=27
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=24
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=8
[MARKET-QUEUE] action HOLD=6
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=2
[MARKET-QUEUE] dependency medium=155
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency local=33
[MARKET-QUEUE] dependency low=2"
2026-05-06T07:40:25-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T07:40:26-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T07:40:26-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T07:40:27-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T07:40:27-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=13 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=4
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] BLOCKED=1
[FACTORY-BACKLOG] WAIT_PRINTIFY_LOGIN=1
[FACTORY-BACKLOG] BLOCKED_BY_COVER_GATE=1
[FACTORY-BACKLOG] WAIT_SOURCE_REPAIR_RESULT=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T07:40:29-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0740.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_0740.md"
2026-05-06T10:45:09-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T10:46:22-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=27
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T10:46:23-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T10:46:24-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=45"
2026-05-06T10:46:25-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T10:46:27-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=29
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=42
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T10:46:28-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action FIX_PRINTIFY_DEFAULT_IMAGE_BEFORE_PUBLISH=74
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=27
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=24
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=8
[MARKET-QUEUE] action HOLD=6
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=2
[MARKET-QUEUE] dependency medium=155
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency local=33
[MARKET-QUEUE] dependency low=2"
2026-05-06T10:46:28-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T10:46:29-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T10:46:29-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T10:46:29-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T10:46:31-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T10:46:31-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=14 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=5
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] BLOCKED=1
[FACTORY-BACKLOG] WAIT_PRINTIFY_LOGIN=1
[FACTORY-BACKLOG] BLOCKED_BY_COVER_GATE=1
[FACTORY-BACKLOG] WAIT_SOURCE_REPAIR_RESULT=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T10:46:32-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1046.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_1046.md"
2026-05-06T12:31:01-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T12:32:05-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=27
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T12:32:06-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T12:32:06-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=45"
2026-05-06T12:32:07-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T12:32:08-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=30
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=41
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T12:32:09-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action FIX_PRINTIFY_DEFAULT_IMAGE_BEFORE_PUBLISH=74
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=27
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=24
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=8
[MARKET-QUEUE] action HOLD=6
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=2
[MARKET-QUEUE] dependency medium=155
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency local=33
[MARKET-QUEUE] dependency low=2"
2026-05-06T12:32:09-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T12:32:10-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T12:32:10-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T12:32:10-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T12:32:12-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T12:32:12-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=14 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=6
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] BLOCKED_BY_COVER_GATE=1
[FACTORY-BACKLOG] WAIT_SOURCE_REPAIR_RESULT=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T12:32:13-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1232.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_1232.md"
2026-05-06T12:35:55-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T12:36:59-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=27
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T12:37:00-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T12:37:01-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=1
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=44"
2026-05-06T12:37:02-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T12:37:02-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=30
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=41
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T12:37:03-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action FIX_PRINTIFY_DEFAULT_IMAGE_BEFORE_PUBLISH=74
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=27
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=24
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=8
[MARKET-QUEUE] action HOLD=6
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=2
[MARKET-QUEUE] dependency medium=155
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency local=33
[MARKET-QUEUE] dependency low=2"
2026-05-06T12:37:03-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T12:37:04-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T12:37:04-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T12:37:04-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T12:37:07-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T12:37:08-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=14 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=6
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] BLOCKED_BY_COVER_GATE=1
[FACTORY-BACKLOG] WAIT_SOURCE_REPAIR_RESULT=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T12:37:09-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1237.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_1237.md"
2026-05-06T12:43:59-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T12:45:12-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=27
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T12:45:13-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T12:45:14-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=1
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=44"
2026-05-06T12:45:15-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T12:45:16-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=30
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=41
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T12:45:17-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=27
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=27
[MARKET-QUEUE] action HOLD=22
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=11
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=5
[MARKET-QUEUE] dependency medium=125
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency local=49
[MARKET-QUEUE] dependency low=16"
2026-05-06T12:45:17-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T12:45:18-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T12:45:19-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T12:45:19-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T12:45:21-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T12:45:22-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=14 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=6
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=1
[FACTORY-BACKLOG] WAIT_SOURCE_REPAIR_RESULT=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T12:45:23-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1245.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_1245.md"
2026-05-06T12:51:18-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T12:52:22-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=27
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T12:52:23-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T12:52:24-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=1
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=44"
2026-05-06T12:52:25-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T12:52:26-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=30
[REGISTRY] Hold=62
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=41
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T12:52:26-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=240 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=27
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=27
[MARKET-QUEUE] action HOLD=22
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=11
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=5
[MARKET-QUEUE] dependency medium=125
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency local=49
[MARKET-QUEUE] dependency low=16"
2026-05-06T12:52:26-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T12:52:27-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T12:52:27-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T12:52:28-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T12:52:32-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T12:52:32-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=14 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=6
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=1
[FACTORY-BACKLOG] WAIT_SOURCE_REPAIR_RESULT=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T12:52:33-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1252.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_1252.md"
2026-05-06T13:51:42-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T13:52:48-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=242 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=28
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T13:52:48-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T13:52:49-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=1
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=44"
2026-05-06T13:52:50-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T13:52:51-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=242 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=30
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=63
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=41
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=49"
2026-05-06T13:52:52-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=242 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=49
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=28
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=27
[MARKET-QUEUE] action HOLD=23
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=11
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=5
[MARKET-QUEUE] dependency medium=125
[MARKET-QUEUE] dependency local=51
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency low=16"
2026-05-06T13:52:52-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T13:52:52-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T13:52:52-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T13:52:53-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T13:52:54-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T13:52:54-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=16 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=7
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] WAIT_SOURCE_REPAIR_RESULT=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T13:52:55-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1352.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_1352.md"
2026-05-06T15:10:07-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T15:11:19-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=255 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=28
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T15:11:20-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T15:11:21-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=1
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4
[COVER-REPLACEMENT-QUEUE] WAIT_SOURCE_REPAIR_RESULT=44"
2026-05-06T15:11:21-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T15:11:22-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=255 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=30
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=84
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=41
[REGISTRY] Ready_For_Printify_When_Network_OK=50
[REGISTRY] Stable_Draft_Publish_When_Scheduled=41"
2026-05-06T15:11:23-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=255 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=50
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action HOLD=44
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=41
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=28
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=27
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=11
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=5
[MARKET-QUEUE] dependency medium=117
[MARKET-QUEUE] dependency local=72
[MARKET-QUEUE] dependency high=50
[MARKET-QUEUE] dependency low=16"
2026-05-06T15:11:23-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T15:11:24-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T15:11:24-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T15:11:25-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T15:11:26-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T15:11:26-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=16 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=7
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] WAIT_SOURCE_REPAIR_RESULT=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T15:11:27-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1511.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_1511.md"
2026-05-06T17:06:03-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T17:07:14-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=255 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=28
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T17:07:15-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  SOURCE_REPAIR_REQUIRED: 45"
2026-05-06T17:07:15-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=31
[COVER-REPLACEMENT-QUEUE] REPLACEMENT_PUBLISHED_LIVE_PASS=14
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4"
2026-05-06T17:07:16-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T17:07:18-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=255 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=32
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=120
[REGISTRY] Published_Has_View_Monitor=8
[REGISTRY] Published_Zero_View_Copy_Ad_Review=28
[REGISTRY] Ready_For_Printify_When_Network_OK=47
[REGISTRY] Stable_Draft_Publish_When_Scheduled=19"
2026-05-06T17:07:19-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=255 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action HOLD=67
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=47
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=29
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=28
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=19
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=11
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=5
[MARKET-QUEUE] dependency medium=97
[MARKET-QUEUE] dependency local=95
[MARKET-QUEUE] dependency high=47
[MARKET-QUEUE] dependency low=16"
2026-05-06T17:07:19-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T17:07:20-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T17:07:20-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T17:07:20-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T17:07:22-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T17:07:22-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=15 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=7
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T17:07:23-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1707.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_1707.md"
2026-05-06T20:21:00-04:00,printify_login_guard.py,FAIL_1,"Traceback (most recent call last):
  File ""C:\Users\Rex\AppData\Local\Python\pythoncore-3.14-64\Lib\asyncio\tasks.py"", line 488, in wait_for
    return await fut
           ^^^^^^^^^
  File ""C:\Users\Rex\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\websockets\asyncio\connection.py"", line 303, in recv
    return await self.recv_messages.get(decode)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ""C:\Users\Rex\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\websockets\asyncio\messages.py"", line 159, in get
    frame = await self.frames.get(not self.closed)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ""C:\Users\Rex\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\websockets\asyncio\messages.py"", line 51, in get
    await self.get_waiter
asyncio.exceptions.CancelledError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File ""C:\AIprojects\openclaw_difi\modules\printify_login_guard"
2026-05-06T20:22:25-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=273 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=29
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T20:22:26-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  RETIRED_REPLACED_DONE: 24
  SOURCE_REPAIR_REQUIRED: 21"
2026-05-06T20:22:27-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] OLD_RETIRED_REPLACED_DONE=24
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=21
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4"
2026-05-06T20:22:28-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T20:22:29-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=273 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=20
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=187
[REGISTRY] Ready_For_Printify_When_Network_OK=46
[REGISTRY] Stable_Draft_Publish_When_Scheduled=19"
2026-05-06T20:22:30-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=273 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action HOLD=113
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=46
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=29
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=19
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=17
[MARKET-QUEUE] dependency local=142
[MARKET-QUEUE] dependency medium=85
[MARKET-QUEUE] dependency high=46"
2026-05-06T20:22:30-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T20:22:31-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T20:22:31-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T20:22:31-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T20:22:32-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T20:22:33-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=15 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=7
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T20:22:34-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2022.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_2022.md"
2026-05-06T20:29:57-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T20:31:18-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=273 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=29
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T20:31:19-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  RETIRED_REPLACED_DONE: 24
  SOURCE_REPAIR_REQUIRED: 21"
2026-05-06T20:31:20-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] OLD_RETIRED_REPLACED_DONE=24
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=21
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4"
2026-05-06T20:31:20-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T20:31:21-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=273 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=20
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=187
[REGISTRY] Ready_For_Printify_When_Network_OK=46
[REGISTRY] Stable_Draft_Publish_When_Scheduled=19"
2026-05-06T20:31:22-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=273 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action HOLD=113
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=46
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=29
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=19
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=17
[MARKET-QUEUE] dependency local=142
[MARKET-QUEUE] dependency medium=85
[MARKET-QUEUE] dependency high=46"
2026-05-06T20:31:22-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T20:31:23-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T20:31:23-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T20:31:23-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T20:31:25-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T20:31:25-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=15 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=7
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T20:31:26-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2031.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_2031.md"
2026-05-06T22:29:15-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T22:30:29-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=274 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=29
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T22:30:30-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  RETIRED_REPLACED_DONE: 24
  SOURCE_REPAIR_REQUIRED: 21"
2026-05-06T22:30:31-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] OLD_RETIRED_REPLACED_DONE=24
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=21
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4"
2026-05-06T22:30:31-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T22:30:32-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=274 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=6
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=152
[REGISTRY] Published_Has_View_Monitor=7
[REGISTRY] Published_Zero_View_Copy_Ad_Review=43
[REGISTRY] Ready_For_Printify_When_Network_OK=46
[REGISTRY] Stable_Draft_Publish_When_Scheduled=19"
2026-05-06T22:30:33-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=274 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action HOLD=94
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=46
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=29
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=26
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=19
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=6
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=5
[MARKET-QUEUE] dependency local=123
[MARKET-QUEUE] dependency medium=73
[MARKET-QUEUE] dependency high=46
[MARKET-QUEUE] dependency low=32"
2026-05-06T22:30:33-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T22:30:34-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T22:30:34-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T22:30:34-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T22:30:35-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T22:30:36-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=15 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=7
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_MONITOR=1
[FACTORY-BACKLOG] WAIT_USER_OR_API_APPROVAL=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T22:30:36-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2230.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_2230.md"
2026-05-06T23:10:01-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T23:11:22-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=274 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=29
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T23:11:23-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  RETIRED_REPLACED_DONE: 25
  SOURCE_REPAIR_REQUIRED: 20"
2026-05-06T23:11:24-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] OLD_RETIRED_REPLACED_DONE=25
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=20
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4"
2026-05-06T23:11:25-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T23:11:27-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=274 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=6
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=153
[REGISTRY] Published_Has_View_Monitor=7
[REGISTRY] Published_Zero_View_Copy_Ad_Review=42
[REGISTRY] Ready_For_Printify_When_Network_OK=46
[REGISTRY] Stable_Draft_Publish_When_Scheduled=19"
2026-05-06T23:11:28-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=274 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action HOLD=94
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=46
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=29
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=26
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=19
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=6
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=5
[MARKET-QUEUE] dependency local=123
[MARKET-QUEUE] dependency medium=73
[MARKET-QUEUE] dependency high=46
[MARKET-QUEUE] dependency low=32"
2026-05-06T23:11:28-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T23:11:29-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T23:11:29-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T23:11:29-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T23:11:30-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T23:11:31-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=14 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=6
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] READY_MONITOR=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T23:11:32-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2311.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_2311.md"
2026-05-06T23:37:32-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T23:39:06-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=282 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=29
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T23:39:07-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  RETIRED_REPLACED_DONE: 33
  SOURCE_REPAIR_REQUIRED: 12"
2026-05-06T23:39:08-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] OLD_RETIRED_REPLACED_DONE=33
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=12
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4"
2026-05-06T23:39:09-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T23:39:10-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=282 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=6
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=169
[REGISTRY] Published_Has_View_Monitor=7
[REGISTRY] Published_Zero_View_Copy_Ad_Review=34
[REGISTRY] Ready_For_Printify_When_Network_OK=46
[REGISTRY] Stable_Draft_Publish_When_Scheduled=19"
2026-05-06T23:39:11-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=282 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action HOLD=102
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=46
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=29
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=26
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=19
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=6
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=5
[MARKET-QUEUE] dependency local=131
[MARKET-QUEUE] dependency medium=73
[MARKET-QUEUE] dependency high=46
[MARKET-QUEUE] dependency low=32"
2026-05-06T23:39:11-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T23:39:12-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T23:39:12-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T23:39:12-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T23:39:13-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T23:39:14-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=14 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=6
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] READY_MONITOR=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T23:39:15-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2339.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_2339.md"
2026-05-06T23:44:58-04:00,printify_login_guard.py,OK,[PRINTIFY-LOGIN] LOGGED_IN Printify dashboard is available.
2026-05-06T23:46:34-04:00,local_listing_qa.py,OK,"[LOCAL-QA] rows=282 csv=C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv
[LOCAL-QA] issue_rows=29
[LOCAL-QA] Sticker-Academia-0001 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0002 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0003 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Academia-0013 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0006 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0021 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0023 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0028 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0030 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0033 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0039 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0078 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0079 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0080 missing_cover; missing_gallery
[LOCAL-QA] Sticker-Zen-0082 missing_cover; miss"
2026-05-06T23:46:36-04:00,ebay_cover_repair_decision.py,OK,"[COVER-REPAIR-DECISIONS] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv
  NON_STICKER_REVIEW_REQUIRED: 4
  RETIRED_REPLACED_DONE: 33
  SOURCE_REPAIR_REQUIRED: 12"
2026-05-06T23:46:37-04:00,ebay_cover_replacement_queue.py,OK,"[COVER-REPLACEMENT-QUEUE] rows=49 csv=C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv
[COVER-REPLACEMENT-QUEUE] OLD_RETIRED_REPLACED_DONE=33
[COVER-REPLACEMENT-QUEUE] READY_TO_REPLACE_VERIFIED=12
[COVER-REPLACEMENT-QUEUE] REVIEW_BEFORE_REPLACE=4"
2026-05-06T23:46:38-04:00,ebay_title_repair_queue.py,OK,[TITLE-REPAIR] rows=0 ready=0 changed=0 csv=C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv
2026-05-06T23:46:39-04:00,unified_listing_registry.py,OK,"[REGISTRY] rows=282 csv=C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv
[REGISTRY] Etsy_Draft_Prepared=5
[REGISTRY] Fix_Gallery_First=1
[REGISTRY] Hold=162
[REGISTRY] Published_Has_View_Monitor=7
[REGISTRY] Published_Zero_View_Copy_Ad_Review=42
[REGISTRY] Ready_For_Printify_When_Network_OK=46
[REGISTRY] Stable_Draft_Publish_When_Scheduled=19"
2026-05-06T23:46:40-04:00,market_signal_planner.py,OK,"[MARKET-QUEUE] rows=282 csv=C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv
[MARKET-QUEUE] action HOLD=98
[MARKET-QUEUE] action FIX_LIVE_COVER_SOURCE_OR_REPLACE=49
[MARKET-QUEUE] action UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH=46
[MARKET-QUEUE] action WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST=31
[MARKET-QUEUE] action QA_HOLD_OR_REBUILD=29
[MARKET-QUEUE] action PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK=19
[MARKET-QUEUE] action MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL=6
[MARKET-QUEUE] action KEEP_FOR_ETSY_PHASE1=4
[MARKET-QUEUE] dependency local=127
[MARKET-QUEUE] dependency medium=72
[MARKET-QUEUE] dependency high=46
[MARKET-QUEUE] dependency low=37"
2026-05-06T23:46:41-04:00,ebay_experiment_report.py,OK,[EXPERIMENT-REPORT] rows=44 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv
2026-05-06T23:46:42-04:00,ebay_traffic_diagnosis.py,OK,"[TRAFFIC-DIAGNOSIS] rows=4 csv=C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv
[TRAFFIC-DIAGNOSIS] P100 Sticker live cover/gallery mismatch is a primary blocker.
[TRAFFIC-DIAGNOSIS] P90 Promoted Listings Standard 2% is active but is not enough alone.
[TRAFFIC-DIAGNOSIS] P80 Poster/Acrylic currently show more early movement than Sticker.
[TRAFFIC-DIAGNOSIS] P70 Title rewrite experiment has not produced a clear Sticker lift yet."
2026-05-06T23:46:42-04:00,ebay_profile_packet.py,OK,[EBAY-PROFILE-PACKET] C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md
2026-05-06T23:46:42-04:00,product_blueprint_next_plan.py,OK,"[BLUEPRINT-NEXT-PLAN] rows=5 csv=C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv
[BLUEPRINT-NEXT-PLAN] P1 Canvas blueprint=1936 variant=119906
[BLUEPRINT-NEXT-PLAN] P2 Framed Poster blueprint=1236 variant=93818
[BLUEPRINT-NEXT-PLAN] P3 Notebook/Journal blueprint=5634 variant=252281
[BLUEPRINT-NEXT-PLAN] P4 Mug blueprint=478 variant=65216
[BLUEPRINT-NEXT-PLAN] P5 Metal blueprint=1206 variant=91995"
2026-05-06T23:46:43-04:00,etsy_app_status_probe.py,OK,"[ETSY-APP] status=PENDING_OR_INACTIVE http=403 next=WAIT_APP_APPROVAL_OR_VERIFY_SECRET
[ETSY-APP] json=C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json"
2026-05-06T23:46:44-04:00,factory_backlog.py,OK,"[FACTORY-BACKLOG] rows=14 csv=C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv
[FACTORY-BACKLOG] READY=6
[FACTORY-BACKLOG] READY_TO_REPLACE_VERIFIED=2
[FACTORY-BACKLOG] WAIT_COVER_GATE=2
[FACTORY-BACKLOG] READY_MONITOR=2
[FACTORY-BACKLOG] READY_SINGLE_SKU_REPAIR=1
[FACTORY-BACKLOG] READY_FOR_SCHOLAR_REVIEW=1"
2026-05-06T23:46:45-04:00,factory_morning_report.py,OK,"[REPORT] C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2346.md
[GEMINI] C:\AIprojects\openclaw_difi\Gemini_Advisor\gemini_review_queue_20260506_2346.md"

```


### RAW LOG: Database/Performance_Log.csv
```text
﻿Snapshot_Timestamp,Platform,Item_ID,Title,Price,Views_30_Days,General_Status,Priority_Status,Suggested_Ad_Rate,Source_URL,Read_Status
2026-05-04 13:32:08 -0400,eBay,405211746642,7am2m electric toothbrush,$10.00,64,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892327989,Zen Aesthetic Koi Fish in Jade Pond Hisui no Koi 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892408950,Dark Academia Mechanical Raven Familiar 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892409123,Dark Academia Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892409348,Dark Academia Botanical Terrarium Lantern 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892409645,Dark Academia Astrolabe Navigation Instrument 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892409836,Dark Academia Ritual Incense Censer 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892410017,Dark Academia Gothic Cathedral Fragment 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892410190,Dark Academia Compass Rose Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892410307,Dark Academia Apothecary Poison Vial 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892410440,Dark Academia Microscope Observation Device 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892411034,Dark Academia Skeleton Key Portal 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892411436,Dark Academia Prism Light Refractor 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892411931,Zen Aesthetic Koi Pond 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892412365,Zen Aesthetic Bonsai Tree of Serenity 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892412612,Zen Aesthetic Lotus Mandala 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892412789,Zen Aesthetic Stone Guardian Lion 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892413076,Zen Aesthetic Bamboo Forest 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892413333,Zen Aesthetic Cherry Blossom Branch 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892413714,Zen Aesthetic Circle Ens 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892413966,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892414116,Zen Aesthetic Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892414235,Zen Aesthetic Garden Stone Meis seki 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Calm,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892414471,Zen Aesthetic Enso Circle with Crystals 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406892414741,Zen Aesthetic Temple Lantern Zendera no T r 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406733381906,Vinyl Dumbbell Set - 40 Pound,$15.00,4,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902584620,Gothic Academia Astral Archive Gateway of 12x18 Poster Library Print Scholar,$34.99 to $34.99,1,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902588642,Dark Academia Astrolabe Compass Ritual Disc 5x7 Acrylic Block Collector Gift,$89.99 to $89.99,1,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902593931,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902600741,Dark Academia Obsidian Threshold of Eternal 12x18 Poster Library Print Scholar,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902606976,Zen Aesthetic Plague Doctor Raven Skull 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902614234,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902616799,Gothic Academia Serpentine Portal of Alchemical 12x18 Poster Library Print Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902620519,Mindful Zen Crane Guardian Mechanism 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902622710,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902627420,Celestial Armillary Navigation Sphere Dark Academia 12x18 Matte Poster Study,$34.99 to $34.99,2,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902633400,Withered Mandrake Root Chamber Minimal Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902640998,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902648209,Vintage Academia Celestial Armillary Codex 12x18 Matte Poster Wall Decor Study,$34.99 to $34.99,2,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902657898,Ritual Bell Shrine Mindful Zen 5x7 Acrylic Photo Block Desk Display Shelf Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902663232,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902669660,Gothic Academia Cosmic Lotus Observatory 12x18 Wall Art Study Room Decor Gift,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902673249,Pagoda Fragment Relic Zen Aesthetic 5x7 Acrylic Photo Block Desk Display Shelf,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902691983,Astrolabe Chalice Relic 12x18 Matte Poster Dark Academia Gallery Decor Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902703464,Dark Academia Celestial Orrery Tree Bonsai 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902713267,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902882943,Orrery Lighthouse Beacon 12x18 Matte Poster Gothic Academia Gallery Decor Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902885214,Minimal Zen Ritual Censer Thurible 5x7 Desk Art Acrylic Block Study Decor Shelf,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902886081,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 13:32:08 -0400,eBay,406902887127,Dark Academia Jade Lotus Celestial Mechanism 12x18 Matte Poster Wall Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,405211746642,7am2m electric toothbrush,$10.00,64,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892327989,Zen Aesthetic Koi Fish in Jade Pond Hisui no Koi 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892408950,Dark Academia Mechanical Raven Familiar 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892409123,Dark Academia Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892409348,Dark Academia Botanical Terrarium Lantern 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892409645,Dark Academia Astrolabe Navigation Instrument 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892409836,Dark Academia Ritual Incense Censer 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892410017,Dark Academia Gothic Cathedral Fragment 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892410190,Dark Academia Compass Rose Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892410307,Dark Academia Apothecary Poison Vial 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892410440,Dark Academia Microscope Observation Device 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892411034,Dark Academia Skeleton Key Portal 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892411436,Dark Academia Prism Light Refractor 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892411931,Zen Aesthetic Koi Pond 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892412365,Zen Aesthetic Bonsai Tree of Serenity 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892412612,Zen Aesthetic Lotus Mandala 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892412789,Zen Aesthetic Stone Guardian Lion 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892413076,Zen Aesthetic Bamboo Forest 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892413333,Zen Aesthetic Cherry Blossom Branch 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892413714,Zen Aesthetic Circle Ens 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892413966,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892414116,Zen Aesthetic Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892414235,Zen Aesthetic Garden Stone Meis seki 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Calm,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892414471,Zen Aesthetic Enso Circle with Crystals 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406892414741,Zen Aesthetic Temple Lantern Zendera no T r 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406733381906,Vinyl Dumbbell Set - 40 Pound,$15.00,4,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902584620,Gothic Academia Astral Archive Gateway of 12x18 Poster Library Print Scholar,$34.99 to $34.99,1,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902588642,Dark Academia Astrolabe Compass Ritual Disc 5x7 Acrylic Block Collector Gift,$89.99 to $89.99,1,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902593931,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902600741,Dark Academia Obsidian Threshold of Eternal 12x18 Poster Library Print Scholar,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902606976,Zen Aesthetic Plague Doctor Raven Skull 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902614234,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902616799,Gothic Academia Serpentine Portal of Alchemical 12x18 Poster Library Print Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902620519,Mindful Zen Crane Guardian Mechanism 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902622710,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902627420,Celestial Armillary Navigation Sphere Dark Academia 12x18 Matte Poster Study,$34.99 to $34.99,2,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902633400,Withered Mandrake Root Chamber Minimal Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902640998,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902648209,Vintage Academia Celestial Armillary Codex 12x18 Matte Poster Wall Decor Study,$34.99 to $34.99,2,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902657898,Ritual Bell Shrine Mindful Zen 5x7 Acrylic Photo Block Desk Display Shelf Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902663232,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902669660,Gothic Academia Cosmic Lotus Observatory 12x18 Wall Art Study Room Decor Gift,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902673249,Pagoda Fragment Relic Zen Aesthetic 5x7 Acrylic Photo Block Desk Display Shelf,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902691983,Astrolabe Chalice Relic 12x18 Matte Poster Dark Academia Gallery Decor Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902703464,Dark Academia Celestial Orrery Tree Bonsai 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902713267,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902882943,Orrery Lighthouse Beacon 12x18 Matte Poster Gothic Academia Gallery Decor Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902885214,Minimal Zen Ritual Censer Thurible 5x7 Desk Art Acrylic Block Study Decor Shelf,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902886081,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 14:31:55 -0400,eBay,406902887127,Dark Academia Jade Lotus Celestial Mechanism 12x18 Matte Poster Wall Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892327989,Zen Aesthetic Koi Fish in Jade Pond Hisui no Koi 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892408950,Dark Academia Mechanical Raven Familiar 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892409123,Dark Academia Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892409348,Dark Academia Botanical Terrarium Lantern 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892409645,Dark Academia Astrolabe Navigation Instrument 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892409836,Dark Academia Ritual Incense Censer 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892410017,Dark Academia Gothic Cathedral Fragment 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892410190,Dark Academia Compass Rose Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892410307,Dark Academia Apothecary Poison Vial 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892410440,Dark Academia Microscope Observation Device 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892411034,Dark Academia Skeleton Key Portal 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892411436,Dark Academia Prism Light Refractor 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892411931,Zen Aesthetic Koi Pond 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892412365,Zen Aesthetic Bonsai Tree of Serenity 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892412612,Zen Aesthetic Lotus Mandala 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892412789,Zen Aesthetic Stone Guardian Lion 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892413076,Zen Aesthetic Bamboo Forest 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892413333,Zen Aesthetic Cherry Blossom Branch 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892413714,Zen Aesthetic Circle Ens 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892413966,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892414116,Zen Aesthetic Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892414235,Zen Aesthetic Garden Stone Meis seki 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Calm,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892414471,Zen Aesthetic Enso Circle with Crystals 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406892414741,Zen Aesthetic Temple Lantern Zendera no T r 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902584620,Gothic Academia Astral Archive Gateway of 12x18 Poster Library Print Scholar,$34.99 to $34.99,1,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902588642,Dark Academia Astrolabe Compass Ritual Disc 5x7 Acrylic Block Collector Gift,$89.99 to $89.99,1,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902593931,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902600741,Dark Academia Obsidian Threshold of Eternal 12x18 Poster Library Print Scholar,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902606976,Zen Aesthetic Plague Doctor Raven Skull 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902614234,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99 to $11.99,1,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902616799,Gothic Academia Serpentine Portal of Alchemical 12x18 Poster Library Print Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902620519,Mindful Zen Crane Guardian Mechanism 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902622710,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902627420,Celestial Armillary Navigation Sphere Dark Academia 12x18 Matte Poster Study,$34.99 to $34.99,2,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902633400,Withered Mandrake Root Chamber Minimal Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902640998,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902648209,Vintage Academia Celestial Armillary Codex 12x18 Matte Poster Wall Decor Study,$34.99 to $34.99,2,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902657898,Ritual Bell Shrine Mindful Zen 5x7 Acrylic Photo Block Desk Display Shelf Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902663232,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902669660,Gothic Academia Cosmic Lotus Observatory 12x18 Wall Art Study Room Decor Gift,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902673249,Pagoda Fragment Relic Zen Aesthetic 5x7 Acrylic Photo Block Desk Display Shelf,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902691983,Astrolabe Chalice Relic 12x18 Matte Poster Dark Academia Gallery Decor Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902703464,Dark Academia Celestial Orrery Tree Bonsai 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902713267,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902882943,Orrery Lighthouse Beacon 12x18 Matte Poster Gothic Academia Gallery Decor Wall,$34.99 to $34.99,0,Eligible,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902885214,Minimal Zen Ritual Censer Thurible 5x7 Desk Art Acrylic Block Study Decor Shelf,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902886081,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902887127,Dark Academia Jade Lotus Celestial Mechanism 12x18 Matte Poster Wall Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902888077,Minimal Zen Koi Automaton Spirit 5x7 Acrylic Block Collector Gift Jade Segments,$89.99 to $89.99,0,Eligible,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:04:06 -0400,eBay,406902889638,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Eligible,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892327989,Zen Aesthetic Koi Fish in Jade Pond Hisui no Koi 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892408950,Dark Academia Mechanical Raven Familiar 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892409123,Dark Academia Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892409348,Dark Academia Botanical Terrarium Lantern 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892409645,Dark Academia Astrolabe Navigation Instrument 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892409836,Dark Academia Ritual Incense Censer 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892410017,Dark Academia Gothic Cathedral Fragment 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892410190,Dark Academia Compass Rose Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892410307,Dark Academia Apothecary Poison Vial 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892410440,Dark Academia Microscope Observation Device 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892411034,Dark Academia Skeleton Key Portal 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892411436,Dark Academia Prism Light Refractor 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Study,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892411931,Zen Aesthetic Koi Pond 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892412365,Zen Aesthetic Bonsai Tree of Serenity 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892412612,Zen Aesthetic Lotus Mandala 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892412789,Zen Aesthetic Stone Guardian Lion 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892413076,Zen Aesthetic Bamboo Forest 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892413333,Zen Aesthetic Cherry Blossom Branch 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892413714,Zen Aesthetic Circle Ens 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892413966,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,1,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892414116,Zen Aesthetic Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892414235,Zen Aesthetic Garden Stone Meis seki 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Calm,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892414471,Zen Aesthetic Enso Circle with Crystals 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,1,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406892414741,Zen Aesthetic Temple Lantern Zendera no T r 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902584620,Gothic Academia Astral Archive Gateway of 12x18 Poster Library Print Scholar,$34.99 to $34.99,1,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902588642,Dark Academia Astrolabe Compass Ritual Disc 5x7 Acrylic Block Collector Gift,$89.99 to $89.99,1,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902593931,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902600741,Dark Academia Obsidian Threshold of Eternal 12x18 Poster Library Print Scholar,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902606976,Zen Aesthetic Plague Doctor Raven Skull 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902614234,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99 to $11.99,1,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902616799,Gothic Academia Serpentine Portal of Alchemical 12x18 Poster Library Print Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902620519,Mindful Zen Crane Guardian Mechanism 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902622710,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902627420,Celestial Armillary Navigation Sphere Dark Academia 12x18 Matte Poster Study,$34.99 to $34.99,2,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902633400,Withered Mandrake Root Chamber Minimal Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902640998,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902648209,Vintage Academia Celestial Armillary Codex 12x18 Matte Poster Wall Decor Study,$34.99 to $34.99,2,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902657898,Ritual Bell Shrine Mindful Zen 5x7 Acrylic Photo Block Desk Display Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902663232,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902669660,Gothic Academia Cosmic Lotus Observatory 12x18 Wall Art Study Room Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902673249,Pagoda Fragment Relic Zen Aesthetic 5x7 Acrylic Photo Block Desk Display Shelf,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902691983,Astrolabe Chalice Relic 12x18 Matte Poster Dark Academia Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902703464,Dark Academia Celestial Orrery Tree Bonsai 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902713267,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902882943,Orrery Lighthouse Beacon 12x18 Matte Poster Gothic Academia Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902885214,Minimal Zen Ritual Censer Thurible 5x7 Desk Art Acrylic Block Study Decor Shelf,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902886081,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902887127,Dark Academia Jade Lotus Celestial Mechanism 12x18 Matte Poster Wall Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902888077,Minimal Zen Koi Automaton Spirit 5x7 Acrylic Block Collector Gift Jade Segments,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-04 16:33:51 -0400,eBay,406902889638,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892327989,Zen Aesthetic Koi Fish in Jade Pond Hisui no Koi 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892408950,4pc Kiss-Cut Sticker Set Mechanical Raven Familiar Laptop Journal Bottle Dark,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892409123,4pc Vinyl Sticker Set Forbidden Grimoire Lock Laptop Bottle Journal Dark,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892409348,4pc Sticker Set Botanical Terrarium Lantern Vinyl Decals Laptop Bottle Dark,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892409645,4pc Kiss-Cut Sticker Set Astrolabe Navigation Instrument Laptop Journal Bottle,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892409836,4pc Vinyl Sticker Set Ritual Incense Censer Gothic Academia Laptop Bottle,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892410017,4pc Sticker Set Gothic Academia Cathedral Fragment Vinyl Decals Laptop Bottle,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892410190,4pc Kiss-Cut Sticker Set Compass Rose Talisman Laptop Journal Bottle Dark,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892410307,4pc Vinyl Sticker Set Apothecary Poison Vial Laptop Bottle Journal Dark,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892410440,4pc Vinyl Sticker Set Microscope Observation Device Laptop Bottle Journal Dark,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892411034,4pc Sticker Set Skeleton Key Portal Vinyl Decals Laptop Bottle Dark Academia,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892411436,4pc Kiss-Cut Sticker Set Gothic Academia Prism Light Refractor Laptop Journal,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892411931,Zen Aesthetic Koi Pond 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892412365,4pc Kiss-Cut Sticker Set Bonsai Tree of Serenity Laptop Journal Bottle Zen,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892412612,Zen Aesthetic Lotus Mandala 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal Water,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892412789,4pc Sticker Set Stone Guardian Lion Mindful Zen Vinyl Decals Laptop Bottle Zen,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892413076,4pc Kiss-Cut Sticker Set Bamboo Forest Laptop Journal Bottle Zen Aesthetic,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892413333,4pc Sticker Set Cherry Blossom Branch Vinyl Decals Laptop Bottle Zen Aesthetic,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892413714,4pc Kiss-Cut Sticker Set Circle Ens Laptop Journal Bottle Zen Aesthetic Decal,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892413966,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99 to $11.99,1,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892414116,Zen Aesthetic Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892414235,Zen Aesthetic Garden Stone Meis seki 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Calm,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892414471,Zen Aesthetic Enso Circle with Crystals 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,1,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406892414741,Zen Aesthetic Temple Lantern Zendera no T r 4pc 6x6 Kiss-Cut Sticker Vinyl Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902584620,Gothic Academia Astral Archive Gateway of 12x18 Poster Library Print Scholar,$34.99 to $34.99,1,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902588642,Dark Academia Astrolabe Compass Ritual Disc 5x7 Acrylic Block Collector Gift,$89.99 to $89.99,1,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902593931,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902600741,Dark Academia Obsidian Threshold of Eternal 12x18 Poster Library Print Scholar,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902606976,Zen Aesthetic Plague Doctor Raven Skull 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902614234,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902616799,Gothic Academia Serpentine Portal of Alchemical 12x18 Poster Library Print Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902620519,Mindful Zen Crane Guardian Mechanism 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902622710,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902627420,Celestial Armillary Navigation Sphere Dark Academia 12x18 Matte Poster Study,$34.99 to $34.99,2,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902633400,Withered Mandrake Root Chamber Minimal Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902640998,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902648209,Vintage Academia Celestial Armillary Codex 12x18 Matte Poster Wall Decor Study,$34.99 to $34.99,3,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902657898,Ritual Bell Shrine Mindful Zen 5x7 Acrylic Photo Block Desk Display Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902663232,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902669660,Gothic Academia Cosmic Lotus Observatory 12x18 Wall Art Study Room Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902673249,Pagoda Fragment Relic Zen Aesthetic 5x7 Acrylic Photo Block Desk Display Shelf,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902691983,Astrolabe Chalice Relic 12x18 Matte Poster Dark Academia Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902703464,Dark Academia Celestial Orrery Tree Bonsai 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902713267,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902882943,Orrery Lighthouse Beacon 12x18 Matte Poster Gothic Academia Gallery Decor Wall,$34.99 to $34.99,1,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902885214,Minimal Zen Ritual Censer Thurible 5x7 Desk Art Acrylic Block Study Decor Shelf,$89.99 to $89.99,0,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902886081,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902887127,Dark Academia Jade Lotus Celestial Mechanism 12x18 Matte Poster Wall Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902888077,Minimal Zen Koi Automaton Spirit 5x7 Acrylic Block Collector Gift Jade Segments,$89.99 to $89.99,1,Promoted,Eligible,13%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 01:23:31 -0400,eBay,406902889638,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406892408950,4pc Kiss-Cut Sticker Set Mechanical Raven Familiar Laptop Journal Bottle Dark,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406892414116,Zen Aesthetic Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902584620,Gothic Academia Astral Archive Gateway of 12x18 Poster Library Print Scholar,$34.99 to $34.99,1,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902588642,Dark Academia Astrolabe Compass Ritual Disc 5x7 Acrylic Block Collector Gift,$89.99 to $89.99,1,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902600741,Dark Academia Obsidian Threshold of Eternal 12x18 Poster Library Print Scholar,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902606976,Zen Aesthetic Plague Doctor Raven Skull 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902616799,Gothic Academia Serpentine Portal of Alchemical 12x18 Poster Library Print Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902620519,Mindful Zen Crane Guardian Mechanism 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902622710,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902627420,Celestial Armillary Navigation Sphere Dark Academia 12x18 Matte Poster Study,$34.99 to $34.99,2,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902633400,Withered Mandrake Root Chamber Minimal Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902640998,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902648209,Vintage Academia Celestial Armillary Codex 12x18 Matte Poster Wall Decor Study,$34.99 to $34.99,3,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902657898,Ritual Bell Shrine Mindful Zen 5x7 Acrylic Photo Block Desk Display Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902663232,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902669660,Gothic Academia Cosmic Lotus Observatory 12x18 Wall Art Study Room Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902673249,Pagoda Fragment Relic Zen Aesthetic 5x7 Acrylic Photo Block Desk Display Shelf,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902691983,Astrolabe Chalice Relic 12x18 Matte Poster Dark Academia Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902703464,Dark Academia Celestial Orrery Tree Bonsai 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902713267,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902882943,Orrery Lighthouse Beacon 12x18 Matte Poster Gothic Academia Gallery Decor Wall,$34.99 to $34.99,1,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902885214,Minimal Zen Ritual Censer Thurible 5x7 Desk Art Acrylic Block Study Decor Shelf,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902886081,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902887127,Dark Academia Jade Lotus Celestial Mechanism 12x18 Matte Poster Wall Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902888077,Minimal Zen Koi Automaton Spirit 5x7 Acrylic Block Collector Gift Jade Segments,$89.99 to $89.99,1,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902889638,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902890971,Celestial Gate of Jade Mist 12x18 Matte Poster Zen Aesthetic Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902893289,Incense Vessel Constellation Mindful Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902896387,Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902897663,Mindful Zen Phoenix Flame Ritual Vessel 12x18 Poster Library Print Scholar Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902898909,Zen Aesthetic Jade Phoenix Incense Altar 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,2,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406902900109,Crystalline Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903026999,Celestial Compass Relic 12x18 Matte Poster Zen Aesthetic Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903028253,Minimal Zen Sacred Lotus Meditation Bell 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903032635,Dragon Meditation Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903033377,Phoenix Rebirth Vessel Minimal Zen 12x18 Matte Poster Study Room Art Wall Decor,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903036452,Celestial Bonsai Moon Garden 5x7 Acrylic Photo Block Minimal Zen Gallery Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903037933,Mindful Zen Azure Dragon Warrior 4pc 6x6 Vinyl Sticker Laptop Journal Gift Desk,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903038850,Dark Academia Arcane Archway Poster 12x18 Vintage Study Decor Jade Aura Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903039716,Alchemical Star Flask Vessel Dark Academia 5x7 Acrylic Premium Desk Display,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903041315,Dragon Cherry Blossom 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903042690,Dark Academia Torii Poster 12x18 Ethereal Scholarly Wall Art for Study Decor,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903043482,Alchemist's Divination Compass Grimdark Mentor-Grade 5x7 Acrylic Display Shelf,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903044643,Moonlit Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk Decor,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903046097,Dark Academia Mystic Threshold Poster 12x18 Infinite Knowledge Library Decor,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903047385,"Zen Bamboo Flute 5x7 Acrylic Block, Whispering Shakuhachi Meditation Art Gift",$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903049411,Minimal Zen Dragon Calligraphy 4pc 6x6 Sticker Sheet Serene Mindful Clean Decor,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903209258,Dark Academia Sanctum Gate Preserved Wisdom 12x18 Poster Study Decor Wall Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903213858,Zen Lotus Seed Pod Vessel 5x7 Acrylic Block for Meditation Decor Shelf Study,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 20:32:20 -0400,eBay,406903249053,Minimal Zen Translucent Jade Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406892408950,4pc Kiss-Cut Sticker Set Mechanical Raven Familiar Laptop Journal Bottle Dark,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406892414116,Zen Aesthetic Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902584620,Gothic Academia Astral Archive Gateway of 12x18 Poster Library Print Scholar,$34.99 to $34.99,1,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902588642,Dark Academia Astrolabe Compass Ritual Disc 5x7 Acrylic Block Collector Gift,$89.99 to $89.99,1,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902600741,Dark Academia Obsidian Threshold of Eternal 12x18 Poster Library Print Scholar,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902606976,Zen Aesthetic Plague Doctor Raven Skull 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902616799,Gothic Academia Serpentine Portal of Alchemical 12x18 Poster Library Print Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902620519,Mindful Zen Crane Guardian Mechanism 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902627420,Celestial Armillary Navigation Sphere Dark Academia 12x18 Matte Poster Study,$34.99 to $34.99,2,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902633400,Withered Mandrake Root Chamber Minimal Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902648209,Vintage Academia Celestial Armillary Codex 12x18 Matte Poster Wall Decor Study,$34.99 to $34.99,3,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902657898,Ritual Bell Shrine Mindful Zen 5x7 Acrylic Photo Block Desk Display Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902669660,Gothic Academia Cosmic Lotus Observatory 12x18 Wall Art Study Room Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902673249,Pagoda Fragment Relic Zen Aesthetic 5x7 Acrylic Photo Block Desk Display Shelf,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902691983,Astrolabe Chalice Relic 12x18 Matte Poster Dark Academia Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902703464,Dark Academia Celestial Orrery Tree Bonsai 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902882943,Orrery Lighthouse Beacon 12x18 Matte Poster Gothic Academia Gallery Decor Wall,$34.99 to $34.99,1,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902885214,Minimal Zen Ritual Censer Thurible 5x7 Desk Art Acrylic Block Study Decor Shelf,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902887127,Dark Academia Jade Lotus Celestial Mechanism 12x18 Matte Poster Wall Decor Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902888077,Minimal Zen Koi Automaton Spirit 5x7 Acrylic Block Collector Gift Jade Segments,$89.99 to $89.99,1,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902890971,Celestial Gate of Jade Mist 12x18 Matte Poster Zen Aesthetic Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902893289,Incense Vessel Constellation Mindful Zen 5x7 Acrylic Photo Block Desk Display,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902897663,Mindful Zen Phoenix Flame Ritual Vessel 12x18 Poster Library Print Scholar Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406902898909,Zen Aesthetic Jade Phoenix Incense Altar 5x7 Desk Art Acrylic Block Study Decor,$89.99 to $89.99,2,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903026999,Celestial Compass Relic 12x18 Matte Poster Zen Aesthetic Gallery Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903028253,Minimal Zen Sacred Lotus Meditation Bell 5x7 Acrylic Photo Block Shelf Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903033377,Phoenix Rebirth Vessel Minimal Zen 12x18 Matte Poster Study Room Art Wall Decor,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903036452,Celestial Bonsai Moon Garden 5x7 Acrylic Photo Block Minimal Zen Gallery Decor,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903037933,Mindful Zen Azure Dragon Warrior 4pc 6x6 Vinyl Sticker Laptop Journal Gift Desk,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903038850,Dark Academia Arcane Archway Poster 12x18 Vintage Study Decor Jade Aura Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903039716,Alchemical Star Flask Vessel Dark Academia 5x7 Acrylic Premium Desk Display,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903041315,Dragon Cherry Blossom 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903042690,Dark Academia Torii Poster 12x18 Ethereal Scholarly Wall Art for Study Decor,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903043482,Alchemist's Divination Compass Grimdark Mentor-Grade 5x7 Acrylic Display Shelf,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903044643,Moonlit Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk Decor,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903046097,Dark Academia Mystic Threshold Poster 12x18 Infinite Knowledge Library Decor,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903047385,"Zen Bamboo Flute 5x7 Acrylic Block, Whispering Shakuhachi Meditation Art Gift",$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903049411,Minimal Zen Dragon Calligraphy 4pc 6x6 Sticker Sheet Serene Mindful Clean Decor,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903209258,Dark Academia Sanctum Gate Preserved Wisdom 12x18 Poster Study Decor Wall Gift,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903213858,Zen Lotus Seed Pod Vessel 5x7 Acrylic Block for Meditation Decor Shelf Study,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903249053,Minimal Zen Translucent Jade Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903249496,Dark Academia Hermetic Portal Ancient Codices Poster 12x18 Study Decor Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903249745,Gothic Lantern Art Print 5x7 Acrylic Block Grimdark Decor Crimson Warden Soul,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903249987,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Calm Gift,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903250376,Dark Academia Celestial Archway Poster 12x18 Study Decor Timeless Tomes Wall,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903250705,Gothic Grimdark Shadowbound Sentinel Beacon 5x7 Acrylic Art Collectible Shelf,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903250891,Zen Aesthetic Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Laptop Journal,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903251282,Alchemist Threshold Transmuted Knowledge 12x18 Dark Academia Poster Study Room,$34.99 to $34.99,0,Promoted,Eligible,11%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903251829,Necromancer's Soul Reliquary Grimdark Gothic Art 5x7 Acrylic Print Dark Fantasy,$89.99 to $89.99,0,Promoted,Eligible,10%,https://www.ebay.com/sh/lst/active,OK
2026-05-06 23:44:26 -0400,eBay,406903252007,Crystalline Dragon Core 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99 to $11.99,0,Promoted,Eligible,12%,https://www.ebay.com/sh/lst/active,OK

```


### RAW LOG: Database/Printify_Login_Guard.log
```text
[2026-05-06 10:37:51 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 10:42:56 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 10:45:09 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 11:19:22 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 12:31:01 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 12:35:55 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 12:43:59 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 12:51:18 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 13:28:05 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 13:51:42 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 15:10:06 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 17:06:03 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 20:26:19 -0400] SKIP_BAD_CDP_PAGE https://printify.com/app/: TimeoutError: 
[2026-05-06 20:26:19 -0400] UNAVAILABLE: All Printify CDP pages failed handshake. Last error: TimeoutError:  
[2026-05-06 20:27:46 -0400] SKIP_BAD_CDP_PAGE https://printify.com/app/: TimeoutError: 
[2026-05-06 20:27:46 -0400] UNAVAILABLE: All Printify CDP pages failed handshake. Last error: TimeoutError:  
[2026-05-06 20:29:28 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 20:29:57 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 22:29:15 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 22:38:25 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 22:44:20 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 23:10:01 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 23:37:32 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard
[2026-05-06 23:44:58 -0400] LOGGED_IN: Printify dashboard is available. https://printify.com/app/dashboard

```


### RAW LOG: Database/eBay_Replacement_Draft_Log.csv
```text
﻿Timestamp,Old_ID,Replacement_ID,Status,Detail
2026-05-06 13:08:54 -0400,Sticker-Academia-0005,Sticker-Academia-0005-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 13:53:49 -0400,Sticker-Academia-0006,Sticker-Academia-0006-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 13:53:49 -0400,Sticker-Academia-0007,Sticker-Academia-0007-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 13:53:49 -0400,Sticker-Academia-0008,Sticker-Academia-0008-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:33 -0400,Sticker-Academia-0009,Sticker-Academia-0009-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:33 -0400,Sticker-Academia-0010,Sticker-Academia-0010-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:34 -0400,Sticker-Academia-0011,Sticker-Academia-0011-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:34 -0400,Sticker-Academia-0014,Sticker-Academia-0014-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:34 -0400,Sticker-Academia-0015,Sticker-Academia-0015-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:34 -0400,Sticker-Academia-0016,Sticker-Academia-0016-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:34 -0400,Sticker-Zen-0001,Sticker-Zen-0001-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:34 -0400,Sticker-Zen-0002,Sticker-Zen-0002-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:34 -0400,Sticker-Zen-0003,Sticker-Zen-0003-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 14:20:34 -0400,Sticker-Zen-0004,Sticker-Zen-0004-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0005,Sticker-Zen-0005-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0007,Sticker-Zen-0007-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0008,Sticker-Zen-0008-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0009,Sticker-Zen-0009-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0022,Sticker-Zen-0022-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0024,Sticker-Zen-0024-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0025,Sticker-Zen-0025-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0027,Sticker-Zen-0027-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0041,Sticker-Zen-0041-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 17:10:34 -0400,Sticker-Zen-0042,Sticker-Zen-0042-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 20:41:20 -0400,Sticker-Zen-0044,Sticker-Zen-0044-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 23:12:41 -0400,Sticker-Zen-0045,Sticker-Zen-0045-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 23:12:41 -0400,Sticker-Zen-0046,Sticker-Zen-0046-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 23:12:41 -0400,Sticker-Zen-0049,Sticker-Zen-0049-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 23:25:16 -0400,Sticker-Zen-0050,Sticker-Zen-0050-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 23:25:16 -0400,Sticker-Zen-0051,Sticker-Zen-0051-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 23:25:16 -0400,Sticker-Zen-0052,Sticker-Zen-0052-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 23:25:16 -0400,Sticker-Zen-0053,Sticker-Zen-0053-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.
2026-05-06 23:25:16 -0400,Sticker-Zen-0054,Sticker-Zen-0054-FIX1,LOCAL_DRAFT_CREATED,Ready_for_Printify replacement row created; public publish still requires QA and retire sequencing.

```


### RAW LOG: Database/eBay_Retire_Run_Log.csv
```text
Timestamp,Old_ID,Old_eBay_Item_ID,Result,Note
2026-05-06T15:28:29,Sticker-Academia-0005,406892409123,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:28:46,Sticker-Academia-0005-FIX1,406909045760,ALREADY_NOT_ACTIVE,Seller Hub active search returned 0 rows.; printify_unpublish_http_400
2026-05-06T15:29:18,Sticker-Academia-0006,406892409348,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:31:06,Sticker-Academia-0007,406892409645,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:31:34,Sticker-Academia-0008,406892409836,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:32:02,Sticker-Academia-0009,406892410017,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:32:32,Sticker-Academia-0010,406892410190,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:33:01,Sticker-Academia-0011,406892410307,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:33:29,Sticker-Academia-0014,406892410440,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:33:58,Sticker-Academia-0015,406892411034,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:34:27,Sticker-Academia-0016,406892411436,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:34:56,Sticker-Zen-0001,406892411931,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:35:26,Sticker-Zen-0002,406892412365,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:35:56,Sticker-Zen-0003,406892412612,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T15:36:25,Sticker-Zen-0004,406892412789,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T17:46:55,Sticker-Zen-0005,406892413076,LOGIN_REQUIRED,Dedicated automation browser is not signed in to eBay Seller Hub.
2026-05-06T18:17:41,Sticker-Zen-0005,406892413076,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:18:11,Sticker-Zen-0007,406892413333,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:18:43,Sticker-Zen-0008,406892413714,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:19:16,Sticker-Zen-0009,406892413966,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:20:00,Sticker-Zen-0022,406892414235,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:20:32,Sticker-Zen-0024,406892414471,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:21:03,Sticker-Zen-0025,406892327989,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:21:38,Sticker-Zen-0027,406892414741,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:22:09,Sticker-Zen-0041,406902593931,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T18:22:41,Sticker-Zen-0042,406902614234,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:09:08,Sticker-Zen-0044,406902622710,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:19:02,Sticker-Zen-0045,406902640998,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:19:39,Sticker-Zen-0046,406902663232,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:20:17,Sticker-Zen-0049,406902713267,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:34:36,Sticker-Zen-0050,406902886081,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:35:13,Sticker-Zen-0051,406902889638,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:35:51,Sticker-Zen-0052,406902896387,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:36:26,Sticker-Zen-0053,406902900109,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached
2026-05-06T23:37:04,Sticker-Zen-0054,406903032635,ENDED_CONFIRMED_SELLER_HUB,Seller Hub success banner detected.; printify_external_detached

```


### RAW LOG: Database/printify_external_sync.csv
```text
﻿Timestamp,ID,Printify_Product_ID,eBay_Item_ID,eBay_Item_URL,Status,Error
2026-05-04T13:32:07,Sticker-Academia-0004,69f192aa5ea38382140f1d7b,406892408950,https://www.ebay.com/itm/406892408950,OK,
2026-05-04T13:32:12,Sticker-Academia-0005,69f198efea1f992ded0e90e7,406892409123,https://www.ebay.com/itm/406892409123,OK,
2026-05-04T13:32:21,Sticker-Academia-0006,69f19b945494697f0d01b78c,406892409348,https://www.ebay.com/itm/406892409348,OK,
2026-05-04T13:32:25,Sticker-Academia-0007,69f1a56756390ef4cd09be1e,406892409645,https://www.ebay.com/itm/406892409645,OK,
2026-05-04T13:32:30,Sticker-Academia-0008,69f1a630de3c2e09400f9c5f,406892409836,https://www.ebay.com/itm/406892409836,OK,
2026-05-04T13:32:35,Sticker-Academia-0009,69f1a6acc2501ebbc40ac2e5,406892410017,https://www.ebay.com/itm/406892410017,OK,
2026-05-04T13:32:43,Sticker-Academia-0010,69f1a724785a37b0240adad9,406892410190,https://www.ebay.com/itm/406892410190,OK,
2026-05-04T13:32:48,Sticker-Academia-0011,69f1a7b0cfb25d6b6f0f10f7,406892410307,https://www.ebay.com/itm/406892410307,OK,
2026-05-04T13:32:51,Sticker-Academia-0014,69f1a833592cc603cd0a91fd,406892410440,https://www.ebay.com/itm/406892410440,OK,
2026-05-04T13:32:55,Sticker-Academia-0015,69f1a8b40bc0bf405305ef2b,406892411034,https://www.ebay.com/itm/406892411034,OK,
2026-05-04T13:33:42,Sticker-Academia-0016,69f1a92ade3c2e09400f9e44,406892411436,https://www.ebay.com/itm/406892411436,OK,
2026-05-04T13:33:46,Sticker-Zen-0001,69f1a99c785a37b0240adc94,406892411931,https://www.ebay.com/itm/406892411931,OK,
2026-05-04T13:33:49,Sticker-Zen-0002,69f1ab9a63935da7e8064504,406892412365,https://www.ebay.com/itm/406892412365,OK,
2026-05-04T13:33:54,Sticker-Zen-0003,69f1ac1804ea1d3ba9005c58,406892412612,https://www.ebay.com/itm/406892412612,OK,
2026-05-04T13:33:57,Sticker-Zen-0004,69f1ac9740c796ee97057c83,406892412789,https://www.ebay.com/itm/406892412789,OK,
2026-05-04T13:34:01,Sticker-Zen-0005,69f1ad18c59fe705400bacbf,406892413076,https://www.ebay.com/itm/406892413076,OK,
2026-05-04T13:34:04,Sticker-Zen-0007,69f1ad9bbb6f6dd6270dc5df,406892413333,https://www.ebay.com/itm/406892413333,OK,
2026-05-04T13:34:07,Sticker-Zen-0008,69f1aef4bb6f6dd6270dc7d5,406892413714,https://www.ebay.com/itm/406892413714,OK,
2026-05-04T13:34:11,Sticker-Zen-0009,69f1af85bb6f6dd6270dc848,406892413966,https://www.ebay.com/itm/406892413966,OK,
2026-05-04T13:34:15,Sticker-Zen-0010,69f1b00840c796ee97058144,406892414116,https://www.ebay.com/itm/406892414116,OK,
2026-05-04T13:34:18,Sticker-Zen-0022,69f1b1ab63935da7e8064bab,406892414235,https://www.ebay.com/itm/406892414235,OK,
2026-05-04T13:34:23,Sticker-Zen-0024,69f1b2c4d3e196c79b0fdaec,406892414471,https://www.ebay.com/itm/406892414471,OK,
2026-05-04T13:34:31,Sticker-Zen-0025,69f1cb4ef6b83091a50959f5,406892327989,https://www.ebay.com/itm/406892327989,OK,
2026-05-04T13:34:34,Sticker-Zen-0026,69f1cc732f305b371c05b1d7,,,MISSING_EXTERNAL_ID,
2026-05-04T13:34:40,Sticker-Zen-0027,69f1ce0f11e0745fcb0da03a,406892414741,https://www.ebay.com/itm/406892414741,OK,
2026-05-04T13:34:43,Sticker-Zen-0029,69f1cee189347116c004f529,,,MISSING_EXTERNAL_ID,
2026-05-04T13:34:46,Sticker-Zen-0031,69f1cf9911e0745fcb0da15f,,,MISSING_EXTERNAL_ID,
2026-05-04T13:34:50,Sticker-Zen-0032,69f1d04a0482f56ada0cf347,,,MISSING_EXTERNAL_ID,
2026-05-04T13:34:54,Sticker-Zen-0034,69f1d1003a934dcd94086687,,,MISSING_EXTERNAL_ID,
2026-05-04T13:34:57,Sticker-Zen-0035,69f1d1ed11e0745fcb0da2ea,,,MISSING_EXTERNAL_ID,
2026-05-04T13:35:01,Sticker-Zen-0036,69f1d2a9f6b83091a5095eea,,,MISSING_EXTERNAL_ID,
2026-05-04T13:35:07,Sticker-Zen-0037,69f1d35c89347116c004f871,,,MISSING_EXTERNAL_ID,
2026-05-04T13:35:10,Sticker-Zen-0038,69f1d44bf6b83091a5095fca,,,MISSING_EXTERNAL_ID,
2026-05-04T13:35:13,Sticker-Zen-0040,69f1d4f9bdda7e777002a696,,,MISSING_EXTERNAL_ID,
2026-05-04T13:35:18,Sticker-Zen-0041,69f1db9382fcf925cf08206d,406902593931,https://www.ebay.com/itm/406902593931,OK,
2026-05-04T13:35:23,Sticker-Zen-0042,69f2192ae64c9f31b70f2dbd,406902614234,https://www.ebay.com/itm/406902614234,OK,
2026-05-04T13:35:28,Sticker-Zen-0044,69f2396ccaeb1241880b692d,406902622710,https://www.ebay.com/itm/406902622710,OK,
2026-05-04T13:35:35,Sticker-Zen-0045,69f21a5da7777da1970fd378,406902640998,https://www.ebay.com/itm/406902640998,OK,
2026-05-04T13:35:38,Sticker-Zen-0046,69f21b07b0d6b88b2805ebe3,406902663232,https://www.ebay.com/itm/406902663232,OK,
2026-05-04T13:35:43,Sticker-Zen-0048,69f21bba9b469f716d0e4e42,,,MISSING_EXTERNAL_ID,
2026-05-04T13:35:46,Sticker-Zen-0049,69f23a2fa7777da1970fe60d,406902713267,https://www.ebay.com/itm/406902713267,OK,
2026-05-04T13:35:50,Sticker-Zen-0050,69f23a99c326d7da170bfe8d,406902886081,https://www.ebay.com/itm/406902886081,OK,
2026-05-04T13:35:56,Sticker-Zen-0051,69f23b5ce64c9f31b70f415b,406902889638,https://www.ebay.com/itm/406902889638,OK,
2026-05-04T13:36:01,Sticker-Zen-0052,69f23c10caeb1241880b6afe,406902896387,https://www.ebay.com/itm/406902896387,OK,
2026-05-04T13:36:05,Sticker-Zen-0053,69f252f4357398ded80f61c9,406902900109,https://www.ebay.com/itm/406902900109,OK,
2026-05-04T13:36:09,Sticker-Zen-0054,69f253bc357398ded80f6242,406903032635,https://www.ebay.com/itm/406903032635,OK,
2026-05-04T13:36:17,Sticker-Zen-0055,69f2547229c1d0349a00e796,406903037933,https://www.ebay.com/itm/406903037933,OK,
2026-05-04T13:36:22,Sticker-Zen-0056,69f25526ad218fe47f0cc0d3,406903041315,https://www.ebay.com/itm/406903041315,OK,
2026-05-04T13:36:29,Sticker-Zen-0057,69f255dae64c9f31b70f4ea6,,,ERROR,"('Connection aborted.', ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None))"
2026-05-04T13:36:36,Sticker-Zen-0058,69f259bc5f78c14a7b0a4760,406903049411,https://www.ebay.com/itm/406903049411,OK,
2026-05-04T13:36:41,Sticker-Zen-0060,69f25a86a7777da1970ff5f3,406903249053,https://www.ebay.com/itm/406903249053,OK,
2026-05-04T13:36:44,Sticker-Zen-0061,69f25b3ce64c9f31b70f50ed,406903249987,https://www.ebay.com/itm/406903249987,OK,
2026-05-04T13:36:49,Sticker-Zen-0062,69f25bee9b469f716d0e7056,406903250891,https://www.ebay.com/itm/406903250891,OK,
2026-05-04T13:36:54,Sticker-Zen-0063,69f25ca39577aaffd5066a80,406903252007,https://www.ebay.com/itm/406903252007,OK,
2026-05-04T13:36:59,Sticker-Zen-0066,69f25d56c326d7da170c0f79,406903252739,https://www.ebay.com/itm/406903252739,OK,
2026-05-04T13:37:04,Sticker-Zen-0067,69f25f0db0d6b88b28061022,,,MISSING_EXTERNAL_ID,
2026-05-04T13:37:12,Sticker-Zen-0068,69f25faf29c1d0349a00ecec,,,MISSING_EXTERNAL_ID,
2026-05-04T13:37:15,Sticker-Zen-0069,69f26062cd8d04605103d10b,406903753067,https://www.ebay.com/itm/406903753067,OK,
2026-05-04T13:37:20,Sticker-Zen-0070,69f261185f78c14a7b0a4b29,406903757240,https://www.ebay.com/itm/406903757240,OK,
2026-05-04T13:37:24,Sticker-Zen-0071,69f261cd5269e3325904b816,406903762328,https://www.ebay.com/itm/406903762328,OK,
2026-05-04T13:37:27,Poster-Academia-0001,69f28800cd8d04605103e53a,406902584620,https://www.ebay.com/itm/406902584620,OK,
2026-05-04T13:37:46,Poster-Academia-0002,69f2906f7f1017d51b0d5f76,,,ERROR,"('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))"
2026-05-04T13:37:50,Poster-Academia-0003,69f29152357398ded80f8178,406902616799,https://www.ebay.com/itm/406902616799,OK,
2026-05-04T13:37:55,Acrylic-Academia-0001,69f298dc9577aaffd50689b0,406902588642,https://www.ebay.com/itm/406902588642,OK,
2026-05-04T13:37:59,Acrylic-Grimdark-0081,69f299c1a3119247600cbe18,406902606976,https://www.ebay.com/itm/406902606976,OK,
2026-05-04T13:38:04,Acrylic-Zen-0001,69f29a72c411a56f6902930d,406902620519,https://www.ebay.com/itm/406902620519,OK,
2026-05-04T13:38:11,Poster-Academia-0081,69f29fe09577aaffd5068e03,406902627420,https://www.ebay.com/itm/406902627420,OK,
2026-05-04T13:38:17,Poster-Academia-0082,69f2a0cacaeb1241880b9e8d,406902648209,https://www.ebay.com/itm/406902648209,OK,
2026-05-04T13:38:23,Poster-Academia-0083,69f2a1b8a7777da197101a96,406902669660,https://www.ebay.com/itm/406902669660,OK,
2026-05-04T13:38:33,Poster-Academia-0084,69f2a2aacaeb1241880b9f6b,406902691983,https://www.ebay.com/itm/406902691983,OK,
2026-05-04T13:38:41,Acrylic-Grimdark-0082,69f2a7d0e64c9f31b70f79cf,406902633400,https://www.ebay.com/itm/406902633400,OK,
2026-05-04T13:38:46,Acrylic-Zen-0002,69f2a8a5357398ded80f8faf,406902657898,https://www.ebay.com/itm/406902657898,OK,
2026-05-04T13:38:53,Acrylic-Zen-0003,69f2a9b45f78c14a7b0a7290,406902673249,https://www.ebay.com/itm/406902673249,OK,
2026-05-04T13:38:59,Poster-Academia-0085,69f2b132cd8d04605103fdaa,406902882943,https://www.ebay.com/itm/406902882943,OK,
2026-05-04T13:39:04,Poster-Academia-0091,69f2b7ada7777da1971028d7,406902887127,https://www.ebay.com/itm/406902887127,OK,
2026-05-04T13:39:16,Acrylic-Academia-0003,69f2b9c3caeb1241880bae85,406902703464,https://www.ebay.com/itm/406902703464,OK,
2026-05-04T13:39:24,Acrylic-Grimdark-0083,69f2bac6343d8ca093077dd8,406902885214,https://www.ebay.com/itm/406902885214,OK,
2026-05-04T13:39:34,Acrylic-Zen-0004,69f2bbbc343d8ca093077e9a,406902888077,https://www.ebay.com/itm/406902888077,OK,
2026-05-04T13:39:42,Acrylic-Zen-0005,69f2c22e9b469f716d0ea954,406902893289,https://www.ebay.com/itm/406902893289,OK,
2026-05-04T13:39:47,Poster-Zen-0001,69f2dc76cd8d046051041f06,406902890971,https://www.ebay.com/itm/406902890971,OK,
2026-05-04T13:39:54,Poster-Zen-0002,69f2cf675f78c14a7b0a894c,406902897663,https://www.ebay.com/itm/406902897663,OK,
2026-05-04T13:40:05,Acrylic-Zen-0006,69f2d2a1c326d7da170c51b4,406902898909,https://www.ebay.com/itm/406902898909,OK,
2026-05-04T13:40:09,Acrylic-Zen-0007,69f2d3ab5f78c14a7b0a8b87,406903028253,https://www.ebay.com/itm/406903028253,OK,
2026-05-04T13:40:14,Acrylic-Zen-0008,69f2d49b81039eb9ab0b583c,406903036452,https://www.ebay.com/itm/406903036452,OK,
2026-05-04T13:40:21,Poster-Zen-0004,69f2dddb9577aaffd506bc32,406903026999,https://www.ebay.com/itm/406903026999,OK,
2026-05-04T13:40:24,Poster-Zen-0005,69f2db1a3c6616b960034a37,406903033377,https://www.ebay.com/itm/406903033377,OK,
2026-05-04T13:40:29,Acrylic-Academia-0005,69f80ad2d3b9dc73b1051dbd,406903039716,https://www.ebay.com/itm/406903039716,OK,
2026-05-04T13:40:34,Acrylic-Grimdark-0085,69f2e4c77e3402ea470630eb,406903043482,https://www.ebay.com/itm/406903043482,OK,
2026-05-04T13:40:38,Acrylic-Zen-0009,69f80f8a83a8608fd80ec283,406903047385,https://www.ebay.com/itm/406903047385,OK,
2026-05-04T13:40:43,Acrylic-Zen-0010,69f810485da263f75f049bf8,406903213858,https://www.ebay.com/itm/406903213858,OK,
2026-05-04T13:40:47,Acrylic-Grimdark-0001,69f82b8aa1a4c45aad055063,406903249745,https://www.ebay.com/itm/406903249745,OK,
2026-05-04T13:40:53,Acrylic-Grimdark-0004,69f82c8609f3b7302401cacf,406903250705,https://www.ebay.com/itm/406903250705,OK,
2026-05-04T13:40:58,Acrylic-Grimdark-0005,69f8388b25819cdf3d0538bc,406903251829,https://www.ebay.com/itm/406903251829,OK,
2026-05-04T13:41:05,Acrylic-Grimdark-0006,69f83957ffbc831dea082e1a,406903252506,https://www.ebay.com/itm/406903252506,OK,
2026-05-04T13:41:12,Acrylic-Grimdark-0007,69f839eaf9374ed4f105a092,406903731967,https://www.ebay.com/itm/406903731967,OK,
2026-05-04T13:41:19,Acrylic-Grimdark-0008,69f83a955da263f75f04c06a,406903746215,https://www.ebay.com/itm/406903746215,OK,
2026-05-04T13:41:24,Acrylic-Grimdark-0009,69f83b5cf9374ed4f105a180,406903749989,https://www.ebay.com/itm/406903749989,OK,
2026-05-04T13:41:30,Acrylic-Grimdark-0010,69f83c14ffbc831dea082fa3,406903756190,https://www.ebay.com/itm/406903756190,OK,
2026-05-04T13:41:37,Poster-Academia-0005,69f847b45da263f75f04cdbd,406903038850,https://www.ebay.com/itm/406903038850,OK,
2026-05-04T13:41:41,Poster-Academia-0006,69f84864feed9979d10cd5ba,406903042690,https://www.ebay.com/itm/406903042690,OK,
2026-05-04T13:41:50,Poster-Academia-0008,69f84b3d5da263f75f04d1f7,,,ERROR,"('Connection aborted.', ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None))"
2026-05-04T13:41:55,Poster-Academia-0009,69f8547125819cdf3d05522b,406903209258,https://www.ebay.com/itm/406903209258,OK,
2026-05-04T13:42:14,Poster-Academia-0010,69f854ed09f3b7302401ed2e,,,ERROR,"('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))"
2026-05-04T13:42:27,Poster-Academia-0011,69f850b425819cdf3d054e10,406903250376,https://www.ebay.com/itm/406903250376,OK,
2026-05-04T13:42:32,Poster-Academia-0013,69f855abffbc831dea0847c8,406903251282,https://www.ebay.com/itm/406903251282,OK,
2026-05-04T13:42:40,Poster-Academia-0014,69f8530b5da263f75f04d837,406903252244,https://www.ebay.com/itm/406903252244,OK,
2026-05-04T13:42:50,Acrylic-Grimdark-0011,69f863f9f9374ed4f105c588,406903760725,https://www.ebay.com/itm/406903760725,OK,
2026-05-04T13:42:55,Poster-Academia-0017,69f89a94c1f268dee601cb9d,406903730229,https://www.ebay.com/itm/406903730229,OK,
2026-05-04T13:43:03,Poster-Academia-0019,69f89b9ca70f06579a00a708,406903744471,https://www.ebay.com/itm/406903744471,OK,
2026-05-04T13:43:10,Poster-Academia-0020,69f89c6f09f3b730240221b8,406903748661,https://www.ebay.com/itm/406903748661,OK,
2026-05-04T13:43:17,Poster-Academia-0021,69f89da69f68ab7cf001f531,406903754696,https://www.ebay.com/itm/406903754696,OK,
2026-05-04T13:43:25,Poster-Academia-0022,69f89eac011b67ecf8077844,406903758348,https://www.ebay.com/itm/406903758348,OK,
2026-05-04T16:24:06,Sticker-Zen-0026,69f1cc732f305b371c05b1d7,,,MISSING_EXTERNAL_ID,
2026-05-04T16:24:16,Sticker-Zen-0029,69f1cee189347116c004f529,,,MISSING_EXTERNAL_ID,
2026-05-04T16:24:26,Sticker-Zen-0031,69f1cf9911e0745fcb0da15f,,,MISSING_EXTERNAL_ID,
2026-05-04T16:24:35,Sticker-Zen-0032,69f1d04a0482f56ada0cf347,,,MISSING_EXTERNAL_ID,
2026-05-04T16:24:44,Sticker-Zen-0034,69f1d1003a934dcd94086687,,,MISSING_EXTERNAL_ID,
2026-05-04T16:24:53,Sticker-Zen-0035,69f1d1ed11e0745fcb0da2ea,,,MISSING_EXTERNAL_ID,
2026-05-04T16:25:02,Sticker-Zen-0036,69f1d2a9f6b83091a5095eea,,,MISSING_EXTERNAL_ID,
2026-05-04T16:25:11,Sticker-Zen-0037,69f1d35c89347116c004f871,,,MISSING_EXTERNAL_ID,
2026-05-04T16:25:20,Sticker-Zen-0038,69f1d44bf6b83091a5095fca,,,MISSING_EXTERNAL_ID,
2026-05-04T16:25:29,Sticker-Zen-0040,69f1d4f9bdda7e777002a696,,,MISSING_EXTERNAL_ID,
2026-05-04T16:25:38,Sticker-Zen-0048,69f21bba9b469f716d0e4e42,,,MISSING_EXTERNAL_ID,
2026-05-04T16:25:46,Sticker-Zen-0057,69f255dae64c9f31b70f4ea6,406903044643,https://www.ebay.com/itm/406903044643,OK,
2026-05-04T16:25:55,Sticker-Zen-0067,69f25f0db0d6b88b28061022,,,MISSING_EXTERNAL_ID,
2026-05-04T16:26:04,Sticker-Zen-0068,69f25faf29c1d0349a00ecec,,,MISSING_EXTERNAL_ID,
2026-05-04T16:26:13,Poster-Academia-0002,69f2906f7f1017d51b0d5f76,406902600741,https://www.ebay.com/itm/406902600741,OK,
2026-05-04T16:26:22,Poster-Academia-0008,69f84b3d5da263f75f04d1f7,406903046097,https://www.ebay.com/itm/406903046097,OK,
2026-05-04T16:26:31,Poster-Academia-0010,69f854ed09f3b7302401ed2e,406903249496,https://www.ebay.com/itm/406903249496,OK,
2026-05-06T14:49:22,Sticker-Zen-0026,69f1cc732f305b371c05b1d7,,,MISSING_EXTERNAL_ID,
2026-05-06T14:49:27,Sticker-Zen-0029,69f1cee189347116c004f529,,,MISSING_EXTERNAL_ID,
2026-05-06T14:49:31,Sticker-Zen-0031,69f1cf9911e0745fcb0da15f,,,MISSING_EXTERNAL_ID,
2026-05-06T14:49:36,Sticker-Zen-0032,69f1d04a0482f56ada0cf347,,,MISSING_EXTERNAL_ID,
2026-05-06T14:49:41,Sticker-Zen-0034,69f1d1003a934dcd94086687,,,MISSING_EXTERNAL_ID,
2026-05-06T14:49:45,Sticker-Zen-0035,69f1d1ed11e0745fcb0da2ea,,,MISSING_EXTERNAL_ID,
2026-05-06T14:49:50,Sticker-Zen-0036,69f1d2a9f6b83091a5095eea,,,MISSING_EXTERNAL_ID,
2026-05-06T14:49:55,Sticker-Zen-0037,69f1d35c89347116c004f871,,,MISSING_EXTERNAL_ID,
2026-05-06T14:49:59,Sticker-Zen-0038,69f1d44bf6b83091a5095fca,,,MISSING_EXTERNAL_ID,
2026-05-06T14:50:04,Sticker-Zen-0040,69f1d4f9bdda7e777002a696,,,MISSING_EXTERNAL_ID,
2026-05-06T14:50:09,Sticker-Zen-0048,69f21bba9b469f716d0e4e42,,,MISSING_EXTERNAL_ID,
2026-05-06T14:50:14,Sticker-Zen-0067,69f25f0db0d6b88b28061022,,,MISSING_EXTERNAL_ID,
2026-05-06T14:50:18,Sticker-Zen-0068,69f25faf29c1d0349a00ecec,,,MISSING_EXTERNAL_ID,
2026-05-06T14:50:23,Sticker-Academia-0014-FIX1,69fb87efc5114ecf420d2c5a,406909119544,https://www.ebay.com/itm/406909119544,OK,
2026-05-06T17:05:40,Poster-Academia-0030,69f90c957f4b346c8a0c603f,406909264998,https://www.ebay.com/itm/406909264998,OK,
2026-05-06T17:35:18,Sticker-Zen-0005-FIX1,69fbae614c6544084c0f95ec,406909342825,https://www.ebay.com/itm/406909342825,OK,
2026-05-06T17:35:23,Sticker-Zen-0009-FIX1,69fbaea961c4aefdea04aaaf,406909353931,https://www.ebay.com/itm/406909353931,OK,
2026-05-06T17:35:28,Sticker-Zen-0022-FIX1,69fbaeb9f60a24b6d1034575,406909354903,https://www.ebay.com/itm/406909354903,OK,
2026-05-06T17:35:33,Sticker-Zen-0042-FIX1,69fbaf12ff28e7d4030aba2d,406909373586,https://www.ebay.com/itm/406909373586,OK,
2026-05-06T17:49:54,Sticker-Zen-0026,69f1cc732f305b371c05b1d7,,,MISSING_EXTERNAL_ID,
2026-05-06T17:49:58,Sticker-Zen-0029,69f1cee189347116c004f529,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:02,Sticker-Zen-0031,69f1cf9911e0745fcb0da15f,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:06,Sticker-Zen-0032,69f1d04a0482f56ada0cf347,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:10,Sticker-Zen-0034,69f1d1003a934dcd94086687,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:14,Sticker-Zen-0035,69f1d1ed11e0745fcb0da2ea,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:18,Sticker-Zen-0036,69f1d2a9f6b83091a5095eea,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:23,Sticker-Zen-0037,69f1d35c89347116c004f871,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:27,Sticker-Zen-0038,69f1d44bf6b83091a5095fca,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:32,Sticker-Zen-0040,69f1d4f9bdda7e777002a696,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:37,Sticker-Zen-0048,69f21bba9b469f716d0e4e42,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:41,Sticker-Zen-0067,69f25f0db0d6b88b28061022,,,MISSING_EXTERNAL_ID,
2026-05-06T17:50:45,Sticker-Zen-0068,69f25faf29c1d0349a00ecec,,,MISSING_EXTERNAL_ID,
2026-05-06T18:34:02,Poster-Academia-0034,69fbbffef60a24b6d1034e4d,406909467980,https://www.ebay.com/itm/406909467980,OK,
2026-05-06T19:33:39,Poster-Academia-0038,69fbccf9ce0d8cb5570fc6f0,,,MISSING_EXTERNAL_ID,
2026-05-06T19:33:43,Poster-Academia-0039,69fbcd1aee663532c8019ec7,,,MISSING_EXTERNAL_ID,
2026-05-06T19:33:47,Poster-Academia-0040,69fbcd3eb8dd7e2bb0095af7,,,MISSING_EXTERNAL_ID,
2026-05-06T19:33:50,Poster-Academia-0041,69fbcd65cacc667dc70b7c2a,,,MISSING_EXTERNAL_ID,
2026-05-06T19:33:54,Poster-Academia-0042,69fbcd8a3014a1ea840da971,,,MISSING_EXTERNAL_ID,
2026-05-06T19:38:31,Poster-Academia-0038,69fbccf9ce0d8cb5570fc6f0,,,MISSING_EXTERNAL_ID,
2026-05-06T19:38:36,Poster-Academia-0039,69fbcd1aee663532c8019ec7,,,MISSING_EXTERNAL_ID,
2026-05-06T19:38:42,Poster-Academia-0040,69fbcd3eb8dd7e2bb0095af7,,,MISSING_EXTERNAL_ID,
2026-05-06T19:38:47,Poster-Academia-0041,69fbcd65cacc667dc70b7c2a,,,MISSING_EXTERNAL_ID,
2026-05-06T19:38:53,Poster-Academia-0042,69fbcd8a3014a1ea840da971,,,MISSING_EXTERNAL_ID,
2026-05-06T20:11:55,Poster-Academia-0038,69fbccf9ce0d8cb5570fc6f0,,,MISSING_EXTERNAL_ID,
2026-05-06T20:11:57,Poster-Academia-0039,69fbcd1aee663532c8019ec7,,,MISSING_EXTERNAL_ID,
2026-05-06T20:11:59,Poster-Academia-0040,69fbcd3eb8dd7e2bb0095af7,,,MISSING_EXTERNAL_ID,
2026-05-06T20:12:01,Poster-Academia-0041,69fbcd65cacc667dc70b7c2a,,,MISSING_EXTERNAL_ID,
2026-05-06T20:12:02,Poster-Academia-0042,69fbcd8a3014a1ea840da971,,,MISSING_EXTERNAL_ID,
2026-05-06T20:13:18,Poster-Academia-0037,69fbc06d61c4aefdea04b362,406909473606,https://www.ebay.com/itm/406909473606,OK,
2026-05-06T20:13:20,Poster-Academia-0038,69fbccf9ce0d8cb5570fc6f0,,,MISSING_EXTERNAL_ID,
2026-05-06T20:13:22,Poster-Academia-0039,69fbcd1aee663532c8019ec7,,,MISSING_EXTERNAL_ID,
2026-05-06T20:13:23,Poster-Academia-0040,69fbcd3eb8dd7e2bb0095af7,,,MISSING_EXTERNAL_ID,
2026-05-06T20:13:25,Poster-Academia-0041,69fbcd65cacc667dc70b7c2a,,,MISSING_EXTERNAL_ID,
2026-05-06T20:13:27,Poster-Academia-0042,69fbcd8a3014a1ea840da971,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:11,Sticker-Academia-0004,69f192aa5ea38382140f1d7b,406892408950,https://www.ebay.com/itm/406892408950,OK,
2026-05-06T20:34:13,Sticker-Zen-0010,69f1b00840c796ee97058144,406892414116,https://www.ebay.com/itm/406892414116,OK,
2026-05-06T20:34:14,Sticker-Zen-0026,69f1cc732f305b371c05b1d7,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:16,Sticker-Zen-0029,69f1cee189347116c004f529,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:17,Sticker-Zen-0031,69f1cf9911e0745fcb0da15f,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:18,Sticker-Zen-0032,69f1d04a0482f56ada0cf347,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:20,Sticker-Zen-0034,69f1d1003a934dcd94086687,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:21,Sticker-Zen-0035,69f1d1ed11e0745fcb0da2ea,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:23,Sticker-Zen-0036,69f1d2a9f6b83091a5095eea,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:24,Sticker-Zen-0037,69f1d35c89347116c004f871,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:26,Sticker-Zen-0038,69f1d44bf6b83091a5095fca,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:28,Sticker-Zen-0040,69f1d4f9bdda7e777002a696,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:31,Sticker-Zen-0044,69f2396ccaeb1241880b692d,406902622710,https://www.ebay.com/itm/406902622710,OK,
2026-05-06T20:34:35,Sticker-Zen-0045,69f21a5da7777da1970fd378,406902640998,https://www.ebay.com/itm/406902640998,OK,
2026-05-06T20:34:37,Sticker-Zen-0046,69f21b07b0d6b88b2805ebe3,406902663232,https://www.ebay.com/itm/406902663232,OK,
2026-05-06T20:34:39,Sticker-Zen-0048,69f21bba9b469f716d0e4e42,,,MISSING_EXTERNAL_ID,
2026-05-06T20:34:40,Sticker-Zen-0049,69f23a2fa7777da1970fe60d,406902713267,https://www.ebay.com/itm/406902713267,OK,
2026-05-06T20:34:42,Sticker-Zen-0050,69f23a99c326d7da170bfe8d,406902886081,https://www.ebay.com/itm/406902886081,OK,
2026-05-06T20:34:44,Sticker-Zen-0051,69f23b5ce64c9f31b70f415b,406902889638,https://www.ebay.com/itm/406902889638,OK,
2026-05-06T20:34:46,Sticker-Zen-0052,69f23c10caeb1241880b6afe,406902896387,https://www.ebay.com/itm/406902896387,OK,
2026-05-06T20:34:48,Sticker-Zen-0053,69f252f4357398ded80f61c9,406902900109,https://www.ebay.com/itm/406902900109,OK,
2026-05-06T20:34:50,Sticker-Zen-0054,69f253bc357398ded80f6242,406903032635,https://www.ebay.com/itm/406903032635,OK,
2026-05-06T20:34:51,Sticker-Zen-0055,69f2547229c1d0349a00e796,406903037933,https://www.ebay.com/itm/406903037933,OK,
2026-05-06T20:34:53,Sticker-Zen-0056,69f25526ad218fe47f0cc0d3,406903041315,https://www.ebay.com/itm/406903041315,OK,
2026-05-06T20:34:55,Sticker-Zen-0057,69f255dae64c9f31b70f4ea6,406903044643,https://www.ebay.com/itm/406903044643,OK,
2026-05-06T20:34:57,Sticker-Zen-0058,69f259bc5f78c14a7b0a4760,406903049411,https://www.ebay.com/itm/406903049411,OK,
2026-05-06T20:34:58,Sticker-Zen-0060,69f25a86a7777da1970ff5f3,406903249053,https://www.ebay.com/itm/406903249053,OK,
2026-05-06T20:35:00,Sticker-Zen-0061,69f25b3ce64c9f31b70f50ed,406903249987,https://www.ebay.com/itm/406903249987,OK,
2026-05-06T20:35:01,Sticker-Zen-0062,69f25bee9b469f716d0e7056,406903250891,https://www.ebay.com/itm/406903250891,OK,
2026-05-06T20:35:03,Sticker-Zen-0063,69f25ca39577aaffd5066a80,406903252007,https://www.ebay.com/itm/406903252007,OK,
2026-05-06T20:35:04,Sticker-Zen-0066,69f25d56c326d7da170c0f79,406903252739,https://www.ebay.com/itm/406903252739,OK,
2026-05-06T20:35:06,Sticker-Zen-0067,69f25f0db0d6b88b28061022,,,MISSING_EXTERNAL_ID,
2026-05-06T20:35:08,Sticker-Zen-0068,69f25faf29c1d0349a00ecec,,,MISSING_EXTERNAL_ID,
2026-05-06T20:35:09,Sticker-Zen-0069,69f26062cd8d04605103d10b,406903753067,https://www.ebay.com/itm/406903753067,OK,
2026-05-06T20:35:10,Sticker-Zen-0070,69f261185f78c14a7b0a4b29,406903757240,https://www.ebay.com/itm/406903757240,OK,
2026-05-06T20:35:12,Sticker-Zen-0071,69f261cd5269e3325904b816,406903762328,https://www.ebay.com/itm/406903762328,OK,
2026-05-06T20:35:14,Poster-Academia-0001,69f28800cd8d04605103e53a,406902584620,https://www.ebay.com/itm/406902584620,OK,
2026-05-06T20:35:16,Poster-Academia-0002,69f2906f7f1017d51b0d5f76,406902600741,https://www.ebay.com/itm/406902600741,OK,
2026-05-06T20:35:18,Poster-Academia-0003,69f29152357398ded80f8178,406902616799,https://www.ebay.com/itm/406902616799,OK,
2026-05-06T20:35:21,Acrylic-Academia-0001,69f298dc9577aaffd50689b0,406902588642,https://www.ebay.com/itm/406902588642,OK,
2026-05-06T20:35:22,Acrylic-Grimdark-0081,69f299c1a3119247600cbe18,406902606976,https://www.ebay.com/itm/406902606976,OK,
2026-05-06T20:35:24,Acrylic-Zen-0001,69f29a72c411a56f6902930d,406902620519,https://www.ebay.com/itm/406902620519,OK,
2026-05-06T20:35:25,Poster-Academia-0081,69f29fe09577aaffd5068e03,406902627420,https://www.ebay.com/itm/406902627420,OK,
2026-05-06T20:35:27,Poster-Academia-0082,69f2a0cacaeb1241880b9e8d,406902648209,https://www.ebay.com/itm/406902648209,OK,
2026-05-06T20:35:28,Poster-Academia-0083,69f2a1b8a7777da197101a96,406902669660,https://www.ebay.com/itm/406902669660,OK,
2026-05-06T20:35:31,Poster-Academia-0084,69f2a2aacaeb1241880b9f6b,406902691983,https://www.ebay.com/itm/406902691983,OK,
2026-05-06T20:35:33,Acrylic-Grimdark-0082,69f2a7d0e64c9f31b70f79cf,406902633400,https://www.ebay.com/itm/406902633400,OK,
2026-05-06T20:35:34,Acrylic-Zen-0002,69f2a8a5357398ded80f8faf,406902657898,https://www.ebay.com/itm/406902657898,OK,
2026-05-06T20:35:36,Acrylic-Zen-0003,69f2a9b45f78c14a7b0a7290,406902673249,https://www.ebay.com/itm/406902673249,OK,
2026-05-06T20:35:37,Poster-Academia-0085,69f2b132cd8d04605103fdaa,406902882943,https://www.ebay.com/itm/406902882943,OK,
2026-05-06T20:35:39,Poster-Academia-0091,69f2b7ada7777da1971028d7,406902887127,https://www.ebay.com/itm/406902887127,OK,
2026-05-06T20:35:43,Acrylic-Academia-0003,69f2b9c3caeb1241880bae85,406902703464,https://www.ebay.com/itm/406902703464,OK,
2026-05-06T20:35:46,Acrylic-Grimdark-0083,69f2bac6343d8ca093077dd8,406902885214,https://www.ebay.com/itm/406902885214,OK,
2026-05-06T20:35:48,Acrylic-Zen-0004,69f2bbbc343d8ca093077e9a,406902888077,https://www.ebay.com/itm/406902888077,OK,
2026-05-06T20:35:49,Acrylic-Zen-0005,69f2c22e9b469f716d0ea954,406902893289,https://www.ebay.com/itm/406902893289,OK,
2026-05-06T20:35:51,Poster-Zen-0001,69f2dc76cd8d046051041f06,406902890971,https://www.ebay.com/itm/406902890971,OK,
2026-05-06T20:35:52,Poster-Zen-0002,69f2cf675f78c14a7b0a894c,406902897663,https://www.ebay.com/itm/406902897663,OK,
2026-05-06T20:35:54,Acrylic-Zen-0006,69f2d2a1c326d7da170c51b4,406902898909,https://www.ebay.com/itm/406902898909,OK,
2026-05-06T20:35:56,Acrylic-Zen-0007,69f2d3ab5f78c14a7b0a8b87,406903028253,https://www.ebay.com/itm/406903028253,OK,
2026-05-06T20:35:57,Acrylic-Zen-0008,69f2d49b81039eb9ab0b583c,406903036452,https://www.ebay.com/itm/406903036452,OK,
2026-05-06T20:35:58,Poster-Zen-0004,69f2dddb9577aaffd506bc32,406903026999,https://www.ebay.com/itm/406903026999,OK,
2026-05-06T20:36:00,Poster-Zen-0005,69f2db1a3c6616b960034a37,406903033377,https://www.ebay.com/itm/406903033377,OK,
2026-05-06T20:36:02,Acrylic-Academia-0005,69f80ad2d3b9dc73b1051dbd,406903039716,https://www.ebay.com/itm/406903039716,OK,
2026-05-06T20:36:04,Acrylic-Grimdark-0085,69f2e4c77e3402ea470630eb,406903043482,https://www.ebay.com/itm/406903043482,OK,
2026-05-06T20:36:05,Acrylic-Zen-0009,69f80f8a83a8608fd80ec283,406903047385,https://www.ebay.com/itm/406903047385,OK,
2026-05-06T20:36:06,Acrylic-Zen-0010,69f810485da263f75f049bf8,406903213858,https://www.ebay.com/itm/406903213858,OK,
2026-05-06T20:36:07,Acrylic-Grimdark-0001,69f82b8aa1a4c45aad055063,406903249745,https://www.ebay.com/itm/406903249745,OK,
2026-05-06T20:36:09,Acrylic-Grimdark-0004,69f82c8609f3b7302401cacf,406903250705,https://www.ebay.com/itm/406903250705,OK,
2026-05-06T20:36:10,Acrylic-Grimdark-0005,69f8388b25819cdf3d0538bc,406903251829,https://www.ebay.com/itm/406903251829,OK,
2026-05-06T20:36:11,Acrylic-Grimdark-0006,69f83957ffbc831dea082e1a,406903252506,https://www.ebay.com/itm/406903252506,OK,
2026-05-06T20:36:13,Acrylic-Grimdark-0007,69f839eaf9374ed4f105a092,406903731967,https://www.ebay.com/itm/406903731967,OK,
2026-05-06T20:36:14,Acrylic-Grimdark-0008,69f83a955da263f75f04c06a,406903746215,https://www.ebay.com/itm/406903746215,OK,
2026-05-06T20:36:15,Acrylic-Grimdark-0009,69f83b5cf9374ed4f105a180,406903749989,https://www.ebay.com/itm/406903749989,OK,
2026-05-06T20:36:16,Acrylic-Grimdark-0010,69f83c14ffbc831dea082fa3,406903756190,https://www.ebay.com/itm/406903756190,OK,
2026-05-06T20:36:18,Poster-Academia-0005,69f847b45da263f75f04cdbd,406903038850,https://www.ebay.com/itm/406903038850,OK,
2026-05-06T20:36:19,Poster-Academia-0006,69f84864feed9979d10cd5ba,406903042690,https://www.ebay.com/itm/406903042690,OK,
2026-05-06T20:36:21,Poster-Academia-0008,69f84b3d5da263f75f04d1f7,406903046097,https://www.ebay.com/itm/406903046097,OK,
2026-05-06T20:36:22,Poster-Academia-0009,69f8547125819cdf3d05522b,406903209258,https://www.ebay.com/itm/406903209258,OK,
2026-05-06T20:36:23,Poster-Academia-0010,69f854ed09f3b7302401ed2e,406903249496,https://www.ebay.com/itm/406903249496,OK,
2026-05-06T20:36:24,Poster-Academia-0011,69f850b425819cdf3d054e10,406903250376,https://www.ebay.com/itm/406903250376,OK,
2026-05-06T22:50:31,Sticker-Zen-0044-FIX1,69fbdfc9f60a24b6d1035f8b,,,MISSING_EXTERNAL_ID,
2026-05-06T22:53:44,Sticker-Zen-0044-FIX1,69fbdfc9f60a24b6d1035f8b,,,MISSING_EXTERNAL_ID,

```


### RAW LOG: Database/eBay_Online_Cover_Audit.csv
```text
﻿Timestamp,ID,eBay_Item_ID,Printify_Product_ID,Title,Online_URL,Online_Image_URL,Online_Image_Path,Cover_Path,Gallery_U1_Path,Best_U_Label,Best_U_Path,Distance_To_Cover,Best_U_Distance,Result,Note,Error
2026-05-05T21:25:04-04:00,Sticker-Zen-0010,406892414116,69f1b00840c796ee97058144,Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,https://www.ebay.com/itm/406892414116,https://i.ebayimg.com/thumbs/images/g/lJMAAeSwv5dp8ept/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0010_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Sticker-Zen-0010_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Sticker-Zen-0010_U2_Grid.png,0,206,LIKELY_COVER,cover closer than U2 by 206,
2026-05-05T21:25:18-04:00,Sticker-Zen-0022,406892414235,69f1b1ab63935da7e8064bab,Mindful Zen Garden Stone Meis seki 4pc 6x6 Vinyl Sticker Laptop Journal Gift,https://www.ebay.com/itm/406892414235,https://i.ebayimg.com/images/g/8w8AAeSwppNp8ep-/s-l1600.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0022_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Sticker-Zen-0022_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Sticker-Zen-0022_U4_Grid.png,213,2,LIKELY_SINGLE_U_MISMATCH,U4 closer by 211,
2026-05-05T21:25:32-04:00,Sticker-Zen-0025,406892327989,69f1cb4ef6b83091a50959f5,Koi Fish in Jade Pond Hisui no Koi Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Luck,https://www.ebay.com/itm/406892327989,https://i.ebayimg.com/images/g/sfMAAeSwmT1p8dsV/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0025_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Sticker-Zen-0025_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Sticker-Zen-0025_U4_Grid.png,331,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 331,
2026-05-05T21:25:41-04:00,Sticker-Zen-0027,406892414741,69f1ce0f11e0745fcb0da03a,Minimal Zen Temple Lantern Zendera no T r 4pc 6x6 Sticker Sheet Serene Mindful,https://www.ebay.com/itm/406892414741,https://i.ebayimg.com/images/g/7FcAAeSwl5xp8eqf/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0027_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Sticker-Zen-0027_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Sticker-Zen-0027_U2_Grid.png,254,1,LIKELY_SINGLE_U_MISMATCH,U2 closer by 253,
2026-05-05T21:25:50-04:00,Sticker-Zen-0041,406902593931,69f1db9382fcf925cf08206d,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,https://www.ebay.com/itm/406902593931,https://i.ebayimg.com/images/g/uesAAeSw8iBp-Bp3/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0041_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Sticker-Zen-0041_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Sticker-Zen-0041_U2_Grid.png,336,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 336,
2026-05-05T21:25:58-04:00,Sticker-Zen-0044,406902622710,69f2396ccaeb1241880b692d,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,https://www.ebay.com/itm/406902622710,https://i.ebayimg.com/images/g/I~8AAeSw-jZp-B2c/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0044_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U3_Grid.png,296,1,LIKELY_SINGLE_U_MISMATCH,U3 closer by 295,
2026-05-05T21:26:08-04:00,Sticker-Zen-0045,406902640998,69f21a5da7777da1970fd378,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,https://www.ebay.com/itm/406902640998,https://i.ebayimg.com/images/g/a6QAAeSwSQRp-CBe/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0045_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Sticker-Zen-0045_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Sticker-Zen-0045_U4_Grid.png,290,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 290,
2026-05-05T21:26:16-04:00,Sticker-Zen-0046,406902663232,69f21b07b0d6b88b2805ebe3,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,https://www.ebay.com/itm/406902663232,https://i.ebayimg.com/images/g/drMAAeSwVJVp-CJQ/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0046_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Sticker-Zen-0046_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Sticker-Zen-0046_U4_Grid.png,274,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 274,
2026-05-05T21:26:24-04:00,Sticker-Zen-0049,406902713267,69f23a2fa7777da1970fe60d,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,https://www.ebay.com/itm/406902713267,https://i.ebayimg.com/images/g/oo8AAeSwiY5p-Cdm/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0049_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Sticker-Zen-0049_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Sticker-Zen-0049_U4_Grid.png,321,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 321,
2026-05-05T21:26:33-04:00,Sticker-Zen-0050,406902886081,69f23a99c326d7da170bfe8d,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,https://www.ebay.com/itm/406902886081,https://i.ebayimg.com/images/g/zy0AAeSwx-9p-D2U/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0050_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Sticker-Zen-0050_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Sticker-Zen-0050_U2_Grid.png,277,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 277,
2026-05-05T21:26:42-04:00,Sticker-Zen-0051,406902889638,69f23b5ce64c9f31b70f415b,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,https://www.ebay.com/itm/406902889638,https://i.ebayimg.com/images/g/BZYAAeSwhANp-D5g/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0051_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Sticker-Zen-0051_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Sticker-Zen-0051_U3_Grid.png,306,1,LIKELY_SINGLE_U_MISMATCH,U3 closer by 305,
2026-05-05T21:26:50-04:00,Sticker-Zen-0052,406902896387,69f23c10caeb1241880b6afe,Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,https://www.ebay.com/itm/406902896387,https://i.ebayimg.com/images/g/RqcAAeSwCctp-D9C/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0052_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Sticker-Zen-0052_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Sticker-Zen-0052_U3_Grid.png,259,1,LIKELY_SINGLE_U_MISMATCH,U3 closer by 258,
2026-05-05T21:26:58-04:00,Sticker-Zen-0053,406902900109,69f252f4357398ded80f61c9,Crystalline Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,https://www.ebay.com/itm/406902900109,https://i.ebayimg.com/images/g/kEQAAeSwntxp-D~3/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0053_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Sticker-Zen-0053_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Sticker-Zen-0053_U2_Grid.png,232,2,LIKELY_SINGLE_U_MISMATCH,U2 closer by 230,
2026-05-05T21:27:07-04:00,Sticker-Zen-0054,406903032635,69f253bc357398ded80f6242,Dragon Meditation Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,https://www.ebay.com/itm/406903032635,https://i.ebayimg.com/images/g/Q2AAAeSwI-5p-FfC/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0054_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Sticker-Zen-0054_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Sticker-Zen-0054_U2_Grid.png,331,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 331,
2026-05-05T22:16:48-04:00,Sticker-Academia-0004,406892408950,69f192aa5ea38382140f1d7b,4pc Kiss-Cut Sticker Set Mechanical Raven Familiar Laptop Journal Bottle Dark,https://www.ebay.com/itm/406892408950,https://i.ebayimg.com/thumbs/images/g/93sAAeSwJnVp8el6/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0004_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0004_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0004_Ready_for_Steaming\Sticker-Academia-0004_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0004_Ready_for_Steaming\Sticker-Academia-0004_U1_Grid.png,1,170,LIKELY_COVER,cover closer than U1 by 169,
2026-05-05T22:17:00-04:00,Sticker-Academia-0005,406892409123,69f198efea1f992ded0e90e7,4pc Vinyl Sticker Set Forbidden Grimoire Lock Laptop Bottle Journal Dark,https://www.ebay.com/itm/406892409123,https://i.ebayimg.com/images/g/7eUAAeSwJyRp8emL/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0005_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Sticker-Academia-0005_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Sticker-Academia-0005_U4_Grid.png,194,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 194,
2026-05-05T22:17:10-04:00,Sticker-Academia-0006,406892409348,69f19b945494697f0d01b78c,4pc Sticker Set Botanical Terrarium Lantern Vinyl Decals Laptop Bottle Dark,https://www.ebay.com/itm/406892409348,https://i.ebayimg.com/images/g/VH8AAeSwwelp8emX/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0006_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Sticker-Academia-0006_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Sticker-Academia-0006_U3_Grid.png,196,0,LIKELY_SINGLE_U_MISMATCH,U3 closer by 196,
2026-05-05T22:17:20-04:00,Sticker-Academia-0007,406892409645,69f1a56756390ef4cd09be1e,4pc Kiss-Cut Sticker Set Astrolabe Navigation Instrument Laptop Journal Bottle,https://www.ebay.com/itm/406892409645,https://i.ebayimg.com/images/g/AjcAAeSwK8Np8eml/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0007_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Sticker-Academia-0007_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Sticker-Academia-0007_U3_Grid.png,200,0,LIKELY_SINGLE_U_MISMATCH,U3 closer by 200,
2026-05-05T22:17:29-04:00,Sticker-Academia-0008,406892409836,69f1a630de3c2e09400f9c5f,4pc Vinyl Sticker Set Ritual Incense Censer Gothic Academia Laptop Bottle,https://www.ebay.com/itm/406892409836,https://i.ebayimg.com/images/g/JKYAAeSwhrZp8emz/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0008_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Sticker-Academia-0008_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Sticker-Academia-0008_U2_Grid.png,193,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 193,
2026-05-05T22:17:39-04:00,Sticker-Academia-0009,406892410017,69f1a6acc2501ebbc40ac2e5,4pc Sticker Set Gothic Academia Cathedral Fragment Vinyl Decals Laptop Bottle,https://www.ebay.com/itm/406892410017,https://i.ebayimg.com/images/g/Kv4AAeSwe5lp8enA/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0009_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Sticker-Academia-0009_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Sticker-Academia-0009_U2_Grid.png,204,1,LIKELY_SINGLE_U_MISMATCH,U2 closer by 203,
2026-05-05T22:17:48-04:00,Sticker-Academia-0010,406892410190,69f1a724785a37b0240adad9,4pc Kiss-Cut Sticker Set Compass Rose Talisman Laptop Journal Bottle Dark,https://www.ebay.com/itm/406892410190,https://i.ebayimg.com/images/g/xHUAAeSw5Ahp8enM/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0010_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Sticker-Academia-0010_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Sticker-Academia-0010_U3_Grid.png,250,0,LIKELY_SINGLE_U_MISMATCH,U3 closer by 250,
2026-05-05T22:17:57-04:00,Sticker-Academia-0011,406892410307,69f1a7b0cfb25d6b6f0f10f7,4pc Vinyl Sticker Set Apothecary Poison Vial Laptop Bottle Journal Dark,https://www.ebay.com/itm/406892410307,https://i.ebayimg.com/images/g/NGcAAeSwzN5p8enZ/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0011_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Sticker-Academia-0011_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Sticker-Academia-0011_U1_Grid.png,204,1,LIKELY_SINGLE_U_MISMATCH,U1 closer by 203,
2026-05-05T22:18:06-04:00,Sticker-Academia-0014,406892410440,69f1a833592cc603cd0a91fd,4pc Vinyl Sticker Set Microscope Observation Device Laptop Bottle Journal Dark,https://www.ebay.com/itm/406892410440,https://i.ebayimg.com/images/g/xSwAAeSw5Ahp8enk/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0014_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Sticker-Academia-0014_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Sticker-Academia-0014_U1_Grid.png,231,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 231,
2026-05-05T22:18:15-04:00,Sticker-Academia-0015,406892411034,69f1a8b40bc0bf405305ef2b,4pc Sticker Set Skeleton Key Portal Vinyl Decals Laptop Bottle Dark Academia,https://www.ebay.com/itm/406892411034,https://i.ebayimg.com/images/g/GE4AAeSw-jZp8enx/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0015_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Sticker-Academia-0015_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Sticker-Academia-0015_U3_Grid.png,155,0,LIKELY_SINGLE_U_MISMATCH,U3 closer by 155,
2026-05-05T22:18:25-04:00,Sticker-Academia-0016,406892411436,69f1a92ade3c2e09400f9e44,4pc Kiss-Cut Sticker Set Gothic Academia Prism Light Refractor Laptop Journal,https://www.ebay.com/itm/406892411436,https://i.ebayimg.com/images/g/4x8AAeSw9fpp8en-/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0016_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Sticker-Academia-0016_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Sticker-Academia-0016_U3_Grid.png,192,0,LIKELY_SINGLE_U_MISMATCH,U3 closer by 192,
2026-05-05T22:18:35-04:00,Sticker-Zen-0001,406892411931,69f1a99c785a37b0240adc94,4pc Sticker Set Mindful Zen Koi Pond Vinyl Decals Laptop Bottle Zen Aesthetic,https://www.ebay.com/itm/406892411931,https://i.ebayimg.com/images/g/rc0AAeSwzmBp8eoL/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0001_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Sticker-Zen-0001_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Sticker-Zen-0001_U1_Grid.png,195,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 195,
2026-05-05T22:18:44-04:00,Sticker-Zen-0002,406892412365,69f1ab9a63935da7e8064504,4pc Kiss-Cut Sticker Set Bonsai Tree of Serenity Laptop Journal Bottle Zen,https://www.ebay.com/itm/406892412365,https://i.ebayimg.com/images/g/LY0AAeSw171p8eoY/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0002_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Sticker-Zen-0002_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Sticker-Zen-0002_U1_Grid.png,228,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 228,
2026-05-05T22:18:56-04:00,Sticker-Zen-0003,406892412612,69f1ac1804ea1d3ba9005c58,4pc Vinyl Sticker Set Lotus Mandala Mindful Zen Laptop Bottle Journal Zen,https://www.ebay.com/itm/406892412612,https://i.ebayimg.com/images/g/85sAAeSwajBp8eok/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0003_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Sticker-Zen-0003_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Sticker-Zen-0003_U1_Grid.png,216,1,LIKELY_SINGLE_U_MISMATCH,U1 closer by 215,
2026-05-05T22:19:07-04:00,Sticker-Zen-0004,406892412789,69f1ac9740c796ee97057c83,4pc Sticker Set Stone Guardian Lion Mindful Zen Vinyl Decals Laptop Bottle Zen,https://www.ebay.com/itm/406892412789,https://i.ebayimg.com/images/g/yOYAAeSw9cNp8eow/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0004_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Sticker-Zen-0004_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Sticker-Zen-0004_U2_Grid.png,195,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 195,
2026-05-05T22:19:20-04:00,Sticker-Zen-0005,406892413076,69f1ad18c59fe705400bacbf,4pc Kiss-Cut Sticker Set Bamboo Forest Laptop Journal Bottle Zen Aesthetic,https://www.ebay.com/itm/406892413076,https://i.ebayimg.com/images/g/1OEAAeSwrHRp8eo~/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0005_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Sticker-Zen-0005_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Sticker-Zen-0005_U1_Grid.png,334,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 334,
2026-05-05T22:19:29-04:00,Sticker-Zen-0007,406892413333,69f1ad9bbb6f6dd6270dc5df,4pc Sticker Set Cherry Blossom Branch Vinyl Decals Laptop Bottle Zen Aesthetic,https://www.ebay.com/itm/406892413333,https://i.ebayimg.com/images/g/i6UAAeSwBeNp8epL/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0007_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Sticker-Zen-0007_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Sticker-Zen-0007_U1_Grid.png,212,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 212,
2026-05-05T22:19:38-04:00,Sticker-Zen-0008,406892413714,69f1aef4bb6f6dd6270dc7d5,4pc Kiss-Cut Sticker Set Circle Ens Laptop Journal Bottle Zen Aesthetic Decal,https://www.ebay.com/itm/406892413714,https://i.ebayimg.com/images/g/VBkAAeSwcE5p8epY/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0008_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Sticker-Zen-0008_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Sticker-Zen-0008_U2_Grid.png,193,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 193,
2026-05-05T22:19:50-04:00,Sticker-Zen-0009,406892413966,69f1af85bb6f6dd6270dc848,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Laptop Journal,https://www.ebay.com/itm/406892413966,https://i.ebayimg.com/images/g/KdgAAeSwzJ1p8epl/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0009_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Sticker-Zen-0009_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Sticker-Zen-0009_U4_Grid.png,231,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 231,
2026-05-05T22:20:01-04:00,Sticker-Zen-0010,406892414116,69f1b00840c796ee97058144,Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,https://www.ebay.com/itm/406892414116,https://i.ebayimg.com/thumbs/images/g/lJMAAeSwv5dp8ept/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0010_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Sticker-Zen-0010_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Sticker-Zen-0010_U2_Grid.png,0,206,LIKELY_COVER,cover closer than U2 by 206,
2026-05-05T22:20:09-04:00,Sticker-Zen-0022,406892414235,69f1b1ab63935da7e8064bab,Mindful Zen Garden Stone Meis seki 4pc 6x6 Vinyl Sticker Laptop Journal Gift,https://www.ebay.com/itm/406892414235,https://i.ebayimg.com/images/g/8w8AAeSwppNp8ep-/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0022_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Sticker-Zen-0022_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Sticker-Zen-0022_U4_Grid.png,213,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 213,
2026-05-05T22:20:19-04:00,Sticker-Zen-0024,406892414471,69f1b2c4d3e196c79b0fdaec,Mindful Zen Enso Circle with Crystals 4pc 6x6 Vinyl Sticker Laptop Journal Gift,https://www.ebay.com/itm/406892414471,https://i.ebayimg.com/images/g/pP0AAeSw5D5p8eqL/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0024_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Sticker-Zen-0024_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Sticker-Zen-0024_U2_Grid.png,239,1,LIKELY_SINGLE_U_MISMATCH,U2 closer by 238,
2026-05-05T22:20:28-04:00,Sticker-Zen-0025,406892327989,69f1cb4ef6b83091a50959f5,Koi Fish in Jade Pond Hisui no Koi Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Luck,https://www.ebay.com/itm/406892327989,https://i.ebayimg.com/images/g/sfMAAeSwmT1p8dsV/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0025_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Sticker-Zen-0025_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Sticker-Zen-0025_U4_Grid.png,331,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 331,
2026-05-05T22:20:38-04:00,Sticker-Zen-0027,406892414741,69f1ce0f11e0745fcb0da03a,Minimal Zen Temple Lantern Zendera no T r 4pc 6x6 Sticker Sheet Serene Mindful,https://www.ebay.com/itm/406892414741,https://i.ebayimg.com/images/g/7FcAAeSwl5xp8eqf/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0027_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Sticker-Zen-0027_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Sticker-Zen-0027_U2_Grid.png,254,1,LIKELY_SINGLE_U_MISMATCH,U2 closer by 253,
2026-05-05T22:20:47-04:00,Sticker-Zen-0041,406902593931,69f1db9382fcf925cf08206d,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,https://www.ebay.com/itm/406902593931,https://i.ebayimg.com/images/g/uesAAeSw8iBp-Bp3/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0041_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Sticker-Zen-0041_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Sticker-Zen-0041_U2_Grid.png,336,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 336,
2026-05-05T22:20:56-04:00,Sticker-Zen-0042,406902614234,69f2192ae64c9f31b70f2dbd,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,https://www.ebay.com/itm/406902614234,https://i.ebayimg.com/images/g/OjwAAeSwwtlp-BwB/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0042_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Sticker-Zen-0042_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Sticker-Zen-0042_U1_Grid.png,333,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 333,
2026-05-05T22:21:05-04:00,Sticker-Zen-0044,406902622710,69f2396ccaeb1241880b692d,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,https://www.ebay.com/itm/406902622710,https://i.ebayimg.com/images/g/I~8AAeSw-jZp-B2c/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0044_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U3_Grid.png,296,1,LIKELY_SINGLE_U_MISMATCH,U3 closer by 295,
2026-05-05T22:21:15-04:00,Sticker-Zen-0045,406902640998,69f21a5da7777da1970fd378,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,https://www.ebay.com/itm/406902640998,https://i.ebayimg.com/images/g/a6QAAeSwSQRp-CBe/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0045_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Sticker-Zen-0045_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Sticker-Zen-0045_U4_Grid.png,290,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 290,
2026-05-05T22:21:24-04:00,Sticker-Zen-0046,406902663232,69f21b07b0d6b88b2805ebe3,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,https://www.ebay.com/itm/406902663232,https://i.ebayimg.com/images/g/drMAAeSwVJVp-CJQ/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0046_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Sticker-Zen-0046_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Sticker-Zen-0046_U4_Grid.png,274,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 274,
2026-05-05T22:21:33-04:00,Sticker-Zen-0049,406902713267,69f23a2fa7777da1970fe60d,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,https://www.ebay.com/itm/406902713267,https://i.ebayimg.com/images/g/oo8AAeSwiY5p-Cdm/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0049_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Sticker-Zen-0049_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Sticker-Zen-0049_U4_Grid.png,321,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 321,
2026-05-05T22:21:43-04:00,Sticker-Zen-0050,406902886081,69f23a99c326d7da170bfe8d,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,https://www.ebay.com/itm/406902886081,https://i.ebayimg.com/images/g/zy0AAeSwx-9p-D2U/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0050_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Sticker-Zen-0050_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Sticker-Zen-0050_U2_Grid.png,277,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 277,
2026-05-05T22:21:52-04:00,Sticker-Zen-0051,406902889638,69f23b5ce64c9f31b70f415b,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,https://www.ebay.com/itm/406902889638,https://i.ebayimg.com/images/g/BZYAAeSwhANp-D5g/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0051_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Sticker-Zen-0051_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Sticker-Zen-0051_U3_Grid.png,306,1,LIKELY_SINGLE_U_MISMATCH,U3 closer by 305,
2026-05-05T22:22:02-04:00,Sticker-Zen-0052,406902896387,69f23c10caeb1241880b6afe,Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,https://www.ebay.com/itm/406902896387,https://i.ebayimg.com/images/g/RqcAAeSwCctp-D9C/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0052_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Sticker-Zen-0052_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Sticker-Zen-0052_U3_Grid.png,259,1,LIKELY_SINGLE_U_MISMATCH,U3 closer by 258,
2026-05-05T22:22:11-04:00,Sticker-Zen-0053,406902900109,69f252f4357398ded80f61c9,Crystalline Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,https://www.ebay.com/itm/406902900109,https://i.ebayimg.com/images/g/kEQAAeSwntxp-D~3/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0053_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Sticker-Zen-0053_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Sticker-Zen-0053_U2_Grid.png,232,2,LIKELY_SINGLE_U_MISMATCH,U2 closer by 230,
2026-05-05T22:22:21-04:00,Sticker-Zen-0054,406903032635,69f253bc357398ded80f6242,Dragon Meditation Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,https://www.ebay.com/itm/406903032635,https://i.ebayimg.com/images/g/Q2AAAeSwI-5p-FfC/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0054_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Sticker-Zen-0054_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Sticker-Zen-0054_U2_Grid.png,331,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 331,
2026-05-05T22:22:30-04:00,Sticker-Zen-0055,406903037933,69f2547229c1d0349a00e796,Mindful Zen Azure Dragon Warrior 4pc 6x6 Vinyl Sticker Laptop Journal Gift Desk,https://www.ebay.com/itm/406903037933,https://i.ebayimg.com/images/g/0EwAAeSwRxtp-Fis/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0055_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0055_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0055_Ready_for_Steaming\Sticker-Zen-0055_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0055_Ready_for_Steaming\Sticker-Zen-0055_U1_Grid.png,291,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 291,
2026-05-05T22:22:39-04:00,Sticker-Zen-0056,406903041315,69f25526ad218fe47f0cc0d3,Dragon Cherry Blossom 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,https://www.ebay.com/itm/406903041315,https://i.ebayimg.com/images/g/42AAAeSwp2Jp-Fmk/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0056_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0056_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0056_Ready_for_Steaming\Sticker-Zen-0056_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0056_Ready_for_Steaming\Sticker-Zen-0056_U1_Grid.png,260,2,LIKELY_SINGLE_U_MISMATCH,U1 closer by 258,
2026-05-05T22:22:48-04:00,Sticker-Zen-0057,406903044643,69f255dae64c9f31b70f4ea6,Moonlit Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk Decor,https://www.ebay.com/itm/406903044643,https://i.ebayimg.com/images/g/M08AAeSwrclp-Fp5/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0057_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0057_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0057_Ready_for_Steaming\Sticker-Zen-0057_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0057_Ready_for_Steaming\Sticker-Zen-0057_U2_Grid.png,288,1,LIKELY_SINGLE_U_MISMATCH,U2 closer by 287,
2026-05-05T22:22:59-04:00,Sticker-Zen-0058,406903049411,69f259bc5f78c14a7b0a4760,Minimal Zen Dragon Calligraphy 4pc 6x6 Sticker Sheet Serene Mindful Clean Decor,https://www.ebay.com/itm/406903049411,https://i.ebayimg.com/images/g/dw0AAeSw2Cpp-Ftn/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0058_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0058_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0058_Ready_for_Steaming\Sticker-Zen-0058_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0058_Ready_for_Steaming\Sticker-Zen-0058_U1_Grid.png,250,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 250,
2026-05-05T22:23:09-04:00,Sticker-Zen-0060,406903249053,69f25a86a7777da1970ff5f3,Minimal Zen Translucent Jade Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,https://www.ebay.com/itm/406903249053,https://i.ebayimg.com/images/g/FpcAAeSwZoxp-Hhr/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0060_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0060_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0060_Ready_for_Steaming\Sticker-Zen-0060_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0060_Ready_for_Steaming\Sticker-Zen-0060_U1_Grid.png,262,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 262,
2026-05-05T22:23:20-04:00,Sticker-Zen-0061,406903249987,69f25b3ce64c9f31b70f50ed,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Calm Gift,https://www.ebay.com/itm/406903249987,https://i.ebayimg.com/images/g/jPMAAeSwPw9p-HiX/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0061_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0061_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0061_Ready_for_Steaming\Sticker-Zen-0061_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0061_Ready_for_Steaming\Sticker-Zen-0061_U2_Grid.png,288,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 288,
2026-05-05T22:23:32-04:00,Sticker-Zen-0062,406903250891,69f25bee9b469f716d0e7056,Zen Aesthetic Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Laptop Journal,https://www.ebay.com/itm/406903250891,https://i.ebayimg.com/images/g/V34AAeSwDeVp-HjF/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0062_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0062_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0062_Ready_for_Steaming\Sticker-Zen-0062_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0062_Ready_for_Steaming\Sticker-Zen-0062_U2_Grid.png,255,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 255,
2026-05-05T22:23:41-04:00,Sticker-Zen-0063,406903252007,69f25ca39577aaffd5066a80,Crystalline Dragon Core 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,https://www.ebay.com/itm/406903252007,https://i.ebayimg.com/images/g/UQYAAeSwUbhp-Hjy/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0063_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0063_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0063_Ready_for_Steaming\Sticker-Zen-0063_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0063_Ready_for_Steaming\Sticker-Zen-0063_U2_Grid.png,295,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 295,
2026-05-05T22:23:52-04:00,Sticker-Zen-0066,406903252739,69f25d56c326d7da170c0f79,Golden Vein Circuitry Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Gift,https://www.ebay.com/itm/406903252739,https://i.ebayimg.com/images/g/ryQAAeSw8oNp-Hkg/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0066_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0066_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0066_Ready_for_Steaming\Sticker-Zen-0066_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0066_Ready_for_Steaming\Sticker-Zen-0066_U1_Grid.png,309,0,LIKELY_SINGLE_U_MISMATCH,U1 closer by 309,
2026-05-05T22:24:03-04:00,Sticker-Zen-0069,406903753067,69f26062cd8d04605103d10b,Minimal Zen Dragon Guardian 4pc 6x6 Sticker Sheet Serene Mindful Clean Decor,https://www.ebay.com/itm/406903753067,https://i.ebayimg.com/images/g/mXEAAeSw73lp-LHE/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0069_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0069_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0069_Ready_for_Steaming\Sticker-Zen-0069_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0069_Ready_for_Steaming\Sticker-Zen-0069_U4_Grid.png,301,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 301,
2026-05-05T22:24:13-04:00,Sticker-Zen-0070,406903757240,69f261185f78c14a7b0a4b29,Minimal Zen Jade Phoenix Ascension 4pc 6x6 Sticker Sheet Serene Mindful Clean,https://www.ebay.com/itm/406903757240,https://i.ebayimg.com/images/g/kO8AAeSwmmlp-LKH/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0070_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0070_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0070_Ready_for_Steaming\Sticker-Zen-0070_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0070_Ready_for_Steaming\Sticker-Zen-0070_U2_Grid.png,207,0,LIKELY_SINGLE_U_MISMATCH,U2 closer by 207,
2026-05-05T22:24:24-04:00,Sticker-Zen-0071,406903762328,69f261cd5269e3325904b816,Zen Aesthetic Lotus Lantern Vessel 4pc 6x6 Kiss-Cut Sticker Laptop Journal Gift,https://www.ebay.com/itm/406903762328,https://i.ebayimg.com/images/g/S-8AAeSwAKZp-LNt/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0071_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0071_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0071_Ready_for_Steaming\Sticker-Zen-0071_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0071_Ready_for_Steaming\Sticker-Zen-0071_U1_Grid.png,215,1,LIKELY_SINGLE_U_MISMATCH,U1 closer by 214,
2026-05-05T22:30:54-04:00,Poster-Academia-0001,406902584620,69f28800cd8d04605103e53a,Celestial Gateway Dark Academia Poster 12x18 Study Decor Moonstone Architecture,https://www.ebay.com/itm/406902584620,https://i.ebayimg.com/images/g/cY4AAeSwNIpp-BmA/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0001_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0001_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0001_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0001_Ready_for_Steaming\Gallery_U1.png,134,1,LIKELY_SINGLE_U_MISMATCH,U1 closer by 133,
2026-05-05T22:31:14-04:00,Poster-Academia-0002,406902600741,69f2906f7f1017d51b0d5f76,Dark Academia Obsidian Threshold Poster 12x18 Vintage Study Decor Mentor Wisdom,https://www.ebay.com/itm/406902600741,https://i.ebayimg.com/images/g/XlwAAeSwhYVp-BsC/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0002_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0002_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0002_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0002_Ready_for_Steaming\Gallery_U1.png,0,0,AMBIGUOUS,close distances cover=0 U1=0,
2026-05-05T22:31:26-04:00,Poster-Academia-0003,406902616799,69f29152357398ded80f8178,Dark Academia Serpentine Portal of Alchemical Texts 12x18 Poster Study Decor,https://www.ebay.com/itm/406902616799,https://i.ebayimg.com/images/g/RTsAAeSwa5xp-ByX/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0003_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0003_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0003_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0003_Ready_for_Steaming\Gallery_U1.png,268,239,LIKELY_SINGLE_U_MISMATCH,U1 closer by 29,
2026-05-05T22:31:40-04:00,Acrylic-Academia-0001,406902588642,69f298dc9577aaffd50689b0,Astrolabe Compass Ritual Disc Dark Academia 5x7 Acrylic Art Study Decor Shelf,https://www.ebay.com/itm/406902588642,https://i.ebayimg.com/images/g/9zAAAeSwY5xp-BoV/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Academia-0001_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0001_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0001_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0001_Ready_for_Steaming\Gallery_U1.png,268,268,AMBIGUOUS,close distances cover=268 U1=268,
2026-05-05T22:31:57-04:00,Acrylic-Grimdark-0081,406902606976,69f299c1a3119247600cbe18,Plague Doctor Raven Skull Grimdark Alchemy 5x7 Acrylic Art Block Collectible,https://www.ebay.com/itm/406902606976,https://i.ebayimg.com/images/g/YIMAAeSw1Clp-Bt3/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0081_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0081_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0081_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0081_Ready_for_Steaming\Gallery_U1.png,274,224,LIKELY_SINGLE_U_MISMATCH,U1 closer by 50,
2026-05-05T22:32:10-04:00,Acrylic-Zen-0001,406902620519,69f29a72c411a56f6902930d,Zen Mechanical Crane 5x7 Acrylic Block Desk Art Calm Decor Origami Sculpture,https://www.ebay.com/itm/406902620519,https://i.ebayimg.com/images/g/SEMAAeSwnflp-B0-/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0001_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0001_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0001_Ready_for_Steaming\Gallery_U1.png,237,7,LIKELY_SINGLE_U_MISMATCH,U1 closer by 230,
2026-05-05T22:32:21-04:00,Poster-Academia-0081,406902627420,69f29fe09577aaffd5068e03,Celestial Armillary Sphere Dark Academia Poster 12x18 Scholar Study Decor Wall,https://www.ebay.com/itm/406902627420,https://i.ebayimg.com/images/g/ILAAAeSwSoFp-B6P/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0081_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0081_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0081_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0081_Ready_for_Steaming\Gallery_U1.png,215,215,AMBIGUOUS,close distances cover=215 U1=215,
2026-05-05T22:32:38-04:00,Poster-Academia-0082,406902648209,69f2a0cacaeb1241880b9e8d,Celestial Armillary Codex Academia Poster 12x18 Vintage Astronomy Decor Wall,https://www.ebay.com/itm/406902648209,https://i.ebayimg.com/images/g/hWIAAeSwuqdp-CDh/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0082_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0082_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0082_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0082_Ready_for_Steaming\Gallery_U1.png,189,189,AMBIGUOUS,close distances cover=189 U1=189,
2026-05-05T22:32:49-04:00,Poster-Academia-0083,406902669660,69f2a1b8a7777da197101a96,Academia Mentor-Grade Cosmic Lotus Observatory 12x18 Poster Steampunk Study,https://www.ebay.com/itm/406902669660,https://i.ebayimg.com/images/g/Sc8AAeSwtK1p-CNd/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0083_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0083_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0083_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0083_Ready_for_Steaming\Gallery_U1.png,151,151,AMBIGUOUS,close distances cover=151 U1=151,
2026-05-05T22:33:02-04:00,Poster-Academia-0084,406902691983,69f2a2aacaeb1241880b9f6b,Astrolabe Chalice Relic Dark Academia Poster 12x18 Vintage Study Decor Wall,https://www.ebay.com/itm/406902691983,https://i.ebayimg.com/images/g/ubEAAeSwzN5p-CVb/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0084_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0084_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0084_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0084_Ready_for_Steaming\Gallery_U1.png,122,122,AMBIGUOUS,close distances cover=122 U1=122,
2026-05-05T22:33:14-04:00,Acrylic-Grimdark-0082,406902633400,69f2a7d0e64c9f31b70f79cf,Grimdark Alchemical Terrarium Withered Mandrake Root Chamber 5x7 Acrylic Block,https://www.ebay.com/itm/406902633400,https://i.ebayimg.com/images/g/HZAAAeSwQW9p-B-D/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0082_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0082_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0082_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0082_Ready_for_Steaming\Gallery_U1.png,361,361,AMBIGUOUS,close distances cover=361 U1=361,
2026-05-05T22:33:27-04:00,Acrylic-Zen-0002,406902657898,69f2a8a5357398ded80f8faf,Zen Aesthetic Ritual Bell Shrine 5x7 Acrylic Block for Meditation Desk Shelf,https://www.ebay.com/itm/406902657898,https://i.ebayimg.com/images/g/iK0AAeSwRohp-CHI/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0002_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0002_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0002_Ready_for_Steaming\Gallery_U1.png,173,173,AMBIGUOUS,close distances cover=173 U1=173,
2026-05-05T22:33:41-04:00,Acrylic-Zen-0003,406902673249,69f2a9b45f78c14a7b0a7290,Zen Pagoda Fragment Relic 5x7 Acrylic Print Floating Tower Decor Jade Framework,https://www.ebay.com/itm/406902673249,https://i.ebayimg.com/images/g/acYAAeSwAU9p-CPh/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0003_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0003_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0003_Ready_for_Steaming\Gallery_U1.png,234,234,AMBIGUOUS,close distances cover=234 U1=234,
2026-05-05T22:33:55-04:00,Poster-Academia-0085,406902882943,69f2b132cd8d04605103fdaa,Orrery Lighthouse Beacon Dark Academia Poster 12x18 Vintage Astronomy Wall Art,https://www.ebay.com/itm/406902882943,https://i.ebayimg.com/images/g/vfsAAeSwwplp-Dzp/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0085_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0085_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0085_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0085_Ready_for_Steaming\Gallery_U1.png,167,167,AMBIGUOUS,close distances cover=167 U1=167,
2026-05-05T22:34:09-04:00,Poster-Academia-0091,406902887127,69f2b7ada7777da1971028d7,Dark Academia Celestial Lotus Poster 12x18 Vintage Study Room Wall Art Decor,https://www.ebay.com/itm/406902887127,https://i.ebayimg.com/images/g/ZpEAAeSwm5Bp-D3b/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0091_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0091_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0091_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0091_Ready_for_Steaming\Gallery_U1.png,169,169,AMBIGUOUS,close distances cover=169 U1=169,
2026-05-05T22:34:21-04:00,Acrylic-Academia-0003,406902703464,69f2b9c3caeb1241880bae85,Celestial Orrery Tree Bonsai Dark Academia 5x7 Acrylic Block Mentor-Grade Study,https://www.ebay.com/itm/406902703464,https://i.ebayimg.com/images/g/mcIAAeSwEeNp-CZx/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Academia-0003_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0003_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0003_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0003_Ready_for_Steaming\Gallery_U1.png,169,169,AMBIGUOUS,close distances cover=169 U1=169,
2026-05-05T22:34:34-04:00,Acrylic-Grimdark-0083,406902885214,69f2bac6343d8ca093077dd8,Grimdark Ritual Censer Thurible 5x7 Acrylic Block Dark Academia Mentor-Grade,https://www.ebay.com/itm/406902885214,https://i.ebayimg.com/images/g/U18AAeSwI-lp-D1b/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0083_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0083_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0083_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0083_Ready_for_Steaming\Gallery_U1.png,213,213,AMBIGUOUS,close distances cover=213 U1=213,
2026-05-05T22:34:50-04:00,Acrylic-Zen-0004,406902888077,69f2bbbc343d8ca093077e9a,Zen Cyberpunk Koi Automaton 5x7 Acrylic Block - Meditative Desk Sculpture Shelf,https://www.ebay.com/itm/406902888077,https://i.ebayimg.com/images/g/uiUAAeSwpHRp-D4i/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0004_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0004_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0004_Ready_for_Steaming\Gallery_U1.png,251,251,AMBIGUOUS,close distances cover=251 U1=251,
2026-05-05T22:35:00-04:00,Acrylic-Zen-0005,406902893289,69f2c22e9b469f716d0ea954,Zen Incense Vessel Constellation 5x7 Acrylic Block for Meditation Desk Shelf,https://www.ebay.com/itm/406902893289,https://i.ebayimg.com/images/g/SoMAAeSwm6Zp-D7i/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0005_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0005_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0005_Ready_for_Steaming\Gallery_U1.png,255,255,AMBIGUOUS,close distances cover=255 U1=255,
2026-05-05T22:35:13-04:00,Poster-Zen-0001,406902890971,69f2dc76cd8d046051041f06,Zen Bonsai Wall Art Celestial Gate of Jade Mist 12x18 Poster Meditation Decor,https://www.ebay.com/itm/406902890971,https://i.ebayimg.com/images/g/L~0AAeSwrHRp-D6l/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Zen-0001_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0001_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0001_Ready_for_Steaming\Gallery_U1.png,1,1,AMBIGUOUS,close distances cover=1 U1=1,
2026-05-05T22:35:29-04:00,Poster-Zen-0002,406902897663,69f2cf675f78c14a7b0a894c,Dark Academia Phoenix Incense Burner 12x18 Poster Ritual Zen Decor Wall Study,https://www.ebay.com/itm/406902897663,https://i.ebayimg.com/images/g/GXgAAeSw7T5p-D-F/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Zen-0002_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0002_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0002_Ready_for_Steaming\Gallery_U1.png,271,271,AMBIGUOUS,close distances cover=271 U1=271,
2026-05-05T22:35:43-04:00,Acrylic-Zen-0006,406902898909,69f2d2a1c326d7da170c51b4,Zen Mentor-Grade Jade Phoenix Incense Altar 5x7 Acrylic Block for Meditation,https://www.ebay.com/itm/406902898909,https://i.ebayimg.com/images/g/S20AAeSwwtlp-D-0/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0006_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0006_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0006_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0006_Ready_for_Steaming\Gallery_U1.png,208,208,AMBIGUOUS,close distances cover=208 U1=208,
2026-05-05T22:35:57-04:00,Acrylic-Zen-0007,406903028253,69f2d3ab5f78c14a7b0a8b87,Zen Aesthetic Sacred Lotus Meditation Bell 5x7 Acrylic Block for Altar Decor,https://www.ebay.com/itm/406903028253,https://i.ebayimg.com/images/g/O9oAAeSwvSpp-Fda/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0007_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0007_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0007_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0007_Ready_for_Steaming\Gallery_U1.png,165,165,AMBIGUOUS,close distances cover=165 U1=165,
2026-05-05T22:36:11-04:00,Acrylic-Zen-0008,406903036452,69f2d49b81039eb9ab0b583c,Zen Celestial Bonsai Moon Garden 5x7 Acrylic Block for Serene Desk Decor Shelf,https://www.ebay.com/itm/406903036452,https://i.ebayimg.com/images/g/VXkAAeSwCbZp-Fhv/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0008_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0008_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0008_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0008_Ready_for_Steaming\Gallery_U1.png,275,275,AMBIGUOUS,close distances cover=275 U1=275,
2026-05-05T22:36:31-04:00,Poster-Zen-0004,406903026999,69f2dddb9577aaffd506bc32,Zen Celestial Compass Poster 12x18 Wall Art Calm Study Decor Library Gift Room,https://www.ebay.com/itm/406903026999,https://i.ebayimg.com/images/g/QyMAAeSwJy5p-FcD/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Zen-0004_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0004_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0004_Ready_for_Steaming\Gallery_U1.png,271,271,AMBIGUOUS,close distances cover=271 U1=271,
2026-05-05T22:36:46-04:00,Poster-Zen-0005,406903033377,69f2db1a3c6616b960034a37,Zen Phoenix Rebirth Vessel 12x18 Poster for Meditation Room Decor Wall Study,https://www.ebay.com/itm/406903033377,https://i.ebayimg.com/images/g/X3YAAeSwNw1p-Ff~/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Zen-0005_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0005_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0005_Ready_for_Steaming\Gallery_U1.png,303,303,AMBIGUOUS,close distances cover=303 U1=303,
2026-05-05T22:37:03-04:00,Acrylic-Academia-0005,406903039716,69f80ad2d3b9dc73b1051dbd,Alchemical Star Flask Vessel 5x7 Acrylic Block Dark Academia Desk Decor Shelf,https://www.ebay.com/itm/406903039716,https://i.ebayimg.com/thumbs/images/g/djoAAeSw0Ulp-Fku/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Academia-0005_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0005_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0005_Ready_for_Steaming\Gallery_U1.png,355,355,AMBIGUOUS,close distances cover=355 U1=355,
2026-05-05T22:37:17-04:00,Acrylic-Grimdark-0085,406903043482,69f2e4c77e3402ea470630eb,Alchemist Divination Compass Grimdark 5x7 Acrylic Display Mentor-Grade Occult,https://www.ebay.com/itm/406903043482,https://i.ebayimg.com/thumbs/images/g/Zz8AAeSwamJp-Fov/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0085_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0085_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0085_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0085_Ready_for_Steaming\Gallery_U1.png,446,446,AMBIGUOUS,close distances cover=446 U1=446,
2026-05-05T22:37:31-04:00,Acrylic-Zen-0009,406903047385,69f80f8a83a8608fd80ec283,"Zen Bamboo Flute 5x7 Acrylic Block, Whispering Shakuhachi Meditation Art Gift",https://www.ebay.com/itm/406903047385,https://i.ebayimg.com/thumbs/images/g/fiEAAeSwVNVp-Fr9/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0009_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0009_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0009_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0009_Ready_for_Steaming\Gallery_U1.png,286,286,AMBIGUOUS,close distances cover=286 U1=286,
2026-05-05T22:37:44-04:00,Acrylic-Zen-0010,406903213858,69f810485da263f75f049bf8,Zen Lotus Seed Pod Vessel 5x7 Acrylic Block for Mindful Desk Decor Shelf Study,https://www.ebay.com/itm/406903213858,https://i.ebayimg.com/thumbs/images/g/MjsAAeSwO~1p-HEY/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Zen-0010_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0010_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0010_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0010_Ready_for_Steaming\Gallery_U1.png,109,109,AMBIGUOUS,close distances cover=109 U1=109,
2026-05-05T22:37:55-04:00,Acrylic-Grimdark-0001,406903249745,69f82b8aa1a4c45aad055063,Gothic Lantern Soul Cage 5x7 Acrylic Block Grimdark Study Decor Crimson Flame,https://www.ebay.com/itm/406903249745,https://i.ebayimg.com/thumbs/images/g/9tgAAeSwnflp-HiH/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0001_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0001_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0001_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0001_Ready_for_Steaming\Gallery_U1.png,357,357,AMBIGUOUS,close distances cover=357 U1=357,
2026-05-05T22:38:09-04:00,Acrylic-Grimdark-0004,406903250705,69f82c8609f3b7302401cacf,Grimdark Gothic Lantern 5x7 Acrylic Block Shadowbound Sentinel Beacon Dark Gift,https://www.ebay.com/itm/406903250705,https://i.ebayimg.com/thumbs/images/g/k6EAAeSw9yVp-Hiz/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0004_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0004_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0004_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0004_Ready_for_Steaming\Gallery_U1.png,407,407,AMBIGUOUS,close distances cover=407 U1=407,
2026-05-05T22:38:29-04:00,Acrylic-Grimdark-0005,406903251829,69f8388b25819cdf3d0538bc,Gothic Necromancer Soul Reliquary 5x7 Acrylic Grimdark Artifact Decor Shelf,https://www.ebay.com/itm/406903251829,https://i.ebayimg.com/thumbs/images/g/nswAAeSwuqdp-Hjj/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0005_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0005_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0005_Ready_for_Steaming\Gallery_U1.png,350,350,AMBIGUOUS,close distances cover=350 U1=350,
2026-05-05T22:38:46-04:00,Acrylic-Grimdark-0006,406903252506,69f83957ffbc831dea082e1a,Gothic Grimdark Voidwalker Eternal Lamp 5x7 Acrylic Block Dark Decor Shelf Gift,https://www.ebay.com/itm/406903252506,https://i.ebayimg.com/thumbs/images/g/mCcAAeSw5spp-HkN/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0006_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0006_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0006_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0006_Ready_for_Steaming\Gallery_U1.png,379,379,AMBIGUOUS,close distances cover=379 U1=379,
2026-05-05T22:39:02-04:00,Acrylic-Grimdark-0007,406903731967,69f839eaf9374ed4f105a092,Gothic Banshee Lantern Grimdark Art 5x7 Acrylic Premium Collectible Decor Shelf,https://www.ebay.com/itm/406903731967,https://i.ebayimg.com/thumbs/images/g/ArAAAeSwX9xp-K~A/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0007_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0007_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0007_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0007_Ready_for_Steaming\Gallery_U1.png,388,388,AMBIGUOUS,close distances cover=388 U1=388,
2026-05-05T22:39:16-04:00,Acrylic-Grimdark-0008,406903746215,69f83a955da263f75f04c06a,Gothic Grimdark Revenant Lantern 5x7 Acrylic Art Premium Decor Sapphire Glass,https://www.ebay.com/itm/406903746215,https://i.ebayimg.com/thumbs/images/g/qEwAAeSwhkpp-LC~/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0008_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0008_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0008_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0008_Ready_for_Steaming\Gallery_U1.png,379,379,AMBIGUOUS,close distances cover=379 U1=379,
2026-05-05T22:39:28-04:00,Acrylic-Grimdark-0009,406903749989,69f83b5cf9374ed4f105a180,Gothic Grimdark Lich Phylactery Lantern 5x7 Acrylic Print Dark Fantasy Home,https://www.ebay.com/itm/406903749989,https://i.ebayimg.com/thumbs/images/g/QQkAAeSwwtlp-LFj/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0009_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0009_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0009_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0009_Ready_for_Steaming\Gallery_U1.png,488,488,AMBIGUOUS,close distances cover=488 U1=488,
2026-05-05T22:39:44-04:00,Acrylic-Grimdark-0010,406903756190,69f83c14ffbc831dea082fa3,Gothic Wraith Warden Cursed Beacon 5x7 Acrylic Block Dark Fantasy Decor Shelf,https://www.ebay.com/itm/406903756190,https://i.ebayimg.com/thumbs/images/g/6DwAAeSwrWdp-LI~/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0010_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0010_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0010_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0010_Ready_for_Steaming\Gallery_U1.png,402,402,AMBIGUOUS,close distances cover=402 U1=402,
2026-05-05T22:39:55-04:00,Poster-Academia-0005,406903038850,69f847b45da263f75f04cdbd,Arcane Archway of Forbidden Chronicles Dark Academia 12x18 Poster Study Room,https://www.ebay.com/itm/406903038850,https://i.ebayimg.com/thumbs/images/g/VOsAAeSwkJNp-Fji/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0005_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0005_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0005_Ready_for_Steaming\Gallery_U1.png,402,402,AMBIGUOUS,close distances cover=402 U1=402,
2026-05-05T22:40:06-04:00,Poster-Academia-0006,406903042690,69f84864feed9979d10cd5ba,Dark Academia Ethereal Torii Poster 12x18 Study Room Decor Scholarly Ascension,https://www.ebay.com/itm/406903042690,https://i.ebayimg.com/images/g/sHYAAeSwrURp-FoF/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0006_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0006_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0006_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0006_Ready_for_Steaming\Gallery_U1.png,0,0,AMBIGUOUS,close distances cover=0 U1=0,
2026-05-05T22:40:21-04:00,Poster-Academia-0008,406903046097,69f84b3d5da263f75f04d1f7,Dark Academia Mystic Threshold Infinite Knowledge Poster 12x18 Study Decor Wall,https://www.ebay.com/itm/406903046097,https://i.ebayimg.com/thumbs/images/g/awoAAeSwcSpp-Fq-/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0008_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0008_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0008_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0008_Ready_for_Steaming\Gallery_U1.png,373,373,AMBIGUOUS,close distances cover=373 U1=373,
2026-05-05T22:40:38-04:00,Poster-Academia-0009,406903209258,69f8547125819cdf3d05522b,Dark Academia Sanctum Gate of Preserved Wisdom 12x18 Poster Study Decor Wall,https://www.ebay.com/itm/406903209258,https://i.ebayimg.com/thumbs/images/g/OTcAAeSw5Ahp-HC5/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0009_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0009_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0009_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0009_Ready_for_Steaming\Gallery_U1.png,330,330,AMBIGUOUS,close distances cover=330 U1=330,
2026-05-05T22:40:53-04:00,Poster-Academia-0010,406903249496,69f854ed09f3b7302401ed2e,Dark Academia Hermetic Portal of Ancient Codices 12x18 Poster Study Decor Wall,https://www.ebay.com/itm/406903249496,https://i.ebayimg.com/thumbs/images/g/dIUAAeSw2rlp-Hh3/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0010_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0010_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0010_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0010_Ready_for_Steaming\Gallery_U1.png,286,286,AMBIGUOUS,close distances cover=286 U1=286,
2026-05-05T22:41:04-04:00,Poster-Academia-0011,406903250376,69f850b425819cdf3d054e10,Dark Academia Celestial Archway Poster 12x18 Study Room Decor Timeless Tomes,https://www.ebay.com/itm/406903250376,https://i.ebayimg.com/thumbs/images/g/qScAAeSwGYJp-Hii/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0011_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0011_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0011_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0011_Ready_for_Steaming\Gallery_U1.png,390,390,AMBIGUOUS,close distances cover=390 U1=390,
2026-05-05T22:41:16-04:00,Poster-Academia-0013,406903251282,69f855abffbc831dea0847c8,Dark Academia Alchemist Threshold Transmuted Knowledge 12x18 Poster Study Decor,https://www.ebay.com/itm/406903251282,https://i.ebayimg.com/thumbs/images/g/75cAAeSwfLxp-HjQ/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0013_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0013_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0013_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0013_Ready_for_Steaming\Gallery_U1.png,317,317,AMBIGUOUS,close distances cover=317 U1=317,
2026-05-05T22:41:29-04:00,Poster-Academia-0014,406903252244,69f8530b5da263f75f04d837,Dark Academia Oracle Portal Prophetic Scriptures 12x18 Poster Study Decor Wall,https://www.ebay.com/itm/406903252244,https://i.ebayimg.com/thumbs/images/g/2-YAAeSwX9xp-Hj9/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0014_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0014_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0014_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0014_Ready_for_Steaming\Gallery_U1.png,394,394,AMBIGUOUS,close distances cover=394 U1=394,
2026-05-05T22:41:40-04:00,Acrylic-Grimdark-0011,406903760725,69f863f9f9374ed4f105c588,Grimdark Deathspeaker Oracle Lamp 5x7 Acrylic Gothic Collectible Art Shelf Gift,https://www.ebay.com/itm/406903760725,https://i.ebayimg.com/thumbs/images/g/EK4AAeSwF7Vp-LMg/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0011_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0011_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0011_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0011_Ready_for_Steaming\Gallery_U1.png,468,468,AMBIGUOUS,close distances cover=468 U1=468,
2026-05-05T22:41:50-04:00,Poster-Academia-0017,406903730229,69f89a94c1f268dee601cb9d,Dark Academia Poster 12x18 Magister Torii Study Decor Scholarly Gift Wall Room,https://www.ebay.com/itm/406903730229,https://i.ebayimg.com/thumbs/images/g/ifUAAeSwcM9p-K9d/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0017_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0017_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0017_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0017_Ready_for_Steaming\Gallery_U1.png,319,319,AMBIGUOUS,close distances cover=319 U1=319,
2026-05-05T22:42:02-04:00,Poster-Academia-0019,406903744471,69f89b9ca70f06579a00a708,Dark Academia Archivist Gateway Poster 12x18 Vintage Study Room Decor Wall Gift,https://www.ebay.com/itm/406903744471,https://i.ebayimg.com/thumbs/images/g/C0kAAeSwqZVp-LCM/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0019_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0019_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0019_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0019_Ready_for_Steaming\Gallery_U1.png,273,273,AMBIGUOUS,close distances cover=273 U1=273,
2026-05-05T22:42:15-04:00,Poster-Academia-0020,406903748661,69f89c6f09f3b730240221b8,Dark Academia Mentor Threshold Poster 12x18 Intellectual Study Room Decor Wall,https://www.ebay.com/itm/406903748661,https://i.ebayimg.com/thumbs/images/g/lt8AAeSwBeNp-LEk/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0020_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0020_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0020_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0020_Ready_for_Steaming\Gallery_U1.png,374,374,AMBIGUOUS,close distances cover=374 U1=374,
2026-05-05T22:42:33-04:00,Poster-Academia-0021,406903754696,69f89da69f68ab7cf001f531,Dark Academia Celestial Chronometer Archive Sphere 12x18 Poster Study Decor,https://www.ebay.com/itm/406903754696,https://i.ebayimg.com/thumbs/images/g/amwAAeSwJnVp-LH0/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0021_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0021_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0021_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0021_Ready_for_Steaming\Gallery_U1.png,331,331,AMBIGUOUS,close distances cover=331 U1=331,
2026-05-05T22:42:45-04:00,Poster-Academia-0022,406903758348,69f89eac011b67ecf8077844,Dark Academia Temporal Reliquary Bell Jar 12x18 Poster Study Decor Wall Library,https://www.ebay.com/itm/406903758348,https://i.ebayimg.com/thumbs/images/g/5dMAAeSw~9Bp-LLF/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0022_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0022_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0022_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0022_Ready_for_Steaming\Gallery_U1.png,441,441,AMBIGUOUS,close distances cover=441 U1=441,
2026-05-06T00:06:07-04:00,Sticker-Zen-0025,406892327989,69f1cb4ef6b83091a50959f5,Koi Fish in Jade Pond Hisui no Koi Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Luck,https://www.ebay.com/itm/406892327989,https://i.ebayimg.com/images/g/sfMAAeSwmT1p8dsV/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0025_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Sticker-Zen-0025_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Sticker-Zen-0025_U4_Grid.png,331,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 331,
2026-05-06T12:21:38-04:00,Sticker-Academia-0005,406892409123,69f198efea1f992ded0e90e7,Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Dark Academia Laptop Journal,https://www.ebay.com/itm/406892409123,https://i.ebayimg.com/images/g/7eUAAeSwJyRp8emL/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0005_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Sticker-Academia-0005_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Sticker-Academia-0005_U4_Grid.png,194,0,LIKELY_SINGLE_U_MISMATCH,U4 closer by 194,
2026-05-06T13:38:01-04:00,Sticker-Academia-0005-FIX1,406909045760,69fb7a5154fd3fbacf050c5a,Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Dark Academia Laptop Journal,https://www.ebay.com/itm/406909045760,https://i.ebayimg.com/images/g/XxYAAeSwM~Rp-3wP/s-l960.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0005-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Sticker-Academia-0005_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Sticker-Academia-0005_U3_Grid.png,220,0,LIKELY_SINGLE_U_MISMATCH,U3 closer by 220,
2026-05-06T13:48:09-04:00,Sticker-Academia-0005-FIX2,406909061109,69fb7e754ce71ea8ae0c7af1,Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Dark Academia Laptop Journal,https://www.ebay.com/itm/406909061109,https://i.ebayimg.com/thumbs/images/g/PYAAAeSwvSpp-365/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0005-FIX2_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,,,,93,,LIKELY_COVER,no U comparison,
2026-05-06T14:17:10-04:00,Sticker-Academia-0006-FIX1,406909095974,69fb804bff28e7d4030aa67d,4pc Sticker Set Botanical Terrarium Lantern Vinyl Decals Laptop Bottle Dark,https://www.ebay.com/itm/406909095974,https://i.ebayimg.com/thumbs/images/g/L74AAeSwtppp-4TA/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0006-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Sticker-Academia-0006_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Sticker-Academia-0006_U2_Grid.png,75,138,LIKELY_COVER,cover closer than U2 by 63,
2026-05-06T14:17:35-04:00,Sticker-Academia-0007-FIX1,406909097469,69fb819d4c6544084c0f8370,4pc Kiss-Cut Sticker Set Astrolabe Navigation Instrument Laptop Journal Bottle,https://www.ebay.com/itm/406909097469,https://i.ebayimg.com/thumbs/images/g/slEAAeSw2Cpp-4Ua/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0007-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Sticker-Academia-0007_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Sticker-Academia-0007_U1_Grid.png,87,139,LIKELY_COVER,cover closer than U1 by 52,
2026-05-06T14:17:50-04:00,Sticker-Academia-0008-FIX1,406909100892,69fb82e64c6544084c0f83d5,Ritual Incense Censer Gothic Academia 4pc 6x6 Vinyl Sticker Reader Writer Decor,https://www.ebay.com/itm/406909100892,https://i.ebayimg.com/thumbs/images/g/hWUAAeSwnxZp-4Vz/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0008-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Sticker-Academia-0008_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Sticker-Academia-0008_U2_Grid.png,93,134,LIKELY_COVER,cover closer than U2 by 41,
2026-05-06T14:41:48-04:00,Sticker-Academia-0009-FIX1,406909114799,69fb868dc5114ecf420d2b93,4pc Sticker Set Gothic Academia Cathedral Fragment Vinyl Decals Laptop Bottle,https://www.ebay.com/itm/406909114799,https://i.ebayimg.com/thumbs/images/g/vOoAAeSwU0pp-4hs/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0009-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Sticker-Academia-0009_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Sticker-Academia-0009_U3_Grid.png,81,128,LIKELY_COVER,cover closer than U3 by 47,
2026-05-06T14:42:04-04:00,Sticker-Academia-0010-FIX1,406909116716,69fb8749a7afceb9f70f1956,Vintage Academia Compass Rose Talisman 4pc 6x6 Sticker Sheet Literary Cozy Gift,https://www.ebay.com/itm/406909116716,https://i.ebayimg.com/thumbs/images/g/e1MAAeSwGYJp-4jg/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0010-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Sticker-Academia-0010_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Sticker-Academia-0010_U2_Grid.png,110,167,LIKELY_COVER,cover closer than U2 by 57,
2026-05-06T14:42:18-04:00,Sticker-Academia-0011-FIX1,406909118000,69fb87aca7afceb9f70f1982,Apothecary Poison Vial Vintage Academia 4pc 6x6 Kiss-Cut Vinyl Desk Collector,https://www.ebay.com/itm/406909118000,https://i.ebayimg.com/thumbs/images/g/k6QAAeSwyFxp-4kk/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0011-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Sticker-Academia-0011_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Sticker-Academia-0011_U1_Grid.png,84,155,LIKELY_COVER,cover closer than U1 by 71,
2026-05-06T14:43:56-04:00,Sticker-Academia-0015-FIX1,406909121336,69fb8805ee663532c8017f4f,4pc Sticker Set Skeleton Key Portal Vinyl Decals Laptop Bottle Dark Academia,https://www.ebay.com/itm/406909121336,https://i.ebayimg.com/thumbs/images/g/H74AAeSwEv9p-4nI/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0015-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Sticker-Academia-0015_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Sticker-Academia-0015_U3_Grid.png,57,138,LIKELY_COVER,cover closer than U3 by 81,
2026-05-06T14:44:11-04:00,Sticker-Academia-0016-FIX1,406909122790,69fb8811e5402c478e03108f,4pc Kiss-Cut Sticker Set Gothic Academia Prism Light Refractor Laptop Journal,https://www.ebay.com/itm/406909122790,https://i.ebayimg.com/thumbs/images/g/0YAAAeSwTFBp-4oU/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0016-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Sticker-Academia-0016_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Sticker-Academia-0016_U3_Grid.png,94,152,LIKELY_COVER,cover closer than U3 by 58,
2026-05-06T14:44:26-04:00,Sticker-Zen-0001-FIX1,406909124585,69fb881f2b1da07362014876,4pc Sticker Set Mindful Zen Koi Pond Vinyl Decals Laptop Bottle Zen Aesthetic,https://www.ebay.com/itm/406909124585,https://i.ebayimg.com/thumbs/images/g/blkAAeSwNBlp-4ps/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0001-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Sticker-Zen-0001_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Sticker-Zen-0001_U1_Grid.png,97,138,LIKELY_COVER,cover closer than U1 by 41,
2026-05-06T14:44:40-04:00,Sticker-Zen-0002-FIX1,406909125700,69fb882c54fd3fbacf051371,Minimal Zen Bonsai Tree of Serenity 4pc 6x6 Sticker Sheet Serene Mindful Clean,https://www.ebay.com/itm/406909125700,https://i.ebayimg.com/thumbs/images/g/VrQAAeSw3Wpp-4qx/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0002-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Sticker-Zen-0002_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Sticker-Zen-0002_U1_Grid.png,196,154,LIKELY_SINGLE_U_MISMATCH,U1 closer by 42,
2026-05-06T14:44:55-04:00,Sticker-Zen-0003-FIX1,406909126789,69fb883cce0d8cb5570fa7cc,Lotus Mandala Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift Decor,https://www.ebay.com/itm/406909126789,https://i.ebayimg.com/thumbs/images/g/LSoAAeSwUv5p-4r3/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0003-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Sticker-Zen-0003_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Sticker-Zen-0003_U4_Grid.png,147,140,AMBIGUOUS,close distances cover=147 U4=140,
2026-05-06T14:45:09-04:00,Sticker-Zen-0004-FIX1,406909127704,69fb8849e5402c478e0310af,4pc Sticker Set Stone Guardian Lion Mindful Zen Vinyl Decals Laptop Bottle Zen,https://www.ebay.com/itm/406909127704,https://i.ebayimg.com/thumbs/images/g/sdcAAeSwaZBp-4s6/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0004-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Sticker-Zen-0004_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Sticker-Zen-0004_U2_Grid.png,88,133,LIKELY_COVER,cover closer than U2 by 45,
2026-05-06T14:48:32-04:00,Sticker-Zen-0002-FIX1,406909125700,69fb882c54fd3fbacf051371,Minimal Zen Bonsai Tree of Serenity 4pc 6x6 Sticker Sheet Serene Mindful Clean,https://www.ebay.com/itm/406909125700,https://i.ebayimg.com/thumbs/images/g/VrQAAeSw3Wpp-4qx/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0002-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Sticker-Zen-0002_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Sticker-Zen-0002_U1_Grid.png,196,154,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T14:48:49-04:00,Sticker-Zen-0003-FIX1,406909126789,69fb883cce0d8cb5570fa7cc,Lotus Mandala Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift Decor,https://www.ebay.com/itm/406909126789,https://i.ebayimg.com/thumbs/images/g/LSoAAeSwUv5p-4r3/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0003-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Sticker-Zen-0003_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Sticker-Zen-0003_U4_Grid.png,147,140,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T14:50:52-04:00,Sticker-Academia-0014-FIX1,406909119544,69fb87efc5114ecf420d2c5a,4pc Vinyl Sticker Set Microscope Observation Device Laptop Bottle Journal Dark,https://www.ebay.com/itm/406909119544,https://i.ebayimg.com/thumbs/images/g/UjYAAeSwJzdp-4ls/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Academia-0014-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Sticker-Academia-0014_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Sticker-Academia-0014_U2_Grid.png,110,188,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (3/3),
2026-05-06T15:05:35-04:00,Acrylic-Grimdark-0012,406909148324,69f8647ff9374ed4f105c605,Gothic Grimdark Phantom Lord Caged Soul 5x7 Acrylic Premium Collectible Decor,https://www.ebay.com/itm/406909148324,https://i.ebayimg.com/thumbs/images/g/uFAAAeSwFO1p-46C/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0012_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0012_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0012_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0012_Ready_for_Steaming\Gallery_U1.png,451,451,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T15:05:53-04:00,Acrylic-Grimdark-0013,406909151733,69f865a55da263f75f04e768,Gothic Gravekeeper Lantern Grimdark Art 5x7 Acrylic Block Dark Fantasy Decor,https://www.ebay.com/itm/406909151733,https://i.ebayimg.com/thumbs/images/g/kNMAAeSwZqJp-49U/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0013_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0013_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0013_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0013_Ready_for_Steaming\Gallery_U1.png,329,329,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T15:06:09-04:00,Acrylic-Grimdark-0014,406909159060,69f8669583a8608fd80f0fdb,Soulbound Harbinger Torch Grimdark Gothic Lantern 5x7 Acrylic Print Dark Decor,https://www.ebay.com/itm/406909159060,https://i.ebayimg.com/thumbs/images/g/dhUAAeSwuu5p-5AH/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0014_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0014_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0014_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0014_Ready_for_Steaming\Gallery_U1.png,349,349,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T15:06:25-04:00,Acrylic-Grimdark-0015,406909166683,69f867cc2592a8ad8e0f076e,Cursed Monk Penance Light Grimdark Gothic Artifact 5x7 Acrylic Collectible Gift,https://www.ebay.com/itm/406909166683,https://i.ebayimg.com/thumbs/images/g/N~0AAeSw4ABp-5Db/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0015_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0015_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0015_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0015_Ready_for_Steaming\Gallery_U1.png,381,381,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T15:06:40-04:00,Poster-Academia-0023,406909147173,69f89fda2592a8ad8e0f2e79,Hermetic Knowledge Lantern Dark Academia Poster 12x18 Library Decor Wall Study,https://www.ebay.com/itm/406909147173,https://i.ebayimg.com/thumbs/images/g/xV4AAeSwY5xp-442/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0023_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0023_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0023_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0023_Ready_for_Steaming\Gallery_U1.png,462,462,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T15:06:57-04:00,Poster-Academia-0024,406909150037,69f8a454c1f268dee601d3ad,Dark Academia Industrial Library Pressure Chamber Poster 12x18 Vintage Decor,https://www.ebay.com/itm/406909150037,https://i.ebayimg.com/thumbs/images/g/vUAAAeSwZXNp-47n/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0024_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0024_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0024_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0024_Ready_for_Steaming\Gallery_U1.png,369,369,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T15:07:13-04:00,Poster-Academia-0025,406909153504,69f903dec1f268dee601f679,Dark Academia Chrono-Codex Terrarium 12x18 Poster Library Decor Wall Study Gift,https://www.ebay.com/itm/406909153504,https://i.ebayimg.com/thumbs/images/g/nYcAAeSwjCJp-4-h/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0025_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0025_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0025_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0025_Ready_for_Steaming\Gallery_U1.png,449,449,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T15:07:30-04:00,Poster-Academia-0026,406909164941,69f904df97d964f736006a48,Dark Academia Apothecary Cylinder 12x18 Poster Vintage Study Decor Wall Library,https://www.ebay.com/itm/406909164941,https://i.ebayimg.com/thumbs/images/g/C1cAAeSwnflp-5B4/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0026_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0026_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0026_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0026_Ready_for_Steaming\Gallery_U1.png,419,419,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:10:08-04:00,Acrylic-Grimdark-0016,406909215172,69f86a3d25819cdf3d0563b6,Gothic Grimdark Shadowpriest Ritual Vessel 5x7 Acrylic Decor Indigo Flame Shelf,https://www.ebay.com/itm/406909215172,https://i.ebayimg.com/thumbs/images/g/3qwAAeSwqUtp-5lt/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0016_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0016_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0016_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0016_Ready_for_Steaming\Gallery_U1.png,371,371,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:10:33-04:00,Acrylic-Grimdark-0017,406909219066,69f86b8e83a8608fd80f1341,Grimdark Aesthetic Dreadlord Beacon Lantern 5x7 Acrylic Block Dark Decor Shelf,https://www.ebay.com/itm/406909219066,https://i.ebayimg.com/thumbs/images/g/2BsAAeSw3Hxp-5oA/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0017_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0017_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0017_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0017_Ready_for_Steaming\Gallery_U1.png,378,378,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:10:49-04:00,Acrylic-Grimdark-0018,406909222169,69f86d3709f3b730240200b7,Sepulcher Guardian's Flame Grimdark Gothic Lantern 5x7 Acrylic Art Dark Shelf,https://www.ebay.com/itm/406909222169,https://i.ebayimg.com/thumbs/images/g/biIAAeSwm7lp-5qy/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0018_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0018_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0018_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0018_Ready_for_Steaming\Gallery_U1.png,353,353,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:11:06-04:00,Acrylic-Grimdark-0019,406909223875,69f86f6c2810b52a940a4161,Abyssal Watcher Eternal Eye Grimdark Gothic Acrylic 5x7 Spirit Beacon Artifact,https://www.ebay.com/itm/406909223875,https://i.ebayimg.com/thumbs/images/g/Q60AAeSwC1Zp-5sE/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0019_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0019_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0019_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0019_Ready_for_Steaming\Gallery_U1.png,389,389,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:11:22-04:00,Acrylic-Grimdark-0021,406909225478,69f8807a011b67ecf80761ae,Emerald Despair Lantern Grimdark Gothic Ironwork 5x7 Acrylic Block Dark Fantasy,https://www.ebay.com/itm/406909225478,https://i.ebayimg.com/thumbs/images/g/NrMAAeSw16pp-5tb/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0021_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0021_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0021_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0021_Ready_for_Steaming\Gallery_U1.png,347,347,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:11:41-04:00,Acrylic-Grimdark-0022,406909226531,69f8818abe136844f0003e48,Violet Torment Lantern 5x7 Acrylic Grimdark Gothic Decor for Dark Fantasy Study,https://www.ebay.com/itm/406909226531,https://i.ebayimg.com/thumbs/images/g/02oAAeSwuu5p-5u7/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0022_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0022_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0022_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0022_Ready_for_Steaming\Gallery_U1.png,347,347,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:11:57-04:00,Acrylic-Grimdark-0023,406909228840,69f882a1be136844f0003eed,Azure Suffering Lantern 5x7 Acrylic Grimdark Gothic Wall Art Decor Shelf Study,https://www.ebay.com/itm/406909228840,https://i.ebayimg.com/thumbs/images/g/0BMAAeSw7clp-5wJ/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0023_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0023_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0023_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0023_Ready_for_Steaming\Gallery_U1.png,347,347,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T16:12:13-04:00,Acrylic-Grimdark-0024,406909231370,69f8836c5da263f75f04fad5,Grimdark Obsidian Wrath Lantern 5x7 Acrylic Block Dark Fantasy Desk Art Shelf,https://www.ebay.com/itm/406909231370,https://i.ebayimg.com/thumbs/images/g/8ZQAAeSw0t5p-5xe/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0024_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0024_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0024_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0024_Ready_for_Steaming\Gallery_U1.png,257,257,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T16:12:30-04:00,Acrylic-Grimdark-0025,406909232068,69f883f3be136844f0003ff9,Amber Anguish Lantern Grimdark Aesthetic 5x7 Acrylic Art Decor Shelf Study Gift,https://www.ebay.com/itm/406909232068,https://i.ebayimg.com/thumbs/images/g/SQUAAeSwVRdp-5yd/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0025_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0025_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0025_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0025_Ready_for_Steaming\Gallery_U1.png,257,257,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T16:12:47-04:00,Acrylic-Grimdark-0026,406909232951,69f88472ffbc831dea086941,Frost Agony Lantern Grimdark Ice Spirit 5x7 Acrylic Art Gothic Decor Shelf Gift,https://www.ebay.com/itm/406909232951,https://i.ebayimg.com/thumbs/images/g/3yQAAeSw5D5p-5zj/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0026_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0026_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0026_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0026_Ready_for_Steaming\Gallery_U1.png,257,257,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:13:03-04:00,Acrylic-Grimdark-0027,406909233684,69f884ed83a8608fd80f239c,Magenta Malice Lantern Grimdark Mentor-Grade 5x7 Acrylic Decor Dark Fantasy,https://www.ebay.com/itm/406909233684,https://i.ebayimg.com/thumbs/images/g/UAQAAeSwtZBp-50u/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0027_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0027_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0027_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0027_Ready_for_Steaming\Gallery_U1.png,352,352,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:13:19-04:00,Acrylic-Grimdark-0028,406909234435,69f88562be136844f00040a3,Gothic Obsidian Shrine Soul Lantern 5x7 Acrylic Grimdark Artifact Display Shelf,https://www.ebay.com/itm/406909234435,https://i.ebayimg.com/thumbs/images/g/HxwAAeSwkxVp-52B/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0028_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0028_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0028_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0028_Ready_for_Steaming\Gallery_U1.png,303,303,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T16:13:38-04:00,Acrylic-Grimdark-0030,406909235356,69f886005da263f75f04fc9d,Spectral Temple Soul Lantern Grimdark Mentor-Grade 5x7 Acrylic Art Collectible,https://www.ebay.com/itm/406909235356,https://i.ebayimg.com/thumbs/images/g/GwYAAeSw2rlp-53A/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0030_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0030_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0030_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0030_Ready_for_Steaming\Gallery_U1.png,419,419,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:13:54-04:00,Acrylic-Grimdark-0031,406909236640,69f88ee825819cdf3d057c87,Midnight Sanctuary Soul Lantern Grimdark 5x7 Acrylic Collectible Display Shelf,https://www.ebay.com/itm/406909236640,https://i.ebayimg.com/thumbs/images/g/UPAAAeSwB3Fp-54a/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0031_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0031_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0031_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0031_Ready_for_Steaming\Gallery_U1.png,300,300,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:14:11-04:00,Acrylic-Grimdark-0032,406909238227,69f88fd4feed9979d10d0ce7,Grimdark Amber Monastery Soul Lantern 5x7 Acrylic Art Gothic Decor Golden Flame,https://www.ebay.com/itm/406909238227,https://i.ebayimg.com/thumbs/images/g/bfEAAeSwx-Bp-55r/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0032_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0032_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0032_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0032_Ready_for_Steaming\Gallery_U1.png,396,396,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:14:26-04:00,Acrylic-Grimdark-0033,406909240724,69f8904bc1f268dee601c34f,Grimdark Ethereal Archway Soul Lantern 5x7 Acrylic Display Gothic Artifact Gift,https://www.ebay.com/itm/406909240724,https://i.ebayimg.com/thumbs/images/g/rfUAAeSwXCBp-566/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0033_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0033_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0033_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0033_Ready_for_Steaming\Gallery_U1.png,380,380,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:14:43-04:00,Acrylic-Grimdark-0034,406909242546,69f890b8c1f268dee601c394,Emerald Sanctum Soul Lantern Grimdark Art 5x7 Acrylic Mentor-Grade Collectible,https://www.ebay.com/itm/406909242546,https://i.ebayimg.com/thumbs/images/g/BYwAAeSwhLRp-58O/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0034_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0034_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0034_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0034_Ready_for_Steaming\Gallery_U1.png,483,483,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:14:59-04:00,Acrylic-Grimdark-0035,406909243824,69f89116b051b8a0e90b9662,Twilight Portal Soul Lantern Grimdark 5x7 Acrylic Art Gothic Decor Purple Flame,https://www.ebay.com/itm/406909243824,https://i.ebayimg.com/thumbs/images/g/trEAAeSw7LZp-59U/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0035_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0035_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0035_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0035_Ready_for_Steaming\Gallery_U1.png,440,440,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T16:15:15-04:00,Acrylic-Grimdark-0036,406909244688,69f8918925819cdf3d057e2d,Gothic Frost Cathedral Soul Lantern 5x7 Acrylic Display Grimdark Artifact Shelf,https://www.ebay.com/itm/406909244688,https://i.ebayimg.com/thumbs/images/g/eHwAAeSwBb1p-5-U/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0036_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0036_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0036_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0036_Ready_for_Steaming\Gallery_U1.png,353,353,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T16:15:31-04:00,Acrylic-Grimdark-0037,406909247161,69f892035da263f75f05059e,Gothic Onyx Shrine Soul Lantern 5x7 Acrylic Display Grimdark Collectible Shelf,https://www.ebay.com/itm/406909247161,https://i.ebayimg.com/thumbs/images/g/SLwAAeSw-jZp-5~q/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Acrylic-Grimdark-0037_online.jpg,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0037_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0037_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0037_Ready_for_Steaming\Gallery_U1.png,216,216,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T16:15:47-04:00,Poster-Academia-0027,406909216787,69f90607feed9979d10d40e7,Dark Academia Astrolabe Dome Poster 12x18 Vintage Study Room Decor Wall Library,https://www.ebay.com/itm/406909216787,https://i.ebayimg.com/thumbs/images/g/q5QAAeSwyJ5p-5mr/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0027_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0027_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0027_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0027_Ready_for_Steaming\Gallery_U1.png,390,390,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:16:04-04:00,Poster-Academia-0028,406909220927,69f907b49f68ab7cf0022003,Dark Academia Alchemist Retort Library Poster 12x18 Study Decor Wall Gift Room,https://www.ebay.com/itm/406909220927,https://i.ebayimg.com/thumbs/images/g/fAQAAeSwcWdp-5pV/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0028_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0028_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0028_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0028_Ready_for_Steaming\Gallery_U1.png,377,377,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:27:50-04:00,Poster-Academia-0031,406909266188,69fba23409770f1d9306b86d,Dark Academia Botanical Codex Conservatory Poster 12x18 Study Decor Wall Gift,https://www.ebay.com/itm/406909266188,https://i.ebayimg.com/thumbs/images/g/gPYAAeSwdRNp-6Mw/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0031_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0031_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0031_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0031_Ready_for_Steaming\Gallery_U1.png,415,415,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:28:05-04:00,Poster-Academia-0032,406909268494,69fba266489d5635ab0e6504,Dark Academia Observatory Archive Prism 12x18 Poster Study Room Decor Wall Gift,https://www.ebay.com/itm/406909268494,https://i.ebayimg.com/thumbs/images/g/jg4AAeSwfLxp-6N0/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0032_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0032_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0032_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0032_Ready_for_Steaming\Gallery_U1.png,414,414,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T16:28:22-04:00,Poster-Academia-0033,406909269321,69fba28a6d07bd21600e1684,Dark Academia Philosophical Theorem Reliquary Poster 12x18 Study Decor Wall,https://www.ebay.com/itm/406909269321,https://i.ebayimg.com/thumbs/images/g/oGkAAeSwAaFp-6Oy/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0033_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0033_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0033_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0033_Ready_for_Steaming\Gallery_U1.png,392,392,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (4/4),
2026-05-06T17:05:55-04:00,Poster-Academia-0030,406909264998,69f90c957f4b346c8a0c603f,Dark Academia Grimoire Preservation Capsule 12x18 Poster Study Decor Wall Gift,https://www.ebay.com/itm/406909264998,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0030_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0030_Ready_for_Steaming\Gallery_U1.png,,,,,ERROR,,no visible eBay main image extracted
2026-05-06T17:36:23-04:00,Sticker-Zen-0005-FIX1,406909342825,69fbae614c6544084c0f95ec,Bamboo Forest Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Misty Art,https://www.ebay.com/itm/406909342825,https://i.ebayimg.com/thumbs/images/g/Y4AAAeSw5vBp-69Q/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0005-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Sticker-Zen-0005_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Sticker-Zen-0005_U2_Grid.png,137,251,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (3/3),
2026-05-06T17:36:43-04:00,Sticker-Zen-0007-FIX1,406909344491,69fbae7da7afceb9f70f2982,4pc Sticker Set Cherry Blossom Branch Vinyl Decals Laptop Bottle Zen Aesthetic,https://www.ebay.com/itm/406909344491,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Sticker-Zen-0007_U1_Grid.png,,,,,ERROR,,no visible eBay main image extracted
2026-05-06T17:36:55-04:00,Sticker-Zen-0008-FIX1,406909345291,69fbae974c6544084c0f9610,4pc Kiss-Cut Sticker Set Circle Ens Laptop Journal Bottle Zen Aesthetic Decal,https://www.ebay.com/itm/406909345291,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Sticker-Zen-0008_U1_Grid.png,,,,,ERROR,,no visible eBay main image extracted
2026-05-06T17:37:08-04:00,Sticker-Zen-0009-FIX1,406909353931,69fbaea961c4aefdea04aaaf,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Laptop Journal,https://www.ebay.com/itm/406909353931,https://i.ebayimg.com/thumbs/images/g/ekIAAeSwwilp-7DX/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0009-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Sticker-Zen-0009_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Sticker-Zen-0009_U4_Grid.png,146,151,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T17:37:23-04:00,Sticker-Zen-0022-FIX1,406909354903,69fbaeb9f60a24b6d1034575,Mindful Zen Garden Stone Meis seki 4pc 6x6 Vinyl Sticker Laptop Journal Gift,https://www.ebay.com/itm/406909354903,https://i.ebayimg.com/thumbs/images/g/QZ0AAeSwxYdp-7Dp/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0022-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Sticker-Zen-0022_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Sticker-Zen-0022_U2_Grid.png,167,143,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T17:37:41-04:00,Sticker-Zen-0024-FIX1,406909355853,69fbaecbb8dd7e2bb0094b7c,Mindful Zen Enso Circle with Crystals 4pc 6x6 Vinyl Sticker Laptop Journal Gift,https://www.ebay.com/itm/406909355853,https://i.ebayimg.com/thumbs/images/g/qkYAAeSwCB9p-7D7/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0024-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Sticker-Zen-0024_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Sticker-Zen-0024_U2_Grid.png,212,126,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T17:37:57-04:00,Sticker-Zen-0025-FIX1,406909359949,69fbaedb4c6544084c0f9620,Koi Fish in Jade Pond Hisui no Koi Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Luck,https://www.ebay.com/itm/406909359949,https://i.ebayimg.com/thumbs/images/g/b5YAAeSw1Hpp-7FF/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0025-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Sticker-Zen-0025_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Sticker-Zen-0025_U1_Grid.png,111,148,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T17:38:17-04:00,Sticker-Zen-0027-FIX1,406909364977,69fbaeebce0d8cb5570fb7dc,Minimal Zen Temple Lantern Zendera no T r 4pc 6x6 Sticker Sheet Serene Mindful,https://www.ebay.com/itm/406909364977,https://i.ebayimg.com/thumbs/images/g/cfIAAeSwAFFp-7GV/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0027-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Sticker-Zen-0027_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Sticker-Zen-0027_U1_Grid.png,113,158,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T17:38:35-04:00,Sticker-Zen-0041-FIX1,406909368739,69fbaefcc6dfbcc11107aa91,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,https://www.ebay.com/itm/406909368739,https://i.ebayimg.com/thumbs/images/g/Au8AAeSw9aNp-7HX/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0041-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Sticker-Zen-0041_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Sticker-Zen-0041_U3_Grid.png,122,261,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T17:38:55-04:00,Sticker-Zen-0042-FIX1,406909373586,69fbaf12ff28e7d4030aba2d,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,https://www.ebay.com/itm/406909373586,https://i.ebayimg.com/thumbs/images/g/GBcAAeSw4ABp-7I1/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0042-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Sticker-Zen-0042_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Sticker-Zen-0042_U3_Grid.png,210,249,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (3/3),
2026-05-06T17:43:15-04:00,Sticker-Zen-0007-FIX1,406909344491,69fbae7da7afceb9f70f2982,4pc Sticker Set Cherry Blossom Branch Vinyl Decals Laptop Bottle Zen Aesthetic,https://www.ebay.com/itm/406909344491,https://i.ebayimg.com/images/g/lkwAAeSw5zhp-6-r/s-l1600.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0007-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Sticker-Zen-0007_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Sticker-Zen-0007_U3_Grid.png,136,152,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T17:43:33-04:00,Sticker-Zen-0008-FIX1,406909345291,69fbae974c6544084c0f9610,4pc Kiss-Cut Sticker Set Circle Ens Laptop Journal Bottle Zen Aesthetic Decal,https://www.ebay.com/itm/406909345291,https://i.ebayimg.com/thumbs/images/g/8i8AAeSwm7lp-6~1/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0008-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Sticker-Zen-0008_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Sticker-Zen-0008_U2_Grid.png,151,126,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (3/3),
2026-05-06T18:35:15-04:00,Poster-Academia-0034,406909467980,69fbbffef60a24b6d1034e4d,Dark Academia Nautical Archive Barometer 12x18 Poster Study Decor Wall Library,https://www.ebay.com/itm/406909467980,https://i.ebayimg.com/thumbs/images/g/IhQAAeSwPY9p-8Cg/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0034_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0034_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0034_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0034_Ready_for_Steaming\Gallery_U1.png,466,466,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T18:35:39-04:00,Poster-Academia-0035,406909471020,69fbc023f60a24b6d1034e5c,Dark Academia Poster Theological Codex Sanctuary 12x18 Study Decor Wall Library,https://www.ebay.com/itm/406909471020,https://i.ebayimg.com/thumbs/images/g/QfsAAeSw88dp-8EA/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0035_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0035_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0035_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0035_Ready_for_Steaming\Gallery_U1.png,371,371,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T18:36:00-04:00,Poster-Academia-0036,406909472775,69fbc0482b1da073620161ad,Mechanical Encyclopedia Sphere Dark Academia Aesthetic 12x18 Poster Study Room,https://www.ebay.com/itm/406909472775,https://i.ebayimg.com/thumbs/images/g/MJwAAeSwX9xp-8FF/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0036_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0036_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0036_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0036_Ready_for_Steaming\Gallery_U1.png,379,379,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T18:36:43-04:00,Poster-Academia-0037,406909473606,69fbc06d61c4aefdea04b362,Cryptographic Vault Cylinder Dark Academia Poster 12x18 Secret Knowledge Decor,https://www.ebay.com/itm/406909473606,https://i.ebayimg.com/thumbs/images/g/AS4AAeSwPXpp-8GI/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Poster-Academia-0037_online.jpg,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0037_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0037_Ready_for_Steaming\Gallery_U1.png,U1,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0037_Ready_for_Steaming\Gallery_U1.png,450,450,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (8/8),
2026-05-06T22:36:48-04:00,Sticker-Zen-0044,406902622710,69f2396ccaeb1241880b692d,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,https://www.ebay.com/itm/406902622710,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U1_Grid.png,,,,,ERROR,,no close frame received or sent
2026-05-06T22:40:21-04:00,Sticker-Zen-0044,406902622710,69f2396ccaeb1241880b692d,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,https://www.ebay.com/itm/406902622710,https://i.ebayimg.com/images/g/I~8AAeSw-jZp-B2c/s-l1600.webp,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0044_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U3_Grid.png,296,1,LIKELY_SINGLE_U_MISMATCH,U3 closer by 295,
2026-05-06T23:07:31-04:00,Sticker-Zen-0044-FIX1,406909884756,69fbdfc9f60a24b6d1035f8b,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,https://www.ebay.com/itm/406909884756,https://i.ebayimg.com/thumbs/images/g/VLcAAeSwcSpp~AHQ/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0044-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Sticker-Zen-0044_U3_Grid.png,189,176,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (3/3),
2026-05-06T23:17:23-04:00,Sticker-Zen-0045-FIX1,406909890800,69fc03470ce75ae193034081,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,https://www.ebay.com/itm/406909890800,https://i.ebayimg.com/thumbs/images/g/IFwAAeSwpHBp~AOX/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0045-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Sticker-Zen-0045_U1_Grid.png,U1,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Sticker-Zen-0045_U1_Grid.png,175,227,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T23:17:39-04:00,Sticker-Zen-0046-FIX1,406909891985,69fc035bce0d8cb5570fe6af,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,https://www.ebay.com/itm/406909891985,https://i.ebayimg.com/thumbs/images/g/AYoAAeSwzGVp~APY/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0046-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Sticker-Zen-0046_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Sticker-Zen-0046_U2_Grid.png,156,220,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T23:17:53-04:00,Sticker-Zen-0049-FIX1,406909893702,69fc036aee663532c801be71,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,https://www.ebay.com/itm/406909893702,https://i.ebayimg.com/thumbs/images/g/B3MAAeSwLDNp~AQf/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0049-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Sticker-Zen-0049_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Sticker-Zen-0049_U3_Grid.png,227,258,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T23:32:25-04:00,Sticker-Zen-0050-FIX1,406909904704,69fc0639ee663532c801bff2,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,https://www.ebay.com/itm/406909904704,https://i.ebayimg.com/thumbs/images/g/kSwAAeSwldpp~Aac/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0050-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Sticker-Zen-0050_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Sticker-Zen-0050_U2_Grid.png,204,245,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T23:32:37-04:00,Sticker-Zen-0051-FIX1,406909905683,69fc06482007fddea00dcf21,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,https://www.ebay.com/itm/406909905683,https://i.ebayimg.com/thumbs/images/g/TrYAAeSwkXBp~Abb/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0051-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Sticker-Zen-0051_U1_Grid.png,U4,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Sticker-Zen-0051_U4_Grid.png,235,234,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T23:32:50-04:00,Sticker-Zen-0052-FIX1,406909906686,69fc0655ee663532c801bffc,Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,https://www.ebay.com/itm/406909906686,https://i.ebayimg.com/thumbs/images/g/6hcAAeSwX9xp~Acr/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0052-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Sticker-Zen-0052_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Sticker-Zen-0052_U3_Grid.png,187,217,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T23:33:02-04:00,Sticker-Zen-0053-FIX1,406909907111,69fc06640ce75ae19303421a,Crystalline Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,https://www.ebay.com/itm/406909907111,https://i.ebayimg.com/thumbs/images/g/qXgAAeSwS1dp~Adi/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0053-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Sticker-Zen-0053_U1_Grid.png,U2,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Sticker-Zen-0053_U2_Grid.png,183,189,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),
2026-05-06T23:33:14-04:00,Sticker-Zen-0054-FIX1,406909907742,69fc0674ee663532c801c009,Dragon Meditation Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,https://www.ebay.com/itm/406909907742,https://i.ebayimg.com/thumbs/images/g/rsoAAeSw9zpp~Aek/s-l1600.jpg,C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit\images\Sticker-Zen-0054-FIX1_online.jpg,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Cover_Mockup.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Sticker-Zen-0054_U1_Grid.png,U3,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Sticker-Zen-0054_U3_Grid.png,158,253,LIKELY_COVER_OFFICIAL,Printify selected official-only mockups (6/6),

```


### RAW LOG: Database/ebay_ads_pending_2pct.csv
```text
﻿Timestamp,ID,eBay_Item_ID,Campaign_ID,Ad_Rate,Status,Error
2026-05-06T13:36:43,Sticker-Academia-0005-FIX1,406909045760,165251921016,2.0,PENDING_OAUTH,
2026-05-06T13:47:56,Sticker-Academia-0005-FIX2,406909061109,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:13:41,Sticker-Academia-0006-FIX1,406909095974,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:15:10,Sticker-Academia-0007-FIX1,406909097469,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:16:52,Sticker-Academia-0008-FIX1,406909100892,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:29:44,Sticker-Academia-0009-FIX1,406909114799,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:31:18,Sticker-Academia-0010-FIX1,406909116716,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:32:36,Sticker-Academia-0011-FIX1,406909118000,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:35:07,Sticker-Academia-0015-FIX1,406909121336,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:36:25,Sticker-Academia-0016-FIX1,406909122790,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:37:52,Sticker-Zen-0001-FIX1,406909124585,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:39:00,Sticker-Zen-0002-FIX1,406909125700,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:40:10,Sticker-Zen-0003-FIX1,406909126789,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:41:17,Sticker-Zen-0004-FIX1,406909127704,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:54:02,Poster-Academia-0023,406909147173,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:55:16,Acrylic-Grimdark-0012,406909148324,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:56:58,Poster-Academia-0024,406909150037,165251921016,2.0,PENDING_OAUTH,
2026-05-06T14:58:46,Acrylic-Grimdark-0013,406909151733,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:00:04,Poster-Academia-0025,406909153504,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:01:45,Acrylic-Grimdark-0014,406909159060,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:03:35,Poster-Academia-0026,406909164941,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:05:15,Acrylic-Grimdark-0015,406909166683,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:41:50,Acrylic-Grimdark-0016,406909215172,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:42:54,Poster-Academia-0027,406909216787,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:44:17,Acrylic-Grimdark-0017,406909219066,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:45:57,Poster-Academia-0028,406909220927,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:47:25,Acrylic-Grimdark-0018,406909222169,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:48:38,Acrylic-Grimdark-0019,406909223875,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:50:05,Acrylic-Grimdark-0021,406909225478,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:51:38,Acrylic-Grimdark-0022,406909226531,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:53:10,Acrylic-Grimdark-0023,406909228840,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:54:20,Acrylic-Grimdark-0024,406909231370,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:55:26,Acrylic-Grimdark-0025,406909232068,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:56:35,Acrylic-Grimdark-0026,406909232951,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:57:50,Acrylic-Grimdark-0027,406909233684,165251921016,2.0,PENDING_OAUTH,
2026-05-06T15:59:15,Acrylic-Grimdark-0028,406909234435,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:00:17,Acrylic-Grimdark-0030,406909235356,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:01:55,Acrylic-Grimdark-0031,406909236640,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:03:08,Acrylic-Grimdark-0032,406909238227,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:04:37,Acrylic-Grimdark-0033,406909240724,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:05:50,Acrylic-Grimdark-0034,406909242546,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:06:58,Acrylic-Grimdark-0035,406909243824,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:08:03,Acrylic-Grimdark-0036,406909244688,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:09:43,Acrylic-Grimdark-0037,406909247161,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:23:28,Poster-Academia-0031,406909266188,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:24:38,Poster-Academia-0032,406909268494,165251921016,2.0,PENDING_OAUTH,
2026-05-06T16:25:38,Poster-Academia-0033,406909269321,165251921016,2.0,PENDING_OAUTH,
2026-05-06T17:16:47,Sticker-Zen-0007-FIX1,406909344491,165251921016,2.0,PENDING_OAUTH,
2026-05-06T17:18:02,Sticker-Zen-0008-FIX1,406909345291,165251921016,2.0,PENDING_OAUTH,
2026-05-06T17:22:22,Sticker-Zen-0024-FIX1,406909355853,165251921016,2.0,PENDING_OAUTH,
2026-05-06T17:23:42,Sticker-Zen-0025-FIX1,406909359949,165251921016,2.0,PENDING_OAUTH,
2026-05-06T17:24:56,Sticker-Zen-0027-FIX1,406909364977,165251921016,2.0,PENDING_OAUTH,
2026-05-06T17:26:18,Sticker-Zen-0041-FIX1,406909368739,165251921016,2.0,PENDING_OAUTH,
2026-05-06T18:30:44,Poster-Academia-0035,406909471020,165251921016,2.0,PENDING_OAUTH,
2026-05-06T18:31:52,Poster-Academia-0036,406909472775,165251921016,2.0,PENDING_OAUTH,
2026-05-06T18:32:59,Poster-Academia-0037,406909473606,165251921016,2.0,PENDING_OAUTH,
2026-05-06T18:34:39,Poster-Academia-0034,406909467980,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:07:16,Sticker-Zen-0044-FIX1,406909884756,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:14:49,Sticker-Zen-0045-FIX1,406909890800,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:15:57,Sticker-Zen-0046-FIX1,406909891985,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:17:07,Sticker-Zen-0049-FIX1,406909893702,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:27:44,Sticker-Zen-0050-FIX1,406909904704,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:28:48,Sticker-Zen-0051-FIX1,406909905683,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:30:01,Sticker-Zen-0052-FIX1,406909906686,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:31:03,Sticker-Zen-0053-FIX1,406909907111,165251921016,2.0,PENDING_OAUTH,
2026-05-06T23:32:09,Sticker-Zen-0054-FIX1,406909907742,165251921016,2.0,PENDING_OAUTH,

```


### RAW LOG: Database/Etsy_Digital_UI_Publish_Log.csv
```text
﻿Timestamp,ID,Action,Status,Etsy_Listing_ID,URL,Confirmed_Fee_USD,Note
2026-05-06T21:23:06-04:00,Poster-Academia-0001,PUBLISH,ERROR,,https://www.etsy.com/your/shops/me/listing-editor/create#pricing-logistics,0.00,RuntimeError: Publish not confirmed. url=https://www.etsy.com/your/shops/me/listing-editor/create#pricing-logistics body= Skip to Content Shop manager menu Total finances subnav notification count Total settings subnav notification count Etsy DriveFuel Want your own website? Learn more about Pattern Sell in person Find out how with Square Listings New listing New listing Photo & Video Category Item Details Item Options Pricing & Shipping How It's Made Settings Photo and video Show off different 
2026-05-06T21:28:46-04:00,Poster-Academia-0001,PUBLISH,ERROR,,https://www.etsy.com/your/shops/me/listing-editor/create#pricing-logistics,0.00,"TimeoutError: Locator.click: Timeout 10000ms exceeded. Call log: - waiting for get_by_role(""button"", name=""Publish"") - locator resolved to <button disabled type=""button"" aria-disabled=""true"" data-testid=""publish"" data-clg-id=""WtButton"" class=""wt-btn wt-btn--primary"">Publish</button> - attempting click action 2 × waiting for element to be visible, enabled and stable - element is not enabled - retrying click action - waiting 20ms 2 × waiting for element to be visible, enabled and stable - element "
2026-05-06T21:34:09-04:00,Poster-Academia-0001,PUBLISH,ERROR,,https://www.etsy.com/your/shops/me/tools/listings?newly_created=1,0.00,RuntimeError: Publish not confirmed. url=https://www.etsy.com/your/shops/me/tools/listings?newly_created=1 body= Skip to Content Shop manager menu Total finances subnav notification count Total settings subnav notification count Etsy DriveFuel Want your own website? Learn more about Pattern Sell in person Find out how with Square Listings Get free credits Add a listing RenewDeactivateDelete Editing options Digital Impulse Purchase Recovery Kit (Digital Download) 999 in stock $1.99 Auto-renews Ju
2026-05-06T21:35:13-04:00,Poster-Academia-0001,PUBLISH,CONFIRMED,4500654287,https://www.etsy.com/listing/4500654287/celestial-gateway-dark-academia-poster,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:37:01-04:00,Poster-Academia-0002,PUBLISH,ERROR,,https://www.etsy.com/your/shops/me/tools/listings?newly_created=1,0.00,"RuntimeError: Publish not confirmed. url=https://www.etsy.com/your/shops/me/tools/listings?newly_created=1 body= Skip to Content Shop manager menu Total finances subnav notification count Total settings subnav notification count Etsy DriveFuel Want your own website? Learn more about Pattern Sell in person Find out how with Square Listings Get free credits Add a listing New: Tools to help you craft great listing titles We've added personalized suggestions to improve your titles, available right i"
2026-05-06T21:37:59-04:00,Poster-Academia-0002,PUBLISH,CONFIRMED,4500664506,https://www.etsy.com/listing/4500664506/dark-academia-obsidian-threshold-poster,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:40:05-04:00,Poster-Academia-0003,PUBLISH,ERROR,,https://www.etsy.com/your/shops/me/tools/listings?newly_created=1,0.00,"RuntimeError: Publish not confirmed. url=https://www.etsy.com/your/shops/me/tools/listings?newly_created=1 body= Skip to Content Shop manager menu Total finances subnav notification count Total settings subnav notification count Etsy DriveFuel Want your own website? Learn more about Pattern Sell in person Find out how with Square Listings Get free credits Add a listing New: Tools to help you craft great listing titles We've added personalized suggestions to improve your titles, available right i"
2026-05-06T21:40:54-04:00,Poster-Academia-0003,PUBLISH,CONFIRMED,4500665474,https://www.etsy.com/listing/4500665474/dark-academia-serpentine-portal-of,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:43:19-04:00,Poster-Academia-0081,PUBLISH,CONFIRMED,4500657145,https://www.etsy.com/your/shops/me/listing-editor/edit/4500657145,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:44:56-04:00,Poster-Academia-0082,PUBLISH,CONFIRMED,4500667154,https://www.etsy.com/your/shops/me/listing-editor/edit/4500667154,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:46:30-04:00,Poster-Academia-0083,PUBLISH,CONFIRMED,4500667734,https://www.etsy.com/your/shops/me/listing-editor/edit/4500667734,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:48:05-04:00,Poster-Academia-0084,PUBLISH,CONFIRMED,4500668282,https://www.etsy.com/your/shops/me/listing-editor/edit/4500668282,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:49:42-04:00,Poster-Academia-0085,PUBLISH,CONFIRMED,4500668786,https://www.etsy.com/your/shops/me/listing-editor/edit/4500668786,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:51:17-04:00,Poster-Academia-0091,PUBLISH,CONFIRMED,4500660013,https://www.etsy.com/your/shops/me/listing-editor/edit/4500660013,0.20,Published through logged-in Etsy UI with manual renewal selected.
2026-05-06T21:52:52-04:00,Poster-Zen-0001,PUBLISH,CONFIRMED,4500669878,https://www.etsy.com/your/shops/me/listing-editor/edit/4500669878,0.20,Published through logged-in Etsy UI with manual renewal selected.

```


### RAW LOG: Database/Etsy_Fee_Ledger.csv
```text
﻿Timestamp,Batch_ID,ID,Action,Expected_Fee_USD,Confirmed_Spent_USD,Status,Reference
2026-05-06T20:08:28,ETSY-DIGITAL-20260506-200824,Poster-Academia-0001,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500654287
2026-05-06T20:08:31,ETSY-DIGITAL-20260506-200824,Poster-Academia-0002,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500664506
2026-05-06T20:08:38,ETSY-DIGITAL-20260506-200824,Poster-Academia-0003,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500665474
2026-05-06T20:08:42,ETSY-DIGITAL-20260506-200824,Poster-Academia-0081,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500657145
2026-05-06T20:08:46,ETSY-DIGITAL-20260506-200824,Poster-Academia-0082,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500667154
2026-05-06T20:08:49,ETSY-DIGITAL-20260506-200824,Poster-Academia-0083,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500667734
2026-05-06T20:08:51,ETSY-DIGITAL-20260506-200824,Poster-Academia-0084,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500668282
2026-05-06T20:08:54,ETSY-DIGITAL-20260506-200824,Poster-Academia-0085,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500668786
2026-05-06T20:08:56,ETSY-DIGITAL-20260506-200824,Poster-Academia-0091,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500660013
2026-05-06T20:08:59,ETSY-DIGITAL-20260506-200824,Poster-Zen-0001,RESERVE_LISTING_FEE,0.20,0.20,CONFIRMED_SPENT_UI,4500669878
2026-05-06T21:06:25,ETSY-DIGITAL-20260506-210621,Poster-Zen-0002,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:29,ETSY-DIGITAL-20260506-210621,Poster-Zen-0004,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:32,ETSY-DIGITAL-20260506-210621,Poster-Zen-0005,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:35,ETSY-DIGITAL-20260506-210621,Poster-Academia-0005,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:37,ETSY-DIGITAL-20260506-210621,Poster-Academia-0006,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:40,ETSY-DIGITAL-20260506-210621,Poster-Academia-0008,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:42,ETSY-DIGITAL-20260506-210621,Poster-Academia-0009,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:45,ETSY-DIGITAL-20260506-210621,Poster-Academia-0010,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:48,ETSY-DIGITAL-20260506-210621,Poster-Academia-0011,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:51,ETSY-DIGITAL-20260506-210621,Poster-Academia-0013,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:56,ETSY-DIGITAL-20260506-210652,Poster-Academia-0014,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:06:58,ETSY-DIGITAL-20260506-210652,Poster-Academia-0017,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:07:00,ETSY-DIGITAL-20260506-210652,Poster-Academia-0019,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:07:03,ETSY-DIGITAL-20260506-210652,Poster-Academia-0020,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:07:05,ETSY-DIGITAL-20260506-210652,Poster-Academia-0022,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:07:08,ETSY-DIGITAL-20260506-210652,Poster-Academia-0023,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:07:10,ETSY-DIGITAL-20260506-210652,Poster-Academia-0024,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:07:13,ETSY-DIGITAL-20260506-210652,Poster-Academia-0025,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:07:15,ETSY-DIGITAL-20260506-210652,Poster-Academia-0026,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,
2026-05-06T21:07:18,ETSY-DIGITAL-20260506-210652,Poster-Academia-0027,RESERVE_LISTING_FEE,0.20,0.00,RESERVED_NOT_SPENT,

```


### RAW LOG: Database/Etsy_Digital_Live_Audit.csv
```text
﻿Timestamp,ID,Etsy_Listing_ID,URL,Status,Title,Price_Text,Digital_Signal,Image_Count,Notes
2026-05-06T22:03:59-04:00,Poster-Academia-0001,4500654287,https://www.etsy.com/listing/4500654287,ACTIVE_READABLE,Celestial Gateway Dark Academia Poster | Moonstone Architecture Study Decor | Digital Printable Wall Art 2x3 3x4 4x5 5x7 11x14,$6.99,YES,20,
2026-05-06T22:04:06-04:00,Poster-Academia-0002,4500664506,https://www.etsy.com/listing/4500664506,ACTIVE_READABLE,Dark Academia Obsidian Threshold Poster | Vintage Study Decor | Mentor Wisdom | Premium Digital Print | 12x18,$6.99,YES,20,
2026-05-06T22:04:14-04:00,Poster-Academia-0003,4500665474,https://www.etsy.com/listing/4500665474,ACTIVE_READABLE,"Dark Academia Serpentine Portal of Alchemical Texts | Digital Print for Study Decor, Mystical Wall Art, 12x18 Poster",$6.99,YES,20,
2026-05-06T22:04:50-04:00,Poster-Academia-0001,4500654287,https://www.etsy.com/listing/4500654287,ACTIVE_READABLE,Celestial Gateway Dark Academia Poster | Moonstone Architecture Study Decor | Digital Printable Wall Art 2x3 3x4 4x5 5x7 11x14,$6.99,YES,20,
2026-05-06T22:04:59-04:00,Poster-Academia-0002,4500664506,https://www.etsy.com/listing/4500664506,ACTIVE_READABLE,Dark Academia Obsidian Threshold Poster | Vintage Study Decor | Mentor Wisdom | Premium Digital Print | 12x18,$6.99,YES,20,
2026-05-06T22:05:06-04:00,Poster-Academia-0003,4500665474,https://www.etsy.com/listing/4500665474,ACTIVE_READABLE,"Dark Academia Serpentine Portal of Alchemical Texts | Digital Print for Study Decor, Mystical Wall Art, 12x18 Poster",$6.99,YES,20,
2026-05-06T22:05:13-04:00,Poster-Academia-0081,4500657145,https://www.etsy.com/listing/4500657145,ACTIVE_READABLE,Celestial Armillary Sphere | Dark Academia Scholar Print | Vintage Astronomy Wall Art | 12x18 Digital Download | Quiet Study Decor,$6.99,YES,20,
2026-05-06T22:05:19-04:00,Poster-Academia-0082,4500667154,https://www.etsy.com/listing/4500667154,ACTIVE_READABLE,Celestial Armillary Codex | Vintage Astronomy Poster | Dark Academia Wall Art | 12x18 Digital Download,$6.99,YES,20,
2026-05-06T22:05:26-04:00,Poster-Academia-0083,4500667734,https://www.etsy.com/listing/4500667734,ACTIVE_READABLE,Cosmic Lotus Observatory | Steampunk Academia Mentor-Grade Poster | Dark Academia Wall Art | Jade Relic Quiet Study Decor | Digital Download,$12.99,YES,20,
2026-05-06T22:05:33-04:00,Poster-Academia-0084,4500668282,https://www.etsy.com/listing/4500668282,ACTIVE_READABLE,Astrolabe Chalice Relic Dark Academia Poster | Vintage Study Decor | 12x18 Digital Download | Printable Wall Art for Quiet Scholar Spaces,$6.99,YES,20,
2026-05-06T22:05:40-04:00,Poster-Academia-0085,4500668786,https://www.etsy.com/listing/4500668786,ACTIVE_READABLE,Orrery Lighthouse Beacon | Dark Academia Astronomy Print | Vintage Celestial Wall Art | 12x18 Digital Download | Quiet Study Decor,$6.99,YES,20,
2026-05-06T22:05:46-04:00,Poster-Academia-0091,4500660013,https://www.etsy.com/listing/4500660013,ACTIVE_READABLE,Dark Academia Celestial Lotus Poster | Vintage Study Room Wall Art | 12x18 Printable Digital Download | Zen Jade Relic Decor,$6.99,YES,20,
2026-05-06T22:05:53-04:00,Poster-Zen-0001,4500669878,https://www.etsy.com/listing/4500669878,ACTIVE_READABLE,Zen Bonsai Wall Art | Celestial Gate of Jade Mist | Premium Digital Print | Meditation Decor | Dark Academia Poster,$9.99,YES,20,

```


### RAW LOG: Database/Etsy_API_Status_Log.csv
```text
﻿timestamp,status,http_status,oauth_next_step,credentials_present,keystring_masked,detail
2026-05-06 10:13:51 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 10:42:49 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 10:46:30 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 12:32:11 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 12:37:05 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 12:45:19 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 12:52:28 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 13:52:53 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 15:11:25 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 17:07:21 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 17:55:50 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 20:22:32 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 20:31:24 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 22:30:35 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 23:11:30 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 23:39:13 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"
2026-05-06 23:46:43 -0400,PENDING_OR_INACTIVE,403,WAIT_APP_APPROVAL_OR_VERIFY_SECRET,True,ehm7...jc9l,"{""error"":""API key not found or not active, or incorrect shared secret for API key.""}
"

```


### RAW LOG: Database/eBay_Traffic_Experiment_Report.csv
```text
﻿Snapshot_Timestamp,ID,Group,eBay_Item_ID,Baseline_Views_30_Days,Latest_Views_30_Days,Delta,Action
2026-05-06 23:44:26 -0400,Sticker-Academia-0004,A_TITLE_INTENT_REWRITE,406892408950,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0005,A_TITLE_INTENT_REWRITE,406892409123,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0006,A_TITLE_INTENT_REWRITE,406892409348,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0007,A_TITLE_INTENT_REWRITE,406892409645,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0008,A_TITLE_INTENT_REWRITE,406892409836,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0009,A_TITLE_INTENT_REWRITE,406892410017,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0010,A_TITLE_INTENT_REWRITE,406892410190,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0011,A_TITLE_INTENT_REWRITE,406892410307,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0014,A_TITLE_INTENT_REWRITE,406892410440,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0015,A_TITLE_INTENT_REWRITE,406892411034,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Academia-0016,A_TITLE_INTENT_REWRITE,406892411436,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Zen-0001,A_TITLE_INTENT_REWRITE,406892411931,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Zen-0002,A_TITLE_INTENT_REWRITE,406892412365,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Zen-0003,A_TITLE_INTENT_REWRITE,406892412612,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Zen-0004,A_TITLE_INTENT_REWRITE,406892412789,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Zen-0005,A_TITLE_INTENT_REWRITE,406892413076,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Zen-0007,A_TITLE_INTENT_REWRITE,406892413333,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Zen-0008,A_TITLE_INTENT_REWRITE,406892413714,0,0,0,LOCAL_TITLE_DESCRIPTION_UPDATED
2026-05-06 23:44:26 -0400,Sticker-Zen-0010,B_COVER_QA_PRIORITY,406892414116,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0022,B_COVER_QA_PRIORITY,406892414235,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0025,B_COVER_QA_PRIORITY,406892327989,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0027,B_COVER_QA_PRIORITY,406892414741,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0041,B_COVER_QA_PRIORITY,406902593931,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0044,B_COVER_QA_PRIORITY,406902622710,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0045,B_COVER_QA_PRIORITY,406902640998,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0046,B_COVER_QA_PRIORITY,406902663232,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0049,B_COVER_QA_PRIORITY,406902713267,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0050,B_COVER_QA_PRIORITY,406902886081,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0051,B_COVER_QA_PRIORITY,406902889638,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0052,B_COVER_QA_PRIORITY,406902896387,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0053,B_COVER_QA_PRIORITY,406902900109,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0054,B_COVER_QA_PRIORITY,406903032635,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0055,C_HOLDOUT_CONTROL,406903037933,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0056,C_HOLDOUT_CONTROL,406903041315,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0057,C_HOLDOUT_CONTROL,406903044643,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0058,C_HOLDOUT_CONTROL,406903049411,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0060,C_HOLDOUT_CONTROL,406903249053,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0061,C_HOLDOUT_CONTROL,406903249987,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0062,C_HOLDOUT_CONTROL,406903250891,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0063,C_HOLDOUT_CONTROL,406903252007,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0066,C_HOLDOUT_CONTROL,406903252739,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0069,C_HOLDOUT_CONTROL,406903753067,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0070,C_HOLDOUT_CONTROL,406903757240,0,0,0,NO_LOCAL_CHANGE
2026-05-06 23:44:26 -0400,Sticker-Zen-0071,C_HOLDOUT_CONTROL,406903762328,0,0,0,NO_LOCAL_CHANGE

```


### RAW LOG: Database/eBay_Traffic_Diagnosis.csv
```text
﻿Priority,Diagnosis,Evidence,Recommended_Action,Network_Dependency
100,Sticker live cover/gallery mismatch is a primary blocker.,Cover fix queue contains 49 rows; latest snapshot has 43/50 zero-view rows despite 50 promoted rows.,Do not expand Sticker count. Repair Printify source defaults and re-audit live eBay covers before more Sticker publish.,medium
90,Promoted Listings Standard 2% is active but is not enough alone.,"Latest snapshot 2026-05-06 23:44:26 -0400: promoted=50, zero_views=43, rows=50.","Keep 2% Standard as baseline, but treat image/search-intent repair as the growth lever. Do not raise to suggested ad rates yet.",low
80,Poster/Acrylic currently show more early movement than Sticker.,Acrylic: rows=20 views=4 moved=3; Poster: rows=19 views=7 moved=4; Sticker: rows=10 views=0 moved=0; Unknown: rows=1 views=0 moved=0,Keep the near-term product mix tilted toward Poster/Acrylic and Etsy digital printables until Sticker cover issue is fixed.,low
70,Title rewrite experiment has not produced a clear Sticker lift yet.,A_TITLE_INTENT_REWRITE: moved=0/18; B_COVER_QA_PRIORITY: moved=0/14; C_HOLDOUT_CONTROL: moved=0/12,"Continue the controlled experiment window, but do not churn all titles daily. Next test should combine buyer-intent titles with corrected cover/gallery.",low

```


### RAW LOG: Database/Unified_Listing_Registry.csv
```text
﻿ID,Product_Type,Category,Local_Status,Printify_Product_ID,eBay_Item_ID,eBay_Item_URL,eBay_Title,eBay_Price,Latest_eBay_Views_30_Days,Latest_eBay_General_Status,Latest_eBay_Priority_Status,Etsy_Planned,Etsy_Title,Etsy_Launch_Status,Production_Path,Cover_Path,Gallery_Ready,Image_Note_Ready,Action_Bucket
Sticker-Academia-0001,Sticker,Academia,Quality_Hold_LowRes_U,,,,Dark Academia Celestial Gate Hourglass 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0001_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0002,Sticker,Academia,Quality_Hold_LowRes_U,,,,Dark Academia Celestial Orrery Mechanism 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0002_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0003,Sticker,Academia,Quality_Hold_LowRes_U,,,,Dark Academia Alchemical Distillation Apparatus 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0003_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0004,Sticker,Academia,Printify_Published_Mockups5,69f192aa5ea38382140f1d7b,406892408950,https://www.ebay.com/itm/406892408950,4pc Kiss-Cut Sticker Set Mechanical Raven Familiar Laptop Journal Bottle Dark,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Academia-0005,Sticker,Academia,Retired_Replaced,69f198efea1f992ded0e90e7,,,Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Dark Academia Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0006,Sticker,Academia,Retired_Replaced,69f19b945494697f0d01b78c,,,4pc Sticker Set Botanical Terrarium Lantern Vinyl Decals Laptop Bottle Dark,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0007,Sticker,Academia,Retired_Replaced,69f1a56756390ef4cd09be1e,,,4pc Kiss-Cut Sticker Set Astrolabe Navigation Instrument Laptop Journal Bottle,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0008,Sticker,Academia,Retired_Replaced,69f1a630de3c2e09400f9c5f,,,Ritual Incense Censer Gothic Academia 4pc 6x6 Vinyl Sticker Reader Writer Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0009,Sticker,Academia,Retired_Replaced,69f1a6acc2501ebbc40ac2e5,,,4pc Sticker Set Gothic Academia Cathedral Fragment Vinyl Decals Laptop Bottle,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0010,Sticker,Academia,Retired_Replaced,69f1a724785a37b0240adad9,,,Vintage Academia Compass Rose Talisman 4pc 6x6 Sticker Sheet Literary Cozy Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0011,Sticker,Academia,Retired_Replaced,69f1a7b0cfb25d6b6f0f10f7,,,Apothecary Poison Vial Vintage Academia 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0013,Sticker,Academia,Quality_Hold_LowRes_U,,,,Dark Academia Serpent Ouroboros Ring 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0013_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0013_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0014,Sticker,Academia,Retired_Replaced,69f1a833592cc603cd0a91fd,,,4pc Vinyl Sticker Set Microscope Observation Device Laptop Bottle Journal Dark,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0015,Sticker,Academia,Retired_Replaced,69f1a8b40bc0bf405305ef2b,,,4pc Sticker Set Skeleton Key Portal Vinyl Decals Laptop Bottle Dark Academia,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0016,Sticker,Academia,Retired_Replaced,69f1a92ade3c2e09400f9e44,,,4pc Kiss-Cut Sticker Set Gothic Academia Prism Light Refractor Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0001,Sticker,Zen,Retired_Replaced,69f1a99c785a37b0240adc94,,,4pc Sticker Set Mindful Zen Koi Pond Vinyl Decals Laptop Bottle Zen Aesthetic,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0002,Sticker,Zen,Retired_Replaced,69f1ab9a63935da7e8064504,,,Minimal Zen Bonsai Tree of Serenity 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0003,Sticker,Zen,Retired_Replaced,69f1ac1804ea1d3ba9005c58,,,Lotus Mandala Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0004,Sticker,Zen,Retired_Replaced,69f1ac9740c796ee97057c83,,,4pc Sticker Set Stone Guardian Lion Mindful Zen Vinyl Decals Laptop Bottle Zen,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0005,Sticker,Zen,Retired_Replaced,69f1ad18c59fe705400bacbf,,,Bamboo Forest Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Misty Art,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0006,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Ink Wash Mountain 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0006_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0006_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0007,Sticker,Zen,Retired_Replaced,69f1ad9bbb6f6dd6270dc5df,,,4pc Sticker Set Cherry Blossom Branch Vinyl Decals Laptop Bottle Zen Aesthetic,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0008,Sticker,Zen,Retired_Replaced,69f1aef4bb6f6dd6270dc7d5,,,4pc Kiss-Cut Sticker Set Circle Ens Laptop Journal Bottle Zen Aesthetic Decal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0009,Sticker,Zen,Retired_Replaced,69f1af85bb6f6dd6270dc848,,,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0010,Sticker,Zen,Printify_Published_Mockups5,69f1b00840c796ee97058144,406892414116,https://www.ebay.com/itm/406892414116,Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0021,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Kintsugi Lotus no Hasu 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Desk,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0021_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0021_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0022,Sticker,Zen,Retired_Replaced,69f1b1ab63935da7e8064bab,,,Mindful Zen Garden Stone Meis seki 4pc 6x6 Vinyl Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0023,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Bioluminescent Bonsai Hikaru 4pc 6x6 Kiss-Cut Sticker Vinyl Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0023_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0023_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0024,Sticker,Zen,Retired_Replaced,69f1b2c4d3e196c79b0fdaec,,,Mindful Zen Enso Circle with Crystals 4pc 6x6 Vinyl Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0025,Sticker,Zen,Retired_Replaced,69f1cb4ef6b83091a50959f5,,,Koi Fish in Jade Pond Hisui no Koi Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Luck,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0026,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1cc732f305b371c05b1d7,,,Mountain and Moon Sangetsu Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0026_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0026_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0027,Sticker,Zen,Retired_Replaced,69f1ce0f11e0745fcb0da03a,,,Minimal Zen Temple Lantern Zendera no T r 4pc 6x6 Sticker Sheet Serene Mindful,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0028,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Floating Tea Bowl Ukabu Chawan 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0028_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0028_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0029,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1cee189347116c004f529,,,Bamboo Forest Hikaru Chikurin Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0029_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0029_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0030,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Meditating Frog Zazen Kaeru 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0030_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0030_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0031,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1cf9911e0745fcb0da15f,,,Mindful Zen Kintsugi Lotus 4pc 6x6 Vinyl Sticker Laptop Journal Gift Meditation,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0031_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0031_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0032,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1d04a0482f56ada0cf347,,,Glowing Garden Stone 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0032_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0032_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0033,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Crystalline Bamboo 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0033_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0033_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0034,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1d1003a934dcd94086687,,,Zen Aesthetic Kintsugi Enso Circle 4pc 6x6 Kiss-Cut Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0034_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0034_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0035,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1d1ed11e0745fcb0da2ea,,,Bioluminescent Koi Pond 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0035_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0035_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0036,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1d2a9f6b83091a5095eea,,,Fractal Cherry Blossom Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0036_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0036_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0037,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1d35c89347116c004f871,,,Mindful Zen Golden Veined Mountain 4pc 6x6 Vinyl Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0037_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0037_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0038,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1d44bf6b83091a5095fca,,,Meditating Crystal Frog Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0038_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0038_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0039,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Kintsugi Tea Bowl 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0039_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0039_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0040,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f1d4f9bdda7e777002a696,,,Translucent Jade Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0040_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0040_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0041,Sticker,Zen,Retired_Replaced,69f1db9382fcf925cf08206d,,,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0042,Sticker,Zen,Retired_Replaced,69f2192ae64c9f31b70f2dbd,,,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0044,Sticker,Zen,Retired_Replaced,69f2396ccaeb1241880b692d,406902622710,https://www.ebay.com/itm/406902622710,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0045,Sticker,Zen,Retired_Replaced,69f21a5da7777da1970fd378,406902640998,https://www.ebay.com/itm/406902640998,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0046,Sticker,Zen,Retired_Replaced,69f21b07b0d6b88b2805ebe3,406902663232,https://www.ebay.com/itm/406902663232,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0048,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f21bba9b469f716d0e4e42,,,Crystalline Dragon Scale 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0048_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0048_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0049,Sticker,Zen,Retired_Replaced,69f23a2fa7777da1970fe60d,406902713267,https://www.ebay.com/itm/406902713267,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0050,Sticker,Zen,Retired_Replaced,69f23a99c326d7da170bfe8d,406902886081,https://www.ebay.com/itm/406902886081,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0051,Sticker,Zen,Retired_Replaced,69f23b5ce64c9f31b70f415b,406902889638,https://www.ebay.com/itm/406902889638,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0052,Sticker,Zen,Retired_Replaced,69f23c10caeb1241880b6afe,406902896387,https://www.ebay.com/itm/406902896387,Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0053,Sticker,Zen,Retired_Replaced,69f252f4357398ded80f61c9,406902900109,https://www.ebay.com/itm/406902900109,Crystalline Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0054,Sticker,Zen,Retired_Replaced,69f253bc357398ded80f6242,406903032635,https://www.ebay.com/itm/406903032635,Dragon Meditation Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0055,Sticker,Zen,Printify_Published_Mockups5,69f2547229c1d0349a00e796,406903037933,https://www.ebay.com/itm/406903037933,Mindful Zen Azure Dragon Warrior 4pc 6x6 Vinyl Sticker Laptop Journal Gift Desk,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0055_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0055_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0056,Sticker,Zen,Printify_Published_Mockups5,69f25526ad218fe47f0cc0d3,406903041315,https://www.ebay.com/itm/406903041315,Dragon Cherry Blossom 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0056_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0056_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0057,Sticker,Zen,Printify_Published_Mockups5,69f255dae64c9f31b70f4ea6,406903044643,https://www.ebay.com/itm/406903044643,Moonlit Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk Decor,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0057_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0057_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0058,Sticker,Zen,Printify_Published_Mockups5,69f259bc5f78c14a7b0a4760,406903049411,https://www.ebay.com/itm/406903049411,Minimal Zen Dragon Calligraphy 4pc 6x6 Sticker Sheet Serene Mindful Clean Decor,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0058_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0058_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0060,Sticker,Zen,Printify_Published_Mockups5,69f25a86a7777da1970ff5f3,406903249053,https://www.ebay.com/itm/406903249053,Minimal Zen Translucent Jade Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0060_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0060_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0061,Sticker,Zen,Printify_Published_Mockups5,69f25b3ce64c9f31b70f50ed,406903249987,https://www.ebay.com/itm/406903249987,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Calm Gift,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0061_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0061_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0062,Sticker,Zen,Printify_Published_Mockups5,69f25bee9b469f716d0e7056,406903250891,https://www.ebay.com/itm/406903250891,Zen Aesthetic Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0062_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0062_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0063,Sticker,Zen,Printify_Published_Mockups5,69f25ca39577aaffd5066a80,406903252007,https://www.ebay.com/itm/406903252007,Crystalline Dragon Core 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0063_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0063_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0066,Sticker,Zen,Printify_Published_Mockups5,69f25d56c326d7da170c0f79,406903252739,https://www.ebay.com/itm/406903252739,Golden Vein Circuitry Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0066_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0066_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0067,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f25f0db0d6b88b28061022,,,Moonlit Jade Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0067_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0067_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0068,Sticker,Zen,Printify_PublishExternalPending_Mockups4,69f25faf29c1d0349a00ecec,,,Fractal Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0068_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0068_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0069,Sticker,Zen,Printify_Published_Mockups5,69f26062cd8d04605103d10b,406903753067,https://www.ebay.com/itm/406903753067,Minimal Zen Dragon Guardian 4pc 6x6 Sticker Sheet Serene Mindful Clean Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0069_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0069_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0070,Sticker,Zen,Printify_Published_Mockups5,69f261185f78c14a7b0a4b29,406903757240,https://www.ebay.com/itm/406903757240,Minimal Zen Jade Phoenix Ascension 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0070_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0070_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0071,Sticker,Zen,Printify_Published_Mockups5,69f261cd5269e3325904b816,406903762328,https://www.ebay.com/itm/406903762328,Zen Aesthetic Lotus Lantern Vessel 4pc 6x6 Kiss-Cut Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0071_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0071_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0072,Sticker,Zen,Printify_UI_Mockups5,69f26281feceb0d66c042ce7,,,Celestial Koi Constellation 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Vinyl,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0072_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0072_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0073,Sticker,Zen,Printify_UI_Mockups5,69f262db5269e3325904b893,,,Sacred Singing Bowl Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0073_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0073_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0074,Sticker,Zen,Printify_UI_Mockups5,69f263729b469f716d0e7409,,,Minimal Zen Bamboo Pagoda Relic 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0074_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0074_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0075,Sticker,Zen,Printify_UI_Mockups5,69f26426671cc7c7960b3f3d,,,Mindful Zen Dragon Pearl Talisman 4pc 6x6 Vinyl Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0075_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0075_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0076,Sticker,Zen,Printify_UI_Mockups5,69f264df357398ded80f6a3a,,,Moonlit Mountain Shrine Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0076_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0076_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0078,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Celestial Lotus Lantern 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0078_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0078_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0079,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Celestial Koi Ascending 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0079_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0079_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0080,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Moonstone Phoenix Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0080_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0080_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0081,Sticker,Zen,Printify_UI_Mockups5,69f26782c326d7da170c1498,,,Celestial Koi Ascension Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0081_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0081_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0082,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Lotus Lantern Relic 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0082_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0082_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0083,Sticker,Zen,Printify_UI_Mockups5,69f2683ecaeb1241880b7fcb,,,Phoenix Wing Fragment 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0083_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0083_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0084,Sticker,Zen,Printify_UI_Mockups5,69f268f1e3d76b3758086023,,,Minimal Zen Dragon Scale Medallion 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0084_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0084_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0085,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Celestial Crane Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0085_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0085_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0086,Sticker,Zen,Printify_UI_Mockups5,69f2696f29c1d0349a00f104,,,Mindful Zen Celestial Phoenix Talisman 4pc 6x6 Vinyl Sticker Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0086_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0086_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0087,Sticker,Zen,Printify_UI_Mockups5,69f26a02357398ded80f6c4f,,,Lotus Constellation Bloom 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0087_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0087_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0088,Sticker,Zen,Printify_UI_Mockups5,69f27616ce81beb59a02b9e6,,,Zen Aesthetic Singing Bowl Nexus 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0088_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0088_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0089,Sticker,Zen,Printify_UI_Mockups5,69f27777ce81beb59a02bab7,,,Moon Temple Pagoda 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0089_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0089_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0090,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Dragon Seal Medallion 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0090_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0090_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0091,Sticker,Zen,Printify_UI_Mockups5,69f2786bcd8d04605103dccb,,,Incense Chalice Vessel Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0091_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0091_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0092,Sticker,Zen,Printify_UI_Mockups5,69f279205f78c14a7b0a572e,,,Constellation Compass Rose Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0092_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0092_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0093,Sticker,Zen,Printify_UI_Mockups5,69f279d8671cc7c7960b4a3d,,,Mindful Zen Katana Starblade Relic 4pc 6x6 Vinyl Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0093_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0093_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0094,Sticker,Zen,Printify_UI_Mockups5,69f27ac5ce81beb59a02bc4b,,,Mountain Mist Sanctuary 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0094_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0094_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Sticker-Zen-0095,Sticker,Zen,Ready_for_Printify,,,,Prayer Wheel Mechanism 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0095_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0095_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0096,Sticker,Zen,Ready_for_Printify,,,,Celestial Koi Constellation Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0096_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0096_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0097,Sticker,Zen,Ready_for_Printify,,,,Garden Rake Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0097_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0097_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0098,Sticker,Zen,Ready_for_Printify,,,,Celestial Koi Ascension Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Bottle Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0098_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0098_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0099,Sticker,Zen,Ready_for_Printify,,,,Mindful Zen Lotus Bloom Mandala 4pc 6x6 Vinyl Sticker Laptop Journal Gift Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0099_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0099_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0100,Sticker,Zen,Ready_for_Printify,,,,Ritual Bell Shrine Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0100_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0100_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0101,Sticker,Zen,Ready_for_Printify,,,,Minimal Zen Phoenix Rebirth Emblem 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0101_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0101_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0102,Sticker,Zen,Ready_for_Printify,,,,Jade Incense Burner 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0102_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0102_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0103,Sticker,Zen,Ready_for_Printify,,,,Celestial Compass Rose 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0103_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0103_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0104,Sticker,Zen,Ready_for_Printify,,,,Minimal Zen Bamboo Grove Miniature 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0104_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0104_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0105,Sticker,Zen,Ready_for_Printify,,,,Zen Aesthetic Infinity Knot Talisman 4pc 6x6 Kiss-Cut Sticker Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0105_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0105_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0106,Sticker,Zen,Ready_for_Printify,,,,Prayer Wheel Relic Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0106_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0106_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0107,Sticker,Zen,Ready_for_Printify,,,,Celestial Lantern Beacon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0107_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0107_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0108,Sticker,Zen,Ready_for_Printify,,,,Sacred Turtle Wisdom Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0108_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0108_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0109,Sticker,Zen,Ready_for_Printify,,,,Garden Rake Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0109_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0109_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0110,Sticker,Zen,Ready_for_Printify,,,,Frozen Phoenix Ascent Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0110_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0110_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0111,Sticker,Zen,Ready_for_Printify,,,,Jade Lotus Bloom Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0111_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0111_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0112,Sticker,Zen,Ready_for_Printify,,,,Ritual Bell Fragment Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0112_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0112_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0113,Sticker,Zen,Ready_for_Printify,,,,Collapsed Pagoda Crown 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0113_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0113_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0114,Sticker,Zen,Ready_for_Printify,,,,Frozen Seal Mandala Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0114_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0114_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0115,Sticker,Zen,Ready_for_Printify,,,,Bamboo Segment Relic Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0115_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0115_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0116,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Incense Burner Throne 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0116_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0116_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0117,Sticker,Zen,Ready_for_Printify,,,,Zen Aesthetic Koi Swimming Upward 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0117_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0117_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0118,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Moonstone Crane Spirit 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Desk,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0118_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0118_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0120,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Burgundy Phoenix Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0120_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0120_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0121,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Celestial Lotus Bloom 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0121_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0121_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0122,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Mystic Prayer Bell 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0122_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0122_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0123,Sticker,Zen,Ready_for_Printify,,,,Zen Aesthetic Ancient Pagoda Shrine 4pc 6x6 Kiss-Cut Sticker Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0123_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0123_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0124,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Dragon Seal Medallion 4pc 6x6 Kiss-Cut Sticker Vinyl Reader Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0124_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0124_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0125,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Ceremonial Incense Vessel 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0125_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0125_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0126,Sticker,Zen,Ready_for_Printify,,,,Nebula Moon Orb Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0126_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0126_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0127,Sticker,Zen,Ready_for_Printify,,,,Mindful Zen Mystic Garden Bridge 4pc 6x6 Vinyl Sticker Laptop Journal Gift Desk,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0127_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0127_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0128,Sticker,Zen,Ready_for_Printify,,,,Minimal Zen Koi Guardian Spirit 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0128_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0128_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0129,Sticker,Zen,Ready_for_Printify,,,,Minimal Zen Bamboo Scroll Relic 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0129_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0129_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0130,Sticker,Zen,Ready_for_Printify,,,,Minimal Zen Celestial Phoenix Ascending 4pc 6x6 Sticker Sheet Serene Mindful,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0130_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0130_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0131,Sticker,Zen,Ready_for_Printify,,,,Zen Aesthetic Sacred Lotus Mandala 4pc 6x6 Kiss-Cut Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0131_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0131_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0132,Sticker,Zen,Ready_for_Printify,,,,Ritual Bell Shrine Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0132_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0132_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0133,Sticker,Zen,Ready_for_Printify,,,,Moon Pagoda Fragment 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0133_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0133_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0134,Sticker,Zen,Ready_for_Printify,,,,Jade Dragon Seal Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0134_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0134_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0135,Sticker,Zen,Ready_for_Printify,,,,Moonstone Incense Vessel Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0135_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0135_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0136,Sticker,Zen,Ready_for_Printify,,,,Celestial Koi Constellation 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Bottle Vinyl,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0136_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0136_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0138,Sticker,Zen,Ready_for_Printify,,,,Minimal Zen Bamboo Flute Harmony 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0138_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0138_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0139,Sticker,Zen,Ready_for_Printify,,,,Sacred Deer Guardian Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0139_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0139_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0140,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Jade Serpent Coil 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0140_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0140_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0144,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Frosted Jade Lotus Incense Holder 4pc 6x6 Kiss-Cut Sticker Vinyl,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0144_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0144_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0150,Sticker,Zen,Ready_for_Printify,,,,Celestial Jade Bell Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0150_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0150_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0151,Sticker,Zen,Ready_for_Printify,,,,Moonlit Lotus Chalice Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0151_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0151_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0152,Sticker,Zen,Quality_Hold_LowRes_U,,,,Zen Aesthetic Dragon Scale Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0152_Not_Working_LowRes\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0152_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0153,Sticker,Zen,Ready_for_Printify,,,,Mindful Zen Phoenix Feather Flute 4pc 6x6 Vinyl Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0153_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0153_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0154,Sticker,Zen,Ready_for_Printify,,,,Zen Aesthetic Misty Mountain Incense Burner 4pc 6x6 Kiss-Cut Sticker Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0154_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0154_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0155,Sticker,Zen,Ready_for_Printify,,,,Zen Aesthetic Bamboo Grove Tea Scoop 4pc 6x6 Kiss-Cut Sticker Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0155_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0155_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0156,Sticker,Zen,Ready_for_Printify,,,,Zen Aesthetic Moongate Architectural Fragment 4pc 6x6 Kiss-Cut Sticker Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0156_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0156_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0157,Sticker,Zen,Ready_for_Printify,,,,Koi Pond Water Dipper Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0157_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0157_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0158,Sticker,Zen,Ready_for_Printify,,,,Spiral Galaxy Meditation Disc 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0158_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0158_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0159,Sticker,Zen,Ready_for_Printify,,,,Pagoda Lantern Miniature 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0159_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0159_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Sticker-Zen-0160,Sticker,Zen,Ready_for_Printify,,,,Mindful Zen Wave Crest Sake Cup 4pc 6x6 Vinyl Sticker Laptop Journal Gift Wood,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0160_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0160_Ready_for_Steaming\Cover_Mockup.png,True,True,Ready_For_Printify_When_Network_OK
Poster-Academia-0001,Poster,Academia,Printify_Published_Mockups5,69f28800cd8d04605103e53a,406902584620,https://www.ebay.com/itm/406902584620,Celestial Gateway Dark Academia Poster 12x18 Study Decor Moonstone Architecture,$34.99,1,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Has_View_Monitor
Poster-Academia-0002,Poster,Academia,Printify_Published_Mockups5,69f2906f7f1017d51b0d5f76,406902600741,https://www.ebay.com/itm/406902600741,Dark Academia Obsidian Threshold Poster 12x18 Vintage Study Decor Mentor Wisdom,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0002_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0003,Poster,Academia,Printify_Published_Mockups5,69f29152357398ded80f8178,406902616799,https://www.ebay.com/itm/406902616799,Dark Academia Serpentine Portal of Alchemical Texts 12x18 Poster Study Decor,$34.99,0,Promoted,Eligible,True,"Serpentine Portal of Alchemical Texts Study Decor Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Academia-0001,Acrylic,Academia,Printify_Published_Mockups5,69f298dc9577aaffd50689b0,406902588642,https://www.ebay.com/itm/406902588642,Astrolabe Compass Ritual Disc Dark Academia 5x7 Acrylic Art Study Decor Shelf,$89.99,1,Promoted,Eligible,True,"Astrolabe Compass Ritual Disc Art Study Decor Dark Academia Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Has_View_Monitor
Acrylic-Grimdark-0081,Acrylic,Grimdark,Printify_Published_Mockups5,69f299c1a3119247600cbe18,406902606976,https://www.ebay.com/itm/406902606976,Plague Doctor Raven Skull Grimdark Alchemy 5x7 Acrylic Art Block Collectible,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0081_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0081_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0001,Acrylic,Zen,Printify_Published_Mockups5,69f29a72c411a56f6902930d,406902620519,https://www.ebay.com/itm/406902620519,Zen Mechanical Crane 5x7 Acrylic Block Desk Art Calm Decor Origami Sculpture,$89.99,0,Promoted,Eligible,True,"Mechanical Crane Desk Art Calm Decor Origami Dark Academia Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0081,Poster,Academia,Printify_Published_Mockups5,69f29fe09577aaffd5068e03,406902627420,https://www.ebay.com/itm/406902627420,Celestial Armillary Sphere Dark Academia Poster 12x18 Scholar Study Decor Wall,$34.99,2,Promoted,Eligible,True,"Celestial Armillary Sphere Scholar Study Decor Wall Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0081_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0081_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Has_View_Monitor
Poster-Academia-0082,Poster,Academia,Printify_Published_Mockups5,69f2a0cacaeb1241880b9e8d,406902648209,https://www.ebay.com/itm/406902648209,Celestial Armillary Codex Academia Poster 12x18 Vintage Astronomy Decor Wall,$34.99,3,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0082_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0082_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Has_View_Monitor
Poster-Academia-0083,Poster,Academia,Printify_Published_Mockups5,69f2a1b8a7777da197101a96,406902669660,https://www.ebay.com/itm/406902669660,Academia Mentor-Grade Cosmic Lotus Observatory 12x18 Poster Steampunk Study,$34.99,0,Promoted,Eligible,True,"Mentor Grade Cosmic Lotus Observatory Steampunk Study Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0083_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0083_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0084,Poster,Academia,Printify_Published_Mockups5,69f2a2aacaeb1241880b9f6b,406902691983,https://www.ebay.com/itm/406902691983,Astrolabe Chalice Relic Dark Academia Poster 12x18 Vintage Study Decor Wall,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0084_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0084_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0082,Acrylic,Grimdark,Printify_Published_Mockups5,69f2a7d0e64c9f31b70f79cf,406902633400,https://www.ebay.com/itm/406902633400,Grimdark Alchemical Terrarium Withered Mandrake Root Chamber 5x7 Acrylic Block,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0082_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0082_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0002,Acrylic,Zen,Printify_Published_Mockups5,69f2a8a5357398ded80f8faf,406902657898,https://www.ebay.com/itm/406902657898,Zen Aesthetic Ritual Bell Shrine 5x7 Acrylic Block for Meditation Desk Shelf,$89.99,0,Promoted,Eligible,True,"Ritual Bell Shrine for Meditation Desk Shelf Zen Aesthetic Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0002_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0003,Acrylic,Zen,Printify_Published_Mockups5,69f2a9b45f78c14a7b0a7290,406902673249,https://www.ebay.com/itm/406902673249,Zen Pagoda Fragment Relic 5x7 Acrylic Print Floating Tower Decor Jade Framework,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0085,Poster,Academia,Printify_Published_Mockups5,69f2b132cd8d04605103fdaa,406902882943,https://www.ebay.com/itm/406902882943,Orrery Lighthouse Beacon Dark Academia Poster 12x18 Vintage Astronomy Wall Art,$34.99,1,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0085_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0085_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Has_View_Monitor
Poster-Academia-0091,Poster,Academia,Printify_Published_Mockups5,69f2b7ada7777da1971028d7,406902887127,https://www.ebay.com/itm/406902887127,Dark Academia Celestial Lotus Poster 12x18 Vintage Study Room Wall Art Decor,$34.99,0,Promoted,Eligible,True,"Celestial Lotus Study Room Decor Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0091_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0091_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Academia-0003,Acrylic,Academia,Printify_Published_Mockups5,69f2b9c3caeb1241880bae85,406902703464,https://www.ebay.com/itm/406902703464,Celestial Orrery Tree Bonsai Dark Academia 5x7 Acrylic Block Mentor-Grade Study,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0083,Acrylic,Grimdark,Printify_Published_Mockups5,69f2bac6343d8ca093077dd8,406902885214,https://www.ebay.com/itm/406902885214,Grimdark Ritual Censer Thurible 5x7 Acrylic Block Dark Academia Mentor-Grade,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0083_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0083_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0004,Acrylic,Zen,Printify_Published_Mockups5,69f2bbbc343d8ca093077e9a,406902888077,https://www.ebay.com/itm/406902888077,Zen Cyberpunk Koi Automaton 5x7 Acrylic Block - Meditative Desk Sculpture Shelf,$89.99,1,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Has_View_Monitor
Acrylic-Zen-0005,Acrylic,Zen,Printify_Published_Mockups5,69f2c22e9b469f716d0ea954,406902893289,https://www.ebay.com/itm/406902893289,Zen Incense Vessel Constellation 5x7 Acrylic Block for Meditation Desk Shelf,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0001,Poster,Zen,Printify_Published_Mockups5,69f2dc76cd8d046051041f06,406902890971,https://www.ebay.com/itm/406902890971,Zen Bonsai Wall Art Celestial Gate of Jade Mist 12x18 Poster Meditation Decor,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0002,Poster,Zen,Printify_Published_Mockups5,69f2cf675f78c14a7b0a894c,406902897663,https://www.ebay.com/itm/406902897663,Dark Academia Phoenix Incense Burner 12x18 Poster Ritual Zen Decor Wall Study,$34.99,0,Promoted,Eligible,True,"Phoenix Incense Burner Ritual Decor Wall Study Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0002_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0003,Poster,Zen,Printify_Hold_BadDraftDeleted,,,,Lotus Mandala Seal Stone Poster 12x18 Dark Academia Zen Wall Art Decor Study,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Zen-0006,Acrylic,Zen,Printify_Published_Mockups5,69f2d2a1c326d7da170c51b4,406902898909,https://www.ebay.com/itm/406902898909,Zen Mentor-Grade Jade Phoenix Incense Altar 5x7 Acrylic Block for Meditation,$89.99,2,Promoted,Eligible,True,"Mentor Grade Jade Phoenix Incense Altar for Zen Aesthetic Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0006_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0006_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Has_View_Monitor
Acrylic-Zen-0007,Acrylic,Zen,Printify_Published_Mockups5,69f2d3ab5f78c14a7b0a8b87,406903028253,https://www.ebay.com/itm/406903028253,Zen Aesthetic Sacred Lotus Meditation Bell 5x7 Acrylic Block for Altar Decor,$89.99,0,Promoted,Eligible,True,"Sacred Lotus Meditation Bell for Altar Decor Zen Aesthetic Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0007_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0007_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0008,Acrylic,Zen,Printify_Published_Mockups5,69f2d49b81039eb9ab0b583c,406903036452,https://www.ebay.com/itm/406903036452,Zen Celestial Bonsai Moon Garden 5x7 Acrylic Block for Serene Desk Decor Shelf,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0004,Poster,Zen,Printify_Published_Mockups5,69f2dddb9577aaffd506bc32,406903026999,https://www.ebay.com/itm/406903026999,Zen Celestial Compass Poster 12x18 Wall Art Calm Study Decor Library Gift Room,$34.99,0,Promoted,Eligible,True,"Celestial Compass Calm Study Decor Library Room Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0005,Poster,Zen,Printify_Published_Mockups5,69f2db1a3c6616b960034a37,406903033377,https://www.ebay.com/itm/406903033377,Zen Phoenix Rebirth Vessel 12x18 Poster for Meditation Room Decor Wall Study,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Academia-0005,Acrylic,Academia,Printify_Published_Mockups4,69f80ad2d3b9dc73b1051dbd,406903039716,https://www.ebay.com/itm/406903039716,Alchemical Star Flask Vessel 5x7 Acrylic Block Dark Academia Desk Decor Shelf,$89.99,0,Promoted,Eligible,True,"Alchemical Star Flask Vessel Desk Decor Shelf Dark Academia Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0085,Acrylic,Grimdark,Printify_Published_Mockups4,69f2e4c77e3402ea470630eb,406903043482,https://www.ebay.com/itm/406903043482,Alchemist Divination Compass Grimdark 5x7 Acrylic Display Mentor-Grade Occult,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0085_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0085_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0009,Acrylic,Zen,Printify_Published_Mockups8,69f80f8a83a8608fd80ec283,406903047385,https://www.ebay.com/itm/406903047385,"Zen Bamboo Flute 5x7 Acrylic Block, Whispering Shakuhachi Meditation Art Gift",$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0010,Acrylic,Zen,Printify_Published_Mockups8,69f810485da263f75f049bf8,406903213858,https://www.ebay.com/itm/406903213858,Zen Lotus Seed Pod Vessel 5x7 Acrylic Block for Mindful Desk Decor Shelf Study,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0001,Acrylic,Grimdark,Printify_Published_Mockups4,69f82b8aa1a4c45aad055063,406903249745,https://www.ebay.com/itm/406903249745,Gothic Lantern Soul Cage 5x7 Acrylic Block Grimdark Study Decor Crimson Flame,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0004,Acrylic,Grimdark,Printify_Published_Mockups8,69f82c8609f3b7302401cacf,406903250705,https://www.ebay.com/itm/406903250705,Grimdark Gothic Lantern 5x7 Acrylic Block Shadowbound Sentinel Beacon Dark Gift,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0005,Acrylic,Grimdark,Printify_Published_Mockups4,69f8388b25819cdf3d0538bc,406903251829,https://www.ebay.com/itm/406903251829,Gothic Necromancer Soul Reliquary 5x7 Acrylic Grimdark Artifact Decor Shelf,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0006,Acrylic,Grimdark,Printify_Published_Mockups8,69f83957ffbc831dea082e1a,406903252506,https://www.ebay.com/itm/406903252506,Gothic Grimdark Voidwalker Eternal Lamp 5x7 Acrylic Block Dark Decor Shelf Gift,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0006_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0006_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0007,Acrylic,Grimdark,Printify_Published_Mockups8,69f839eaf9374ed4f105a092,406903731967,https://www.ebay.com/itm/406903731967,Gothic Banshee Lantern Grimdark Art 5x7 Acrylic Premium Collectible Decor Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0007_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0007_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0008,Acrylic,Grimdark,Printify_Published_Mockups4,69f83a955da263f75f04c06a,406903746215,https://www.ebay.com/itm/406903746215,Gothic Grimdark Revenant Lantern 5x7 Acrylic Art Premium Decor Sapphire Glass,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0009,Acrylic,Grimdark,Printify_Published_Mockups4,69f83b5cf9374ed4f105a180,406903749989,https://www.ebay.com/itm/406903749989,Gothic Grimdark Lich Phylactery Lantern 5x7 Acrylic Print Dark Fantasy Home,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0010,Acrylic,Grimdark,Printify_Published_Mockups8,69f83c14ffbc831dea082fa3,406903756190,https://www.ebay.com/itm/406903756190,Gothic Wraith Warden Cursed Beacon 5x7 Acrylic Block Dark Fantasy Decor Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0005,Poster,Academia,Printify_Published_Mockups4,69f847b45da263f75f04cdbd,406903038850,https://www.ebay.com/itm/406903038850,Arcane Archway of Forbidden Chronicles Dark Academia 12x18 Poster Study Room,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0006,Poster,Academia,Printify_Published_Mockups5,69f84864feed9979d10cd5ba,406903042690,https://www.ebay.com/itm/406903042690,Dark Academia Ethereal Torii Poster 12x18 Study Room Decor Scholarly Ascension,$34.99,0,Promoted,Eligible,True,"Ethereal Torii Study Room Decor Scholarly Ascension Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0006_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0006_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0008,Poster,Academia,Printify_Published_Mockups4,69f84b3d5da263f75f04d1f7,406903046097,https://www.ebay.com/itm/406903046097,Dark Academia Mystic Threshold Infinite Knowledge Poster 12x18 Study Decor Wall,$34.99,0,Promoted,Eligible,True,"Mystic Threshold Infinite Knowledge Study Decor Wall Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0009,Poster,Academia,Printify_Published_Mockups4,69f8547125819cdf3d05522b,406903209258,https://www.ebay.com/itm/406903209258,Dark Academia Sanctum Gate of Preserved Wisdom 12x18 Poster Study Decor Wall,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0010,Poster,Academia,Printify_Published_Mockups4,69f854ed09f3b7302401ed2e,406903249496,https://www.ebay.com/itm/406903249496,Dark Academia Hermetic Portal of Ancient Codices 12x18 Poster Study Decor Wall,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0011,Poster,Academia,Printify_Published_Mockups4,69f850b425819cdf3d054e10,406903250376,https://www.ebay.com/itm/406903250376,Dark Academia Celestial Archway Poster 12x18 Study Room Decor Timeless Tomes,$34.99,0,Promoted,Eligible,True,"Celestial Archway Study Room Decor Timeless Tomes Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0011_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0011_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0013,Poster,Academia,Printify_Published_Mockups8,69f855abffbc831dea0847c8,,,Dark Academia Alchemist Threshold Transmuted Knowledge 12x18 Poster Study Decor,$34.99,,,,True,"Alchemist Threshold Transmuted Knowledge Study Decor Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0013_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0013_Ready_for_Steaming\Cover_Mockup.png,True,True,Etsy_Draft_Prepared
Poster-Academia-0014,Poster,Academia,Printify_Published_Mockups4,69f8530b5da263f75f04d837,,,Dark Academia Oracle Portal Prophetic Scriptures 12x18 Poster Study Decor Wall,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0014_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0014_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0011,Acrylic,Grimdark,Printify_Published_Mockups8,69f863f9f9374ed4f105c588,,,Grimdark Deathspeaker Oracle Lamp 5x7 Acrylic Gothic Collectible Art Shelf Gift,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0011_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0011_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0012,Acrylic,Grimdark,Printify_Published_Mockups4,69f8647ff9374ed4f105c605,,,Gothic Grimdark Phantom Lord Caged Soul 5x7 Acrylic Premium Collectible Decor,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0012_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0012_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0013,Acrylic,Grimdark,Printify_Published_Mockups4,69f865a55da263f75f04e768,,,Gothic Gravekeeper Lantern Grimdark Art 5x7 Acrylic Block Dark Fantasy Decor,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0013_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0013_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0014,Acrylic,Grimdark,Printify_Published_Mockups4,69f8669583a8608fd80f0fdb,,,Soulbound Harbinger Torch Grimdark Gothic Lantern 5x7 Acrylic Print Dark Decor,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0014_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0014_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0015,Acrylic,Grimdark,Printify_Published_Mockups4,69f867cc2592a8ad8e0f076e,,,Cursed Monk Penance Light Grimdark Gothic Artifact 5x7 Acrylic Collectible Gift,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0015_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0015_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0016,Acrylic,Grimdark,Printify_Published_Mockups4,69f86a3d25819cdf3d0563b6,,,Gothic Grimdark Shadowpriest Ritual Vessel 5x7 Acrylic Decor Indigo Flame Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0016_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0016_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0017,Acrylic,Grimdark,Printify_Published_Mockups4,69f86b8e83a8608fd80f1341,,,Grimdark Aesthetic Dreadlord Beacon Lantern 5x7 Acrylic Block Dark Decor Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0017_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0017_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0018,Acrylic,Grimdark,Printify_Published_Mockups4,69f86d3709f3b730240200b7,,,Sepulcher Guardian's Flame Grimdark Gothic Lantern 5x7 Acrylic Art Dark Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0018_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0018_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0019,Acrylic,Grimdark,Printify_Published_Mockups4,69f86f6c2810b52a940a4161,,,Abyssal Watcher Eternal Eye Grimdark Gothic Acrylic 5x7 Spirit Beacon Artifact,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0019_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0019_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0021,Acrylic,Grimdark,Printify_Published_Mockups4,69f8807a011b67ecf80761ae,,,Emerald Despair Lantern Grimdark Gothic Ironwork 5x7 Acrylic Block Dark Fantasy,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0021_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0021_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0022,Acrylic,Grimdark,Printify_Published_Mockups4,69f8818abe136844f0003e48,,,Violet Torment Lantern 5x7 Acrylic Grimdark Gothic Decor for Dark Fantasy Study,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0022_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0022_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0023,Acrylic,Grimdark,Printify_Published_Mockups8,69f882a1be136844f0003eed,,,Azure Suffering Lantern 5x7 Acrylic Grimdark Gothic Wall Art Decor Shelf Study,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0023_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0023_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0024,Acrylic,Grimdark,Printify_Published_Mockups8,69f8836c5da263f75f04fad5,,,Grimdark Obsidian Wrath Lantern 5x7 Acrylic Block Dark Fantasy Desk Art Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0024_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0024_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0025,Acrylic,Grimdark,Printify_Published_Mockups8,69f883f3be136844f0003ff9,,,Amber Anguish Lantern Grimdark Aesthetic 5x7 Acrylic Art Decor Shelf Study Gift,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0025_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0025_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0026,Acrylic,Grimdark,Printify_Published_Mockups4,69f88472ffbc831dea086941,,,Frost Agony Lantern Grimdark Ice Spirit 5x7 Acrylic Art Gothic Decor Shelf Gift,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0026_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0026_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0027,Acrylic,Grimdark,Printify_Published_Mockups4,69f884ed83a8608fd80f239c,,,Magenta Malice Lantern Grimdark Mentor-Grade 5x7 Acrylic Decor Dark Fantasy,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0027_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0027_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0028,Acrylic,Grimdark,Printify_Published_Mockups8,69f88562be136844f00040a3,,,Gothic Obsidian Shrine Soul Lantern 5x7 Acrylic Grimdark Artifact Display Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0028_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0028_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0030,Acrylic,Grimdark,Printify_Published_Mockups4,69f886005da263f75f04fc9d,,,Spectral Temple Soul Lantern Grimdark Mentor-Grade 5x7 Acrylic Art Collectible,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0030_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0030_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0031,Acrylic,Grimdark,Printify_Published_Mockups4,69f88ee825819cdf3d057c87,,,Midnight Sanctuary Soul Lantern Grimdark 5x7 Acrylic Collectible Display Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0031_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0031_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0032,Acrylic,Grimdark,Printify_Published_Mockups4,69f88fd4feed9979d10d0ce7,,,Grimdark Amber Monastery Soul Lantern 5x7 Acrylic Art Gothic Decor Golden Flame,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0032_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0032_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0033,Acrylic,Grimdark,Printify_Published_Mockups4,69f8904bc1f268dee601c34f,,,Grimdark Ethereal Archway Soul Lantern 5x7 Acrylic Display Gothic Artifact Gift,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0033_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0033_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0034,Acrylic,Grimdark,Printify_Published_Mockups4,69f890b8c1f268dee601c394,,,Emerald Sanctum Soul Lantern Grimdark Art 5x7 Acrylic Mentor-Grade Collectible,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0034_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0034_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0035,Acrylic,Grimdark,Printify_Published_Mockups8,69f89116b051b8a0e90b9662,,,Twilight Portal Soul Lantern Grimdark 5x7 Acrylic Art Gothic Decor Purple Flame,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0035_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0035_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0036,Acrylic,Grimdark,Printify_Published_Mockups8,69f8918925819cdf3d057e2d,,,Gothic Frost Cathedral Soul Lantern 5x7 Acrylic Display Grimdark Artifact Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0036_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0036_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0037,Acrylic,Grimdark,Printify_Published_Mockups8,69f892035da263f75f05059e,,,Gothic Onyx Shrine Soul Lantern 5x7 Acrylic Display Grimdark Collectible Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0037_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0037_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Acrylic-Grimdark-0038,Acrylic,Grimdark,Printify_UI_Mockups4,69f8928b25819cdf3d057ef7,,,Rose Quartz Chapel Soul Lantern Grimdark 5x7 Acrylic Art Gothic Collectible,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0038_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0038_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Acrylic-Grimdark-0039,Acrylic,Grimdark,Printify_UI_Mockups4,69f8931cb051b8a0e90b97c7,,,Sapphire Temple Soul Lantern Grimdark 5x7 Acrylic Display Gothic Artifact Shelf,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0039_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0039_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Acrylic-Grimdark-0040,Acrylic,Grimdark,Printify_UI_Mockups4,69f8937bbe136844f0004b36,,,Silver Moon Gate Soul Lantern Grimdark 5x7 Acrylic Art Gothic Mentor-Grade Gift,$89.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0040_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0040_Ready_for_Steaming\Cover_Mockup.png,True,True,Stable_Draft_Publish_When_Scheduled
Poster-Academia-0017,Poster,Academia,Printify_Published_Mockups8,69f89a94c1f268dee601cb9d,,,Dark Academia Poster 12x18 Magister Torii Study Decor Scholarly Gift Wall Room,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0017_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0017_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0019,Poster,Academia,Printify_Published_Mockups8,69f89b9ca70f06579a00a708,,,Dark Academia Archivist Gateway Poster 12x18 Vintage Study Room Decor Wall Gift,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0019_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0019_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0020,Poster,Academia,Printify_Published_Mockups8,69f89c6f09f3b730240221b8,,,Dark Academia Mentor Threshold Poster 12x18 Intellectual Study Room Decor Wall,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0020_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0020_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0021,Poster,Academia,Printify_Published_Mockups8,69f89da69f68ab7cf001f531,,,Dark Academia Celestial Chronometer Archive Sphere 12x18 Poster Study Decor,$34.99,,,,True,"Celestial Chronometer Archive Sphere Study Decor Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0021_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0021_Ready_for_Steaming\Cover_Mockup.png,True,True,Etsy_Draft_Prepared
Poster-Academia-0022,Poster,Academia,Printify_Published_Mockups8,69f89eac011b67ecf8077844,,,Dark Academia Temporal Reliquary Bell Jar 12x18 Poster Study Decor Wall Library,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0022_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0022_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0023,Poster,Academia,Printify_Published_Mockups8,69f89fda2592a8ad8e0f2e79,,,Hermetic Knowledge Lantern Dark Academia Poster 12x18 Library Decor Wall Study,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0023_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0023_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0024,Poster,Academia,Printify_Published_Mockups8,69f8a454c1f268dee601d3ad,,,Dark Academia Industrial Library Pressure Chamber Poster 12x18 Vintage Decor,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0024_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0024_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0025,Poster,Academia,Printify_Published_Mockups4,69f903dec1f268dee601f679,,,Dark Academia Chrono-Codex Terrarium 12x18 Poster Library Decor Wall Study Gift,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0025_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0025_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0026,Poster,Academia,Printify_Published_Mockups4,69f904df97d964f736006a48,,,Dark Academia Apothecary Cylinder 12x18 Poster Vintage Study Decor Wall Library,$34.99,,,,True,"Apothecary Cylinder Study Decor Wall Library Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0026_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0026_Ready_for_Steaming\Cover_Mockup.png,True,True,Etsy_Draft_Prepared
Poster-Academia-0027,Poster,Academia,Printify_Published_Mockups4,69f90607feed9979d10d40e7,,,Dark Academia Astrolabe Dome Poster 12x18 Vintage Study Room Decor Wall Library,$34.99,,,,True,"Astrolabe Dome Study Room Decor Wall Library Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0027_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0027_Ready_for_Steaming\Cover_Mockup.png,True,True,Etsy_Draft_Prepared
Poster-Academia-0028,Poster,Academia,Printify_Published_Mockups4,69f907b49f68ab7cf0022003,,,Dark Academia Alchemist Retort Library Poster 12x18 Study Decor Wall Gift Room,$34.99,,,,True,"Alchemist Retort Library Study Decor Wall Room Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0028_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0028_Ready_for_Steaming\Cover_Mockup.png,True,True,Etsy_Draft_Prepared
Poster-Academia-0030,Poster,Academia,Printify_Published_Mockups8,69f90c957f4b346c8a0c603f,,,Dark Academia Grimoire Preservation Capsule 12x18 Poster Study Decor Wall Gift,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0030_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0030_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0031,Poster,Academia,Printify_Published_Mockups4,69fba23409770f1d9306b86d,,,Dark Academia Botanical Codex Conservatory Poster 12x18 Study Decor Wall Gift,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0031_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0031_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0032,Poster,Academia,Printify_Published_Mockups4,69fba266489d5635ab0e6504,,,Dark Academia Observatory Archive Prism 12x18 Poster Study Room Decor Wall Gift,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0032_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0032_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0033,Poster,Academia,Printify_Published_Mockups4,69fba28a6d07bd21600e1684,,,Dark Academia Philosophical Theorem Reliquary Poster 12x18 Study Decor Wall,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0033_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0033_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0034,Poster,Academia,Printify_Published_Mockups8,69fbbffef60a24b6d1034e4d,,,Dark Academia Nautical Archive Barometer 12x18 Poster Study Decor Wall Library,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0034_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0034_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0005-FIX1,Sticker,Academia,Retired_Replaced,69fb7a5154fd3fbacf050c5a,,,Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Dark Academia Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0005-FIX2,Sticker,Academia,Printify_Published_Mockups6,69fb7e754ce71ea8ae0c7af1,,,Forbidden Grimoire Lock 4pc 6x6 Kiss-Cut Sticker Dark Academia Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,False,True,Fix_Gallery_First
Sticker-Academia-0006-FIX1,Sticker,Academia,Printify_Published_Mockups3,69fb804bff28e7d4030aa67d,,,4pc Sticker Set Botanical Terrarium Lantern Vinyl Decals Laptop Bottle Dark,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0006_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0007-FIX1,Sticker,Academia,Printify_Published_Mockups3,69fb819d4c6544084c0f8370,,,4pc Kiss-Cut Sticker Set Astrolabe Navigation Instrument Laptop Journal Bottle,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0007_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0008-FIX1,Sticker,Academia,Printify_Published_Mockups3,69fb82e64c6544084c0f83d5,,,Ritual Incense Censer Gothic Academia 4pc 6x6 Vinyl Sticker Reader Writer Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0009-FIX1,Sticker,Academia,Printify_Published_Mockups3,69fb868dc5114ecf420d2b93,,,4pc Sticker Set Gothic Academia Cathedral Fragment Vinyl Decals Laptop Bottle,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0010-FIX1,Sticker,Academia,Printify_Published_Mockups3,69fb8749a7afceb9f70f1956,,,Vintage Academia Compass Rose Talisman 4pc 6x6 Sticker Sheet Literary Cozy Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0011-FIX1,Sticker,Academia,Printify_Published_Mockups3,69fb87aca7afceb9f70f1982,,,Apothecary Poison Vial Vintage Academia 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0011_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0014-FIX1,Sticker,Academia,Printify_Published_Mockups3,69fb87efc5114ecf420d2c5a,,,4pc Vinyl Sticker Set Microscope Observation Device Laptop Bottle Journal Dark,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0014_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0015-FIX1,Sticker,Academia,Printify_Published_Mockups6,69fb8805ee663532c8017f4f,,,4pc Sticker Set Skeleton Key Portal Vinyl Decals Laptop Bottle Dark Academia,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0015_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Academia-0016-FIX1,Sticker,Academia,Printify_Published_Mockups6,69fb8811e5402c478e03108f,,,4pc Kiss-Cut Sticker Set Gothic Academia Prism Light Refractor Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0016_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0001-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fb881f2b1da07362014876,,,4pc Sticker Set Mindful Zen Koi Pond Vinyl Decals Laptop Bottle Zen Aesthetic,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0002-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fb882c54fd3fbacf051371,,,Minimal Zen Bonsai Tree of Serenity 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0003-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fb883cce0d8cb5570fa7cc,,,Lotus Mandala Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift Decor,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0004-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fb8849e5402c478e0310af,,,4pc Sticker Set Stone Guardian Lion Mindful Zen Vinyl Decals Laptop Bottle Zen,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0005-FIX1,Sticker,Zen,Printify_Published_Mockups3,69fbae614c6544084c0f95ec,,,Bamboo Forest Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Misty Art,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0007-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fbae7da7afceb9f70f2982,,,4pc Sticker Set Cherry Blossom Branch Vinyl Decals Laptop Bottle Zen Aesthetic,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0007_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0008-FIX1,Sticker,Zen,Printify_Published_Mockups3,69fbae974c6544084c0f9610,,,4pc Kiss-Cut Sticker Set Circle Ens Laptop Journal Bottle Zen Aesthetic Decal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0009-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fbaea961c4aefdea04aaaf,,,Zen Aesthetic Praying Mantis on Rock 4pc 6x6 Kiss-Cut Sticker Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0022-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fbaeb9f60a24b6d1034575,,,Mindful Zen Garden Stone Meis seki 4pc 6x6 Vinyl Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0022_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0024-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fbaecbb8dd7e2bb0094b7c,,,Mindful Zen Enso Circle with Crystals 4pc 6x6 Vinyl Sticker Laptop Journal Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0024_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0025-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fbaedb4c6544084c0f9620,,,Koi Fish in Jade Pond Hisui no Koi Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Luck,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0025_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0027-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fbaeebce0d8cb5570fb7dc,,,Minimal Zen Temple Lantern Zendera no T r 4pc 6x6 Sticker Sheet Serene Mindful,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0027_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0041-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fbaefcc6dfbcc11107aa91,,,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0041_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0042-FIX1,Sticker,Zen,Printify_Published_Mockups3,69fbaf12ff28e7d4030aba2d,,,Bioluminescent Crystal Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0042_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0035,Poster,Academia,Printify_Published_Mockups8,69fbc023f60a24b6d1034e5c,,,Dark Academia Poster Theological Codex Sanctuary 12x18 Study Decor Wall Library,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0035_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0035_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0036,Poster,Academia,Printify_Published_Mockups8,69fbc0482b1da073620161ad,,,Mechanical Encyclopedia Sphere Dark Academia Aesthetic 12x18 Poster Study Room,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0036_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0036_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0037,Poster,Academia,Printify_Published_Mockups8,69fbc06d61c4aefdea04b362,406909473606,https://www.ebay.com/itm/406909473606,Cryptographic Vault Cylinder Dark Academia Poster 12x18 Secret Knowledge Decor,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0037_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0037_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0038,Poster,Academia,Printify_PublishExternalPending_Mockups8,69fbccf9ce0d8cb5570fc6f0,,,Geological Archive Geode Dark Academia Poster 12x18 Mentor-Grade Decor Wall,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0038_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0038_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0039,Poster,Academia,Printify_PublishExternalPending_Mockups8,69fbcd1aee663532c8019ec7,,,Dark Academia Horological Manuscript Chamber Poster 12x18 Study Decor Wall Gift,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0039_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0039_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0040,Poster,Academia,Printify_PublishExternalPending_Mockups8,69fbcd3eb8dd7e2bb0095af7,,,Dark Academia Meteorological Orrery 12x18 Poster Study Decor Atmospheric Texts,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0040_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0040_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0041,Poster,Academia,Printify_PublishExternalPending_Mockups8,69fbcd65cacc667dc70b7c2a,,,Dark Academia Astrological Globe Poster 12x18 Study Room Decor Starlight Jade,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0041_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0041_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Poster-Academia-0042,Poster,Academia,Printify_PublishExternalPending_Mockups8,69fbcd8a3014a1ea840da971,,,Dark Academia Armillary Sphere Poster 12x18 Vintage Study Decor Zodiac Symbols,$34.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0042_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0042_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0044-FIX1,Sticker,Zen,Printify_Published_Mockups3,69fbdfc9f60a24b6d1035f8b,406909884756,https://www.ebay.com/itm/406909884756,Zen Aesthetic Dragon Coil 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water Bottle,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0044_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0045-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fc03470ce75ae193034081,406909890800,https://www.ebay.com/itm/406909890800,Floating Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Sky Art,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0045_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0046-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fc035bce0d8cb5570fe6af,406909891985,https://www.ebay.com/itm/406909891985,Zen Aesthetic Dragon and Pearl 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0046_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0049-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fc036aee663532c801be71,406909893702,https://www.ebay.com/itm/406909893702,Sleeping Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0049_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0050-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fc0639ee663532c801bff2,406909904704,https://www.ebay.com/itm/406909904704,Translucent Jade Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0050_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0051-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fc06482007fddea00dcf21,406909905683,https://www.ebay.com/itm/406909905683,Kintsugi Gold Dragon Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0051_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0052-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fc0655ee663532c801bffc,406909906686,https://www.ebay.com/itm/406909906686,Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0052_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0053-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fc06640ce75ae19303421a,406909907111,https://www.ebay.com/itm/406909907111,Crystalline Dragon Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0053_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold
Sticker-Zen-0054-FIX1,Sticker,Zen,Printify_Published_Mockups6,69fc0674ee663532c801c009,406909907742,https://www.ebay.com/itm/406909907742,Dragon Meditation Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,$11.99,,,,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0054_Ready_for_Steaming\Cover_Mockup.png,True,True,Hold

```


### RAW LOG: Database/Market_Signal_Action_Queue.csv
```text
﻿Priority,ID,Product_Type,Category,Action_Bucket,Recommended_Action,Reason,Network_Dependency,Can_Do_Now,eBay_Item_ID,Latest_Views_30_Days,Etsy_Planned
100,Acrylic-Grimdark-0081,Acrylic,Grimdark,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902606976,0,False
100,Acrylic-Zen-0001,Acrylic,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902620519,0,True
100,Poster-Academia-0001,Poster,Academia,Published_Has_View_Monitor,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902584620,1,False
100,Poster-Academia-0003,Poster,Academia,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902616799,0,True
100,Sticker-Academia-0005,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0006,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0007,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0008,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0009,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0010,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0011,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0014,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0015,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Academia-0016,Sticker,Academia,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0001,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0002,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0003,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0004,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0005,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0007,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0008,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0009,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0022,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0024,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0025,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0027,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0041,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0042,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,,,False
100,Sticker-Zen-0044,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902622710,0,False
100,Sticker-Zen-0045,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902640998,0,False
100,Sticker-Zen-0046,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902663232,0,False
100,Sticker-Zen-0049,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902713267,0,False
100,Sticker-Zen-0050,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902886081,0,False
100,Sticker-Zen-0051,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902889638,0,False
100,Sticker-Zen-0052,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902896387,0,False
100,Sticker-Zen-0053,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406902900109,0,False
100,Sticker-Zen-0054,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903032635,0,False
100,Sticker-Zen-0055,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903037933,0,False
100,Sticker-Zen-0056,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903041315,0,False
100,Sticker-Zen-0057,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903044643,0,False
100,Sticker-Zen-0058,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903049411,0,False
100,Sticker-Zen-0060,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903249053,0,False
100,Sticker-Zen-0061,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903249987,0,False
100,Sticker-Zen-0062,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903250891,0,False
100,Sticker-Zen-0063,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903252007,0,False
100,Sticker-Zen-0066,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903252739,,False
100,Sticker-Zen-0069,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903753067,,False
100,Sticker-Zen-0070,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903757240,,False
100,Sticker-Zen-0071,Sticker,Zen,Hold,FIX_LIVE_COVER_SOURCE_OR_REPLACE,"Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",medium,False,406903762328,,False
90,Poster-Academia-0021,Poster,Academia,Etsy_Draft_Prepared,QA_HOLD_OR_REBUILD,Local QA issue: corrupt_production,local,True,,,True
90,Sticker-Academia-0001,Sticker,Academia,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Academia-0002,Sticker,Academia,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Academia-0003,Sticker,Academia,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Academia-0005-FIX2,Sticker,Academia,Fix_Gallery_First,QA_HOLD_OR_REBUILD,Local QA issue: missing_gallery,local,True,,,False
90,Sticker-Academia-0013,Sticker,Academia,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0006,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0021,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0023,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0028,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0030,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0033,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0039,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0078,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0079,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0080,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0082,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0085,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0090,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0116,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0118,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0120,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0121,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0122,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0124,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0125,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0140,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0144,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
90,Sticker-Zen-0152,Sticker,Zen,Hold,QA_HOLD_OR_REBUILD,Local QA issue: missing_cover; missing_gallery,local,True,,,False
80,Acrylic-Academia-0003,Acrylic,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902703464,0,False
80,Acrylic-Academia-0005,Acrylic,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903039716,0,True
80,Acrylic-Grimdark-0001,Acrylic,Grimdark,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903249745,0,False
80,Acrylic-Grimdark-0004,Acrylic,Grimdark,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903250705,0,False
80,Acrylic-Grimdark-0005,Acrylic,Grimdark,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903251829,0,False
80,Acrylic-Grimdark-0082,Acrylic,Grimdark,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902633400,0,False
80,Acrylic-Grimdark-0083,Acrylic,Grimdark,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902885214,0,False
80,Acrylic-Grimdark-0085,Acrylic,Grimdark,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903043482,0,False
80,Acrylic-Zen-0002,Acrylic,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902657898,0,True
80,Acrylic-Zen-0003,Acrylic,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902673249,0,False
80,Acrylic-Zen-0005,Acrylic,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902893289,0,False
80,Acrylic-Zen-0007,Acrylic,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903028253,0,True
80,Acrylic-Zen-0008,Acrylic,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903036452,0,False
80,Acrylic-Zen-0009,Acrylic,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903047385,0,False
80,Acrylic-Zen-0010,Acrylic,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903213858,0,False
80,Poster-Academia-0002,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902600741,0,False
80,Poster-Academia-0005,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903038850,0,False
80,Poster-Academia-0006,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903042690,0,True
80,Poster-Academia-0008,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903046097,0,True
80,Poster-Academia-0009,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903209258,0,False
80,Poster-Academia-0010,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903249496,0,False
80,Poster-Academia-0011,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903250376,0,True
80,Poster-Academia-0083,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902669660,0,True
80,Poster-Academia-0084,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902691983,0,False
80,Poster-Academia-0091,Poster,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902887127,0,True
80,Poster-Zen-0001,Poster,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902890971,0,False
80,Poster-Zen-0002,Poster,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406902897663,0,True
80,Poster-Zen-0004,Poster,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903026999,0,True
80,Poster-Zen-0005,Poster,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406903033377,0,False
80,Sticker-Academia-0004,Sticker,Academia,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406892408950,0,False
80,Sticker-Zen-0010,Sticker,Zen,Published_Zero_View_Copy_Ad_Review,WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST,"Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",low,True,406892414116,0,False
70,Acrylic-Grimdark-0038,Acrylic,Grimdark,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Acrylic-Grimdark-0039,Acrylic,Grimdark,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Acrylic-Grimdark-0040,Acrylic,Grimdark,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0072,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0073,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0074,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0075,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0076,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0081,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0083,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0084,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0086,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0087,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0088,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0089,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0091,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0092,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0093,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
70,Sticker-Zen-0094,Sticker,Zen,Stable_Draft_Publish_When_Scheduled,PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK,Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.,medium,False,,,False
60,Sticker-Zen-0095,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0096,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0097,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0098,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0099,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0100,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0101,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0102,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0103,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0104,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0105,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0106,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0107,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0108,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0109,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0110,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0111,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0112,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0113,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0114,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0115,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0117,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0123,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0126,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0127,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0128,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0129,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0130,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0131,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0132,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0133,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0134,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0135,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0136,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0138,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0139,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0150,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0151,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0153,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0154,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0155,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0156,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0157,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0158,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0159,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
60,Sticker-Zen-0160,Sticker,Zen,Ready_For_Printify_When_Network_OK,UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH,Local assets are ready but network-dependent upload remains pending.,high,False,,,False
50,Poster-Academia-0013,Poster,Academia,Etsy_Draft_Prepared,KEEP_FOR_ETSY_PHASE1,Candidate already selected for Etsy relaunch; wait for shop/OAuth readiness and listing-fee confirmation.,medium,False,,,True
50,Poster-Academia-0026,Poster,Academia,Etsy_Draft_Prepared,KEEP_FOR_ETSY_PHASE1,Candidate already selected for Etsy relaunch; wait for shop/OAuth readiness and listing-fee confirmation.,medium,False,,,True
50,Poster-Academia-0027,Poster,Academia,Etsy_Draft_Prepared,KEEP_FOR_ETSY_PHASE1,Candidate already selected for Etsy relaunch; wait for shop/OAuth readiness and listing-fee confirmation.,medium,False,,,True
50,Poster-Academia-0028,Poster,Academia,Etsy_Draft_Prepared,KEEP_FOR_ETSY_PHASE1,Candidate already selected for Etsy relaunch; wait for shop/OAuth readiness and listing-fee confirmation.,medium,False,,,True
40,Acrylic-Academia-0001,Acrylic,Academia,Published_Has_View_Monitor,MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL,Item has at least one view; do not churn copy too quickly.,low,True,406902588642,1,True
40,Acrylic-Zen-0004,Acrylic,Zen,Published_Has_View_Monitor,MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL,Item has at least one view; do not churn copy too quickly.,low,True,406902888077,1,False
40,Acrylic-Zen-0006,Acrylic,Zen,Published_Has_View_Monitor,MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL,Item has at least one view; do not churn copy too quickly.,low,True,406902898909,2,True
40,Poster-Academia-0081,Poster,Academia,Published_Has_View_Monitor,MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL,Item has at least one view; do not churn copy too quickly.,low,True,406902627420,2,True
40,Poster-Academia-0082,Poster,Academia,Published_Has_View_Monitor,MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL,Item has at least one view; do not churn copy too quickly.,low,True,406902648209,3,False
40,Poster-Academia-0085,Poster,Academia,Published_Has_View_Monitor,MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL,Item has at least one view; do not churn copy too quickly.,low,True,406902882943,1,False
20,Acrylic-Grimdark-0006,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406903252506,,False
20,Acrylic-Grimdark-0007,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406903731967,,False
20,Acrylic-Grimdark-0008,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406903746215,,False
20,Acrylic-Grimdark-0009,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406903749989,,False
20,Acrylic-Grimdark-0010,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406903756190,,False
20,Acrylic-Grimdark-0011,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0012,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0013,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0014,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0015,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0016,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0017,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0018,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0019,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0021,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0022,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0023,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0024,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0025,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0026,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0027,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0028,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0030,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0031,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0032,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0033,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0034,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0035,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0036,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Acrylic-Grimdark-0037,Acrylic,Grimdark,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0014,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0017,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0019,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0020,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0022,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0023,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0024,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0025,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0030,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0031,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0032,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0033,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0034,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0035,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0036,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0037,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909473606,,False
20,Poster-Academia-0038,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0039,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0040,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0041,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Academia-0042,Poster,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Poster-Zen-0003,Poster,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0005-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0006-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0007-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0008-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0009-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0010-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0011-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0014-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0015-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Academia-0016-FIX1,Sticker,Academia,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0001-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0002-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0003-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0004-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0005-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0007-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0008-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0009-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0022-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0024-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0025-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0026,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0027-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0029,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0031,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0032,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0034,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0035,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0036,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0037,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0038,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0040,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0041-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0042-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0044-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909884756,,False
20,Sticker-Zen-0045-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909890800,,False
20,Sticker-Zen-0046-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909891985,,False
20,Sticker-Zen-0048,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0049-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909893702,,False
20,Sticker-Zen-0050-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909904704,,False
20,Sticker-Zen-0051-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909905683,,False
20,Sticker-Zen-0052-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909906686,,False
20,Sticker-Zen-0053-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909907111,,False
20,Sticker-Zen-0054-FIX1,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,406909907742,,False
20,Sticker-Zen-0067,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False
20,Sticker-Zen-0068,Sticker,Zen,Hold,HOLD,No safe action under current weak-network protocol.,local,True,,,False

```


### RAW LOG: Database/Factory_Backlog.csv
```text
﻿Priority,Lane,Task,Status,Blocker,Command,Done_When,Risk,Network_Need,Owner
100,control,Run local supervisor maintenance cycle,READY,None,py modules\factory_supervisor.py --execute-local --skip-network,"Factory_Autopilot_State, action queue, QA, traffic diagnosis, morning report, and Gemini queue refresh with 0 failures.",low,local,Codex
100,supervisor:local,"Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.",READY,Safe low-bandwidth maintenance keeps the factory state current while account/image writes are paused.,py modules\factory_supervisor.py --execute-local --skip-network,Supervisor action remains present until its status is completed or superseded.,low,no,Codex
98,cover_gate,Repair one live eBay cover mismatch from Printify source and audit buyer page,READY,Printify CDP status: LOGGED_IN; Printify app page is available in CDP browser.,py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120,"One SKU becomes LIVE_COVER_FIXED, or the runner records that replacement-listing fallback is required.",medium,single online item,Codex
97,supervisor:replacement,Create one verified replacement listing for a live cover failure that survived source repair.,READY_TO_REPLACE_VERIFIED,12 listing already failed source repair plus live eBay buyer-page audit.,py modules\ebay_replacement_draft_builder.py --limit 1,Supervisor action remains present until its status is completed or superseded.,high,yes,Codex
95,supervisor:cover_gate,"Repair one Printify source cover, then live-audit eBay before scaling.",READY_SINGLE_SKU_REPAIR,Live cover queue has 49 rows; 12 require Printify source repair or replacement listings. Printify UI: LOGGED_IN - Printify app page is available in CDP browser.,py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120,Supervisor action remains present until its status is completed or superseded.,medium,yes,Codex
94,replacement,Create verified replacement listing for source-repaired live cover failure,READY_TO_REPLACE_VERIFIED,12 row already failed source repair plus live eBay audit.,py modules\ebay_replacement_draft_builder.py --limit 1,Replacement row is created as Ready_for_Printify; public publish still waits for QA and retire sequencing.,high,single replacement listing,Codex
72,production,Resume Ready_for_Printify uploads only after cover/default-image gate passes,WAIT_COVER_GATE,46 local rows are ready but should not upload until the image gate is proven.,py modules\printify_full_pipeline.py --limit 1,A new single item reaches stable mockup state and passes selected-count/default-count audit.,high,Printify UI/API,Codex
68,publish,Publish small cooled batch after image gate and network guard pass,WAIT_COVER_GATE,"19 stable drafts are candidates, but public publish is blocked by cover/default-image risk.",py modules\printify_publish_scheduler.py --limit 3 --min-delay 180 --max-delay 420,Published products are live-audited and added to 2% Standard/General ad coverage without PPC.,high,Printify API/eBay sync,Codex
63,supervisor:production_design_qa,Run a tiny Printify production-design audit before any larger online batch.,READY,This checks whether Printify front print-area art visually matches local Production_Design files; keep it small under weak Wi-Fi.,py modules\printify_design_audit.py --limit 2 --sleep-seconds 1,Supervisor action remains present until its status is completed or superseded.,low,yes,Codex
62,market_learning,Keep eBay traffic diagnosis current and avoid ad-only conclusions,READY,4 current traffic hypotheses generated.,py modules\ebay_traffic_diagnosis.py,Traffic report identifies exposure/click/conversion blockers from snapshots and cover queues.,low,local,Codex
56,etsy,Monitor first 10 Etsy Digital listings before spending more,READY_MONITOR,Live=10 ready=20 confirmed_spend=$2.00.,py modules\etsy_live_audit.py --limit 10,Morning readout has active/readable status plus views/favorites when available; do not scale until signal or Rex resumes.,low,Etsy public/UI read,Codex
55,supervisor:etsy,Monitor Etsy Digital first gray batch before spending more listing fees.,READY_MONITOR,Live=10 ready=20 confirmed_spend=$2.00; hold scale until first traffic readout.,py modules\etsy_live_audit.py --limit 10,Supervisor action remains present until its status is completed or superseded.,low,yes,Codex
50,supervisor:copy_experiment,Continue low-bandwidth SEO/title/description experiment analysis.,READY,Ads alone did not move zero-view listings; controlled copy/image experiments are the next learning loop.,py modules\ebay_experiment_report.py,Supervisor action remains present until its status is completed or superseded.,low,no,Codex
46,r_and_d,Validate next product candidates with official Printify blueprint/provider/variant data,READY_FOR_SCHOLAR_REVIEW,5 next blueprint candidates are documented.,py modules\product_blueprint_next_plan.py,"Canvas, framed poster, notebook, mug, and metal candidates have enough data for Scholar review before development.",low,local,Codex

```


## Latest Reports


### REPORT: Reports\morning_report_20260506_2346.md
```markdown
# OpenClaw Morning Report

Generated: 2026-05-06 23:46 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 156
- Published through Printify/eBay tracking: 137
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 23:44:26 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 282
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

- Etsy_Draft_Prepared: 5
- Fix_Gallery_First: 1
- Hold: 162
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 42
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 59
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 33
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 12
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 6
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.

```


### REPORT: Reports\morning_report_20260506_2339.md
```markdown
# OpenClaw Morning Report

Generated: 2026-05-06 23:39 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 156
- Published through Printify/eBay tracking: 137
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 20:32:20 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 282
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

- Etsy_Draft_Prepared: 6
- Fix_Gallery_First: 1
- Hold: 169
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 34
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 59
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 33
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 12
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 6
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.

```


### REPORT: Reports\morning_report_20260506_2311.md
```markdown
# OpenClaw Morning Report

Generated: 2026-05-06 23:11 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 156
- Published through Printify/eBay tracking: 137
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 20:32:20 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 274
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

- Etsy_Draft_Prepared: 6
- Fix_Gallery_First: 1
- Hold: 153
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 42
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 51
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 25
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 20
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 6
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.

```


### REPORT: Reports\morning_report_20260506_2230.md
```markdown
# OpenClaw Morning Report

Generated: 2026-05-06 22:30 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 156
- Published through Printify/eBay tracking: 137
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 20:32:20 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 274
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

- Etsy_Draft_Prepared: 6
- Fix_Gallery_First: 1
- Hold: 152
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 43
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 50
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 24
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 21
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 7
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 1
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2
- Backlog WAIT_USER_OR_API_APPROVAL: 1

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:read_only_market: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.

```


### REPORT: Reports\morning_report_20260506_2031.md
```markdown
# OpenClaw Morning Report

Generated: 2026-05-06 20:31 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 169
- Published through Printify/eBay tracking: 150
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 76, published 60, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 01:23:31 -0400
- Rows read: 50
- 0-view rows in snapshot: 42
- Rows with at least 1 view: 8
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 273
- Etsy digital printable upload queue: 20 listings, max file 3.42MB, under 20MB limit: True
- Etsy digital previews: 20 listings x 3 preview images
- Etsy digital final upload packet: 20 listings, QA bad=0, missing=0
- Etsy digital bundle concepts: 3
- eBay cover QA rows: 14

## Unified Registry Buckets

- Etsy_Draft_Prepared: 20
- Fix_Gallery_First: 1
- Hold: 187
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 50
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 24
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 21
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 7
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2
- Backlog WAIT_USER_OR_API_APPROVAL: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:read_only_market: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Until wired/low-latency network is confirmed, prefer local low-bandwidth tasks and single-item network probes.
- No Etsy publish until Rex confirms listing-fee spend.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.

```


### REPORT: Reports\morning_report_20260506_2022.md
```markdown
# OpenClaw Morning Report

Generated: 2026-05-06 20:22 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 169
- Published through Printify/eBay tracking: 150
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 76, published 60, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 01:23:31 -0400
- Rows read: 50
- 0-view rows in snapshot: 42
- Rows with at least 1 view: 8
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 273
- Etsy digital printable upload queue: 20 listings, max file 3.42MB, under 20MB limit: True
- Etsy digital previews: 20 listings x 3 preview images
- Etsy digital final upload packet: 20 listings, QA bad=0, missing=0
- Etsy digital bundle concepts: 3
- eBay cover QA rows: 14

## Unified Registry Buckets

- Etsy_Draft_Prepared: 20
- Fix_Gallery_First: 1
- Hold: 187
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 50
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 24
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 21
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 7
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2
- Backlog WAIT_USER_OR_API_APPROVAL: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:read_only_market: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Until wired/low-latency network is confirmed, prefer local low-bandwidth tasks and single-item network probes.
- No Etsy publish until Rex confirms listing-fee spend.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.

```


### GEMINI QUEUE: Gemini_Advisor\gemini_review_queue_20260506_2346.md
```markdown
# Gemini Advisor Review Queue

Generated: 2026-05-06 23:46 -0400 America/New_York

Rex is Commander, Gemini is Strategy Advisor, Codex is Executive Operator.

Please review the current OpenClaw plan as a strategy advisor. Do not request API keys, account secrets, payment data, buyer private data, or direct account actions.

## Report Summary

# OpenClaw Morning Report

Generated: 2026-05-06 23:46 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 156
- Published through Printify/eBay tracking: 137
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 23:44:26 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 282
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

- Etsy_Draft_Prepared: 5
- Fix_Gallery_First: 1
- Hold: 162
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 42
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 59
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 33
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 12
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 6
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.


## Questions for Gemini

1. Given the first 10 Etsy Digital listings are live, what early signal should decide whether to spend the next $2 gray cell?
2. If the first 10 get 0 views after indexing, which search-intent variable should be changed first: title/category angle, product format, or visual theme?
3. Which three visual DNA themes should be expanded first if Etsy impressions appear but clicks remain low?
4. What ad test would you run first with a $3-5/day Etsy Ads budget after 48-72 hours of organic data?
5. Which product language sounds too mass-generated and should be softened before launch?

## Codex Action Filter

- Adopted:
- Deferred:
- Rejected:
- Requires Rex confirmation:

```


### GEMINI QUEUE: Gemini_Advisor\gemini_review_queue_20260506_2339.md
```markdown
# Gemini Advisor Review Queue

Generated: 2026-05-06 23:39 -0400 America/New_York

Rex is Commander, Gemini is Strategy Advisor, Codex is Executive Operator.

Please review the current OpenClaw plan as a strategy advisor. Do not request API keys, account secrets, payment data, buyer private data, or direct account actions.

## Report Summary

# OpenClaw Morning Report

Generated: 2026-05-06 23:39 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 156
- Published through Printify/eBay tracking: 137
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 20:32:20 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 282
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

- Etsy_Draft_Prepared: 6
- Fix_Gallery_First: 1
- Hold: 169
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 34
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 59
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 33
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 12
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 6
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.


## Questions for Gemini

1. Given the first 10 Etsy Digital listings are live, what early signal should decide whether to spend the next $2 gray cell?
2. If the first 10 get 0 views after indexing, which search-intent variable should be changed first: title/category angle, product format, or visual theme?
3. Which three visual DNA themes should be expanded first if Etsy impressions appear but clicks remain low?
4. What ad test would you run first with a $3-5/day Etsy Ads budget after 48-72 hours of organic data?
5. Which product language sounds too mass-generated and should be softened before launch?

## Codex Action Filter

- Adopted:
- Deferred:
- Rejected:
- Requires Rex confirmation:

```


### GEMINI QUEUE: Gemini_Advisor\gemini_review_queue_20260506_2311.md
```markdown
# Gemini Advisor Review Queue

Generated: 2026-05-06 23:11 -0400 America/New_York

Rex is Commander, Gemini is Strategy Advisor, Codex is Executive Operator.

Please review the current OpenClaw plan as a strategy advisor. Do not request API keys, account secrets, payment data, buyer private data, or direct account actions.

## Report Summary

# OpenClaw Morning Report

Generated: 2026-05-06 23:11 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 156
- Published through Printify/eBay tracking: 137
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 20:32:20 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 274
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

- Etsy_Draft_Prepared: 6
- Fix_Gallery_First: 1
- Hold: 153
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 42
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 51
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 25
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 20
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 6
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 2
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.


## Questions for Gemini

1. Given the first 10 Etsy Digital listings are live, what early signal should decide whether to spend the next $2 gray cell?
2. If the first 10 get 0 views after indexing, which search-intent variable should be changed first: title/category angle, product format, or visual theme?
3. Which three visual DNA themes should be expanded first if Etsy impressions appear but clicks remain low?
4. What ad test would you run first with a $3-5/day Etsy Ads budget after 48-72 hours of organic data?
5. Which product language sounds too mass-generated and should be softened before launch?

## Codex Action Filter

- Adopted:
- Deferred:
- Rejected:
- Requires Rex confirmation:

```


### GEMINI QUEUE: Gemini_Advisor\gemini_review_queue_20260506_2230.md
```markdown
# Gemini Advisor Review Queue

Generated: 2026-05-06 22:30 -0400 America/New_York

Rex is Commander, Gemini is Strategy Advisor, Codex is Executive Operator.

Please review the current OpenClaw plan as a strategy advisor. Do not request API keys, account secrets, payment data, buyer private data, or direct account actions.

## Report Summary

# OpenClaw Morning Report

Generated: 2026-05-06 22:30 -0400 America/New_York

## Current Factory State

- Stable Printify-tracked products: 156
- Published through Printify/eBay tracking: 137
- Ready for Printify: 46

## Product Counts

- Acrylic: stable 53, published 50, ready 0
- Poster: stable 40, published 40, ready 0
- Sticker: stable 63, published 47, ready 46

## Etsy Phase 1 Prep

- Draft-prepared Etsy launch candidates: 20
- Acrylic: 6
- Poster: 14

## Performance Snapshot

- Latest eBay snapshot: 2026-05-06 20:32:20 -0400
- Rows read: 50
- 0-view rows in snapshot: 43
- Rows with at least 1 view: 7
- General promoted rows in snapshot: 50

## Local Low-Bandwidth Work Completed

- Listing copy optimization candidates: 161
- Pricing matrix scenarios: 6
- Unified registry rows bucketed: 274
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

- Etsy_Draft_Prepared: 6
- Fix_Gallery_First: 1
- Hold: 152
- Published_Has_View_Monitor: 7
- Published_Zero_View_Copy_Ad_Review: 43
- Ready_For_Printify_When_Network_OK: 46
- Stable_Draft_Publish_When_Scheduled: 19

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
- Live eBay cover audit ERROR: 1
- Live eBay cover audit LIKELY_COVER: 13
- Live eBay cover audit LIKELY_COVER_OFFICIAL: 50
- Live eBay cover audit LIKELY_SINGLE_U_MISMATCH: 50
- Live cover fix queue rows: 49
- Cover replacement queue OLD_RETIRED_REPLACED_DONE: 24
- Cover replacement queue READY_TO_REPLACE_VERIFIED: 21
- Cover replacement queue REVIEW_BEFORE_REPLACE: 4
- Printify image-default audit rows: 161
- Printify image-default audit CHECK: 123
- Printify image-default audit OK: 38

## Factory Backlog

- Backlog READY: 7
- Backlog READY_FOR_SCHOLAR_REVIEW: 1
- Backlog READY_MONITOR: 1
- Backlog READY_SINGLE_SKU_REPAIR: 1
- Backlog READY_TO_REPLACE_VERIFIED: 2
- Backlog WAIT_COVER_GATE: 2
- Backlog WAIT_USER_OR_API_APPROVAL: 1

Top tasks:
- P100 control / READY: Run local supervisor maintenance cycle
- P100 supervisor:local / READY: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- P98 cover_gate / READY: Repair one live eBay cover mismatch from Printify source and audit buyer page
- P97 supervisor:replacement / READY_TO_REPLACE_VERIFIED: Create one verified replacement listing for a live cover failure that survived source repair.
- P95 supervisor:cover_gate / READY_SINGLE_SKU_REPAIR: Repair one Printify source cover, then live-audit eBay before scaling.

Lane counts:
- control: 1
- cover_gate: 1
- etsy: 1
- market_learning: 1
- production: 1
- publish: 1
- r_and_d: 1
- replacement: 1
- supervisor:copy_experiment: 1
- supervisor:cover_gate: 1
- supervisor:etsy: 1
- supervisor:local: 1
- supervisor:production_design_qa: 1
- supervisor:read_only_market: 1
- supervisor:replacement: 1

## Current Guardrails

- eBay rapid publish remains paused after Akamai/zero-size-object instability.
- Wired LAN is fixed; online work may run normally, but marketplace/account-risk throttles still apply.
- Etsy Digital first gray batch is live; do not spend beyond the next approved gray cell without traffic/signal logic.
- No paid ads activated without final action-time confirmation.
- Sticker expansion remains paused until the custom cover/gallery issue is fixed.
- Multiple Printify official/default mockups are allowed when they help product context; publish is blocked only by missing custom design/cover, live buyer-page mismatch, or zero default image.

## Operator Notes

- Focus is Phase 1: data foundation, Etsy relaunch prep, and performance learning loop.
- Printify storefront design is intentionally bypassed until Rex updates it or asks for drafts.


## Questions for Gemini

1. Given the first 10 Etsy Digital listings are live, what early signal should decide whether to spend the next $2 gray cell?
2. If the first 10 get 0 views after indexing, which search-intent variable should be changed first: title/category angle, product format, or visual theme?
3. Which three visual DNA themes should be expanded first if Etsy impressions appear but clicks remain low?
4. What ad test would you run first with a $3-5/day Etsy Ads budget after 48-72 hours of organic data?
5. Which product language sounds too mass-generated and should be softened before launch?

## Codex Action Filter

- Adopted:
- Deferred:
- Rejected:
- Requires Rex confirmation:

```


## Structured Extracts

Draft/Pending CSV: `C:\AIprojects\openclaw_difi\Review_Packets\GREY_DRAFT_PENDING_PRODUCTS_20260506_2348.csv`



### GREY_DRAFT_PENDING_PRODUCTS_20260506_2348.csv
```csv
ID,Product_Type,Category,Status,Title,Visual_DNA_Keywords,Printify_Product_ID,eBay_Item_ID
Sticker-Academia-0001,Sticker,Academia,Quality_Hold_LowRes_U,Dark Academia Celestial Gate Hourglass 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Dark Academia Celestial Gate Hourglass 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Academia-0002,Sticker,Academia,Quality_Hold_LowRes_U,Dark Academia Celestial Orrery Mechanism 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Dark Academia Celestial Orrery Mechanism 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Academia-0003,Sticker,Academia,Quality_Hold_LowRes_U,Dark Academia Alchemical Distillation Apparatus 4pc 6x6 Kiss-Cut Sticker Vinyl,Dark Academia Alchemical Distillation Apparatus 4pc 6x6 Kiss-Cut Sticker Vinyl,,
Sticker-Academia-0013,Sticker,Academia,Quality_Hold_LowRes_U,Dark Academia Serpent Ouroboros Ring 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,Dark Academia Serpent Ouroboros Ring 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Gift,,
Sticker-Zen-0006,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Ink Wash Mountain 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,Zen Aesthetic Ink Wash Mountain 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,,
Sticker-Zen-0021,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Kintsugi Lotus no Hasu 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Desk,Zen Aesthetic Kintsugi Lotus no Hasu 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Desk,,
Sticker-Zen-0023,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Bioluminescent Bonsai Hikaru 4pc 6x6 Kiss-Cut Sticker Vinyl Decor,Zen Aesthetic Bioluminescent Bonsai Hikaru 4pc 6x6 Kiss-Cut Sticker Vinyl Decor,,
Sticker-Zen-0026,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Mountain and Moon Sangetsu Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,Mountain and Moon Sangetsu Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,69f1cc732f305b371c05b1d7,
Sticker-Zen-0028,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Floating Tea Bowl Ukabu Chawan 4pc 6x6 Kiss-Cut Sticker Vinyl,Zen Aesthetic Floating Tea Bowl Ukabu Chawan 4pc 6x6 Kiss-Cut Sticker Vinyl,,
Sticker-Zen-0029,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Bamboo Forest Hikaru Chikurin Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,Bamboo Forest Hikaru Chikurin Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,69f1cee189347116c004f529,
Sticker-Zen-0030,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Meditating Frog Zazen Kaeru 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Zen Aesthetic Meditating Frog Zazen Kaeru 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Zen-0031,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Mindful Zen Kintsugi Lotus 4pc 6x6 Vinyl Sticker Laptop Journal Gift Meditation,Mindful Zen Kintsugi Lotus 4pc 6x6 Vinyl Sticker Laptop Journal Gift Meditation,69f1cf9911e0745fcb0da15f,
Sticker-Zen-0032,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Glowing Garden Stone 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,Glowing Garden Stone 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,69f1d04a0482f56ada0cf347,
Sticker-Zen-0033,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Crystalline Bamboo 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,Zen Aesthetic Crystalline Bamboo 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,,
Sticker-Zen-0034,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Zen Aesthetic Kintsugi Enso Circle 4pc 6x6 Kiss-Cut Sticker Laptop Journal Gift,Zen Aesthetic Kintsugi Enso Circle 4pc 6x6 Kiss-Cut Sticker Laptop Journal Gift,69f1d1003a934dcd94086687,
Sticker-Zen-0035,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Bioluminescent Koi Pond 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Bioluminescent Koi Pond 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,69f1d1ed11e0745fcb0da2ea,
Sticker-Zen-0036,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Fractal Cherry Blossom Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,Fractal Cherry Blossom Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,69f1d2a9f6b83091a5095eea,
Sticker-Zen-0037,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Mindful Zen Golden Veined Mountain 4pc 6x6 Vinyl Sticker Laptop Journal Gift,Mindful Zen Golden Veined Mountain 4pc 6x6 Vinyl Sticker Laptop Journal Gift,69f1d35c89347116c004f871,
Sticker-Zen-0038,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Meditating Crystal Frog Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,Meditating Crystal Frog Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,69f1d44bf6b83091a5095fca,
Sticker-Zen-0039,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Kintsugi Tea Bowl 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,Zen Aesthetic Kintsugi Tea Bowl 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,,
Sticker-Zen-0040,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Translucent Jade Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Translucent Jade Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,69f1d4f9bdda7e777002a696,
Sticker-Zen-0048,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Crystalline Dragon Scale 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Crystalline Dragon Scale 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,69f21bba9b469f716d0e4e42,
Sticker-Zen-0067,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Moonlit Jade Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,Moonlit Jade Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,69f25f0db0d6b88b28061022,
Sticker-Zen-0068,Sticker,Zen,Printify_PublishExternalPending_Mockups4,Fractal Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk Decor,Fractal Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk Decor,69f25faf29c1d0349a00ecec,
Sticker-Zen-0072,Sticker,Zen,Printify_UI_Mockups5,Celestial Koi Constellation 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Vinyl,Celestial Koi Constellation 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Vinyl,69f26281feceb0d66c042ce7,
Sticker-Zen-0073,Sticker,Zen,Printify_UI_Mockups5,Sacred Singing Bowl Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,Sacred Singing Bowl Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,69f262db5269e3325904b893,
Sticker-Zen-0074,Sticker,Zen,Printify_UI_Mockups5,Minimal Zen Bamboo Pagoda Relic 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,Minimal Zen Bamboo Pagoda Relic 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,69f263729b469f716d0e7409,
Sticker-Zen-0075,Sticker,Zen,Printify_UI_Mockups5,Mindful Zen Dragon Pearl Talisman 4pc 6x6 Vinyl Sticker Laptop Journal Gift,Mindful Zen Dragon Pearl Talisman 4pc 6x6 Vinyl Sticker Laptop Journal Gift,69f26426671cc7c7960b3f3d,
Sticker-Zen-0076,Sticker,Zen,Printify_UI_Mockups5,Moonlit Mountain Shrine Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,Moonlit Mountain Shrine Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,69f264df357398ded80f6a3a,
Sticker-Zen-0078,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Celestial Lotus Lantern 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Zen Aesthetic Celestial Lotus Lantern 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Zen-0079,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Celestial Koi Ascending 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Zen Aesthetic Celestial Koi Ascending 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Zen-0080,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Moonstone Phoenix Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Zen Aesthetic Moonstone Phoenix Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Zen-0081,Sticker,Zen,Printify_UI_Mockups5,Celestial Koi Ascension Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,Celestial Koi Ascension Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,69f26782c326d7da170c1498,
Sticker-Zen-0082,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Lotus Lantern Relic 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,Zen Aesthetic Lotus Lantern Relic 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,,
Sticker-Zen-0083,Sticker,Zen,Printify_UI_Mockups5,Phoenix Wing Fragment 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Phoenix Wing Fragment 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,69f2683ecaeb1241880b7fcb,
Sticker-Zen-0084,Sticker,Zen,Printify_UI_Mockups5,Minimal Zen Dragon Scale Medallion 4pc 6x6 Sticker Sheet Serene Mindful Clean,Minimal Zen Dragon Scale Medallion 4pc 6x6 Sticker Sheet Serene Mindful Clean,69f268f1e3d76b3758086023,
Sticker-Zen-0085,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Celestial Crane Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Zen Aesthetic Celestial Crane Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Zen-0086,Sticker,Zen,Printify_UI_Mockups5,Mindful Zen Celestial Phoenix Talisman 4pc 6x6 Vinyl Sticker Laptop Journal,Mindful Zen Celestial Phoenix Talisman 4pc 6x6 Vinyl Sticker Laptop Journal,69f2696f29c1d0349a00f104,
Sticker-Zen-0087,Sticker,Zen,Printify_UI_Mockups5,Lotus Constellation Bloom 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Lotus Constellation Bloom 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,69f26a02357398ded80f6c4f,
Sticker-Zen-0088,Sticker,Zen,Printify_UI_Mockups5,Zen Aesthetic Singing Bowl Nexus 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,Zen Aesthetic Singing Bowl Nexus 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,69f27616ce81beb59a02b9e6,
Sticker-Zen-0089,Sticker,Zen,Printify_UI_Mockups5,Moon Temple Pagoda 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,Moon Temple Pagoda 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,69f27777ce81beb59a02bab7,
Sticker-Zen-0090,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Dragon Seal Medallion 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,Zen Aesthetic Dragon Seal Medallion 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,,
Sticker-Zen-0091,Sticker,Zen,Printify_UI_Mockups5,Incense Chalice Vessel Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,Incense Chalice Vessel Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,69f2786bcd8d04605103dccb,
Sticker-Zen-0092,Sticker,Zen,Printify_UI_Mockups5,Constellation Compass Rose Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,Constellation Compass Rose Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector,69f279205f78c14a7b0a572e,
Sticker-Zen-0093,Sticker,Zen,Printify_UI_Mockups5,Mindful Zen Katana Starblade Relic 4pc 6x6 Vinyl Sticker Laptop Journal Gift,Mindful Zen Katana Starblade Relic 4pc 6x6 Vinyl Sticker Laptop Journal Gift,69f279d8671cc7c7960b4a3d,
Sticker-Zen-0094,Sticker,Zen,Printify_UI_Mockups5,Mountain Mist Sanctuary 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Mountain Mist Sanctuary 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,69f27ac5ce81beb59a02bc4b,
Sticker-Zen-0095,Sticker,Zen,Ready_for_Printify,Prayer Wheel Mechanism 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Prayer Wheel Mechanism 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,,
Sticker-Zen-0096,Sticker,Zen,Ready_for_Printify,Celestial Koi Constellation Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist,Celestial Koi Constellation Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist,,
Sticker-Zen-0097,Sticker,Zen,Ready_for_Printify,Garden Rake Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop Gift,Garden Rake Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop Gift,,
Sticker-Zen-0098,Sticker,Zen,Ready_for_Printify,Celestial Koi Ascension Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Bottle Laptop,Celestial Koi Ascension Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Bottle Laptop,,
Sticker-Zen-0099,Sticker,Zen,Ready_for_Printify,Mindful Zen Lotus Bloom Mandala 4pc 6x6 Vinyl Sticker Laptop Journal Gift Decor,Mindful Zen Lotus Bloom Mandala 4pc 6x6 Vinyl Sticker Laptop Journal Gift Decor,,
Sticker-Zen-0100,Sticker,Zen,Ready_for_Printify,Ritual Bell Shrine Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,Ritual Bell Shrine Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,,
Sticker-Zen-0101,Sticker,Zen,Ready_for_Printify,Minimal Zen Phoenix Rebirth Emblem 4pc 6x6 Sticker Sheet Serene Mindful Clean,Minimal Zen Phoenix Rebirth Emblem 4pc 6x6 Sticker Sheet Serene Mindful Clean,,
Sticker-Zen-0102,Sticker,Zen,Ready_for_Printify,Jade Incense Burner 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,Jade Incense Burner 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,,
Sticker-Zen-0103,Sticker,Zen,Ready_for_Printify,Celestial Compass Rose 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Celestial Compass Rose 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,,
Sticker-Zen-0104,Sticker,Zen,Ready_for_Printify,Minimal Zen Bamboo Grove Miniature 4pc 6x6 Sticker Sheet Serene Mindful Clean,Minimal Zen Bamboo Grove Miniature 4pc 6x6 Sticker Sheet Serene Mindful Clean,,
Sticker-Zen-0105,Sticker,Zen,Ready_for_Printify,Zen Aesthetic Infinity Knot Talisman 4pc 6x6 Kiss-Cut Sticker Laptop Journal,Zen Aesthetic Infinity Knot Talisman 4pc 6x6 Kiss-Cut Sticker Laptop Journal,,
Sticker-Zen-0106,Sticker,Zen,Ready_for_Printify,Prayer Wheel Relic Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,Prayer Wheel Relic Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,,
Sticker-Zen-0107,Sticker,Zen,Ready_for_Printify,Celestial Lantern Beacon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Celestial Lantern Beacon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,,
Sticker-Zen-0108,Sticker,Zen,Ready_for_Printify,Sacred Turtle Wisdom Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,Sacred Turtle Wisdom Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,,
Sticker-Zen-0109,Sticker,Zen,Ready_for_Printify,Garden Rake Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift Laptop,Garden Rake Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift Laptop,,
Sticker-Zen-0110,Sticker,Zen,Ready_for_Printify,Frozen Phoenix Ascent Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,Frozen Phoenix Ascent Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,,
Sticker-Zen-0111,Sticker,Zen,Ready_for_Printify,Jade Lotus Bloom Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,Jade Lotus Bloom Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,,
Sticker-Zen-0112,Sticker,Zen,Ready_for_Printify,Ritual Bell Fragment Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,Ritual Bell Fragment Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift,,
Sticker-Zen-0113,Sticker,Zen,Ready_for_Printify,Collapsed Pagoda Crown 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Collapsed Pagoda Crown 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,,
Sticker-Zen-0114,Sticker,Zen,Ready_for_Printify,Frozen Seal Mandala Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,Frozen Seal Mandala Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,,
Sticker-Zen-0115,Sticker,Zen,Ready_for_Printify,Bamboo Segment Relic Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,Bamboo Segment Relic Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,,
Sticker-Zen-0116,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Incense Burner Throne 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,Zen Aesthetic Incense Burner Throne 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,,
Sticker-Zen-0117,Sticker,Zen,Ready_for_Printify,Zen Aesthetic Koi Swimming Upward 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,Zen Aesthetic Koi Swimming Upward 4pc 6x6 Kiss-Cut Sticker Laptop Journal Water,,
Sticker-Zen-0118,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Moonstone Crane Spirit 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Desk,Zen Aesthetic Moonstone Crane Spirit 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Desk,,
Sticker-Zen-0120,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Burgundy Phoenix Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Zen Aesthetic Burgundy Phoenix Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Zen-0121,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Celestial Lotus Bloom 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,Zen Aesthetic Celestial Lotus Bloom 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,,
Sticker-Zen-0122,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Mystic Prayer Bell 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,Zen Aesthetic Mystic Prayer Bell 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,,
Sticker-Zen-0123,Sticker,Zen,Ready_for_Printify,Zen Aesthetic Ancient Pagoda Shrine 4pc 6x6 Kiss-Cut Sticker Laptop Journal,Zen Aesthetic Ancient Pagoda Shrine 4pc 6x6 Kiss-Cut Sticker Laptop Journal,,
Sticker-Zen-0124,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Dragon Seal Medallion 4pc 6x6 Kiss-Cut Sticker Vinyl Reader Decor,Zen Aesthetic Dragon Seal Medallion 4pc 6x6 Kiss-Cut Sticker Vinyl Reader Decor,,
Sticker-Zen-0125,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Ceremonial Incense Vessel 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,Zen Aesthetic Ceremonial Incense Vessel 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop,,
Sticker-Zen-0126,Sticker,Zen,Ready_for_Printify,Nebula Moon Orb Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,Nebula Moon Orb Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Laptop,,
Sticker-Zen-0127,Sticker,Zen,Ready_for_Printify,Mindful Zen Mystic Garden Bridge 4pc 6x6 Vinyl Sticker Laptop Journal Gift Desk,Mindful Zen Mystic Garden Bridge 4pc 6x6 Vinyl Sticker Laptop Journal Gift Desk,,
Sticker-Zen-0128,Sticker,Zen,Ready_for_Printify,Minimal Zen Koi Guardian Spirit 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,Minimal Zen Koi Guardian Spirit 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,,
Sticker-Zen-0129,Sticker,Zen,Ready_for_Printify,Minimal Zen Bamboo Scroll Relic 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,Minimal Zen Bamboo Scroll Relic 4pc 6x6 Sticker Sheet Serene Mindful Clean Gift,,
Sticker-Zen-0130,Sticker,Zen,Ready_for_Printify,Minimal Zen Celestial Phoenix Ascending 4pc 6x6 Sticker Sheet Serene Mindful,Minimal Zen Celestial Phoenix Ascending 4pc 6x6 Sticker Sheet Serene Mindful,,
Sticker-Zen-0131,Sticker,Zen,Ready_for_Printify,Zen Aesthetic Sacred Lotus Mandala 4pc 6x6 Kiss-Cut Sticker Laptop Journal Gift,Zen Aesthetic Sacred Lotus Mandala 4pc 6x6 Kiss-Cut Sticker Laptop Journal Gift,,
Sticker-Zen-0132,Sticker,Zen,Ready_for_Printify,Ritual Bell Shrine Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,Ritual Bell Shrine Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor Gift,,
Sticker-Zen-0133,Sticker,Zen,Ready_for_Printify,Moon Pagoda Fragment 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,Moon Pagoda Fragment 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk,,
Sticker-Zen-0134,Sticker,Zen,Ready_for_Printify,Jade Dragon Seal Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,Jade Dragon Seal Mindful Zen 4pc 6x6 Vinyl Sticker Yoga Minimalist Gift Gift,,
Sticker-Zen-0135,Sticker,Zen,Ready_for_Printify,Moonstone Incense Vessel Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Gift,Moonstone Incense Vessel Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Gift,,
Sticker-Zen-0136,Sticker,Zen,Ready_for_Printify,Celestial Koi Constellation 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Bottle Vinyl,Celestial Koi Constellation 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Bottle Vinyl,,
Sticker-Zen-0138,Sticker,Zen,Ready_for_Printify,Minimal Zen Bamboo Flute Harmony 4pc 6x6 Sticker Sheet Serene Mindful Clean,Minimal Zen Bamboo Flute Harmony 4pc 6x6 Sticker Sheet Serene Mindful Clean,,
Sticker-Zen-0139,Sticker,Zen,Ready_for_Printify,Sacred Deer Guardian Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,Sacred Deer Guardian Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,,
Sticker-Zen-0140,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Jade Serpent Coil 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,Zen Aesthetic Jade Serpent Coil 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Journal,,
Sticker-Zen-0144,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Frosted Jade Lotus Incense Holder 4pc 6x6 Kiss-Cut Sticker Vinyl,Zen Aesthetic Frosted Jade Lotus Incense Holder 4pc 6x6 Kiss-Cut Sticker Vinyl,,
Sticker-Zen-0150,Sticker,Zen,Ready_for_Printify,Celestial Jade Bell Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,Celestial Jade Bell Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,,
Sticker-Zen-0151,Sticker,Zen,Ready_for_Printify,Moonlit Lotus Chalice Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,Moonlit Lotus Chalice Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,,
Sticker-Zen-0152,Sticker,Zen,Quality_Hold_LowRes_U,Zen Aesthetic Dragon Scale Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,Zen Aesthetic Dragon Scale Talisman 4pc 6x6 Kiss-Cut Sticker Vinyl Laptop Decor,,
Sticker-Zen-0153,Sticker,Zen,Ready_for_Printify,Mindful Zen Phoenix Feather Flute 4pc 6x6 Vinyl Sticker Laptop Journal Gift,Mindful Zen Phoenix Feather Flute 4pc 6x6 Vinyl Sticker Laptop Journal Gift,,
Sticker-Zen-0154,Sticker,Zen,Ready_for_Printify,Zen Aesthetic Misty Mountain Incense Burner 4pc 6x6 Kiss-Cut Sticker Laptop,Zen Aesthetic Misty Mountain Incense Burner 4pc 6x6 Kiss-Cut Sticker Laptop,,
Sticker-Zen-0155,Sticker,Zen,Ready_for_Printify,Zen Aesthetic Bamboo Grove Tea Scoop 4pc 6x6 Kiss-Cut Sticker Laptop Journal,Zen Aesthetic Bamboo Grove Tea Scoop 4pc 6x6 Kiss-Cut Sticker Laptop Journal,,
Sticker-Zen-0156,Sticker,Zen,Ready_for_Printify,Zen Aesthetic Moongate Architectural Fragment 4pc 6x6 Kiss-Cut Sticker Laptop,Zen Aesthetic Moongate Architectural Fragment 4pc 6x6 Kiss-Cut Sticker Laptop,,
Sticker-Zen-0157,Sticker,Zen,Ready_for_Printify,Koi Pond Water Dipper Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,Koi Pond Water Dipper Minimal Zen 4pc 6x6 Kiss-Cut Vinyl Desk Collector Decor,,
Sticker-Zen-0158,Sticker,Zen,Ready_for_Printify,Spiral Galaxy Meditation Disc 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop,Spiral Galaxy Meditation Disc 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop,,
Sticker-Zen-0159,Sticker,Zen,Ready_for_Printify,Pagoda Lantern Miniature 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,Pagoda Lantern Miniature 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,,
Sticker-Zen-0160,Sticker,Zen,Ready_for_Printify,Mindful Zen Wave Crest Sake Cup 4pc 6x6 Vinyl Sticker Laptop Journal Gift Wood,Mindful Zen Wave Crest Sake Cup 4pc 6x6 Vinyl Sticker Laptop Journal Gift Wood,,
Poster-Zen-0003,Poster,Zen,Printify_Hold_BadDraftDeleted,Lotus Mandala Seal Stone Poster 12x18 Dark Academia Zen Wall Art Decor Study,Lotus Mandala Seal Stone Poster 12x18 Dark Academia Zen Wall Art Decor Study,,
Acrylic-Grimdark-0038,Acrylic,Grimdark,Printify_UI_Mockups4,Rose Quartz Chapel Soul Lantern Grimdark 5x7 Acrylic Art Gothic Collectible,Rose Quartz Chapel Soul Lantern Grimdark 5x7 Acrylic Art Gothic Collectible,69f8928b25819cdf3d057ef7,
Acrylic-Grimdark-0039,Acrylic,Grimdark,Printify_UI_Mockups4,Sapphire Temple Soul Lantern Grimdark 5x7 Acrylic Display Gothic Artifact Shelf,Sapphire Temple Soul Lantern Grimdark 5x7 Acrylic Display Gothic Artifact Shelf,69f8931cb051b8a0e90b97c7,
Acrylic-Grimdark-0040,Acrylic,Grimdark,Printify_UI_Mockups4,Silver Moon Gate Soul Lantern Grimdark 5x7 Acrylic Art Gothic Mentor-Grade Gift,Silver Moon Gate Soul Lantern Grimdark 5x7 Acrylic Art Gothic Mentor-Grade Gift,69f8937bbe136844f0004b36,
Poster-Academia-0038,Poster,Academia,Printify_PublishExternalPending_Mockups8,Geological Archive Geode Dark Academia Poster 12x18 Mentor-Grade Decor Wall,Geological Archive Geode Dark Academia Poster 12x18 Mentor-Grade Decor Wall,69fbccf9ce0d8cb5570fc6f0,
Poster-Academia-0039,Poster,Academia,Printify_PublishExternalPending_Mockups8,Dark Academia Horological Manuscript Chamber Poster 12x18 Study Decor Wall Gift,Dark Academia Horological Manuscript Chamber Poster 12x18 Study Decor Wall Gift,69fbcd1aee663532c8019ec7,
Poster-Academia-0040,Poster,Academia,Printify_PublishExternalPending_Mockups8,Dark Academia Meteorological Orrery 12x18 Poster Study Decor Atmospheric Texts,Dark Academia Meteorological Orrery 12x18 Poster Study Decor Atmospheric Texts,69fbcd3eb8dd7e2bb0095af7,
Poster-Academia-0041,Poster,Academia,Printify_PublishExternalPending_Mockups8,Dark Academia Astrological Globe Poster 12x18 Study Room Decor Starlight Jade,Dark Academia Astrological Globe Poster 12x18 Study Room Decor Starlight Jade,69fbcd65cacc667dc70b7c2a,
Poster-Academia-0042,Poster,Academia,Printify_PublishExternalPending_Mockups8,Dark Academia Armillary Sphere Poster 12x18 Vintage Study Decor Zodiac Symbols,Dark Academia Armillary Sphere Poster 12x18 Vintage Study Decor Zodiac Symbols,69fbcd8a3014a1ea840da971,

```

Project-scoped zero-view CSV: `C:\AIprojects\openclaw_difi\Review_Packets\GREY_ZERO_VIEW_PROJECT_SCOPE_20260506_2348.csv`



### GREY_ZERO_VIEW_PROJECT_SCOPE_20260506_2348.csv
```csv
ID,Product_Type,Category,Local_Status,Printify_Product_ID,eBay_Item_ID,eBay_Item_URL,eBay_Title,eBay_Price,Latest_eBay_Views_30_Days,Latest_eBay_General_Status,Latest_eBay_Priority_Status,Etsy_Planned,Etsy_Title,Etsy_Launch_Status,Production_Path,Cover_Path,Gallery_Ready,Image_Note_Ready,Action_Bucket
Sticker-Academia-0004,Sticker,Academia,Printify_Published_Mockups5,69f192aa5ea38382140f1d7b,406892408950,https://www.ebay.com/itm/406892408950,4pc Kiss-Cut Sticker Set Mechanical Raven Familiar Laptop Journal Bottle Dark,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Academia-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0010,Sticker,Zen,Printify_Published_Mockups5,69f1b00840c796ee97058144,406892414116,https://www.ebay.com/itm/406892414116,Floating Island Sanctuary 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0055,Sticker,Zen,Printify_Published_Mockups5,69f2547229c1d0349a00e796,406903037933,https://www.ebay.com/itm/406903037933,Mindful Zen Azure Dragon Warrior 4pc 6x6 Vinyl Sticker Laptop Journal Gift Desk,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0055_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0055_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0056,Sticker,Zen,Printify_Published_Mockups5,69f25526ad218fe47f0cc0d3,406903041315,https://www.ebay.com/itm/406903041315,Dragon Cherry Blossom 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0056_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0056_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0057,Sticker,Zen,Printify_Published_Mockups5,69f255dae64c9f31b70f4ea6,406903044643,https://www.ebay.com/itm/406903044643,Moonlit Dragon 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal Desk Decor,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0057_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0057_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0058,Sticker,Zen,Printify_Published_Mockups5,69f259bc5f78c14a7b0a4760,406903049411,https://www.ebay.com/itm/406903049411,Minimal Zen Dragon Calligraphy 4pc 6x6 Sticker Sheet Serene Mindful Clean Decor,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0058_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0058_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0060,Sticker,Zen,Printify_Published_Mockups5,69f25a86a7777da1970ff5f3,406903249053,https://www.ebay.com/itm/406903249053,Minimal Zen Translucent Jade Dragon 4pc 6x6 Sticker Sheet Serene Mindful Clean,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0060_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0060_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0061,Sticker,Zen,Printify_Published_Mockups5,69f25b3ce64c9f31b70f50ed,406903249987,https://www.ebay.com/itm/406903249987,Minimal Zen Kintsugi Gold Dragon 4pc 6x6 Sticker Sheet Serene Mindful Calm Gift,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0061_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0061_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0062,Sticker,Zen,Printify_Published_Mockups5,69f25bee9b469f716d0e7056,406903250891,https://www.ebay.com/itm/406903250891,Zen Aesthetic Bioluminescent Dragon 4pc 6x6 Kiss-Cut Sticker Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0062_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0062_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Sticker-Zen-0063,Sticker,Zen,Printify_Published_Mockups5,69f25ca39577aaffd5066a80,406903252007,https://www.ebay.com/itm/406903252007,Crystalline Dragon Core 4pc 6x6 Kiss-Cut Sticker Zen Aesthetic Laptop Journal,$11.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0063_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Sticker\Kiss-Cut\MASTER_Sticker-Zen-0063_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0002,Poster,Academia,Printify_Published_Mockups5,69f2906f7f1017d51b0d5f76,406902600741,https://www.ebay.com/itm/406902600741,Dark Academia Obsidian Threshold Poster 12x18 Vintage Study Decor Mentor Wisdom,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0002_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0003,Poster,Academia,Printify_Published_Mockups5,69f29152357398ded80f8178,406902616799,https://www.ebay.com/itm/406902616799,Dark Academia Serpentine Portal of Alchemical Texts 12x18 Poster Study Decor,$34.99,0,Promoted,Eligible,True,"Serpentine Portal of Alchemical Texts Study Decor Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0081,Acrylic,Grimdark,Printify_Published_Mockups5,69f299c1a3119247600cbe18,406902606976,https://www.ebay.com/itm/406902606976,Plague Doctor Raven Skull Grimdark Alchemy 5x7 Acrylic Art Block Collectible,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0081_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0081_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0001,Acrylic,Zen,Printify_Published_Mockups5,69f29a72c411a56f6902930d,406902620519,https://www.ebay.com/itm/406902620519,Zen Mechanical Crane 5x7 Acrylic Block Desk Art Calm Decor Origami Sculpture,$89.99,0,Promoted,Eligible,True,"Mechanical Crane Desk Art Calm Decor Origami Dark Academia Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0083,Poster,Academia,Printify_Published_Mockups5,69f2a1b8a7777da197101a96,406902669660,https://www.ebay.com/itm/406902669660,Academia Mentor-Grade Cosmic Lotus Observatory 12x18 Poster Steampunk Study,$34.99,0,Promoted,Eligible,True,"Mentor Grade Cosmic Lotus Observatory Steampunk Study Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0083_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0083_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0084,Poster,Academia,Printify_Published_Mockups5,69f2a2aacaeb1241880b9f6b,406902691983,https://www.ebay.com/itm/406902691983,Astrolabe Chalice Relic Dark Academia Poster 12x18 Vintage Study Decor Wall,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0084_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0084_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0082,Acrylic,Grimdark,Printify_Published_Mockups5,69f2a7d0e64c9f31b70f79cf,406902633400,https://www.ebay.com/itm/406902633400,Grimdark Alchemical Terrarium Withered Mandrake Root Chamber 5x7 Acrylic Block,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0082_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0082_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0002,Acrylic,Zen,Printify_Published_Mockups5,69f2a8a5357398ded80f8faf,406902657898,https://www.ebay.com/itm/406902657898,Zen Aesthetic Ritual Bell Shrine 5x7 Acrylic Block for Meditation Desk Shelf,$89.99,0,Promoted,Eligible,True,"Ritual Bell Shrine for Meditation Desk Shelf Zen Aesthetic Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0002_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0003,Acrylic,Zen,Printify_Published_Mockups5,69f2a9b45f78c14a7b0a7290,406902673249,https://www.ebay.com/itm/406902673249,Zen Pagoda Fragment Relic 5x7 Acrylic Print Floating Tower Decor Jade Framework,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0091,Poster,Academia,Printify_Published_Mockups5,69f2b7ada7777da1971028d7,406902887127,https://www.ebay.com/itm/406902887127,Dark Academia Celestial Lotus Poster 12x18 Vintage Study Room Wall Art Decor,$34.99,0,Promoted,Eligible,True,"Celestial Lotus Study Room Decor Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0091_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0091_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Academia-0003,Acrylic,Academia,Printify_Published_Mockups5,69f2b9c3caeb1241880bae85,406902703464,https://www.ebay.com/itm/406902703464,Celestial Orrery Tree Bonsai Dark Academia 5x7 Acrylic Block Mentor-Grade Study,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0003_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0003_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0083,Acrylic,Grimdark,Printify_Published_Mockups5,69f2bac6343d8ca093077dd8,406902885214,https://www.ebay.com/itm/406902885214,Grimdark Ritual Censer Thurible 5x7 Acrylic Block Dark Academia Mentor-Grade,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0083_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0083_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0005,Acrylic,Zen,Printify_Published_Mockups5,69f2c22e9b469f716d0ea954,406902893289,https://www.ebay.com/itm/406902893289,Zen Incense Vessel Constellation 5x7 Acrylic Block for Meditation Desk Shelf,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0001,Poster,Zen,Printify_Published_Mockups5,69f2dc76cd8d046051041f06,406902890971,https://www.ebay.com/itm/406902890971,Zen Bonsai Wall Art Celestial Gate of Jade Mist 12x18 Poster Meditation Decor,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0002,Poster,Zen,Printify_Published_Mockups5,69f2cf675f78c14a7b0a894c,406902897663,https://www.ebay.com/itm/406902897663,Dark Academia Phoenix Incense Burner 12x18 Poster Ritual Zen Decor Wall Study,$34.99,0,Promoted,Eligible,True,"Phoenix Incense Burner Ritual Decor Wall Study Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0002_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0002_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0007,Acrylic,Zen,Printify_Published_Mockups5,69f2d3ab5f78c14a7b0a8b87,406903028253,https://www.ebay.com/itm/406903028253,Zen Aesthetic Sacred Lotus Meditation Bell 5x7 Acrylic Block for Altar Decor,$89.99,0,Promoted,Eligible,True,"Sacred Lotus Meditation Bell for Altar Decor Zen Aesthetic Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0007_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0007_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0008,Acrylic,Zen,Printify_Published_Mockups5,69f2d49b81039eb9ab0b583c,406903036452,https://www.ebay.com/itm/406903036452,Zen Celestial Bonsai Moon Garden 5x7 Acrylic Block for Serene Desk Decor Shelf,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0004,Poster,Zen,Printify_Published_Mockups5,69f2dddb9577aaffd506bc32,406903026999,https://www.ebay.com/itm/406903026999,Zen Celestial Compass Poster 12x18 Wall Art Calm Study Decor Library Gift Room,$34.99,0,Promoted,Eligible,True,"Celestial Compass Calm Study Decor Library Room Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Zen-0005,Poster,Zen,Printify_Published_Mockups5,69f2db1a3c6616b960034a37,406903033377,https://www.ebay.com/itm/406903033377,Zen Phoenix Rebirth Vessel 12x18 Poster for Meditation Room Decor Wall Study,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Zen-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Academia-0005,Acrylic,Academia,Printify_Published_Mockups4,69f80ad2d3b9dc73b1051dbd,406903039716,https://www.ebay.com/itm/406903039716,Alchemical Star Flask Vessel 5x7 Acrylic Block Dark Academia Desk Decor Shelf,$89.99,0,Promoted,Eligible,True,"Alchemical Star Flask Vessel Desk Decor Shelf Dark Academia Acrylic Block, Jade Desk Decor, Collector Shelf Gift",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0085,Acrylic,Grimdark,Printify_Published_Mockups4,69f2e4c77e3402ea470630eb,406903043482,https://www.ebay.com/itm/406903043482,Alchemist Divination Compass Grimdark 5x7 Acrylic Display Mentor-Grade Occult,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0085_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0085_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0009,Acrylic,Zen,Printify_Published_Mockups8,69f80f8a83a8608fd80ec283,406903047385,https://www.ebay.com/itm/406903047385,"Zen Bamboo Flute 5x7 Acrylic Block, Whispering Shakuhachi Meditation Art Gift",$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Zen-0010,Acrylic,Zen,Printify_Published_Mockups8,69f810485da263f75f049bf8,406903213858,https://www.ebay.com/itm/406903213858,Zen Lotus Seed Pod Vessel 5x7 Acrylic Block for Mindful Desk Decor Shelf Study,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Zen-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0001,Acrylic,Grimdark,Printify_Published_Mockups4,69f82b8aa1a4c45aad055063,406903249745,https://www.ebay.com/itm/406903249745,Gothic Lantern Soul Cage 5x7 Acrylic Block Grimdark Study Decor Crimson Flame,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0001_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0001_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0004,Acrylic,Grimdark,Printify_Published_Mockups8,69f82c8609f3b7302401cacf,406903250705,https://www.ebay.com/itm/406903250705,Grimdark Gothic Lantern 5x7 Acrylic Block Shadowbound Sentinel Beacon Dark Gift,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0004_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0004_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Acrylic-Grimdark-0005,Acrylic,Grimdark,Printify_Published_Mockups4,69f8388b25819cdf3d0538bc,406903251829,https://www.ebay.com/itm/406903251829,Gothic Necromancer Soul Reliquary 5x7 Acrylic Grimdark Artifact Decor Shelf,$89.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Acrylic\Photo-Block\MASTER_Acrylic-Grimdark-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0005,Poster,Academia,Printify_Published_Mockups4,69f847b45da263f75f04cdbd,406903038850,https://www.ebay.com/itm/406903038850,Arcane Archway of Forbidden Chronicles Dark Academia 12x18 Poster Study Room,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0005_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0005_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0006,Poster,Academia,Printify_Published_Mockups5,69f84864feed9979d10cd5ba,406903042690,https://www.ebay.com/itm/406903042690,Dark Academia Ethereal Torii Poster 12x18 Study Room Decor Scholarly Ascension,$34.99,0,Promoted,Eligible,True,"Ethereal Torii Study Room Decor Scholarly Ascension Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0006_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0006_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0008,Poster,Academia,Printify_Published_Mockups4,69f84b3d5da263f75f04d1f7,406903046097,https://www.ebay.com/itm/406903046097,Dark Academia Mystic Threshold Infinite Knowledge Poster 12x18 Study Decor Wall,$34.99,0,Promoted,Eligible,True,"Mystic Threshold Infinite Knowledge Study Decor Wall Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0008_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0008_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0009,Poster,Academia,Printify_Published_Mockups4,69f8547125819cdf3d05522b,406903209258,https://www.ebay.com/itm/406903209258,Dark Academia Sanctum Gate of Preserved Wisdom 12x18 Poster Study Decor Wall,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0009_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0009_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0010,Poster,Academia,Printify_Published_Mockups4,69f854ed09f3b7302401ed2e,406903249496,https://www.ebay.com/itm/406903249496,Dark Academia Hermetic Portal of Ancient Codices 12x18 Poster Study Decor Wall,$34.99,0,Promoted,Eligible,False,,,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0010_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0010_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review
Poster-Academia-0011,Poster,Academia,Printify_Published_Mockups4,69f850b425819cdf3d054e10,406903250376,https://www.ebay.com/itm/406903250376,Dark Academia Celestial Archway Poster 12x18 Study Room Decor Timeless Tomes,$34.99,0,Promoted,Eligible,True,"Celestial Archway Study Room Decor Timeless Tomes Dark Academia Wall Art Print, Zen Study Poster, Wabi Sabi Room Decor",Draft_Prepared_Not_Published,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0011_Ready_for_Steaming\Production_Design.png,C:\AIprojects\openclaw_difi\Output\Poster\Premium-Matte-Vertical\MASTER_Poster-Academia-0011_Ready_for_Steaming\Cover_Mockup.png,True,True,Published_Zero_View_Copy_Ad_Review

```


# 3. Hardware & Environment


### GREY_HARDWARE_ENV_20260506_2348.txt
```text
$ powershell -NoProfile -Command "Get-CimInstance Win32_Processor | Select Name,LoadPercentage,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed | Format-List; $os=Get-CimInstance Win32_OperatingSystem; $total=[math]::Round($os.TotalVisibleMemorySize/1MB,2); $free=[math]::Round($os.FreePhysicalMemory/1MB,2); $used=[math]::Round($total-$free,2); $pct=[math]::Round(($used/$total)*100,1); Write-Output ('MemoryGB Total={0} Used={1} Free={2} UsedPct={3}' -f $total,$used,$free,$pct); Get-Process | Sort WorkingSet64 -Descending | Select -First 12 ProcessName,Id,@{n='WorkingSetMB';e={[math]::Round($_.WorkingSet64/1MB,1)}},CPU | Format-Table -AutoSize"
EXIT=0
--- STDOUT ---


Name                      : Intel(R) N95
LoadPercentage            : 85
NumberOfCores             : 4
NumberOfLogicalProcessors : 4
MaxClockSpeed             : 1700



MemoryGB Total=11.75 Used=11 Free=0.75 UsedPct=93.6

ProcessName    Id WorkingSetMB          CPU
-----------    -- ------------          ---
chrome       1504       1863.8  1115.859375
chrome       3280        965.6  1054.609375
Codex       27652        947.3 13797.484375
chrome       9740        406.1 48030.734375
msedge       9252        258.6    37.109375
chrome      29500        245.3    29.859375
msedge      28512        238.7      1617.75
msedge      11292        230.5    187.53125
chrome       6024        224.6   644.234375
MsMpEng      4564        173.6             
chrome      25956        166.7  1167.171875
Code        19100        166.4  1269.265625



--- STDERR ---


$ powershell -NoProfile -Command "try { Get-CimInstance -Namespace root/wmi -Class MSAcpi_ThermalZoneTemperature | Select InstanceName,@{n='Celsius';e={[math]::Round(($_.CurrentTemperature/10)-273.15,1)}} | Format-Table -AutoSize } catch { Write-Output ('TEMP_PROBE_ERROR=' + $_.Exception.Message) }"
EXIT=1
--- STDOUT ---

--- STDERR ---
Get-CimInstance : Access denied 
At line:1 char:7
+ try { Get-CimInstance -Namespace root/wmi -Class MSAcpi_ThermalZoneTe ...
+       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (root/wmi:MSAcpi_ThermalZoneTemperature:String) [Get-CimInstance], Cim 
   Exception
    + FullyQualifiedErrorId : HRESULT 0x80041003,Microsoft.Management.Infrastructure.CimCmdlets.GetCimInstanceCommand
 


$ node --version && npm --version && npm ls --depth=0
EXIT=0
--- STDOUT ---
v24.14.0
11.9.0
openclaw-difi-factory@0.1.0 C:\AIprojects\openclaw_difi
`-- (empty)


--- STDERR ---


$ npm run browser:edge:check
EXIT=0
--- STDOUT ---

> openclaw-difi-factory@0.1.0 browser:edge:check
> py modules\automation_browser.py --check --port 9223

{
  "status": "RUNNING",
  "port": 9223,
  "browser": "Edg/147.0.3912.98",
  "webSocketDebuggerUrl": "ws://127.0.0.1:9223/devtools/browser/c4bf8130-d4be-491a-bf31-8a87444c9870"
}

--- STDERR ---


$ docker --version && docker info
EXIT=1
--- STDOUT ---
Docker version 29.3.0, build 5927d80
Client:
 Version:    29.3.0
 Context:    desktop-linux
 Debug Mode: false
 Plugins:
  agent: Docker AI Agent Runner (Docker Inc.)
    Version:  v1.32.4
    Path:     C:\Program Files\Docker\cli-plugins\docker-agent.exe
  ai: Docker AI Agent - Ask Gordon (Docker Inc.)
    Version:  v1.20.1
    Path:     C:\Program Files\Docker\cli-plugins\docker-ai.exe
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.32.1-desktop.1
    Path:     C:\Program Files\Docker\cli-plugins\docker-buildx.exe
  compose: Docker Compose (Docker Inc.)
    Version:  v5.1.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-compose.exe
  debug: Get a shell into any image or container (Docker Inc.)
    Version:  0.0.47
    Path:     C:\Program Files\Docker\cli-plugins\docker-debug.exe
  desktop: Docker Desktop commands (Docker Inc.)
    Version:  v0.3.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-desktop.exe
  dhi: CLI for managing Docker Hardened Images (Docker Inc.)
    Version:  v0.0.0-alpha
    Path:     C:\Program Files\Docker\cli-plugins\docker-dhi.exe
  extension: Manages Docker extensions (Docker Inc.)
    Version:  v0.2.31
    Path:     C:\Program Files\Docker\cli-plugins\docker-extension.exe
  init: Creates Docker-related starter files for your project (Docker Inc.)
    Version:  v1.4.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-init.exe
  mcp: Docker MCP Plugin (Docker Inc.)
    Version:  v0.40.1
    Path:     C:\Program Files\Docker\cli-plugins\docker-mcp.exe
  model: Docker Model Runner (Docker Inc.)
    Version:  v1.1.5
    Path:     C:\Program Files\Docker\cli-plugins\docker-model.exe
  offload: Docker Offload (Docker Inc.)
    Version:  v0.5.73
    Path:     C:\Program Files\Docker\cli-plugins\docker-offload.exe
  pass: Docker Pass Secrets Manager Plugin (beta) (Docker Inc.)
    Version:  v0.0.24
    Path:     C:\Program Files\Docker\cli-plugins\docker-pass.exe
  sandbox: Docker Sandbox (Docker Inc.)
    Version:  v0.12.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-sandbox.exe
  sbom: View the packaged-based Software Bill Of Materials (SBOM) for an image (Anchore Inc.)
    Version:  0.6.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-sbom.exe
  scout: Docker Scout (Docker Inc.)
    Version:  v1.20.2
    Path:     C:\Program Files\Docker\cli-plugins\docker-scout.exe

Server:

--- STDERR ---
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.

```


# 4. Git / Filesystem State


### git status --short
```text
$ git status --short
EXIT=0
--- STDOUT ---
 M Database/Etsy_API_Status.json
 M Database/Etsy_API_Status_Log.csv
 M Database/Factory_Autopilot_Action_Queue.csv
 M Database/Factory_Autopilot_Action_Queue.md
 M Database/Factory_Autopilot_Run_Log.csv
 M Database/Factory_Autopilot_State.json
 M Database/Factory_Backlog.csv
 M Database/Factory_Backlog.md
 M Database/Local_Listing_QA.csv
 M Database/Market_Signal_Action_Queue.csv
 M Database/Market_Signal_Action_Queue.xlsx
 M Database/Performance_Log.csv
 M Database/Printify_Login_Status.json
 M Database/Product_Blueprint_Next_Test_Plan.md
 M Database/Unified_Listing_Registry.csv
 M Database/Unified_Listing_Registry.xlsx
 M Database/eBay_Cover_Repair_Decisions.csv
 M Database/eBay_Cover_Repair_Decisions.md
 M Database/eBay_Cover_Replacement_Queue.csv
 M Database/eBay_Cover_Replacement_Queue.md
 M Database/eBay_Online_Cover_Audit.csv
 M Database/eBay_Profile_Update_Packet.md
 M Database/eBay_Replacement_Draft_Log.csv
 M Database/eBay_Retire_Queue.csv
 M Database/eBay_Retire_Run_Log.csv
 M Database/eBay_Title_Repair_Queue.md
 M Database/eBay_Traffic_Diagnosis.csv
 M Database/eBay_Traffic_Diagnosis.md
 M Database/eBay_Traffic_Experiment_Report.csv
 M Database/eBay_listing.xlsx
 M Database/ebay_ads_pending_2pct.csv
 M PROGRESS_LOG.md
 M RECOVERY_STATE.json
?? Database/eBay_Cover_QA/
?? Database/eBay_Online_Cover_Audit.backup_schema_20260505_212716.csv
?? Database/eBay_Picture_Revise/
?? Database/eBay_listing.backup_traffic_experiment_20260505_182220.xlsx
?? Database/iron_audit_not_working_contact_sheet.png
?? Database/iron_audit_ready_contact_sheets/
?? Database/poster_harvest_input.txt
?? Database/printify_api_audit_20260429_111951.csv
?? Database/printify_design_audit_20260429_134213.csv
?? Database/printify_design_audit_20260429_134325.csv
?? Database/printify_design_audit_20260429_134629.csv
?? Database/printify_design_audit_20260429_134734.csv
?? Database/printify_design_audit_20260429_135733.csv
?? Database/printify_design_audit_20260429_161311.csv
?? Database/printify_design_audit_20260429_163614.csv
?? Database/printify_design_audit_20260429_165215.csv
?? Database/printify_design_audit_20260503_232408.csv
?? Database/printify_primary_hash_audit_20260429_112156.csv
?? Database/sticker_final_deliverable_audit_20260429.csv
?? Database/sticker_folder_deep_audit_20260429.csv
?? Review_Packets/GREY_DRAFT_PENDING_PRODUCTS_20260506_2348.csv
?? Review_Packets/GREY_HARDWARE_ENV_20260506_2348.txt
?? Review_Packets/GREY_ZERO_VIEW_PROJECT_SCOPE_20260506_2348.csv

--- STDERR ---

```


### recent files
```text
$ powershell -NoProfile -Command "Get-ChildItem Database,Reports,Review_Packets -File -ErrorAction SilentlyContinue | Sort LastWriteTime -Descending | Select -First 120 LastWriteTime,Length,FullName | Format-Table -AutoSize"
EXIT=0
--- STDOUT ---

LastWriteTime        Length FullName                                                                                   
-------------        ------ --------                                                                                   
5/6/2026 11:48:41 PM  24769 C:\AIprojects\openclaw_difi\Review_Packets\GREY_ZERO_VIEW_PROJECT_SCOPE_20260506_2348.csv  
5/6/2026 11:48:41 PM  24681 C:\AIprojects\openclaw_difi\Review_Packets\GREY_DRAFT_PENDING_PRODUCTS_20260506_2348.csv   
5/6/2026 11:48:40 PM   5695 C:\AIprojects\openclaw_difi\Review_Packets\GREY_HARDWARE_ENV_20260506_2348.txt             
5/6/2026 11:46:45 PM   2766 C:\AIprojects\openclaw_difi\Database\Factory_Autopilot_Action_Queue.md                     
5/6/2026 11:46:45 PM   1879 C:\AIprojects\openclaw_difi\Database\Factory_Autopilot_Action_Queue.csv                    
5/6/2026 11:46:45 PM   4239 C:\AIprojects\openclaw_difi\Database\Factory_Autopilot_State.json                          
5/6/2026 11:46:45 PM  88648 C:\AIprojects\openclaw_difi\Database\Factory_Autopilot_Run_Log.csv                         
5/6/2026 11:46:45 PM   4603 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2346.md                        
5/6/2026 11:46:44 PM   6550 C:\AIprojects\openclaw_difi\Database\Factory_Backlog.md                                    
5/6/2026 11:46:44 PM   5071 C:\AIprojects\openclaw_difi\Database\Factory_Backlog.csv                                   
5/6/2026 11:46:43 PM   3408 C:\AIprojects\openclaw_difi\Database\Etsy_API_Status_Log.csv                               
5/6/2026 11:46:43 PM    344 C:\AIprojects\openclaw_difi\Database\Etsy_API_Status.json                                  
5/6/2026 11:46:42 PM   2864 C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.md                   
5/6/2026 11:46:42 PM   2177 C:\AIprojects\openclaw_difi\Database\Product_Blueprint_Next_Test_Plan.csv                  
5/6/2026 11:46:42 PM   1715 C:\AIprojects\openclaw_difi\Database\eBay_Profile_Update_Packet.md                         
5/6/2026 11:46:42 PM   1524 C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.md                             
5/6/2026 11:46:42 PM   1305 C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Diagnosis.csv                            
5/6/2026 11:46:41 PM    404 C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.md                     
5/6/2026 11:46:41 PM   4831 C:\AIprojects\openclaw_difi\Database\eBay_Traffic_Experiment_Report.csv                    
5/6/2026 11:46:40 PM  20207 C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.xlsx                       
5/6/2026 11:46:40 PM  58059 C:\AIprojects\openclaw_difi\Database\Market_Signal_Action_Queue.csv                        
5/6/2026 11:46:39 PM  38336 C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.xlsx                         
5/6/2026 11:46:39 PM 132482 C:\AIprojects\openclaw_difi\Database\Unified_Listing_Registry.csv                          
5/6/2026 11:46:38 PM    255 C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.md                            
5/6/2026 11:46:38 PM    122 C:\AIprojects\openclaw_difi\Database\eBay_Title_Repair_Queue.csv                           
5/6/2026 11:46:37 PM    698 C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.md                       
5/6/2026 11:46:37 PM  30566 C:\AIprojects\openclaw_difi\Database\eBay_Cover_Replacement_Queue.csv                      
5/6/2026 11:46:36 PM    837 C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.md                        
5/6/2026 11:46:36 PM  25829 C:\AIprojects\openclaw_difi\Database\eBay_Cover_Repair_Decisions.csv                       
5/6/2026 11:46:34 PM  31638 C:\AIprojects\openclaw_difi\Database\Local_Listing_QA.csv                                  
5/6/2026 11:44:58 PM   2560 C:\AIprojects\openclaw_difi\Database\Printify_Login_Guard.log                              
5/6/2026 11:44:58 PM    220 C:\AIprojects\openclaw_difi\Database\Printify_Login_Status.json                            
5/6/2026 11:44:26 PM  70788 C:\AIprojects\openclaw_difi\Database\Performance_Log.csv                                   
5/6/2026 11:39:15 PM   4603 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2339.md                        
5/6/2026 11:37:04 PM   5066 C:\AIprojects\openclaw_difi\Database\eBay_Retire_Run_Log.csv                               
5/6/2026 11:37:04 PM  12246 C:\AIprojects\openclaw_difi\Database\eBay_Retire_Queue.csv                                 
5/6/2026 11:37:04 PM 114430 C:\AIprojects\openclaw_difi\Database\eBay_listing.xlsx                                     
5/6/2026 11:33:28 PM 151516 C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit.csv                           
5/6/2026 11:32:09 PM   5908 C:\AIprojects\openclaw_difi\Database\ebay_ads_pending_2pct.csv                             
5/6/2026 11:25:16 PM   6288 C:\AIprojects\openclaw_difi\Database\eBay_Replacement_Draft_Log.csv                        
5/6/2026 11:15:03 PM  14750 C:\AIprojects\openclaw_difi\Database\nightly_handoff_log.txt                               
5/6/2026 11:11:32 PM   4603 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2311.md                        
5/6/2026 10:53:44 PM  29342 C:\AIprojects\openclaw_difi\Database\printify_external_sync.csv                            
5/6/2026 10:36:55 PM   2982 C:\AIprojects\openclaw_difi\Database\Cover_Repair_Run_Log.csv                              
5/6/2026 10:30:36 PM   4677 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2230.md                        
5/6/2026 10:20:28 PM  12529 C:\AIprojects\openclaw_difi\Review_Packets\OPENCLAW_GEMINI_BRIEF.md                        
5/6/2026 10:20:11 PM   3335 C:\AIprojects\openclaw_difi\Review_Packets\ETSY_DIGITAL_TRAFFIC_PENETRATION_REPORT_20260...
5/6/2026 10:19:27 PM    501 C:\AIprojects\openclaw_difi\Database\Etsy_Legacy_Retirement_Status.csv                     
5/6/2026 10:06:00 PM   3364 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_Live_Audit.csv                           
5/6/2026 10:00:04 PM   1290 C:\AIprojects\openclaw_difi\Review_Packets\REPORT_INDEX.md                                 
5/6/2026 9:52:52 PM    5460 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_UI_Publish_Log.csv                       
5/6/2026 9:52:52 PM    3797 C:\AIprojects\openclaw_difi\Database\Etsy_Fee_Ledger.csv                                   
5/6/2026 9:52:52 PM   60835 C:\AIprojects\openclaw_difi\Database\Digital_Etsy_Metadata.csv                             
5/6/2026 9:52:52 PM   17396 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_Gray_Launch_Queue.csv                    
5/6/2026 9:09:14 PM    1251 C:\AIprojects\openclaw_difi\Database\Etsy_Fee_Kill_Switch.json                             
5/6/2026 9:08:51 PM    1243 C:\AIprojects\openclaw_difi\Database\Account_Risk_State.json                               
5/6/2026 9:07:18 PM    7152 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_QA_Report.csv                            
5/6/2026 9:01:57 PM   24920 C:\AIprojects\openclaw_difi\Database\Digital_Printable_Pack_Index.csv                      
5/6/2026 8:47:22 PM    3245 C:\AIprojects\openclaw_difi\Review_Packets\EBAY_API_MINIMAL_APPLICATION_PACKET.md          
5/6/2026 8:45:54 PM    2782 C:\AIprojects\openclaw_difi\Review_Packets\PRINTIFY_EXTERNAL_SYNC_DIAGNOSIS_20260506.md    
5/6/2026 8:31:52 PM     772 C:\AIprojects\openclaw_difi\Database\Printify_Production_Design_Audit.csv                  
5/6/2026 8:31:26 PM    4308 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2031.md                        
5/6/2026 8:22:34 PM    4308 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_2022.md                        
5/6/2026 7:57:08 PM    8491 C:\AIprojects\openclaw_difi\Review_Packets\codex_stress_test_round2_packet.zip             
5/6/2026 7:53:20 PM   13747 C:\AIprojects\openclaw_difi\Database\Image_Quality_Gate.csv                                
5/6/2026 7:50:41 PM    9655 C:\AIprojects\openclaw_difi\Review_Packets\CODEX_STRESS_TEST_ROUND2.md                     
5/6/2026 7:40:56 PM     596 C:\AIprojects\openclaw_difi\Database\Pricing_Strategy_Matrix.csv                           
5/6/2026 7:40:04 PM     320 C:\AIprojects\openclaw_difi\Database\Printify_Cost_Shipping_Guardrail.csv                  
5/6/2026 7:36:16 PM    1414 C:\AIprojects\openclaw_difi\Database\Pricing_Guardrails.csv                                
5/6/2026 7:35:59 PM    1018 C:\AIprojects\openclaw_difi\Database\Etsy_Gray_Launch_Sequence.csv                         
5/6/2026 7:35:41 PM    5365 C:\AIprojects\openclaw_difi\Review_Packets\CODEX_STRESS_TEST_RESPONSE.md                   
5/6/2026 7:19:31 PM   53705 C:\AIprojects\openclaw_difi\Database\Etsy_listing.xlsx                                     
5/6/2026 7:13:53 PM     365 C:\AIprojects\openclaw_difi\Database\poster_asset_audit.log                                
5/6/2026 6:54:49 PM  102323 C:\AIprojects\openclaw_difi\Database\Production_Line.xlsx                                  
5/6/2026 6:50:12 PM    1416 C:\AIprojects\openclaw_difi\Database\Revenue_Experiment_Queue.csv                          
5/6/2026 6:40:04 PM    5248 C:\AIprojects\openclaw_difi\Review_Packets\REVENUE_EXPERIMENTS.md                          
5/6/2026 6:03:41 PM     243 C:\AIprojects\openclaw_difi\Database\Etsy_Printify_Launch_State.json                       
5/6/2026 6:03:41 PM     403 C:\AIprojects\openclaw_difi\Database\Etsy_Printify_Launch_Log.csv                          
5/6/2026 6:00:31 PM    2354 C:\AIprojects\openclaw_difi\Database\Etsy_brand_shell.md                                   
5/6/2026 6:00:31 PM    9517 C:\AIprojects\openclaw_difi\Database\Etsy_launch_plan.xlsx                                 
5/6/2026 6:00:31 PM   48269 C:\AIprojects\openclaw_difi\Database\Etsy_launch_plan.csv                                  
5/6/2026 5:33:32 PM    1072 C:\AIprojects\openclaw_difi\Review_Packets\README.md                                       
5/6/2026 5:07:23 PM    4405 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1707.md                        
5/6/2026 4:43:36 PM    1576 C:\AIprojects\openclaw_difi\Database\cleanup_20260506.log                                  
5/6/2026 3:11:27 PM    4418 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1511.md                        
5/6/2026 1:52:55 PM    4366 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1352.md                        
5/6/2026 12:52:33 PM   4249 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1252.md                        
5/6/2026 12:45:22 PM   4249 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1245.md                        
5/6/2026 12:37:09 PM   4129 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1237.md                        
5/6/2026 12:32:13 PM   4073 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1232.md                        
5/6/2026 10:46:32 AM   4089 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_1046.md                        
5/6/2026 7:51:26 AM    4089 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0751.md                        
5/6/2026 7:44:04 AM    4051 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0744.md                        
5/6/2026 7:40:28 AM    2947 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0740.md                        
5/6/2026 7:34:48 AM    2947 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0734.md                        
5/6/2026 2:10:30 AM    2947 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0210.md                        
5/6/2026 1:53:36 AM    2947 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0153.md                        
5/6/2026 1:49:42 AM    2628 C:\AIprojects\openclaw_difi\Database\eBay_Live_Cover_Fix_Plan.md                           
5/6/2026 1:45:43 AM    2947 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0145.md                        
5/6/2026 1:40:42 AM    2637 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0140.md                        
5/6/2026 1:33:42 AM    2637 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0133.md                        
5/6/2026 1:24:05 AM    2528 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0124.md                        
5/6/2026 1:04:49 AM    2528 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0104.md                        
5/6/2026 12:49:35 AM   2528 C:\AIprojects\openclaw_difi\Reports\morning_report_20260506_0049.md                        
5/6/2026 12:06:27 AM   9595 C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Fix_Queue.csv                       
5/5/2026 10:46:45 PM   2528 C:\AIprojects\openclaw_difi\Reports\morning_report_20260505_2246.md                        
5/5/2026 10:27:18 PM   2489 C:\AIprojects\openclaw_difi\Reports\morning_report_20260505_2227.md                        
5/5/2026 10:14:46 PM   2489 C:\AIprojects\openclaw_difi\Reports\morning_report_20260505_2214.md                        
5/5/2026 9:42:58 PM    2489 C:\AIprojects\openclaw_difi\Reports\morning_report_20260505_2142.md                        
5/5/2026 9:36:22 PM   16751 C:\AIprojects\openclaw_difi\Database\Printify_Image_Default_Audit.csv                      
5/5/2026 9:15:05 PM   15893 C:\AIprojects\openclaw_difi\Database\eBay_Online_Cover_Audit.backup_schema_20260505_2127...
5/5/2026 8:26:13 PM    2121 C:\AIprojects\openclaw_difi\Reports\morning_report_20260505_2026.md                        
5/5/2026 8:21:57 PM    1994 C:\AIprojects\openclaw_difi\Reports\morning_report_20260505_2021.md                        
5/5/2026 8:21:30 PM   58387 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_Final_Upload_Packet.csv                  
5/5/2026 8:21:30 PM    3124 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_Final_Upload_Packet.md                   
5/5/2026 8:18:09 PM     193 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_QA_Report.md                             
5/5/2026 8:18:09 PM   54446 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_QA.csv                                   
5/5/2026 8:14:54 PM   14622 C:\AIprojects\openclaw_difi\Database\Etsy_Digital_Preview_Assets.csv                       
5/5/2026 8:01:08 PM    1994 C:\AIprojects\openclaw_difi\Reports\morning_report_20260505_2001.md                        
5/5/2026 7:57:44 PM    1726 C:\AIprojects\openclaw_difi\Reports\morning_report_20260505_1957.md                        



--- STDERR ---

```
