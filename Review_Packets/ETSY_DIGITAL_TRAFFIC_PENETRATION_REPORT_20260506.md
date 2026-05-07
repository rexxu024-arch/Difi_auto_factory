# Etsy Digital Gray Launch - Traffic Penetration Report

- Generated: 2026-05-06 20:08:59  (America/New_York)
- Batch: ETSY-DIGITAL-20260506-200824
- Batch hard cap: $2.00
- Daily hard cap: $6.00
- Selected listings: 10
- QA pass/reserved: 10
- QA hold: 0
- Reserved fee: $2.00
- Confirmed spent: $0.00
- Launch status: READY_BLOCKED_ETSY_AUTH

## Guardrail Verdict

- Paid Etsy publish is blocked before spend because account/API access is not yet clean.
- This is the correct money-sensitive behavior: no retry storm, no duplicate fee risk, no listing fee burned while auth is ambiguous.

## First Batch Items

| ID | Price | ZIP MB | QA | Fee | Launch Status |
|---|---:|---:|---|---:|---|
| Poster-Academia-0001 | $6.99 | 11.31 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Academia-0002 | $6.99 | 12.63 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Academia-0003 | $6.99 | 11.36 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Academia-0081 | $6.99 | 11.18 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Academia-0082 | $6.99 | 13.73 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Academia-0083 | $12.99 | 10.09 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Academia-0084 | $6.99 | 12.08 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Academia-0085 | $6.99 | 11.11 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Academia-0091 | $6.99 | 9.17 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |
| Poster-Zen-0001 | $9.99 | 11.28 | PASS | $0.20 | READY_BLOCKED_ETSY_AUTH |

## Tomorrow Morning Readout Logic

- If Etsy access is restored overnight: publish only up to the first 10 passed items, then read views/favorites/orders and compare against the $6 daily cap.
- If all first 10 get 0 views after the initial indexing window: stop further fee spend, rewrite SEO around lower-competition long-tail terms, and test a different digital-product angle before scaling.
- If Etsy access remains blocked: report 0 spend, 10 staged products, and the exact account/API blocker instead of pretending traffic data exists.
