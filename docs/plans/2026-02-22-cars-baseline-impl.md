# CARS Baseline Setup — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Install llama.cpp on titan-pc (CPU-only i5-8400), download Phi-3.5-mini and Qwen2.5-3B GGUF models, run 3 smoke test prompts, capture timing/memory metrics, output structured JSON results.

**Architecture:** Shell script provisions titan-pc (llama.cpp + models). Python benchmark runner executes prompts via subprocess, captures latency/memory/tokens, writes JSON. All scripts live in `soul-bench/scripts/`, prompts in `soul-bench/prompts/`, results in `soul-bench/results/`.

**Tech Stack:** Bash, Python 3.12 (stdlib only — subprocess, json, time, pathlib), llama.cpp (CPU build), GGUF Q4_K_M models from HuggingFace.

**Target machine:** titan-pc (192.168.0.113, SSH alias `titan-pc`, i5-8400 6-core, 7.6GB RAM, no GPU, Ubuntu 24.04, Python 3.12)

---

## Task 1: Create project structure and smoke test prompts

**Files:**
- Create: `soul-bench/scripts/` (directory)
- Create: `soul-bench/prompts/smoke-test.json`
- Create: `soul-bench/results/.gitkeep`

**Step 1: Create directories**

```bash
mkdir -p ~/soul/soul-bench/scripts ~/soul/soul-bench/prompts ~/soul/soul-bench/results
touch ~/soul/soul-bench/results/.gitkeep
```

**Step 2: Write smoke-test.json**

Create `soul-bench/prompts/smoke-test.json`:

```json
[
  {
    "id": "reasoning-01",
    "task": "reasoning",
    "prompt": "A farmer has 17 sheep. All but 9 die. How many are left? Think step by step, then give the final answer as a single number.",
    "expected_answer": "9",
    "scoring": "exact_match_number"
  },
  {
    "id": "code-01",
    "task": "code",
    "prompt": "Write a Python function called `is_palindrome` that takes a string and returns True if it is a palindrome (ignoring case and spaces), False otherwise. Include a docstring. Output only the function, no explanation.",
    "expected_answer": "def is_palindrome",
    "scoring": "contains_function"
  },
  {
    "id": "classification-01",
    "task": "classification",
    "prompt": "Classify this email as exactly one of: SPAM or NOT_SPAM. Reply with only the label, nothing else.\n\nEmail: \"Congratulations! You've won a free iPhone 15 Pro! Click here immediately to claim your prize before it expires. Limited time offer!\"",
    "expected_answer": "SPAM",
    "scoring": "exact_match_label"
  }
]
```

**Step 3: Commit**

```bash
cd ~/soul/soul-bench
git init
git add prompts/smoke-test.json results/.gitkeep
git commit -m "feat: add smoke test prompts and project structure"
```

---

## Task 2: Write setup-titan.sh

**Files:**
- Create: `soul-bench/scripts/setup-titan.sh`

**Step 1: Write the setup script**

