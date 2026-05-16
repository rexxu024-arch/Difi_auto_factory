"""Upgrade Shock & Awe prompts held by the quality gate."""

from __future__ import annotations

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES = [
    PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_MJ_Dispatch_Queue.csv",
    PROJECT_ROOT / "Database" / "Shock_And_Awe_V5_Zone2_Printify_Private_Queue.csv",
]

UPGRADES = {
    "OC-NYC-CYBER-006": {
        "prompt": (
            "wall-worthy cyber bonsai displayed as a premium gallery object, brushed titanium trunk and branches, "
            "black jade root system gripping a dark basalt slab, neon circuit sap glowing inside the bark, "
            "smoky jade leaf clusters reduced to sculptural geometry, cinematic dark-luxury room aura, "
            "collector-grade vertical canvas composition with visible impasto texture and controlled negative space, "
            "east-shell west-sci-fi core, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark"
        ),
        "note": "Upgraded for wall-art composition, stronger room aura, and clearer premium canvas fit.",
    },
    "OC-NYC-ASSASSIN-009": {
        "prompt": (
            "classical Greek theatre mask reconstructed as a private museum relic, black titanium facial planes, "
            "deep smoky jade inlays under the cheekbones, brushed brass kintsugi-like fracture seams, "
            "dark walnut gallery wall background, dramatic chiaroscuro and Rembrandt lighting, "
            "collector-grade vertical canvas artwork with impasto surface texture, original cultural fusion object, "
            "no exact historical replica, no readable marks, no text, no logo --v 6.1 --ar 2:3 --style raw --no skin, person, watermark"
        ),
        "note": "Upgraded for text/logo control, stronger material collision, and less generic mask framing.",
    },
}


def update_file(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    changed = 0
    for row in rows:
        sku = row.get("Internal_SKU")
        if sku not in UPGRADES:
            continue
        prompt_field = "MJ_Master_Prompt" if "MJ_Master_Prompt" in row else "MJ_Prompt"
        if prompt_field in row:
            row[prompt_field] = UPGRADES[sku]["prompt"]
        if "Dispatch_Status" in row and row.get("Dispatch_Status") == "PROMPT_NEEDS_UPGRADE":
            row["Dispatch_Status"] = "HOLD_PROMPT_QUALITY_REVIEW"
        if "Review_Note" in row:
            row["Review_Note"] = (row.get("Review_Note", "").rstrip(".") + ". " + UPGRADES[sku]["note"]).strip()
        changed += 1
    if changed:
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    return changed


def main() -> int:
    total = 0
    for path in FILES:
        changed = update_file(path)
        total += changed
        print(f"[SHOCK-PROMPT-UPGRADE] {path.name} changed={changed}")
    print(f"[SHOCK-PROMPT-UPGRADE-DONE] total={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
