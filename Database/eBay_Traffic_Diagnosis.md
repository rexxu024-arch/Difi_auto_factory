# eBay Traffic Diagnosis

Generated: 2026-05-06 12:52:27 -0400 America/New_York

## P100 Sticker live cover/gallery mismatch is a primary blocker.
- Evidence: Cover fix queue contains 49 rows; latest snapshot has 42/50 zero-view rows despite 50 promoted rows.
- Action: Do not expand Sticker count. Repair Printify source defaults and re-audit live eBay covers before more Sticker publish.
- Network dependency: medium

## P90 Promoted Listings Standard 2% is active but is not enough alone.
- Evidence: Latest snapshot 2026-05-06 01:23:31 -0400: promoted=50, zero_views=42, rows=50.
- Action: Keep 2% Standard as baseline, but treat image/search-intent repair as the growth lever. Do not raise to suggested ad rates yet.
- Network dependency: low

## P80 Poster/Acrylic currently show more early movement than Sticker.
- Evidence: Acrylic: rows=9 views=2 moved=2; Poster: rows=9 views=7 moved=4; Sticker: rows=32 views=2 moved=2
- Action: Keep the near-term product mix tilted toward Poster/Acrylic and Etsy digital printables until Sticker cover issue is fixed.
- Network dependency: low

## P70 Title rewrite experiment has not produced a clear Sticker lift yet.
- Evidence: A_TITLE_INTENT_REWRITE: moved=0/18; B_COVER_QA_PRIORITY: moved=0/14; C_HOLDOUT_CONTROL: moved=0/12
- Action: Continue the controlled experiment window, but do not churn all titles daily. Next test should combine buyer-intent titles with corrected cover/gallery.
- Network dependency: low
