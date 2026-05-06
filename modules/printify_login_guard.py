"""Recover or verify the Printify CDP browser login.

The guard never stores passwords and never chooses an unknown Google account.
It relies on the existing Chrome remote-debug profile and the saved Google
session. If Printify asks for a password or a different Google account, it
stops and records a manual-login requirement.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.printify_mockup_ui_uploader import CdpPage


CHROME_DEBUG_URL = "http://127.0.0.1:9222"
DATABASE_DIR = PROJECT_ROOT / "Database"
STATUS_JSON = DATABASE_DIR / "Printify_Login_Status.json"
RUN_LOG = DATABASE_DIR / "Printify_Login_Guard.log"


def now_text() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def clean(value: object) -> str:
    return str(value or "").strip()


def append_log(message: str) -> None:
    DATABASE_DIR.mkdir(exist_ok=True)
    with RUN_LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"[{now_text()}] {message}\n")


def write_status(status: str, detail: str, url: str = "") -> dict[str, str]:
    payload = {
        "timestamp": now_text(),
        "status": status,
        "detail": detail,
        "url": url,
        "allowed_google_email": Config.PRINTIFY_LOGIN_EMAIL,
    }
    STATUS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    append_log(f"{status}: {detail} {url}")
    return payload


def list_pages() -> list[dict]:
    with urllib.request.urlopen(f"{CHROME_DEBUG_URL}/json/list", timeout=10) as response:
        return json.load(response)


def new_tab(url: str) -> dict:
    request = urllib.request.Request(f"{CHROME_DEBUG_URL}/json/new", data=url.encode("utf-8"), method="PUT")
    return json.loads(urllib.request.urlopen(request, timeout=10).read().decode("utf-8", "ignore"))


def find_printify_page() -> dict | None:
    pages = list_pages()
    app_pages = [
        page
        for page in pages
        if page.get("type") == "page"
        and "printify.com" in clean(page.get("url"))
        and page.get("webSocketDebuggerUrl")
    ]
    if app_pages:
        app_pages.sort(key=lambda page: ("/app/" not in clean(page.get("url")), clean(page.get("url"))))
        return app_pages[0]
    tab = new_tab("https://printify.com/app/dashboard")
    return tab if tab.get("webSocketDebuggerUrl") else None


async def page_snapshot(page: CdpPage) -> dict[str, str]:
    return await page.eval(
        r"""(() => ({
            url: location.href,
            title: document.title || '',
            text: ((document.body && document.body.innerText) || '').slice(0, 4000)
        }))()"""
    )


def is_logged_in(snapshot: dict[str, str]) -> bool:
    url = clean(snapshot.get("url"))
    text = clean(snapshot.get("text"))
    if "printify.com/app/" in url and "/auth/login" not in url:
        if "Log in" not in text[:300] and "Continue with Google" not in text:
            return True
    return False


async def click_printify_google(page: CdpPage) -> bool:
    return bool(
        await page.eval(
            r"""(() => {
                const visible = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
                const candidates = [...document.querySelectorAll('button,a,div[role="button"]')]
                    .filter(visible)
                    .filter(e => /google/i.test((e.innerText || e.ariaLabel || '').trim()));
                const button = candidates[0];
                if (!button) return false;
                button.click();
                return true;
            })()"""
        )
    )


async def click_allowed_google_account(page: CdpPage, email: str) -> str:
    escaped = json.dumps(email)
    result = await page.eval(
        r"""((email) => {
            const visible = e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
            const text = (document.body && document.body.innerText) || '';
            if (/Enter your password|Forgot password/i.test(text)) return 'PASSWORD_REQUIRED';
            const nodes = [...document.querySelectorAll('div[role="link"], div[role="button"], button, a')]
              .filter(visible);
            const exact = nodes.find(e => ((e.innerText || '').toLowerCase()).includes(email.toLowerCase()));
            if (exact) {
                exact.click();
                return 'CLICKED_ALLOWED_ACCOUNT';
            }
            if (/choose an account|sign in with google|accounts\.google/i.test(text)) {
                const accountTexts = nodes.map(e => (e.innerText || '').trim()).filter(Boolean).join(' | ');
                return 'ALLOWED_ACCOUNT_NOT_VISIBLE: ' + accountTexts.slice(0, 500);
            }
            return 'NO_GOOGLE_ACCOUNT_CHOOSER';
        })(""" + escaped + """)"""
    )
    return clean(result)


async def recover_login(timeout: int = 90, dry_run: bool = False) -> dict[str, str]:
    if not Config.PRINTIFY_LOGIN_EMAIL:
        return write_status("BLOCKED_MISSING_EMAIL", "PRINTIFY_LOGIN_EMAIL is not configured.")
    page_info = find_printify_page()
    if not page_info:
        return write_status("UNAVAILABLE", "No CDP Printify page and could not create one.")
    async with CdpPage(page_info["webSocketDebuggerUrl"]) as page:
        await page.navigate("https://printify.com/app/dashboard")
        await asyncio.sleep(5)
        snap = await page_snapshot(page)
        if is_logged_in(snap):
            return write_status("LOGGED_IN", "Printify dashboard is available.", clean(snap.get("url")))
        if dry_run:
            return write_status("LOGIN_REQUIRED", "Dry run stopped before Google login attempt.", clean(snap.get("url")))

        clicked = await click_printify_google(page)
        if not clicked:
            snap = await page_snapshot(page)
            return write_status("MANUAL_LOGIN_REQUIRED", "Could not find Printify Google login button.", clean(snap.get("url")))

        deadline = time.time() + timeout
        account_action = ""
        while time.time() < deadline:
            await asyncio.sleep(3)
            snap = await page_snapshot(page)
            url = clean(snap.get("url"))
            if is_logged_in(snap):
                return write_status("LOGGED_IN", "Recovered Printify login through saved Google session.", url)
            if "accounts.google.com" in url:
                account_action = await click_allowed_google_account(page, Config.PRINTIFY_LOGIN_EMAIL)
                if account_action.startswith("PASSWORD_REQUIRED") or account_action.startswith("ALLOWED_ACCOUNT_NOT_VISIBLE"):
                    return write_status("MANUAL_LOGIN_REQUIRED", account_action, url)
        snap = await page_snapshot(page)
        return write_status("TIMEOUT", f"Login recovery timed out. Last account action: {account_action}", clean(snap.get("url")))


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify or recover Printify login in Chrome CDP profile.")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = asyncio.run(recover_login(timeout=args.timeout, dry_run=args.dry_run))
    print(f"[PRINTIFY-LOGIN] {result['status']} {result['detail']}")
    if result["status"] != "LOGGED_IN":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
