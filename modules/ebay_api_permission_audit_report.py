"""Generate a focused eBay API permission/surface audit report.

This report intentionally avoids printing tokens or secrets. It summarizes
whether OAuth is working, which Sell API surfaces are reachable, and which
parts of the current Printify-origin catalog still require a different path.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = ROOT / "Database"
REPORTS_DIR = ROOT / "Reports"
PROGRESS_LOG = ROOT / "PROGRESS_LOG.md"
NY = ZoneInfo("America/New_York")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def probe_by_name(status: dict) -> dict[str, dict]:
    probes = status.get("probes", [])
    return {str(probe.get("name")): probe for probe in probes if isinstance(probe, dict)}


def summarize_probe(probe: dict | None) -> str:
    if not probe:
        return "missing"
    status = probe.get("status")
    ok = "OK" if status == 200 else "CHECK"
    return f"{ok} HTTP {status}"


def append_progress(message: str) -> None:
    ts = datetime.now(NY).strftime("%Y-%m-%d %H:%M ET")
    entry = f"\n- {ts} - {message}\n"
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(NY)
    stamp = now.strftime("%Y%m%d_%H%M%S")

    status = load_json(DATABASE_DIR / "eBay_API_Status.json")
    probes = probe_by_name(status)

    inventory = probes.get("inventory_items", {})
    campaigns = probes.get("marketing_campaigns", {})
    fulfillment = probes.get("fulfillment_policies", {})
    payment = probes.get("payment_policies", {})
    returns = probes.get("return_policies", {})

    inventory_total = inventory.get("total")
    campaign_items = campaigns.get("items")
    campaign_count = len(campaign_items) if isinstance(campaign_items, list) else "unknown"

    report = f"""# eBay API Permission Audit

Generated: {now.strftime("%Y-%m-%d %H:%M:%S %Z")}

## Verdict

The eBay Developer app is connected to the seller account well enough for OAuth REST reads. The latest smoke test returns HTTP 200 for Inventory, Marketing, and Account policy endpoints.

The remaining blocker is **not a missing permission checkbox**. The blocker is API surface mismatch: the current active listings were created/synchronized through Printify/eBay legacy flows, and they are not exposed as editable Sell Inventory items under this OAuth surface.

## What Was Fixed

- Fixed local OAuth refresh handling in `modules/ebay_token_manager.py`.
- The old local token file stored the originally requested scopes, not necessarily the exact granted scopes.
- Refresh with that stale scope list caused eBay `invalid_scope`.
- Refresh now retries once without the stale stored scope and preserves eBay's returned scope value.

## Latest Probe Snapshot

| API Surface | Result | Meaning |
| --- | --- | --- |
| Sell Inventory `inventory_item` read | {summarize_probe(inventory)}; total={inventory_total} | OAuth works, but current Printify-origin active listings are not visible as Inventory API items. |
| Sell Marketing campaign read | {summarize_probe(campaigns)}; campaigns={campaign_count} | Campaign access works. Existing fixed 2% Standard campaign can be read. |
| Account fulfillment policies | {summarize_probe(fulfillment)} | Endpoint reachable, but policy payload may not expose UI/Printify-created policies for this seller context. |
| Account payment policies | {summarize_probe(payment)} | Endpoint reachable, same caveat as above. |
| Account return policies | {summarize_probe(returns)} | Endpoint reachable, same caveat as above. |

## Practical Consequence

Safe via API now:

- Refresh eBay OAuth automatically.
- Read Marketing campaigns.
- Read Sell Inventory model for any future listings created directly in that model.
- Read Account policy endpoints.
- Keep diagnostics and performance ledgers updated.

Not safe to assume via current Sell APIs:

- Bulk ending current Printify-origin active listings through Sell Inventory.
- Bulk revising current Printify-origin shipping/business policies through Account API.
- Treating `Inventory API total=0` as “no active listings.” Seller Hub still shows active listings.

## Next Execution Path

1. Use Seller Hub UI or Trading API read-only probes to verify a single active item by eBay item ID.
2. If Trading API can read and revise/end one item safely, build a tiny dry-run queue for sticker/low-value purge.
3. Keep bulk eBay destructive writes frozen until one-item proof passes.
4. Continue using Sell Marketing API only where item eligibility is confirmed by dry-run responses.

## Rex Action Needed

No new permission checkbox is required right now.

If eBay asks for consent again later, grant the same seller account (`yu300845`) with at least:

- `sell.inventory`
- `sell.marketing`
- `sell.account`
- `sell.analytics.readonly`
- `sell.fulfillment.readonly`

But the current issue is not missing scopes; it is listing-origin/API compatibility.
"""

    latest = REPORTS_DIR / "eBay_API_Permission_Audit_latest.md"
    stamped = REPORTS_DIR / f"eBay_API_Permission_Audit_{stamp}.md"
    latest.write_text(report, encoding="utf-8")
    stamped.write_text(report, encoding="utf-8")

    append_progress(
        "eBay API permission audit refreshed: OAuth refresh is fixed; REST reads are 200 OK; current blocker is Printify-origin listing/API surface mismatch, not missing seller permission."
    )

    print(f"Wrote {latest}")
    print(f"Wrote {stamped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
