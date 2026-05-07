"""Audit live Etsy listing pages from the staged OpenClaw digital queue."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATABASE = PROJECT_ROOT / "Database"
QUEUE_PATH = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
AUDIT_PATH = DATABASE / "Etsy_Digital_Live_Audit.csv"

FIELDS = [
    "Timestamp",
    "ID",
    "Etsy_Listing_ID",
    "URL",
    "Status",
    "Title",
    "Price_Text",
    "Digital_Signal",
    "Image_Count",
    "Notes",
]


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _append_rows(rows: list[dict]) -> None:
    exists = AUDIT_PATH.exists()
    with AUDIT_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def _published_candidates(limit: int, ids: set[str] | None = None) -> list[dict]:
    rows = []
    for row in _read_rows(QUEUE_PATH):
        listing_id = str(row.get("Etsy_Listing_ID") or "").strip()
        item_id = str(row.get("ID") or "").strip()
        if not listing_id:
            continue
        if ids and item_id not in ids and listing_id not in ids:
            continue
        rows.append(row)
        if len(rows) >= limit:
            break
    return rows


def audit_listing(page, row: dict) -> dict:
    listing_id = str(row.get("Etsy_Listing_ID") or "").strip()
    item_id = str(row.get("ID") or "").strip()
    url = f"https://www.etsy.com/listing/{listing_id}"
    result = {
        "Timestamp": _now(),
        "ID": item_id,
        "Etsy_Listing_ID": listing_id,
        "URL": url,
        "Status": "ERROR",
        "Title": "",
        "Price_Text": "",
        "Digital_Signal": "UNKNOWN",
        "Image_Count": "",
        "Notes": "",
    }
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3500)
        body = page.locator("body").inner_text(timeout=15000)
        lower = body.lower()
        if "this listing is no longer available" in lower or "listing is unavailable" in lower:
            result["Status"] = "NOT_ACTIVE"
        elif "etsy" in lower and (item_id.lower() in lower or "digital" in lower or "download" in lower):
            result["Status"] = "ACTIVE_READABLE"
        else:
            result["Status"] = "READABLE_UNCERTAIN"

        title = ""
        for selector in ["h1", "[data-buy-box-region='title']"]:
            try:
                title = page.locator(selector).first.inner_text(timeout=3000).strip()
                if title:
                    break
            except Exception:
                pass
        result["Title"] = re.sub(r"\s+", " ", title)[:240]

        price = ""
        try:
            price_candidates = re.findall(r"(?:US\s*)?\$[0-9]+(?:\.[0-9]{2})?", body)
            if price_candidates:
                price = price_candidates[0]
        except Exception:
            pass
        result["Price_Text"] = price
        result["Digital_Signal"] = "YES" if ("digital download" in lower or "instant download" in lower or "download files" in lower) else "NO"
        try:
            result["Image_Count"] = str(page.locator("img").count())
        except Exception:
            result["Image_Count"] = ""
    except PlaywrightTimeoutError as exc:
        result["Status"] = "TIMEOUT"
        result["Notes"] = str(exc)[:240]
    except Exception as exc:  # noqa: BLE001
        result["Status"] = "ERROR"
        result["Notes"] = str(exc)[:240]
    return result


def run(limit: int, ids: set[str] | None, port: int, close_tabs: bool) -> list[dict]:
    candidates = _published_candidates(limit, ids)
    if not candidates:
        print("[etsy-live-audit] no published candidates")
        return []
    results: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        for row in candidates:
            page = context.new_page()
            result = audit_listing(page, row)
            results.append(result)
            print(f"[etsy-live-audit] {result['ID']} {result['Etsy_Listing_ID']} {result['Status']} {result['Digital_Signal']}")
            if close_tabs:
                page.close()
        browser.close()
    _append_rows(results)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit live Etsy public listing pages.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--ids", default="", help="Comma-separated local IDs or Etsy listing IDs.")
    parser.add_argument("--port", type=int, default=9223)
    parser.add_argument("--keep-tabs", action="store_true")
    args = parser.parse_args()
    ids = {part.strip() for part in args.ids.split(",") if part.strip()} or None
    run(args.limit, ids, args.port, close_tabs=not args.keep_tabs)


if __name__ == "__main__":
    main()
