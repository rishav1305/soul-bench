# Focused Dev Strategy — 5 Projects That Matter

**Date:** 2026-02-23
**Status:** Approved
**Replaces:** `2026-02-22-dev-strategy-design.md` (Build-Ship-Learn Flywheel, 37 projects)

---

## Problem

The previous strategy spread effort across 37 projects with a process goal ("extract 2 repos/week"). Creating standalone repos without direction is not an achievement. No project was reaching a meaningful milestone.

## Strategy: Sequential Focus on 5 Projects

Five projects with clear goals. One project at a time. Full focus until milestone. No context-switching.

---

## The 5 Projects

| # | Project | Goal | Done When |
|---|---------|------|-----------|
| 1 | **soul-planner** | Inbuilt planner for Claude Code. Assign tasks that Claude can take up. | `/task add "do X"` queues a task, Claude executes it in background, output captured. |
| 2 | **soul-mesh** | Combine devices into one virtual heavy machine for LLM inference. User-friendly install. | SSH into the mesh as one big machine. Set up environment. Run LLM inference. |
| 3 | **soul-outreach** | Market a product or skill in multiple ways. | `outreach import -> enrich -> draft -> send --dry-run -> stats` works end-to-end. |
| 4 | **soul-viz** | Visualizations from data source to webpage. All infra under the hood. | `POST /viz/chart` with data + prompt returns rendered chart on frontend. |
| 5 | **soul-os** | Autonomous machine that performs tasks and self-heals. | Autonomous loop uses soul-planner to queue and execute tasks. |

Everything else is either a supporting module for one of these 5, or it doesn't matter right now.

---

## Build Order

```
Phase 1: soul-planner    (Weeks 1-2)     Accelerates everything else
Phase 2: soul-mesh        (Weeks 3-5)     Strongest portfolio piece
Phase 3: soul-outreach    (Weeks 6-8)     Income-critical
Phase 4: soul-viz         (Weeks 9-10)    Research + demo value
Ongoing: soul-os          (side-effects)  Gets better as other projects integrate
```

---

## Phase 1: soul-planner (Weeks 1-2)

**Architecture:** Standalone git repo at `~/soul/soul-planner/`, symlinked into `~/.claude/`.

```
~/soul/soul-planner/              # Git repo (publishable)
├── skills/planner/SKILL.md       # Slash command handler
├── agents/task-runner.md         # Background execution agent
├── planner/
│   ├── db.py                     # SQLite task queue
│   ├── scheduler.py              # Priority + dependency resolver
│   └── runner.py                 # Claude Code Task tool spawner
├── tests/
├── README.md
└── pyproject.toml

~/.claude/skills/planner -> ~/soul/soul-planner/skills/planner     # symlink
~/.claude/agents/task-runner.md -> ~/soul/soul-planner/agents/task-runner.md
```

**Two modes:**
1. **Queue mode:** `/task add "description" --priority high --depends-on 3` for ad-hoc tasks
2. **Schedule mode:** Reads daily planner blocks, auto-queues block tasks at start time

**Components:**
- Task CRUD (add, list, status, cancel, retry)
- SQLite persistence (`~/.claude/soul-planner/tasks.db`)
- Dependency resolution (Task B waits for Task A)
- Priority scheduling (critical tasks jump queue)
- Background execution via Claude Code Task tool (`run_in_background: true`)
- Output capture and status tracking
- Daily block integration (schedule mode reads `docs/daily-planner.md`)

**Milestone:** I can run `/task add "extract soul-outreach db module"` and Claude picks it up, executes it, and I can check the result with `/task status`.

---

## Phase 2: soul-mesh (Weeks 3-5)

**Current state:** 253 tests, 3,370 LoC, v0.2.0. Cluster inventory working (node registry, heartbeats, WebSocket transport, TUI dashboard). Tested across titan-pi + titan-pc.

**What to build:**

### Layer 1: Unified SSH Gateway
- `soul-mesh shell` or `ssh mesh` drops into a virtual environment
- Aggregated view of resources across all nodes
- Can run commands that dispatch to the right node

### Layer 2: Shared Filesystem
- File registry DB table (id, path, size, sha256, owner_node_id)
- rsync-based file transfer between nodes
- Auto-sync model weights directory
- CLI: `soul-mesh push/pull/files`

### Layer 3: LLM Inference Proxy
- Model registry (which node runs which model)
- `POST /api/mesh/infer` routes to node with model loaded (OpenAI-compatible)
- Model lifecycle: `soul-mesh models load phi-3 --node titan-pc`
- Routing: least-busy node with requested model
- CLI: `soul-mesh infer --model phi-3 "What is 2+2?"`

### Layer 4: User-Friendly Install
- `pip install soul-mesh` with guided setup wizard
- `soul-mesh init` auto-detects hardware, generates config
- Documentation for adding nodes to the mesh

**Milestone:** SSH into the mesh. See it as one big machine. Load a GGUF model on titan-pc. Run inference from titan-pi. It just works.

