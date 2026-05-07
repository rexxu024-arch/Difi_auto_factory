from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import random
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

import websockets

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATABASE_DIR = PROJECT_ROOT / "Database"
PIVOT_CSV = DATABASE_DIR / "eBay_Quiet_Jade_Pivot.csv"
LOG_CSV = DATABASE_DIR / "eBay_UI_Title_Revise_Log.csv"
CDP_PORT = int(os.getenv("OPENCLAW_EBAY_CDP_PORT") or os.getenv("OPENCLAW_CDP_PORT") or "9223")


def now_text() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def clean(value: Any) -> str:
    return str(value or "").replace("\n", " ").replace("\r", " ").strip()


def http_json(url: str, method: str = "GET") -> dict[str, Any]:
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.load(response)


def new_tab(port: int, url: str) -> dict[str, Any]:
    encoded = urllib.parse.quote(url, safe=":/?=&%")
    return http_json(f"http://127.0.0.1:{port}/json/new?{encoded}", method="PUT")


def close_tab(port: int, tab_id: str) -> None:
    if not tab_id:
        return
    try:
        http_json(f"http://127.0.0.1:{port}/json/close/{tab_id}")
    except Exception:
        pass


async def send(ws, state: dict[str, int], method: str, params: dict | None = None) -> dict[str, Any]:
    state["seq"] += 1
    msg = {"id": state["seq"], "method": method}
    if params is not None:
        msg["params"] = params
    await ws.send(json.dumps(msg))
    while True:
        data = json.loads(await ws.recv())
        if data.get("id") == msg["id"]:
            return data


async def eval_js(ws, state: dict[str, int], expression: str) -> Any:
    result = await send(ws, state, "Runtime.evaluate", {"expression": expression, "returnByValue": True})
    return result.get("result", {}).get("result", {}).get("value")


async def wait_for_ready(ws, state: dict[str, int], timeout: int = 45) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        value = await eval_js(ws, state, "document.readyState")
        if value == "complete":
            return
        await asyncio.sleep(1)


def load_plan(ids: set[str] | None = None, limit: int = 0) -> list[dict[str, str]]:
    rows = list(csv.DictReader(PIVOT_CSV.open("r", encoding="utf-8-sig", newline=""))) if PIVOT_CSV.exists() else []
    selected = []
    for row in rows:
        if ids and row.get("ID") not in ids and row.get("eBay_Item_ID") not in ids:
            continue
        if not clean(row.get("eBay_Item_ID")) or not clean(row.get("New_Title")):
            continue
        selected.append(row)
        if limit and len(selected) >= limit:
            break
    return selected


def append_log(row: dict[str, Any]) -> None:
    headers = [
        "Timestamp",
        "ID",
        "eBay_Item_ID",
        "Action",
        "Old_Title_UI",
        "Target_Title",
        "Result",
        "Detail",
    ]
    exists = LOG_CSV.exists()
    with LOG_CSV.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in headers})


async def type_text(ws, state: dict[str, int], text: str, min_delay: float, max_delay: float) -> None:
    await send(ws, state, "Input.dispatchKeyEvent", {"type": "keyDown", "modifiers": 2, "windowsVirtualKeyCode": 65, "code": "KeyA", "key": "a"})
    await send(ws, state, "Input.dispatchKeyEvent", {"type": "keyUp", "modifiers": 2, "windowsVirtualKeyCode": 65, "code": "KeyA", "key": "a"})
    await send(ws, state, "Input.dispatchKeyEvent", {"type": "keyDown", "windowsVirtualKeyCode": 8, "code": "Backspace", "key": "Backspace"})
    await send(ws, state, "Input.dispatchKeyEvent", {"type": "keyUp", "windowsVirtualKeyCode": 8, "code": "Backspace", "key": "Backspace"})
    for ch in text:
        await send(ws, state, "Input.insertText", {"text": ch})
        await asyncio.sleep(random.uniform(min_delay, max_delay))


