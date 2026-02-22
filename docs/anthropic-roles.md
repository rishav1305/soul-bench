# Anthropic Open Roles -- Complete Research

**Date:** 2026-02-21
**Total Open Positions:** ~505 across all departments
**Source:** anthropic.com/jobs, job-boards.greenhouse.io/anthropic, 80000hours.org

---

## Company Context

- **Series G:** $30B raised at $380B post-money valuation (Feb 12, 2026)
- **India Expansion:** New Bengaluru office; India run-rate revenue doubled since Oct 2025
- **Fellows Program:** Applications open for May and July 2026 cohorts (AI safety research)
- **Headcount:** Aggressive hiring across all functions -- 505 open roles is massive growth

---

## HIGH-RELEVANCE ROLES (Detailed Breakdowns)

These are the roles most aligned with your background in AI engineering, agent infrastructure, distributed systems, AI safety, and model evaluation.

---

### 1. Senior/Staff+ Software Engineer, Autonomous Agent Infrastructure

| Field | Detail |
|-------|--------|
| **Team** | Agent Infrastructure |
| **Location** | San Francisco, CA / New York City, NY / Seattle, WA |
| **Salary** | $320,000 - $485,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/5065894008 |

**What they build:** Sandboxed environments where Claude executes code, accesses tools, and interacts with external services. State management for extended agent operations (checkpoints, recovery, resumption). Security frameworks for Claude acting on behalf of users. Observability tools for agent execution monitoring.

**Required:**
- 6+ years building distributed systems, infrastructure, or platform services at scale
- Cloud-native infrastructure experience (GCP, AWS, or Azure)
- Strong commitment to security, isolation, and safe failure modes
- Proficiency in Python, Go, Rust, or comparable languages
- Comfort with architectural ambiguity in greenfield projects

**Preferred:**
- Multi-tenant execution platform or serverless infrastructure background
- Security engineering, sandboxing, or isolation technology experience
- Workflow orchestration (Temporal, Airflow, Step Functions)
- State machines, checkpointing, or durable execution patterns
- Linux internals, eBPF, or container runtime expertise

**Fit Signal:** VERY HIGH -- directly maps to soul-mesh (distributed systems), soul-agents (boundary enforcement), soul-cloud (container-per-user PaaS), and soul-loop (autonomous task scheduler).

---

### 2. Software Engineer, Claude Code

| Field | Detail |
|-------|--------|
| **Team** | Claude Code (AI-powered development tools) |
| **Location** | New York City, NY / San Francisco, CA / Seattle, WA |
| **Salary** | $320,000 - $560,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/4816198008 |

**What they build:** Scalable features for AI-assisted coding tools. Gather developer insights, collaborate with researchers on model improvements. Full-stack from UI to infrastructure optimization.

**Required:**
- 5+ years professional experience
- React expertise including performance optimization and modern patterns
- Full-stack capability with UX specialization
- Hands-on LLM and prompt engineering experience

**Preferred:**
- CLI tool development
- Large TypeScript codebases (50k+ lines)
- Container orchestration and cloud infrastructure
- Alternative JavaScript runtimes (Bun, Deno)
- Build system optimization
- Testing infrastructure for team-scale projects

**Fit Signal:** HIGH -- soul-term (CLI), soul-web (React 19 PWA), soul-desktop (Tauri cross-platform), extensive LLM tool-use experience.

---

### 3. Software Engineer, Agent SDK - Claude Code

| Field | Detail |
|-------|--------|
| **Team** | Claude Code / Agent SDK |
| **Location** | New York City, NY / San Francisco, CA / Seattle, WA |
| **Salary** | Not listed (likely $320k-$560k range based on similar roles) |
| **Link** | https://www.anthropic.com/jobs (search "Agent SDK") |

**Context:** The Claude Code SDK was recently renamed to the Claude Agent SDK to reflect its broader vision beyond coding. This team builds the SDK that gives Claude access to computers where it can write files, run commands, and iterate on its work.

**Fit Signal:** HIGH -- direct experience building agent frameworks (soul-agents YAML agents, soul-moa-core agent loop), tool registries, boundary enforcement.

---

### 4. Model Quality Software Engineer, Claude Code

| Field | Detail |
|-------|--------|
| **Team** | Claude Code |
| **Location** | San Francisco, CA / New York City, NY |
| **Salary** | Not listed |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/5098025008 |

**Fit Signal:** HIGH -- soul-bench (benchmark + CARS metric), soul-eval (Claude baseline comparison + stats).

