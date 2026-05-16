from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config
from modules.ebay_token_manager import EbayTokenError, get_access_token

DATABASE = ROOT / "Database"
REPORTS = ROOT / "Reports"
TOKEN_FILE = DATABASE / ".ebay_oauth_tokens.json"
NY_TZ = ZoneInfo("America/New_York")

METRICS = [
    "LISTING_IMPRESSION_TOTAL",
    "LISTING_IMPRESSION_SEARCH_RESULTS_PAGE",
    "LISTING_VIEWS_TOTAL",
    "LISTING_VIEWS_SOURCE_SEARCH_RESULTS_PAGE",
    "LISTING_VIEWS_SOURCE_OFF_EBAY",
    "CLICK_THROUGH_RATE",
    "SALES_CONVERSION_RATE",
    "TRANSACTION",
]


def now_et() -> datetime:
    return datetime.now(NY_TZ)


def load_token() -> str:
    try:
        return get_access_token()
    except EbayTokenError:
        pass
    if TOKEN_FILE.exists():
        data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
        token = str(data.get("access_token") or "").strip()
        if token:
            return token
    token = Config.EBAY_SELLER_TOKEN
    if not token:
        raise RuntimeError("Missing eBay OAuth token. Run modules/ebay_oauth_flow.py first.")
    return token


def value(item: dict[str, Any]) -> Any:
    return item.get("value") if isinstance(item, dict) else item


def request_report(days: int) -> dict[str, Any]:
    # eBay Analytics treats the current marketplace day as not fully closed;
    # using "today" can be rejected as a future end date near timezone edges.
    end = now_et().date() - timedelta(days=1)
    start = end - timedelta(days=max(days - 1, 0))
    filters = f"marketplace_ids:{{EBAY_US}},date_range:[{start:%Y%m%d}..{end:%Y%m%d}]"
    params = {
        "filter": filters,
        "dimension": "LISTING",
        "metric": ",".join(METRICS),
        "sort": "-LISTING_IMPRESSION_TOTAL",
    }
    url = Config.EBAY_API_BASE_URL.rstrip("/") + "/sell/analytics/v1/traffic_report"
    headers = {
        "Authorization": f"Bearer {load_token()}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, params=params, timeout=60)
    body = response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
    if response.status_code >= 400:
        raise RuntimeError(f"eBay analytics traffic report failed {response.status_code}: {body}")
    return body


def flatten_report(report: dict[str, Any]) -> list[dict[str, Any]]:
    metric_keys = [m.get("key") for m in report.get("header", {}).get("metrics", [])]
    title_by_listing: dict[str, str] = {}
    for block in report.get("dimensionMetadata", []) or []:
        for row in block.get("metadataRecords", []) or []:
            listing_id = str(value(row.get("value")) or "")
            values = row.get("metadataValues") or []
            if listing_id and values:
                title_by_listing[listing_id] = str(value(values[0]) or "")

    rows = []
    for record in report.get("records", []) or []:
        listing_id = str(value((record.get("dimensionValues") or [{}])[0]) or "")
        row: dict[str, Any] = {
            "Listing_ID": listing_id,
            "Title": title_by_listing.get(listing_id, ""),
        }
        for key, metric_value in zip(metric_keys, record.get("metricValues") or []):
            row[str(key)] = value(metric_value)
        rows.append(row)
    return rows


def write_outputs(rows: list[dict[str, Any]], days: int, report: dict[str, Any]) -> tuple[Path, Path]:
    DATABASE.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    timestamp = now_et().strftime("%Y%m%d_%H%M%S")
    csv_path = DATABASE / f"eBay_Analytics_Traffic_{days}d_{timestamp}.csv"
    latest_csv = DATABASE / "eBay_Analytics_Traffic_latest.csv"
    md_path = REPORTS / "eBay_Analytics_Traffic_latest.md"
    fields = ["Listing_ID", "Title"] + METRICS
    for path in [csv_path, latest_csv]:
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in fields})

    total = len(rows)
    zero_impressions = sum(1 for row in rows if float(row.get("LISTING_IMPRESSION_TOTAL") or 0) <= 0)
    zero_views = sum(1 for row in rows if float(row.get("LISTING_VIEWS_TOTAL") or 0) <= 0)
    top = sorted(rows, key=lambda r: float(r.get("LISTING_IMPRESSION_TOTAL") or 0), reverse=True)[:10]
    lines = [
        "# eBay Analytics Traffic Report",
        "",
        f"Generated: {now_et().strftime('%Y-%m-%d %H:%M:%S %z')} America/New_York",
        f"Range: {days} days",
        f"Last updated by eBay: {report.get('lastUpdatedDate', '')}",
        "",
        "## Summary",
        "",
        f"- Listings in report: {total}",
        f"- Zero impressions: {zero_impressions}/{total}",
        f"- Zero views: {zero_views}/{total}",
        "",
        "## Top Impressions",
        "",
    ]
    for row in top:
        lines.append(
            f"- {row.get('Listing_ID')}: impressions={row.get('LISTING_IMPRESSION_TOTAL', 0)}, "
            f"views={row.get('LISTING_VIEWS_TOTAL', 0)}, tx={row.get('TRANSACTION', 0)} | {row.get('Title', '')[:120]}"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return latest_csv, md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    report = request_report(days=args.days)
    rows = flatten_report(report)
    csv_path, md_path = write_outputs(rows, args.days, report)
    print(f"[EBAY-ANALYTICS] rows={len(rows)} csv={csv_path} md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
