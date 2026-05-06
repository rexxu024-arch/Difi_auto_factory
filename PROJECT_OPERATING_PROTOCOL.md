# Project Operating Protocol

This is the default collaboration protocol for future project work with this user.

## Persistent Context Rules

- When the user gives a deadline-driven task, first write or update `CURRENT_TASK.md`.
- After each completed batch, update `PROGRESS_LOG.md`.
- Before leaving, pausing, or handing off a thread, write a clear handoff checkpoint.
- Do not rely on chat history as the only memory source. Chat can break; repo files remain.

## OpenClaw Full Access Rule

For OpenClaw / Difi Auto Factory work, the user has granted standing project-level permission for:

- Reading, writing, and repairing files under the project folder.
- Running project scripts, local virtualenv tools, and project automation utilities.
- Installing missing project Python dependencies into the project `.venv`.
- Querying project-related APIs such as Printify for status, audit, draft repair, and listing preparation.
- Inspecting project-related browser pages such as Printify and eBay Seller Hub when already logged in.

Do not repeatedly ask for confirmation for these routine project actions. If the Codex app's sandbox still forces a tool-level approval, treat that as a system execution gate, not as a new user decision.

Still pause for:

- Payment, orders, purchases, subscriptions, or account billing/payment credentials.
- Broad public eBay publishing/sync that may materially affect account health.
- Destructive local/cloud deletion unless the target is narrowly verified as a bad project artifact or draft cleanup already within the task scope.
- Sensitive personal data unrelated to the OpenClaw project.

## Recovery Rules

When recovering context after a broken or restarted thread, read local project records first:

1. `CURRENT_TASK.md`
2. `PROGRESS_LOG.md`
3. `RECOVERY_STATE.json`
4. Any handoff/checkpoint files
5. Latest logs, audits, spreadsheets, and git status

Only continue from verified project records. Do not invent missing requirements.

## Automation-First End State

- Codex labor is for building and debugging the factory, not for becoming the permanent factory.
- Every recurring decision should eventually become a Python script, queue, audit gate, report, or scheduled automation.
- Manual browser work is acceptable only as a discovery probe. Once a rule is learned, save it into repo code or durable logs.
- Prefer extending the existing Printify-centered pipeline over adding a parallel marketplace system.
- Use eBay/Etsy APIs as narrow support layers for what Printify cannot do reliably: read-only performance data, ad/campaign state, lightweight metadata sync, listing-health checks, and analytics.
- Keep product creation, production design upload, mockup generation, and marketplace push anchored in Printify unless a specific verified blocker requires a replacement path.
- Avoid duplicate sources of truth. If an API sync is added, it must reconcile back into `Database/eBay_listing.xlsx`, `Unified_Listing_Registry`, and supervisor/backlog outputs.
- The current factory supervisor entrypoint is:
  `py modules\factory_supervisor.py --execute-local --skip-network`
- Before any large online batch, run:
  `py modules\factory_supervisor.py`
  and obey the generated action queue in `Database\Factory_Autopilot_Action_Queue.csv`.
- Public publish must remain blocked when the supervisor marks `cover_gate` as `BLOCKING_PUBLISH`.
