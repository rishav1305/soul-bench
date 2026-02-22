# soul-registry

> Model cards, deploy gates, version tracking, and config export to soul-moa.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Research Tool |
| Status | Scaffolded |
| Location | `~/soul/soul-moe/src/soul_moe/registry/` |
| License | MIT |

## What It Is

A model registry that tracks every model variant (base, quantized, fine-tuned) with model cards, benchmark results, and deploy gate status. When a model passes the deploy gate, it exports a YAML config that soul-moa hot-reloads for serving.

## Pipeline

```
Model (quantized or fine-tuned)
    |
    v
Register with model card:
    - Base model, quantization format, fine-tuning details
    - Benchmark results (per-task accuracy, CARS score)
    - Resource requirements (VRAM, disk, latency)
    |
    v
Deploy Gate Check:
    - Overall accuracy >= 80% vs Claude baseline?
    - No single task below 70%?
    - P95 latency < 5s?
    - Fits in memory budget?
    |
    ├── PASS -> export YAML config to soul-moa
    └── FAIL -> logged, can retry after improvements
```

### Model Card Fields

- Model name, version, base model
- Quantization format (GGUF Q4_K_M, AWQ, MLX)
- Fine-tuning details (task, dataset size, epochs)
- Benchmark results (10 tasks + overall)
- CARS score
- Deploy gate status (pass/fail with reasons)
- Resource requirements

## Strategic Value

Model registry and deploy gates show ML governance practices. Not just training models but managing their lifecycle with quality gates.
