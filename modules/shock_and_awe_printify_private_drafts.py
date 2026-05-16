"""Create Printify draft products for Shock & Awe V5 finalists.

These products are private fulfillment/showcase drafts only. This script never
calls Printify's publish endpoint and never syncs to eBay/Etsy.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules import printify_uploader


PRODUCTION = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Printify_Production_Files.csv"
PRIVATE_QUEUE = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Zone2_Printify_Private_Queue.csv"
OUTPUT = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Printify_Private_Drafts.csv"
NY_TZ = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return str(value or "").strip()


def headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {Config.Printify_API_KEY}",
        "Content-Type": "application/json",
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def private_map(path: Path = PRIVATE_QUEUE) -> dict[str, dict[str, str]]:
    return {clean(row.get("Internal_SKU")): row for row in read_csv(path)}


def existing_map(path: Path = OUTPUT) -> dict[str, dict[str, str]]:
    return {clean(row.get("Final_SKU")): row for row in read_csv(path)}


def title_for(final: dict[str, str], private: dict[str, str]) -> str:
    title = ""
    payload = clean(private.get("Payload_JSON"))
    if payload:
        try:
            title = clean(json.loads(payload).get("title"))
        except Exception:
            title = ""
    if not title:
        title = f"{clean(private.get('Concept_Name')) or clean(final.get('Final_SKU'))} - OpenClaw NYC Private Atelier"
    return title[:140]


def description_for(private: dict[str, str]) -> str:
    parts = [
        clean(private.get("Private_Copy")),
        clean(private.get("Cultural_Anchor")),
        clean(private.get("Placement_Scene")),
        clean(private.get("Objection_Reply")),
        "Private showcase draft only. Built for direct-client preview and future Printify fulfillment; not synced to public marketplaces.",
    ]
    return "\n\n".join(part for part in parts if part)


def create_payload(final: dict[str, str], private: dict[str, str], image_id: str) -> dict:
    variant_id = int(clean(final.get("Variant_ID")))
    price = int(round(float(clean(final.get("RRP_USD"))) * 100))
    return {
        "title": title_for(final, private),
        "description": description_for(private),
        "blueprint_id": int(clean(final.get("Blueprint_ID"))),
        "print_provider_id": int(clean(final.get("Provider_ID"))),
        "variants": [
            {
                "id": variant_id,
                "price": price,
                "is_enabled": True,
                "sku": clean(final.get("Final_SKU")),
            }
        ],
        "print_areas": [
            {
                "variant_ids": [variant_id],
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": image_id,
                                "x": 0.5,
                                "y": 0.5,
                                "scale": 1,
                                "angle": 0,
                            }
                        ],
                    }
                ],
            }
        ],
    }


def create_product(payload: dict) -> str:
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            response = requests.post(
                f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products.json",
                headers=headers(),
                json=payload,
                timeout=180,
            )
            response.raise_for_status()
            return clean(response.json().get("id"))
        except Exception as exc:
            last_error = exc
            print(f"[SHOCK-PRIVATE-DRAFT-RETRY] attempt={attempt} {exc}", flush=True)
            time.sleep(4 * attempt)
    raise RuntimeError(f"Printify product create failed: {last_error}")


def run(
    limit: int,
    dry_run: bool = False,
    production_csv: Path = PRODUCTION,
    private_queue_csv: Path = PRIVATE_QUEUE,
    output_csv: Path = OUTPUT,
) -> int:
    final_rows = read_csv(production_csv)
    private = private_map(private_queue_csv)
    existing = existing_map(output_csv)
    out_rows = list(existing.values())
    processed = 0
    for final in final_rows:
        if processed >= limit:
            break
        sku = clean(final.get("Final_SKU"))
        current = existing.get(sku)
        if current and clean(current.get("Draft_Status")) == "PRINTIFY_DRAFT_CREATED":
            continue
        source_private = private.get(sku, {})
        image_path = PROJECT_ROOT / clean(final.get("Production_Design_File"))
        if not image_path.exists():
            row = dict(final)
            row.update({"Draft_Status": "SOURCE_MISSING", "Draft_Error": str(image_path)})
            out_rows.append(row)
            continue
        if dry_run:
            print(f"[SHOCK-PRIVATE-DRAFT-DRY] {sku} {image_path}")
            processed += 1
            continue
        try:
            image_id = printify_uploader._image_upload(image_path, f"{sku}_Private_Production.png", allow_jpeg=True)
            payload = create_payload(final, source_private, image_id)
            product_id = create_product(payload)
            row = dict(final)
            row.update(
                {
                    "Printify_Image_ID": image_id,
                    "Printify_Product_ID": product_id,
                    "Draft_Status": "PRINTIFY_DRAFT_CREATED",
                    "Draft_Created_At_ET": datetime.now(NY_TZ).strftime("%Y-%m-%d %I:%M:%S %p %Z"),
                    "Publish_Policy": "PRIVATE_DRAFT_ONLY_DO_NOT_PUBLISH",
                    "Draft_Error": "",
                    "Printify_Title": payload["title"],
                }
            )
            out_rows = [r for r in out_rows if clean(r.get("Final_SKU")) != sku]
            out_rows.append(row)
            write_csv(output_csv, out_rows)
            print(f"[SHOCK-PRIVATE-DRAFT] {sku} product={product_id}", flush=True)
            processed += 1
        except Exception as exc:
            row = dict(final)
            row.update({"Draft_Status": "PRINTIFY_DRAFT_ERROR", "Draft_Error": repr(exc)[:500]})
            out_rows = [r for r in out_rows if clean(r.get("Final_SKU")) != sku]
            out_rows.append(row)
            write_csv(output_csv, out_rows)
            print(f"[SHOCK-PRIVATE-DRAFT-ERROR] {sku}: {exc}", flush=True)
            break
    write_csv(output_csv, out_rows)
    print(f"[SHOCK-PRIVATE-DRAFT-DONE] processed={processed} csv={output_csv}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Shock & Awe Printify private draft products")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--production-csv", type=Path, default=PRODUCTION)
    parser.add_argument("--private-queue-csv", type=Path, default=PRIVATE_QUEUE)
    parser.add_argument("--output-csv", type=Path, default=OUTPUT)
    args = parser.parse_args()
    return run(
        max(1, args.limit),
        dry_run=args.dry_run,
        production_csv=args.production_csv if args.production_csv.is_absolute() else PROJECT_ROOT / args.production_csv,
        private_queue_csv=args.private_queue_csv if args.private_queue_csv.is_absolute() else PROJECT_ROOT / args.private_queue_csv,
        output_csv=args.output_csv if args.output_csv.is_absolute() else PROJECT_ROOT / args.output_csv,
    )


if __name__ == "__main__":
    raise SystemExit(main())
