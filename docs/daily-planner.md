# Soul Ecosystem — Daily Planner

**Current Phase:** Phase 1 — Foundation (Weeks 1-2, Feb 22 - Mar 7)
**Strategy:** Build-Ship-Learn Flywheel (5 parallel tracks)
**Plans:** `docs/plans/2026-02-22-execution-plan-design.md`, `docs/plans/2026-02-22-dev-strategy-design.md`, `docs/plans/2026-02-22-marketing-strategy-design.md`

## Daily Rhythm

```
BLOCK 1: BUILD (9am - 1pm, 4h)
  Track A: Ship products — extract 2 projects/week from soul-app backup

BLOCK 2: EXPLORE (2pm - 6pm, 4h)
  Track B: Quantitative Finance — soul-finance, paper trading
  Track C: Data Analytics — soul-analytics, DuckDB, insights
  Track D: ML Research — CARS benchmark, soul-bench, quantization

BLOCK 3: MARKET (7pm - 11pm, 4h)
  Track E: Dashboard + marketing channels (LinkedIn, blog, job portals, freelance platforms, outreach)
```

## Legend

`[x]` done | `[ ]` pending | `[>]` in progress | `[-]` skipped | `[!]` blocked

---

# WEEK 1: Foundation (Feb 22 - Feb 28)

## Day 1 — Sun Feb 22

### Block 1: BUILD — soul-skills extraction setup (9am-1pm)
- [ ] SSH to titan-pc, list files in `soul/skills/` from soul-app backup
- [ ] Extract all 8 source files to `~/soul/soul-skills/soul_skills/`
- [ ] Create project structure: `pyproject.toml`, `README.md`, `CLAUDE.md`, `.gitignore`
- [ ] Init git repo, first commit (raw extraction)

### Block 2: EXPLORE — CARS baseline setup (2pm-6pm)
- [ ] SSH to titan-pc, install llama.cpp (compile from source for i5-8400)
- [ ] Download 3B model (e.g., Phi-3-mini-4k GGUF 4-bit) to titan-pc
- [ ] Run smoke test: simple prompt, verify inference works
- [ ] Document hardware baseline: inference speed, memory usage

### Block 3: MARKET — job portal profiles (7pm-11pm)
- [ ] Create Naukri profile, upload resume, set job preferences (AI/ML/Data, Delhi/Bangalore/Remote)
- [ ] Create Indeed profile, upload resume, set alerts for "AI Engineer" + "Data Engineer"
- [ ] Create Instahyre profile, enable "let companies find me"
- [ ] Read `docs/plans/2026-02-22-marketing-execution-plan.md` Task 1 for profile content

### Evening Review (11pm, 15min)
- [ ] Log what got done, note blockers, set tomorrow's focus

---

## Day 2 — Mon Feb 23

### Block 1: BUILD — soul-skills standalone (9am-1pm)
- [ ] Create `soul_skills/config.py` with `SKILLS_` env prefix (pydantic-settings)
- [ ] Replace all `soul.*` / `brain.*` imports with standalone equivalents
- [ ] Verify: `grep -r "from soul\|from brain" soul_skills/` returns ZERO
- [ ] Commit: standalone conversion

### Block 2: EXPLORE — soul-bench scaffolding (2pm-6pm)
- [ ] Review existing soul-bench scaffold at `~/soul/soul-bench/`
- [ ] Design 10 benchmark tasks (from soul-os task types)
- [ ] Implement CARS metric calculator: `CARS = Accuracy / (VRAM_GB x Latency_s)`
- [ ] Set up Colab Pro notebook for T4 GPU benchmark runs

### Block 3: MARKET — job portals continued + first content (7pm-11pm)
- [ ] Create Wellfound profile, follow target companies from `docs/marketing/target-companies.md`
- [ ] Create Monster India profile, upload resume
- [ ] Enable LinkedIn "Open to Work" (visible to recruiters only)
- [ ] Scan LinkedIn Jobs + Naukri, apply to 3-5 best matches

