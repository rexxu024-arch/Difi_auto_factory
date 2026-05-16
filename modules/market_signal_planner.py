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
RETIRE_QUEUE = DATABASE_DIR / "eBay_Retire_Queue.csv"
PRINTIFY_DEFAULT_AUDIT = DATABASE_DIR / "Printify_Image_Default_Audit.csv"
GALLERY_DUPLICATE_AUDIT = DATABASE_DIR / "Printify_Gallery_Duplicate_Audit.csv"
LIVE_GALLERY_AUDIT = DATABASE_DIR / "eBay_Live_Gallery_Duplicate_Audit.csv"
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


def _retired_old_ids():
    retired = set()
    for row in _read_csv(RETIRE_QUEUE):
        if (row.get("Status") or "").strip() == "RETIRED_CONFIRMED":
            old_id = (row.get("Old_ID") or "").strip()
            if old_id:
                retired.add(old_id)
    return retired


def _title_only_issue(qa):
    if not qa:
        return False
    issues = [
        issue.strip()
        for issue in str(qa.get("Issues") or "").split(";")
        if issue.strip()
    ]
    return bool(issues) and all(issue.startswith("title_length_") for issue in issues)


def _qa_issues(qa):
    if not qa:
        return []
    return [
        issue.strip()
        for issue in str(qa.get("Issues") or "").split(";")
        if issue.strip()
    ]


def _description_note_only_issue(qa):
    issues = _qa_issues(qa)
    return bool(issues) and all(issue == "missing_image_note" for issue in issues)


def _copy_only_issue(qa):
    issues = _qa_issues(qa)
    return bool(issues) and all(
        issue == "missing_image_note" or issue.startswith("title_length_")
        for issue in issues
    )


def _default_needs_action(default_row):
    if not default_row:
        return False
    product_type = str(default_row.get("Product_Type") or "").strip().lower()
    status = str(default_row.get("Status") or "").strip()
    ebay_item_id = str(default_row.get("eBay_Item_ID") or "").strip()
    if product_type.startswith("sticker"):
        # Sticker expansion is frozen. Legacy sticker source-image issues are
        # tracked by cover/gallery history, but they must not block the current
        # Poster/Acrylic/Etsy experiments.
        return False
    error = (default_row.get("Error") or "").strip()
    if error:
        return True
    try:
        selected = int(default_row.get("Selected_Count") or 0)
        expected = int(default_row.get("Expected_Count") or 0)
        defaults = int(default_row.get("Default_Count") or 0)
    except ValueError:
        return default_row.get("Result") != "OK"
    # Multiple Printify official/default mockups are allowed; they help buyers
    # understand physical context. Gate only true insufficiency.
    return selected < expected or defaults < 1


def _gallery_duplicate_needs_action(gallery_row):
    if not gallery_row:
        return False
    result = (gallery_row.get("Result") or "").strip()
    if result in {"", "OK"}:
        return False
    if result == "CHECK_CUSTOM_GALLERY_REPEATS_RISK":
        try:
            selected = int(gallery_row.get("Selected_Count") or 0)
            unique = int(gallery_row.get("Unique_Visual_Count") or 0)
            exact = int(gallery_row.get("Exact_Duplicate_Count") or 0)
            near = int(gallery_row.get("Near_Duplicate_Count") or 0)
        except ValueError:
            return True
        # Custom concept/detail images are allowed for Poster/Acrylic when
        # they are visually unique and the listing copy explains that the main
        # artwork is the produced item. Treat that case as an advisory, not a
        # hard publish blocker.
        if selected > 0 and unique >= selected and exact == 0 and near == 0:
            return False
    return True


def _live_gallery_clears_source_risk(gallery_row, live_row):
    if not gallery_row or not live_row:
        return False
    if (gallery_row.get("Result") or "").strip() != "CHECK_CUSTOM_GALLERY_REPEATS_RISK":
        return False
    return (live_row.get("Result") or "").strip() in {"OK", "OK_DOM_DUPLICATE_ONLY"}


