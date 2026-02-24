# Daily Content Strategy — "The Content Refinery"

**Date:** 2026-02-23
**Status:** Approved (v2 — revised with cognitive-mode agents + platform-specific frequency)
**Approach:** Build in Public with Single-Topic Days (LinkedIn/Substack) + Multi-Topic Days (Twitter/Reddit)

---

## Problem

Block 3 (MARKET) was doing two unrelated things: content creation and job hunting. Content was planned at 2 posts/week with a rigid day-of-week rotation and copy-paste across platforms. Topics were picked by the system, not the user. No tracking of what was posted or where.

## Solution

1. Split into 4 blocks: SOCIAL (content) and SCOUT (jobs) are separate
2. Platform-specific frequency and tone (not one-size-fits-all)
3. Single-Topic Days for algorithm authority (LinkedIn/Substack), Multi-Topic Days for real-time energy (Twitter/Reddit)
4. Cognitive-mode agents (short-form vs long-form) instead of per-platform agents
5. Content Refinery pipeline: Capture -> Strategy -> Draft -> Publish -> Track
6. Post tracker for logging what was published and engagement metrics

---

## Platform Strategy

| Platform | Frequency | Content Style | Audience |
|----------|-----------|---------------|----------|
| Twitter/X | 1-2x daily | Raw technical wins, build-in-public updates, AI news | Developers, tech peers |
| LinkedIn | 3x/week (Mon/Wed/Fri) | Polished launches, career insights, AI & law | Hiring managers, consulting clients |
| Reddit | Daily engagement | Comment on 3-5 threads in r/LocalLLaMA, r/selfhosted. No self-promo. | Developer community |
| Substack | 1x/week | Weekly digest or deep-dive research piece | Subscribers, researchers |
| dev.to / Hashnode | 2x/month | Practical technical tutorials, cross-posted from blog | Developer community |
| Personal Blog | 1-2x/month | Canonical long-form research and product documentation | All audiences |
| Hugging Face | Per project | Major releases (fine-tuned models, Gradio spaces) | ML community |
| GitHub | 3-5 commits/week | Continuous commit evidence | Recruiters, developers |

### Platform Tone

- **Twitter/X:** Raw, fast, honest. Hooks and threads. "Just got soul-mesh inference working across 2 devices" energy.
- **LinkedIn:** Professional, data-first. Lead with metrics or lessons. No buzzwords.
- **Reddit:** Genuinely helpful. Answer questions, share insights. Never self-promote without adding value. Know each subreddit's culture.
- **Substack:** Research-depth. Can be 1,500+ words. Newsletter format with subscriber value.
- **dev.to / Hashnode:** Tutorial-style, reproducible. Step-by-step with code.
- **Blog:** Authoritative long-form. The canonical source others link to.

---

## Topic Strategy

### Single-Topic Days (LinkedIn + Substack)

AI-driven discovery engines categorize expertise better when you stick to one theme per day. This builds Topic Authority.

| Day | Topic Theme | Examples |
|-----|-------------|---------|
| Monday | AI Engineering | Agentic workflows, Python, LLMs, soul-planner, soul-mesh |
| Wednesday | Product Shipping | Updates on soul-* projects, architecture decisions, shipping insights |
| Friday | AI & Law | LLM research applied to legal domain, criminology insights |

### Multi-Topic Days (Twitter + Reddit)

These platforms are chronological and reward real-time energy. Post whatever was built today. If you're working on a Raspberry Pi server rack in the morning and legal research in the afternoon, post both.

### The Synergy Rule

Bridge topics at intersections instead of keeping them in silos:
- Don't just post about Law -> Post about **automating legal research using local LLMs**
- Don't just post about Server Rack -> Post about **hardware requirements for running a private legal data vault**
- Don't just post about Shipping -> Post about **analytics of how AI developers use your specific tools**

---

## Agent Architecture: 4 Cognitive-Mode Agents

Grouped by linguistic and strategic requirements, not by platform.

