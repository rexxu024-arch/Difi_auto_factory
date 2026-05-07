# OpenClaw Grunt Engine - Cruise Factory Design

Generated: 2026-05-07 EDT  
Workspace: `C:\AIprojects\openclaw_difi`

## 1. Purpose

The Grunt Engine is the 24/7 background-task layer for work that does not need Rex's business decision:

- data cleaning
- local report refresh
- image preflight checks
- SEO/copy signal refresh
- cross-platform mapping
- hardware heartbeat
- quality-floor quarantine

It is intentionally portable. The queue and quality/resource gates should move to future AI-labor businesses without depending on Printify/eBay/Etsy.

## 2. Deliverables

### Task_Queue_Modular

Implemented:

```text
modules/task_queue_modular.py
Database/Grunt_Task_Queue.jsonl
```

Commands:

```powershell
npm run grunt:seed
npm run grunt:queue
```

Queue status values:

```text
PENDING
DEFERRED
RUNNING
DONE
FAILED
QUARANTINED
```

Each task carries:

```text
task_id, action, command, priority, resource_class, cost_cap_usd,
requires_network, requires_login, expected_outputs, qa_profile,
attempts, max_attempts
```

### Hardware_Heartbeat_Monitor

Implemented:

```text
modules/hardware_heartbeat_monitor.py
Database/Hardware_Heartbeat.csv
Database/Hardware_Heartbeat_State.json
```

Command:

```powershell
npm run hardware:heartbeat
```

It reads:

- CPU load
- memory use
- temperature if Windows exposes WMI thermal sensors
- GPU engine utilization if available
- battery/power state
- fan RPM if `Win32_Fan` exposes it

If fan or temperature sensors are unavailable, the monitor explicitly records that fact rather than pretending it knows.

### Quality_Floor_Guard

Implemented:

```text
modules/quality_floor_guard.py
Database/Quality_Floor_Guard.csv
Database/Quality_Floor_Guard_State.json
Database/Quality_Floor_Quarantine/
```

Command:

```powershell
npm run quality:floor
```

It evaluates 50 baseline QA rules covering:

- project-root containment
- non-empty files
- temporary/cache/browser-profile exclusions
- secret-marker detection
- CSV/JSON parse sanity
- text encoding/control-character sanity
- image openability
- image resolution
- image contrast
- clipping
- edge energy / softness
- aspect ratio
- root screenshot/debug artifacts
- personal temp source paths
- buyer/order action artifacts

Default action is physical quarantine, not deletion. That is the safer production interpretation of "physical smash": failed outputs are removed from Rex's review queue and isolated for forensic review.

### The Grunt Engine

Implemented:

```text
modules/grunt_engine.py
Database/Grunt_Engine_Run_Log.csv
Database/Grunt_Engine_State.json
Database/Grunt_Maintenance_Plan.json
```

Commands:

```powershell
npm run grunt:dry
npm run grunt:once
npm run grunt:cruise
```

The engine:

1. samples the resource allocator;
2. records a hardware heartbeat;
3. chooses a queued task compatible with the current duty-cycle window;
4. runs only allowlisted local-safe commands;
5. checks expected outputs through Quality_Floor_Guard;
6. updates the modular queue and run log.

## 3. 24h Duty Cycle

Policy file:

```text
Database/System_Resource_Policy.json
```

| Window | Time New York | Purpose | Resource Behavior |
|---|---:|---|---|
| Cruise | 00:00-04:00 | low-urgent background work | target CPU 40-50%, batch 4 max |
| Rest Maintenance | 04:00-06:00 | heartbeat, quality scan, maintenance plan | no unattended reboot/defrag/battery cycling |
| Morning Reports | 06:00-10:00 | reports, market reads, Gemini/Rex briefs | moderate |
| Peak Rex Online | 10:00-23:00 | interactive UI scripts, API reads/writes with feedback | high feedback, browser-safe |
| Preflight Checkpoint | 23:00-24:00 | git/report/queue planning | conservative |

## 4. Safety Notes

The user asked for defrag, cold restart, and battery cycling in Rest. These are potentially disruptive or hardware-specific, so the first implementation writes a protected maintenance plan rather than executing them.

Guarded actions:

```text
Windows restart / cold boot
battery charge-discharge cycle
defrag/optimize-volume on SSD or system disk
permanent deletion rather than quarantine
```

This keeps the system self-operating without turning a maintenance window into a surprise outage.

## 5. Current Best Use

Run once:

```powershell
npm run grunt:seed
npm run grunt:dry
npm run grunt:once
```

Run continuously:

```powershell
npm run grunt:cruise
```

For now, use `grunt:cruise` when Rex explicitly wants the laptop to keep working in the background. The next improvement is to install it as a Windows Scheduled Task with a Rex-visible stop switch.

## 6. Hardware Cooldown Guard

Implemented after the high-efficiency mode request:

```text
modules/hardware_cooldown_guard.py
Database/Hardware_Cooldown_State.json
Database/Hardware_Cooldown_Log.csv
```

Command:

```powershell
npm run hardware:cooldown
```

Behavior:

- Samples a heartbeat.
- Looks at recent heartbeat streaks.
- Activates a cooldown window when CPU, memory, or temperature proxy stays hot.
- Does not shut down Windows, kill user programs, or force battery cycling.
- During cooldown, it blocks heavy local classes such as image rendering, browser automation, and asset builds.
- It still allows low-CPU API reads/writes, heartbeat, reports, and queue planning in conservative mode.

This distinction matters: an API publish call is not the same as a Midjourney/image-render batch or UI browser loop.

## 7. Risk Guard Portability

The portable design boundary for the next project is:

```text
FactoryTask -> Risk_Guard -> Cost_Guard -> Resource_Guard -> Quality_Floor_Guard -> Executor
```

The pieces that should move unchanged into a future AI labor business:

- `Task_Queue_Modular`: task identity, priority, retry, cost cap, expected outputs.
- `Quality_Floor_Guard`: 50-rule artifact floor and quarantine-first behavior.
- `system_resource_allocator`: 24h duty cycle and laptop-safe scheduling.
- `hardware_cooldown_guard`: sustained-load protection.
- Risk-state JSON pattern from marketplace work:
  - `Account_Risk_State.json`
  - kill-switch JSON files
  - publish jitter logs
  - login anomaly states

Business-specific adapters should stay replaceable:

- Printify/eBay/Etsy API clients.
- Marketplace title/description builders.
- Product-specific price calculators.
- Platform-specific UI fallback scripts.

The target for new projects is not to copy marketplace code. It is to copy the gates, logs, queue shape, retry model, and quarantine behavior.
