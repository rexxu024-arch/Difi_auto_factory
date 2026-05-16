"""Convert Printify gallery audits into an actionable public-release queue.

The goal is to keep marketplace experiments from using products whose gallery
set is suspicious, duplicated, or still unclear. This is read-only: no publish,
no price change, no listing end.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT_ROOT / "Database" / "Printify_Gallery_Duplicate_Audit.csv"
OUT = PROJECT_ROOT / "Database" / "Public_Release_Readiness_Queue.csv"
REPORT = PROJECT_ROOT / "Reports" / "Public_Release_Readiness_Report.md"
PROGRESS = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

HEADERS = [
    "ID",
    "Product_Type",
    "Printify_Product_ID",
    "eBay_Item_ID",
    "Readiness",
    "Next_Action",
    "Selected_Count",
    "Unique_Visual_Count",
    "Exact_Duplicate_Count",
    "Near_Duplicate_Count",
    "Reason",
]


def now_et() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M ET")


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def classify(row: dict[str, str]) -> tuple[str, str, str]:
    product_type = clean(row.get("Product_Type"))
    result = clean(row.get("Result")).upper()
    if product_type.lower() == "sticker":
        return "FROZEN", "DO_NOT_EXPAND_STICKER", "Sticker expansion is closed by Rex due eBay price compression."
    if result == "OK":
        return "READY_FOR_EXPERIMENT_MONITOR", "KEEP_OR_USE_AS_CLEAN_REFERENCE", "Gallery audit is visually unique enough for controlled public experiments."
    if "CHECK_CUSTOM_GALLERY" in result:
        return "HOLD_GALLERY_REVIEW", "INSPECT_OR_REBUILD_GALLERY_BEFORE_SCALE", "Gallery has custom/default mix risk; do not clone or scale until buyer-facing gallery is verified."
    if clean(row.get("Error")):
        return "HOLD_ERROR", "RETRY_AUDIT", clean(row.get("Error"))
    return "HOLD_UNKNOWN", "MANUAL_REVIEW", f"Unclassified gallery audit result: {result or 'blank'}"


def main() -> int:
    output: list[dict[str, str]] = []
    for row in read_rows(AUDIT):
        readiness, action, reason = classify(row)
        output.append(
            {
                "ID": clean(row.get("ID")),
                "Product_Type": clean(row.get("Product_Type")),
                "Printify_Product_ID": clean(row.get("Printify_Product_ID")),
                "eBay_Item_ID": clean(row.get("eBay_Item_ID")),
                "Readiness": readiness,
                "Next_Action": action,
                "Selected_Count": clean(row.get("Selected_Count")),
                "Unique_Visual_Count": clean(row.get("Unique_Visual_Count")),
                "Exact_Duplicate_Count": clean(row.get("Exact_Duplicate_Count")),
                "Near_Duplicate_Count": clean(row.get("Near_Duplicate_Count")),
                "Reason": reason,
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(output)

    counts: dict[str, int] = {}
    for row in output:
        counts[row["Readiness"]] = counts.get(row["Readiness"], 0) + 1
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Public Release Readiness Report",
        "",
        f"- Generated: {now_et()}",
        f"- Source audit: `{AUDIT}`",
        f"- Queue: `{OUT}`",
        "",
        "## Counts",
        "",
    ]
    for key in sorted(counts):
        lines.append(f"- {key}: {counts[key]}")
    lines += [
        "",
        "## Policy",
        "",
        "- READY rows can be used as clean references for controlled Poster/Acrylic experiments.",
        "- HOLD rows must not be cloned, scaled, or used as source-of-truth until a buyer-facing gallery audit passes.",
        "- This script performs no marketplace writes and no fee actions.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## {now_et()} - Public release readiness queue\n"
            f"- Converted gallery audit into readiness queue: {counts}.\n"
            f"- Queue: `{OUT}`; report: `{REPORT}`.\n"
            "- No marketplace write, publish, price, ad, or fee action was taken.\n"
        )
    print(f"[PUBLIC-RELEASE-READINESS] rows={len(output)} counts={counts} queue={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
