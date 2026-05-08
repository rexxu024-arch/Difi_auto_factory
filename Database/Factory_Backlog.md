# Factory Backlog

Generated: 2026-05-07 22:11:25 -0400 America/New_York

## Status Counts

- READY: 5
- READY_AFTER_IMAGE_QA: 2
- READY_MONITOR: 2
- WAIT_NETWORK: 1
- READY_FOR_SCHOLAR_REVIEW: 1

## Lane Counts

- control: 1
- supervisor:local: 1
- production: 1
- supervisor:publish: 1
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

### P72 production - READY_AFTER_IMAGE_QA
- Task: Resume Ready_for_Printify uploads in audited single-item batches
- Blocker: 46 local rows are ready; Cover Gate is cleared, so proceed only through single-item upload plus production-design/default-image audit.
- Command: `py modules\printify_full_pipeline.py --limit 1`
- Done when: A new single item reaches stable mockup state and passes selected-count/default-count audit.
- Risk/network: high / Printify UI/API

### P70 supervisor:publish - WAIT_NETWORK
- Task: Publish small cooled batch if network guard is healthy.
- Blocker: Stable=139 published=123 ready=46; network=unknown.
- Command: `py modules\printify_publish_scheduler.py --limit 3 --min-delay 180 --max-delay 420`
- Done when: Supervisor action remains present until its status is completed or superseded.
- Risk/network: high / yes

### P68 publish - READY_AFTER_IMAGE_QA
- Task: Publish small cooled batch after default-image and live-cover spot audit
- Blocker: 16 stable drafts are candidates. Cover Gate is cleared; continue with cooled scheduler and post-publish live-cover spot checks.
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
- Blocker: 5 current traffic hypotheses generated.
- Command: `py modules\ebay_traffic_diagnosis.py`
- Done when: Traffic report identifies exposure/click/conversion blockers from snapshots and cover queues.
- Risk/network: low / local

### P56 etsy - READY_MONITOR
- Task: Monitor first 10 Etsy Digital listings before spending more
- Blocker: Live=10 ready=0 confirmed_spend=$2.00.
- Command: `py modules\etsy_live_audit.py --limit 10`
- Done when: Morning readout has active/readable status plus views/favorites when available; do not scale until signal or Rex resumes.
- Risk/network: low / Etsy public/UI read

### P55 supervisor:etsy - READY_MONITOR
- Task: Monitor Etsy Digital first gray batch before spending more listing fees.
- Blocker: Live=10 ready=0 confirmed_spend=$2.00; hold scale until first traffic readout.
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
