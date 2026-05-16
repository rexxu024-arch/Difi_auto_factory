from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config


DATABASE = ROOT / "Database"
REPORTS = ROOT / "Reports"
PLAN = DATABASE / "Printify_Free_Shipping_Repair_Plan.csv"
OUT_CSV = DATABASE / "Printify_Free_Shipping_Source_Probe.csv"
OUT_MD = REPORTS / "Printify_Free_Shipping_Source_Probe.md"
PROGRESS_LOG = ROOT / "PROGRESS_LOG.md"
NY = ZoneInfo("America/New_York")


def clean(value) -> str:
    return str(value or "").replace("\n", " ").replace("\r", " ").strip()


def now_et() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %Z")


def headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {Config.Printify_API_KEY}",
        "Content-Type": "application/json",
    }


def api_url(path: str) -> str:
    return f"{Config.Printify_API_URL.rstrip('/')}{path}"


def request_json(method: str, path: str, payload: dict | None = None) -> requests.Response:
    return requests.request(method, api_url(path), headers=headers(), json=payload, timeout=120)


def free_shipping_value(product: dict) -> str:
    props = product.get("sales_channel_properties")
    if isinstance(props, dict):
        return str(props.get("free_shipping"))
    return ""


def load_plan() -> list[dict[str, str]]:
    if not PLAN.exists():
        raise FileNotFoundError(f"Run printify_free_shipping_repair_plan.py first: {PLAN}")
    with PLAN.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def choose_rows(
    rows: list[dict[str, str]],
    limit: int,
    workbook_id: str | None,
    product_id: str | None,
) -> list[dict[str, str]]:
    if product_id:
        matches = [row for row in rows if clean(row.get("Printify_Product_ID")) == product_id]
        if matches:
            return matches[:limit]
        return [
            {
                "Workbook_ID": workbook_id or f"PRINTIFY-{product_id}",
                "Printify_Product_ID": product_id,
                "External_ID": "",
                "Repair_Decision": "DIRECT_PRODUCT_ID_PROBE",
            }
        ]
    if workbook_id:
        return [row for row in rows if clean(row.get("Workbook_ID")) == workbook_id][:limit]
    priority = [
        "SOURCE_PATCH_BEFORE_PUBLISH",
        "SOURCE_PATCH_THEN_EBAY_READBACK",
        "SOURCE_PATCH_THEN_MARKETPLACE_SEO_OVERRIDE",
        "SOURCE_PATCH_CANDIDATE",
    ]
    chosen: list[dict[str, str]] = []
    for decision in priority:
        for row in rows:
            if len(chosen) >= limit:
                break
            if clean(row.get("Repair_Decision")) != decision:
                continue
            if clean(row.get("Locked")).lower() == "true":
                continue
            if clean(row.get("Free_Shipping_State")) == "FREE_SHIPPING_TRUE":
                continue
            if not clean(row.get("Printify_Product_ID")):
                continue
            chosen.append(row)
        if len(chosen) >= limit:
            break
    return chosen


def append_result(result: dict[str, str]) -> None:
    fields = [
        "Timestamp",
        "Workbook_ID",
        "Printify_Product_ID",
        "External_ID",
        "Decision",
        "Before_Free_Shipping",
        "HTTP_Update",
        "After_Free_Shipping",
        "Result",
        "Error",
    ]
    exists = OUT_CSV.exists()
    with OUT_CSV.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow({key: result.get(key, "") for key in fields})


