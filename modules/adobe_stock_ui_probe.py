"""Probe or upload the curated Adobe Stock pilot through the contributor UI.

The script intentionally separates probing from upload. It uses the local Edge
profile because Adobe Contributor does not expose a public submit API here.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from adobe_stock_isolation import assert_adobe_write_paths
from automation_browser import DEFAULT_PORT, DEFAULT_PROFILE, cdp_status, launch as launch_browser


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "Database"
REVIEW = PROJECT_ROOT / "Review_Packets"
PROGRESS_LOG = PROJECT_ROOT / "PROGRESS_LOG.md"
NY_TZ = ZoneInfo("America/New_York")

STATUS_CSV = DATABASE / "Adobe_Stock_UI_Upload_Status.csv"
REPORT = REVIEW / "Adobe_Stock_UI_Upload_Status_latest.md"
ADOBE_UPLOAD_URL = "https://contributor.stock.adobe.com/en/uploads?upload=1"
CURATED_INDEX_BY_PROFILE = {
    "strict-premium": DATABASE / "Adobe_Stock_Curated_Pilot_strict_premium.csv",
    "broad": DATABASE / "Adobe_Stock_Curated_Pilot.csv",
    "first-submit-7": DATABASE / "Adobe_Stock_First_Submit_7.csv",
}


def now_text() -> str:
    return datetime.now(NY_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def edge_user_data_dir() -> Path:
    return Path.home() / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data"


def curated_files(profile: str) -> tuple[list[Path], Path]:
    source_index = CURATED_INDEX_BY_PROFILE[profile]
    rows = read_rows(source_index)
    files: list[Path] = []
    for row in rows:
        local = row.get("Local_Path", "")
        if not local:
            continue
        path = PROJECT_ROOT / local
        if path.exists():
            files.append(path)
    return files, source_index


def page_state(body: str) -> str:
    lowered = body.lower()
    if "sign in or create an account" in lowered or "continue with google" in lowered:
        return "NEEDS_ADOBE_LOGIN"
    if "upload your files" in lowered or "uploaded files" in lowered or "drag & drop files" in lowered:
        return "UPLOAD_PAGE_READY"
    return "UNKNOWN_PAGE_STATE"


def write_report(status: str, detail: str, file_count: int, profile: str, source_index: Path) -> None:
    lines = [
        "# Adobe Stock UI Upload Status",
        "",
        f"Generated: {now_text()}",
        "",
        f"- Status: {status}",
        f"- Profile: {profile}",
        f"- Source index: `{source_index.relative_to(PROJECT_ROOT)}`",
        f"- Curated files: {file_count}",
        f"- Detail: {detail}",
        "",
        "## Rex Action",
        "",
        "- NEEDS_ADOBE_LOGIN: open Adobe Contributor in Edge and sign in, then rerun probe.",
        "- UPLOAD_PAGE_READY: run upload only for the small curated or first-submit pack, then visually inspect Adobe's AI disclosure/category/keyword screen before final submit.",
        "",
        "## Guard",
        "",
        "Probe mode never uploads. Upload mode only sets the curated image files into the Adobe Contributor upload input after a logged-in page is detected.",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def append_progress(status: str, detail: str) -> None:
    with PROGRESS_LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"\n- {now_text()}: Adobe Stock UI probe status={status}; {detail}\n")


def inspect_page(page, mode: str, files: list[Path]) -> tuple[str, str, str]:
    page.goto(ADOBE_UPLOAD_URL, wait_until="domcontentloaded", timeout=60_000)
    body = page.locator("body").inner_text(timeout=30_000)
    status = page_state(body)
    detail = "Contributor upload page detected." if status == "UPLOAD_PAGE_READY" else "Adobe login is required in Edge before upload automation."

    uploaded = "false"
    if mode == "upload":
        if status != "UPLOAD_PAGE_READY":
            raise RuntimeError("Adobe Contributor is not logged in; refusing upload.")
        file_input = page.locator("input[type='file']").first
        try:
            file_input.set_input_files([str(path) for path in files], timeout=30_000)
            uploaded = "true"
            detail = f"Set {len(files)} curated image files into Adobe upload input."
        except PlaywrightTimeoutError as exc:
            detail = f"Could not find Adobe file input: {type(exc).__name__}"
            status = "UPLOAD_INPUT_NOT_FOUND"
    return status, detail, uploaded


def run_persistent(mode: str, headless: bool, files: list[Path]) -> tuple[str, str, str]:
    assert_adobe_write_paths((STATUS_CSV, REPORT))
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(edge_user_data_dir()),
            channel="msedge",
            headless=headless,
            viewport={"width": 1400, "height": 900},
        )
        page = context.pages[0] if context.pages else context.new_page()
        status, detail, uploaded = inspect_page(page, mode, files)
        context.close()
        return status, detail, uploaded


def run_cdp(mode: str, files: list[Path], cdp_port: int, launch_cdp: bool) -> tuple[str, str, str]:
    current = cdp_status(cdp_port)
    if current.get("status") != "RUNNING":
        if not launch_cdp:
            return "CDP_NOT_RUNNING", f"Edge CDP is not running on port {cdp_port}.", "false"
        current = launch_browser("edge", cdp_port, DEFAULT_PROFILE, ADOBE_UPLOAD_URL, minimized=False)

    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{cdp_port}")
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = None
        for candidate in context.pages:
            if "contributor.stock.adobe.com" in candidate.url:
                page = candidate
                break
        if page is None:
            page = context.new_page()
        status, detail, uploaded = inspect_page(page, mode, files)
        # Do not close the CDP browser; Rex may need to finish a visible login.
        return status, detail, uploaded


def run(mode: str, headless: bool, profile: str, transport: str, cdp_port: int, launch_cdp: bool) -> dict[str, str]:
    assert_adobe_write_paths((STATUS_CSV, REPORT))
    files, source_index = curated_files(profile)
    if mode == "upload" and not files:
        raise RuntimeError("No curated Adobe files found. Run the Adobe curated/first-submit pack builder first.")

    if transport == "cdp":
        status, detail, uploaded = run_cdp(mode, files, cdp_port, launch_cdp)
    else:
        status, detail, uploaded = run_persistent(mode, headless, files)

    rows = [
        {
            "Checked_At": now_text(),
            "Mode": mode,
            "Profile": profile,
            "Headless": str(headless).lower(),
            "Transport": transport,
            "CDP_Port": str(cdp_port),
            "Status": status,
            "Source_Index": str(source_index.relative_to(PROJECT_ROOT)),
            "Curated_File_Count": str(len(files)),
            "Uploaded_To_Input": uploaded,
            "Detail": detail,
        }
    ]
    write_rows(STATUS_CSV, rows)
    write_report(status, detail, len(files), profile, source_index)
    append_progress(status, detail)
    return rows[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["probe", "upload"], default="probe")
    parser.add_argument("--profile", choices=["strict-premium", "broad", "first-submit-7"], default="strict-premium")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--transport", choices=["persistent", "cdp"], default="persistent")
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--launch-cdp", action="store_true")
    args = parser.parse_args()
    result = run(
        mode=args.mode,
        headless=args.headless,
        profile=args.profile,
        transport=args.transport,
        cdp_port=args.cdp_port,
        launch_cdp=args.launch_cdp,
    )
    print("[ADOBE-UI]", result)


if __name__ == "__main__":
    main()
