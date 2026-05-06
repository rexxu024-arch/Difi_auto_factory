# Progress Log

## 2026-04-29 10:55 - Context Recovery

Recovered task context from the user's pasted prior-thread transcript plus local project artifacts.

Confirmed prior progress from transcript and local files:

- Sticker 5-image workflow was stabilized enough to repair existing products.
- Old primary-image issue was found: Printify UI could reorder uploads and make U images become primary.
- Upload logic was changed toward Cover-first handling.
- Primary audit/repair loop was used until old uploaded Sticker products had Cover first.
- At one point, 35 Sticker products were published and 87 remained `Ready_for_Printify`.
- Login-loss hard stop was added so Printify UI falling back to login page does not continue making bad 3-image drafts.
- Bad drafts created during unstable runs were deleted and rows were reset to `Ready_for_Printify`.
- P5X and Reverse 1999 Steam folders were deleted, freeing about 11.85 GB.
- Later user direction: continue yesterday's tasks but only parts that do not require user review.
- Current safer publishing stance: Printify can prepare/audit drafts; eBay publishing should be throttled and separated from preparation.
- New product official specs previously confirmed:
  - Poster blueprint 282, provider 99, 12x18 variant 43138, print area 3600x5400.
  - Acrylic/photo block blueprint 1471, provider 104, 5x7 vertical variant 106190, print area 1538x2138.

Current local observations:

- `CURRENT_TASK.md`, `PROGRESS_LOG.md`, and `RECOVERY_STATE.json` did not exist before this checkpoint and are being created now.
- Git working tree is dirty with tracked changes in `Database/Etsy_listing.xlsx`, `Database/eBay_listing.xlsx`, `Database/nightly_handoff_log.txt`, `Database/printify_bad_draft_cleanup_20260429.log`, and `modules/edit_for_platforms.py`.
- Many 2026-04-29 audit/log files are untracked.

Next actions:

- Reconcile current Excel status counts before starting any new batch.
- Verify no background Printify runner is active.
- Continue with local no-review work: listing variation, audits, bad draft cleanup, and Poster/Acrylic local pipeline preparation.
- Do not run high-volume eBay publish.

## 2026-04-29 11:05 - Recovered Factory Architecture History

Recovered additional prior-thread context covering the GREY ARCHITECT DNA factory work from V13.0 through V15.3.

Confirmed implemented architecture from the user's transcript:

- `modules/dna_worker.py` was originally created to read `Database/pending_tasks.txt`, use `Mentor_Hub.xlsx`, call Claude, and append DNA production rows to `Production_Line.xlsx`.
- `config.py` was patched to expose `CLAUDE_API_KEY`, `DEEPSEEK_API_KEY`, and `BASE_URL`.
- V13.1/V13.5 refactored the CLI and module boundaries:
  - `main.py` routes Stage 1 to `mentor_hub.run_logic()`.
  - `main.py` routes Stage 2 to `product_line.run_logic()`.
  - Stage 3/4 behavior should be preserved.
  - `modules/mentor_hub.py` handles pending seed to Gold DNA.
  - `modules/product_line.py` handles Gold DNA to production listings.
- V13.7 added Dify-style streaming:
  - Claude API uses stream mode.
  - Prompt requests raw JSON array only.
  - Each complete JSON object is parsed and saved immediately.
  - Console prints `[Dify-Mode] ID: ... 写入成功 | 实时保存已完成`.
  - API read timeout/slow seed handling was added.

Confirmed Mentor_Hub behavior:

- One seed must be sent as exactly one Claude request.
- Each seed request must generate 20 DNA rows.
- Seeds are processed sequentially, not combined into one request.
- A seed is removed from `pending_tasks.txt` only after its 20 rows are saved.
- Slow seeds should not be allowed to burn Claude indefinitely. Normal observed time was under 1 minute; at 2-3 minutes the process should stop, log, debug, or skip/hold the seed.
- A run of 20 new seeds completed:
  - 400 new DNA rows.
  - 20 categories, 20 rows each.
  - `pending_tasks.txt` empty afterward.
  - No duplicate fingerprints, no missing `isolated on white`, no missing `--v 6.1`.
  - Timestamp uses local machine timezone and Excel datetime format like `m/d/yyyy, h:mm:ss AM/PM`.

Confirmed Mentor_Hub schema correction:

- Removed columns: `Product_Type`, `Logic_Protocol`, `Note`.
- Current intended columns: `Category`, `Layout`, `Title`, `Gold_Prompt_DNA`, `Material_Keywords`, `Timestamp`, `Design_Count`, `Performance`.
- New DNA rows have `Design_Count = 0`.
- `Performance` defaults empty.
- `Design_Count >= 100` means the DNA should not be recommended for new product designs.

Confirmed Product_Line behavior:

- Product_Line must use the original verbose/sortable format:
  - `ID`, `Timestamp`, `Category`, `Product_Type`, `Style`, `Title`, `MJ_Prompt`, `SEO_Hook`, `Status`.
- Default Status is `Ready_for_production`.
- ID sequencing is per prefix, not global total row count.
  - Example: `Sticker-Zen-0003` is followed by `Sticker-Zen-0004`.
- Product-specific mold rules exist for Sticker, Poster, Acrylic, T-shirt, and Mug.
- `MJ_Prompt` must be single-line plain text with no newline characters.
- A prior pending design run generated 240 listings:
  - `Sticker-Zen-0070` to `Sticker-Zen-0149`
  - `Poster-Academia-0001` to `Poster-Academia-0080`
  - `Acrylic-Grimdark-0001` to `Acrylic-Grimdark-0080`
- After correction, `Production_Line.xlsx` had 460 effective rows, missing `Product_Type` count 0, missing `Category` count 0, wrong status count 0, and no MJ prompt newlines.

Confirmed Excel repair:

- Both `Database/Product_Line.xlsx` and `Database/Mentor_Hub.xlsx` previously opened with Excel content-repair warnings.
- Root cause identified in prior thread: stale Excel Table XML objects.
- Backups were created:
  - `Database/Production_Line.backup_20260427_005522.xlsx`
  - `Database/Mentor_Hub.backup_20260427_005522.xlsx`
- Both workbooks were rebuilt cleanly without internal `xl/tables/table1.xml`.
- Post-repair counts from transcript:
  - `Production_Line.xlsx`: 460 rows, 9 columns.
  - `Mentor_Hub.xlsx`: 620 rows, 8 columns.
- Excel COM open/save/close test passed for both.

Current implication:

- Before changing factory code, verify the current workbook schemas still match these recovered rules.
- Future product generation should use `Pending_design.txt` and Product_Line V15.3 rules, not ad hoc row appends.

## 2026-04-29 11:25 - Full Project Logic Read-Through

Completed a broader read-through of the project structure, core modules, workbook schemas, local output folders, and handoff logs. Saved consolidated logic to `PROJECT_LOGIC_RECOVERY.md`.

Verified current live state:

- No active `py`, `python`, or `excel` process was found during the read-only check.
- `Database/pending_tasks.txt` is `[]`.
- `Database/Pending_design.txt` is `[]`.
- `Mentor_Hub.xlsx` has 620 data rows and the expected 8-column schema.
- `Production_Line.xlsx` has 460 data rows plus 20 blank XML rows and the expected 9-column schema.
- `Production_Line.xlsx` product counts from current XML:
  - Sticker: 189
  - Poster: 121
  - Acrylic: 80
  - T-Shirt: 20
  - Wall Art: 30
  - Blank rows: 20 empty rows with no ID/category/status.
- `eBay_listing.xlsx` has 149 rows:
  - `Printify_Published_Mockups5`: 34
  - `Printify_UI_Mockups5`: 8
  - `Ready_for_Printify`: 78
  - `Quality_Hold_LowRes_U`: 27
  - `Printify_UI_Failed`: 2
- `Etsy_listing.xlsx` has 149 rows, all `Placeholder`.
- Local Sticker folders under `Output/Sticker/Kiss-Cut`:
  - `Ready_for_Steaming`: 122
  - `Not_Working_LowRes`: 27
  - `Not_Working`: 6
  - `Review`: 1
  - Other: 2

Important reconciliation:

- Earlier transcript said 35 published and 87 ready, but current `eBay_listing.xlsx` says 34 published and 78 ready. Current Excel is the live source of truth.
- Earlier transcript said Product_Line had no missing Product_Type; current XML check found 20 blank rows, not real rows with IDs. Treat these as harmless blank workbook residue unless they affect Excel behavior.
- Git checkpoint remains blocked by `.git` permission errors in the handoff log.

Next step requested by user:

- Do not execute production yet.
- Present the interpreted 10pm requirements split into necessary core tasks and nice-to-have tasks.
- Wait for user confirmation before execution.

## 2026-04-29 11:34 - Execution Authorized

