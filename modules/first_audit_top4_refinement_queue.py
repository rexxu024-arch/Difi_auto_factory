from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Database" / "First_Audit_V5_Zones1_3_Release_Manifest.csv"
OUT_QUEUE = ROOT / "Database" / "First_Audit_V5_Top4_Refinement_MJ_Dispatch_Queue.csv"
NY_TZ = ZoneInfo("America/New_York")

TOP_IDS = ["V5-02", "V5-08", "V5-10", "V5-19"]

PROMPTS = {
    "V5-02": (
        "Brooklyn Bridge steel cable reliquary at midnight, macro architectural artifact study, "
        "braided suspension cables as black titanium prayer cords, smoky jade light trapped inside "
        "heavy refractive acrylic, sodium amber highlights, cold East River fog diffusion, "
        "chiaroscuro museum lighting, brushed titanium finish, unpolished jade accents, kintsugi-like "
        "gold stress lines, luxury executive desk object, shot on 85mm lens, f/8, ultra-sharp focus, "
        "physical depth, no skyline postcard feeling, no readable text, no logo --v 6.1 --ar 5:7 "
        "--style raw --stylize 800 --chaos 45 --no skin, person, watermark, letters, words, logo, blurry"
    ),
    "V5-08": (
        "celestial anatomy folio from an impossible nineteenth-century observatory, antique anatomical "
        "plate fused with astrological instrument geometry, ink-black vellum and smoky jade wash, "
        "brushed brass measuring rings, kintsugi hairline constellations, Rembrandt side lighting, "
        "archival museum poster composition, crisp engraved linework, controlled negative space, "
        "intellectual dark academia gallery print, shot flat with f/8 copy-stand sharpness, no readable "
        "text, no labels --v 6.1 --ar 2:3 --style raw --stylize 700 --chaos 35 --no skin, person, "
        "watermark, letters, words, logo, blurry"
    ),
    "V5-10": (
        "silent orrery house as a blackened brass and smoky jade astronomical desk shrine, nested "
        "planetary rings suspended in thick optical acrylic, cold jade core glow, brushed titanium "
        "axis pins, fine kintsugi calibration marks as abstract non-readable glyphs, cinematic fog "
        "diffusion, chiaroscuro lighting, luxury executive office artifact, macro product photography, "
        "85mm lens, f/8, ultra-sharp focus, real glass refraction and shadow contact, no readable text "
        "--v 6.1 --ar 5:7 --style raw --stylize 850 --chaos 40 --no skin, person, watermark, letters, "
        "words, logo, blurry"
    ),
    "V5-19": (
        "neo-auspicious prosperity capsule as an elevated collectible desk object, faceted smoky jade "
        "and brushed chrome geometry, algorithmic lucky form without traditional myth creature, inner "
        "neon bodega window glow, kintsugi micro seams, heavy refractive acrylic casing, high-end toy "
        "photography meets luxury industrial design, black walnut desk shadow, 85mm lens, f/8, "
        "ultra-sharp focus, no dragon, no lion, no religious icon, no readable text, no logo --v 6.1 "
        "--ar 5:7 --style raw --stylize 750 --chaos 50 --no skin, person, dragon, lion, letters, "
        "words, watermark, logo, blurry"
    ),
}


FIELDS = [
    "Internal_SKU",
    "Dispatch_Status",
    "Batch",
    "Concept_Name",
    "Product_Type",
    "Recommended_Format",
    "MJ_Master_Prompt",
    "QA_Gate",
    "Output_Folder",
    "Review_Note",
    "Source_Release_ID",
    "Source_Hero_File",
    "Fast_Upscale_Lock",
    "Created_At_ET",
]


def load_manifest() -> list[dict[str, str]]:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clean_prompt(value: str) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def build_rows() -> list[dict[str, str]]:
    by_id = {row["Release_ID"]: row for row in load_manifest()}
    missing = [release_id for release_id in TOP_IDS if release_id not in by_id]
    if missing:
        raise RuntimeError(f"Missing release rows: {missing}")
    timestamp = datetime.now(NY_TZ).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    rows: list[dict[str, str]] = []
    for release_id in TOP_IDS:
        source = by_id[release_id]
        sku = f"{source['SKU']}-R1"
        output_folder = f"Output/First_Audit/V5_Top4_Refinement/{sku}"
        rows.append(
            {
                "Internal_SKU": sku,
                "Dispatch_Status": "READY_FOR_MJ",
                "Batch": "First Audit V5 Top4 Relaxed Refinement",
                "Concept_Name": source["Concept_Name"],
                "Product_Type": source["Source_Product_Vector"],
                "Recommended_Format": source["Studio_Recommendation"],
                "MJ_Master_Prompt": clean_prompt(PROMPTS[release_id]),
                "QA_Gate": "RELAXED_GRID_ONLY_NO_AUTO_UPSCALE_NO_TEXT_NO_LOGO",
                "Output_Folder": output_folder,
                "Review_Note": (
                    "Second-pass draft grid for Rex/Gemini curation. Relaxed mode is allowed; "
                    "Fast/Upscale remains locked until Rex selects a Top 1% final."
                ),
                "Source_Release_ID": release_id,
                "Source_Hero_File": source["Hero_File"],
                "Fast_Upscale_Lock": "LOCKED_NO_AUTOMATIC_UPSCALE",
                "Created_At_ET": timestamp,
            }
        )
    return rows


def write_queue(rows: list[dict[str, str]]) -> None:
    OUT_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_QUEUE.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows = build_rows()
    write_queue(rows)
    print(f"[FIRST-AUDIT-TOP4-REFINE] queue={OUT_QUEUE}")
    print(f"[FIRST-AUDIT-TOP4-REFINE] ready={len(rows)}")
    for row in rows:
        print(
            f"[FIRST-AUDIT-TOP4-REFINE] {row['Internal_SKU']} "
            f"chars={len(row['MJ_Master_Prompt'])} lock={row['Fast_Upscale_Lock']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
