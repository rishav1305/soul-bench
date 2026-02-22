# soul-moa-integration

> Drop-in soul-os replacement layer with identical function signatures.

| Field | Value |
|-------|-------|
| Type | **PRIVATE** |
| Category | Bridge |
| Status | Scaffolded |
| Location | `~/soul/soul-moa/src/soul_moa/integration/` |
| License | Proprietary |

## What It Is

The bridge that connects soul-moa to soul-os. Exposes the exact same function signatures as `brain/claude_client.py` so that soul-os can switch from Claude API to local models with 3-4 import changes and zero code modifications.

## Integration Map

| soul-os File | soul-moa Replacement |
|---|---|
| `brain/claude_client.py` | `soul_moa.integration.soul_os_client` |
| `brain/llm/router.py` | `soul_moa.integration.soul_os_router` |
| `brain/llm/classifier.py` | `soul_moa.integration.soul_os_classifier` |
| `brain/agents/registry.py` (lines 58, 67, 76) | Change import path |

## Migration Steps

```python
# Before (soul-os)
from brain.claude_client import ask_claude, ask_agentic, classify_untrusted

# After (soul-moa)
from soul_moa.integration.soul_os_client import ask_claude, ask_agentic, classify_untrusted
# Same function signatures, same return types, same behavior
```

### Gradual Phase-Out Strategy

1. **Phase 1**: Local model as primary, Claude API as fallback (via soul-moa-failsafe)
2. **Phase 2**: Monitor accuracy retention per task type (via soul-moa-telemetry)
3. **Phase 3**: At 90%+ retention across all 10 task types, remove Claude fallback

## Strategic Value

Private because it's soul-os-specific glue code. The value is in enabling the Claude -> local model migration without breaking the production system.
