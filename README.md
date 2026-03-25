# soul-bench

> **52 LLMs. 7 providers. 30 prompts. 10 task categories. One metric that matters: CARS.**

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Research Tool / LLM Benchmark |
| Status | **52 cloud models + 2 local models benchmarked** |
| Prompts | 30 structured (10 categories x 3 prompts) |
| Scoring | Dual: strict (exact format) + relaxed (correct answer) |
| Key metric | CARS (Cost-Adjusted Response Score) |
| License | MIT |

## Cloud Benchmark Results (March 2026)

**52 models** from **7 providers** evaluated on 30 structured-output prompts via LiteLLM.

### Top 10 by Strict Accuracy

| # | Model | Provider | Strict % | Relaxed % | Format Tax | Latency | CARS_Size |
|---|-------|----------|----------|-----------|------------|---------|-----------|
| 1 | **o3** | OpenAI | **85.0%** | 85.0% | **0pp** | 4.72s | 0.0009 |
| 2 | **gpt-oss-20b** | OpenAI | 79.4% | 82.7% | 3.3pp | 1.61s | **0.0257** |
| 3 | **gpt-5.2** | OpenAI | 78.2% | 91.5% | 13.3pp | 2.69s | 0.0007 |
| 4 | **gpt-4o** | OpenAI | 77.8% | 87.8% | 10.0pp | 3.00s | 0.0013 |
| 5 | **gpt-3.5-turbo** | OpenAI | 75.7% | 75.7% | 0pp | 1.50s | 0.0252 |
| 6 | **claude-sonnet-4** | Anthropic | 73.4% | **93.4%** | 20.0pp | 4.72s | 0.0022 |
| 7 | **gpt-4.1-mini** | OpenAI | 72.0% | 85.3% | 13.3pp | 2.06s | 0.0117 |
| 8 | **gpt-4-turbo** | OpenAI | 71.5% | 84.8% | 13.3pp | 8.83s | 0.0005 |
| 9 | **claude-3-5-sonnet-v2** | Anthropic | 71.2% | 91.2% | 20.0pp | 3.71s | 0.0027 |
| 10 | **gemini-3-flash-no-reasoning** | Google | 69.7% | 89.7% | 20.0pp | 4.94s | 0.0047 |

Full results (all 52 models): [`results/cloud-2026-03-24/`](results/cloud-2026-03-24/)

### Key Findings

1. **o3 is #1 strict (85.0%) with zero format tax** — the only reasoning model that follows format instructions perfectly
2. **A $0.002 model beats GPT-4o:** gpt-oss-20b (20B) scores 79.4% vs GPT-4o's 77.8% at 17x better efficiency
3. **Format Tax averages 14pp** across all 52 models — models know the answer but can't follow format instructions
4. **Reasoning HURTS structured tasks:** Gemini 2.5 Flash scores 2x worse with reasoning enabled (33.6% vs 66.8%)
5. **Generation regression is real:** GPT-5 < GPT-3.5 Turbo (-19pp), Gemini 2.5 Pro < 2.0 Flash (-32pp)

### Local Benchmark Results (Feb 2026, CPU/GPU)

| Model | Size | Accuracy | Latency | CARS_Size |
|-------|------|----------|---------|-----------|
| **Qwen2.5-3B-Instruct Q4_K_M** | 1.96 GB | **78.5%** | **2.06s** | **0.1948** |
| Phi-3.5-mini-instruct Q4_K_M | 2.23 GB | 62.4% | 3.89s | 0.0721 |

Full local results in [`results/`](results/)

### Category Accuracy

| Category | Phi-3.5-mini | Qwen2.5-3B |
|----------|-------------|------------|
| System health | 66.7% | **100%** |
| Code generation | **100%** | **100%** |
| Email drafting | **66.7%** | 33.3% |
| Contact research | **100%** | **100%** |
| Knowledge QA | **86.7%** | **86.7%** |
| Task planning | 33.3% | **50%** |
| Classification | 0% | **100%** |
| Campaign planning | **100%** | 60% |
| Reply classification | 33.3% | **66.7%** |
| Infra management | **66.7%** | **66.7%** |
| Reasoning | 0% | **100%** |
| Code (smoke) | **100%** | **100%** |

## What It Is

A benchmark framework that evaluates local LLMs across 10 task categories derived from real soul-os workloads. Introduces the CARS (Cost-Aware Reasoning Score) metric that balances accuracy against resource cost -- because a model that's 95% as good at 10% the cost is often the right choice.

## CARS Metric

Three variants for different deployment targets:

