"""Create/publish a curated Etsy launch batch through the connected Printify shop.

Etsy Open API approval is not required for this path. Printify owns product
creation and marketplace push; Etsy UI/API is still needed for storefront shell
edits and deleting non-Printify legacy listings.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.printify_uploader import PRINTIFY_SPECS, _price_to_cents


DATABASE_DIR = PROJECT_ROOT / "Database"
PLAN_CSV = DATABASE_DIR / "Etsy_launch_plan.csv"
LOG_CSV = DATABASE_DIR / "Etsy_Printify_Launch_Log.csv"
STATE_JSON = DATABASE_DIR / "Etsy_Printify_Launch_State.json"
SHOP_ID = str(Config.Printify_ETSY_SHOP_ID or "")

PUBLISH_BODY = {
    "title": True,
    "description": True,
    "images": True,
    "variants": True,
    "tags": True,
    "keyFeatures": True,
    "shipping_template": True,
}


def now_text() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def headers(content_type: bool = True) -> dict[str, str]:
    result = {"Authorization": f"Bearer {Config.Printify_API_KEY}"}
    if content_type:
        result["Content-Type"] = "application/json"
    return result


def api_url(path: str) -> str:
    return f"{Config.Printify_API_URL.rstrip('/')}{path}"


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def read_plan() -> list[dict[str, str]]:
    if not PLAN_CSV.exists():
        raise FileNotFoundError(f"Missing Etsy launch plan: {PLAN_CSV}")
    with PLAN_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_log() -> list[dict[str, str]]:
    if not LOG_CSV.exists():
        return []
    with LOG_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def append_log(row: dict[str, str]) -> None:
    LOG_CSV.parent.mkdir(exist_ok=True)
    fieldnames = [
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
    exists = LOG_CSV.exists()
    with LOG_CSV.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in fieldnames})


def product_type(value: str) -> str:
    text = clean(value).lower()
    if text.startswith("poster"):
        return "Poster"
    if text.startswith("acry"):
        return "Acrylic"
    if text.startswith("stick"):
        return "Sticker"
    raise ValueError(f"Unsupported Etsy launch product type: {value}")


def image_upload(path: Path, item_id: str) -> str:
    upload_path = path
    if path.suffix.lower() == ".png" and path.stat().st_size > 3 * 1024 * 1024:
        out_dir = path.parent / "_printify_upload"
        out_dir.mkdir(exist_ok=True)
        upload_path = out_dir / f"{path.stem}_etsy_q92.jpg"
        if not upload_path.exists() or upload_path.stat().st_mtime < path.stat().st_mtime:
            with Image.open(path) as image:
                image.load()
                image.convert("RGB").save(upload_path, quality=92, optimize=True, progressive=True, subsampling=0)
    encoded = base64.b64encode(upload_path.read_bytes()).decode("utf-8")
    file_name = f"{item_id}_Etsy_Production_{int(time.time())}{upload_path.suffix}"
    last_error: Exception | None = None
    for attempt in range(1, 6):
        try:
            print(f"[ETSY-UPLOAD] {item_id} attempt={attempt} file={upload_path.name} size={len(encoded)//1024}KB", flush=True)
            response = requests.post(
                api_url("/uploads/images.json"),
                headers=headers(),
                json={"file_name": file_name, "contents": encoded},
                timeout=180,
            )
            response.raise_for_status()
            return response.json()["id"]
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt < 5:
                time.sleep(4 * attempt)
    raise RuntimeError(f"Image upload failed for {item_id}: {last_error}")


def build_payload(row: dict[str, str], production_image_id: str) -> dict:
    ptype = product_type(row["Product_Type"])
    spec = PRINTIFY_SPECS[ptype]
    variant_id = spec["variant_id"]
    tags = [clean(tag) for tag in clean(row.get("Etsy_Tags")).split(",") if clean(tag)]
    return {
        "title": clean(row["Etsy_Title"])[:140],
        "description": row["Etsy_Description"].replace("\r\n", "\n").replace("\r", "\n").strip(),
        "tags": tags[:13],
        "blueprint_id": spec["blueprint_id"],
        "print_provider_id": spec["provider_id"],
        "variants": [
            {
                "id": variant_id,
                "price": _price_to_cents(row.get("Price"), spec["default_price"]),
                "is_enabled": True,
                "sku": f"ETSY-{clean(row['ID'])}",
            }
        ],
        "print_areas": [
            {
                "variant_ids": [variant_id],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [{"id": production_image_id, "x": 0.5, "y": 0.5, "scale": 1, "angle": 0}],
                    }
                ],
            }
        ],
        # Deliberately omit custom gallery images for Etsy first pass.
        # Printify official mockups are safer for buyer expectation.
    }


def fetch_product(product_id: str) -> dict:
    response = requests.get(
        api_url(f"/shops/{SHOP_ID}/products/{product_id}.json"),
        headers=headers(content_type=False),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def create_product(row: dict[str, str]) -> str:
    item_id = clean(row["ID"])
    production_path = Path(clean(row["Production_Path"]))
    if not production_path.exists():
        raise FileNotFoundError(f"Missing production design for {item_id}: {production_path}")
    image_id = image_upload(production_path, item_id)
    payload = build_payload(row, image_id)
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            print(f"[ETSY-CREATE] {item_id} attempt={attempt}", flush=True)
            response = requests.post(
                api_url(f"/shops/{SHOP_ID}/products.json"),
                headers=headers(),
                json=payload,
                timeout=180,
            )
            response.raise_for_status()
            product_id = response.json()["id"]
            append_log(
                {
                    "Timestamp": now_text(),
                    "ID": item_id,
                    "Product_Type": product_type(row["Product_Type"]),
                    "Action": "CREATE",
                    "Status": "CREATED",
                    "Printify_Etsy_Product_ID": product_id,
                    "Note": "Created in Printify Etsy shop with official mockup-first policy.",
                }
            )
            return product_id
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt < 3:
                time.sleep(8 * attempt)
    raise RuntimeError(f"Product create failed for {item_id}: {last_error}")


def selected_count(product: dict) -> int:
    return sum(1 for image in product.get("images") or [] if image.get("is_selected_for_publishing") is not False)


def official_count(product: dict) -> int:
    return sum(
        1
        for image in product.get("images") or []
        if image.get("is_selected_for_publishing") is not False and "images.printify.com/mockup" in str(image.get("src") or "")
    )


def wait_mockups(product_id: str, minimum: int = 3, timeout: int = 120) -> tuple[dict, int, int]:
    deadline = time.time() + timeout
    last = {}
    while time.time() < deadline:
        last = fetch_product(product_id)
        selected = selected_count(last)
        official = official_count(last)
        if selected >= minimum and official >= 1:
            return last, selected, official
        time.sleep(8)
    return last or fetch_product(product_id), selected_count(last or {}), official_count(last or {})


def publish_product(row: dict[str, str], product_id: str) -> tuple[str, str]:
    item_id = clean(row["ID"])
    response = requests.post(
        api_url(f"/shops/{SHOP_ID}/products/{product_id}/publish.json"),
        headers=headers(),
        json=PUBLISH_BODY,
        timeout=180,
    )
    response.raise_for_status()
    external_id = ""
    external_handle = ""
    for _ in range(10):
        product = fetch_product(product_id)
        external = product.get("external") or {}
        external_id = clean(external.get("id"))
        external_handle = clean(external.get("handle"))
        if external_id or external_handle:
            break
        time.sleep(8)
    append_log(
        {
            "Timestamp": now_text(),
            "ID": item_id,
            "Product_Type": product_type(row["Product_Type"]),
            "Action": "PUBLISH",
            "Status": "PUBLISHED" if external_id or external_handle else "PUBLISHED_EXTERNAL_PENDING",
            "Printify_Etsy_Product_ID": product_id,
            "External_ID": external_id,
            "External_Handle": external_handle,
            "Note": f"Printify publish HTTP {response.status_code}",
        }
    )
    return external_id, external_handle


def existing_launch_ids() -> set[str]:
    ids = set()
    for row in read_log():
        if clean(row.get("Status")) in {"CREATED", "PUBLISHED", "PUBLISHED_EXTERNAL_PENDING"}:
            ids.add(clean(row.get("ID")))
    return ids


def run(limit: int, publish: bool, smoke: bool = False) -> None:
    if not SHOP_ID:
        raise RuntimeError("Printify_ETSY_SHOP_ID is not configured.")
    rows = [row for row in read_plan() if product_type(row.get("Product_Type")) in {"Poster", "Acrylic"}]
    done_ids = existing_launch_ids()
    rows = [row for row in rows if clean(row["ID"]) not in done_ids]
    if smoke:
        rows = rows[:1]
    elif limit:
        rows = rows[:limit]
    created = 0
    published = 0
    for row in rows:
        item_id = clean(row["ID"])
        try:
            product_id = create_product(row)
            product, selected, official = wait_mockups(product_id, minimum=3)
            print(f"[ETSY-MOCKUPS] {item_id} product={product_id} selected={selected} official={official}", flush=True)
            if selected < 3 or official < 1:
                append_log(
                    {
                        "Timestamp": now_text(),
                        "ID": item_id,
                        "Product_Type": product_type(row["Product_Type"]),
                        "Action": "MOCKUP_CHECK",
                        "Status": "HOLD_MOCKUP_INSUFFICIENT",
                        "Printify_Etsy_Product_ID": product_id,
                        "Note": f"selected={selected} official={official}",
                    }
                )
                continue
            created += 1
            if publish:
                external_id, external_handle = publish_product(row, product_id)
                published += 1
                print(f"[ETSY-PUBLISH] {item_id} product={product_id} external={external_id or external_handle or 'PENDING'}")
        except Exception as exc:  # noqa: BLE001
            append_log(
                {
                    "Timestamp": now_text(),
                    "ID": item_id,
                    "Product_Type": clean(row.get("Product_Type")),
                    "Action": "ERROR",
                    "Status": "FAILED",
                    "Note": str(exc),
                }
            )
            print(f"[ETSY-FAIL] {item_id}: {exc}", flush=True)
    STATE_JSON.write_text(
        json.dumps(
            {
                "timestamp": now_text(),
                "shop_id": SHOP_ID,
                "attempted": len(rows),
                "created": created,
                "published": published,
                "publish_requested": publish,
                "log": str(LOG_CSV),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"[ETSY-DONE] attempted={len(rows)} created={created} published={published} publish={publish}")


def delete_legacy_printify_products(dry_run: bool = True) -> None:
    response = requests.get(api_url(f"/shops/{SHOP_ID}/products.json?limit=50"), headers=headers(content_type=False), timeout=120)
    response.raise_for_status()
    products = response.json().get("data") or []
    launch_products = {clean(row.get("Printify_Etsy_Product_ID")) for row in read_log()}
    deleted = 0
    for product in products:
        product_id = clean(product.get("id"))
        title = clean(product.get("title"))
        if product_id in launch_products:
            continue
        if title and ("kiss-cut stickers" in title.lower() or "drive" in title.lower() or product.get("external", {}).get("id") == ""):
            print(f"[ETSY-LEGACY-DELETE{'-DRY' if dry_run else ''}] {product_id} {title}")
            if not dry_run:
                resp = requests.delete(api_url(f"/shops/{SHOP_ID}/products/{product_id}.json"), headers=headers(), timeout=120)
                print(f"  -> http={resp.status_code}")
                deleted += int(resp.status_code in {200, 202, 204})
    print(f"[ETSY-LEGACY-DONE] deleted={deleted} dry_run={dry_run}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--delete-legacy", action="store_true")
    parser.add_argument("--delete-legacy-commit", action="store_true")
    args = parser.parse_args()
    if args.delete_legacy or args.delete_legacy_commit:
        delete_legacy_printify_products(dry_run=not args.delete_legacy_commit)
    else:
        run(limit=args.limit, publish=args.publish, smoke=args.smoke)


if __name__ == "__main__":
    main()
