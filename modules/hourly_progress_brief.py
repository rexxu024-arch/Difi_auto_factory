from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REPORTS = PROJECT_ROOT / "Reports"


def now_et() -> datetime:
    return datetime.now(ZoneInfo("America/New_York"))


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {}


def money(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def count_by(rows: list[dict], key: str) -> Counter:
    return Counter(row.get(key) or "UNKNOWN" for row in rows)


def latest_by_id(rows: list[dict], key: str) -> list[dict]:
    latest: dict[str, dict] = {}
    for row in rows:
        item_id = row.get(key) or ""
        if item_id:
            latest[item_id] = row
    return list(latest.values())


def etsy_progress() -> dict:
    queue = read_csv(DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv")
    fee = read_csv(DATABASE / "Etsy_Fee_Ledger.csv")
    guard = read_json(DATABASE / "Etsy_Fee_Kill_Switch.json")
    risk = read_json(DATABASE / "Account_Risk_State.json").get("states", {}).get("etsy", {})
    live = [row for row in queue if row.get("Etsy_Listing_ID")]
    confirmed = [row for row in queue if str(row.get("Fee_Status", "")).startswith("CONFIRMED")]
    spend = sum(money(row.get("Confirmed_Spent_USD")) for row in fee if str(row.get("Status", "")).startswith("CONFIRMED"))
    return {
        "target": int(guard.get("authorized_pool_listings") or 250),
        "budget": money(guard.get("authorized_pool_budget_usd") or 50),
        "absolute_cap": money(guard.get("absolute_no_result_spend_cap_usd") or 60),
        "queued": len(queue),
        "live": len(live),
        "confirmed": len(confirmed),
        "spend": spend,
        "risk_state": risk.get("risk_state", "UNKNOWN"),
        "paid_allowed": bool(risk.get("paid_publish_allowed")),
        "launch_status": count_by(queue, "Launch_Status"),
        "fee_status": count_by(queue, "Fee_Status"),
    }


def v7_progress() -> dict:
    concepts = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_Queue.csv")
    mj = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv")
    visual = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_Visual_QA.csv")
    upload = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_Upload_Queue.csv")
    listing = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_Listing_Packet.csv")
    return {
        "target": 60,
        "concepts": len(concepts),
        "mj_submitted": sum(1 for row in mj if row.get("Dispatch_Status") == "MJ_SUBMITTED"),
        "mj_ready": sum(1 for row in mj if row.get("Dispatch_Status") == "READY_FOR_MJ"),
        "harvest_ready": sum(1 for row in mj if row.get("Harvest_Status") == "READY_FOR_VISUAL_QA"),
        "harvest_hold": sum(1 for row in mj if "HOLD" in str(row.get("Harvest_Status", ""))),
        "visual": len(visual),
        "visual_status": count_by(visual, "Gate_Status"),
        "upload_ready": sum(1 for row in upload if str(row.get("Package_Status", "")).startswith("READY")),
        "upload_total": len(upload),
        "listing_packet": len(listing),
        "listing_status": count_by(listing, "Launch_Readiness"),
    }


def private_showcase_progress() -> dict:
    zone2 = read_csv(DATABASE / "Shock_And_Awe_V5_Printify_Private_Drafts.csv")
    final = read_csv(DATABASE / "Shock_And_Awe_V5_Final_Selection.csv")
    zones13 = read_csv(DATABASE / "Shock_And_Awe_V5_Zones1_3_MJ_Dispatch_Queue.csv")
    zones13_drafts = read_csv(DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Drafts.csv")
    zones13_selection = read_csv(DATABASE / "Shock_And_Awe_V5_Zones1_3_Final_Selection.csv")
    zones13_private_drafts = sum(
        1 for row in zones13_drafts if row.get("Draft_Status") == "PRINTIFY_DRAFT_CREATED"
    )
    zone2_private_drafts = sum(
        1 for row in zone2 if row.get("Draft_Status") == "PRINTIFY_DRAFT_CREATED"
    )
    zones13_harvested = sum(
        1
        for row in zones13
        if row.get("Harvest_Status") in {"GRID_FOUND", "READY_FOR_VISUAL_QA", "VISUAL_QA_PASSED"}
    )
    zones13_visual_ready = sum(1 for row in zones13 if row.get("Harvest_Status") == "READY_FOR_VISUAL_QA")
    zones13_visual_pass = sum(1 for row in zones13 if str(row.get("Visual_QA_Status") or "").startswith("PASS"))
    zones13_visual_review = sum(1 for row in zones13 if str(row.get("Visual_QA_Status") or "").startswith("REVIEW"))
    zones13_visual_hold = sum(1 for row in zones13 if str(row.get("Visual_QA_Status") or "").startswith("HOLD"))
    zones13_selection_hold = sum(1 for row in zones13_selection if str(row.get("Final_Status") or "").startswith("HOLD"))
    return {
        "target": 30,
        "private_drafts_total": zone2_private_drafts + zones13_private_drafts,
        "zone2_private_drafts": zone2_private_drafts,
        "zones13_private_drafts": zones13_private_drafts,
        "final_selected": len(final) + len(zones13_selection),
        "zones13_selection_hold": zones13_selection_hold,
        "zones13_submitted": sum(1 for row in zones13 if row.get("Dispatch_Status") == "MJ_SUBMITTED"),
        "zones13_ready": sum(1 for row in zones13 if row.get("Dispatch_Status") == "READY_FOR_MJ"),
        "zones13_grid_found": zones13_harvested,
        "zones13_visual_ready": zones13_visual_ready,
        "zones13_visual_pass": zones13_visual_pass,
        "zones13_visual_review": zones13_visual_review,
        "zones13_visual_hold": zones13_visual_hold,
        "zones13_total": len(zones13),
    }


def ebay_progress() -> dict:
    perf_rows = read_csv(DATABASE / "Performance_Log.csv")
    latest_ts = ""
    latest = []
    for row in perf_rows:
        ts = row.get("Snapshot_Timestamp") or ""
        if ts > latest_ts:
            latest_ts = ts
            latest = [row]
        elif ts == latest_ts:
            latest.append(row)
    return {
        "latest_ts": latest_ts,
        "rows": len(latest),
        "zero_view": sum(1 for row in latest if row.get("Views_30_Days") == "0"),
        "has_view": sum(1 for row in latest if str(row.get("Views_30_Days") or "").isdigit() and int(row.get("Views_30_Days") or 0) > 0),
        "promoted": sum(1 for row in latest if row.get("General_Status") == "Promoted"),
    }


def backlog_progress() -> dict:
    rows = read_csv(DATABASE / "Factory_Backlog.csv")
    return {
        "rows": len(rows),
        "status": count_by(rows, "Status"),
        "top_ready": [
            {
                "priority": row.get("Priority"),
                "lane": row.get("Lane"),
                "task": row.get("Task"),
                "status": row.get("Status"),
            }
            for row in sorted(rows, key=lambda r: int(r.get("Priority") or 0), reverse=True)
            if str(row.get("Status", "")).startswith("READY")
        ][:5],
    }


def build_report() -> tuple[str, dict]:
    etsy = etsy_progress()
    v7 = v7_progress()
    private = private_showcase_progress()
    ebay = ebay_progress()
    backlog = backlog_progress()
    timestamp = now_et().strftime("%Y-%m-%d %H:%M:%S %z")
    data = {
        "timestamp": timestamp,
        "etsy": etsy,
        "v7": v7,
        "private_showcase": private,
        "ebay": ebay,
        "backlog": backlog,
    }

    lines = [
        f"# OpenClaw Hourly Progress Brief",
        "",
        f"Generated: {timestamp} America/New_York",
        "",
        "## Dashboard",
        "",
        f"- Etsy paid launch: {etsy['live']}/{etsy['target']} live/identified, ${etsy['spend']:.2f}/${etsy['budget']:.2f} confirmed spend, risk `{etsy['risk_state']}`, paid_allowed={etsy['paid_allowed']}.",
        f"- Etsy V7 Darwinian Lab: {v7['concepts']}/{v7['target']} concepts, {v7['mj_submitted']}/{v7['target']} MJ submitted, {v7['harvest_ready']}/{v7['target']} harvest-ready, {v7['visual']}/{v7['target']} visual-QA image rows, {v7['upload_ready']}/{v7['target']} upload-ready packages.",
        f"- Private Shock & Awe: {private['private_drafts_total']}/30 private Printify drafts ({private['zone2_private_drafts']} Zone2 + {private['zones13_private_drafts']} Zone1/3), {private['final_selected']}/30 reviewed selections, {private['zones13_submitted']}/20 Zone1/3 prompts submitted, {private['zones13_grid_found']}/20 grids harvested, {private['zones13_visual_ready']}/20 visual-ready, QA PASS/REVIEW/HOLD={private['zones13_visual_pass']}/{private['zones13_visual_review']}/{private['zones13_visual_hold']}, production holds={private['zones13_selection_hold']}.",
        f"- eBay signal: latest snapshot `{ebay['latest_ts'] or 'none'}`, {ebay['zero_view']}/{ebay['rows']} zero-view, {ebay['has_view']} with views, {ebay['promoted']} promoted.",
        f"- Backlog: {backlog['rows']} rows; READY-like tasks={sum(v for k, v in backlog['status'].items() if str(k).startswith('READY'))}.",
        "",
        "## Status Details",
        "",
        f"- Etsy launch statuses: {dict(etsy['launch_status'])}",
        f"- Etsy fee statuses: {dict(etsy['fee_status'])}",
        f"- V7 visual QA statuses: {dict(v7['visual_status'])}",
        f"- V7 listing statuses: {dict(v7['listing_status'])}",
        "",
        "## Next Ready Tasks",
        "",
    ]
    if backlog["top_ready"]:
        for item in backlog["top_ready"]:
            lines.append(f"- P{item['priority']} `{item['lane']}` {item['status']}: {item['task']}")
    else:
        lines.append("- No READY task found; refresh backlog or inspect blockers.")

    text = "\n".join(lines) + "\n"
    return text, data


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    text, data = build_report()
    stamp = now_et().strftime("%Y%m%d_%H%M")
    report_path = REPORTS / f"hourly_progress_{stamp}.md"
    latest_path = REPORTS / "hourly_progress_latest.md"
    json_path = DATABASE / "Hourly_Progress_State.json"
    report_path.write_text(text, encoding="utf-8")
    latest_path.write_text(text, encoding="utf-8")
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
