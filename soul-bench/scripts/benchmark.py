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
    info = {
        "hostname": platform.node(),
        "cpu": "unknown",
        "cores": os.cpu_count() or 0,
        "ram_gb": 0.0,
    }
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    info["cpu"] = line.split(":")[1].strip()
                    break
    except OSError:
        pass
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
    name = Path(model_path).name.lower()
    if "phi" in name:
        return "phi"
    if "qwen" in name:
        return "qwen"
    return "qwen"


def format_prompt(raw_prompt: str, model_family: str) -> str:
    tmpl = CHAT_TEMPLATES[model_family]
    return f"{tmpl['prefix']}{raw_prompt}{tmpl['suffix']}"


def get_model_size_gb(model_path: str) -> float:
    return round(os.path.getsize(model_path) / (1024**3), 3)


def run_prompt(model_path: str, prompt: str, max_tokens: int = 256) -> dict:
    model_family = detect_model_family(model_path)
    formatted = format_prompt(prompt, model_family)

    cmd = [
        str(LLAMA_CLI),
        "-m", model_path,
        "-p", formatted,
        "-n", str(max_tokens),
        "-c", "2048",
        "--no-display-prompt",
        "--log-disable",
    ]

    start = time.perf_counter()
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

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

    tokens_generated = 0
    tokens_per_second = 0.0
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
    scoring = prompt_data.get("scoring", "")
    expected = prompt_data.get("expected_answer", "")
    resp_lower = response.lower().strip()

    if scoring == "exact_match_number":
        return 1.0 if expected in response else 0.0
    elif scoring == "contains_function":
        return 1.0 if expected in response else 0.0
    elif scoring == "exact_match_label":
        return 1.0 if expected.lower() == resp_lower else 0.0
    return 0.0


def run_benchmark(model_path: str, prompts: list[dict]) -> dict:
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

    if not LLAMA_CLI.exists():
        print(f"ERROR: llama-cli not found at {LLAMA_CLI}")
        print("Run setup-titan.sh first.")
        raise SystemExit(1)

    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"ERROR: Prompts file not found: {prompts_path}")
        raise SystemExit(1)
    with open(prompts_path) as f:
        prompts = json.load(f)
    print(f"Loaded {len(prompts)} prompts from {prompts_path}")

    if args.models:
        model_paths = args.models
    else:
        model_paths = find_models(DEFAULT_MODELS_DIR)
    if not model_paths:
        print(f"ERROR: No .gguf models found in {DEFAULT_MODELS_DIR}")
        print("Run setup-titan.sh first.")
        raise SystemExit(1)
    print(f"Found {len(model_paths)} model(s)")

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

        model_name = Path(model_path).stem
        out_file = results_dir / f"{date_str}-{model_name}.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n  Saved: {out_file}")

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
