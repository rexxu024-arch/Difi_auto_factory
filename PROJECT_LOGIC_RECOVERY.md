# OpenClaw Difi Project Logic Recovery

Last updated: 2026-04-29

This document consolidates the recovered project memory, current filesystem state, and the user's final-deliverable expectations. It is intended as the first file to read when recovering from a broken thread.

## Project Identity

Project name: Difi Auto Factory / OpenClaw Difi.

Purpose: an end-to-end AI ecommerce product factory:

1. Generate strategy/DNA concepts.
2. Convert DNA into production prompts.
3. Dispatch prompts to Midjourney through Discord.
4. Harvest grids/upscaled assets.
5. Build local production assets.
6. Generate marketplace listings.
7. Upload/stage/publish through Printify.
8. Protect eBay/Etsy account health with throttled publishing and uniqueness checks.

## Persistent Context Protocol

Default collaboration rules for this user:

- A deadline task must first update `CURRENT_TASK.md`.
- Each completed batch must update `PROGRESS_LOG.md`.
- Before leaving or pausing, write a handoff checkpoint.
- Do not rely on chat history as the only memory. Repo files are the durable source.
- On recovery, read `CURRENT_TASK.md`, `PROGRESS_LOG.md`, `RECOVERY_STATE.json`, then latest logs/Excel state/git status.

## Main Pipelines

### Pipeline A - GREY ARCHITECT DNA Factory

Entry files:

- `main.py`
- `modules/mentor_hub.py`
- `modules/product_line.py`
- `modules/streaming_json.py`
- `Database/pending_tasks.txt`
- `Database/Pending_design.txt`
- `Database/Mentor_Hub.xlsx`
- `Database/Production_Line.xlsx`

Stage routing:

- Stage 1: `mentor_hub.run_logic()`
- Stage 2: `product_line.run_logic()`
- Stage 3: `mj_harvest.run_logic()`
- Stage 4: `iron_audit.run_logic()`

Mentor_Hub contract:

- Input queue: `Database/pending_tasks.txt`
- One seed equals one Claude/DeepSeek request.
- Do not combine multiple seeds into one request.
- Each seed must produce exactly 20 Gold DNA rows.
- Process seeds sequentially.
- Stream raw JSON array output.
- Parse each complete JSON object and save immediately.
- Remove a seed from pending only after the full 20-row group is saved.
- If one seed slows beyond normal time, stop/debug/hold rather than burning API indefinitely.
- Normal observed seed time: under about 1 minute. A 2-minute seed is a warning threshold.

Mentor_Hub schema:

- `Category`
- `Layout`
- `Title`
- `Gold_Prompt_DNA`
- `Material_Keywords`
- `Timestamp`
- `Design_Count`
- `Performance`

Mentor_Hub lifecycle:

- New DNA row starts with `Design_Count = 0`.
- `Performance` defaults blank.
- `Design_Count >= 100` means the DNA should not be recommended for new production.

Product_Line contract:

- Input queue: `Database/Pending_design.txt`
- Queue format is a JSON array, e.g. `[{ "Category": "Sticker-Zen", "Product_Type": "Sticker", "Count": 10 }]`.
- `Count` and `Number_of_Designs` are both accepted by current code.
- One API batch can produce at most 20 designs.
- After each successful saved design, decrement `Pending_design.txt`.
- Update the source Mentor_Hub row's `Design_Count` and `Timestamp` per produced design.
- Default status for new rows: `Ready_for_production`.
- ID sequence is per prefix, not global workbook count.

Product_Line schema:

- `ID`
- `Timestamp`
- `Category`
- `Product_Type`
- `Style`
- `Title`
- `MJ_Prompt`
- `SEO_Hook`
- `Status`

Product_Line old-format rules:

- Keep the verbose sortable table shape.
- `Product_Type` must not be missing on real rows.
- `Category` should be the main sortable category, such as `Zen`, `Academia`, or `Grimdark`.
- `Style` should be `Category Mentor-Grade`.
- IDs should look like `Sticker-Zen-0001`, `Poster-Academia-0001`, `Acrylic-Grimdark-0001`.
- Sequence is prefix-specific. `Sticker-Zen-0003` is followed by `Sticker-Zen-0004`, regardless of total row count.
- `MJ_Prompt` must be single-line plain text with no `\n` or `\r`.

