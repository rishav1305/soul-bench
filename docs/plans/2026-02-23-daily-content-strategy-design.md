# Daily Content Strategy — "Build in Public" Stream

**Date:** 2026-02-23
**Status:** Approved
**Approach:** Approach A — Daily content from Block 1 (BUILD) and Block 2 (EXPLORE) work

---

## Problem

Block 3 (MARKET) was doing two unrelated things: content creation and job hunting. Content was planned at 2 posts/week, missing the opportunity to turn daily BUILD and EXPLORE work into a consistent public signal.

## Solution

Split into 4 blocks. Add a dedicated SOCIAL block for daily content. Separate SCOUT block for job/freelance applications.

---

## Daily Rhythm (4 Blocks, 12-14h)

```
Block 1: BUILD   (9am - 1pm,  4h)  Ship projects, extract code, write tests
Block 2: EXPLORE (2pm - 6pm,  4h)  Research, analytics, CARS, finance
Block 3: SOCIAL  (7pm - 9pm,  2h)  Content from Block 1+2 -> all platforms
Block 4: SCOUT   (9pm - 11pm, 2h)  Job portals, freelance platforms, recruiter outreach, applications
```

---

## Content Architecture

Every day's BUILD and EXPLORE work produces one primary content piece, repurposed across platforms.

### Rotating Content Types

| Day | Type | Source Block | Example |
|-----|------|-------------|---------|
| Mon | Deep Dive | BUILD | "How soul-mesh handles hub election under network partitions" |
| Tue | Metrics Post | EXPLORE | "CARS baseline: Phi-3-mini scores 0.42 on 7.6GB RAM" |
| Wed | Architecture Diagram | BUILD | "System diagram: soul-outreach pipeline from import to send" |
| Thu | Opinion/Insight | Either | "Why I stopped writing React manually and started architecting instead" |
| Fri | Weekly Progress | Both | "This week: 203 tests in soul-mesh, CARS v0.2 published" |
| Sat | Blog Assembly | Week's content | Long-form post assembled from Mon-Fri micro-content |
| Sun | Rest | -- | No content production |

---

## Platform Strategy

Each piece gets formatted per platform, not copy-pasted.

| Platform | Format | Audience | Frequency |
|----------|--------|----------|-----------|
| LinkedIn | 800-1200 char professional post, 1-2 tags | Hiring managers, consulting clients | Daily (Mon-Fri) |
| Twitter/X | Thread (3-5 tweets) or single tweet with link | Developer community, tech peers | Daily (Mon-Fri) |
| dev.to | Saturday blog post (600-1000 words) | Developer community | Weekly |
| Reddit | Genuine comments on r/selfhosted, r/MachineLearning | Developer community | 2-3x/week |
| Blog (rishavchatterjee.com) | Full article, canonical URL | All audiences | Weekly (Saturday) |

### Platform Tone

- **LinkedIn:** Data-first, professional. Lead with metrics. No buzzwords.
- **Twitter:** Technical and direct. Show code/diagrams. Engage in threads.
- **dev.to:** Tutorial-style, reproducible. Show the "how."
- **Reddit:** Answer questions, share insights. Never self-promote without adding value.

---

## Block 3: SOCIAL Workflow (2 hours)

```
7:00 PM - 7:15 PM  CAPTURE (15 min)
  Review today's Block 1 + Block 2 work
  Pick 2-3 interesting things: a metric, a decision, a diagram
  Select content type from rotation

7:15 PM - 7:45 PM  DRAFT (30 min)
  Write primary piece (LinkedIn post or blog section)
  Use social-writer agent for first draft
  Review and edit for accuracy + tone

7:45 PM - 8:15 PM  REPURPOSE (30 min)
  Adapt to Twitter thread format
  Queue Reddit comment if relevant thread exists
  Saturday: assemble week's posts into dev.to blog article

8:15 PM - 8:45 PM  PUBLISH + ENGAGE (30 min)
  Post to platforms (LinkedIn + Twitter daily, others as scheduled)
  Respond to comments/DMs from previous posts

8:45 PM - 9:00 PM  LOG (15 min)
  Update content tracker in daily planner
  Note engagement metrics from yesterday's posts
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

## Content Capture System

During Block 1 and Block 2, jot 1-line notes in `docs/content-log.md`:

```
2026-02-23 | BUILD | soul-mesh transport module extracted, 40 new tests | architecture
2026-02-23 | EXPLORE | CARS baseline: Phi-3 3B scored 0.42, 2.1s latency | metrics
```

By 7 PM, there are 2-4 raw content ideas to choose from. No blank-page problem.

---

## Content Quality Gates

Three gates before anything goes public:

1. **Concrete artifact?** Must contain a metric, diagram, or code snippet. If not, add one or skip.
2. **Audience value?** At least one audience (hiring manager / consulting prospect / developer) must learn something.
3. **Identity match?** Matches Rishav's framing as AI-augmented architect. Honest tech tiers. No overclaiming.

All content requires user review and approval before posting.

---

## Weekly Blog Assembly (Saturday)

Not written from scratch — assembled from the week's daily posts:

1. Pull Mon-Fri LinkedIn posts
2. Pick strongest 2-3 themes
3. Expand into 600-1000 word article with metrics/diagrams
4. Publish on blog (canonical), cross-post to dev.to
5. Share link on LinkedIn + Twitter

Saturday Block 3 is mostly editing, not writing.

---

## Automation with Claude Code Agents

- **social-writer agent:** Draft LinkedIn posts and tweets from content-log entries
- **outreach-researcher agent:** Find relevant Reddit threads to comment on
- **knowledge-agent:** Consolidate week's content-log into blog outline

User reviews, edits, and approves. Agents do first-draft work.

---

## Metrics

| Metric | Target (Week 1) | Target (Week 4) |
|--------|-----------------|-----------------|
| LinkedIn posts/week | 5 | 5 |
| Twitter posts/week | 5 | 5 |
| Blog posts/month | 4 | 4 |
| LinkedIn impressions/week | 500 | 2,000 |
| Profile views/week | 50 | 200 |
| Inbound messages/week | 1 | 5 |
| dev.to followers | 0 | 25 |
| Job applications/week | 10 | 15 |
| Recruiter connections/week | 5 | 10 |

---

## Changes from Previous Strategy

| Before | After |
|--------|-------|
| 3 blocks (BUILD, EXPLORE, MARKET) | 4 blocks (BUILD, EXPLORE, SOCIAL, SCOUT) |
| 2 LinkedIn posts/week | 5 LinkedIn posts/week (daily Mon-Fri) |
| Blog planned but not scheduled | Weekly Saturday assembly from daily posts |
| Content + job hunting mixed in Block 3 | Content (SOCIAL) and job hunting (SCOUT) separated |
| Ad-hoc content topics | Rotating content types with capture system |
| No Twitter/dev.to/Reddit | All platforms active |
