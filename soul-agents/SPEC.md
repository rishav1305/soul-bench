# soul-agents

## Overview
Agent framework with boundary enforcement — safe, constrained AI agents defined via YAML.

## Status
**Ready to Extract** | Source exists in soul-os

## Description
soul-agents provides a framework for building AI agents with explicit tool boundaries. Agents are defined declaratively in YAML with permitted tools, system prompts, and safety constraints. The boundary enforcement model ensures agents can only access approved capabilities.

## Key Components
- **Agent Registry**: Register and manage agents with capabilities
- **Tool Executor**: Execute tools within boundary constraints
- **YAML Agent Definitions**: Declarative agent configuration
- **Boundary Enforcement**: Restrict agent access to approved tools only
- **Prompt Templates**: Reusable prompt patterns for agents

## Source Files (from soul-os)
- `soul-os/brain/agents/registry.py`
- `soul-os/brain/tools/tool_executor.py`
- `soul-os/brain/agents/prompts/*.yaml`

## Extraction Plan
1. Copy agent framework files
2. Replace all `brain.*` imports
3. Create standalone configuration
4. Write clean README showing boundary enforcement model
5. Working example: YAML agent with tool boundaries
6. GitHub Actions CI
7. Publish to PyPI

## Portfolio Signal
Demonstrates AI safety thinking — boundary enforcement is directly relevant to Anthropic and safety-focused roles.

## Timeline
Sprint 1 (Week 1-2), parallel with soul-outreach Phase 1.
