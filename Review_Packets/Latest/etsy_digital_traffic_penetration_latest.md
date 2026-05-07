# Etsy Digital Traffic Penetration Report

Generated: 2026-05-07 08:01:48 -0400 America/New_York

## Summary

- Published digital listings confirmed locally: 10
- Public active/readable listing ids in last live audit: 10
- Queue statuses: {'PUBLISHED_UI_CONFIRMED': 10, 'RELEASED_TO_DRAFT_QUEUE': 20}
- Metadata statuses: {'PUBLISHED_ETSY_UI_CONFIRMED': 10, 'READY_FOR_ETSY_DRAFT': 29}
- Confirmed Etsy listing-fee spend total: $2.00
- Confirmed Etsy listing-fee spend today: $0.00 / $6.00 daily gray cap
- Next no-spend candidate batch: 10/10 QA-ready; projected fee if later published $2.00; spent now $0.00

## Traffic Stats

- Views/favorites/orders are not available from the current local files.
- Etsy Open API is still unavailable, and I did not open Edge UI during the hardware cooldown window.
- Therefore this report treats traffic as unread, not zero. No performance conclusion should be drawn until Seller/Etsy stats are read.

## Access / Blockers

- Etsy API status: ERROR
- Etsy API next step: WAIT_APP_APPROVAL
- Etsy API detail: HTTP 500: {"error":"Server Error"}
- Etsy risk state: UI_LOGGED_IN_API_PENDING
- Hardware guard at report time: cooldown active due elevated memory; browser/UI readback deferred.

## Published IDs

- Poster-Academia-0001 -> 4500654287 ($0.20)
- Poster-Academia-0002 -> 4500664506 ($0.20)
- Poster-Academia-0003 -> 4500665474 ($0.20)
- Poster-Academia-0081 -> 4500657145 ($0.20)
- Poster-Academia-0082 -> 4500667154 ($0.20)
- Poster-Academia-0083 -> 4500667734 ($0.20)
- Poster-Academia-0084 -> 4500668282 ($0.20)
- Poster-Academia-0085 -> 4500668786 ($0.20)
- Poster-Academia-0091 -> 4500660013 ($0.20)
- Poster-Zen-0001 -> 4500669878 ($0.20)

## Next Action

1. Do not publish the next Etsy batch until traffic stats are read or Rex explicitly wants the next $2 gray cell spent.
2. After cooldown clears, use Edge UI read-only mode to collect views/favorites/orders for the 10 live listings.
3. If live listings still have no Etsy search entry after readback, rewrite the next batch toward lower-competition terms before paying another $2.
4. If any listing has impressions/favorites, publish the prepared next 10 QA-ready candidates under the $2 batch cap and compare Track C search intent.

## Money Guard Verdict

- PASS: no new fee was spent by this report.
- PASS: next 10 candidates are prepared without reservation or publish.
- STOP CONDITION: ambiguous Etsy publish confirmation or duplicate fee risk remains a hard stop.
