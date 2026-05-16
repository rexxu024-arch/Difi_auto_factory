"""Build a small Midjourney experiment packet for identity-locked scene mockups.

Goal: verify whether product/design images can be placed into richer scenes
without changing the actual product. This module only prepares prompts and a
review packet; it does not submit to Discord/MJ.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "Database"
REVIEW = ROOT / "Review_Packets"

POD_READY = DATABASE / "Etsy_POD_Printify_Launch_Ready_Full.csv"
LAUNCH_PLAN = DATABASE / "Etsy_launch_plan.csv"
LAUNCH_LOG = DATABASE / "Etsy_Printify_Launch_Log.csv"
DIGITAL_QUEUE = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
OUT_CSV = DATABASE / "MJ_Identity_Locked_Scene_Experiment.csv"
OUT_DISPATCH_CSV = DATABASE / "MJ_Identity_Locked_Scene_Dispatch_Queue.csv"
OUT_MD = REVIEW / "MJ_IDENTITY_LOCKED_SCENE_EXPERIMENT.md"


PARAM_SETS = [
    {
        "Name": "IW_HIGH_LOW_STYLE",
        "Suffix": "--v 6.1 --ar 4:5 --style raw --iw 2 --stylize 50 --chaos 5 --no redesign, changed artwork, altered pattern, different object, text, watermark",
    },
    {
        "Name": "IW_HIGH_MED_STYLE",
        "Suffix": "--v 6.1 --ar 4:5 --style raw --iw 2 --stylize 100 --chaos 8 --no redesign, changed artwork, altered pattern, different object, text, watermark",
    },
    {
        "Name": "IW_MED_SAFE",
        "Suffix": "--v 6.1 --ar 4:5 --style raw --iw 1.5 --stylize 75 --chaos 5 --no redesign, changed artwork, altered pattern, different object, text, watermark",
    },
]

SCENES = {
    "Poster": "quiet luxury apartment reading nook, walnut chair, soft morning side light, gallery wall, realistic scale, premium editorial interior photo",
    "Acrylic": "executive desk shelf, walnut surface, brass lamp, shallow depth of field, realistic acrylic thickness and refraction, quiet luxury office",
    "Digital": "designer workspace flat lay, ivory paper samples, laptop corner, natural light, printable pack preview arranged neatly, realistic paper texture",
}


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def et_now() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def find_path(row: dict[str, str], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = clean(row.get(key))
        if value and Path(value).exists():
            return value
    return ""


def latest_printify_launch_status() -> dict[str, str]:
    latest: dict[str, str] = {}
    for row in read_csv(LAUNCH_LOG):
        item_id = clean(row.get("ID"))
        if item_id:
            latest[item_id] = clean(row.get("Status"))
    return latest


def find_pod_sample_from_launch_plan(target_type: str) -> dict[str, str] | None:
    """Fallback to already launched POD rows when the ready queue is empty."""
    latest_status = latest_printify_launch_status()
    preferred_statuses = {
        "PUBLISHED_EXTERNAL_CONFIRMED",
        "PUBLISHED_EXTERNAL_PENDING",
        "EXTERNAL_STILL_PENDING_NEEDS_RECONCILE",
    }
    for row in read_csv(LAUNCH_PLAN):
        if clean(row.get("Product_Type")).lower() != target_type.lower():
            continue
        if latest_status.get(clean(row.get("ID"))) not in preferred_statuses:
            continue
        ref = find_path(row, ("Cover_Path", "Production_Path"))
        if not ref:
            continue
        return {
            "ID": clean(row.get("ID")),
            "Product_Type": target_type,
            "Reference_Image": ref,
            "Title": clean(row.get("Etsy_Title")),
        }
    return None


def pick_samples() -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    pod_rows = read_csv(POD_READY)
    for target_type in ("Poster", "Acrylic"):
        found = False
        for row in pod_rows:
            if clean(row.get("Product_Type")).lower().startswith(target_type.lower()):
                ref = find_path(row, ("Cover_Path", "Production_Path"))
                if ref:
                    samples.append(
                        {
                            "ID": clean(row.get("ID")),
                            "Product_Type": target_type,
                            "Reference_Image": ref,
                            "Title": clean(row.get("Etsy_Title")),
                        }
                    )
                    found = True
                    break
        if not found:
            fallback = find_pod_sample_from_launch_plan(target_type)
            if fallback:
                samples.append(fallback)
    digital_rows = read_csv(DIGITAL_QUEUE)
    for row in digital_rows:
        ref = find_path(row, ("Preview_Path", "Cover_Path", "Preview_Image", "Image_Path", "Local_Path"))
        if ref:
            samples.append(
                {
                    "ID": clean(row.get("ID")),
                    "Product_Type": "Digital",
                    "Reference_Image": ref,
                    "Title": clean(row.get("Title") or row.get("Etsy_Title") or row.get("Meta_Title")),
                }
            )
            break
    return samples


def build_prompt(sample: dict[str, str], suffix: str) -> str:
    scene = SCENES[sample["Product_Type"]]
    return (
        f"{sample['Reference_Image']} "
        f"place the exact same product shown in the reference image into this scene: {scene}. "
        "Preserve exact product design, exact artwork, exact pattern, exact colors, exact proportions, exact object silhouette. "
        "Do not redraw the product, do not invent a new product, do not change the printed artwork. "
        "Only change environment, camera angle, lighting, and surrounding props. "
        f"{suffix}"
    )


def run() -> None:
    rows: list[dict[str, str]] = []
    dispatch_rows: list[dict[str, str]] = []
    for sample in pick_samples():
        for params in PARAM_SETS:
            prompt = build_prompt(sample, params["Suffix"])
            sku = f"{sample['ID']}-{params['Name']}"
            output_folder = ROOT / "Output" / "Scene_Mockups" / "Identity_Locked" / sku
            rows.append(
                {
                    "ID": sample["ID"],
                    "Product_Type": sample["Product_Type"],
                    "Param_Set": params["Name"],
                    "Reference_Image": sample["Reference_Image"],
                    "Prompt": prompt,
                    "Expected_QA": "PASS only if product identity is unchanged; HOLD on any subject/pattern/color/proportion drift.",
                }
            )
            dispatch_rows.append(
                {
                    "Internal_SKU": sku,
                    "Product_Type": sample["Product_Type"],
                    "Source_ID": sample["ID"],
                    "Param_Set": params["Name"],
                    "Reference_Image": sample["Reference_Image"],
                    "MJ_Master_Prompt": prompt,
                    "Output_Folder": str(output_folder),
                    "Dispatch_Status": "READY_FOR_MJ",
                    "Expected_QA": "PASS only if product identity is unchanged; HOLD on any subject/pattern/color/proportion drift.",
                }
            )
    fields = ["ID", "Product_Type", "Param_Set", "Reference_Image", "Prompt", "Expected_QA"]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    dispatch_fields = [
        "Internal_SKU",
        "Product_Type",
        "Source_ID",
        "Param_Set",
        "Reference_Image",
        "MJ_Master_Prompt",
        "Output_Folder",
        "Dispatch_Status",
        "Expected_QA",
    ]
    with OUT_DISPATCH_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=dispatch_fields)
        writer.writeheader()
        writer.writerows(dispatch_rows)
    lines = [
        "# MJ Identity-Locked Scene Experiment",
        "",
        f"Generated: {et_now()}",
        f"Samples: {len(set(row['ID'] for row in rows))}",
        f"Prompt variants: {len(rows)}",
        f"Dispatcher queue: `{OUT_DISPATCH_CSV}`",
        "",
        "Run through the verified MJ path one item at a time. Do not use outputs in Etsy/eBay until QA confirms the product image did not drift.",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['ID']} - {row['Param_Set']}",
                "",
                f"Reference: `{row['Reference_Image']}`",
                "",
                "```text",
                row["Prompt"],
                "```",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"identity_locked_scene_experiment prompts={len(rows)}")
    print(f"csv={OUT_CSV}")
    print(f"dispatch_queue={OUT_DISPATCH_CSV}")
    print(f"packet={OUT_MD}")


if __name__ == "__main__":
    run()
