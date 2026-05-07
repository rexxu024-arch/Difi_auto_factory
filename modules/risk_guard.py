import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RISK_PATH = PROJECT_ROOT / "Database" / "Account_Risk_State.json"
FEE_PATH = PROJECT_ROOT / "Database" / "Etsy_Fee_Kill_Switch.json"


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


def assert_etsy_fee_batch_allowed(planned_count, ambiguous_count=0, duplicate_paid_count=0, daily_spend_so_far=0.0):
    config = fee_kill_switch()
    if not config:
        return True
    expected_fee = float(config.get("expected_listing_fee_usd", 0.20))
    planned_fee = planned_count * expected_fee
    if planned_count > int(config.get("batch_listing_cap", 10)):
        raise RiskBlocked(f"Etsy batch listing cap exceeded: {planned_count}")
    if planned_fee > float(config.get("batch_fee_cap_usd", 2.0)):
        raise RiskBlocked(f"Etsy batch fee cap exceeded: ${planned_fee:.2f}")
    if daily_spend_so_far + planned_fee > float(config.get("daily_listing_fee_cap_usd", 6.0)):
        raise RiskBlocked(f"Etsy daily fee cap exceeded: ${daily_spend_so_far + planned_fee:.2f}")
    if ambiguous_count >= int(config.get("ambiguous_publish_cap", 1)):
        raise RiskBlocked("Etsy ambiguous paid publish cap reached; stop and reconcile.")
    if duplicate_paid_count > int(config.get("duplicate_paid_listing_cap", 0)):
        raise RiskBlocked("Etsy duplicate paid listing cap exceeded.")
    return True