```
[Git Commits + Research Notes + Content Log]
              |
      [1. THE ARCHITECT]
      Capture + Strategy
      Reads: git log (72h), post-log (72h), content-log
      Decides: topic + platform routing + draft angles
              |
      ┌───────┴───────┐
      |               |
[2. SHORT-FORM]  [3. LONG-FORM]
  Ghostwriter      Authority
  Twitter + Reddit   LinkedIn + Blog + Substack
      |               |
      └───────┬───────┘
              |
       [User Review]
       5 min HITL
              |
       [Post API]
       Buffer or custom Python
              |
       [4. THE ANALYST]
       Track + Pivot Logic
```

### Agent 1: The Architect (Orchestrator)

**Role:** Capture + Strategy phases.
**Input:** Git commits (last 72h via Gitea API), post-log (what was already published), content-log (raw notes).
**Output:** Today's topic, platform routing, draft angles for each agent.
**Key skill:** Single source of truth for brand voice. Knows which topics have been covered recently. Prevents duplication.

### Agent 2: Short-Form Ghostwriter (Twitter + Reddit)

**Role:** High-velocity, high-engagement content.
**Platforms:** Twitter/X threads, Reddit comments.
**Tone:** Hooks, snark, "uncomfortably honest" Reddit energy. Raw technical wins.
**Platform knowledge:** X character limits (280/tweet), Reddit no-self-promo rules, r/LocalLLaMA culture, r/selfhosted expectations.

### Agent 3: Long-Form Authority (LinkedIn + Blog + Substack)

**Role:** Structured, SEO-friendly, professional content.
**Platforms:** LinkedIn posts, blog articles, Substack newsletters.
**Tone:** Data-first, professional. Can bridge AI engineering and law. Hashtag strategy, newsletter formatting.
**Platform knowledge:** LinkedIn 3,000 char limit, SEO best practices, Substack newsletter layout.

### Agent 4: The Analyst (Tracker)

**Role:** Track phase + pivot logic.
**Input:** Post-log with engagement metrics.
**Output:** Not just numbers -- actionable pivot recommendations.
**Example:** "Your hardware posts on r/LocalLLaMA get 10x clicks vs AI Law posts. Suggest moving hardware content to Tuesday."
**Weekly:** Engagement report with platform-specific trends and topic performance.

### Why Cognitive-Mode > Per-Platform

1. **Context consistency:** Short-form and long-form groups maintain cohesive personality. Separate per-platform agents hallucinate different brand voices.
2. **Token efficiency:** Brand guidelines passed to 4 agents instead of 8.
3. **Lower maintenance:** If X changes its algorithm, update one agent, not five.

---

## Block 3: SOCIAL Workflow (2 hours)

### The Content Refinery Pipeline

```
7:00 PM - 7:15 PM  CAPTURE (15 min)
  Pull git commits from last 72 hours (git log or Gitea API)
  Review post-log: what was published in last 72 hours
  Dump raw notes into content-log if not already captured during BUILD/EXPLORE
  Identify gaps: what was built but not yet posted about

7:15 PM - 7:30 PM  STRATEGY (15 min)
  Architect agent analyzes: fresh work, covered topics, today's theme day
  Proposes: topic + platform routing + draft angles
  User approves topic or redirects

7:30 PM - 8:00 PM  DRAFT (30 min)
  Short-Form + Long-Form agents draft in parallel
  Short-Form: Twitter thread + Reddit comment angles
  Long-Form: LinkedIn post (if Mon/Wed/Fri) + blog section (if applicable)
  User reviews drafts (5 min each)

8:00 PM - 8:30 PM  PUBLISH + ENGAGE (30 min)
  Post via API or manual
  Respond to comments/DMs from previous posts
  Reddit: comment on 3-5 relevant threads (r/LocalLLaMA, r/selfhosted)

8:30 PM - 9:00 PM  TRACK (30 min)
  Log all posts to post-tracker (docs/post-log.md)
  Pull yesterday's engagement metrics
  Analyst agent: weekly pivot recommendations (Saturdays)
```

