"""Quality review held Shock & Awe prompts before more MJ dispatch.

This is a conservative gate. It does not try to prove creative greatness by
volume; it records why a prompt is strong enough to dispatch or why it needs
revision before spending more generation cycles.
"""

from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUEUE = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_MJ_Dispatch_Queue.csv"
REPORT_CSV = PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Prompt_Quality_Review.csv"
REPORT_MD = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_V5_PROMPT_QUALITY_REVIEW.md"
NY_TZ = ZoneInfo("America/New_York")

MATERIAL_TERMS = {
    "smoky jade",
    "black titanium",
    "brushed titanium",
    "brushed brass",
    "antique gold",
    "dark gold",
    "molten brass",
    "obsidian",
    "frost metal",
    "impasto",
    "refractive",
    "holographic",
}
COMPOSITION_TERMS = {
    "museum",
    "plinth",
    "studio product photography",
    "gallery",
    "framed poster",
    "canvas",
    "macro photography",
    "composition",
}
RISK_TERMS = {
    "kratos",
    "iron man",
    "bearbrick",
    "marvel",
    "disney",
    "dark souls",
    "god of war",
    "star wars",
}


def clean(value: str) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def count_terms(text: str, terms: set[str]) -> int:
    lower = text.lower()
    return sum(1 for term in terms if term in lower)


def score_prompt(row: dict[str, str]) -> dict[str, str | int]:
    prompt = clean(row.get("MJ_Master_Prompt", ""))
    product = clean(row.get("Product_Type", ""))
    concept = clean(row.get("Concept_Name", ""))
    lower = prompt.lower()
    material_hits = count_terms(prompt, MATERIAL_TERMS)
    composition_hits = count_terms(prompt, COMPOSITION_TERMS)
    risk_hits = [term for term in RISK_TERMS if term in lower]

    buyer_persona = 4
    if any(token in lower for token in ["office", "desk", "collector", "museum", "gallery", "luxury", "premium"]):
        buyer_persona += 1

    material = min(5, 2 + material_hits)
    composition = min(5, 2 + composition_hits)
    novelty = 4
    if any(token in lower for token in ["original", "reconstructed", "abstract", "artifact", "relic"]):
        novelty += 1

    ip_safety = 5
    if risk_hits:
        ip_safety = 3
    if "without recognizable ip" in lower or "no copyrighted design" in lower or "fully original" in lower:
        ip_safety = min(5, ip_safety + 1)

    text_safety = 5 if all(token in lower for token in ["no text", "no logo"]) else 3
    product_fit = 4
    if product == "Acrylic Block" and any(token in lower for token in ["object", "artifact", "relic", "photography", "plinth", "refractive"]):
        product_fit = 5
    if product in {"Canvas", "Framed Poster"} and any(token in lower for token in ["wall art", "poster", "canvas", "gallery", "composition"]):
        product_fit = 5

    total = buyer_persona + material + composition + novelty + ip_safety + text_safety + product_fit
    recommendation = "READY_FOR_MJ" if total >= 32 and ip_safety >= 5 and text_safety >= 5 and material >= 4 else "PROMPT_NEEDS_UPGRADE"
    notes = []
    if material < 4:
        notes.append("material illusion is not concrete enough")
    if composition < 4:
        notes.append("composition/product-format cue is weak")
    if ip_safety < 5:
        notes.append("contains direct or near-direct IP/style risk")
    if text_safety < 5:
        notes.append("needs stronger no-text/no-logo control")
    if total >= 34:
        notes.append("strong candidate for partner demo")
    return {
        "Internal_SKU": clean(row.get("Internal_SKU")),
        "Concept_Name": concept,
        "Product_Type": product,
        "Buyer_Persona": buyer_persona,
        "Material_Illusion": material,
        "Composition": composition,
        "Novelty": novelty,
        "IP_Safety": ip_safety,
        "Text_Safety": text_safety,
        "Product_Fit": product_fit,
        "Total": total,
        "Recommendation": recommendation,
        "Review_Notes": "; ".join(notes) or "passes baseline top-demo gate",
    }


def review(limit: int) -> int:
    with QUEUE.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    reviewed = []
    count = 0
    for row in rows:
        if count >= limit:
            break
        if row.get("Dispatch_Status") != "HOLD_PROMPT_QUALITY_REVIEW":
            continue
        result = score_prompt(row)
        reviewed.append(result)
        row["Dispatch_Status"] = str(result["Recommendation"])
        row["Review_Note"] = clean(row.get("Review_Note")) + f" Quality review: {result['Review_Notes']}."
        count += 1

    with QUEUE.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    report_fields = [
        "Internal_SKU",
        "Concept_Name",
        "Product_Type",
        "Buyer_Persona",
        "Material_Illusion",
        "Composition",
        "Novelty",
        "IP_Safety",
        "Text_Safety",
        "Product_Fit",
        "Total",
        "Recommendation",
        "Review_Notes",
    ]
    existing = []
    if REPORT_CSV.exists():
        with REPORT_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
            existing = list(csv.DictReader(handle))
    merged = {row["Internal_SKU"]: row for row in existing if row.get("Internal_SKU")}
    for row in reviewed:
        merged[str(row["Internal_SKU"])] = row
    with REPORT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=report_fields)
        writer.writeheader()
        writer.writerows(merged.values())

    stamp = datetime.now(NY_TZ).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    lines = [
        "# Shock & Awe V5 Prompt Quality Review",
        "",
        f"Updated: {stamp}",
        "",
        "Threshold: only prompts that pass material, IP, text, and product-fit gates return to READY_FOR_MJ.",
        "",
    ]
    for row in merged.values():
        lines.append(f"## {row['Internal_SKU']} - {row['Concept_Name']}")
        lines.append(f"- Product: {row['Product_Type']}")
        lines.append(f"- Score: {row['Total']} / 35")
        lines.append(f"- Recommendation: {row['Recommendation']}")
        lines.append(f"- Notes: {row['Review_Notes']}")
        lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"[SHOCK-PROMPT-REVIEW] reviewed={count} report={REPORT_CSV}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Review Shock & Awe held prompts")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    return review(max(1, args.limit))


if __name__ == "__main__":
    raise SystemExit(main())
