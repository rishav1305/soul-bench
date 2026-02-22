# soul-moa-core

## Overview
Minimal working Mixture of Agents implementation — the STRONGEST portfolio differentiator.

## Status
**To Implement** | From soul-moa scaffold

## Description
soul-moa-core is the core implementation of the Mixture of Agents (MoA) pattern. It includes Agent SDK primitives and the proposer/aggregator pattern where multiple diverse agents generate solutions that are then synthesized into a superior response.

## Architecture
```
Input Query
    |
    v
[Proposer 1] [Proposer 2] [Proposer 3]  (diverse models/prompts)
    |              |              |
    v              v              v
[         Aggregator Agent          ]    (synthesizes best response)
    |
    v
Final Response
```

## Key Features
- Agent SDK primitives (base agent, tool use, message passing)
- Proposer agent pool with diverse configurations
- Aggregator agent with synthesis strategies
- Quality comparison metrics
- Working demo showing MoA outperforming individual agents

## Why This Is the Strongest Differentiator
- **Original research contribution** — not just using APIs
- **Novel architecture** — demonstrates system design thinking
- **Quantifiable results** — can show MoA beats individual models
- **Interview talking point** — deep technical discussion material
- **Blog post**: "Implementing Mixture of Agents for Production Systems"

## Timeline
Sprint 2 (Week 3-4), parallel with soul-outreach Phase 2.
