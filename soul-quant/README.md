# soul-quant

> Quantization pipelines for GGUF, AWQ, and MLX formats.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Research Tool |
| Status | Scaffolded |
| Location | `~/soul/soul-moe/src/soul_moe/quantization/` |
| License | MIT |

## What It Is

Quantization pipelines that convert full-precision models into efficient formats for local inference. Supports three targets: GGUF (llama.cpp, cross-platform), AWQ (vLLM, cloud GPU), and MLX (Apple Silicon native). Automated quality comparison ensures quantization doesn't degrade accuracy below thresholds.

## Quantization Formats

| Format | Runtime | Target Hardware | Primary Quant |
|--------|---------|----------------|---------------|
| GGUF | llama.cpp / llama-server | Mac, Linux, Pi | Q4_K_M |
| AWQ | vLLM | Cloud GPU (A100, H100) | 4-bit |
| MLX | MLX framework | Apple Silicon (Metal) | 4-bit |

## Pipeline

```
Full-precision model (HuggingFace)
    |
    ├── GGUF Q4_K_M -> benchmark -> CARS score
    ├── AWQ 4-bit -> benchmark -> CARS score
    └── MLX 4-bit -> benchmark -> CARS score
    |
    v
Compare: which format retains most accuracy?
    |
    v
Best format -> soul-registry (if passes deploy gate)
```

### Deploy Gate

Models must pass before deployment:
- Overall accuracy retention >= 80% vs full-precision
- No single task below 70% accuracy
- P95 latency < 5 seconds (500-token output)
- Fits in memory budget (tier-specific)

## Strategic Value

**Shows ML depth beyond just using APIs.** Quantization pipeline demonstrates understanding of model compression, inference optimization, and quality-cost tradeoffs. Directly relevant to Google, Meta, Mistral roles.