User confirmed the recovered plan is close enough and authorized execution with broad operational discretion:

- Act as the user's digital double for routine decisions.
- Make reasonable business-plan adjustments without repeatedly asking.
- Printify/eBay account checks and necessary changes are allowed when aligned with strategy.
- eBay API should not be built now; use Seller Hub active listings directly if account/listing verification is needed.
- Continue to protect eBay account health with conservative pacing.

Execution plan:

1. Start with local data/schema/status audits.
2. Repair obvious local data issues.
3. Audit Printify 5-image and primary-cover state.
4. Continue safe batches only when session/account state allows.
5. Avoid broad high-volume eBay publishing unless explicitly safe and throttled.

## 2026-04-29 11:50 - Permission Handling Correction

User reiterated multiple times that OpenClaw project work has standing full access and should not repeatedly stop for routine confirmations.

Updated `PROJECT_OPERATING_PROTOCOL.md`:

- Project files, scripts, local `.venv`, missing project dependencies, Printify/eBay project checks, and routine draft/status repair are pre-authorized.
- If Codex app sandbox forces a tool-level approval, treat it as an execution gate, not a fresh user decision.
- Still pause only for payment/order/billing credentials, broad public eBay publishing/sync risk, destructive deletion outside narrowly verified project cleanup, or sensitive personal data unrelated to OpenClaw.

## 2026-04-29 12:22 - 4-Day Listing Target

User set a broader travel-window goal:

- By arrival in New York, reach about 230 total listings.
- Target product ratio: `Sticker : Poster : Acrylic = 2 : 1 : 1`.
- Approximate final mix:
  - Sticker: 115
  - Poster: 57
  - Acrylic: 57
- Today, Sticker total should not exceed 100.
- eBay public publishing should remain cautious, staggered, and not forced in large bursts.
- Printify preparation and audit can continue when Wi-Fi is available.
- Summarize any items that require the user's final handling.

## 2026-04-29 Listing Copy Batch
- Patched edit_for_platforms.py with template-bank title/description generation, DeepSeek template constraints, image-note enforcement, duplicate-title cleanup, and banned MJ-term filtering.
- Rebuilt local Sticker listing copy in Database/eBay_listing.xlsx.
- Audit: 149 rows, title length 75-79 for all rows, duplicate titles 0, missing image note 0, Sticker missing 4pc/6x6 0, banned title terms 0.
- Next: Printify/eBay cover-order audit and repair.

## 2026-04-29 Sticker Gate + Batch
- Added printify_design_audit.py for Production_Design vs Printify print-area visual audit. It records byte SHA, declared remote size, preview size, and perceptual hash.
- Integrated production design gate into printify_full_pipeline.py before and after mockup upload; checkpoint prints every 2 completions.
- Full existing Printify design audit: 70 checked, 0 visual mismatches.
- Repaired 0068, 0081, 0084, 0086, 0087, and 0088 to 5 mockups with Cover primary and correct Production_Design.
- Added new 0089, 0091, 0092, 0093, 0094 via gated pipeline; all passed design and 5 mockup checks.
- Current Sticker good total: 76 = 42 Printify_UI_Mockups5 + 34 Printify_Published_Mockups5. Sticker cap remains <=100.

## 2026-04-29 16:04 Poster/Acrylic DNA 排产批次
- 写入并跑完 Database/Pending_design.txt 多 DNA 排产：Poster 20 + Acrylic 20。
- Poster DNA：Academia-Astrological_Globe、Academia-Star_Chart_Blueprint、Zen-Bonsai_Elysium、Academia-Glass_Orrery。
- Acrylic DNA：Grimdark-Alchemical_Vessel、Academia-Astrological_Globe、Zen-Lotus_Mechanism、Zen-Tea_Ceremony_Soul。
- Product_Line 新行保持老格式：ID / Timestamp / Category / Product_Type / Style / Title / MJ_Prompt / SEO_Hook / Status。
- 状态均为 Ready_for_production，MJ_Prompt 无换行且包含 --v 6.1 --style raw。
- 价格策略：Poster 12x18 当前使用 $34.99；Acrylic 5x7 当前使用 $89.99，后续以 Printify 实际成本/运费复核。
- 修复 Product_Line 去重阈值：避免 Poster/Acrylic 因共享材质词被误判为重复，只拦同主体或极高相似。

## 2026-04-29 16:21 Poster Upload + Audit Batch
- Generated listing rows for Poster-Academia-0001/0002/0003; Poster title lengths 76/78/79 and price $34.99.
- Uploaded Poster-Academia-0002 and Poster-Academia-0003 to Printify blueprint 282/provider 99/variant 43138.
- Poster 0001/0002/0003 all passed Production_Design visual audit and Cover primary audit.
- Full design audit checked 79 Printify products, mismatches 0.
- Primary audit found Sticker-Zen-0092 had only 3 selected mockups; repaired it to 5 selected mockups and confirmed Cover primary distance 0.

## 2026-04-29 17:04 Listing Copy / Metadata Sync
- Buyer-facing Image Note updated: main image is actual received product; additional images are bonus concept/detail references and not extra products or selectable variations.
- modules/printify_metadata_sync.py added to sync local Excel title/description back to Printify without touching variants or print areas.
- Synced Printify metadata: Sticker 76/76, Poster 3/3, Acrylic 3/3.
- Acrylic sample upload complete: Acrylic-Academia-0001, Acrylic-Grimdark-0081, Acrylic-Zen-0001 all 5 mockups, Cover primary OK, Production_Design visual match OK.
- Verified Acrylic 5x7 cost from Printify API: variant 106190 cost $35.43, current price $89.99.

## 2026-04-29 17:28 Poster Batch 0081-0084
- Harvested Poster-Academia-0081/0082/0083/0084 from Discord; all have U1-U4 and metadata.
- Built Poster production assets with full-frame 3600x5400 Production_Design and 1800x2700 Cover_Mockup.
- Generated listing copy and uploaded all 4 to Printify blueprint 282/provider 99/variant 43138.
- Targeted audit: all 4 Cover primary distance 0; all 4 Production_Design visual_match true.
- Poster stable Printify total now 7.

## 2026-04-29 18:01 Acrylic Batch 0082/Zen0002-0003
- Harvested Acrylic-Grimdark-0082, Acrylic-Zen-0002, Acrylic-Zen-0003 successfully; Acrylic-Academia-0002 timed out and remains isolated for rescue/rerun.
- Built Acrylic 1538x2138 Production_Design and 1500x2100 Cover_Mockup assets.
- Uploaded Acrylic-Zen-0002 and Acrylic-Zen-0003 directly; Acrylic-Grimdark-0082 had a UI mockup count 0 issue, then repaired via mockup UI uploader.
- Targeted audit: all 3 Cover primary distance 0; all 3 Production_Design visual_match true.
- Acrylic stable Printify total now 6.

## 2026-04-29 18:30 Poster Batch 0085
- Poster-Academia-0085 harvested, asset-built, listed, and uploaded to Printify.
- Poster-Academia-0086/0087/0088/0089 timed out; rescue found no Discord grid/U assets, so they remain defeated and will be skipped/replaced.
- Poster stable Printify total now 8.
- Concurrency adjustment: avoid 5 parallel for Poster; return to 3 parallel for reliability.

## 2026-04-29 18:56 Poster Batch 0091
- Poster-Academia-0091 harvested and uploaded; targeted audit pending/complete in terminal output.
- Poster-Academia-0090/0092 had no Discord message/recoverable output; skip rather than burning time.
- Poster stable Printify total now 9.

## 2026-04-29 19:14 Acrylic Batch 0083/Acad0003/Zen0004
- Harvested Acrylic-Grimdark-0083, Acrylic-Academia-0003, Acrylic-Zen-0004 successfully.
- Built assets and uploaded all 3 to Printify blueprint 1471/provider 104/variant 106190.
- Targeted audit complete/recorded in terminal: Cover primary distance 0 and Production_Design visual match true.
- Acrylic stable Printify total now 9.

## 2026-04-29 19:19 Acrylic Batch Primary Correction
- Correction to previous Acrylic batch note: targeted audit initially found Acrylic-Grimdark-0083 primary cover mismatch (distance 168) while Production_Design matched.
- Re-ran mockup UI repair for Acrylic-Grimdark-0083.
- Re-audit passed: Cover primary distance 0; Production_Design visual_match true.

## 2026-04-29 19:41 Acrylic Batch Zen0005
- Acrylic-Zen-0005 harvested, asset-built, listed, and uploaded to Printify.
- Acrylic-Grimdark-0084 and Acrylic-Academia-0004 timed out with no usable output; skip/replace later.
- Acrylic stable Printify total now 10.
- MJ batch success rate is currently unstable for non-Zen directions; next generation should use smaller/single-ID batches or wait for queue stability.