### Evening Review (11pm, 15min)
- [ ] soul-skills standalone? Benchmark design done? Portals count?

---

## Day 3 — Tue Feb 24

### Block 1: BUILD — soul-skills tests + soul-goals extraction (9am-1pm)
- [ ] Write tests for soul-skills (target: 15+ tests covering core functionality)
- [ ] Run tests: `cd ~/soul/soul-skills && python -m pytest tests/ -v`
- [ ] Push soul-skills to Gitea
- [ ] Start soul-goals: extract 5 files from titan-pc backup to `~/soul/soul-goals/`

### Block 2: EXPLORE — CARS baseline runs (2pm-6pm)
- [ ] Run Phi-3-mini 3B 4-bit through benchmark tasks on titan-pc
- [ ] Record: accuracy per task, latency, VRAM usage
- [ ] Calculate CARS score
- [ ] Start Colab notebook: run same benchmark on T4 for comparison

### Block 3: MARKET — freelance platforms batch 1 (7pm-11pm)
- [ ] Prepare freelance-specific profile content (headline, summary, rate, portfolio)
- [ ] Apply to Toptal (screening + timed test)
- [ ] Apply to Turing (automated coding tests)
- [ ] Apply to Andela (interview-based)
- [ ] Set up Twitter/X profile for tech content

### Evening Review (11pm, 15min)
- [ ] soul-skills tests passing? Goals extraction started? CARS results?

---

## Day 4 — Wed Feb 25

### Block 1: BUILD — soul-goals standalone + tests (9am-1pm)
- [ ] Create project structure: `pyproject.toml`, `README.md`, `CLAUDE.md`, `.gitignore`
- [ ] Create `soul_goals/config.py` with `GOALS_` env prefix
- [ ] Replace all `soul.*` / `brain.*` imports with standalone equivalents
- [ ] Write tests (target: 10+ tests)
- [ ] Run tests: `cd ~/soul/soul-goals && python -m pytest tests/ -v`
- [ ] Init git, commit, push to Gitea

### Block 2: EXPLORE — DuckDB analytics setup (2pm-6pm)
- [ ] Create `~/soul/soul-analytics/` repo structure
- [ ] Install DuckDB, set up initial database
- [ ] Load first dataset: market data from Yahoo Finance (1 year NSE index)
- [ ] Write first analysis notebook: basic market stats, moving averages
- [ ] Commit: soul-analytics foundation

### Block 3: MARKET — freelance platforms batch 2 + recruiter outreach (7pm-11pm)
- [ ] Apply to Uplers (profile review + skill test)
- [ ] Apply to Arc.dev (async coding challenge)
- [ ] Connect with 5 recruiters on LinkedIn (search "AI recruiter India")
- [ ] Register with 1-2 recruitment agencies (Michael Page, Hays India)
- [ ] LinkedIn post #1: building in public update (37 projects, extraction pattern)

### Evening Review (11pm, 15min)
- [ ] soul-goals done? Analytics loaded? Freelance apps count?

---

## Day 5 — Thu Feb 26

### Block 1: BUILD — push to GitHub + soul-outreach continued (9am-1pm)
- [ ] Push soul-skills to GitHub (public repo, clean README)
- [ ] Push soul-goals to GitHub (public repo, clean README)
- [ ] Verify both: CI-ready, `pip install -e .` works
- [ ] soul-outreach: review current state, identify next module to build (pipeline or CLI)

### Block 2: EXPLORE — Zerodha + finance setup (2pm-6pm)
- [ ] Create `~/soul/soul-finance/` repo structure
- [ ] Set up Yahoo Finance data ingestion (yfinance library)
- [ ] Pull 1 year of NSE Nifty 50 daily data into DuckDB
- [ ] Implement basic momentum strategy: buy when 20-day MA > 50-day MA
- [ ] Backtest on historical data, record results