async def revise_one(
    row: dict[str, str],
    port: int,
    dry_run: bool = False,
    min_delay: float = 0.02,
    max_delay: float = 0.07,
    submit_matching: bool = False,
) -> tuple[str, str, str]:
    item_id = clean(row.get("eBay_Item_ID"))
    target = clean(row.get("New_Title"))
    url = (
        f"https://www.ebay.com/sl/list?mode=ReviseItem&itemId={item_id}"
        f"&ReturnURL=https%3A%2F%2Fwww.ebay.com%2Fsh%2Flst%2Factive%3Fkeyword%3D{item_id}"
    )
    tab = new_tab(port, url)
    tab_id = tab.get("id", "")
    try:
        async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=30_000_000) as ws:
            state = {"seq": 0}
            await send(ws, state, "Page.enable")
            await send(ws, state, "Runtime.enable")
            await send(ws, state, "Page.navigate", {"url": url})
            await wait_for_ready(ws, state)
            await asyncio.sleep(random.uniform(5, 8))
            page = await eval_js(
                ws,
                state,
                r"""(() => ({
                    url: location.href,
                    title: document.title,
                    text: document.body ? document.body.innerText.slice(0, 3500) : '',
                    titleValue: (document.querySelector('input[name="title"]') || {}).value || ''
                }))()""",
            )
            text = page.get("text") or ""
            if "Sign in" in text[:1200] or "signin.ebay.com" in (page.get("url") or ""):
                return "LOGIN_REQUIRED", clean(page.get("titleValue")), "Seller Hub revise page requires login."
            old_title = clean(page.get("titleValue"))
            if not old_title:
                return "TITLE_INPUT_MISSING", "", (page.get("title") or "")[:300]
            if old_title == target and not submit_matching:
                return "ALREADY_MATCHED", old_title, "Revise UI already has target title."
            if dry_run:
                return "DRY_RUN_WOULD_REVISE", old_title, target
            if old_title != target:
                focused = await eval_js(
                    ws,
                    state,
                    r"""(() => {
                        const input=document.querySelector('input[name="title"]');
                        if (!input) return false;
                        input.scrollIntoView({block:'center'});
                        input.focus();
                        input.select();
                        return true;
                    })()""",
                )
                if not focused:
                    return "FAILED_FOCUS_TITLE", old_title, "title input focus failed"
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await type_text(ws, state, target, min_delay, max_delay)
                value = await eval_js(
                    ws,
                    state,
                    r"""(() => {
                        const input=document.querySelector('input[name="title"]');
                        if (!input) return '';
                        input.dispatchEvent(new Event('input', {bubbles:true}));
                        input.dispatchEvent(new Event('change', {bubbles:true}));
                        return input.value;
                    })()""",
                )
                if clean(value) != target:
                    return "FAILED_SET_TITLE", old_title, f"value after typing={clean(value)}"
            await eval_js(ws, state, "window.scrollTo({top: Math.floor(document.body.scrollHeight * 0.82), behavior:'smooth'}); true")
            await asyncio.sleep(random.uniform(1.5, 3.0))
            button_info = await eval_js(
                ws,
                state,
                r"""(() => {
                    const buttons=[...document.querySelectorAll('button')].filter(btn => (btn.innerText || '').trim() === 'Revise it' && !!(btn.offsetWidth || btn.offsetHeight || btn.getClientRects().length));
                    if (!buttons.length) return null;
                    const btn=buttons[buttons.length - 1];
                    btn.scrollIntoView({block:'center'});
                    const r=btn.getBoundingClientRect();
                    return {x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2), disabled: !!btn.disabled, text: (btn.innerText || '').trim()};
                })()""",
            )
            if not button_info:
                return "FAILED_CLICK_REVISE", old_title, "Revise it button not found"
            await asyncio.sleep(random.uniform(0.5, 1.2))
            await send(ws, state, "Input.dispatchMouseEvent", {"type": "mouseMoved", "x": button_info["x"], "y": button_info["y"]})
            await send(ws, state, "Input.dispatchMouseEvent", {"type": "mousePressed", "x": button_info["x"], "y": button_info["y"], "button": "left", "clickCount": 1})
            await asyncio.sleep(random.uniform(0.05, 0.18))
            await send(ws, state, "Input.dispatchMouseEvent", {"type": "mouseReleased", "x": button_info["x"], "y": button_info["y"], "button": "left", "clickCount": 1})
            await asyncio.sleep(random.uniform(9, 14))
            final = await eval_js(
                ws,
                state,
                r"""(() => ({
                    url: location.href,
                    title: document.title,
                    text: document.body ? document.body.innerText.slice(0, 5000) : ''
                }))()""",
            )
            final_text = final.get("text") or ""
            final_title = final.get("title") or ""
            final_url = final.get("url") or ""
            if "Listing revised" in final_text or "successfully revised" in final_text or "active?keyword" in final_url:
                return "REVISED_SUBMITTED", old_title, clean(final_title)[:300]
            if "fix" in final_text.lower() and "error" in final_text.lower():
                return "REVISE_ERROR_PAGE", old_title, clean(final_text)[:500]
            return "REVISE_SUBMITTED_UNCONFIRMED", old_title, clean(final_title or final_text)[:500]
    finally:
        close_tab(port, tab_id)