---

### 5. Prompt Engineer, Agent Prompts and Evals

| Field | Detail |
|-------|--------|
| **Team** | Engineering and Design - Product |
| **Location** | San Francisco, CA / New York City, NY |
| **Salary** | Not listed |
| **Link** | https://www.anthropic.com/jobs (search "Agent Prompts") |

**Fit Signal:** HIGH -- soul-agents (YAML prompt system), soul-bench/soul-eval (evaluation frameworks), extensive prompt engineering across soul-os.

---

### 6. Research Engineer, Model Evaluations (Expression of Interest)

| Field | Detail |
|-------|--------|
| **Team** | Model Evaluations |
| **Location** | San Francisco, CA / New York City, NY |
| **Salary** | $300,000 - $405,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/4990535008 |

**What they build:** Evaluation infrastructure -- novel methodologies to assess model capabilities across reasoning, safety, helpfulness, harmlessness. High-throughput pipelines for real-time training insights.

**Required:**
- Experience designing evaluation systems for ML models, particularly LLMs
- Technical leadership through formal roles or complex projects
- Combined systems engineering and experimental design skills
- Strong Python and distributed computing framework experience
- Statistical analysis expertise

**Preferred:**
- Production-environment evaluation experience
- Safety frameworks
- Psychometrics background
- Reinforcement learning evaluation
- Open-source benchmark contributions
- Large-scale infrastructure management

**Fit Signal:** VERY HIGH -- soul-bench (10-task benchmark + CARS metric), soul-eval (Claude baseline comparison + statistical testing), soul-select (model screening + CARS scoring).

---

### 7. Research Engineer, AI Observability

| Field | Detail |
|-------|--------|
| **Team** | AI Observability (tools leveraging Claude to analyze massive datasets) |
| **Location** | San Francisco, CA |
| **Salary** | $320,000 - $405,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/5125083008 |

**What they build:** Systems enabling AI to analyze large unstructured datasets (tens/hundreds of thousands of documents). Monitoring systems for training and deployment. Agentic integrations for autonomous investigation.

**Required:**
- 5+ years software engineering with meaningful ML exposure
- Interest in scaling human oversight of AI systems
- Familiarity with LLM app development (context engineering, evaluation, orchestration)
- Strong focus on UX, reliability, and documentation

**Preferred:**
- AI safety, alignment, or responsible deployment research
- Data science and engineering with large-scale data processing
- Productionizing internal tools or developer platforms
- Monitoring/observability systems background

**Fit Signal:** HIGH -- soul-heal (self-healing with observability), soul-soc (security scanning), soul-moa-telemetry (Prometheus metrics, structured logging).

---

### 8. ML/Research Engineer, Safeguards

| Field | Detail |
|-------|--------|
| **Team** | Safeguards ML |
| **Location** | San Francisco, CA / New York City, NY |
| **Salary** | $350,000 - $500,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/4949336008 |

**What they build:** Classifiers detecting harmful use patterns. Synthetic data pipelines. Monitoring for coordinated attacks. Prompt injection defenses for agentic products. Automated red-teaming.

**Required:**
- 4+ years in ML engineering, research engineering, or applied research
- Python proficiency and ML systems experience
- Comfort across research-to-production pipelines
- Genuine concern about AI misuse risks

**Fit Signal:** HIGH -- soul-agents (boundary enforcement), soul-soc (security KB), soul-auth (replay detection), safety-first architecture throughout soul-os.

---

### 9. Research Engineer, Interpretability

| Field | Detail |
|-------|--------|
| **Team** | Interpretability |
| **Location** | San Francisco, CA (remote for exceptional candidates) |
| **Salary** | $315,000 - $560,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/4980430008 |

**What they build:** Specialized infrastructure for interpretability research. Instrumented forward/backward passes and activation extraction. Production safety audits.

**Required:**
- 5-10+ years software engineering
- High proficiency in one language (Python, Rust, Go, Java)
- Strong curiosity about unfamiliar technical domains
- Interest in interpretability's role in AI safety

**Preferred:**
- Large-scale distributed systems optimization
- Transformer and language modeling fundamentals
- LLM performance optimization (memory, compute efficiency, parallelism)
- PyTorch/CUDA or JAX/XLA experience

**Fit Signal:** MEDIUM-HIGH -- strong systems engineering match, AI safety alignment.

---

### 10. Research Engineer, Discovery