### Block 3: MARKET — content + communities (7pm-11pm)
- [ ] Join r/selfhosted on Reddit (comment on 2-3 relevant posts)
- [ ] Join MLOps Community Slack (introduce yourself)
- [ ] Join Latent Space Discord (lurk, find relevant threads)
- [ ] Blog post #1 outline: "How I Architect 37 Projects as a Solo AI Engineer"
- [ ] Connect with 5 more recruiters on LinkedIn

### Evening Review (11pm, 15min)
- [ ] GitHub repos live? Finance backtest results? Communities joined?

---

## Day 6 — Fri Feb 27

### Block 1: BUILD — soul-outreach pipeline (9am-1pm)
- [ ] soul-outreach: build next priority module (pipeline, email sender, or CLI)
- [ ] Write tests for new module
- [ ] Verify: all existing tests still pass
- [ ] Commit progress

### Block 2: EXPLORE — CARS results + paper trading (2pm-6pm)
- [ ] Finalize CARS baseline results for 3B model (4-bit quantization)
- [ ] Write up results: accuracy per task, CARS score, comparison notes
- [ ] soul-finance: implement paper trading simulator (no real money)
- [ ] Run momentum strategy on recent 30 days, track simulated P&L

### Block 3: MARKET — blog draft + LinkedIn + applications (7pm-11pm)
- [ ] Write blog post #1 first draft (sections 1-3)
- [ ] LinkedIn post #2: CARS metric teaser or extraction pattern insight
- [ ] Scan job portals, apply to 5-8 roles (LinkedIn Jobs, Naukri, Indeed)
- [ ] Respond to any recruiter messages from the week

### Evening Review (11pm, 15min)
- [ ] Outreach module done? CARS documented? Blog draft progress?

---

## Day 7 — Sat Feb 28

### Block 1: BUILD — soul-mesh continued (9am-1pm)
- [ ] soul-mesh: identify next modules to extract (transport, sync, relay)
- [ ] Build next module with tests
- [ ] Verify: all 16+ tests still pass
- [ ] Commit progress

### Block 2: EXPLORE — analytics insight + research review (2pm-6pm)
- [ ] soul-analytics: produce first data insight (market trend visualization)
- [ ] Format as LinkedIn-ready chart/insight
- [ ] Review all CARS data collected this week, identify gaps
- [ ] Plan Week 2 EXPLORE priorities (extended CARS? more finance data?)

### Block 3: MARKET — week review + content batch (7pm-11pm)
- [ ] Finish blog post #1 draft
- [ ] Batch-write next week's 2 LinkedIn posts
- [ ] Review Instahyre/Wellfound inbound matches
- [ ] Refresh Naukri profile (triggers "recently active" boost)
- [ ] Plan next week's content topics

### Week 1 Review (11pm, 30min)
```
## Week 1 Review — Feb 28
### Block 1 (BUILD — Track A)
- soul-skills: extracted? [ ] standalone? [ ] tests? [ ] Gitea? [ ] GitHub? [ ]
- soul-goals: extracted? [ ] standalone? [ ] tests? [ ] Gitea? [ ] GitHub? [ ]
- soul-outreach: next module done? [ ]
- soul-mesh: continued? [ ]

### Block 2 (EXPLORE — Tracks B/C/D)
- CARS baseline 3B results: [ ]
- soul-finance repo + backtest: [ ]
- soul-analytics + first dataset: [ ]
- soul-bench scaffolded: [ ]

### Block 3 (MARKET — Track E + channels)
- Job portals live: __ / 6
- Freelance platforms applied: __ / 5
- Recruiter connections: __ / 10
- LinkedIn posts published: __ / 2
- Blog post #1 status: outline [ ] draft [ ] published [ ]
- Communities joined: __ / 3
- Job applications submitted: __

### Phase 1 Gate Progress (need 6/8 by end of Week 2)
- [ ] soul-skills extracted with tests, on GitHub
- [ ] soul-goals extracted with tests, on GitHub
- [ ] CARS baseline results for 3B models
- [ ] soul-finance repo with data ingestion working
- [ ] 6 job portal profiles live
- [ ] 5+ freelance platform applications submitted
- [ ] 2 LinkedIn posts published
- [ ] Blog post #1 drafted

### Week 2 Adjustments
- ...
```

