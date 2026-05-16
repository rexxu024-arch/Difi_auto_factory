"""Upload local reference images to Discord and rewrite MJ prompts with URLs.

Midjourney cannot use a Windows filesystem path as an image prompt. For
identity-locked scene work, the source product image must first be uploaded to
Discord so the prompt starts with a real HTTPS image URL. This script performs
that bridge and updates the dispatch queue in-place.
"""

from __future__ import annotations

import argparse
import csv
import json
import mimetypes
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import mj_harvest


QUEUE = PROJECT_ROOT / "Database" / "MJ_Identity_Locked_Scene_Dispatch_Queue.csv"
NY_TZ = ZoneInfo("America/New_York")
LOCAL_IMAGE_RE = re.compile(r"^(?P<path>[A-Za-z]:\\[^\n\r]+?\.(?:png|jpg|jpeg|webp))\s+", re.IGNORECASE)
EXTRA_FIELDS = [
    "Reference_Image_Path",
    "Reference_Image_URL",
    "Reference_Upload_Message_ID",
    "Reference_Uploaded_At_ET",
    "Reference_Upload_Error",
]


def clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def now_et() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %I:%M:%S %p %Z")


def read_rows(queue: Path) -> tuple[list[dict[str, str]], list[str]]:
    with queue.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        for field in EXTRA_FIELDS:
            if field not in fields:
                fields.append(field)
        return list(reader), fields


def write_rows(queue: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with queue.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def local_reference_path(prompt: str) -> Path | None:
    match = LOCAL_IMAGE_RE.search(prompt)
    if not match:
        return None
    path = Path(match.group("path"))
    return path if path.exists() else None


def upload_reference(path: Path, sku: str) -> tuple[str, str]:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    payload = {
        "content": f"OpenClaw MJ reference image for {sku}",
        "attachments": [{"id": "0", "filename": path.name}],
    }
    with path.open("rb") as handle:
        response = mj_harvest.requests.post(
            f"https://discord.com/api/v9/channels/{mj_harvest.Config.CHANNEL_ID}/messages",
            headers={"Authorization": mj_harvest.Config.TOKEN},
            data={"payload_json": json.dumps(payload)},
            files={"files[0]": (path.name, handle, mime)},
            timeout=60,
        )
    response.raise_for_status()
    data = response.json()
    attachments = data.get("attachments") or []
    if not attachments:
        raise RuntimeError("Discord upload response had no attachments")
    return clean(attachments[0].get("url")), clean(data.get("id"))


def rewrite_prompt(prompt: str, url: str) -> str:
    match = LOCAL_IMAGE_RE.search(prompt)
    if not match:
        return prompt
    return url + " " + prompt[match.end():].strip()


def should_prepare(row: dict[str, str], retry_holds: bool) -> bool:
    status = clean(row.get("Dispatch_Status"))
    if status == "READY_FOR_MJ":
        return True
    if not retry_holds:
        return False
    harvest_status = clean(row.get("Harvest_Status"))
    error = clean(row.get("Harvest_Error"))
    return (
        status == "MJ_SUBMITTED"
        and harvest_status == "VISUAL_QA_HOLD_IDENTITY_DRIFT"
        and "local file path was not a true image reference" in error
    )


def reset_for_url_retry(row: dict[str, str]) -> None:
    sku = clean(row.get("Internal_SKU"))
    if not sku.endswith("-URL_REF_RETRY"):
        row["Internal_SKU"] = f"{sku}-URL_REF_RETRY"
    output = clean(row.get("Output_Folder"))
    if output and not output.endswith("_URL_REF_RETRY"):
        row["Output_Folder"] = f"{output}_URL_REF_RETRY"
    row["Dispatch_Status"] = "READY_FOR_MJ"
    for field in (
        "Dispatched_At_ET",
        "Dispatch_Response_Status",
        "Dispatch_Confirm_Message_ID",
        "Dispatch_Error",
        "Harvest_Status",
        "Grid_Message_ID",
        "Grid_File",
        "U1_File",
        "U2_File",
        "U3_File",
        "U4_File",
        "Last_Harvest_ET",
        "Harvest_Error",
        "Grid_Wait_First_ET",
        "Grid_Wait_Attempts",
    ):
        row[field] = ""


def prepare(limit: int, queue: Path = QUEUE, retry_holds: bool = False) -> int:
    mj_harvest._validate_runtime_config()
    rows, fields = read_rows(queue)
    done = 0
    for row in rows:
        if done >= limit:
            break
        if not should_prepare(row, retry_holds):
            continue
        prompt = clean(row.get("MJ_Master_Prompt"))
        if clean(row.get("Reference_Image_URL")).startswith("https://"):
            if retry_holds:
                reset_for_url_retry(row)
                done += 1
                print(f"[MJ-REFERENCE-RETRY-READY] {clean(row.get('Internal_SKU'))} existing_url={clean(row.get('Reference_Image_URL'))}")
                write_rows(queue, rows, fields)
            continue
        path = local_reference_path(prompt)
        if not path:
            row["Reference_Upload_Error"] = "No local image path found at prompt start"
            continue
        sku = clean(row.get("Internal_SKU"))
        try:
            url, message_id = upload_reference(path, sku)
            row["Reference_Image_Path"] = str(path)
            row["Reference_Image_URL"] = url
            row["Reference_Upload_Message_ID"] = message_id
            row["Reference_Uploaded_At_ET"] = now_et()
            row["Reference_Upload_Error"] = ""
            row["MJ_Master_Prompt"] = rewrite_prompt(prompt, url)
            if retry_holds:
                reset_for_url_retry(row)
            done += 1
            print(f"[MJ-REFERENCE-UPLOADED] {sku} url={url}")
            write_rows(queue, rows, fields)
        except Exception as exc:
            row["Reference_Upload_Error"] = repr(exc)[:500]
            print(f"[MJ-REFERENCE-FAILED] {sku}: {exc}")
            write_rows(queue, rows, fields)
            return 1
    print(f"[MJ-REFERENCE-DONE] uploaded={done}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload local MJ reference images and rewrite prompts with HTTPS URLs")
    parser.add_argument("--queue", default=str(QUEUE))
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--retry-holds", action="store_true", help="Turn prior identity-drift rows into URL-reference READY_FOR_MJ retries.")
    args = parser.parse_args()
    return prepare(max(1, args.limit), queue=Path(args.queue), retry_holds=args.retry_holds)


if __name__ == "__main__":
    raise SystemExit(main())