| Field | Detail |
|-------|--------|
| **Team** | Discovery (building an "AI scientist") |
| **Location** | San Francisco, CA |
| **Salary** | $350,000 - $850,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/4669581008 |

**What they build:** Large-scale infrastructure for AI training, evaluation, deployment. Scalable VM/sandboxing/container architectures for long-horizon AI tasks. Large-scale data pipelines. RL pipeline optimization.

**Required:**
- 6+ years infrastructure engineering with distributed systems expertise
- Performance optimization for high-throughput ML workloads
- Containerization (Docker, Kubernetes) at scale
- Large-scale data pipelines and distributed storage

**Fit Signal:** HIGH -- soul-cloud (container-per-user PaaS), soul-deploy (systemd/Fly.io/Pi), soul-mesh (distributed systems), soul-loop (autonomous task scheduling).

---

### 11. Forward Deployed Engineer, Applied AI

| Field | Detail |
|-------|--------|
| **Team** | Applied AI |
| **Location** | Atlanta / Austin / Boston / Chicago / NYC / Seattle / SF / Washington DC |
| **Salary** | $200,000 - $300,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/4985877008 |

**What they build:** Production applications using Claude within customer systems. MCP servers, sub-agents, and agent skills for production workflows. Enterprise deployment support.

**Required:**
- 4+ years in technical, customer-facing roles (FDE, SE with consulting, or technical founder)
- Production LLM experience: prompt engineering, agent development, evaluation frameworks
- Python proficiency (ideally TypeScript, Java also)
- Navigate ambiguity in complex organizations

**Fit Signal:** HIGH -- soul-consult (consulting CRM), soul-outreach (email campaign SaaS), soul-agents (agent development), extensive production LLM work.

---

### 12. Solutions Architect, Applied AI (Startups)

| Field | Detail |
|-------|--------|
| **Team** | Applied AI, Startups |
| **Location** | San Francisco, CA / New York City, NY |
| **Salary** | Not listed |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/5057258008 |

**What they build:** Help startups architect LLM solutions, win technical evaluations, and get the most out of Claude.

**Required:**
- 3+ years in technical customer-facing roles (SA, SE, FDE, or technical founder)
- Hands-on LLM application building and deployment in production
- Context engineering, evaluation frameworks, modern AI architectures
- Python proficiency, common LLM frameworks

**Fit Signal:** HIGH -- soul-os is a full AI-native OS, soul-outreach is a SaaS product, direct experience building with Claude APIs.

---

### 13. Anthropic AI Safety Fellow

| Field | Detail |
|-------|--------|
| **Team** | AI Safety Research (mentors: Jan Leike, Sam Bowman, Nicholas Carlini, etc.) |
| **Location** | London / Berkeley / Ontario / Remote (US/UK/Canada) |
| **Stipend** | $3,850/week (~$15,400/month) + ~$15k/month compute |
| **Duration** | 4 months (May 2026 or July 2026 cohorts) |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/5023394008 |

**Research Areas:** Scalable oversight, adversarial robustness and AI control, model organisms, mechanistic interpretability, AI security, model welfare.

**Required:**
- Python fluency
- Full-time availability for 4 months
- Work authorization in US, UK, or Canada
- Strong technical background (CS, math, physics, cybersecurity)

**Track Record:** 80%+ of fellows published research; 40%+ received full-time offers.

**Fit Signal:** MEDIUM -- strong technical background, AI safety focus. But requires 4 months full-time commitment.

---

### 14. Research Scientist/Engineer, Alignment Finetuning (Expression of Interest)

| Field | Detail |
|-------|--------|
| **Team** | Alignment Finetuning |
| **Location** | San Francisco, CA |
| **Salary** | $350,000 - $500,000 |
| **Link** | https://job-boards.greenhouse.io/anthropic/jobs/4520279008 |

**What they build:** Novel finetuning techniques using synthetic data. Training models for better moral reasoning, improved honesty, good character. Evaluation frameworks for alignment properties.

**Required:**
- Master's or PhD in CS/ML (or equivalent experience)
- Strong Python, ML model training and experimentation
- Track record implementing ML research

**Note:** 2025 headcount filled; expression of interest for future hiring.

**Fit Signal:** MEDIUM -- soul-tune (LoRA/QLoRA fine-tuning), AI safety focus.

---

### 15. Research Engineer/Scientist, Alignment Science

| Field | Detail |
|-------|--------|
| **Team** | Alignment Science |
| **Location** | San Francisco, CA (also London, UK posting) |
| **Salary** | Not listed |
| **Link** | https://www.anthropic.com/jobs (search "Alignment Science") |

