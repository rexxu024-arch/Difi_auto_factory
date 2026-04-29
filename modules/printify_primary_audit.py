import argparse
import io
import sys
from pathlib import Path

import requests
from openpyxl import load_workbook
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config

EBAY_BOOK = PROJECT_ROOT / "Database" / "eBay_listing.xlsx"
FIX_STATUS = "Printify_PrimaryFix_Needed"


def _headers():
    return {"Authorization": f"Bearer {Config.Printify_API_KEY}"}


def _ahash(image):
    image = image.convert("L").resize((16, 16), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if pixel > avg else "0" for pixel in pixels)


def _distance(a, b):
    return sum(left != right for left, right in zip(a, b))


def _fetch_product(product_id):
    response = requests.get(
        f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products/{product_id}.json",
        headers=_headers(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _remote_hash(url):
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return _ahash(Image.open(io.BytesIO(response.content)))


def _default_matches_cover(product_id, cover_path, threshold=8):
    product = _fetch_product(product_id)
    images = product.get("images") or []
    if len(images) != 5:
        return False, f"selected image count is {len(images)}"
    default = next((image for image in images if image.get("is_default")), images[0])
    cover_hash = _ahash(Image.open(cover_path))
    default_hash = _remote_hash(default["src"])
    distance = _distance(cover_hash, default_hash)
    return distance <= threshold, f"default-cover distance={distance}"


def audit_and_mark(limit=0):
    wb = load_workbook(EBAY_BOOK)
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    cols = {header: index + 1 for index, header in enumerate(headers)}
    checked = 0
    fixes = 0
    try:
        for row in range(2, ws.max_row + 1):
            status = ws.cell(row, cols["Status"]).value
            if status not in {"Printify_UI_Mockups5", "Printify_Published_Mockups5", FIX_STATUS}:
                continue
            product_id = ws.cell(row, cols["Printify_Product_ID"]).value
            cover_path = ws.cell(row, cols["Cover_Path"]).value
            item_id = ws.cell(row, cols["ID"]).value
            if not product_id or not cover_path or not Path(cover_path).exists():
                continue
            checked += 1
            ok, note = _default_matches_cover(str(product_id), cover_path)
            if ok:
                if status != "Printify_Published_Mockups5":
                    ws.cell(row, cols["Status"]).value = "Printify_UI_Mockups5"
                print(f"[PRIMARY-OK] {item_id} {note}")
            else:
                ws.cell(row, cols["Status"]).value = FIX_STATUS
                fixes += 1
                print(f"[PRIMARY-FIX] {item_id} {note}")
            wb.save(EBAY_BOOK)
            if limit and checked >= limit:
                break
    finally:
        wb.close()
    print(f"[DONE] primary audit checked={checked} fixes={fixes}")
    return fixes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    audit_and_mark(limit=args.limit)
