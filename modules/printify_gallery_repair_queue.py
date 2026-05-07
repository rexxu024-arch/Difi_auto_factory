"""Build a repair queue for Printify/eBay gallery duplicate risks."""

from __future__ import annotations

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
AUDIT_CSV = DATABASE_DIR / "Printify_Gallery_Duplicate_Audit.csv"
OUT_CSV = DATABASE_DIR / "Printify_Gallery_Repair_Queue.csv"
OUT_MD = DATABASE_DIR / "Printify_Gallery_Repair_Queue.md"

HEADERS = [
    "Priority",
    "ID",
    "Product_Type",
    "eBay_Item_ID",
    "Printify_Product_ID",
    "Issue",
    "Selected_Count",
    "Unique_Visual_Count",
    "Repair_Strategy",
    "Can_Auto_Repair",
    "Next_Command",
    "Notes",
]


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def plan(row: dict[str, str]) -> dict[str, str]:
    issue = clean(row.get("Result"))
    product = clean(row.get("Product_Type"))
    if issue == "CHECK_CUSTOM_GALLERY_REPEATS_RISK" and product in {"Poster", "Acrylic"}:
        return {
            "Priority": "96",
            "Repair_Strategy": "REBUILD_OR_RESELECT_OFFICIAL_ONLY",
            "Can_Auto_Repair": "No",
            "Next_Command": f"py modules\\printify_gallery_duplicate_audit.py --ids {row['ID']} --deep-hash",
            "Notes": "Non-sticker products should show one actual artwork plus official product-context mockups. Custom U/detail gallery on live marketplace can look like repeated product spam.",
        }
    if issue == "CHECK_EXACT_DUPLICATE":
        priority = "94" if product in {"Poster", "Acrylic"} else "90"
        return {
            "Priority": priority,
            "Repair_Strategy": "LIVE_VERIFY_THEN_RESELECT_UNIQUE_OR_REPLACE",
            "Can_Auto_Repair": "No",
            "Next_Command": f"py modules\\printify_gallery_duplicate_audit.py --ids {row['ID']} --deep-hash",
            "Notes": "Selected Printify gallery contains exact duplicate URLs. Verify buyer page; if duplicates are visible, repair source selection or create a clean replacement listing before more scale.",
        }
    return {
        "Priority": "80",
        "Repair_Strategy": "MANUAL_REVIEW",
        "Can_Auto_Repair": "No",
        "Next_Command": f"py modules\\printify_gallery_duplicate_audit.py --ids {row['ID']} --deep-hash",
        "Notes": "Unexpected gallery duplicate audit result.",
    }


def build_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(AUDIT_CSV):
        if clean(row.get("Result")) in {"", "OK"}:
            continue
        action = plan(row)
        rows.append(
            {
                "Priority": action["Priority"],
                "ID": clean(row.get("ID")),
                "Product_Type": clean(row.get("Product_Type")),
                "eBay_Item_ID": clean(row.get("eBay_Item_ID")),
                "Printify_Product_ID": clean(row.get("Printify_Product_ID")),
                "Issue": clean(row.get("Result")),
                "Selected_Count": clean(row.get("Selected_Count")),
                "Unique_Visual_Count": clean(row.get("Unique_Visual_Count")),
                "Repair_Strategy": action["Repair_Strategy"],
                "Can_Auto_Repair": action["Can_Auto_Repair"],
                "Next_Command": action["Next_Command"],
                "Notes": action["Notes"],
            }
        )
    rows.sort(key=lambda item: (-int(item["Priority"]), item["Product_Type"], item["ID"]))
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["Issue"]] = counts.get(row["Issue"], 0) + 1
    lines = [
        "# Printify Gallery Repair Queue",
        "",
        f"Rows: {len(rows)}",
        "",
        "## Issue Counts",
        "",
    ]
    for issue, count in sorted(counts.items()):
        lines.append(f"- {issue}: {count}")
    lines.extend(["", "## Top Repairs", ""])
    for row in rows[:30]:
        lines.append(
            f"- P{row['Priority']} {row['ID']} {row['Product_Type']} {row['Issue']} -> {row['Repair_Strategy']}"
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_outputs(rows)
    print(f"[GALLERY-REPAIR-QUEUE] rows={len(rows)} csv={OUT_CSV}")
    for issue, count in sorted({row["Issue"]: sum(1 for item in rows if item["Issue"] == row["Issue"]) for row in rows}.items()):
        print(f"[GALLERY-REPAIR-QUEUE] {issue}={count}")


if __name__ == "__main__":
    main()
