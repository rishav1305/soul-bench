# soul-bench

> 10-task benchmark suite with the CARS efficiency metric.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Research Tool |
| Status | Scaffolded |
| Location | `~/soul/soul-moe/src/soul_moe/benchmarks/` |
| License | MIT |

## What It Is

A benchmark framework that evaluates AI models across 10 task categories derived from real soul-os workloads. Introduces the CARS (Cost-Aware Reasoning Score) metric that balances reasoning accuracy against resource cost — because a model that's 95% as good at 10% the cost is often the right choice.

## CARS Metric

```
CARS = Reasoning Accuracy / (VRAM_GB x Latency_s)
```

Higher is better. A model with 80% accuracy using 4GB VRAM in 1s scores 20.0 CARS. The same accuracy using 16GB in 3s scores 1.67 CARS. CARS reveals which models give the best bang-per-resource.

## 10 Task Categories

| # | Task | soul-os Source | Benchmark File |
|---|------|---------------|----------------|
| 1 | System health monitoring | brain/agents/system.yaml | system_health.py |
| 2 | Code generation & refactoring | claude_client.ask_agentic() | code_generation.py |
| 3 | Email draft generation | outreach/copywriter.py | email_drafting.py |
| 4 | Contact research & enrichment | outreach/researcher.py | contact_research.py |
| 5 | Knowledge base queries | tools/tool_executor._kb_tool() | knowledge_queries.py |
| 6 | Task planning & execution | autonomous_loop.py | task_planning.py |
| 7 | Content classification | claude_client.classify_untrusted() | classification.py |
| 8 | Campaign orchestration | outreach/outreach.py | campaign_orch.py |
| 9 | Reply classification | outreach/reply_ingest.py | reply_classif.py |
| 10 | Infrastructure management | agents/system.yaml | infra_mgmt.py |

### Key Design Decisions

- **Real workloads**: Benchmarks derived from actual soul-os usage, not synthetic tasks
- **Reproducible**: Fixed seed data, deterministic evaluation, version-pinned dependencies
- **CARS is the primary ranking metric**: Not just accuracy — cost-efficiency matters for local inference
- **Claude baselines**: Every benchmark includes Claude Haiku/Sonnet/Opus baselines for comparison

## Strategic Value

**CARS is an original research contribution.** A practical efficiency metric for model selection is directly relevant to any team deploying models in production. The benchmark suite shows research methodology — reproducible experiments, controlled baselines, statistical analysis.
