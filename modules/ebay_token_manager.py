from __future__ import annotations

import argparse
import base64
import csv
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config

try:
    from modules.ebay_oauth_flow import DEFAULT_SCOPES
except Exception:
    DEFAULT_SCOPES = [
        "https://api.ebay.com/oauth/api_scope",
        "https://api.ebay.com/oauth/api_scope/commerce.identity.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.account",
        "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.marketing",
        "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.stores.readonly",
    ]


DATABASE = ROOT / "Database"
TOKEN_FILE = DATABASE / ".ebay_oauth_tokens.json"
REFRESH_LOG = DATABASE / "eBay_OAuth_Refresh_Log.csv"
NY_TZ = ZoneInfo("America/New_York")
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"


class EbayTokenError(RuntimeError):
    pass


def now_et() -> datetime:
    return datetime.now(NY_TZ)


def now_text() -> str:
    return now_et().isoformat(timespec="seconds")


def parse_dt(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=NY_TZ)
    return dt.astimezone(NY_TZ)


def redact(value: str | None) -> str:
    if not value:
        return ""
    return f"{value[:5]}...{value[-5:]}" if len(value) >= 14 else "***"


def read_token_file() -> dict[str, Any]:
    if not TOKEN_FILE.exists():
        return {}
    try:
        return json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        raise EbayTokenError(f"Cannot read eBay token file: {exc}") from exc


def write_token_file(data: dict[str, Any]) -> None:
    DATABASE.mkdir(exist_ok=True)
    temp = TOKEN_FILE.with_suffix(".json.tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp.replace(TOKEN_FILE)


def basic_auth_header() -> str:
    if not Config.EBAY_CLIENT_ID or not Config.EBAY_CLIENT_SECRET:
        raise EbayTokenError("Missing EBAY_CLIENT_ID or EBAY_CLIENT_SECRET for eBay OAuth refresh.")
    raw = f"{Config.EBAY_CLIENT_ID}:{Config.EBAY_CLIENT_SECRET}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def seconds_until(value: datetime | None) -> int | None:
    if not value:
        return None
    return int((value - now_et()).total_seconds())


def token_status() -> dict[str, Any]:
    data = read_token_file()
    access_exp = parse_dt(data.get("access_token_expires_at_et"))
    refresh_exp = parse_dt(data.get("refresh_token_expires_at_et"))
    return {
        "timestamp_et": now_text(),
        "token_file": str(TOKEN_FILE),
        "access_token_present": bool(data.get("access_token")),
        "refresh_token_present": bool(data.get("refresh_token")),
        "access_token_expires_at_et": access_exp.isoformat(timespec="seconds") if access_exp else "",
        "refresh_token_expires_at_et": refresh_exp.isoformat(timespec="seconds") if refresh_exp else "",
        "access_token_seconds_remaining": seconds_until(access_exp),
        "refresh_token_seconds_remaining": seconds_until(refresh_exp),
        "access_token_redacted": redact(str(data.get("access_token") or "")),
        "refresh_token_redacted": redact(str(data.get("refresh_token") or "")),
    }


def log_refresh(status: str, detail: str = "", http_status: int | str = "") -> None:
    DATABASE.mkdir(exist_ok=True)
    exists = REFRESH_LOG.exists()
    with REFRESH_LOG.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp_et", "status", "http_status", "detail"])
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp_et": now_text(),
                "status": status,
                "http_status": http_status,
                "detail": detail[:500],
            }
        )