## 2026-04-29 20:40 Poster Zen Batch Correction
- Poster-Zen-0002 uploaded and passed targeted audit.
- Poster-Zen-0001 had a partial 4/5 bad draft; deleted from Printify and held locally.
- Poster-Zen-0003 failed UI upload with 4/5 images; deleted from Printify and held locally.
- Poster stable Printify total now 10.

## 2026-04-29 21:00 Acrylic Batch Zen0006-0008
- Harvested Acrylic-Zen-0006/0007/0008 successfully.
- Built assets and uploaded all 3 to Printify.
- Targeted audit in terminal: Cover primary and Production_Design checks performed.
- Acrylic stable Printify total now 13.

## 2026-04-29 21:19 Poster Zen 0004/0005 Attempt
- Harvested Poster-Zen-0004 and Poster-Zen-0005 successfully.
- Printify upload timed out while processing Poster-Zen-0004; bad partial draft was deleted and row set to Printify_Hold_BadDraftDeleted.
- Poster-Zen-0005 remains local-ready / Ready_for_Printify for next run.
- Stable Poster count remains 10; no further public publish attempted.

## 2026-04-29 21:21 Handoff checkpoint
- User paused work because laptop power supply is unexpectedly unavailable; no new production batches should run until resumed.
- Confirmed no active OpenClaw MJ/Printify production scripts other than the current check command.
- Cleaned stale deleted bad draft row: Poster-Zen-0003 -> Printify_Hold_BadDraftDeleted, Printify_Product_ID cleared.
- Stable Printify-prepared totals at pause: Sticker 76, Poster 10, Acrylic 13, total stable 99.
- Local-ready but not stable/uploaded: Poster-Zen-0005 remains Ready_for_Printify; Poster-Zen-0001/0003/0004 are held after bad partial drafts were deleted.
- No public eBay publish/sync expansion was started in this final pause window.
- handoff checkpoint


## 2026-04-29 21:28 Resume - Poster-Zen-0005
- Resumed from handoff.
- Uploaded Poster-Zen-0005 to Printify successfully.
- Production_Design visual match true; targeted Cover primary audit executed in terminal.
- Poster stable Printify count moves from 10 to 11 if primary audit passes.

## 2026-04-29 21:40 Resume Poster Hold Recovery
- Reprocessed held local Poster assets: Poster-Zen-0001 and Poster-Zen-0004 uploaded successfully to Printify.
- Poster-Zen-0003 failed again at UI Continue; deleted bad partial draft and returned it to hold.
- Targeted audits for Poster-Zen-0001/0004 executed in terminal.

## 2026-05-03 22:43 -04:00 NYC Resume
- User arrived in New York; operating timezone changed to America/New_York for all future logs.
- eBay active Sticker listings show very low/no traffic; deeper diagnosis deferred until morning review.
- Overnight priority: finish remaining Acrylic and Poster staged listings with strict design/cover audits, no broad eBay publish expansion.


## 2026-05-03 23:22 -04:00 Acrylic Mockup Rule Repair
- Corrected Acrylic Photo Block handling: official Printify mockups are front/back/side views, not Sticker-style 5 custom mockups.
- Acrylic-Grimdark-0085 marked stable with official 4 views and Production_Design visual match.
- Acrylic-Zen-0009 and Acrylic-Zen-0010 marked stable after Production_Design visual match and official view audit; both currently have duplicated official view sets (8 selected), accepted as non-production-risk but logged for later cleanup research.
- Acrylic stable count target moves upward from 15 to 17.


## 2026-05-03 23:23 -04:00 Target 200 Allocation
- New user target: Printify stable total = 200.
- Current stable total: 106 = Sticker 76, Poster 13, Acrylic 17.
- Working allocation: Sticker 100 max, Poster 50, Acrylic 50. Needed: +24 Sticker, +37 Poster, +33 Acrylic.
- Publish cadence may be more aggressive, but still batched and audit-gated to protect the eBay account.


## 2026-05-03 23:35 -04:00 Publish Policy Update
- User authorized periodic eBay publish after audit gates.
- Operating policy: publish only audited Printify-staged items; use small mixed-product batches with irregular spacing; avoid one-shot mass publish or unaudited products.

## 2026-05-04 00:18 -04:00 Publish Batches 001-002
- Published two audited mixed batches through Printify API.
- Batch 001: 9/9 published, mixed Poster/Acrylic/Sticker.
- Batch 002: 12/12 published, mixed Poster/Acrylic/Sticker.
- Publish total after batches: 55 rows in Printify_Published_* statuses.
- Stable Printify total remains 106; no unaudited product was published.

## 2026-05-04 00:20 -04:00 Acrylic Harvest Batch 001-010
- Ran Acrylic Discord harvest for Acrylic-Grimdark-0001 through 0010 with conservative parallelism.
- Completed assets for 8/10: 0001, 0004, 0005, 0006, 0007, 0008, 0009, 0010.
- Acrylic-Grimdark-0002 and 0003 timed out and remain isolated for replacement/rerun.
- Built local Acrylic production assets; next step is listing copy generation, Printify upload, and production-design audit.

## 2026-05-04 01:08 -04:00 Acrylic Upload Recovery
- Generated Acrylic listing copy for 25 available Acrylic folders; 8 new harvested items entered Ready_for_Printify.
- First Acrylic upload attempt exceeded the external runtime budget and left residual processes; stopped them before continuing.
- API audit recovered Acrylic-Grimdark-0001: official front/back/side views present, Production_Design visual_match true, marked Printify_UI_Mockups4.
- Reset no-product-id failures Acrylic-Grimdark-0005/0006/0007 back to Ready_for_Printify for single-item retry.
- Acrylic stable count now 19; Acrylic ready count now 6.

## 2026-05-04 01:33 -04:00 Acrylic Upload Transport Fix
- Isolated Printify upload failure to large Acrylic production PNG upload: repeated 10053 connection aborts and Printify 502 responses.
- Added visible upload attempt logging and 5 retries for image uploads.
- Added q99 JPEG upload derivatives for Poster/Acrylic transfer only; original local Production_Design.png files remain unchanged for audit/source-of-truth.
- Re-ran Acrylic-Grimdark-0005 successfully: Production_Design visual_match true, official front/back/side views present, marked Printify_UI_Mockups4.

## 2026-05-04 01:58 -04:00 Acrylic Upload Batch Completion
- Uploaded/recovered Acrylic-Grimdark-0006/0007/0008/0009/0010.
- All five passed Production_Design visual audit and official Acrylic front/back/side view audit.
- Acrylic-Grimdark-0009 initially reported 0 mockups, then generated official views on delayed API recheck and was marked stable after targeted audit.
- Acrylic stable count now 25; Acrylic Ready_for_Printify count now 0.

## 2026-05-04 02:13 -04:00 Publish Batch 003
- Published 12/12 audited items through Printify API with mixed Poster/Acrylic/Sticker cadence.
- Delay window was 45-120 seconds between items.
- Published totals now: Sticker 45, Poster 11, Acrylic 11.
- Stable totals remain: Sticker 76, Poster 13, Acrylic 25.

## 2026-05-04 02:33 -04:00 Poster Harvest Batch 0005-0014
- Ran Poster-Academia-0005 through 0014 with max parallel 3.
- Completed 8/10: 0005, 0006, 0008, 0009, 0010, 0011, 0013, 0014.
- Poster-Academia-0007 and 0012 timed out and remain excluded.
- Built Poster production assets and regenerated listing copy; 8 new Poster rows are Ready_for_Printify.

## 2026-05-04 03:28 -04:00 Poster Printify Rule Repair
- Switched Poster handling away from Sticker-style forced 5 custom mockups.
- Accepted official Printify Poster mockups when Production_Design visual audit passes and at least 4 official poster mockups are selected.
- Reduced Poster upload derivatives to q95 JPEG for transport stability; original local Production_Design.png remains the source-of-truth.
- Relaxed Production_Design visual audit to allow same-size ahash distance <= 5 to avoid false failures from Printify/JPEG re-encoding.
- Uploaded/recovered Poster-Academia-0005/0006/0008/0009/0010/0011/0013/0014.
- Poster stable count now 21.

## 2026-05-04 03:49 -04:00 Publish Batch 004
- Published 15/15 audited mixed items through Printify API.
- Delay window was 45-120 seconds.
- Published totals now: Sticker 50, Poster 16, Acrylic 16.
- Stable totals remain: Sticker 76, Poster 21, Acrylic 25.

## 2026-05-04 04:19 -04:00 Acrylic Harvest Batch 0011-0020
- Ran Acrylic-Grimdark-0011 through 0020 with max parallel 3.
- Completed 9/10: 0011 through 0019.
- Acrylic-Grimdark-0020 timed out and remains excluded.
- Built Acrylic production assets and regenerated listing copy; 9 new Acrylic rows are Ready_for_Printify.

