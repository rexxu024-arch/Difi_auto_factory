Repro/Status Summary — V38.5 changes

Overview
- Reverted to the sliding-window controller (March 29 behavior) and Patient Worker harvesting rules.
- Controller: WINDOW_SIZE = 3. A slot opens only when a .png appears in `output/` for a task; the controller keeps up to 3 imagines in flight.
- Harvester: fingerprint-based harvesting — only click U1 when the message explicitly contains `(100%)`. Sleep 3s buffer, then click U1 once (no retries).

Files changed
- `main.py`
  - Implemented the Sliding Window controller (WINDOW_SIZE = 3). Tracks `in_flight` tasks and opens slots only when output files appear.

- `harvester.py`
  - Simplified to Patient Worker: scans recent messages for the task ID, requires `(100%)`, sleeps 3s, clicks U1 once, no retries or attempt loops.

Behavior notes
- This change intentionally removes complex retry/attempt loops to prevent aggressive clicking (HTTP 400) and simplify the pipeline.

How to run & push
- Ensure runtime dependencies are installed: `requests`, `python-dotenv`, `Pillow`, `rembg`, `urllib3`.
- To commit and push locally:

  git add .
  git commit -m "V38.5: Reverted to March 29 Sliding Window Logic"
  git push origin main

If you'd like, I can create a simple mock harness to validate the sliding-window behavior without hitting Discord.