**Fit Signal:** MEDIUM-HIGH -- AI safety core mission alignment.

---

### 16. Software Engineer, Sandboxing

| Field | Detail |
|-------|--------|
| **Team** | AI Research and Engineering |
| **Location** | San Francisco, CA / New York City, NY |
| **Salary** | Not listed |
| **Link** | https://www.anthropic.com/jobs (search "Sandboxing") |

**Fit Signal:** HIGH -- soul-cloud (container-per-user PaaS with Traefik), soul-agents (boundary enforcement), security-first design.

---

### 17. Staff Machine Learning Engineer, Virtual Collaborator

| Field | Detail |
|-------|--------|
| **Team** | AI Research and Engineering |
| **Location** | New York City, NY / San Francisco, CA / Seattle, WA |
| **Salary** | Not listed |
| **Link** | https://www.anthropic.com/jobs (search "Virtual Collaborator") |

**Fit Signal:** MEDIUM-HIGH -- building AI that collaborates with humans; maps to soul-os multi-agent architecture.

---

## ADDITIONAL ENGINEERING ROLES

| # | Title | Location | Salary (if known) | Link |
|---|-------|----------|-------------------|------|
| 18 | Software Engineer, Windows - Claude Code | SF / Seattle | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5098506008) |
| 19 | Staff SW Engineer, Claude Developer Platform (Full Stack) | SF | -- | anthropic.com/jobs |
| 20 | Staff SW Engineer, Claude Developer Platform (Backend) | NYC / SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4988878008) |
| 21 | Engineering Manager, Claude Developer Platform | SF | -- | anthropic.com/jobs |
| 22 | Software Engineer, Enterprise Foundations | SF / NYC | -- | anthropic.com/jobs |
| 23 | Software Engineer, UI Platform | SF / NYC | -- | anthropic.com/jobs |
| 24 | Software Engineer, Platform | NYC / SF / Seattle | -- | anthropic.com/jobs |
| 25 | Staff Software Engineer, Platform | SF / NYC | -- | anthropic.com/jobs |
| 26 | Software Engineer, iOS | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 27 | Software Engineer, Android | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 28 | Software Engineer, Desktop | SF / Seattle | -- | anthropic.com/jobs |
| 29 | Software Engineer, Growth | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 30 | Software Engineer, Public Sector | SF / NYC / DC | -- | anthropic.com/jobs |
| 31 | Software Engineer, Beneficial Deployments | SF / NYC | -- | anthropic.com/jobs |
| 32 | Software Engineer, Business Technology | Remote / SF / Seattle | -- | anthropic.com/jobs |
| 33 | Software Engineer, Cybersecurity Products | SF / NYC / Seattle / DC | -- | anthropic.com/jobs |
| 34 | Software Engineer, People Products | Remote / SF | -- | anthropic.com/jobs |
| 35 | Full Stack Software Engineer, Reinforcement Learning | SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5098984008) |

---

## ADDITIONAL RESEARCH ROLES