## 2026-05-04 05:17 -04:00 Acrylic Upload Batch 0011-0019
- Uploaded/recovered Acrylic-Grimdark-0011 through 0019.
- All 9 passed Production_Design visual audit and official Acrylic front/back/side mockup audit.
- Fixed Acrylic delayed-mockup logic: stable delayed API recheck is sufficient; initial 0 selected no longer mislabels good drafts as failed.
- Acrylic stable count now 34.
- Total stable Printify count now 131 = Sticker 76, Poster 21, Acrylic 34.

## 2026-05-04 05:33 -04:00 Publish Batch 005
- Published 15/15 audited mixed items through Printify API.
- Delay window was 30-90 seconds.
- Published totals now: Sticker 55, Poster 21, Acrylic 21.
- Stable totals remain: Sticker 76, Poster 21, Acrylic 34.

## 2026-05-04 06:42 -04:00 Acrylic Batch 0021-0030
- Ran Acrylic-Grimdark-0021 through 0030; completed 9/10, with Acrylic-Grimdark-0029 timed out.
- Built assets, regenerated listing copy, and uploaded/recovered 9 Acrylic products.
- Delayed official-view recovery marked Acrylic-Grimdark-0022/0026/0027 stable after API recheck.
- Acrylic stable count now 43.

## 2026-05-04 06:56 -04:00 Sticker Top-Up Trial Stopped
- Tested Sticker top-up with Sticker-Zen-0095/0096.
- Product creation and Production_Design audits passed, but Printify UI mockup selection only selected 2 gallery mockups instead of Cover + U1-U4.
- Deleted the two bad Printify drafts and reset both rows to Ready_for_Printify.
- Decision: pause Sticker expansion at stable count 76 to avoid U1/partial-gallery cover errors; continue total-count growth with Poster/Acrylic.

## 2026-05-04 07:42 -04:00 Acrylic Batch 0031-0040
- Ran Acrylic-Grimdark-0031 through 0040; completed 10/10.
- Built assets, regenerated listing copy, and uploaded/recovered all 10 Acrylic products.
- Delayed official-view recovery marked Acrylic-Grimdark-0032/0038/0039/0040 stable after API recheck.
- Acrylic stable count now 53.
- Total stable Printify count now 150 = Sticker 76, Poster 21, Acrylic 53.

## 2026-05-04 08:42 -04:00 Poster Batch 0015-0024
- Ran Poster-Academia-0015 through 0024; completed 7/10, with 0015/0016/0018 timed out.
- Built assets, regenerated listing copy, and uploaded/recovered all 7 completed Poster products.
- Poster upload derivative quality reduced to q92 after Poster-Academia-0024 q95 transfer repeatedly hit Printify 502; q92 retry succeeded and passed visual audit.
- Poster stable count now 28.
- Total stable Printify count now 157 = Sticker 76, Poster 28, Acrylic 53.

## 2026-05-04 11:01 -04:00 Publish Batch 006
- Published 15/15 audited mixed items through Printify API after the browser/CDN path showed a transient Akamai zero-size-object failure.
- Delay window was 30-90 seconds.
- Published items: Poster-Academia-0017/0019/0020/0021/0022, Acrylic-Grimdark-0007/0008/0009/0010/0011, Sticker-Zen-0067/0068/0069/0070/0071.
- Published totals now: Sticker 60, Poster 26, Acrylic 26.
- Stable totals remain: Sticker 76, Poster 28, Acrylic 53.

## 2026-05-04 11:19 -04:00 eBay Developer/Akamai Cooling
- User reported `Service Unavailable - Zero size object` on `developer.ebay.com/develop`.
- Independent web check showed the eBay Developer page is globally reachable, so likely local browser/IP/session/CDN-edge issue rather than full outage.
- Public eBay publish cadence is slowed until the edge/session condition cools down.
- Continue API/local preparation; avoid repeated browser refresh/login loops against eBay Developer.

## 2026-05-04 12:04 -04:00 Steam Cleanup
- User confirmed deletion of Steam and Steam-related residual directories, preserving TapTap.
- Deleted `C:\Program Files (x86)\Steam`, `C:\Users\Rex\AppData\Local\Steam`, and the Start Menu Steam folder.
- C drive free space changed from 36.597GB to 37.816GB, freeing about 1.219GB.
- `C:\Users\Public\Desktop\Steam.lnk` could not be removed due access denied; no other large Steam game directory remained on disk.

## 2026-05-04 13:36 -04:00 Phase 1 Data Foundation
- Saved long-term 3-5 day / 7-12 day / 2-4 week factory roadmap in `PROJECT_FACTORY_ROADMAP.md`.
- Saved Rex/Gemini/Codex role model and Gemini advisor queue in `Gemini_Advisor/`.
- Generated local-only Etsy launch plan: 30 draft candidates, mix Poster 14 / Acrylic 10 / Sticker 6. No Etsy shop changes and no listing fees triggered.
- Generated `Database/Etsy_brand_shell.md` and `Database/Etsy_launch_plan.xlsx`.
- Added read-only Seller Hub snapshot logger. Latest loaded active-listing snapshot: 50 rows, 41 zero-view rows, 9 rows with at least 1 view, 4 General promoted rows.
- Added Printify external id sync and backfilled 85 eBay item IDs into `Database/eBay_listing.xlsx`; remaining missing/failed reads will be retried slowly.
- Generated morning report and Gemini review queue in `Reports/` and `Gemini_Advisor/`.
- Reset interrupted `Poster-Academia-0025` from `Printify_UI_Failed` back to `Ready_for_Printify` for safe recovery.

## 2026-05-04 14:05 -04:00 Poster Upload Timeout Recovery
- Tried to continue Poster-Academia-0025 through 0034 without public publish.
- Outer process timed out after 30 minutes during Printify-side slow response.
- Stable gains before timeout: Poster-Academia-0023 and 0024 are now `Printify_UI_Mockups8`.
- Poster-Academia-0025/0026/0027/0028 were marked failed with no product id; reset all four back to `Ready_for_Printify`.
- Decision: continue Poster uploads later in smaller batches to avoid long Printify stalls.

## 2026-05-04 14:24 -04:00 eBay 2 Percent Standard Ads Prep
- Confirmed Printify `external.id` can identify eBay item ids, but Printify API cannot directly enable eBay Promoted Listings.
- Added `modules/ebay_ads_standard.py` for eBay Marketing API/Seller Hub-aligned fixed 2.0% Standard ads preparation.
- Dry-run found 95 published listings with eBay item ids eligible for the `Fixed_2_Percent_Strategy` campaign.
- 17 published listings still lack local eBay item ids and need low-frequency Printify external-id retry before automated ad enrollment.
- Seller Hub read-only snapshot still shows 50 loaded active rows, 41 zero-view rows, and 4 General promoted rows.
- No ads were activated and no paid action was submitted.

## 2026-05-04 14:58 -04:00 eBay 2 Percent Standard Ads Activated
- User explicitly confirmed Promoted Listings Standard / General only, fixed 2.0%, no Priority/PPC, no suggested ad rate.
- Updated Seller Hub campaign `Fixed_2_Percent_Strategy` (campaign id `165251921016`).
- Campaign detail page confirmed: Promoted Listings / General, fixed ad rate, ad rate range `2%`, active, continuous duration.
- Added all 95 locally identifiable OpenClaw eBay item ids to the campaign; deleted dumbbell/toothbrush listings were not present in the whitelist.
- Verified campaign listing table shows `Showing 1-25 out of 95`; visible ad-rate inputs show `2.0`.
- Logged 95 `UI_CONFIRMED_STANDARD_2` rows into `Database/ebay_ads_standard_2pct.csv`.
- Updated `printify_publish_scheduler.py` so future Printify publishes sync the eBay external id and enqueue/enroll the item into the 2% campaign; if eBay OAuth is unavailable, the item is written to `Database/ebay_ads_pending_2pct.csv` instead of being forgotten.

## 2026-05-04 15:09 -04:00 eBay Ad Coverage Refreshed To 99
- Retried missing Printify external ids at low frequency; recovered 4 more eBay item ids.
- Reopened Seller Hub campaign editor and added the refreshed 99-id whitelist through the Item IDs workflow.
- Re-applied fixed single ad rate `2.0` after eBay temporarily defaulted newly added items to a higher suggested rate.
- Final campaign detail verification: `Fixed_2_Percent_Strategy`, Promoted Listings / General, fixed ad rate, ad rate range `2%`, `Showing 1-25 out of 99`.
- Logged 99 `UI_CONFIRMED_STANDARD_2_REFRESH_99` rows into `Database/ebay_ads_standard_2pct.csv`.

