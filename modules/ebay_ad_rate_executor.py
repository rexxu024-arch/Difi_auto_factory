from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.ebay_ads_standard import DEFAULT_CAMPAIGN_ID, resolve_campaign_id, _api

DATABASE_DIR = PROJECT_ROOT / "Database"
DEFAULT_PLAN = DATABASE_DIR / "eBay_Ad_Rate_Execution_Shortlist_NoSticker.csv"
LOG_PATH = DATABASE_DIR / "eBay_Ad_Rate_Execution_Log.csv"

LOG_FIELDS = [
    "Timestamp",
    "Mode",
    "ID",
    "Product_Type",
    "eBay_Item_ID",
    "Campaign_ID",
    "Ad_Rate_Pct",
    "Estimated_Profit_USD",
    "HTTP_Status",
    "Result",
    "Error",
]


def now_text() -> str:
    return datetime.now().isoformat(timespec="seconds")


def as_float(value: str | int | float | None, default: float = 0.0) -> float:
    try:
        return float(str(value or "").strip())
    except ValueError:
        return default


def load_plan(path: Path, limit: int = 0) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    blocked_ids = load_blocked_listing_ids()
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            product_type = str(row.get("Product_Type") or "").strip()
            if product_type.lower() == "sticker":
                continue
            ebay_id = str(row.get("eBay_Item_ID") or "").strip()
            if ebay_id in blocked_ids:
                continue
            ad_rate = as_float(row.get("Ad_Rate_Pct"))
            profit = as_float(row.get("Estimated_Profit_USD"))
            max_rate = as_float(row.get("Max_Effective_Ad_Rate_Pct"))
            if not ebay_id or ad_rate <= 0:
                continue
            if max_rate and ad_rate > max_rate:
                continue
            if profit <= 0:
                continue
            rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows


def load_blocked_listing_ids() -> set[str]:
    """Avoid hammering listings already proven incompatible with Marketing API.

    eBay returns HTTP 207 for per-listing failures. Some Printify-origin active
    listings show as "invalid or ended" in Marketing API even while visible in
    Seller Hub, so repeating them only creates noise and account-risk surface.
    """
    if not LOG_PATH.exists():
        return set()
    blocked: set[str] = set()
    with LOG_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            ebay_id = str(row.get("eBay_Item_ID") or "").strip()
            result = str(row.get("Result") or "")
            mode = str(row.get("Mode") or "")
            if mode not in {"UPDATE", "CREATE"} or not ebay_id:
                continue
            if "invalid or has ended" in result or '"statusCode": 404' in result:
                blocked.add(ebay_id)
    return blocked


def write_log(rows: list[dict[str, str]]) -> None:
    DATABASE_DIR.mkdir(exist_ok=True)
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def request_payload(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "listingId": str(row.get("eBay_Item_ID") or "").strip(),
            "bidPercentage": f"{as_float(row.get('Ad_Rate_Pct')):.1f}",
        }
        for row in rows
    ]


def log_rows(
    mode: str,
    rows: list[dict[str, str]],
    campaign_id: str,
    http_status: int | str = "",
    result: str = "",
    error: str = "",
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        out.append(
            {
                "Timestamp": now_text(),
                "Mode": mode,
                "ID": str(row.get("ID") or ""),
                "Product_Type": str(row.get("Product_Type") or ""),
                "eBay_Item_ID": str(row.get("eBay_Item_ID") or ""),
                "Campaign_ID": campaign_id,
                "Ad_Rate_Pct": f"{as_float(row.get('Ad_Rate_Pct')):.1f}",
                "Estimated_Profit_USD": f"{as_float(row.get('Estimated_Profit_USD')):.2f}",
                "HTTP_Status": str(http_status),
                "Result": result[:1500],
                "Error": error[:1000],
            }
        )
    return out


def execute(rows: list[dict[str, str]], campaign_id: str, mode: str, dry_run: bool) -> None:
    payload = {"requests": request_payload(rows)}
    if dry_run:
        logs = log_rows("DRY_RUN_" + mode, rows, campaign_id, result=json.dumps(payload, ensure_ascii=False))
        write_log(logs)
        print(f"[EBAY-ADS-DRY] mode={mode} campaign={campaign_id} rows={len(rows)}")
        return

    endpoint = {
        "update": f"/sell/marketing/v1/ad_campaign/{campaign_id}/bulk_update_ads_bid_by_listing_id",
        "create": f"/sell/marketing/v1/ad_campaign/{campaign_id}/bulk_create_ads_by_listing_id",
    }[mode]
    response = _api("POST", endpoint, json=payload)
    try:
        body = response.json()
    except Exception:
        body = {"raw": response.text[:2000]}
    body_text = json.dumps(body, ensure_ascii=False)
    response_rows = body.get("responses") or []
    logs: list[dict[str, str]] = []
    if response_rows and len(response_rows) == len(rows):
        for row, item in zip(rows, response_rows):
            item_text = json.dumps(item, ensure_ascii=False)
            has_error = bool(item.get("errors"))
            logs.extend(
                log_rows(
                    mode.upper(),
                    [row],
                    campaign_id,
                    item.get("statusCode", response.status_code),
                    item_text,
                    item_text if has_error else "",
                )
            )
    else:
        error_text = body_text if not response.ok else ""
        logs = log_rows(mode.upper(), rows, campaign_id, response.status_code, body_text, error_text)
    write_log(logs)
    print(f"[EBAY-ADS-{mode.upper()}] campaign={campaign_id} rows={len(rows)} http={response.status_code}")
    success_count = sum(
        1
        for item in response_rows
        if int(item.get("statusCode") or response.status_code or 0) < 300 and not item.get("errors")
    )
    error_count = sum(1 for item in response_rows if item.get("errors") or int(item.get("statusCode") or 0) >= 300)
    if response_rows:
        print(f"[EBAY-ADS-{mode.upper()}] row_success={success_count} row_error={error_count}")
    if response.status_code >= 400:
        raise RuntimeError(body_text[:1000])


def run(plan_path: Path, limit: int, campaign_id: str, mode: str, dry_run: bool) -> int:
    rows = load_plan(plan_path, limit=limit)
    if not rows:
        print("[EBAY-ADS] no eligible no-sticker rows")
        return 0
    resolved = resolve_campaign_id(campaign_id or DEFAULT_CAMPAIGN_ID)
    if not resolved:
        raise RuntimeError("No valid eBay Promoted Listings Standard campaign id found.")
    execute(rows, resolved, mode=mode, dry_run=dry_run)
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=str(DEFAULT_PLAN))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--campaign-id", default="")
    parser.add_argument("--mode", choices=["update", "create"], default="update")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    count = run(Path(args.plan), args.limit, args.campaign_id, args.mode, dry_run=not args.execute)
    print(f"[EBAY-ADS] processed={count} dry_run={not args.execute} mode={args.mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
