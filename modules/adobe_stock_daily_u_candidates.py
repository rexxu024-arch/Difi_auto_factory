"""Build Adobe Stock upload candidates from harvested daily U-button files.

Grid images are review evidence only. U1-U4 full-resolution files become the
candidate assets, then image QA decides whether they are usable for Adobe.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adobe_stock_quality_policy import validate_adobe_production_image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
QUEUE = DATABASE / "Adobe_Stock_Daily_MJ_Dispatch_Queue.csv"
OUT = DATABASE / "Adobe_Stock_Daily_U_Candidates.csv"
REPORT = REVIEW / "Adobe_Stock_Daily_U_Candidates_latest.md"
NY_TZ = ZoneInfo("America/New_York")

FIELDS = [
    "Asset_ID",
    "Source_Queue_ID",
    "Parent_SKU",
    "Variant",
    "Family",
    "Product_Type",
    "Filename",
    "Source_Path",
    "Source_Provenance",
    "Title",
    "Keywords",
    "Category",
    "Releases",
    "Created_Using_AI",
    "Adobe_Description",
    "Width",
    "Height",
    "Pixels",
    "Short_Edge",
    "Long_Edge",
    "Mode",
    "Format",
    "File_Bytes",
    "QA_Status",
    "Upload_Status",
    "Issues",
]

PUBLIC_BAN_TERMS = {
    "openclaw",
    "first audit",
    "sweatshop",
    "etsy",
    "ebay",
    "printify",
    "midjourney",
    "codex",
    "gemini",
    "claude",
    "deepseek",
    "dify",
}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split()).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def public_guard(*values: str) -> str:
    text = " ".join(values).lower()
    for term in PUBLIC_BAN_TERMS:
        if term in text:
            return term
    return ""


def title_for_variant(base_title: str, variant: str) -> str:
    title = clean(base_title)
    if len(title) <= 70:
        return title
    return title[:70].rstrip()


def description_for(row: dict[str, str], variant: str) -> str:
    title = title_for_variant(clean(row.get("Adobe_Title")), variant)
    return (
        f"{title}. High-resolution material background for commercial design, "
        "branding layouts, packaging mockups, websites, presentations, and editorial compositions. "
        "No people, no logo, no text. Buyer should review final suitability for their project."
    )


def candidate_filename(row: dict[str, str], variant: str, source_path: Path) -> str:
    stem = Path(clean(row.get("Source_Queue_ID")) or clean(row.get("Internal_SKU"))).stem.lower()
    stem = stem.replace("adobe-daily-", "adobe-stock-").replace("_", "-")
    return f"{stem}-{variant.lower()}{source_path.suffix.lower() or '.png'}"


def build(limit: int = 0) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(QUEUE):
        harvest_status = clean(row.get("Harvest_Status"))
        guard_status = clean(row.get("Duplicate_Guard_Status"))
        guard_reason = clean(row.get("Duplicate_Guard_Reason"))
        if (
            harvest_status.startswith("HARVEST_HOLD")
            or "DUPLICATE" in harvest_status
            or guard_status == "HOLD"
            or "duplicate" in guard_reason.lower()
        ):
            continue
        parent = clean(row.get("Internal_SKU"))
        source_queue = clean(row.get("Source_Queue_ID"))
        family = clean(row.get("Concept_Name")).split(" / ", 1)[0]
        product_type = clean(row.get("Concept_Name")).split(" / ", 1)[1] if " / " in clean(row.get("Concept_Name")) else ""
        for variant in ("U1", "U2", "U3", "U4"):
            raw_path = clean(row.get(f"{variant}_File"))
            if not raw_path:
                continue
            source_path = resolve_path(raw_path)
            candidate = {
                "Asset_ID": f"{parent}-{variant}",
                "Source_Queue_ID": source_queue,
                "Parent_SKU": parent,
                "Variant": variant,
                "Family": family,
                "Product_Type": product_type,
                "Filename": candidate_filename(row, variant, source_path),
                "Source_Path": str(source_path.relative_to(PROJECT_ROOT)) if source_path.exists() else raw_path,
                "Source_Provenance": f"mj_u_button_full_res_{variant.lower()}",
                "Title": title_for_variant(clean(row.get("Adobe_Title")), variant),
                "Keywords": clean(row.get("Adobe_Keywords")),
                "Category": clean(row.get("Adobe_Category")) or "8",
                "Releases": "",
                "Created_Using_AI": clean(row.get("Created_Using_AI")) or "true",
                "Adobe_Description": description_for(row, variant),
            }
            blocked = public_guard(candidate["Title"], candidate["Keywords"], candidate["Adobe_Description"])
            if blocked:
                candidate["QA_Status"] = "HOLD_PUBLIC_METADATA_TERM"
                candidate["Upload_Status"] = "HOLD_DO_NOT_UPLOAD"
                candidate["Issues"] = f"blocked public term: {blocked}"
            else:
                ok, status, info = validate_adobe_production_image(source_path, {**row, **candidate})
                candidate.update(info)
                candidate["QA_Status"] = status
                candidate["Upload_Status"] = "QA_PASS_NOT_UPLOADED" if ok else "HOLD_DO_NOT_UPLOAD"
                candidate["Issues"] = info.get("Quality_Reasons", "")
            rows.append(candidate)
            if limit and len(rows) >= limit:
                return rows
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row.get("QA_Status", "") for row in rows)
    family_counts = Counter(row.get("Family", "") for row in rows)
    passed = sum(1 for row in rows if row.get("QA_Status", "").startswith("QA_PASS"))
    lines = [
        "# Adobe Stock Daily U Candidates",
        "",
        f"Generated: {now_text()}",
        "",
        f"- U-button files found: {len(rows)}",
        f"- QA passed: {passed}",
        f"- Status: {dict(status_counts)}",
        f"- Candidate CSV: `{OUT.relative_to(PROJECT_ROOT)}`",
        "",
        "## Policy",
        "",
        "- Grid files are evidence/review only.",
        "- U1-U4 full-resolution files are stock candidates.",
        "- No public metadata may contain internal project/tool names.",
        "- Adobe upload remains blocked until image QA and metadata QA pass.",
        "",
        "## Family Mix",
        "",
    ]
    for family, count in family_counts.most_common():
        lines.append(f"- {family or 'unknown'}: {count}")
    lines.append("")
    lines.append("## First 20 Candidates")
    lines.append("")
    for row in rows[:20]:
        lines.append(f"- {row['Asset_ID']} | {row['QA_Status']} | {row['Title']} | {row['Source_Path']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_progress(rows: list[dict[str, str]]) -> None:
    passed = sum(1 for row in rows if row.get("QA_Status", "").startswith("QA_PASS"))
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n- {now_text()}: Adobe Stock daily U candidates rebuilt; "
            f"u_files={len(rows)}; qa_pass={passed}; no upload/spend.\n"
        )


def main() -> int:
    rows = build()
    write_csv(OUT, rows)
    write_report(rows)
    append_progress(rows)
    print(f"[ADOBE-DAILY-U] u_files={len(rows)} qa_pass={sum(1 for row in rows if row.get('QA_Status', '').startswith('QA_PASS'))} csv={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
