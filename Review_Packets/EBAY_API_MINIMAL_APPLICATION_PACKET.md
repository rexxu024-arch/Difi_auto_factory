# eBay API Minimal Application Packet

Generated: 2026-05-06 20:47:22 America/New_York

## Why This Matters Now

Printify API `publish.json` returned HTTP 200 for multiple products but did not create/return eBay `external.id`. This proves we need a real eBay-side publish/revise route instead of counting Printify API publish as live inventory.

## Apply/Enable First: 1-2 APIs

### 1. Sell Inventory API - Highest Priority

Use case for OpenClaw:

- Create inventory item records from already-QA-passed Printify assets.
- Create and publish fixed-price offers on eBay.
- Receive real eBay listing ids deterministically.
- Revise title, description, quantity, price, and picture URLs through code instead of Seller Hub browser scraping.

Why first:

- It directly fixes the current blocker: Printify-ready products with no eBay external id.
- It gives us idempotency and auditability, so we can avoid duplicate listings and false-published rows.

Official docs:

- Inventory API overview: https://developer.ebay.com/api-docs/sell/inventory/overview.html
- Create offer: https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/createOffer
- Publish offer: https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/publishOffer
- Required fields before publish: https://developer.ebay.com/api-docs/sell/static/inventory/publishing-offers.html

### 2. Sell Marketing API - Second Priority

Use case for OpenClaw:

- Create/update `Fixed_2_Percent_Strategy` campaign.
- Add newly published items to Promoted Listings Standard / General at fixed 2.0%.
- Avoid Priority/PPC and ignore suggested rates.

Why second:

- Ads are not enough to solve 0 views, but once listings are correct, this automates the fixed baseline promotion rule.

Official docs:

- Marketing API overview: https://developer.ebay.com/api-docs/sell/marketing/overview.html
- Promoted Listings overview: https://developer.ebay.com/api-docs/sell/static/marketing/pl-overview.html

## Dependency: Sell Account API / Business Policies

Inventory API requires the seller account to use eBay business policies before active offers can be published. We should use Account API only to read or reference existing fulfillment/payment/return policy IDs first. Do not start by editing payment/order settings.

Official doc note: Inventory API overview states active listing publish requires business policies and may use Account API for listing policies.

## Recommended Rex Action When Developer Account Is Approved

1. Create one production app keyset.
2. Grant only scopes needed for Sell Inventory, Sell Marketing, and read-only Account policy lookup.
3. Give Codex the app credentials through `.env` only.
4. First live proof: publish exactly one already-QA-passed replacement listing, confirm eBay id, confirm cover image, then stop.
5. Only after that, enroll that one listing into fixed 2% Standard/General campaign.

## Do Not Do Yet

- Do not build a parallel full listing engine for every marketplace.
- Do not touch orders, payment settings, buyer messages, or billing through API.
- Do not migrate all existing eBay listings to Inventory API until one product path is proven.
