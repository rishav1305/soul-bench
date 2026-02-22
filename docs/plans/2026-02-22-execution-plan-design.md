# Build-Ship-Learn Flywheel — 6-Week Execution Plan

**Date:** 2026-02-22
**Status:** Approved
**Depends on:** dev-strategy-design.md (5 tracks), marketing-strategy-design.md (11 channels)
**Replaces:** sprint1-implementation.md (completed)

---

## Overview

Phase-gated execution of the Build-Ship-Learn Flywheel across all 5 tracks, integrated with the 11-channel marketing strategy. 3 phases, 6 weeks, gates between each.

**Daily blocks:**
```
Block 1 (9am-1pm)   BUILD      Track A: Ship products
Block 2 (2pm-6pm)   EXPLORE    Tracks B/C/D: Finance, analytics, ML research
Block 3 (7pm-11pm)  MARKET     Track E + marketing channels
```

**Already completed (Sprint 1):**
- soul-search: 4 commits, 15 tests, on Gitea
- soul-import: 4 commits, 54 tests, on Gitea
- soul-query: scaffold, on Gitea
- soul-viz: scaffold, on Gitea

---

## Phase 1: Foundation (Weeks 1-2, Feb 22 - Mar 7)

**Theme:** Fast wins + profiles live everywhere + research baseline
**Cost:** 0 INR

### BUILD block (9am-1pm) — Track A

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W1 Mon-Tue | soul-skills extraction | 8 files extracted, standalone, tests |
| W1 Wed-Thu | soul-goals extraction | 5 files extracted, standalone, tests |
| W1 Fri | Push both to Gitea + GitHub | 2 repos public |
| W2 Mon-Wed | soul-outreach continued build | Pipeline + CLI working |
| W2 Thu-Fri | soul-mesh continued build | Transport + sync modules |

### EXPLORE block (2pm-6pm) — Tracks B, C, D

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W1 Mon-Tue | CARS baseline setup (Track D) | llama.cpp on titan-pc, 3B model downloaded |
| W1 Wed-Thu | soul-bench runner scaffolding (Track D) | Benchmark harness running on Colab T4 |
| W1 Fri | DuckDB analytics setup (Track C) | soul-analytics repo + first dataset loaded |
| W2 Mon-Tue | CARS baseline runs (Track D) | 3B model 4-bit results published |
| W2 Wed-Thu | Zerodha API setup (Track B) | soul-finance repo, data ingestion from Yahoo Finance |
| W2 Fri | Paper trading scaffold (Track B) | Basic momentum strategy on historical data |

### MARKET block (7pm-11pm) — Track E + Marketing

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W1 Mon | Job portal profiles (Naukri, Indeed, Instahyre) | 3 profiles live |
| W1 Tue | Job portal profiles (Wellfound, Monster, LinkedIn Jobs) | 6 profiles live |
| W1 Wed-Thu | Freelance platforms (Toptal, Turing, Andela, Uplers, Arc.dev) | 5 applications submitted |
| W1 Fri | Recruiter outreach (connect with 10 on LinkedIn, register 3 agencies) | 13 recruiter touchpoints |
| W2 Mon | Blog post #1 outline: "How I Architect 37 Projects with AI Tools" | Draft started |
| W2 Tue-Wed | LinkedIn post #1 + Twitter setup | First content published |
| W2 Thu | Join communities (r/selfhosted, MLOps Slack, Latent Space Discord) | 3 communities joined |
| W2 Fri | Blog post #1 draft complete + LinkedIn post #2 | Blog ready for editing |

### Phase 1 Gate

Must hit 6/8 to proceed to Phase 2:

- [ ] soul-skills extracted with tests, on GitHub
- [ ] soul-goals extracted with tests, on GitHub
- [ ] CARS baseline results for 3B models
- [ ] soul-finance repo with data ingestion working
- [ ] 6 job portal profiles live
- [ ] 5+ freelance platform applications submitted
- [ ] 2 LinkedIn posts published
- [ ] Blog post #1 drafted

---

## Phase 2: Core (Weeks 3-4, Mar 8 - Mar 21)

**Theme:** Architecture projects + content cadence + first outreach
**Cost:** ~2000-3000 INR/month

