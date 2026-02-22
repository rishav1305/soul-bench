# Soul Architecture — How Everything Connects

## The Three Pillars

```
soul-moe (Research Lab)                    soul-moa (Agent SDK)
~/projects/public/soul-moe/                ~/projects/public/soul-moa/
┌─────────────────────────┐                ┌─────────────────────────┐
│ Selection (CARS scoring) │                │ Core (agent loop, tools) │
│ Quantization (GGUF/AWQ) │  model configs │ MoA (proposer/aggregator)│
│ Fine-tuning (LoRA/QLoRA)│ ─────────────> │ Failsafe (circuit break) │
│ Benchmarks (10 tasks)   │                │ Models (universal client) │
│ Evaluation (vs Claude)  │ <───────────── │ Telemetry (metrics, logs) │
│ Registry (deploy gates) │  feedback logs │ Integration (soul-os shim)│
└─────────────────────────┘                └────────────┬────────────┘
                                                        │
                                           drop-in replacement
                                           (3-4 import changes)
                                                        │
                                                        v
                                           soul-os (Operating System)
                                           ~/soul-os/
                                           ┌─────────────────────────┐
                                           │ Brain (FastAPI + Claude) │
                                           │ Modules (outreach, heal) │
                                           │ Mesh (multi-device)      │
                                           │ Frontend (React PWA)     │
                                           │ CLI (setup, deploy)      │
                                           └────────────┬────────────┘
                                                        │
                                                        v
                                           Users (web / desktop / terminal / mobile)
```

## Data Flows

### soul-moe -> soul-moa (Model Pipeline)

1. soul-moe screens model candidates using CARS metric
2. Top candidates are quantized (GGUF Q4_K_M for Mac, AWQ for cloud)
3. Fine-tuned on soul-os task data (10 categories)
4. Must pass deploy gate: >=80% accuracy vs Claude, P95 latency <5s
5. Passing models exported as YAML config to soul-moa
6. soul-moa hot-reloads new model configs without restart

### soul-moa -> soul-os (Integration)

Drop-in replacement — identical function signatures:

| soul-os File | soul-moa Replacement |
|---|---|
| `brain/claude_client.py` | `soul_moa.integration.soul_os_client` |
| `brain/llm/router.py` | `soul_moa.integration.soul_os_router` |
| `brain/llm/classifier.py` | `soul_moa.integration.soul_os_classifier` |
| `brain/agents/registry.py` (3 imports) | Change `claude_client` -> `soul_os_client` |

Gradual phase-out strategy:
1. Local model as primary, Claude API as fallback
2. Monitor accuracy retention per task type
3. At 90%+ retention across all tasks, remove Claude fallback

### soul-moa -> soul-moe (Feedback Loop)

1. soul-moa logs every request: prompt, response, latency, quality score
2. Feedback stored as structured JSON in telemetry output
3. soul-moe uses feedback as fine-tuning training data
4. Closed loop: better models -> better responses -> better training data

## Extraction Pattern

How to extract a soul-os module into a standalone repo:

1. **Identify boundary** — Find the module directory in soul-os (e.g., `brain/mesh/`)
2. **Map dependencies** — What does the module import from brain/*?
3. **Copy files** — Create new repo with src/ structure
4. **Replace imports** — Change `brain.db.store` -> standalone config, `brain.config` -> pydantic-settings
5. **Add standalone config** — Pydantic settings class with env var support
6. **Write README** — Architecture diagram, install, usage, examples
7. **Add CI** — GitHub Actions: lint, test, type check
8. **Publish** — PyPI package with `pyproject.toml`

## soul-os Module Map

What stays in the monolith vs what gets extracted:

| Module | Path | Decision | Reason |
|--------|------|----------|--------|
| Agents + Tools | brain/agents/, brain/tools/ | **EXTRACT** -> soul-agents | Strong portfolio piece, reusable |
| Mesh + Relay | brain/mesh/, brain/relay/ | **EXTRACT** -> soul-mesh | Strong portfolio piece, reusable |
| Outreach | brain/modules/outreach/ | **EXTRACTED** -> soul-outreach | Revenue product |
| Consulting | brain/modules/outreach/consulting.py | **EXTRACT** -> soul-outreach | Part of outreach product |
| Knowledge | brain/modules/knowledge/ | **STAYS** | Tightly coupled to soul-os workflows |
| Healing | brain/modules/healing/ | **STAYS** | soul-os specific (systemd, service management) |
| Content | brain/modules/content/ | **STAYS** | Depends on knowledge + outreach modules |
| Auth/JWT | brain/auth/ | **STAYS** | Standard pattern, not unique enough to extract |
| LLM Router | brain/llm/ | **REPLACED** by soul-moa | soul-moa integration replaces this |
| Cloud | brain/cloud/ | **FUTURE** -> soul-cloud | Extract when cloud product is prioritized |
| CLI | brain/cli/ | **STAYS** | soul-os specific installer/daemon management |

## Hardware Targets

| Device | Role | Specs |
|--------|------|-------|
| Raspberry Pi (titan-pi) | Production soul-os host | ARM64, Ubuntu Server, systemd |
| Mac Studio M5 Max | Model inference (soul-moe/moa) | 128GB unified, 40-core GPU, Metal |
| Cloud VMs (Fly.io) | Hosted soul-os + relay server | Variable, Docker containers |
| User devices | mesh nodes | Anything: desktop, laptop, phone, tablet |

## soul-os Internal Architecture

```
soul-os/
├── brain/                    # Python FastAPI backend
│   ├── main.py               # App + lifespan
│   ├── config.py             # Pydantic settings
│   ├── claude_client.py      # All Claude calls (will be replaced by soul-moa)
│   ├── autonomous_loop.py    # Background task scheduler
│   ├── api/                  # REST + WebSocket endpoints
│   ├── db/store.py           # Async SQLite (aiosqlite, WAL mode)
│   ├── agents/               # YAML agent definitions + registry
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
├── image/                    # OS image builder for Pi
├── scripts/                  # Install, backup, monitor
└── workspace/                # Claude's operational home (soul.db, CLAUDE.md)
```

## Key Design Decisions

1. **Single SQLite DB** — One `soul.db` for all state. WAL mode for mesh sync.
2. **Claude as callable service** — `claude-agent-sdk` Python package, not raw subprocess
3. **CLAUDE.md = auto context** — Placed in workspace/, Claude reads it automatically
4. **Modules pattern** — Register routes, tables, agents on startup. Feature flags via env vars.
5. **Frontend served by FastAPI** — React builds to static/, one process, one port
6. **Environment-driven config** — Same brain code runs on Pi, Mac, Android, cloud VM
7. **Mesh is additive** — Single device = mesh of one, same code path
