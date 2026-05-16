"""Build a stricter First Audit extension shortlist from private drafts.

This is local-only: it does not publish, spend, or touch marketplace accounts.
It exists so "continue monthly tasks" has a concrete Studio-series production
step after the first lookbook is built.
"""

from __future__ import annotations

import csv
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets" / "First_Audit_001"

MANIFEST = DATABASE / "First_Audit_001_Asset_Manifest.csv"
OUT_CSV = DATABASE / "First_Audit_001_Extension_Candidates.csv"
OUT_MD = REVIEW / "FIRST_AUDIT_EXTENSION_CANDIDATES.md"

SOURCE_FILES = [
    DATABASE / "Shock_And_Awe_V5_Printify_Private_Drafts.csv",
    DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Drafts.csv",
]

ALLOWED_MEDIA = ("Acrylic Block", "Framed Poster")
REVIEW_MEDIA = ("Canvas",)
BANNED_MEDIA = ("Mug", "Notebook", "Phone Case", "T-Shirt", "Sticker")


def clean(value: object) -> str:
    return str(value or "").strip()


def et_now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def selected_skus() -> set[str]:
    return {clean(row.get("SKU")) for row in read_csv(MANIFEST) if clean(row.get("SKU"))}


def media_status(media: str) -> tuple[str, int]:
    media_l = media.lower()
    if media in ALLOWED_MEDIA or "acrylic" in media_l or ("framed" in media_l and "poster" in media_l):
        return "FIRST_AUDIT_EXTENSION_READY", 100
    if media in REVIEW_MEDIA:
        return "REVIEW_CARRIER_CANVAS_ONLY_IF_REX_ACCEPTS", 72
    if any(token.lower() in media_l for token in BANNED_MEDIA):
        return "HOLD_CHEAP_CARRIER", 0
    return "REVIEW_UNKNOWN_CARRIER", 30


def visual_score(row: dict[str, str]) -> int:
    status = clean(row.get("Selection_Status") or row.get("QA_Status") or row.get("Status"))
    note = clean(row.get("QA_Note") or row.get("Decision_Note"))
    score = 0
    if "PASS" in status:
        score += 30
    if "REVIEW_UPSCALE" in status:
        score += 18
    if "PRODUCTION_READY" in clean(row.get("Production_Status")):
        score += 22
    if clean(row.get("Printify_Product_ID")):
        score += 16
    if "Only upscale/reformat required" in note:
        score += 8
    if "Visual QA pass" in note:
        score += 12
    return score


def collect(limit: int = 15) -> list[dict[str, str]]:
    already = selected_skus()
    candidates: list[dict[str, str]] = []
    for source in SOURCE_FILES:
        for row in read_csv(source):
            sku = clean(row.get("Final_SKU") or row.get("SKU"))
            if not sku or sku in already:
                continue
            media = clean(row.get("Product_Vector"))
            gate, media_score = media_status(media)
            if gate == "HOLD_CHEAP_CARRIER":
                continue
            score = media_score + visual_score(row)
            candidates.append(
                {
                    "Generated_At_ET": et_now(),
                    "Candidate_Rank": "",
                    "SKU": sku,
                    "Concept": clean(row.get("Concept_Name")) or sku,
                    "Product_Vector": media,
                    "Gate_Status": gate,
                    "Score": str(score),
                    "Blueprint_ID": clean(row.get("Blueprint_ID")),
                    "Provider_ID": clean(row.get("Provider_ID")),
                    "Variant_ID": clean(row.get("Variant_ID")),
                    "Base_Cost_USD": clean(row.get("Base_Cost_USD")),
                    "Shipping_USD": clean(row.get("Shipping_USD")),
                    "Recommended_RRP_USD": clean(row.get("Recommended_RRP_USD")),
                    "Selected_File": clean(row.get("Selected_File")),
                    "Production_Design_File": clean(row.get("Production_Design_File")),
                    "Printify_Product_ID": clean(row.get("Printify_Product_ID")),
                    "Decision_Note": clean(row.get("QA_Note") or row.get("Decision_Note")),
                    "Next_Action": "Rex visual review, then promote strongest 3-6 into THE FIRST AUDIT: 001.",
                }
            )
    candidates.sort(key=lambda r: (-int(r["Score"]), r["Product_Vector"], r["SKU"]))
    for idx, row in enumerate(candidates[:limit], start=1):
        row["Candidate_Rank"] = str(idx)
    return candidates[:limit]


def write_outputs(rows: list[dict[str, str]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    fields = [
        "Generated_At_ET",
        "Candidate_Rank",
        "SKU",
        "Concept",
        "Product_Vector",
        "Gate_Status",
        "Score",
        "Blueprint_ID",
        "Provider_ID",
        "Variant_ID",
        "Base_Cost_USD",
        "Shipping_USD",
        "Recommended_RRP_USD",
        "Selected_File",
        "Production_Design_File",
        "Printify_Product_ID",
        "Decision_Note",
        "Next_Action",
    ]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# First Audit Extension Candidates",
        "",
        f"Generated: {et_now()}",
        f"Rows: {len(rows)}",
        "",
        "Rule: only optical acrylic / framed poster candidates are auto-ready. Canvas remains review-only; mugs/notebooks/phone cases are excluded from the Studio series.",
        "",
        "| Rank | SKU | Concept | Medium | Gate | Score |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['Candidate_Rank']} | {row['SKU']} | {row['Concept']} | "
            f"{row['Product_Vector']} | {row['Gate_Status']} | {row['Score']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = collect()
    write_outputs(rows)
    ready = sum(1 for r in rows if r["Gate_Status"] == "FIRST_AUDIT_EXTENSION_READY")
    print(f"[FIRST-AUDIT-EXTENSION] candidates={len(rows)} ready={ready} csv={OUT_CSV}")
    print(f"[FIRST-AUDIT-EXTENSION] report={OUT_MD}")


if __name__ == "__main__":
    main()