### BUILD block (9am-1pm) — Track A

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W3 Mon-Wed | soul-brain extraction | 9 files extracted, orchestrator + intent + persona standalone |
| W3 Thu-Fri | soul-brain tests + push | Tests passing, on Gitea + GitHub |
| W4 Mon-Wed | soul-agents build | Registry, tool executor, YAML prompts, boundary enforcement |
| W4 Thu | soul-agents tests | Boundary enforcement tests passing |
| W4 Fri | soul-agents push + soul-moa-core scaffold review | 2 repos shipped |

### EXPLORE block (2pm-6pm) — Tracks B, C, D

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W3 Mon-Tue | Finance data ingestion (Track B) | NSE bhavcopy + Yahoo Finance daily pulls into DuckDB |
| W3 Wed-Thu | CARS extended setup (Track D) | 8B model quantized, Colab T4 benchmark running |
| W3 Fri | Analytics first dataset (Track C) | Market data analysis notebook, first LinkedIn data insight |
| W4 Mon-Tue | Paper trading v1 (Track B) | Momentum strategy backtested on 1 year NSE data |
| W4 Wed-Thu | CARS extended results (Track D) | 8B model results, CARS leaderboard draft |
| W4 Fri | soul-analytics insight #2 (Track C) | Second dataset analyzed, blog-ready charts |

### MARKET block (7pm-11pm) — Track E + Marketing

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W3 Mon | Publish blog post #1 + cross-post dev.to | First blog live |
| W3 Tue | LinkedIn post #3 (extraction pattern deep-dive) | Content cadence established |
| W3 Wed | Apply to 7 remaining freelance platforms | All 12 platforms submitted |
| W3 Thu | Cold email infra setup (sending domain, SPF/DKIM/DMARC) | Deliverability ready |
| W3 Fri | LinkedIn post #4 + engage 10 target people's posts | Engagement routine started |
| W4 Mon | Email warmup started + 5-10 LinkedIn DMs | Outreach pipeline active |
| W4 Tue | Blog post #2 outline: "Self-Healing AI: Hysteresis + Remediation" | Draft started |
| W4 Wed-Thu | 10 job applications/week routine established | Application pipeline steady |
| W4 Fri | LinkedIn post #5 + blog post #2 draft + weekly analytics review | Content + metrics |

### Phase 2 Gate

Must hit 6/8 to proceed to Phase 3:

- [ ] soul-brain extracted with tests, on GitHub
- [ ] soul-agents built with boundary enforcement tests, on GitHub
- [ ] CARS leaderboard with 3B + 8B results drafted
- [ ] Paper trading backtested on 1+ strategy
- [ ] Blog posts #1 published, #2 drafted
- [ ] 4+ LinkedIn posts published
- [ ] Cold email infra live (domain warmed)
- [ ] 10+ freelance platforms applied to

---

## Phase 3: Scale (Weeks 5-6, Mar 22 - Apr 4)

**Theme:** Implementation depth + launch prep + scale what works
**Cost:** ~5000-8000 INR/month

### BUILD block (9am-1pm) — Track A

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W5 Mon-Wed | soul-query implementation | Guardrails working, SQL generation from prompts |
| W5 Thu-Fri | soul-query tests + Redshift engine | Integration tests, schema whitelist enforced |
| W6 Mon-Wed | soul-viz implementation | Chart selector working, dashboard generation from data |
| W6 Thu | soul-viz tests | End-to-end prompt-to-chart tests |
| W6 Fri | Push both + ecosystem review | 9+ projects shipped total |

### EXPLORE block (2pm-6pm) — Tracks B, C, D

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W5 Mon-Tue | Finance backtesting v2 (Track B) | Mean-reversion strategy added, compare with momentum |
| W5 Wed-Thu | Extended CARS runs (Track D) | Multiple quantization levels compared (4-bit vs 8-bit) |
| W5 Fri | soul-bench automated runner (Track D) | Benchmark runs from titan-pi, results auto-published |
| W6 Mon-Tue | Paper trading live (Track B) | Best strategy running paper trades on Zerodha |
| W6 Wed-Thu | Analytics deep-dive (Track C) | Monthly report: CARS leaderboard + market analysis |
| W6 Fri | Dashboard MVP (Track E) | soul-web panels showing build pipeline + research + finance |

