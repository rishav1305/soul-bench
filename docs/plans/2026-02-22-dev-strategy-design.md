# Build-Ship-Learn Flywheel — Dev Strategy Design

**Date:** 2026-02-22
**Status:** Approved
**Replaces:** MASTER_PLAN.md (sequential 7-phase approach)

---

## Problem

The existing dev master plan is sequential and slow: 7 phases over 6+ months, one project at a time. This doesn't match the goal of shipping fast, building a research portfolio, doing analytics, and generating income from multiple angles simultaneously.

## Strategy: Build-Ship-Learn Flywheel

Five parallel tracks running concurrently, with content generated as a byproduct of building. Every build produces a blog post, every analytics insight feeds a LinkedIn post, every research result becomes a thread.

## Redesigned Daily Blocks

```
Block 1 (9am-1pm)   BUILD      Ship code. 2 projects/week target.
Block 2 (2pm-6pm)   EXPLORE    Research, analytics, trading, experiments.
Block 3 (7pm-11pm)  MARKET     Content from today's builds. LinkedIn, blog, outreach.
```

## Hardware Inventory

| Node | Specs | Role |
|------|-------|------|
| titan-pi | RPi5 16GB, ARM64 | Production host (soul-os, services) |
| titan-pc | i5-8400, 8GB RAM, Intel UHD 630, 841GB free | Storage, backups, light compute |
| Cloud GPU | Colab Pro ($12/mo) -> RunPod/Vast.ai as needed | ML inference, benchmarking |

---

## Track A: Ship Products (BUILD block)

**Goal:** Extract, package, and ship 2 projects per week from existing codebase.

### Tier 1 — Ready to extract (have code in soul-app backup)

| # | Project | Source | What It Ships |
|---|---------|--------|---------------|
| 1 | soul-outreach | Migrated, config.py + agents/client.py done | Email campaign platform |
| 2 | soul-mesh | Migrated, 16 tests passing | Distributed mesh networking |
| 3 | soul-import | soul-app `soul/importers/` (7 .py) | ChatGPT, RSS, URL, email, CSV, Drive importers |
| 4 | soul-skills | soul-app `soul/skills/` (8 .py) | Web research, scraping, price compare, drafting |
| 5 | soul-brain | soul-app `soul/brain/` (9 .py) | Orchestrator, intent, persona, self-model, boundaries |
| 6 | soul-search | soul-app `soul/search/` (8 .py) | DuckDuckGo, Brave, Tavily, Google aggregator |
| 7 | soul-goals | soul-app `soul/goals/` (5 .py) | Goal planner, executor, manager, templates |

### Tier 2 — Have specs, need build-out

| # | Project | Origin | What It Ships |
|---|---------|--------|---------------|
| 8 | soul-query | delve-ai split | NL-to-SQL engine with guardrails |
| 9 | soul-viz | delve-ai split | Prompt-to-visualization, dashboards |
| 10 | soul-agents | soul-os extraction | YAML agents with boundary enforcement |
| 11 | soul-moa-core | soul-moa scaffold | MoA proposer/aggregator |
| 12 | cortex | soul-app dossier | Agentic OS for Raspberry Pi |

### Tier 3 — Research code, need packaging

| # | Project | What It Ships |
|---|---------|---------------|
| 13 | soul-bench | CARS benchmark runner (from cognitive-cost-quantization) |
| 14 | soul-eval | Claude baseline comparison + stats |

### delve-ai Decomposition

delve-ai splits into 2 new projects + enhancements to 6 existing ones:

**New projects:**
- **soul-query** — NL-to-SQL core: intent classification, SQL generation, schema context injection, table whitelisting, dual engine support (Redshift + Athena), query validation, results export
- **soul-viz** — Visualization layer: chart generation from query results, prompt-to-dashboard, exportable dashboard definitions

**Enhanced existing projects:**

| delve-ai Component | Attaches To |
|--------------------|-------------|
| Agent routing/orchestration | soul-agents |
| Observability (Prometheus + Jaeger) | soul-moa-telemetry |
| Hybrid RAG (embeddings retrieval) | soul-knowledge |
| Frontend (query UI) | soul-web |
| Role-based access | soul-auth |
| Learning loop (feedback -> improve) | soul-eval |

### Extraction Pattern (standard for all)

1. Create repo structure (pyproject.toml, README, tests/)
2. Copy source files from backup or soul-os
3. Replace `brain.*` imports with standalone equivalents
4. Replace `brain.config.settings` with pydantic-settings (PROJECT_ prefix)
5. Replace `brain.claude_client` with project-specific Anthropic SDK wrapper
6. Verify: `grep -r "from brain" src/` returns ZERO results
7. Write tests, CI, README
8. Push to Gitea, then GitHub

### Shipping Cadence

- Week 1-2: soul-import, soul-search (smallest, fastest wins)
- Week 3-4: soul-skills, soul-goals (medium complexity)
- Week 5-6: soul-brain, soul-agents (core architecture)
- Ongoing: soul-query, soul-viz, cortex (larger builds)

---

## Track B: Quantitative Finance (EXPLORE block)

**Goal:** Build soul-finance for automated trading and backtesting.

