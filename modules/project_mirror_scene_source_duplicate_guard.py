"""Hold Project Mirror scene rows whose source artwork duplicates prior rows.

This guard runs before dispatching more Midjourney scene mockups. It prevents a
near-duplicate source design from consuming another scene pair and later leaking
as repeated marketplace/gallery assets.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUEUE = PROJECT_ROOT / "Database" / "Project_Mirror_Identity_Locked_Scene_Dispatch_Queue.csv"
PRESELECT = PROJECT_ROOT / "Database" / "Project_Mirror_Identity_Locked_Scene_Preselect.csv"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")


def now_et() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M ET")


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_rows(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def visual_hash(path: Path, size: int = 12) -> str:
    image = Image.open(path).convert("L").resize((size, size), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if px >= avg else "0" for px in pixels)


def hamming(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right))


def source_group(row: dict[str, str]) -> str:
    concept = clean(row.get("Concept_Name"))
    return concept.split()[0] if concept else clean(row.get("Internal_SKU")).rsplit("-", 1)[0]


def main() -> int:
    if not QUEUE.exists():
        print("[PM-SCENE-SOURCE-GUARD] queue missing")
        return 0
    headers, rows = read_rows(QUEUE)
    if "Review_Note" not in headers:
        headers.append("Review_Note")
    seen: list[tuple[str, str, str]] = []
    held_groups: set[str] = set()
    if PRESELECT.exists():
        _, preselect_rows = read_rows(PRESELECT)
        for pre in preselect_rows:
            if "DUPLICATE" in clean(pre.get("Decision")):
                queue_id = clean(pre.get("Queue_ID"))
                if queue_id:
                    held_groups.add(queue_id.rsplit("-", 1)[0].replace("PM-SCENE", "PM-PREMIUM"))
    changed = 0
    for row in rows:
        group = source_group(row)
        raw_path = clean(row.get("Reference_Image_Path"))
        path = Path(raw_path)
        if not path.exists():
            continue
        sig = visual_hash(path)
        duplicate_of = ""
        for prior_sig, prior_group, prior_sku in seen:
            if prior_group != group and hamming(sig, prior_sig) <= 6:
                duplicate_of = f"{prior_group} via {prior_sku}"
                break
        if duplicate_of:
            held_groups.add(group)
        else:
            seen.append((sig, group, clean(row.get("Internal_SKU"))))

    for row in rows:
        group = source_group(row)
        if group not in held_groups:
            continue
        if clean(row.get("Dispatch_Status")) == "READY_FOR_MJ":
            row["Dispatch_Status"] = "HOLD_SOURCE_DUPLICATE"
            changed += 1
        note = clean(row.get("Review_Note"))
        marker = "source duplicate hold"
        if marker not in note.lower():
            row["Review_Note"] = f"{note}; Source duplicate hold: visually overlaps an earlier Project Mirror premium candidate.".strip("; ")

    if changed:
        write_rows(QUEUE, headers, rows)
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Project Mirror scene source duplicate guard\n"
            f"- Held READY scene rows from {len(held_groups)} duplicate source group(s); changed={changed}.\n"
            "- This prevents repeated scene galleries before MJ dispatch; no upscale, publish, or fee.\n"
        )
    print(f"[PM-SCENE-SOURCE-GUARD] duplicate_groups={len(held_groups)} changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
