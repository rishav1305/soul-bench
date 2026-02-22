---
name: warn-cross-project-import
enabled: true
event: file
action: warn
conditions:
  - field: new_text
    operator: regex_match
    pattern: from brain\.|import brain\.
  - field: file_path
    operator: not_contains
    value: soul-os
---

**Cross-project import detected!**

You're importing from `brain.*` outside of soul-os. The `brain` package is internal to soul-os.

Use the standalone extracted module instead:
- `brain.modules.outreach.*` -> `outreach.*` (soul-outreach)
- `brain.agents.*` -> `soul_agents.*` (soul-agents)
- `brain.mesh.*` -> `soul_mesh.*` (soul-mesh)
- `brain.modules.healing.*` -> `soul_heal.*` (soul-heal)
- `brain.auth.*` -> `soul_auth.*` (soul-auth)
- `brain.claude_client.*` -> `outreach.agents.client` or `soul_moa.core.*`
