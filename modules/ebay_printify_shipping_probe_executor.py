from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config


DATABASE = ROOT / "Database"
REPORTS = ROOT / "Reports"
QUEUE_CSV = DATABASE / "eBay_Printify_Shipping_Template_Probe_Queue.csv"
OUT_CSV = DATABASE / "eBay_Printify_Shipping_Template_Probe_Execution.csv"
OUT_MD = REPORTS / "eBay_Printify_Shipping_Template_Probe_Execution.md"
NY = ZoneInfo("America/New_York")

PUBLISH_SHIPPING_ONLY = {
    "title": False,
    "description": False,
    "images": False,
    "variants": False,
    "tags": False,
    "keyFeatures": False,
    "shipping_template": True,
}


def now_text() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def read_queue() -> list[dict[str, str]]:
    if not QUEUE_CSV.exists():
        return []
    with QUEUE_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: clean(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {Config.Printify_API_KEY}",
        "Content-Type": "application/json",
    }


def request_with_retry(method: str, url: str, payload: dict[str, Any] | None = None) -> requests.Response:
    last: Exception | None = None
    for _ in range(3):
        try:
            response = requests.request(method, url, headers=headers(), json=payload, timeout=180)
            if response.status_code in {429, 500, 502, 503, 504}:
                last = RuntimeError(f"HTTP {response.status_code}: {response.text[:300]}")
                continue
            return response
        except Exception as exc:  # noqa: BLE001
            last = exc
    raise RuntimeError(f"Printify request failed after retries: {last}")


def enabled_variants(product: dict[str, Any]) -> list[dict[str, Any]]:
    return [variant for variant in product.get("variants") or [] if variant.get("is_enabled")]


def selected_images(product: dict[str, Any]) -> list[dict[str, Any]]:
    return [image for image in product.get("images") or [] if image.get("is_selected_for_publishing")]


def run(limit: int, execute: bool) -> list[dict[str, str]]:
    rows = read_queue()
    if limit:
        rows = rows[:limit]
    base = Config.Printify_API_URL.rstrip("/")
    out: list[dict[str, str]] = []
    for row in rows:
        product_id = clean(row.get("Printify_Product_ID"))
        local_id = clean(row.get("ID"))
        item_id = clean(row.get("eBay_Item_ID"))
        get_status = publish_status = ""
        result = "DRY_RUN_READY"
        error = ""
        external_id = ""
        visible = ""
        locked = ""
        enabled_count = selected_count = 0
        try:
            get_resp = request_with_retry("GET", f"{base}/shops/{Config.Printify_SHOP_ID}/products/{product_id}.json")
            get_status = str(get_resp.status_code)
            get_resp.raise_for_status()
            product = get_resp.json()
            visible = str(bool(product.get("visible")))
            locked = str(bool(product.get("is_locked")))
            enabled_count = len(enabled_variants(product))
            selected_count = len(selected_images(product))
            external = product.get("external") or {}
            external_id = clean(external.get("id"))
            if product.get("is_locked"):
                result = "HOLD_LOCKED_PRODUCT"
            elif external_id and external_id != item_id:
                result = "HOLD_EXTERNAL_MISMATCH"
                error = f"Printify external id {external_id} != queue eBay item {item_id}"
            elif selected_count < 4:
                result = "HOLD_LOW_SELECTED_IMAGES"
            elif enabled_count < 1:
                result = "HOLD_NO_ENABLED_VARIANT"
            elif execute:
                pub_resp = request_with_retry(
                    "POST",
                    f"{base}/shops/{Config.Printify_SHOP_ID}/products/{product_id}/publish.json",
                    payload=PUBLISH_SHIPPING_ONLY,
                )
                publish_status = str(pub_resp.status_code)
                pub_resp.raise_for_status()
                result = "PUBLISH_SHIPPING_TEMPLATE_SENT"
            else:
                result = "DRY_RUN_READY"
        except Exception as exc:  # noqa: BLE001
            result = "FAILED"
            error = f"{type(exc).__name__}: {exc}"[:800]
        out.append(
            {
                "Timestamp": now_text(),
                "Mode": "EXECUTE" if execute else "DRY_RUN",
                "ID": local_id,
                "Product_Type": clean(row.get("Product_Type")),
                "eBay_Item_ID": item_id,
                "Printify_Product_ID": product_id,
                "External_ID": external_id,
                "Visible": visible,
                "Is_Locked": locked,
                "Enabled_Variants": str(enabled_count),
                "Selected_Images": str(selected_count),
                "GET_Status": get_status,
                "Publish_Status": publish_status,
                "Payload": json.dumps(PUBLISH_SHIPPING_ONLY, separators=(",", ":")),
                "Result": result,
                "Error": error,
                "Title": clean(row.get("Title")),
            }
        )
        print(f"[EBAY-SHIPPING-PROBE] {local_id} mode={'EXECUTE' if execute else 'DRY'} result={result}")
    return out


def write_outputs(rows: list[dict[str, str]]) -> None:
    fields = [
        "Timestamp",
        "Mode",
        "ID",
        "Product_Type",
        "eBay_Item_ID",
        "Printify_Product_ID",
        "External_ID",
        "Visible",
        "Is_Locked",
        "Enabled_Variants",
        "Selected_Images",
        "GET_Status",
        "Publish_Status",
        "Payload",
        "Result",
        "Error",
        "Title",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["Result"]] = counts.get(row["Result"], 0) + 1
    lines = [
        "# eBay Printify Shipping Template Probe Execution",
        "",
        f"Generated: {now_text()}",
        f"Rows: {len(rows)}",
        "",
        "## Result Counts",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in sorted(counts.items()))
    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "- Default run is dry-run only.",
            "- Live mode sends only `shipping_template=true`; it does not touch title, description, image gallery, variants, tags, or key features.",
            "- After one live probe, re-run the eBay inventory/category audit before any rollout.",
            "",
            f"CSV: {OUT_CSV}",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[EBAY-SHIPPING-PROBE-DONE] rows={len(rows)} csv={OUT_CSV} md={OUT_MD}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run or execute one-item Printify shipping-template probe for eBay listings.")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--execute", action="store_true", help="Actually POST Printify publish.json with shipping_template=true only.")
    args = parser.parse_args()
    if args.execute and args.limit != 1:
        raise SystemExit("--execute is restricted to --limit 1 for account-safety.")
    rows = run(limit=args.limit, execute=args.execute)
    write_outputs(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
