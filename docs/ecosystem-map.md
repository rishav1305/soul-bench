# Soul Ecosystem Map

Single source of truth for all 31 extractable projects in the Soul AI ecosystem.

## Status Legend

| Status | Meaning |
|--------|---------|
| PRODUCTION | Running in production with real usage |
| HAS CODE | Scaffold + some implementation |
| SCAFFOLDED | Full directory structure (src/tests/configs), no code |
| SPEC ONLY | CLAUDE.md with project spec, no repo structure |

## Category Legend

| Category | Meaning | License |
|----------|---------|---------|
| OPEN | Open source, portfolio/credibility | MIT |
| PRIVATE | Private repo, monetization target | Proprietary |
| DUAL | Open core + premium features | MIT + BSL |

---

## A. From soul-os (18 Projects)

Extractable components from the production monolith at `~/soul-os/`.

| # | Project | Category | Status | Source Path | Description |
|---|---------|----------|--------|-------------|-------------|
| 1 | soul-os | PRIVATE | PRODUCTION | ~/soul-os/ | AI-native OS — 6,700 Python + 3,000 React, 17 phases |
| 2 | soul-mesh | OPEN | SPEC ONLY | brain/mesh/ + brain/relay/ | Distributed systems: hub election, WebSocket sync, NAT relay |
| 3 | soul-relay | OPEN | SPEC ONLY | brain/relay/ | Standalone NAT traversal relay server |
| 4 | soul-knowledge | PRIVATE | PRODUCTION | brain/modules/knowledge/ | Semantic search: ChromaDB + SQLite FTS, CVE scanner |
| 5 | soul-outreach | DUAL | HAS CODE | brain/modules/outreach/ | Email campaign platform: import, enrich, draft, review, send |
| 6 | soul-cloud | PRIVATE | PRODUCTION | brain/cloud/ | Container-per-user PaaS with Traefik routing |
| 7 | soul-consult | PRIVATE | PRODUCTION | brain/modules/outreach/consulting.py | Consulting CRM: leads, discovery, proposals, engagements |
| 8 | soul-agents | OPEN | SPEC ONLY | brain/agents/ + brain/tools/ | YAML-configured agents with code-level boundary enforcement |
| 9 | soul-heal | OPEN | PRODUCTION | brain/modules/healing/ | Self-healing: DB-backed remediation, hysteresis, nightly intelligence |
| 10 | soul-auth | OPEN | PRODUCTION | brain/auth/ | JWT + token family replay detection, bcrypt, refresh rotation |
| 11 | soul-loop | OPEN | PRODUCTION | brain/autonomous_loop.py | Autonomous task scheduler with module tick system |
| 12 | soul-soc | OPEN | PRODUCTION | brain/modules/knowledge/cve_scanner.py | Security operations: Ubuntu CVE scanning, security knowledge base |
| 13 | soul-content | PRIVATE | PRODUCTION | brain/modules/content/ | Content pipeline: research ingestion, social drafts, approval queue |
| 14 | soul-web | OPEN | PRODUCTION | frontend/ | React 19 PWA: 8 pages, dark theme, WebSocket streaming |
| 15 | soul-desktop | OPEN | PRODUCTION | desktop/ | Tauri v2 cross-platform: tray icon, brain lifecycle, auto-update |
| 16 | soul-term | OPEN | PRODUCTION | brain/cli/ | Click-based CLI: setup, start/stop, deploy, container, mesh |
| 17 | soul-services | PRIVATE | PRODUCTION | deploy/docker/ | Docker orchestration: Vaultwarden, Gitea, Uptime Kuma |
| 18 | soul-deploy | PRIVATE | PRODUCTION | deploy/ | systemd + Fly.io + Pi: cloud-init, OS image builder, auto-update |

### soul-outreach Feature Backlog

