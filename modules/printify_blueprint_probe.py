import argparse
import csv
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import Config
from modules.resilient_http import request_with_retry

DATABASE_DIR = PROJECT_ROOT / "Database"
CANDIDATES = DATABASE_DIR / "Product_Blueprint_Scholar_Verification.csv"
DETAILS_CSV = DATABASE_DIR / "Product_Blueprint_Official_Details.csv"
RAW_DIR = DATABASE_DIR / "Printify_Catalog_Raw"

HEADERS = [
    "Product_Family",
    "Priority",
    "Blueprint_ID",
    "Blueprint_Title",
    "Provider_ID",
    "Provider_Title",
    "Variant_ID",
    "Variant_Title",
    "Variant_Options",
    "Cost_Cents",
    "Suggested_Retail_Cents",
    "Print_Area",
    "US_Shipping_First_Cents",
    "US_Shipping_Additional_Cents",
    "Shipping_Profile",
    "Decision",
    "Probe_Status",
    "Probe_Timestamp",
]


def _headers():
    return {"Authorization": f"Bearer {Config.Printify_API_KEY}"}


def _get(path, cache_name):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = RAW_DIR / cache_name
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    url = f"{Config.Printify_API_URL.rstrip('/')}{path}"
    response = request_with_retry("GET", url, headers=_headers(), timeout=35, attempts=3)
    response.raise_for_status()
    data = response.json()
    cache_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def _items(data, *keys):
    if isinstance(data, list):
        return data
    for key in keys:
        value = data.get(key) if isinstance(data, dict) else None
        if isinstance(value, list):
            return value
    if isinstance(data, dict) and isinstance(data.get("data"), list):
        return data["data"]
    return []


def _clean(value):
    return str(value or "").strip()


def _cost(variant):
    for key in ("cost", "price", "cost_cents", "suggested_retail_price"):
        value = variant.get(key)
        if isinstance(value, (int, float)):
            return int(value)
    return ""


def _retail(variant):
    for key in ("recommended_retail_price", "suggested_retail_price", "price"):
        value = variant.get(key)
        if isinstance(value, (int, float)):
            return int(value)
    return ""


def _print_area(variant):
    parts = []
    for key in ("placeholders", "print_areas"):
        value = variant.get(key)
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, dict):
                    continue
                width = item.get("width") or item.get("print_area_width")
                height = item.get("height") or item.get("print_area_height")
                position = item.get("position") or item.get("name") or ""
                if width and height:
                    parts.append(f"{position}:{width}x{height}".strip(":"))
                elif item:
                    parts.append(json.dumps(item, ensure_ascii=False)[:160])
    return " | ".join(parts)


def _shipping_summary(data):
    zones = _items(data, "profiles", "shipping", "data")
    if not zones:
        return ""
    snippets = []
    for zone in zones[:3]:
        if not isinstance(zone, dict):
            continue
        title = zone.get("title") or zone.get("country") or zone.get("name") or ""
        first = zone.get("first_item") or zone.get("first") or zone.get("cost") or ""
        additional = zone.get("additional_items") or zone.get("additional") or ""
        snippets.append(f"{title}: first={first} add={additional}")
    return " | ".join(snippets)


def _shipping_for_variant(data, variant_id, country="US"):
    for profile in _items(data, "profiles", "shipping", "data"):
        if not isinstance(profile, dict):
            continue
        variant_ids = {str(value) for value in profile.get("variant_ids") or []}
        countries = {str(value) for value in profile.get("countries") or []}
        if str(variant_id) not in variant_ids:
            continue
        if country and countries and country not in countries:
            continue
        first = profile.get("first_item") or {}
        additional = profile.get("additional_items") or {}
        return first.get("cost", ""), additional.get("cost", "")
    return "", ""


def _read_candidates(limit=0, priority_max=4, ids=None):
    ids = {str(item).strip() for item in (ids or []) if str(item).strip()}
    with CANDIDATES.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = []
    seen = set()
    for row in rows:
        bid = _clean(row.get("Blueprint_ID"))
        if not bid or bid in seen:
            continue
        if ids and bid not in ids:
            continue
        try:
            priority = int(row.get("Priority") or 99)
        except ValueError:
            priority = 99
        if priority > priority_max:
            continue
        seen.add(bid)
        selected.append(row)
        if limit and len(selected) >= limit:
            break
    return selected


