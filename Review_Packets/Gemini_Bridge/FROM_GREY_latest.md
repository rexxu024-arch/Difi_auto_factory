The factory is stable, but we are facing a **Traffic/Intent Gap** on eBay (88% zero-view rate) and a **Gallery Integrity Blocker** for Stickers. The pivot to "Quiet Luxury/Reading Nook" intent is the correct strategic move to bypass the 0-view stagnation.

### Strategic Critique
1.  **Sticker Freeze is Mandatory:** With 22 rows of gallery debt and high 0-views, scaling stickers now risks account quality scores. We must solve the "Gallery Integrity" logic before the 47 ready items move.
2.  **Etsy Signal over Spend:** We have 10 digital listings live. Do not trigger the next $5.80 spend until we see at least 1 organic view or favorite. If 10 listings generate 0 signal, the issue is SEO/Niche, not volume.
3.  **Intent > Ads:** The 2% General Ad rate is a baseline, not a driver. The "Track A" SEO experiment (Quiet Luxury/Study Room) is the primary lever for the 44 zero-view listings.

### Risk Assessment
*   **Account Health:** High. Gallery duplicate risk is being managed before it hits the marketplace.
*   **Financial:** Low. Etsy spend is capped; eBay ads are fixed at 2%.
*   **Technical:** Moderate. Etsy API OAuth is failing; fallback to Edge CDP UI automation is the current stable path.

```json
{
  "tasks": [
    {
      "title": "Fix Sticker Gallery Integrity Debt",
      "priority": 100,
      "lane": "supervisor:production_design_qa",
      "rationale": "22 rows of risky/duplicate gallery images are blocking 47 sticker uploads. Logic must ensure unique buyer-facing mockups.",
      "command": "py modules\\gallery_integrity_fix.py --target stickers --repair-debt",
      "risk": "Low. Local metadata cleanup before upload."
    },
    {
      "title": "Refresh eBay Seller Hub Snapshot",
      "priority": 90,
      "lane": "supervisor:read_only_market",
      "rationale": "Current traffic data is stale. Need to verify if 'Track A' SEO rewrites impacted the 44 zero-view listings.",
      "command": "py modules\\ebay_sellerhub_snapshot.py",
      "risk": "Low. Read-only browser operation."
    },
    {
      "title": "Etsy Digital Signal Audit",
      "priority": 85,
      "lane": "etsy",
      "rationale": "Audit the 10 live digital listings for views/favorites. Block further listing fees ($5.80) if organic signal is zero.",
      "command": "py modules\\etsy_live_audit.py --limit 10 --check-signal",
      "risk": "Low. Read-only public/UI check."
    },
    {
      "title": "Expand Poster/Acrylic Intent Rewrites",
      "priority": 80,
      "lane": "supervisor:copy_experiment",
      "rationale": "Poster/Acrylic show better signal. Apply 'Reading Nook' and 'Collector Shelf' intent to remaining zero-view inventory.",
      "command": "py modules\\ebay_experiment_report.py --apply-intent --category wall_art",
      "risk": "Low. Metadata updates only."
    },
    {
      "title": "Printify Production Design Audit (Poster/Acrylic)",
      "priority": 75,
      "lane": "production",
      "rationale": "Verify visual match for next batch of high-signal items (Poster/Acrylic) before network sync.",
      "command": "py modules\\printify_design_audit.py --limit 5 --category non-sticker",
      "risk": "Low. Visual QA check."
    }
  ]
}
```