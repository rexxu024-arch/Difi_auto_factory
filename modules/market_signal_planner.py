import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import Workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
REGISTRY = DATABASE_DIR / "Unified_Listing_Registry.csv"
COPY_PLAN = DATABASE_DIR / "Listing_Copy_Optimization.csv"
QA_PLAN = DATABASE_DIR / "Local_Listing_QA.csv"
COVER_FIX_QUEUE = DATABASE_DIR / "eBay_Online_Cover_Fix_Queue.csv"
PRINTIFY_DEFAULT_AUDIT = DATABASE_DIR / "Printify_Image_Default_Audit.csv"
OUTPUT_CSV = DATABASE_DIR / "Market_Signal_Action_Queue.csv"
OUTPUT_XLSX = DATABASE_DIR / "Market_Signal_Action_Queue.xlsx"

HEADERS = [
    "Priority",
    "ID",
    "Product_Type",
    "Category",
    "Action_Bucket",
    "Recommended_Action",
    "Reason",
    "Network_Dependency",
    "Can_Do_Now",
    "eBay_Item_ID",
    "Latest_Views_30_Days",
    "Etsy_Planned",
]


def _read_csv(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _by_id(rows):
    return {row.get("ID"): row for row in rows if row.get("ID")}


def _title_only_issue(qa):
    if not qa:
        return False
    issues = [
        issue.strip()
        for issue in str(qa.get("Issues") or "").split(";")
        if issue.strip()
    ]
    return bool(issues) and all(issue.startswith("title_length_") for issue in issues)


def _priority(row, qa, cover_fix, default_check):
    if cover_fix:
        return 100
    if default_check:
        return 88
    bucket = row.get("Action_Bucket")
    if qa and int(qa.get("Issue_Count") or 0) > 0 and not _title_only_issue(qa):
        return 90
    if _title_only_issue(qa):
        return 82
    if bucket == "Published_Zero_View_Copy_Ad_Review":
        return 80
    if bucket == "Stable_Draft_Publish_When_Scheduled":
        return 70
    if bucket == "Ready_For_Printify_When_Network_OK":
        return 60
    if bucket == "Etsy_Draft_Prepared":
        return 50
    if bucket == "Published_Has_View_Monitor":
        return 40
    return 20


def _recommend(row, copy, qa, cover_fix, default_check):
    if cover_fix:
        return (
            "FIX_LIVE_COVER_SOURCE_OR_REPLACE",
            "Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",
            "medium",
            False,
        )
    if default_check:
        return (
            "FIX_PRINTIFY_DEFAULT_IMAGE_BEFORE_PUBLISH",
            "Printify image-default audit is CHECK for this product. Do not publish until exactly one selected image is default and the local cover/production design audit passes.",
            "medium",
            False,
        )
    bucket = row.get("Action_Bucket")
    issue_count = int((qa or {}).get("Issue_Count") or 0)
    if issue_count and _title_only_issue(qa):
        return (
            "LOCAL_TITLE_LENGTH_REPAIR_FOR_NEXT_SYNC",
            f"Published title is outside the 75-79 character house rule: {(qa or {}).get('Issues')}",
            "low",
            True,
        )
    if issue_count:
        return (
            "QA_HOLD_OR_REBUILD",
            f"Local QA issue: {(qa or {}).get('Issues')}",
            "local",
            True,
        )
    if bucket == "Published_Zero_View_Copy_Ad_Review":
        return (
            "WAIT_24H_AFTER_2PCT_ADS_THEN_APPLY_COPY_TEST",
            "Published item has 0 visible views in last Seller Hub snapshot; 2% General ads are active, so wait for a cleaner baseline before editing online.",
            "low",
            True,
        )
    if bucket == "Stable_Draft_Publish_When_Scheduled":
        return (
            "PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK",
            "Stable Printify mockups exist; publish only via cooled scheduler and audit image order afterward.",
            "medium",
            False,
        )
    if bucket == "Ready_For_Printify_When_Network_OK":
        return (
            "UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH",
            "Local assets are ready but network-dependent upload remains pending.",
            "high",
            False,
        )
    if bucket == "Etsy_Draft_Prepared":
        return (
            "KEEP_FOR_ETSY_PHASE1",
            "Candidate already selected for Etsy relaunch; wait for shop/OAuth readiness and listing-fee confirmation.",
            "medium",
            False,
        )
    if bucket == "Published_Has_View_Monitor":
        return (
            "MONITOR_FOR_CLICK_OR_FAVORITE_SIGNAL",
            "Item has at least one view; do not churn copy too quickly.",
            "low",
            True,
        )
    if copy and copy.get("Needs_Local_Update") == "True":
        return (
            "LOCAL_COPY_READY_FOR_SAFE_SYNC",
            "Copy candidate exists; online sync deferred.",
            "medium",
            False,
        )
    return ("HOLD", "No safe action under current weak-network protocol.", "local", True)


def build_rows():
    registry = _read_csv(REGISTRY)
    copy_by_id = _by_id(_read_csv(COPY_PLAN))
    qa_by_id = _by_id(_read_csv(QA_PLAN))
    cover_fix_by_id = _by_id(_read_csv(COVER_FIX_QUEUE))
    default_audit_by_id = _by_id(_read_csv(PRINTIFY_DEFAULT_AUDIT))
    rows = []
    for item in registry:
        copy = copy_by_id.get(item.get("ID"))
        qa = qa_by_id.get(item.get("ID"))
        cover_fix = cover_fix_by_id.get(item.get("ID"))
        default_row = default_audit_by_id.get(item.get("ID"))
        default_check = default_row and default_row.get("Result") != "OK"
        action, reason, dependency, can_do_now = _recommend(item, copy, qa, cover_fix, default_check)
        rows.append(
            {
                "Priority": _priority(item, qa, cover_fix, default_check),
                "ID": item.get("ID"),
                "Product_Type": item.get("Product_Type"),
                "Category": item.get("Category"),
                "Action_Bucket": item.get("Action_Bucket"),
                "Recommended_Action": action,
                "Reason": reason,
                "Network_Dependency": dependency,
                "Can_Do_Now": can_do_now,
                "eBay_Item_ID": item.get("eBay_Item_ID"),
                "Latest_Views_30_Days": item.get("Latest_eBay_Views_30_Days"),
                "Etsy_Planned": item.get("Etsy_Planned"),
            }
        )
    rows.sort(key=lambda row: (-int(row["Priority"]), row["Product_Type"], row["ID"]))
    return rows


def write_outputs(rows):
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    wb = Workbook()
    ws = wb.active
    ws.title = "Action Queue"
    ws.append(HEADERS)
    for row in rows:
        ws.append([row.get(header, "") for header in HEADERS])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for column, width in {
        "A": 10,
        "B": 24,
        "C": 14,
        "E": 34,
        "F": 40,
        "G": 90,
        "H": 18,
        "J": 18,
    }.items():
        ws.column_dimensions[column].width = width
    wb.save(OUTPUT_XLSX)
    wb.close()


def main():
    rows = build_rows()
    write_outputs(rows)
    actions = Counter(row["Recommended_Action"] for row in rows)
    deps = Counter(row["Network_Dependency"] for row in rows)
    print(f"[MARKET-QUEUE] rows={len(rows)} csv={OUTPUT_CSV}")
    for key, count in actions.most_common():
        print(f"[MARKET-QUEUE] action {key}={count}")
    for key, count in deps.most_common():
        print(f"[MARKET-QUEUE] dependency {key}={count}")


if __name__ == "__main__":
    main()
