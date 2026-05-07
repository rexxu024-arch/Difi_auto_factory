# Factory Backlog

Generated: 2026-05-06 23:11:30 -0400 America/New_York

## Status Counts

- READY: 6
- READY_TO_REPLACE_VERIFIED: 2
- WAIT_COVER_GATE: 2
- READY_MONITOR: 2
- READY_SINGLE_SKU_REPAIR: 1
- READY_FOR_SCHOLAR_REVIEW: 1

## Lane Counts

- control: 1
- supervisor:local: 1
- cover_gate: 1
- supervisor:replacement: 1
- supervisor:cover_gate: 1
- replacement: 1
- production: 1
- publish: 1
- supervisor:production_design_qa: 1
- market_learning: 1
- etsy: 1
- supervisor:etsy: 1
- supervisor:copy_experiment: 1
- r_and_d: 1

## Tasks

### P100 control - READY
- Task: Run local supervisor maintenance cycle
- Blocker: None
- Command: `py modules\factory_supervisor.py --execute-local --skip-network`
- Done when: Factory_Autopilot_State, action queue, QA, traffic diagnosis, morning report, and Gemini queue refresh with 0 failures.
- Risk/network: low / local

### P100 supervisor:local - READY
- Task: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- Blocker: Safe low-bandwidth maintenance keeps the factory state current while account/image writes are paused.
- Command: `py modules\factory_supervisor.py --execute-local --skip-network`
- Done when: Supervisor action remains present until its status is completed or superseded.
- Risk/network: low / no

### P98 cover_gate - READY
- Task: Repair one live eBay cover mismatch from Printify source and audit buyer page
- Blocker: Printify CDP status: LOGGED_IN; Printify app page is available in CDP browser.
- Command: `py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120`
- Done when: One SKU becomes LIVE_COVER_FIXED, or the runner records that replacement-listing fallback is required.
- Risk/network: medium / single online item

### P97 supervisor:replacement - READY_TO_REPLACE_VERIFIED
- Task: Create one verified replacement listing for a live cover failure that survived source repair.
- Blocker: 21 listing already failed source repair plus live eBay buyer-page audit.
- Command: `py modules\ebay_replacement_draft_builder.py --limit 1`
- Done when: Supervisor action remains present until its status is completed or superseded.
- Risk/network: high / yes

### P95 supervisor:cover_gate - READY_SINGLE_SKU_REPAIR
- Task: Repair one Printify source cover, then live-audit eBay before scaling.
- Blocker: Live cover queue has 49 rows; 21 require Printify source repair or replacement listings. Printify UI: LOGGED_IN - Printify app page is available in CDP browser.
- Command: `py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120`
- Done when: Supervisor action remains present until its status is completed or superseded.
- Risk/network: medium / yes

### P94 replacement - READY_TO_REPLACE_VERIFIED
- Task: Create verified replacement listing for source-repaired live cover failure
- Blocker: 20 row already failed source repair plus live eBay audit.
- Command: `py modules\ebay_replacement_draft_builder.py --limit 1`
- Done when: Replacement row is created as Ready_for_Printify; public publish still waits for QA and retire sequencing.
- Risk/network: high / single replacement listing

### P72 production - WAIT_COVER_GATE
- Task: Resume Ready_for_Printify uploads only after cover/default-image gate passes
- Blocker: 46 local rows are ready but should not upload until the image gate is proven.
- Command: `py modules\printify_full_pipeline.py --limit 1`
- Done when: A new single item reaches stable mockup state and passes selected-count/default-count audit.
- Risk/network: high / Printify UI/API

### P68 publish - WAIT_COVER_GATE
- Task: Publish small cooled batch after image gate and network guard pass
- Blocker: 19 stable drafts are candidates, but public publish is blocked by cover/default-image risk.
- Command: `py modules\printify_publish_scheduler.py --limit 3 --min-delay 180 --max-delay 420`
- Done when: Published products are live-audited and added to 2% Standard/General ad coverage without PPC.
- Risk/network: high / Printify API/eBay sync

### P63 supervisor:production_design_qa - READY
- Task: Run a tiny Printify production-design audit before any larger online batch.
- Blocker: This checks whether Printify front print-area art visually matches local Production_Design files; keep it small under weak Wi-Fi.
- Command: `py modules\printify_design_audit.py --limit 2 --sleep-seconds 1`
- Done when: Supervisor action remains present until its status is completed or superseded.
- Risk/network: low / yes

### P62 market_learning - READY
- Task: Keep eBay traffic diagnosis current and avoid ad-only conclusions
- Blocker: 4 current traffic hypotheses generated.
- Command: `py modules\ebay_traffic_diagnosis.py`
- Done when: Traffic report identifies exposure/click/conversion blockers from snapshots and cover queues.
- Risk/network: low / local

### P56 etsy - READY_MONITOR
- Task: Monitor first 10 Etsy Digital listings before spending more
- Blocker: Live=10 ready=20 confirmed_spend=$2.00.
- Command: `py modules\etsy_live_audit.py --limit 10`
- Done when: Morning readout has active/readable status plus views/favorites when available; do not scale until signal or Rex resumes.
- Risk/network: low / Etsy public/UI read

### P55 supervisor:etsy - READY_MONITOR
- Task: Monitor Etsy Digital first gray batch before spending more listing fees.
- Blocker: Live=10 ready=20 confirmed_spend=$2.00; hold scale until first traffic readout.
- Command: `py modules\etsy_live_audit.py --limit 10`
- Done when: Supervisor action remains present until its status is completed or superseded.
- Risk/network: low / yes

### P50 supervisor:copy_experiment - READY
- Task: Continue low-bandwidth SEO/title/description experiment analysis.
- Blocker: Ads alone did not move zero-view listings; controlled copy/image experiments are the next learning loop.
- Command: `py modules\ebay_experiment_report.py`
- Done when: Supervisor action remains present until its status is completed or superseded.
- Risk/network: low / no

### P46 r_and_d - READY_FOR_SCHOLAR_REVIEW
- Task: Validate next product candidates with official Printify blueprint/provider/variant data
- Blocker: 5 next blueprint candidates are documented.
- Command: `py modules\product_blueprint_next_plan.py`
- Done when: Canvas, framed poster, notebook, mug, and metal candidates have enough data for Scholar review before development.
- Risk/network: low / local
