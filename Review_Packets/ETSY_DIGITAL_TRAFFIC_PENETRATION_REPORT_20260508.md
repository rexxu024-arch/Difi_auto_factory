# Etsy Digital Traffic Penetration Report

Generated: 2026-05-08 08:00:10 -0400 America/New_York

## Summary

- Published digital listings confirmed locally: 10
- Public active/readable listings in latest live audit: 10
- Prepared but unpublished draft-queue candidates: 20
- Queue statuses: `PUBLISHED_UI_CONFIRMED=10`, `RELEASED_TO_DRAFT_QUEUE=20`
- QA status: `PASS=30`
- Confirmed Etsy listing-fee spend total: `$2.00`
- Confirmed Etsy listing-fee spend today: `$0.00 / $6.00` daily gray cap
- Next 20 candidates remain no-spend prepared assets; no new listing fees were triggered.

## Traffic Stats

- Views/favorites/orders are still not available from local files.
- Etsy Open API remains unavailable: `PENDING_OR_INACTIVE`, HTTP `403`, next step `WAIT_APP_APPROVAL_OR_VERIFY_SECRET`.
- Safe public readback confirms the 10 published listings are active/readable, digital, and image-complete, but public pages do not expose shop-manager traffic stats.
- Treat current traffic as `UNREAD`, not `ZERO`, until Seller/Etsy stats are read from Shop Manager or API becomes active.

## Live Public Readback

| ID | Etsy Listing ID | Price | Status | Digital | Images |
|---|---:|---:|---|---|---:|
| Poster-Academia-0001 | 4500654287 | $6.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Academia-0002 | 4500664506 | $6.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Academia-0003 | 4500665474 | $6.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Academia-0081 | 4500657145 | $6.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Academia-0082 | 4500667154 | $6.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Academia-0083 | 4500667734 | $12.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Academia-0084 | 4500668282 | $6.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Academia-0085 | 4500668786 | $6.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Academia-0091 | 4500660013 | $6.99 | ACTIVE_READABLE | YES | 20 |
| Poster-Zen-0001 | 4500669878 | $9.99 | ACTIVE_READABLE | YES | 20 |

## Blockers

- Etsy API app/key is still pending or inactive, so automated traffic stat pull is blocked.
- Browser/UI stats read should remain read-only and should not trigger publish, renewal, ads, or fee-bearing actions.
- Do not release the next paid batch until at least one of these is true:
  - Shop Manager stats are safely read.
  - Etsy API becomes active.
  - Rex explicitly authorizes the next `$2` gray-cell spend despite unread traffic.

## Next Action

1. Hold Etsy spending at `$2.00` total and `$0.00` today.
2. Keep the 20 no-spend candidates staged.
3. Next safe action is read-only Shop Manager traffic capture for views/favorites/orders.
4. If the 10 published listings show no views after a real stats read, rewrite the next batch toward lower-competition buyer-intent phrases before spending another `$2`.

## Money Guard Verdict

- PASS: no new fee was spent.
- PASS: daily cap is untouched today.
- PASS: public listing availability is healthy.
- STOP: no next-batch publish until traffic stats are read or Rex explicitly spends the next gray cell.