---

# TRACKING

## Extraction Tracker

| # | Project | Extracted | Standalone | Tests | Gitea | GitHub |
|---|---------|-----------|------------|-------|-------|--------|
| 1 | soul-search | [x] | [x] | [x] 15 | [x] | [ ] |
| 2 | soul-import | [x] | [x] | [x] 54 | [x] | [ ] |
| 3 | soul-query | [x] scaffold | [x] | [ ] | [x] | [ ] |
| 4 | soul-viz | [x] scaffold | [x] | [ ] | [x] | [ ] |
| 5 | soul-skills | [ ] | [ ] | [ ] | [ ] | [ ] |
| 6 | soul-goals | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7 | soul-brain | [ ] | [ ] | [ ] | [ ] | [ ] |
| 8 | soul-agents | [ ] | [ ] | [ ] | [ ] | [ ] |
| 9 | soul-outreach | [>] partial | [>] | [ ] | [ ] | [ ] |
| 10 | soul-mesh | [>] partial | [>] | [x] 16 | [ ] | [ ] |

## Research Tracker

| Experiment | Setup | Running | Results | Published |
|-----------|-------|---------|---------|-----------|
| CARS baseline 3B 4-bit | [ ] | [ ] | [ ] | [ ] |
| CARS extended 8B | [ ] | [ ] | [ ] | [ ] |
| Finance momentum backtest | [ ] | [ ] | [ ] | [ ] |
| Finance mean-reversion backtest | [ ] | [ ] | [ ] | [ ] |

## Marketing Tracker

| Channel | Setup | Active | Metric |
|---------|-------|--------|--------|
| Naukri | [ ] | [ ] | recruiter views: __ |
| Indeed | [ ] | [ ] | applications: __ |
| Instahyre | [ ] | [ ] | inbound matches: __ |
| Wellfound | [ ] | [ ] | applications: __ |
| Monster India | [ ] | [ ] | recruiter views: __ |
| LinkedIn Jobs | [ ] | [ ] | applications: __ |
| Toptal | [ ] | [ ] | status: __ |
| Turing | [ ] | [ ] | status: __ |
| Andela | [ ] | [ ] | status: __ |
| Uplers | [ ] | [ ] | status: __ |
| Arc.dev | [ ] | [ ] | status: __ |
| LinkedIn Posts | [ ] | [ ] | posts: __ / impressions: __ |
| Blog | [ ] | [ ] | posts: __ / views: __ |
| Twitter/X | [ ] | [ ] | tweets: __ |
| Communities | [ ] | [ ] | joined: __ / 3 |
| Recruiters | [ ] | [ ] | connected: __ / 10 |

## Blog Tracker

| # | Title | Outline | Draft | Published | Shared |
|---|-------|---------|-------|-----------|--------|
| 1 | How I Architect 37 Projects as a Solo AI Engineer | [ ] | [ ] | [ ] | [ ] |
| 2 | Self-Healing AI: Hysteresis + Remediation | [ ] | [ ] | [ ] | [ ] |
| 3 | NL-to-SQL with Guardrails | [ ] | [ ] | [ ] | [ ] |

## Revenue Tracker

| Month | Consulting | Freelance | Product | Total |
|-------|-----------|-----------|---------|-------|
| Mar | $0 | $0 | $0 | $0 |
| Apr | | | | |
| May | | | | |

---

# DAILY REVIEW TEMPLATE

```
## Day __ Review — [date]
### Block 1 (BUILD)
- Completed: ...
- Blocked: ...
### Block 2 (EXPLORE)
- Completed: ...
- Blocked: ...
### Block 3 (MARKET)
- Completed: ...
- Blocked: ...
### Metrics
- Job applications submitted: __
- LinkedIn posts: __
- Code commits: __
### Tomorrow Focus
1. ...
2. ...
3. ...
```
