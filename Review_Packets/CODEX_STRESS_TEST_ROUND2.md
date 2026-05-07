# Codex Stress Test Round 2

Updated: 2026-05-06 New York time

This file is written for Rex and Gemini. It answers the second pressure-test batch and turns the answers into operational guardrails.

## 1. Traffic Penetration If 10 Digital Products Stay 0 View

Prompt:

> Assume the first 10 Digital products still have 0 views after 24 hours. Do not answer "wait" or "check network." Give two aggressive penetration variables: one category-competition downgrade, one SEO search-volume restructuring. How do we tell whether visual DNA is bad or account weight is locked?

### Variable A: Category Competition Downgrade

If broad printable wall art is a black hole, downgrade from broad category competition into narrower buyer-use cases.

Do not keep titles like:

- `Dark Academia Printable Wall Art`
- `Zen Printable Poster`
- `Jade Wall Art Download`

Test lower-competition intent cells:

- `study room printable`
- `reading nook wall art`
- `home office printable`
- `library decor print`
- `dark academia dorm decor`
- `meditation room print`
- `wabi sabi entryway print`
- `book lover wall art`
- `small apartment gallery wall`

Logic:

Broad "wall art" is crowded. Smaller room/use-case keywords may have lower volume but less competition and clearer buyer intent. If a new shop has weak account weight, it should first aim for thinner search lanes.

### Variable B: SEO Search-Volume Restructuring

If current SEO is too poetic, split listings into search-intent templates:

1. Buyer object first:
   - `Printable Wall Art, Dark Academia Study Room Decor, Instant Download`

2. Room/use case first:
   - `Study Room Wall Art Printable, Library Decor Digital Download`

3. Gift/persona first:
   - `Book Lover Wall Art, Dark Academia Printable Gift for Reader`

4. Style/aesthetic first:
   - `Wabi Sabi Printable Wall Art, Zen Meditation Room Decor`

5. Color/material first:
   - `Emerald Green Wall Art Printable, Jade Decor Digital Download`

This is not just synonym spinning. The experiment changes the first 40-60 title characters, because Etsy/eBay search and human scanning heavily weight the early title phrase.

### How To Tell Visual DNA vs Account Weight

If account/shop weight is locked or extremely weak:

- Many different products and title templates all get 0 views.
- Even simpler buyer-intent products get 0 views.
- Views do not differ by visual quality.
- No favorites, no external clicks, no marketplace impressions.

If visual DNA is the problem:

- Listings get views but no favorites/clicks/orders.
- Some product types get views but specific visuals underperform.
- Lower-aesthetic or more literal designs outperform ornate niche designs.
- External traffic sent directly to the listing produces weak saves/clicks.

Diagnostic sequence:

1. Keep 10 current digital listings as control.
2. Add 5 low-competition buyer-use-case digital listings.
3. Add 5 simplified, more literal room-decor visuals.
4. If all 20 are still 0 view after indexing, suspect shop/account/indexing problem.
5. If some get views but no conversion, improve visual/product offer.

## 2. Financial Kill-Switch For Etsy Listing Fees

Prompt:

> If Etsy batch publishing has API jitter and cannot confirm success, but listing fee counter might be moving, do we preserve output or preserve capital? Set a hard cap and explain how not to waste money.

Answer:

The system must preserve capital first. If paid listing state is ambiguous, stop. Do not keep retrying.

### Fee Kill-Switch Rules

Default Etsy test budget:

- Authorized pool: 200 listings.
- Expected listing fee: $0.20/listing.
- Total pool ceiling: about $40.

Operational hard caps:

- Per batch cap: 10 listings or $2.00 before manual/automated reconciliation.
- Ambiguous publish cap: 1 ambiguous paid action. If we cannot confirm whether one listing published, stop the batch immediately.
- Duplicate-create cap: 0 tolerated duplicate paid listings. If duplicate risk is detected, stop.
- Daily Etsy listing-fee cap during testing: $6.00 unless Rex explicitly raises it.
- Full 200 pool can only be consumed after performance data justifies expansion.

### Confirmation Logic

Before paid publish:

- Generate a local idempotency key: `Local_ID + Shop_ID + Draft_Group + Content_Hash`.
- Write a `PUBLISH_INTENT` row locally.
- Publish one listing.
- Confirm by Etsy API/UI/Printify external state.
- Only then mark `PUBLISHED_CONFIRMED`.

If API/UI times out:

- Do not retry create blindly.
- Query by title/SKU/local idempotency marker.
- If still ambiguous, mark `PUBLISH_AMBIGUOUS_HOLD` and stop the batch.

