#!/usr/bin/env python3
"""
Build dashboard-optimized JSON from raw CARS benchmark results.

Transforms the full results.json (1.4MB, 52 models x 30 prompts with full responses)
into a compact dashboard.json (~60KB) optimized for frontend consumption.

Also produces:
- models.json: Model-level summary data (leaderboard, efficiency, format tax)
- prompts.json: Prompt-level data with truncated responses (for head-to-head view)
- metadata.json: Benchmark metadata, categories, providers

Usage:
    python3 build_dashboard_data.py
"""

import json
from pathlib import Path
from datetime import datetime

RESULTS_DIR = Path(__file__).parent.parent / "results" / "cloud-2026-03-24"
OUTPUT_DIR = Path(__file__).parent / "data"

PROVIDER_MAP = {
    "anthropic": "Anthropic",
    "claude": "Anthropic",
    "openai": "OpenAI",
    "gpt": "OpenAI",
    "gemini": "Google",
    "google": "Google",
    "amazon": "Amazon",
    "nova": "Amazon",
    "mistral": "Mistral",
    "mixtral": "Mistral",
    "qwen": "Alibaba",
    "deepseek": "DeepSeek",
    "mercury": "Mercury",
}

CATEGORY_LABELS = {
    "campaign-planning": "Campaign Planning",
    "classification": "Classification",
    "code-generation": "Code Generation",
    "contact-research": "Contact Research",
    "email-drafting": "Email Drafting",
    "infra-management": "Infra Management",
    "knowledge-qa": "Knowledge QA",
    "reply-classification": "Reply Classification",
    "system-health": "System Health",
    "task-planning": "Task Planning",
}


def classify_provider(model_id: str, model_name: str) -> str:
    combined = (model_id + " " + model_name).lower()
    # Check specific patterns first
    if combined.startswith("o3") or combined.startswith("o4"):
        return "OpenAI"
    if "r1" in combined and "deepseek" in combined:
        return "DeepSeek"
    if combined == "r1" or "deepseek.r1" in combined:
        return "DeepSeek"
    for key, provider in PROVIDER_MAP.items():
        if key in combined:
            return provider
    return "Other"


def build_models_json(raw_data):
    """Model-level summary for leaderboard + efficiency views."""
    models = []
    for m in raw_data:
        s = m["summary"]
        provider = classify_provider(m["model_id"], m["model"])
        strict = round(s["avg_accuracy"] * 100, 1)
        relaxed = round(s["avg_accuracy_relaxed"] * 100, 1)

        cat_strict = {CATEGORY_LABELS.get(k, k): round(v * 100, 1)
                      for k, v in m.get("category_accuracy", {}).items()}
        cat_relaxed = {CATEGORY_LABELS.get(k, k): round(v * 100, 1)
                       for k, v in m.get("category_accuracy_relaxed", {}).items()}

        models.append({
            "id": m["model"],
            "model_id": m["model_id"],
            "provider": provider,
            "strict_pct": strict,
            "relaxed_pct": relaxed,
            "format_tax_pp": round(relaxed - strict, 1),
            "latency_s": round(s["avg_latency_s"], 2),
            "tps": round(s["avg_tokens_per_second"], 1),
            "est_size_gb": m.get("est_size_gb", 0),
            "cars_size": round(m.get("cars_size", 0), 6),
            "cars_size_relaxed": round(m.get("cars_size_relaxed", 0), 6),
            "cars_ram": round(m.get("cars_ram", 0), 6),
            "cars_vram": round(m.get("cars_vram", 0), 6),
            "total_prompts": s["total_prompts"],
            "total_errors": s["total_errors"],
            "category_strict": cat_strict,
            "category_relaxed": cat_relaxed,
        })

    return sorted(models, key=lambda x: -x["strict_pct"])


def build_prompts_json(raw_data):
    """Prompt-level data for head-to-head comparison view.
    Responses truncated to 300 chars to keep file size manageable."""
    prompts = []
    for m in raw_data:
        provider = classify_provider(m["model_id"], m["model"])
        for r in m["results"]:
            prompts.append({
                "model": m["model"],
                "provider": provider,
                "prompt_id": r["id"],
                "task": r["task"],
                "prompt_preview": r["prompt"][:150],
                "response_preview": (r["response"] or "")[:300],
                "strict": r["accuracy"],
                "relaxed": r.get("accuracy_relaxed", r["accuracy"]),
                "latency_s": round(r["latency_s"], 2),
                "tps": round(r.get("tokens_per_second", 0), 1),
            })
    return prompts


