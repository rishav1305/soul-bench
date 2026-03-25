#!/usr/bin/env python3
"""
CARS Benchmark Runner — Soul Bench (LiteLLM Proxy Edition)
============================================================
Runs CARS benchmarks against ALL available models via a unified LiteLLM proxy.
Dynamically discovers models from the proxy's /models endpoint.

Usage:
    # Run against all discovered text models:
    LITELLM_API_KEY=sk-xxx python3 cars_benchmark_litellm.py

    # Run specific models only:
    LITELLM_API_KEY=sk-xxx python3 cars_benchmark_litellm.py --models gpt-4o,claude-sonnet-4-6

    # Smoke test (3 prompts only):
    LITELLM_API_KEY=sk-xxx python3 cars_benchmark_litellm.py --smoke

    # List available models without running:
    LITELLM_API_KEY=sk-xxx python3 cars_benchmark_litellm.py --list-models

Author: Banner (Data Science Expert, Soul Team)
Date: 2026-03-24
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

# ============================================================================
# Configuration
# ============================================================================

PROMPTS_DIR = Path(os.path.expanduser("~/soul-v2/internal/bench/prompts"))
OUTPUT_DIR = Path(os.path.expanduser("~/soul-roles/shared/briefs/banner-analyses"))

LITELLM_BASE_URL = os.environ.get(
    "LITELLM_BASE_URL",
    "https://api.mercury.weather.com/litellm/v1"
)

# Patterns to EXCLUDE from benchmarking (not text-generation models)
EXCLUDE_PATTERNS = [
    r"embed",           # embedding models
    r"rerank",          # rerankers
    r"stable-diffusion", r"stable-image", r"stable-style", # image gen
    r"nova-canvas",     # image gen
    r"nova-reel",       # video gen
    r"nova-sonic",      # audio
    r"pegasus",         # video understanding
    r"-vision$",        # vision-only endpoints
    r"^fake-",          # test endpoints
    r"-image(?:-preview)?$",  # image generation endpoints
]

# Models to skip (known non-chat, duplicates, or internal routing)
SKIP_MODELS = {
    "fake-openai-endpoint",
    "amazon.titan-embeddings",
    "amazon.titan-embed-text-v2:0",
    "cohere.embed-multilingual-v3",
    "cohere.embed-english-v3",
    "gemini-embedding-001",
    "text-embedding-ada-002",
    "mercury/onprem.chat",          # generic internal router
    "mercury/devflow.default",      # internal routing
    "mercury/devflow.claude",       # internal routing
    "mercury/devflow.gemini",       # internal routing
    "bedrock/amazon.rerank-v1:0",
    "bedrock/cohere.rerank-v3-5:0",
    "bedrock/amazon.nova-canvas-v1:0",
    "bedrock/amazon.nova-reel-v1:0",
    "bedrock/amazon.nova-reel-v1:1",
    "bedrock/amazon.nova-sonic-v1:0",
    "bedrock/stability.stable-diffusion-xl-v1",
    "bedrock/stability.stable-image-remove-background-v1:0",
    "bedrock/stability.stable-image-style-guide-v1:0",
    "bedrock/stability.stable-image-control-sketch-v1:0",
    "bedrock/stability.stable-image-erase-object-v1:0",
    "bedrock/stability.stable-image-control-structure-v1:0",
    "bedrock/stability.stable-image-search-recolor-v1:0",
    "bedrock/stability.stable-image-inpaint-v1:0",
    "bedrock/stability.stable-image-search-replace-v1:0",
    "bedrock/stability.stable-style-transfer-v1:0",
    "bedrock/twelvelabs.pegasus-1-2-v1:0",
    "bedrock/twelvelabs.marengo-embed-2-7-v1:0",
    "gemini/gemini-pro-vision",
    "gemini/gemini-1.5-pro-vision",
    "gemini/gemini-2.5-flash-image",
    "gemini/gemini-3-pro-image-preview",
    "gemini/gemini-3.1-flash-image-preview",
}

# Deduplicate: map aliases to canonical model IDs
# When multiple IDs point to the same model, keep only the canonical one
CANONICAL_MAP = {
    # Claude duplicates — keep specific version IDs
    "Claude-4.5-Opus": None,                    # skip, use claude-4.5-opus
    "Claude-4-Sonnet": None,                    # skip, use claude-sonnet-4-20250514
    "Claude-4-Sonnet:1m-context": None,         # skip duplicate
    "Claude-4.5-Sonnet": None,                  # skip, use claude-sonnet-4-5-20250929
    "Claude-4.5-Sonnet:1m-context": None,       # skip duplicate
    "Claude-3.5-Sonnet": None,                  # skip, use bedrock version
    "Claude-3.7-Sonnet": None,                  # skip, use bedrock version
    # Bedrock duplicates with context variants
    "bedrock/anthropic.claude-sonnet-4-20250514-v1:0:1m-context": None,
    "bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0:1m-context": None,
    # Bedrock context size variants — keep the base
    "bedrock/amazon.nova-pro-v1:0:300k": None,
    "bedrock/amazon.nova-pro-v1:0:24k": None,
    "bedrock/amazon.nova-lite-v1:0:300k": None,
    "bedrock/amazon.nova-lite-v1:0:24k": None,
    "bedrock/amazon.nova-micro-v1:0:128k": None,
    "bedrock/amazon.nova-micro-v1:0:24k": None,
    "bedrock/amazon.nova-premier-v1:0:8k": None,
    "bedrock/amazon.nova-premier-v1:0:20k": None,
    "bedrock/amazon.nova-premier-v1:0:1000k": None,
    "bedrock/amazon.nova-premier-v1:0:mm": None,
    # OpenAI duplicates
    "openai/gpt-4o": None,                      # use gpt-4o
    "openai/gpt-4": None,                       # use gpt-4-06-13
    "openai/gpt-4-32k": None,                   # use gpt-4-32k-0613
    "gpt-4-32k-0314": None,                     # old version
    # Gemini path duplicates — prefer non-prefixed or gemini/ prefixed
    "gemini/gemini-2.5-pro": None,              # use gemini-2.5-pro
    "gemini/gemini-2.5-flash-lite": None,       # use gemini-2.5-flash-lite
    # Reasoning model duplicates
    "gemini-3-flash-no-reasoning": None,        # use gemini/gemini-3-flash-no-reasoning
    "gemini-3-flash-reasoning": None,           # use gemini/gemini-3-flash
}

# Estimated model sizes (billions of parameters) for CARS score computation
# Best-effort estimates from public info; unknown models default to 50B
MODEL_SIZE_ESTIMATES = {
    # Claude family
    "claude-haiku-4-5-20251001": 8,
    "claude-sonnet-4-20250514": 70,
    "claude-sonnet-4-5-20250929": 70,
    "claude-sonnet-4-6": 70,
    "claude-4.5-opus": 175,
    "claude-opus-4-5-20251101": 175,
    "claude-opus-4-6": 200,
    "bedrock/anthropic.claude-3-haiku-20240307-v1:0": 8,
    "bedrock/anthropic.claude-3-5-haiku-20241022-v1:0": 8,
    "bedrock/anthropic.claude-3-sonnet-20240229-v1:0": 70,
    "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0": 70,
    "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0": 70,
    "bedrock/anthropic.claude-sonnet-4-20250514-v1:0": 70,
    "bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0": 70,
    "bedrock/anthropic.claude-sonnet-4-6": 70,
    "bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0": 70,
    "bedrock/anthropic.claude-3-7-sonnet-20250219-v1:0": 70,
    "bedrock/anthropic.claude-opus-4-20250514-v1:0": 175,
    "bedrock/anthropic.claude-opus-4-1-20250805-v1:0": 175,
    "bedrock/anthropic.claude-opus-4-5-20251101-v1:0": 175,
    # GPT family
    "gpt-3.5-turbo-0125": 20,
    "gpt-4-06-13": 175,
    "gpt-4-turbo": 175,
    "gpt-4o": 200,
    "gpt-4o-mini": 8,
    "gpt-4.1": 200,
    "gpt-4.1-mini": 30,
    "gpt-4.1-nano": 8,
    "gpt-5": 400,
    "gpt-5-pro": 500,
    "gpt-5.2": 400,
    "gpt-5.2-pro": 500,
    "gpt-5.3-codex": 300,
    "gpt-5.3-codex-spark": 100,
    "gpt-5-mini": 50,
    "gpt-5-nano": 8,
    "gpt-5.1-codex": 300,
    "gpt-5.1-codex-max": 400,
    "gpt-4-32k-0613": 175,
    "o4-mini": 50,
    "o4-mini-deep-research": 50,
    "openai/o3-mini": 50,
    "openai/o3": 200,
    "openai/o1-mini": 50,
    "bedrock/openai.gpt-oss-120b-1:0": 120,
    "bedrock/openai.gpt-oss-20b-1:0": 20,
    # Gemini family
    "gemini-2.5-pro": 175,
    "gemini-2.5-flash-lite": 8,
    "gemini/gemini-pro": 50,
    "gemini/gemini-1.5-pro": 100,
    "gemini/gemini-2.0-flash": 30,
    "gemini/gemini-2.5-pro-exp-03-25": 175,
    "gemini/gemini-2.5-flash-preview-04-17": 30,
    "gemini/gemini-2.5-pro-preview-05-06": 175,
    "gemini/gemini-2.5-flash": 30,
    "gemini/gemini-2.5-flash-no-reasoning": 30,
    "gemini/gemini-3-flash-no-reasoning": 30,
    "gemini/gemini-3-flash": 30,
    "gemini-3-pro": 175,
    "gemini-3.1-pro": 175,
    # Llama family
    "bedrock/meta.llama3-2-1b-instruct-v1:0": 1,
    "bedrock/meta.llama3-2-3b-instruct-v1:0": 3,
    "bedrock/meta.llama3-2-11b-instruct-v1:0": 11,
    "bedrock/meta.llama3-2-90b-instruct-v1:0": 90,
    "bedrock/meta.llama3-3-70b-instruct-v1:0": 70,
    "bedrock/meta.llama4-scout-17b-instruct-v1:0": 17,
    "bedrock/meta.llama4-maverick-17b-instruct-v1:0": 17,
    # Mistral family
    "bedrock/mistral.mistral-7b-instruct-v0:2": 7,
    "bedrock/mistral.mixtral-8x7b-instruct-v0:1": 47,
    "bedrock/mistral.pixtral-large-2502-v1:0": 124,
    "bedrock/mistral.mistral-large-2407-v1:0": 123,
    # Amazon
    "amazon.titan-text-lite-v1": 7,
    "amazon.titan-text-express-v1": 30,
    "bedrock/amazon.nova-pro-v1:0": 50,
    "bedrock/amazon.nova-lite-v1:0": 15,
    "bedrock/amazon.nova-micro-v1:0": 3,
    "bedrock/amazon.nova-premier-v1:0": 100,
    # Cohere
    "cohere.command-text-v14": 52,
    # DeepSeek
    "bedrock/us.deepseek.r1-v1:0": 671,
    "bedrock/deepseek.r1-v1:0": 671,
    # Qwen
    "bedrock/qwen.qwen3-coder-30b-a3b-v1:0": 30,
    "bedrock/qwen.qwen3-32b-v1:0": 32,
    # Mercury on-prem
    "mercury/onprem": 8,
    "mercury/onprem.gemma3": 27,
    "mercury/onprem.llama3.3": 70,
    "mercury/onprem.qwen3-coder": 30,
    "mercury/onprem.deepseek-r1": 671,
    "mercury/onprem.phi3": 14,
    "mercury/onprem.qwen2.5": 32,
    "mercury/onprem.nemotron-mini": 4,
    "mercury/onprem.deepseek-coder-small": 7,
    "mercury/onprem.qwen3-coder-next": 30,
    "mercury/onprem.gpt-oss:120b": 120,
}

DEFAULT_SIZE_GB = 50  # fallback for unknown models

# All benchmark categories
ALL_CATEGORIES = [
    "system-health", "code-generation", "classification",
    "knowledge-qa", "task-planning", "email-drafting",
    "contact-research", "campaign-planning", "reply-classification",
    "infra-management",
]

SMOKE_CATEGORIES = ["smoke-test"]

CATEGORY_ID_MAP = {
    "smoke": "smoke-test", "sh": "system-health", "cg": "code-generation",
    "cl": "classification", "kq": "knowledge-qa", "tp": "task-planning",
    "ed": "email-drafting", "cr": "contact-research", "cp": "campaign-planning",
    "rc": "reply-classification", "im": "infra-management",
}


# ============================================================================
# Model Discovery
# ============================================================================

def discover_models(api_key: str) -> list[str]:
    """Discover all available models from the LiteLLM proxy."""
    url = f"{LITELLM_BASE_URL}/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    all_ids = [m["id"] for m in data.get("data", [])]
    return all_ids


def is_text_model(model_id: str) -> bool:
    """Check if a model ID looks like a text-generation model."""
    if model_id in SKIP_MODELS:
        return False
    if model_id in CANONICAL_MAP:
        return False  # deduplicated away
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, model_id, re.IGNORECASE):
            return False
    return True


def filter_text_models(all_model_ids: list[str]) -> list[str]:
    """Filter to only text-generation models, deduplicated."""
    return sorted([m for m in all_model_ids if is_text_model(m)])


def get_model_size(model_id: str) -> float:
    """Get estimated model size in billions of parameters."""
    return MODEL_SIZE_ESTIMATES.get(model_id, DEFAULT_SIZE_GB)


def get_display_name(model_id: str) -> str:
    """Generate a human-readable display name from model ID."""
    name = model_id
    # Strip common prefixes
    for prefix in ["bedrock/anthropic.", "bedrock/meta.", "bedrock/mistral.",
                   "bedrock/amazon.", "bedrock/us.anthropic.", "bedrock/us.deepseek.",
                   "bedrock/deepseek.", "bedrock/openai.", "bedrock/qwen.",
                   "openai/", "gemini/"]:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    # Clean up version suffixes for readability
    name = re.sub(r'-v\d+:\d+$', '', name)
    return name


# ============================================================================
# Prompt Loading
# ============================================================================

def load_prompts(categories: list[str] | None = None) -> list[dict]:
    """Load benchmark prompts from JSON files."""
    cats = categories or ALL_CATEGORIES
    all_prompts = []
    for cat in cats:
        path = PROMPTS_DIR / f"{cat}.json"
        if not path.exists():
            print(f"  WARNING: Category file not found: {path}")
            continue
        with open(path) as f:
            prompts = json.load(f)
            all_prompts.extend(prompts)
    return all_prompts


# ============================================================================
# Scoring Methods (identical to original — matching Go harness)
# ============================================================================

def extract_json(text: str) -> str:
    match = re.search(r'```(?:json)?\s*\n?(.*?)```', text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def extract_code_block(text: str) -> str:
    match = re.search(r'```(?:\w+)?\s*\n?(.*?)```', text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def _find_keys_recursive(obj: dict, keys: set[str], depth: int = 0) -> dict:
    found = {}
    if depth > 2 or not isinstance(obj, dict):
        return found
    for k, v in obj.items():
        if k in keys:
            found[k] = v
        if isinstance(v, dict):
            found.update(_find_keys_recursive(v, keys - set(found.keys()), depth + 1))
    return found

def score_json_schema(response: str, config: dict) -> float:
    json_str = extract_json(response)
    total_checks = 0
    passed_checks = 0
    total_checks += 1
    try:
        parsed = json.loads(json_str)
        if not isinstance(parsed, dict):
            return 0.0
        passed_checks += 1
    except (json.JSONDecodeError, ValueError):
        return 0.0

    required_keys = config.get("required_keys", [])
    found_values = {}
    top_level_found = sum(1 for key in required_keys if key in parsed)
    if top_level_found < len(required_keys):
        found_values = _find_keys_recursive(parsed, set(required_keys))
    else:
        found_values = {k: parsed[k] for k in required_keys if k in parsed}

    for key in required_keys:
        total_checks += 1
        if key in parsed or key in found_values:
            passed_checks += 1

    field_checks = config.get("field_checks", {})
    for field, allowed_values in field_checks.items():
        total_checks += 1
        val = parsed.get(field) or found_values.get(field)
        if val is not None and str(val) in allowed_values:
            passed_checks += 1

    return passed_checks / total_checks if total_checks > 0 else 0.0

def score_contains_keywords(response: str, config: dict) -> float:
    keywords = config.get("keywords", [])
    if not keywords:
        return 0.0
    lower = response.lower()
    return sum(1 for kw in keywords if kw.lower() in lower) / len(keywords)

def score_code_executes(response: str, config: dict) -> float:
    code = extract_code_block(response)
    src = code if "package " in code else "package main\n" + code
    tmp_path = "/tmp/bench_code_check.go"
    try:
        with open(tmp_path, "w") as f:
            f.write(src)
        result = subprocess.run(["go", "vet", tmp_path], capture_output=True, text=True, timeout=10)
        return 1.0 if result.returncode == 0 else 0.0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return 0.5 if ("func " in code and "{" in code and "}" in code) else 0.0
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

def score_ordered_steps(response: str, config: dict) -> float:
    steps = config.get("required_order", [])
    if len(steps) < 2:
        return 0.0
    lower = response.lower()
    constraints = len(steps) - 1
    met = 0
    for i in range(constraints):
        pos_a = lower.find(steps[i].lower())
        pos_b = lower.find(steps[i + 1].lower())
        if pos_a >= 0 and pos_b >= 0 and pos_a < pos_b:
            met += 1
    return met / constraints

def score_exact_match_label(expected: str, response: str) -> float:
    return 1.0 if expected.strip().lower() == response.strip().lower() else 0.0

def score_exact_match_label_relaxed(expected: str, response: str) -> float:
    exp = expected.strip().lower()
    resp = response.strip().lower()
    if exp == resp:
        return 1.0
    resp_clean = re.sub(r'[*_]+', '', resp).strip()
    if exp == resp_clean:
        return 1.0
    first_line = resp.split('\n')[0].strip().lower()
    first_line_clean = re.sub(r'[*#\-:_]', '', first_line).strip()
    if exp == first_line_clean:
        return 1.0
    if exp in first_line_clean:
        return 1.0
    return 0.0

def score_exact_match_number(expected: str, response: str) -> float:
    matches = re.findall(r'\b(\d+(?:\.\d+)?)\b', response)
    if not matches:
        return 0.0
    return 1.0 if matches[-1].strip() == expected.strip() else 0.0

def score_contains_function(expected: str, response: str) -> float:
    return 1.0 if expected in response else 0.0

def score_result(response: str, prompt: dict, relaxed: bool = False) -> float:
    scoring = prompt.get("scoring", "")
    config = prompt.get("scoring_config", {})
    expected = prompt.get("expected_answer", "")
    label_scorer = score_exact_match_label_relaxed if relaxed else score_exact_match_label
    scorers = {
        "json_schema": lambda: score_json_schema(response, config),
        "contains_keywords": lambda: score_contains_keywords(response, config),
        "code_executes": lambda: score_code_executes(response, config),
        "ordered_steps": lambda: score_ordered_steps(response, config),
        "exact_match_label": lambda: label_scorer(expected, response),
        "exact_match_number": lambda: score_exact_match_number(expected, response),
        "contains_function": lambda: score_contains_function(expected, response),
    }
    scorer = scorers.get(scoring)
    return scorer() if scorer else 0.0


# ============================================================================
# LiteLLM API Caller (unified — all models go through one endpoint)
# ============================================================================

def call_litellm(prompt_text: str, model_id: str, api_key: str,
                 max_tokens: int = 512, temperature: float = 0.0) -> dict:
    """Call any model via the LiteLLM OpenAI-compatible proxy."""
    url = f"{LITELLM_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": model_id,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt_text}],
    }

    start = time.monotonic()
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=180)
        latency = time.monotonic() - start

        if resp.status_code != 200:
            error_body = resp.text[:500]
            return {
                "response": f"[API error {resp.status_code}: {error_body}]",
                "latency_s": latency,
                "error": True,
                "error_code": resp.status_code,
            }

        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            return {
                "response": "[No choices in response]",
                "latency_s": latency,
                "error": True,
            }

        text = choices[0].get("message", {}).get("content", "")
        usage = data.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        return {
            "response": text,
            "latency_s": latency,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "tokens_per_second": output_tokens / latency if latency > 0 else 0,
            "error": False,
        }
    except requests.exceptions.Timeout:
        return {
            "response": "[timeout after 180s]",
            "latency_s": 180.0,
            "error": True,
        }
    except Exception as e:
        return {
            "response": f"[exception: {e}]",
            "latency_s": time.monotonic() - start,
            "error": True,
        }


# ============================================================================
# Benchmark Runner
# ============================================================================

def run_benchmark(model_id: str, prompts: list[dict], api_key: str,
                  verbose: bool = True) -> dict:
    """Run full benchmark for a single model via LiteLLM proxy."""
    display = get_display_name(model_id)
    est_size = get_model_size(model_id)

    print(f"\n{'='*60}")
    print(f"  Benchmarking: {display} ({model_id})")
    print(f"  Est. size: {est_size}B params | Prompts: {len(prompts)}")
    print(f"{'='*60}")

    results = []
    cat_scores_strict: dict[str, list[float]] = {}
    cat_scores_relaxed: dict[str, list[float]] = {}
    total_errors = 0
    consecutive_errors = 0
    EARLY_BAIL_THRESHOLD = 5  # Drop model after 5 consecutive errors

    for i, prompt in enumerate(prompts):
        pid = prompt["id"]
        task = prompt["task"]
        cat_key = pid.split("-")[0] if "-" in pid else pid

        if verbose:
            print(f"  [{i+1}/{len(prompts)}] {pid}: {task[:50]}...", end=" ", flush=True)

        resp = call_litellm(prompt["prompt"], model_id, api_key)

        if resp.get("error"):
            accuracy_strict = 0.0
            accuracy_relaxed = 0.0
            total_errors += 1
            consecutive_errors += 1
            if verbose:
                err_code = resp.get("error_code", "?")
                print(f"ERROR[{err_code}] ({resp['latency_s']:.1f}s)")
            # If we get a 429 rate limit, pause longer
            if resp.get("error_code") == 429:
                print("    Rate limited — waiting 10s...")
                time.sleep(10)
            # Early bailout: if first N prompts ALL error, this model is unreachable
            if consecutive_errors >= EARLY_BAIL_THRESHOLD and total_errors == i + 1:
                print(f"  EARLY BAIL: {EARLY_BAIL_THRESHOLD} consecutive errors — model unreachable")
                break
        else:
            consecutive_errors = 0  # Reset on success
            accuracy_strict = score_result(resp["response"], prompt, relaxed=False)
            accuracy_relaxed = score_result(resp["response"], prompt, relaxed=True)
            if verbose:
                delta = "" if accuracy_strict == accuracy_relaxed else f" (relaxed={accuracy_relaxed:.2f})"
                print(f"acc={accuracy_strict:.2f}{delta} ({resp['latency_s']:.1f}s, "
                      f"{resp.get('tokens_per_second', 0):.0f} tok/s)")

        result = {
            "id": pid,
            "task": task,
            "prompt": prompt["prompt"],
            "expected": prompt.get("expected_answer", ""),
            "response": resp["response"][:500],
            "accuracy": accuracy_strict,
            "accuracy_relaxed": accuracy_relaxed,
            "latency_s": resp["latency_s"],
            "tokens_per_second": resp.get("tokens_per_second", 0),
            "input_tokens": resp.get("input_tokens", 0),
            "output_tokens": resp.get("output_tokens", 0),
            "error": resp.get("error", False),
        }
        results.append(result)

        cat_scores_strict.setdefault(cat_key, []).append(accuracy_strict)
        cat_scores_relaxed.setdefault(cat_key, []).append(accuracy_relaxed)

        # Rate limiting delay
        if i < len(prompts) - 1:
            time.sleep(0.5)

    # Compute summary
    valid_results = [r for r in results if not r["error"]]
    n = len(valid_results) if valid_results else 1

    avg_accuracy = sum(r["accuracy"] for r in valid_results) / n
    avg_accuracy_relaxed = sum(r["accuracy_relaxed"] for r in valid_results) / n
    avg_latency = sum(r["latency_s"] for r in valid_results) / n
    avg_tps = sum(r["tokens_per_second"] for r in valid_results) / n

    category_accuracy = {}
    for cat_id, scores in cat_scores_strict.items():
        cat_name = CATEGORY_ID_MAP.get(cat_id, cat_id)
        category_accuracy[cat_name] = sum(scores) / len(scores) if scores else 0.0

    category_accuracy_relaxed = {}
    for cat_id, scores in cat_scores_relaxed.items():
        cat_name = CATEGORY_ID_MAP.get(cat_id, cat_id)
        category_accuracy_relaxed[cat_name] = sum(scores) / len(scores) if scores else 0.0

    cars_size_strict = avg_accuracy / (est_size * avg_latency) if (est_size > 0 and avg_latency > 0) else 0
    cars_size_relaxed = avg_accuracy_relaxed / (est_size * avg_latency) if (est_size > 0 and avg_latency > 0) else 0

    bench_result = {
        "model": display,
        "model_id": model_id,
        "model_key": model_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "summary": {
            "avg_accuracy": round(avg_accuracy, 4),
            "avg_accuracy_relaxed": round(avg_accuracy_relaxed, 4),
            "avg_latency_s": round(avg_latency, 3),
            "avg_tokens_per_second": round(avg_tps, 1),
            "total_prompts": len(prompts),
            "total_errors": total_errors,
            "valid_results": len(valid_results),
        },
        "cars_ram": 0.0,
        "cars_size": round(cars_size_strict, 6),
        "cars_size_relaxed": round(cars_size_relaxed, 6),
        "cars_vram": 0.0,
        "category_accuracy": {k: round(v, 4) for k, v in sorted(category_accuracy.items())},
        "category_accuracy_relaxed": {k: round(v, 4) for k, v in sorted(category_accuracy_relaxed.items())},
        "est_size_gb": est_size,
    }

    delta_pp = (avg_accuracy_relaxed - avg_accuracy) * 100
    print(f"\n  Strict:  acc={avg_accuracy:.3f}, CARS_Size={cars_size_strict:.6f}")
    print(f"  Relaxed: acc={avg_accuracy_relaxed:.3f}, CARS_Size={cars_size_relaxed:.6f} (+{delta_pp:.1f}pp)")
    print(f"  Latency: {avg_latency:.2f}s, TPS: {avg_tps:.0f}, Errors: {total_errors}/{len(prompts)}")

    return bench_result


# ============================================================================
# Report Generation
# ============================================================================

def generate_markdown_report(all_results: list[dict], output_path: Path) -> str:
    """Generate a markdown comparison report."""
    lines = [
        "# CARS Benchmark Results — Full Multi-Model Comparison",
        f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
        f"*Models tested: {len(all_results)} | Prompts: {all_results[0]['summary']['total_prompts']} across "
        f"{len(all_results[0]['category_accuracy'])} categories*",
        f"*API: LiteLLM proxy (unified endpoint)*",
        "",
        "## Leaderboard (sorted by relaxed accuracy)",
        "",
        "| # | Model | Strict | Relaxed | Gap | Latency | Tok/s | CARS_Size | Est. Size | Errors |",
        "|---|-------|--------|---------|-----|---------|-------|-----------|-----------|--------|",
    ]

    sorted_results = sorted(all_results, key=lambda x: x["summary"]["avg_accuracy_relaxed"], reverse=True)
    for rank, r in enumerate(sorted_results, 1):
        s = r["summary"]
        gap = (s["avg_accuracy_relaxed"] - s["avg_accuracy"]) * 100
        lines.append(
            f"| {rank} | **{r['model']}** | {s['avg_accuracy']:.1%} | {s['avg_accuracy_relaxed']:.1%} | "
            f"+{gap:.0f}pp | {s['avg_latency_s']:.2f}s | {s['avg_tokens_per_second']:.0f} | "
            f"{r['cars_size_relaxed']:.6f} | {r['est_size_gb']}B | "
            f"{s['total_errors']}/{s['total_prompts']} |"
        )

    # Category breakdown
    lines.extend(["", "## Category Accuracy (Relaxed)", ""])

    # Top 10 models for the category table (too wide otherwise)
    top_models = sorted_results[:15]
    header = "| Category | " + " | ".join(r["model"][:15] for r in top_models) + " |"
    sep = "|----------|" + "|".join(["------"] * len(top_models)) + "|"
    lines.extend([header, sep])

    all_cats = sorted(set(cat for r in all_results for cat in r["category_accuracy_relaxed"]))
    for cat in all_cats:
        row = f"| {cat} |"
        for r in top_models:
            score = r["category_accuracy_relaxed"].get(cat, 0)
            row += f" {score:.0%} |"
        lines.append(row)

    # CARS efficiency table
    lines.extend([
        "", "## CARS Efficiency (sorted by CARS_Size relaxed — higher = more efficient)", "",
        "| Model | Est. Size | Relaxed Acc | Latency | CARS_Size |",
        "|-------|-----------|-------------|---------|-----------|",
    ])
    for r in sorted(all_results, key=lambda x: x["cars_size_relaxed"], reverse=True)[:20]:
        s = r["summary"]
        lines.append(
            f"| {r['model']} | {r['est_size_gb']}B | {s['avg_accuracy_relaxed']:.1%} | "
            f"{s['avg_latency_s']:.2f}s | **{r['cars_size_relaxed']:.6f}** |"
        )

    lines.extend([
        "", "---",
        f"*Benchmark runner: `cars_benchmark_litellm.py` | Scoring: 7 methods matching Go harness*",
        f"*All models accessed via LiteLLM proxy at {LITELLM_BASE_URL}*",
    ])

    report = "\n".join(lines)
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\n  Report saved: {output_path}")
    return report


# ============================================================================
# Smoke Test (quick validation of a model)
# ============================================================================

def smoke_test_model(model_id: str, api_key: str) -> bool:
    """Quick test — send one prompt to verify model responds."""
    resp = call_litellm("What is 2+2? Respond with just the number.", model_id, api_key, max_tokens=10)
    if resp.get("error"):
        return False
    return len(resp.get("response", "")) > 0


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="CARS Benchmark Runner (LiteLLM)")
    parser.add_argument("--models", default=None,
                        help="Comma-separated model IDs (default: auto-discover all)")
    parser.add_argument("--categories", default="all",
                        help="Comma-separated categories or 'all' or 'smoke'")
    parser.add_argument("--smoke", action="store_true",
                        help="Run smoke test only (3 prompts)")
    parser.add_argument("--list-models", action="store_true",
                        help="List available models and exit")
    parser.add_argument("--skip-validation", action="store_true",
                        help="Skip smoke-test validation of each model before benchmarking")
    parser.add_argument("--output", default=None,
                        help="Output JSON path (default: auto-generated)")
    parser.add_argument("--quiet", action="store_true",
                        help="Less verbose output")
    parser.add_argument("--max-models", type=int, default=0,
                        help="Max models to benchmark (0=all)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from interim results file, skipping already-completed models")
    args = parser.parse_args()

    api_key = os.environ.get("LITELLM_API_KEY", "")
    if not api_key:
        print("ERROR: LITELLM_API_KEY not set.")
        print("  export LITELLM_API_KEY=sk-xxx")
        sys.exit(1)

    print("=" * 60)
    print("  CARS Benchmark Runner — Soul Bench (LiteLLM Edition)")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Proxy: {LITELLM_BASE_URL}")
    print("=" * 60)

    # Discover models
    print("\nDiscovering models from proxy...")
    try:
        all_model_ids = discover_models(api_key)
        print(f"  Found {len(all_model_ids)} total models on proxy")
    except Exception as e:
        print(f"  ERROR discovering models: {e}")
        sys.exit(1)

    # Filter to text models
    if args.models:
        text_models = [m.strip() for m in args.models.split(",")]
        print(f"  Using {len(text_models)} specified models")
    else:
        text_models = filter_text_models(all_model_ids)
        print(f"  Filtered to {len(text_models)} text-generation models")

    if args.list_models:
        print(f"\n  Available text-generation models ({len(text_models)}):")
        print(f"  {'Model ID':<60s} {'Display':<30s} {'Est. Size':>10s}")
        print(f"  {'-'*60} {'-'*30} {'-'*10}")
        for m in text_models:
            print(f"  {m:<60s} {get_display_name(m):<30s} {get_model_size(m):>8}B")
        print(f"\n  Skipped models ({len(all_model_ids) - len(text_models)}):")
        skipped = [m for m in all_model_ids if m not in text_models]
        for m in sorted(skipped):
            print(f"    {m}")
        return

    if args.max_models > 0:
        text_models = text_models[:args.max_models]
        print(f"  Limited to first {args.max_models} models")

    # Validate models with smoke test (unless skipped)
    validated_models = []
    if not args.skip_validation:
        print(f"\nValidating {len(text_models)} models (quick smoke test)...")
        for i, model_id in enumerate(text_models):
            display = get_display_name(model_id)
            print(f"  [{i+1}/{len(text_models)}] {display}...", end=" ", flush=True)
            if smoke_test_model(model_id, api_key):
                print("OK")
                validated_models.append(model_id)
            else:
                print("FAILED (skipping)")
            time.sleep(0.3)  # rate limit courtesy
    else:
        validated_models = text_models

    if not validated_models:
        print("\n  ERROR: No models passed validation!")
        sys.exit(1)

    print(f"\n  {len(validated_models)} models ready for benchmarking")

    # Load prompts
    if args.smoke:
        categories = SMOKE_CATEGORIES
    elif args.categories == "all":
        categories = ALL_CATEGORIES
    else:
        categories = [c.strip() for c in args.categories.split(",")]

    print(f"\nLoading prompts from {len(categories)} categories...")
    prompts = load_prompts(categories)
    print(f"  Loaded {len(prompts)} prompts")

    if not prompts:
        print("  ERROR: No prompts loaded!")
        sys.exit(1)

    total_calls = len(validated_models) * len(prompts)
    est_minutes = total_calls * 3.0 / 60  # ~3s per call average
    print(f"\n  Total API calls: {total_calls} ({len(validated_models)} models x {len(prompts)} prompts)")
    print(f"  Estimated time: ~{est_minutes:.0f} minutes")

    # Resume support: load previous results and skip completed models
    all_results = []
    completed_display_names = set()
    if args.resume:
        interim_path = OUTPUT_DIR / "cars-benchmark-interim.json"
        if interim_path.exists():
            with open(interim_path) as f:
                all_results = json.load(f)
            completed_display_names = {r["model"] for r in all_results}
            print(f"\n  RESUME: Loaded {len(all_results)} completed models from interim results")
            for name in sorted(completed_display_names):
                print(f"    ✓ {name}")
        else:
            print("\n  RESUME: No interim file found — starting fresh")

    # Run benchmarks
    failed_models = []
    for idx, model_id in enumerate(validated_models):
        # Skip already-completed models when resuming
        display_name = get_display_name(model_id)
        if display_name in completed_display_names:
            print(f"\n  [{idx+1}/{len(validated_models)}] SKIP (already done): {display_name}")
            continue
        display = get_display_name(model_id)
        print(f"\n  [{idx+1}/{len(validated_models)}] Starting: {display}")
        try:
            result = run_benchmark(model_id, prompts, api_key, verbose=not args.quiet)
            # Only keep results where at least 50% of prompts succeeded
            if result["summary"]["valid_results"] >= len(prompts) * 0.5:
                all_results.append(result)
            else:
                print(f"  DROPPED: {display} — too many errors ({result['summary']['total_errors']}/{len(prompts)})")
                failed_models.append(model_id)
        except Exception as e:
            print(f"\n  ERROR running {model_id}: {e}")
            failed_models.append(model_id)
            continue

        # Save intermediate results after each model (crash safety)
        if all_results:
            interim_path = OUTPUT_DIR / "cars-benchmark-interim.json"
            with open(interim_path, "w") as f:
                json.dump(all_results, f, indent=2)

    if not all_results:
        print("\n  ERROR: No benchmark results produced!")
        sys.exit(1)

    # Save final results
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    json_path = Path(args.output) if args.output else OUTPUT_DIR / f"cars-benchmark-{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n  Raw results saved: {json_path}")

    # Generate markdown report
    md_path = OUTPUT_DIR / f"cars-benchmark-{timestamp}.md"
    generate_markdown_report(all_results, md_path)

    # Clean up interim file
    interim_path = OUTPUT_DIR / "cars-benchmark-interim.json"
    if interim_path.exists():
        interim_path.unlink()

    # Print final summary
    print("\n" + "=" * 60)
    print("  BENCHMARK COMPLETE")
    print("=" * 60)
    print(f"  Models tested: {len(all_results)} (failed: {len(failed_models)})")
    print(f"\n  {'Model':<40s} {'Strict':>7s} {'Relaxed':>8s} {'Latency':>8s} {'CARS':>10s}")
    print(f"  {'-'*40} {'-'*7} {'-'*8} {'-'*8} {'-'*10}")

    for r in sorted(all_results, key=lambda x: x["summary"]["avg_accuracy_relaxed"], reverse=True):
        s = r["summary"]
        print(f"  {r['model']:<40s} {s['avg_accuracy']:>6.1%} {s['avg_accuracy_relaxed']:>7.1%} "
              f"{s['avg_latency_s']:>7.2f}s {r['cars_size_relaxed']:>10.6f}")

    if failed_models:
        print(f"\n  Failed/dropped models: {', '.join(get_display_name(m) for m in failed_models)}")

    print(f"\n  Results: {json_path}")
    print(f"  Report:  {md_path}")

    return all_results


if __name__ == "__main__":
    main()