def _priority(row, qa, cover_fix, default_check, gallery_duplicate):
    product_type = str(row.get("Product_Type") or "").strip()
    if cover_fix:
        return 100
    if gallery_duplicate:
        return 91
    if default_check:
        return 88
    if product_type.startswith("Sticker"):
        return 25
    bucket = row.get("Action_Bucket")
    if qa and int(qa.get("Issue_Count") or 0) > 0 and not _copy_only_issue(qa):
        return 90
    if _copy_only_issue(qa):
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


def _recommend(row, copy, qa, cover_fix, default_check, gallery_duplicate):
    if cover_fix:
        return (
            "FIX_LIVE_COVER_SOURCE_OR_REPLACE",
            "Live eBay buyer page uses a single U/detail image instead of the local cover. Repair Printify source defaults and re-sync; if eBay Inventory-managed variation images still reject the repair, create a verified replacement listing and retire the bad one.",
            "medium",
            False,
        )
    if gallery_duplicate:
        return (
            "FIX_PRINTIFY_DUPLICATE_GALLERY_BEFORE_MORE_SYNC",
            f"Printify selected gallery has repeated or risky buyer-facing images: {gallery_duplicate.get('Result')} selected={gallery_duplicate.get('Selected_Count')} unique={gallery_duplicate.get('Unique_Visual_Count')} notes={gallery_duplicate.get('Notes')}",
            "medium",
            False,
        )
    if default_check:
        return (
            "FIX_PRINTIFY_IMAGE_INSUFFICIENCY_BEFORE_PUBLISH",
            "Printify image audit shows too few selected mockups or no default image. Multiple official/default mockups are allowed when the custom design is present.",
            "medium",
            False,
        )
    if str(row.get("Product_Type") or "").strip().startswith("Sticker"):
        return (
            "HOLD_STICKER_FROZEN",
            "Sticker expansion and repair are frozen by Rex because the eBay sticker market is too price-compressed; keep only passive monitoring unless deletion/retirement is explicitly selected later.",
            "local",
            True,
        )
    bucket = row.get("Action_Bucket")
    issue_count = int((qa or {}).get("Issue_Count") or 0)
    if issue_count and _copy_only_issue(qa):
        if _description_note_only_issue(qa):
            return (
                "LOCAL_DESCRIPTION_IMAGE_NOTE_PATCH",
                "Description is missing the buyer-facing note that only the main artwork is the produced item and supporting images are conceptual/detail previews.",
                "low",
                True,
            )
        return (
            "LOCAL_TITLE_LENGTH_REPAIR_FOR_NEXT_SYNC",
            f"Copy-only QA issue: {(qa or {}).get('Issues')}. Repair title length and/or add the buyer-facing image note before the next safe sync.",
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
    retired_old_ids = _retired_old_ids()
    cover_fix_by_id = {
        item_id: row
        for item_id, row in _by_id(_read_csv(COVER_FIX_QUEUE)).items()
        if item_id not in retired_old_ids
    }
    default_audit_by_id = _by_id(_read_csv(PRINTIFY_DEFAULT_AUDIT))
    gallery_duplicate_by_id = _by_id(_read_csv(GALLERY_DUPLICATE_AUDIT))
    live_gallery_by_id = _by_id(_read_csv(LIVE_GALLERY_AUDIT))
    rows = []
    for item in registry:
        copy = copy_by_id.get(item.get("ID"))
        qa = qa_by_id.get(item.get("ID"))
        cover_fix = cover_fix_by_id.get(item.get("ID"))
        default_row = default_audit_by_id.get(item.get("ID"))
        gallery_duplicate = gallery_duplicate_by_id.get(item.get("ID"))
        default_check = _default_needs_action(default_row)
        if _live_gallery_clears_source_risk(gallery_duplicate, live_gallery_by_id.get(item.get("ID"))):
            gallery_duplicate = None
        gallery_check = gallery_duplicate if _gallery_duplicate_needs_action(gallery_duplicate) else None
        action, reason, dependency, can_do_now = _recommend(item, copy, qa, cover_fix, default_check, gallery_check)
        rows.append(
            {
                "Priority": _priority(item, qa, cover_fix, default_check, gallery_check),
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
