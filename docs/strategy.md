# Soul AI — Strategy

## Product Positioning

**External**: "Soul AI" — one integrated product. An AI that runs on your device, learns your workflows, and works across devices.

**Internal**: 31+ modular projects with independent release cycles.

**Principle**: Sell the meal, not the ingredients. Nobody buys "soul-mesh" from an unknown brand. They buy "an AI that works offline and syncs across devices."

## Why NOT the AWS Model

| Factor | AWS (works) | Solo founder (doesn't work) |
|--------|-------------|---------------------------|
| Engineering team | 100,000+ | 1 person |
| Support per product | Dedicated teams | You, stretched thin |
| Sales cycle | Enterprise sales org | You cold-emailing |
| Time to maintain 31 products | Distributed | All on you |
| Brand trust to sell infra | Decades | Zero (today) |

31 products = 31 half-baked products = $0 revenue.

## Decision Matrix

| Approach | Revenue Potential | Probability of Success | Expected Value |
|----------|-------------------|----------------------|----------------|
| 31 separate products | High if all succeed | <1% | Very low |
| 5-8 products (mini-AWS) | Medium | ~5% | Low |
| 1 integrated product | Medium-High | ~25% | Highest |
| **1 product + consulting** | **High** | **~40%** | **Highest** |

## Licensing Strategy

### Open Source (MIT) — Portfolio / Credibility

Build reputation, attract employers/clients, enable community contributions.

| Project | Why It Impresses | Target Audience |
|---------|-----------------|-----------------|
| soul-mesh | Distributed systems, hub election, WebSocket sync | Anthropic, Google |
| soul-moa-core | Clean agent SDK design, boundary enforcement | AI engineers |
| soul-moa-orchestrator | MoA paper implementation, novel architecture | All AI labs |
| soul-moa-failsafe | Production resilience patterns | Senior eng roles |
| soul-bench | CARS metric — original research contribution | AI researchers |
| soul-quant | Quantization pipeline shows ML depth | Google, Meta |
| soul-tune | Fine-tuning pipeline shows training competence | OpenAI, Anthropic |
| soul-agents | YAML-configured agents with code-level boundaries | AI safety roles |
| soul-auth | Token family replay detection — non-trivial security | Security roles |
| soul-heal | Self-healing with hysteresis — systems thinking | SRE/Platform roles |

### Private — Monetize

| Project | Revenue Model |
|---------|--------------|
| soul-outreach (premium features) | SaaS subscription |
| soul-consult | Internal consulting pipeline tool |
| soul-knowledge | Vertical knowledge base (CVE, security) |
| soul-cloud | PaaS — container provisioning |
| soul-content | AI content generation |
| soul-os (integrated) | The full product — license/sell |
| All outreach-* premium features | Part of soul-outreach SaaS |
| Campaigns | Not code — execution projects |
| soul-brand | Not code — brand assets |

### Dual License (Open Core + Premium)

| Open Part (MIT) | Closed Part (BSL) |
|-----------------|-------------------|
| soul-outreach core (import, enrich, draft, review, send) | Premium features (analytics, A/B, segmentation, billing) |
| soul-bench framework | Benchmark results & trained models |
| soul-quant pipeline | Quantized model weights |
| soul-tune pipeline | Fine-tuned adapters |

## Revenue Model

### Phase 1: Consulting + Portfolio (NOW -> 3 months)

- Open source the impressive infra (soul-mesh, soul-agents, soul-moa-core)
- Use portfolio to land consulting contracts at $150-300/hr
- Revenue target: $10-20K/month
- This funds everything else

| Model | Expected Revenue | Time to First $ |
|-------|-----------------|-----------------|
| Consulting/Freelance | $150-300/hr | 2-4 weeks |
| Contract work | $10-30K/month | 1-2 months |

### Phase 2: One SaaS Product (3-6 months)

Pick ONE: soul-outreach as standalone product.

| Tier | Price | Includes |
|------|-------|---------|
| Free | $0 | Core features, 1 workspace, 10 templates |
| Pro | $29/mo | Unlimited campaigns, analytics, API access |
| Team | $99/mo | Multi-workspace, collaboration, priority support |
| Self-hosted | Open source | Core features, BYOI (bring your own infrastructure) |

Revenue target: $2-5K MRR from early adopters.

### Phase 3: Expand Based on Data (6-12 months)

- See which features customers actually pay for
- THEN consider splitting or expanding
- Potential: managed soul-os cloud at soul-os.app

## Target Audiences

### AI Lab Hiring Managers

What they see: production AI systems, not demos.

Key signals:
- Architects production AI systems using AI coding tools (31 projects, 9,700 lines)
- CARS metric (original research)
- Boundary enforcement (AI safety thinking)
- Hub election algorithm (distributed systems architecture)
- Claude Code power user: custom agents, hooks, CLAUDE.md, commands

Key repos: soul-os, soul-mesh, soul-agents, soul-moa

### CTOs / VP Engineering (Consulting)

What they see: someone who builds AND ships production AI.

Value prop: "I architect and ship production AI systems 10x faster by combining 6 years of data engineering with AI coding tools."

Consulting packages (from soul-os consulting pipeline):

| Package | Focus | Target |
|---------|-------|--------|
| Shield | Risk, Compliance, Security | Legal, Healthcare, Finance |
| Magnet | Customer Experience, Retention | SaaS, Subscription |
| Engine | Innovation, R&D | R&D-heavy orgs |
| Brain | Knowledge Management | Enterprise |

### Developers (Product Users)

What they see: useful open source tools.

Key repos: soul-outreach (self-hosted), soul-moa-core (agent SDK), soul-mesh (networking).

Value prop: Self-hosted, privacy-first alternatives to SaaS tools.

## Meta-Demonstration

The outreach campaign IS the portfolio proof:

"This email was sent using my own AI outreach tool."

- soul-outreach drafted the email -> proves the product works
- soul-agents managed the agent -> proves boundary enforcement
- soul-os orchestrated everything -> proves the platform
- The email itself is the demo
