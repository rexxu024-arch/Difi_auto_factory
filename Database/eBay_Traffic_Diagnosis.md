# eBay Traffic Diagnosis

Generated: 2026-05-07 20:57:44 -0400 America/New_York

## P100 Cover Gate is cleared; the current blocker is traffic/product-market fit.
- Evidence: Active cover fix queue is 0 after excluding 50 retired old eBay IDs; latest snapshot has 40/44 zero-view rows despite 44 promoted rows.
- Action: Keep image-order audits in the QA gate, but shift growth effort to Track A/B/C experiments: buyer-intent SEO, product mix, price/room-use positioning, and Etsy digital gray launch.
- Network dependency: low

## P90 Promoted Listings Standard 2% is active but is not enough alone.
- Evidence: Latest snapshot 2026-05-07 18:02:39 -0400: promoted=44, zero_views=40, rows=44.
- Action: Keep 2% Standard as baseline, but treat image/search-intent repair as the growth lever. Do not raise to suggested ad rates yet.
- Network dependency: low

## P85 Repeated or risky gallery images can suppress buyer trust and marketplace quality scoring.
- Evidence: Printify gallery duplicate audit has 22 non-OK rows. This includes exact repeated selected image URLs and non-sticker custom gallery sets that can look like duplicate spam on eBay.
- Action: Pause expansion, repair selected galleries to unique official product mockups, and only resume small-batch publish after duplicate audit is OK.
- Network dependency: medium

## P80 Poster/Acrylic currently show more early movement than Sticker.
- Evidence: Acrylic: rows=22 views=3 moved=2; Poster: rows=22 views=4 moved=2
- Action: Keep the near-term product mix tilted toward Poster/Acrylic and Etsy digital printables until Sticker cover issue is fixed.
- Network dependency: low

## P70 Title rewrite experiment has not produced a clear Sticker lift yet.
- Evidence: A_TITLE_INTENT_REWRITE: moved=0/18; B_COVER_QA_PRIORITY: moved=0/14; C_HOLDOUT_CONTROL: moved=0/12
- Action: Continue the controlled experiment window, but do not churn all titles daily. Next test should combine buyer-intent titles with corrected cover/gallery.
- Network dependency: low
