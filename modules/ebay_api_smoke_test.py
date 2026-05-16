from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config
from modules.ebay_token_manager import EbayTokenError, get_access_token

DATABASE = ROOT / "Database"
STATUS_JSON = DATABASE / "eBay_API_Status.json"
STATUS_LOG = DATABASE / "eBay_API_Status_Log.csv"
OAUTH_TOKEN_FILE = DATABASE / ".ebay_oauth_tokens.json"
NY_TZ = ZoneInfo("America/New_York")


def now_et() -> str:
    return datetime.now(NY_TZ).isoformat(timespec="seconds")


def redact_token(token: str | None) -> str:
    if not token:
        return ""
    return f"{token[:4]}...{token[-4:]}" if len(token) >= 12 else "***"


def load_best_token() -> tuple[str, str]:
    try:
        token = get_access_token()
        if token:
            return token, "Database/.ebay_oauth_tokens.json:auto_refresh"
    except EbayTokenError:
        pass
    if OAUTH_TOKEN_FILE.exists():
        try:
            data = json.loads(OAUTH_TOKEN_FILE.read_text(encoding="utf-8"))
            token = str(data.get("access_token") or "").strip()
            if token:
                return token, "Database/.ebay_oauth_tokens.json"
        except Exception:
            pass
    return Config.EBAY_SELLER_TOKEN, ".env"


def safe_json(response: requests.Response) -> Any:
    try:
        return response.json()
    except Exception:
        return response.text[:1000]


def probe(name: str, method: str, path: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    url = Config.EBAY_API_BASE_URL.rstrip("/") + path
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    started = datetime.now(NY_TZ)
    try:
        response = requests.request(method, url, headers=headers, params=params, timeout=45)
        elapsed_ms = int((datetime.now(NY_TZ) - started).total_seconds() * 1000)
        body = safe_json(response)
        return {
            "name": name,
            "url": url,
            "status_code": response.status_code,
            "ok": 200 <= response.status_code < 300,
            "elapsed_ms": elapsed_ms,
            "error_id": extract_error_id(body),
            "message": extract_message(body),
            "body_sample": body if response.status_code >= 400 else summarize_success(name, body),
        }
    except Exception as exc:
        elapsed_ms = int((datetime.now(NY_TZ) - started).total_seconds() * 1000)
        return {
            "name": name,
            "url": url,
            "status_code": 0,
            "ok": False,
            "elapsed_ms": elapsed_ms,
            "error_id": type(exc).__name__,
            "message": str(exc),
            "body_sample": "",
        }


def extract_error_id(body: Any) -> str:
    if isinstance(body, dict):
        errors = body.get("errors")
        if isinstance(errors, list) and errors:
            return str(errors[0].get("errorId") or errors[0].get("error_id") or "")
        return str(body.get("error") or body.get("errorId") or "")
    return ""


def extract_message(body: Any) -> str:
    if isinstance(body, dict):
        errors = body.get("errors")
        if isinstance(errors, list) and errors:
            return str(errors[0].get("message") or errors[0].get("longMessage") or "")
        return str(body.get("error_description") or body.get("message") or "")
    return str(body)[:300]


def summarize_success(name: str, body: Any) -> Any:
    if not isinstance(body, dict):
        return str(body)[:300]
    if name == "inventory_items":
        return {
            "total": body.get("total"),
            "size": body.get("size"),
            "limit": body.get("limit"),
        }
    if name.endswith("_policies"):
        key = next((k for k in body if k.endswith("Policies")), "")
        values = body.get(key) if key else None
        return {key or "policy_container": len(values) if isinstance(values, list) else None}
    return {k: body.get(k) for k in list(body)[:5]}


def write_log(status: dict[str, Any]) -> None:
    DATABASE.mkdir(exist_ok=True)
    STATUS_JSON.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    exists = STATUS_LOG.exists()
    with STATUS_LOG.open("a", encoding="utf-8", newline="") as handle:
        fields = [
            "timestamp_et",
            "token_present",
            "token_redacted",
            "overall",
            "probe",
            "status_code",
            "ok",
            "elapsed_ms",
            "error_id",
            "message",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        if not exists:
            writer.writeheader()
        for item in status.get("probes", []):
            writer.writerow(
                {
                    "timestamp_et": status["timestamp_et"],
                    "token_present": status["token_present"],
                    "token_redacted": status["token_redacted"],
                    "overall": status["overall"],
                    "probe": item["name"],
                    "status_code": item["status_code"],
                    "ok": item["ok"],
                    "elapsed_ms": item["elapsed_ms"],
                    "error_id": item.get("error_id", ""),
                    "message": item.get("message", ""),
                }
            )


def main() -> int:
    token, token_source = load_best_token()
    status: dict[str, Any] = {
        "timestamp_et": now_et(),
        "token_present": bool(token),
        "token_redacted": redact_token(token),
        "token_source": token_source,
        "overall": "NOT_TESTED",
        "probes": [],
        "notes": [],
    }
    if not token:
        status["overall"] = "MISSING_TOKEN"
        status["notes"].append("Set EBAY_SELLER_TOKEN or eBay_seller_token in .env.")
        write_log(status)
        print("[EBAY-API] missing token")
        return 2

    tests = [
        ("inventory_items", "GET", "/sell/inventory/v1/inventory_item", {"limit": 1}),
        ("marketing_campaigns", "GET", "/sell/marketing/v1/ad_campaign", {"limit": 10}),
        ("fulfillment_policies", "GET", "/sell/account/v1/fulfillment_policy", {"marketplace_id": "EBAY_US"}),
        ("payment_policies", "GET", "/sell/account/v1/payment_policy", {"marketplace_id": "EBAY_US"}),
        ("return_policies", "GET", "/sell/account/v1/return_policy", {"marketplace_id": "EBAY_US"}),
    ]
    for name, method, path, params in tests:
        result = probe(name, method, path, token, params)
        status["probes"].append(result)
        print(f"[EBAY-API] {name} status={result['status_code']} ok={result['ok']} msg={result.get('message','')[:160]}")

    ok_count = sum(1 for item in status["probes"] if item["ok"])
    if ok_count == len(status["probes"]):
        status["overall"] = "OK_ALL_READ_PROBES"
    elif ok_count:
        status["overall"] = "PARTIAL_OK_CHECK_SCOPES"
    else:
        status["overall"] = "FAILED_CHECK_TOKEN_OR_KEYSET"
    write_log(status)
    return 0 if ok_count else 1


if __name__ == "__main__":
    raise SystemExit(main())
