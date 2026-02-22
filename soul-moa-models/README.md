# soul-moa-models

> Universal model client abstraction: OpenAI-compatible, Anthropic fallback, local inference.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Library |
| Status | Scaffolded |
| Location | `~/soul/soul-moa/src/soul_moa/models/` |
| License | MIT |

## What It Is

A unified client interface that abstracts away model provider differences. Supports any OpenAI-compatible API (llama-server, vLLM, Ollama, OpenAI), Anthropic Claude API, and local inference runtimes (MLX). Same function signature regardless of backend.

## Architecture

```
ModelClient (abstract)
    |
    ├── OpenAICompatClient    # llama-server, vLLM, Ollama, OpenAI
    ├── AnthropicClient       # Claude API (Haiku, Sonnet, Opus)
    └── LocalClient           # MLX native inference
```

### Key Design Decisions

- **OpenAI-compatible as universal interface**: Most local model servers (llama-server, vLLM, Ollama) expose OpenAI-compatible endpoints
- **Streaming-first**: All clients return async iterators
- **Token counting**: Track input/output tokens for cost and context management
- **Model tiers**: Chat (fast/cheap), Code (balanced), Reason (complex) — each tier maps to different backends

### Model Tier Mapping

| Tier | Replaces | Local Models | Fallback |
|------|----------|-------------|----------|
| Chat | Claude Haiku | Qwen3-4B-A2B, Phi-4-mini | Claude Haiku |
| Code | Claude Sonnet | Qwen3-30B-A3B, DeepSeek-Coder-V3-Lite | Claude Sonnet |
| Reason | Claude Opus | DeepSeek-R1-Distill-32B, Qwen-QwQ-32B | Claude Opus |

## Strategic Value

Model client abstraction is a common pattern but doing it well (with streaming, token counting, and tier routing) shows production ML engineering skills.