Create `soul-bench/scripts/setup-titan.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# CARS Baseline — titan-pc setup script
# Installs llama.cpp (CPU-only) and downloads GGUF models
# Run ON titan-pc: bash setup-titan.sh

LLAMA_DIR="$HOME/llama.cpp"
MODELS_DIR="$HOME/models"

echo "=== CARS Baseline Setup ==="
echo "Target: $(hostname) — $(uname -m)"
echo ""

# 1. Install build dependencies
echo "--- Installing build dependencies ---"
sudo apt-get update -qq
sudo apt-get install -y -qq cmake build-essential curl wget

# 2. Clone and build llama.cpp (CPU-only)
if [ -d "$LLAMA_DIR" ]; then
    echo "--- llama.cpp already cloned, pulling latest ---"
    cd "$LLAMA_DIR" && git pull
else
    echo "--- Cloning llama.cpp ---"
    git clone https://github.com/ggml-org/llama.cpp.git "$LLAMA_DIR"
fi

echo "--- Building llama.cpp (CPU-only) ---"
cd "$LLAMA_DIR"
cmake -B build -DGGML_CUDA=OFF -DGGML_METAL=OFF
cmake --build build --config Release -j$(nproc)

# Verify build
if [ ! -f "$LLAMA_DIR/build/bin/llama-cli" ]; then
    echo "ERROR: llama-cli not found after build"
    exit 1
fi
echo "llama-cli built: $LLAMA_DIR/build/bin/llama-cli"

# Add to PATH for this session
export PATH="$LLAMA_DIR/build/bin:$PATH"
echo ""
echo "Add to your .bashrc:"
echo "  export PATH=\"$LLAMA_DIR/build/bin:\$PATH\""
echo ""

# 3. Download models
mkdir -p "$MODELS_DIR"

# Phi-3.5-mini-instruct Q4_K_M (~2.4GB)
PHI_URL="https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF/resolve/main/Phi-3.5-mini-instruct-Q4_K_M.gguf"
PHI_FILE="$MODELS_DIR/Phi-3.5-mini-instruct-Q4_K_M.gguf"
if [ -f "$PHI_FILE" ]; then
    echo "--- Phi-3.5-mini already downloaded ---"
else
    echo "--- Downloading Phi-3.5-mini-instruct Q4_K_M (~2.4GB) ---"
    wget -q --show-progress -O "$PHI_FILE" "$PHI_URL"
fi

# Qwen2.5-3B-Instruct Q4_K_M (~2.0GB)
QWEN_URL="https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf"
QWEN_FILE="$MODELS_DIR/qwen2.5-3b-instruct-q4_k_m.gguf"
if [ -f "$QWEN_FILE" ]; then
    echo "--- Qwen2.5-3B already downloaded ---"
else
    echo "--- Downloading Qwen2.5-3B-Instruct Q4_K_M (~2.0GB) ---"
    wget -q --show-progress -O "$QWEN_FILE" "$QWEN_URL"
fi

# 4. Verify
echo ""
echo "=== Verification ==="
llama-cli --version 2>&1 || echo "(version flag may not be supported — checking binary exists)"
ls -lh "$MODELS_DIR"/*.gguf
echo ""
echo "=== Setup complete ==="
echo "Models directory: $MODELS_DIR"
echo "llama-cli: $LLAMA_DIR/build/bin/llama-cli"

# 5. Quick smoke test — run a tiny prompt to verify inference works
echo ""
echo "--- Quick inference smoke test ---"
echo "Running: 'Hello, what is 2+2?' with Phi-3.5-mini..."
llama-cli -m "$PHI_FILE" -p "<|user|>\nWhat is 2+2? Answer with just the number.<|end|>\n<|assistant|>\n" -n 32 --no-display-prompt 2>/dev/null
echo ""
echo "If you see a response above, inference is working."
```

**Step 2: Make executable and commit**

```bash
chmod +x ~/soul/soul-bench/scripts/setup-titan.sh
cd ~/soul/soul-bench
git add scripts/setup-titan.sh
git commit -m "feat: add titan-pc setup script for llama.cpp and model downloads"
```

---

## Task 3: Write benchmark.py runner

**Files:**
- Create: `soul-bench/scripts/benchmark.py`

**Step 1: Write the benchmark runner**

Create `soul-bench/scripts/benchmark.py`:

```python
#!/usr/bin/env python3
"""CARS Baseline Benchmark Runner.

Runs smoke test prompts against GGUF models via llama-cli,
captures latency, peak memory, and token throughput.
Outputs structured JSON to results/.

Usage (on titan-pc):
    python3 benchmark.py
    python3 benchmark.py --models ~/models/Phi-3.5-mini-instruct-Q4_K_M.gguf
    python3 benchmark.py --prompts ../prompts/smoke-test.json
"""

import argparse
import json
import os
import platform
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
DEFAULT_PROMPTS = SCRIPT_DIR.parent / "prompts" / "smoke-test.json"
DEFAULT_MODELS_DIR = Path.home() / "models"
DEFAULT_RESULTS_DIR = SCRIPT_DIR.parent / "results"
LLAMA_CLI = Path.home() / "llama.cpp" / "build" / "bin" / "llama-cli"

# Chat templates per model family
CHAT_TEMPLATES = {
    "phi": {
        "prefix": "<|user|>\n",
        "suffix": "<|end|>\n<|assistant|>\n",
    },
    "qwen": {
        "prefix": "<|im_start|>user\n",
        "suffix": "<|im_end|>\n<|im_start|>assistant\n",
    },
}


def get_hardware_info() -> dict:
    """Collect hardware info from the current machine."""
    info = {
        "hostname": platform.node(),
        "cpu": "unknown",
        "cores": os.cpu_count() or 0,
        "ram_gb": 0.0,
    }
    # CPU model
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    info["cpu"] = line.split(":")[1].strip()
                    break
    except OSError:
        pass
    # Total RAM
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    info["ram_gb"] = round(kb / 1024 / 1024, 1)
                    break
    except OSError:
        pass
    return info


def detect_model_family(model_path: str) -> str:
    """Detect chat template family from model filename."""
    name = Path(model_path).name.lower()
    if "phi" in name:
        return "phi"
    if "qwen" in name:
        return "qwen"
    return "qwen"  # default to chatml-style


def format_prompt(raw_prompt: str, model_family: str) -> str:
    """Wrap raw prompt in the model's chat template."""
    tmpl = CHAT_TEMPLATES[model_family]
    return f"{tmpl['prefix']}{raw_prompt}{tmpl['suffix']}"


def get_model_size_gb(model_path: str) -> float:
    """Get model file size in GB."""
    return round(os.path.getsize(model_path) / (1024**3), 3)


def run_prompt(model_path: str, prompt: str, max_tokens: int = 256) -> dict:
    """Run a single prompt through llama-cli and capture metrics."""
    model_family = detect_model_family(model_path)
    formatted = format_prompt(prompt, model_family)

    cmd = [
        str(LLAMA_CLI),
        "-m", model_path,
        "-p", formatted,
        "-n", str(max_tokens),
        "--no-display-prompt",
        "--log-disable",
    ]

    start = time.perf_counter()
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Monitor peak memory via /proc/[pid]/status
    peak_rss_kb = 0
    pid = proc.pid
    status_path = f"/proc/{pid}/status"

    while proc.poll() is None:
        try:
            with open(status_path) as f:
                for line in f:
                    if line.startswith("VmHWM:"):
                        hwm_kb = int(line.split()[1])
                        peak_rss_kb = max(peak_rss_kb, hwm_kb)
                        break
        except (OSError, ProcessLookupError):
            pass
        time.sleep(0.1)

    # Final check
    try:
        with open(status_path) as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    hwm_kb = int(line.split()[1])
                    peak_rss_kb = max(peak_rss_kb, hwm_kb)
                    break
    except (OSError, ProcessLookupError):
        pass

    elapsed = time.perf_counter() - start
    stdout = proc.stdout.read().strip() if proc.stdout else ""
    stderr = proc.stderr.read().strip() if proc.stderr else ""

    # Try to extract token count from stderr (llama.cpp prints stats there)
    tokens_generated = 0
    tokens_per_second = 0.0
    # llama.cpp prints: "llama_perf_sampler_print:    sampling time = ... ms / N runs"
    # and: "llama_perf_context_print:        eval time = ... ms / N tokens (... ms per token, ... tokens per second)"
    eval_match = re.search(
        r"eval time\s*=\s*[\d.]+\s*ms\s*/\s*(\d+)\s*tokens\s*\([\d.]+\s*ms per token,\s*([\d.]+)\s*tokens per second\)",
        stderr,
    )
    if eval_match:
        tokens_generated = int(eval_match.group(1))
        tokens_per_second = float(eval_match.group(2))

    return {
        "response": stdout,
        "latency_s": round(elapsed, 2),
        "peak_ram_mb": round(peak_rss_kb / 1024, 1),
        "tokens_generated": tokens_generated,
        "tokens_per_second": round(tokens_per_second, 2),
        "stderr_snippet": stderr[-500:] if stderr else "",
    }


def score_result(response: str, prompt_data: dict) -> float:
    """Simple scoring for smoke test prompts. Returns 0.0 or 1.0."""
    scoring = prompt_data.get("scoring", "")
    expected = prompt_data.get("expected_answer", "")
    resp_lower = response.lower().strip()

    if scoring == "exact_match_number":
        return 1.0 if expected in response else 0.0
    elif scoring == "contains_function":
        return 1.0 if expected in response else 0.0
    elif scoring == "exact_match_label":
        return 1.0 if expected.lower() in resp_lower else 0.0
    return 0.0


def run_benchmark(model_path: str, prompts: list[dict]) -> dict:
    """Run all prompts against a model and return structured results."""
    model_name = Path(model_path).stem
    model_size = get_model_size_gb(model_path)
    hardware = get_hardware_info()

    print(f"\n{'='*60}")
    print(f"Model: {model_name}")
    print(f"Size:  {model_size} GB")
    print(f"{'='*60}")

    results = []
    total_accuracy = 0.0

    for i, prompt_data in enumerate(prompts, 1):
        task = prompt_data["task"]
        prompt_id = prompt_data["id"]
        print(f"\n  [{i}/{len(prompts)}] {prompt_id} ({task})...")

        metrics = run_prompt(model_path, prompt_data["prompt"])
        accuracy = score_result(metrics["response"], prompt_data)
        total_accuracy += accuracy

        result = {
            "id": prompt_id,
            "task": task,
            "prompt": prompt_data["prompt"],
            "expected": prompt_data.get("expected_answer", ""),
            "response": metrics["response"],
            "accuracy": accuracy,
            "latency_s": metrics["latency_s"],
            "peak_ram_mb": metrics["peak_ram_mb"],
            "tokens_generated": metrics["tokens_generated"],
            "tokens_per_second": metrics["tokens_per_second"],
        }
        results.append(result)

        status = "PASS" if accuracy == 1.0 else "FAIL"
        print(f"         {status} | {metrics['latency_s']}s | "
              f"{metrics['peak_ram_mb']}MB RAM | "
              f"{metrics['tokens_per_second']} tok/s")

    avg_accuracy = total_accuracy / len(prompts) if prompts else 0.0
    avg_latency = sum(r["latency_s"] for r in results) / len(results) if results else 0.0
    avg_ram_mb = sum(r["peak_ram_mb"] for r in results) / len(results) if results else 0.0
    avg_ram_gb = avg_ram_mb / 1024

    # CARS calculations
    cars_ram = round(avg_accuracy / (avg_ram_gb * avg_latency), 4) if (avg_ram_gb * avg_latency) > 0 else 0.0
    cars_size = round(avg_accuracy / (model_size * avg_latency), 4) if (model_size * avg_latency) > 0 else 0.0

    output = {
        "model": model_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hardware": hardware,
        "model_size_gb": model_size,
        "results": results,
        "summary": {
            "avg_accuracy": round(avg_accuracy, 3),
            "avg_latency_s": round(avg_latency, 2),
            "avg_peak_ram_mb": round(avg_ram_mb, 1),
            "avg_tokens_per_second": round(
                sum(r["tokens_per_second"] for r in results) / len(results), 2
            ) if results else 0.0,
        },
        "cars_ram": cars_ram,
        "cars_size": cars_size,
    }

    print(f"\n  Summary: accuracy={avg_accuracy:.1%} | "
          f"latency={avg_latency:.1f}s | RAM={avg_ram_mb:.0f}MB")
    print(f"  CARS_RAM={cars_ram} | CARS_Size={cars_size}")

    return output


def find_models(models_dir: Path) -> list[str]:
    """Find all .gguf files in models directory."""
    if not models_dir.exists():
        return []
    return sorted(str(p) for p in models_dir.glob("*.gguf"))


def main():
    parser = argparse.ArgumentParser(description="CARS Baseline Benchmark Runner")
    parser.add_argument(
        "--models", nargs="*",
        help="Model file paths. Default: all .gguf in ~/models/",
    )
    parser.add_argument(
        "--prompts", type=str, default=str(DEFAULT_PROMPTS),
        help=f"Prompts JSON file. Default: {DEFAULT_PROMPTS}",
    )
    parser.add_argument(
        "--results-dir", type=str, default=str(DEFAULT_RESULTS_DIR),
        help=f"Results output directory. Default: {DEFAULT_RESULTS_DIR}",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=256,
        help="Max tokens to generate per prompt. Default: 256",
    )
    args = parser.parse_args()

    # Verify llama-cli exists
    if not LLAMA_CLI.exists():
        print(f"ERROR: llama-cli not found at {LLAMA_CLI}")
        print("Run setup-titan.sh first.")
        raise SystemExit(1)

    # Load prompts
    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"ERROR: Prompts file not found: {prompts_path}")
        raise SystemExit(1)
    with open(prompts_path) as f:
        prompts = json.load(f)
    print(f"Loaded {len(prompts)} prompts from {prompts_path}")

    # Find models
    if args.models:
        model_paths = args.models
    else:
        model_paths = find_models(DEFAULT_MODELS_DIR)
    if not model_paths:
        print(f"ERROR: No .gguf models found in {DEFAULT_MODELS_DIR}")
        print("Run setup-titan.sh first.")
        raise SystemExit(1)
    print(f"Found {len(model_paths)} model(s)")

    # Run benchmarks
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")

    all_results = []
    for model_path in model_paths:
        if not os.path.exists(model_path):
            print(f"WARNING: Model not found: {model_path}, skipping")
            continue
        result = run_benchmark(model_path, prompts)
        all_results.append(result)

        # Save individual result
        model_name = Path(model_path).stem
        out_file = results_dir / f"{date_str}-{model_name}.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n  Saved: {out_file}")

    # Print comparison table
    if len(all_results) > 1:
        print(f"\n{'='*60}")
        print("COMPARISON")
        print(f"{'='*60}")
        print(f"{'Model':<40} {'Acc':>5} {'Lat':>6} {'RAM':>7} {'CARS_R':>7} {'CARS_S':>7}")
        print("-" * 73)
        for r in all_results:
            print(f"{r['model']:<40} "
                  f"{r['summary']['avg_accuracy']:>5.1%} "
                  f"{r['summary']['avg_latency_s']:>5.1f}s "
                  f"{r['summary']['avg_peak_ram_mb']:>6.0f}M "
                  f"{r['cars_ram']:>7.4f} "
                  f"{r['cars_size']:>7.4f}")


if __name__ == "__main__":
    main()
```