This may sacrifice speed, but it prevents repeating paid listing creation. The correct bias is: lose time, not money.

## 3. Aesthetic QA Against AI-Fluff And Fake Mockups

Prompt:

> For Dark Academia, if AI copy sounds like AI fluff or mockup shadow physics looks fake, do we have non-text QA? How can histogram/contrast analysis catch fake-looking products?

Answer:

There are two different QA layers: text QA and image QA.

### Text QA For AI-Fluff

Machine-fluff indicators:

- Too many abstract adjectives: `ethereal`, `timeless`, `captivating`, `enchanting`, `immersive`, repeated without concrete product facts.
- No buyer-use case in first paragraph.
- No clear physical/digital deliverable.
- Repeated niche words across many listings.
- Title/description says "concept" too vaguely.

Action:

- Flag if description has high adjective density and low product-fact density.
- Force rewrite using concrete facts: size, material, room, gift use, digital/physical delivery, image note.

### Non-Text Image QA

For images/mockups, the system can analyze:

- Histogram clipping:
  - Too much pure black or pure white suggests lost detail or artificial cutout.

- Contrast range:
  - Very low contrast means muddy image.
  - Extremely high contrast plus clipped shadows means fake/dramatic artifact risk.

- Edge energy / sharpness:
  - Low edge energy means blurry.
  - Excessive edge halos can indicate over-sharpening.

- Shadow consistency:
  - Detect dominant light direction by bright/dark gradients.
  - If product object has highlights from one side but cast shadows imply another, flag for review.

- Background realism:
  - For POD mockups, official Printify mockups are trusted over AI-created lifestyle mockups.
  - AI lifestyle mockups should be considered optional premium assets, not core proof, until a stricter vision QA gate exists.

### Practical Current Gate

Current production gates already verify:

- local production image matches Printify print area;
- buyer-facing live eBay image is not an unintended U/detail image;
- Poster/Acrylic gallery images are derived from the same production image, not unrelated alternate products.

Next automation improvement:

- Add `image_quality_gate.py` to produce scores for brightness clipping, contrast, sharpness, and crop safety.
- Fail only on hard defects; soft aesthetic concerns go into `REVIEW_RECOMMENDED`.

## 4. Account Firewall / Shadow-Ban Pre-emption

Prompt:

> If one Etsy shop has login abnormality, can the system isolate via physical MAC address and browser fingerprint so it does not spread to other backup accounts?

Answer:

I will not design a system to evade Etsy/eBay detection, spoof fingerprints, bypass suspension, or continue operating backup accounts after one account is flagged. That is not safe for Rex's long-term business.

Also, a website normally does not see the laptop's LAN MAC address. MAC spoofing is not a reliable or appropriate marketplace safety control.

### Correct Account Firewall Definition

In this project, "account firewall" means compliant containment, not evasion.

Entity boundaries:

- Shop ID.
- Marketplace account.
- API credential/token.
- Browser profile directory.
- Cookie jar/session.
- Automation queue.
- Publish budget counter.
- Risk state file.

If one shop/account shows login anomaly:

1. Immediately stop all write actions for that marketplace.
2. Quarantine that browser profile/session.
3. Stop paid publish actions.
4. Preserve logs/screenshots.
5. Do not switch to a backup account to continue the same activity.
6. Resume only after account health is understood.

### Current Architecture State

Current system already has pieces of this:

- Dedicated automation Edge profile on CDP port 9223.
- Etsy login block recorded as a hard publish pause.
- API pending/inactive state prevents Etsy API publishing.
- Paid Etsy publish is not allowed while login/account state is unstable.
- eBay/Printify local queues are separate from Etsy queues.

Needed next:

- Add `Account_Risk_State.json` with per-marketplace states:
  - `OK`
  - `READ_ONLY`
  - `LOGIN_ANOMALY`
  - `PUBLISH_PAUSED`
  - `PAID_ACTION_PAUSED`

- Make every publish script check this state before writing online.

### Millisecond-Level Claim

I should not claim millisecond-level platform containment. The correct engineering target is deterministic preflight blocking before any write action. That is enough for this project because all high-risk actions pass through scripts/queues.

## Summary For Rex

This round's operational changes:

- Treat 0-view as a search/category/account-weight experiment, not a network issue.
- Etsy paid publishing must have a hard financial kill-switch.
- Add image QA beyond text generation to catch fake-looking products.
- Account firewall is compliant quarantine and queue blocking, not fingerprint evasion.

Recommended next files to implement:

- `Database/Etsy_Fee_Kill_Switch.json`
- `Database/Account_Risk_State.json`
- `modules/image_quality_gate.py`
- publish-script preflight checks against risk state and fee cap.
