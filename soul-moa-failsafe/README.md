# soul-moa-failsafe

> Production resilience: circuit breakers, fallback chains, retry policies, health monitoring.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Library |
| Status | Scaffolded |
| Location | `~/soul/soul-moa/src/soul_moa/failsafe/` |
| License | MIT |

## What It Is

A resilience library for AI model serving. Provides circuit breakers (stop calling a failing model), fallback chains (local model -> Claude API -> cached response), retry policies (exponential backoff with jitter), and health monitoring for all model backends.

## Patterns

```
Request -> Circuit Breaker Check
    |
    ├── Circuit CLOSED (healthy) -> try primary model
    |       |
    |       ├── Success -> return response
    |       └── Failure -> increment failure count
    |                       |
    |                       └── threshold reached -> OPEN circuit
    |
    ├── Circuit OPEN (failing) -> skip to fallback chain
    |       |
    |       └── after cooldown -> HALF-OPEN (try one request)
    |
    └── Fallback Chain:
         1. Local model (llama-server)
         2. Claude API (Anthropic SDK)
         3. Cached response (if available)
         4. Graceful error
```

### Key Components

- **CircuitBreaker**: Per-model circuit with configurable failure threshold and cooldown
- **FallbackChain**: Ordered list of providers, tries each until one succeeds
- **RetryPolicy**: Exponential backoff with jitter, max retries, timeout
- **HealthMonitor**: Periodic health checks for all backends, updates circuit state

## Strategic Value

Production resilience patterns are table stakes for senior engineering roles. Shows that you think about failure modes, not just happy paths. Relevant to any infrastructure or platform role.