These are planned features for soul-outreach (#5), not standalone projects. Specs at `~/soul/soul-outreach/docs/features/`.

| Feature | Category | Description |
|---------|----------|-------------|
| campaign-builder | PRIVATE | Visual campaign builder UI |
| draft-review | PRIVATE | Draft review interface |
| analytics | PRIVATE | Analytics dashboard |
| email-templates | DUAL | Template system |
| landing-page | OPEN | Marketing landing page |
| docs | OPEN | Documentation site |
| multi-workspace | PRIVATE | Multi-workspace support |
| ab-testing | PRIVATE | A/B testing |
| advanced-segmentation | PRIVATE | Contact segmentation |
| api-keys | PRIVATE | API key management |
| webhooks | PRIVATE | Webhook integration |
| auto-followup | PRIVATE | Automated follow-up sequences |
| sentiment-routing | PRIVATE | Sentiment-based reply routing |
| consulting-pipeline | PRIVATE | Consulting CRM features |
| stripe-billing | PRIVATE | Stripe billing integration |
| plugin-system | PRIVATE | Plugin architecture |
| template-marketplace | PRIVATE | Template marketplace |

---

## B. From soul-moa (6 Projects)

Agent SDK components at `~/soul/soul-moa/`.

| # | Project | Category | Status | Location | Description |
|---|---------|----------|--------|----------|-------------|
| 19 | soul-moa-core | OPEN | SCAFFOLDED | src/soul_moa/core/ | Agent loop, tool registry, boundary enforcement, streaming |
| 20 | soul-moa-orchestrator | OPEN | SCAFFOLDED | src/soul_moa/moa/ | MoA proposer/aggregator — the key innovation |
| 21 | soul-moa-failsafe | OPEN | SCAFFOLDED | src/soul_moa/failsafe/ | Circuit breakers, fallback chains, retry policies, health monitoring |
| 22 | soul-moa-models | OPEN | SCAFFOLDED | src/soul_moa/models/ | Universal model client: OpenAI-compat, Anthropic fallback, local |
| 23 | soul-moa-telemetry | OPEN | SCAFFOLDED | src/soul_moa/telemetry/ | Prometheus metrics, structured logging, feedback for training |
| 24 | soul-moa-integration | PRIVATE | SCAFFOLDED | src/soul_moa/integration/ | Drop-in soul-os replacement layer (same API as claude_client.py) |

---

## C. From soul-moe (7 Projects)

Model research components at `~/soul/soul-moe/`.

| # | Project | Category | Status | Location | Description |
|---|---------|----------|--------|----------|-------------|
| 25 | soul-bench | OPEN | SCAFFOLDED | src/soul_moe/benchmarks/ | 10-task benchmark suite + CARS metric |
| 26 | soul-select | OPEN | SCAFFOLDED | src/soul_moe/selection/ | Model candidate screening, CARS scoring, leaderboard |
| 27 | soul-quant | OPEN | SCAFFOLDED | src/soul_moe/quantization/ | GGUF/AWQ/MLX quantization pipelines |
| 28 | soul-tune | OPEN | SCAFFOLDED | src/soul_moe/finetuning/ | MLX LoRA + Unsloth QLoRA fine-tuning |
| 29 | soul-eval | OPEN | SCAFFOLDED | src/soul_moe/evaluation/ | Claude baseline comparison + statistical tests |
| 30 | soul-registry | OPEN | SCAFFOLDED | src/soul_moe/registry/ | Model cards, deploy gates, config export to soul-moa |
| 31 | soul-serve | OPEN | SCAFFOLDED | src/soul_moe/serving/ | Multi-model serving: llama-server, vLLM, MLX configs |

---

## Summary

| Metric | Count |
|--------|-------|
| **Total projects** | **31** |
| Production (in soul-os) | 14 |
| Has code (extracted) | 1 |
| Scaffolded (full structure) | 13 |
| Spec only | 3 |
| Open source | 19 |
| Private | 10 |
| Dual license | 2 |

## Location Index

| Directory | Contents |
|-----------|----------|
| ~/soul-os/ | Production monolith (18 extractable projects) |
| ~/soul/soul-moa/ | Agent SDK scaffold (6 projects) |
| ~/soul/soul-moe/ | Model research scaffold (7 projects) |
| ~/soul/soul-outreach/ | Extracted outreach product |
| ~/soul/soul-mesh/ | Extracted mesh networking |
| ~/soul/ | Command center + all project dirs |
