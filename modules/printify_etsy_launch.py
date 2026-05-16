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
from modules.risk_guard import assert_allowed, assert_etsy_fee_batch_allowed, assert_no_first_audit_public_assets


DATABASE_DIR = PROJECT_ROOT / "Database"
PLAN_CSV = DATABASE_DIR / "Etsy_launch_plan.csv"
LOG_CSV = DATABASE_DIR / "Etsy_Printify_Launch_Log.csv"
STATE_JSON = DATABASE_DIR / "Etsy_Printify_Launch_State.json"
FEE_LEDGER_CSV = DATABASE_DIR / "Etsy_Fee_Ledger.csv"
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


def etsy_description(row: dict[str, str]) -> str:
    existing = str(row.get("Etsy_Description") or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if existing:
        return existing
    title = clean(row.get("Etsy_Title") or row.get("Title") or row.get("ID"))
    ptype = product_type(row.get("Product_Type", ""))
    category = clean(row.get("Category"))
    note = clean(row.get("Selection_Rationale"))
    if ptype == "Acrylic":
        product_note = "This 5x7 acrylic photo block is produced through Printify as a physical desk or shelf display piece with official product mockups."
    else:
        product_note = "This matte poster is produced through Printify as a physical wall art print with official product mockups."
    return (
        f"{title}\n\n"
        f"A curated {category or ptype} visual from Quiet Relic Studio, selected for collectible atmosphere, detailed material illusion, and room-ready presentation.\n\n"
        f"{product_note}\n\n"
        "Only the main product artwork is the final printed design. Additional gallery images are official product or concept previews to help show scale, texture, and display context.\n\n"
        f"Selection note: {note}" if note else
        f"{title}\n\n"
        f"A curated {category or ptype} visual from Quiet Relic Studio, selected for collectible atmosphere, detailed material illusion, and room-ready presentation.\n\n"
        f"{product_note}\n\n"
        "Only the main product artwork is the final printed design. Additional gallery images are official product or concept previews to help show scale, texture, and display context."
    )


def read_plan(plan_csv: Path = PLAN_CSV) -> list[dict[str, str]]:
    if not plan_csv.exists():
        raise FileNotFoundError(f"Missing Etsy launch plan: {plan_csv}")
    with plan_csv.open("r", encoding="utf-8-sig", newline="") as handle:
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


def etsy_spend_today() -> float:
    if not FEE_LEDGER_CSV.exists():
        return 0.0
    today = datetime.now().astimezone().date().isoformat()
    total = 0.0
    with FEE_LEDGER_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if not clean(row.get("Timestamp")).startswith(today):
                continue
            try:
                total += float(row.get("Confirmed_Spent_USD") or 0)
            except ValueError:
                continue
    return round(total, 2)


def append_fee_ledger(item_id: str, reference: str, status: str = "CONFIRMED_SPENT_PRINTIFY_ETSY") -> None:
    fieldnames = [
        "Timestamp",
        "Batch_ID",
        "ID",
        "Action",
        "Expected_Fee_USD",
        "Confirmed_Spent_USD",
        "Status",
        "Reference",
    ]
    exists = FEE_LEDGER_CSV.exists()
    with FEE_LEDGER_CSV.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "Timestamp": now_text(),
                "Batch_ID": "ETSY-POD-PRINTIFY",
                "ID": item_id,
                "Action": "ETSY_LISTING_FEE_RESERVE",
                "Expected_Fee_USD": "0.20",
                "Confirmed_Spent_USD": "0.20",
                "Status": status,
                "Reference": reference,
            }
        )


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
    payload = {
        "title": clean(row["Etsy_Title"])[:140],
        "description": etsy_description(row),
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
    assert_no_first_audit_public_assets(
        {"row": row, "payload": payload},
        context=f"Printify Etsy launch payload {clean(row.get('ID'))}",
    )
    return payload


def fetch_product(product_id: str) -> dict:
    response = requests.get(
        api_url(f"/shops/{SHOP_ID}/products/{product_id}.json"),
        headers=headers(content_type=False),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def put_product(product_id: str, payload: dict) -> dict:
    response = requests.put(
        api_url(f"/shops/{SHOP_ID}/products/{product_id}.json"),
        headers=headers(),
        json=payload,
        timeout=180,
    )
    response.raise_for_status()
    return response.json() if response.content else {}


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


def exact_duplicate_count(product: dict) -> int:
    seen: set[str] = set()
    duplicates = 0
    for image in product.get("images") or []:
        if image.get("is_selected_for_publishing") is False:
            continue
        key = clean(image.get("mockup_id")) or clean(image.get("src")).split("?")[0]
        if not key:
            continue
        if key in seen:
            duplicates += 1
        else:
            seen.add(key)
    return duplicates


def camera_label(image: dict) -> str:
    src = clean(image.get("src"))
    if "camera_label=" not in src:
        return ""
    return src.split("camera_label=", 1)[1].split("&", 1)[0]


def image_key(image: dict) -> str:
    return clean(image.get("mockup_id")) or clean(image.get("id")) or clean(image.get("src")).split("?")[0]


def selected_mix(product: dict) -> tuple[int, int, int]:
    selected = [image for image in product.get("images") or [] if image.get("is_selected_for_publishing") is not False]
    official = sum(1 for image in selected if "images.printify.com/mockup" in str(image.get("src") or ""))
    unique = len({image_key(image) for image in selected if image_key(image)})
    return len(selected), official, unique


def repair_duplicate_mockups(product_id: str, product_type_name: str) -> tuple[dict, str]:
    product = fetch_product(product_id)
    images = product.get("images") or []
    official = [image for image in images if "images.printify.com/mockup" in str(image.get("src") or "")]
    preferred = {
        "Poster": ["front", "close-up", "context-1", "context-2"],
        "Acrylic": ["front", "back", "side-1", "side-2", "context-1"],
    }.get(product_type_name, [])
    picked: list[dict] = []
    picked_keys: set[str] = set()
    for label in preferred:
        for image in official:
            key = image_key(image)
            if key and key not in picked_keys and camera_label(image) == label:
                picked.append(image)
                picked_keys.add(key)
                break
    for image in official:
        if len(picked) >= 4:
            break
        key = image_key(image)
        if key and key not in picked_keys:
            picked.append(image)
            picked_keys.add(key)
    if len(picked) < 3:
        return product, f"repair_skipped_unique_official={len(picked)}"
    selected_keys = {image_key(image) for image in picked}
    selected_order = {image_key(image): index for index, image in enumerate(picked)}
    repaired_images = []
    for image in images:
        item = dict(image)
        key = image_key(item)
        is_selected = key in selected_keys
        item["is_selected_for_publishing"] = is_selected
        item["is_default"] = is_selected and selected_order.get(key) == 0
        item["order"] = selected_order.get(key) if is_selected else None
        repaired_images.append(item)
    payload = dict(product)
    payload["images"] = repaired_images
    put_product(product_id, payload)
    updated = fetch_product(product_id)
    selected, official_count_after, unique_after = selected_mix(updated)
    note = f"dedup_repair selected={selected} official={official_count_after} unique={unique_after}"
    return updated, note


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


def run(limit: int, publish: bool, smoke: bool = False, plan_csv: Path = PLAN_CSV) -> None:
    if not SHOP_ID:
        raise RuntimeError("Printify_ETSY_SHOP_ID is not configured.")
    rows = [
        row
        for row in read_plan(plan_csv)
        if product_type(row.get("Product_Type")) in {"Poster", "Acrylic"}
        and clean(row.get("Launch_Status")).startswith("Draft_Prepared")
    ]
    done_ids = existing_launch_ids()
    rows = [row for row in rows if clean(row["ID"]) not in done_ids]
    if smoke:
        rows = rows[:1]
    elif limit:
        rows = rows[:limit]
    if publish and rows:
        assert_allowed("etsy", "paid_publish")
        assert_etsy_fee_batch_allowed(len(rows), daily_spend_so_far=etsy_spend_today())
    created = 0
    published = 0
    for row in rows:
        item_id = clean(row["ID"])
        try:
            product_id = create_product(row)
            product, selected, official = wait_mockups(product_id, minimum=3)
            duplicates = exact_duplicate_count(product)
            print(f"[ETSY-MOCKUPS] {item_id} product={product_id} selected={selected} official={official} duplicates={duplicates}", flush=True)
            if duplicates and product_type(row["Product_Type"]) in {"Poster", "Acrylic"}:
                product, repair_note = repair_duplicate_mockups(product_id, product_type(row["Product_Type"]))
                selected = selected_count(product)
                official = official_count(product)
                duplicates = exact_duplicate_count(product)
                print(
                    f"[ETSY-MOCKUPS-REPAIR] {item_id} product={product_id} "
                    f"{repair_note} duplicates={duplicates}",
                    flush=True,
                )
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
            if duplicates:
                append_log(
                    {
                        "Timestamp": now_text(),
                        "ID": item_id,
                        "Product_Type": product_type(row["Product_Type"]),
                        "Action": "MOCKUP_CHECK",
                        "Status": "HOLD_DUPLICATE_MOCKUPS",
                        "Printify_Etsy_Product_ID": product_id,
                        "Note": f"selected={selected} official={official} duplicate_count={duplicates}",
                    }
                )
                continue
            created += 1
            if publish:
                external_id, external_handle = publish_product(row, product_id)
                published += 1
                append_fee_ledger(item_id, external_id or external_handle or product_id)
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
                "plan_csv": str(plan_csv),
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
    parser.add_argument("--plan-csv", default=str(PLAN_CSV), help="Launch plan CSV to consume.")
    parser.add_argument("--delete-legacy", action="store_true")
    parser.add_argument("--delete-legacy-commit", action="store_true")
    args = parser.parse_args()
    if args.delete_legacy or args.delete_legacy_commit:
        delete_legacy_printify_products(dry_run=not args.delete_legacy_commit)
    else:
        run(limit=args.limit, publish=args.publish, smoke=args.smoke, plan_csv=Path(args.plan_csv))


if __name__ == "__main__":
    main()