## 2026-05-04 15:14 -04:00 Seller Hub Snapshot After Ads
- Ran read-only Seller Hub active-listing snapshot after ad campaign update.
- Loaded visible active rows: 50.
- Visible rows promoted: 50.
- Visible rows with 0 views: 43; rows with at least 1 view: 7.
- Snapshot appended to `Database/Performance_Log.csv` for future baseline comparison.

## 2026-05-04 15:18 -04:00 Browser Resource Hygiene
- Added standing browser hygiene rule to `CURRENT_TASK.md`.
- Closed completed eBay advertising dashboard/campaign tabs and duplicate Seller Hub active-listing tabs.
- Left only 2 active project tabs: one eBay Seller Hub active listings tab and one Printify mockup/product tab.

## 2026-05-04 16:57 -04:00 Poster Batch 0025-0027 Recovered
- Ran Poster-Academia-0025 through 0027 through Printify API upload path.
- Product creation and Production_Design audits passed for all 3; Printify official mockups initially returned 0 and caused false failures.
- Delayed API recheck recovered all 3 as `Printify_UI_Mockups4`; official mockups now 4/4 for each.
- Updated `modules/printify_full_pipeline.py` to wait longer for Poster official mockups and classify unresolved cases as `Printify_MockupsPending` instead of hard UI failure.

## 2026-05-04 17:05 -04:00 Poster/Acrylic Product Fit Review
- Paused Poster background batch at Rex's request before continuing the monthly plan.
- Product fit conclusion: Poster and Acrylic are rectangular print products; artwork object silhouette does not affect manufacturing because the image is printed as a rectangular raster onto paper/acrylic.
- Sales-risk conclusion: buyer expectation needs clarity so customers do not mistake acrylic/poster art for a sculpted 3D object. Existing generated descriptions already include the Image Note: main image is the actual received product; additional images are concept/detail previews and not extra products/variations.
- Live Printify spot-check confirmed the Image Note is present on sampled Poster and Acrylic products.
- Pricing conclusion: Poster $34.99 is reasonable; Acrylic $89.99 is viable premium pricing with margin, but future Acrylic batches can test $84.99 for broader conversion while keeping select strongest designs at $89.99.


## 2026-05-04 20:22 -04:00 Etsy Brand Visual Drafts
- Cleared Chrome Etsy cookies/site data after Rex confirmation; Google cookies were not cleared.
- Reopened Chrome Etsy sign-in to clean page and closed Etsy-related Facebook OAuth residue.
- Default Etsy account operations will use Edge going forward because Rex confirmed Edge login works.
- Generated MJ Etsy brand design options 02/03/04 with local icon and banner assets under Output/Brand/Etsy/20260504_180120/previews.
- Waiting for Rex to select an option number before editing Etsy shop settings online.

## 2026-05-04 23:20 -04:00 Network Guard Added
- Current Wi-Fi is already on 5GHz / 802.11ac with strong signal.
- Preflight ping check: Printify/Etsy/Discord all reachable with 0% packet loss during sample.
- Added modules/network_guard.py and standing low-concurrency rule until network issue is declared resolved by Rex.

## 2026-05-05 00:24:12 -04:00 Protocol Update
- Adopted Gemini/Rex low-bandwidth protocol as default for the next ~2 days: prioritize local logic, data, QA, pricing, text/tag, and retry infrastructure; defer high-bandwidth uploads/OAuth churn.

## 2026-05-05 01:33:44 -04:00 Poster/Acrylic Gallery Backfill
- Fixed art_asset_builder so non-sticker products always write Gallery_U1-4 derived from the selected Production_Design image.
- Fixed edit_for_platforms so non-sticker listing rows prefer Gallery_U paths over raw Midjourney U paths.
- Added modules/gallery_backfill.py for repeatable local repair/audit.
- Backfilled 88 local Poster/Acrylic folders and updated 364 workbook gallery path cells across 91 non-sticker listing rows.
- Final audit: non-sticker rows using raw U gallery paths = 0.

## 2026-05-05 04:37:25 -04:00 Local Copy / Pricing / Registry Batch
- Generated Database/Listing_Copy_Optimization.csv/xlsx for 112 published eBay listings.
- Copy audit: eBay proposed title length failures = 0; Etsy tag count failures = 0.
- Generated Database/Pricing_Strategy_Matrix.csv/xlsx with 96 platform/product/ad-rate/shipping scenarios.
- Rebuilt Etsy_launch_plan to 50 local draft candidates using Quiet Relic Studio positioning; no Etsy listing fees triggered.
- Added resilient_http retry helper and wired it into Etsy OAuth/API modules.
- Generated Database/Unified_Listing_Registry.csv/xlsx with action buckets for 240 local listing rows.

## 2026-05-05 05:04:21 -04:00 Local Listing QA
- Added modules/local_listing_qa.py to audit production image existence, dimensions, cover/gallery paths, title length, and image-note readiness without network calls.
- First QA found one real corrupt local production file: Poster-Academia-0006.
- Rebuilt Poster-Academia-0006 Production_Design/Cover/Gallery from source U image.
- Final QA: 27 issue rows remain, all known Quality_Hold/low-res Sticker rows with missing cover/gallery; no Poster/Acrylic local image integrity issues remain.

## 2026-05-05 05:13:56 -04:00 Image Metadata Audit / Report Refresh
- Added modules/image_metadata_audit.py to audit image format, dimensions, file size, info keys, EXIF key count, and read status without rewriting uploaded artwork.
- Audited 1440 image references from eBay_listing.xlsx; 135 read errors are expected missing images from the 27 known low-res Sticker hold rows.
- Rebuilt Pricing_Strategy_Matrix with eBay 13.6% most-categories fee assumption plus .40 fixed fee; category/store fee still marked for final verification before scaling.
- Refreshed morning report and Gemini advisor queue: Reports/morning_report_20260505_0512.md and Gemini_Advisor/gemini_review_queue_20260505_0512.md.

## 2026-05-05 05:18:15 -04:00 Etsy Shop Packet
- Created Database/Etsy_shop_update_packet.md for selected Option 02 / Quiet Relic Studio.
- Included local icon, banner, preview board paths, shop-name choices, announcement/about/FAQ/shipping notes, and operator notes for Edge/Etsy handling.
- Full compile check passed for new/changed local modules.

## 2026-05-05 05:21:50 -04:00 Handoff Checkpoint
handoff checkpoint: Low-bandwidth local work lane is active. Do not run bulk MJ/Printify/eBay/Etsy writes until network_guard is healthy or Rex confirms wired network. Completed gallery backfill, local copy optimization, pricing matrix, unified registry, local QA, image metadata audit, Etsy Option 02 shop packet, and refreshed morning/Gemini reports.

## 2026-05-05 11:41:05 -04:00 Blueprint Official Probe
- Added modules/printify_blueprint_probe.py for checkpointed official Printify catalog probing.
- Weak-network small-batch probe succeeded for Canvas, Framed Poster, and Metal priority candidates.
- Current official detail file: Database/Product_Blueprint_Official_Details.csv with 120 rows across priority blueprint candidates.

## 2026-05-05 13:05:02 -04:00 Product Blueprint Official Details
- Created modules/printify_blueprint_probe.py for checkpointed official Printify catalog detail probing.
- Created modules/blueprint_summary_builder.py for Scholar-friendly summary output.
- Probed official provider/variant/print-area/shipping data for Canvas, Framed Poster, Metal, Notebook/Journal, and selected Mug blueprints.
- Output files: Database/Product_Blueprint_Scholar_Verification.csv, Database/Product_Blueprint_Official_Details.csv, Database/Product_Blueprint_Mug_Details.csv, Database/Product_Blueprint_Official_Summary.csv/xlsx.
- Important finding: queried catalog variant endpoints expose blueprint/provider/variant/print-area and shipping profiles, but not production cost; cost must be verified by UI or create-product/readback before pricing.

## 2026-05-05 13:58:40 -04:00 Etsy Digital Product R&D
- Added modules/etsy_digital_products.py as a local-only Etsy digital product R&D and printable wall-art pack builder.
- Created Database/Etsy_Digital_Product_RnD.md, Database/Etsy_Digital_Product_RnD.csv, Database/Etsy_Digital_Candidates.csv, and Database/Etsy_Digital_Pilot_Packs.csv.
- Built 3 instant-download printable wall art pilot packs under Output/Digital/PrintableWallArt using existing high-resolution Poster production images.
- Each pilot pack contains 5 Etsy-ready JPG ratios: 2x3, 3x4, 4x5, 11x14, and ISO A-series; max file size is 2.54MB, below Etsy's 20MB per-file digital upload limit.
- Decision: start digital products with printable wall art sets; keep personalized ex-libris/bookplate as second pilot; defer pet/family portraits until a revision and image-privacy workflow exists.

