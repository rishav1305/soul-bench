# soul-moa-core

> Agent SDK primitives: agent loop, tool registry, boundary enforcement, streaming, context management.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Framework |
| Status | Scaffolded |
| Location | `~/soul/soul-moa/src/soul_moa/core/` |
| License | MIT |

## What It Is

The foundational agent SDK that provides the building blocks for AI agent systems. Defines the agent loop (observe -> think -> act -> observe), tool registration with type-safe schemas, code-level boundary enforcement, streaming response handling, and context window management.

## Core Abstractions

```python
# Agent loop
class Agent:
    async def run(self, prompt: str) -> AsyncIterator[Message]:
        while not done:
            observation = await self.observe()      # gather context
            thought = await self.think(observation)  # LLM call
            action = await self.act(thought)         # tool execution
            yield action

# Tool registry
class ToolRegistry:
    def register(self, name: str, handler: Callable, schema: dict): ...
    def execute(self, name: str, args: dict) -> Result: ...
    def check_boundary(self, name: str, agent: Agent) -> bool: ...

# Boundary enforcement
class Boundary:
    device_ok: bool    # can access device resources
    network_ok: bool   # can make network calls
    workspace_ok: bool # can modify workspace files
```

### Key Design Decisions

- **Code-level boundaries**: Tool execution physically blocked, not prompt-asked
- **Streaming-first**: All agent responses are async iterators
- **Framework-agnostic**: No dependency on FastAPI or any specific web framework
- **Composable**: Agents can delegate to sub-agents with tighter boundaries

## Strategic Value

**Clean SDK design is the foundation for everything else in soul-moa.** Demonstrates framework architecture skills. The boundary enforcement pattern is directly relevant to AI safety engineering.
