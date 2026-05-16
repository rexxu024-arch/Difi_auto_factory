from __future__ import annotations

import base64
import json
import secrets
import sys
import time
import urllib.parse
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Event
from typing import Any
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config


DATABASE = ROOT / "Database"
TOKEN_FILE = DATABASE / ".ebay_oauth_tokens.json"
STATE_FILE = DATABASE / ".ebay_oauth_state.json"
NY_TZ = ZoneInfo("America/New_York")

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


def now_et() -> str:
    return datetime.now(NY_TZ).isoformat(timespec="seconds")


def require_config() -> None:
    missing = []
    if not Config.EBAY_CLIENT_ID:
        missing.append("EBAY_CLIENT_ID")
    if not Config.EBAY_CLIENT_SECRET:
        missing.append("EBAY_CLIENT_SECRET")
    if not Config.EBAY_REDIRECT_URI:
        missing.append("EBAY_RUNAME or EBAY_REDIRECT_URI")
    if missing:
        raise SystemExit(f"Missing eBay OAuth config: {', '.join(missing)}")


def auth_url(scopes: list[str] | None = None, state: str | None = None) -> str:
    require_config()
    state = state or secrets.token_urlsafe(24)
    STATE_FILE.write_text(json.dumps({"state": state, "created_at_et": now_et()}, indent=2), encoding="utf-8")
    params = {
        "client_id": Config.EBAY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": Config.EBAY_REDIRECT_URI,
        "scope": " ".join(scopes or DEFAULT_SCOPES),
        "state": state,
        "prompt": "login",
    }
    return "https://auth.ebay.com/oauth2/authorize?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def basic_auth_header() -> str:
    raw = f"{Config.EBAY_CLIENT_ID}:{Config.EBAY_CLIENT_SECRET}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def exchange_code(code: str) -> dict[str, Any]:
    require_config()
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {
        "Authorization": basic_auth_header(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": Config.EBAY_REDIRECT_URI,
    }
    response = requests.post(url, headers=headers, data=data, timeout=60)
    body = response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
    if response.status_code >= 400:
        raise RuntimeError(f"eBay token exchange failed {response.status_code}: {body}")
    body["saved_at_et"] = now_et()
    body["scope"] = str(body.get("scope") or " ".join(DEFAULT_SCOPES))
    if "expires_in" in body:
        body["access_token_expires_at_et"] = (datetime.now(NY_TZ) + timedelta(seconds=int(body["expires_in"]) - 60)).isoformat(timespec="seconds")
    if "refresh_token_expires_in" in body:
        body["refresh_token_expires_at_et"] = (datetime.now(NY_TZ) + timedelta(seconds=int(body["refresh_token_expires_in"]) - 60)).isoformat(timespec="seconds")
    TOKEN_FILE.write_text(json.dumps(body, indent=2), encoding="utf-8")
    print(f"[EBAY-OAUTH] saved token file={TOKEN_FILE}")
    print(f"[EBAY-OAUTH] access_token_present={bool(body.get('access_token'))} refresh_token_present={bool(body.get('refresh_token'))}")
    return body


class CallbackHandler(BaseHTTPRequestHandler):
    server_version = "OpenClawEbayOAuth/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        return

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        code = (qs.get("code") or [""])[0]
        state = (qs.get("state") or [""])[0]
        expected = ""
        if STATE_FILE.exists():
            try:
                expected = json.loads(STATE_FILE.read_text(encoding="utf-8")).get("state", "")
            except Exception:
                expected = ""
        if expected and state != expected:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"eBay OAuth state mismatch. Close this tab and retry.")
            self.server.result = {"error": "state_mismatch", "state": state}
            self.server.done.set()
            return
        if not code:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing eBay OAuth code.")
            self.server.result = {"error": "missing_code", "query": qs}
            self.server.done.set()
            return
        try:
            token = exchange_code(code)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"eBay OAuth success. You can close this tab.")
            self.server.result = {"ok": True, "token_present": bool(token.get("access_token"))}
        except Exception as exc:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(exc).encode("utf-8", errors="replace"))
            self.server.result = {"error": str(exc)}
        self.server.done.set()


class OAuthServer(HTTPServer):
    done: Event
    result: dict[str, Any]


def serve_callback(port: int = 8777, timeout_seconds: int = 300) -> int:
    url = auth_url()
    print("[EBAY-OAUTH] Open this URL in the browser and grant access:")
    print(url)
    server = OAuthServer(("127.0.0.1", port), CallbackHandler)
    server.done = Event()
    server.result = {}
    server.timeout = 1
    deadline = time.time() + timeout_seconds
    print(f"[EBAY-OAUTH] waiting for callback on http://localhost:{port}/ ...")
    while time.time() < deadline and not server.done.is_set():
        server.handle_request()
    server.server_close()
    if not server.result:
        print("[EBAY-OAUTH] timeout waiting for callback")
        return 2
    print("[EBAY-OAUTH] result=", json.dumps(server.result, ensure_ascii=False))
    return 0 if server.result.get("ok") else 1


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if "--url" in argv:
        print(auth_url())
        return 0
    if "--exchange-code" in argv:
        idx = argv.index("--exchange-code")
        code = argv[idx + 1]
        exchange_code(code)
        return 0
    port = 8777
    if "--port" in argv:
        port = int(argv[argv.index("--port") + 1])
    return serve_callback(port=port)


if __name__ == "__main__":
    raise SystemExit(main())
