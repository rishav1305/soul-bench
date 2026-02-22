# Soul AI — Roadmap

Prioritized action plan with dependencies and "done" criteria.

## Priority Tiers

### P0: Income-Critical (Weeks 1-4)

Must complete first. Generates revenue or enables job search.

#### 1. soul-outreach Phase 1: Extract & Standalone

- **Source**: soul-os `brain/modules/outreach/`
- **Target**: `~/projects/public/soul-outreach/`
- **Work**: Replace brain.* imports, standalone config, standalone DB init, CLI entry point
- **Done when**: `pip install soul-outreach` works, `outreach import/enrich/draft/review/send` work standalone
- **Dependencies**: None
- **Effort**: ~1 week

#### 2. soul-agents: Extract from soul-os

- **Source**: soul-os `brain/agents/` + `brain/tools/`
- **Target**: `~/projects/public/soul-agents/` (needs code)
- **Work**: Extract agent registry, YAML loader, tool executor, boundary enforcement
- **Done when**: `pip install soul-agents` works, working example with YAML agent + boundary enforcement
- **Dependencies**: None (parallel with #1)
- **Effort**: ~3-4 days

#### 3. soul-mesh: Extract from soul-os

- **Source**: soul-os `brain/mesh/` + `brain/relay/`
- **Target**: `~/projects/public/soul-mesh/` (needs code)
- **Work**: Extract node identity, discovery, hub election, transport, sync
- **Done when**: `pip install soul-mesh` works, working 2-node demo on local network
- **Dependencies**: None (parallel with #1, #2)
- **Effort**: ~3-4 days

---

### P1: Differentiator (Weeks 3-6)

Strongest portfolio pieces. What sets you apart.

#### 4. soul-moa-core: Implement MoA

- **Source**: `~/projects/public/soul-moa/` (scaffold exists)
- **Work**: Implement agent loop, tool registry, boundary enforcement, streaming, MoA proposer/aggregator
- **Done when**: Working MoA demo where proposer/aggregator beats individual agents on at least 3 task types
- **Dependencies**: None (can start anytime)
- **Effort**: ~1 week

#### 5. soul-brand: GitHub + LinkedIn Polish

- **Work**: Profile README, 5 pinned repos with clean READMEs, CI badges, PyPI links, LinkedIn optimization
- **Done when**: GitHub profile is professional with 5+ pinned repos, all with CI green
- **Dependencies**: #1, #2, #3 (need repos to pin)
- **Effort**: ~2-3 days

---

### P2: Deploy (Weeks 4-8)

Run outreach campaigns and publish content.

#### 6. campaign-ai-labs: Execute

- **Contacts**: 80-120 (LinkedIn -> CSV import)
- **Enrichment**: Researcher agent pulls team papers, open roles, interviewer backgrounds
- **Personalization**: Lead with relevant project per role (infra -> soul-mesh, safety -> soul-agents, research -> soul-moa)
- **Done when**: Contacts imported, enriched, drafts reviewed, first batch sent
- **Dependencies**: #1 (soul-outreach working), #5 (portfolio live)
- **Effort**: Ongoing

#### 7. campaign-consulting: Execute

- **Contacts**: 100-150 (target CTOs/VPs)
- **Done when**: Pipeline active, first discovery calls booked
- **Dependencies**: #1, #5 (parallel with #6)

#### 8. soul-blog: Publish 2-3 Technical Posts

- Post ideas:
  - "Building a Self-Healing AI OS on Raspberry Pi"
  - "Boundary Enforcement for Safe AI Agents"
  - "CARS: A Cost-Aware Metric for Local Model Selection"
- **Done when**: 2-3 posts published, linked from GitHub profile and LinkedIn
- **Dependencies**: #2, #4 (content from projects)

---

### P3: Product (Months 2-3)

Turn soul-outreach into a real product.

#### 9. outreach-analytics: Build Dashboard

- Usage stats, campaign performance, reply rates
- **Dependencies**: #1

#### 10. outreach-landing-page: Create & Deploy

- Marketing site explaining the product
- **Dependencies**: #1

#### 11. outreach-email-templates: Template System

- Pre-built templates for common use cases
- **Dependencies**: #1

#### 12. soul-outreach Phase 2: Product Polish

- Onboarding flow, documentation, error handling
- **Dependencies**: #9, #10, #11

---

### P4: Revenue (Months 3-6)

Monetize the product.

#### 13. outreach-stripe-billing: Payment Integration

- Free/Pro/Team tiers
- **Dependencies**: #12

#### 14. soul-outreach Phase 3: Open-Core Premium

- Separate MIT core from BSL premium features
- **Dependencies**: #13

---

### P5: Research (Months 3-6, parallel)

Build the research portfolio. Can run in parallel with P3/P4.

#### 15. soul-bench: Benchmark Framework + CARS

- Implement 10-task benchmark suite
- Run Claude baselines (Haiku, Sonnet, Opus)
- **Dependencies**: None

#### 16. soul-eval: Evaluation Framework

- Statistical comparison tools
- Claude baseline vs local model reports
- **Dependencies**: #15

#### 17. soul-moe Phase 1: Model Selection

- Screen model candidates
- Run CARS scoring
- First quantization experiments
- **Dependencies**: #15, #16

---

## Dependency Graph

```
P0 (Weeks 1-4)
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 1. outreach  │  │ 2. agents    │  │ 3. mesh      │
│    extract   │  │    extract   │  │    extract   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
P1 (Weeks 3-6)           v
┌──────────────┐  ┌──────────────┐
│ 4. moa-core  │  │ 5. brand     │
│    implement │  │    polish    │
└──────┬───────┘  └──────┬───────┘
       │                 │
P2 (Weeks 4-8)           v
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 6. campaign  │  │ 7. campaign  │  │ 8. blog      │
│    ai-labs   │  │    consulting│  │    posts     │
└──────────────┘  └──────────────┘  └──────────────┘

P3-P4 (Months 2-6)              P5 (Months 3-6, parallel)
┌──────────────┐                 ┌──────────────┐
│ 9-12.outreach│                 │ 15. bench    │
│    product   │                 │ 16. eval     │
│ 13-14.billing│                 │ 17. moe ph1  │
└──────────────┘                 └──────────────┘
```

## Reality Check

### What's strong
- soul-os is genuinely impressive — 6,700 lines with real architecture
- The three-repo ecosystem shows systems thinking at scale
- 31+ extractable projects from one person is a strong portfolio signal

### What needs attention
- soul-moa and soul-moe are 0% implemented — architecture plans only
- Plans without code don't impress hiring managers at top labs
- Need to pick 2-3 and actually build them before they have portfolio value
- CARS metric and MoA orchestrator are the most original contributions — need working code

### Critical path to job search
1. Extract soul-outreach (income tool)
2. Extract soul-agents + soul-mesh (portfolio)
3. Implement soul-moa-core (differentiator)
4. Polish GitHub + LinkedIn (visibility)
5. Execute campaign-ai-labs (outreach)

Everything else is secondary until the critical path is done.

## Current Sprint

_To be updated with active work items._
