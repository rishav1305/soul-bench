# Profile Overhaul — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update all professional platforms and internal docs to reflect the paradigm shift from traditional coder to AI-augmented architect, with honest tech tiers and Engineer/Consultant/Researcher vision pillars.

**Architecture:** Create a canonical identity file (`docs/profile/identity.md`) as single source of truth, then derive all platform-specific content from it. Internal docs updated first, then drafts for each public platform (user approves before anything goes live).

**Tech Stack:** Markdown files, git, LinkedIn (manual updates), GitHub profile repo, website (rishavchatterjee.com)

---

### Task 1: Create Canonical Identity File

**Files:**
- Create: `docs/profile/identity.md`

**Step 1: Create the profile directory**

```bash
mkdir -p ~/soul/docs/profile
```

**Step 2: Write `docs/profile/identity.md`**

This is the single source of truth. All platform content derives from this file. Contents:

```markdown
# Rishav Chatterjee — Professional Identity

**Last updated:** 2026-02-22
**Canonical source:** All platform profiles derive from this file.

---

## Core Identity

**Title:** AI Engineer | Consultant | Researcher

**One-Liner:** I architect and ship production AI systems — from mesh networks to autonomous agents — using AI coding tools as my development environment. 6 years of Python, SQL, and data platform engineering give me the domain knowledge to direct AI effectively.

**Location:** Delhi, India

---

## Three Pillars (Vision)

### Engineer
I architect and ship production AI systems using AI coding tools as my primary development environment. 31 interconnected projects, distributed mesh networks, autonomous agents, self-healing infrastructure. I don't type every line — I design every system.

### Consultant
I solve AI infrastructure problems for enterprises. GOAT platform at Gartner (5,000+ users), data quality frameworks at IBM-TWC (60% time reduction), data platforms at Novartis (15 brands, 99.5% accuracy). 6 years of domain knowledge in data engineering, now multiplied by AI tooling.

### Researcher
CARS metric (Cost-Aware Reasoning Score) — an original efficiency metric for evaluating local AI models. 10-task benchmark suite with Claude baselines. I study how to measure and optimize AI systems, not just build them.

---

## Honest Tech Tiers

### Tier 1: I Write (6 years hands-on)
Python, SQL, Bash/Shell, Apache Airflow, dbt, data pipeline code, Snowflake queries, AWS Glue scripts

### Tier 2: I Build with AI Tools
React, FastAPI, Tauri, WebSocket, Docker, distributed systems, infrastructure as code
Tools used: Claude Code (primary), Google Copilot, Cline, Kilo Code

### Tier 3: I Architect & Configure
Claude Code configuration (CLAUDE.md, custom agents, hooks, commands), system design, AI workflows, CI/CD pipelines, multi-agent orchestration patterns

---

## Career Arc

### Phase 1: Data Engineer (2018-2022)
- **Polestar Solutions** (Jun 2018 - Apr 2020): Data pipelines for Jubilant FoodWorks (66% execution time reduction), IndiaMART (AWS migration), Reckitt Benckiser (Azure Databricks)
- **Novartis Healthcare** (May 2020 - Dec 2022): HIVE-to-Snowflake migration (60% performance gain), Airflow/Alteryx orchestration, 99.5% data accuracy across 15 pharmaceutical brands

### Phase 2: AI Platform Lead (2022-present)
- **Gartner India via Bitwise** (Dec 2022 - present): Launched GOAT agentic AI platform (5,000+ users, 88% query resolution improvement), re-architected AWS EKS to serverless Lambda, A/B testing framework (40% token efficiency)
- **IBM-TWC freelance** (Feb 2023 - present): 60% processing time reduction, 30% infrastructure savings, data quality frameworks, dbt migrations

### Phase 3: AI-Augmented Architect (2024-present)
- **Soul ecosystem**: 31 interconnected projects (20 public), 9,700 lines production code in soul-os
- **AI tool mastery**: Claude Code power user — 14 subagents, hookify rules, CLAUDE.md workflows, custom commands
- **Paradigm shift**: From "How do I code this?" to "How do I achieve this?"

---

## Key Proof Points

| Metric | Source |
|--------|--------|
| 5,000+ concurrent users | GOAT platform, Gartner |
| 99.5% data accuracy, 15 brands | Novartis |
| 60% processing time reduction | IBM-TWC |
| 88% query resolution improvement | GOAT platform |
| 31 interconnected projects | Soul ecosystem |
| 20 public repositories | GitHub |
| 9,700 lines production code | soul-os |
| 14 Claude Code subagents | Soul command center |
| CARS metric (original research) | soul-bench / soul-eval |

---

## What NOT to Claim

- Manual React/frontend proficiency (build with AI tools)
- Manual TypeScript proficiency (build with AI tools)
- Manual distributed systems coding (architecture is mine, code is AI-generated)
- "Full-stack developer" without the AI-tools qualifier
- Deep ML/model training expertise (I evaluate and orchestrate models, don't train from scratch)

---

## Education

- **Delhi Technological University (DTU)** — B.Tech, Environmental Engineering (2014-2018)

---

## Contact

- Email: mail@rishavchatterjee.com
- LinkedIn: linkedin.com/in/chatterjeerishav
- GitHub: github.com/rishav1305
- Website: rishavchatterjee.com
- Phone: +91 9560382351
```

