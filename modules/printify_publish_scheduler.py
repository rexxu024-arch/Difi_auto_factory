import argparse
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from openpyxl import load_workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules import ebay_ads_standard


EBAY_BOOK = PROJECT_ROOT / "Database" / "eBay_listing.xlsx"
PUBLISHABLE_PREFIXES = ("Printify_UI_Mockups",)
RETRYABLE_EXTERNAL_PENDING_PREFIXES = ("Printify_PublishExternalPending_Mockups",)
PUBLISHED_PREFIXES = ("Printify_Published", "Printify_Published_Mockups")
PUBLISH_BODY = {
    "title": True,
    "description": True,
    "images": True,
    "variants": True,
    "tags": True,
    "keyFeatures": True,
    "shipping_template": True,
}


def _headers():
    return {
        "Authorization": f"Bearer {Config.Printify_API_KEY}",
        "Content-Type": "application/json",
    }


def _product_type(value):
    text = str(value or "").strip().lower()
    if text.startswith("poster"):
        return "Poster"
    if text.startswith("acry"):
        return "Acrylic"
    if text.startswith("stick"):
        return "Sticker"
    return "Other"


def _publish_suffix(status):
    text = str(status or "")
    if "Mockups" in text:
        return text.split("Mockups", 1)[1]
    return ""


