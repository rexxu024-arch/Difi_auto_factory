import argparse
import base64
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.resilient_http import request_with_retry

AUTH_URL = "https://www.etsy.com/oauth/connect"
TOKEN_URL = "https://api.etsy.com/v3/public/oauth/token"


def _token_path():
    return Path(Config.ETSY_TOKEN_FILE)


def _state_path():
    return Path(Config.ETSY_STATE_FILE)


def _validate_credentials():
    missing = []
    if not Config.ETSY_KEYSTRING:
        missing.append("ETSY_KEYSTRING / Etsy_Key_string")
    if not Config.ETSY_SHARED_SECRET:
        missing.append("ETSY_SHARED_SECRET / Etsy_shared_secret")
    if missing:
        raise RuntimeError("Missing Etsy API credentials in .env: " + ", ".join(missing))


def _b64url(data):
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def generate_pkce():
    verifier = _b64url(secrets.token_bytes(64))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def save_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def load_json(path):
    path = Path(path)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def make_authorize_url():
    _validate_credentials()
    verifier, challenge = generate_pkce()
    state = secrets.token_urlsafe(24)
    payload = {
        "state": state,
        "code_verifier": verifier,
        "created_at": int(time.time()),
        "redirect_uri": Config.ETSY_REDIRECT_URI,
        "scopes": Config.ETSY_SCOPES,
    }
    save_json(_state_path(), payload)
    params = {
        "response_type": "code",
        "redirect_uri": Config.ETSY_REDIRECT_URI,
        "scope": Config.ETSY_SCOPES,
        "client_id": Config.ETSY_KEYSTRING,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return AUTH_URL + "?" + urllib.parse.urlencode(params)


def exchange_code(code, state):
    _validate_credentials()
    stored = load_json(_state_path())
    if not stored or stored.get("state") != state:
        raise RuntimeError("Etsy OAuth state mismatch; refusing token exchange.")
    data = {
        "grant_type": "authorization_code",
        "client_id": Config.ETSY_KEYSTRING,
        "redirect_uri": stored["redirect_uri"],
        "code": code,
        "code_verifier": stored["code_verifier"],
    }
    response = request_with_retry("POST", TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=30)
    if response.status_code >= 400:
        raise RuntimeError(f"Etsy token exchange failed HTTP {response.status_code}: {response.text[:500]}")
    token = response.json()
    persist_token(token)
    return token


def refresh_access_token(refresh_token=None):
    _validate_credentials()
    current = load_json(_token_path())
    refresh_token = refresh_token or current.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("No Etsy refresh_token available. Run OAuth authorization first.")
    response = request_with_retry(
        "POST",
        TOKEN_URL,
        data={"grant_type": "refresh_token", "client_id": Config.ETSY_KEYSTRING, "refresh_token": refresh_token},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"Etsy token refresh failed HTTP {response.status_code}: {response.text[:500]}")
    token = response.json()
    persist_token(token)
    return token


def persist_token(token):
    now = int(time.time())
    payload = {
        "access_token": token.get("access_token"),
        "refresh_token": token.get("refresh_token"),
        "token_type": token.get("token_type", "Bearer"),
        "expires_in": int(token.get("expires_in") or 3600),
        "expires_at": now + int(token.get("expires_in") or 3600) - 120,
        "obtained_at": now,
    }
    if not payload["access_token"] or not payload["refresh_token"]:
        raise RuntimeError("Etsy token response missing access_token or refresh_token.")
    save_json(_token_path(), payload)
    try:
        _state_path().unlink(missing_ok=True)
    except Exception:
        pass
    print(f"[ETSY-AUTH] token saved: {_token_path()} expires_in={payload['expires_in']}s")
    return payload


def get_valid_token(force_refresh=False):
    token = load_json(_token_path())
    if not token:
        raise RuntimeError("No Etsy OAuth token stored. Run `py modules\\etsy_auth.py auth-url` and authorize first.")
    if force_refresh or int(token.get("expires_at") or 0) <= int(time.time()):
        token = refresh_access_token(token.get("refresh_token"))
    return token["access_token"]


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    server_version = "OpenClawEtsyOAuth/1.0"

    def log_message(self, format, *args):
        return

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        error = query.get("error", [""])[0]
        if error:
            body = f"Etsy OAuth error: {error} {query.get('error_description', [''])[0]}"
            self.send_response(400)
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
            self.server.result = {"error": body}
            return
        code = query.get("code", [""])[0]
        state = query.get("state", [""])[0]
        if not code or not state:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing code/state.")
            return
        try:
            exchange_code(code, state)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Etsy OAuth connected. You may close this tab.")
            self.server.result = {"ok": True}
        except Exception as exc:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(exc).encode("utf-8"))
            self.server.result = {"error": str(exc)}


def listen_callback(timeout=300):
    parsed = urllib.parse.urlparse(Config.ETSY_REDIRECT_URI)
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if host not in {"localhost", "127.0.0.1"}:
        raise RuntimeError("Automatic local callback only supports localhost redirect URIs. Use `exchange --code ... --state ...` for non-local redirects.")
    server = HTTPServer((host, port), OAuthCallbackHandler)
    server.timeout = 1
    server.result = None
    deadline = time.time() + timeout
    print(f"[ETSY-AUTH] waiting for OAuth callback on {Config.ETSY_REDIRECT_URI}")
    while time.time() < deadline and not server.result:
        server.handle_request()
    server.server_close()
    if not server.result:
        raise TimeoutError("Timed out waiting for Etsy OAuth callback.")
    if server.result.get("error"):
        raise RuntimeError(server.result["error"])
    return True


def main():
    parser = argparse.ArgumentParser(description="Etsy OAuth 2.0 PKCE helper.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("auth-url")
    listen = sub.add_parser("listen")
    listen.add_argument("--timeout", type=int, default=300)
    exchange = sub.add_parser("exchange")
    exchange.add_argument("--code", required=True)
    exchange.add_argument("--state", required=True)
    sub.add_parser("refresh")
    sub.add_parser("status")
    args = parser.parse_args()
    if args.cmd == "auth-url":
        print(make_authorize_url())
    elif args.cmd == "listen":
        listen_callback(args.timeout)
    elif args.cmd == "exchange":
        exchange_code(args.code, args.state)
    elif args.cmd == "refresh":
        refresh_access_token()
    elif args.cmd == "status":
        _validate_credentials()
        token = load_json(_token_path())
        print(json.dumps({
            "credentials_present": True,
            "token_present": bool(token.get("access_token")),
            "refresh_present": bool(token.get("refresh_token")),
            "expires_at": token.get("expires_at"),
            "seconds_remaining": int(token.get("expires_at") or 0) - int(time.time()) if token else None,
            "redirect_uri": Config.ETSY_REDIRECT_URI,
            "scopes": Config.ETSY_SCOPES,
            "token_file": str(_token_path()),
        }, indent=2))


if __name__ == "__main__":
    main()
