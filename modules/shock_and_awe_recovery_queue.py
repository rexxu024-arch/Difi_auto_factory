from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW_PACKETS = PROJECT_ROOT / "Review_Packets"

SELECTION_CSV = DATABASE / "Shock_And_Awe_V5_Zones1_3_Final_Selection.csv"
DISPATCH_CSV = DATABASE / "Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv"
RECOVERY_CSV = DATABASE / "Shock_And_Awe_V5_Recovery_MJ_Queue.csv"
RECOVERY_MD = REVIEW_PACKETS / "OPERATION_SHOCK_AND_AWE_V5_RECOVERY_QUEUE.md"

CSV_HEADERS = [
    "Recovery_Priority",
    "Internal_SKU",
    "Concept_Name",
    "Product_Vector",
    "Blueprint_ID",
    "Provider_ID",
    "Variant_ID",
    "Recovery_Action",
    "Original_Status",
    "Original_QA_Note",
    "Prompt_Source",
    "Recovery_MJ_Prompt",
    "Output_Folder",
    "Blocking_Risk",
    "Done_When",
]


REPROMPTS = {
    "OC-NYC-MUSEUM-019": (
        "museum-grade still life of a sealed scholar's anatomical folio on black velvet, "
        "brass astrolabe fragments, obsidian paperweight, smoky amber varnish, "
        "Dutch Golden Age chiaroscuro lighting, aged vellum diagrams rendered as abstract unreadable marks, "
        "no people, no hands, no face, no portrait, no readable text, no typography, no logo "
        "--v 6.1 --ar 2:3 --style raw --stylize 150 --no skin, person, face, hands, watermark"
    ),
    "OC-NYC-AUSPICIOUS-030": (
        "luxury neo-auspicious abstract guardian totem as a faceted chrome and smoky jade desk object, "
        "algorithmic lucky geometry, neon bodega window glow, high-end collectible toy photography, "
        "no dragon, no lion, no traditional myth creature, no religious icon, no readable text, no logo "
        "--v 6.1 --ar 2:3 --style raw --stylize 180 --no skin, person, dragon, lion, letters, watermark"
    ),
}


def now_et() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def clean(value: object) -> str:
    return str(value or "").strip()


def build_rows() -> list[dict[str, str]]:
    selection = read_csv(SELECTION_CSV)
    dispatch = {row.get("Internal_SKU"): row for row in read_csv(DISPATCH_CSV)}
    holds = [row for row in selection if clean(row.get("Final_Status")).startswith("HOLD")]
    rows: list[dict[str, str]] = []

    for idx, row in enumerate(holds, start=1):
        sku = clean(row.get("Final_SKU") or row.get("Source_SKU"))
        original = dispatch.get(sku, {})
        status = clean(row.get("Final_Status"))
        qa_note = clean(row.get("QA_Note"))
        original_prompt = clean(original.get("MJ_Master_Prompt"))
        output_folder = clean(original.get("Output_Folder"))

        if sku in REPROMPTS:
            action = "REPROMPT_AND_SUBMIT"
            prompt = REPROMPTS[sku]
            prompt_source = "SAFETY_REWRITE"
            risk = "Original visual violated hard QA redline; do not reuse old selected image."
            done_when = "A fresh grid is harvested, visual QA has no people/hands/dragon/myth-creature redline, then private draft can be built."
        else:
            action = "VERIFIED_MJ_UI_SUBMIT_REQUIRED"
            prompt = original_prompt
            prompt_source = "ORIGINAL_PROMPT_REUSE"
            risk = "Raw Discord interaction endpoint returned false-positive success; do not blind retry that path."
            done_when = "Prompt is submitted through a verified browser/UI or freshly captured Discord session path and persistent Midjourney grid message id is recorded."

        rows.append(
            {
                "Recovery_Priority": str(idx),
                "Internal_SKU": sku,
                "Concept_Name": clean(row.get("Concept_Name") or original.get("Concept_Name")),
                "Product_Vector": clean(row.get("Product_Vector") or original.get("Product_Type")),
                "Blueprint_ID": clean(row.get("Blueprint_ID")),
                "Provider_ID": clean(row.get("Provider_ID")),
                "Variant_ID": clean(row.get("Variant_ID")),
                "Recovery_Action": action,
                "Original_Status": status,
                "Original_QA_Note": qa_note,
                "Prompt_Source": prompt_source,
                "Recovery_MJ_Prompt": prompt,
                "Output_Folder": output_folder,
                "Blocking_Risk": risk,
                "Done_When": done_when,
            }
        )
    return rows


def write_report(rows: list[dict[str, str]]) -> None:
    REVIEW_PACKETS.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["Recovery_Action"]] = counts.get(row["Recovery_Action"], 0) + 1

    lines = [
        "# Operation Shock & Awe V5 Recovery Queue",
        "",
        f"Generated: {now_et()} America/New_York",
        "",
        "Purpose: close the remaining 6 private-showcase gaps without repeating the raw Discord false-positive path or reusing redlined visuals.",
        "",
        "## Summary",
        "",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Execution Guard",
            "",
            "- Do not use the previous raw Discord interactions endpoint for these rows until a fresh session payload is verified.",
            "- Redline rows must use the rewritten prompt, not the old image or old prompt.",
            "- A row is not complete until a persistent Midjourney grid message id exists, U1-U4 are harvested, visual QA passes, and the private Printify draft is built.",
            "",
            "## Queue",
            "",
            "| Priority | SKU | Concept | Action | Product | Done When |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['Recovery_Priority']} | {row['Internal_SKU']} | {row['Concept_Name']} | "
            f"{row['Recovery_Action']} | {row['Product_Vector']} | {row['Done_When']} |"
        )
    lines.append("")
    RECOVERY_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_csv(RECOVERY_CSV, rows)
    write_report(rows)
    print(f"[RECOVERY-QUEUE] rows={len(rows)} csv={RECOVERY_CSV}")
    print(f"[RECOVERY-QUEUE] report={RECOVERY_MD}")


if __name__ == "__main__":
    main()
