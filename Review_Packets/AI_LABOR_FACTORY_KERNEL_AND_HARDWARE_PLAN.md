# AI Labor Factory Kernel + Laptop Resource Plan

Generated: 2026-05-07 EDT  
Workspace: `C:\AIprojects\openclaw_difi`

## 1. New Mainline Branch

After current Poster top-up and external ID reconciliation, OpenClaw gains a second durable branch:

```text
Universal AI Labor Factory Kernel
```

Goal:

```text
Separate business logic from risk, quality, cost, and resource controls so the same factory brain can migrate from Printify/Etsy/eBay into other revenue projects.
```

Implemented portable core:

```text
modules/factory_core/contracts.py
modules/factory_core/portable_gates.py
modules/factory_core/__init__.py
```

The current OpenClaw marketplace code remains the first business implementation. Future businesses should define new task producers and adapters, but reuse:

```text
FactoryTask
GateResult
ExecutionDecision
GateStack
cost_cap_gate
no_customer_message_gate
system_resource_allocator
```

## 2. Logic Decoupling Standard

Every future project should expose tasks in this neutral shape:

```json
{
  "task_id": "unique id",
  "business": "openclaw | stock_assets | research_agent | content_factory",
  "lane": "production | qa | publish | monitor | research",
  "action": "verb",
  "priority": 0,
  "risk_level": "low|medium|high",
  "cost_cap_usd": 0,
  "resource_class": "local_light|local_heavy|image_batch|api_read|online_publish_safe",
  "requires_network": false,
  "requires_login": false,
  "inputs": {},
  "expected_outputs": {}
}
```

This lets Codex move Risk Guard and Quality Gate to a new project without dragging Printify/eBay code with it.

## 3. 24-Hour Laptop Power Plan

The machine is an Intel N95 laptop, so the plan is “steady and clever,” not brute-force workstation behavior.

| New York Time | Mode | Best Work | Default Cap |
|---|---|---|---|
| 00:00-06:30 | Night Heavy | image QA, asset building, metadata generation, reports, local batch scoring | parallel 2, batch 8 |
| 06:30-10:00 | Morning Reports | Seller/Etsy/eBay readouts, Gemini/Rex summaries, market signal refresh | parallel 2, batch 5 |
| 10:00-18:00 | Rex Interactive | low CPU scripts, small API reads, single browser tasks | parallel 1, batch 2 |
| 18:00-23:00 | Evening Online | guarded Printify/API work, small publish-safe batches, QA spot checks | parallel 2, batch 4 |
| 23:00-24:00 | Preflight/Checkpoint | git push, report refresh, next-night queue planning | parallel 1, batch 3 |

## 4. Hardware Protection Thresholds

Temperature preferred thresholds:

```text
<=75C: normal
80C+: reduce to conservative
85C+: cooldown 20 minutes
90C+: critical pause
```

If Windows blocks thermal sensors, use CPU/memory proxy:

```text
CPU >=75%: conservative
CPU >=88% for 3 consecutive checks: cooldown
Memory >=82%: conservative
Memory >=92% for 3 consecutive checks: cooldown
Battery discharging: avoid heavy/background drains
```

This is especially important because prior hardware snapshots showed:

```text
CPU sample reached 100%
Memory was around 84% used
WMI temperature probe was denied/unavailable
```

## 5. Resource Allocator

Implemented:

```text
modules/system_resource_allocator.py
Database/System_Resource_Policy.json
Database/System_Resource_State.json
Database/System_Resource_Allocation.csv
```

Commands:

```powershell
npm run system:resources
npm run system:resources:watch
py modules\system_resource_allocator.py --task-class image_batch --priority 80 --json
py modules\system_resource_allocator.py --task-class online_publish_safe --priority 95 --json
```

Decision outputs:

```text
RUN
RUN_CONSERVATIVE
DEFER_TO_NIGHT
PAUSE_COOLDOWN
```

The allocator does not blindly change Windows power settings. It writes a machine-readable allocation decision that production modules can obey. This is safer and portable.

## 6. How This Changes Factory Behavior

Before launching a large batch:

```text
1. network_guard checks internet/platform stability.
2. system_resource_allocator checks laptop load/heat/power.
3. risk_guard checks account/platform/fee boundaries.
4. quality gates check image/product correctness.
5. only then does the production module run.
```

The target is not maximum speed. The target is:

```text
maximum useful throughput without account risk, fee leakage, image mistakes, or laptop abuse.
```

## 7. Next Integration Step

The allocator currently reports decisions. The next engineering step is to make `factory_supervisor.py` call it and automatically downgrade heavy jobs when the allocator says:

```text
RUN_CONSERVATIVE
DEFER_TO_NIGHT
PAUSE_COOLDOWN
```

This should be done before any future always-on overnight daemon.
