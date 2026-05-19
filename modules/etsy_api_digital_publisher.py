"""Publish Etsy digital download listings through Etsy Open API v3.

This is the API-first replacement for the temporary Edge UI bridge. It keeps
the same money guard: create/upload can produce drafts, but a listing is only
activated when the local fee guard allows the $0.20 listing fee and the active
state is confirmed by a follow-up read.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import etsy_api
from modules.etsy_digital_ui_publisher import (
    FEE_LEDGER_PATH,
    LOG_FIELDS,
    METADATA_PATH,
    QUEUE_PATH,
    UI_LOG_PATH,
    _append_csv,
    _clean,
    _confirmed_spend_today,
    _metadata_by_id,
    _preview_paths,
    _read_csv,
    _safe_digital_upload_path,
    _write_csv,
)
from modules.risk_guard import assert_allowed, assert_etsy_fee_batch_allowed, fee_kill_switch


DEFAULT_TAXONOMY_ID = 2078  # Digital Prints


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _tags(row: dict) -> list[str]:
    raw = row.get("Meta_Tags") or row.get("Tags") or ""
    parts = [re.sub(r"\s+", " ", part).strip() for part in str(raw).split(",")]
    tags = []
    seen = set()
    for tag in parts:
        if not tag:
            continue
        tag = tag[:20].strip()
        key = tag.lower()
        if key not in seen:
            tags.append(tag)
            seen.add(key)
        if len(tags) >= 13:
            break
    return tags


def _select_candidates(limit: int, preferred_ids: set[str] | None = None) -> list[dict]:
    metadata = _metadata_by_id()
    rows = []
    for row in _read_csv(QUEUE_PATH):
        if preferred_ids and row.get("ID") not in preferred_ids:
            continue
        if not row.get("QA_Status", "").startswith("PASS"):
            continue
        if row.get("Etsy_Listing_ID"):
            continue
        if row.get("Fee_Status") == "CONFIRMED_SPENT":
            continue
        if row.get("Launch_Status") not in {"READY_BLOCKED_ETSY_AUTH", "READY_TO_PUBLISH", "READY_UI_PUBLISH", "READY_API_PUBLISH"}:
            continue
        merged = dict(row)
        merged.update({f"Meta_{k}": v for k, v in (metadata.get(row.get("ID", "")) or {}).items()})
        rows.append(merged)
        if len(rows) >= limit:
            break
    return rows


def _update_queue(row_id: str, updates: dict) -> None:
    rows = _read_csv(QUEUE_PATH)
    for row in rows:
        if row.get("ID") == row_id:
            row.update({k: str(v) for k, v in updates.items()})
            break
    if rows:
        fieldnames = list(rows[0].keys())
        for key in updates:
            if key not in fieldnames:
                fieldnames.append(key)
        _write_csv(QUEUE_PATH, rows, fieldnames)


def _update_metadata(row_id: str, updates: dict) -> None:
    rows = _read_csv(METADATA_PATH)
    for row in rows:
        if row.get("ID") == row_id:
            row.update({k: str(v) for k, v in updates.items() if k in row})
            break
    if rows:
        _write_csv(METADATA_PATH, rows, list(rows[0].keys()))


def _log(row_id: str, status: str, listing_id: str = "", url: str = "", fee: float = 0.0, note: str = "") -> None:
    _append_csv(
        UI_LOG_PATH,
        [
            {
                "Timestamp": _now(),
                "ID": row_id,
                "Action": "API_PUBLISH",
                "Status": status,
                "Etsy_Listing_ID": listing_id,
                "URL": url,
                "Confirmed_Fee_USD": f"{fee:.2f}",
                "Note": note[:500],
            }
        ],
        LOG_FIELDS,
    )


def _reserve_fee(row_id: str, fee: float) -> None:
    ledger = _read_csv(FEE_LEDGER_PATH)
    ledger.append(
        {
            "Timestamp": _now(),
            "ID": row_id,
            "Action": "ETSY_LISTING_FEE_RESERVE",
            "Projected_Fee_USD": f"{fee:.2f}",
            "Confirmed_Spent_USD": "0.00",
            "Status": "RESERVED_NOT_SPENT_API",
            "Reference": "",
            "Notes": "Reserved before Etsy API activation; confirm active listing before marking spent.",
        }
    )
    fieldnames = list(ledger[0].keys()) if ledger else [
        "Timestamp",
        "ID",
        "Action",
        "Projected_Fee_USD",
        "Confirmed_Spent_USD",
        "Status",
        "Reference",
        "Notes",
    ]
    _write_csv(FEE_LEDGER_PATH, ledger, fieldnames)


def _confirm_fee(row_id: str, listing_id: str, fee: float) -> None:
    ledger = _read_csv(FEE_LEDGER_PATH)
    for row in reversed(ledger):
        if row.get("ID") == row_id and row.get("Status") == "RESERVED_NOT_SPENT_API":
            row["Confirmed_Spent_USD"] = f"{fee:.2f}"
            row["Status"] = "CONFIRMED_SPENT_API"
            row["Reference"] = listing_id
            break
    if ledger:
        _write_csv(FEE_LEDGER_PATH, ledger, list(ledger[0].keys()))


def create_draft_listing(shop_id: int, row: dict) -> dict:
    payload = {
        "quantity": 999,
        "title": _clean(row.get("Title") or row.get("Meta_Title"))[:140],
        "description": _clean(row.get("Meta_Description") or row.get("Description")),
        "price": str(row.get("Price") or row.get("Meta_Price") or "6.99"),
        "who_made": "i_did",
        "when_made": "2020_2026",
        "taxonomy_id": DEFAULT_TAXONOMY_ID,
        "type": "download",
        "is_supply": False,
        "should_auto_renew": False,
        "tags": _tags(row),
        "sku": [f"DIGITAL-{row['ID']}"],
    }
    return etsy_api.request("POST", f"/shops/{shop_id}/listings", json_body=payload)


def upload_images(shop_id: int, listing_id: int, row: dict) -> list[dict]:
    results = []
    for rank, image_path in enumerate(_preview_paths(row), start=1):
        path = Path(image_path)
        with path.open("rb") as handle:
            files = {"image": (path.name, handle, "image/jpeg")}
            data = {"rank": rank}
            results.append(etsy_api.request("POST", f"/shops/{shop_id}/listings/{listing_id}/images", data=data, files=files))
    return results


def _digital_upload_paths(row: dict) -> list[Path]:
    raw = str(row.get("Zip_Path") or "")
    parts = [part.strip() for part in raw.split(";") if part.strip()]
    if len(parts) <= 1:
        return [_safe_digital_upload_path(row)]

    paths: list[Path] = []
    for index, part in enumerate(parts, start=1):
        source = Path(part).resolve()
        if not source.exists():
            raise FileNotFoundError(source)
        upload_dir = source.parent / "_etsy_upload"
        upload_dir.mkdir(exist_ok=True)
        safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "-", str(row["ID"]))[:46].strip("-")
        target = upload_dir / f"OC-{safe_stem}-part-{index:02d}.zip"
        if not target.exists() or target.stat().st_mtime < source.stat().st_mtime or target.stat().st_size != source.stat().st_size:
            import shutil

            shutil.copy2(source, target)
        if len(target.name) > 70:
            raise ValueError(f"Etsy-safe upload filename is too long: {target.name}")
        paths.append(target)
    return paths


def upload_digital_file(shop_id: int, listing_id: int, row: dict) -> list[dict]:
    results = []
    for path in _digital_upload_paths(row):
        with path.open("rb") as handle:
            files = {"file": (path.name, handle, "application/zip")}
            results.append(etsy_api.request("POST", f"/shops/{shop_id}/listings/{listing_id}/files", data={"name": path.name}, files=files))
    return results


def activate_listing(shop_id: int, listing_id: int) -> dict:
    etsy_api.request("PATCH", f"/shops/{shop_id}/listings/{listing_id}", json_body={"state": "active"})
    return etsy_api.request("GET", f"/listings/{listing_id}")


def publish(limit: int = 1, dry_run: bool = False, draft_only: bool = False, ids: list[str] | None = None) -> dict:
    assert_allowed("etsy", "paid_publish")
    preferred = set(ids or []) or None
    candidates = _select_candidates(limit, preferred_ids=preferred)
    if not candidates:
        return {"selected": 0, "published": 0, "status": "NO_CANDIDATES"}
    if not draft_only:
        assert_etsy_fee_batch_allowed(len(candidates), daily_spend_so_far=_confirmed_spend_today())
    fee = float((fee_kill_switch() or {}).get("expected_listing_fee_usd", 0.20))
    if dry_run:
        return {"selected": len(candidates), "published": 0, "status": "DRY_RUN", "ids": [r["ID"] for r in candidates]}

    shop_id = int(etsy_api.first_shop_id())
    results = []
    for row in candidates:
        row_id = row["ID"]
        listing_id = ""
        try:
            draft = create_draft_listing(shop_id, row)
            listing_id = str(draft.get("listing_id") or "")
            if not listing_id:
                raise RuntimeError(f"Draft listing created without listing_id: {json.dumps(draft)[:500]}")
            _update_queue(row_id, {"Launch_Status": "API_DRAFT_CREATED", "Etsy_Listing_ID": listing_id, "Notes": "Draft created by Etsy API; media upload pending/complete."})
            upload_images(shop_id, int(listing_id), row)
            upload_digital_file(shop_id, int(listing_id), row)
            if draft_only:
                _log(row_id, "DRAFT_CREATED", listing_id, draft.get("url", ""), 0.0, "Draft plus media created; not activated, no listing fee confirmed.")
                results.append({"ID": row_id, "status": "DRAFT_CREATED", "listing_id": listing_id})
                continue
            _reserve_fee(row_id, fee)
            active = activate_listing(shop_id, int(listing_id))
            if active.get("state") != "active":
                raise RuntimeError(f"Activation not confirmed: {json.dumps(active)[:500]}")
            url = active.get("url") or f"https://www.etsy.com/listing/{listing_id}"
            _confirm_fee(row_id, listing_id, fee)
            _update_queue(
                row_id,
                {
                    "Launch_Status": "PUBLISHED_API_CONFIRMED",
                    "Fee_Status": "CONFIRMED_SPENT",
                    "Etsy_Listing_ID": listing_id,
                    "Shadow_Status": "PENDING_PUBLIC_PING",
                    "Shadow_Check_Due_At": (datetime.now().astimezone() + timedelta(hours=24)).isoformat(timespec="seconds"),
                    "Notes": f"Published via Etsy API at {url}",
                },
            )
            _update_metadata(row_id, {"Status": "PUBLISHED_ETSY_API_CONFIRMED"})
            _log(row_id, "CONFIRMED", listing_id, url, fee, "Published through Etsy Open API.")
            results.append({"ID": row_id, "status": "PUBLISHED", "listing_id": listing_id, "url": url})
        except Exception as exc:  # noqa: BLE001
            _log(row_id, "ERROR", listing_id, "", 0.0, f"{type(exc).__name__}: {_clean(exc)}")
            if listing_id:
                _update_queue(row_id, {"Launch_Status": "API_DRAFT_NEEDS_RECONCILE", "Etsy_Listing_ID": listing_id, "Notes": f"API publish error after draft creation: {_clean(exc)[:300]}"})
            results.append({"ID": row_id, "status": "ERROR", "listing_id": listing_id, "error": str(exc)[:500]})
            break
    return {"selected": len(candidates), "published": sum(1 for r in results if r["status"] == "PUBLISHED"), "results": results}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--draft-only", action="store_true")
    parser.add_argument("--id", action="append", default=[])
    args = parser.parse_args()
    print(json.dumps(publish(limit=args.limit, dry_run=args.dry_run, draft_only=args.draft_only, ids=args.id), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
