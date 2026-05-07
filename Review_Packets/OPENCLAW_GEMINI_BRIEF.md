# OpenClaw Gemini Brief

Generated: 2026-05-06 21:58:00 -04:00 America/New_York

This is the copy/paste brief for Gemini. Gemini does **not** need direct access to the repo, code, or folders to understand the strategy. The implementation details are summarized as business capabilities and current operational facts.

## Critical Update

NETWORK IS FIXED.

The old low-bandwidth assumption is no longer valid.

- Rex moved to wired LAN / Ethernet for production work.
- Ethernet is active at 1Gbps.
- Wi-Fi is disconnected for production work.
- Latest checks showed 0% packet loss to Printify, eBay, Etsy, Discord, and OpenAI.
- Typical latency is about 5-8ms.
- A 50MB download test reached about 214Mbps.
- Online production can resume at normal/high throughput.
- Remaining throttles should be business/account-risk throttles, not network throttles.

ETSY DIGITAL TEST IS LIVE.

- Etsy UI login works in the dedicated Edge automation profile.
- Codex published the first 10 OpenClaw Etsy Digital printable listings through Etsy UI.
- Confirmed Etsy listing-fee spend is $2.00.
- Etsy API is still pending approval, so UI automation is the current route.
- Etsy Shop Manager initially showed 12 active listings: 10 OpenClaw digital tests plus 2 old DriveFuel listings. The two old DriveFuel listings have now been deleted/retired; their public pages show unavailable.

## Role Split

- Rex: commander and final business/risk owner.
- Gemini: strategy advisor and business logic reviewer.
- Codex: execution operator, programmer, QA builder, and automation debugger.

Gemini should focus on strategy, buyer psychology, marketplace positioning, product selection, pricing, and which experiments matter. Codex handles implementation.

## Business Goal

Rex is building a Printify-first POD factory that can:

- Generate product concepts and visual DNA.
- Produce high-quality product assets.
- QA production images before publishing.
- Push products to eBay/Etsy through Printify/API/browser workflows.
- Monitor performance.
- Identify winning DNA.
- Generate variations.
- Eventually run with minimal human intervention.

The goal is not merely "more listings." The goal is a durable, semi-automated revenue engine.

## Current Product Strategy

Current product families:

- Sticker: low-price discovery/traffic product. Current cap is 100 active/public listings.
- Poster: mid-price wall art product.
- Acrylic photo block: premium/high-margin shelf decor.

Target direction:

- Current medium target is around 200 total Printify/eBay listings.
- Desired rough ratio is Sticker : Poster : Acrylic = 2 : 1 : 1.
- Sticker should not expand blindly until the cover-image issue is cleaned up.
- Poster and Acrylic are currently more important for premium positioning.

## Current Marketplace Counts

Current tracked state:

- Sticker: 70 published/live tracked, plus 15 old bad Sticker listings already retired/replaced.
- Poster: 36 published/live tracked.
- Acrylic: 50 published/live tracked.

Interpretation:

- Acrylic has reached the current target of 50.
- Poster needs about 14 more published listings to reach 50.
- Sticker is already within Rex's requested 70-100 range.
- Next Sticker work should be repair/replacement quality control, not raw expansion.

## Main Technical/Business Problem Found

Many early eBay Sticker listings had the wrong buyer-facing cover image.

What happened:

- The old workflow uploaded the main cover plus individual detail images.
- eBay sometimes chose one detail image as the public cover.
- Buyers saw one isolated design/detail instead of the intended 4-piece sticker set.

Why it matters:

- Even if the art quality is high, the listing looks confusing.
- It hurts trust, click-through, and buyer expectation.
- Ads cannot fix a bad first impression.

Verified fix:

- For Sticker listings, publish with the main Cover image only as custom art.
- Keep Printify's official product mockups in the gallery.
- Keep individual detail images local for QA/reference, not first-pass public gallery.

Poster/Acrylic are different:

- They are full-surface products.
- The production design is one full image.
- Printify official mockups are useful and should generally stay because they show the object context.

## Current Cover Repair State

Current state:

- 15 old bad Sticker listings have been safely retired after verified replacements.
- 31 more old Sticker listings are ready for replacement/retirement once their new versions pass live cover audit.
- 4 ambiguous/non-Sticker rows need review before replacement.
- A latest batch of 10 Sticker replacements has been created/published; 4 still need eBay external ID sync and the batch still needs final live buyer-page cover audit before retiring old originals.

Immediate operational sequence:

1. Sync missing eBay external IDs for the latest replacement batch.
2. Live-audit the latest 10 replacement listings.
3. Retire old originals only after replacement buyer-page cover passes.
4. Continue Poster production to 50.
5. Do not expand Sticker above 100.

## eBay Traffic Problem

Observed issue:

- Many listings still have zero or near-zero views.
- eBay 2% General ads did not produce a meaningful immediate lift.

Current hypothesis:

- Ads are not the root solution.
- The likely bottlenecks are:
  - wrong/weak first image on early Sticker listings,
  - cold account/category momentum,
  - title/search-intent mismatch,
  - item specifics/category trust,
  - low profile/store trust,
  - product-market fit still unproven,
  - too many similar listings without clear buyer segmentation.

Recommended strategic frame:

- Treat ads as an amplifier, not a cure.
- First fix image trust and buyer intent.
- Then run small controlled title/price/product-mix experiments.

## Ads Policy

Rex authorized only:

- eBay Promoted Listings Standard / General.
- Fixed 2.0% ad rate.
- No Priority/PPC.
- No suggested ad rate.

Automation is pending because eBay Developer/OAuth access is not fully approved yet.

## eBay Developer API State

eBay Developer account access is pending approval.

When available, the first APIs should be narrow:

1. Sell Marketing API: manage fixed 2% Standard/General ads.
2. Sell Analytics API: read traffic/performance signals.

Avoid building a second full listing system. Printify should remain the main production and listing-push path. eBay API should support analytics, ads, audits, and reconciliation.

## Etsy State

Etsy shop exists and the first digital gray batch is now live.

Current state:

- Etsy API/app is pending/inactive.
- Etsy UI login works in the dedicated Edge profile, not Rex's daily Chrome.
- First Etsy Digital batch: 10 live printable wall-art listings, confirmed spend $2.00.
- Etsy shop brand shell is still not final.
- Two old legacy DriveFuel listings have been deleted/retired; their public pages now show unavailable.

Strategic direction:

- Etsy should launch with a curated premium shell, not a brute-force dump.
- Treat the first 10 digital listings as a gray test, not proof of product-market fit.
- Copy should be more poetic than eBay but still SEO-aware.
- Store identity should support premium decor, Zen/dark-academia/jade relic aesthetics, and future broader bestsellers.
- Spend control: Rex authorized a 200-listing long-run experiment pool, but before signal the practical spending pool is $40 normal / $60 hard-with-rationale. Do not burn the pool without views/favorites/search signal.

## Pricing Notes

Current pricing examples:

- Sticker: around $11.99.
- Poster 12x18 matte: around $34.99.
- Acrylic 5x7 block: around $89.99.

Strategic question:

- For a cold shop, premium pricing may be okay for Acrylic if positioning is strong, but Poster/Acrylic should probably be tested with small price/offer experiments rather than assumed perfect.

## Production Quality Rule

The production image must match what Printify will print.

Current QA principle:

- Do not just trust that a listing published.
- Audit that the uploaded production design matches the local intended design.
- For Sticker, the buyer-facing cover must match the intended product cover.
- For Poster/Acrylic, the design should be full-frame and not sticker-cut/die-cut.

This is more important than speed because bad production art can create refunds, trust damage, and wasted listings.

## What Codex Is Doing Next

Execution priorities:

1. QA the first 10 Etsy Digital public listings and read initial traffic when Etsy exposes it.
2. Finish latest Sticker replacement audit and old-listing retirement.
3. Bring Poster count to 50 only when eBay/Printify external sync is controlled.
4. Keep Acrylic around 50 unless a clearly stronger premium DNA/product test is ready.
5. Keep eBay ads/API automation ready for OAuth approval.
6. Keep turning manual labor into scripts, queues, QA gates, and reports.

## Stress Test / Guardrails Update

Codex answered Gemini's stress-test prompts in `Review_Packets/CODEX_STRESS_TEST_RESPONSE.md`.

Key updates:

- Current network guard is `full_throughput`, not low-bandwidth.
- Etsy is authorized as a 200-listing experiment pool once login is stable, but publishing will be staged with stop rules.
- Digital printable wall art is now the first no-Printify-cost Etsy experiment.
- Pricing uses free-shipping presentation where possible, but internal profit math includes Printify shipping.
- eBay low-view risk is treated as a market/channel learning problem, not just a listing-volume problem.

## What Gemini Should Advise On

Please advise Rex on strategy, not code:

1. If eBay views remain near zero after cover fixes, what should be tested first: title intent, category/item specifics, profile trust, price, product mix, or store branding?
2. Should the next effort prioritize premium Poster/Acrylic over Sticker once the Sticker repair backlog is clean?
3. Should Etsy launch as a narrow Zen/dark-academia premium decor shop or a broader premium AI-art/decor shop?
4. Are the current Poster/Acrylic prices too high for a cold shop, or should Rex keep premium pricing and improve presentation first?
5. What buyer personas or gift occasions should the next product DNA target?
6. What should be the smallest credible experiment that can tell whether the store has product-market fit?

## Important Constraint For Gemini

Gemini should not assume Rex wants to manually operate the system.

Rex wants Codex to build a system where:

- repeated operations become scripts,
- performance feedback becomes structured data,
- good DNA becomes new variations,
- bad products are quarantined,
- account-risk gates stop unsafe actions,
- Rex only handles final strategic decisions and high-risk approvals.

## Human Summary

The old "network is too unstable" bottleneck is gone. The main bottleneck is now marketplace quality and conversion learning: correct images, clear buyer intent, better store trust, controlled product mix, and performance-driven iteration.


## Update - 2026-05-06 20:48:25 America/New_York

- Etsy Digital gray launch first batch is staged: 10/10 QA PASS, $2 reserved, $0 spent. Etsy publish is blocked correctly because app/API/login is not clean. Morning traffic penetration report is scheduled and stored in `Review_Packets/ETSY_DIGITAL_TRAFFIC_PENETRATION_REPORT_20260506.md`.
- eBay/Printify publish route issue is now proven: Printify API `publish.json` can return HTTP 200 without generating an eBay external id. `Poster-Academia-0038..0042` and `Sticker-Zen-0044-FIX1` are Printify-ready but not confirmed live eBay listings. The scheduler now counts success only when external id exists.
- Browser isolation improved: Printify login guard, supervisor, mockup uploader, and full pipeline now default to dedicated Edge CDP port 9223 instead of Rex's daily Chrome 9222.
- eBay traffic snapshot remains weak: 43/50 sampled active listings at 0 views, all 50 promoted with Standard/General; product stats now show Sticker has 0 movement while Poster/Acrylic show limited movement. Ads alone are not the lever; cover/gallery correctness and eBay API publish/revise control are the priority.
- Minimal eBay API packet is stored in `Review_Packets/EBAY_API_MINIMAL_APPLICATION_PACKET.md`: first Inventory API, second Marketing API; Account API only for business-policy lookup.
