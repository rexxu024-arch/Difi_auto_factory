"""Public visibility sentinel for Etsy API-created listings.

This is a no-login, read-only probe. It never publishes, edits, or spends.
It checks whether already-confirmed listings have a public Etsy page after the
scheduled visibility window.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATABASE = PROJECT_ROOT / "Database"
REPORTS = PROJECT_ROOT / "Reports"
QUEUE = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
RISK = DATABASE / "Account_Risk_State.json"
LOG = DATABASE / "Etsy_Shadowban_Sentinel.csv"
REPORT = REPORTS / "Etsy_Shadowban_Sentinel_latest.md"
LIVE_AUDIT = DATABASE / "Etsy_Digital_Live_Audit.csv"


def now() -> datetime:
    return datetime.now().astimezone()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def due(row: dict[str, str], force: bool) -> bool:
    if force:
        return True
    due_at = row.get("Shadow_Check_Due_At") or ""
    if not due_at:
        return False
    try:
        return datetime.fromisoformat(due_at) <= now()
    except ValueError:
        return True


def public_probe(listing_id: str) -> tuple[str, int, str]:
    url = f"https://www.etsy.com/listing/{listing_id}"
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 OpenClawVisibilityCheck/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
        timeout=45,
        allow_redirects=True,
    )
    text = response.text[:2000]
    if response.status_code == 200 and ("etsy" in text.lower() or "/listing/" in response.url):
        return "PUBLIC_VISIBLE", response.status_code, response.url
    if response.status_code in {404, 410}:
        return "PUBLIC_NOT_FOUND_REVIEW_REQUIRED", response.status_code, response.url
    if response.status_code in {403, 429, 503}:
        return "PUBLIC_PING_BLOCKED_RETRY", response.status_code, response.url
    return "PUBLIC_UNKNOWN_RETRY", response.status_code, response.url


def read_live_audit_map() -> dict[str, dict[str, str]]:
    """Return the latest browser/API live-audit row per Etsy listing id.

    Etsy can return 403 to no-login probes even when the listing is perfectly
    visible in an authenticated/browser audit. Treat that as probe friction, not
    as shadowban evidence.
    """
    latest: dict[str, dict[str, str]] = {}
    for row in read_csv(LIVE_AUDIT):
        listing_id = row.get("Etsy_Listing_ID") or ""
        if listing_id:
            latest[listing_id] = row
    return latest


def update_risk_if_needed(results: list[dict[str, str]]) -> None:
    hard = [row for row in results if row["Shadow_Status"] == "PUBLIC_NOT_FOUND_REVIEW_REQUIRED"]
    if not hard:
        return
    data = {}
    if RISK.exists():
        data = json.loads(RISK.read_text(encoding="utf-8-sig"))
    data.setdefault("states", {}).setdefault("etsy", {})
    etsy = data["states"]["etsy"]
    etsy["paid_publish_allowed"] = False
    etsy["risk_state"] = "SHADOWBANNED_SANDBOX_REVIEW_REQUIRED"
    etsy["notes"] = (
        f"Public visibility sentinel found {len(hard)} confirmed listing(s) returning 404/410. "
        "Pause Etsy API publishing until Rex/Codex reviews public visibility."
    )
    data["updated_at"] = now().isoformat(timespec="seconds")
    RISK.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def run(limit: int = 10, force: bool = False, dry_run: bool = False) -> dict:
    rows = read_csv(QUEUE)
    live_audit = read_live_audit_map()
    candidates = [
        row
        for row in rows
        if row.get("Etsy_Listing_ID")
        and row.get("Launch_Status") in {"PUBLISHED_API_CONFIRMED", "PUBLISHED_UI_CONFIRMED"}
        and row.get("Shadow_Status") not in {"PUBLIC_VISIBLE", "ACTIVE_CONFIRMED_BY_BROWSER_AUDIT"}
        and due(row, force)
    ][:limit]
    results = []
    for row in candidates:
        listing_id = row["Etsy_Listing_ID"]
        if dry_run:
            status, http_status, final_url = "DRY_RUN_WOULD_PROBE", 0, f"https://www.etsy.com/listing/{listing_id}"
        else:
            status, http_status, final_url = public_probe(listing_id)
        audit_row = live_audit.get(listing_id, {})
        if status == "PUBLIC_PING_BLOCKED_RETRY" and audit_row.get("Status") == "ACTIVE_READABLE":
            status = "ACTIVE_CONFIRMED_BY_BROWSER_AUDIT"
            final_url = audit_row.get("URL") or final_url
        row["Shadow_Status"] = status
        row["Shadow_Last_Checked_At"] = now().isoformat(timespec="seconds")
        row["Shadow_HTTP_Status"] = str(http_status)
        row["Shadow_Public_URL"] = final_url
        results.append(
            {
                "Timestamp": row["Shadow_Last_Checked_At"],
                "ID": row.get("ID", ""),
                "Etsy_Listing_ID": listing_id,
                "Shadow_Status": status,
                "HTTP_Status": str(http_status),
                "URL": final_url,
            }
        )
    if candidates and not dry_run:
        fieldnames = list(rows[0].keys())
        for key in ["Shadow_Status", "Shadow_Last_Checked_At", "Shadow_HTTP_Status", "Shadow_Public_URL"]:
            if key not in fieldnames:
                fieldnames.append(key)
        write_csv(QUEUE, rows, fieldnames)
    if results:
        existing = read_csv(LOG)
        all_rows = existing + results
        write_csv(LOG, all_rows, ["Timestamp", "ID", "Etsy_Listing_ID", "Shadow_Status", "HTTP_Status", "URL"])
        update_risk_if_needed(results)
    REPORTS.mkdir(parents=True, exist_ok=True)
    report = [
        "# Etsy Shadowban Sentinel",
        "",
        f"Generated: {now().isoformat(timespec='seconds')}",
        f"Checked: {len(results)}",
        "",
    ]
    for row in results:
        report.append(f"- {row['ID']} / {row['Etsy_Listing_ID']}: {row['Shadow_Status']} HTTP {row['HTTP_Status']}")
    if not results:
        report.append("- No due listings to probe.")
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    return {"checked": len(results), "statuses": {status: sum(1 for r in results if r["Shadow_Status"] == status) for status in sorted({r["Shadow_Status"] for r in results})}, "report": str(REPORT)}


def main() -> None:
    parser = argparse.ArgumentParser(description="No-login public visibility probe for Etsy listings.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(limit=args.limit, force=args.force, dry_run=args.dry_run), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
