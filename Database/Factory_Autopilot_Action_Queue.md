# Factory Autopilot Action Queue

Generated: 2026-05-08T07:29:42-04:00 America/New_York

- Network mode: conservative (loss=0.0% avg=7ms jitter=9999ms)
- Resource mode: RUN (temperature sensor DENIED_OR_UNAVAILABLE; using CPU/memory proxy)
- Resource max parallel/batch: 2/5
- eBay workbook rows: 299
- Stable: 136
- Published: 127
- Ready for Printify: 47
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
- Reason: Stable=136 published=127 ready=47; network=conservative.
- Command: `py modules\printify_publish_scheduler.py --limit 3 --min-delay 180 --max-delay 420`
- Network: yes; login: Printify API; risk: high

### P65 read_only_market: READY
- Action: Refresh eBay Seller Hub performance snapshot.
- Reason: Performance data is stale or absent; this is read-only but browser/network dependent.
- Command: `py modules\ebay_sellerhub_snapshot.py`
- Network: yes; login: eBay Seller Hub; risk: low

### P63 production_design_qa: READY
- Action: Run a tiny Printify production-design audit before any larger online batch.
- Reason: This checks whether Printify front print-area art visually matches local Production_Design files; keep it small under weak Wi-Fi.
- Command: `py modules\printify_design_audit.py --limit 2 --sleep-seconds 1`
- Network: yes; login: Printify API; risk: low

### P55 etsy: READY_MONITOR
- Action: Monitor Etsy Digital first gray batch before spending more listing fees.
- Reason: Live=10 ready=0 confirmed_spend=$2.00; hold scale until first traffic readout.
- Command: `py modules\etsy_live_audit.py --limit 10`
- Network: yes; login: Etsy UI/public; risk: low

### P50 copy_experiment: READY
- Action: Continue low-bandwidth SEO/title/description experiment analysis.
- Reason: Ads alone did not move zero-view listings; controlled copy/image experiments are the next learning loop.
- Command: `py modules\ebay_experiment_report.py`
- Network: no; login: no; risk: low
