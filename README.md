# Soul AI

> One AI that runs everywhere, manages itself, and grows with you.

## What is Soul AI?

Soul AI is a local-first, self-hosting AI platform that runs on every device — desktop, laptop, phone, Raspberry Pi, or cloud. It creates its own isolated environment, connects multiple devices into one unified system, and works with or without internet.

Unlike cloud-only AI products, Soul AI runs on **your** hardware. Your data stays local. Multiple devices pool their resources and act as one machine through mesh networking.

## Architecture

```
soul-moe (Research)          soul-moa (Agent SDK)         soul-os (Platform)
trains & quantizes    -->    serves local models    -->   runs the AI OS
open-source models          with Claude fallback         on any device
                     <--                            <--
                     feedback for training           user interactions
```

---

## All 31 Projects

### From soul-os — Core Platform (18 projects)

| # | Project | Type | Category | Description |
|---|---------|------|----------|-------------|
| 1 | [soul-os](soul-os/) | Private | Product | AI-native OS — 6,700 Python + 3,000 React, 17 phases |
| 2 | [soul-mesh](soul-mesh/) | Public | Infrastructure | Distributed mesh: hub election, WebSocket sync, NAT relay |
| 3 | [soul-relay](soul-relay/) | Public | Infrastructure | Standalone NAT traversal relay server |
| 4 | [soul-knowledge](soul-knowledge/) | Private | Product | Semantic search: ChromaDB + SQLite FTS, CVE scanner |
| 5 | [soul-outreach](soul-outreach/) | Dual | Product | Email campaign platform with full lifecycle |
| 6 | [soul-cloud](soul-cloud/) | Private | Product | Container-per-user PaaS with Traefik routing |
| 7 | [soul-consult](soul-consult/) | Private | Product | Consulting CRM: leads, discovery, proposals |
| 8 | [soul-agents](soul-agents/) | Public | Framework | YAML-configured agents with code-level boundary enforcement |
| 9 | [soul-heal](soul-heal/) | Public | Framework | Self-healing: DB-backed remediation, hysteresis |
| 10 | [soul-auth](soul-auth/) | Public | Library | JWT + token family replay detection |
| 11 | [soul-loop](soul-loop/) | Public | Framework | Autonomous task scheduler with module tick system |
| 12 | [soul-soc](soul-soc/) | Public | Library | Security operations: CVE scanning, security knowledge base |
| 13 | [soul-content](soul-content/) | Private | Product | Content pipeline: research ingestion, social drafts |
| 14 | [soul-web](soul-web/) | Public | App | React 19 PWA: 8 pages, dark theme, WebSocket streaming |
| 15 | [soul-desktop](soul-desktop/) | Public | App | Tauri v2 cross-platform desktop app |
| 16 | [soul-term](soul-term/) | Public | App | Click-based CLI: setup, deploy, mesh |
| 17 | [soul-services](soul-services/) | Private | DevOps | Docker orchestration: Vaultwarden, Gitea, Uptime Kuma |
| 18 | [soul-deploy](soul-deploy/) | Private | DevOps | systemd + Fly.io + Pi: cloud-init, OS images, auto-update |

### From soul-moa — Agent SDK (6 projects)

| # | Project | Type | Category | Description |
|---|---------|------|----------|-------------|
| 19 | [soul-moa-core](soul-moa-core/) | Public | Framework | Agent loop, tool registry, boundary enforcement, streaming |
| 20 | [soul-moa-orchestrator](soul-moa-orchestrator/) | Public | Framework | MoA proposer/aggregator — the key innovation |
| 21 | [soul-moa-failsafe](soul-moa-failsafe/) | Public | Library | Circuit breakers, fallback chains, retry policies |
| 22 | [soul-moa-models](soul-moa-models/) | Public | Library | Universal model client: OpenAI-compat, Anthropic, local |
| 23 | [soul-moa-telemetry](soul-moa-telemetry/) | Public | Library | Prometheus metrics, structured logging, feedback |
| 24 | [soul-moa-integration](soul-moa-integration/) | Private | Bridge | Drop-in soul-os replacement layer |

### From soul-moe — Model Research (7 projects)

| # | Project | Type | Category | Description |
|---|---------|------|----------|-------------|
| 25 | [soul-bench](soul-bench/) | Public | Research | 10-task benchmark suite + CARS metric |
| 26 | [soul-select](soul-select/) | Public | Research | Model candidate screening, CARS scoring, leaderboard |
| 27 | [soul-quant](soul-quant/) | Public | Research | GGUF/AWQ/MLX quantization pipelines |
| 28 | [soul-tune](soul-tune/) | Public | Research | MLX LoRA + Unsloth QLoRA fine-tuning |
| 29 | [soul-eval](soul-eval/) | Public | Research | Claude baseline comparison + statistical tests |
| 30 | [soul-registry](soul-registry/) | Public | Research | Model cards, deploy gates, config export |
| 31 | [soul-serve](soul-serve/) | Public | Infrastructure | Multi-model serving: llama-server, vLLM, MLX |

---

## Summary

| Metric | Count |
|--------|-------|
| Total projects | 31 |
| Public | 20 |
| Private | 9 |
| Dual (open core) | 2 |
| Production | 14 |
| Scaffolded | 13 |
| Has code | 1 |
| Spec only | 3 |

## Getting Started

```bash
curl -fsSL https://get.soul-os.dev | bash
soul-os setup
```

## Status

| Component | Status |
|-----------|--------|
| soul-os | Production (~v0.17, 17 phases) |
| soul-outreach | Extracted, has code |
| soul-moa | Architecture complete, scaffolded |
| soul-moe | Architecture complete, scaffolded |

## License

- **Public projects** (soul-mesh, soul-agents, soul-bench, etc.) — MIT
- **Dual projects** (soul-outreach) — MIT (core) + BSL (premium)
- **Private projects** (soul-os, soul-cloud, etc.) — Proprietary