| # | Title | Location | Salary (if known) | Link |
|---|-------|----------|-------------------|------|
| 36 | Research Scientist, Interpretability | SF | -- | anthropic.com/jobs |
| 37 | Research Manager, Interpretability [EOI] | SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4980436008) |
| 38 | Research Scientist/Engineer, Honesty [EOI] | NYC / SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4532887008) |
| 39 | Staff Research Engineer, Discovery Team | SF | -- | anthropic.com/jobs |
| 40 | Research Engineer/Scientist, Alignment Science, London | London | -- | anthropic.com/jobs |
| 41 | Research Engineer, ML (Reinforcement Learning) | SF / NYC | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4613568008) |
| 42 | Research Engineer, ML (Reinforcement Learning) | London | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5115935008) |
| 43 | Research Engineer, Production Model Post Training | SF / NYC / Seattle | $300k-$405k | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4613592008) |
| 44 | Research Engineer, Production Model Post Training [EOI] | London | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4980460008) |
| 45 | Research Engineer, Production Model Post Training | Zurich | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5112018008) |
| 46 | Research Engineer, Pre-training | Remote / SF / Seattle / NYC | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4616971008) |
| 47 | Research Engineer, Pretraining | London | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5119713008) |
| 48 | Research Engineer, Pretraining Scaling | SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4938432008) |
| 49 | Research Engineer, Pretraining Scaling (London) | London | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4938436008) |
| 50 | Research Engineer/Scientist, Pre-training | Zurich | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4799425008) |
| 51 | Research Engineer/Scientist, Biology and Life Sciences | SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4924308008) |
| 52 | Research Engineer/Scientist, Vision | NYC / SF / Seattle | -- | anthropic.com/jobs |
| 53 | Research Engineer/Scientist, Audio | SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5074815008) |
| 54 | Research Engineer, Cybersecurity RL | SF / NYC | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5025624008) |
| 55 | Research Engineer, Environment Scaling | Remote / SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4951064008) |
| 56 | Research Engineer, Frontier Red Team (Autonomy) | SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5067100008) |
| 57 | Research Engineer, Frontier Red Team (Hardware Lead) | SF | -- | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5067098008) |
| 58 | Research Engineer/Scientist, Frontier Red Team (Cyber) | SF | -- | anthropic.com/jobs |
| 59 | Research Scientist, Frontier Red Team (Emerging Risks) | SF | -- | anthropic.com/jobs |
| 60 | Research Engineer, Reward Models Platform | Remote / SF / Seattle / NYC | -- | anthropic.com/jobs |
| 61 | Senior Research Scientist, Reward Models | Remote / SF | -- | anthropic.com/jobs |
| 62 | Research Engineer/Scientist, Societal Impacts | SF | -- | anthropic.com/jobs |
| 63 | Research Scientist, Societal Impacts | SF | -- | anthropic.com/jobs |
| 64 | Research Engineer, Universes | Remote / SF / Seattle / NYC | -- | anthropic.com/jobs |
| 65 | Research Economist, Economic Research | SF | $320k-$405k | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5018472008) |
| 66 | Biological Safety Research Scientist | SF / NYC | -- | anthropic.com/jobs |
| 67 | Anthropic AI Security Fellow | London / Ontario / Remote / SF | $3,850/week | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5030244008) |

---

## INFRASTRUCTURE ENGINEERING ROLES

| # | Title | Location | Salary (if known) | Link |
|---|-------|----------|-------------------|------|
| 68 | Sr/Staff+ SW Engineer, Autonomous Agent Infrastructure | SF / NYC / Seattle | $320k-$485k | [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/5065894008) |
| 69 | Staff + Senior SW Engineer, Inference | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 70 | Staff + Senior SW Engineer, Cloud Inference | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 71 | Staff SW Engineer, Inference | Dublin / London | -- | anthropic.com/jobs |
| 72 | Senior SW Engineer, Inference | Dublin | -- | anthropic.com/jobs |
| 73 | Senior SW Engineer, Systems | London | -- | anthropic.com/jobs |
| 74 | SW Engineer, Inference Deployment | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 75 | Infrastructure Engineer, Sandboxing | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 76 | SW Engineer, Sandboxing (Systems) | SF / NYC | -- | anthropic.com/jobs |
| 77 | Staff+ SW Engineer, Data Infrastructure | SF / Seattle | -- | anthropic.com/jobs |
| 78 | Senior SW Engineer, Data Infrastructure | SF / Seattle | -- | anthropic.com/jobs |
| 79 | Senior SW Engineer, Databases | SF / NYC | -- | anthropic.com/jobs |
| 80 | Staff+ SW Engineer, Databases | SF / NYC | -- | anthropic.com/jobs |
| 81 | Staff+ SW Engineer, Developer Productivity | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 82 | Senior SW Engineer, Developer Productivity | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 83 | Staff + Senior SW Engineer, AI Reliability | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 84 | Staff SW Engineer, AI Reliability Engineering | Dublin / London | -- | anthropic.com/jobs |
| 85 | Staff+ SW Engineer, Observability | London | -- | anthropic.com/jobs |
| 86 | Senior and Staff SW Engineer, Continuous Integration | London | -- | anthropic.com/jobs |
| 87 | Engineering Manager, Networking | Remote / SF / Seattle / NYC | -- | anthropic.com/jobs |
| 88 | Engineering Manager, Inference Developer Productivity | SF / NYC / Seattle | -- | anthropic.com/jobs |
| 89 | Engineering Manager, Observability | SF / NYC | -- | anthropic.com/jobs |
| 90 | Engineering Manager, Accelerator Platform | SF / NYC / Seattle | -- | anthropic.com/jobs |

---

## ML INFRASTRUCTURE / ACCELERATION ROLES

