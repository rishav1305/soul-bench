# soul-relay

> Lightweight relay server for NAT traversal between mesh nodes.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Infrastructure |
| Status | Spec Only (code in soul-os) |
| Source | `~/soul-os/brain/relay/` |
| License | MIT |

## What It Is

A standalone FastAPI relay server that enables mesh nodes behind different NATs to communicate. It passes encrypted packets between nodes without seeing their content. Designed to run cheaply on Fly.io ($5/month).

## Architecture

```
Node A (behind NAT)     Relay Server (Fly.io)     Node B (behind NAT)
     │                       │                          │
     ├── register ──────────>│                          │
     │                       │<──────── register ───────┤
     │                       │                          │
     ├── encrypted msg ─────>│──── forward ────────────>│
     │<──── encrypted msg ───│<─────── reply ───────────┤
```

### Key Features

- JWT-authenticated WebSocket connections
- DB-backed node state (SQLite, separate from brain)
- Rate limiting per account
- Automatic node pruning (stale connections)
- Account-scoped routing (IDOR prevention via account_id JWT claims)
- Healthcheck endpoint

### Deployment

- Docker image: `deploy/relay/Dockerfile` (python:3.11-slim, non-root)
- Fly.io config: `deploy/relay/fly.toml` (iad region, 256MB, persistent /data volume)

## Strategic Value

Complements soul-mesh. Shows understanding of NAT traversal, relay architecture, and zero-trust networking.