def refresh_access_token(scopes: list[str] | None = None) -> str:
    data = read_token_file()
    refresh_token = str(data.get("refresh_token") or "").strip()
    if not refresh_token:
        raise EbayTokenError("Missing eBay refresh_token. Run the OAuth consent flow once.")
    refresh_exp = parse_dt(data.get("refresh_token_expires_at_et"))
    if refresh_exp and refresh_exp <= now_et():
        raise EbayTokenError("eBay refresh_token is expired. Rex must run OAuth consent again.")

    headers = {
        "Authorization": basic_auth_header(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    requested_scope = ""
    if scopes is not None:
        payload["scope"] = " ".join(scopes)
        requested_scope = payload["scope"]
    else:
        stored_scope = str(data.get("scope") or "").strip()
        if stored_scope:
            payload["scope"] = stored_scope
            requested_scope = stored_scope

    try:
        response = requests.post(TOKEN_URL, headers=headers, data=payload, timeout=60)
    except Exception as exc:
        log_refresh("ERROR", f"{type(exc).__name__}: {exc}")
        raise EbayTokenError(f"eBay refresh request failed: {exc}") from exc

    body: dict[str, Any]
    try:
        body = response.json()
    except Exception:
        body = {"raw": response.text[:1000]}

    if (
        response.status_code == 400
        and isinstance(body, dict)
        and body.get("error") == "invalid_scope"
        and payload.get("scope")
        and scopes is None
    ):
        # Older token files may contain the originally requested scopes rather
        # than the scopes eBay actually granted. Retrying without a scope lets
        # eBay issue an access token using the refresh token's real grant.
        retry_payload = {key: value for key, value in payload.items() if key != "scope"}
        response = requests.post(TOKEN_URL, headers=headers, data=retry_payload, timeout=60)
        try:
            body = response.json()
        except Exception:
            body = {"raw": response.text[:1000]}
        requested_scope = ""

    if response.status_code >= 400:
        message = json.dumps(body, ensure_ascii=False)[:500]
        log_refresh("FAILED", message, response.status_code)
        raise EbayTokenError(f"eBay token refresh failed {response.status_code}: {message}")

    access_token = str(body.get("access_token") or "").strip()
    if not access_token:
        log_refresh("FAILED", "No access_token in eBay refresh response", response.status_code)
        raise EbayTokenError("eBay refresh response did not include access_token.")

    updated = dict(data)
    updated.update(body)
    updated["refresh_token"] = str(body.get("refresh_token") or data.get("refresh_token") or "")
    updated["scope"] = str(body.get("scope") or data.get("scope") or requested_scope or "")
    updated["saved_at_et"] = now_text()
    expires_in = int(body.get("expires_in") or 7200)
    updated["access_token_expires_at_et"] = (now_et() + timedelta(seconds=max(expires_in - 60, 60))).isoformat(
        timespec="seconds"
    )
    if "refresh_token_expires_in" in body:
        refresh_in = int(body.get("refresh_token_expires_in") or 0)
        if refresh_in:
            updated["refresh_token_expires_at_et"] = (now_et() + timedelta(seconds=max(refresh_in - 60, 60))).isoformat(
                timespec="seconds"
            )
    write_token_file(updated)
    log_refresh("REFRESHED", f"expires_in={expires_in}", response.status_code)
    return access_token


def get_access_token(force_refresh: bool = False, margin_seconds: int = 600) -> str:
    data = read_token_file()
    access_token = str(data.get("access_token") or "").strip()
    access_exp = parse_dt(data.get("access_token_expires_at_et"))
    remaining = seconds_until(access_exp)
    if (
        access_token
        and not force_refresh
        and (remaining is None or remaining > margin_seconds)
    ):
        return access_token
    if data.get("refresh_token"):
        return refresh_access_token()
    if Config.EBAY_SELLER_TOKEN:
        log_refresh("FALLBACK_ENV_TOKEN", "No refresh token file; using env seller token")
        return Config.EBAY_SELLER_TOKEN
    raise EbayTokenError("Missing usable eBay token. Run modules/ebay_oauth_flow.py.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.refresh or args.force:
        token = get_access_token(force_refresh=True, margin_seconds=0)
        status = token_status()
        status["refreshed_access_token_redacted"] = redact(token)
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 0

    status = token_status()
    if not args.status:
        try:
            get_access_token(force_refresh=False)
            status = token_status()
            status["manager_check"] = "OK"
        except Exception as exc:
            status["manager_check"] = f"ERROR: {exc}"
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0 if str(status.get("manager_check", "OK")).startswith("OK") else 1


if __name__ == "__main__":
    raise SystemExit(main())
