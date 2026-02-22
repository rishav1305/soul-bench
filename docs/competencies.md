# Soul AI — Competency Signals

What each project demonstrates to different audiences.

## How I Build

All Soul ecosystem projects are built using AI coding tools (Claude Code primarily, plus Google Copilot, Cline, Kilo Code). The competencies below reflect **what I can architect and ship**, not what I manually code line-by-line. My hands-on coding proficiency is in Python, SQL, and shell scripting (6 years). Everything else is built by directing AI tools with architectural intent and domain knowledge.

## For AI Lab Hiring Managers

| Competency | Evidence | Project(s) |
|------------|----------|------------|
| Ships production systems | 6,700 lines, 17 phases, deployed on Pi | soul-os |
| Distributed systems | Hub election, NAT relay, WebSocket sync, delta replication | soul-mesh |
| AI agent architecture | Agent loop, tool registry, boundary enforcement, MoA orchestration | soul-moa-core, soul-agents, soul-loop |
| ML research methodology | CARS metric (original), 10-task benchmark suite, statistical evaluation | soul-bench, soul-eval |
| Production ML | Quantization pipelines (GGUF/AWQ/MLX), fine-tuning (LoRA/QLoRA), model serving | soul-quant, soul-tune, soul-serve |
| AI safety / alignment | Code-level boundary enforcement, tool sandboxing, approval gates | soul-agents |
| Systems engineering | Self-healing with hysteresis, crash-consistent backups, nightly intelligence | soul-heal |
| Security engineering | JWT token family replay detection, CSRF, rate limiting, payload hash verification | soul-auth, soul-soc |
| Full-stack systems (AI-built) | Architected Python FastAPI + React PWA + Tauri desktop + Click CLI using AI coding tools | soul-web, soul-desktop, soul-term |
| Product thinking | Integrated product with 8 UI pages, module system, mesh, cloud deploy | soul-os |

## For Consulting Clients (CTOs / VPs)

| Competency | Evidence | Project(s) |
|------------|----------|------------|
| Production AI systems | Running AI OS with 17 feature phases, real deployment | soul-os |
| Agent orchestration | Multi-agent system with boundary enforcement and approval flows | soul-agents, soul-loop |
| Data pipeline engineering | Full outreach funnel: import -> enrich -> draft -> review -> send -> classify | soul-outreach |
| Security-conscious | JWT, CSRF, rate limiting, DNC enforcement, CAN-SPAM compliance | soul-os |
| Self-healing systems | DB-backed remediation, hysteresis, crash-loop guards, nightly intelligence | soul-heal |
| Infrastructure | systemd services, Docker orchestration, Fly.io deployment, OS image builder | soul-deploy, soul-services |

## For Developer Community

| Competency | Evidence | Project(s) |
|------------|----------|------------|
| AI-augmented open source | Working examples, CI, PyPI published — built with Claude Code + AI tools | All open repos |
| Useful self-hosted tools | Outreach platform, mesh networking, agent framework | soul-outreach, soul-mesh, soul-agents |
| Documentation quality | Architecture docs, CLAUDE.md patterns, technical blog posts | soul-blog |
| Framework design | Pluggable module system, YAML configuration, hot-reloadable config | soul-moa-core, soul-agents |

## Per-Company Talking Points

### Anthropic

| Their Focus | Your Proof |
|-------------|------------|
| Claude safety | soul-agents boundary enforcement is code-level, not prompt-based |
| Claude integration | soul-os uses claude-agent-sdk extensively, deep API experience |
| Agent reliability | soul-moa-failsafe: circuit breakers, fallback chains, health monitoring |
| Research rigor | CARS metric is practical safety/efficiency research, reproducible benchmarks |
| Production systems | 6,700 lines deployed on Pi, 17 phases, systemd, self-healing |

### Google DeepMind

| Their Focus | Your Proof |
|-------------|------------|
| Distributed AI | soul-mesh: hub election, WebSocket sync, NAT relay, storage federation |
| Agent research | soul-moa: MoA orchestration (paper implementation), proposer/aggregator |
| Evaluation methodology | soul-eval: Claude baselines, statistical comparison, CARS metric |
| Scale | soul-os mesh pools resources across devices (acts as one machine) |

### OpenAI

| Their Focus | Your Proof |
|-------------|------------|
| Platform engineering | soul-os: full platform with API, auth, modules, mesh, multi-platform |
| Applied AI products | soul-outreach: production AI product with real users |
| Multi-agent systems | soul-moa-core: agent orchestration, tool registry, MoA layers |
| Developer tools | soul-agents: YAML-configured agents, pip-installable SDK |

### Meta FAIR / Mistral / Cohere

| Their Focus | Your Proof |
|-------------|------------|
| Model optimization | soul-quant: GGUF/AWQ/MLX quantization, CARS efficiency metric |
| Fine-tuning | soul-tune: MLX LoRA + Unsloth QLoRA, task-specific training data |
| Inference | soul-serve: multi-runtime serving (llama.cpp, vLLM, MLX) |
| Open source ML | soul-moe: complete research framework, reproducible experiments |

## Blog Post -> Interview Talking Point Map

| Blog Post | Interview Questions It Prepares For |
|-----------|-------------------------------------|
| "Building a Self-Healing AI OS on Raspberry Pi" | "Tell me about a complex system you built." / "How do you handle failures in production?" |
| "Boundary Enforcement for Safe AI Agents" | "How do you think about AI safety?" / "What guardrails would you put around AI agents?" |
| "CARS: A Cost-Aware Metric for Local Model Selection" | "Tell me about your research." / "How do you evaluate model quality vs. cost?" |
| "MoA for Production Systems" | "How would you orchestrate multiple models?" / "What's your experience with multi-agent systems?" |
| "From Monolith to Mesh: Distributed AI on Consumer Hardware" | "How do you design distributed systems?" / "Tell me about a technical architecture decision." |

## The Meta-Demonstration

The single most powerful signal: **the outreach email itself is the proof**.

"This email was sent using my own AI outreach tool."

What this one sentence proves:
- Built a production AI product (soul-outreach)
- Uses AI agents in production (soul-agents drafted the email)
- Has data pipeline engineering skills (import -> enrich -> draft -> review -> send)
- Has security awareness (DNC, rate limits, CAN-SPAM compliance)
- Ships real systems, not demos
- Confident enough to use own tools for the most important emails of his career
