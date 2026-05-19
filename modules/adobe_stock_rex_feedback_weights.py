"""Apply Rex visual QA feedback to Adobe Stock generation weights."""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
QA = DATABASE / "Adobe_Stock_Rex_Visual_QA.csv"
CANDIDATES = DATABASE / "Adobe_Stock_Local_Upscaled_Candidates.csv"
DAILY_U_CANDIDATES = DATABASE / "Adobe_Stock_Daily_U_Candidates.csv"
MARKET_SAMPLES = DATABASE / "Adobe_Stock_Market_Sample_MJ_Dispatch_Queue.csv"
OUT = DATABASE / "Adobe_Stock_Rex_Feedback_Weights.csv"
REPORT = REVIEW / "Adobe_Stock_Rex_Feedback_Weights_latest.md"
NY_TZ = ZoneInfo("America/New_York")

FIELDS = ["Family", "Pass_Count", "Reject_Count", "Pass_Rate", "Weight", "Action"]


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build() -> list[dict[str, str]]:
    family_by_asset = {row.get("Parent_Asset_ID", ""): row.get("Family", "") for row in read_rows(CANDIDATES)}
    for row in read_rows(DAILY_U_CANDIDATES):
        asset_id = row.get("Asset_ID", "")
        family = row.get("Family", "")
        if asset_id and family:
            family_by_asset[asset_id] = family
    for row in read_rows(MARKET_SAMPLES):
        sku = row.get("Internal_SKU", "")
        concept = row.get("Concept_Name", "")
        family = concept.split(" / ", 1)[0] if concept else ""
        if sku and family:
            family_by_asset[sku] = family
    pass_counts: Counter[str] = Counter()
    reject_counts: Counter[str] = Counter()
    for row in read_rows(QA):
        family = family_by_asset.get(row.get("Parent_Asset_ID", ""), "unknown") or "unknown"
        decision = (row.get("Decision") or "").upper()
        if decision == "PASS":
            pass_counts[family] += 1
        elif decision == "REJECT":
            reject_counts[family] += 1
    families = sorted(set(pass_counts) | set(reject_counts))
    rows: list[dict[str, str]] = []
    for family in families:
        passed = pass_counts[family]
        rejected = reject_counts[family]
        total = passed + rejected
        rate = passed / total if total else 0
        if total < 2:
            weight = "0.80"
            action = "HOLD_MORE_EVIDENCE"
        elif rate >= 0.75:
            weight = "1.65"
            action = "INCREASE_NIGHT_GENERATION"
        elif rate >= 0.45:
            weight = "1.00"
            action = "KEEP_MODERATE"
        else:
            weight = "0.45"
            action = "REMAKE_DNA_CLEANER_SHARPER_NOT_BANNED"
        rows.append(
            {
                "Family": family,
                "Pass_Count": str(passed),
                "Reject_Count": str(rejected),
                "Pass_Rate": f"{rate:.2f}",
                "Weight": weight,
                "Action": action,
            }
        )
    rows.sort(key=lambda row: (float(row["Weight"]), int(row["Pass_Count"])), reverse=True)
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    lines = [
        "# Adobe Stock Rex Feedback Weights",
        "",
        f"Generated: {now_text()}",
        "",
        "## Rule",
        "",
        "- Morning Rex QA trains generation weights.",
        "- PASS families get more night production.",
        "- REJECT families are downgraded or remade before more generation.",
        "",
        "## Weights",
        "",
    ]
    for row in rows:
        lines.append(
            f"- {row['Family']}: pass={row['Pass_Count']}, reject={row['Reject_Count']}, "
            f"rate={row['Pass_Rate']}, weight={row['Weight']}, action={row['Action']}"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock Rex visual QA feedback weights rebuilt; families={len(rows)}; "
            f"top={rows[0]['Family'] if rows else 'none'}.\n"
        )


def main() -> int:
    rows = build()
    write_csv(rows)
    write_report(rows)
    append_progress(rows)
    print(f"[ADOBE-REX-WEIGHTS] families={len(rows)} csv={OUT} report={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
