# Soul Ecosystem — Command Center

Umbrella project for the Soul AI ecosystem. Documentation, planning hub, and single source of truth.
All projects live under ~/soul/ as subdirectories. Each subdirectory contains a README.md with project details.

## Current Focus

**Strategy:** Sequential Focus on 5 Projects (see `docs/plans/2026-02-23-focused-dev-strategy-design.md`)

| Phase | Project | Milestone |
|-------|---------|-----------|
| **NOW** | soul-planner | Queue tasks, Claude executes in background |
| Next | soul-mesh | SSH into mesh as one machine, run LLM inference |
| Then | soul-outreach | CLI pipeline: import -> enrich -> draft -> send |
| Then | soul-viz | POST data + prompt, get rendered chart |
| Ongoing | soul-os | Autonomous loop integrates with soul-planner |

See `docs/daily-planner.md` for granular day-by-day tasks.

## Daily Rhythm (12-14h)

```
Block 1: BUILD   (9am - 1pm,  4h)  Current phase project ONLY
Block 2: EXPLORE (2pm - 6pm,  4h)  Research that feeds current project
Block 3: SOCIAL  (7pm - 9pm,  2h)  Content from Block 1+2 -> LinkedIn, Twitter, blog, dev.to, Reddit
Block 4: SCOUT   (9pm - 11pm, 2h)  Job portals, freelance platforms, recruiter outreach, applications
```

## Quick Commands

When I say **"today"**: Read `docs/daily-planner.md`, find today's date, show all 4 blocks with sub-tasks. Flag uncompleted tasks from yesterday.

When I say **"status"**: Read the tracker tables at the bottom of `docs/daily-planner.md` — Extraction Tracker, Campaign Tracker, Blog Tracker, Revenue Tracker. Show current progress.

When I say **"sprint"**: Read `docs/daily-planner.md` for the current week. Show week theme, daily block themes, and weekly milestones.

## Working Across Projects

| Resource | Location |
|----------|----------|
| soul-planner | ~/soul/soul-planner/ (symlinked into ~/.claude/) |
| soul-mesh | ~/soul/soul-mesh/ |
| soul-outreach | ~/soul/soul-outreach/ |
| soul-viz | ~/soul/soul-viz/ |
| soul-os (production) | ~/soul-os/ |
| Architecture doc | ~/.claude/soul-files/soul-os-architecture.md |
| This command center | ~/soul/ |

**Rules:**
- ALWAYS read the target project's own CLAUDE.md before working in that repo
- cd to the project directory before running project-specific commands
- Each project has its own hookify rules — they apply when editing files in that project
- Never import `brain.*` outside soul-os — use standalone modules instead

## Conventions (enforced via hookify)

- **Python**: 3.11+, FastAPI, pydantic-settings, aiosqlite, structlog
- **Frontend**: React 19, Vite, dark theme, Recharts
- **Testing**: pytest, httpx for API tests
- **Security**:
  - All LLM calls through centralized client modules (never direct Anthropic SDK)
  - All email through `outreach/email_sender.py` (never direct SMTP)
  - All tool execution through boundary-checked registries
  - Never hardcode secrets — use env vars with project prefix (SOUL_, OUTREACH_, SOUL_MOA_, SOUL_MOE_)
  - Never concat SQL — use parameterized queries with `?` placeholders
  - Never use SHA-256/MD5 for password hashing — use bcrypt
  - No silent `except: pass` — always log and handle errors
  - No blocking calls in async functions — use aiofiles, asyncio.sleep, httpx

## The 5 Projects That Matter

| # | Project | Goal | Status |
|---|---------|------|--------|
| 1 | **soul-planner** | Inbuilt planner for Claude Code with task assignment | Spec only |
| 2 | **soul-mesh** | Combine devices into one virtual heavy machine for LLM inference | v0.2.0, 253 tests |
| 3 | **soul-outreach** | Market a product or skill in multiple ways | 8% extracted |
| 4 | **soul-viz** | Source-to-webpage visualization, all infra under the hood | Scaffold |
| 5 | **soul-os** | Autonomous machine that performs tasks and self-heals | Production |

Everything else is either a supporting module for one of these 5, or parked.

## Documentation

| Doc | Covers |
|-----|--------|
| docs/plans/2026-02-23-focused-dev-strategy-design.md | 5-project strategy with milestones |
| docs/plans/2026-02-23-daily-content-strategy-design.md | SOCIAL block daily content pipeline |
| docs/daily-planner.md | Day-by-day tasks + trackers |
| docs/content-log.md | Daily capture from BUILD + EXPLORE |
