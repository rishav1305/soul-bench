# soul-eval

> Model evaluation framework with Claude baselines and statistical comparison.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Research Tool |
| Status | Scaffolded |
| Location | `~/soul/soul-moe/src/soul_moe/evaluation/` |
| License | MIT |

## What It Is

An evaluation framework that compares local models against Claude baselines (Haiku, Sonnet, Opus) across all 10 task categories. Provides statistical significance tests, accuracy retention reports, and CARS efficiency comparisons.

## Evaluation Pipeline

```
Model under test + Claude baseline
    |
    v
Run both on same benchmark dataset (soul-bench)
    |
    v
Statistical comparison:
    - Per-task accuracy (with confidence intervals)
    - Overall accuracy retention (% of Claude baseline)
    - CARS efficiency comparison
    - Paired t-test / Wilcoxon signed-rank test
    |
    v
Report: "Model X retains 87% of Claude Sonnet accuracy at 12x CARS efficiency"
```

### Key Features

- **Claude baselines**: Every evaluation includes Claude Haiku/Sonnet/Opus as reference points
- **Statistical rigor**: Confidence intervals, significance tests, not just point estimates
- **Per-task breakdown**: Some models are better at code, others at reasoning — see where
- **Accuracy retention**: The key metric for deploy gate decisions (>=80% required)

## Strategic Value

Evaluation methodology shows research rigor. Statistical comparison (not just "it seems good") demonstrates the kind of analysis expected in ML research roles.