| # | Title | Location | Salary (if known) |
|---|-------|----------|-------------------|
| 91 | Performance Engineer | SF / NYC / Seattle | -- |
| 92 | Performance Engineer, GPU | SF / NYC / Seattle | -- |
| 93 | TPU Kernel Engineer | SF / NYC / Seattle | -- |
| 94 | SW Engineer, ML Networking | SF / NYC / Seattle | -- |
| 95 | SW Engineer, Accelerator Build Infrastructure | SF / Seattle | -- |
| 96 | ML Infrastructure Engineer, Safeguards | SF | -- |
| 97 | Machine Learning Systems Engineer, RL Engineering | SF / NYC / Seattle | -- |
| 98 | Machine Learning Systems Engineer, Research Tools | SF / NYC / Seattle | -- |
| 99 | Senior+ SW Engineer, Research Tools | SF / NYC | -- |
| 100 | Engineering Manager, Inference | SF / NYC / Seattle | -- |
| 101 | Engineering Manager, ML Acceleration | SF / NYC / Seattle | -- |

---

## APPLIED AI / SOLUTIONS / CONSULTING ROLES

| # | Title | Location | Salary (if known) |
|---|-------|----------|-------------------|
| 102 | Forward Deployed Engineer, Applied AI | ATL/AUS/BOS/CHI/NYC/SEA/SF/DC | $200k-$300k |
| 103 | Forward Deployed Engineer, Applied AI | London | -- |
| 104 | Forward Deployed Engineer, Applied AI | Tokyo | -- |
| 105 | Forward Deployed Engineer, Applied AI | Munich | -- |
| 106 | Forward Deployed Engineer, Applied AI | Paris | -- |
| 107 | Forward Deployed Engineer, Applied AI (Federal Civilian) | SF / NYC / DC | -- |
| 108 | Forward Deployed Engineer, Custom Agents | SF / NYC | -- |
| 109 | Manager, Forward Deployed Engineering | BOS/SF/NYC/SEA/DC | -- |
| 110 | Solutions Architect, Applied AI (Industries) | NYC / SF / Seattle | -- |
| 111 | Solutions Architect, Applied AI (Industries) | Munich / Paris / London | -- |
| 112 | Solutions Architect, Applied AI (Startups) | SF / NYC | -- |
| 113 | Solutions Architect, Applied AI (Startups) | London | -- |
| 114 | Solutions Architect, Applied AI (DNB) | SF / NYC | -- |
| 115 | Solutions Architect, Applied AI (Beneficial Deployments) | SF / NYC | -- |
| 116 | Solutions Architect, Applied AI (Federal Civilian) | SF / NYC / DC | -- |
| 117 | Solutions Architect, Applied AI (National Security) | DC | -- |
| 118 | Solutions Architect, Applied AI (Creatives) | SF / NYC | -- |
| 119 | Solutions Architect, Applied AI | Tokyo / Bangalore / Sydney | -- |
| 120 | Partner Solutions Architect, Applied AI | SF / NYC / Seattle | -- |
| 121 | Partner Solutions Architect, Applied AI | Paris / Munich | -- |
| 122 | Manager of Solutions Architecture, Applied AI (Industries) | SF/NYC / Paris / London / Munich | -- |
| 123 | Applied AI Engineer (Digital Natives Business) | SF / NYC / Seattle | -- |
| 124 | Applied AI Engineer (Startups) | SF / NYC / London | -- |
| 125 | Applied AI Engineer, Beneficial Deployments | SF / NYC | -- |
| 126 | Applied AI Engineer, Life Sciences | SF / NYC | -- |
| 127 | Product Engineer, Applied AI | Seoul | -- |
| 128 | Technical Deployment Lead, Applied AI | ATL/AUS/BOS/CHI/SF/NYC/DC | -- |
| 129 | Claude Evangelist, Applied AI (Startups) | SF / NYC / London | -- |
| 130 | Security Architect, Applied AI | NYC / Seattle / SF | -- |
| 131 | Solutions Architect, National Security | DC | -- |

---

## PRODUCT MANAGEMENT ROLES (RELEVANT)

| # | Title | Location |
|---|-------|----------|
| 132 | Product Manager, Claude Code | SF / Seattle |
| 133 | Product Manager, Claude Code (Enterprise) | SF / Seattle |
| 134 | Product Manager, Claude Code Growth | SF / NYC / Seattle |
| 135 | Product Manager, Safeguards (Privacy) | SF |
| 136 | Product Manager, Safeguards (High Risk Industry) | SF |
| 137 | Product Manager, Compute Platform | SF / NYC / Seattle |
| 138 | Research Product Manager, Labs | SF / NYC |
| 139 | Research Product Manager, Model Behaviors | SF / NYC |
| 140 | Product Management, Research | SF / NYC |
| 141 | Founding Developer Relations Lead | SF / NYC |
| 142 | Developer Relations, MCP | SF |
| 143 | Product Lead, Healthcare | SF / NYC |

