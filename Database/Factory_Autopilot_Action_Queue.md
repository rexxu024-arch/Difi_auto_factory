# Factory Autopilot Action Queue

Generated: 2026-05-06T15:11:27-04:00 America/New_York

- Network mode: unknown (network guard skipped)
- eBay workbook rows: 255
- Stable: 175
- Published: 134
- Ready for Printify: 50
- Live cover fix queue rows: 49
- Repair decisions: {'SOURCE_REPAIR_REQUIRED': 45, 'NON_STICKER_REVIEW_REQUIRED': 4}
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
- Reason: 1 listing already failed source repair plus live eBay buyer-page audit.
- Command: `py modules\ebay_replacement_draft_builder.py --limit 1`
- Network: yes; login: Printify API/UI and eBay live audit; risk: high

### P95 cover_gate: READY_SINGLE_SKU_REPAIR
- Action: Repair one Printify source cover, then live-audit eBay before scaling.
- Reason: Live cover queue has 49 rows; 45 require Printify source repair or replacement listings. Printify UI: LOGGED_IN - Printify app page is available in CDP browser.
- Command: `py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120`
- Network: yes; login: Printify remote-debug profile; risk: medium

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

### P55 etsy: WAIT_USER_OR_API_APPROVAL
- Action: Keep Etsy launch packet local until shop/API approval is ready.
- Reason: Etsy developer app is pending approval and Rex has not asked to publish Etsy listings yet.
- Command: `py modules\etsy_digital_listing_export.py`
- Network: no; login: no; risk: low

### P50 copy_experiment: READY
- Action: Continue low-bandwidth SEO/title/description experiment analysis.
- Reason: Ads alone did not move zero-view listings; controlled copy/image experiments are the next learning loop.
- Command: `py modules\ebay_experiment_report.py`
- Network: no; login: no; risk: low
