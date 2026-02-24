# Content Pipeline Agents Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the generic `social-writer` agent with 4 cognitive-mode agents that implement the Content Refinery pipeline from the content strategy.

**Architecture:** 4 agents split by cognitive mode (not platform). The Architect produces a structured brief, Short-Form and Long-Form writers consume it in parallel, the Analyst tracks and recommends pivots. Each agent is a markdown file in `.claude/agents/` with YAML frontmatter.

**Tech Stack:** Claude Code agent definitions (markdown + YAML frontmatter), no Python code.

**Reference docs:**
- Content strategy: `docs/plans/2026-02-23-daily-content-strategy-design.md`
- Identity: `docs/profile/identity.md`
- Existing agent example: `.claude/agents/social-writer.md`
- Content log: `docs/content-log.md`
- Post log: `docs/post-log.md`

---

### Task 1: Create the Content Architect agent

**Files:**
- Create: `.claude/agents/content-architect.md`

**What it does:** Capture + Strategy phases. Reads git commits (72h), content-log, post-log. Outputs a structured brief with today's topic, platform routing, and draft angles. Prevents duplication by checking what was already posted.

**Step 1: Create the agent file**

Create `.claude/agents/content-architect.md` with:

- YAML frontmatter: name `content-architect`, description with 3 examples (user says "start social block", "what should I post about", "capture today's work"), model `sonnet`, tools `[Read, Glob, Grep]` (read-only -- never writes drafts)
- System prompt sections:
  - **Role:** The Architect -- Capture + Strategy for the Content Refinery pipeline
  - **Input sources:** Git log (72h), `docs/content-log.md`, `docs/post-log.md`, `docs/plans/2026-02-23-daily-content-strategy-design.md`
  - **Topic strategy:** Reference Single-Topic Days (Mon=AI Engineering, Wed=Product Shipping, Fri=AI & Law) for LinkedIn/Substack. Multi-Topic Days for Twitter/Reddit. Sunday=Trending (no commit review).
  - **Duplication check:** Read post-log, skip topics posted in last 72h
  - **Quality gates:** (1) Concrete artifact? (2) Audience value? (3) Identity match?
  - **Identity rules:** Read from `docs/profile/identity.md`. AI-augmented architect, honest tech tiers, no overclaiming.
  - **Output format:** Structured brief (markdown) with: topic, angle, platform routing table, draft angles per writer (short-form angles + long-form angles), concrete artifacts to reference

**Step 2: Verify the YAML frontmatter is valid**

Run: `python3 -c "import yaml; yaml.safe_load(open('.claude/agents/content-architect.md').read().split('---')[1])"`
Expected: No errors, prints the frontmatter dict

**Step 3: Commit**

```bash
git add .claude/agents/content-architect.md
git commit -m "feat: add content-architect agent (Capture + Strategy)"
```

---

### Task 2: Create the Short-Form Writer agent

**Files:**
- Create: `.claude/agents/short-form-writer.md`

**What it does:** Drafts Twitter/X threads and Reddit posts. Raw, fast, honest tone. Consumes the Architect's brief.

**Step 1: Create the agent file**

Create `.claude/agents/short-form-writer.md` with:

- YAML frontmatter: name `short-form-writer`, description with 3 examples (draft tweet, draft Reddit post, draft Twitter thread), model `sonnet`, tools `[Read, Write, Glob]`
- System prompt sections:
  - **Role:** Short-Form Ghostwriter -- high-velocity, high-engagement content
  - **Platforms:** Twitter/X (threads + single tweets) and Reddit (r/ClaudeAI, r/LocalLLaMA, r/selfhosted, r/programming)
  - **Voice:** Raw, fast, honest. Hooks and threads. Build-in-public energy. "Just got X working" energy. No emojis unless user requests.
  - **Twitter rules:** 280 char/tweet max. Threads numbered 1/, 2/. Hook tweet first. No hashtags unless natural. 4-6 tweets max per thread.
  - **Reddit rules:** No self-promo. Genuinely helpful. Know subreddit culture. Share technical approach, not product pitch. Title is a statement of what you built, not a question.
  - **Input:** Expects an Architect brief OR direct user prompt with topic + context
  - **Identity rules:** Reference `docs/profile/identity.md`. Honest tech tiers.
  - **Output:** Save drafts to `docs/drafts/YYYY-MM-DD-{platform}-{topic}.md`. Status: "Awaiting approval -- do not publish."
  - **Quality checklist:** Every claim grounded? No buzzwords? Specific numbers? Within length limits? Would a developer find this credible?

**Step 2: Verify YAML frontmatter**

Run: `python3 -c "import yaml; yaml.safe_load(open('.claude/agents/short-form-writer.md').read().split('---')[1])"`
Expected: No errors

**Step 3: Commit**

```bash
git add .claude/agents/short-form-writer.md
git commit -m "feat: add short-form-writer agent (Twitter + Reddit)"
```

---

### Task 3: Create the Long-Form Writer agent

**Files:**
- Create: `.claude/agents/long-form-writer.md`

**What it does:** Drafts LinkedIn posts, blog articles, and Substack newsletters. Professional, data-first, structured tone. Consumes the Architect's brief.

**Step 1: Create the agent file**

Create `.claude/agents/long-form-writer.md` with:

- YAML frontmatter: name `long-form-writer`, description with 3 examples (draft LinkedIn post, draft blog article, draft Substack newsletter), model `sonnet`, tools `[Read, Write, Glob]`
- System prompt sections:
  - **Role:** Long-Form Authority -- structured, professional content
  - **Platforms:** LinkedIn (posts), Blog (articles), Substack (newsletters), dev.to/Hashnode (tutorials)
  - **Voice:** Professional, data-first. Lead with metrics or lessons. No buzzwords. Can bridge AI engineering and law. No emojis unless user requests.
  - **LinkedIn rules:** 1,500-2,500 chars. Short paragraphs. 3-5 hashtags at the very end, separated from body. Hook line first. CTA at end.
  - **Blog rules:** 400-800 words. Title prefixed with `TITLE:`. SEO-friendly. Practical, reproducible.
  - **Substack rules:** 1,000-1,500 words. Newsletter format with subscriber value. Weekly digest or deep-dive.
  - **dev.to rules:** Tutorial-style, step-by-step with code blocks. Cross-posted from blog.
  - **Input:** Expects an Architect brief OR direct user prompt with topic + context
  - **Identity rules:** Reference `docs/profile/identity.md`. Three pillars (Engineer/Consultant/Researcher). Honest tech tiers. "8 years of data engineering" framing. Never claim manual frontend proficiency.
  - **Output:** Save drafts to `docs/drafts/YYYY-MM-DD-{platform}-{topic}.md`. Status: "Awaiting approval -- do not publish."
  - **Quality checklist:** Every claim grounded? No buzzwords? Specific numbers? Within length limits? Senior engineer credibility? Identity match?

**Step 2: Verify YAML frontmatter**

Run: `python3 -c "import yaml; yaml.safe_load(open('.claude/agents/long-form-writer.md').read().split('---')[1])"`
Expected: No errors

**Step 3: Commit**

```bash
git add .claude/agents/long-form-writer.md
git commit -m "feat: add long-form-writer agent (LinkedIn + Blog + Substack)"
```

---

### Task 4: Create the Content Analyst agent

**Files:**
- Create: `.claude/agents/content-analyst.md`

**What it does:** Track phase + pivot logic. Logs published posts to post-log. On Saturdays, produces weekly pivot report with engagement trends and recommendations.

**Step 1: Create the agent file**

Create `.claude/agents/content-analyst.md` with:

- YAML frontmatter: name `content-analyst`, description with 3 examples (log a published post, pull engagement metrics, weekly pivot report), model `haiku`, tools `[Read, Write, Edit, Glob]`
- System prompt sections:
  - **Role:** The Analyst -- Track phase and pivot logic for the Content Refinery
  - **Daily tasks:** Log published posts to `docs/post-log.md` in the format: `DATE | PLATFORM | TOPIC | TITLE/HOOK | LINK | LIKES | COMMENTS | VIEWS`. Update content tracker in `docs/daily-planner.md`.
  - **Weekly tasks (Saturday):** Produce pivot report: top-performing content by platform, topic authority scores, pivot recommendations (timing, topic emphasis, platform focus), follower/subscriber growth.
  - **Input:** Post details (platform, topic, title, link) OR request for weekly report
  - **Output format for daily:** Updated post-log entry + confirmation
  - **Output format for weekly:** Structured report saved to `docs/reports/weekly-content-YYYY-MM-DD.md`
  - **Rules:** Never fabricate engagement numbers. If metrics aren't available, mark as `--` and note "metrics pending". Track trends over time, not absolute numbers.

**Step 2: Verify YAML frontmatter**

Run: `python3 -c "import yaml; yaml.safe_load(open('.claude/agents/content-analyst.md').read().split('---')[1])"`
Expected: No errors

**Step 3: Commit**

```bash
git add .claude/agents/content-analyst.md
git commit -m "feat: add content-analyst agent (Track + Pivot)"
```

---

### Task 5: Retire old social-writer agent

**Files:**
- Modify: `.claude/agents/social-writer.md`

**Step 1: Update social-writer to redirect**

Replace the social-writer agent body with a redirect notice that points to the 3 new writer agents. Keep the frontmatter valid but update the description to say "Deprecated -- use content-architect, short-form-writer, or long-form-writer instead."

This preserves backward compatibility (the agent still exists if referenced) while steering users to the new agents.

**Step 2: Commit**

```bash
git add .claude/agents/social-writer.md
git commit -m "refactor: deprecate social-writer in favor of cognitive-mode agents"
```

---

### Task 6: Test the pipeline end-to-end

**Step 1: Test content-architect**

Invoke content-architect with: "Analyze the last 72h of work and produce a content brief for today."
Verify: Returns structured brief with topic, platform routing, draft angles.

**Step 2: Test short-form-writer**

Invoke short-form-writer with the Architect's brief + "Draft a Twitter thread and Reddit post about soul-planner."
Verify: Saves drafts to `docs/drafts/`, correct tone, within length limits.

**Step 3: Test long-form-writer**

Invoke long-form-writer with the Architect's brief + "Draft a LinkedIn post about soul-planner."
Verify: Saves draft to `docs/drafts/`, correct tone, within length limits.

**Step 4: Test content-analyst**

Invoke content-analyst with: "Log these draft posts to the post-log as pending."
Verify: Updates `docs/post-log.md`.

**Step 5: Final commit**

```bash
git add docs/drafts/ docs/post-log.md docs/content-log.md
git commit -m "test: verify content pipeline agents end-to-end"
```
