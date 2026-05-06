import argparse
import csv
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.mj_harvest import Config, _interaction, _validate_runtime_config

OUTPUT_ROOT = PROJECT_ROOT / "Output" / "Brand" / "Etsy"
LOG_PATH = PROJECT_ROOT / "Database" / "etsy_brand_mj_jobs.csv"

MJ_SUFFIX = "--v 6.1 --style raw --stylize 200 --no text, letters, words, logo text, watermark, people, face"

SCHEMES = [
    {
        "code": "01",
        "name": "Jade Archive Studio",
        "shop_names": ["JadeArchiveStudio", "JadeArchiveCo", "TheJadeArchive"],
        "icon": (
            "premium square shop icon, carved imperial jade seal emblem inside a subtle antique gold frame, "
            "archive drawer geometry, scholar studio object, ink green stone, warm paper white negative space, "
            "minimal luxury brand mark, centered composition, no typography"
        ),
        "banner": (
            "premium Etsy shop banner, quiet scholar archive shelf with jade seals, antique brass catalog drawers, "
            "ink-wash paper texture, moonlit study room, dark green and warm ivory palette, curated high-end wall art "
            "and acrylic object studio atmosphere, elegant negative space, no typography"
        ),
    },
    {
        "code": "02",
        "name": "Quiet Relic Studio",
        "shop_names": ["QuietRelicStudio", "QuietRelicCo", "RelicQuiet"],
        "icon": (
            "premium square shop icon, luminous jade relic bell inside a glass museum display case, oxidized bronze, "
            "soft smoke blue glow, black lacquer background, tiny kintsugi seams, collectible object studio mark, "
            "centered simple silhouette, no typography"
        ),
        "banner": (
            "premium Etsy shop banner, dark museum shelf of jade relics, kintsugi vessels, bronze bells, crystalline "
            "acrylic refraction, quiet ritual-object gallery, cinematic low light, obsidian and smoke blue palette, "
            "luxury collectible decor atmosphere, no typography"
        ),
    },
    {
        "code": "03",
        "name": "Scholar Grove Atelier",
        "shop_names": ["ScholarGrove", "ScholarGroveArt", "GroveAtelier"],
        "icon": (
            "premium square shop icon, miniature bonsai beside an open scholar book and small jade moonstone, "
            "wabi-sabi ceramic base, antique brass linework, moss green and warm walnut palette, calm study decor "
            "brand mark, centered clean silhouette, no typography"
        ),
        "banner": (
            "premium Etsy shop banner, zen study room shelf with bonsai, jade paperweight, old books, ink brush, "
            "soft morning light, wabi-sabi textures, moss green, walnut, moonstone white, warm approachable luxury "
            "decor atmosphere, no typography"
        ),
    },
    {
        "code": "04",
        "name": "Lumen Relic Gallery",
        "shop_names": ["LumenRelic", "LumenRelicArt", "RelicLumen"],
        "icon": (
            "premium square shop icon, glowing jade crystal relic inside a black glass frame, celestial gate motif, "
            "cyan internal glow, gold dust, dark navy background, high-end mystical gallery mark, centered crisp "
            "silhouette, no typography"
        ),
        "banner": (
            "premium Etsy shop banner, dramatic celestial artifact gallery with glowing jade crystals, acrylic light "
            "refraction, dark academia shelves, gold dust, black glass and deep navy palette, high click appeal but "
            "premium clean composition, no typography"
        ),
    },
]


def now_slug():
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_log():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        with LOG_PATH.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "Timestamp",
                    "Job_ID",
                    "Scheme",
                    "Asset_Type",
                    "Prompt",
                    "Status",
                    "Grid_Path",
                    "Message_ID",
                ],
            )
            writer.writeheader()


def append_log(row):
    ensure_log()
    with LOG_PATH.open("a", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "Timestamp",
                "Job_ID",
                "Scheme",
                "Asset_Type",
                "Prompt",
                "Status",
                "Grid_Path",
                "Message_ID",
            ],
        )
        writer.writerow(row)


def build_jobs(limit=None):
    jobs = []
    for scheme in SCHEMES:
        jobs.append(
            {
                "scheme": scheme["code"],
                "name": scheme["name"],
                "asset_type": "icon",
                "ar": "1:1",
                "prompt": scheme["icon"],
            }
        )
        jobs.append(
            {
                "scheme": scheme["code"],
                "name": scheme["name"],
                "asset_type": "banner",
                "ar": "4:1",
                "prompt": scheme["banner"],
            }
        )
    if limit:
        jobs = jobs[: int(limit)]
    return jobs


def send_job(job, run_dir, nonce):
    job_id = f"ETSYBRAND_{job['scheme']}_{job['asset_type'].upper()}_{nonce}"
    prompt = f"{job['prompt']} ID_{job_id} --ar {job['ar']} {MJ_SUFFIX}"
    payload = {
        "type": 2,
        "application_id": Config.APP_ID,
        "guild_id": Config.GUILD_ID,
        "channel_id": Config.CHANNEL_ID,
        "session_id": Config.SESSION_ID,
        "data": {
            "version": Config.MJ_VERSION,
            "id": Config.MJ_ID,
            "name": "imagine",
            "type": 1,
            "options": [{"type": 3, "name": "prompt", "value": prompt}],
        },
    }
    response = _interaction(payload)
    status = "SUBMITTED" if response else "FAILED_SUBMIT"
    append_log(
        {
            "Timestamp": dt.datetime.now().isoformat(timespec="seconds"),
            "Job_ID": job_id,
            "Scheme": job["name"],
            "Asset_Type": job["asset_type"],
            "Prompt": prompt,
            "Status": status,
            "Grid_Path": "",
            "Message_ID": "",
        }
    )
    print(f"[EtsyBrandMJ] {job_id} {status}")
    return {**job, "job_id": job_id, "prompt": prompt, "status": status, "run_dir": str(run_dir)}