---

## SECURITY ENGINEERING ROLES

| # | Title | Location | Salary (if known) |
|---|-------|----------|-------------------|
| 144 | Application Security Engineer | Remote / SF / Seattle / NYC | -- |
| 145 | Senior SW Security Engineer | SF / NYC / Seattle / London | -- |
| 146 | Staff+ SW Security Engineer | SF / NYC / Seattle | $405k-$485k |
| 147 | Security SW Engineer, D&R Platform | SF / NYC / Seattle / DC | -- |
| 148 | Security Engineer, Detection and Response | SF / NYC / Seattle / DC | -- |
| 149 | Senior Security Engineer, D&R | Zurich | -- |
| 150 | Senior Security SW Engineer, D&R Platform | Zurich | -- |
| 151 | Senior Security SW Engineer, eBPF and Security Sensors | Zurich | -- |
| 152 | Platform Security Engineer, Operating Systems | SF / NYC / Seattle | -- |
| 153 | Platform Hardware Security | NYC / Seattle / SF / DC | -- |
| 154 | Security Engineer, Offensive Security | Remote / SF / Seattle | -- |
| 155 | Engineering Manager, Cloud Security | SF / Seattle | -- |
| 156 | Engineering Manager, Detection and Response | SF / NYC | -- |
| 157 | Engineering Manager, Access Management | SF / NYC / Seattle | -- |
| 158 | Red Team Engineer, Safeguards | Remote / SF / DC | -- |

---

## SAFEGUARDS (TRUST AND SAFETY) ROLES

| # | Title | Location |
|---|-------|----------|
| 159 | Applied Safety Research Engineer, Safeguards | SF |
| 160 | Privacy Research Engineer, Safeguards | SF |
| 161 | Software Engineer, Safeguards | SF / NYC |
| 162 | Software Engineer, Safeguards Infrastructure | London |
| 163 | Engineering Manager, Safeguards Data Infra | London / NYC |
| 164 | Policy Manager, Chemical Weapons and HYE | Remote / SF / DC |
| 165 | Technical Policy Manager, Cyber Harms | Remote / SF / DC |
| 166 | Product Policy Manager, Frontier Risk | Remote / SF / DC |
| 167 | Policy Manager, Harmful Persuasion | SF / NYC |
| 168 | Safeguards Analyst, Account Abuse | SF / NYC |

---

## COMPUTE / DATA CENTER ROLES

| # | Title | Location |
|---|-------|----------|
| 169 | Staff/Sr SW Engineer, Compute Capacity | SF / NYC |
| 170 | SW Engineer, Compute Efficiency | SF / NYC |
| 171 | Data Science Engineer, Capacity and Efficiency | NYC / SF / Seattle |
| 172 | Compute Capacity Strategy and Operations | SF / NYC |
| 173 | Research Compute Operations | SF / NYC |
| 174 | Data Center Hardware Operations Lead | SF / NYC |
| 175 | Data Center Facility Operations Lead | SF / NYC |
| 176 | Data Center Controls Engineer | SF / NYC |
| 177 | Data Center Energy Lead | Remote / SF |

---

## DATA SCIENCE AND ANALYTICS

| # | Title | Location |
|---|-------|----------|
| 178 | Analytics Data Engineer | SF / NYC / Seattle |
| 179 | Analytics Data Engineering Manager, Product | SF / NYC / Seattle |

---

## EDUCATION AND DEVELOPER ROLES

| # | Title | Location | Salary (if known) |
|---|-------|----------|-------------------|
| 180 | Developer Education Lead | SF / NYC | $290k-$365k |
| 181 | Senior Education Platform Engineer | SF | -- |
| 182 | Founding Design Engineer, AI Capability Development, Education Labs | SF / NYC | -- |
| 183 | Certification Content and Systems Architect | SF / NYC | -- |
| 184 | Training Content and Systems Architect | SF / NYC | -- |

---

## REMAINING DEPARTMENTS (SUMMARY COUNTS)