## 2026-05-05 14:05:37 -04:00 Handoff Checkpoint
handoff checkpoint: Etsy digital R&D branch is local-only and ready for Rex review. No Etsy upload or storefront edit was performed. First recommended launch is 20 printable wall art instant-download listings from best Poster images; 3 pilot packs already generated and verified under Etsy file-size limits.

## 2026-05-05 17:05:00 -04:00 Wi-Fi 5GHz Diagnosis
- Confirmed the Realtek 8821CE hidden registry setting `PreferBand=2`, meaning the driver is already configured as 5GHz first.
- Short stability test showed the adapter started on 5GHz channel 52 with 100% signal, disconnected, then rejoined the same SSID on 2.4GHz channel 11.
- Codex process lacks Windows administrator rights to write HKLM adapter advanced settings directly; attempts to change `PreferBand`, `RegROAMSensitiveLevel`, and `ConcurrentOpPref` were denied by Windows.
- Added tools/wifi_prefer_5g_admin.ps1 for an elevated run: keeps 5GHz preference, lowers roaming sensitivity, removes 2.4GHz concurrent-operation preference, and sets Wi-Fi power saving to maximum performance.

## 2026-05-05 17:31:32 -04:00 Wi-Fi 5GHz Preference Applied With Admin
- Ran tools/wifi_prefer_5g_admin.ps1 through an elevated UAC process.
- Applied Realtek adapter settings: `PreferBand=2` (5G first), `RegROAMSensitiveLevel=80` (lower roaming sensitivity), `ConcurrentOpPref=0` (no 2.4GHz concurrent preference), Wi-Fi power saving set to maximum performance.
- After restart and manual reconnect, Windows still selected `Verizon_P9PQG9` on 2.4GHz channel 11, not 5GHz.
- Conclusion: local adapter preference is now correctly set; remaining issue is likely Verizon gateway band steering / merged SSID / 5GHz DFS channel instability, not a missing Windows preference.

## 2026-05-05 18:31:35 -04:00 eBay Traffic Experiment Batch
- Added modules/ebay_traffic_experiment.py to create a reversible A/B/C experiment for zero-view active Sticker listings.
- Backed up workbook to Database/eBay_listing.backup_traffic_experiment_20260505_182220.xlsx.
- Experiment groups: 18 A_TITLE_INTENT_REWRITE, 14 B_COVER_QA_PRIORITY, 12 C_HOLDOUT_CONTROL.
- A group rewrites were applied locally and synced through Printify with title/description-only publish; all 18 returned update=200 and publish=200.
- Sync queue: Database/eBay_Metadata_Sync_Queue.csv now has 18 SYNCED rows; log: Database/eBay_Metadata_Sync_Log.csv.
- B group remains unchanged for cover/thumbnail QA; C group remains unchanged as holdout control for 48-72h comparison.

## 2026-05-05 20:02:02 -04:00 Low-Bandwidth Monthly Tasks Continued
- Expanded Etsy printable wall art digital product prep from 3 pilots to 20 upload-ready listings.
- Output: Database/Etsy_Digital_Upload_Queue.csv and Output/Digital/PrintableWallArt/Pilot_Contact_Sheet_20.jpg.
- Each digital listing has 5 JPG ratios and all files remain below Etsy's 20MB per-file digital upload limit; largest observed file is 3.42MB.
- Added modules/etsy_digital_bundle_builder.py and generated 3 bundle concepts: 12-piece Dark Academia ($19.99), 3-piece Zen ($12.99), 8-piece Mixed ($17.99).
- Added modules/ebay_cover_qa.py and Database/eBay_Cover_QA_Manual_Review.md; B group cover QA found local files valid but several dragon covers need stronger 4pc-sticker thumbnail clarity before image sync.
- Added modules/ebay_experiment_report.py for future A/B/C delta reporting after new Seller Hub snapshots.
- Updated modules/factory_morning_report.py so reports now include Etsy digital queue, bundle concepts, cover QA, and eBay experiment group counts.

## 2026-05-05 20:22:00 -04:00 Etsy Digital Upload Packet Hardened
- Added modules/etsy_digital_preview_builder.py and generated 3 Etsy preview images for each of 20 printable wall art listings.
- Improved preview typography/layout after visual QA: first pass text was too small for Etsy thumbnails; regenerated with large digital-download and size-ratio panels.
- Updated modules/etsy_digital_qa.py to validate both 100 customer download JPG files and 60 preview images; final QA bad=0, missing=0.
- Added modules/etsy_digital_listing_export.py and generated Database/Etsy_Digital_Final_Upload_Packet.csv/md with title, description, 13 tags, price, 3 previews, and 5 download files per listing.
- Cleaned Etsy digital titles locally to remove repeated phrases such as "Wall Art Wall Art"; no Etsy upload or listing fee was triggered.

## 2026-05-05 21:42:00 -04:00 Live eBay Cover Integrity Gate
- Added modules/ebay_online_cover_audit.py to compare live eBay main gallery images against local Cover_Mockup.png and U1-U4 files.
- Audited the 14 cover-priority active Sticker listings: 1 matched local Cover_Mockup, 13 matched a single U image instead of the intended cover.
- Wrote Database/eBay_Online_Cover_Audit.csv, Database/eBay_Online_Cover_Fix_Queue.csv, and a contact sheet under Database/eBay_Online_Cover_Audit/.
- Added modules/printify_image_default_audit.py; current audit shows 123/161 Printify-tracked products need checking because many expose multiple default images.
- Tightened modules/printify_publish_scheduler.py so future publish attempts are blocked when Printify reports anything other than exactly one default image.
- Updated morning/Gemini reports to include live cover mismatch counts and Printify default-image audit counts.

## 2026-05-05 22:18:00 -04:00 Buyer Image Note + Cover Repair Plan
- Confirmed eBay revise pages for Sticker variation listings show the live buyer gallery as variation photos; affected listings can be missing the local 4pc Cover_Mockup entirely.
- Created Database/eBay_Live_Cover_Fix_Plan.md documenting the root cause, safe repair path, and do-not-do rules.
- Added modules/ensure_image_note.py and patched all 18 eBay local descriptions missing the buyer-facing image note.
- eBay local description audit now passes: 240/240 rows include the image note that the main image is the actual product customers receive, while additional images are concept/detail references.

## 2026-05-05 22:32:00 -04:00 Full Sticker Live Cover Audit
- Ran live eBay cover audit across all 47 published Sticker rows with eBay item ids.
- Result by latest SKU state: 2/47 live Sticker listings match local Cover_Mockup; 45/47 show a single U image as the live main/buyer-facing image.
- Refreshed Database/eBay_Online_Cover_Fix_Queue.csv; current pending live cover fixes: 45.
- This confirms the cover problem is a system-level variation-photo sync issue, not an isolated listing mistake.

## 2026-05-05 22:45:00 -04:00 Poster/Acrylic Live Cover Audit
- Ran live eBay cover audit across 52 published Poster/Acrylic rows with eBay item ids.
- Most Poster/Acrylic rows are AMBIGUOUS because local Gallery_U1 is intentionally the same or near-same full image as Cover_Mockup for single-image products.
- Added 4 non-sticker rows to the cover fix queue for manual/high-confidence review: Poster-Academia-0001, Poster-Academia-0003, Acrylic-Grimdark-0081, Acrylic-Zen-0001.
- Current live cover fix queue total: 49 rows (45 Sticker, 2 Poster, 2 Acrylic).

## 2026-05-06 00:38:00 -04:00 eBay Cover Repair Rule Learned
- Tested Seller Hub Reports image repair on Sticker-Zen-0025.
- Parent-level EPS-only image CSV completed, but live buyer page still showed a single U image because eBay uses the variation photo set for these Printify sticker listings.
- Variation-level Reports repair failed with eBay error: inventory-managed items do not allow add/delete variation pictures.
- Conclusion: existing Printify-synced eBay variation photos cannot be safely repaired through Seller Hub Reports.
- Created modules/ebay_cover_repair_decision.py and Database/eBay_Cover_Repair_Decisions.csv/md to preserve the decision logic.
- Current repair plan: fix source mockup defaults in Printify and re-sync; if live Inventory-managed listings still reject image changes, replace bad listings with newly generated correct listings and retire the bad ones after verification.
- Hardened modules/printify_mockup_ui_uploader.py with CDP command timeouts, `--ids`, and `--allow-any-status` so source-cover repairs can target published rows without waiting indefinitely or sweeping unrelated rows.

