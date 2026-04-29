import argparse
import asyncio
import json
import sys
import time
import urllib.request
from pathlib import Path

import requests
import websockets
from openpyxl import load_workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules import printify_uploader
from modules.printify_mockup_ui_uploader import _assets, _fetch_product, _selected_count, _upload_mockups


EBAY_BOOK = PROJECT_ROOT / "Database" / "eBay_listing.xlsx"
CHROME_DEBUG_URL = "http://127.0.0.1:9222"


class PrintifyLoginRequired(RuntimeError):
    pass


def _assert_printify_ui_logged_in():
    try:
        with urllib.request.urlopen(f"{CHROME_DEBUG_URL}/json/list", timeout=10) as response:
            pages = json.load(response)
    except Exception as exc:
        raise PrintifyLoginRequired(f"Printify browser control is unavailable: {exc}") from exc
    printify_pages = [page for page in pages if "printify.com/app" in page.get("url", "")]
    if not printify_pages:
        raise PrintifyLoginRequired("Open and log in to Printify in the Codex browser before UI mockup upload.")
    if any("/auth/login" in page.get("url", "") for page in printify_pages):
        raise PrintifyLoginRequired("Printify login required in Codex browser; stopping before creating more products.")


def _open_product_tab(product_id):
    url = f"https://printify.com/app/mockup-library/shops/{Config.Printify_SHOP_ID}/products/{product_id}?revealUploads=true"
    with urllib.request.urlopen(f"{CHROME_DEBUG_URL}/json/list", timeout=10) as response:
        pages = json.load(response)
    tab = next((page for page in pages if product_id in page.get("url", "") and page.get("webSocketDebuggerUrl")), None)
    if not tab:
        tab = next(
            (page for page in pages if "printify.com/app/" in page.get("url", "") and page.get("webSocketDebuggerUrl")),
            None,
        )
    if not tab:
        req = urllib.request.Request(f"{CHROME_DEBUG_URL}/json/new", data=url.encode("utf-8"), method="PUT")
        tab = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8", "ignore"))
    if tab.get("webSocketDebuggerUrl"):
        async def navigate():
            async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=20_000_000) as sock:
                seq = 1
                async def send(method, params=None):
                    nonlocal seq
                    msg = {"id": seq, "method": method}
                    if params is not None:
                        msg["params"] = params
                    await sock.send(json.dumps(msg))
                    my_id = seq
                    seq += 1
                    while True:
                        data = json.loads(await sock.recv())
                        if data.get("id") == my_id:
                            return data
                await send("Page.enable")
                await send("Page.navigate", {"url": url})
        asyncio.run(navigate())
    time.sleep(8)


def _headers():
    return {"Authorization": f"Bearer {Config.Printify_API_KEY}", "Content-Type": "application/json"}


def _ensure_product_id(row):
    existing = str(row.get("Printify_Product_ID") or "").strip()
    if existing:
        return existing
    production_path, stock_paths, missing = printify_uploader._validate_row_assets(row)
    if missing:
        raise RuntimeError("; ".join(missing))
    version = str(int(time.time()))
    production_id = printify_uploader._image_upload(production_path, f"{row['ID']}_Production_{version}.png")
    stock_ids = [printify_uploader._image_upload(path, f"{row['ID']}_{label}_{version}.png") for label, path in stock_paths]
    payload = printify_uploader._build_payload(row, stock_ids, production_id)
    response = requests.post(
        f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products.json",
        headers=_headers(),
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["id"]


def _load_workbook_rows(limit):
    wb = load_workbook(EBAY_BOOK)
    ws = wb.active
    headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    if "Printify_Product_ID" not in headers:
        ws.cell(1, ws.max_column + 1).value = "Printify_Product_ID"
        headers.append("Printify_Product_ID")
    cols = {header: idx + 1 for idx, header in enumerate(headers)}
    rows = []
    eligible = {"Ready_for_Printify", "Printify_BaseStaged_DefaultMockups3", "Printify_PhotoMismatch", "Printify_UI_Failed", "Printify_PrimaryFix_Needed"}
    for row_idx in range(2, ws.max_row + 1):
        row = {header: ws.cell(row_idx, cols[header]).value for header in headers}
        row["_row_idx"] = row_idx
        if row.get("Status") in eligible:
            rows.append(row)
            if limit and len(rows) >= limit:
                break
    return wb, ws, headers, cols, rows


def _set_cell(ws, cols, row_idx, name, value):
    if name not in cols:
        ws.cell(1, ws.max_column + 1).value = name
        cols[name] = ws.max_column
    ws.cell(row_idx, cols[name]).value = value


def run(limit=0, batch_size=75, batch_delay=3600, publish=False):
    wb, ws, headers, cols, rows = _load_workbook_rows(limit)
    completed = 0
    try:
        for row in rows:
            item_id = row["ID"]
            row_idx = row["_row_idx"]
            try:
                _assert_printify_ui_logged_in()
                product_id = _ensure_product_id(row)
                _set_cell(ws, cols, row_idx, "Printify_Product_ID", product_id)
                _set_cell(ws, cols, row_idx, "Status", "Printify_BaseStaged_DefaultMockups3")
                wb.save(EBAY_BOOK)

                _open_product_tab(product_id)
                asyncio.run(
                    _upload_mockups(
                        product_id,
                        _assets({**row, "Printify_Product_ID": product_id}),
                        publish=publish,
                        product_type=row.get("Product_Type") or "Sticker",
                    )
                )
                product = _fetch_product(product_id)
                count = _selected_count(product)
                if count != 5:
                    raise RuntimeError(f"selected mockups={count}, expected 5")
                _set_cell(
                    ws,
                    cols,
                    row_idx,
                    "Status",
                    "Printify_Published_Mockups5" if publish else "Printify_UI_Mockups5",
                )
                wb.save(EBAY_BOOK)
                completed += 1
                print(f"[FULL-PIPELINE] {completed}/{len(rows)} {item_id} product={product_id} selected_mockups=5")
                if batch_size and completed % batch_size == 0 and completed < len(rows):
                    print(f"[BATCH-COOLDOWN] {completed}/{len(rows)} sleeping {batch_delay}s")
                    time.sleep(batch_delay)
            except PrintifyLoginRequired as exc:
                print(f"[FULL-PIPELINE-PAUSED] {item_id}: {exc}")
                break
            except Exception as exc:
                _set_cell(ws, cols, row_idx, "Status", "Printify_UI_Failed")
                wb.save(EBAY_BOOK)
                print(f"[FULL-PIPELINE-FAIL] {item_id}: {exc}")
                continue
    finally:
        wb.close()
    print(f"[DONE] Full Printify pipeline completed: {completed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=75)
    parser.add_argument("--batch-delay", type=int, default=3600)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    run(limit=args.limit, batch_size=args.batch_size, batch_delay=args.batch_delay, publish=args.publish)
