"""Build A/B Midjourney test queue for Project Mirror DNA drafts."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
IN_CSV = DATABASE_DIR / "Project_Mirror_Mentor_DNA_Draft.csv"
OUT_CSV = DATABASE_DIR / "Project_Mirror_AB_MJ_Test_Queue.csv"
OUT_MD = REVIEW_DIR / "PROJECT_MIRROR_AB_TEST_QUEUE.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

HEADERS = [
    "Test_ID",
    "DNA_ID",
    "Variant",
    "Category",
    "Title",
    "Product_Fit",
    "MJ_Prompt",
    "Status",
    "Output_Folder",
    "QA_Target",
    "Notes",
]


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def read_rows() -> list[dict[str, str]]:
    with IN_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def folder_for(dna_id: str, variant: str) -> str:
    safe = dna_id.replace(" ", "_").replace("/", "_")
    return str(PROJECT_ROOT / "Output" / "Project_Mirror" / safe / variant)


def build_queue() -> list[dict[str, str]]:
    queue = []
    for row in read_rows():
        dna_id = row["DNA_ID"]
        for variant, prompt_field, note in (
            ("A_OLD_LOGIC", "AB_Test_A_OldLogic", "baseline prompt style"),
            ("B_PROJECT_MIRROR", "AB_Test_B_ProjectMirror", "reference-derived premium DNA"),
        ):
            queue.append(
                {
                    "Test_ID": f"{dna_id}-{variant}",
                    "DNA_ID": dna_id,
                    "Variant": variant,
                    "Category": row["Category"],
                    "Title": row["Title"],
                    "Product_Fit": row["Product_Fit"],
                    "MJ_Prompt": row[prompt_field],
                    "Status": "READY_FOR_MJ_DRAFT_GRID",
                    "Output_Folder": folder_for(dna_id, variant),
                    "QA_Target": (
                        "judge premium physical-product feasibility, executive gift fit, material depth, "
                        "thumbnail clarity, and non-generic luxury signal"
                    ),
                    "Notes": note,
                }
            )
    return queue


def write_csv(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Mirror A/B MJ Test Queue",
        "",
        f"Generated: {now_et().strftime('%Y-%m-%d %H:%M %z')}",
        "",
        "Purpose: compare old prompt logic against Project Mirror reference-derived DNA before promoting new aesthetic DNA into Mentor Hub or production.",
        "",
        "Execution rule: draft grids only. No upscale. No marketplace publish.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['Test_ID']}",
                f"- Category: {row['Category']}",
                f"- Product fit: {row['Product_Fit']}",
                f"- QA target: {row['QA_Target']}",
                "",
                "```text",
                row["MJ_Prompt"],
                "```",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    by_variant: dict[str, int] = {}
    for row in rows:
        by_variant[row["Variant"]] = by_variant.get(row["Variant"], 0) + 1
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror A/B MJ Queue\n"
        f"- Built {len(rows)} draft-grid MJ test rows from 9 Project Mirror DNA drafts: {by_variant}.\n"
        f"- Output CSV: `{OUT_CSV}`; review packet: `{OUT_MD}`.\n"
        "- Queue is draft-grid only: no upscale, no publish, no fee.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    rows = build_queue()
    write_csv(rows)
    write_md(rows)
    append_progress(rows)
    print({"rows": len(rows), "csv": str(OUT_CSV), "review": str(OUT_MD)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
