from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW_PACKETS = PROJECT_ROOT / "Review_Packets"

RECOVERY_CSV = DATABASE / "Shock_And_Awe_V5_Recovery_MJ_Queue.csv"
UI_PACKET_CSV = DATABASE / "Shock_And_Awe_V5_UI_Submission_Packet.csv"
UI_PACKET_MD = REVIEW_PACKETS / "OPERATION_SHOCK_AND_AWE_V5_UI_SUBMISSION_PACKET_latest.md"
UI_CLIPBOARD_TXT = REVIEW_PACKETS / "OPERATION_SHOCK_AND_AWE_V5_UI_CLIPBOARD_PROMPTS_latest.txt"
UI_CLIPBOARD_JSON = DATABASE / "Shock_And_Awe_V5_UI_Clipboard_Prompts.json"

FIELDS = [
    "Paste_Order",
    "Internal_SKU",
    "Concept_Name",
    "Recovery_Action",
    "Product_Vector",
    "Blueprint_ID",
    "Provider_ID",
    "Variant_ID",
    "Prompt_One_Line",
    "Output_Folder",
    "Required_Proof",
    "Post_Submit_Update",
    "Safety_Note",
]


def now_et() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\n", " ").replace("\r", " ").split()).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_rows() -> list[dict[str, str]]:
    recovery = read_csv(RECOVERY_CSV)
    rows: list[dict[str, str]] = []
    for idx, row in enumerate(recovery, start=1):
        action = clean(row.get("Recovery_Action"))
        if action == "REPROMPT_AND_SUBMIT":
            safety = "Use rewritten safety prompt only; do not reuse old redlined image or old prompt."
        else:
            safety = "Use verified Discord/Midjourney web UI or freshly captured safe session only; do not use the raw interactions endpoint."
        rows.append(
            {
                "Paste_Order": str(idx),
                "Internal_SKU": clean(row.get("Internal_SKU")),
                "Concept_Name": clean(row.get("Concept_Name")),
                "Recovery_Action": action,
                "Product_Vector": clean(row.get("Product_Vector")),
                "Blueprint_ID": clean(row.get("Blueprint_ID")),
                "Provider_ID": clean(row.get("Provider_ID")),
                "Variant_ID": clean(row.get("Variant_ID")),
                "Prompt_One_Line": clean(row.get("Recovery_MJ_Prompt")),
                "Output_Folder": clean(row.get("Output_Folder")),
                "Required_Proof": "Persistent Midjourney Bot grid message id visible in channel; transient command echo is not enough.",
                "Post_Submit_Update": (
                    "Update Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv: "
                    "Dispatch_Status=MJ_SUBMITTED, Grid_Message_ID/Dispatch_Confirm_Message_ID=<persistent id>, "
                    "then run shock_and_awe_mj_harvester.py and shock_and_awe_visual_qa.py."
                ),
                "Safety_Note": safety,
            }
        )
    return rows


def write_markdown(rows: list[dict[str, str]]) -> None:
    REVIEW_PACKETS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Operation Shock & Awe V5 UI Submission Packet",
        "",
        f"Generated: {now_et()} America/New_York",
        "",
        "Purpose: close the 6 remaining private-showcase gaps without repeating the raw Discord false-positive path.",
        "",
        "## Hard Guards",
        "",
        "- Submit through verified Discord/Midjourney UI only, or a freshly captured safe session path with visible persistent grid proof.",
        "- Do not mark a row submitted from an HTTP 2xx response alone.",
        "- Redline rows must use the rewritten prompt in this packet.",
        "- A row is complete only after persistent grid id, U1-U4 harvest, visual QA pass, production design build, and Printify private draft creation.",
        "",
        "## Paste Queue",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['Paste_Order']}. {row['Internal_SKU']} - {row['Concept_Name']}",
                "",
                f"- Action: {row['Recovery_Action']}",
                f"- Product Vector: {row['Product_Vector']} / blueprint {row['Blueprint_ID']} / provider {row['Provider_ID']} / variant {row['Variant_ID']}",
                f"- Safety: {row['Safety_Note']}",
                "- Prompt:",
                "",
                "```text",
                row["Prompt_One_Line"],
                "```",
                "",
                f"- Required proof: {row['Required_Proof']}",
                "",
            ]
        )
    UI_PACKET_MD.write_text("\n".join(lines), encoding="utf-8")


def write_clipboard_files(rows: list[dict[str, str]]) -> None:
    REVIEW_PACKETS.mkdir(parents=True, exist_ok=True)
    text_lines = [
        "Operation Shock & Awe V5 - UI Clipboard Prompts",
        f"Generated: {now_et()} America/New_York",
        "Guard: paste only into verified Midjourney/Discord UI; do not mark submitted until a persistent grid message id is visible.",
        "",
    ]
    json_rows: list[dict[str, object]] = []
    for row in rows:
        prompt = clean(row.get("Prompt_One_Line"))
        text_lines.extend(
            [
                f"## {row['Paste_Order']} | {row['Internal_SKU']} | {row['Concept_Name']} | {row['Recovery_Action']}",
                prompt,
                "",
            ]
        )
        json_rows.append(
            {
                "paste_order": int(row["Paste_Order"]),
                "internal_sku": row["Internal_SKU"],
                "concept_name": row["Concept_Name"],
                "recovery_action": row["Recovery_Action"],
                "prompt_one_line": prompt,
                "required_proof": row["Required_Proof"],
                "output_folder": row["Output_Folder"],
                "post_submit_update": row["Post_Submit_Update"],
            }
        )
    UI_CLIPBOARD_TXT.write_text("\n".join(text_lines), encoding="utf-8")
    UI_CLIPBOARD_JSON.write_text(json.dumps(json_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    rows = build_rows()
    write_csv(UI_PACKET_CSV, rows)
    write_markdown(rows)
    write_clipboard_files(rows)
    print(f"[SHOCK-UI-PACKET] rows={len(rows)} csv={UI_PACKET_CSV}")
    print(f"[SHOCK-UI-PACKET] md={UI_PACKET_MD}")
    print(f"[SHOCK-UI-PACKET] clipboard_txt={UI_CLIPBOARD_TXT}")
    print(f"[SHOCK-UI-PACKET] clipboard_json={UI_CLIPBOARD_JSON}")
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
