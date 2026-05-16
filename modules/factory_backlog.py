"""Build a durable monthly factory backlog from current queues.

This is a local-only coordinator artifact. It does not touch marketplace
accounts; it turns the current action queues, cover gates, Etsy readiness, and
product R&D packets into one sortable backlog that can survive chat/context
loss.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
SUPERVISOR_COOLDOWN_MINUTES = 120

ACTION_QUEUE = DATABASE_DIR / "Factory_Autopilot_Action_Queue.csv"
MARKET_QUEUE = DATABASE_DIR / "Market_Signal_Action_Queue.csv"
COVER_REPAIR_DECISIONS = DATABASE_DIR / "eBay_Cover_Repair_Decisions.csv"
COVER_REPLACEMENT_QUEUE = DATABASE_DIR / "eBay_Cover_Replacement_Queue.csv"
GALLERY_REPLACEMENT_QUEUE = DATABASE_DIR / "eBay_Gallery_Replacement_Queue.csv"
REPLACEMENT_DRAFT_LOG = DATABASE_DIR / "eBay_Replacement_Draft_Log.csv"
PRINTIFY_GALLERY_REPAIR_QUEUE = DATABASE_DIR / "Printify_Gallery_Repair_Queue.csv"
TRAFFIC_DIAGNOSIS = DATABASE_DIR / "eBay_Traffic_Diagnosis.csv"
PERFORMANCE_LOG = DATABASE_DIR / "Performance_Log.csv"
EBAY_EXPERIMENT_REPORT = DATABASE_DIR / "eBay_Traffic_Experiment_Report.csv"
PRINTIFY_PRODUCTION_DESIGN_AUDIT = DATABASE_DIR / "Printify_Production_Design_Audit.csv"
ETSY_LIVE_AUDIT = DATABASE_DIR / "Etsy_Digital_Live_Audit.csv"
BLUEPRINT_PLAN = DATABASE_DIR / "Product_Blueprint_Next_Test_Plan.csv"
FALLBACK_EVAL = PROJECT_ROOT / "Review_Packets" / "FALLBACK_PROJECTS_ENGINEERING_EVAL_20260507_1108.md"
SSD_MIGRATION_PLAN = PROJECT_ROOT / "Review_Packets" / "SSD_1TB_ASSET_MIGRATION_PLAN.md"
SSD_MIGRATION_INVENTORY = DATABASE_DIR / "SSD_Migration_Inventory.csv"
ETSY_DIGITAL_PACKET = DATABASE_DIR / "Etsy_Digital_Final_Upload_Packet.csv"
ETSY_DIGITAL_METADATA = DATABASE_DIR / "Digital_Etsy_Metadata.csv"
ETSY_GRAY_QUEUE = DATABASE_DIR / "Etsy_Digital_Gray_Launch_Queue.csv"
ETSY_FEE_LEDGER = DATABASE_DIR / "Etsy_Fee_Ledger.csv"
ETSY_FEE_KILL_SWITCH = DATABASE_DIR / "Etsy_Fee_Kill_Switch.json"
ACCOUNT_RISK_STATE = DATABASE_DIR / "Account_Risk_State.json"
ETSY_POD_READY_FULL = DATABASE_DIR / "Etsy_POD_Printify_Launch_Ready_Full.csv"
ETSY_POD_CANDIDATES = DATABASE_DIR / "Etsy_POD_Next_Batch_Candidates.csv"
ETSY_LAUNCH_PLAN = DATABASE_DIR / "Etsy_launch_plan.csv"
ETSY_PRINTIFY_LAUNCH_LOG = DATABASE_DIR / "Etsy_Printify_Launch_Log.csv"
ETSY_DARWINIAN_QUEUE = DATABASE_DIR / "Etsy_Darwinian_Lab_V7_Queue.csv"
ETSY_DARWINIAN_MJ_QUEUE = DATABASE_DIR / "Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv"
ETSY_DARWINIAN_PACKET = DATABASE_DIR / "Etsy_Darwinian_Lab_V7_Listing_Packet.csv"
ETSY_DARWINIAN_UPLOAD = DATABASE_DIR / "Etsy_Darwinian_Lab_V7_Upload_Queue.csv"
ETSY_DARWINIAN_PLAN = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_V7_DARWINIAN_LAB_PLAN.md"
ETSY_DIGITAL_PREVIEW_ASSETS = DATABASE_DIR / "Etsy_Digital_Preview_Assets.csv"
ETSY_DIGITAL_PHOTO_REPAIR_LOG = DATABASE_DIR / "Etsy_Digital_Photo_Repair_Log.csv"
SUPERVISOR_STATE = DATABASE_DIR / "Factory_Autopilot_State.json"
STRATEGIC_MODE = DATABASE_DIR / "Strategic_Mode.json"
SHOCK_ROSTER = DATABASE_DIR / "Shock_And_Awe_Showcase_Roster.csv"
SHOCK_QUEUE = DATABASE_DIR / "Shock_And_Awe_Printify_Private_Queue.csv"
SHOCK_SPEC = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_SPEC_SHEETS_20260509.md"
SHOCK_V5_QUEUE = DATABASE_DIR / "Shock_And_Awe_V5_Zone2_Printify_Private_Queue.csv"
SHOCK_V5_SPEC = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_V5_ZONE2_CONCEPTS_20260509.md"
SHOCK_V5_RND = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_V5_BLUEPRINT_RND_20260509.md"
SHOCK_V5_MJ_QUEUE = DATABASE_DIR / "Shock_And_Awe_V5_MJ_Dispatch_Queue.csv"
SHOCK_V5_ZONES13_MJ_QUEUE = DATABASE_DIR / "Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv"
SHOCK_V5_RECOVERY_QUEUE = DATABASE_DIR / "Shock_And_Awe_V5_Recovery_MJ_Queue.csv"
SHOCK_V5_RECOVERY_REPORT = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_V5_RECOVERY_QUEUE.md"
SHOCK_V5_UI_SUBMIT_PACKET = DATABASE_DIR / "Shock_And_Awe_V5_UI_Submission_Packet.csv"
SHOCK_V5_UI_SUBMIT_REPORT = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_V5_UI_SUBMISSION_PACKET_latest.md"
SHOCK_V5_DEMO_INDEX = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_V5_PARTNER_DEMO_INDEX_20260509.md"
SHOCK_BLUEPRINT_RND = DATABASE_DIR / "Shock_And_Awe_Blueprint_RnD.csv"
SHOCK_V5_PRIVATE_DRAFTS = DATABASE_DIR / "Shock_And_Awe_V5_Printify_Private_Drafts.csv"
SHOCK_V5_FINAL_PACKET = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_V5_ZONE2_FINAL_PACKET_20260509.md"
SHOCK_V5_ZONES13_SELECTION = DATABASE_DIR / "Shock_And_Awe_V5_Zones1_3_Final_Selection.csv"
SHOCK_V5_ZONES13_PRODUCTION = DATABASE_DIR / "Shock_And_Awe_V5_Zones1_3_Printify_Production_Files.csv"
SHOCK_V5_ZONES13_PRIVATE_DRAFTS = DATABASE_DIR / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Drafts.csv"
SHOCK_V5_PRIVATE_STATUS = PROJECT_ROOT / "Review_Packets" / "OPERATION_SHOCK_AND_AWE_PRIVATE_SHOWCASE_STATUS_latest.md"
GEMINI_BRIDGE_DIR = PROJECT_ROOT / "Review_Packets" / "Gemini_Bridge"
GEMINI_SUPERVISOR_STATE = DATABASE_DIR / "Gemini_Supervisor_Checkin_State.json"
GEMINI_CHAT_SYNC_STATE = DATABASE_DIR / "Gemini_Chat_Sync_State.json"
TO_GREY_LATEST = GEMINI_BRIDGE_DIR / "TO_GREY_latest.md"
FROM_GREY_LATEST = GEMINI_BRIDGE_DIR / "FROM_GREY_latest.md"
FROM_GEMINI_CHAT_LATEST = GEMINI_BRIDGE_DIR / "FROM_GEMINI_CHAT_latest.md"
FIRST_AUDIT_MANIFEST = DATABASE_DIR / "First_Audit_001_Asset_Manifest.csv"
FIRST_AUDIT_GUARD_AUDIT = DATABASE_DIR / "First_Audit_001_Guard_Audit.csv"
FIRST_AUDIT_EXTENSION = DATABASE_DIR / "First_Audit_001_Extension_Candidates.csv"
FIRST_AUDIT_LOOKBOOK = PROJECT_ROOT / "Review_Packets" / "First_Audit_001" / "THE_FIRST_AUDIT_001_LOOKBOOK.pdf"
FIRST_AUDIT_CYBER_QUEUE = DATABASE_DIR / "First_Audit_Cyber_Renaissance_Draft_Queue.csv"
FIRST_AUDIT_CYBER_MJ_QUEUE = DATABASE_DIR / "First_Audit_Cyber_Renaissance_MJ_Dispatch_Queue.csv"
FIRST_AUDIT_CYBER_MJ_PACKET = PROJECT_ROOT / "Review_Packets" / "First_Audit_001" / "FIRST_AUDIT_CYBER_RENAISSANCE_MJ_DISPATCH_PACKET.md"
FIRST_AUDIT_CYBER_GRID_REVIEW = PROJECT_ROOT / "Review_Packets" / "First_Audit_001" / "FIRST_AUDIT_CYBER_RENAISSANCE_GRID_REVIEW.md"
FIRST_AUDIT_CYBER_CONTACT_SHEET = PROJECT_ROOT / "Review_Packets" / "First_Audit_001" / "FIRST_AUDIT_CYBER_RENAISSANCE_GRID_CONTACT_SHEET.jpg"
FIRST_AUDIT_CYBER_PRESELECT = PROJECT_ROOT / "Review_Packets" / "First_Audit_001" / "FIRST_AUDIT_CYBER_RENAISSANCE_TECHNICAL_PRESELECT.md"
FIRST_AUDIT_CYBER_PRESELECT_SHEET = PROJECT_ROOT / "Review_Packets" / "First_Audit_001" / "FIRST_AUDIT_CYBER_RENAISSANCE_PRESELECT_CONTACT_SHEET.jpg"
V155_PURGE_REPORT = PROJECT_ROOT / "Reports" / "V155_Great_Purge_And_First_Release.md"
V155_PURGE_CANDIDATES = DATABASE_DIR / "V155_Etsy_Purge_Candidates.csv"
V155_RELEASE_DIR = PROJECT_ROOT / "Release" / "OC-V155-001-Executive-Jade-Desk-Gift"
NETWORK_PATH_STATE = DATABASE_DIR / "Network_Path_State.json"
MONTHLY_RUNWAY_STATE = DATABASE_DIR / "Monthly_Task_Runway_State.json"
V16_AESTHETIC_DNA_MATRIX = DATABASE_DIR / "V16_Aesthetic_DNA_Matrix.csv"
V16_AESTHETIC_DNA_PACKET = PROJECT_ROOT / "Review_Packets" / "V16_Aesthetic_DNA_Matrix.md"
ADOBE_STOCK_KEYWORD_PACK = DATABASE_DIR / "Adobe_Stock_Keyword_Pack.csv"
ADOBE_STOCK_METADATA_SCHEMA = DATABASE_DIR / "Adobe_Stock_Metadata_Schema.csv"
ADOBE_STOCK_SCAFFOLD = PROJECT_ROOT / "Review_Packets" / "Adobe_Stock_Passive_Fortress_Scaffold.md"
PERFORMANCE_LIFECYCLE_RULES = DATABASE_DIR / "Performance_Lifecycle_Rules.csv"
PERFORMANCE_LIFECYCLE_PACKET = PROJECT_ROOT / "Review_Packets" / "Performance_Lifecycle_Autopilot.md"
PROJECT_MIRROR_POOL_INDEX = DATABASE_DIR / "Aesthetic_DNA_Pool_Index.csv"
PROJECT_MIRROR_SOURCE_CANDIDATES = DATABASE_DIR / "Aesthetic_DNA_Source_Candidates.csv"
PROJECT_MIRROR_DISTILLATION_JOBS = DATABASE_DIR / "Project_Mirror_Distillation_Jobs.csv"
PROJECT_MIRROR_MENTOR_DNA = DATABASE_DIR / "Project_Mirror_Mentor_DNA_Draft.csv"
PROJECT_MIRROR_AB_QUEUE = DATABASE_DIR / "Project_Mirror_AB_MJ_Test_Queue.csv"
PROJECT_MIRROR_AB_PACKET = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_AB_TEST_QUEUE.md"
PROJECT_MIRROR_DISPATCH_QUEUE = DATABASE_DIR / "Project_Mirror_MJ_Dispatch_Queue.csv"
PROJECT_MIRROR_GRID_REVIEW = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_AB_GRID_REVIEW.md"
PROJECT_MIRROR_CONTACT_SHEET = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_AB_GRID_CONTACT_SHEET.jpg"
PROJECT_MIRROR_SCORECARD = DATABASE_DIR / "Project_Mirror_AB_Scorecard.csv"
PROJECT_MIRROR_SCORECARD_PACKET = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_AB_SCORECARD.md"
PROJECT_MIRROR_PROMOTED_DNA = DATABASE_DIR / "Project_Mirror_Promoted_DNA.csv"
PROJECT_MIRROR_PROMOTED_PACKET = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_PROMOTED_DNA.md"
PROJECT_MIRROR_PRODUCT_MATRIX = DATABASE_DIR / "Project_Mirror_Product_Matrix.csv"
PROJECT_MIRROR_PRODUCT_MATRIX_PACKET = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_PRODUCT_MATRIX.md"
PROJECT_MIRROR_REFINEMENT_QUEUE = DATABASE_DIR / "Project_Mirror_Production_Refinement_Queue.csv"
PROJECT_MIRROR_REFINEMENT_PACKET = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_PRODUCTION_REFINEMENT_QUEUE.md"
PROJECT_MIRROR_REFINEMENT_MJ_QUEUE = DATABASE_DIR / "Project_Mirror_Refinement_MJ_Dispatch_Queue.csv"
PROJECT_MIRROR_REFINEMENT_MJ_PACKET = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_REFINEMENT_MJ_DISPATCH_QUEUE.md"
PROJECT_MIRROR_REFINEMENT_GRID_REVIEW = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_REFINEMENT_GRID_REVIEW.md"
PROJECT_MIRROR_REFINEMENT_CONTACT_SHEET = PROJECT_ROOT / "Review_Packets" / "Project_Mirror" / "PROJECT_MIRROR_REFINEMENT_GRID_CONTACT_SHEET.jpg"

BACKLOG_CSV = DATABASE_DIR / "Factory_Backlog.csv"
BACKLOG_MD = DATABASE_DIR / "Factory_Backlog.md"

HEADERS = [
    "Priority",
    "Lane",
    "Task",
    "Status",
    "Blocker",
    "Command",
    "Done_When",
    "Risk",
    "Network_Need",
    "Owner",
]


def now_text() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def count_by(path: Path, column: str) -> Counter:
    counts: Counter = Counter()
    for row in read_csv(path):
        counts[clean(row.get(column)) or "Unknown"] += 1
    return counts


def count_market_actions_non_sticker() -> Counter:
    """Count actionable market tasks after Rex froze new Sticker expansion."""
    counts: Counter = Counter()
    for row in read_csv(MARKET_QUEUE):
        if clean(row.get("Product_Type")).lower() == "sticker":
            continue
        counts[clean(row.get("Recommended_Action")) or "Unknown"] += 1
    return counts


def pending_gallery_replacement_rows() -> list[dict[str, str]]:
    """Rows that still need a one-off local GalleryFix draft.

    The gallery queue is a preparation artifact. Once the local replacement
    draft exists, the same queue row must not keep re-entering the monthly loop
    as READY; otherwise the cruise dispatcher burns turns recreating a report.
    """
    created = {
        clean(row.get("Replacement_ID"))
        for row in read_csv(REPLACEMENT_DRAFT_LOG)
        if clean(row.get("Status")) == "GALLERY_LOCAL_DRAFT_CREATED"
    }
    return [
        row
        for row in read_csv(GALLERY_REPLACEMENT_QUEUE)
        if clean(row.get("Replacement_Status")) == "READY_FOR_LOCAL_DRAFT_WHEN_APPROVED"
        and clean(row.get("Replacement_SKU")) not in created
    ]


def csv_count(path: Path) -> int:
    return len(read_csv(path))


def is_missing_or_stale(target: Path, source: Path) -> bool:
    if not source.exists():
        return False
    if not target.exists():
        return True
    try:
        return target.stat().st_mtime < source.stat().st_mtime
    except OSError:
        return True


def file_age_minutes(path: Path) -> int | None:
    if not path.exists():
        return None
    try:
        age_seconds = datetime.now(ZoneInfo("America/New_York")).timestamp() - path.stat().st_mtime
    except OSError:
        return None
    return max(0, int(age_seconds // 60))


def is_recent(path: Path, max_minutes: int) -> bool:
    age = file_age_minutes(path)
    return age is not None and age < max_minutes


def supervisor_action_recent_status(command: str) -> tuple[str, str] | None:
    """Translate recently completed supervisor leaves into cooldown states.

    The action queue is intentionally durable, but it should not keep re-selecting
    short read-only probes every heartbeat when their output files are fresh.
    """
    checks = [
        (
            "ebay_sellerhub_snapshot.py",
            PERFORMANCE_LOG,
            120,
            "DONE_RECENT_SNAPSHOT",
            "SellerHub snapshot",
        ),
        (
            "printify_design_audit.py",
            PRINTIFY_PRODUCTION_DESIGN_AUDIT,
            120,
            "DONE_RECENT_DESIGN_AUDIT",
            "Printify production-design audit",
        ),
        (
            "etsy_live_audit.py",
            ETSY_LIVE_AUDIT,
            120,
            "DONE_RECENT_ETSY_LIVE_AUDIT",
            "Etsy live audit",
        ),
        (
            "ebay_experiment_report.py",
            EBAY_EXPERIMENT_REPORT,
            180,
            "DONE_RECENT_EXPERIMENT_REPORT",
            "eBay experiment report",
        ),
    ]
    for needle, output_path, cooldown_minutes, done_status, label in checks:
        if needle not in command:
            continue
        age = file_age_minutes(output_path)
        if is_recent(output_path, cooldown_minutes):
            return (
                done_status,
                (
                    f"{label} output is fresh "
                    f"(age={age}m; cooldown={cooldown_minutes}m). "
                    "Continue-monthly should move to production/market tasks instead of rerunning this leaf."
                ),
            )
    return None


def etsy_gray_summary() -> dict[str, object]:
    queue_rows = read_csv(ETSY_GRAY_QUEUE)
    ledger_rows = read_csv(ETSY_FEE_LEDGER)
    published = [row for row in queue_rows if clean(row.get("Launch_Status")) == "PUBLISHED_UI_CONFIRMED"]
    ready = [
        row
        for row in queue_rows
        if clean(row.get("Launch_Status")) in {"READY_BLOCKED_ETSY_AUTH", "READY_TO_PUBLISH", "READY_UI_PUBLISH", "READY_API_PUBLISH"}
        and not clean(row.get("Etsy_Listing_ID"))
    ]
    confirmed_spend = 0.0
    daily_spend = 0.0
    today_prefix = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
    for row in ledger_rows:
        if clean(row.get("Status")).startswith("CONFIRMED"):
            try:
                amount = float(row.get("Confirmed_Spent_USD") or 0)
            except ValueError:
                amount = 0.0
            confirmed_spend += amount
            if clean(row.get("Timestamp")).startswith(today_prefix):
                daily_spend += amount
    fee_config = {}
    if ETSY_FEE_KILL_SWITCH.exists():
        try:
            fee_config = json.loads(ETSY_FEE_KILL_SWITCH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            fee_config = {}
    daily_cap = float(fee_config.get("daily_listing_fee_cap_usd", 0) or 0)
    expected_fee = float(fee_config.get("expected_listing_fee_usd", 0.20) or 0.20)
    return {
        "queue_rows": len(queue_rows),
        "published": len(published),
        "ready": len(ready),
        "confirmed_spend": confirmed_spend,
        "daily_spend": daily_spend,
        "daily_cap": daily_cap,
        "expected_fee": expected_fee,
        "daily_fee_slots": max(0, int((daily_cap - daily_spend + 1e-9) / expected_fee)) if daily_cap else 999,
    }


def etsy_metadata_ready_count() -> int:
    return sum(
        1
        for row in read_csv(ETSY_DIGITAL_METADATA)
        if clean(row.get("Status")) == "READY_FOR_ETSY_DRAFT"
    )


def etsy_digital_photo_repair_summary() -> dict[str, object]:
    """Track existing Etsy digital listings that still need richer preview photos.

    This is a safe edit lane: it appends preview images to already-published
    digital listings and does not create new Etsy listings or listing fees.
    The actual uploader still verifies the live image count through Etsy API
    before uploading, so this local summary is used only to surface work.
    """
    preview_rows = read_csv(ETSY_DIGITAL_PREVIEW_ASSETS)
    queue_rows = read_csv(ETSY_GRAY_QUEUE)
    live_ids = {
        clean(row.get("ID"))
        for row in queue_rows
        if clean(row.get("Etsy_Listing_ID"))
    }
    locally_packable_ids: set[str] = set()
    for row in queue_rows:
        item_id = clean(row.get("ID"))
        if not item_id or item_id not in live_ids:
            continue
        pack_dir_value = clean(row.get("Pack_Dir"))
        zip_value = clean(row.get("Zip_Path"))
        pack_dir = Path(pack_dir_value) if pack_dir_value else (Path(zip_value).with_suffix("") if zip_value else None)
        if pack_dir and pack_dir.exists():
            locally_packable_ids.add(item_id)
    preview_ids = {
        clean(row.get("ID"))
        for row in preview_rows
        if clean(row.get("ID")) in live_ids
    }
    repaired_ids = {
        clean(row.get("ID"))
        for row in read_csv(ETSY_DIGITAL_PHOTO_REPAIR_LOG)
        if clean(row.get("Status")) in {"REPAIRED", "SKIP_ALREADY_RICH"}
        and clean(row.get("After_Count"))
        and int(clean(row.get("After_Count")) or "0") >= 5
    }
    missing_preview_count = max(0, len(locally_packable_ids - preview_ids))
    remaining_ids = sorted(preview_ids - repaired_ids)
    return {
        "live_with_listing_id": len(live_ids),
        "locally_packable": len(locally_packable_ids),
        "preview_assets": len(preview_ids),
        "repaired_or_rich": len(repaired_ids),
        "remaining": len(remaining_ids),
        "missing_preview_count": missing_preview_count,
    }


def etsy_pod_launch_summary() -> dict[str, object]:
    """Summarize official Printify->Etsy POD launch rows that can still run.

    This is intentionally separate from the Etsy digital queue. Rex wants the
    monthly loop to move concrete product work forward, and the POD launch
    runner already owns fee/risk guards, mockup duplicate holds, and external-id
    reconciliation.
    """
    plan_rows = read_csv(ETSY_POD_READY_FULL)
    log_rows = read_csv(ETSY_PRINTIFY_LAUNCH_LOG)
    terminal_statuses = {
        "PUBLISHED",
        "PUBLISHED_EXTERNAL_PENDING",
        "PUBLISHED_EXTERNAL_CONFIRMED",
        "EXTERNAL_STILL_PENDING_NEEDS_RECONCILE",
        "HOLD_DUPLICATE_MOCKUPS",
        "HOLD_MOCKUP_INSUFFICIENT",
        "FAILED",
    }
    latest_by_id: dict[str, dict[str, str]] = {}
    for row in log_rows:
        item_id = clean(row.get("ID"))
        if item_id:
            latest_by_id[item_id] = row
    handled_ids = {
        item_id
        for item_id, row in latest_by_id.items()
        if clean(row.get("Status")) in terminal_statuses
    }
    ready_rows = [
        row
        for row in plan_rows
        if clean(row.get("ID"))
        and clean(row.get("ID")) not in handled_ids
        and clean(row.get("Launch_Status")).startswith("Draft_Prepared")
        and clean(row.get("Product_Type")) in {"Poster", "Acrylic"}
    ]
    counts = Counter(clean(row.get("Product_Type")) or "Unknown" for row in ready_rows)
    latest_status = clean(log_rows[-1].get("Status")) if log_rows else ""
    latest_by_product: dict[str, dict[str, str]] = {}
    for row in log_rows:
        product_id = clean(row.get("Printify_Etsy_Product_ID"))
        if product_id:
            latest_by_product[product_id] = row
    pending_external = [
        row
        for row in latest_by_product.values()
        if clean(row.get("Status")) == "PUBLISHED_EXTERNAL_PENDING"
    ]
    return {
        "plan_rows": len(plan_rows),
        "ready": len(ready_rows),
        "ready_by_type": dict(counts),
        "handled": len(handled_ids),
        "latest_status": latest_status,
        "pending_external": len(pending_external),
    }


def etsy_pod_candidate_summary() -> dict[str, object]:
    plan_rows = read_csv(ETSY_LAUNCH_PLAN)
    candidate_rows = read_csv(ETSY_POD_CANDIDATES)
    log_rows = read_csv(ETSY_PRINTIFY_LAUNCH_LOG)
    latest_by_id: dict[str, dict[str, str]] = {}
    for row in log_rows:
        item_id = clean(row.get("ID"))
        if item_id:
            latest_by_id[item_id] = row
    handled_statuses = {
        "PUBLISHED",
        "PUBLISHED_EXTERNAL_PENDING",
        "PUBLISHED_EXTERNAL_CONFIRMED",
        "EXTERNAL_STILL_PENDING_NEEDS_RECONCILE",
        "HOLD_DUPLICATE_MOCKUPS",
        "HOLD_MOCKUP_INSUFFICIENT",
        "FAILED",
    }
    unhandled = [
        row
        for row in plan_rows
        if clean(row.get("Product_Type")) in {"Poster", "Acrylic"}
        and clean(row.get("Launch_Status")).startswith("Draft_Prepared")
        and clean(latest_by_id.get(clean(row.get("ID")), {}).get("Status")) not in handled_statuses
    ]
    candidates_stale = is_missing_or_stale(ETSY_POD_CANDIDATES, ETSY_LAUNCH_PLAN)
    if ETSY_PRINTIFY_LAUNCH_LOG.exists() and ETSY_POD_CANDIDATES.exists():
        candidates_stale = candidates_stale or (
            ETSY_POD_CANDIDATES.stat().st_mtime < ETSY_PRINTIFY_LAUNCH_LOG.stat().st_mtime
        )
    return {
        "plan_rows": len(plan_rows),
        "candidates": len(candidate_rows),
        "unhandled_plan": len(unhandled),
        "candidates_stale": candidates_stale,
    }


def first_audit_cyber_summary() -> dict[str, object]:
    concept_rows = read_csv(FIRST_AUDIT_CYBER_QUEUE)
    mj_rows = read_csv(FIRST_AUDIT_CYBER_MJ_QUEUE)
    ready_concepts = [
        row
        for row in concept_rows
        if clean(row.get("status")).startswith("READY_FOR_MJ_DRAFT")
    ]
    mj_status = Counter(clean(row.get("Dispatch_Status")) or "Unknown" for row in mj_rows)
    harvest_status = Counter(clean(row.get("Harvest_Status")) or "Unknown" for row in mj_rows)
    grid_ready = (
        harvest_status.get("GRID_FOUND", 0)
        + harvest_status.get("READY_FOR_VISUAL_QA", 0)
        + harvest_status.get("VISUAL_QA_PASSED", 0)
    )
    queue_due = bool(ready_concepts) and (
        not FIRST_AUDIT_CYBER_MJ_QUEUE.exists()
        or FIRST_AUDIT_CYBER_MJ_QUEUE.stat().st_mtime < FIRST_AUDIT_CYBER_QUEUE.stat().st_mtime
    )
    review_due = bool(grid_ready) and (
        not FIRST_AUDIT_CYBER_GRID_REVIEW.exists()
        or not FIRST_AUDIT_CYBER_CONTACT_SHEET.exists()
        or FIRST_AUDIT_CYBER_GRID_REVIEW.stat().st_mtime < FIRST_AUDIT_CYBER_MJ_QUEUE.stat().st_mtime
    )
    preselect_due = bool(grid_ready) and (
        not FIRST_AUDIT_CYBER_PRESELECT.exists()
        or not FIRST_AUDIT_CYBER_PRESELECT_SHEET.exists()
        or FIRST_AUDIT_CYBER_PRESELECT.stat().st_mtime < FIRST_AUDIT_CYBER_MJ_QUEUE.stat().st_mtime
    )
    return {
        "concepts": len(concept_rows),
        "ready_concepts": len(ready_concepts),
        "mj_rows": len(mj_rows),
        "mj_ready": mj_status.get("READY_FOR_MJ", 0),
        "mj_submitted": mj_status.get("MJ_SUBMITTED", 0),
        "mj_failed": mj_status.get("MJ_DISPATCH_FAILED", 0),
        "mj_unconfirmed": mj_status.get("MJ_SUBMIT_UNCONFIRMED_RETRY", 0),
        "grid_ready": grid_ready,
        "harvest_ready": harvest_status.get("READY_FOR_VISUAL_QA", 0) + harvest_status.get("VISUAL_QA_PASSED", 0),
        "queue_due": queue_due,
        "review_due": review_due,
        "preselect_due": preselect_due,
    }


def state() -> dict:
    if not SUPERVISOR_STATE.exists():
        return {}
    try:
        return json.loads(SUPERVISOR_STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def strategic_mode() -> dict:
    if not STRATEGIC_MODE.exists():
        return {}
    try:
        return json.loads(STRATEGIC_MODE.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}


def account_state(platform: str) -> dict:
    return read_json(ACCOUNT_RISK_STATE).get("states", {}).get(platform, {})


def etsy_write_allowed() -> bool:
    state = account_state("etsy")
    return bool(state.get("write_allowed", True))


def etsy_paid_publish_allowed() -> bool:
    state = account_state("etsy")
    return bool(state.get("paid_publish_allowed", True)) and etsy_write_allowed()


def etsy_risk_blocker() -> str:
    state = account_state("etsy")
    risk_state = clean(state.get("risk_state")) or "UNKNOWN"
    notes = clean(state.get("notes"))
    if notes:
        return f"Etsy risk_state={risk_state}; {notes}"
    return f"Etsy risk_state={risk_state}"


def ebay_paid_publish_allowed() -> bool:
    state = account_state("ebay")
    return bool(state.get("paid_publish_allowed", True)) and bool(state.get("write_allowed", True))


def ebay_risk_blocker() -> str:
    state = account_state("ebay")
    risk_state = clean(state.get("risk_state")) or "UNKNOWN"
    notes = clean(state.get("notes"))
    if notes:
        return f"eBay risk_state={risk_state}; {notes}"
    return f"eBay risk_state={risk_state}"


def minutes_since_iso(value: str | None) -> int:
    if not value:
        return 10**9
    try:
        prior = datetime.fromisoformat(value)
        if prior.tzinfo is None:
            prior = prior.replace(tzinfo=ZoneInfo("America/New_York"))
        return int((datetime.now(ZoneInfo("America/New_York")) - prior.astimezone(ZoneInfo("America/New_York"))).total_seconds() // 60)
    except ValueError:
        return 10**9


def supervisor_state_age_minutes() -> int:
    """Age of the last heavy local supervisor refresh.

    The monthly-task loop should not keep selecting supervisor maintenance just
    because it is safe. It is useful state refresh work, but after one successful
    run it should cool down so core production tasks can take the lead.
    """

    supervisor_state = read_json(SUPERVISOR_STATE)
    timestamp = (
        clean(supervisor_state.get("generated_at"))
        or clean(supervisor_state.get("timestamp"))
        or clean(supervisor_state.get("updated_at"))
    )
    age = minutes_since_iso(timestamp or None)
    return max(0, age)


def network_path_status() -> tuple[bool, str]:
    state = read_json(NETWORK_PATH_STATE)
    timestamp = clean(state.get("timestamp"))
    age = minutes_since_iso(timestamp or None)
    active = clean(state.get("active_alias")) or "UNKNOWN"
    speed = clean(state.get("active_link_speed"))
    alert = clean(state.get("alert"))
    due = age >= 30 or bool(alert) or not NETWORK_PATH_STATE.exists()
    summary = f"active={active}; speed={speed or 'UNKNOWN'}; last_age={age}m; alert={alert or 'none'}"
    return due, summary


def project_mirror_summary() -> dict[str, object]:
    pool_rows = read_csv(PROJECT_MIRROR_POOL_INDEX)
    source_rows = read_csv(PROJECT_MIRROR_SOURCE_CANDIDATES)
    jobs = read_csv(PROJECT_MIRROR_DISTILLATION_JOBS)
    mentor_rows = read_csv(PROJECT_MIRROR_MENTOR_DNA)
    ab_rows = read_csv(PROJECT_MIRROR_AB_QUEUE)
    dispatch_rows = read_csv(PROJECT_MIRROR_DISPATCH_QUEUE)
    score_rows = read_csv(PROJECT_MIRROR_SCORECARD)
    promoted_rows = read_csv(PROJECT_MIRROR_PROMOTED_DNA)
    matrix_rows = read_csv(PROJECT_MIRROR_PRODUCT_MATRIX)
    refinement_rows = read_csv(PROJECT_MIRROR_REFINEMENT_QUEUE)
    refinement_mj_rows = read_csv(PROJECT_MIRROR_REFINEMENT_MJ_QUEUE)
    job_status = Counter(clean(row.get("Status")) or "Unknown" for row in jobs)
    ab_status = Counter(clean(row.get("Status")) or "Unknown" for row in ab_rows)
    dispatch_status = Counter(clean(row.get("Dispatch_Status")) or "Unknown" for row in dispatch_rows)
    harvest_status = Counter(clean(row.get("Harvest_Status")) or "Unknown" for row in dispatch_rows)
    refinement_mj_status = Counter(clean(row.get("Dispatch_Status")) or "Unknown" for row in refinement_mj_rows)
    refinement_mj_harvest = Counter(clean(row.get("Harvest_Status")) or "Unknown" for row in refinement_mj_rows)
    accepted_refs = sum(1 for row in pool_rows if clean(row.get("Status")).startswith("ACCEPTED"))
    source_candidate_refs = sum(1 for row in pool_rows if clean(row.get("Status")) == "SOURCE_CANDIDATE_REVIEW")
    complete_pair_keys: dict[str, set[str]] = {}
    for row in dispatch_rows:
        if clean(row.get("Harvest_Status")) != "GRID_FOUND":
            continue
        sku = clean(row.get("Internal_SKU"))
        if not sku:
            continue
        pair_key = sku.rsplit("-", 1)[0]
        branch = "B" if sku.endswith("B_PROJECT_MIRROR") else "A" if sku.endswith("A_OLD_LOGIC") else sku
        complete_pair_keys.setdefault(pair_key, set()).add(branch)
    complete_pairs = sum(1 for branches in complete_pair_keys.values() if {"A", "B"}.issubset(branches))
    ab_due = bool(mentor_rows) and (
        not PROJECT_MIRROR_AB_QUEUE.exists()
        or is_missing_or_stale(PROJECT_MIRROR_AB_QUEUE, PROJECT_MIRROR_MENTOR_DNA)
        or is_missing_or_stale(PROJECT_MIRROR_AB_PACKET, PROJECT_MIRROR_MENTOR_DNA)
    )
    dispatch_due = bool(ab_rows) and (
        not PROJECT_MIRROR_DISPATCH_QUEUE.exists()
        or is_missing_or_stale(PROJECT_MIRROR_DISPATCH_QUEUE, PROJECT_MIRROR_AB_QUEUE)
    )
    contact_due = harvest_status.get("GRID_FOUND", 0) > 0 and (
        not PROJECT_MIRROR_CONTACT_SHEET.exists()
        or is_missing_or_stale(PROJECT_MIRROR_CONTACT_SHEET, PROJECT_MIRROR_DISPATCH_QUEUE)
        or is_missing_or_stale(PROJECT_MIRROR_GRID_REVIEW, PROJECT_MIRROR_DISPATCH_QUEUE)
    )
    score_due = complete_pairs > 0 and (
        not PROJECT_MIRROR_SCORECARD.exists()
        or is_missing_or_stale(PROJECT_MIRROR_SCORECARD, PROJECT_MIRROR_DISPATCH_QUEUE)
        or is_missing_or_stale(PROJECT_MIRROR_SCORECARD_PACKET, PROJECT_MIRROR_DISPATCH_QUEUE)
    )
    promoted_due = bool(score_rows) and (
        not PROJECT_MIRROR_PROMOTED_DNA.exists()
        or is_missing_or_stale(PROJECT_MIRROR_PROMOTED_DNA, PROJECT_MIRROR_SCORECARD)
        or is_missing_or_stale(PROJECT_MIRROR_PROMOTED_PACKET, PROJECT_MIRROR_SCORECARD)
    )
    matrix_due = bool(promoted_rows) and (
        not PROJECT_MIRROR_PRODUCT_MATRIX.exists()
        or is_missing_or_stale(PROJECT_MIRROR_PRODUCT_MATRIX, PROJECT_MIRROR_PROMOTED_DNA)
        or is_missing_or_stale(PROJECT_MIRROR_PRODUCT_MATRIX_PACKET, PROJECT_MIRROR_PROMOTED_DNA)
    )
    refinement_due = bool(matrix_rows) and (
        not PROJECT_MIRROR_REFINEMENT_QUEUE.exists()
        or is_missing_or_stale(PROJECT_MIRROR_REFINEMENT_QUEUE, PROJECT_MIRROR_PRODUCT_MATRIX)
        or is_missing_or_stale(PROJECT_MIRROR_REFINEMENT_PACKET, PROJECT_MIRROR_PRODUCT_MATRIX)
    )
    refinement_mj_due = bool(refinement_rows) and (
        not PROJECT_MIRROR_REFINEMENT_MJ_QUEUE.exists()
        or is_missing_or_stale(PROJECT_MIRROR_REFINEMENT_MJ_QUEUE, PROJECT_MIRROR_REFINEMENT_QUEUE)
        or is_missing_or_stale(PROJECT_MIRROR_REFINEMENT_MJ_PACKET, PROJECT_MIRROR_REFINEMENT_QUEUE)
    )
    refinement_contact_due = refinement_mj_harvest.get("GRID_FOUND", 0) > 0 and (
        not PROJECT_MIRROR_REFINEMENT_CONTACT_SHEET.exists()
        or is_missing_or_stale(PROJECT_MIRROR_REFINEMENT_CONTACT_SHEET, PROJECT_MIRROR_REFINEMENT_MJ_QUEUE)
        or is_missing_or_stale(PROJECT_MIRROR_REFINEMENT_GRID_REVIEW, PROJECT_MIRROR_REFINEMENT_MJ_QUEUE)
    )
    return {
        "pool_rows": len(pool_rows),
        "source_rows": len(source_rows),
        "jobs": len(jobs),
        "accepted_refs": accepted_refs,
        "source_candidate_refs": source_candidate_refs,
        "mentor_rows": len(mentor_rows),
        "ab_rows": len(ab_rows),
        "ab_due": ab_due,
        "waiting_images": job_status.get("WAITING_ACCEPTED_IMAGE", 0),
        "ready_for_vision": job_status.get("READY_FOR_VISION", 0),
        "ab_ready": ab_status.get("READY_FOR_MJ_DRAFT_GRID", 0),
        "dispatch_rows": len(dispatch_rows),
        "dispatch_due": dispatch_due,
        "dispatch_ready": dispatch_status.get("READY_FOR_MJ", 0),
        "dispatch_submitted": dispatch_status.get("MJ_SUBMITTED", 0),
        "grid_found": harvest_status.get("GRID_FOUND", 0),
        "complete_pairs": complete_pairs,
        "contact_due": contact_due,
        "contact_exists": PROJECT_MIRROR_CONTACT_SHEET.exists() and PROJECT_MIRROR_GRID_REVIEW.exists(),
        "score_rows": len(score_rows),
        "score_due": score_due,
        "promoted_rows": len(promoted_rows),
        "promoted_due": promoted_due,
        "matrix_rows": len(matrix_rows),
        "matrix_due": matrix_due,
        "refinement_rows": len(refinement_rows),
        "refinement_due": refinement_due,
        "refinement_mj_rows": len(refinement_mj_rows),
        "refinement_mj_due": refinement_mj_due,
        "refinement_mj_ready": refinement_mj_status.get("READY_FOR_MJ", 0),
        "refinement_mj_submitted": refinement_mj_status.get("MJ_SUBMITTED", 0),
        "refinement_mj_grid_found": refinement_mj_harvest.get("GRID_FOUND", 0),
        "refinement_contact_due": refinement_contact_due,
        "refinement_contact_exists": PROJECT_MIRROR_REFINEMENT_CONTACT_SHEET.exists() and PROJECT_MIRROR_REFINEMENT_GRID_REVIEW.exists(),
    }


def is_winddown_window() -> bool:
    current = datetime.now(ZoneInfo("America/New_York")).time()
    return current.hour == 5 and 30 <= current.minute <= 55


def add(rows: list[dict[str, str]], priority: int, lane: str, task: str, status: str, blocker: str, command: str, done_when: str, risk: str = "low", network: str = "local", owner: str = "Codex") -> None:
    rows.append(
        {
            "Priority": str(priority),
            "Lane": lane,
            "Task": task,
            "Status": status,
            "Blocker": blocker,
            "Command": command,
            "Done_When": done_when,
            "Risk": risk,
            "Network_Need": network,
            "Owner": owner,
        }
    )


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    mode = strategic_mode()
    supervisor = state()
    printify_ui = supervisor.get("printify_ui_status") or {}
    market_actions = count_by(MARKET_QUEUE, "Recommended_Action")
    market_actions_non_sticker = count_market_actions_non_sticker()
    repair_methods = count_by(COVER_REPAIR_DECISIONS, "Repair_Method")
    replacement_status = count_by(COVER_REPLACEMENT_QUEUE, "Replacement_Status")
    gallery_replacement_status = count_by(GALLERY_REPLACEMENT_QUEUE, "Replacement_Status")
    gallery_replacement_pending = pending_gallery_replacement_rows()
    diagnosis_count = csv_count(TRAFFIC_DIAGNOSIS)
    blueprint_count = csv_count(BLUEPRINT_PLAN)
    etsy_digital_count = csv_count(ETSY_DIGITAL_PACKET)
    etsy_metadata_ready = etsy_metadata_ready_count()
    etsy_gray = etsy_gray_summary()
    etsy_can_write = etsy_write_allowed()
    etsy_can_paid_publish = etsy_paid_publish_allowed()
    etsy_blocker = etsy_risk_blocker()
    ebay_can_paid_publish = ebay_paid_publish_allowed()
    ebay_blocker = ebay_risk_blocker()
    etsy_photo_repair = etsy_digital_photo_repair_summary()
    etsy_pod = etsy_pod_launch_summary()
    etsy_pod_candidates = etsy_pod_candidate_summary()
    etsy_darwinian_count = csv_count(ETSY_DARWINIAN_QUEUE)
    etsy_darwinian_assets = count_by(ETSY_DARWINIAN_QUEUE, "Asset_Status")
    etsy_darwinian_mj = count_by(ETSY_DARWINIAN_MJ_QUEUE, "Dispatch_Status")
    etsy_darwinian_harvest = count_by(ETSY_DARWINIAN_MJ_QUEUE, "Harvest_Status")
    first_audit_cyber = first_audit_cyber_summary()
    project_mirror = project_mirror_summary()

    v155_release_ready = (
        (V155_RELEASE_DIR / "01_Hero_Production.png").exists()
        and (V155_RELEASE_DIR / "02_Mockup_Luxury_Desk.jpg").exists()
        and (V155_RELEASE_DIR / "03_Mockup_Art_Gallery.jpg").exists()
        and (V155_RELEASE_DIR / "04_Narrative_Matrix.md").exists()
    )
    v155_active = V155_PURGE_REPORT.exists()
    v155_candidates = csv_count(V155_PURGE_CANDIDATES)
    add(
        rows,
        140,
        "v155_purge",
        "Run V15.5 low-value active listing purge audit and first weaponized release check",
        "DONE_CURRENT" if V155_PURGE_REPORT.exists() and v155_release_ready and v155_candidates == 0 else "READY",
        (
            f"purge_report={V155_PURGE_REPORT.exists()}; current_candidates={v155_candidates}; "
            f"weaponized_folder_ready={v155_release_ready}; this guards against drifting back into low-price blind volume."
        ),
        "py modules\\v155_purge_and_release.py --policy hard --max-price 15 --min-age-hours 48",
        "Low-value active Etsy purge candidates are audited; first V15.5 release folder has all four required files.",
        "low",
        "Etsy API",
    )

    network_due, network_summary = network_path_status()
    add(
        rows,
        35,
        "hardware_network",
        "Monitor whether Windows fell back from Ethernet to Wi-Fi",
        "READY" if network_due else "DONE_NOT_DUE",
        network_summary,
        "py modules\\network_path_monitor.py --expected-alias \"Ethernet 3\"",
        "Network path state is refreshed; notify Rex only if active path is not Ethernet 3 or Ethernet is down.",
        "low",
        "local",
    )

    add(
        rows,
        61,
        "project_mirror",
        "Maintain Project Mirror reference-derived aesthetic DNA scaffold",
        "DONE_SCAFFOLD_READY_SOURCE_REVIEW"
        if project_mirror["pool_rows"] and project_mirror["source_candidate_refs"]
        else "READY",
        (
            f"pool_slots={project_mirror['pool_rows']}; source_candidates={project_mirror['source_rows']}; "
            f"source_candidate_refs={project_mirror['source_candidate_refs']}; accepted_refs={project_mirror['accepted_refs']}."
        ),
        "py modules\\project_mirror_aesthetic_dna.py",
        "Project Mirror has a source pool, schema, source candidates, and review packet for premium DNA extraction.",
        "low",
        "local",
    )
    add(
        rows,
        60,
        "project_mirror",
        "Seed starter source candidates into Project Mirror pool",
        "DONE_SEEDED" if project_mirror["source_candidate_refs"] else "READY",
        (
            f"source_candidates={project_mirror['source_rows']}; "
            f"pool_source_candidate_refs={project_mirror['source_candidate_refs']}. "
            "Next step is accepted local-image review before any vision call."
        ),
        "py modules\\project_mirror_apply_source_candidates.py",
        "Vetted source-candidate URLs are recorded for DNA-only reference research without redistributing source images.",
        "low",
        "network-light",
    )
    add(
        rows,
        59,
        "project_mirror",
        "Prepare Project Mirror vision distillation jobs after accepted references exist",
        "READY"
        if project_mirror["ready_for_vision"]
        else "WAIT_ACCEPTED_IMAGES"
        if project_mirror["waiting_images"]
        else "READY",
        (
            f"jobs={project_mirror['jobs']}; ready_for_vision={project_mirror['ready_for_vision']}; "
            f"waiting_images={project_mirror['waiting_images']}; accepted_refs={project_mirror['accepted_refs']}."
        ),
        "py modules\\project_mirror_distiller_skeleton.py",
        "Vision jobs are ready only after local accepted references exist; otherwise do not spend vision/API calls.",
        "low",
        "local",
    )
    add(
        rows,
        58,
        "project_mirror",
        "Build Mentor-Hub-style DNA drafts from Project Mirror source candidates",
        "DONE_DRAFT_READY" if project_mirror["mentor_rows"] else "READY",
        f"mentor_rows={project_mirror['mentor_rows']}; output={PROJECT_MIRROR_MENTOR_DNA.relative_to(PROJECT_ROOT)}.",
        "py modules\\project_mirror_mentor_dna_draft.py",
        "Reference-derived source candidates are turned into original Mentor-Hub-compatible DNA drafts.",
        "low",
        "local",
    )
    add(
        rows,
        57,
        "project_mirror",
        "Build A/B MJ draft-grid queue comparing old logic against Project Mirror DNA",
        "READY" if project_mirror["ab_due"] else "DONE_AB_QUEUE_READY",
        (
            f"ab_rows={project_mirror['ab_rows']}; ab_ready={project_mirror['ab_ready']}; "
            f"ab_due={project_mirror['ab_due']}; draft grids only, no upscale."
        ),
        "py modules\\project_mirror_ab_mj_queue.py",
        "A/B queue exists for old-prompt vs Project-Mirror DNA comparison before promoting any new premium DNA into production.",
        "low",
        "local",
    )
    add(
        rows,
        56,
        "project_mirror",
        "Build standard Project Mirror MJ dispatch queue from A/B prompt rows",
        "READY" if project_mirror["dispatch_due"] else "DONE_DISPATCH_QUEUE_READY",
        (
            f"dispatch_rows={project_mirror['dispatch_rows']}; dispatch_due={project_mirror['dispatch_due']}; "
            "uses standard MJ dispatcher schema; draft grids only, no upscale."
        ),
        "py modules\\project_mirror_dispatch_queue.py",
        "Project Mirror A/B rows are converted to the standard MJ dispatch schema so continue-monthly can dispatch real draft-grid work.",
        "low",
        "local",
    )
    add(
        rows,
        55,
        "project_mirror",
        "Dispatch next Project Mirror A/B draft-grid pair through Midjourney",
        "READY" if project_mirror["dispatch_ready"] else "DONE_NO_READY_DISPATCH_ROWS",
        (
            f"ready={project_mirror['dispatch_ready']}; submitted={project_mirror['dispatch_submitted']}; "
            f"grid_found={project_mirror['grid_found']}; complete_pairs={project_mirror['complete_pairs']}; no upscale."
        ),
        "py modules\\shock_and_awe_mj_dispatcher.py --queue Database\\Project_Mirror_MJ_Dispatch_Queue.csv --limit 2",
        "One A/B pair is submitted as draft grids; upscale remains blocked until Rex selects a Top 1% image.",
        "medium",
        "Discord/MJ",
    )
    add(
        rows,
        54,
        "project_mirror",
        "Harvest Project Mirror submitted draft grids",
        "READY" if project_mirror["dispatch_submitted"] > project_mirror["grid_found"] else "DONE_HARVEST_CURRENT",
        (
            f"submitted={project_mirror['dispatch_submitted']}; grid_found={project_mirror['grid_found']}; "
            f"complete_pairs={project_mirror['complete_pairs']}."
        ),
        "py modules\\shock_and_awe_mj_harvester.py --queue Database\\Project_Mirror_MJ_Dispatch_Queue.csv --limit 4",
        "Submitted Project Mirror MJ grids have local grid files for A/B visual review.",
        "low",
        "Discord/MJ",
    )
    add(
        rows,
        53,
        "project_mirror",
        "Build Project Mirror A/B visual contact sheet for Rex/Gemini review",
        "READY" if project_mirror["contact_due"] else "DONE_CONTACT_CURRENT" if project_mirror["contact_exists"] else "WAIT_GRIDS",
        (
            f"grid_found={project_mirror['grid_found']}; complete_pairs={project_mirror['complete_pairs']}; "
            f"contact_due={project_mirror['contact_due']}; contact_exists={project_mirror['contact_exists']}."
        ),
        "py modules\\project_mirror_grid_review.py",
        "Latest Project Mirror draft grids are assembled into a contact sheet and review packet.",
        "low",
        "local",
    )
    add(
        rows,
        52,
        "project_mirror",
        "Score Project Mirror A/B draft grids and select visual winners",
        "READY" if project_mirror["score_due"] else "DONE_SCORECARD_CURRENT" if project_mirror["score_rows"] else "WAIT_COMPLETE_PAIRS",
        (
            f"complete_pairs={project_mirror['complete_pairs']}; score_rows={project_mirror['score_rows']}; "
            f"score_due={project_mirror['score_due']}."
        ),
        "py modules\\project_mirror_ab_scorecard.py",
        "A/B grid winners are scored into a durable scorecard before any production promotion.",
        "low",
        "local",
    )
    add(
        rows,
        51,
        "project_mirror",
        "Promote Project Mirror winners into production-grade DNA candidates",
        "READY" if project_mirror["promoted_due"] else "DONE_PROMOTED_CURRENT" if project_mirror["promoted_rows"] else "WAIT_SCORECARD",
        (
            f"score_rows={project_mirror['score_rows']}; promoted_rows={project_mirror['promoted_rows']}; "
            f"promoted_due={project_mirror['promoted_due']}."
        ),
        "py modules\\project_mirror_promote_winning_dna.py",
        "Winning Project Mirror A/B rows are converted into Mentor-Hub-compatible promoted DNA.",
        "low",
        "local",
    )
    add(
        rows,
        50,
        "project_mirror",
        "Map promoted Project Mirror DNA to Printify product carriers and price lanes",
        "READY" if project_mirror["matrix_due"] else "DONE_MATRIX_CURRENT" if project_mirror["matrix_rows"] else "WAIT_PROMOTED_DNA",
        (
            f"promoted_rows={project_mirror['promoted_rows']}; matrix_rows={project_mirror['matrix_rows']}; "
            f"matrix_due={project_mirror['matrix_due']}."
        ),
        "py modules\\project_mirror_product_matrix.py",
        "Promoted DNA has carrier, blueprint, target price, and no-publish production lane recommendations.",
        "low",
        "local",
    )
    add(
        rows,
        49,
        "project_mirror",
        "Build Project Mirror controlled production refinement queue",
        "READY" if project_mirror["refinement_due"] else "DONE_REFINEMENT_QUEUE_CURRENT" if project_mirror["refinement_rows"] else "WAIT_PRODUCT_MATRIX",
        (
            f"matrix_rows={project_mirror['matrix_rows']}; refinement_rows={project_mirror['refinement_rows']}; "
            f"refinement_due={project_mirror['refinement_due']}; no publish, no upscale."
        ),
        "py modules\\project_mirror_production_refinement_queue.py",
        "Best Project Mirror DNA is translated into controlled product-specific MJ refinement prompts for acrylic/poster candidates.",
        "low",
        "local",
    )
    add(
        rows,
        48,
        "project_mirror",
        "Convert Project Mirror refinement winners into MJ draft-grid dispatch rows",
        "READY" if project_mirror["refinement_mj_due"] else "DONE_REFINEMENT_MJ_QUEUE_CURRENT" if project_mirror["refinement_mj_rows"] else "WAIT_REFINEMENT_QUEUE",
        (
            f"refinement_rows={project_mirror['refinement_rows']}; "
            f"refinement_mj_rows={project_mirror['refinement_mj_rows']}; "
            f"ready={project_mirror['refinement_mj_ready']}; "
            f"submitted={project_mirror['refinement_mj_submitted']}; "
            f"grid_found={project_mirror['refinement_mj_grid_found']}; no upscale."
        ),
        "py modules\\project_mirror_refinement_mj_queue.py",
        "Production-refinement prompts are in standard MJ dispatcher format so the monthly loop can keep moving into draft-grid generation.",
        "low",
        "local",
    )
    add(
        rows,
        47,
        "project_mirror",
        "Dispatch next Project Mirror production-refinement draft grids",
        "READY" if project_mirror["refinement_mj_ready"] else "DONE_NO_READY_REFINEMENT_DISPATCH",
        (
            f"ready={project_mirror['refinement_mj_ready']}; "
            f"submitted={project_mirror['refinement_mj_submitted']}; "
            f"grid_found={project_mirror['refinement_mj_grid_found']}; draft-grid only."
        ),
        "py modules\\shock_and_awe_mj_dispatcher.py --queue Database\\Project_Mirror_Refinement_MJ_Dispatch_Queue.csv --limit 2",
        "Two production-refinement concepts are submitted as draft grids for later product-fit scoring; no upscale is used.",
        "medium",
        "Discord/MJ",
    )
    add(
        rows,
        46,
        "project_mirror",
        "Harvest Project Mirror production-refinement draft grids",
        "READY" if project_mirror["refinement_mj_submitted"] > project_mirror["refinement_mj_grid_found"] else "DONE_REFINEMENT_HARVEST_CURRENT",
        (
            f"submitted={project_mirror['refinement_mj_submitted']}; "
            f"grid_found={project_mirror['refinement_mj_grid_found']}."
        ),
        "py modules\\shock_and_awe_mj_harvester.py --queue Database\\Project_Mirror_Refinement_MJ_Dispatch_Queue.csv --limit 4",
        "Submitted refinement draft grids are downloaded for product-fit QA and Rex review.",
        "low",
        "Discord/MJ",
    )
    add(
        rows,
        45,
        "project_mirror",
        "Build Project Mirror production-refinement contact sheet",
        "READY" if project_mirror["refinement_contact_due"] else "DONE_REFINEMENT_REVIEW_CURRENT" if project_mirror["refinement_contact_exists"] else "WAIT_REFINEMENT_GRIDS",
        (
            f"grid_found={project_mirror['refinement_mj_grid_found']}; "
            f"contact_due={project_mirror['refinement_contact_due']}; "
            "Rex/Gemini need a visual sheet before any upscale or product creation."
        ),
        "py modules\\project_mirror_refinement_grid_review.py",
        "Project Mirror refinement grids are assembled into a product-fit contact sheet and review packet.",
        "low",
        "local",
    )

    if mode.get("mode") == "THE_FIRST_AUDIT_STUDIO_SERIES":
        manifest_count = csv_count(FIRST_AUDIT_MANIFEST)
        extension_count = csv_count(FIRST_AUDIT_EXTENSION)
        guard_due = is_missing_or_stale(FIRST_AUDIT_GUARD_AUDIT, FIRST_AUDIT_MANIFEST)
        extension_due = (
            is_missing_or_stale(FIRST_AUDIT_EXTENSION, SHOCK_V5_PRIVATE_DRAFTS)
            or is_missing_or_stale(FIRST_AUDIT_EXTENSION, SHOCK_V5_ZONES13_PRIVATE_DRAFTS)
        )
        add(
            rows,
            126,
            "first_audit",
            "Run First Audit leak guard before any public marketplace work",
            "READY" if guard_due else "DONE_GUARD_CURRENT",
            f"manifest_assets={manifest_count}; guard_due={guard_due}; public queue leak scan is mandatory for Studio/private separation.",
            "py modules\\first_audit_guard.py --allow-findings",
            "First Audit blocklist and guard report are current; any public queue leak is surfaced before marketplace work continues.",
            "low",
            "local",
        )
        add(
            rows,
            125,
            "first_audit",
            "Extend First Audit shortlist toward 12-15 stronger Studio candidates",
            "READY" if extension_due else "DONE_EXTENSION_PACKET_READY",
            (
                f"current_manifest={manifest_count}; extension_candidates={extension_count}; "
                f"extension_due={extension_due}; only optical acrylic/framed poster candidates auto-pass, cheap carriers are excluded. "
                "If fewer than 12 candidates qualify, the next step is visual review or fresh MJ production, not rerunning this packet."
            ),
            "py modules\\first_audit_candidate_expander.py",
            "A ranked extension packet exists for Rex/Gemini visual review, separating Studio-grade acrylic/framed candidates from cheap carriers.",
            "low",
            "local",
        )
        lookbook_due = is_missing_or_stale(FIRST_AUDIT_LOOKBOOK, FIRST_AUDIT_MANIFEST)
        add(
            rows,
            124,
            "first_audit",
            "Rebuild First Audit lookbook when manifest changes",
            "READY" if lookbook_due else "DONE_LOOKBOOK_CURRENT",
            f"lookbook_due={lookbook_due}; output={FIRST_AUDIT_LOOKBOOK.relative_to(PROJECT_ROOT)}.",
            "py modules\\first_audit_lookbook_builder.py",
            "The First Audit PDF/contact sheet/manifest reflect the latest protected Studio shortlist.",
            "medium",
            "local",
        )
        if first_audit_cyber["ready_concepts"]:
            add(
                rows,
                128,
                "first_audit",
                "Build Cyber-Renaissance MJ draft dispatch packet for First Audit expansion",
                "READY" if first_audit_cyber["queue_due"] else "DONE_MJ_PACKET_CURRENT",
                (
                    f"concepts={first_audit_cyber['concepts']}; ready_concepts={first_audit_cyber['ready_concepts']}; "
                    f"mj_rows={first_audit_cyber['mj_rows']}; mj_ready={first_audit_cyber['mj_ready']}; "
                    "draft grids only; upscale is blocked until Rex approves Top 1%."
                ),
                "py modules\\first_audit_cyber_mj_queue.py",
                "Cyber-Renaissance concepts are converted to standard MJ dispatch rows with no-upscale guard and review packet.",
                "low",
                "local",
            )
            add(
                rows,
                127,
                "first_audit",
                "Dispatch one First Audit Cyber-Renaissance draft grid to Midjourney",
                (
                    "READY"
                    if first_audit_cyber["mj_ready"]
                    else "DONE_ALL_DISPATCHED"
                    if first_audit_cyber["mj_rows"]
                    and first_audit_cyber["mj_submitted"] == first_audit_cyber["mj_rows"]
                    and not first_audit_cyber["mj_unconfirmed"]
                    and not first_audit_cyber["mj_failed"]
                    else "WAITING_MJ_PACKET_OR_HARVEST"
                ),
                (
                    f"mj_ready={first_audit_cyber['mj_ready']}; submitted={first_audit_cyber['mj_submitted']}; "
                    f"unconfirmed={first_audit_cyber['mj_unconfirmed']}; failed={first_audit_cyber['mj_failed']}. "
                    "Submit one grid only; no upscale."
                ),
                "py modules\\shock_and_awe_mj_dispatcher.py --queue Database\\First_Audit_Cyber_Renaissance_MJ_Dispatch_Queue.csv --limit 1",
                "One Cyber-Renaissance draft grid is submitted for Rex review without consuming upscale minutes.",
                "medium",
                "Discord/Midjourney",
            )
            add(
                rows,
                126,
                "first_audit",
                "Harvest First Audit Cyber-Renaissance draft grids without upscale",
                "READY" if first_audit_cyber["mj_submitted"] > first_audit_cyber["grid_ready"] else "DONE_DRAFT_GRIDS_CURRENT",
                (
                    f"submitted={first_audit_cyber['mj_submitted']}; draft_grids={first_audit_cyber['grid_ready']}; "
                    f"unconfirmed={first_audit_cyber['mj_unconfirmed']}. "
                    "Grid-only harvest; no MJ upscale unless Rex later selects Top 1%."
                ),
                "py modules\\shock_and_awe_mj_harvester.py --queue Database\\First_Audit_Cyber_Renaissance_MJ_Dispatch_Queue.csv --limit 6",
                "Draft grids are downloaded for Rex/Gemini preselection; U1-U4/upscale remains blocked by policy.",
                "medium",
                "Discord/Midjourney",
            )
            add(
                rows,
                125,
                "first_audit",
                "Build Rex review contact sheet for First Audit Cyber-Renaissance grids",
                "READY" if first_audit_cyber["review_due"] else "DONE_GRID_REVIEW_PACKET_CURRENT",
                (
                    f"draft_grids={first_audit_cyber['grid_ready']}; "
                    f"review_due={first_audit_cyber['review_due']}; "
                    f"contact_sheet={FIRST_AUDIT_CYBER_CONTACT_SHEET.relative_to(PROJECT_ROOT)}."
                ),
                "py modules\\first_audit_cyber_grid_review.py",
                "A concrete contact sheet and markdown packet lets Rex inspect Cyber-Renaissance grids without opening raw folders.",
                "low",
                "local",
            )
            add(
                rows,
                124,
                "first_audit",
                "Build technical preselection worksheet for First Audit Cyber-Renaissance grids",
                "READY" if first_audit_cyber["preselect_due"] else "DONE_PRESELECT_PACKET_CURRENT",
                (
                    f"draft_grids={first_audit_cyber['grid_ready']}; "
                    f"preselect_due={first_audit_cyber['preselect_due']}; "
                    f"preselect_sheet={FIRST_AUDIT_CYBER_PRESELECT_SHEET.relative_to(PROJECT_ROOT)}."
                ),
                "py modules\\first_audit_cyber_grid_preselector.py",
                "The 2x2 draft grids are sliced into technical candidates so Rex can review a shorter top-candidate sheet before authorizing any upscale.",
                "low",
                "local",
            )

    if mode.get("mode") == "SHOCK_AND_AWE_PRIVATE_SHOWCASE":
        version = clean(mode.get("version"))
        is_v5 = version.startswith("V5") or version.startswith("FINAL_MVP")
        if is_v5:
            shock_count = csv_count(SHOCK_V5_QUEUE)
            private_queue = count_by(SHOCK_V5_QUEUE, "Status")
            status = "DONE_ZONE2_CONCEPTS_WAITING_MJ" if shock_count >= 10 and SHOCK_V5_SPEC.exists() else "READY"
            command = "py modules\\shock_and_awe_v5_builder.py"
            done_when = "Zone 2 has 10 concept rows with SKU, private copy, MJ prompt, verified Printify anchor, payload JSON, and no eBay/Etsy sync."
            task = "Build Operation Shock and Awe V5 private showcase concepts and production queue"
            blocker = (
                f"V5 active; Zone 2 rows={shock_count}; waiting for MJ/QA="
                f"{private_queue.get('CONCEPT_READY_WAITING_MJ', 0)}. "
                "Public eBay/Etsy SEO tasks are suspended for this packet."
            )
        else:
            shock_count = csv_count(SHOCK_ROSTER)
            private_queue = count_by(SHOCK_QUEUE, "Status")
            status = "READY_FOR_VISUAL_PRODUCTION" if shock_count >= 20 and SHOCK_SPEC.exists() else "READY"
            command = "py modules\\shock_and_awe_showcase_builder.py"
            done_when = "20 Studio Spec Sheets and 20 Printify private draft payload rows exist with SKU, private title/description, MJ prompt, Printify vector, landed cost, and premium retail."
            task = "Build 20 high-net-worth private-client showcase spec sheets and production queue"
            blocker = (
                f"Operation Shock and Awe active; showcase rows={shock_count}; Printify private queue waiting for MJ/QA="
                f"{private_queue.get('WAITING_FOR_MJ_IMAGE_QA', 0)}. Public eBay/Etsy SEO tasks are suspended."
            )
        add(
            rows,
            120,
            "private_showcase",
            task,
            status,
            blocker,
            command,
            done_when,
            "low",
            "local/API catalog only",
        )
        if is_v5:
            rnd_count = csv_count(SHOCK_BLUEPRINT_RND)
            mj_ready = count_by(SHOCK_V5_MJ_QUEUE, "Dispatch_Status")
            zones13_ready = count_by(SHOCK_V5_ZONES13_MJ_QUEUE, "Dispatch_Status")
            add(
                rows,
                121,
                "private_showcase",
                "Expand verified Printify product formats for private showcase pipeline",
                "DONE_BLUEPRINT_RND" if rnd_count and SHOCK_V5_RND.exists() else "READY",
                f"Blueprint R&D candidates={rnd_count}; report_exists={SHOCK_V5_RND.exists()}. Use official catalog truth, not stale user/Grey numeric codes.",
                "py modules\\shock_and_awe_blueprint_rnd.py",
                "R&D report identifies verified Tower/Base/Experimental formats and flags invalid or misleading target IDs.",
                "low",
                "Printify catalog API",
            )
            add(
                rows,
                122,
                "private_showcase",
                "Prepare partner-demo Midjourney dispatch queue and sales index",
                (
                    "DONE_MJ_QUEUE_WAITING_VISUAL_GENERATION"
                    if (mj_ready.get("READY_FOR_MJ", 0) >= 10 or mj_ready.get("MJ_SUBMITTED", 0) >= 10)
                    and SHOCK_V5_DEMO_INDEX.exists()
                    else "READY"
                ),
                f"V5 MJ-ready rows={mj_ready.get('READY_FOR_MJ', 0)}; partner demo index exists={SHOCK_V5_DEMO_INDEX.exists()}.",
                "py modules\\shock_and_awe_mj_queue.py",
                "10 Zone 2 rows are ready for MJ visual generation, with partner-facing story/sales index prepared.",
                "low",
                "local",
            )
            submitted = mj_ready.get("MJ_SUBMITTED", 0)
            failed = mj_ready.get("MJ_DISPATCH_FAILED", 0)
            quality_hold = mj_ready.get("HOLD_PROMPT_QUALITY_REVIEW", 0)
            zones13_rows = read_csv(SHOCK_V5_ZONES13_MJ_QUEUE)
            zones13_submitted = sum(1 for row in zones13_rows if clean(row.get("Dispatch_Status")) == "MJ_SUBMITTED")
            zones13_harvest = count_by(SHOCK_V5_ZONES13_MJ_QUEUE, "Harvest_Status")
            zones13_terminal = {"READY_FOR_VISUAL_QA", "VISUAL_QA_PASSED", "GRID_TIMEOUT_HOLD", "HARVEST_HOLD", "HARVEST_ERROR_HOLD"}
            zones13_active_harvest = [
                row
                for row in zones13_rows
                if clean(row.get("Dispatch_Status")) == "MJ_SUBMITTED"
                and clean(row.get("Harvest_Status")) not in zones13_terminal
            ]
            zones13_ready_for_qa = (
                zones13_harvest.get("READY_FOR_VISUAL_QA", 0)
                + zones13_harvest.get("VISUAL_QA_PASSED", 0)
            )
            zones13_held = sum(zones13_harvest.get(status, 0) for status in {"GRID_TIMEOUT_HOLD", "HARVEST_HOLD", "HARVEST_ERROR_HOLD"})
            zones13_selection = read_csv(SHOCK_V5_ZONES13_SELECTION)
            zones13_selected = sum(1 for row in zones13_selection if clean(row.get("Final_Status")).startswith("SELECTED"))
            zones13_production_ready = csv_count(SHOCK_V5_ZONES13_PRODUCTION)
            zones13_private_drafts = count_by(SHOCK_V5_ZONES13_PRIVATE_DRAFTS, "Draft_Status")
            zones13_draft_count = zones13_private_drafts.get("PRINTIFY_DRAFT_CREATED", 0)
            recovery_rows = read_csv(SHOCK_V5_RECOVERY_QUEUE)
            recovery_actions = count_by(SHOCK_V5_RECOVERY_QUEUE, "Recovery_Action")
            ui_submit_rows = read_csv(SHOCK_V5_UI_SUBMIT_PACKET)
            if recovery_rows and ui_submit_rows:
                recovery_status = "WAITING_VERIFIED_MJ_UI_SUBMIT"
            elif recovery_rows:
                recovery_status = "READY_BUILD_UI_SUBMIT_PACKET"
            else:
                recovery_status = "READY_BUILD_RECOVERY_QUEUE"
            add(
                rows,
                130,
                "private_showcase",
                "Build and execute Shock & Awe 6-gap recovery queue",
                recovery_status,
                (
                    f"recovery_rows={len(recovery_rows)}; actions={dict(recovery_actions)}; "
                    f"report_exists={SHOCK_V5_RECOVERY_REPORT.exists()}; "
                    f"ui_packet_rows={len(ui_submit_rows)}; ui_packet_exists={SHOCK_V5_UI_SUBMIT_REPORT.exists()}; "
                    f"held={zones13_held}."
                ),
                "py modules\\shock_and_awe_recovery_queue.py && py modules\\shock_and_awe_ui_submit_packet.py",
                "All remaining private showcase gaps have explicit recovery actions and a one-line UI submission packet that avoids the raw Discord false-positive path.",
                "medium",
                "local then verified Midjourney UI",
            )
            add(
                rows,
                129,
                "private_showcase",
                "Dispatch one Shock & Awe Zones 1/3 private-demo prompt to Midjourney",
                "READY" if zones13_ready.get("READY_FOR_MJ", 0) else "DONE_WAITING_HARVEST",
                (
                    f"zones1_3_READY_FOR_MJ={zones13_ready.get('READY_FOR_MJ', 0)}; "
                    f"submitted={zones13_ready.get('MJ_SUBMITTED', 0)}; failed={zones13_ready.get('MJ_DISPATCH_FAILED', 0)}."
                ),
                "py modules\\shock_and_awe_mj_dispatcher.py --queue Database\\Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv --limit 1",
                "One remaining private showcase concept is submitted for visual generation without public marketplace spend.",
                "medium",
                "Discord/Midjourney",
            )
            add(
                rows,
                128,
                "private_showcase",
                "Harvest Shock & Awe Zones 1/3 Midjourney outputs",
                "READY" if zones13_active_harvest else ("DONE_PRODUCTION_READY" if zones13_production_ready >= zones13_selected and zones13_selected else "DONE_WAITING_VISUAL_QA"),
                (
                    f"submitted={zones13_submitted}; active_harvest={len(zones13_active_harvest)}; "
                    f"ready_for_visual_qa={zones13_ready_for_qa}; held={zones13_held}; "
                    f"selected={zones13_selected}; production_ready={zones13_production_ready}; "
                    f"private_drafts={zones13_draft_count}; harvest_status={dict(zones13_harvest)}."
                ),
                "py modules\\shock_and_awe_mj_harvester.py --queue Database\\Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv --limit 10",
                "Zones 1/3 grids and U1-U4 assets are harvested or explicitly held so the 30-unit private demo does not disappear from the active loop.",
                "medium",
                "Discord/Midjourney",
            )
            add(
                rows,
                127,
                "private_showcase",
                "Create Printify private drafts for Shock & Awe Zones 1/3 selected finalists",
                "DONE_WAITING_RECOVERY_GAPS" if zones13_selected and zones13_draft_count >= zones13_selected else ("READY" if zones13_production_ready else "WAITING_PRODUCTION_SELECTION"),
                (
                    f"selected={zones13_selected}; production_ready={zones13_production_ready}; "
                    f"private_drafts_created={zones13_draft_count}; status_packet_exists={SHOCK_V5_PRIVATE_STATUS.exists()}."
                ),
                (
                    "py modules\\shock_and_awe_zones1_3_production_selector.py && "
                    "py modules\\shock_and_awe_printify_private_drafts.py "
                    "--production-csv Database\\Shock_And_Awe_V5_Zones1_3_Printify_Production_Files.csv "
                    "--private-queue-csv Database\\Shock_And_Awe_V5_Zones1_3_Printify_Private_Queue.csv "
                    "--output-csv Database\\Shock_And_Awe_V5_Zones1_3_Printify_Private_Drafts.csv --limit 2 && "
                    "py modules\\shock_and_awe_private_status_report.py"
                ),
                "All QA-selected Zones 1/3 finals have production files, private Printify drafts, and the 30-unit status packet is refreshed.",
                "medium",
                "Printify API",
            )
            add(
                rows,
                123,
                "private_showcase",
                "Dispatch one Shock & Awe private showcase prompt to Midjourney",
                "READY" if mj_ready.get("READY_FOR_MJ", 0) else "DONE_WAITING_HARVEST",
                f"READY_FOR_MJ={mj_ready.get('READY_FOR_MJ', 0)}; quality_hold={quality_hold}; submitted={submitted}; failed={failed}.",
                "py modules\\shock_and_awe_mj_dispatcher.py --limit 1",
                "At least one private showcase visual prompt is submitted to Midjourney for later review/harvest.",
                "medium",
                "Discord/Midjourney",
            )
            harvest_status = count_by(SHOCK_V5_MJ_QUEUE, "Harvest_Status")
            harvest_ready = harvest_status.get("READY_FOR_VISUAL_QA", 0) + harvest_status.get("VISUAL_QA_PASSED", 0)
            add(
                rows,
                125,
                "private_showcase",
                "Harvest Shock & Awe Midjourney outputs and prepare visual QA",
                "READY" if submitted and harvest_ready < submitted else "DONE_READY_FOR_VISUAL_QA",
                f"submitted={submitted}; ready_for_visual_qa={harvest_ready}; waiting_or_partial={submitted - harvest_ready}.",
                "py modules\\shock_and_awe_mj_harvester.py --limit 10",
                "Submitted Zone 2 images are downloaded per SKU, upscales are requested once, and complete U1-U4 sets are ready for visual QA.",
                "medium",
                "Discord/Midjourney",
            )
            private_drafts = count_by(SHOCK_V5_PRIVATE_DRAFTS, "Draft_Status")
            draft_count = private_drafts.get("PRINTIFY_DRAFT_CREATED", 0)
            add(
                rows,
                126,
                "private_showcase",
                "Create Printify private drafts for Shock & Awe Zone 2 finalists",
                "DONE_WAITING_REX_VISUAL_REVIEW" if draft_count >= 10 and SHOCK_V5_FINAL_PACKET.exists() else "READY",
                f"private_drafts_created={draft_count}; final_packet_exists={SHOCK_V5_FINAL_PACKET.exists()}.",
                "py modules\\shock_and_awe_printify_private_drafts.py --limit 1",
                "10 Zone 2 finalists exist as Printify private drafts with production files, product IDs, and review packet.",
                "medium",
                "Printify API",
            )
            add(
                rows,
                124,
                "private_showcase",
                "Review and upgrade held Shock & Awe prompts before more MJ dispatch",
                "READY" if quality_hold else "DONE",
                f"{quality_hold} prompts are held for Rex top-tier demo quality review.",
                "py modules\\shock_and_awe_prompt_quality_review.py --limit 8",
                "Held prompts receive rubric scores and upgrade notes before any further MJ dispatch.",
                "low",
                "local/Gemini optional",
            )

    if not etsy_pod["ready"] and etsy_pod_candidates["unhandled_plan"]:
        add(
            rows,
            125,
            "etsy_pod",
            "Select next high-quality Poster/Acrylic Etsy POD candidates from launch plan",
            "READY" if etsy_pod_candidates["candidates_stale"] or etsy_pod_candidates["candidates"] == 0 else "DONE_CANDIDATES_READY",
            (
                f"ready_full={etsy_pod['ready']}; unhandled_plan={etsy_pod_candidates['unhandled_plan']}; "
                f"current_candidates={etsy_pod_candidates['candidates']}; stale={etsy_pod_candidates['candidates_stale']}. "
                "Sticker expansion is frozen; choose Poster/Acrylic only."
            ),
            "py modules\\etsy_pod_candidate_selector.py --limit 10",
            "The next Etsy POD candidate CSV is refreshed with QA-worthy Poster/Acrylic rows before preflight or paid launch.",
            "low",
            "local",
        )

    if etsy_photo_repair["remaining"] or etsy_photo_repair["missing_preview_count"]:
        if etsy_photo_repair["missing_preview_count"]:
            add(
                rows,
                117,
                "etsy_archive_quality",
                "Generate missing Etsy digital preview image sets for active listings",
                "READY",
                (
                    f"live_with_listing_id={etsy_photo_repair['live_with_listing_id']}; "
                    f"locally_packable={etsy_photo_repair['locally_packable']}; "
                    f"preview_assets={etsy_photo_repair['preview_assets']}; "
                    f"missing_preview_sets={etsy_photo_repair['missing_preview_count']}. "
                    "This is local asset generation and does not spend listing fees."
                ),
                "py modules\\etsy_digital_preview_builder.py --limit 120",
                "All active Etsy digital rows have five local preview images ready for safe API upload.",
                "low",
                "local",
            )
        if etsy_photo_repair["remaining"]:
            add(
                rows,
                116,
                "etsy_archive_quality",
                "Append richer preview photos to existing Etsy digital listings",
                "READY" if etsy_can_write else "WAIT_RISK",
                (
                    f"remaining_preview_richness_repairs={etsy_photo_repair['remaining']}; "
                    f"repaired_or_rich={etsy_photo_repair['repaired_or_rich']}; "
                    "edits existing listings only, no new listing fee. "
                    + ("" if etsy_can_write else etsy_blocker)
                ),
                "py modules\\etsy_digital_photo_gap_repair_uploader.py --limit 25 --execute",
                "Existing digital listings reach at least five preview images through Etsy API without creating new listings or fees.",
                "medium",
                "Etsy API",
            )
    if etsy_pod["ready"]:
        add(
            rows,
            124,
            "etsy_pod",
            "Launch one high-quality Printify-backed Etsy POD listing through official API",
            "READY" if etsy_can_paid_publish else "WAIT_RISK",
            (
                f"ready={etsy_pod['ready']} by_type={etsy_pod['ready_by_type']}; "
                f"handled={etsy_pod['handled']}; latest_log_status={etsy_pod['latest_status']}. "
                "Runner enforces fee cap, official mockup count, duplicate-image hold, and external-id reconciliation. "
                + ("" if etsy_can_paid_publish else etsy_blocker)
            ),
            "py modules\\printify_etsy_launch.py --plan-csv Database\\Etsy_POD_Printify_Launch_Ready_Full.csv --limit 1 --publish",
            "One Poster/Acrylic Etsy POD listing is published or safely held by mockup/duplicate guard, with launch log and fee ledger updated.",
            "medium",
            "Printify/Etsy API",
        )
    if etsy_pod["pending_external"]:
        add(
            rows,
            124,
            "etsy_pod",
            "Poll Printify Etsy external ids for newly published POD listings",
            "READY",
            f"pending_external={etsy_pod['pending_external']}; this is no-spend/no-republish reconciliation.",
            "py modules\\etsy_printify_external_poll.py --max-age-minutes 30 --limit 10",
            "All newly published POD rows have Etsy external ids backfilled or are held for delayed reconcile without duplicate publish.",
            "low",
            "Printify API",
        )

    gemini_state = read_json(GEMINI_SUPERVISOR_STATE)
    free_age = minutes_since_iso(clean(gemini_state.get("last_free_checkin_at")) or None)
    paid_age = minutes_since_iso(clean(gemini_state.get("last_paid_checkin_at")) or None)
    health_age = minutes_since_iso(clean(gemini_state.get("last_free_health_at")) or None)
    free_gemini_due = free_age >= 180 or health_age >= 360
    paid_gemini_due = paid_age >= 720 and is_winddown_window()
    paid_waiting_winddown = paid_age >= 720 and not is_winddown_window()
    gemini_due = free_gemini_due or paid_gemini_due
    add(
        rows,
        45 if gemini_due else 25 if paid_waiting_winddown else 35,
        "grey_advisor",
        "Run independent Gemini/Grey supervisor check-in when due",
        "READY" if gemini_due else "WAIT_UNTIL_0530_PAID_REVIEW" if paid_waiting_winddown else "DONE_NOT_DUE",
        (
            f"free_checkin_age={free_age}m; paid_checkin_age={paid_age}m; "
            f"health_age={health_age}m; free_due={free_gemini_due}; "
            f"paid_winddown_due={paid_gemini_due}. This is a separate advisor cadence, not the 10-minute task-continuation heartbeat. "
            "Routine check-ins use free tier; paid tier is reserved for winddown/high-risk decisions."
        ),
        "py modules\\gemini_supervisor_checkin.py",
        "Gemini free/paid advisor state is refreshed; any Grey recommendations are parsed into local review tasks, not executed directly.",
        "low",
        "Gemini API",
    )

    chat_state = read_json(GEMINI_CHAT_SYNC_STATE)
    chat_age = minutes_since_iso(clean(chat_state.get("timestamp")) or None)
    add(
        rows,
        54,
        "grey_web_sync",
        "05:30 ET low-frequency sync to Gemini thread `Codex 自动化矩阵升级计划`",
        "READY_WINDDOWN_WEB_SYNC" if is_winddown_window() and chat_age >= 720 else "WAIT_UNTIL_0530_ET",
        (
            f"target_thread=https://gemini.google.com/u/1/app/d2ab3afa2778aa9e; "
            f"last_web_sync_age={chat_age}m; Edge only; idle check required."
        ),
        "py modules\\gemini_chat_sync.py --execute --wait-until-idle-minutes 60",
        "Daily sitrep is pasted into the correct Gemini thread only during winddown/major-breakthrough windows, with idle/focus safeguards.",
        "medium",
        "Edge/Gemini web",
    )

    supervisor_age = supervisor_state_age_minutes()
    supervisor_due = supervisor_age >= SUPERVISOR_COOLDOWN_MINUTES
    add(
        rows,
        35 if supervisor_due else 20,
        "control",
        "Run local supervisor maintenance cycle",
        "READY" if supervisor_due else "WAIT_COOLDOWN",
        (
            f"last_supervisor_age={supervisor_age}m; "
            f"cooldown={SUPERVISOR_COOLDOWN_MINUTES}m. "
            "This is maintenance only; production tasks outrank it during normal monthly work."
        ),
        "py modules\\factory_supervisor.py --execute-local --skip-network",
        "Factory_Autopilot_State, action queue, QA, traffic diagnosis, morning report, and Gemini queue refresh with 0 failures.",
    )

    if repair_methods.get("SOURCE_REPAIR_REQUIRED", 0):
        ui_status = clean(printify_ui.get("status")) or "UNKNOWN"
        add(
            rows,
            98,
            "cover_gate",
            "Repair one live eBay cover mismatch from Printify source and audit buyer page",
            "READY" if ui_status == "LOGGED_IN" else "BLOCKED",
            f"Printify CDP status: {ui_status}; {clean(printify_ui.get('reason'))}",
            "py modules\\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120",
            "One SKU becomes LIVE_COVER_FIXED, or the runner records that replacement-listing fallback is required.",
            "medium",
            "single online item",
        )

    image_insufficiency = market_actions.get("FIX_PRINTIFY_IMAGE_INSUFFICIENCY_BEFORE_PUBLISH", 0)
    gallery_duplicates = market_actions.get("FIX_PRINTIFY_DUPLICATE_GALLERY_BEFORE_MORE_SYNC", 0)
    if gallery_duplicates:
        add(
            rows,
            94,
            "gallery_integrity",
            "Repair repeated/risky Printify gallery images before more public publish",
            "BLOCKING_PUBLISH",
            f"{gallery_duplicates} products have exact duplicate selected images or custom gallery repeat risk.",
            "py modules\\printify_gallery_duplicate_audit.py --sleep-seconds 0.1",
            "All live/staged products in duplicate audit are OK, or risky rows are queued for source repair/replacement.",
            "medium",
            "Printify API",
        )

    if gallery_replacement_pending:
        add(
            rows,
            93,
            "gallery_replacement",
            "Prepare clean replacement path for non-sticker custom-gallery risk",
            "READY_FOR_SAMPLE",
            (
                f"{len(gallery_replacement_pending)} Poster/Acrylic rows still need a local GalleryFix draft; "
                f"queue_status={dict(gallery_replacement_status)}."
            ),
            "py modules\\ebay_replacement_draft_builder.py --queue gallery --limit 1",
            "One GalleryFix sample is created, Printify source audit passes with official mockups, eBay live-gallery audit passes, then batch replacement can proceed.",
            "medium",
            "local first, then single online item",
        )
    elif gallery_replacement_status.get("READY_FOR_LOCAL_DRAFT_WHEN_APPROVED", 0):
        add(
            rows,
            38,
            "gallery_replacement",
            "Gallery replacement local draft already prepared; wait for downstream QA",
            "DONE_WAITING_PRINTIFY_QA",
            (
                f"queue_status={dict(gallery_replacement_status)}; matching GalleryFix draft already exists in "
                f"{REPLACEMENT_DRAFT_LOG.name}. Do not rerun queue preparation as monthly work."
            ),
            "",
            "Prepared GalleryFix draft enters normal Printify source QA/publish sequencing; the backlog should not repeatedly rebuild the same queue.",
            "low",
            "none",
        )

    if image_insufficiency:
        add(
            rows,
            92,
            "image_integrity",
            "Clear Printify selected/default insufficiency before publish resumes",
            "BLOCKED_BY_COVER_GATE",
            f"{image_insufficiency} products have too few selected images or no default image.",
            "py modules\\printify_image_default_audit.py --sleep-seconds 1",
            "Products that stay insufficient are either repaired or held; multiple official/default mockups are allowed.",
            "medium",
            "Printify API",
        )

    if replacement_status.get("READY_TO_REPLACE_VERIFIED", 0):
        add(
            rows,
            94,
            "replacement",
            "Create verified replacement listing for source-repaired live cover failure",
            "READY_TO_REPLACE_VERIFIED",
            f"{replacement_status['READY_TO_REPLACE_VERIFIED']} row already failed source repair plus live eBay audit.",
            "py modules\\ebay_replacement_draft_builder.py --limit 1",
            "Replacement row is created as Ready_for_Printify; public publish still waits for QA and retire sequencing.",
            "high",
            "single replacement listing",
        )

    if replacement_status.get("WAIT_SOURCE_REPAIR_RESULT", 0):
        add(
            rows,
            88,
            "fallback",
            "Prepare replacement-listing path if source re-sync cannot repair Inventory-managed eBay images",
            "WAIT_SOURCE_REPAIR_RESULT",
            f"{replacement_status['WAIT_SOURCE_REPAIR_RESULT']} rows waiting for one source repair result.",
            "py modules\\ebay_cover_replacement_queue.py",
            "Replacement queue separates safe replace candidates from non-sticker manual review rows.",
            "medium",
            "local",
        )

    if market_actions.get("UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH", 0):
        add(
            rows,
            72,
            "production",
            "Resume Ready_for_Printify uploads in audited single-item batches",
            "READY_AFTER_IMAGE_QA",
            f"{market_actions['UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH']} local rows are ready; Cover Gate is cleared, so proceed only through single-item upload plus production-design/default-image audit.",
            "py modules\\printify_full_pipeline.py --limit 1",
            "A new single item reaches stable mockup state and passes selected-count/default-count audit.",
            "high",
            "Printify UI/API",
        )

    if market_actions_non_sticker.get("PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK", 0):
        add(
            rows,
            68,
            "publish",
            "Publish small cooled batch after default-image and live-cover spot audit",
            "READY_AFTER_IMAGE_QA" if ebay_can_paid_publish else "WAIT_EBAY_PUBLISH_GUARD",
            (
                f"{market_actions_non_sticker['PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK']} non-Sticker stable drafts are candidates. "
                "Cover Gate is cleared; continue with cooled scheduler and post-publish live-cover spot checks. "
                + ("" if ebay_can_paid_publish else ebay_blocker)
            ),
            "py modules\\printify_publish_scheduler.py --limit 2 --cycle Poster,Acrylic --min-delay 240 --max-delay 720",
            "Published Poster/Acrylic products are live-audited and added to guarded Standard/General ad coverage without PPC; no new Sticker inventory is published.",
            "high",
            "Printify API/eBay sync",
        )

    ebay_diag_age = file_age_minutes(TRAFFIC_DIAGNOSIS)
    if diagnosis_count:
        add(
            rows,
            62,
            "market_learning",
            "Keep eBay traffic diagnosis current and avoid ad-only conclusions",
            "DONE_RECENT_DIAGNOSIS" if is_recent(TRAFFIC_DIAGNOSIS, 180) else "READY",
            f"{diagnosis_count} current traffic hypotheses generated; age={ebay_diag_age if ebay_diag_age is not None else 'missing'}m.",
            "py modules\\ebay_traffic_diagnosis.py",
            "Traffic report identifies exposure/click/conversion blockers from snapshots and cover queues.",
        )

    if etsy_darwinian_count:
        v7_mj_rows = read_csv(ETSY_DARWINIAN_MJ_QUEUE)
        v7_ready = etsy_darwinian_mj.get("READY_FOR_MJ", 0)
        v7_submitted = sum(1 for row in v7_mj_rows if clean(row.get("Dispatch_Status")) == "MJ_SUBMITTED")
        v7_harvest_ready = (
            etsy_darwinian_harvest.get("READY_FOR_VISUAL_QA", 0)
            + etsy_darwinian_harvest.get("VISUAL_QA_PASSED", 0)
        )
        v7_harvest_terminal = {
            "READY_FOR_VISUAL_QA",
            "VISUAL_QA_PASSED",
            "GRID_TIMEOUT_HOLD",
            "HARVEST_HOLD",
            "HARVEST_ERROR_HOLD",
        }
        v7_active_harvest = [
            row
            for row in v7_mj_rows
            if clean(row.get("Dispatch_Status")) == "MJ_SUBMITTED"
            and clean(row.get("Harvest_Status")) not in v7_harvest_terminal
        ]
        v7_harvest_hold_count = sum(
            1
            for row in v7_mj_rows
            if clean(row.get("Harvest_Status")) in {"GRID_TIMEOUT_HOLD", "HARVEST_HOLD", "HARVEST_ERROR_HOLD"}
        )
        v7_visual_qa = count_by(ETSY_DARWINIAN_MJ_QUEUE, "Visual_QA_Status")
        v7_packet_rows = read_csv(ETSY_DARWINIAN_PACKET)
        v7_packet = count_by(ETSY_DARWINIAN_PACKET, "Launch_Readiness")
        v7_upload = count_by(ETSY_DARWINIAN_UPLOAD, "Package_Status")
        v7_gray_ids = {
            clean(row.get("ID"))
            for row in read_csv(ETSY_GRAY_QUEUE)
            if clean(row.get("ID")).startswith("OC-ETSY-")
        }
        v7_packageable_remaining = sum(
            1
            for row in v7_packet_rows
            if clean(row.get("Launch_Readiness")) in {"READY_FOR_METADATA_QA", "READY_AFTER_UPSCALE_REVIEW"}
            and clean(row.get("Internal_SKU")) not in v7_gray_ids
        )
        v7_queued = etsy_darwinian_assets.get("QUEUED_FOR_MJ", 0)
        v7_staged_remaining = etsy_darwinian_assets.get("STAGED_CONCEPT_ONLY", 0)
        v7_pending_visual_qa = sum(
            1
            for row in v7_mj_rows
            if clean(row.get("Harvest_Status")) in {"READY_FOR_VISUAL_QA", "VISUAL_QA_PASSED"}
            and clean(row.get("Visual_QA_Status")) in {"", "PENDING_IMAGE_GENERATION"}
        )
        v7_qa_completed = max(0, v7_harvest_ready - v7_pending_visual_qa)
        add(
            rows,
            118,
            "etsy_darwinian_lab",
            "Build/extend V7 Etsy Darwinian Lab production queue from six public-market test pools",
            (
                "READY_BUILD_NEXT_MJ_QUEUE"
                if v7_staged_remaining and not v7_ready
                else ("DONE_MJ_QUEUE_BUILT" if v7_queued >= 6 else "READY_BUILD_MJ_QUEUE")
            ),
            (
                f"concepts={etsy_darwinian_count}; queued_for_mj={v7_queued}; "
                f"staged_remaining={v7_staged_remaining}; mj_ready={v7_ready}; submitted={v7_submitted}; "
                f"plan_exists={ETSY_DARWINIAN_PLAN.exists()}."
            ),
            "py modules\\etsy_darwinian_lab_mj_queue.py --per-pool 1",
            "The next one-per-pool Etsy test wave is queued for image generation with no Etsy listing fee spent.",
            "low",
            "local",
        )
        add(
            rows,
            119,
            "etsy_darwinian_lab",
            "Dispatch first V7 Etsy cross-pool visual samples to Midjourney",
            "READY" if v7_ready else ("WAITING_FOR_HARVEST" if v7_submitted else "WAITING_FOR_MJ_QUEUE"),
            f"READY_FOR_MJ={v7_ready}; submitted={v7_submitted}; no Etsy fee until QA and fee guard pass.",
            "py modules\\shock_and_awe_mj_dispatcher.py --queue Database\\Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv --limit 6",
            "One representative concept from each V7 Etsy pool is submitted for visual generation and can later be harvested/QAed.",
            "medium",
            "Discord/Midjourney",
        )
        add(
            rows,
            120,
            "etsy_darwinian_lab",
            "Harvest V7 Etsy cross-pool Midjourney outputs and prepare image QA",
            "READY" if v7_active_harvest else "WAITING_FOR_SUBMITTED_MJ",
            (
                f"submitted={v7_submitted}; active_harvest={len(v7_active_harvest)}; "
                f"ready_for_visual_qa={v7_harvest_ready}; held={v7_harvest_hold_count}; "
                f"harvest_status={dict(etsy_darwinian_harvest)}."
            ),
            "py modules\\shock_and_awe_mj_harvester.py --queue Database\\Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv --limit 6",
            "The first six Etsy experiment samples have grid/U assets downloaded and are ready for quality gate review before any paid Etsy listing action.",
            "medium",
            "Discord/Midjourney",
        )
        add(
            rows,
            121,
            "etsy_darwinian_lab",
            "Run local visual QA for V7 Etsy cross-pool samples",
            "READY" if v7_pending_visual_qa else "DONE_WAITING_LISTING_PACKET",
            (
                f"ready_for_visual_qa={v7_harvest_ready}; pending_visual_qa={v7_pending_visual_qa}; "
                f"qa_completed={v7_qa_completed}; visual_qa={dict(v7_visual_qa)}."
            ),
            "py modules\\etsy_darwinian_lab_visual_qa.py --limit 6",
            "All harvested V7 samples receive local image metrics, pool-specific flags, best U image choices, and contact sheets before paid Etsy launch.",
            "low",
            "local",
        )
        add(
            rows,
            122,
            "etsy_darwinian_lab",
            "Build V7 Etsy listing readiness packet after visual QA",
            "READY" if v7_visual_qa and not v7_packet else "DONE_WAITING_LAUNCH_GUARD",
            f"visual_qa={dict(v7_visual_qa)}; listing_packet={dict(v7_packet)}.",
            "py modules\\etsy_darwinian_lab_listing_packet.py --limit 6",
            "QA-passed or upscale-review assets are separated from vectorization/layout holds, with Etsy metadata and no fee spend.",
            "low",
            "local",
        )
        add(
            rows,
            123,
            "etsy_darwinian_lab",
            "Package V7 Etsy digital candidates for spotcheck before paid launch",
            "READY" if v7_packageable_remaining and not v7_upload else "DONE_READY_FOR_SPOTCHECK",
            (
                f"listing_packet={dict(v7_packet)}; upload_queue={dict(v7_upload)}; "
                f"packageable_remaining={v7_packageable_remaining}; gray_queue_ids={len(v7_gray_ids)}."
            ),
            "py modules\\etsy_darwinian_lab_package_builder.py --limit 6",
            "Ready/upscale-review candidates have preview images, download ZIPs, and an upload queue with no Etsy fee spent.",
            "low",
            "local",
        )

    if etsy_gray["published"]:
        if etsy_metadata_ready and not etsy_gray["ready"]:
            etsy_stage_status = "READY" if etsy_gray["daily_fee_slots"] > 0 else "WAIT_FEE_CAP"
            add(
                rows,
                68,
                "etsy",
                "Stage next Etsy digital metadata rows into guarded gray launch queue",
                etsy_stage_status,
                (
                    f"metadata_ready={etsy_metadata_ready}; gray_ready={etsy_gray['ready']}; "
                    f"today_spend=${etsy_gray['daily_spend']:.2f}/${etsy_gray['daily_cap']:.2f}; "
                    f"confirmed_spend=${etsy_gray['confirmed_spend']:.2f}."
                ),
                "py modules\\etsy_digital_gray_launch.py --limit 3",
                "A small batch of READY_FOR_ETSY_DRAFT rows is moved into the gray launch queue with QA and fee-reserve checks before any paid publish.",
                "medium",
                "local/API-safe",
            )
        if etsy_gray["ready"]:
            add(
                rows,
                67,
                "etsy",
                "Publish next Etsy digital batch under fee guard",
                "WAIT_V155_POD_PRIORITY" if v155_active else ("READY" if etsy_can_paid_publish else "WAIT_RISK"),
                (
                    f"{etsy_gray['ready']} guarded Etsy digital rows are ready; "
                    f"confirmed_spend=${etsy_gray['confirmed_spend']:.2f}. "
                    + ("V15.5 is active, so Digital publish is held behind Acrylic/Poster POD and purge work. " if v155_active else "")
                    + ("" if etsy_can_paid_publish else etsy_blocker)
                ),
                "py modules\\etsy_api_digital_publisher.py --limit 1",
                "One Etsy digital listing is published only if V15.5 POD priority is satisfied; ledger confirms $0.20 spend and the row gets an Etsy listing id before the next paid action.",
                "medium",
                "Etsy API",
            )
        etsy_live_age = file_age_minutes(ETSY_LIVE_AUDIT)
        etsy_live_status = (
            "READY_MONITOR"
            if not is_recent(ETSY_LIVE_AUDIT, 120)
            else "DONE_RECENT_MONITOR"
        )
        add(
            rows,
            66,
            "etsy",
            "Etsy public listing engine: read signal, then publish next controlled batch under fee guard",
            etsy_live_status if etsy_can_write else "READY_MONITOR_ONLY",
            (
                f"Live={etsy_gray['published']} ready={etsy_gray['ready']} "
                f"confirmed_spend=${etsy_gray['confirmed_spend']:.2f}; "
                f"live_audit_age={etsy_live_age if etsy_live_age is not None else 'missing'}m. "
                + ("" if etsy_can_write else etsy_blocker)
            ),
            "py modules\\etsy_live_audit.py --limit 20",
            "Etsy signal is refreshed; if fee/risk guard allows and copy/QA passes, the next non-spam batch can be prepared/published under the $50/$60 budget.",
            "medium",
            "Etsy public/API or Edge UI",
        )
    elif etsy_digital_count:
        add(
            rows,
            66,
            "etsy",
            "Start Etsy public listing engine under fee guard",
            "WAIT_V155_POD_PRIORITY" if v155_active else ("READY" if etsy_gray["ready"] and etsy_can_paid_publish else "WAIT_RISK"),
            (
                f"{etsy_digital_count} legacy packet rows and {etsy_gray['ready']} gray queue rows prepared; "
                f"confirmed_spend=${etsy_gray['confirmed_spend']:.2f}. "
                + ("V15.5 is active, so Digital publish is held behind Acrylic/Poster POD and purge work. " if v155_active else "")
                + ("" if etsy_can_paid_publish else etsy_blocker)
            ),
            "py modules\\etsy_api_digital_publisher.py --limit 1",
            "One listing is published and confirmed before the next; no blind retries or duplicate fee spend. Scale only by controlled batches under the $50/$60 budget.",
            "medium",
            "Etsy API or Edge UI",
        )

    if blueprint_count:
        add(
            rows,
            46,
            "r_and_d",
            "Validate next product candidates with official Printify blueprint/provider/variant data",
            "DONE_READY_FOR_SCHOLAR_REVIEW" if blueprint_count else "READY_FOR_SCHOLAR_REVIEW",
            f"{blueprint_count} next blueprint candidates are documented.",
            "py modules\\product_blueprint_next_plan.py",
            "Canvas, framed poster, notebook, mug, and metal candidates have enough data for Scholar review before development.",
        )

    runway_age = file_age_minutes(MONTHLY_RUNWAY_STATE)
    runway_state = {}
    if MONTHLY_RUNWAY_STATE.exists():
        try:
            runway_state = json.loads(MONTHLY_RUNWAY_STATE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            runway_state = {}
    runway_alert = bool(runway_state.get("alert"))
    v16_age = file_age_minutes(V16_AESTHETIC_DNA_MATRIX)
    v16_ready = V16_AESTHETIC_DNA_MATRIX.exists() and V16_AESTHETIC_DNA_PACKET.exists()
    add(
        rows,
        57,
        "strategy_replenishment",
        "Build V16 premium aesthetic DNA matrix for high-end product development",
        "DONE_CURRENT" if v16_ready and is_recent(V16_AESTHETIC_DNA_MATRIX, 1440) else "READY",
        (
            f"matrix_exists={V16_AESTHETIC_DNA_MATRIX.exists()}; "
            f"packet_exists={V16_AESTHETIC_DNA_PACKET.exists()}; "
            f"age={v16_age if v16_age is not None else 'missing'}m. "
            "This is monthly-task replenishment: turn Rex/Gemini high-end strategy into executable DNA rows."
        ),
        "py modules\\v16_aesthetic_dna_matrix.py",
        "A durable premium DNA matrix exists for DeepSeek/Claude/MJ to create higher-value acrylic/poster designs without touching marketplaces.",
        "low",
        "local",
    )

    performance_lifecycle_age = file_age_minutes(PERFORMANCE_LIFECYCLE_RULES)
    performance_lifecycle_ready = PERFORMANCE_LIFECYCLE_RULES.exists() and PERFORMANCE_LIFECYCLE_PACKET.exists()
    add(
        rows,
        55,
        "performance_lifecycle",
        "Define performance lifecycle rules for views, favorites, ads, retirements, and winner cloning",
        "DONE_CURRENT" if performance_lifecycle_ready and is_recent(PERFORMANCE_LIFECYCLE_RULES, 1440) else "READY",
        (
            f"rules_exists={PERFORMANCE_LIFECYCLE_RULES.exists()}; "
            f"packet_exists={PERFORMANCE_LIFECYCLE_PACKET.exists()}; "
            f"age={performance_lifecycle_age if performance_lifecycle_age is not None else 'missing'}m. "
            "This converts marketplace signals into controlled actions instead of blind volume."
        ),
        "py modules\\performance_lifecycle_autopilot_plan.py",
        "The system has explicit no-fee rules for when to rewrite, promote, bundle, retire, or clone listings.",
        "low",
        "local",
    )

    adobe_scaffold_age = file_age_minutes(ADOBE_STOCK_KEYWORD_PACK)
    adobe_scaffold_ready = (
        ADOBE_STOCK_KEYWORD_PACK.exists()
        and ADOBE_STOCK_METADATA_SCHEMA.exists()
        and ADOBE_STOCK_SCAFFOLD.exists()
    )
    add(
        rows,
        34,
        "adobe_stock",
        "Prepare Adobe Stock passive-fortress metadata and keyword scaffold",
        "DONE_CURRENT" if adobe_scaffold_ready and is_recent(ADOBE_STOCK_KEYWORD_PACK, 1440) else "READY",
        (
            f"keyword_pack_exists={ADOBE_STOCK_KEYWORD_PACK.exists()}; "
            f"schema_exists={ADOBE_STOCK_METADATA_SCHEMA.exists()}; "
            f"packet_exists={ADOBE_STOCK_SCAFFOLD.exists()}; "
            f"age={adobe_scaffold_age if adobe_scaffold_age is not None else 'missing'}m. "
            "No upload: this only prepares low-risk texture/background stock assets."
        ),
        "py modules\\adobe_stock_scaffold.py",
        "Adobe Stock has a reusable metadata schema and keyword family pack ready for later FTP/CSV automation.",
        "low",
        "local",
    )

    add(
        rows,
        56,
        "control",
        "Check monthly-task runway and alert Rex/Gemini before the queue gets thin",
        "READY" if not is_recent(MONTHLY_RUNWAY_STATE, 240) else ("DONE_ALERT_ACTIVE" if runway_alert else "DONE_RUNWAY_CURRENT"),
        (
            f"state_exists={MONTHLY_RUNWAY_STATE.exists()}; "
            f"age={runway_age if runway_age is not None else 'missing'}m; "
            f"alert={runway_alert}; "
            f"estimated_days={runway_state.get('estimated_remaining_days', 'unknown')}. "
            "Warn Rex/Gemini when remaining actionable monthly work is at or below two days."
        ),
        "py modules\\monthly_task_runway_monitor.py",
        "A local state file and Rex/Gemini packet exist if the monthly task runway falls to two days or less.",
        "low",
        "local",
    )

    ssd_inventory_age = file_age_minutes(SSD_MIGRATION_INVENTORY)
    ssd_plan_ready = SSD_MIGRATION_PLAN.exists() and SSD_MIGRATION_INVENTORY.exists()
    add(
        rows,
        32,
        "infrastructure",
        "Prepare PNY 1TB SSD asset migration and bloodshop storage plan",
        "DONE_READY_FOR_SSD" if ssd_plan_ready and is_recent(SSD_MIGRATION_INVENTORY, 1440) else "READY",
        (
            f"plan_exists={SSD_MIGRATION_PLAN.exists()}; "
            f"inventory_exists={SSD_MIGRATION_INVENTORY.exists()}; "
            f"inventory_age={ssd_inventory_age if ssd_inventory_age is not None else 'missing'}m. "
            "Run before and after the SSD arrives; this planning command does not move files."
        ),
        "py modules\\ssd_migration_plan.py",
        "A safe migration inventory and arrival procedure exist for moving assets/Adobe-stock batches to the external SSD without moving secrets or active databases.",
        "low",
        "local",
    )

    add(
        rows,
        30,
        "fallback_income",
        "Prepare fallback AI labor income track after core Printify/Etsy/eBay work is unblocked or waiting",
        "DONE_FEASIBILITY_WAIT_CORE" if FALLBACK_EVAL.exists() else "READY_FEASIBILITY",
        f"Fallback feasibility report exists={FALLBACK_EVAL.exists()}; keep behind active P0/P1 unless those tracks are waiting on data or Rex input.",
        "py modules\\fallback_income_factory_plan.py",
        "Adobe Stock/microstock or other repeatable AI labor track has a cold feasibility report, reusable OpenClaw module map, and first safe scaffold plan.",
        "low",
        "research/local",
    )

    live_repair_rows = read_csv(PRINTIFY_GALLERY_REPAIR_QUEUE)
    for action in read_csv(ACTION_QUEUE):
        if clean(action.get("lane")) == "gallery_integrity" and not live_repair_rows:
            continue
        lane = clean(action.get("lane"))
        command = clean(action.get("command"))
        status = clean(action.get("status"))
        priority = int(clean(action.get("priority")) or 20)
        reason = clean(action.get("reason"))
        recent_status = supervisor_action_recent_status(command)
        if recent_status and status.upper().startswith("READY"):
            status, reason = recent_status
            priority = min(priority, 25)
        if lane == "local" and "factory_supervisor.py --execute-local" in command and status.upper().startswith("READY"):
            priority = min(priority, 35)
            reason = (
                f"{reason} Maintenance is capped below production tasks; "
                "continue-monthly should not spend the prime loop on reports unless no concrete work is ready."
            )
        if lane == "local" and "factory_supervisor.py --execute-local" in command and not supervisor_due:
            priority = min(priority, 20)
            status = "WAIT_COOLDOWN"
            reason = (
                f"Local supervisor already refreshed {supervisor_age}m ago; "
                f"cooldown={SUPERVISOR_COOLDOWN_MINUTES}m. Continue-monthly should select production/market tasks instead."
            )
        add(
            rows,
            priority,
            f"supervisor:{lane}",
            clean(action.get("action")),
            status,
            reason,
            command,
            "Supervisor action remains present until its status is completed or superseded.",
            clean(action.get("risk")) or "low",
            clean(action.get("requires_network")) or "unknown",
        )

    rows.sort(key=lambda row: (-int(row["Priority"]), row["Lane"], row["Task"]))
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    with BACKLOG_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    status_counts = Counter(row["Status"] for row in rows)
    lane_counts = Counter(row["Lane"] for row in rows)
    lines = [
        "# Factory Backlog",
        "",
        f"Generated: {now_text()} America/New_York",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in status_counts.most_common():
        lines.append(f"- {status}: {count}")
    lines.extend(["", "## Lane Counts", ""])
    for lane, count in lane_counts.most_common():
        lines.append(f"- {lane}: {count}")
    lines.extend(["", "## Tasks", ""])
    for row in rows:
        lines.extend(
            [
                f"### P{row['Priority']} {row['Lane']} - {row['Status']}",
                f"- Task: {row['Task']}",
                f"- Blocker: {row['Blocker']}",
                f"- Command: `{row['Command']}`",
                f"- Done when: {row['Done_When']}",
                f"- Risk/network: {row['Risk']} / {row['Network_Need']}",
                "",
            ]
        )
    BACKLOG_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_outputs(rows)
    print(f"[FACTORY-BACKLOG] rows={len(rows)} csv={BACKLOG_CSV}")
    for status, count in Counter(row["Status"] for row in rows).most_common():
        print(f"[FACTORY-BACKLOG] {status}={count}")


if __name__ == "__main__":
    main()
