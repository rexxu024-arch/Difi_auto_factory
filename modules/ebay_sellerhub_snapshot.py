import argparse
import asyncio
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import websockets

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
PERFORMANCE_LOG = DATABASE_DIR / "Performance_Log.csv"
ACTIVE_URL = "https://www.ebay.com/sh/lst/active"

HEADERS = [
    "Snapshot_Timestamp",
    "Platform",
    "Item_ID",
    "Title",
    "Price",
    "Views_30_Days",
    "General_Status",
    "Priority_Status",
    "Suggested_Ad_Rate",
    "Source_URL",
    "Read_Status",
]


def _now():
    try:
        return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")
    except Exception:
        return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _http_json(url, method="GET"):
    request = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


async def _send(ws, seq_state, method, params=None):
    seq_state["seq"] += 1
    message = {"id": seq_state["seq"], "method": method}
    if params is not None:
        message["params"] = params
    await ws.send(json.dumps(message))
    while True:
        data = json.loads(await ws.recv())
        if data.get("id") == message["id"]:
            return data


async def _read_active_text(cdp_port=9222, scrolls=0):
    encoded = urllib.parse.quote(ACTIVE_URL, safe=":/?&=%")
    created_or_reused_page = {}
    try:
        page = _http_json(f"http://127.0.0.1:{cdp_port}/json/new?{encoded}", method="PUT")
        created_or_reused_page = page
    except Exception:
        pages = _http_json(f"http://127.0.0.1:{cdp_port}/json/list")
        page = next((item for item in pages if item.get("type") == "page"), pages[0])
        created_or_reused_page = {}
    ws_url = page["webSocketDebuggerUrl"]
    try:
        async with websockets.connect(ws_url, max_size=30_000_000) as ws:
            state = {"seq": 0}
            await _send(ws, state, "Page.enable")
            await _send(ws, state, "Runtime.enable")
            await _send(ws, state, "Page.navigate", {"url": ACTIVE_URL})
            for _ in range(15):
                await asyncio.sleep(1)
                ready = await _send(
                    ws,
                    state,
                    "Runtime.evaluate",
                    {"expression": "document.readyState", "returnByValue": True},
                )
                value = ready.get("result", {}).get("result", {}).get("value")
                if value == "complete":
                    break
            await asyncio.sleep(4)
            for _ in range(max(0, scrolls)):
                await _send(
                    ws,
                    state,
                    "Runtime.evaluate",
                    {
                        "expression": "window.scrollBy(0, Math.floor(window.innerHeight * 0.85)); undefined",
                        "returnByValue": True,
                    },
                )
                await asyncio.sleep(2)
            result = await _send(
                ws,
                state,
                "Runtime.evaluate",
                {
                    "expression": "({url: location.href, title: document.title, text: document.body ? document.body.innerText : ''})",
                    "returnByValue": True,
                },
            )
            return result.get("result", {}).get("result", {}).get("value") or {}
    finally:
        page_id = created_or_reused_page.get("id")
        if page_id:
            try:
                _http_json(f"http://127.0.0.1:{cdp_port}/json/close/{page_id}")
            except Exception:
                pass


def _parse_rows(page):
    text = page.get("text") or ""
    url = page.get("url") or ACTIVE_URL
    title = page.get("title") or ""
    if re.search(r"Service Unavailable|Zero size object|errors\.edgesuite\.net|Reference #", text + " " + url + " " + title, re.I):
        return [], "EDGE_ERROR"
    if re.search(r"Sign in|Password|Email or username", text, re.I):
        return [], "LOGIN_OR_AUTH"
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    rows = []
    for index, line in enumerate(lines):
        match = re.search(r"Buy It Now\s*[·-]\s*(\d{9,})", line)
        if not match:
            continue
        item_id = match.group(1)
        title_line = ""
        for back in range(index - 1, max(index - 8, -1), -1):
            candidate = lines[back]
            if not candidate.startswith("Link.") and "Show Listing Details" not in candidate and "variation" not in candidate.lower():
                title_line = candidate
                break
        price = ""
        views = ""
        general = ""
        priority = ""
        suggested = ""
        for forward in range(index + 1, min(index + 18, len(lines))):
            candidate = lines[forward]
            if not price and candidate.startswith("$"):
                price = candidate
            view_match = re.search(r"Views?\s+(\d+)", candidate, re.I)
            if view_match and not views:
                views = view_match.group(1)
            if candidate.startswith("General:"):
                general = candidate.replace("General:", "").strip()
            if candidate.startswith("Priority:"):
                priority = candidate.replace("Priority:", "").strip()
            if candidate.startswith("Suggested ad rate:"):
                suggested = candidate.replace("Suggested ad rate:", "").strip()
        rows.append(
            {
                "Snapshot_Timestamp": _now(),
                "Platform": "eBay",
                "Item_ID": item_id,
                "Title": title_line,
                "Price": price,
                "Views_30_Days": views,
                "General_Status": general,
                "Priority_Status": priority,
                "Suggested_Ad_Rate": suggested,
                "Source_URL": url,
                "Read_Status": "OK",
            }
        )
    return rows, "OK"


def _append_log(rows):
    PERFORMANCE_LOG.parent.mkdir(exist_ok=True)
    exists = PERFORMANCE_LOG.exists()
    with PERFORMANCE_LOG.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def run(cdp_port=9222, scrolls=0, dry_run=False):
    page = asyncio.run(_read_active_text(cdp_port=cdp_port, scrolls=scrolls))
    rows, status = _parse_rows(page)
    if status != "OK":
        print(f"[EBAY-SNAPSHOT] read_status={status}; entering quiet no-write mode")
        return []
    if not dry_run:
        _append_log(rows)
    zero_views = sum(1 for row in rows if str(row.get("Views_30_Days")) == "0")
    one_plus = sum(1 for row in rows if str(row.get("Views_30_Days")).isdigit() and int(row["Views_30_Days"]) > 0)
    promoted = sum(1 for row in rows if row.get("General_Status") == "Promoted")
    print(
        f"[EBAY-SNAPSHOT] rows={len(rows)} zero_views={zero_views} one_plus_views={one_plus} promoted={promoted} dry_run={dry_run}"
    )
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp-port", type=int, default=9222)
    parser.add_argument("--scrolls", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(cdp_port=args.cdp_port, scrolls=args.scrolls, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
