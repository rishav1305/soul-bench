---
name: block-hardcoded-secrets
enabled: true
event: file
action: block
conditions:
  - field: new_text
    operator: regex_match
    pattern: (password|secret|api_key|token|credential)\s*=\s*["'][^"']{8,}["']
---

**Hardcoded secret detected!**

Never hardcode credentials in source code. Use environment variables with the project-specific prefix:
- soul-os: `SOUL_` prefix via `brain/config.py`
- soul-outreach: `OUTREACH_` prefix via `outreach/config.py`
- soul-moa: `SOUL_MOA_` prefix via `config/settings.py`
- soul-moe: `SOUL_MOE_` prefix via `.env`
