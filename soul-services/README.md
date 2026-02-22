# soul-services

> Docker orchestration for companion services (Vaultwarden, Gitea, Uptime Kuma).

| Field | Value |
|-------|-------|
| Type | **PRIVATE** |
| Category | DevOps |
| Status | Production (in soul-os) |
| Source | `~/soul-os/deploy/docker/` |
| License | Proprietary |

## What It Is

Docker Compose configurations for companion services that soul-os manages: Vaultwarden (password manager), Gitea (git hosting), and Uptime Kuma (monitoring). Each service has resource limits, SQLite backends, and is monitored by the healing module for automatic recovery.

## Services

| Service | Purpose | Memory Limit |
|---------|---------|-------------|
| Vaultwarden | Secret/password backup store | 128MB |
| Gitea | SQLite-backed git hosting | 256MB |
| Uptime Kuma | Passive monitoring dashboard | 128MB |

### Components

| File | Purpose |
|------|---------|
| deploy/docker/vaultwarden/docker-compose.yml | Vaultwarden compose |
| deploy/docker/gitea/docker-compose.yml | Gitea compose |
| deploy/docker/uptime-kuma/docker-compose.yml | Uptime Kuma compose |
| scripts/restore-docker-service.sh | Idempotent volume restore (integrity check, allowlist) |
| brain/api/docker_services.py | Read-only Docker services status API |

### Key Features

- Resource-constrained (fits on Raspberry Pi alongside soul-os)
- Healing module monitors container health
- Idempotent restore script with integrity checks
- Read-only status API endpoint

## Strategic Value

Shows operational maturity — not just running soul-os but managing a suite of companion services with resource constraints on limited hardware.