async def run(
    rows: list[dict[str, str]],
    port: int,
    dry_run: bool,
    min_delay: float,
    max_delay: float,
    between_min: float,
    between_max: float,
    submit_matching: bool,
) -> None:
    for row in rows:
        try:
            result, old_title, detail = await asyncio.wait_for(
                revise_one(
                    row,
                    port=port,
                    dry_run=dry_run,
                    min_delay=min_delay,
                    max_delay=max_delay,
                    submit_matching=submit_matching,
                ),
                timeout=120,
            )
        except Exception as exc:  # noqa: BLE001
            result, old_title, detail = "ERROR", "", f"{type(exc).__name__}: {exc}"
        append_log(
            {
                "Timestamp": now_text(),
                "ID": clean(row.get("ID")),
                "eBay_Item_ID": clean(row.get("eBay_Item_ID")),
                "Action": "TITLE_REVISE_ONLY",
                "Old_Title_UI": old_title,
                "Target_Title": clean(row.get("New_Title")),
                "Result": result,
                "Detail": detail,
            }
        )
        print(f"[EBAY-UI-TITLE] {row.get('ID')} {result}")
        await asyncio.sleep(random.uniform(between_min, between_max))


def main() -> None:
    parser = argparse.ArgumentParser(description="Narrow eBay Seller Hub title-only revise helper.")
    parser.add_argument("--ids", default="", help="Comma-separated local IDs or eBay item IDs. Empty means all pivot rows.")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--cdp-port", type=int, default=CDP_PORT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--min-delay", type=float, default=0.02)
    parser.add_argument("--max-delay", type=float, default=0.07)
    parser.add_argument("--between-min", type=float, default=4.0)
    parser.add_argument("--between-max", type=float, default=9.0)
    parser.add_argument("--submit-matching", action="store_true", help="Click Revise it even when the edit form already shows the target title.")
    args = parser.parse_args()
    ids = {item.strip() for item in args.ids.split(",") if item.strip()} or None
    rows = load_plan(ids=ids, limit=args.limit)
    asyncio.run(
        run(
            rows,
            port=args.cdp_port,
            dry_run=args.dry_run,
            min_delay=args.min_delay,
            max_delay=max(args.min_delay, args.max_delay),
            between_min=args.between_min,
            between_max=max(args.between_min, args.between_max),
            submit_matching=args.submit_matching,
        )
    )


if __name__ == "__main__":
    main()
