"""Recover unconfirmed Midjourney dispatch rows after a safe wait.

Discord can occasionally return 204 for an interaction that never produces a
stable Midjourney channel echo. Those rows are not reliable submissions and can
block the monthly loop forever. This utility only resets rows that have no
confirmed message id and have aged beyond a conservative wait window.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NY_TZ = ZoneInfo("America/New_York")


def clean(value: object) -> str:
    return str(value or "").strip()


def parse_et(value: str) -> datetime | None:
    text = clean(value)
    if text.endswith((" EDT", " EST")):
        text = text.rsplit(" ", 1)[0]
    for fmt in ("%Y-%m-%d %I:%M:%S %p %Z", "%Y-%m-%d %I:%M:%S %p", "%Y-%m-%d %H:%M:%S %Z", "%Y-%m-%d %H:%M:%S"):
        try:
            parsed = datetime.strptime(text, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=NY_TZ)
            return parsed.astimezone(NY_TZ)
        except ValueError:
            continue
    return None


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    for field in ["Recovery_At_ET", "Recovery_Note"]:
        if field not in fields:
            fields.append(field)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def recover(queue: Path, min_age_minutes: int) -> int:
    rows, fields = read_rows(queue)
    now = datetime.now(NY_TZ)
    touched = 0
    for row in rows:
        if clean(row.get("Dispatch_Status")) != "MJ_SUBMIT_UNCONFIRMED_RETRY":
            continue
        if clean(row.get("Dispatch_Confirm_Message_ID")):
            continue
        dispatched_at = parse_et(clean(row.get("Dispatched_At_ET")))
        if not dispatched_at:
            continue
        age_minutes = int((now - dispatched_at).total_seconds() // 60)
        if age_minutes < min_age_minutes:
            continue
        prior_error = clean(row.get("Dispatch_Error"))
        row["Dispatch_Status"] = "READY_FOR_MJ"
        row["Dispatch_Response_Status"] = ""
        row["Dispatch_Error"] = ""
        row["Recovery_At_ET"] = now.strftime("%Y-%m-%d %I:%M:%S %p %Z")
        row["Recovery_Note"] = (
            f"Reset after unconfirmed Discord 204 aged {age_minutes}m without Midjourney echo. "
            f"Prior error: {prior_error[:180]}"
        )
        touched += 1
    if touched:
        write_rows(queue, rows, fields)
    print(f"[MJ-UNCONFIRMED-RECOVER] queue={queue} recovered={touched} min_age={min_age_minutes}m")
    return touched


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", required=True)
    parser.add_argument("--min-age-minutes", type=int, default=10)
    args = parser.parse_args()
    queue = (PROJECT_ROOT / args.queue).resolve() if not Path(args.queue).is_absolute() else Path(args.queue)
    recover(queue, args.min_age_minutes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
