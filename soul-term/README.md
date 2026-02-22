# soul-term

> Click-based CLI for setup, daemon management, deployment, and mesh operations.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | App |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/cli/` |
| License | MIT |

## What It Is

The unified command-line interface for soul-os. Handles first-time setup (venv, deps, daemon registration), daemon lifecycle (start/stop/restart), container mode (podman/docker/nerdctl), cloud deployment (Fly.io), mesh operations (link/status), and system updates with rollback.

## Commands

```bash
# Setup & lifecycle
soul-os setup              # First-time installation wizard
soul-os start / stop / restart / status / logs

# Container mode
soul-os container setup / status / stop / start / logs / update

# Cloud deploy
soul-os deploy fly         # Deploy to Fly.io

# Mesh
soul-os mesh link          # Link device to account
soul-os mesh status        # Show mesh topology

# Maintenance
soul-os update             # GitHub release check, semver compare, rollback
soul-os reset              # Wipe data (confirmation + backup)
soul-os uninstall          # Daemon deregistration
```

### Components

| File | Purpose |
|------|---------|
| main.py | Click entry point (console_scripts) |
| daemon.py | start/stop/restart/status/logs (systemd + launchd) |
| setup_cmd.py | Universal installer: venv, deps, .env, daemon, health check |
| platform.py | Platform detection (Linux/macOS/Pi/systemd/launchd) |
| runtime.py | Venv creation, dependency installation, Claude CLI detection |
| service_installer.py | systemd unit + launchd plist generation |
| container.py | Container CLI (podman/docker/nerdctl auto-detection) |
| deploy_cmd.py | Fly.io deploy (flyctl, secrets via stdin) |
| connect.py | Connect mode: remote server URL validation |
| update_cmd.py | GitHub release check, semver comparison, rollback |
| reset_cmd.py | Reset with confirmation, backup, symlink protection |
| uninstall_cmd.py | Daemon deregistration |
| mesh_cmd.py | Mesh link/status |

## Strategic Value

Demonstrates CLI design, cross-platform support (systemd/launchd), and installer engineering. Works headless for SSH access to Pi/server.