def fetch_messages(limit=100):
    response = requests.get(
        f"https://discord.com/api/v9/channels/{Config.CHANNEL_ID}/messages?limit={limit}",
        headers={"Authorization": Config.TOKEN},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def message_complete_for_job(message, job_id):
    content = str(message.get("content") or "")
    if f"ID_{job_id}" not in content:
        return False
    if not message.get("attachments"):
        return False
    if "Waiting to start" in content or "queued" in content.lower():
        return False
    percent = re.findall(r"\((\d{1,3})%\)|\b(\d{1,3})%", content)
    for pair in percent:
        values = [int(v) for v in pair if v]
        if values and max(values) < 100:
            return False
    return True


def download_grid(message, job, run_dir):
    attachment = message["attachments"][0]
    url = attachment.get("url") or attachment.get("proxy_url")
    if not url:
        return None
    filename = f"{job['scheme']}_{job['asset_type']}_grid.png"
    path = Path(run_dir) / filename
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    path.write_bytes(response.content)
    try:
        with Image.open(path) as img:
            img.verify()
    except Exception:
        path.unlink(missing_ok=True)
        raise
    append_log(
        {
            "Timestamp": dt.datetime.now().isoformat(timespec="seconds"),
            "Job_ID": job["job_id"],
            "Scheme": job["name"],
            "Asset_Type": job["asset_type"],
            "Prompt": job["prompt"],
            "Status": "GRID_DOWNLOADED",
            "Grid_Path": str(path),
            "Message_ID": str(message.get("id") or ""),
        }
    )
    print(f"[EtsyBrandMJ] {job['job_id']} grid downloaded -> {path}")
    return path


def poll_jobs(jobs, run_dir, timeout=360):
    pending = {job["job_id"]: job for job in jobs if job.get("status") == "SUBMITTED"}
    deadline = time.time() + timeout
    downloaded = {}
    while pending and time.time() < deadline:
        try:
            messages = fetch_messages(100)
        except Exception as exc:
            print(f"[EtsyBrandMJ] message fetch failed: {exc}")
            time.sleep(8)
            continue
        for message in messages:
            for job_id, job in list(pending.items()):
                if message_complete_for_job(message, job_id):
                    try:
                        downloaded[job_id] = download_grid(message, job, run_dir)
                        del pending[job_id]
                    except Exception as exc:
                        print(f"[EtsyBrandMJ] download failed for {job_id}: {exc}")
        if pending:
            print(f"[EtsyBrandMJ] waiting for {len(pending)} grids...")
            time.sleep(10)
    for job_id, job in pending.items():
        append_log(
            {
                "Timestamp": dt.datetime.now().isoformat(timespec="seconds"),
                "Job_ID": job_id,
                "Scheme": job["name"],
                "Asset_Type": job["asset_type"],
                "Prompt": job["prompt"],
                "Status": "POLL_TIMEOUT",
                "Grid_Path": "",
                "Message_ID": "",
            }
        )
    return downloaded


def make_contact_sheet(run_dir):
    paths = sorted(Path(run_dir).glob("*_grid.png"))
    if not paths:
        return None
    thumbs = []
    for path in paths:
        with Image.open(path).convert("RGB") as img:
            img.thumbnail((520, 260))
            canvas = Image.new("RGB", (540, 310), "white")
            x = (540 - img.width) // 2
            y = 10
            canvas.paste(img, (x, y))
            draw = ImageDraw.Draw(canvas)
            label = path.stem.replace("_grid", "").replace("_", " ").upper()
            draw.text((16, 280), label, fill=(0, 0, 0))
            thumbs.append(canvas)
    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 540, rows * 310), (245, 245, 245))
    for idx, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((idx % cols) * 540, (idx // cols) * 310))
    out = Path(run_dir) / "etsy_brand_contact_sheet.jpg"
    sheet.save(out, quality=92)
    print(f"[EtsyBrandMJ] contact sheet -> {out}")
    return out


def write_prompt_manifest(run_dir, jobs):
    manifest = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "schemes": SCHEMES,
        "jobs": jobs,
    }
    path = Path(run_dir) / "etsy_brand_mj_manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=360)
    parser.add_argument("--no-send", action="store_true")
    args = parser.parse_args()

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    run_dir = OUTPUT_ROOT / now_slug()
    run_dir.mkdir(parents=True, exist_ok=True)
    _validate_runtime_config()
    nonce = dt.datetime.now().strftime("%H%M%S")
    jobs = build_jobs(args.limit or None)
    if args.no_send:
        write_prompt_manifest(run_dir, jobs)
        print(run_dir)
        return
    submitted = []
    for idx, job in enumerate(jobs, 1):
        submitted.append(send_job(job, run_dir, f"{nonce}_{idx:02d}"))
        time.sleep(4)
    write_prompt_manifest(run_dir, submitted)
    poll_jobs(submitted, run_dir, args.timeout)
    make_contact_sheet(run_dir)
    print(f"[EtsyBrandMJ] done: {run_dir}")


if __name__ == "__main__":
    main()
