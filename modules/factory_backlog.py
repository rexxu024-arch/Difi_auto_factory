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

ACTION_QUEUE = DATABASE_DIR / "Factory_Autopilot_Action_Queue.csv"
MARKET_QUEUE = DATABASE_DIR / "Market_Signal_Action_Queue.csv"
COVER_REPAIR_DECISIONS = DATABASE_DIR / "eBay_Cover_Repair_Decisions.csv"
COVER_REPLACEMENT_QUEUE = DATABASE_DIR / "eBay_Cover_Replacement_Queue.csv"
TRAFFIC_DIAGNOSIS = DATABASE_DIR / "eBay_Traffic_Diagnosis.csv"
BLUEPRINT_PLAN = DATABASE_DIR / "Product_Blueprint_Next_Test_Plan.csv"
ETSY_DIGITAL_PACKET = DATABASE_DIR / "Etsy_Digital_Final_Upload_Packet.csv"
SUPERVISOR_STATE = DATABASE_DIR / "Factory_Autopilot_State.json"

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


def csv_count(path: Path) -> int:
    return len(read_csv(path))


def state() -> dict:
    if not SUPERVISOR_STATE.exists():
        return {}
    try:
        return json.loads(SUPERVISOR_STATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


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
    supervisor = state()
    printify_ui = supervisor.get("printify_ui_status") or {}
    market_actions = count_by(MARKET_QUEUE, "Recommended_Action")
    repair_methods = count_by(COVER_REPAIR_DECISIONS, "Repair_Method")
    replacement_status = count_by(COVER_REPLACEMENT_QUEUE, "Replacement_Status")
    diagnosis_count = csv_count(TRAFFIC_DIAGNOSIS)
    blueprint_count = csv_count(BLUEPRINT_PLAN)
    etsy_digital_count = csv_count(ETSY_DIGITAL_PACKET)

    add(
        rows,
        100,
        "control",
        "Run local supervisor maintenance cycle",
        "READY",
        "None",
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
            "Resume Ready_for_Printify uploads only after cover/default-image gate passes",
            "WAIT_COVER_GATE",
            f"{market_actions['UPLOAD_TO_PRINTIFY_SINGLE_ITEM_BATCH']} local rows are ready but should not upload until the image gate is proven.",
            "py modules\\printify_full_pipeline.py --limit 1",
            "A new single item reaches stable mockup state and passes selected-count/default-count audit.",
            "high",
            "Printify UI/API",
        )

    if market_actions.get("PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK", 0):
        add(
            rows,
            68,
            "publish",
            "Publish small cooled batch after image gate and network guard pass",
            "WAIT_COVER_GATE",
            f"{market_actions['PUBLISH_IN_SMALL_BATCH_WHEN_NETWORK_OK']} stable drafts are candidates, but public publish is blocked by cover/default-image risk.",
            "py modules\\printify_publish_scheduler.py --limit 3 --min-delay 180 --max-delay 420",
            "Published products are live-audited and added to 2% Standard/General ad coverage without PPC.",
            "high",
            "Printify API/eBay sync",
        )

    if diagnosis_count:
        add(
            rows,
            62,
            "market_learning",
            "Keep eBay traffic diagnosis current and avoid ad-only conclusions",
            "READY",
            f"{diagnosis_count} current traffic hypotheses generated.",
            "py modules\\ebay_traffic_diagnosis.py",
            "Traffic report identifies exposure/click/conversion blockers from snapshots and cover queues.",
        )

    if etsy_digital_count:
        add(
            rows,
            54,
            "etsy",
            "Hold Etsy digital packet until shop/API readiness, then launch curated low-cost test",
            "WAIT_USER_OR_API_APPROVAL",
            f"{etsy_digital_count} digital listing rows prepared locally; no Etsy fee triggered.",
            "py modules\\etsy_digital_listing_export.py",
            "When Etsy is cleared, first 20-30 curated listings have files, previews, tags, descriptions, and pricing ready.",
            "low",
            "local now / Etsy later",
        )

    if blueprint_count:
        add(
            rows,
            46,
            "r_and_d",
            "Validate next product candidates with official Printify blueprint/provider/variant data",
            "READY_FOR_SCHOLAR_REVIEW",
            f"{blueprint_count} next blueprint candidates are documented.",
            "py modules\\product_blueprint_next_plan.py",
            "Canvas, framed poster, notebook, mug, and metal candidates have enough data for Scholar review before development.",
        )

    for action in read_csv(ACTION_QUEUE):
        add(
            rows,
            int(clean(action.get("priority")) or 20),
            f"supervisor:{clean(action.get('lane'))}",
            clean(action.get("action")),
            clean(action.get("status")),
            clean(action.get("reason")),
            clean(action.get("command")),
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
