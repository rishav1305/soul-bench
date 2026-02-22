# soul-serve

> Multi-model serving: llama-server, vLLM, and MLX runtime configurations.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Infrastructure |
| Status | Scaffolded |
| Location | `~/soul/soul-moe/src/soul_moe/serving/` |
| License | MIT |

## What It Is

Serving configurations and management for running multiple local models simultaneously. Supports three runtimes: llama-server (llama.cpp, cross-platform), vLLM (cloud GPU, high throughput), and MLX (Apple Silicon native). All expose OpenAI-compatible endpoints for soul-moa to consume.

## Runtimes

| Runtime | Hardware | Best For | API |
|---------|----------|---------|-----|
| llama-server | Mac, Linux, Pi (CPU/GPU) | Single model, low overhead | OpenAI-compatible |
| vLLM | Cloud GPU (A100, H100) | High throughput, batching | OpenAI-compatible |
| MLX | Apple Silicon (Metal) | Native Mac inference | OpenAI-compatible |

## Multi-Model Serving

```
soul-serve manages multiple models simultaneously:

Port 8081: llama-server (Chat tier: Qwen3-4B-A2B, Q4_K_M)
Port 8082: llama-server (Code tier: Qwen3-30B-A3B, Q4_K_M)
Port 8083: llama-server (Reason tier: DeepSeek-R1-Distill-32B, Q4_K_M)
    |
    v
soul-moa connects to all three, routes by task_type
```

### Key Features

- **Process management**: Start/stop/restart individual model servers
- **Resource budgeting**: Ensure total VRAM usage fits available memory
- **Health checks**: Periodic ping to verify each server is responsive
- **Config-driven**: YAML configs per model (from soul-registry export)

### Hardware Target

Mac Studio M5 Max (128GB unified memory):
- Chat tier: ~4 GB
- Code tier: ~16 GB
- Reason tier: ~20 GB
- Total: ~40 GB, leaving 88 GB for OS + applications

## Strategic Value

Multi-model serving shows practical ML infrastructure skills. Managing resource budgets across multiple models on consumer hardware demonstrates efficiency-first thinking.
