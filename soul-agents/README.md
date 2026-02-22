# soul-agents

> YAML-configured AI agents with code-level boundary enforcement.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Framework |
| Status | Spec Only (code in soul-os) |
| Source | `~/soul-os/brain/agents/` + `~/soul-os/brain/tools/` |
| Target | `~/projects/public/soul-agents/` |
| License | MIT |

## What It Is

A framework for defining AI agents via YAML configuration with code-level (not prompt-level) boundary enforcement. Each agent declares which tools it can use, what permission mode it operates in, and what system prompt it receives. The tool executor enforces boundaries at runtime — an agent declared with `network_ok: false` physically cannot make network calls.

## YAML Agent Definition

```yaml
name: system_agent
description: Monitors and maintains system health
tools:
  - Bash
  - Read
  - Glob
  - Grep
permission_mode: bypassPermissions
max_turns: 10
system_prompt: |
  You are the system agent for Soul-OS.
  Monitor CPU, memory, disk, network, and running services.
  Critical thresholds: disk >85%, CPU temp >80C, memory >90%.
```

## Architecture

```
YAML Definition -> Agent Registry -> Agent Factory -> Tool Executor
                                                         |
                                                  Boundary Check
                                                  (device_ok / network_ok / workspace_ok)
```

### Components

| File | Purpose |
|------|---------|
| registry.py | Agent factory + YAML loader |
| prompts/*.yaml | Agent definitions (system, copywriter, researcher, knowledge, social_writer, proposal_writer) |
| tools/tool_executor.py | Tool execution with boundary enforcement |

### Key Design Decisions

- **Code-level boundaries**: Not prompt-based ("please don't do X") but code-enforced (physically cannot do X)
- **YAML configuration**: Non-engineers can define agent capabilities
- **Tool allowlists**: Each agent declares exactly which tools it can use
- **Permission modes**: `bypassPermissions` for autonomous, `acceptEdits` for interactive

## Strategic Value

**Top portfolio piece for AI safety roles.** Boundary enforcement is directly relevant to Anthropic's safety work. Demonstrates that you think about AI safety as an engineering problem, not just a prompting problem.

## Extraction Plan

1. Copy `brain/agents/` and `brain/tools/` to standalone repo
2. Create standalone `AgentRunner` class (replaces dependency on FastAPI app)
3. Add `pip install soul-agents` with working example
4. Publish YAML schema documentation