**Step 3: Commit**

```bash
git add docs/profile/identity.md
git commit -m "Add canonical identity file: single source of truth for all profiles"
```

---

### Task 2: Update MEMORY.md

**Files:**
- Modify: `/home/rishav/.claude/projects/-home-rishav-soul/memory/MEMORY.md`

**Step 1: Add Profile Identity section to MEMORY.md**

Add after the "Project State" section:

```markdown
## Profile Identity

Rishav is an **AI-augmented architect**, not a traditional coder. Key framing rules:

- **Three pillars**: Engineer / Consultant / Researcher — these are his VISION and career targets
- **Honest tech tiers**:
  - Tier 1 "I write": Python, SQL, Bash, Airflow, dbt, data pipelines (6 years hands-on)
  - Tier 2 "I build with AI tools": React, FastAPI, Tauri, WebSocket, Docker, distributed systems
  - Tier 3 "I architect & configure": Claude Code (CLAUDE.md, agents, hooks, commands), system design
- **DO NOT claim** manual proficiency in React, TypeScript, or frontend — he builds these with AI coding tools
- **DO NOT say** "full-stack developer" without qualifying "with AI tools"
- **DO say** he architects systems, directs AI tools, and draws on 6 years of data engineering domain knowledge
- **Canonical source**: `~/soul/docs/profile/identity.md`
```

