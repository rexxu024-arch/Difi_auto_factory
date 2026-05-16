from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime
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
PERFORMANCE_LOG = DATABASE / "Performance_Log.csv"
TOKEN_FILE = DATABASE / ".ebay_oauth_tokens.json"
OUT_CSV = DATABASE / "eBay_API_Inventory_Category_Audit.csv"
OUT_MD = REPORTS / "eBay_API_Inventory_Category_Audit.md"
NY = ZoneInfo("America/New_York")


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\n", " ").replace("\r", " ")).strip()


def to_int(value: Any) -> int:
    try:
        return int(re.sub(r"[^0-9]", "", clean(value)) or "0")
    except ValueError:
        return 0


def to_float(value: Any) -> float:
    try:
        return float(re.sub(r"[^0-9.]", "", clean(value)) or "0")
    except ValueError:
        return 0.0


def now_et() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def load_token() -> str:
    try:
        return get_access_token()
    except EbayTokenError:
        pass
    if TOKEN_FILE.exists():
        data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
        token = clean(data.get("access_token"))
        if token:
            return token
    return clean(Config.EBAY_SELLER_TOKEN)


def latest_performance_rows(target: str, limit: int) -> tuple[str, list[dict[str, str]]]:
    if not PERFORMANCE_LOG.exists():
        return "", []
    with PERFORMANCE_LOG.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return "", []
    latest = max(clean(row.get("Snapshot_Timestamp")) for row in rows)
    selected = []
    for row in rows:
        if clean(row.get("Snapshot_Timestamp")) != latest:
            continue
        title = clean(row.get("Title")).lower()
        if "toothbrush" in title or "dumbbell" in title:
            continue
        views = to_int(row.get("Views_30_Days"))
        if target == "zero-view" and views != 0:
            continue
        if target == "viewed" and views <= 0:
            continue
        selected.append(row)
        if limit and len(selected) >= limit:
            break
    return latest, selected


def browse_item_group(item_group_id: str, token: str) -> tuple[int, dict[str, Any] | None, str]:
    url = f"{Config.EBAY_API_BASE_URL.rstrip()}/buy/browse/v1/item/get_items_by_item_group"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    }
    try:
        response = requests.get(
            url,
            headers=headers,
            params={"item_group_id": item_group_id},
            timeout=45,
        )
    except Exception as exc:
        return 0, None, f"{type(exc).__name__}: {exc}"
    if not (200 <= response.status_code < 300):
        return response.status_code, None, response.text[:500]
    try:
        data = response.json()
    except Exception as exc:
        return response.status_code, None, f"JSON_ERROR: {exc}"
    items = data.get("items") or []
    if not items:
        return response.status_code, None, "NO_ITEMS"
    return response.status_code, items[0], ""


def infer_product_type(title: str, category_path: str) -> str:
    text = f"{title} {category_path}".lower()
    if "sticker" in text or "decal" in text:
        return "Sticker"
    if "acrylic" in text or "photo block" in text:
        return "Acrylic"
    if "poster" in text or "wall art" in text:
        return "Poster"
    if "mug" in text:
        return "Mug"
    return "Unknown"


def images(item: dict[str, Any]) -> list[str]:
    out = []
    main = ((item.get("image") or {}).get("imageUrl") or "").strip()
    if main:
        out.append(main)
    for image in item.get("additionalImages") or []:
        url = clean((image or {}).get("imageUrl"))
        if url:
            out.append(url)
    return out


def availability(item: dict[str, Any]) -> dict[str, Any]:
    values = item.get("estimatedAvailabilities") or []
    return values[0] if values else {}


def shipping(item: dict[str, Any]) -> dict[str, Any]:
    values = item.get("shippingOptions") or []
    return values[0] if values else {}


def included_regions(item: dict[str, Any]) -> list[str]:
    locations = item.get("shipToLocations") or {}
    return [clean(region.get("regionName")) for region in locations.get("regionIncluded") or [] if region]


