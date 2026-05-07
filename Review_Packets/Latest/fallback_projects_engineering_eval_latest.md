# Fall-back Projects Engineering Evaluation

Generated: 2026-05-07 11:12:15 -0400 America/New_York

## Verdict

Build 1: Pinterest visual traffic queue, using official API only, no browser/session automation.
Build 2: Microstock metadata/export matrix, but keep it metadata-only until contributor account requirements are verified.
Defer: B2B cold-email crawler. It has the highest legal/deliverability risk and requires a human sales funnel before automation.

## Cold Engineering Matrix

| Rank | Option | Time to Deploy | Cash Cost | Success / Stability | Bottleneck | Ban Risk | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | B: Pinterest visual traffic engine | 8-16h for queue + official API prototype after account/app access | $0-$5/mo if using free/cheap image hosting; no listing fees | Medium: best fit for visual assets, but traffic is indirect and needs 2-4 weeks of pin history; Medium if pins index; weak short-term conversion, useful as free traffic layer | Pinterest requires official API access/boards plus publicly reachable image URLs; local files cannot be posted directly | Medium-low only if official API, slow pacing, unique pins; high if browser/session automation or duplicate spam | BUILD_FIRST |
| 2 | A: Microstock FTP/CSV export matrix | 6-10h for metadata/export pack; 12-24h for first platform FTP adapter after credentials | $0 direct; optional stock keyword tools or hosting not required | Low-medium: assets can be reused, but AI-stock review, similarity, and low royalties make payoff slow; Low early, medium only after hundreds/thousands accepted across platforms | Different agency requirements; Freepik FTP is locked until contributor level; review queues can take weeks | Medium if near-duplicates/AI disclosure wrong; low if platform-specific QA and slow submissions | BUILD_SECOND_AS_METADATA_ONLY |
| 3 | C: B2B indie studio cold email crawler | 15-30h for prototype; 40h+ for compliant deliverability/CRM pipeline | $20-$100/mo for domain/inbox/warmup/verifier if done seriously | Low short-term, high variance; direct-ticket upside exists but needs portfolio, offer proof, and human sales follow-up; Very unstable until a trust funnel exists | Email discovery accuracy, spam filtering, opt-out compliance, domain reputation, manual objection handling | High: spam complaints, sender-domain damage, platform scraping blocks, privacy/compliance exposure | DEFER |

## First Code Framework

- Pinterest queue generated: `C:\AIprojects\openclaw_difi\Database\Pinterest_Pin_Queue.csv` (30 rows).
- Microstock export queue generated: `C:\AIprojects\openclaw_difi\Database\Microstock_Export_Queue.csv` (40 rows).
- Evaluation matrix generated: `C:\AIprojects\openclaw_difi\Database\Fallback_Project_Evaluation.csv`.

### Pinterest Engine Skeleton

1. Read `Pinterest_Pin_Queue.csv`.
2. QA: source image exists, non-low-res, non-duplicate, unique board/destination cadence.
3. Host the image at a public HTTPS URL; Pinterest cannot fetch local laptop file paths.
4. Use official Pinterest API after app approval and `pins:write`; one worker, token bucket, jitter, per-board pacing.
5. Write pin_id and analytics back to the unified registry; never use session-cookie scraping.

### Microstock Export Skeleton

1. Read `Microstock_Export_Queue.csv`.
2. Run image QA and similarity/dedup filter.
3. Embed/emit metadata per platform: filename, title/description, keywords, category, AI disclosure.
4. Export per-platform CSV and staging folders; FTP only after account credentials and platform requirements are verified.

## Source-Aware Risk Notes

- Pinterest supports creating/managing Pins/Boards through its API, but its own guidance says bulk creation must obey spam/abuse rules; Trial access pins may be sandbox-only until Standard access.
- Pinterest policy warns against unapproved automation and repetitive/deceptive money-making content. So we use official API, slow pacing, unique pins, and no session-cookie botting.
- Freepik official contributor docs say FTP upload is only available after 500 published files. This blocks a new-account FTP matrix there.
- Shutterstock contributor docs support FTP/FTPS uploads and CSV metadata. That makes it a realistic first stock adapter once account status exists.
- Adobe Stock accepts generative AI content only with proper rights, AI labeling, and strict quality/legal standards; near-duplicate spam is dangerous.
- FTC CAN-SPAM guidance covers B2B commercial email too and requires truthful headers, non-deceptive subject, ad disclosure, physical postal address, opt-out, and honoring opt-outs. This makes cold email unsuitable for unsupervised automation now.

## Primary Source Links

- Pinterest content API/use case: https://developers.pinterest.com/usecase/content/
- Pinterest access tiers: https://developers.pinterest.com/docs/key-concepts/access-tiers/
- Pinterest developer guidelines: https://policy.pinterest.com/developer-guidelines
- Freepik contributor upload levels: https://support.freepik.com/s/article/Contributor-Level-Upload
- Freepik content submission requirements: https://support.freepik.com/s/article/What-can-I-sell-on-Freepik
- Shutterstock FTPS upload help entry: https://support.submit.shutterstock.com/s/article/How-do-I-upload-content-via-FTPS
- Adobe Stock generative AI content rules: https://helpx.adobe.com/stock/contributor/help/generative-ai-content.html
- FTC CAN-SPAM compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business

## Recommendation

Highest ROI next sprint: Pinterest queue first, because it attacks the current zero-view problem without new listing fees and reuses existing visual assets.
Second sprint: Microstock metadata/export, because it creates a zero-marginal-cost asset distribution backlog without touching marketplace accounts.
Do not build the cold-email crawler until there is a portfolio landing page, compliant sender identity, opt-out handling, and hand-reviewed lead scoring.