def _fetch_product(product_id):
    response = requests.get(
        f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products/{product_id}.json",
        headers={"Authorization": _headers()["Authorization"]},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _selected_count(product):
    return sum(1 for image in product.get("images") or [] if image.get("is_selected_for_publishing") is not False)


def _selected_images(product):
    return [
        image
        for image in product.get("images") or []
        if image.get("is_selected_for_publishing") is not False
    ]


def _ensure_column(ws, cols, name):
    if name not in cols:
        ws.cell(1, ws.max_column + 1).value = name
        cols[name] = ws.max_column
    return cols[name]


def _sync_external_id_for_row(ws, cols, row_idx, item_id, product_id, attempts=5, delay=12):
    ebay_col = _ensure_column(ws, cols, "eBay_Item_ID")
    url_col = _ensure_column(ws, cols, "eBay_Item_URL")
    type_col = _ensure_column(ws, cols, "External_Type")
    sync_col = _ensure_column(ws, cols, "External_Sync_Timestamp")
    existing = str(ws.cell(row_idx, ebay_col).value or "").strip()
    if existing:
        return existing, "existing"
    for attempt in range(1, attempts + 1):
        product = _fetch_product(product_id)
        external = product.get("external") or {}
        ebay_id = str(external.get("id") or "").strip()
        if ebay_id:
            ws.cell(row_idx, ebay_col).value = ebay_id
            ws.cell(row_idx, url_col).value = str(external.get("handle") or "").strip()
            ws.cell(row_idx, type_col).value = str(external.get("type") or "").strip()
            ws.cell(row_idx, sync_col).value = datetime.now()
            return ebay_id, f"synced_attempt_{attempt}"
        if attempt < attempts:
            time.sleep(delay)
    return "", "missing_external_id"


def _preflight(row):
    product_id = str(row.get("Printify_Product_ID") or "").strip()
    if not product_id:
        return False, "missing Printify_Product_ID"
    product = _fetch_product(product_id)
    if not product.get("print_areas"):
        return False, "missing print_areas"
    selected_images = _selected_images(product)
    selected = len(selected_images)
    selected_srcs = [str(image.get("src") or "") for image in selected_images]
    if len(set(selected_srcs)) != len(selected_srcs):
        return False, f"selected gallery contains duplicate image URLs: selected={selected}, unique={len(set(selected_srcs))}"
    defaults = [image for image in selected_images if image.get("is_default")]
    product_type = _product_type(row.get("Product_Type"))
    if product_type == "Sticker" and selected < 3:
        return False, f"selected mockups={selected}, expected >=3 official cover mockups"
    if product_type == "Sticker":
        custom_gallery = [
            image for image in selected_images
            if "pfy-prod-products-mockup-media" in str(image.get("src") or "")
        ]
        if custom_gallery:
            return False, f"sticker custom gallery images selected={len(custom_gallery)}; use cover-only official mockups before publish"
    if product_type == "Poster" and selected < 4:
        return False, f"selected mockups={selected}, expected >=4"
    if product_type == "Poster" and any("pfy-prod-products-mockup-media" in src for src in selected_srcs):
        return False, "poster custom gallery images selected; use official product mockups only"
    if product_type == "Acrylic" and selected < 4:
        return False, f"selected mockups={selected}, expected >=4"
    if product_type == "Acrylic" and any("pfy-prod-products-mockup-media" in src for src in selected_srcs):
        return False, "acrylic custom gallery images selected; use official product mockups only"
    if len(defaults) < 1:
        return False, "default image count=0, expected at least 1 before publish"
    return True, f"selected mockups={selected}, defaults={len(defaults)}"


def _publish(product_id):
    last_error = None
    for attempt in range(1, 4):
        try:
            response = requests.post(
                f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products/{product_id}/publish.json",
                headers=_headers(),
                json=PUBLISH_BODY,
                timeout=180,
            )
            if response.status_code in {200, 201, 202, 204}:
                return response.status_code
            response.raise_for_status()
        except Exception as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(8 * attempt)
    raise last_error


def _load_publishable(limit, product_cycle, ids=None, retry_pending=False):
    wanted_ids = {str(item).strip() for item in (ids or []) if str(item).strip()}
    wb = load_workbook(EBAY_BOOK)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    cols = {header: idx + 1 for idx, header in enumerate(headers)}
    if "Publish_Timestamp" not in cols:
        ws.cell(1, ws.max_column + 1).value = "Publish_Timestamp"
        cols["Publish_Timestamp"] = ws.max_column
    buckets = {product_type: [] for product_type in product_cycle}
    for row_idx in range(2, ws.max_row + 1):
        row_id = str(ws.cell(row_idx, cols["ID"]).value or "").strip()
        if wanted_ids and row_id not in wanted_ids:
            continue
        status = str(ws.cell(row_idx, cols["Status"]).value or "")
        allowed_prefixes = PUBLISHABLE_PREFIXES + (RETRYABLE_EXTERNAL_PENDING_PREFIXES if retry_pending else ())
        if status.startswith(PUBLISHED_PREFIXES) or not status.startswith(allowed_prefixes):
            continue
        product_type = _product_type(ws.cell(row_idx, cols["Product_Type"]).value)
        if product_type not in buckets:
            continue
        row = {header: ws.cell(row_idx, cols[header]).value for header in headers if header in cols}
        row["_row_idx"] = row_idx
        buckets[product_type].append(row)

    selected = []
    while len(selected) < limit and any(buckets.values()):
        for product_type in product_cycle:
            if buckets[product_type] and len(selected) < limit:
                selected.append(buckets[product_type].pop(0))
    return wb, ws, cols, selected


def run(limit=8, min_delay=90, max_delay=240, product_cycle=None, dry_run=False, ids=None, retry_pending=False):
    product_cycle = product_cycle or ["Poster", "Acrylic", "Sticker"]
    wb, ws, cols, rows = _load_publishable(limit, product_cycle, ids=ids, retry_pending=retry_pending)
    done = 0
    try:
        for row in rows:
            item_id = row["ID"]
            product_id = str(row.get("Printify_Product_ID") or "").strip()
            row_idx = row["_row_idx"]
            try:
                ok, note = _preflight(row)
                if not ok:
                    print(f"[PUBLISH-SKIP] {item_id}: {note}")
                    continue
                if dry_run:
                    print(f"[PUBLISH-DRY] {item_id} product={product_id} {note}")
                    continue
                code = _publish(product_id)
                suffix = _publish_suffix(row.get("Status"))
                ws.cell(row_idx, cols["Publish_Timestamp"]).value = datetime.now()
                ebay_id, external_note = _sync_external_id_for_row(ws, cols, row_idx, item_id, product_id)
                if ebay_id:
                    ws.cell(row_idx, cols["Status"]).value = f"Printify_Published_Mockups{suffix}" if suffix else "Printify_Published"
                else:
                    ws.cell(row_idx, cols["Status"]).value = (
                        f"Printify_PublishExternalPending_Mockups{suffix}" if suffix else "Printify_PublishExternalPending"
                    )
                if ebay_id:
                    ads_ok = ebay_ads_standard.enroll_listing(item_id, ebay_id)
                    ads_note = "ads_enrolled" if ads_ok else "ads_queued"
                else:
                    ads_note = "ads_waiting_for_external_id"
                done += 1 if ebay_id else 0
                wb.save(EBAY_BOOK)
                print(
                    f"[PUBLISH-OK] {item_id} product={product_id} http={code} {note} "
                    f"external={external_note} ebay={ebay_id or 'MISSING'} {ads_note}"
                )
                if done < len(rows):
                    delay = random.randint(min_delay, max_delay)
                    print(f"[PUBLISH-SLEEP] {delay}s")
                    time.sleep(delay)
            except Exception as exc:
                print(f"[PUBLISH-FAIL] {item_id}: {exc}")
                continue
    finally:
        wb.close()
    print(f"[DONE] publish attempted={len(rows)} external_confirmed={done}")
    return done


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--min-delay", type=int, default=90)
    parser.add_argument("--max-delay", type=int, default=240)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cycle", default="Poster,Acrylic,Sticker")
    parser.add_argument("--ids", default="", help="Comma-separated listing IDs to publish exactly.")
    parser.add_argument("--retry-pending", action="store_true", help="Explicitly retry Printify_PublishExternalPending rows.")
    args = parser.parse_args()
    cycle = [part.strip() for part in args.cycle.split(",") if part.strip()]
    ids = [part.strip() for part in args.ids.split(",") if part.strip()]
    run(
        limit=args.limit,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        product_cycle=cycle,
        dry_run=args.dry_run,
        ids=ids,
        retry_pending=args.retry_pending,
    )


if __name__ == "__main__":
    main()
