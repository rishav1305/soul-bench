# soul-tune

> Fine-tuning pipelines: MLX LoRA (Mac) and Unsloth QLoRA (cloud GPU).

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Research Tool |
| Status | Scaffolded |
| Location | `~/soul/soul-moe/src/soul_moe/finetuning/` |
| License | MIT |

## What It Is

Task-specific fine-tuning pipelines using LoRA (Low-Rank Adaptation) and QLoRA (Quantized LoRA). Two runtimes: MLX LoRA for on-device training on Apple Silicon, and Unsloth QLoRA for cloud GPU training on RunPod/Vast.ai A100s.

## Training Data Source

Training data comes from soul-os production usage via soul-moa-telemetry feedback logs:

```
soul-os usage -> soul-moa-telemetry (feedback logs)
    |
    v
Structured training data: {prompt, response, task_type, quality_score}
    |
    v
soul-tune: LoRA/QLoRA fine-tuning
    |
    v
Fine-tuned adapter -> benchmark -> deploy gate -> soul-registry
```

## Runtimes

| Runtime | Hardware | Best For |
|---------|----------|---------|
| MLX LoRA | Mac Studio M5 Max (128GB) | Quick iterations, small datasets |
| Unsloth QLoRA | Cloud A100 (RunPod/Vast.ai) | Large datasets, full fine-tuning runs |

### Key Design Decisions

- **Task-specific adapters**: One LoRA adapter per task category, not one giant fine-tune
- **Quality-gated**: Fine-tuned models must pass deploy gate before deployment
- **Feedback loop**: Production feedback -> fine-tuning data -> better models -> better feedback
- **Cost-conscious**: MLX for iteration, cloud GPU only for final training runs

## Strategic Value

**Shows training competence, not just inference.** Fine-tuning pipeline demonstrates understanding of LoRA, quantized training, and the full model improvement cycle. Relevant to OpenAI, Anthropic training infrastructure roles.