**Step 2: No commit needed** (memory files aren't in git)

---

### Task 3: Update competencies.md with Honest Tiers

**Files:**
- Modify: `docs/competencies.md`

**Step 1: Add "How I Build" preamble after the title**

Insert after line 1 (`# Soul AI — Competency Signals`):

```markdown

## How I Build

All Soul ecosystem projects are built using AI coding tools (Claude Code primarily, plus Google Copilot, Cline, Kilo Code). The competencies below reflect **what I can architect and ship**, not what I manually code line-by-line. My hands-on coding proficiency is in Python, SQL, and shell scripting (6 years). Everything else is built by directing AI tools with architectural intent and domain knowledge.
```

**Step 2: Fix the "Full-stack development" row in the AI Lab table**

Change line 17 from:
```
| Full-stack development | Python FastAPI + React PWA + Tauri desktop + Click CLI | soul-web, soul-desktop, soul-term |
```
To:
```
| Full-stack systems (AI-built) | Architected Python FastAPI + React PWA + Tauri desktop + Click CLI using AI coding tools | soul-web, soul-desktop, soul-term |
```

**Step 3: Fix the "Clean open source code" row in Developer Community table**

Change line 35 from:
```
| Clean open source code | Working examples, CI, PyPI published | All open repos |
```
To:
```
| AI-augmented open source | Working examples, CI, PyPI published — built with Claude Code + AI tools | All open repos |
```

**Step 4: Commit**

```bash
git add docs/competencies.md
git commit -m "Update competencies with honest tiers preamble and AI-tools qualifier"
```

---

### Task 4: Update strategy.md Positioning

**Files:**
- Modify: `docs/strategy.md`

**Step 1: Update Target Audiences > AI Lab section (lines 109-119)**

Replace the "Key signals" list with:

```markdown
Key signals:
- Architects production AI systems using AI coding tools (31 projects, 9,700 lines)
- CARS metric (original research)
- Boundary enforcement (AI safety thinking)
- Hub election algorithm (distributed systems architecture)
- Claude Code power user: custom agents, hooks, CLAUDE.md, commands
```

**Step 2: Update CTO/VP section value prop (line 125)**

Change from:
```
Value prop: "I build production AI agent systems."
```
To:
```
Value prop: "I architect and ship production AI systems 10x faster by combining 6 years of data engineering with AI coding tools."
```

**Step 3: Commit**

```bash
git add docs/strategy.md
git commit -m "Update strategy positioning to reflect AI-augmented architect identity"
```

---

### Task 5: Draft GitHub README

**Files:**
- Modify: `rishav1305/README.md`

**Step 1: Write the new README**

Full replacement of `rishav1305/README.md`. Key changes:
- New lead with one-liner from identity.md
- Three pillars: Engineer / Consultant / Researcher (revised descriptions)
- Tech stack badges split into "I write" and "I build with AI" rows
- Updated Claude Code Power User section emphasizing configuration mastery
- Keep highlighted projects table
- Keep "Currently Building" and "Open to" sections

**Step 2: Show to user for approval**

Print the full README and ask: "Here's the updated GitHub README. Approve before I commit/push?"

**Step 3: Commit (only after approval)**

```bash
git add rishav1305/README.md
git commit -m "Update GitHub profile README: AI-augmented architect identity"
```

**DO NOT push to GitHub without explicit user approval.**

---

### Task 6: Draft LinkedIn Content

**Files:**
- Create: `drafts/linkedin-headline.md`
- Create: `drafts/linkedin-about.md`

**Step 1: Write headline draft**

```markdown
AI Engineer | Consultant | Researcher — Building Production AI Systems with AI Coding Tools | Python, Data Platforms, Claude Code
```

Note: LinkedIn headline max is 220 chars. This is ~115 chars, fits well.

**Step 2: Write About section draft**

Three pillars + honest tech tiers + currently building. Keep under LinkedIn's 2,600 char limit. No consulting rates mentioned. Professional tone.

**Step 3: Show both to user for approval**

Print headline + about section and ask: "Here's the LinkedIn update. Approve before I update?"

**Step 4: Commit drafts**

```bash
git add drafts/linkedin-headline.md drafts/linkedin-about.md
git commit -m "Draft LinkedIn headline and about section for profile overhaul"
```

**User must manually update LinkedIn** — we only draft, never publish.

---

### Task 7: Draft Website Update Spec

**Files:**
- Create: `drafts/website-updates.md`

**Step 1: Write update spec for rishavchatterjee.com**

Document what needs to change on the website:
- Professional Summary: new identity one-liner
- Core Skills: replace flat list with honest tiers
- New section: "How I Work" (AI-augmented workflow description)
- Projects: add Soul ecosystem highlights
- Update availability line

**Step 2: Show to user for approval**

This is a spec, not code. The website is hosted externally (Next.js on Vercel). The user or a future session will implement the actual code changes.

**Step 3: Commit**

```bash
git add drafts/website-updates.md
git commit -m "Draft website update spec for profile overhaul"
```

---

### Task 8: Draft Resume Update

**Files:**
- Create: `drafts/resume-updates.md`

**Step 1: Write resume update spec**

Document changes to the resume:
- New summary paragraph with AI-augmented architect framing
- Tech stack section using tiers
- New "Portfolio / Current Projects" section with Soul ecosystem
- Experience bullets stay (real accomplishments)
- Skills deprioritized: React, Next.js, TypeScript (unless qualified)

**Step 2: Show to user for approval**

**Step 3: Commit**

```bash
git add drafts/resume-updates.md
git commit -m "Draft resume update spec for profile overhaul"
```

---

### Task 9: Final Review and Consistency Check

**Files:**
- Read: all files created/modified in Tasks 1-8

**Step 1: Cross-check all platforms against identity.md**

Verify:
- Three pillars appear consistently across all platforms
- Honest tiers are used everywhere (no platform claims manual React/TS proficiency)
- One-liner is consistent
- Key proof points match
- "What NOT to claim" rules are respected

**Step 2: Report any inconsistencies to user**

**Step 3: Final commit if any fixes needed**

---

## Execution Notes

- Tasks 1-4 (internal docs) can proceed without user approval — these are internal files
- Tasks 5-8 (public-facing drafts) each require explicit user approval before any publishing
- Task 5 (GitHub README) requires approval before git push
- Task 6 (LinkedIn) produces drafts only — user updates LinkedIn manually
- Task 7 (Website) produces a spec — actual code changes are a separate session
- Task 8 (Resume) produces a spec — user updates resume in their preferred editor
- Nothing goes public without explicit user approval
