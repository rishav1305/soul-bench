# soul-loop

> Autonomous task scheduler with module tick system.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Framework |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/autonomous_loop.py` |
| License | MIT |

## What It Is

A background asyncio loop that runs on a configurable interval (default: every 15 minutes). It checks system health, processes pending tasks, routes tasks to the best mesh node, and ticks all registered modules (outreach, healing, content).

## How It Works

```python
async def autonomous_loop(app_state):
    while True:
        await asyncio.sleep(interval * 60)

        # 1. Check system health
        async for msg in ask_claude("Check system health"):
            await db.log_event("health_check", msg)

        # 2. Process pending tasks
        for task in await db.get_pending_tasks():
            node = await mesh.best_node_for(task)
            if node.is_self:
                await execute_task(task)
            else:
                await mesh.assign_task(task, node)

        # 3. Tick all modules
        for module in app_state.modules:
            await module.tick(app_state)
```

### Key Design Decisions

- **Non-blocking**: All Claude calls are async, never blocks the event loop
- **Mesh-aware**: Routes heavy tasks to most powerful available node
- **Module ticks**: Each module gets a `tick()` call per loop iteration
- **Configurable interval**: `SOUL_LOOP_INTERVAL_MINUTES` env var
- **Battery-aware**: Avoids heavy tasks on battery-powered nodes

## Strategic Value

Demonstrates autonomous AI orchestration. The scheduler pattern (health check -> task routing -> module ticks) shows how to build reliable background AI systems.
