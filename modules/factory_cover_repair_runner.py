"""Run one recoverable Printify-source cover repair and live eBay audit.

This runner is intentionally single-item by default. It turns the learned manual
cover repair process into a resumable queue:

1. Check network and Printify CDP login.
2. Pick one SOURCE_REPAIR_REQUIRED decision.
3. Re-upload/select Printify mockups through the hardened UI uploader.
4. Verify Printify selected/default image counts.
5. Re-audit the live eBay buyer image.
6. Mark the decision row with the next state.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import ebay_online_cover_audit, factory_supervisor, network_guard
from modules.printify_mockup_ui_uploader import _default_count, _fetch_product, _selected_count


DATABASE_DIR = PROJECT_ROOT / "Database"
DECISIONS = DATABASE_DIR / "eBay_Cover_Repair_Decisions.csv"
RUN_LOG = DATABASE_DIR / "Cover_Repair_Run_Log.csv"

DECISION_HEADERS = [
    "ID",
    "Product_Type",
    "eBay_Item_ID",
    "Printify_Product_ID",
    "Online_Result",
    "Best_U_Label",
    "Repair_Method",
    "Repair_Note",
    "Cover_Path",
    "Status",
]

LOG_HEADERS = [
    "Timestamp",
    "ID",
    "Stage",
    "Status",
    "Detail",
]


def now_text() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_decisions() -> list[dict[str, str]]:
    if not DECISIONS.exists():
        return []
    with DECISIONS.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_decisions(rows: list[dict[str, str]]) -> None:
    headers = DECISION_HEADERS[:]
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with DECISIONS.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def append_log(item_id: str, stage: str, status: str, detail: str) -> None:
    exists = RUN_LOG.exists()
    with RUN_LOG.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_HEADERS)
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "Timestamp": now_text(),
                "ID": item_id,
                "Stage": stage,
                "Status": status,
                "Detail": detail[:1200],
            }
        )


def pick_candidate(rows: list[dict[str, str]], ids: list[str] | None = None) -> dict[str, str] | None:
    id_set = set(ids or [])
    allowed_statuses = {"", "PENDING", "WAIT_SOURCE_REPAIR_RESULT", "SOURCE_REPAIR_FAILED", "SOURCE_REPAIR_DONE_LIVE_STILL_BAD"}
    candidates = []
    for row in rows:
        if clean(row.get("Repair_Method")) != "SOURCE_REPAIR_REQUIRED":
            continue
        if id_set and clean(row.get("ID")) not in id_set:
            continue
        if clean(row.get("Status")) not in allowed_statuses:
            continue
        candidates.append(row)
    candidates.sort(key=lambda row: (clean(row.get("Product_Type")) != "Sticker", clean(row.get("ID"))))
    return candidates[0] if candidates else None


def set_decision_status(rows: list[dict[str, str]], item_id: str, status: str) -> None:
    for row in rows:
        if clean(row.get("ID")) == item_id:
            row["Status"] = status
            row["Last_Repair_Attempt"] = now_text()
            break
    write_decisions(rows)


def run_uploader(item_id: str, expected_count: int, publish: bool, timeout: int) -> subprocess.CompletedProcess:
    command = [
        sys.executable,
        str(PROJECT_ROOT / "modules" / "printify_mockup_ui_uploader.py"),
        "--ids",
        item_id,
        "--allow-any-status",
        "--expected-count",
        str(expected_count),
    ]
    if publish:
        command.append("--publish")
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def verify_printify(product_id: str, expected_count: int) -> tuple[bool, str]:
    product = _fetch_product(product_id)
    selected = _selected_count(product)
    defaults = _default_count(product)
    ok = selected >= expected_count and defaults >= 1
    return ok, f"selected={selected} expected_at_least={expected_count} defaults={defaults}"


def run(limit: int = 1, ids: list[str] | None = None, dry_run: bool = False, post_sync_wait: int = 120) -> int:
    ui = factory_supervisor.printify_ui_status()
    if ui["status"] != "LOGGED_IN":
        append_log("", "preflight", "WAIT_PRINTIFY_LOGIN", f"{ui['status']} - {ui['reason']}")
        print(f"[COVER-REPAIR-WAIT] Printify UI: {ui['status']} - {ui['reason']}")
        return 2

    strategy = network_guard.report(count=2)["strategy"]
    if strategy["mode"] == "pause":
        append_log("", "preflight", "WAIT_NETWORK", str(strategy))
        print(f"[COVER-REPAIR-WAIT] network={strategy}")
        return 2

    repaired = 0
    for _ in range(max(1, limit)):
        rows = read_decisions()
        candidate = pick_candidate(rows, ids=ids)
        if not candidate:
            print("[COVER-REPAIR] no candidate")
            return 0 if repaired else 1
        item_id = clean(candidate.get("ID"))
        product_id = clean(candidate.get("Printify_Product_ID"))
        expected_count = 5
        if not item_id or not product_id:
            set_decision_status(rows, item_id, "BLOCKED_MISSING_ID")
            append_log(item_id, "pick", "BLOCKED", "Missing ID or Printify product id")
            continue
        if dry_run:
            print(f"[COVER-REPAIR-DRY] {item_id} product={product_id}")
            append_log(item_id, "dry_run", "READY", product_id)
            return 0

        set_decision_status(rows, item_id, "SOURCE_REPAIR_RUNNING")
        append_log(item_id, "source_repair", "START", product_id)
        print(f"[COVER-REPAIR] repairing {item_id} product={product_id}")
        try:
            result = run_uploader(item_id, expected_count=expected_count, publish=True, timeout=900)
        except subprocess.TimeoutExpired as exc:
            rows = read_decisions()
            set_decision_status(rows, item_id, "SOURCE_REPAIR_TIMEOUT")
            append_log(item_id, "source_repair", "TIMEOUT", str(exc))
            print(f"[COVER-REPAIR-TIMEOUT] {item_id}")
            return 2

        output = (result.stdout or "").strip()
        append_log(item_id, "source_repair", f"EXIT_{result.returncode}", output)
        if result.returncode != 0 or "[MOCKUP-UI-FAIL]" in output:
            rows = read_decisions()
            set_decision_status(rows, item_id, "SOURCE_REPAIR_FAILED")
            print(f"[COVER-REPAIR-FAIL] {item_id}\n{output[-1200:]}")
            return 2

        ok, note = verify_printify(product_id, expected_count=expected_count)
        append_log(item_id, "printify_verify", "OK" if ok else "CHECK", note)
        if not ok:
            rows = read_decisions()
            set_decision_status(rows, item_id, "SOURCE_REPAIR_DEFAULT_CHECK_FAILED")
            print(f"[COVER-REPAIR-CHECK] {item_id} {note}")
            return 2

        if post_sync_wait > 0:
            print(f"[COVER-REPAIR] waiting {post_sync_wait}s before live audit")
            time.sleep(post_sync_wait)

        audit_records = ebay_online_cover_audit.run(
            ids=[item_id],
            limit=1,
            wait_seconds=5.0,
            source_mode="workbook",
        )
        live_result = clean(audit_records[0].get("Result")) if audit_records else "ERROR"
        rows = read_decisions()
        if live_result == "LIKELY_COVER":
            set_decision_status(rows, item_id, "LIVE_COVER_FIXED")
        elif live_result == "LIKELY_SINGLE_U_MISMATCH":
            set_decision_status(rows, item_id, "SOURCE_REPAIR_DONE_LIVE_STILL_BAD")
        else:
            set_decision_status(rows, item_id, f"LIVE_AUDIT_{live_result or 'UNKNOWN'}")
        append_log(item_id, "live_audit", live_result, str(audit_records[0] if audit_records else {}))
        print(f"[COVER-REPAIR-DONE] {item_id} live={live_result}")
        repaired += 1
        if ids:
            break
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--ids", default="", help="Comma-separated local IDs to repair first.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--post-sync-wait", type=int, default=120)
    args = parser.parse_args()
    ids = [part.strip() for part in args.ids.split(",") if part.strip()] or None
    raise SystemExit(run(limit=args.limit, ids=ids, dry_run=args.dry_run, post_sync_wait=args.post_sync_wait))


if __name__ == "__main__":
    main()
