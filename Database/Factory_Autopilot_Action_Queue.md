# Factory Autopilot Action Queue

Generated: 2026-05-07T22:29:29-04:00 America/New_York

- Network mode: unknown (network guard skipped)
- Resource mode: RUN_CONSERVATIVE (temperature sensor DENIED_OR_UNAVAILABLE; using CPU/memory proxy; memory elevated 83.9%)
- Resource max parallel/batch: 1/1
- eBay workbook rows: 299
- Stable: 139
- Published: 126
- Ready for Printify: 46
- Live cover fix queue rows: 49
- Repair decisions: {'RETIRED_REPLACED_DONE': 49}
- Printify default audit: {'OK': 38, 'CHECK': 123}
- Printify UI status: {'status': 'LOGGED_IN', 'reason': 'Printify app page is available in CDP browser.'}

## Actions

### P100 local: READY
- Action: Refresh local QA, registry, market queue, cover decisions, experiment report, and morning report.
- Reason: Safe low-bandwidth maintenance keeps the factory state current while account/image writes are paused.
- Command: `py modules\factory_supervisor.py --execute-local --skip-network`
- Network: no; login: no; risk: low

### P70 publish: WAIT_NETWORK
- Action: Publish small cooled batch if network guard is healthy.
- Reason: Stable=139 published=126 ready=46; network=unknown.
- Command: `py modules\printify_publish_scheduler.py --limit 3 --min-delay 180 --max-delay 420`
- Network: yes; login: Printify API; risk: high

### P63 production_design_qa: READY
- Action: Run a tiny Printify production-design audit before any larger online batch.
- Reason: This checks whether Printify front print-area art visually matches local Production_Design files; keep it small under weak Wi-Fi. Resource guard says conservative: temperature sensor DENIED_OR_UNAVAILABLE; using CPU/memory proxy; memory elevated 83.9%
- Command: `py modules\printify_design_audit.py --limit 2 --sleep-seconds 1`
- Network: yes; login: Printify API; risk: low

### P55 etsy: READY_MONITOR
- Action: Monitor Etsy Digital first gray batch before spending more listing fees.
- Reason: Live=10 ready=0 confirmed_spend=$2.00; hold scale until first traffic readout. Resource guard says conservative: temperature sensor DENIED_OR_UNAVAILABLE; using CPU/memory proxy; memory elevated 83.9%
- Command: `py modules\etsy_live_audit.py --limit 10`
- Network: yes; login: Etsy UI/public; risk: low

### P50 copy_experiment: READY
- Action: Continue low-bandwidth SEO/title/description experiment analysis.
- Reason: Ads alone did not move zero-view listings; controlled copy/image experiments are the next learning loop.
- Command: `py modules\ebay_experiment_report.py`
- Network: no; login: no; risk: low
