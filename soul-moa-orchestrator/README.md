# soul-moa-orchestrator

> Mixture of Agents (MoA) orchestration: proposer/aggregator layers for multi-model collaboration.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Framework |
| Status | Scaffolded |
| Location | `~/soul/soul-moa/src/soul_moa/moa/` |
| License | MIT |

## What It Is

Implementation of the Mixture of Agents architecture where multiple specialized models collaborate on complex tasks. Proposer models generate diverse candidate responses, then an aggregator model synthesizes the best answer. Configurable per task type — simple tasks use a single model, complex tasks use full MoA.

## Architecture

```
User Prompt
    |
    v
Task Router (classify: chat/code/reason)
    |
    ├── Simple task -> Single model (fast, cheap)
    |
    └── Complex task -> MoA Pipeline:
         |
         ├── Proposer Layer 1
         │   ├── Model A (e.g., Qwen3-30B) -> candidate 1
         │   ├── Model B (e.g., DeepSeek-V3) -> candidate 2
         │   └── Model C (e.g., Phi-4) -> candidate 3
         |
         ├── Proposer Layer 2 (optional)
         │   └── Refine candidates using each other's outputs
         |
         └── Aggregator
             └── Best model synthesizes final response from all candidates
```

### Key Design Decisions

- **MoA is optional**: Single model for simple tasks, MoA for complex (configurable per task_type)
- **Layer count configurable**: 1-3 proposer layers (more layers = better quality, higher latency)
- **Model diversity**: Proposers should be different architectures for diverse perspectives
- **Aggregator selection**: Best model (highest CARS score) does the final synthesis
- **Streaming**: Aggregator streams its response while proposers run in parallel

## Strategic Value

**The key innovation and strongest differentiator.** MoA paper implementation shows you can go from research paper to production system. This is the most impressive piece for AI lab interviews — demonstrates multi-agent orchestration, model routing, and production ML architecture.
