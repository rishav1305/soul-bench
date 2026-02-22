# soul-heal

> Self-healing automation with DB-backed remediation, hysteresis, and nightly intelligence.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Framework |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/modules/healing/` |
| License | MIT |

## What It Is

An autonomous self-healing system that monitors system health (disk, temperature, memory, failed services), attempts remediation with safety guards, and runs nightly intelligence cycles where Claude summarizes the day's events into actionable learnings.

## Architecture

```
Health Checks (every 5 min via systemd timer)
    |
    v
Checker -> disk usage, CPU temp, memory, failed services
    |
    v
Remediator -> attempt fix (with guards)
    |           - explicit service allowlist (only "soul-os")
    |           - DB-backed rate limits
    |           - hysteresis (don't flap between fix/unfix)
    v
Nightly Intelligence (02:30 daily)
    |
    v
Claude summarizes events -> learnings table (context, insight, confidence)
```

### Components

| File | Purpose |
|------|---------|
| checker.py | System health checks (disk, temp, mem, services) |
| remediator.py | DB-backed remediation with rate limits, hysteresis, allowlist |
| nightly.py | Nightly Claude summarization -> learnings |

### Key Design Decisions

- **Service allowlist**: Only "soul-os" can be restarted. Prevents runaway remediation.
- **Hysteresis**: Won't oscillate between fix and unfix states.
- **DB-backed rate limits**: Prevents repeated remediation attempts in short windows.
- **Runtime-aware**: Knows if running in Docker vs systemd, adjusts remediation accordingly.
- **Crash-consistent backups**: sqlite3 .backup with lock, daily at 02:00.

## Strategic Value

Demonstrates systems thinking and SRE practices. Self-healing with safety guards (hysteresis, allowlists, rate limits) shows mature operational engineering. Relevant to SRE/Platform roles at any company.
