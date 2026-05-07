from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.request
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.system_resource_allocator import sample_resources


DATABASE_DIR = PROJECT_ROOT / "Database"
STATE_PATH = DATABASE_DIR / "Memory_Pressure_Guard_State.json"
LOG_PATH = DATABASE_DIR / "Memory_Pressure_Guard_Log.csv"
NY = ZoneInfo("America/New_York")

PROJECT_DOMAINS = (
    "printify.com/app",
    "www.ebay.com/sh/",
    "www.ebay.com/sl/",
    "www.etsy.com/your/shops/",
    "developer.ebay.com",
    "developer.etsy.com",
)

SAFE_IDLE_URL_PATTERNS = (
    "edge://newtab",
    "printify.com/app/dashboard",
    "www.ebay.com/sh/lst/active",
    "www.etsy.com/your/shops/me/dashboard",
    "www.etsy.com/your/shops/me/tools/listings",
)

UNSAFE_EDITOR_PATTERNS = (
    "listing-editor/create",
    "listing-editor/edit",
    "printify.com/app/editor",
    "printify.com/app/mockup-library",
    "payments",
    "billing",
    "orders",
    "messages",
)


def now_text() -> str:
    return datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S %z")


def _http_json(url: str, method: str = "GET", timeout: int = 5):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    if not data:
        return {}
    try:
        return json.loads(data.decode("utf-8", errors="replace"))
    except json.JSONDecodeError:
        return {"raw": data.decode("utf-8", errors="replace")}


def _close_edge_tabs(port: int, execute: bool, close_all_project_idle: bool) -> list[dict[str, str]]:
    closed: list[dict[str, str]] = []
    try:
        pages = _http_json(f"http://127.0.0.1:{port}/json/list")
    except Exception as exc:  # noqa: BLE001
        return [{"action": "EDGE_CDP_UNAVAILABLE", "error": f"{type(exc).__name__}: {exc}"}]
    if not isinstance(pages, list):
        return [{"action": "EDGE_CDP_BAD_RESPONSE"}]

    for page in pages:
        if page.get("type") != "page":
            continue
        url = page.get("url", "")
        title = page.get("title", "")
        if any(pattern in url for pattern in UNSAFE_EDITOR_PATTERNS):
            continue
        is_safe_idle = any(pattern in url for pattern in SAFE_IDLE_URL_PATTERNS)
        is_project_page = any(domain in url for domain in PROJECT_DOMAINS)
        should_close = is_safe_idle or (close_all_project_idle and is_project_page)
        if not should_close:
            continue
        row = {
            "action": "CLOSE_EDGE_PROJECT_TAB" if execute else "WOULD_CLOSE_EDGE_PROJECT_TAB",
            "id": str(page.get("id", "")),
            "title": title[:160],
            "url": url[:240],
        }
        if execute:
            try:
                _http_json(f"http://127.0.0.1:{port}/json/close/{page['id']}")
            except Exception as exc:  # noqa: BLE001
                row["error"] = f"{type(exc).__name__}: {exc}"
        closed.append(row)
    return closed


def _append_log(state: dict) -> None:
    row = {
        "Timestamp": state.get("timestamp", ""),
        "Mode": state.get("mode", ""),
        "Execute": state.get("execute", ""),
        "Memory_Before": state.get("memory_before", ""),
        "Memory_After": state.get("memory_after", ""),
        "CPU_Before": state.get("cpu_before", ""),
        "CPU_After": state.get("cpu_after", ""),
        "Closed_Count": len(state.get("closed_tabs", [])),
        "Decision": state.get("decision", ""),
        "Reason": state.get("reason", ""),
    }
    exists = LOG_PATH.exists()
    LOG_PATH.parent.mkdir(exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def run(
    *,
    execute: bool = False,
    cdp_port: int = 9223,
    memory_soft_pct: float = 86.0,
    memory_hard_pct: float = 92.0,
    close_all_project_idle: bool = False,
) -> dict:
    before = sample_resources()
    should_clean = (before.memory_used_pct or 0) >= memory_soft_pct
    closed_tabs: list[dict[str, str]] = []
    mode = "NOOP_BELOW_THRESHOLD"
    if should_clean:
        mode = "EXECUTE_CLEANUP" if execute else "DRY_RUN_CLEANUP"
        closed_tabs = _close_edge_tabs(cdp_port, execute=execute, close_all_project_idle=close_all_project_idle)
        if execute:
            time.sleep(3)
    after = sample_resources() if execute else before
    memory_after = after.memory_used_pct
    if (memory_after or 0) >= memory_hard_pct:
        decision = "MEMORY_STILL_HARD_PRESSURE"
        reason = "keep only local/report/API-read tasks; consider longer rest cycle if repeated"
    elif (memory_after or 0) >= memory_soft_pct:
        decision = "MEMORY_STILL_WARM_BUT_WORKABLE"
        reason = "continue light work; avoid browser/image-heavy tasks"
    else:
        decision = "MEMORY_OK_CONTINUE"
        reason = "normal work may continue under marketplace risk guards"

    state = {
        "timestamp": now_text(),
        "mode": mode,
        "execute": execute,
        "cdp_port": cdp_port,
        "memory_soft_pct": memory_soft_pct,
        "memory_hard_pct": memory_hard_pct,
        "memory_before": before.memory_used_pct,
        "memory_after": memory_after,
        "cpu_before": before.cpu_load_pct,
        "cpu_after": after.cpu_load_pct,
        "closed_tabs": closed_tabs,
        "top_processes": before.top_processes[:8],
        "decision": decision,
        "reason": reason,
        "privacy_rule": "Only closes project automation Edge tabs through CDP 9223. Does not inspect or close Rex's daily Chrome tabs.",
        "rest_rule": "Do not shutdown/restart by default; if pressure stays high after cleanup, write rest-cycle recommendation unless Rex explicitly requests immediate power action.",
    }
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    _append_log(state)
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description="Close safe idle project tabs before pausing work for memory pressure.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--cdp-port", type=int, default=9223)
    parser.add_argument("--memory-soft-pct", type=float, default=86.0)
    parser.add_argument("--memory-hard-pct", type=float, default=92.0)
    parser.add_argument("--close-all-project-idle", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    state = run(
        execute=args.execute,
        cdp_port=args.cdp_port,
        memory_soft_pct=args.memory_soft_pct,
        memory_hard_pct=args.memory_hard_pct,
        close_all_project_idle=args.close_all_project_idle,
    )
    if args.json:
        print(json.dumps(state, indent=2, ensure_ascii=False))
    else:
        print(
            f"[MEMORY-GUARD] {state['decision']} before={state['memory_before']} "
            f"after={state['memory_after']} closed={len(state['closed_tabs'])}"
        )


if __name__ == "__main__":
    main()