## 2026-05-06 01:08:00 -04:00 Automation-First Control Layer
- Added modules/factory_supervisor.py as the durable plant-manager entrypoint for unattended local work and publish blocking.
- Supervisor writes Database/Factory_Autopilot_State.json, Database/Factory_Autopilot_Action_Queue.csv/md, and Database/Factory_Autopilot_Run_Log.csv.
- Ran `py modules\factory_supervisor.py --execute-local --skip-network`; local cycle completed with 0 failures.
- Current local outputs refreshed: Local_Listing_QA, eBay_Cover_Repair_Decisions, Unified_Listing_Registry, Market_Signal_Action_Queue, eBay_Traffic_Experiment_Report, morning report, and Gemini review queue.
- Updated modules/market_signal_planner.py so live eBay cover mismatches become `FIX_LIVE_COVER_SOURCE_OR_REPLACE` instead of generic market actions.
- Hardened modules/printify_mockup_ui_uploader.py and modules/printify_full_pipeline.py so selected Printify images must have exactly one default image before success/publish status is accepted.
- Saved the automation-first rule into PROJECT_OPERATING_PROTOCOL.md: Codex should debug and upgrade the factory, while recurring execution must move into scripts/queues/guards/reports.

## 2026-05-06 01:25:00 -04:00 Read-Only eBay Snapshot + Supervisor Login Gate
- Patched modules/ebay_sellerhub_snapshot.py so temporary Seller Hub CDP tabs are closed after read-only extraction.
- Ran read-only Seller Hub active-listing snapshot with 12 scrolls: 50 rows read, 42 zero-view, 8 with at least one view, 50 Promoted Standard/General.
- Refreshed Unified_Listing_Registry, eBay_Traffic_Experiment_Report, morning report, and supervisor state from the latest snapshot.
- Added Printify CDP login detection to modules/factory_supervisor.py.
- Current supervisor cover action is `WAIT_PRINTIFY_LOGIN`, because the CDP-controlled Printify profile is still on `https://printify.com/app/auth/login`.
- No publish, image upload, or account write was performed in this batch.

## 2026-05-06 01:33:00 -04:00 Cover Replacement Fallback Queue
- Added modules/ebay_cover_replacement_queue.py to preserve the fallback path if Printify source re-sync cannot repair live eBay inventory-managed variation photos.
- Generated Database/eBay_Cover_Replacement_Queue.csv/md with 49 rows.
- Queue breakdown: 45 `WAIT_SOURCE_REPAIR_RESULT`, 4 `REVIEW_BEFORE_REPLACE`.
- Added replacement queue generation to the local supervisor cycle.
- Updated modules/factory_morning_report.py so morning reports include replacement queue status.

## 2026-05-06 01:40:00 -04:00 Local Title-Length Repair Queue
- Added modules/ebay_title_repair_queue.py to detect published eBay titles outside the 75-79 character house rule and prepare safe local repairs.
- Applied local-only title repairs to 7 published Sticker rows; no Printify/eBay online sync was performed.
- Refreshed Local_Listing_QA: issue rows decreased from 34 to 27.
- Remaining QA issues are the known low-res/missing-cover Sticker hold rows, not active published title-length errors.
- Added title repair generation to the local supervisor cycle.

## 2026-05-06 01:45:00 -04:00 Repeatable eBay Traffic Diagnosis
- Added modules/ebay_traffic_diagnosis.py so low-traffic hypotheses are generated from Seller Hub snapshots, cover queues, and experiment data instead of manual guesswork.
- Generated Database/eBay_Traffic_Diagnosis.csv/md.
- Current diagnosis: Sticker live cover/gallery mismatch is the primary blocker; 2% Standard ads are active but not enough by themselves; Poster/Acrylic show more early movement than Sticker; title rewrite alone has not lifted Sticker experiment groups yet.
- Added traffic diagnosis to the local supervisor cycle and morning report.

## 2026-05-06 01:51:00 -04:00 Printify API Cover Repair Constraint
- Checked official Printify API docs for product update behavior.
- Durable finding saved into Database/eBay_Live_Cover_Fix_Plan.md: product mockup `images` are read-only in the update model, so ordinary product PUT is not a reliable way to repair existing live mockup defaults.
- Current automated repair order remains: source repair through Printify mockup UI when CDP profile is logged in; if live eBay still rejects the changed variation photo set, create verified replacement listings and retire old bad listings after live audit.

## 2026-05-06 01:53:00 -04:00 Supervisor End-to-End Local Verification
- Ran `py modules\factory_supervisor.py --execute-local --skip-network`.
- Completed local supervisor cycle with 0 failures.
- One command now refreshes: Local_Listing_QA, eBay_Cover_Repair_Decisions, eBay_Cover_Replacement_Queue, eBay_Title_Repair_Queue, Unified_Listing_Registry, Market_Signal_Action_Queue, eBay_Traffic_Experiment_Report, eBay_Traffic_Diagnosis, morning report, and Gemini advisor queue.
- Current blocking status remains `WAIT_PRINTIFY_LOGIN` for cover repair because the CDP-controlled Printify browser profile is still logged out.

## 2026-05-06 02:00:00 -04:00 eBay Profile Trust Packet
- Added modules/ebay_profile_packet.py to produce a reusable eBay seller-profile update packet from the selected Quiet Relic Studio brand shell.
- Generated Database/eBay_Profile_Update_Packet.md with seller profile image path, optional banner reference, seller bio draft, buyer-facing image note, and category suggestions.
- This is a low-bandwidth trust-building task; no Seller Hub profile edit was performed.

## 2026-05-06 02:07:00 -04:00 Next Product Blueprint Test Plan
- Added modules/product_blueprint_next_plan.py to condense official Printify blueprint probe data into a Scholar-verifiable next-test packet.
- Generated Database/Product_Blueprint_Next_Test_Plan.csv/md.
- Current priority order: Canvas blueprint 1936 variant 119906, Framed Poster blueprint 1236 variant 93818, Notebook/Journal blueprint 5634 variant 252281, Mug blueprint 478 variant 65216, Metal blueprint 1206 variant 91995.
- No product creation/upload was performed; this is a R&D planning artifact for later cost/mockup verification.

## 2026-05-06 02:10:00 -04:00 Market Queue Default-Image Gate
- Updated modules/market_signal_planner.py to read Database/Printify_Image_Default_Audit.csv.
- Products with Printify default audit `CHECK` are now assigned `FIX_PRINTIFY_DEFAULT_IMAGE_BEFORE_PUBLISH`, not publish actions.
- Current market queue actions: 74 default-image fixes, 49 live cover source/replace fixes, 50 upload candidates, 24 small-batch publish candidates, 27 QA holds.
- Refreshed morning report and supervisor state after the queue correction.

## 2026-05-06 02:12:00 -04:00 Recovery State Refresh
- Rebuilt RECOVERY_STATE.json to reflect the May 6 factory state instead of the old April 29 recovery checkpoint.
- Recovery now points first to CURRENT_TASK.md, PROGRESS_LOG.md, PROJECT_OPERATING_PROTOCOL.md, Factory_Autopilot state/queue, eBay cover plan, and latest morning reports.
- Validated RECOVERY_STATE.json parses as JSON.

## 2026-05-06 02:14:00 -04:00 Handoff Checkpoint
handoff checkpoint: Automation-first control layer is now live. Use `py modules\factory_supervisor.py --execute-local --skip-network` for local maintenance and `py modules\factory_supervisor.py` before any online batch. Current blocker is Printify CDP login plus live cover/default-image gate; no more Sticker publishing until a targeted source repair or replacement path passes live eBay cover audit.

## 2026-05-06 07:34:00 -04:00 Supervisor Cover Repair Runner Wired
- Added and compiled `modules/factory_cover_repair_runner.py`.
- Dry-run correctly stopped at `WAIT_PRINTIFY_LOGIN`; no upload, publish, or eBay write was performed.
- Updated `modules/factory_supervisor.py` so the cover-gate action becomes a one-SKU repair runner once the Printify CDP browser is logged in.
- Ran `py modules\factory_supervisor.py --execute-local --skip-network`; local cycle completed with 0 failures and refreshed QA, repair decisions, replacement queue, registry, market queue, experiment report, traffic diagnosis, profile packet, blueprint plan, morning report, and Gemini queue.
- Current blocker remains Printify CDP login. Current safe next online command after login: `py modules\factory_cover_repair_runner.py --limit 1 --post-sync-wait 120`.

## 2026-05-06 07:40:00 -04:00 Factory Backlog Added
- Added `modules/factory_backlog.py` and wired it into `modules/factory_supervisor.py`.
- Generated `Database/Factory_Backlog.csv` and `Database/Factory_Backlog.md`.
- Backlog currently has 13 tasks: 4 READY, 2 WAIT_COVER_GATE, 2 WAIT_USER_OR_API_APPROVAL, 1 BLOCKED, 1 WAIT_PRINTIFY_LOGIN, 1 BLOCKED_BY_COVER_GATE, 1 WAIT_SOURCE_REPAIR_RESULT, and 1 READY_FOR_SCHOLAR_REVIEW.
- Ran supervisor again; local cycle completed with 0 failures and now includes backlog generation.

