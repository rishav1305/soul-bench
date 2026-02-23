# Soul Ecosystem — Daily Planner

**Current Phase:** Phase 1 — Foundation (Weeks 1-2, Feb 22 - Mar 7)
**Strategy:** Build-Ship-Learn Flywheel (5 parallel tracks)
**Plans:** `docs/plans/2026-02-22-execution-plan-design.md`, `docs/plans/2026-02-22-dev-strategy-design.md`, `docs/plans/2026-02-22-marketing-strategy-design.md`, `docs/plans/2026-02-23-daily-content-strategy-design.md`

## Daily Rhythm

```
BLOCK 1: BUILD (9am - 1pm, 4h)
  Ship products, extract code, write tests

BLOCK 2: EXPLORE (2pm - 6pm, 4h)
  Research, analytics, CARS benchmark, finance, DuckDB

BLOCK 3: SOCIAL (7pm - 9pm, 2h)
  Content from Block 1+2 -> LinkedIn, Twitter, blog, dev.to, Reddit

BLOCK 4: SCOUT (9pm - 11pm, 2h)
  Job portals, freelance platforms, recruiter outreach, applications
```

## Legend

`[x]` done | `[ ]` pending | `[>]` in progress | `[-]` skipped | `[!]` blocked

---

# WEEK 1: Foundation (Feb 22 - Feb 28)

## Day 1 — Sun Feb 22

### Block 1: BUILD — soul-mesh continued (9am-1pm)
- [x] Review soul-mesh current state (16 tests, node/discovery/election done)
- [x] Identify next modules to extract (transport, sync, relay)
- [x] Extract and standalone-ify next module with tests
- [x] Verify: all tests pass, zero `from brain` imports

### Block 2: EXPLORE — CARS baseline setup (2pm-6pm)
- [x] SSH to titan-pc, install llama.cpp (compile from source for i5-8400)
- [x] Download 3B model (e.g., Phi-3-mini-4k GGUF 4-bit) to titan-pc
- [x] Run smoke test: simple prompt, verify inference works
- [x] Document hardware baseline: inference speed, memory usage

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

### Block 3: SOCIAL — first daily content (7pm-9pm)
- [ ] Set up content-log: create `docs/content-log.md`
- [ ] Draft LinkedIn post from today's BUILD work (soul-skills extraction)
- [ ] Draft Twitter thread from today's EXPLORE work (soul-bench scaffolding)
- [ ] Post after user approval

### Block 4: SCOUT — job portals continued (9pm-11pm)
- [ ] Create Wellfound profile, follow target companies from `docs/marketing/target-companies.md`
- [ ] Create Monster India profile, upload resume
- [ ] Enable LinkedIn "Open to Work" (visible to recruiters only)
- [ ] Scan LinkedIn Jobs + Naukri, apply to 3-5 best matches

### Evening Review (11pm, 15min)
- [ ] soul-skills standalone? Benchmark design done? Content posted? Portals count?

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

### Block 3: SOCIAL — metrics post (7pm-9pm)
- [ ] Review Block 1+2 notes from content-log
- [ ] Draft LinkedIn post: CARS baseline metrics (Tue = Metrics Post)
- [ ] Adapt to Twitter thread
- [ ] Post after user approval

### Block 4: SCOUT — freelance platforms batch 1 (9pm-11pm)
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

### Block 3: SOCIAL — architecture diagram (7pm-9pm)
- [ ] Review Block 1+2 notes from content-log
- [ ] Draft LinkedIn post: soul-goals architecture or DuckDB analytics setup (Wed = Architecture)
- [ ] Adapt to Twitter thread with diagram
- [ ] Post after user approval

### Block 4: SCOUT — freelance platforms batch 2 + recruiter outreach (9pm-11pm)
- [ ] Apply to Uplers (profile review + skill test)
- [ ] Apply to Arc.dev (async coding challenge)
- [ ] Connect with 5 recruiters on LinkedIn (search "AI recruiter India")
- [ ] Register with 1-2 recruitment agencies (Michael Page, Hays India)