### Components

| Module | What It Does |
|--------|-------------|
| soul-finance/data | Market data ingestion (Zerodha Kite API, Yahoo Finance, NSE) |
| soul-finance/backtest | Strategy backtesting engine (vectorbt or custom) |
| soul-finance/signals | Technical indicators + ML signal generation |
| soul-finance/execute | Paper trading first, then live (Zerodha Kite) |
| soul-finance/dashboard | Portfolio tracking, P&L, risk metrics |

### Approach

1. Start with paper trading only (no real money until backtested)
2. Indian markets first (NSE/BSE via Zerodha Kite API)
3. DuckDB for analytics, not Postgres
4. Strategies: start with momentum/mean-reversion, graduate to ML signals

### Budget

- Zerodha account: existing
- Data feeds: free tier (Yahoo Finance, NSE bhavcopy)
- Cloud compute: none needed initially (runs on titan-pi)

---

## Track C: Data Analytics Lab (EXPLORE block)

**Goal:** Build soul-analytics for deep data analysis with published insights.

### Data Sources

| Source | Type | Use |
|--------|------|-----|
| Financial/market data | Time series | Trading signals, market analysis |
| AI/ML benchmarks | Structured | CARS leaderboard, model comparisons |
| Public datasets (Kaggle) | Various | Practice, blog content |
| Personal/business data | Mixed | soul-os metrics, outreach analytics |

### Stack

- DuckDB for all analytics (no Postgres overhead)
- Jupyter notebooks for exploration
- Recharts/D3 for visualization (via soul-viz)
- Published insights -> LinkedIn posts, blog articles

### Output

- Weekly data insight (LinkedIn post)
- Monthly deep-dive (blog post)
- Quarterly research report (CARS leaderboard update)

---

## Track D: ML Research on a Budget (EXPLORE block)

**Goal:** Run CARS benchmarks and quantization experiments without expensive hardware.

### Approach

1. **CPU-first:** llama.cpp on titan-pc (i5-8400, 8GB RAM) for small models (3B quantized)
2. **Cloud GPU:** Colab Pro ($12/mo, T4 15GB) for benchmarking runs
3. **Graduate:** RunPod/Vast.ai ($0.30-0.50/hr) for larger experiments when needed

### Research Agenda

| Experiment | Hardware | Timeline |
|-----------|----------|----------|
| CARS baseline (3B models, 4-bit) | Colab T4 | Week 1-2 |
| CARS extended (8B models) | Colab T4 | Week 3-4 |
| MLX fine-tuning experiments | Colab / RunPod | Month 2 |
| soul-bench automated runner | titan-pi orchestration | Month 2 |

### Key Metric

```
CARS = Reasoning Accuracy / (VRAM_GB x Latency_s)
```

Deploy gate: >=80% accuracy vs Claude, no task below 70%, P95 latency <5s.

---

## Track E: Personal Intelligence Dashboard (BUILD block)

**Goal:** soul-os dashboard that ties all tracks together.

### Panels

| Panel | Data Source | Shows |
|-------|-----------|-------|
| Build Pipeline | Gitea API + soul-deploy | Projects shipped, CI status, GitHub stars |
| Finance | soul-finance | Portfolio value, daily P&L, active strategies |
| Analytics | soul-analytics | Recent insights, dataset status, metrics |
| Research | soul-bench | CARS leaderboard, experiment status |
| Outreach | soul-outreach | Campaign metrics, reply rates, pipeline |
| Career | channel-tracker.md | Applications, responses, interviews |

### Implementation

- Extend existing soul-web React PWA
- WebSocket for real-time updates
- Mobile-friendly (existing PWA capability)

---

## Updated Ecosystem Count

| Category | Count |
|----------|-------|
| Previous ecosystem | 33 projects |
| New from delve-ai split | +2 (soul-query, soul-viz) |
| New from Track B | +1 (soul-finance) |
| New from Track C | +1 (soul-analytics) |
| **Total** | **37 projects** |

---

## 6-Week Sprint Overview

| Week | BUILD (Track A) | EXPLORE (Tracks B-D) | MARKET (Track E + content) |
|------|----------------|---------------------|---------------------------|
| 1 | soul-import, soul-search extract | CARS baseline setup | Blog: "Why I split a monolith into 37 projects" |
| 2 | soul-skills, soul-goals extract | Paper trading scaffold | LinkedIn: extraction pattern post |
| 3 | soul-brain extract | Finance data ingestion | Blog: "CARS metric explained" |
| 4 | soul-agents build | Analytics first dataset | LinkedIn: soul-query announcement |
| 5 | soul-query scaffold | Extended CARS runs | Blog: "NL-to-SQL with guardrails" |
| 6 | soul-viz scaffold | Finance backtesting | Portfolio site update |

---

## Success Criteria (6 weeks)

- 7+ projects extracted and pushed to GitHub with tests
- soul-query scaffolded with schema guardrails working
- CARS leaderboard published with 3B + 8B results
- Paper trading running on at least 1 strategy
- 6 LinkedIn posts, 3 blog posts published
- soul-os dashboard showing real-time data from 3+ tracks
