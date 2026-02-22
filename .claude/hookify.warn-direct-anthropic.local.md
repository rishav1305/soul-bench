---
name: warn-direct-anthropic
enabled: true
event: file
action: warn
conditions:
  - field: new_text
    operator: regex_match
    pattern: anthropic\.Anthropic\(|client\.messages\.create\(|from anthropic import|import anthropic
---

**Direct Anthropic SDK usage detected!**

All Anthropic API calls MUST go through centralized client modules:
- **soul-os**: `brain/claude_client.py` (subprocess wrapper + direct SDK)
- **soul-outreach**: `outreach/agents/client.py` (dual-mode: CLI + SDK)
- **soul-moa**: `core/tool_registry.py` (boundary-enforced execution)

This ensures: untrusted content isolation, consistent error handling, audit logging, cost tracking.
