"""Repair Printify mockup-library source selections before touching eBay.

Some eBay listings show repeated gallery images even when the Printify mockup
library currently shows a clean selection. Printify's eBay integration can lag,
so this script first re-saves the source mockup selection in Printify and only
then optionally asks Printify to republish images to the sales channel.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import io
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.automation_browser import DEFAULT_PROFILE, cdp_status, launch
from modules.printify_gallery_duplicate_audit import audit_row, workbook_rows
from modules.printify_mockup_ui_uploader import CdpPage, _target_ws


DATABASE_DIR = PROJECT_ROOT / "Database"
REPAIR_QUEUE = DATABASE_DIR / "Printify_Gallery_Repair_Queue.csv"
OUT_CSV = DATABASE_DIR / "Printify_Gallery_Source_Repair_Log.csv"
CDP_PORT = int(os.getenv("OPENCLAW_PRINTIFY_CDP_PORT") or os.getenv("OPENCLAW_CDP_PORT") or "9223")


def clean(value: object) -> str:
    return str(value or "").strip()


def ahash(image: Image.Image) -> str:
    image = image.convert("L").resize((16, 16), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if pixel > avg else "0" for pixel in pixels)


def hash_distance(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right))


def best_cover_candidate(candidates: list[dict], cover_path: str) -> dict | None:
    if not cover_path or not Path(cover_path).exists():
        return candidates[0] if candidates else None
    local_hash = ahash(Image.open(cover_path))
    scored = []
    for candidate in candidates:
        src = clean(candidate.get("src"))
        if not src:
            continue
        try:
            response = requests.get(src, timeout=30)
            response.raise_for_status()
            remote_hash = ahash(Image.open(io.BytesIO(response.content)))
            scored.append((hash_distance(local_hash, remote_hash), candidate))
        except Exception:
            continue
    if not scored:
        return candidates[0] if candidates else None
    scored.sort(key=lambda item: item[0])
    best_score, best = scored[0]
    best["Cover_Distance"] = str(best_score)
    return best


def read_repair_queue() -> list[dict[str, str]]:
    if not REPAIR_QUEUE.exists():
        return []
    with REPAIR_QUEUE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {Config.Printify_API_KEY}",
        "Content-Type": "application/json",
    }


def publish_images(product_id: str) -> int:
    response = requests.post(
        f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products/{product_id}/publish.json",
        headers=headers(),
        json={
            "title": False,
            "description": False,
            "images": True,
            "variants": False,
            "tags": False,
            "keyFeatures": False,
            "shipping_template": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.status_code


def api_gallery_mix(product_id: str) -> dict[str, str]:
    response = requests.get(
        f"{Config.Printify_API_URL.rstrip('/')}/shops/{Config.Printify_SHOP_ID}/products/{product_id}.json",
        headers={"Authorization": f"Bearer {Config.Printify_API_KEY}"},
        timeout=180,
    )
    response.raise_for_status()
    images = response.json().get("images") or []
    official = 0
    custom = 0
    other = 0
    for image in images:
        src = clean(image.get("src"))
        if "images.printify.com/mockup/" in src:
            official += 1
        elif "pfy-prod-products-mockup-media" in src:
            custom += 1
        else:
            other += 1
    return {
        "Api_Image_Count": str(len(images)),
        "Api_Official_Count": str(official),
        "Api_Custom_Count": str(custom),
        "Api_Other_Count": str(other),
    }


def ensure_edge_cdp() -> None:
    status = cdp_status(CDP_PORT)
    if status.get("status") == "RUNNING":
        return
    launch("edge", CDP_PORT, DEFAULT_PROFILE, "about:blank", minimized=False)


def is_cdp_connection_error(exc: Exception) -> bool:
    text = str(exc)
    return "WinError 10061" in text or "Connection refused" in text or "actively refused" in text


async def resave_current_selection(product_id: str, wait_seconds: int = 10) -> dict[str, str]:
    ensure_edge_cdp()
    ws_url = _target_ws(product_id)
    async with CdpPage(ws_url) as page:
        await page.navigate(
            f"https://printify.com/app/mockup-library/shops/{Config.Printify_SHOP_ID}/products/{product_id}?revealUploads=true"
        )
        for _ in range(35):
            if await page.eval("!!location.href && /\\/auth\\/login/.test(location.href)"):
                raise RuntimeError("Printify login required in Edge project browser")
            if await page.eval("!!document.body && /Mockup library/.test(document.body.innerText || '')"):
                break
            await asyncio.sleep(1)
        state = await page.eval(
            r"""(() => {
                const text = (document.body && document.body.innerText) || '';
                const selected = ((text.match(/(\d+)\s+selected/) || [])[1] || '').trim();
                const variant = ((text.match(/([^\n]+)\s+\(\d+\/\d+\)/) || [])[1] || '').trim();
                const selectedItems = [...document.querySelectorAll('button.mockup-container,.mockup-container')]
                  .filter(e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length))
                  .filter(e => {
                    const ctrl = e.querySelector('[data-testid="checkboxWrapper"], [role="checkbox"], input[type="checkbox"]');
                    return (e.innerText || '').includes('check') || (ctrl && (ctrl.checked || ctrl.getAttribute('aria-checked') === 'true'));
                  }).length;
                return {selected, variant, selectedItems, text: text.slice(0, 1000)};
            })()"""
        )
        saved = await page.eval(
            r"""(() => {
                const visible = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
                const button = [...document.querySelectorAll('button')]
                  .filter(visible)
                  .find(e => (e.innerText || '').trim() === 'Save selection' && !e.disabled);
                if (!button) return false;
                button.click();
                return true;
            })()"""
        )
        if not saved:
            raise RuntimeError("Save selection button not found or disabled")
        await asyncio.sleep(wait_seconds)
        return {
            "UI_Selected_Text": clean(state.get("selected")),
            "UI_Selected_Items": clean(state.get("selectedItems")),
            "UI_Variant_Text": clean(state.get("variant")),
            "Save_Clicked": "Yes",
        }


async def select_official_mockups(product_id: str, product_type: str, wait_seconds: int = 10) -> dict[str, str]:
    ensure_edge_cdp()
    ws_url = _target_ws(product_id)
    desired = {
        "Acrylic": ["Front", "Back", "Side 1", "Side 2"],
        "Poster": [],
    }.get(product_type, [])
    async with CdpPage(ws_url) as page:
        await page.navigate(
            f"https://printify.com/app/mockup-library/shops/{Config.Printify_SHOP_ID}/products/{product_id}?revealUploads=true"
        )
        for _ in range(35):
            if await page.eval("!!location.href && /\\/auth\\/login/.test(location.href)"):
                raise RuntimeError("Printify login required in Edge project browser")
            if await page.eval("!!document.body && /Mockup library/.test(document.body.innerText || '')"):
                break
            await asyncio.sleep(1)
        clicked = []

        async def center(expression: str) -> dict | None:
            return await page.eval(expression)

        clear_box = await center(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                const e=[...document.querySelectorAll('button,[role="button"]')]
                  .filter(visible)
                  .find(e=>clean(e.innerText||e.ariaLabel||'')==='Clear all');
                if(!e)return null;
                const r=e.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
            })()"""
        )
        if clear_box:
            await page.click(clear_box["x"], clear_box["y"])
            await asyncio.sleep(1.5)

        tab_box = await center(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                const e=[...document.querySelectorAll('button,[role="button"]')]
                  .filter(visible)
                  .find(e=>clean(e.innerText||e.ariaLabel||'')==='Printify mockups');
                if(!e)return null;
                const r=e.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
            })()"""
        )
        if tab_box:
            await page.click(tab_box["x"], tab_box["y"])
            await asyncio.sleep(1)

        labels = desired or await page.eval(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                return [...document.querySelectorAll('button.view-type-card')]
                  .filter(visible)
                  .map(e=>clean(e.innerText||e.ariaLabel||''))
                  .filter(Boolean)
                  .slice(0,4);
            })()"""
        )
        for label in labels[:4]:
            card_box = await center(
                r"""(() => {
                    const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                    const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                    const label = """ + json.dumps(label) + r""";
                    const e=[...document.querySelectorAll('button.view-type-card')]
                      .filter(visible)
                      .find(e=>clean(e.innerText||e.ariaLabel||'')===label);
                    if(!e)return null;
                    const r=e.getBoundingClientRect();
                    return {x:r.x+r.width/2,y:r.y+r.height/2};
                })()"""
            )
            if not card_box:
                continue
            await page.click(card_box["x"], card_box["y"])
            await asyncio.sleep(1)
            select_box = await center(
                r"""(() => {
                    const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                    const e=[...document.querySelectorAll('button.mockup-container,.mockup-container')]
                      .filter(visible)
                      .find(e=>{
                        const r=e.getBoundingClientRect();
                        return r.width>180 && r.height>180 && r.x < 540 && r.y > 340;
                      });
                    if(!e)return null;
                    const r=e.getBoundingClientRect();
                    return {x:r.x+24,y:r.y+24};
                })()"""
            )
            if not select_box:
                continue
            await page.click(select_box["x"], select_box["y"])
            clicked.append(label)
            await asyncio.sleep(1)

        selected = await page.eval(
            r"""(() => ((((document.body&&document.body.innerText)||'').match(/(\d+)\s+selected/)||[])[1] || ''))()"""
        )
        save_box = await center(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                const e=[...document.querySelectorAll('button')]
                  .filter(visible)
                  .find(e=>clean(e.innerText||'')==='Save selection' && !e.disabled);
                if(!e)return null;
                const r=e.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
            })()"""
        )
        if not save_box:
            raise RuntimeError(f"Could not save official mockup selection: clicked={clicked}, selected={selected}")
        await page.click(save_box["x"], save_box["y"])
        await asyncio.sleep(wait_seconds)
        return {
            "UI_Selected_Text": clean(selected),
            "UI_Selected_Items": str(len(clicked)),
            "UI_Variant_Text": "|".join(clicked),
            "Save_Clicked": "Yes",
        }


async def select_sticker_cover_plus_official(product_id: str, cover_path: str = "", wait_seconds: int = 10) -> dict[str, str]:
    """Select one uploaded cover mockup plus official Printify sticker mockups.

    The sticker official-only probe showed eBay can repeat the first official
    image into picture slots 1/2. This path keeps one custom Cover selected and
    adds official context mockups, then API verification decides whether the
    result is safe.
    """

    ensure_edge_cdp()
    ws_url = _target_ws(product_id)
    async with CdpPage(ws_url) as page:
        await page.navigate(
            f"https://printify.com/app/mockup-library/shops/{Config.Printify_SHOP_ID}/products/{product_id}?revealUploads=true"
        )
        for _ in range(35):
            if await page.eval("!!location.href && /\\/auth\\/login/.test(location.href)"):
                raise RuntimeError("Printify login required in Edge project browser")
            if await page.eval("!!document.body && /Mockup library/.test(document.body.innerText || '')"):
                break
            await asyncio.sleep(1)

        async def center(expression: str) -> dict | None:
            return await page.eval(expression)

        clear_box = await center(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                const e=[...document.querySelectorAll('button,[role="button"]')]
                  .filter(visible)
                  .find(e=>clean(e.innerText||e.ariaLabel||'')==='Clear all');
                if(!e)return null;
                const r=e.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
            })()"""
        )
        if clear_box:
            await page.click(clear_box["x"], clear_box["y"])
            await asyncio.sleep(1.5)

        uploads_tab = await center(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                const e=[...document.querySelectorAll('button,[role="button"]')]
                  .filter(visible)
                  .find(e=>clean(e.innerText||e.ariaLabel||'')==='My Uploads');
                if(!e)return null;
                const r=e.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
            })()"""
        )
        if uploads_tab:
            await page.click(uploads_tab["x"], uploads_tab["y"])
            await asyncio.sleep(1)
        for _ in range(15):
            has_uploads = await page.eval(
                r"""(() => [...document.querySelectorAll('button.mockup-container,.mockup-container img,img')]
                  .some(e => {
                    const img = e.tagName === 'IMG' ? e : e.querySelector?.('img');
                    return img && /pfy-prod-products-mockup-media/.test(img.src || '');
                  }))()"""
            )
            if has_uploads:
                break
            if uploads_tab:
                await page.click(uploads_tab["x"], uploads_tab["y"])
            await asyncio.sleep(1)

        upload_candidates = await page.eval(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                return [...document.querySelectorAll('button.mockup-container,.mockup-container')]
                  .filter(visible)
                  .filter(e=>{
                    const r=e.getBoundingClientRect();
                    return r.width>180 && r.height>180 && r.x < 540;
                  })
                  .sort((a,b)=>a.getBoundingClientRect().y-b.getBoundingClientRect().y)
                  .slice(0,24)
                  .map((e,i)=>{
                    const r=e.getBoundingClientRect();
                   return {
                      i,
                      x:r.x+r.width/2,
                      y:r.y+r.height/2,
                      checkX:r.x+24,
                      checkY:r.y+24,
                      src:e.querySelector('img')?.src||''
                    };
                  });
            })()"""
        )
        best_cover = best_cover_candidate(upload_candidates or [], cover_path)
        if not best_cover:
            raise RuntimeError("Could not locate uploaded cover mockup candidates")
        # Printify recently changed this grid so clicking the card center can
        # open a preview dialog instead of selecting the image. The top-left
        # checkbox area is the stable intent: select exactly this mockup.
        await page.click(best_cover.get("checkX") or best_cover["x"], best_cover.get("checkY") or best_cover["y"])
        await asyncio.sleep(0.8)
        cover_selected = True
        if not cover_selected:
            raise RuntimeError("Could not select uploaded cover mockup")

        cover_save_box = await center(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                const e=[...document.querySelectorAll('button')]
                  .filter(visible)
                  .find(e=>clean(e.innerText||'')==='Save selection' && !e.disabled);
                if(!e)return null;
                const r=e.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
            })()"""
        )
        if not cover_save_box:
            raise RuntimeError("Could not save sticker cover-only phase")
        await page.click(cover_save_box["x"], cover_save_box["y"])
        await asyncio.sleep(max(3, wait_seconds))
        await page.navigate(
            f"https://printify.com/app/mockup-library/shops/{Config.Printify_SHOP_ID}/products/{product_id}?revealUploads=true"
        )
        for _ in range(35):
            if await page.eval("!!location.href && /\\/auth\\/login/.test(location.href)"):
                raise RuntimeError("Printify login required in Edge project browser")
            if await page.eval("!!document.body && /Mockup library/.test(document.body.innerText || '')"):
                break
            await asyncio.sleep(1)

        tab_box = await center(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                const e=[...document.querySelectorAll('button,[role="button"]')]
                  .filter(visible)
                  .find(e=>clean(e.innerText||e.ariaLabel||'')==='Printify mockups');
                if(!e)return null;
                const r=e.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
            })()"""
        )
        if not tab_box:
            raise RuntimeError("Printify mockups tab not found")
        await page.click(tab_box["x"], tab_box["y"])
        await asyncio.sleep(1.5)

        labels = await page.eval(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                return [...document.querySelectorAll('button.view-type-card')]
                  .filter(visible)
                  .map(e=>clean(e.innerText||e.ariaLabel||''))
                  .filter(Boolean)
                  .slice(0,3);
            })()"""
        )
        clicked = []
        for label in labels[:3]:
            card_box = await center(
                r"""(() => {
                    const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                    const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                    const label = """ + json.dumps(label) + r""";
                    const e=[...document.querySelectorAll('button.view-type-card')]
                      .filter(visible)
                      .find(e=>clean(e.innerText||e.ariaLabel||'')===label);
                    if(!e)return null;
                    const r=e.getBoundingClientRect();
                    return {x:r.x+r.width/2,y:r.y+r.height/2};
                })()"""
            )
            if not card_box:
                continue
            await page.click(card_box["x"], card_box["y"])
            await asyncio.sleep(0.8)
            select_box = await center(
                r"""(() => {
                    const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                    const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                    const e=[...document.querySelectorAll('[role="checkbox"], pfy-checkbox, .select-all-checkbox')]
                      .filter(visible)
                      .find(e=>clean(e.innerText||e.textContent||e.ariaLabel||'')==='Select all'
                        && e.getBoundingClientRect().x < 1020);
                    if(!e)return null;
                    const r=e.getBoundingClientRect();
                    return {x:r.x+r.width/2,y:r.y+r.height/2};
                })()"""
            )
            if not select_box:
                continue
            await page.click(select_box["x"], select_box["y"])
            clicked.append(label)
            await asyncio.sleep(0.8)
        if len(clicked) < 3:
            direct_cards = await page.eval(
                r"""(() => {
                    const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                    return [...document.querySelectorAll('button.mockup-container,.mockup-container')]
                      .filter(visible)
                      .filter(e=>{
                        const r=e.getBoundingClientRect();
                        return r.width>180 && r.height>180 && r.x < 540;
                      })
                      .sort((a,b)=>a.getBoundingClientRect().y-b.getBoundingClientRect().y)
                      .slice(0,3)
                      .map((e,i)=>{
                        const r=e.getBoundingClientRect();
                        return {i, x:r.x+r.width/2, y:r.y+r.height/2, checkX:r.x+24, checkY:r.y+24};
                      });
                })()"""
            )
            clicked = []
            for idx, card in enumerate(direct_cards or [], start=1):
                await page.click(card.get("checkX") or card["x"], card.get("checkY") or card["y"])
                clicked.append(f"Grid {idx}")
                await asyncio.sleep(0.8)
        if len(clicked) < 3:
            raise RuntimeError(f"Could not select 3 official sticker mockups: {clicked}")

        selected = await page.eval(
            r"""(() => ((((document.body&&document.body.innerText)||'').match(/(\d+)\s+selected/)||[])[1] || ''))()"""
        )
        save_box = await center(
            r"""(() => {
                const visible=e=>!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length);
                const clean=s=>(s||'').replace(/\s+/g,' ').trim();
                const e=[...document.querySelectorAll('button')]
                  .filter(visible)
                  .find(e=>clean(e.innerText||'')==='Save selection' && !e.disabled);
                if(!e)return null;
                const r=e.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
            })()"""
        )
        if not save_box:
            raise RuntimeError(f"Could not save sticker cover+official selection: clicked={clicked}, selected={selected}")
        await page.click(save_box["x"], save_box["y"])
        await asyncio.sleep(wait_seconds)
        return {
            "UI_Selected_Text": clean(selected),
            "UI_Selected_Items": str(1 + len(clicked)),
            "UI_Variant_Text": f"Cover(distance={best_cover.get('Cover_Distance', 'NA')})|" + "|".join(clicked),
            "Save_Clicked": "Yes",
        }


def candidate_rows(limit: int, ids: set[str], include_custom_risk: bool) -> list[dict[str, str]]:
    if ids:
        workbook = {row["ID"]: row for row in workbook_rows(ids=ids)}
        return [workbook[item_id] for item_id in ids if item_id in workbook]
    queued = []
    for row in read_repair_queue():
        issue = clean(row.get("Issue"))
        if issue == "CHECK_EXACT_DUPLICATE" or (include_custom_risk and issue == "CHECK_CUSTOM_GALLERY_REPEATS_RISK"):
            queued.append(row)
        if limit and len(queued) >= limit:
            break
    wanted = [clean(row.get("ID")) for row in queued if clean(row.get("ID"))]
    workbook = {row["ID"]: row for row in workbook_rows(ids=set(wanted))}
    return [workbook[item_id] for item_id in wanted if item_id in workbook]


def append_log(rows: list[dict[str, str]]) -> None:
    fields = [
        "Timestamp",
        "ID",
        "Product_Type",
        "Printify_Product_ID",
        "eBay_Item_ID",
        "Action",
        "UI_Selected_Text",
        "UI_Selected_Items",
        "UI_Variant_Text",
        "Post_Result",
        "Post_Selected_Count",
        "Post_Unique_Visual_Count",
        "Api_Image_Count",
        "Api_Official_Count",
        "Api_Custom_Count",
        "Api_Other_Count",
        "Publish_Status",
        "Error",
    ]
    exists = OUT_CSV.exists()
    with OUT_CSV.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def run(
    limit: int,
    ids: set[str],
    include_custom_risk: bool,
    publish: bool,
    sleep_seconds: float,
    official_only: bool,
    sticker_cover_plus_official: bool,
) -> int:
    rows = candidate_rows(limit=limit, ids=ids, include_custom_risk=include_custom_risk)
    log_rows = []
    done = 0
    for row in rows:
        item_id = clean(row.get("ID"))
        product_id = clean(row.get("Printify_Product_ID"))
        record = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S %z"),
            "ID": item_id,
            "Product_Type": clean(row.get("Product_Type")),
            "Printify_Product_ID": product_id,
            "eBay_Item_ID": clean(row.get("eBay_Item_ID")),
            "Action": "RESAVE_CURRENT_SELECTION",
            "Publish_Status": "",
            "Error": "",
        }
        try:
            for attempt in range(2):
                try:
                    if sticker_cover_plus_official:
                        record["Action"] = "SELECT_STICKER_COVER_PLUS_OFFICIAL"
                        record.update(asyncio.run(select_sticker_cover_plus_official(product_id, clean(row.get("Cover_Path")))))
                    elif official_only:
                        record["Action"] = "SELECT_OFFICIAL_ONLY"
                        record.update(asyncio.run(select_official_mockups(product_id, record["Product_Type"])))
                    else:
                        record.update(asyncio.run(resave_current_selection(product_id)))
                    break
                except Exception as exc:  # noqa: BLE001
                    if attempt == 0 and is_cdp_connection_error(exc):
                        ensure_edge_cdp()
                        time.sleep(2)
                        continue
                    raise
            post = audit_row(row, deep_hash=False)
            record["Post_Result"] = clean(post.get("Result"))
            record["Post_Selected_Count"] = clean(post.get("Selected_Count"))
            record["Post_Unique_Visual_Count"] = clean(post.get("Unique_Visual_Count"))
            if sticker_cover_plus_official and clean(row.get("Product_Type")) == "Sticker":
                mix = api_gallery_mix(product_id)
                record.update(mix)
                if not (
                    mix["Api_Image_Count"] == "4"
                    and mix["Api_Official_Count"] == "3"
                    and mix["Api_Custom_Count"] == "1"
                    and mix["Api_Other_Count"] == "0"
                ):
                    raise RuntimeError(
                        "Unsafe sticker gallery mix after save: "
                        f"images={mix['Api_Image_Count']} official={mix['Api_Official_Count']} "
                        f"custom={mix['Api_Custom_Count']} other={mix['Api_Other_Count']}"
                    )
            if publish:
                code = publish_images(product_id)
                record["Publish_Status"] = f"images_publish_http_{code}"
            done += 1
            print(
                f"[PRINTIFY-SOURCE-REPAIR] {item_id} post={record['Post_Result']} "
                f"selected={record['Post_Selected_Count']} unique={record['Post_Unique_Visual_Count']} "
                f"{record['Publish_Status']}"
            )
        except Exception as exc:
            record["Error"] = str(exc)
            print(f"[PRINTIFY-SOURCE-REPAIR-FAIL] {item_id}: {exc}")
        log_rows.append(record)
        append_log([record])
        if sleep_seconds:
            time.sleep(sleep_seconds)
    print(f"[PRINTIFY-SOURCE-REPAIR-DONE] rows={len(rows)} done={done} log={OUT_CSV}")
    return done


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--ids", default="", help="Comma-separated workbook IDs.")
    parser.add_argument("--include-custom-risk", action="store_true")
    parser.add_argument("--official-only", action="store_true")
    parser.add_argument("--sticker-cover-plus-official", action="store_true")
    parser.add_argument("--publish-images", action="store_true")
    parser.add_argument("--sleep-seconds", type=float, default=2.0)
    args = parser.parse_args()
    ids = {value.strip() for value in args.ids.split(",") if value.strip()}
    run(
        limit=args.limit,
        ids=ids,
        include_custom_risk=args.include_custom_risk,
        publish=args.publish_images,
        sleep_seconds=args.sleep_seconds,
        official_only=args.official_only,
        sticker_cover_plus_official=args.sticker_cover_plus_official,
    )


if __name__ == "__main__":
    main()