### MARKET block (7pm-11pm) — Track E + Marketing

| Week | Day Focus | Deliverable |
|------|-----------|-------------|
| W5 Mon | Blog post #2 published + cross-post | 2 blogs live |
| W5 Tue | LinkedIn post #6 (soul-query announcement) | NL-to-SQL content |
| W5 Wed | First 20-30 cold emails sent | Outbound pipeline active |
| W5 Thu | Evaluate LinkedIn Premium (upgrade if 1000+ impressions/post) | Data-driven decision |
| W5 Fri | LinkedIn post #7 + community engagement review | Cut underperforming communities |
| W6 Mon | Blog post #3 outline: "NL-to-SQL with Guardrails" | Technical depth piece |
| W6 Tue | Portfolio site update (showcase 9+ projects) | rishavchatterjee.com refreshed |
| W6 Wed | LinkedIn post #8 + scale cold email to 15-20/day if reply rate >5% | Scale what works |
| W6 Thu | Product Hunt prep for soul-outreach (if Phase 1-2 complete) | Launch checklist started |
| W6 Fri | Blog post #3 draft + 6-week retrospective | Metrics review, plan next cycle |

### Phase 3 Gate (Final)

Must hit 7/10:

- [ ] soul-query with working guardrails + tests, on GitHub
- [ ] soul-viz with chart generation + tests, on GitHub
- [ ] 9+ total projects extracted and on GitHub
- [ ] CARS leaderboard published with 3B + 8B results
- [ ] Paper trading running on 1+ strategy
- [ ] Dashboard MVP showing data from 3+ tracks
- [ ] 3 blog posts published
- [ ] 8+ LinkedIn posts published
- [ ] 50+ job applications submitted
- [ ] Cold outreach generating replies

---

## Phase Summary

| | Phase 1 (W1-2) | Phase 2 (W3-4) | Phase 3 (W5-6) |
|---|---|---|---|
| **Track A** | soul-skills, soul-goals | soul-brain, soul-agents | soul-query, soul-viz impl |
| **Track B** | Zerodha setup, Yahoo data | Backtest momentum, NSE ingestion | Paper trading live |
| **Track C** | DuckDB setup, first dataset | 2 analytics insights | Monthly report |
| **Track D** | CARS baseline 3B | CARS extended 8B | Automated runner, leaderboard |
| **Track E** | -- | -- | Dashboard MVP |
| **Marketing** | Profiles (6 portals, 5 freelance) | Content cadence, cold email infra | Scale outbound, portfolio update |
| **Cost** | 0 INR | ~2000-3000 INR/mo | ~5000-8000 INR/mo |
| **Gate** | 6/8 | 6/8 | 7/10 |

---

## Success Criteria (6 weeks)

From dev-strategy-design.md, validated against this plan:

- 9+ projects extracted and pushed to GitHub with tests
- soul-query with schema guardrails working
- CARS leaderboard published with 3B + 8B results
- Paper trading running on at least 1 strategy
- 8+ LinkedIn posts, 3 blog posts published
- soul-os dashboard showing real-time data from 3+ tracks
- 50+ job applications submitted across 6 portals
- 10+ freelance platforms applied to
- Cold email infrastructure live and generating replies

---

## Key Dependencies

```
Phase 1 -> Phase 2:
  soul-skills/goals done -> frees time for soul-brain/agents
  CARS baseline done -> informs extended runs
  Job portals live -> application pipeline feeds Phase 2 volume

Phase 2 -> Phase 3:
  soul-brain done -> soul-query can import orchestration patterns
  soul-agents done -> boundary enforcement informs soul-query guardrails
  Cold email infra warmed -> ready for outbound campaigns
  Content cadence proven -> scale what works in Phase 3
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| soul-brain extraction complex (9 files, deep dependencies) | Allocate 3 full days, accept partial extraction |
| CARS runs need GPU time | Pre-book Colab Pro sessions, have RunPod as fallback |
| Cold email deliverability takes 2-3 weeks | Start warmup in Phase 2 Week 3, ready by Phase 3 |
| Freelance platform vetting slow (Toptal 2-4 weeks) | Apply in Phase 1, don't block on results |
| Spreading too thin across 5 tracks | BUILD block is sacred — Track A always gets 4h/day |
