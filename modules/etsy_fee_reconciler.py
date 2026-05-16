from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
QUEUE = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
LEDGER = DATABASE / "Etsy_Fee_Ledger.csv"
METADATA = DATABASE / "Digital_Etsy_Metadata.csv"
RECON_LOG = DATABASE / "Etsy_Fee_Reconciliation_Log.csv"
NY = ZoneInfo("America/New_York")


def now() -> datetime:
    return datetime.now(NY)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def append_csv(path: Path, rows: list[dict[str, str]], headers: list[str]) -> None:
    exists = path.exists()
    with path.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def parse_time(value: str) -> datetime | None:
    value = str(value or "").strip()
    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S %z"]:
        try:
            parsed = datetime.strptime(value, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=NY)
            return parsed
        except ValueError:
            pass
    return None


def reconcile(max_age_minutes: int = 30, execute: bool = False) -> dict[str, int]:
    queue_rows = read_csv(QUEUE)
    ledger_rows = read_csv(LEDGER)
    metadata_rows = read_csv(METADATA)
    cutoff = now() - timedelta(minutes=max_age_minutes)
    releasable_ids: set[str] = set()
    log_rows: list[dict[str, str]] = []

    for row in queue_rows:
        item_id = row.get("ID", "")
        if row.get("Fee_Status") != "RESERVED_NOT_SPENT":
            continue
        if row.get("Etsy_Listing_ID"):
            continue
        if row.get("Launch_Status") not in {"READY_BLOCKED_ETSY_AUTH", "READY_TO_PUBLISH", "READY_UI_PUBLISH", "READY_API_PUBLISH"}:
            continue
        ts = parse_time(row.get("Timestamp", ""))
        if ts and ts > cutoff:
            continue
        releasable_ids.add(item_id)
        log_rows.append(
            {
                "Timestamp": now().isoformat(timespec="seconds"),
                "ID": item_id,
                "Batch_ID": row.get("Batch_ID", ""),
                "Action": "RELEASE_RESERVED_NOT_SPENT",
                "Execute": str(execute),
                "Reason": "No Etsy listing id and confirmed spent is 0.00; old auth-block reservation should not occupy the fee pool.",
            }
        )

    if execute and releasable_ids:
        for row in queue_rows:
            if row.get("ID") in releasable_ids and row.get("Fee_Status") == "RESERVED_NOT_SPENT" and not row.get("Etsy_Listing_ID"):
                row["Fee_Status"] = "RELEASED_NOT_SPENT"
                row["Launch_Status"] = "RELEASED_TO_DRAFT_QUEUE"
                row["Notes"] = "Released by etsy_fee_reconciler; no listing was created and no fee was confirmed spent."
        for row in ledger_rows:
            if row.get("ID") in releasable_ids and row.get("Status") == "RESERVED_NOT_SPENT" and not row.get("Reference"):
                row["Status"] = "RELEASED_NOT_SPENT"
        for row in metadata_rows:
            if row.get("ID") in releasable_ids and row.get("Status") == "GRAY_QUEUE_RESERVED_NOT_SPENT":
                row["Status"] = "READY_FOR_ETSY_DRAFT"
        if queue_rows:
            write_csv(QUEUE, queue_rows, list(queue_rows[0].keys()))
        if ledger_rows:
            write_csv(LEDGER, ledger_rows, list(ledger_rows[0].keys()))
        if metadata_rows:
            write_csv(METADATA, metadata_rows, list(metadata_rows[0].keys()))
    if log_rows:
        append_csv(RECON_LOG, log_rows, ["Timestamp", "ID", "Batch_ID", "Action", "Execute", "Reason"])
    return {"candidates": len(releasable_ids), "released": len(releasable_ids) if execute else 0}


def main() -> None:
    parser = argparse.ArgumentParser(description="Release stale Etsy fee reservations that never spent money.")
    parser.add_argument("--max-age-minutes", type=int, default=30)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    result = reconcile(max_age_minutes=args.max_age_minutes, execute=args.execute)
    print(f"[ETSY-FEE-RECON] candidates={result['candidates']} released={result['released']} execute={args.execute}")


if __name__ == "__main__":
    main()
