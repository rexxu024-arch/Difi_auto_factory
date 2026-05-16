# OpenClaw Setup Dependencies

This is the quick rebuild checklist for a new Windows machine. It lists runtime packages, browser/UI dependencies, API credentials, and local data folders needed to make the current OpenClaw / Difi Auto Factory project operational again.

## 1. Core Runtime

Required:

- Windows 10/11 with PowerShell.
- Python 3.11 or 3.12 recommended.
- Node.js LTS and npm.
- Git.
- Microsoft Edge.
- Google Chrome optional, but Edge should be the default automation browser for marketplace work.

Recommended setup command:

```powershell
npm run setup:win
```

This creates `.venv`, upgrades pip, and installs `requirements.txt`.

If Playwright standalone browser support is needed:

```powershell
.venv\Scripts\python -m playwright install chromium
```

Most current UI automation uses Edge/Chrome CDP, so the installed local browser is still the important piece.

## 2. Python Packages

Installed from `requirements.txt`:

- `python-dotenv` for `.env` loading.
- `requests` for Printify, Etsy, eBay, Discord/Midjourney, Gemini, Claude/DeepSeek HTTP calls.
- `openpyxl` for `Mentor_Hub.xlsx`, `Production_Line.xlsx`, and other workbook handling.
- `pillow` for QA sheets, mockups, contact sheets, digital pack previews, image transforms.
- `websockets` for Chrome/Edge CDP browser control.
- `pandas` for CSV/listing analysis utilities.
- `pywin32` for Windows COM/clipboard/window helpers.
- `rembg` for sticker/background removal workflows.
- `openai` for DeepSeek-compatible SDK usage in older CSV/listing modules.
- `tzdata` for stable timezone behavior on Windows.
- `playwright` for Etsy UI modules that use Playwright/CDP.

Heavy transitive dependencies to expect:

- `rembg` may install ONNX-related packages.
- `pillow` and image QA modules can use noticeable CPU on large batches.

## 3. Node / npm Layer

`package.json` is mainly a local command launcher, not a frontend app. Important npm scripts:

- `npm run setup:win`
- `npm run doctor`
- `npm run local`
- `npm run printify:login`
- `npm run etsy:api-status`
- `npm run gemini:smoke`
- `npm run grey:sitrep`
- `npm run gemini:chat:send`
- `npm run system:resources`
- `npm run hardware:heartbeat`
- `npm run endurance:winddown`
- `npm run backlog`

The real work is still Python modules under `modules/`.

## 4. Browser / UI Automation Dependencies

Primary pattern:

- Use Edge for Printify/Etsy/eBay/Discord/Gemini web work.
- Start Edge with a CDP/debug port when automation needs to inspect or operate logged-in pages.
- Default local CDP port is usually `9223`.

Relevant environment variables:

- `OPENCLAW_CDP_PORT`
- `OPENCLAW_PRINTIFY_CDP_PORT`
- `OPENCLAW_EBAY_CDP_PORT`

Browser state to preserve on migration:

- Edge profile logged into Printify.
- Edge profile logged into Etsy.
- Edge profile logged into eBay Seller Hub.
- Edge profile logged into Discord/Midjourney server.
- Edge profile logged into Gemini chat thread if web sync is used.

Do not rely on Chrome for project automation unless Edge is unavailable.

## 5. Required API Accounts / Credentials

Values belong in `.env`. Never commit `.env`.

Printify:

- `Printify_API_KEY`
- `Printify_EBAY_SHOP_ID`
- `Printify_ETSY_SHOP_ID`
- `PRINTIFY_LOGIN_EMAIL`

Discord / Midjourney:

- `DISCORD_TOKEN`
- `GUILD_ID`
- `CHANNEL_ID`
- Legacy/current Midjourney interaction values may also be needed by `modules/mj_harvest.py`: app id, command id/version, session id, MJ bot id if present in `.env`.

Dify / Product Line:

- `Product_line_API_KEY`
- `Product_line_API_URL`

LLM providers:

- `DEEPSEEK_API_KEY`
- `DEEPSEEK_BASE_URL`
- `CLAUDE_API_KEY`
- `CLAUDE_BASE_URL`
- `GEMINI_API_KEY`
- `Gemnini_free_api_key` or `GEMINI_FREE_API_KEY`
- `Gemini_paid_apid_key` or `GEMINI_PAID_API_KEY`
- `GEMINI_MODEL`
- `GEMINI_FREE_MODEL`
- `GEMINI_PAID_MODEL`

Etsy:

- `ETSY_KEYSTRING` / `Etsy_Key_string`
- `ETSY_SHARED_SECRET` / `Etsy_shared_secret`
- `ETSY_REDIRECT_URI`
- `ETSY_TOKEN_FILE`

eBay:

- `EBAY_CLIENT_ID`
- `EBAY_CLIENT_SECRET`
- `EBAY_REDIRECT_URI` / RuName
- `EBAY_API_BASE_URL`
- OAuth token file under `Database/.ebay_oauth_tokens.json`

Adobe Stock:

- Contributor account is browser-based for now.
- Future FTP credentials should be stored separately in `.env` or an ignored local secret file once configured.

## 6. Local Data Folders To Migrate

Git intentionally ignores most operational state and generated assets. A new computer needs both the Git repo and a private data backup.

Private folders/files to back up:

- `Database/`
- `Output/`
- `Release/`
- `First_Audit_Release/`
- `Reports/`
- `Review_Packets/`
- `Assets/`
- `Private_Assets/`
- `Archive_Assets/`
- `adobe_stock_factory/`
- `.env`
- `.browser_profiles/` if used

Important token/state files:

- `Database/.etsy_oauth_tokens.json`
- `Database/.etsy_oauth_state.json`
- `Database/.ebay_oauth_tokens.json`
- `Database/.ebay_oauth_state.json`

These are intentionally not in Git.

## 7. External Tools / Optional Binaries

Optional but useful:

- `cloudflared.exe` for temporary OAuth callback tunnels.
- Browser DevTools/CDP via Edge.
- Windows Task Scheduler if long-shift or shutdown automation is later moved out of Codex.

Avoid committing:

- `tools/cloudflared.exe`
- screenshots
- logs
- contact sheets with commercial designs
- generated product assets

## 8. First Smoke Tests On A New Machine

Run these after setup:

```powershell
npm run doctor
npm run etsy:api-status
npm run gemini:smoke
python .\modules\ebay_token_manager.py --status
python .\modules\ebay_api_smoke_test.py
python .\modules\printify_sales_channel_audit.py
```

For local-only checks:

```powershell
npm run local
python .\modules\printify_design_audit.py --limit 2 --sleep-seconds 1
python .\modules\adobe_stock_scaffold.py
```

## 9. Current Migration Strategy

Recommended future SSD layout:

- Keep the Git repo on the internal drive if performance is acceptable.
- Move heavy ignored folders (`Output`, `Release`, `First_Audit_Release`, `adobe_stock_factory/assets`) to the external SSD.
- Use directory junctions (`mklink /J`) only after confirming the SSD drive letter is stable.

Do not move `.env` or token files to a removable drive unless the drive is always connected and encrypted.

## 10. Codex App / Plugin Side

Useful Codex-side plugins/skills currently available in this environment:

- Browser / browser-use for local and in-app browser checks.
- GitHub for repository operations.
- Spreadsheets for `.xlsx` / `.csv` analysis.
- Documents and Presentations for future sales materials or lookbooks.
- imagegen skill for bitmap generation/editing when needed.

These are Codex environment capabilities, not Python dependencies. If moving machines or accounts, verify the Codex desktop app has these plugins enabled again.

