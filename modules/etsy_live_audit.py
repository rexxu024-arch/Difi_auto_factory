"""Audit live Etsy listing pages from the staged OpenClaw digital queue."""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

import websockets

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.automation_browser import DEFAULT_PROFILE, cdp_status, launch

DATABASE = PROJECT_ROOT / "Database"
QUEUE_PATH = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
AUDIT_PATH = DATABASE / "Etsy_Digital_Live_Audit.csv"

FIELDS = [
    "Timestamp",
    "ID",
    "Etsy_Listing_ID",
    "URL",
    "Status",
    "Title",
    "Price_Text",
    "Digital_Signal",
    "Image_Count",
    "Notes",
]


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _append_rows(rows: list[dict]) -> None:
    exists = AUDIT_PATH.exists()
    with AUDIT_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def _published_candidates(limit: int, ids: set[str] | None = None) -> list[dict]:
    rows = []
    for row in _read_rows(QUEUE_PATH):
        listing_id = str(row.get("Etsy_Listing_ID") or "").strip()
        item_id = str(row.get("ID") or "").strip()
        if not listing_id:
            continue
        if ids and item_id not in ids and listing_id not in ids:
            continue
        rows.append(row)
        if len(rows) >= limit:
            break
    return rows


def _http_text(url: str, method: str = "GET") -> str:
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode("utf-8", errors="replace")


def _http_json(url: str, method: str = "GET") -> dict:
    return json.loads(_http_text(url, method=method))


def _ensure_edge_cdp(port: int) -> None:
    status = cdp_status(port)
    if status.get("status") == "RUNNING":
        return
    launch("edge", port, DEFAULT_PROFILE, "about:blank", minimized=False)


def _new_target(port: int, url: str) -> dict:
    encoded = urllib.parse.quote(url, safe=":/?=&")
    return _http_json(f"http://127.0.0.1:{port}/json/new?{encoded}", method="PUT")


def _close_target(port: int, target_id: str | None) -> None:
    if not target_id:
        return
    try:
        _http_text(f"http://127.0.0.1:{port}/json/close/{target_id}")
    except Exception:
        pass


async def _cdp_eval(ws, seq_state: dict[str, int], method: str, params: dict | None = None) -> dict:
    seq_state["seq"] += 1
    message = {"id": seq_state["seq"], "method": method}
    if params is not None:
        message["params"] = params
    await ws.send(json.dumps(message))
    while True:
        data = json.loads(await ws.recv())
        if data.get("id") == seq_state["seq"]:
            return data


async def audit_listing(row: dict, port: int) -> dict:
    listing_id = str(row.get("Etsy_Listing_ID") or "").strip()
    item_id = str(row.get("ID") or "").strip()
    url = f"https://www.etsy.com/listing/{listing_id}"
    result = {
        "Timestamp": _now(),
        "ID": item_id,
        "Etsy_Listing_ID": listing_id,
        "URL": url,
        "Status": "ERROR",
        "Title": "",
        "Price_Text": "",
        "Digital_Signal": "UNKNOWN",
        "Image_Count": "",
        "Notes": "",
    }
    target = None
    try:
        _ensure_edge_cdp(port)
        target = _new_target(port, url)
        seq_state = {"seq": 0}
        async with websockets.connect(target["webSocketDebuggerUrl"], max_size=20_000_000) as ws:
            await _cdp_eval(ws, seq_state, "Page.enable")
            await _cdp_eval(ws, seq_state, "Runtime.enable")
            for _ in range(35):
                state = await _cdp_eval(
                    ws,
                    seq_state,
                    "Runtime.evaluate",
                    {
                        "expression": r"""(() => ({
                            ready: document.readyState,
                            textLength: ((document.body && document.body.innerText) || '').length
                        }))()""",
                        "returnByValue": True,
                    },
                )
                value = state.get("result", {}).get("result", {}).get("value") or {}
                if value.get("ready") in {"interactive", "complete"} and int(value.get("textLength") or 0) > 200:
                    break
                await asyncio.sleep(0.5)
            await asyncio.sleep(2.5)
            payload = await _cdp_eval(
                ws,
                seq_state,
                "Runtime.evaluate",
                {
                    "expression": r"""(() => ({
                        title: (document.querySelector('h1')?.innerText || document.querySelector("[data-buy-box-region='title']")?.innerText || '').replace(/\s+/g,' ').trim(),
                        body: ((document.body && document.body.innerText) || '').slice(0, 20000),
                        imageCount: document.querySelectorAll('img').length
                    }))()""",
                    "returnByValue": True,
                },
            )
        value = payload.get("result", {}).get("result", {}).get("value") or {}
        body = str(value.get("body") or "")
        lower = body.lower()
        if "this listing is no longer available" in lower or "listing is unavailable" in lower:
            result["Status"] = "NOT_ACTIVE"
        elif "etsy" in lower and (item_id.lower() in lower or "digital" in lower or "download" in lower):
            result["Status"] = "ACTIVE_READABLE"
        else:
            result["Status"] = "READABLE_UNCERTAIN"

        title = str(value.get("title") or "").strip()
        result["Title"] = re.sub(r"\s+", " ", title)[:240]

        price = ""
        try:
            price_candidates = re.findall(r"(?:US\s*)?\$[0-9]+(?:\.[0-9]{2})?", body)
            if price_candidates:
                price = price_candidates[0]
        except Exception:
            pass
        result["Price_Text"] = price
        result["Digital_Signal"] = "YES" if ("digital download" in lower or "instant download" in lower or "download files" in lower) else "NO"
        result["Image_Count"] = str(value.get("imageCount") or "")
    except Exception as exc:  # noqa: BLE001
        result["Status"] = "ERROR"
        result["Notes"] = str(exc)[:240]
    finally:
        if target:
            _close_target(port, target.get("id"))
    return result


async def run_async(limit: int, ids: set[str] | None, port: int) -> list[dict]:
    candidates = _published_candidates(limit, ids)
    if not candidates:
        print("[etsy-live-audit] no published candidates")
        return []
    results: list[dict] = []
    for row in candidates:
        try:
            result = await asyncio.wait_for(audit_listing(row, port), timeout=35)
        except TimeoutError:
            listing_id = str(row.get("Etsy_Listing_ID") or "").strip()
            item_id = str(row.get("ID") or "").strip()
            result = {
                "Timestamp": _now(),
                "ID": item_id,
                "Etsy_Listing_ID": listing_id,
                "URL": f"https://www.etsy.com/listing/{listing_id}",
                "Status": "TIMEOUT_SKIPPED",
                "Title": "",
                "Price_Text": "",
                "Digital_Signal": "UNKNOWN",
                "Image_Count": "",
                "Notes": "Per-listing audit exceeded 35 seconds; skipped to protect loop continuity.",
            }
        results.append(result)
        print(f"[etsy-live-audit] {result['ID']} {result['Etsy_Listing_ID']} {result['Status']} {result['Digital_Signal']}")
        await asyncio.sleep(0.7)
    _append_rows(results)
    return results


def run(limit: int, ids: set[str] | None, port: int) -> list[dict]:
    return asyncio.run(run_async(limit, ids, port))


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit live Etsy public listing pages.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--ids", default="", help="Comma-separated local IDs or Etsy listing IDs.")
    parser.add_argument("--port", type=int, default=9223)
    parser.add_argument("--keep-tabs", action="store_true", help="Deprecated; CDP mode always closes audit tabs.")
    args = parser.parse_args()
    ids = {part.strip() for part in args.ids.split(",") if part.strip()} or None
    run(args.limit, ids, args.port)


if __name__ == "__main__":
    main()
