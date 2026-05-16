"""Publish staged Etsy digital downloads through the logged-in Edge UI.

This is a narrow bridge while Etsy Open API approval is pending. It obeys the
same fee kill switch as the API path: one listing proof first, no blind retries,
and every confirmed publish is written to the fee ledger.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import re
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.risk_guard import assert_allowed, assert_etsy_fee_batch_allowed, fee_kill_switch

DATABASE = PROJECT_ROOT / "Database"
QUEUE_PATH = DATABASE / "Etsy_Digital_Gray_Launch_Queue.csv"
QA_PATH = DATABASE / "Etsy_Digital_QA_Report.csv"
FEE_LEDGER_PATH = DATABASE / "Etsy_Fee_Ledger.csv"
METADATA_PATH = DATABASE / "Digital_Etsy_Metadata.csv"
UI_LOG_PATH = DATABASE / "Etsy_Digital_UI_Publish_Log.csv"

ETSY_CREATE_URL = "https://www.etsy.com/your/shops/me/listing-editor/create"

LOG_FIELDS = [
    "Timestamp",
    "ID",
    "Action",
    "Status",
    "Etsy_Listing_ID",
    "URL",
    "Confirmed_Fee_USD",
    "Note",
]


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _append_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    exists = path.exists()
    with path.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def _confirmed_spend_today() -> float:
    today = datetime.now().date().isoformat()
    total = 0.0
    for row in _read_csv(FEE_LEDGER_PATH):
        if str(row.get("Timestamp", "")).startswith(today) and str(row.get("Status", "")).startswith("CONFIRMED"):
            try:
                total += float(row.get("Confirmed_Spent_USD") or 0)
            except ValueError:
                pass
    return total


def _metadata_by_id() -> dict[str, dict]:
    return {row.get("ID", ""): row for row in _read_csv(METADATA_PATH)}


def _select_candidates(limit: int) -> list[dict]:
    metadata = _metadata_by_id()
    rows = []
    for row in _read_csv(QUEUE_PATH):
        if not row.get("QA_Status", "").startswith("PASS"):
            continue
        if row.get("Etsy_Listing_ID"):
            continue
        if row.get("Fee_Status") == "CONFIRMED_SPENT":
            continue
        if row.get("Launch_Status") not in {"READY_BLOCKED_ETSY_AUTH", "READY_TO_PUBLISH", "READY_UI_PUBLISH", "READY_API_PUBLISH"}:
            continue
        merged = dict(row)
        merged.update({f"Meta_{k}": v for k, v in (metadata.get(row.get("ID", "")) or {}).items()})
        rows.append(merged)
        if len(rows) >= limit:
            break
    return rows


def _font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _fit(image: Image.Image, size: tuple[int, int], fill=(241, 239, 234)) -> Image.Image:
    canvas = Image.new("RGB", size, fill)
    im = image.copy().convert("RGB")
    im.thumbnail(size, Image.Resampling.LANCZOS)
    canvas.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return canvas


def _draw_wrap(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, max_chars: int, font, fill=(45, 42, 38)):
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        probe = " ".join(current + [word])
        if len(probe) > max_chars and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    x, y = xy
    for line in lines[:8]:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + 12


def _preview_paths(row: dict) -> list[str]:
    custom_preview = str(row.get("Preview_Image") or row.get("Meta_Preview_Image") or "").strip()
    if custom_preview:
        preview_path = Path(custom_preview)
        if preview_path.exists():
            preview_dir = preview_path.parent / "_etsy_preview"
            preview_dir.mkdir(parents=True, exist_ok=True)
            existing = sorted(preview_dir.glob("Preview_*.jpg"))
            if len(existing) >= 5:
                return [str(path) for path in existing[:5]]

            with Image.open(preview_path) as source:
                source = ImageEnhance.Contrast(source.convert("RGB")).enhance(1.02)
                art_square = _fit(source, (1160, 1160), fill=(247, 245, 240))
                art_detail = _fit(source.crop(source.getbbox() or (0, 0, source.width, source.height)), (1300, 1300), fill=(247, 245, 240))

            title = _clean(row.get("Title") or row.get("Meta_Title") or row.get("ID") or preview_path.stem)
            title_font = _font(70, True)
            sub_font = _font(42)
            body_font = _font(34)
            small_font = _font(28)

            p1 = preview_dir / "Preview_01_cover.jpg"
            canvas = Image.new("RGB", (2000, 2000), (242, 239, 232))
            draw = ImageDraw.Draw(canvas)
            canvas.paste(art_square, (420, 170))
            draw.rounded_rectangle([140, 1470, 1860, 1870], radius=34, fill=(255, 254, 250), outline=(185, 178, 169), width=3)
            draw.text((210, 1535), "Digital Download", font=title_font, fill=(35, 32, 28))
            _draw_wrap(draw, (215, 1645), title, 52, sub_font, fill=(78, 70, 62))
            draw.text((215, 1785), "Instant files. No physical item is shipped.", font=body_font, fill=(112, 76, 52))
            canvas.save(p1, "JPEG", quality=92, optimize=True)

            p2 = preview_dir / "Preview_02_detail_zoom.jpg"
            canvas = Image.new("RGB", (2000, 2000), (248, 246, 241))
            draw = ImageDraw.Draw(canvas)
            canvas.paste(art_detail, (120, 210))
            draw.rectangle([120, 210, 1420, 1510], outline=(172, 165, 154), width=3)
            draw.text((1500, 290), "Detail", font=title_font, fill=(35, 32, 28))
            _draw_wrap(draw, (1505, 410), "Close-up preview for texture, linework, and printable atmosphere.", 18, body_font)
            draw.text((1505, 1370), "Curated digital asset", font=small_font, fill=(90, 82, 74))
            canvas.save(p2, "JPEG", quality=92, optimize=True)

            p3 = preview_dir / "Preview_03_included_files.jpg"
            canvas = Image.new("RGB", (2000, 2000), (250, 249, 246))
            draw = ImageDraw.Draw(canvas)
            draw.text((125, 105), "Included", font=title_font, fill=(35, 32, 28))
            included = ["Printable image / design file", "High-resolution preview asset", "Personal-use digital download", "Files delivered through Etsy after purchase"]
            for i, line in enumerate(included):
                y = 330 + i * 260
                draw.rounded_rectangle([130, y, 1870, y + 185], radius=22, fill=(255, 254, 250), outline=(190, 185, 176), width=3)
                draw.text((195, y + 55), line, font=sub_font, fill=(45, 42, 38))
            draw.text((160, 1695), "Use for journaling, personal print projects, moodboards, or decor planning.", font=body_font, fill=(82, 76, 68))
            canvas.save(p3, "JPEG", quality=92, optimize=True)

            p4 = preview_dir / "Preview_04_download_notice.jpg"
            canvas = Image.new("RGB", (2000, 2000), (239, 236, 229))
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle([180, 240, 1820, 1640], radius=36, fill=(255, 254, 250), outline=(184, 178, 169), width=3)
            draw.text((290, 380), "Digital Item", font=title_font, fill=(35, 32, 28))
            _draw_wrap(draw, (300, 540), "This listing is for downloadable files only. No printed product, frame, or physical shipment is included.", 48, sub_font)
            draw.text((300, 1180), "AI-assisted, human-curated, QA checked.", font=body_font, fill=(90, 82, 74))
            draw.text((300, 1270), "Please review previews before purchase.", font=body_font, fill=(112, 76, 52))
            canvas.save(p4, "JPEG", quality=92, optimize=True)

            p5 = preview_dir / "Preview_05_license_note.jpg"
            canvas = Image.new("RGB", (2000, 2000), (250, 249, 246))
            draw = ImageDraw.Draw(canvas)
            draw.text((160, 190), "Use Notes", font=title_font, fill=(35, 32, 28))
            notes = [
                "Personal use digital download",
                "Print quality depends on paper, printer, and scaling",
                "Colors may vary slightly by monitor and device",
                "No resale, redistribution, or commercial upload",
            ]
            for i, line in enumerate(notes):
                y = 420 + i * 245
                draw.rounded_rectangle([160, y, 1840, y + 170], radius=24, fill=(255, 254, 250), outline=(190, 185, 176), width=3)
                draw.text((225, y + 50), line, font=sub_font, fill=(45, 42, 38))
            draw.text((160, 1655), "OpenClaw Archive digital experiment", font=body_font, fill=(82, 76, 68))
            canvas.save(p5, "JPEG", quality=92, optimize=True)
            return [str(p1), str(p2), str(p3), str(p4), str(p5)]

    item_id = row["ID"]
    zip_path = Path(row["Zip_Path"])
    pack_dir = zip_path.with_suffix("")
    preview_dir = pack_dir / "_etsy_preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(preview_dir.glob("Preview_*.jpg"))
    if len(existing) >= 3:
        return [str(path) for path in existing[:3]]

    art_candidates = sorted(pack_dir.glob(f"{item_id}_2x3_*.jpg")) or sorted(pack_dir.glob("*.jpg"))
    if not art_candidates:
        raise FileNotFoundError(f"No printable JPG found in {pack_dir}")
    with Image.open(art_candidates[0]) as source:
        source = ImageEnhance.Contrast(source.convert("RGB")).enhance(1.02)
        art = _fit(source, (860, 1290))

    title = _clean(row.get("Title") or row.get("Meta_Title") or item_id)
    title_font = _font(72, True)
    sub_font = _font(42)
    body_font = _font(34)
    small_font = _font(28)

    p1 = preview_dir / "Preview_01_framed_printable.jpg"
    canvas = Image.new("RGB", (2000, 2000), (239, 236, 229))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, 2000, 1450], fill=(244, 242, 237))
    frame = (600, 120, 1460, 1410)
    draw.rectangle([frame[0] - 42, frame[1] - 42, frame[2] + 42, frame[3] + 42], fill=(49, 43, 38))
    draw.rectangle([frame[0] - 18, frame[1] - 18, frame[2] + 18, frame[3] + 18], fill=(235, 231, 224))
    canvas.paste(art, (frame[0], frame[1]))
    draw.rounded_rectangle([110, 1540, 1030, 1885], radius=28, fill=(255, 254, 250), outline=(184, 178, 169), width=3)
    draw.text((165, 1595), "Digital Download", font=title_font, fill=(35, 32, 28))
    draw.text((170, 1700), "5 printable JPG ratios included", font=sub_font, fill=(78, 70, 62))
    draw.text((170, 1764), "No physical item is shipped", font=body_font, fill=(112, 76, 52))
    draw.text((1270, 1760), "Quiet Relic Studio", font=body_font, fill=(67, 59, 52))
    canvas.save(p1, "JPEG", quality=92, optimize=True)

    p2 = preview_dir / "Preview_02_included_ratios.jpg"
    canvas = Image.new("RGB", (2000, 2000), (250, 249, 246))
    draw = ImageDraw.Draw(canvas)
    draw.text((125, 105), "Included Files", font=title_font, fill=(35, 32, 28))
    for i, line in enumerate(["2x3 ratio: 12x18, 16x24, 20x30", "3x4 ratio: 9x12, 12x16, 18x24", "4x5 ratio: 8x10, 12x15, 16x20", "5x7 ratio: 5x7, 10x14", "11x14 ratio"]):
        y = 310 + i * 250
        draw.rounded_rectangle([130, y, 1870, y + 185], radius=22, fill=(255, 254, 250), outline=(190, 185, 176), width=3)
        draw.text((195, y + 55), line, font=sub_font, fill=(45, 42, 38))
    draw.text((160, 1695), "Print at home or with any local/online print shop.", font=body_font, fill=(82, 76, 68))
    canvas.save(p2, "JPEG", quality=92, optimize=True)

    p3 = preview_dir / "Preview_03_style_detail.jpg"
    canvas = Image.new("RGB", (2000, 2000), (247, 245, 240))
    draw = ImageDraw.Draw(canvas)
    canvas.paste(_fit(art, (1000, 1500)), (110, 210))
    draw.rectangle([110, 210, 1110, 1710], outline=(172, 165, 154), width=3)
    draw.text((1200, 260), "Printable Wall Art", font=title_font, fill=(35, 32, 28))
    _draw_wrap(draw, (1205, 380), title, 26, sub_font)
    draw.rounded_rectangle([1200, 1335, 1845, 1605], radius=24, fill=(255, 254, 250), outline=(190, 185, 176), width=2)
    draw.text((1245, 1390), "Instant digital files", font=body_font, fill=(45, 42, 38))
    draw.text((1245, 1450), "AI-assisted artwork", font=small_font, fill=(90, 82, 74))
    draw.text((1245, 1502), "Personal use license", font=small_font, fill=(90, 82, 74))
    canvas.save(p3, "JPEG", quality=92, optimize=True)

    return [str(p1), str(p2), str(p3)]


def _safe_digital_upload_path(row: dict) -> Path:
    source = Path(row["Zip_Path"]).resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    upload_dir = source.parent / "_etsy_upload"
    upload_dir.mkdir(exist_ok=True)
    safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "-", str(row["ID"]))[:52].strip("-")
    target = upload_dir / f"OC-{safe_stem}.zip"
    if not target.exists() or target.stat().st_mtime < source.stat().st_mtime or target.stat().st_size != source.stat().st_size:
        shutil.copy2(source, target)
    if len(target.name) > 70:
        raise ValueError(f"Etsy-safe upload filename is too long: {target.name}")
    return target


def _parse_listing_id(url: str) -> str:
    match = re.search(r"/listing/(\d+)|/edit/(\d+)", url)
    if not match:
        return ""
    return next(group for group in match.groups() if group)


def _parse_listing_id_from_manager(page, row: dict) -> tuple[str, str]:
    item_id = str(row.get("ID") or "")
    title_start = _clean(row.get("Title") or "")[:50]
    try:
        page.wait_for_function(
            """needle => document.body && document.body.innerText.includes(needle)""",
            arg=item_id,
            timeout=20000,
        )
    except Exception:
        pass
    links = page.locator("a").evaluate_all(
        """els => els.map(a => ({text: (a.innerText || a.ariaLabel || '').trim(), href: a.href}))
        .filter(x => x.href.includes('/listing/') || x.href.includes('listing-editor/edit'))"""
    )
    for link in links:
        text = link.get("text") or ""
        href = link.get("href") or ""
        if item_id in text or (title_start and title_start in text):
            listing_id = _parse_listing_id(href)
            if listing_id:
                return listing_id, href
    return "", page.url


def _set_manual_renew(page) -> None:
    radios = page.locator('input[name="shouldAutoRenew"]')
    if radios.count() >= 2:
        radios.nth(1).evaluate(
            "e => { e.checked=true; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }"
        )


def _choose_radio_by_name(page, name: str, index: int) -> None:
    radios = page.locator(f'input[name="{name}"]')
    if radios.count() > index:
        radios.nth(index).evaluate(
            "e => { e.checked=true; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }"
        )


def _fill_listing(page, row: dict) -> None:
    title = _clean(row.get("Title") or row.get("Meta_Title"))
    description = str(row.get("Meta_Description") or row.get("Description") or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    tags = [tag.strip()[:20] for tag in str(row.get("Meta_Tags") or "").split(",") if tag.strip()]
    if len(tags) < 13:
        tags.extend(["printable wall art", "digital download", "dark academia", "study room decor", "gallery wall"][: 13 - len(tags)])
    price = str(row.get("Price") or row.get("Meta_Price") or "6.99").replace("$", "").strip()
    zip_path = str(_safe_digital_upload_path(row))
    preview_paths = _preview_paths(row)

    page.goto(ETSY_CREATE_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3500)
    for button_text in ("Dismiss", "Got it"):
        try:
            loc = page.get_by_role("button", name=button_text)
            if loc.count() > 0 and loc.first.is_visible():
                loc.first.click(timeout=2000)
                page.wait_for_timeout(500)
        except Exception:
            pass

    # Photos first; Etsy's first file input is the photo/video uploader.
    page.locator("input[type=file]").nth(0).set_input_files(preview_paths)
    page.wait_for_timeout(5000)

    page.locator("#category-field-search").fill("digital wall art printable")
    page.wait_for_timeout(2500)
    page.get_by_text("Digital Prints", exact=True).first.click(timeout=8000)
    page.wait_for_timeout(1500)
    try:
        change_anyway = page.get_by_role("button", name="Change category anyway")
        if change_anyway.count() > 0 and change_anyway.first.is_visible():
            change_anyway.first.click(timeout=5000)
            page.wait_for_timeout(2500)
    except Exception:
        pass

    # Switch to digital downloads. Direct event dispatch avoids sticky UI intercepts.
    page.locator('input[name="listing_type_options_group"][value="download"]').evaluate(
        "e => { e.checked=true; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }"
    )
    page.wait_for_timeout(2500)

    # Target the digital file uploader by its stable section id. After photos
    # upload, Etsy adds extra photo inputs, so positional nth() can hit the
    # wrong uploader and trigger a photo-format error for the ZIP.
    page.locator("#field-digitalFiles input[type=file]").set_input_files(zip_path)
    page.wait_for_timeout(4000)

    page.locator('textarea[name="title"]').fill(title)
    page.locator('textarea[name="description"]').fill(description)

    # Made in 2020-2026.
    selects = page.locator("select")
    if selects.count() > 0:
        try:
            selects.nth(0).select_option(label="2020 - 2026")
        except Exception:
            pass

    tag_input = page.locator("#listing-tags-input")
    for tag in tags[:13]:
        tag_input.fill(tag)
        tag_input.press("Enter")
        page.wait_for_timeout(150)

    page.locator("#listing-price-input").fill(price)
    page.locator("#listing-quantity-input").fill("999")
    try:
        page.get_by_role("button", name="Add SKU").click(timeout=3000)
        page.wait_for_timeout(500)
    except Exception:
        pass
    if page.locator('input[name="sku"]').count() > 0:
        try:
            page.locator('input[name="sku"]').fill(f"DIGITAL-{row['ID']}")
        except Exception:
            pass

    # How it's made: I did; finished product; created by me. Prefer direct radio dispatch for stability.
    _choose_radio_by_name(page, "whoMade", 0)
    _choose_radio_by_name(page, "isSupply", 0)
    _choose_radio_by_name(page, "digitalContentCreatedBy", 1)
    _set_manual_renew(page)


def _wait_until_publish_ready(page, timeout_ms: int = 180000) -> None:
    page.wait_for_function(
        """() => {
            const buttons = [...document.querySelectorAll('button')].filter(b =>
                ((b.innerText || '').trim() === 'Publish') || b.getAttribute('data-testid') === 'publish'
            );
            if (!buttons.some(b => !b.disabled && b.getAttribute('aria-disabled') !== 'true')) return false;
            const loadingText = (document.body && document.body.innerText || '').toLowerCase();
            if (loadingText.includes('uploading') || loadingText.includes('processing files')) return false;
            return true;
        }""",
        timeout=timeout_ms,
    )


def _mark_result(row_id: str, listing_id: str, url: str, fee: float) -> None:
    queue = _read_csv(QUEUE_PATH)
    for row in queue:
        if row.get("ID") == row_id and not row.get("Etsy_Listing_ID"):
            row["Etsy_Listing_ID"] = listing_id
            row["Fee_Status"] = "CONFIRMED_SPENT"
            row["Launch_Status"] = "PUBLISHED_UI_CONFIRMED"
            row["Notes"] = f"Published via Etsy UI at {url}"
            break
    if queue:
        _write_csv(QUEUE_PATH, queue, list(queue[0].keys()))

    metadata = _read_csv(METADATA_PATH)
    for row in metadata:
        if row.get("ID") == row_id:
            row["Status"] = "PUBLISHED_ETSY_UI_CONFIRMED"
            break
    if metadata:
        _write_csv(METADATA_PATH, metadata, list(metadata[0].keys()))

    ledger = _read_csv(FEE_LEDGER_PATH)
    for row in ledger:
        if row.get("ID") == row_id and row.get("Status") == "RESERVED_NOT_SPENT":
            row["Confirmed_Spent_USD"] = f"{fee:.2f}"
            row["Status"] = "CONFIRMED_SPENT_UI"
            row["Reference"] = listing_id or url
            break
    if ledger:
        _write_csv(FEE_LEDGER_PATH, ledger, list(ledger[0].keys()))

    _append_csv(
        UI_LOG_PATH,
        [
            {
                "Timestamp": _now(),
                "ID": row_id,
                "Action": "PUBLISH",
                "Status": "CONFIRMED",
                "Etsy_Listing_ID": listing_id,
                "URL": url,
                "Confirmed_Fee_USD": f"{fee:.2f}",
                "Note": "Published through logged-in Etsy UI with manual renewal selected.",
            }
        ],
        LOG_FIELDS,
    )


def publish(limit: int = 1, dry_run: bool = False, cdp_port: int = 9223) -> dict:
    assert_allowed("etsy", "paid_publish")
    candidates = _select_candidates(limit)
    if not candidates:
        return {"selected": 0, "published": 0, "status": "NO_CANDIDATES"}
    assert_etsy_fee_batch_allowed(len(candidates), daily_spend_so_far=_confirmed_spend_today())
    fee = float((fee_kill_switch() or {}).get("expected_listing_fee_usd", 0.20))

    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{cdp_port}")
        context = browser.contexts[0]
        for row in candidates:
            page = context.new_page()
            try:
                _fill_listing(page, row)
                if dry_run:
                    results.append({"ID": row["ID"], "status": "DRY_RUN_FILLED", "url": page.url})
                    continue
                _wait_until_publish_ready(page)
                page.locator('button[data-testid="publish"]').first.click(timeout=10000)
                page.wait_for_timeout(8000)
                try:
                    change_anyway = page.get_by_role("button", name="Change category anyway")
                    if change_anyway.count() > 0 and change_anyway.first.is_visible():
                        change_anyway.first.click(timeout=10000)
                        page.wait_for_timeout(4000)
                    confirm = page.locator('button[data-testid="publish"], button:has-text("Publish")')
                    if confirm.count() > 0 and confirm.first.is_visible():
                        confirm.first.click(timeout=10000)
                        page.wait_for_timeout(8000)
                except Exception:
                    pass
                url = page.url
                listing_id = _parse_listing_id(url)
                body = page.locator("body").inner_text(timeout=10000)
                if not listing_id and "/tools/listings" in url:
                    listing_id, url = _parse_listing_id_from_manager(page, row)
                if not listing_id and "newly_created=1" in page.url:
                    page.goto("https://www.etsy.com/your/shops/me/tools/listings", wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(12000)
                    listing_id, url = _parse_listing_id_from_manager(page, row)
                if not listing_id and "published" not in body.lower():
                    raise RuntimeError(f"Publish not confirmed. url={url} body={body[:500]}")
                _mark_result(row["ID"], listing_id, url, fee)
                results.append({"ID": row["ID"], "status": "PUBLISHED", "listing_id": listing_id, "url": url})
            except Exception as exc:  # noqa: BLE001
                _append_csv(
                    UI_LOG_PATH,
                    [
                        {
                            "Timestamp": _now(),
                            "ID": row.get("ID", ""),
                            "Action": "PUBLISH",
                            "Status": "ERROR",
                            "Etsy_Listing_ID": "",
                            "URL": page.url,
                            "Confirmed_Fee_USD": "0.00",
                            "Note": f"{type(exc).__name__}: {_clean(exc)}"[:500],
                        }
                    ],
                    LOG_FIELDS,
                )
                results.append({"ID": row.get("ID"), "status": "ERROR", "error": str(exc)[:300], "url": page.url})
                # Money-sensitive path: stop after any ambiguity/error.
                break
            finally:
                page.close()
        browser.close()
    return {"selected": len(candidates), "published": sum(1 for r in results if r["status"] == "PUBLISHED"), "results": results}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cdp-port", type=int, default=9223)
    args = parser.parse_args()
    result = publish(limit=args.limit, dry_run=args.dry_run, cdp_port=args.cdp_port)
    print(result)


if __name__ == "__main__":
    main()