V15.3 product molds:

- Sticker: `Isolated`, `--ar 1:1`, white contour border, vector clean edges, die-cut sticker style, solid white/isolated background.
- Poster: `Full_Frame`, vertical premium poster composition. Current code uses `--ar 2:3` and 12x18 poster language.
- Acrylic: `Full_Frame`, vertical acrylic photo block composition. Current code uses `--ar 5:7` for the 5x7 photo block target.
- T-shirt: `Isolated`, `--ar 2:3`, centered graphic tee style.
- Mug: `Full_Frame`, `--ar 2:1`, continuous seamless panoramic wrap.

Current verified workbook state:

- `Mentor_Hub.xlsx`: 620 data rows, 8 columns, intended schema present.
- `Production_Line.xlsx`: 460 data rows plus 20 blank rows; 9 columns, intended schema present.
- Production_Line product counts from current XML:
  - Sticker: 189
  - Poster: 121
  - Acrylic: 80
  - T-Shirt: 20
  - Wall Art: 30
  - Blank rows: 20 empty rows with no ID/category/status.

### Pipeline B - Midjourney Harvest And Asset Build

Entry files:

- `modules/mj_harvest.py`
- `modules/iron_audit.py`
- `modules/art_asset_builder.py`
- `Output/`
- `Database/mj_defect_log.csv`
- `Database/Harvest_Logs/`

Sticker status:

- Sticker/Kiss-Cut is the strongest implemented path.
- Final deliverable assets are `Cover_Mockup.png`, `Production_Design.png`, `metadata.txt`, and `U1-U4`.
- Low-res 256x256 U images are not deliverable-quality.

Current local Sticker folder state:

- `Ready_for_Steaming`: 122
- `Not_Working_LowRes`: 27
- `Not_Working`: 6
- `Review`: 1
- Other: 2

Poster/Acrylic asset rule:

- Do not reuse Sticker grid logic as primary design.
- Poster/Acrylic should choose the best single U image as production design.
- Other U images can be gallery support if suitable.
- Reject/hold low-resolution sources rather than forcing upload.

Current official Printify specs recovered:

- Premium Matte Vertical Poster:
  - Blueprint ID: 282
  - Provider ID: 99
  - Variant ID: 43138
  - Target: 12x18
  - Print area: 3600x5400
- Photo Block / Acrylic:
  - Blueprint ID: 1471
  - Provider ID: 104
  - Variant ID: 106190
  - Target: 5x7 vertical
  - Print area: 1538x2138

### Pipeline C - Listing Generation

Entry files:

- `modules/edit_for_platforms.py`
- `Database/eBay_listing.xlsx`
- `Database/Etsy_listing.xlsx`

Current listing strategy:

- Title/description generation must avoid mass-generated sameness.
- Current uncommitted code adds deterministic metadata-based variants:
  - profile variation
  - title tail variation
  - description intro/audience/use-case variation
  - DeepSeek instruction to vary sentence structure and keyword order while preserving facts

Current eBay listing state:

- `eBay_listing.xlsx`: 149 rows.
- Status counts:
  - `Printify_Published_Mockups5`: 34
  - `Printify_UI_Mockups5`: 8
  - `Ready_for_Printify`: 78
  - `Quality_Hold_LowRes_U`: 27
  - `Printify_UI_Failed`: 2

Current Etsy listing state:

- `Etsy_listing.xlsx`: 149 rows.
- Status counts:
  - `Placeholder`: 149

### Pipeline D - Printify Upload / Publish

Entry files:

- `modules/printify_uploader.py`
- `modules/printify_mockup_ui_uploader.py`
- `modules/printify_full_pipeline.py`
- `modules/printify_primary_audit.py`
- `Database/eBay_listing.xlsx`

Printify specs in code:

- Sticker:
  - Blueprint ID: 400
  - Provider ID: 99
  - Variant ID: 45754
  - Default price: 1199 cents
- Poster:
  - Blueprint ID: 282
  - Provider ID: 99
  - Variant ID: 43138
  - Default price: 3499 cents
- Acrylic:
  - Blueprint ID: 1471
  - Provider ID: 104
  - Variant ID: 106190
  - Default price: 8999 cents

Sticker Printify image target:

- Stable target is 5 custom images:
  - Cover first/default.
  - U1-U4 included.
  - Selected mockup count is 5.
- If possible, preserve system default mockups too, but 5 stable custom images is the priority.
- The prior primary-image bug was that Printify UI reordered uploads and U images could become default.
- Current strategy: upload Cover first, then add U1-U4, then audit via API.

Printify hard stop:

- If the Printify UI browser is logged out, stop before creating more products.
- Do not create default 3-image bad drafts while logged out.
- User must re-login to Printify browser before UI upload can continue.

Current Printify progress:

- Logs show 23 existing products were API-published successfully earlier.
- Bad drafts were cleaned twice on 2026-04-29.
- Current eBay sheet says 34 `Printify_Published_Mockups5`, 8 `Printify_UI_Mockups5`, 78 `Ready_for_Printify`, 2 `Printify_UI_Failed`.
- This differs slightly from a prior thread statement of 35 published and 87 ready, so current Excel is the live source of truth.

## Account Safety Rules

The user has an older eBay account but wants to avoid spam-like behavior.

Known account context:

- eBay account is about 4 years old.
- About 50 sales.
- About 34 positive feedback.

Publishing rules:

- Split Printify preparation from eBay publishing.
- Printify drafts and audits can be batched.
- eBay publish/sync should be conservative, throttled, and uniqueness-checked.
- Avoid sudden high-volume same-style Sticker listing bursts.
- Prefer a diversified mix across Sticker, Poster, Acrylic when publishing later.
- User confirmation is required for broad external publishing.

## Final Deliverable Alignment

The user's current final deliverable is not just code. It is a signed-off operational factory state:

1. Durable memory:
   - Current task, progress, recovery state, and project logic are saved in repo files.
2. Factory logic:
   - Mentor_Hub and Product_Line schemas match the user's old sortable format.
   - Pending queues are atomic and resumable.
   - API usage is bounded and streaming.
3. Sticker production:
   - Existing wrong-primary products are corrected or marked.
   - 5-image Printify state is reliable.
   - Bad drafts are cleaned.
   - Low-res assets are isolated.
4. New product formats:
   - Poster 282 and Acrylic 1471 use official Printify specs.
   - Local asset building does not use Sticker grid as primary.
   - The goal remains 20 stable uploaded listings per new format, then optionally more DNA-selected styles if time and quality allow.
5. Account protection:
   - eBay publishing is throttled and gated.
   - Similarity is reduced in title/description and product mix.

## Current Execution Gates

Safe to do without user review:

- Read-only audits.
- Local schema repair.
- Local listing text generation for staged/unpublished rows.
- Bad draft cleanup if confirmed by API and sheet status.
- Printify API publish only for already verified 5-image products, if it does not violate eBay throttling policy.
- Product_Line/Mentor_Hub queue processing with bounded API calls.
- Poster/Acrylic local asset prep and validation.

Requires user confirmation or login:

- Printify UI upload if browser session is logged out.
- Broad eBay publishing/sync.
- Irreversible high-volume external actions.
- Ambiguous visual/art-direction decisions that require human taste judgment.

## Known Risks / Inconsistencies

- `config.py` still defines `Config.audit()` twice; the second overrides the first.
- Python launcher can be blocked by local Python manager permissions in this environment; PowerShell XML inspection is currently reliable for read-only Excel checks.
- The repo has many untracked logs/artifacts from 2026-04-29.
- Git checkpoint attempts have failed due to `.git/index.lock` / `.git/FETCH_HEAD` permission denied.
- `Product_Line.xlsx` has 20 blank XML rows; these appear empty and not business data.
- The current Excel counts differ from some prior transcript counts. Current Excel should win.

