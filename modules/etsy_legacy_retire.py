"""Delete explicitly approved legacy Etsy listings through the logged-in UI."""

from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
LOG_PATH = DATABASE / "Etsy_Legacy_Retirement_Log.csv"

APPROVED_LEGACY = {
    "4407466791": "Impulse Purchase Recovery Kit",
    "4366700475": "DriverFuel_SideHustle_Driver_Planner_Kit",
}

FIELDS = [
    "Timestamp",
    "Etsy_Listing_ID",
    "Expected_Title_Fragment",
    "Action",
    "Status",
    "Public_Status",
    "Notes",
]


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _append(row: dict) -> None:
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def _click_visible_button_with_text(page, text: str, prefer_last: bool = False) -> bool:
    """Click a visible button whose visible innerText exactly matches text.

    Etsy image-delete icon buttons expose "Delete" as an accessible name but
    have empty innerText. Using innerText avoids deleting listing photos when
    we mean the listing-level menu command.
    """
    script = """
    ({ text, preferLast }) => {
      const buttons = [...document.querySelectorAll('button')].filter((button) => {
        const visible = !!(button.offsetWidth || button.offsetHeight || button.getClientRects().length);
        return visible && !button.disabled && (button.innerText || '').trim() === text;
      });
      if (!buttons.length) return false;
      const button = preferLast ? buttons[buttons.length - 1] : buttons[0];
      button.click();
      return true;
    }
    """
    return bool(page.evaluate(script, {"text": text, "preferLast": prefer_last}))


def _public_status(context, listing_id: str) -> tuple[str, str]:
    page = context.new_page()
    try:
        page.goto(f"https://www.etsy.com/listing/{listing_id}", wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3000)
        body = page.locator("body").inner_text(timeout=12000).lower()
        if (
            "this listing is no longer available" in body
            or "listing is unavailable" in body
            or "this item is unavailable" in body
            or "sorry, this item is unavailable" in body
            or "uh oh" in body
        ):
            return "NOT_ACTIVE", ""
        if "etsy" in body:
            return "STILL_READABLE", body[:180]
        return "UNKNOWN", body[:180]
    except Exception as exc:  # noqa: BLE001
        return "ERROR", str(exc)[:180]
    finally:
        page.close()


def delete_listing(context, listing_id: str, expected_title: str, dry_run: bool = False) -> dict:
    row = {
        "Timestamp": _now(),
        "Etsy_Listing_ID": listing_id,
        "Expected_Title_Fragment": expected_title,
        "Action": "DRY_RUN" if dry_run else "DELETE",
        "Status": "ERROR",
        "Public_Status": "",
        "Notes": "",
    }
    page = context.new_page()
    try:
        page.goto(f"https://www.etsy.com/your/shops/me/listing-editor/edit/{listing_id}", wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(4500)
        body = page.locator("body").inner_text(timeout=15000)
        if expected_title.lower() not in body.lower():
            row["Status"] = "SKIPPED_TITLE_MISMATCH"
            row["Notes"] = body[:220].replace("\n", " ")
            return row
        if "Active" not in body:
            row["Notes"] = "Listing page did not expose Active status before delete."

        if dry_run:
            row["Status"] = "READY_TO_DELETE"
            return row

        page.get_by_role("button", name="More options").click(timeout=10000)
        page.wait_for_timeout(1000)
        if not _click_visible_button_with_text(page, "Delete", prefer_last=False):
            raise RuntimeError("Could not find listing-level Delete menu item.")
        page.wait_for_timeout(1200)
        if not _click_visible_button_with_text(page, "Delete", prefer_last=True):
            raise RuntimeError("Could not find delete confirmation button.")
        try:
            page.wait_for_url(re.compile(r".*/tools/listings.*|.*/listing-editor/.*"), timeout=20000)
        except PlaywrightTimeoutError:
            pass
        page.wait_for_timeout(4000)
        public_status, note = _public_status(context, listing_id)
        row["Public_Status"] = public_status
        row["Status"] = "DELETED_CONFIRMED" if public_status == "NOT_ACTIVE" else "DELETE_ATTEMPTED_REVIEW"
        row["Notes"] = note
        if public_status != "NOT_ACTIVE":
            row["Notes"] = (row["Notes"] + " | Delete did not deactivate public page; trying Deactivate fallback.").strip()
            page.goto(f"https://www.etsy.com/your/shops/me/listing-editor/edit/{listing_id}", wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(4000)
            page.get_by_role("button", name="More options").click(timeout=10000)
            page.wait_for_timeout(1000)
            if not _click_visible_button_with_text(page, "Deactivate", prefer_last=False):
                raise RuntimeError("Could not find listing-level Deactivate menu item.")
            page.wait_for_timeout(1200)
            if not _click_visible_button_with_text(page, "Deactivate", prefer_last=True):
                raise RuntimeError("Could not find deactivate confirmation button.")
            page.wait_for_timeout(5000)
            public_status, note = _public_status(context, listing_id)
            row["Public_Status"] = public_status
            row["Status"] = "DEACTIVATED_CONFIRMED" if public_status == "NOT_ACTIVE" else "DEACTIVATE_ATTEMPTED_REVIEW"
            row["Notes"] = (row["Notes"] + " | Fallback: " + note).strip()
    except Exception as exc:  # noqa: BLE001
        row["Status"] = "ERROR"
        row["Notes"] = str(exc)[:240]
    finally:
        page.close()
    return row


def run(limit: int, port: int, dry_run: bool = False) -> list[dict]:
    results: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        for listing_id, title in list(APPROVED_LEGACY.items())[:limit]:
            row = delete_listing(context, listing_id, title, dry_run=dry_run)
            _append(row)
            results.append(row)
            print(f"[etsy-legacy-retire] {listing_id} {row['Status']} {row.get('Public_Status','')}")
        browser.close()
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete approved legacy Etsy listings.")
    parser.add_argument("--limit", type=int, default=2)
    parser.add_argument("--port", type=int, default=9223)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.limit, args.port, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
