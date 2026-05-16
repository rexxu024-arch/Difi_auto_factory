"""V8 Grey overseer loop and daily bridge payload.

This module is deliberately advisory. It may call Gemini, write local reports,
and queue review notes, but it must not mutate marketplace listings or spend.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.grey_api_client import GreyApiError, extract_text, generate

DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
BRIDGE = REVIEW / "Gemini_Bridge"
LOG_PATH = DATABASE / "Grey_Overseer_V8_Log.csv"
STATE_PATH = DATABASE / "Grey_Overseer_V8_State.json"
NY_TZ = ZoneInfo("America/New_York")

MAX_PAYLOAD_CHARS = 28000
MAX_LOG_LINES = 500


def now() -> datetime:
    return datetime.now(NY_TZ)


def now_text() -> str:
    return now().isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
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


def tail_lines(path: Path, limit: int = MAX_LOG_LINES) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    return "\n".join(lines[-limit:])


def tail_chars(path: Path, limit: int = 8000) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[-limit:]


def money(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def count_by(rows: list[dict[str, str]], field: str) -> Counter:
    return Counter((row.get(field) or "UNKNOWN").strip() or "UNKNOWN" for row in rows)


def latest_rows_by_timestamp(rows: list[dict[str, str]], ts_field: str) -> list[dict[str, str]]:
    latest = ""
    out: list[dict[str, str]] = []
    for row in rows:
        ts = row.get(ts_field) or ""
        if ts > latest:
            latest = ts
            out = [row]
        elif ts == latest:
            out.append(row)
    return out


def etsy_stats() -> dict:
    queue = read_csv(DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv")
    fee_rows = read_csv(DATABASE / "Etsy_Fee_Ledger.csv")
    live_audit = read_csv(DATABASE / "Etsy_Digital_Live_Audit.csv")
    risk = read_json(DATABASE / "Account_Risk_State.json").get("states", {}).get("etsy", {})
    guard = read_json(DATABASE / "Etsy_Fee_Kill_Switch.json")
    today = now().date().isoformat()
    published_today = [
        row
        for row in queue
        if row.get("Etsy_Listing_ID") and str(row.get("Timestamp") or "").startswith(today)
    ]
    spend = sum(
        money(row.get("Confirmed_Spent_USD"))
        for row in fee_rows
        if str(row.get("Status", "")).startswith("CONFIRMED")
    )
    return {
        "queue_rows": len(queue),
        "live_identified": sum(1 for row in queue if row.get("Etsy_Listing_ID")),
        "published_today": len(published_today),
        "spend_confirmed_usd": round(spend, 2),
        "budget_usd": money(guard.get("authorized_pool_budget_usd") or 50),
        "absolute_cap_usd": money(guard.get("absolute_no_result_spend_cap_usd") or 60),
        "risk_state": risk.get("risk_state", "UNKNOWN"),
        "paid_publish_allowed": bool(risk.get("paid_publish_allowed")),
        "launch_status": dict(count_by(queue, "Launch_Status")),
        "fee_status": dict(count_by(queue, "Fee_Status")),
        "live_audit_status": dict(count_by(live_audit, "Status")),
    }


def ebay_stats() -> dict:
    perf = read_csv(DATABASE / "Performance_Log.csv")
    latest = latest_rows_by_timestamp(perf, "Snapshot_Timestamp")
    ad_plan = read_csv(DATABASE / "eBay_Ad_Rate_Experiment_Plan.csv")
    selected = [row for row in ad_plan if (row.get("Selected_For_Test") or "").lower() == "yes"]
    title_issues = [row for row in ad_plan if row.get("Title_Quality_Issue")]
    return {
        "latest_snapshot_rows": len(latest),
        "latest_snapshot_timestamp": (latest[0].get("Snapshot_Timestamp") if latest else ""),
        "zero_view": sum(1 for row in latest if row.get("Views_30_Days") == "0"),
        "with_views": sum(1 for row in latest if str(row.get("Views_30_Days") or "").isdigit() and int(row.get("Views_30_Days") or 0) > 0),
        "promoted_general": sum(1 for row in latest if row.get("General_Status") == "Promoted"),
        "ad_experiment_selected_rows": len(selected),
        "ad_title_issue_rows": len({row.get("ID") for row in title_issues if row.get("ID")}),
    }


def printify_stats() -> dict:
    zone2 = read_csv(DATABASE / "Shock_And_Awe_V5_Printify_Private_Drafts.csv")
    zones13 = read_csv(DATABASE / "Shock_And_Awe_V5_Zones1_3_Printify_Private_Drafts.csv")
    recovery = read_csv(DATABASE / "Shock_And_Awe_V5_Recovery_MJ_Queue.csv")
    return {
        "private_drafts_created": sum(1 for row in zone2 + zones13 if row.get("Draft_Status") == "PRINTIFY_DRAFT_CREATED"),
        "zone2_private_drafts": sum(1 for row in zone2 if row.get("Draft_Status") == "PRINTIFY_DRAFT_CREATED"),
        "zones13_private_drafts": sum(1 for row in zones13 if row.get("Draft_Status") == "PRINTIFY_DRAFT_CREATED"),
        "private_recovery_rows": len(recovery),
        "private_recovery_status": dict(count_by(recovery, "Recovery_Action")),
    }


def v7_stats() -> dict:
    concepts = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_Queue.csv")
    mj = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_MJ_Dispatch_Queue.csv")
    visual = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_Visual_QA.csv")
    upload = read_csv(DATABASE / "Etsy_Darwinian_Lab_V7_Upload_Queue.csv")
    return {
        "concepts": len(concepts),
        "mj_submitted": sum(1 for row in mj if row.get("Dispatch_Status") == "MJ_SUBMITTED"),
        "harvest_ready": sum(1 for row in mj if row.get("Harvest_Status") == "READY_FOR_VISUAL_QA"),
        "visual_rows": len(visual),
        "visual_status": dict(count_by(visual, "Gate_Status")),
        "upload_ready": sum(1 for row in upload if str(row.get("Package_Status", "")).startswith("READY")),
        "upload_total": len(upload),
    }


def collect_core_data() -> dict:
    backlog = read_csv(DATABASE / "Factory_Backlog.csv")
    ready = [
        {
            "priority": row.get("Priority"),
            "lane": row.get("Lane"),
            "task": row.get("Task"),
            "status": row.get("Status"),
            "blocker": row.get("Blocker"),
        }
        for row in backlog
        if str(row.get("Status", "")).startswith("READY")
    ][:8]
    return {
        "timestamp_et": now_text(),
        "etsy": etsy_stats(),
        "ebay": ebay_stats(),
        "printify_private": printify_stats(),
        "etsy_v7": v7_stats(),
        "backlog_ready": ready,
        "recent_progress_tail": tail_lines(PROGRESS_LOG := PROJECT_ROOT / "PROGRESS_LOG.md", MAX_LOG_LINES),
        "recent_grey_state": read_json(DATABASE / "Grey_Bridge_State.json"),
    }


def truncate_payload(text: str, max_chars: int = MAX_PAYLOAD_CHARS) -> tuple[str, bool]:
    if len(text) <= max_chars:
        return text, False
    head = text[:6000]
    tail = text[-(max_chars - len(head) - 300):]
    marker = "\n\n[TRUNCATED: non-core middle removed by V8 token guard]\n\n"
    return head + marker + tail, True


def call_gemini_with_retry(prompt: str, *, tier: str, attempts: int, retry_sleep: int) -> dict:
    last_error = ""
    for attempt in range(1, attempts + 1):
        try:
            payload = generate(prompt, tier=tier, timeout=120)
            text = extract_text(payload)
            if not text:
                raise GreyApiError("EMPTY_GEMINI_RESPONSE")
            return {"status": "OK", "tier": tier, "attempt": attempt, "text": text}
        except Exception as exc:  # noqa: BLE001
            last_error = f"{type(exc).__name__}: {exc}"
            append_log("API_RETRY", f"tier={tier} attempt={attempt}/{attempts} {last_error}")
            if attempt < attempts:
                time.sleep(retry_sleep)
    return {"status": "ERROR", "tier": tier, "error": last_error}


def build_free_clean_prompt(data: dict) -> str:
    raw = json.dumps(data, ensure_ascii=False, indent=2)
    raw, truncated = truncate_payload(raw)
    return (
        "You are Gemini Flash in the OpenClaw V8 micro-cleaning lane. "
        "Clean and compress the following execution data. Extract only: counters, blockers, error codes, risks, and next obvious action. "
        "Do not invent facts. Do not suggest marketplace writes. Return compact Markdown bullets plus a tiny JSON summary.\n\n"
        f"Payload_Chars: {len(raw)} truncated={truncated}\n\n"
        f"{raw}"
    )


def build_paid_audit_prompt(cleaned: str, data: dict) -> str:
    compact = {
        "timestamp_et": data["timestamp_et"],
        "etsy": data["etsy"],
        "ebay": data["ebay"],
        "printify_private": data["printify_private"],
        "etsy_v7": data["etsy_v7"],
        "backlog_ready": data["backlog_ready"],
    }
    prompt = (
        "你现在是 Grey。请以极其冷酷、重逻辑的审计员视角，审视以下系统的今日执行数据。"
        "指出潜在的致命错误，并给出高维度的纠偏建议。不要说废话。\n\n"
        "Hard rules: advisory only; do not ask for secrets; do not recommend PPC/Priority ads; do not bypass platform defenses; "
        "do not recommend spend beyond caps.\n\n"
        "## Cleaned Flash Summary\n"
        f"{cleaned[:12000]}\n\n"
        "## Core Counters\n"
        f"{json.dumps(compact, ensure_ascii=False, indent=2)}"
    )
    return truncate_payload(prompt)[0]


def render_daily_sitrep(data: dict, free_result: dict, paid_result: dict, *, codex_decision: str) -> str:
    date = now().strftime("%Y%m%d")
    free_text = free_result.get("text") or f"{free_result.get('status')}: {free_result.get('error', '')}"
    paid_text = paid_result.get("text") or f"{paid_result.get('status')}: {paid_result.get('error', '')}"
    lines = [
        f"# Daily Grey SitRep {date}",
        "",
        f"Timestamp_ET: {data['timestamp_et']}",
        "System_Status: NORMAL_WITH_GUARDS",
        "",
        "## 1. 【核心战报】",
        "",
        f"- Etsy API/UI live identified: {data['etsy']['live_identified']}/{data['etsy']['queue_rows']}; today published: {data['etsy']['published_today']}; spend: ${data['etsy']['spend_confirmed_usd']:.2f}/${data['etsy']['budget_usd']:.2f}; risk={data['etsy']['risk_state']}; paid_allowed={data['etsy']['paid_publish_allowed']}.",
        f"- eBay latest snapshot: {data['ebay']['latest_snapshot_timestamp'] or 'none'}; zero-view={data['ebay']['zero_view']}/{data['ebay']['latest_snapshot_rows']}; with views={data['ebay']['with_views']}; promoted={data['ebay']['promoted_general']}; ad experiment selected rows={data['ebay']['ad_experiment_selected_rows']}.",
        f"- Printify private showcase: private drafts={data['printify_private']['private_drafts_created']}/30; recovery gaps={data['printify_private']['private_recovery_rows']}; recovery actions={data['printify_private']['private_recovery_status']}.",
        f"- Etsy V7 public lab: concepts={data['etsy_v7']['concepts']}/60; MJ submitted={data['etsy_v7']['mj_submitted']}/60; harvest-ready={data['etsy_v7']['harvest_ready']}/60; upload-ready={data['etsy_v7']['upload_ready']}/{data['etsy_v7']['upload_total']}.",
        "",
        "## 2. 【流量信号】",
        "",
        f"- eBay visible signal remains weak: {data['ebay']['with_views']} with views vs {data['ebay']['zero_view']} zero-view in latest stored snapshot.",
        f"- Etsy live audit statuses: {data['etsy']['live_audit_status']}. Favorites/orders are not yet reliably available through the local snapshot; treat traffic readback as a next data task.",
        "",
        "## 3. 【审计员 (API Grey) 建议】",
        "",
        "### Flash Cleaning Lane",
        free_text[:5000],
        "",
        "### Pro Audit Lane",
        paid_text[:7000],
        "",
        "## 4. 【Codex 最终决断】",
        "",
        codex_decision,
        "",
    ]
    return "\n".join(lines)


def append_log(status: str, detail: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        if not exists:
            writer.writerow(["Timestamp", "Status", "Detail"])
        writer.writerow([now_text(), status, detail[:2000]])


def write_state(payload: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def run(*, allow_paid: bool, dry_run: bool, retry_sleep: int, attempts: int) -> dict:
    BRIDGE.mkdir(parents=True, exist_ok=True)
    data = collect_core_data()
    free_prompt = build_free_clean_prompt(data)
    cleaned_path = BRIDGE / "TO_GREY_V8_FLASH_CLEAN_latest.md"
    cleaned_path.write_text(free_prompt, encoding="utf-8")

    if dry_run:
        free_result = {"status": "DRY_RUN", "text": "Dry run: Flash cleaning not called."}
        paid_result = {"status": "DRY_RUN", "text": "Dry run: Pro audit not called."}
    else:
        free_result = call_gemini_with_retry(free_prompt, tier="free", attempts=attempts, retry_sleep=retry_sleep)
        cleaned_text = free_result.get("text") if free_result.get("status") == "OK" else json.dumps(data, ensure_ascii=False)[:8000]
        if allow_paid:
            paid_prompt = build_paid_audit_prompt(str(cleaned_text), data)
            (BRIDGE / "TO_GREY_V8_PAID_AUDIT_latest.md").write_text(paid_prompt, encoding="utf-8")
            paid_result = call_gemini_with_retry(paid_prompt, tier="paid", attempts=attempts, retry_sleep=retry_sleep)
        else:
            paid_result = {"status": "SKIPPED_PAID_NOT_ALLOWED", "text": "Paid Pro audit skipped by command flag."}

    codex_decision = (
        "- Adopt: use Grey only as a cold audit lane; keep Codex/local files authoritative.\n"
        "- Adopt: continue Etsy API publishing only under fee/risk guard and avoid Etsy UI while login anomaly is active.\n"
        "- Adopt: eBay sticker pricing must stay profit-positive; ads above 2% require product-level margin proof.\n"
        "- Reject: any API advice that requires platform-defense bypass, uncontrolled spend, or raw log dumping.\n"
        "- Next tilt: Etsy API-safe publish/QA, eBay pricing/ad experiment hygiene, and Shock & Awe recovery gaps."
    )
    sitrep = render_daily_sitrep(data, free_result, paid_result, codex_decision=codex_decision)
    date = now().strftime("%Y%m%d")
    sitrep_path = BRIDGE / f"Daily_Grey_SitRep_{date}.txt"
    latest_path = BRIDGE / "Daily_Grey_SitRep_latest.txt"
    sitrep_path.write_text(sitrep, encoding="utf-8")
    latest_path.write_text(sitrep, encoding="utf-8")

    result = {
        "status": "OK",
        "timestamp_et": data["timestamp_et"],
        "dry_run": dry_run,
        "allow_paid": allow_paid,
        "free_status": free_result.get("status"),
        "paid_status": paid_result.get("status"),
        "sitrep_path": str(sitrep_path),
        "latest_path": str(latest_path),
        "etsy_live": data["etsy"]["live_identified"],
        "etsy_spend": data["etsy"]["spend_confirmed_usd"],
    }
    write_state(result)
    append_log("OK", json.dumps(result, ensure_ascii=False))
    return result


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="OpenClaw V8 Grey overseer daily sitrep")
    parser.add_argument("--allow-paid", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--retry-sleep", type=int, default=60)
    parser.add_argument("--attempts", type=int, default=3)
    args = parser.parse_args()
    try:
        result = run(allow_paid=args.allow_paid, dry_run=args.dry_run, retry_sleep=args.retry_sleep, attempts=args.attempts)
    except Exception as exc:  # noqa: BLE001
        result = {
            "status": "ERROR_RECORDED_LOCAL_CONTINUE",
            "timestamp_et": now_text(),
            "error": f"{type(exc).__name__}: {exc}",
            "message": "Grey overseer failed but must not stall OpenClaw; continue local monthly tasks.",
        }
        write_state(result)
        append_log("ERROR_RECORDED_LOCAL_CONTINUE", json.dumps(result, ensure_ascii=False))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
