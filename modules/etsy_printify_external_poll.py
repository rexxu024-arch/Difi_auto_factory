"""Poll Printify Etsy products whose marketplace external id is still pending.

This is a no-spend, no-republish reconciliation step. It only reads Printify
product state and appends durable status rows when Etsy external ids appear or
when a publish request stays unresolved long enough to require self-healing.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config

NY = ZoneInfo("America/New_York")
DATABASE = PROJECT_ROOT / "Database"
LOG_CSV = DATABASE / "Etsy_Printify_Launch_Log.csv"
STATE_JSON = DATABASE / "Etsy_Printify_External_Poll_State.json"
SHOP_ID = str(Config.Printify_ETSY_SHOP_ID or "")


FIELDS = [
    "Timestamp",
    "ID",
    "Product_Type",
    "Action",
    "Status",
    "Printify_Etsy_Product_ID",
    "External_ID",
    "External_Handle",
    "Note",
]


def now() -> datetime:
    return datetime.now(NY)


def now_text() -> str:
    return now().isoformat(timespec="seconds")


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {Config.Printify_API_KEY}"}


def api_url(path: str) -> str:
    return f"{Config.Printify_API_URL.rstrip('/')}{path}"


def read_rows() -> list[dict[str, str]]:
    if not LOG_CSV.exists():
        return []
    with LOG_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def append_row(row: dict[str, str]) -> None:
    LOG_CSV.parent.mkdir(exist_ok=True)
    exists = LOG_CSV.exists()
    with LOG_CSV.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in FIELDS})


def parse_time(value: str) -> datetime | None:
    text = clean(value)
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=NY)
        return parsed.astimezone(NY)
    except Exception:
        return None


def latest_by_product(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    latest: dict[str, dict[str, str]] = {}
    for row in rows:
        product_id = clean(row.get("Printify_Etsy_Product_ID"))
        if not product_id:
            continue
        latest[product_id] = row
    return latest


def pending_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    latest = latest_by_product(rows)
    result = []
    for row in latest.values():
        if clean(row.get("Status")) in {
            "PUBLISHED_EXTERNAL_PENDING",
            "EXTERNAL_STILL_PENDING_NEEDS_RECONCILE",
        }:
            result.append(row)
    return result


def fetch_product(product_id: str) -> dict:
    response = requests.get(
        api_url(f"/shops/{SHOP_ID}/products/{product_id}.json"),
        headers=headers(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def poll(max_age_minutes: int = 120, limit: int = 20) -> int:
    if not SHOP_ID:
        raise RuntimeError("Printify_ETSY_SHOP_ID is not configured.")
    rows = read_rows()
    pending = pending_rows(rows)[:limit]
    resolved = 0
    held = 0
    checked = 0
    for row in pending:
        checked += 1
        item_id = clean(row.get("ID"))
        product_id = clean(row.get("Printify_Etsy_Product_ID"))
        product = fetch_product(product_id)
        external = product.get("external") or {}
        external_id = clean(external.get("id"))
        external_handle = clean(external.get("handle"))
        if external_id or external_handle:
            append_row(
                {
                    "Timestamp": now_text(),
                    "ID": item_id,
                    "Product_Type": clean(row.get("Product_Type")),
                    "Action": "EXTERNAL_POLL",
                    "Status": "PUBLISHED_EXTERNAL_CONFIRMED",
                    "Printify_Etsy_Product_ID": product_id,
                    "External_ID": external_id,
                    "External_Handle": external_handle,
                    "Note": "External id/handle backfilled by Printify after publish request.",
                }
            )
            resolved += 1
            print(f"[ETSY-EXTERNAL] confirmed {item_id} product={product_id} external={external_id or external_handle}")
            continue
        created_at = parse_time(row.get("Timestamp", ""))
        age = (now() - created_at).total_seconds() / 60 if created_at else 0
        status = clean(row.get("Status"))
        if status == "EXTERNAL_STILL_PENDING_NEEDS_RECONCILE":
            held += 1
            print(f"[ETSY-EXTERNAL] still-held {item_id} product={product_id} age_min={age:.1f}")
        elif age >= max_age_minutes:
            append_row(
                {
                    "Timestamp": now_text(),
                    "ID": item_id,
                    "Product_Type": clean(row.get("Product_Type")),
                    "Action": "EXTERNAL_POLL",
                    "Status": "EXTERNAL_STILL_PENDING_NEEDS_RECONCILE",
                    "Printify_Etsy_Product_ID": product_id,
                    "Note": f"No external id after {age:.1f} minutes; do not republish. Queue delayed reconcile/self-heal.",
                }
            )
            held += 1
            print(f"[ETSY-EXTERNAL] hold {item_id} product={product_id} age_min={age:.1f}")
        else:
            print(f"[ETSY-EXTERNAL] pending {item_id} product={product_id} age_min={age:.1f}")
    STATE_JSON.write_text(
        json.dumps(
            {
                "timestamp": now_text(),
                "checked": checked,
                "resolved": resolved,
                "held": held,
                "pending_remaining": max(0, len(pending) - resolved - held),
                "max_age_minutes": max_age_minutes,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Poll Printify Etsy external ids without republishing.")
    parser.add_argument("--max-age-minutes", type=int, default=120)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    raise SystemExit(poll(max_age_minutes=args.max_age_minutes, limit=args.limit))


if __name__ == "__main__":
    main()