def _write_rows(rows):
    with DETAILS_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def probe(limit=0, priority_max=4, max_providers=2, max_variants=8, ids=None, output_path=None):
    output = []
    global DETAILS_CSV
    if output_path:
        DETAILS_CSV = Path(output_path)
    for candidate in _read_candidates(limit=limit, priority_max=priority_max, ids=ids):
        bid = _clean(candidate["Blueprint_ID"])
        print(f"[PROBE] blueprint={bid} {candidate.get('Printify_Catalog_Title')}", flush=True)
        try:
            blueprint = _get(f"/catalog/blueprints/{bid}.json", f"blueprint_{bid}.json")
            providers_data = _get(
                f"/catalog/blueprints/{bid}/print_providers.json",
                f"blueprint_{bid}_providers.json",
            )
            providers = _items(providers_data, "print_providers", "providers", "data")[:max_providers]
            if not providers:
                output.append(_base_row(candidate, blueprint, probe_status="NO_PROVIDER"))
                _write_rows(output)
                continue
            for provider in providers:
                pid = _clean(provider.get("id"))
                variants_data = _get(
                    f"/catalog/blueprints/{bid}/print_providers/{pid}/variants.json",
                    f"blueprint_{bid}_provider_{pid}_variants.json",
                )
                try:
                    shipping_data = _get(
                        f"/catalog/blueprints/{bid}/print_providers/{pid}/shipping.json",
                        f"blueprint_{bid}_provider_{pid}_shipping.json",
                    )
                except Exception:
                    shipping_data = {}
                variants = _items(variants_data, "variants", "data")[:max_variants]
                if not variants:
                    output.append(_base_row(candidate, blueprint, provider, probe_status="NO_VARIANT"))
                for variant in variants:
                    output.append(_variant_row(candidate, blueprint, provider, variant, shipping_data))
                _write_rows(output)
                time.sleep(1.5)
        except Exception as exc:
            output.append(_base_row(candidate, probe_status=f"ERROR: {exc}"))
            _write_rows(output)
            print(f"[PROBE-ERROR] {bid}: {exc}", flush=True)
    _write_rows(output)
    print(f"[PROBE-DONE] rows={len(output)} csv={DETAILS_CSV}", flush=True)
    return output


def _base_row(candidate, blueprint=None, provider=None, probe_status="OK"):
    now = time.strftime("%Y-%m-%d %H:%M:%S %z")
    return {
        "Product_Family": candidate.get("Product_Family", ""),
        "Priority": candidate.get("Priority", ""),
        "Blueprint_ID": candidate.get("Blueprint_ID", ""),
        "Blueprint_Title": (blueprint or {}).get("title") or candidate.get("Printify_Catalog_Title", ""),
        "Provider_ID": (provider or {}).get("id", ""),
        "Provider_Title": (provider or {}).get("title") or (provider or {}).get("name") or "",
        "Variant_ID": "",
        "Variant_Title": "",
        "Variant_Options": "",
        "Cost_Cents": "",
        "Suggested_Retail_Cents": "",
        "Print_Area": "",
        "Shipping_Profile": "",
        "Decision": candidate.get("Decision", ""),
        "Probe_Status": probe_status,
        "Probe_Timestamp": now,
    }


def _variant_row(candidate, blueprint, provider, variant, shipping_data):
    row = _base_row(candidate, blueprint, provider, "OK")
    first_ship, add_ship = _shipping_for_variant(shipping_data, variant.get("id"))
    row.update(
        {
            "Variant_ID": variant.get("id", ""),
            "Variant_Title": variant.get("title") or variant.get("name") or "",
            "Variant_Options": json.dumps(variant.get("options") or {}, ensure_ascii=False),
            "Cost_Cents": _cost(variant),
            "Suggested_Retail_Cents": _retail(variant),
            "Print_Area": _print_area(variant),
            "US_Shipping_First_Cents": first_ship,
            "US_Shipping_Additional_Cents": add_ship,
            "Shipping_Profile": _shipping_summary(shipping_data),
        }
    )
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--priority-max", type=int, default=4)
    parser.add_argument("--max-providers", type=int, default=2)
    parser.add_argument("--max-variants", type=int, default=8)
    parser.add_argument("--ids", default="", help="Comma-separated blueprint ids to probe.")
    parser.add_argument("--output", default="", help="Optional output CSV path.")
    args = parser.parse_args()
    probe(
        limit=args.limit,
        priority_max=args.priority_max,
        max_providers=args.max_providers,
        max_variants=args.max_variants,
        ids=[item.strip() for item in args.ids.split(",") if item.strip()],
        output_path=args.output or None,
    )


if __name__ == "__main__":
    main()
