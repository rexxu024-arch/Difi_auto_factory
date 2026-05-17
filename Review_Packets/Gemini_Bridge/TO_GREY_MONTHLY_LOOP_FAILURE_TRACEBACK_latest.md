# Monthly Loop Failure Traceback For Grey

Updated: 2026-05-16 ET

Purpose:
This packet is for Gemini/Grey to audit why Codex spent almost a week failing to fully implement Rex's simple requirement: after Rex says "continue monthly tasks", Codex should keep working through the monthly task list until the day's dynamic stop window or a real guard, instead of doing small chunks and waiting for the next heartbeat.

## Rex's Requirement Was Not Ambiguous

Rex repeatedly specified the same desired behavior in different forms:

- One manual "continue monthly tasks" should start a long work block.
- The work block should proceed through the durable monthly task files in priority order.
- After one task finishes, refresh state and immediately continue to the next task.
- Stop only for real blockers: fee/account/privacy/hardware/network guard, Rex-required QA/login/approval, tool/runtime limit, or verified all-done state.
- Heartbeats are backup wakeups, not the primary cadence.
- If Codex is about to end a chat turn, it should leave an explicit continuation trigger/hook so the loop resumes instead of silently idling.
- Rex wanted visible progress, but visibility is not the work itself. The work must continue even when no chat message is being shown.

Conclusion: the failure was not caused by unclear requirements. It was caused by Codex choosing the wrong execution model.

## What Codex Did Wrong

1. Split a long-shift instruction into many small "heartbeat-sized" jobs.
   - Symptom: 3-10 minute work bursts, then idle until the next trigger.
   - Root error: treating the heartbeat as the worker rhythm rather than an emergency wakeup.

2. Let daemon/dispatcher abstractions compete with Codex's role.
   - Symptom: local loops reported "alive" while Rex could not see meaningful high-level progress.
   - Root error: using script health as a proxy for business progress.

3. Overengineered a C-Class routing problem.
   - Symptom: multiple supervisors, dispatcher revisions, heartbeat variants, report scripts, and stale status counters.
   - Root error: not using a primitive while-loop contract early enough.

4. Confused reporting with execution.
   - Symptom: repeated counters or "alive/current_command" without useful progress.
   - Root error: reporting became a task instead of a progress window into real work.

5. Failed to install a reliable turn-close continuation hook at the start.
   - Symptom: after answering Rex's steer conversation, Codex did not always resume monthly tasks.
   - Root error: no mandatory "before final response, ensure long shift and write continue trigger" step.

6. Did not elevate repeated Rex corrections into a durable operating rule fast enough.
   - Symptom: Rex had to repeat the same loop requirement over several days.
   - Root error: chat-local understanding was not converted into enforceable local files/scripts quickly enough.

## Corrected Model

Primary model:

1. Codex chat model remains the active supervisor for the next 2-3 weeks.
2. Local scripts execute deterministic substeps only: QA, packaging, polling, CSV refresh, metadata prep, and safe report generation.
3. "Continue monthly tasks" means:
   - read durable task files;
   - choose the highest-priority safe task;
   - execute it;
   - refresh backlog/state;
   - continue to the next safe task;
   - repeat until a real guard or dynamic stop window.
4. Heartbeats only ensure the chat/loop did not die.
5. Before any final response that may leave the chat idle, Codex must run the turn-close hook.

## New Guardrail To Audit

Grey should judge Codex by these criteria:

- Did the next 12-24 hours show fewer short idle gaps?
- Did progress move from repeated "alive" counters to real deliverables?
- Did Codex stop repeating loop work and return compute to revenue work?
- Did 10-minute updates become optional visibility, while the underlying work continued?
- Did the 1-hour/2-hour summaries show project percentages and ETA, not only command names?
- Did Codex correctly defer low-priority admin to the winddown window and prioritize Adobe Stock, sticker bundles, and daily marketplace drip?

## Codex Self-Correction Commitment

This issue should not consume more production time. The permanent fix is simple:

- keep the monthly task list durable and ordered;
- use a primitive continuous work loop;
- use a turn-close hook;
- use visible progress only as a monitoring layer;
- escalate only true blockers;
- otherwise keep working.

