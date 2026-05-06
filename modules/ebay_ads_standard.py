import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from openpyxl import load_workbook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = PROJECT_ROOT / "Database"
EBAY_BOOK = DATABASE_DIR / "eBay_listing.xlsx"
LOG_PATH = DATABASE_DIR / "ebay_ads_standard_2pct.csv"
PENDING_PATH = DATABASE_DIR / "ebay_ads_pending_2pct.csv"

CAMPAIGN_NAME = "Fixed_2_Percent_Strategy"
DEFAULT_CAMPAIGN_ID = os.getenv("EBAY_AD_CAMPAIGN_ID", "165251921016")
MARKETPLACE_ID = os.getenv("EBAY_MARKETPLACE_ID", "EBAY_US")
AD_RATE = "2.0"
BASE_URL = os.getenv("EBAY_API_BASE_URL", "https://api.ebay.com")

HEADERS = [
    "Timestamp",
    "Action",
    "ID",
    "eBay_Item_ID",
    "Campaign_ID",
    "HTTP_Status",
    "Result",
    "Error",
]
PENDING_HEADERS = [
    "Timestamp",
    "ID",
    "eBay_Item_ID",
    "Campaign_ID",
    "Ad_Rate",
    "Status",
    "Error",
]


def _access_token():
    token = os.getenv("EBAY_ACCESS_TOKEN") or os.getenv("EBAY_OAUTH_TOKEN")
    if not token:
        raise RuntimeError(
            "Missing EBAY_ACCESS_TOKEN / EBAY_OAUTH_TOKEN. eBay Marketing API cannot be used until OAuth is configured."
        )
    return token


def has_access_token():
    return bool(os.getenv("EBAY_ACCESS_TOKEN") or os.getenv("EBAY_OAUTH_TOKEN"))


def _headers():
    return {
        "Authorization": f"Bearer {_access_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE_ID,
    }


def _api(method, path, **kwargs):
    response = requests.request(method, f"{BASE_URL}{path}", headers=_headers(), timeout=90, **kwargs)
    return response


def _log(rows):
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def enqueue_listing(item_id, ebay_item_id, campaign_id=None, status="PENDING_API"):
    ebay_item_id = str(ebay_item_id or "").strip()
    if not ebay_item_id:
        return False
    campaign_id = campaign_id or DEFAULT_CAMPAIGN_ID or CAMPAIGN_NAME
    existing = set()
    if PENDING_PATH.exists():
        with PENDING_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                existing.add((row.get("eBay_Item_ID"), row.get("Campaign_ID")))
    key = (ebay_item_id, campaign_id)
    if key in existing:
        return False
    file_exists = PENDING_PATH.exists()
    with PENDING_PATH.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PENDING_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "Timestamp": datetime.now().isoformat(timespec="seconds"),
                "ID": item_id,
                "eBay_Item_ID": ebay_item_id,
                "Campaign_ID": campaign_id,
                "Ad_Rate": AD_RATE,
                "Status": status,
                "Error": "",
            }
        )
    return True


def _published_listing_ids(limit=0):
    workbook = load_workbook(EBAY_BOOK, read_only=True, data_only=True)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    cols = {header: index for index, header in enumerate(headers)}
    if "eBay_Item_ID" not in cols:
        workbook.close()
        raise RuntimeError("eBay_Item_ID column is missing. Run printify_external_sync.py first.")
    rows = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row or not row[cols["ID"]]:
            continue
        status = str(row[cols.get("Status")] or "")
        item_id = str(row[cols["eBay_Item_ID"]] or "").strip()
        if status.startswith("Printify_Published") and item_id:
            rows.append(
                {
                    "ID": row[cols["ID"]],
                    "Product_Type": row[cols.get("Product_Type")],
                    "Title": row[cols.get("Title")],
                    "eBay_Item_ID": item_id,
                }
            )
            if limit and len(rows) >= limit:
                break
    workbook.close()
    return rows


def find_campaign():
    response = _api("GET", f"/sell/marketing/v1/ad_campaign?campaign_name={CAMPAIGN_NAME}")
    if response.status_code == 404:
        return None
    response.raise_for_status()
    data = response.json()
    campaigns = data.get("campaigns") or data.get("adCampaigns") or []
    for campaign in campaigns:
        if campaign.get("campaignName") == CAMPAIGN_NAME or campaign.get("name") == CAMPAIGN_NAME:
            return campaign
    return campaigns[0] if len(campaigns) == 1 else None


def create_campaign():
    payload = {
        "campaignName": CAMPAIGN_NAME,
        "campaignFundingStrategy": {
            "fundingModel": "COST_PER_SALE",
            "bidPercentage": AD_RATE,
        },
        "marketplaceId": MARKETPLACE_ID,
    }
    response = _api("POST", "/sell/marketing/v1/ad_campaign", json=payload)
    if response.status_code not in {200, 201, 202, 204}:
        response.raise_for_status()
    location = response.headers.get("Location", "")
    campaign_id = location.rstrip("/").split("/")[-1] if location else ""
    return campaign_id, response.status_code, location


