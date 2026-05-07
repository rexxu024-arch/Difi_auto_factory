# Gemini / Grey Bridge Operations

## Roles

- Gemini API is the normal high-frequency Grey bridge.
- Gemini Chat is the low-frequency persistent strategic memory surface.
- Codex must treat Grey output as advisory, not as direct write authority.

## Commands

```powershell
npm run grey:status
npm run grey:prepare
npm run grey:send
npm run grey:parse
npm run gemini:chat:dry
npm run gemini:chat:send
npm run gemini:chat:send:idle
```

## Safety Rules

- API calls never print or commit key values.
- Gemini Chat sync uses Edge CDP 9223 only.
- Gemini Chat thread URL uses the `/u/1/` account context:
  `https://gemini.google.com/u/1/app/d2ab3afa2778aa9e`
- The Grey Chat account hint is `xuyuan02038898080@gmail.com`; this is an account-selection hint only, not a credential.
- Chrome is not used for this workflow.
- Gemini Chat sync defaults to dry-run and writes the payload to:
  `Review_Packets/Gemini_Bridge/DAILY_SITREP_FOR_GEMINI_CHAT_latest.md`
- Actual web sync waits for user idle time unless `--force` is explicitly used.
- Web sync focuses through CDP but writes through OS clipboard and OS-level keyboard events.
- Any Gemini/Grey response is stored and parsed into local task queues first.
- Grey tasks are review recommendations, not direct permission to mutate live listings or spend money.

## Model Routing

- Gemini free tier: strategic critique, pressure tests, task ranking, compact daily review.
- DeepSeek: bulk SEO/title/description/tag drafts.
- Local scripts: QA gates, accounting, cover audits, publish safety, fee kill-switch.
- Stronger paid models: final high-risk reasoning, visual QA where local gates are insufficient, paid-spend decisions.

## Current State

- `Gemnini_free_api_key` works.
- `grey:send` has successfully returned and parsed Grey recommendations.
- `gemini:chat:dry` works.
- First `gemini:chat:send` attempt correctly stopped with `WAIT_USER_ACTIVE` because Rex was using the computer.
