# Soul Ecosystem — Command Center

Umbrella project for the Soul AI ecosystem. Documentation, planning hub, and single source of truth.
All projects live under ~/soul/ as subdirectories. Each subdirectory contains a README.md with project details.

## Current Sprint

**Week 1 (Feb 21-27): Foundation**
1. soul-outreach backend extraction (config, db, pipeline, CLI, API, auth, Docker)
2. soul-mesh extraction (node, discovery, election, transport, sync, relay)
3. soul-agents extraction (registry, tool executor, YAML prompts, boundary enforcement)

See `docs/daily-planner.md` for granular day-by-day tasks.

## Daily Rhythm (12-14h)

```
Block 1: BUILD   (9am - 1pm,  4h)  Ship projects, extract code, write tests
Block 2: EXPLORE (2pm - 6pm,  4h)  Research, analytics, CARS, finance
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
| Production codebase | ~/soul-os/ |
| soul-outreach (extracted) | ~/soul/soul-outreach/ |
| soul-mesh (extracted) | ~/soul/soul-mesh/ |
| soul-moa scaffold | ~/soul/soul-moa/ |
| soul-moe scaffold | ~/soul/soul-moe/ |
| Feature specs | ~/soul/soul-outreach/docs/features/ |
| Campaign strategies | ~/soul/docs/campaigns/ |
| Architecture doc (1,396 lines) | ~/.claude/soul-files/soul-os-architecture.md |
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

## All 37 Projects

### From soul-os (18)

| # | Project | Type | Status | What It Is |
|---|---------|------|--------|------------|
| 1 | soul-os | PRIVATE | Production | AI-native OS — 6,700 Python + 3,000 React |
| 2 | soul-mesh | PUBLIC | Has Code | Hub election, WebSocket sync, NAT relay |
| 3 | soul-relay | PUBLIC | Spec Only | Standalone NAT traversal relay |
| 4 | soul-knowledge | PRIVATE | Production | ChromaDB + SQLite FTS semantic search |
| 5 | soul-outreach | DUAL | Has Code | Email campaign: import, enrich, draft, review, send |
| 6 | soul-cloud | PRIVATE | Production | Container-per-user PaaS with Traefik |
| 7 | soul-consult | PRIVATE | Production | Consulting CRM: leads, proposals, engagements |
| 8 | soul-agents | PUBLIC | Spec Only | YAML agents with boundary enforcement |
| 9 | soul-heal | PUBLIC | Production | Self-healing with hysteresis + remediation |
| 10 | soul-auth | PUBLIC | Production | JWT + token family replay detection |
| 11 | soul-loop | PUBLIC | Production | Autonomous task scheduler + tick system |
| 12 | soul-soc | PUBLIC | Production | Ubuntu CVE scanning + security KB |
| 13 | soul-content | PRIVATE | Production | Content pipeline: research, social drafts |
| 14 | soul-web | PUBLIC | Production | React 19 PWA, 8 pages, WebSocket streaming |
| 15 | soul-desktop | PUBLIC | Production | Tauri v2 cross-platform desktop app |
| 16 | soul-term | PUBLIC | Production | Click-based CLI |
| 17 | soul-services | PRIVATE | Production | Docker: Vaultwarden, Gitea, Uptime Kuma |
| 18 | soul-deploy | PRIVATE | Production | systemd + Fly.io + Pi deployment |

### From soul-moa (6)

| # | Project | Type | Status | What It Is |
|---|---------|------|--------|------------|
| 19 | soul-moa-core | PUBLIC | Scaffolded | Agent loop, tool registry, boundaries, streaming |
| 20 | soul-moa-orchestrator | PUBLIC | Scaffolded | MoA proposer/aggregator |
| 21 | soul-moa-failsafe | PUBLIC | Scaffolded | Circuit breakers, fallback chains |
| 22 | soul-moa-models | PUBLIC | Scaffolded | Universal model client |
| 23 | soul-moa-telemetry | PUBLIC | Scaffolded | Prometheus metrics, structured logging |
| 24 | soul-moa-integration | PRIVATE | Scaffolded | soul-os drop-in replacement layer |

### From soul-moe (7)

| # | Project | Type | Status | What It Is |
|---|---------|------|--------|------------|
| 25 | soul-bench | PUBLIC | Scaffolded | 10-task benchmark + CARS metric |
| 26 | soul-select | PUBLIC | Scaffolded | Model screening + CARS scoring |
| 27 | soul-quant | PUBLIC | Scaffolded | GGUF/AWQ/MLX quantization |
| 28 | soul-tune | PUBLIC | Scaffolded | MLX LoRA + Unsloth QLoRA fine-tuning |
| 29 | soul-eval | PUBLIC | Scaffolded | Claude baseline comparison + stats |
| 30 | soul-registry | PUBLIC | Scaffolded | Model cards + deploy gates |
| 31 | soul-serve | PUBLIC | Scaffolded | Multi-model serving configs |

### From soul-app backup (2)

| # | Project | Type | Status | What It Is |
|---|---------|------|--------|------------|
| 32 | soul-search | PUBLIC | Has Code | Multi-provider web search aggregator |
| 33 | soul-import | PUBLIC | Has Code | Conversation importers (ChatGPT, Claude, RSS, email) |

### From delve-ai (2)

| # | Project | Type | Status | What It Is |
|---|---------|------|--------|------------|
| 34 | soul-query | PUBLIC | Scaffolded | NL-to-SQL engine with schema guardrails |
| 35 | soul-viz | PUBLIC | Scaffolded | Prompt-to-visualization engine |

### New Projects

| # | Project | Type | Status | What It Is |
|---|---------|------|--------|------------|
| 36 | soul-blog | PUBLIC | Spec Only | Technical blog content pipeline |
| 37 | soul-brand | PUBLIC | Spec Only | Brand identity and visual assets |
| 38 | claude-task-manager | PUBLIC | Spec Only | Claude Code extension: background task queue with dependencies and scheduling |

**Summary**: 27 PUBLIC, 9 PRIVATE, 2 DUAL

## Priority Stack

| Priority | Project | Why |
|----------|---------|-----|
| P0 | soul-outreach | Income-critical |
| P0 | soul-agents | Portfolio: AI safety |
| P0 | soul-mesh | Portfolio: distributed systems |
| P1 | soul-moa-core | Strongest differentiator (MoA) |
| P2 | campaign-ai-labs | Primary career objective |
| P5 | soul-bench + soul-eval | Research portfolio |

## Documentation

| Doc | Covers |
|-----|--------|
| docs/daily-planner.md | Day-by-day tasks for 4 weeks + trackers |
| docs/ecosystem-map.md | All 37 projects with full details |
| docs/architecture.md | Technical connections between the 3 repos |
| docs/strategy.md | Licensing, revenue model, target audiences |
| docs/roadmap.md | Prioritized action plan with dependencies |
| docs/competencies.md | Portfolio signals per audience |
| soul-outreach/docs/MASTER_PLAN.md | Full strategic execution plan |

## Extraction Pattern (soul-os -> standalone)

1. Create repo structure (pyproject.toml, README, tests/)
2. Copy source files from `~/soul-os/brain/`
3. Replace `brain.*` imports with standalone equivalents
4. Replace `brain.config.settings` with project-specific pydantic-settings
5. Replace `brain.claude_client` with project-specific Anthropic SDK wrapper
6. Verify: `grep -r "from brain" src/` returns ZERO results
7. Write tests, CI, examples, README
8. Push to GitHub with CI green

## CARS Metric

```
CARS = Reasoning Accuracy / (VRAM_GB x Latency_s)
```

Deploy gate: >=80% accuracy vs Claude, no task below 70%, P95 latency <5s.

## Revenue (one-liner)

NOW: Consulting $150-300/hr | NEXT: soul-outreach SaaS $29/$99/mo | LATER: Expand