def flag_row(perf: dict[str, str], item: dict[str, Any] | None, error: str) -> dict[str, Any]:
    item_id = clean(perf.get("Item_ID"))
    perf_title = clean(perf.get("Title"))
    views = to_int(perf.get("Views_30_Days"))
    if item is None:
        return {
            "Item_ID": item_id,
            "Views_30_Days": views,
            "Perf_Title": perf_title,
            "API_Status": "ERROR",
            "Flags": "API_READ_FAILED",
            "Error": error,
        }
    category_path = clean(item.get("categoryPath"))
    api_title = clean(item.get("title"))
    product_type = infer_product_type(api_title or perf_title, category_path)
    urls = images(item)
    duplicate_images = len(urls) - len(set(urls))
    ship = shipping(item)
    ship_cost = to_float((ship.get("shippingCost") or {}).get("value"))
    brand = clean(item.get("brand"))
    short_description = clean(item.get("shortDescription"))
    avail = availability(item)
    regions = included_regions(item)
    flags: list[str] = []
    if product_type == "Sticker" and not re.search(r"stickers?|decals?|vinyl", category_path, re.I):
        flags.append("CATEGORY_MISMATCH_STICKER")
    if product_type in {"Poster", "Acrylic"} and not re.search(r"poster|wall art|photo|decor|acrylic", category_path, re.I):
        flags.append(f"CATEGORY_MISMATCH_{product_type.upper()}")
    if ship_cost > 0:
        flags.append("SHIPPING_NOT_FREE")
    if brand.lower() in {"", "generic", "ebay_product_rex"} or "ebay_product" in brand.lower():
        flags.append("BRAND_LOW_TRUST")
    if len(short_description) < 80:
        flags.append("SHORT_DESCRIPTION_THIN")
    if len(urls) < 4:
        flags.append("LOW_GALLERY_COUNT")
    if duplicate_images:
        flags.append("EXACT_DUPLICATE_IMAGE_URL")
    if clean(item.get("gtin")).lower() in {"", "does not apply"}:
        flags.append("NO_GTIN_CUSTOM_OK")
    if to_int(avail.get("estimatedRemainingQuantity")) <= 1:
        flags.append("QTY_ONE")
    if "Worldwide" in regions:
        flags.append("WORLDWIDE_SHIPPING_ENABLED")
    return {
        "Item_ID": item_id,
        "Views_30_Days": views,
        "Perf_Title": perf_title,
        "API_Status": "OK",
        "Product_Type_Inferred": product_type,
        "API_Title": api_title,
        "Category_Path": category_path,
        "Category_ID_Path": clean(item.get("categoryIdPath")),
        "Price": (item.get("price") or {}).get("value"),
        "Currency": (item.get("price") or {}).get("currency"),
        "Shipping_Cost": ship_cost,
        "Shipping_Type": clean(ship.get("type") or ship.get("shippingServiceCode")),
        "Brand": brand,
        "GTIN": clean(item.get("gtin")),
        "Condition": clean(item.get("condition")),
        "Quantity_Remaining": to_int(avail.get("estimatedRemainingQuantity")),
        "Quantity_Sold": to_int(avail.get("estimatedSoldQuantity")),
        "Image_Count": len(urls),
        "Duplicate_Image_URL_Count": duplicate_images,
        "Short_Description": short_description,
        "Item_Creation_Date": clean(item.get("itemCreationDate")),
        "Flags": "|".join(flags) if flags else "OK",
        "Error": "",
    }


def write_outputs(snapshot: str, rows: list[dict[str, Any]]) -> None:
    DATABASE.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    fields = [
        "Item_ID",
        "Views_30_Days",
        "Perf_Title",
        "API_Status",
        "Product_Type_Inferred",
        "API_Title",
        "Category_Path",
        "Category_ID_Path",
        "Price",
        "Currency",
        "Shipping_Cost",
        "Shipping_Type",
        "Brand",
        "GTIN",
        "Condition",
        "Quantity_Remaining",
        "Quantity_Sold",
        "Image_Count",
        "Duplicate_Image_URL_Count",
        "Short_Description",
        "Item_Creation_Date",
        "Flags",
        "Error",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    flag_counts = Counter()
    category_counts = Counter()
    for row in rows:
        category_counts[row.get("Category_Path") or "UNKNOWN"] += 1
        for flag in clean(row.get("Flags")).split("|"):
            if flag:
                flag_counts[flag] += 1
    lines = [
        "# eBay API Inventory / Category Audit",
        "",
        f"Generated: {now_et()}",
        f"SellerHub snapshot source: {snapshot or 'missing'}",
        f"Rows audited: {len(rows)}",
        "",
        "## Flag Counts",
        "",
    ]
    for flag, count in flag_counts.most_common():
        lines.append(f"- {flag}: {count}")
    lines.extend(["", "## Category Distribution", ""])
    for category, count in category_counts.most_common(20):
        lines.append(f"- {category}: {count}")
    lines.extend(
        [
            "",
            "## Immediate Interpretation",
            "",
            "- `SHIPPING_NOT_FREE` is a likely conversion/trust drag for low-ticket products. If Rex wants free-shipping positioning, price must include Printify shipping and marketplace fees.",
            "- `BRAND_LOW_TRUST` means eBay buyer-facing brand data still looks like an internal integration name instead of an intentional shop identity.",
            "- `SHORT_DESCRIPTION_THIN` means the public Browse surface may not show the richer description we wrote; this can hurt buyer trust and search snippet quality.",
            "- Category checks are read-only; any online repair should be staged as a separate, reviewed campaign.",
            "",
            f"CSV: {OUT_CSV}",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(target: str, limit: int) -> int:
    token = load_token()
    if not token:
        raise RuntimeError("Missing eBay OAuth token. Run eBay OAuth setup first.")
    snapshot, perf_rows = latest_performance_rows(target, limit)
    out = []
    for index, perf in enumerate(perf_rows, start=1):
        item_id = clean(perf.get("Item_ID"))
        status, item, error = browse_item_group(item_id, token)
        row = flag_row(perf, item, error)
        row["HTTP_Status"] = status
        out.append(row)
        print(f"[EBAY-AUDIT] {index}/{len(perf_rows)} item={item_id} status={status} flags={row.get('Flags')}")
    write_outputs(snapshot, out)
    print(f"[EBAY-AUDIT] rows={len(out)} csv={OUT_CSV} md={OUT_MD}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["zero-view", "viewed", "all"], default="zero-view")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    return run(args.target, args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
