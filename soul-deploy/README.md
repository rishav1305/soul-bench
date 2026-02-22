# soul-deploy

> Deployment tooling: systemd services, Fly.io, cloud-init, OS image builder, auto-updates.

| Field | Value |
|-------|-------|
| Type | **PRIVATE** |
| Category | DevOps |
| Status | Production (in soul-os) |
| Source | `~/soul-os/deploy/` |
| License | Proprietary |

## What It Is

The complete deployment infrastructure for soul-os. Covers systemd service units (hardened), Fly.io cloud deployment, Raspberry Pi OS image building with cloud-init, Cloudflare Tunnel support, and automated weekly updates with rollback.

## Components

### systemd Units

| Unit | Purpose |
|------|---------|
| soul-os.service | Main service (hardened, non-root) |
| soul-os-tunnel.service | Cloudflare Tunnel (optional remote access) |
| soul-os-monitor.timer | Health check every 5 min |
| soul-os-backup.timer | Crash-consistent SQLite backup daily at 02:00 |
| soul-os-nightly.timer | Nightly intelligence cycle at 02:30 |
| soul-os-content.timer | Bi-weekly content flywheel |
| soul-os-update.timer | Weekly auto-update (randomized delay) |
| soul-os-sudoers | Scoped sudo: only systemctl restart soul-os |

### Cloud Deploy

| File | Purpose |
|------|---------|
| fly.toml | Fly.io config (SOUL_RUNTIME_MODE=cloud) |
| Dockerfile | Multi-stage, multi-arch (non-root, cap-drop, healthcheck) |
| docker-compose.yml | Headless container option |

### OS Image Builder

| File | Purpose |
|------|---------|
| image/build-image.sh | Ubuntu + cloud-init -> .img.gz (SHA-256 verified) |
| image/cloud-init/user-data | Hardened first-boot (scoped sudoers, UFW, Avahi mDNS) |
| .github/workflows/build-image.yml | ARM64 image build on release |

### CI/CD

| Workflow | Purpose |
|----------|---------|
| build-docker.yml | Multi-arch Docker to GHCR on push/tags |
| build-image.yml | OS image on release |
| build-desktop.yml | Tauri builds (macOS/Linux/Windows) |
| build-relay.yml | Relay Docker multi-arch to GHCR |

## Strategic Value

Demonstrates DevOps depth: systemd hardening, multi-arch Docker, cloud-init provisioning, CI/CD pipelines, and auto-update with rollback. The Pi deployment path (flash SD card -> boot -> works) shows installer engineering.