def build_metadata_json(raw_data, models):
    """Benchmark metadata."""
    providers = {}
    for m in models:
        p = m["provider"]
        if p not in providers:
            providers[p] = {"count": 0, "models": []}
        providers[p]["count"] += 1
        providers[p]["models"].append(m["id"])

    # Compute provider aggregates
    provider_stats = {}
    for p, info in providers.items():
        p_models = [m for m in models if m["provider"] == p]
        strict_vals = [m["strict_pct"] for m in p_models]
        relaxed_vals = [m["relaxed_pct"] for m in p_models]
        provider_stats[p] = {
            "count": info["count"],
            "models": info["models"],
            "median_strict": round(sorted(strict_vals)[len(strict_vals) // 2], 1),
            "median_relaxed": round(sorted(relaxed_vals)[len(relaxed_vals) // 2], 1),
            "best_strict": round(max(strict_vals), 1),
            "worst_strict": round(min(strict_vals), 1),
            "spread": round(max(strict_vals) - min(strict_vals), 1),
        }

    return {
        "benchmark": {
            "name": "CARS Benchmark",
            "version": "2.0",
            "date": "2026-03-24",
            "description": "Cost-Adjusted Response Score — 52 cloud LLMs evaluated on 30 structured-output prompts across 10 real-world task categories",
        },
        "stats": {
            "total_models": len(models),
            "total_providers": len(providers),
            "total_prompts": 30,
            "total_categories": 10,
            "total_evaluations": len(models) * 30,
            "avg_format_tax_pp": round(
                sum(m["format_tax_pp"] for m in models) / len(models), 1
            ),
        },
        "categories": CATEGORY_LABELS,
        "providers": provider_stats,
        "insights": {
            "top_strict": models[0]["id"],
            "top_strict_score": models[0]["strict_pct"],
            "zero_format_tax": [m["id"] for m in models if m["format_tax_pp"] == 0],
            "most_efficient": sorted(models, key=lambda x: -x["cars_size"])[0]["id"],
            "generation_regressions": [
                {"newer": "gpt-5", "older": "gpt-3.5-turbo-0125", "delta_pp": -19.0},
                {"newer": "gemini-2.5-pro", "older": "gemini-2.0-flash", "delta_pp": -32.4},
                {"newer": "claude-3-7-sonnet-20250219", "older": "claude-3-5-sonnet-20241022", "delta_pp": -37.3},
            ],
            "reasoning_penalties": [
                {"model": "Gemini 2.5 Flash", "with_reasoning": 33.6, "without": 66.8, "penalty_x": 2.0},
                {"model": "Gemini 3 Flash", "with_reasoning": 46.4, "without": 69.7, "penalty_x": 1.5},
            ],
        },
        "methodology": {
            "scoring": "Dual: strict (exact format match) and relaxed (correct answer, any format)",
            "cars_formula": "CARS_Size = Accuracy / (Est_Size_GB x Avg_Latency_s)",
            "infrastructure": "All models tested via LiteLLM unified API",
            "prompts": "30 structured prompts requiring JSON/specific format output",
            "temperature": 0.0,
        },
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load raw data
    with open(RESULTS_DIR / "results.json") as f:
        raw_data = json.load(f)

    print(f"Loaded {len(raw_data)} models from results.json")

    # Build outputs
    models = build_models_json(raw_data)
    prompts = build_prompts_json(raw_data)
    metadata = build_metadata_json(raw_data, models)

    # Write outputs
    with open(OUTPUT_DIR / "models.json", "w") as f:
        json.dump(models, f, indent=2)
    print(f"  models.json: {len(models)} models ({(OUTPUT_DIR / 'models.json').stat().st_size / 1024:.1f} KB)")

    with open(OUTPUT_DIR / "prompts.json", "w") as f:
        json.dump(prompts, f)  # No indent — file is large
    print(f"  prompts.json: {len(prompts)} evaluations ({(OUTPUT_DIR / 'prompts.json').stat().st_size / 1024:.1f} KB)")

    with open(OUTPUT_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"  metadata.json ({(OUTPUT_DIR / 'metadata.json').stat().st_size / 1024:.1f} KB)")

    # Combined dashboard.json (models + metadata, no prompts — prompts loaded on demand)
    dashboard = {
        "metadata": metadata,
        "models": models,
    }
    with open(OUTPUT_DIR / "dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    print(f"  dashboard.json ({(OUTPUT_DIR / 'dashboard.json').stat().st_size / 1024:.1f} KB)")

    print("\nDone. Dashboard data ready for frontend consumption.")


if __name__ == "__main__":
    main()
