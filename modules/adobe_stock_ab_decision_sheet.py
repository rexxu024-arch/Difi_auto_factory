"""Codex decision sheet for Adobe Stock A/B draft grids.

This converts Rex-visible draft grids into an execution queue:
- recommended U-button full-resolution candidates
- remake/hold reasons
- no upload and no upscale performed by this script
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"
QUEUE = DATABASE / "Adobe_Stock_Codex_AB_MJ_Dispatch_Queue.csv"
OUT = DATABASE / "Adobe_Stock_AB_Codex_Decision.csv"
REPORT = REVIEW / "Adobe_Stock_AB_Codex_Decision_latest.md"
ET = ZoneInfo("America/New_York")


# Draft-grid decisions after visual review of
# Review_Packets/Adobe_Stock_AB_Review/adobe_stock_ab_contact_sheet_latest.jpg
# U quadrant is MJ's 2x2 layout: U1 top-left, U2 top-right, U3 bottom-left, U4 bottom-right.
DECISIONS: dict[str, dict[str, str]] = {
    "ADOBE-AB-01-A": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "A",
        "Recommended_U": "U1",
        "Reason": "Most commercially safe white kintsugi marble; clean background, likely usable for packaging and design layouts.",
    },
    "ADOBE-AB-01-C": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "A",
        "Recommended_U": "U2",
        "Reason": "Darker editorial kintsugi variation gives premium contrast without becoming a finished OpenClaw product.",
    },
    "ADOBE-AB-02-A": {
        "Decision": "REMAKE_BEFORE_UPSCALE",
        "Priority": "C",
        "Recommended_U": "",
        "Reason": "Too object-like/crystalline for a clean stock background; remake as macro jade slab with flatter commercial layout.",
    },
    "ADOBE-AB-02-C": {
        "Decision": "HOLD_DO_NOT_UPSCALE",
        "Priority": "D",
        "Recommended_U": "",
        "Reason": "Reads as silk/fog, not smoky jade; low buyer expectation match.",
    },
    "ADOBE-AB-03-A": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "A",
        "Recommended_U": "U2",
        "Reason": "Strong walnut burl texture, high commercial relevance for interiors, branding, product backgrounds.",
    },
    "ADOBE-AB-03-C": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "B",
        "Recommended_U": "U4",
        "Reason": "More continuous walnut grain; useful as a secondary wood background if U image stays sharp.",
    },
    "ADOBE-AB-04-A": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "A",
        "Recommended_U": "U4",
        "Reason": "Aged bronze patina has depth and luxury material character; good for premium background search intent.",
    },
    "ADOBE-AB-04-C": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "B",
        "Recommended_U": "U1",
        "Reason": "Editorial bronze backdrop with copy-space potential; keep if U output is not muddy.",
    },
    "ADOBE-AB-05-A": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "A",
        "Recommended_U": "U1",
        "Reason": "Nero marble is direct stock-market material demand; high contrast, useful, low concept risk.",
    },
    "ADOBE-AB-05-C": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "B",
        "Recommended_U": "U1",
        "Reason": "Cleaner dark-marble editorial variant; acceptable as a second Nero candidate if not too similar.",
    },
    "ADOBE-AB-06-A": {
        "Decision": "SELECT_FOR_U_BUTTON",
        "Priority": "C",
        "Recommended_U": "U2",
        "Reason": "Technically usable brushed metal, but common and less distinctive; only upgrade after A/B candidates.",
    },
    "ADOBE-AB-06-C": {
        "Decision": "HOLD_DO_NOT_UPSCALE",
        "Priority": "D",
        "Recommended_U": "",
        "Reason": "Too blurred/generic, low commercial download pull versus existing stock competition.",
    },
}


FIELDS = [
    "Internal_SKU",
    "Concept_Name",
    "Decision",
    "Priority",
    "Recommended_U",
    "Grid_File",
    "Next_Action",
    "Reason",
    "Adobe_Title",
    "Adobe_Keywords",
]


def now_text() -> str:
    return datetime.now(ET).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def next_action(decision: str, recommended_u: str) -> str:
    if decision == "SELECT_FOR_U_BUTTON":
        return f"Click {recommended_u}; then hold the selected full-resolution U file until Adobe image QA passes."
    if decision == "REMAKE_BEFORE_UPSCALE":
        return "Regenerate prompt; do not spend upscale on current grid."
    return "Hold; no upscale, no upload."


def build() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in read_rows(QUEUE):
        sku = row.get("Internal_SKU", "")
        if sku not in DECISIONS:
            continue
        decision = DECISIONS[sku]
        out.append(
            {
                "Internal_SKU": sku,
                "Concept_Name": row.get("Concept_Name", ""),
                "Decision": decision["Decision"],
                "Priority": decision["Priority"],
                "Recommended_U": decision["Recommended_U"],
                "Grid_File": row.get("Grid_File", ""),
                "Next_Action": next_action(decision["Decision"], decision["Recommended_U"]),
                "Reason": decision["Reason"],
                "Adobe_Title": row.get("Adobe_Title", ""),
                "Adobe_Keywords": row.get("Adobe_Keywords", ""),
            }
        )
    return out


def write_report(rows: list[dict[str, str]]) -> None:
    selected = [row for row in rows if row["Decision"] == "SELECT_FOR_U_BUTTON"]
    remake = [row for row in rows if row["Decision"] == "REMAKE_BEFORE_UPSCALE"]
    held = [row for row in rows if row["Decision"] == "HOLD_DO_NOT_UPSCALE"]
    lines = [
        "# Adobe Stock A/B Codex Decision Sheet",
        "",
        f"Generated: {now_text()}",
        "",
        "## Summary",
        "",
        f"- Draft grids reviewed: {len(rows)}",
        f"- Select for U-button: {len(selected)}",
        f"- Remake before upscale: {len(remake)}",
        f"- Hold / no upscale: {len(held)}",
        "- Upload status: NO UPLOAD. These are draft-grid decisions only.",
        "- Cost rule: no Fast, no creative upscale for Adobe Stock; use relaxed U-button full-resolution outputs only.",
        "",
        "## Selected Upgrade Candidates",
        "",
    ]
    for row in selected:
        lines.append(
            f"- **{row['Internal_SKU']}** ({row['Priority']}) -> {row['Recommended_U']}: "
            f"{row['Concept_Name']} - {row['Reason']}"
        )
    lines.extend(["", "## Remake / Hold", ""])
    for row in remake + held:
        lines.append(f"- **{row['Internal_SKU']}** -> {row['Decision']}: {row['Reason']}")
    lines.extend(
        [
            "",
            "## Next Safe Step",
            "",
            "Run relaxed U-button harvest only for A/B priority candidates when thermal guard allows. "
            "After U files exist, require selected-U full-resolution provenance and `adobe_stock_image_qa.py` before any Contributor upload.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    selected = sum(1 for row in rows if row["Decision"] == "SELECT_FOR_U_BUTTON")
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock A/B Codex decision sheet built; "
            f"reviewed={len(rows)}; selected_for_u={selected}; report={REPORT.relative_to(PROJECT_ROOT)}.\n"
        )


def main() -> int:
    rows = build()
    write_rows(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print(f"[ADOBE-AB-DECISION] reviewed={len(rows)} csv={OUT} report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