def write_report(results: list[dict[str, str]]) -> None:
    ok = [row for row in results if row.get("Result") == "OK"]
    failed = [row for row in results if row.get("Result") != "OK"]
    lines = [
        "# Printify Free Shipping Source Probe",
        "",
        f"Generated: {now_et()}",
        f"Rows this run: {len(results)}",
        f"OK: {len(ok)}",
        f"Failed: {len(failed)}",
        "",
        "## Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- {row.get('Workbook_ID')}: {row.get('Result')} before={row.get('Before_Free_Shipping')} "
            f"after={row.get('After_Free_Shipping')} http={row.get('HTTP_Update')} external={row.get('External_ID')}"
        )
        if row.get("Error"):
            lines.append(f"  - error: {row.get('Error')}")
    lines.extend(
        [
            "",
            "## Next Gate",
            "",
            "- If one no-external product keeps `free_shipping=True` on readback, test one external eBay item before any bulk repair.",
            "- Do not resume ad-rate escalation until eBay front-end readback confirms free shipping and clean brand/title behavior.",
            "",
            f"CSV: {OUT_CSV}",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def log_progress(message: str) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"\n### {now_et()} - Printify free shipping source probe\n\n{message}\n")


def run(limit: int, workbook_id: str | None, product_id: str | None, dry_run: bool) -> int:
    rows = choose_rows(load_plan(), limit=limit, workbook_id=workbook_id, product_id=product_id)
    if not rows:
        print("[FREE-SHIP-PROBE] no eligible rows")
        return 0

    results: list[dict[str, str]] = []
    for row in rows:
        workbook = clean(row.get("Workbook_ID"))
        product_id = clean(row.get("Printify_Product_ID"))
        external = clean(row.get("External_ID"))
        result = {
            "Timestamp": now_et(),
            "Workbook_ID": workbook,
            "Printify_Product_ID": product_id,
            "External_ID": external,
            "Decision": clean(row.get("Repair_Decision")),
        }
        try:
            before_resp = request_json("GET", f"/shops/{Config.Printify_SHOP_ID}/products/{product_id}.json")
            before_resp.raise_for_status()
            before = before_resp.json()
            result["Before_Free_Shipping"] = free_shipping_value(before)
            if dry_run:
                result["HTTP_Update"] = "DRY_RUN"
                result["After_Free_Shipping"] = result["Before_Free_Shipping"]
                result["Result"] = "DRY_RUN"
                print(f"[FREE-SHIP-DRY] {workbook} product={product_id} before={result['Before_Free_Shipping']}")
            else:
                update_resp = request_json(
                    "PUT",
                    f"/shops/{Config.Printify_SHOP_ID}/products/{product_id}.json",
                    {"sales_channel_properties": {"free_shipping": True}},
                )
                result["HTTP_Update"] = str(update_resp.status_code)
                update_resp.raise_for_status()
                after_resp = request_json("GET", f"/shops/{Config.Printify_SHOP_ID}/products/{product_id}.json")
                after_resp.raise_for_status()
                after = after_resp.json()
                result["After_Free_Shipping"] = free_shipping_value(after)
                result["Result"] = "OK" if result["After_Free_Shipping"].lower() == "true" else "READBACK_MISMATCH"
                print(
                    f"[FREE-SHIP-PROBE] {workbook} update={result['HTTP_Update']} "
                    f"before={result['Before_Free_Shipping']} after={result['After_Free_Shipping']}"
                )
        except Exception as exc:  # noqa: BLE001
            result["Result"] = "FAILED"
            result["Error"] = f"{type(exc).__name__}: {exc}"[:500]
            print(f"[FREE-SHIP-FAIL] {workbook} product={product_id}: {result['Error']}")
        append_result(result)
        results.append(result)

    write_report(results)
    ok = sum(1 for row in results if row.get("Result") == "OK")
    log_progress(
        f"- Source-only probe rows: {len(results)}; OK: {ok}; dry_run={dry_run}.\n"
        f"- Report: `{OUT_MD}`\n"
        f"- CSV: `{OUT_CSV}`"
    )
    return 0 if all(row.get("Result") in {"OK", "DRY_RUN"} for row in results) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe Printify source free_shipping repair without marketplace publish.")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--id", dest="workbook_id", default=None)
    parser.add_argument("--product-id", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(
        limit=max(1, args.limit),
        workbook_id=args.workbook_id,
        product_id=args.product_id,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