**Step 2: Make executable and commit**

```bash
chmod +x ~/soul/soul-bench/scripts/benchmark.py
cd ~/soul/soul-bench
git add scripts/benchmark.py
git commit -m "feat: add benchmark runner with CARS metric calculation"
```

---

## Task 4: Deploy and run setup on titan-pc

**Step 1: Copy scripts to titan-pc**

```bash
scp -r ~/soul/soul-bench/scripts/ titan-pc:~/bench-scripts/
scp -r ~/soul/soul-bench/prompts/ titan-pc:~/bench-prompts/
```

**Step 2: Run setup script on titan-pc**

```bash
ssh titan-pc "bash ~/bench-scripts/setup-titan.sh"
```

Expected output: cmake build succeeds, two models downloaded (~4.4GB total), quick smoke test prints a response.

This step takes 15-30 min depending on download speed.

**Step 3: Verify llama-cli works**

```bash
ssh titan-pc "~/llama.cpp/build/bin/llama-cli --version 2>&1; ls -lh ~/models/*.gguf"
```

Expected: llama-cli binary exists, two .gguf files in ~/models/.

---

## Task 5: Run benchmarks and collect results

**Step 1: Run the benchmark runner on titan-pc**

```bash
ssh titan-pc "mkdir -p ~/bench-results && cd ~/bench-scripts && python3 benchmark.py --prompts ~/bench-prompts/smoke-test.json --results-dir ~/bench-results"
```

