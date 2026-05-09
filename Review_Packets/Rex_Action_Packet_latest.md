# Rex Action Packet

Generated: 2026-05-09 01:43:36 EDT

## Need Rex / Account UI Cooperation

1. Etsy OAuth authorize flow
   - Status: API key is active, but OAuth authorization currently lands on Etsy `error.php` before callback.
   - First thing to confirm in the Etsy developer app: this callback URL is allowed exactly:
     `http://localhost:8765/etsy/oauth/callback`
   - If Etsy does not allow that exact local URL, add the official tutorial fallback too:
     `http://localhost:3003/oauth/redirect`
   - After adding it, Codex can complete OAuth and store access/refresh tokens locally.

2. eBay Developer keyset compliance
   - Status: Production keyset is disabled until Marketplace Account Deletion compliance is satisfied.
   - Preferred path: Cloudflare Worker HTTPS endpoint for deletion notifications, not exemption, because OpenClaw stores item/listing/performance data.
   - Codex can prepare endpoint code; Rex only needs to deploy/fill final public HTTPS URL if Cloudflare login requires human verification.

3. Etsy shop name follow-up
   - Status: Option 02 / Quiet Relic Studio shell copy and logo are applied.
   - Still visible: Etsy shop name remains `DriveFuel`; the shop-name custom input did not accept the automated write.
   - Rex can either manually rename it to `QuietRelicStudio`, or leave it temporarily while Codex continues Etsy listing/data work.

## No New Credentials Needed Right Now

- Etsy keystring/shared secret are already in `.env` and ping succeeds.
- Printify API key is present, and the Printify Etsy shop is linked as shop `24260389`.
- Do not paste passwords into chat. If a login expires, use Edge manually or store credentials only in a password manager/browser profile.

## Current Automated Work

- Build Etsy listing experiment pool without spending unless publish path passes QA.
- Keep Sticker expansion frozen until gallery/cover trust is solved.
- Use Poster/Acrylic and Etsy Digital as the main near-term battlefield.
- Etsy storefront shell is partially applied: copy/tagline/about/logo are live; only shop name remains `DriveFuel`.
- Block Printify products whose official mockup gallery contains exact duplicate buyer-facing images until a safe de-duplication route exists.

## Etsy API Pulse

- status: `API_KEY_ACTIVE`
- http_status: `200`
- next: `RUN_OAUTH_PKCE`

## Etsy Spend / Queue Pulse

- confirmed_digital_listing_spend: `$2.00`
- confirmed_pod_listing_spend: `$0.20`
- confirmed_total_etsy_listing_spend: `$2.20`
- next_digital_candidates_ready_no_spend: `29`
- next_digital_projected_fee_if_published: `$5.80`
- printify_etsy_external_pending_checked: `1`
- printify_etsy_external_pending_resolved: `0`

## For Gemini/Grey

The strategic ask is not whether to keep Etsy as a battlefield; Rex has approved a 200-listing test pool. The current tactical blocker is Etsy OAuth authorization returning Etsy error.php before callback, plus duplicate Printify official mockups on some POD products. Storefront shell is mostly applied, but the public shop name remains DriveFuel. Recommend strategy under these constraints: use Etsy Digital/direct API once OAuth is fixed, and only use Printify POD listings when gallery QA passes.