---

## Block 4: SCOUT Workflow (2 hours)

```
9:00 PM - 9:30 PM  SCAN (30 min)
  Check job portals for new matches (LinkedIn Jobs, Naukri, Indeed)
  Check freelance platforms for inbound (Toptal, Turing, Wellfound)

9:30 PM - 10:15 PM  APPLY (45 min)
  Apply to 2-3 best matches
  Customize cover letters / pitch for each
  Update portfolio links if needed

10:15 PM - 10:45 PM  OUTREACH (30 min)
  Respond to recruiter messages
  Send 2-3 connection requests to relevant recruiters/hiring managers
  Follow up on pending applications (1 week old+)

10:45 PM - 11:00 PM  LOG (15 min)
  Update SCOUT tracker: applications sent, responses received
  Refresh Naukri/Indeed profiles (triggers "recently active" boost)
```

---

## Tracking System

### Content Log (docs/content-log.md)

Raw capture during BUILD and EXPLORE blocks:
```
DATE | BLOCK | What happened (1-2 lines) | Topic hint
2026-02-23 | BUILD | soul-planner SQLite schema + 67 tests | ai-engineering
2026-02-23 | EXPLORE | Claude Code Task tool internals researched | ai-engineering
```

### Post Log (docs/post-log.md)

What was actually published:
```
DATE | PLATFORM | TOPIC | TITLE/HOOK | LINK | LIKES | COMMENTS | VIEWS
2026-02-23 | LinkedIn | product-shipping | "Cut 37 projects to 5" | linkedin.com/... | 12 | 3 | 450
2026-02-23 | Twitter | ai-engineering | Thread: soul-planner architecture | x.com/... | 8 | 2 | 200
```

### Weekly Analyst Report (Saturday)

The Analyst agent produces a weekly pivot report:
- Top-performing content by platform
- Topic authority scores (which topics get most engagement)
- Pivot recommendations (shift timing, topic emphasis, platform focus)
- Follower/subscriber growth trends

---

## Content Quality Gates

Three gates before anything goes public:

1. **Concrete artifact?** Must contain a metric, diagram, code snippet, or specific result. No vague "working on stuff" posts.
2. **Audience value?** At least one audience (hiring manager / consulting prospect / developer) must learn something.
3. **Identity match?** Matches Rishav's framing as AI-augmented architect. Honest tech tiers. No overclaiming.

All content requires user review and approval before posting.

---

## Weekly Cadence

| Day | LinkedIn | Twitter | Reddit | Substack | Blog | dev.to |
|-----|----------|---------|--------|----------|------|--------|
| Mon | AI Engineering post | 1-2 tweets | 3-5 comments | -- | -- | -- |
| Tue | -- | 1-2 tweets | 3-5 comments | -- | -- | -- |
| Wed | Product Shipping post | 1-2 tweets | 3-5 comments | -- | -- | -- |
| Thu | -- | 1-2 tweets | 3-5 comments | -- | -- | -- |
| Fri | AI & Law post | 1-2 tweets | 3-5 comments | -- | -- | -- |
| Sat | -- | 1 tweet (blog link) | -- | Weekly digest | Blog post | -- |
| Sun | -- | -- | -- | -- | -- | -- |
| 2x/month | -- | -- | -- | -- | -- | Tutorial |

---

## Metrics

| Metric | Target (Week 1) | Target (Month 1) |
|--------|-----------------|-------------------|
| Twitter posts/week | 7 | 10 |
| LinkedIn posts/week | 3 | 3 |
| Reddit comments/week | 15 | 20 |
| Substack issues/month | 2 | 4 |
| Blog posts/month | 1 | 2 |
| dev.to tutorials/month | 1 | 2 |
| LinkedIn impressions/week | 200 | 1,000 |
| Twitter impressions/week | 100 | 500 |
| Substack subscribers | 0 | 25 |
| Inbound messages/week | 0 | 3 |