def bulk_create_ads(campaign_id, listings, dry_run=True):
    logs = []
    if dry_run:
        for listing in listings:
            logs.append(
                {
                    "Timestamp": datetime.now().isoformat(timespec="seconds"),
                    "Action": "DRY_RUN_ADD_AD",
                    "ID": listing["ID"],
                    "eBay_Item_ID": listing["eBay_Item_ID"],
                    "Campaign_ID": campaign_id,
                    "HTTP_Status": "",
                    "Result": f"Would add listing at fixed bidPercentage={AD_RATE}",
                    "Error": "",
                }
            )
        _log(logs)
        print(f"[ADS-DRY] campaign={campaign_id or CAMPAIGN_NAME} listings={len(listings)} rate={AD_RATE}")
        return logs
    requests_payload = [
        {"listingId": listing["eBay_Item_ID"], "bidPercentage": AD_RATE}
        for listing in listings
    ]
    response = _api(
        "POST",
        f"/sell/marketing/v1/ad_campaign/{campaign_id}/bulk_create_ads_by_listing_id",
        json={"requests": requests_payload},
    )
    result_text = response.text[:1000]
    status_code = response.status_code
    if response.status_code not in {200, 201, 202, 207}:
        response.raise_for_status()
    for listing in listings:
        logs.append(
            {
                "Timestamp": datetime.now().isoformat(timespec="seconds"),
                "Action": "ADD_AD_FIXED_2",
                "ID": listing["ID"],
                "eBay_Item_ID": listing["eBay_Item_ID"],
                "Campaign_ID": campaign_id,
                "HTTP_Status": status_code,
                "Result": result_text,
                "Error": "",
            }
        )
    _log(logs)
    print(f"[ADS-OK] campaign={campaign_id} listings={len(listings)} http={status_code}")
    return logs


def enroll_listing(item_id, ebay_item_id, campaign_id=None, dry_run=False):
    campaign_id = campaign_id or DEFAULT_CAMPAIGN_ID
    listing = {"ID": item_id, "eBay_Item_ID": str(ebay_item_id).strip()}
    if not listing["eBay_Item_ID"]:
        return False
    if dry_run:
        bulk_create_ads(campaign_id or CAMPAIGN_NAME, [listing], dry_run=True)
        return True
    if not has_access_token():
        enqueue_listing(item_id, listing["eBay_Item_ID"], campaign_id=campaign_id, status="PENDING_OAUTH")
        print(f"[ADS-PENDING] {item_id} ebay={listing['eBay_Item_ID']} reason=missing_oauth")
        return False
    if not campaign_id:
        campaign = find_campaign()
        campaign_id = (
            campaign.get("campaignId")
            or campaign.get("campaign_id")
            or campaign.get("adCampaignId")
            if campaign
            else ""
        )
    if not campaign_id:
        enqueue_listing(item_id, listing["eBay_Item_ID"], campaign_id=CAMPAIGN_NAME, status="PENDING_CAMPAIGN_ID")
        print(f"[ADS-PENDING] {item_id} ebay={listing['eBay_Item_ID']} reason=missing_campaign_id")
        return False
    bulk_create_ads(campaign_id, [listing], dry_run=False)
    return True


def run(limit=0, dry_run=True, campaign_id=None, create_if_missing=False):
    listings = _published_listing_ids(limit=limit)
    print(f"[ADS] eligible_with_ebay_id={len(listings)} dry_run={dry_run} rate={AD_RATE}")
    if dry_run:
        return bulk_create_ads(campaign_id or CAMPAIGN_NAME, listings, dry_run=True)
    campaign = None
    if campaign_id:
        resolved_campaign_id = campaign_id
    else:
        campaign = find_campaign()
        resolved_campaign_id = (
            campaign.get("campaignId")
            or campaign.get("campaign_id")
            or campaign.get("adCampaignId")
            if campaign
            else ""
        )
    if not resolved_campaign_id and create_if_missing:
        resolved_campaign_id, status, location = create_campaign()
        print(f"[ADS-CAMPAIGN-CREATED] id={resolved_campaign_id} http={status} location={location}")
    if not resolved_campaign_id:
        raise RuntimeError(
            f"Campaign {CAMPAIGN_NAME} was not found. Create it in Seller Hub or rerun with --create-if-missing after final confirmation."
        )
    return bulk_create_ads(resolved_campaign_id, listings, dry_run=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--campaign-id", default="")
    parser.add_argument("--create-if-missing", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    run(
        limit=args.limit,
        dry_run=not args.execute,
        campaign_id=args.campaign_id or None,
        create_if_missing=args.create_if_missing,
    )


if __name__ == "__main__":
    main()