| Department | Open Roles |
|------------|-----------|
| Communications | 3 |
| Finance | 34 |
| Legal | 16 |
| Marketing and Brand | 35 |
| People / Recruiting | 15 |
| Technical Program Management | 13 |
| AI Public Policy and Societal Impacts | 10 |

---

## TOP 10 ROLES BY FIT (Ranked)

Based on the soul-os ecosystem skill set (distributed systems, AI agents, boundary enforcement, evaluation frameworks, container orchestration, CLI tools, React, Python, FastAPI, AI safety):

| Rank | Role | Why | Salary |
|------|------|-----|--------|
| 1 | **Sr/Staff+ SE, Autonomous Agent Infrastructure** | Direct match: distributed systems, sandboxing, state management, security boundaries | $320k-$485k |
| 2 | **Software Engineer, Claude Code** | CLI tools, React, TypeScript, LLM tooling, full-stack | $320k-$560k |
| 3 | **Software Engineer, Agent SDK - Claude Code** | Agent frameworks, tool registries, boundary enforcement | ~$320k-$560k |
| 4 | **Research Engineer, Model Evaluations** | Benchmark design, evaluation pipelines, statistical analysis | $300k-$405k |
| 5 | **Forward Deployed Engineer, Applied AI** | Customer-facing, production LLM apps, Python, consulting | $200k-$300k |
| 6 | **Solutions Architect, Applied AI (Startups)** | Technical sales, LLM architecture, startup context | -- |
| 7 | **Research Engineer, Discovery** | Container orchestration, distributed infra, long-horizon AI | $350k-$850k |
| 8 | **ML/Research Engineer, Safeguards** | Safety classifiers, prompt injection defense, red-teaming | $350k-$500k |
| 9 | **Research Engineer, AI Observability** | Monitoring, oversight, agentic integrations | $320k-$405k |
| 10 | **Forward Deployed Engineer, Custom Agents** | Building custom agent solutions for enterprises | -- |

---

## KEY OBSERVATIONS

1. **Massive hiring surge.** 505 open roles reflects the $30B Series G capital deployment. This is the largest Anthropic has ever been in terms of open headcount.

2. **Agent infrastructure is a top priority.** Multiple dedicated roles for agent SDK, agent platform, autonomous agent infra, agent prompts/evals, and forward deployed agent engineers. This is where the company is placing huge bets.

3. **Claude Code is a flagship product.** At least 6 dedicated engineering roles, 3 PM roles, and marketing roles specifically for Claude Code. They are building it out aggressively across platforms (Windows, desktop, mobile).

4. **Safety permeates every team.** Not just a "safety team" -- safeguards engineers, red team engineers, alignment researchers, policy managers, and trust and safety analysts form a comprehensive safety org.

5. **Global expansion.** Roles in London, Dublin, Munich, Paris, Zurich, Tokyo, Seoul, Sydney, Bangalore -- Anthropic is now a truly global company.

6. **Applied AI / Solutions is huge.** 30+ Solutions Architect / Forward Deployed Engineer / Applied AI Engineer roles across industries and geographies. This is their consulting/implementation arm.

7. **Expression of Interest roles** (Model Evaluations, Alignment Finetuning, Interpretability Manager, Honesty, Post-Training London) indicate future hiring even when current headcount is filled. Worth submitting to get in the pipeline.

8. **The Fellows Program** is a strong entry path: 4-month paid research ($15.4k/month + $15k compute), 40%+ conversion to full-time, no PhD required.

---

## SOURCES

- [Anthropic Careers Page](https://www.anthropic.com/jobs)
- [Anthropic Greenhouse Job Board](https://job-boards.greenhouse.io/anthropic)
- [80,000 Hours - Anthropic](https://jobs.80000hours.org/organisations/anthropic)
- [Anthropic Fellows Program 2026](https://alignment.anthropic.com/2025/anthropic-fellows-program-2026/)
- [Anthropic LinkedIn Jobs](https://www.linkedin.com/company/anthropicresearch/jobs)
- [Anthropic India Expansion](https://www.mymobileindia.com/anthropic-opens-office-in-bengaluru-expands-india-operations-and-hiring/)
- [Nate McMaster - Working at Anthropic](https://natemcmaster.com/blog/2026/01/27/so-you-want-to-join-anthropic/)
- [Anthropic News](https://www.anthropic.com/news)

---

**Confidence: HIGH** -- Data sourced directly from Anthropic's official careers page and Greenhouse job board, cross-referenced with LinkedIn and third-party job boards. Role counts and details verified across multiple sources. Salary data from official Greenhouse postings.