Expected: 6 runs total (2 models x 3 prompts), prints metrics per prompt and comparison table.

**Step 2: Copy results back to soul-bench**

```bash
scp titan-pc:~/bench-results/*.json ~/soul/soul-bench/results/
```

**Step 3: Commit results**

```bash
cd ~/soul/soul-bench
git add results/*.json
git commit -m "data: add CARS baseline smoke test results for Phi-3.5-mini and Qwen2.5-3B"
```

---

## Task 6: Document hardware baseline

**Files:**
- Create: `soul-bench/results/BASELINE.md`

**Step 1: Write baseline document**

After benchmarks complete, create `soul-bench/results/BASELINE.md` with:

```markdown
# CARS Baseline Results — 2026-02-22

## Hardware
- Machine: titan-pc (192.168.0.113)
- CPU: Intel i5-8400 (6 cores, 2.80GHz, no HT)
- RAM: 7.6GB DDR4
- GPU: None (Intel UHD 630 iGPU, not used)
- OS: Ubuntu 24.04

## Models Tested
| Model | Params | Quant | File Size |
|-------|--------|-------|-----------|
| Phi-3.5-mini-instruct | 3.8B | Q4_K_M | X.X GB |
| Qwen2.5-3B-Instruct | 3B | Q4_K_M | X.X GB |

## Results
[Fill from benchmark JSON output]

| Model | Avg Accuracy | Avg Latency | Peak RAM | Tok/s | CARS_RAM | CARS_Size |
|-------|-------------|-------------|----------|-------|----------|-----------|
| Phi-3.5-mini | X% | Xs | XMXB | X.X | X.XXXX | X.XXXX |
| Qwen2.5-3B | X% | Xs | XMB | X.X | X.XXXX | X.XXXX |

## Per-Task Breakdown
[Fill from benchmark JSON output]

## Observations
- [Fill after seeing results]

## Next Steps
- Day 3: Full 10-task CARS benchmark suite
- Day 3: Colab T4 GPU comparison
- Week 2: Extended to 8B models
```

**Step 2: Fill in actual values from JSON results and commit**

```bash
cd ~/soul/soul-bench
git add results/BASELINE.md
git commit -m "docs: add CARS baseline hardware documentation"
```

---

## Execution Batches

| Batch | Tasks | Description |
|-------|-------|-------------|
| 1 | 1, 2, 3 | Create project structure, setup script, benchmark runner |
| 2 | 4, 5, 6 | Deploy to titan-pc, run benchmarks, document results |

## Notes

- Task 4 (setup) may take 15-30 min for model downloads (~4.4GB) — good time for a break
- If titan-pc runs out of RAM during inference, fall back to Qwen2.5-3B only (smaller model)
- The benchmark.py uses no external dependencies — stdlib only (subprocess, json, time, pathlib)
- Chat templates are hardcoded for Phi and Qwen — extend the `CHAT_TEMPLATES` dict for new model families
- Accuracy is binary (0/1) for smoke test — automated nuanced scoring is a Day 3 soul-bench task