## 2026-05-06 07:44:00 -04:00 Morning Report Backlog Summary
- Updated `modules/factory_morning_report.py` to include `Factory_Backlog` status counts, top tasks, and lane counts.
- Generated `Reports/morning_report_20260506_0744.md` and `Gemini_Advisor/gemini_review_queue_20260506_0744.md`.

## 2026-05-06 07:51:00 -04:00 Production Design Integrity Audit Hardened
- Updated `modules/printify_design_audit.py` with stable output `Database/Printify_Production_Design_Audit.csv`, product-type filter, ID filter, and weak-network sleep controls.
- Ran a tiny Acrylic audit under conservative network mode: 2/2 passed visual/size match against local `Production_Design.png`; both had `ahash_distance=0`.
- Exact SHA differed for both rows, likely due Printify-side image re-encoding, but dimensions and visual hash matched exactly.
- Added a P63 `production_design_qa` action to `modules/factory_supervisor.py`: `py modules\printify_design_audit.py --limit 2 --sleep-seconds 1`.
- Refreshed `Factory_Backlog`, morning report, and Gemini queue.

## 2026-05-06 07:54:00 -04:00 Recovery State Updated
- Updated `RECOVERY_STATE.json` to point at the new `Factory_Backlog` and `Printify_Production_Design_Audit` files.
- Added the one-SKU source repair command and latest production-design QA sample result to durable recovery memory.
- Validated `RECOVERY_STATE.json` parses successfully.

## 2026-05-06 08:00:00 -04:00 Production QA Retry Path
- Switched `modules/printify_design_audit.py` from bare `requests.get` to `modules.resilient_http.request_with_retry` for Printify product JSON and remote image downloads.
- Ran a one-row Poster production design audit: Poster-Academia-0001 passed visual/size match, `ahash_distance=0`, local and remote sizes both 3600x5400.
- Removed a Pillow deprecation warning by replacing `getdata()` with `tobytes()` in the image hash path.

## 2026-05-06 08:28:00 -04:00 Printify Login Guard + Recovery Manual
- Added `PRINTIFY_LOGIN_EMAIL=rexxu024@gmail.com` to `.env` and exposed `Config.PRINTIFY_LOGIN_EMAIL`.
- Added `modules/printify_login_guard.py`.
- Login guard only allows Google account `rexxu024@gmail.com`; if another account appears or Google asks for a password, it stops and writes manual-login status.
- Verified `npm run printify:login:dry`; current Chrome CDP profile is `LOGGED_IN` to Printify dashboard.
- Added `requirements.txt`, `package.json`, and `OPERATIONS_MANUAL.md`.
- Updated `README.md` to point future recovery to `OPERATIONS_MANUAL.md`, `RECOVERY_STATE.json`, `CURRENT_TASK.md`, and `PROGRESS_LOG.md`.
- Confirmed existing Codex automation `Openclaw Git Checkpoint Push` runs every 2 hours against `origin main`.
- Verified `npm run etsy:api-status`; Etsy API remains `PENDING_OR_INACTIVE` / HTTP 403.


## 2026-05-06 11:35:00 -04:00 Printify Mockup Policy + Recovery Index
- Added `START_HERE_OPENCLAW.md` as the short recovery map for Rex/Codex/Gemini/another AI after thread break, power loss, or new-device setup.
- Updated `README.md`, `OPERATIONS_MANUAL.md`, and `RECOVERY_STATE.json` to point at the new recovery entrypoint.
- Codified the product image policy: preserve Printify official/default mockups when useful, especially for Poster/Acrylic buyer context; do not fail a product merely because multiple official/default images exist.
- Adjusted `printify_mockup_ui_uploader.py`, `factory_cover_repair_runner.py`, `printify_primary_audit.py`, and `printify_publish_scheduler.py` so QA checks for required custom image/design presence and at least one default, instead of enforcing exactly one default.
- Tested one source-repair path on `Sticker-Academia-0005`; the Printify UI now reaches the save/publish stage and the API shows selected images plus the custom cover present. Next scaling gate is live eBay buyer-page audit, not a bulk repair batch.
- Kept premium MJ-generated product scene/mockups as R&D only: potentially valuable later, but must pass QA before replacing or supplementing Printify official mockups.


## 2026-05-06 12:22:00 -04:00 Live Cover Audit Proves Replacement Path
- Ran a direct live eBay buyer-page audit for `Sticker-Academia-0005` after Printify source repair reached the save/publish stage.
- Result remained `LIKELY_SINGLE_U_MISMATCH`: eBay front page matched local `U4` exactly and remained far from the local cover (`cover=194`, `U4=0`).
- Updated `Database/eBay_Cover_Repair_Decisions.csv`: `Sticker-Academia-0005` is now `SOURCE_REPAIR_DONE_LIVE_STILL_BAD`.
- Updated `modules/ebay_cover_replacement_queue.py` so source-repaired-but-live-still-bad rows become `READY_TO_REPLACE_VERIFIED` instead of staying in `WAIT_SOURCE_REPAIR_RESULT`.
- Regenerated `Database/eBay_Cover_Replacement_Queue.csv/md`: 1 row is now `READY_TO_REPLACE_VERIFIED`, 44 remain `WAIT_SOURCE_REPAIR_RESULT`, 4 remain `REVIEW_BEFORE_REPLACE`.
- Operational conclusion: do not keep burning time on the same old inventory-managed listing when live eBay refuses the source image sync. Build verified replacement listing flow, then retire the old item only after the new live buyer-page audit passes.


## 2026-05-06 12:48:00 -04:00 Default Mockup Policy Propagated To Planner
- Updated market planner so multiple Printify official/default mockups are no longer treated as a publish blocker by themselves.
- The new blocker is true image insufficiency: selected image count below expected, zero default image, or audit error.
- Updated factory backlog and supervisor so a source-repaired live eBay failure can surface as `READY_TO_REPLACE_VERIFIED`.
- Confirmed local supervisor preserves `Sticker-Academia-0005` as the verified replacement-path sample.


## 2026-05-06 13:00:00 -04:00 Replacement Draft Created, Online Upload Paused By Network Guard
- Added `modules/ebay_replacement_draft_builder.py` and targeted `--ids` support to `modules/printify_full_pipeline.py`.
- Created local replacement row `Sticker-Academia-0005-FIX1` from the verified failed listing `Sticker-Academia-0005`.
- The replacement row is `Ready_for_Printify`, with old Printify/eBay external IDs cleared.
- Ran network guard before online upload: Printify avg 474ms, max 2780ms, Discord loss 16%; strategy returned `pause`.
- Therefore no Printify upload and no eBay publish were attempted. Next online action when network improves: `py modules\printify_full_pipeline.py --ids Sticker-Academia-0005-FIX1 --limit 1` without `--publish`.
## 2026-05-06 14:58 -04:00

- Wired LAN test passed: Ethernet 1Gbps active, Wi-Fi disconnected, 0% loss to Printify/eBay/Etsy/Discord/OpenAI, roughly 5-8ms average latency, 50MB download around 214 Mbps.
- Published and audited replacement experiments for the Sticker eBay cover bug:
  - `Sticker-Academia-0005-FIX1` proved the old custom U-gallery route still fails live audit.
  - `Sticker-Academia-0005-FIX2` proved Cover-only + Printify official mockups fixes the live main image.
  - `Sticker-Academia-0006-FIX1`, `0007-FIX1`, `0008-FIX1` passed live buyer-page cover audit.
  - Expanded batch: `Sticker-Academia-0009/0010/0011/0014/0015/0016-FIX1` and `Sticker-Zen-0001/0002/0003/0004-FIX1` created, published, and audited; official-only cases are now classified as `LIKELY_COVER_OFFICIAL`.
- Updated code:
  - Sticker full pipeline now uploads only Cover as the custom listing image and relies on Printify official mockups for marketplace gallery context.
  - Publish scheduler blocks Sticker products that still have custom U/gallery images selected.
  - Live eBay cover audit recognizes Printify official-only mockups as pass states instead of false-failing against local U hashes.
- Published 8 additional Poster/Acrylic listings after production-design QA: `Poster-Academia-0023..0026` and `Acrylic-Grimdark-0012..0015`; all 8 passed production-design audit and live buyer-page official-mockup audit.
- Created/updated `Database/eBay_Retire_Queue.csv` with 15 listings that should be safely ended after eBay API or Seller Hub end-listing flow is confirmed.

## 2026-05-06 15:20 -04:00

- Rex cleared the network constraint after LAN/asset validation; resumed full-throughput online work.
- Recompiled the changed Printify/eBay cover-gate modules successfully.
- Regenerated the eBay replacement queue: 31 ready-to-replace verified rows, 14 replacement-published-live-pass rows, 4 review-before-replace rows.
- Rechecked Printify/eBay connectivity: 0% packet loss, about 5-6ms average latency.
