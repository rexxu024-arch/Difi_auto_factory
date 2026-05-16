import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RISK_PATH = PROJECT_ROOT / "Database" / "Account_Risk_State.json"
FEE_PATH = PROJECT_ROOT / "Database" / "Etsy_Fee_Kill_Switch.json"
FIRST_AUDIT_BLOCKLIST_PATH = PROJECT_ROOT / "Database" / "First_Audit_001_Blocklist.csv"
ETSY_FEE_LEDGER_PATH = PROJECT_ROOT / "Database" / "Etsy_Fee_Ledger.csv"


class RiskBlocked(RuntimeError):
    pass


def _load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def risk_state():
    return _load_json(RISK_PATH)


def fee_kill_switch():
    return _load_json(FEE_PATH)


def confirmed_etsy_fee_spend() -> float:
    """Return total confirmed Etsy listing-fee spend recorded locally."""
    if not ETSY_FEE_LEDGER_PATH.exists():
        return 0.0
    total = Decimal("0.00")
    with ETSY_FEE_LEDGER_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            status = str(row.get("Status") or "").upper()
            if not status.startswith("CONFIRMED"):
                continue
            value = row.get("Confirmed_Spent_USD")
            if value in (None, ""):
                continue
            try:
                total += Decimal(str(value))
            except Exception:
                continue
    return float(total)


def first_audit_blocklist_markers():
    if not FIRST_AUDIT_BLOCKLIST_PATH.exists():
        return set()
    markers = set()
    with FIRST_AUDIT_BLOCKLIST_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            for key in ("Audit_ID", "SKU", "Production_File", "Source_File"):
                value = (row.get(key) or "").strip()
                if value:
                    markers.add(value.lower().replace("\\", "/"))
            source_file = (row.get("Source_File") or "").strip()
            if source_file:
                source_name = Path(source_file).name
                sku = (row.get("SKU") or "").strip()
                if sku and source_name.lower().startswith(sku.lower()):
                    markers.add(source_name.lower())
    return markers


def marketplace_state(marketplace):
    states = risk_state().get("states") or {}
    return states.get(str(marketplace).lower()) or {}


def assert_allowed(marketplace, action):
    state = marketplace_state(marketplace)
    action = str(action).lower()
    key = {
        "read": "read_allowed",
        "write": "write_allowed",
        "paid_publish": "paid_publish_allowed",
        "paid_ads": "paid_ads_allowed",
    }.get(action, f"{action}_allowed")
    if state and not state.get(key, False):
        raise RiskBlocked(
            f"{marketplace} {action} blocked by Account_Risk_State: "
            f"{state.get('risk_state')} | {state.get('notes', '')}"
        )
    return True


def assert_no_first_audit_public_assets(payload, context="public marketplace payload"):
    """Block The First Audit: 001 assets from public low-price channels.

    `payload` can be a dict/list/string assembled by a publish script before it
    calls Etsy/eBay/Printify. The check is conservative around SKU/full-path
    markers and avoids generic filenames such as Production_Design.png.
    """
    markers = first_audit_blocklist_markers()
    if not markers:
        return True
    blob = json.dumps(payload, ensure_ascii=False, default=str).lower().replace("\\", "/")
    matched = sorted(marker for marker in markers if marker and marker in blob)
    if matched:
        raise RiskBlocked(
            f"First Audit studio asset blocked in {context}: {matched[0]} "
            "(reserved for private Studio inventory, not public Etsy/eBay archive)."
        )
    return True


def assert_etsy_fee_batch_allowed(planned_count, ambiguous_count=0, duplicate_paid_count=0, daily_spend_so_far=0.0):
    config = fee_kill_switch()
    if not config:
        return True
    def cents(value):
        amount = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return int(amount * 100)

    expected_fee_cents = cents(config.get("expected_listing_fee_usd", 0.20))
    planned_fee_cents = planned_count * expected_fee_cents
    batch_cap_cents = cents(config.get("batch_fee_cap_usd", 2.0))
    daily_cap_cents = cents(config.get("daily_listing_fee_cap_usd", 6.0))
    pool_cap_cents = cents(config.get("authorized_pool_budget_usd", 50.0))
    absolute_cap_cents = cents(config.get("absolute_no_result_spend_cap_usd", 60.0))
    daily_spend_cents = cents(daily_spend_so_far)
    total_spend_cents = cents(confirmed_etsy_fee_spend())
    if planned_count > int(config.get("batch_listing_cap", 10)):
        raise RiskBlocked(f"Etsy batch listing cap exceeded: {planned_count}")
    if planned_fee_cents > batch_cap_cents:
        raise RiskBlocked(f"Etsy batch fee cap exceeded: ${planned_fee_cents / 100:.2f}")
    if daily_spend_cents + planned_fee_cents > daily_cap_cents:
        raise RiskBlocked(f"Etsy daily fee cap exceeded: ${(daily_spend_cents + planned_fee_cents) / 100:.2f}")
    if total_spend_cents + planned_fee_cents > absolute_cap_cents:
        raise RiskBlocked(
            f"Etsy absolute listing-fee ceiling exceeded: ${(total_spend_cents + planned_fee_cents) / 100:.2f}"
        )
    if total_spend_cents + planned_fee_cents > pool_cap_cents:
        raise RiskBlocked(
            f"Etsy listing-fee budget exceeded: ${(total_spend_cents + planned_fee_cents) / 100:.2f}"
        )
    if ambiguous_count >= int(config.get("ambiguous_publish_cap", 1)):
        raise RiskBlocked("Etsy ambiguous paid publish cap reached; stop and reconcile.")
    if duplicate_paid_count > int(config.get("duplicate_paid_listing_cap", 0)):
        raise RiskBlocked("Etsy duplicate paid listing cap exceeded.")
    return True
