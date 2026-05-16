from __future__ import annotations

import csv
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
QUEUE = DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Queue.csv"
REVIEW = DATABASE / "Shock_And_Awe_V5_Zones1_3_Prompt_Quality_Review.csv"

IP_RISK_TERMS = {
    "kratos",
    "god of war",
    "dark souls",
    "iron man",
    "bearbrick",
    "bape",
    "pokemon",
    "disney",
    "marvel",
    "dc comics",
    "star wars",
}

HARDCORE_EASTERN_TERMS = {
    "shan hai jing",
    "shanhaijing",
    "dragon phoenix",
    "龙凤",
    "山海经",
}

PRODUCT_AR = {
    "Acrylic Block": "--ar 5:7",
    "Framed Poster": "--ar 2:3",
    "Canvas": "--ar 2:3",
    "Notebook": "--ar 2:3",
    "Mug": "--ar 2:1",
}

PRODUCT_CUES = {
    "Acrylic Block": ["acrylic", "refractive", "object", "product photography", "sculpture"],
    "Framed Poster": ["poster", "framed", "wall art", "gallery"],
    "Canvas": ["canvas", "impasto", "texture", "wall art"],
    "Notebook": ["notebook", "cover", "stationery"],
    "Mug": ["wrap", "panoramic", "seamless", "mug"],
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def contains_any(text: str, terms: set[str] | list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def score_row(row: dict[str, str]) -> dict[str, str]:
    prompt = row["MJ_Master_Prompt"]
    product = row["Product_Type"]
    lower = prompt.lower()
    notes: list[str] = []
    scores = {
        "Buyer_Persona": 5 if len(row.get("Broker_Hook", "")) >= 24 else 3,
        "Material_Illusion": 5 if contains_any(prompt, ["jade", "brass", "titanium", "chrome", "obsidian", "parchment", "impasto", "glass", "metal"]) else 3,
        "Composition": 5 if PRODUCT_AR.get(product, "") in prompt else 2,
        "Novelty": 5 if len(set(re.findall(r"[A-Za-z]{4,}", prompt.lower()))) >= 28 else 3,
        "IP_Safety": 2 if contains_any(prompt, IP_RISK_TERMS) else 5,
        "Eastern_Mythology_Safety": 2 if contains_any(prompt, HARDCORE_EASTERN_TERMS) else 5,
        "Text_Safety": 5 if (("no text" in lower or "no readable text" in lower) and "no logo" in lower) else 2,
        "Product_Fit": 5 if contains_any(prompt, PRODUCT_CUES.get(product, [])) else 3,
    }
    if scores["Composition"] < 5:
        notes.append(f"AR mismatch: expected {PRODUCT_AR.get(product)}")
    if scores["IP_Safety"] < 5:
        notes.append("possible direct IP term")
    if scores["Eastern_Mythology_Safety"] < 5:
        notes.append("hardcore eastern mythology term")
    if scores["Text_Safety"] < 5:
        notes.append("missing no text/no logo")
    if scores["Product_Fit"] < 5:
        notes.append("product-format cue could be stronger")
    total = sum(scores.values())
    recommendation = "READY_FOR_MJ" if total >= 34 and not any(v <= 2 for v in scores.values()) else "HOLD_PROMPT_QUALITY_REVIEW"
    return {
        "Internal_SKU": row["Internal_SKU"],
        "Concept_Name": row["Concept_Name"],
        "Product_Type": product,
        **{key: str(value) for key, value in scores.items()},
        "Total": str(total),
        "Recommendation": recommendation,
        "Review_Notes": "; ".join(notes) if notes else "strong candidate for private demo",
    }


def main() -> int:
    rows = read_rows(QUEUE)
    reviews = [score_row(row) for row in rows]
    by_sku = {row["Internal_SKU"]: row["Recommendation"] for row in reviews}
    for row in rows:
        row["Status"] = by_sku[row["Internal_SKU"]]
    write_rows(QUEUE, rows)
    write_rows(REVIEW, reviews)
    counts: dict[str, int] = {}
    for row in reviews:
        counts[row["Recommendation"]] = counts.get(row["Recommendation"], 0) + 1
    print(f"[SHOCK-V5-REMAINING-QA] rows={len(reviews)} counts={counts} review={REVIEW}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
