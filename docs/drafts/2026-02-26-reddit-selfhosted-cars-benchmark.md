---
date: 2026-02-26
status: "Published"
platform: Reddit
subreddit: r/selfhosted
topic: Local LLM benchmarks on constrained hardware (i5-8400, 8GB RAM)
flair: "AI" or "Discussion"
---

TITLE: What can a 3B LLM actually do on an i5 with 8GB RAM? I benchmarked 10 real-world task categories

---

I had an old desktop sitting around (i5-8400, 8GB RAM, no dedicated GPU) and wanted a real answer to "what can I actually delegate to a local model on this hardware?" Not vibes — actual task results across 10 categories. Ran Phi-3.5-mini and Qwen2.5-3B, both Q4_K_M quantized via llama.cpp.

**Hardware**

| Spec | Value |
|------|-------|
| CPU | Intel i5-8400 (6 cores, 2.80 GHz) |
| RAM | 7.6 GB total |
| GPU | None (CPU-only inference) |
| OS | Ubuntu 24.04 |

**First practical lesson: RAM overhead is brutal**

A 2GB GGUF model does not need 2GB at runtime. It needs 3.4-4.3GB once the KV cache and llama.cpp overhead load up. Qwen2.5-3B (1.96GB on disk) consumed 3.4GB peak RAM. Phi-3.5-mini (2.23GB on disk) hit 4.3GB. Plan for 1.5-2x model size when sizing your machine.

Also: if you're using llama.cpp with Phi-3.5-mini and hit a segfault immediately, the fix is `-c 2048`. Phi's default context window is 128k tokens — llama.cpp tries to pre-allocate that KV cache, and it immediately OOMs on an 8GB machine. Took me a few hours to track that one down.

**What the CPU actually does**

Both models came in at around 66.7% overall accuracy on the smoke test. Inference speed is ~10 tokens/sec on CPU. To put that in perspective: a 150-word response takes about 20-25 seconds. Fine for batch jobs, not great for interactive use.

| Model | Accuracy | Avg Latency | Peak RAM | Gen Speed |
|-------|----------|-------------|----------|-----------|
| Phi-3.5-mini Q4_K_M | 66.7% | 14.8s | 4,324 MB | ~9 t/s |
| Qwen2.5-3B Q4_K_M | 66.7% | 13.2s | 3,426 MB | ~11 t/s |

Same accuracy, but Qwen is faster (1.1x) and uses 20% less RAM. If you're running on constrained hardware, Qwen is the better pick just on RAM alone.

**What actually works vs what doesn't**

Across 10 task categories (30 prompts total), the pattern was consistent:

Works reliably:
- Classification: exact-label output, single-word responses — both models handle this well
- Code generation: syntactically valid Python functions — 100% on both models
- Knowledge QA: answering questions from provided context paragraphs — 86.7% on both

Doesn't work:
- Trick reasoning: "A farmer has 17 sheep. All but 9 die. How many are left?" — both models compute 17-9=8 instead of reading "all but 9 survive." 0% on the CPU smoke test.
- Structured planning: generating ordered multi-step task sequences — hit-or-miss, especially for Phi

The model matters for reasoning: on GPU (Colab T4, same prompts), Qwen hit 100% on reasoning and classification. Phi stayed at 0% on both. So it's not just "3B models can't reason" — it's more specific than that. Phi's chat template causes it to over-generate around constrained-output tasks.

**GPU comparison (if you have one)**

Ran the same benchmark on a Colab T4 to see what a GPU buys you:

| Model | CPU tok/s | GPU tok/s | Speedup |
|-------|-----------|-----------|---------|
| Phi-3.5-mini | ~9 | ~52 | 5.5x |
| Qwen2.5-3B | ~11 | ~48 | 3.3x |

3-6x faster on GPU. For interactive use, GPU makes the difference. For nightly batch jobs on constrained hardware, CPU is fine.

**Model recommendation**

Qwen2.5-3B over Phi-3.5-mini if you're running CPU-only:
- 20% less RAM at runtime (matters a lot when you have 8GB total)
- Slightly faster (~11 t/s vs ~9 t/s)
- Significantly better accuracy on constrained-output tasks (classification, reasoning)

Neither model meets a production-quality bar (I set a gate of >=80% overall with no category below 70%) — but for home automation tasks like classifying events, generating short scripts, or extracting structured data from text, they're genuinely useful.

Full write-up with all results tables, the CARS efficiency metric, and reproduction instructions: https://rishavchatterjee.com/blog/cars-benchmark

---

Anyone running local LLMs on similar hardware for home automation or self-hosted services? What tasks do you actually delegate to them? Curious whether classification and simple code gen are the main use cases for others, or if people are doing something more interesting with constrained hardware.

---

*Repo: github.com/rishav1305/soul-bench — clone it, run setup-titan.sh, and you can reproduce the full benchmark on your own hardware.*
