The Gemini free key is live and `GENERATE_OK`. We now have strategic oversight active without credit depletion risks. The immediate focus remains the **Cover Gate** and **eBay 0-view** crisis. Ads (2% Standard) are running, but if the cover image or SEO intent is mismatched, we are burning time. 

We will proceed with a "Fix-then-Audit" loop: repair the remaining mismatched covers, then audit the Etsy digital pilot to see if that "clean" signal outperforms the messy eBay sticker data.

### Strategic Priorities
1.  **State Integrity:** Run the local supervisor to sync the latest replacement results.
2.  **Cover Gate Execution:** Continue the 1-by-1 replacement of eBay listings where Printify source-mismatch is confirmed.
3.  **Etsy Signal Watch:** Audit the 10 live digital listings. We need to know if $2.00 bought us any favorites or views before committing the next $2.00.
4.  **Traffic Diagnosis:** Deep-dive the 43 zero-view listings. If covers are fixed and ads are on, the blocker is likely "Intent" (Title/Category).

```json
{
  "tasks": [
    {
      "title": "Local Supervisor Maintenance",
      "priority": 100,
      "lane": "control",
      "rationale": "Ensures the local registry and morning report reflect the latest Cover Gate closures and Gemini API status.",
      "command": "py modules\\factory_supervisor.py --execute-local --skip-network",
      "risk": "low"
    },
    {
      "title": "Repair Live eBay Cover Mismatch",
      "priority": 98,
      "lane": "cover_gate",
      "rationale": "Directly addresses the primary production blocker by aligning Printify source images with eBay buyer-facing covers.",
      "command": "py modules\\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120",
      "risk": "medium"
    },
    {
      "title": "Etsy Digital Pilot Audit",
      "priority": 56,
      "lane": "etsy",
      "rationale": "Verify if the first $2.00 spend generated any organic signal (views/favs) before scaling the next batch.",
      "command": "py modules\\etsy_live_audit.py --limit 10",
      "risk": "low"
    },
    {
      "title": "eBay Traffic Diagnosis",
      "priority": 62,
      "lane": "market_learning",
      "rationale": "Analyze why 43/50 listings show 0 views despite 2% ads; identifies if the issue is SEO intent or technical suppression.",
      "command": "py modules\\ebay_traffic_diagnosis.py",
      "risk": "low"
    },
    {
      "title": "Printify Production Design Audit",
      "priority": 63,
      "lane": "supervisor:production_design_qa",
      "rationale": "Visual QA check to ensure local design files match the Printify print area before any new publishing.",
      "command": "py modules\\printify_design_audit.py --limit 2 --sleep-seconds 1",
      "risk": "low"
    }
  ]
}
```