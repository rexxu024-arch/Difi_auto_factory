"""Hold Adobe Stock MJ rows that reused another row's grid.

This prevents a weak prompt-signature match from turning old Discord grids into
new stock assets. The raw downloaded files stay on disk for traceability, but
held rows are removed from candidate flow by clearing grid/U file pointers.
"""

from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
QUEUE = DATABASE / "Adobe_Stock_Daily_MJ_Dispatch_Queue.csv"
REPORT = REVIEW / "Adobe_Stock_MJ_Duplicate_Guard_latest.md"
NY_TZ = ZoneInfo("America/New_York")


EXTRA_FIELDS = [
    "Duplicate_Guard_Status",
    "Duplicate_Guard_Reason",
    "Duplicate_Guard_Checked_ET",
]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        for field in EXTRA_FIELDS:
            if field not in fields:
                fields.append(field)
        return list(reader), fields


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def file_hash(value: str) -> str:
    path = resolve_path(value)
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hold_row(row: dict[str, str], reason: str) -> None:
    preserved = []
    for field in ("Grid_File", "U1_File", "U2_File", "U3_File", "U4_File"):
        if clean(row.get(field)):
            preserved.append(f"{field}={row[field]}")
        row[field] = ""
    row["Harvest_Status"] = "HARVEST_HOLD_DUPLICATE_GRID_ID"
    row["Duplicate_Guard_Status"] = "HOLD"
    row["Duplicate_Guard_Reason"] = reason
    row["Duplicate_Guard_Checked_ET"] = now_text()
    existing_error = clean(row.get("Harvest_Error"))
    trace = "; ".join(preserved)
    row["Harvest_Error"] = "Duplicate grid guard hold: " + reason + (f" | preserved {trace}" if trace else "")
    if existing_error and existing_error not in row["Harvest_Error"]:
        row["Harvest_Error"] += f" | previous: {existing_error[:180]}"


def audit(queue: Path = QUEUE) -> tuple[int, int, list[str]]:
    if not queue.exists():
        raise FileNotFoundError(f"Missing queue: {queue}")
    rows, fields = read_rows(queue)
    id_groups: dict[str, list[int]] = defaultdict(list)
    grid_hash_groups: dict[str, list[int]] = defaultdict(list)
    asset_hash_groups: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for idx, row in enumerate(rows):
        grid_id = clean(row.get("Grid_Message_ID"))
        if grid_id:
            id_groups[grid_id].append(idx)
        grid_file = clean(row.get("Grid_File"))
        digest = file_hash(grid_file) if grid_file else ""
        if digest:
            grid_hash_groups[digest].append(idx)
        for field in ("U1_File", "U2_File", "U3_File", "U4_File"):
            asset_file = clean(row.get(field))
            asset_digest = file_hash(asset_file) if asset_file else ""
            if asset_digest:
                asset_hash_groups[asset_digest].append((idx, field))

    held = 0
    reasons: list[str] = []
    for grid_id, indexes in id_groups.items():
        if len(indexes) <= 1:
            continue
        keeper = indexes[0]
        for idx in indexes[1:]:
            sku = clean(rows[idx].get("Internal_SKU"))
            keeper_sku = clean(rows[keeper].get("Internal_SKU"))
            reason = f"Grid_Message_ID {grid_id} already assigned to {keeper_sku}"
            hold_row(rows[idx], reason)
            reasons.append(f"{sku}: {reason}")
            held += 1

    for digest, indexes in grid_hash_groups.items():
        active_indexes = [idx for idx in indexes if clean(rows[idx].get("Duplicate_Guard_Status")) != "HOLD"]
        if len(active_indexes) <= 1:
            continue
        keeper = active_indexes[0]
        for idx in active_indexes[1:]:
            sku = clean(rows[idx].get("Internal_SKU"))
            keeper_sku = clean(rows[keeper].get("Internal_SKU"))
            reason = f"Grid file hash already assigned to {keeper_sku}; sha256={digest[:16]}"
            hold_row(rows[idx], reason)
            reasons.append(f"{sku}: {reason}")
            held += 1

    for digest, matches in asset_hash_groups.items():
        active_matches = [
            (idx, field)
            for idx, field in matches
            if clean(rows[idx].get("Duplicate_Guard_Status")) != "HOLD"
        ]
        active_indexes = []
        seen_indexes = set()
        for idx, _field in active_matches:
            if idx not in seen_indexes:
                active_indexes.append(idx)
                seen_indexes.add(idx)
        if len(active_indexes) <= 1:
            continue
        keeper = active_indexes[0]
        keeper_sku = clean(rows[keeper].get("Internal_SKU"))
        for idx in active_indexes[1:]:
            sku = clean(rows[idx].get("Internal_SKU"))
            reason = f"U-button asset hash already assigned to {keeper_sku}; sha256={digest[:16]}"
            hold_row(rows[idx], reason)
            reasons.append(f"{sku}: {reason}")
            held += 1

    checked = sum(1 for row in rows if clean(row.get("Grid_Message_ID")) or clean(row.get("Grid_File")))
    write_rows(queue, rows, fields)
    write_report(checked, held, reasons)
    append_progress(checked, held)
    return checked, held, reasons


def write_report(checked: int, held: int, reasons: list[str]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Adobe Stock MJ Duplicate Guard",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Grid rows checked: {checked}",
        f"- Rows held: {held}",
        "",
        "## Holds",
        "",
    ]
    if reasons:
        lines.extend(f"- {reason}" for reason in reasons)
    else:
        lines.append("- None")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(checked: int, held: int) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock MJ duplicate guard checked={checked}; held={held}; no upload/spend.\n"
        )


def main() -> int:
    checked, held, _ = audit()
    print(f"[ADOBE-MJ-DUP-GUARD] checked={checked} held={held} report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
