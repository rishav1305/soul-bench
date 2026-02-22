# soul-os

> AI-native operating system powered by Claude Code.

| Field | Value |
|-------|-------|
| Type | **PRIVATE** |
| Category | Product |
| Status | Production (~v0.17) |
| Lines | ~6,700 Python + 3,000 React |
| Location | `~/soul-os/` |
| License | Proprietary |

## What It Is

Soul-OS is a self-installing, local-first AI operating system that runs on every device — desktop, laptop, Raspberry Pi, phone, or cloud VM. It creates its own isolated environment, manages its own runtimes, and works with or without internet.

One software. Install anywhere. Everything connects.

## Architecture

```
soul-os/
├── brain/                    # Python FastAPI backend
│   ├── main.py               # App + lifespan
│   ├── config.py             # Pydantic settings (SOUL_ prefix)
│   ├── claude_client.py      # All Claude calls (subprocess wrapper)
│   ├── autonomous_loop.py    # Background task scheduler
│   ├── api/                  # REST + WebSocket endpoints
│   ├── db/store.py           # Async SQLite (aiosqlite, WAL mode)
│   ├── agents/               # YAML-configured agents + registry
│   ├── tools/                # Tool executor with boundary enforcement
│   ├── llm/                  # Model router + intent classifier
│   ├── auth/                 # JWT + bcrypt
│   ├── mesh/                 # Multi-device networking
│   ├── relay/                # NAT traversal server
│   ├── cloud/                # Container provisioning
│   ├── modules/
│   │   ├── outreach/         # Email campaigns + consulting
│   │   ├── knowledge/        # ChromaDB semantic search
│   │   ├── healing/          # Self-healing + nightly intelligence
│   │   └── content/          # Content pipeline
│   └── cli/                  # Click-based CLI
├── frontend/                 # React PWA (8 pages, dark theme)
├── desktop/                  # Tauri v2 wrapper
├── deploy/                   # systemd, Docker, Fly.io, cloud-init
└── workspace/                # Claude's operational home (soul.db)
```

## Key Features (17 Phases)

- Phase 0-1: Foundation + knowledge base
- Phase 2: Brain layer (LLM router, tool executor, YAML agents)
- Phase 3: Growth outreach MVP (import, enrich, draft, review, send)
- Phase 4: Backend API + JWT auth + WebSocket bridge
- Phase 5: Frontend UI (React SPA, dark theme, 8 pages)
- Phase 6: Remote access (Tailscale, Cloudflare Tunnel, UFW)
- Phase 7: Domain knowledge (ChromaDB semantic search, CVE scanner)
- Phase 8: Self-healing (DB-backed remediation, hysteresis, nightly intelligence)
- Phase 9: Selective service restore (Docker container health monitoring)
- Phase 10: Content pipeline (research ingestion, social drafts)
- Phase 11: Consulting pipeline (leads, discovery, proposals, engagements)
- Phase 12: CLI packaging (click, pyproject.toml, console_scripts)
- Phase 13: Universal installer (venv, deps, daemon, launchd/systemd)
- Phase 14: Multi-platform (container CLI, Fly.io deploy, setup wizard, OS image)
- Phase 15: Desktop app + PWA (Tauri v2, service worker, offline support)
- Phase 16: Mesh architecture (hub election, WebSocket transport, device linking)
- Phase 17: Cloud infrastructure (relay server, container provisioner, auto-updater)

## Tech Stack

- **Backend**: Python 3.11, FastAPI, aiosqlite, claude-agent-sdk
- **Frontend**: React 18, Vite, WebSocket streaming
- **Desktop**: Tauri v2 (Rust shell, ~5MB binary)
- **Database**: SQLite (WAL mode) + ChromaDB (vectors)
- **Deployment**: systemd, Docker, Fly.io, cloud-init
- **Auth**: JWT (short-lived access + long-lived refresh), bcrypt

## Strategic Value

The flagship product that everything else supports. Demonstrates full-stack engineering, systems design, and product thinking. All other soul-* projects were extracted from or integrate with soul-os.
