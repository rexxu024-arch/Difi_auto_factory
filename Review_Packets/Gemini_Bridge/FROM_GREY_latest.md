Rex, the night shift runner is performing within parameters. We have successfully pivoted from "Cover Gate" to "Gallery Integrity" and "SEO Intent" as the primary levers for eBay traffic. 

The 0-view count (44/50) confirms that 2% General ads are a baseline, not a driver. We are now testing if "Quiet Luxury" and "Deep Work" intent language can break the visibility ceiling for Posters and Acrylics. Stickers remain frozen to prevent further gallery debt.

### Strategic Directives
1.  **Intent over Ads:** Prioritize Track A (SEO/Intent) syncs. If 0-views persist after re-indexing, we re-evaluate category fit.
2.  **Poster/Acrylic Dominance:** Direct all "Ready for Printify" energy here. They show better signal and lower gallery risk than Stickers.
3.  **Etsy Gray Box:** Maintain the $2/batch cap. We are hunting for organic "Favorites" before authorizing the next $4.00 spend.
4.  **Gallery Debt:** The 22 "Source Debt" rows are a silent killer for buyer trust. We fix these locally before any mass-publish.

```json
{
  "tasks": [
    {
      "title": "Local Supervisor Maintenance",
      "priority": 100,
      "lane": "control",
      "rationale": "Ensures factory state, QA, and morning reports are synced before the 06:00 shutdown.",
      "command": "py modules\\factory_supervisor.py --execute-local --skip-network",
      "risk": "low"
    },
    {
      "title": "Refresh eBay Seller Hub Snapshot",
      "priority": 85,
      "lane": "supervisor:read_only_market",
      "rationale": "Critical to see if the 10 Track A SEO rewrites have moved the 0-view needle.",
      "command": "py modules\\ebay_sellerhub_snapshot.py",
      "risk": "low"
    },
    {
      "title": "Audited Poster/Acrylic Upload",
      "priority": 75,
      "lane": "production",
      "rationale": "Advance high-signal products (Poster/Acrylic) while Stickers are frozen. Single-item batch to respect night-shift limits.",
      "command": "py modules\\printify_full_pipeline.py --limit 1",
      "risk": "medium"
    },
    {
      "title": "Etsy Digital Live Audit",
      "priority": 65,
      "lane": "supervisor:etsy",
      "rationale": "Monitor the first 10 listings for organic views/favorites without increasing spend.",
      "command": "py modules\\etsy_live_audit.py --limit 10",
      "risk": "low"
    },
    {
      "title": "Gallery Debt Remediation Prep",
      "priority": 60,
      "lane": "supervisor:production_design_qa",
      "rationale": "Prepare the fix for the 22 risky source-gallery rows to ensure future buyer trust.",
      "command": "py modules\\printify_design_audit.py --limit 5",
      "risk": "low"
    }
  ]
}
```