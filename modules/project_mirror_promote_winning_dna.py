"""Promote Project Mirror A/B winners into production-ready DNA candidates.

This turns the draft-grid scorecard into a compact list that future Mentor Hub,
DeepSeek, or Printify product builders can consume. It is deliberately local:
no marketplace writes, no image upscale, and no fees.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REVIEW_DIR = PROJECT_ROOT / "Review_Packets" / "Project_Mirror"
SCORECARD_CSV = DATABASE_DIR / "Project_Mirror_AB_Scorecard.csv"
MENTOR_DRAFT_CSV = DATABASE_DIR / "Project_Mirror_Mentor_DNA_Draft.csv"
OUT_CSV = DATABASE_DIR / "Project_Mirror_Promoted_DNA.csv"
OUT_MD = REVIEW_DIR / "PROJECT_MIRROR_PROMOTED_DNA.md"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"

HEADERS = [
    "Promoted_ID",
    "Pair_ID",
    "Winning_Variant",
    "Score",
    "Category",
    "Layout",
    "Title",
    "Gold_Prompt_DNA",
    "Material_Keywords",
    "Product_Fit",
    "Promotion_Status",
    "Next_Action",
]


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def score_float(value: object) -> float:
    try:
        return float(clean(value))
    except ValueError:
        return 0.0


def build_rows() -> list[dict[str, str]]:
    score_rows = read_csv(SCORECARD_CSV)
    mentor_rows = {clean(row.get("DNA_ID")): row for row in read_csv(MENTOR_DRAFT_CSV)}
    promoted: list[dict[str, str]] = []
    seen_pairs: set[str] = set()

    winners = [row for row in score_rows if clean(row.get("Winner")).upper() == "YES"]
    winners.sort(key=lambda row: score_float(row.get("Score")), reverse=True)

    for idx, row in enumerate(winners, start=1):
        pair_id = clean(row.get("Pair_ID"))
        if not pair_id or pair_id in seen_pairs:
            continue
        seen_pairs.add(pair_id)

        draft = mentor_rows.get(pair_id, {})
        variant = clean(row.get("Variant"))
        if variant == "A_OLD_LOGIC":
            prompt = clean(draft.get("AB_Test_A_OldLogic"))
            next_action = "Use old-logic composition but refine materials and scene narrative before production."
        else:
            prompt = clean(draft.get("AB_Test_B_ProjectMirror")) or clean(draft.get("Gold_Prompt_DNA"))
            next_action = "Promote as reference-derived premium DNA for controlled poster/acrylic concept production."

        promoted.append(
            {
                "Promoted_ID": f"PM-WIN-{idx:03d}",
                "Pair_ID": pair_id,
                "Winning_Variant": variant,
                "Score": clean(row.get("Score")),
                "Category": clean(draft.get("Category")),
                "Layout": clean(draft.get("Layout")) or "Full_Frame",
                "Title": clean(draft.get("Title")) or pair_id,
                "Gold_Prompt_DNA": prompt,
                "Material_Keywords": clean(draft.get("Material_Keywords")),
                "Product_Fit": clean(draft.get("Product_Fit")),
                "Promotion_Status": "PROMOTED_DRAFT_NO_UPSCALE_NO_PUBLISH",
                "Next_Action": next_action,
            }
        )
    return promoted


def write_csv(rows: list[dict[str, str]]) -> None:
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Mirror Promoted DNA",
        "",
        f"Generated: {now_et().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        "These are draft-grid winners only. No upscale, publish, or marketplace spend has been triggered.",
        "",
        "| Rank | Pair | Winner | Score | Product Fit |",
        "| ---: | --- | --- | ---: | --- |",
    ]
    for idx, row in enumerate(rows, start=1):
        lines.append(
            f"| {idx} | {row['Pair_ID']} | {row['Winning_Variant']} | "
            f"{row['Score']} | {row['Product_Fit']} |"
        )
    lines.append("")
    for row in rows[:5]:
        lines.extend(
            [
                f"## {row['Promoted_ID']} - {row['Title']}",
                f"- Category: {row['Category']}",
                f"- Materials: {row['Material_Keywords']}",
                f"- Next action: {row['Next_Action']}",
                "",
                "```text",
                row["Gold_Prompt_DNA"],
                "```",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    top = rows[0] if rows else {}
    msg = (
        f"\n## {now_et().strftime('%Y-%m-%d %H:%M ET')} - Project Mirror promoted winners\n"
        f"- Promoted {len(rows)} A/B winners into `Database\\Project_Mirror_Promoted_DNA.csv`.\n"
        f"- Top winner: `{clean(top.get('Pair_ID'))}` via `{clean(top.get('Winning_Variant'))}` score `{clean(top.get('Score'))}`.\n"
        "- No upscale, publish, or fee action was taken.\n"
    )
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(msg)


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_md(rows)
    append_progress(rows)
    print(f"[PROJECT-MIRROR-PROMOTE] rows={len(rows)} csv={OUT_CSV}")
    if rows:
        print(
            "[PROJECT-MIRROR-PROMOTE] top="
            f"{rows[0]['Pair_ID']} {rows[0]['Winning_Variant']} score={rows[0]['Score']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
