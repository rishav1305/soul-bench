# soul-select

> Model candidate screening with CARS scoring and leaderboard.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Research Tool |
| Status | Scaffolded |
| Location | `~/soul/soul-moe/src/soul_moe/selection/` |
| License | MIT |

## What It Is

A model selection tool that screens open-source model candidates, runs them through soul-bench benchmarks, scores them with CARS, and maintains a leaderboard. Helps answer: "Which model gives the best accuracy-per-resource for my specific task mix?"

## Pipeline

```
Candidate List (HuggingFace models)
    |
    v
Filter (architecture, size, license, MoE support)
    |
    v
Benchmark (soul-bench, 10 tasks)
    |
    v
CARS Scoring (accuracy / VRAM x latency)
    |
    v
Leaderboard (ranked by CARS per tier)
    |
    v
Top candidates -> soul-quant (quantization)
```

### Model Tiers

| Tier | Target VRAM | Target Latency | Use Cases |
|------|------------|---------------|-----------|
| Chat | <4 GB | <1s P95 | Tasks 5, 7, 9 (fast, cheap) |
| Code | <16 GB | <3s P95 | Tasks 2, 3, 4, 8 (balanced) |
| Reason | <32 GB | <5s P95 | Tasks 1, 6, 10 (complex) |

## Strategic Value

Model selection tooling shows practical ML engineering — not just training models but choosing the right ones for production constraints.
