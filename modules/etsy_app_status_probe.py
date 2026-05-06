"""Probe Etsy app/API readiness without OAuth or listing writes."""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.resilient_http import request_with_retry


DATABASE_DIR = PROJECT_ROOT / "Database"
STATUS_JSON = DATABASE_DIR / "Etsy_API_Status.json"
STATUS_CSV = DATABASE_DIR / "Etsy_API_Status_Log.csv"
PING_URL = "https://api.etsy.com/v3/application/openapi-ping"


def now_text() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %z")


def _masked(value: str | None) -> str:
    value = str(value or "")
    if len(value) <= 8:
        return "present" if value else ""
    return value[:4] + "..." + value[-4:]


def probe() -> dict[str, object]:
    result: dict[str, object] = {
        "timestamp": now_text(),
        "credentials_present": bool(Config.ETSY_KEYSTRING and Config.ETSY_SHARED_SECRET),
        "keystring_masked": _masked(Config.ETSY_KEYSTRING),
        "status": "UNKNOWN",
        "http_status": None,
        "detail": "",
        "oauth_next_step": "WAIT_APP_APPROVAL",
    }
    if not result["credentials_present"]:
        result["status"] = "MISSING_CREDENTIALS"
        result["detail"] = "ETSY_KEYSTRING/ETSY_SHARED_SECRET missing in environment."
        return result
    try:
        response = request_with_retry(
            "GET",
            PING_URL,
            headers={"x-api-key": Config.ETSY_KEYSTRING, "Accept": "application/json"},
            timeout=30,
            attempts=2,
            backoff=2.0,
        )
        result["http_status"] = response.status_code
        result["detail"] = response.text[:500]
        if response.status_code == 200:
            result["status"] = "API_KEY_ACTIVE"
            result["oauth_next_step"] = "RUN_OAUTH_PKCE"
        elif response.status_code == 403:
            result["status"] = "PENDING_OR_INACTIVE"
            result["oauth_next_step"] = "WAIT_APP_APPROVAL_OR_VERIFY_SECRET"
        else:
            result["status"] = f"HTTP_{response.status_code}"
    except Exception as exc:  # noqa: BLE001
        result["status"] = "ERROR"
        result["detail"] = str(exc)[:500]
    return result


def write_outputs(result: dict[str, object]) -> None:
    DATABASE_DIR.mkdir(exist_ok=True)
    STATUS_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    exists = STATUS_CSV.exists()
    fields = ["timestamp", "status", "http_status", "oauth_next_step", "credentials_present", "keystring_masked", "detail"]
    with STATUS_CSV.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow({field: result.get(field, "") for field in fields})


def main() -> None:
    result = probe()
    write_outputs(result)
    print(f"[ETSY-APP] status={result['status']} http={result.get('http_status')} next={result['oauth_next_step']}")
    print(f"[ETSY-APP] json={STATUS_JSON}")
    if result["status"] not in {"API_KEY_ACTIVE", "PENDING_OR_INACTIVE"}:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