---

## Phase 3: soul-outreach (Weeks 6-8)

**Current state:** 250 LoC (config.py + AI client). 3,200 LoC exists in soul-os ready to extract.

**What to build:**

### Week 6: Core Extraction
- `db.py` -- async SQLite schema (campaigns, contacts, drafts, sends, replies)
- `models.py` -- Pydantic schemas
- `email_sender.py` -- SMTP + SHA-256 payload verification + rate limits
- `guardrails.py` -- DNC, rate limiting, CAN-SPAM, banned phrases
- Replace all `brain.*` imports with standalone equivalents
- Verify: zero `from brain` imports remain

### Week 7: CLI Pipeline
- `cli.py` -- Click commands: import, enrich, draft, review, send, stats, doctor
- `reply_ingest.py` -- IMAP poller + classifier
- `agents/copywriter.py` -- Email draft generation
- `agents/researcher.py` -- Contact enrichment
- End-to-end test: import CSV -> enrich -> draft -> review -> send --dry-run

### Week 8: API + Polish
- `app.py` -- FastAPI app with CORS, routes
- `api/*.py` -- CRUD endpoints (campaigns, contacts, drafts, sends, stats)
- Docker compose for full stack
- README with setup guide
- First real campaign (small test batch)

**Milestone:** `outreach import contacts.csv && outreach enrich && outreach draft && outreach send --dry-run` works and shows what would be sent.

---

## Phase 4: soul-viz (Weeks 9-10)

**Current state:** Scaffold. Pydantic models defined (ChartSpec, DashboardSpec, 8 chart types). All implementation stubs.

**What to build:**

### Week 9: Backend
- Implement `ChartSelector.select_chart_type()` -- Claude picks best chart for data + prompt
- Implement `ChartSelector.generate_spec()` -- Claude generates full ChartSpec
- FastAPI endpoint: `POST /viz/chart` accepts `{data, prompt}`, returns ChartSpec
- Tests with mocked Claude responses

### Week 10: Frontend
- React component rendering ChartSpec via Recharts
- Demo page with example datasets
- `POST /viz/dashboard` for multi-panel layouts
- DashboardGenerator implementation

**Milestone:** POST data + "show revenue by month" to the API. Get back a rendered line chart on the frontend.

---

## Ongoing: soul-os

Not a sprint target. Gets better as side-effects of the other 4 projects:

- **From soul-planner:** Autonomous loop queues tasks into planner instead of processing inline
- **From soul-mesh:** soul-os uses mesh for inference instead of local Claude subprocess
- **From soul-outreach:** Already running in production inside soul-os
- **From soul-viz:** Dashboard panels use viz engine for charts

---

## Daily Rhythm

```
Block 1: BUILD   (9am - 1pm,  4h)  Current phase project ONLY
Block 2: EXPLORE (2pm - 6pm,  4h)  Research that feeds current project
Block 3: SOCIAL  (7pm - 9pm,  2h)  Content from BUILD + EXPLORE
Block 4: SCOUT   (9pm - 11pm, 2h)  Jobs, freelance, applications
```

**Block 2 aligns with Block 1:**

| Phase | Block 2 Focus |
|-------|---------------|
| soul-planner | Claude Code extension patterns, task scheduling, agent orchestration |
| soul-mesh | LLM inference distribution, llama.cpp, shared compute, distributed systems |
| soul-outreach | Email deliverability, campaign analytics, enrichment APIs, marketing |
| soul-viz | Visualization research, chart recommendation, Recharts/D3, data analysis |

---

## What Gets Dropped

| Category | Projects | Decision |
|----------|----------|----------|
| **Active (the 5)** | soul-planner, soul-mesh, soul-outreach, soul-viz, soul-os | Sequential development |
| **Already shipped** | soul-import (54 tests), soul-search (15 tests) | Parked. Publish when convenient. |
| **Supporting modules** | soul-auth, soul-knowledge, soul-heal, soul-loop | Stay in soul-os. Extract only if needed. |
| **Dropped from active** | soul-skills, soul-goals, soul-brain, soul-agents, soul-moa-*, soul-moe-*, soul-bench, soul-eval, soul-query, soul-relay, soul-cloud, soul-consult, soul-content, soul-web, soul-desktop, soul-term, soul-services, soul-deploy, soul-soc, soul-blog, soul-brand, soul-finance, soul-analytics | Not actively built. May revisit later. |

---

## Success Criteria (10 weeks)

- [ ] soul-planner: Queue + schedule tasks, Claude executes in background
- [ ] soul-mesh: SSH into mesh as one machine, run LLM inference across devices
- [ ] soul-outreach: Full CLI pipeline working, first campaign sent
- [ ] soul-viz: Data + prompt in, rendered chart out
- [ ] soul-os: Autonomous loop integrated with soul-planner
- [ ] 50+ LinkedIn posts published (from SOCIAL block)
- [ ] 10+ blog posts published (weekly assembly)
- [ ] Job applications ongoing (from SCOUT block)