### Evening Review (11pm, 15min)
- [ ] soul-goals done? Analytics loaded? Content posted? Freelance apps count?

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

### Block 3: SOCIAL — opinion/insight post (7pm-9pm)
- [ ] Review Block 1+2 notes from content-log
- [ ] Draft LinkedIn post: opinion piece (Thu = Opinion/Insight)
- [ ] Adapt to Twitter thread
- [ ] Join r/selfhosted, r/MachineLearning — comment with genuine value
- [ ] Post after user approval

### Block 4: SCOUT — communities + recruiter outreach (9pm-11pm)
- [ ] Join MLOps Community Slack (introduce yourself)
- [ ] Join Latent Space Discord (lurk, find relevant threads)
- [ ] Connect with 5 more recruiters on LinkedIn
- [ ] Scan LinkedIn Jobs + Naukri, apply to 3-5 best matches

### Evening Review (11pm, 15min)
- [ ] GitHub repos live? Finance backtest results? Content posted? Communities joined?

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

### Block 3: SOCIAL — weekly progress post (7pm-9pm)
- [ ] Review content-log for the full week
- [ ] Draft LinkedIn post: week's highlights (Fri = Weekly Progress)
- [ ] Adapt to Twitter thread
- [ ] Post after user approval

### Block 4: SCOUT — applications + follow-ups (9pm-11pm)
- [ ] Scan job portals, apply to 5-8 roles (LinkedIn Jobs, Naukri, Indeed)
- [ ] Respond to any recruiter messages from the week
- [ ] Follow up on pending applications (1 week old+)

### Evening Review (11pm, 15min)
- [ ] Outreach module done? CARS documented? Content posted? Applications count?

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

### Block 3: SOCIAL — blog assembly (7pm-9pm)
- [ ] Pull Mon-Fri LinkedIn posts from content-log
- [ ] Pick 2-3 strongest themes from the week
- [ ] Assemble into 600-1000 word blog post
- [ ] Publish on blog (canonical), cross-post to dev.to
- [ ] Share blog link on LinkedIn + Twitter

### Block 4: SCOUT — week review + refresh (9pm-11pm)
- [ ] Review Instahyre/Wellfound inbound matches
- [ ] Refresh Naukri profile (triggers "recently active" boost)
- [ ] Plan next week's SCOUT priorities
- [ ] Log weekly SCOUT metrics (applications, responses, interviews)

### Week 1 Review (11pm, 30min)
```
## Week 1 Review — Feb 28
### Block 1 (BUILD)
- soul-skills: extracted? [ ] standalone? [ ] tests? [ ] Gitea? [ ] GitHub? [ ]
- soul-goals: extracted? [ ] standalone? [ ] tests? [ ] Gitea? [ ] GitHub? [ ]
- soul-outreach: next module done? [ ]
- soul-mesh: continued? [ ]

### Block 2 (EXPLORE)
- CARS baseline 3B results: [ ]
- soul-finance repo + backtest: [ ]
- soul-analytics + first dataset: [ ]
- soul-bench scaffolded: [ ]

### Block 3 (SOCIAL)
- LinkedIn posts published: __ / 5
- Twitter threads published: __ / 5
- Blog post #1 status: assembled [ ] published [ ] cross-posted [ ]
- Content-log entries: __

### Block 4 (SCOUT)
- Job portals live: __ / 6
- Freelance platforms applied: __ / 5
- Recruiter connections: __ / 10
- Communities joined: __ / 3
- Job applications submitted: __

### Phase 1 Gate Progress (need 6/8 by end of Week 2)
- [ ] soul-skills extracted with tests, on GitHub
- [ ] soul-goals extracted with tests, on GitHub
- [ ] CARS baseline results for 3B models
- [ ] soul-finance repo with data ingestion working
- [ ] 6 job portal profiles live
- [ ] 5+ freelance platform applications submitted
- [ ] 5 LinkedIn posts published
- [ ] Blog post #1 published

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
| 10 | soul-mesh | [x] complete | [x] | [x] 100 | [ ] | [ ] |

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
