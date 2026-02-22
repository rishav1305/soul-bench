# soul-moa-telemetry

> Observability: Prometheus metrics, structured logging, and feedback logging for model training.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Library |
| Status | Scaffolded |
| Location | `~/soul/soul-moa/src/soul_moa/telemetry/` |
| License | MIT |

## What It Is

An observability layer that captures metrics (request latency, token usage, error rates), structured logs (JSON with correlation IDs), and feedback data (prompt/response pairs with quality scores) for fine-tuning via soul-moe.

## Components

### Prometheus Metrics

- `soul_moa_request_duration_seconds` — histogram by model, task_type
- `soul_moa_tokens_total` — counter by model, direction (input/output)
- `soul_moa_errors_total` — counter by model, error_type
- `soul_moa_circuit_breaker_state` — gauge by model (0=closed, 1=open, 0.5=half-open)
- `soul_moa_moa_layer_duration_seconds` — histogram by layer (proposer, aggregator)

### Structured Logging

JSON logs with: timestamp, correlation_id, model, task_type, tokens_in, tokens_out, latency_ms, status.

### Feedback Logging

```json
{
  "prompt": "...",
  "response": "...",
  "model": "qwen3-30b-a3b",
  "task_type": "code",
  "quality_score": 0.85,
  "timestamp": "2026-02-21T12:00:00Z"
}
```

Feedback is consumed by soul-moe as fine-tuning training data, closing the feedback loop.

## Strategic Value

Demonstrates production observability practices. The feedback loop to soul-moe (telemetry -> training data) shows closed-loop ML engineering.