```
CARS_RAM  = Accuracy / (Peak_RAM_GB x Latency_s)     # CPU runs
CARS_Size = Accuracy / (Model_Size_GB x Latency_s)    # Any hardware (reproducible)
CARS_VRAM = Accuracy / (Peak_VRAM_GB x Latency_s)     # GPU runs (--gpu flag)
```

Higher is better. CARS reveals which models give the best bang-per-resource.

## 10 Task Categories (30 prompts)

| # | Category | Prompts | Scoring Method | What It Tests |
|---|----------|---------|---------------|---------------|
| 1 | System health | 3 | `json_schema` | JSON diagnosis from system snapshots |
| 2 | Code generation | 3 | `code_executes` | Python functions that compile and run |
| 3 | Email drafting | 3 | `json_schema` | Structured email from template + contact data |
| 4 | Contact research | 3 | `json_schema` | Enrichment JSON from name + company |
| 5 | Knowledge QA | 3 | `contains_keywords` | Factual extraction from provided context |
| 6 | Task planning | 3 | `json_schema` | Task assignment from agent roster |
| 7 | Classification | 3 | `exact_match_label` | Single-label content classification |
| 8 | Campaign planning | 3 | `ordered_steps` | Correct CLI pipeline step ordering |
| 9 | Reply classification | 3 | `exact_match_label` | Email reply intent (includes adversarial injection test) |
| 10 | Infra management | 3 | `contains_keywords` | Infrastructure diagnosis with required terms |

Plus 3 smoke test prompts (reasoning, code, classification).

## 7 Scoring Methods

All return fractional scores (0.0 to 1.0):

| Method | Type | Logic |
|--------|------|-------|
| `score_json_schema` | Fractional | Parse JSON, check required keys + field values |
| `score_contains_keywords` | Fractional | Case-insensitive keyword matching |
| `score_code_executes` | Binary | `compile()` + function name check |
| `score_ordered_steps` | Fractional | Verify step ordering constraints |
| `score_exact_match_label` | Binary | Exact case-insensitive label match |
| `score_exact_match_number` | Binary | Last number in response matches expected |
| `score_contains_function` | Binary | Function definition substring check |

## Quick Start

### CPU (local machine with llama.cpp installed)

```bash
# Run full suite
python3 scripts/benchmark.py --prompts prompts/ --results-dir results/

# Run single category
python3 scripts/benchmark.py --prompts prompts/01-system-health.json

# Run tests
python3 -m pytest tests/ -v  # 39 tests
```

### GPU (Google Colab, free tier T4)

```bash
# Option 1: Use the notebook
# Open notebooks/cars_benchmark.ipynb in Colab, enable T4 GPU, run all cells

# Option 2: Use llama-cpp-python (no compilation needed)
pip install 'llama-cpp-python>=0.3' \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124
python3 scripts/benchmark.py --prompts prompts/ --results-dir results/ --gpu
```

## Project Structure

```
soul-bench/
  prompts/
    smoke-test.json          # 3 smoke test prompts
    01-system-health.json    # 3 prompts per category
    ...
    10-infra-management.json
  scripts/
    benchmark.py             # Main benchmark runner (434 lines)
    scoring.py               # 7 scoring methods (153 lines)
    colab_setup.py           # Google Colab setup script
    setup-titan.sh           # Local machine setup
  notebooks/
    cars_benchmark.ipynb     # Colab notebook with GPU support
  results/
    BASELINE.md              # CPU baseline (titan-pc)
    2026-02-22-*.json        # CPU benchmark results
    2026-02-24-gpu-*.json    # GPU benchmark results (Colab T4)
    *.md                     # Detailed reports
  tests/
    test_scoring.py          # 25 tests for scoring methods
    test_benchmark.py        # 14 tests for benchmark runner
```

## Reports

- [CARS Baseline Report (Feb 22)](results/2026-02-22-cars-baseline-report.md) -- Day 1, CPU-only, 3 smoke test prompts
- [Full Suite Report (Feb 23-24)](results/2026-02-23-soul-bench-full-suite-report.md) -- 33 prompts, 10 categories, GPU results

## Design Decisions

- **Real workloads**: All 10 categories derived from actual soul-os production tasks
- **Reproducible**: Fixed prompts, deterministic scoring, temperature=0.0
- **Fractional scoring**: Partial credit (0.0-1.0) instead of binary pass/fail
- **Adversarial testing**: Prompt injection resistance test in reply classification
- **CARS is the primary ranking metric**: Not just accuracy -- cost-efficiency matters for local inference
