# CARS Baseline Setup — Design

**Date:** 2026-02-22
**Block:** EXPLORE (Block 2)
**Goal:** Install llama.cpp on titan-pc, download 2 models, run smoke tests, document hardware baseline

## Hardware

- **Machine:** titan-pc (192.168.0.113)
- **CPU:** Intel i5-8400 (6 cores, no HT, 2.80GHz)
- **RAM:** 7.6GB total, ~5.7GB available
- **GPU:** None (Intel UHD 630 iGPU only)
- **Disk:** 841GB free
- **OS:** Ubuntu 24.04, kernel 6.14

## Architecture

```
soul-bench/
  scripts/
    setup-titan.sh           # Install llama.cpp + download models
    benchmark.py             # Run prompts, capture timing/memory, output JSON
  prompts/
    smoke-test.json          # 3 prompts: reasoning, code, classification
  results/
    YYYY-MM-DD-<model>.json  # Structured results per run
```

## Components

### 1. Setup Script (setup-titan.sh)

Runs on titan-pc:
- Install build deps (cmake, g++, git)
- Clone and compile llama.cpp from source (CPU-only, no CUDA)
- Download 2 GGUF models from HuggingFace:
  - Phi-3.5-mini-instruct-Q4_K_M.gguf (~2.4GB)
  - Qwen2.5-3B-Instruct-Q4_K_M.gguf (~2.0GB)
- Verify: `llama-cli --version` works

### 2. Benchmark Runner (benchmark.py)

Runs on titan-pc (Python 3.11+):
- Reads prompts from prompts/smoke-test.json
- For each model x prompt:
  - Launches llama-cli subprocess with the prompt
  - Measures wall-clock latency via time.perf_counter
  - Measures peak RSS memory via /proc/[pid]/status (VmHWM)
  - Captures output text, token count
- Records model file size on disk
- Outputs structured JSON to results/

### 3. Smoke Test Prompts (smoke-test.json)

Three prompts:
1. **Reasoning:** "A farmer has 17 sheep. All but 9 die. How many are left? Explain step by step."
2. **Code:** "Write a Python function that checks if a string is a palindrome. Include docstring."
3. **Classification:** "Classify this email as spam or not-spam: 'Congratulations! You've won a free iPhone. Click here to claim.'"

### 4. Output Format

```json
{
  "model": "phi-3.5-mini-instruct-Q4_K_M",
  "timestamp": "2026-02-22T14:30:00",
  "hardware": {"cpu": "i5-8400", "cores": 6, "ram_gb": 7.6},
  "model_size_gb": 2.4,
  "results": [
    {
      "task": "reasoning",
      "prompt": "...",
      "response": "...",
      "latency_s": 12.3,
      "peak_ram_mb": 3200,
      "tokens_generated": 85,
      "tokens_per_second": 6.9
    }
  ],
  "cars_ram": 0.027,
  "cars_size": 0.034
}
```

## CARS Metric Adaptation

No discrete GPU, so two variants tracked:
- `CARS_RAM = Accuracy / (PeakRAM_GB x Latency_s)` — runtime resource cost
- `CARS_Size = Accuracy / (ModelSize_GB x Latency_s)` — static resource cost

Accuracy scored manually for smoke test (binary correct/incorrect). Automated scoring comes with full soul-bench implementation.

## Models

| Model | Params | Quant | Size | Source |
|-------|--------|-------|------|--------|
| Phi-3.5-mini-instruct | 3.8B | Q4_K_M | ~2.4GB | HuggingFace |
| Qwen2.5-3B-Instruct | 3B | Q4_K_M | ~2.0GB | HuggingFace |

## Decisions

- **CPU-only inference** — no GPU available, llama.cpp compiled without CUDA
- **Track both RAM and model size** — decide which CARS variant is more useful after seeing data
- **2 models** — richer comparison for same effort
- **3 smoke test prompts** — enough to validate setup and get initial timing, not a full benchmark
