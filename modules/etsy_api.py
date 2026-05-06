import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.etsy_auth import get_valid_token
from modules.resilient_http import request_with_retry

API_BASE = "https://api.etsy.com/v3/application"


def api_key_header():
    if not Config.ETSY_KEYSTRING or not Config.ETSY_SHARED_SECRET:
        raise RuntimeError("Missing Etsy API credentials in .env.")
    return f"{Config.ETSY_KEYSTRING}:{Config.ETSY_SHARED_SECRET}"


def headers(oauth=True):
    data = {"x-api-key": api_key_header(), "Accept": "application/json"}
    if oauth:
        data["Authorization"] = f"Bearer {get_valid_token()}"
    return data


def request(method, path, *, params=None, data=None, json_body=None, files=None, oauth=True):
    url = path if str(path).startswith("http") else API_BASE + path
    request_headers = headers(oauth=oauth)
    if files:
        request_headers.pop("Content-Type", None)
    elif json_body is not None:
        request_headers["Content-Type"] = "application/json"
    else:
        request_headers["Content-Type"] = "application/x-www-form-urlencoded"
    response = request_with_retry(method, url, headers=request_headers, params=params, data=data, json=json_body, files=files, timeout=60)
    if response.status_code == 401 and oauth:
        from modules.etsy_auth import refresh_access_token
        refresh_access_token()
        request_headers = headers(oauth=True)
        if files:
            request_headers.pop("Content-Type", None)
        elif json_body is not None:
            request_headers["Content-Type"] = "application/json"
        else:
            request_headers["Content-Type"] = "application/x-www-form-urlencoded"
        response = request_with_retry(method, url, headers=request_headers, params=params, data=data, json=json_body, files=files, timeout=60)
    if response.status_code >= 400:
        raise RuntimeError(f"Etsy API {method} {path} failed HTTP {response.status_code}: {response.text[:1000]}")
    return response.json() if response.text else {}


def get_me():
    return request("GET", "/users/me")


def get_my_shops():
    me = get_me()
    user_id = me.get("user_id") or me.get("user_id_or_name") or me.get("user", {}).get("user_id")
    if not user_id:
        raise RuntimeError(f"Could not determine Etsy user id from /users/me: {me}")
    return request("GET", f"/users/{user_id}/shops")


def first_shop_id():
    shops = get_my_shops()
    results = shops.get("results") or shops.get("shops") or []
    if not results:
        raise RuntimeError(f"No Etsy shop found for authenticated user: {shops}")
    return results[0].get("shop_id")


def get_shop(shop_id=None):
    shop_id = shop_id or first_shop_id()
    return request("GET", f"/shops/{shop_id}")


def get_shop_listings(shop_id=None, state="active", limit=25):
    shop_id = shop_id or first_shop_id()
    return request("GET", f"/shops/{shop_id}/listings", params={"state": state, "limit": limit})


def smoke_test():
    report = {"credentials": "present"}
    report["me"] = get_me()
    report["shops"] = get_my_shops()
    try:
        report["shop"] = get_shop()
    except Exception as exc:
        report["shop_error"] = str(exc)
    return report


def main():
    parser = argparse.ArgumentParser(description="Etsy API smoke/utility wrapper.")
    parser.add_argument("command", choices=["me", "shops", "shop", "listings", "smoke"])
    parser.add_argument("--shop-id", default="")
    parser.add_argument("--state", default="active")
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()
    if args.command == "me":
        result = get_me()
    elif args.command == "shops":
        result = get_my_shops()
    elif args.command == "shop":
        result = get_shop(args.shop_id or None)
    elif args.command == "listings":
        result = get_shop_listings(args.shop_id or None, state=args.state, limit=args.limit)
    else:
        result = smoke_test()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
