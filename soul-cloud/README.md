# soul-cloud

> Container-per-user PaaS with Docker isolation and Traefik routing.

| Field | Value |
|-------|-------|
| Type | **PRIVATE** |
| Category | Product |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/cloud/` |
| License | Proprietary |

## What It Is

A cloud provisioner that creates isolated Docker containers per user with automatic subdomain routing via Traefik. Each user gets their own soul-os instance with resource limits, env-file secrets, and health monitoring.

## Components

| File | Purpose |
|------|---------|
| provisioner.py | Docker CLI wrapper: provision, deprovision, list, status |
| api/cloud.py | Admin-only REST API with container count limits |
| deploy/cloud/docker-compose.yml | Traefik + docker-socket-proxy (read-only) |

### Key Features

- Container-per-user isolation (no shared processes)
- Env-file secrets injection (not CLI args)
- Resource limits (memory, CPU)
- Traefik labels for automatic subdomain routing
- Admin-only API (IDOR prevention)
- Container count limits per account

## Strategic Value

Enables the managed cloud offering at soul-os.app. Demonstrates container orchestration, multi-tenant isolation, and PaaS architecture.
