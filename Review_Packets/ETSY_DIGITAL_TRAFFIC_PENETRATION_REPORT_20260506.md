# Etsy Digital Gray Launch - Traffic Penetration Report

- Updated: 2026-05-06 21:58:00 -04:00 America/New_York
- Status: FIRST BATCH LIVE
- Confirmed Etsy UI route: dedicated Edge profile, CDP port 9223
- Published listings: 10
- Confirmed listing-fee spend: $2.00
- Batch cap: $2.00
- Daily gray cap: $6.00
- Total no-result test pool: $40 normal cap, $60 only with written rationale

## Current Verdict

The first Etsy Digital gray batch is live. This is no longer blocked by Etsy login.

The correct next action is not to blindly spend the remaining pool. The first 10 need a traffic/indexing readout first: views, favorites, search impressions if available, and whether any product gets early signal.

## Live Batch

| ID | Etsy Listing ID | Price | Status |
|---|---:|---:|---|
| Poster-Academia-0001 | 4500654287 | $6.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Academia-0002 | 4500664506 | $6.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Academia-0003 | 4500665474 | $6.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Academia-0081 | 4500657145 | $6.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Academia-0082 | 4500667154 | $6.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Academia-0083 | 4500667734 | $12.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Academia-0084 | 4500668282 | $6.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Academia-0085 | 4500668786 | $6.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Academia-0091 | 4500660013 | $6.99 | PUBLISHED_UI_CONFIRMED |
| Poster-Zen-0001 | 4500669878 | $9.99 | PUBLISHED_UI_CONFIRMED |

All 10 were published as digital/manual-renewal listings through Etsy UI. Etsy Shop Manager initially showed 12 active listings after the run: these 10 OpenClaw tests plus 2 old legacy DriveFuel listings.

The two legacy DriveFuel listings were then deleted/retired:

- 4407466791 - Impulse Purchase Recovery Kit (Digital Download)
- 4366700475 - DriverFuel_SideHustle_Driver_Planner_Kit

Public verification now shows both legacy pages as unavailable, so the active Etsy shop surface should be the 10 OpenClaw digital tests.

## QA State

- ZIP pack count: 10/10 present.
- ZIP size: under Etsy's 20 MB per-file digital upload limit.
- Pack structure: 5 JPG ratios plus README/license note.
- Listing type: Digital.
- Renewal: Manual.
- AI disclosure / digital download language: present in the descriptions generated for the pack.
- Fee guard: confirmed $0.20 per listing, $2.00 total.
- Public page audit: 10/10 active/readable, 10/10 show digital-download signal. Logged in `Database/Etsy_Digital_Live_Audit.csv`.

## Next Readout

Morning readout should answer:

- Do all 10 listings remain active?
- Are the two legacy listings removed/retired?
- Views per listing.
- Favorites per listing.
- Any search/query data Etsy exposes.
- Which title/price/aesthetic combination has the first non-zero signal.

## Stop / Scale Rules

- If all first 10 remain at 0 views after the initial indexing window, stop additional fee spend and change the test variables before spending more.
- First variable to change: lower-competition search intent and more utility-oriented keywords, not simply more dark-academia volume.
- Second variable to change: product format, such as printable sets, gallery wall bundles, or planner/bookplate downloads.
- Do not exceed the $40 normal Etsy experiment pool without a clear traffic signal and written rationale.
