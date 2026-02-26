# Benchmark Blog Post — Design Doc

**Date:** 2026-02-26
**Status:** Approved
**Source material:** `docs/reports/2026-02-23-soul-bench-full-suite-report.md`

---

## Goal

Establish credibility as an AI researcher by publishing benchmark results with the CARS (Cost-Aware Reasoning Score) metric. Lead with data, use research paper rigor.

## Approach

**Approach A: Single canonical paper, adapted per platform.**

One ~2,200-word research-style post on the personal blog. Syndicate to Medium with canonical URL. Condensed discussion post on Reddit.

---

## Platform Deliverables

### 1. Blog Post (Canonical) — rishavchatterjee.com

**Title:** "CARS: A Cost-Aware Metric for Benchmarking Local LLMs on Constrained Hardware"

**Format:** Research paper style (~2,200 words)

| Section | ~Words | Content |
|---------|--------|---------|
| Abstract | 150 | CARS formula, hardware tested, models compared, key finding (Qwen 2.7-3.3x better CARS) |
| 1. Introduction | 200 | Problem: leaderboard accuracy doesn't predict real-world efficiency. Need cost-per-quality on actual hardware. |
| 2. The CARS Metric | 300 | Formula, three variants (CARS_RAM, CARS_Size, CARS_VRAM), why efficiency > raw accuracy for deployment decisions |
| 3. Methodology | 400 | Hardware specs (i5-8400 8GB CPU, Colab T4 GPU), models (Phi-3.5-mini Q4_K_M 2.23GB, Qwen2.5-3B Q4_K_M 1.96GB), 10 task categories, 33 prompts, 7 scoring methods with fractional scoring (0.0-1.0), adversarial injection test |
| 4. Results | 500 | CPU results table, GPU results table, category-level breakdown, head-to-head comparison, GPU vs CPU speedup (3-6x), category divergence analysis |
| 5. Discussion | 300 | Key findings: 3B models fail reasoning but ace classification/code, Qwen resists adversarial injection, deploy gate concept (>=80% accuracy, no category <70%, P95 latency <5s), neither model passes |
| 6. Limitations | 150 | Only 2 models, 33 prompts (small sample), no repeated runs (no statistical significance), single CPU machine, heuristic scoring (not human-evaluated), adversarial test n=1 |
| 7. Reproduction | 150 | Clone repo, run setup script, run benchmark command, how to add models/prompts, link to GitHub |

**Key data to include:**
- CARS formula: `CARS = Accuracy / (Resource_Cost x Latency)`
- Head-to-head table: Accuracy, Latency, VRAM, CARS_Size, CARS_VRAM
- Category accuracy table (12 categories, both models)
- GPU vs CPU speedup comparison
- Deploy gate pass/fail status

**Tone:** Data-first, research rigor, no buzzwords, honest about limitations.

### 2. Medium (Syndication)

- Republish full blog post using Medium "Import a story" (canonical URL to blog)
- Tags: `artificial-intelligence`, `machine-learning`, `benchmarks`, `llm`, `local-ai`
- Submit to "Towards Data Science" or "Towards AI" publication for amplification
- No content changes from blog version

### 3. Reddit — r/LocalLLaMA (Primary)

**Title:** "Benchmarked Phi-3.5-mini vs Qwen2.5-3B across 10 task categories on CPU (i5, 8GB) and GPU (Colab T4) — Qwen wins 2.7-3.3x on efficiency"

**Format:** ~500 words, condensed discussion post

**Structure:**
1. Hook (2 lines): What I tested and why — efficiency > accuracy alone for deployment
2. CARS formula (3 lines): Show formula, one-sentence explanation
3. Key results table: Head-to-head (accuracy, latency, VRAM, CARS scores)
4. Category breakdown table: Where models diverge significantly
5. Interesting finding: Adversarial injection resistance — Qwen passed, Phi failed
6. Deploy gate concept (2 lines): Neither passes >=80% accuracy with no category <70%
7. Link to full paper: Blog URL
8. Discussion prompt: "Anyone else running structured benchmark suites on consumer hardware? What task categories do 3B models fail at consistently?"

**Tone:** Genuinely helpful, data-forward, match r/LocalLLaMA culture. No self-promotion beyond the blog link.

**Flair:** Likely "Benchmark" or "Discussion"

### 4. Reddit — r/selfhosted (Cross-post, adapted)

**Title:** "What can a 3B LLM actually do on an i5 with 8GB RAM? I benchmarked 10 real-world task categories"

**Adjustments from r/LocalLLaMA version:**
- Lead with hardware constraints (the "what can my old hardware do" angle)
- Emphasize CPU-only results and RAM overhead (model size vs runtime memory)
- De-emphasize CARS formula details (r/selfhosted cares about practical "will this run" answers)
- Include the practical finding: "3B models CAN do classification and code gen, CANNOT do trick reasoning"
- Discussion prompt: "Anyone running local LLMs on similar hardware for home automation or self-hosted services? What tasks do you delegate to them?"

**Flair:** Likely "AI" or "Discussion"

---

## Content Quality Gates (from content strategy)

- [x] **Concrete artifact?** CARS metric, benchmark results tables, reproduction commands
- [x] **Audience value?** Practitioners learn which 3B model to pick, what tasks work, what fails
- [x] **Identity match?** AI Researcher pillar — original metric, rigorous methodology, honest limitations

---

## Execution Order

1. Draft the canonical blog post (~2,200 words)
2. Review and approve
3. Publish to blog
4. Syndicate to Medium (import with canonical URL)
5. Draft Reddit r/LocalLLaMA post (~500 words)
6. Draft Reddit r/selfhosted adaptation
7. Review and approve Reddit posts
8. Post to Reddit (timing: 8-9 AM IST for US evening scroll)
9. Log all posts to `docs/post-log.md`

---

## Files to Create

| File | Content |
|------|---------|
| `docs/drafts/2026-02-26-blog-cars-benchmark.md` | Canonical blog post |
| `docs/drafts/2026-02-26-medium-cars-benchmark.md` | Medium version (same as blog, with Medium metadata) |
| `docs/drafts/2026-02-26-reddit-localllama-cars-benchmark.md` | r/LocalLLaMA post |
| `docs/drafts/2026-02-26-reddit-selfhosted-cars-benchmark.md` | r/selfhosted post |
