# Design: Comprehensive Daily Planner

## Date: 2026-02-21

## Problem
Existing daily planner only covers soul-outreach extraction + portfolio as evening tasks. Doesn't manage all 31 projects across 3 career tracks simultaneously.

## Design Decisions

### Daily Rhythm (12-14h)
- **Block 1 (4h):** Primary dev -- soul-outreach critical path
- **Block 2 (4h):** Secondary dev -- project extractions, soul-moa/moe, documentation
- **Block 3 (4h):** Outreach & career -- campaigns, blog, LinkedIn, portfolio
- **Buffer (1h):** 30min morning planning + 30min evening review

### Time Horizon
- Day-by-day for 4 weeks (Feb 21 - Mar 20)
- Weekly cadence for months 2-6

### Project Extraction Schedule (1-2 per week)
- Week 1: soul-mesh + soul-agents (P0 critical path)
- Week 2: soul-heal + soul-auth (production code, easy extracts)
- Week 3: soul-moa-core (P1 differentiator)
- Week 4: soul-loop + soul-soc (production, fills portfolio)

### Approach Selected
Time-blocked daily schedule (Approach A) -- all 3 career tracks advance every day.

### Output Files
- `soul/docs/daily-planner.md` -- the comprehensive planner (replaces soul-outreach version as the master)
- `soul/soul-outreach/docs/daily-planner.md` -- kept as outreach-specific reference
