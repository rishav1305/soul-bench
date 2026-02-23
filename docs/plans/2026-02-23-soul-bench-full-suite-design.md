# soul-bench Full 10-Task Suite — Design

**Date:** 2026-02-23
**Block:** EXPLORE — soul-bench scaffolding
**Status:** Approved

## Goal

Extend soul-bench from 3 smoke-test prompts to a full 30-prompt benchmark suite across 10 task categories derived from real soul-os workloads. Add GPU benchmarking via free-tier Google Colab (T4).

## Decisions

- **All 10 categories adapted to single-turn** — Categories 2 (code gen), 5 (KB queries), 8 (campaign orchestration) simplified for single-turn llama-cli inference
- **3 prompts per category** — 30 total, ~30 min per model on CPU
- **Schema + key fields scoring** — JSON tasks scored as fraction (0.0-1.0) based on parse success + required keys + field validation
- **Modular prompt files** — one JSON per category, benchmark.py discovers all `prompts/*.json`
- **Free Colab with T4** — notebook targets free tier, 16GB VRAM, 3B-7B models

## Architecture

```
soul-bench/
  prompts/
    smoke-test.json              # existing 3-prompt smoke test
    01-system-health.json        # 3 prompts
    02-code-generation.json      # 3 prompts
    03-email-drafting.json       # 3 prompts
    04-contact-research.json     # 3 prompts
    05-knowledge-qa.json         # 3 prompts (adapted from KB queries)
    06-task-planning.json        # 3 prompts
    07-classification.json       # 3 prompts
    08-campaign-planning.json    # 3 prompts (adapted from orchestration)
    09-reply-classification.json # 3 prompts
    10-infra-management.json     # 3 prompts
  scripts/
    benchmark.py                 # extended: --prompts accepts dir or file
    scoring.py                   # new: all scoring methods
    setup-titan.sh               # existing
    colab_benchmark.py           # new: GPU variant with VRAM tracking
  tests/
    test_benchmark.py            # existing 23 tests
    test_scoring.py              # new: tests for all scoring methods
  notebooks/
    cars_benchmark.ipynb         # new: Colab notebook for T4 GPU runs
```

## 10 Task Categories

| # | Category | Adaptation for Single-Turn | Scoring Method |
|---|----------|---------------------------|----------------|
| 1 | System health monitoring | Give snapshot JSON, ask for structured diagnosis | `json_schema` |
| 2 | Code generation | "Write this function" (single function, no multi-turn) | `code_executes` |
| 3 | Email draft generation | Give template + contact data, expect JSON email | `json_schema` |
| 4 | Contact research | Give contact info, expect enrichment JSON | `json_schema` |
| 5 | Knowledge QA | Give context paragraph + question, expect answer with key facts | `contains_keywords` |
| 6 | Task planning | Give agent roster + task list, expect assignment JSON array | `json_schema` |
| 7 | Content classification | Give content + category list, expect single label | `exact_match_label` |
| 8 | Campaign planning | Give campaign goal, expect ordered CLI step list | `ordered_steps` |
| 9 | Reply classification | Give email with adversarial injection, expect label | `exact_match_label` |
| 10 | Infra management | Give emergency + snapshot JSON, expect diagnosis with actions | `contains_keywords` |

## Scoring Methods

All scoring functions live in `scripts/scoring.py`. Each returns a float 0.0-1.0.

| Method | Logic | Score Range |
|--------|-------|-------------|
| `json_schema` | Parse JSON + check required keys + validate field patterns | Fraction of checks passed |
| `contains_keywords` | Check response for expected keywords/phrases | Fraction of matches |
| `code_executes` | `compile()` + check function name present | 1.0 or 0.0 |
| `ordered_steps` | Extract numbered steps, verify ordering constraints | Fraction of constraints met |
| `exact_match_label` | Exact string match after strip/lower | 1.0 or 0.0 |
| `exact_match_number` | Last standalone number in response | 1.0 or 0.0 |
| `contains_function` | Substring check for function def | 1.0 or 0.0 |

## CARS Variants

```
CARS_RAM  = Accuracy / (Peak_RAM_GB x Latency_s)    # CPU runs
CARS_Size = Accuracy / (Model_Size_GB x Latency_s)  # Any hardware
CARS_VRAM = Accuracy / (Peak_VRAM_GB x Latency_s)   # GPU runs
```

VRAM captured via `nvidia-smi --query-gpu=memory.used` polled every 100ms.

## benchmark.py Changes

- `--prompts` accepts a directory (runs all `*.json` in sorted order) or single file
- Scoring functions imported from `scoring.py` instead of inline
- `--gpu` flag enables VRAM tracking via nvidia-smi
- Summary shows per-category accuracy breakdown
- Existing smoke-test behavior preserved (backward compatible)

## Colab Notebook

Self-contained `.ipynb` that:
1. Installs llama.cpp with CUDA (`cmake -DGGML_CUDA=ON`)
2. Downloads models from HuggingFace
3. Runs benchmark.py with `--gpu` flag
4. Captures VRAM via nvidia-smi
5. Produces comparison: CPU (titan-pc) vs GPU (T4)

## Prompt JSON Schema

Each prompt file follows this schema:
```json
[
  {
    "id": "system-health-01",
    "task": "system_health",
    "prompt": "...",
    "expected_answer": "..." or {"key": "value"},
    "scoring": "json_schema",
    "scoring_config": {
      "required_keys": ["findings", "severity", "recommended_actions"],
      "field_checks": {"severity": ["low", "medium", "high", "critical"]}
    }
  }
]
```

The `scoring_config` field is optional and provides parameters to the scoring function.
