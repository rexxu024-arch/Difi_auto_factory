# Factory Autopilot Action Queue

Generated: 2026-05-06T22:30:37-04:00 America/New_York

- Network mode: unknown (network guard skipped)
- eBay workbook rows: 274
- Stable: 156
- Published: 137
- Ready for Printify: 46
- Live cover fix queue rows: 49
- Repair decisions: {'RETIRED_REPLACED_DONE': 24, 'SOURCE_REPAIR_REQUIRED': 21, 'NON_STICKER_REVIEW_REQUIRED': 4}
- Printify default audit: {'OK': 38, 'CHECK': 123}
- Printify UI status: {'status': 'LOGGED_IN', 'reason': 'Printify app page is available in CDP browser.'}

## Actions

### P100 local: READY
- Action: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- Reason: Safe low-bandwidth maintenance keeps the factory state current while account/image writes are paused.
- Command: `py modules\factory_supervisor.py --execute-local --skip-network`
- Network: no; login: no; risk: low

### P97 replacement: READY_TO_REPLACE_VERIFIED
- Action: Create one verified replacement listing for a live cover failure that survived source repair.
- Reason: 21 listing already failed source repair plus live eBay buyer-page audit.
- Command: `py modules\ebay_replacement_draft_builder.py --limit 1`
- Network: yes; login: Printify API/UI and eBay live audit; risk: high

### P95 cover_gate: READY_SINGLE_SKU_REPAIR
- Action: Repair one Printify source cover, then live-audit eBay before scaling.
- Reason: Live cover queue has 49 rows; 21 require Printify source repair or replacement listings. Printify UI: LOGGED_IN - Printify app page is available in CDP browser.
- Command: `py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120`
- Network: yes; login: Printify remote-debug profile; risk: medium

### P63 production_design_qa: READY
- Action: Run a tiny Printify production-design audit before any larger online batch.
- Reason: This checks whether Printify front print-area art visually matches local Production_Design files; keep it small under weak Wi-Fi.
- Command: `py modules\printify_design_audit.py --limit 2 --sleep-seconds 1`
- Network: yes; login: Printify API; risk: low

### P55 etsy: READY_MONITOR
- Action: Monitor Etsy Digital first gray batch before spending more listing fees.
- Reason: Live=10 ready=20 confirmed_spend=$2.00; hold scale until first traffic readout.
- Command: `py modules\etsy_live_audit.py --limit 10`
- Network: yes; login: Etsy UI/public; risk: low

### P50 copy_experiment: READY
- Action: Continue low-bandwidth SEO/title/description experiment analysis.
- Reason: Ads alone did not move zero-view listings; controlled copy/image experiments are the next learning loop.
- Command: `py modules\ebay_experiment_report.py`
- Network: no; login: no; risk: low
