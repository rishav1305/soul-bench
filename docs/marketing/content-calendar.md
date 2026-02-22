# Content Calendar

**Created:** 2026-02-22
**Cadence:** 2 LinkedIn posts/week (Mon + Thu), 1 Twitter thread/week, 3+ standalone tweets/week, 1 blog post/2 weeks
**Voice:** Senior engineer sharing insights. Professional, specific, grounded in real numbers. No emojis.

---

## Content Pillars

1. **Building in public** -- soul ecosystem progress, technical decisions, what worked and what failed
2. **AI engineering lessons** -- insights from 6 years of data engineering + AI tools
3. **Data/numbers posts** -- concrete metrics from past work (88% query resolution, 60% time reduction, 99.5% accuracy)
4. **Opinion/contrarian takes** -- hot takes on AI engineering, tools, agent frameworks

## Content Repurposing Flow

```
Blog post (long, ~2000 words)
  -> 2-3 LinkedIn posts (key insights, excerpts)
    -> 1 Twitter thread (5-7 tweets)
      -> 3-5 standalone tweets (atomic insights)
        -> 1-2 community posts (Reddit, Slack, Discord -- when relevant)
          -> Cold outreach attachment ("wrote about X")
```

---

## Week 1 (Feb 24 - Mar 1)

### LinkedIn Post 1 (Monday)
**Pillar:** Building in public
**Topic:** "Why I'm building 31 AI projects as a solo engineer"

**Draft:**

I am building 31 interconnected AI projects. Alone.

Not because I have to. Because the best way to prove you can architect production AI systems is to actually ship them.

Here is the breakdown: 20 public repositories. 9 private. 9,700 lines of production Python and React in the core system (soul-os). Distributed mesh networking. Autonomous agents with boundary enforcement. Self-healing infrastructure. An AI outreach platform. A desktop app in Tauri. A cost-aware model evaluation framework.

No, I did not write every line by hand. I architect every system, design every interface, make every technical decision -- and I use AI coding tools (Claude Code, primarily) as my development environment. The same way a senior engineer uses an IDE, I use an AI pair programmer. The domain knowledge, the system design, the integration decisions -- those are mine. Six years of data engineering across Novartis, Gartner, and IBM gave me that foundation.

The soul ecosystem is not a portfolio exercise. It is a working thesis: that one engineer with deep domain knowledge and AI tools can build what used to take a team of ten.

I will be sharing the architecture, the failures, and the decisions along the way.

What is the most ambitious solo project you have ever attempted?

---

### LinkedIn Post 2 (Thursday)
**Pillar:** AI engineering lessons
**Topic:** "The honest tech stack: what I write vs what AI writes for me"

**Draft:**

I think the tech industry needs more honesty about what we actually do versus what our tools do.

Here is my honest tech stack, broken into three tiers:

Tier 1 -- I write this myself: Python, SQL, Bash, Airflow, dbt. Six years of muscle memory. When I write a data pipeline or a SQL transformation, it is me, line by line.

Tier 2 -- I build this with AI tools: React, FastAPI, Tauri, WebSocket systems, Docker configurations. I design the architecture, define the interfaces, and direct Claude Code to generate the implementation. I review, test, and iterate on everything. But I am not pretending I hand-write React components from scratch.

Tier 3 -- I architect and configure: Claude Code itself (CLAUDE.md files, custom agents, hookify rules, commands), system design, multi-agent orchestration patterns. This is where I spend most of my time now -- designing how systems fit together.

The paradigm shift is real. I went from "How do I code this?" to "How do I achieve this?" My job is no longer typing. It is thinking.

Some people call this cheating. I call it the future of software engineering. The value moved from keystrokes to decisions.

What does your honest tech stack look like? Where do your tools end and your expertise begin?

---

### Twitter Content

**Thread (repurpose Post 1, 5-7 tweets):**

1/ I am building 31 AI projects as a solo engineer. Here is why and how.

2/ The soul ecosystem: 20 public repos, 9 private. Distributed mesh networking. Autonomous agents. Self-healing infra. An outreach SaaS. A desktop app. 9,700 lines of production code in the core.

3/ The honest part: I did not write every line. I architect every system, make every design decision, and use Claude Code as my primary development environment. AI tools are my IDE.

4/ What I bring: 6 years of data engineering at Novartis, Gartner, and IBM. Domain knowledge is the one thing AI tools cannot replace. Knowing what to build matters more than typing speed.

5/ The thesis: one engineer with deep domain knowledge + AI tools can build what used to require a team of ten. Not by working harder. By working at a different level of abstraction.

6/ I will be sharing the architecture, the technical decisions, and the failures publicly. Building in public means showing the messy parts too.

7/ What is the most ambitious solo project you have built?

**Standalone Tweets:**

- The three tiers of an honest tech stack: what you write, what you build with AI, and what you architect. Most engineers only talk about tier 1.

- Hot take: the best measure of a senior engineer in 2026 is not how much code they write. It is how well they direct the systems that write code for them.

- Shipped soul-mesh hub election this week -- 16 tests passing. Distributed leader election for multi-device AI systems. Building in public, one module at a time.

---

### Blog
- **Start outline** for "How I Architect 31 Projects as a Solo Engineer with AI Tools"
- Sections: motivation, the soul ecosystem map, the honest tech tiers, Claude Code as development environment, what scales and what does not, lessons learned

---

## Week 2 (Mar 2 - Mar 8)

### LinkedIn Post 1 (Monday)
**Pillar:** Data/numbers
**Topic:** "What I learned building a 5,000-user AI platform at Gartner"

**Draft:**

In 2023, I helped launch GOAT -- an agentic AI platform at Gartner that grew to over 5,000 concurrent users.

Here are the numbers that shaped how I think about production AI:

88% query resolution improvement. That was the headline metric. But getting there meant re-architecting the entire serving layer -- migrating from AWS EKS to serverless Lambda to handle unpredictable traffic spikes without burning through compute budget.

40% token efficiency gain. We built an A/B testing framework specifically for prompt engineering. Not just "does this prompt work better?" but "does this prompt work better per dollar spent?" Cost-aware optimization changes how you think about model performance.

The biggest lesson was not technical. It was organizational. AI platforms fail not because the models are bad, but because the feedback loops are too slow. We shortened the cycle from "user complains" to "prompt updated in production" from weeks to hours. That mattered more than any architecture decision.

Building for 5,000 users also taught me that AI system reliability is fundamentally different from traditional software reliability. A 500 error is obvious. A subtly wrong AI response is invisible until someone loses trust.

I now build every AI system with observability and evaluation as first-class concerns, not afterthoughts.

What is the most counterintuitive lesson you have learned from shipping AI to real users?

---

### LinkedIn Post 2 (Thursday)
**Pillar:** Building in public (technical)
**Topic:** "Hub election algorithms: how distributed AI systems pick a leader"

**Draft:**

When you run AI agents across multiple devices -- a laptop, a phone, a home server -- someone has to be in charge. That is the hub election problem.

I have been building soul-mesh, a distributed networking layer for AI systems, and hub election is the core challenge. Here is how it works at a high level:

Every node in the mesh evaluates itself on three dimensions: compute capacity, network stability, and current load. These scores get broadcast to all peers. The node with the highest composite score becomes the hub -- the coordinator that routes messages, syncs state, and manages the agent lifecycle.

But the interesting part is failure handling. What happens when the hub goes offline? The remaining nodes need to detect the failure, trigger a new election, and re-converge -- all without losing in-flight messages or duplicating agent work. The protocol uses heartbeat timeouts with hysteresis to avoid flapping (where leadership bounces back and forth during network instability).

This is not a theoretical exercise. If you want AI agents that work across your devices seamlessly, you need a coordination layer that handles the messy reality of consumer networks: variable latency, NAT traversal, intermittent connectivity.

16 tests passing. The election module is extracted and standalone. More to come.

What problems are you solving in distributed AI systems?

---

### Twitter Content

**Thread (repurpose Post 1, 5-7 tweets):**

1/ I helped build an AI platform that grew to 5,000+ users at Gartner. Here are the lessons that changed how I build AI systems.

2/ 88% query resolution improvement. The headline number. But the real work was re-architecting from EKS to serverless Lambda. AI traffic is spiky and unpredictable. Traditional scaling does not cut it.

3/ 40% token efficiency from an A/B testing framework for prompts. The question is not "does this prompt work better?" It is "does this prompt work better per dollar?" Cost-aware optimization is underrated.

4/ The biggest lesson was not technical. Feedback loop speed matters more than architecture. We cut the cycle from "user reports bad response" to "prompt updated in production" from weeks to hours.

5/ AI reliability is fundamentally different from software reliability. A 500 error is obvious. A subtly wrong AI response is invisible until trust erodes. Observability is not optional.

6/ I now treat evaluation and observability as first-class architectural concerns in every AI system I build. Not afterthoughts. Not nice-to-haves. Core infrastructure.

7/ What is the most counterintuitive lesson you have learned shipping AI to production?

**Standalone Tweets:**

- The difference between a demo and production AI: observability. If you cannot measure when your model is subtly wrong, you do not have a product.

- Cost-per-query should be on every AI system dashboard right next to accuracy. We built an A/B framework at Gartner specifically for this. 40% token savings.

- Just extracted the hub election module from soul-mesh into a standalone package. Distributed leader election for multi-device AI systems. Clean interfaces, 16 tests, zero dependencies on the monolith.

---

### Blog
- **Continue outline** for blog post #1, start writing introduction and "soul ecosystem map" section

---

## Week 3 (Mar 9 - Mar 15)

### LinkedIn Post 1 (Monday)
**Pillar:** Opinion/contrarian
**Topic:** "AI tools didn't make me a worse engineer. They made me an architect."

**Draft:**

There is a growing narrative that AI coding tools are making engineers lazy. That we are losing fundamental skills. That the next generation will not know how to debug a segfault.

I disagree. Not because I think the concern is baseless -- it is real for people who never had the fundamentals to begin with. But for engineers with deep domain knowledge, AI tools do something different. They elevate you.

I spent six years writing Python, SQL, and Bash by hand. Building data pipelines at Novartis. Debugging Airflow DAGs at 2 AM. Wrestling with Snowflake query optimization. That foundation is not gone. It is the reason I can effectively direct AI tools now.

The shift is not from "engineer" to "non-engineer." It is from "How do I code this?" to "How do I achieve this?" I spend my time on system design, integration architecture, failure mode analysis, and evaluation frameworks. The things that actually determine whether a project succeeds or fails.

When I architect 31 interconnected AI projects using Claude Code, I am not outsourcing my thinking. I am applying my thinking at a higher level of abstraction. The domain knowledge guides every prompt. The systems experience catches every architectural mistake the tool makes.

AI tools did not replace my engineering skills. They gave those skills leverage.

The question is not whether you use AI tools. It is whether you have the depth to use them well.

---

### LinkedIn Post 2 (Thursday)
**Pillar:** Data/numbers
**Topic:** "99.5% data accuracy across 15 pharma brands: lessons from Novartis"

**Draft:**

At Novartis, I worked on data platforms serving 15 pharmaceutical brands. The accuracy requirement was 99.5%. In pharma, the remaining 0.5% can mean regulatory findings.

Here is what I learned about data quality at that scale:

We migrated from HIVE to Snowflake and saw a 60% performance gain. But performance was not the point. The migration was driven by data quality. HIVE's schema-on-read approach meant bad data surfaced late -- sometimes weeks after ingestion. Snowflake's tighter validation caught issues at the gate.

Airflow orchestration was critical. Not just for scheduling, but for building quality checkpoints into every pipeline stage. We treated data validation as a first-class step, not an afterthought. Every transformation had assertion tests. Every load had row-count reconciliation.

The hardest part was not the technology. It was getting 15 brand teams to agree on data definitions. "Net sales" meant something different to every team. Standardization was a political problem disguised as a technical one.

Three lessons I still apply today: First, validate early and often -- catching bad data at ingestion is ten times cheaper than catching it in a report. Second, make data quality visible -- dashboards showing accuracy metrics changed behavior faster than any policy memo. Third, the hardest data problems are definitional, not computational.

These lessons from regulated-industry data engineering now inform how I build AI system evaluation frameworks.

What is the highest-stakes data quality challenge you have worked on?

---

### Twitter Content

**Thread (repurpose opinion post, 5-7 tweets):**

1/ "AI tools make engineers lazy." I keep hearing this. Here is why I think it is wrong -- for engineers who already have depth.

2/ I spent 6 years writing Python, SQL, and Bash by hand. Data pipelines at Novartis. Airflow DAGs at Gartner. That foundation is still there. AI tools did not erase it.

3/ What changed: I went from "How do I code this?" to "How do I achieve this?" The shift is not from engineer to non-engineer. It is from coder to architect.

4/ When I build 31 projects with Claude Code, I am not outsourcing my thinking. I am applying my domain knowledge at a higher level. System design. Integration patterns. Failure mode analysis.

5/ The tools catch syntax. I catch architectural mistakes. The tools generate implementations. I design the system those implementations fit into.

6/ AI tools did not replace my engineering skills. They gave those skills leverage. The question is not whether you use them. It is whether you have the depth to direct them well.

7/ The real risk is not experienced engineers using AI tools. It is junior engineers who never build the foundation that makes AI tools effective.

**Standalone Tweets:**

- Data quality lesson from pharma: catching bad data at ingestion is 10x cheaper than catching it in a report. This applies to AI evaluation too -- validate your model outputs early and often.

- Unpopular opinion: most AI agent frameworks are over-engineered for what people actually need. A well-structured prompt with clear boundaries beats a complex orchestration layer 90% of the time.

- The hardest problems in enterprise data are not computational. They are definitional. Getting 15 teams to agree on what "net sales" means is harder than building the pipeline.

---

### Blog
- **Finish draft** of blog post #1 ("How I Architect 31 Projects as a Solo Engineer with AI Tools")
- Start editing pass

---

## Week 4 (Mar 16 - Mar 22)

### LinkedIn Post 1 (Monday)
**Pillar:** Building in public
**Topic:** "Building in public update: soul-mesh, soul-agents, soul-outreach"

**Draft:**

Four weeks of building in public. Here is what shipped, what stalled, and what I learned.

Shipped: soul-mesh hub election is extracted and standalone. 16 tests passing. Distributed leader election, heartbeat monitoring, and failure detection -- all working without any dependency on the monolith. The node discovery and transport layers are next.

In progress: soul-outreach has a working config system and a Claude API client wrapper. The database layer and campaign pipeline are the current focus. This is the income-critical project -- an AI-powered outreach tool that handles research, personalization, and sending.

Stalled: soul-agents (YAML-based agent definitions with boundary enforcement) is still at spec stage. It is the right architecture, but soul-outreach and soul-mesh had higher priority this month.

What I learned: extraction is harder than greenfield. Pulling modules out of a 9,700-line monolith while keeping them functional is like surgery. Every import is a hidden dependency. Every shared utility needs to be re-implemented or properly isolated. But the result is cleaner code, better test coverage, and repositories that other engineers can actually understand.

Next month: complete soul-outreach Phase 1 (working CLI + web UI), finish soul-mesh transport layer, and start soul-agents extraction.

What are you building this month?

---

### LinkedIn Post 2 (Thursday)
**Pillar:** AI engineering lessons (research)
**Topic:** "CARS: a cost-aware metric for evaluating local AI models"

**Draft:**

Most AI benchmarks measure accuracy. Some measure speed. Almost none measure both in the context of what it actually costs to run the model.

That is why I built CARS -- the Cost-Aware Reasoning Score.

The formula: CARS = Reasoning Accuracy / (VRAM in GB x Latency in seconds).

Here is the problem it solves. Say you are evaluating two local models for a production task. Model A scores 92% accuracy but needs 24GB VRAM and takes 3.1 seconds per request. Model B scores 85% accuracy but runs on 8GB VRAM in 0.9 seconds. Which is better? It depends on your deployment constraints, and CARS gives you a single number to compare.

The evaluation suite uses 10 tasks with Claude as the baseline. The deploy gate requires at least 80% accuracy relative to Claude, no single task below 70%, and P95 latency under 5 seconds. Models that pass all three criteria are production-ready.

Why this matters: as local AI models become viable for production workloads, we need evaluation frameworks that account for the full cost of deployment -- not just accuracy on a benchmark leaderboard. A model that scores 95% but requires a $10,000 GPU is not better than one that scores 88% on hardware you already own.

CARS is part of soul-bench and soul-eval, both open source.

How do you evaluate models for production deployment? What metrics matter most to you?

---

### Twitter Content

**Thread (CARS metric explainer, 5-7 tweets):**

1/ I built a metric for evaluating local AI models that most benchmarks ignore: cost. It is called CARS -- Cost-Aware Reasoning Score. Here is what it does and why it matters.

2/ The formula: CARS = Reasoning Accuracy / (VRAM_GB x Latency_seconds). One number that captures accuracy, memory cost, and speed simultaneously.

3/ The problem: Model A scores 92% accuracy on 24GB VRAM at 3.1s/request. Model B scores 85% on 8GB at 0.9s. Which is better? Depends on your constraints. CARS gives you a comparable number.

4/ The evaluation: 10 tasks, Claude as baseline. Deploy gate: >=80% vs Claude accuracy, no task below 70%, P95 latency under 5 seconds. Pass all three = production-ready.

5/ Why it matters: as local models become viable, we need to stop evaluating on accuracy alone. A model that needs a $10K GPU is not "better" than one that runs on hardware you own.

6/ CARS is part of soul-bench (benchmark suite) and soul-eval (comparison framework). Both will be open source. Contributions welcome.

7/ How do you evaluate models for production? What dimensions matter most beyond raw accuracy?

**Standalone Tweets:**

- Month 1 building in public recap: soul-mesh hub election extracted (16 tests), soul-outreach config + API client done, 8 LinkedIn posts published. Consistency beats intensity.

- Extraction lesson: pulling modules out of a 9,700-line monolith is harder than writing them from scratch. Every import is a hidden dependency. The payoff is code that other engineers can actually read.

- The deploy gate concept: do not just measure if a model is accurate. Measure if it is accurate enough, fast enough, and cheap enough for your specific hardware. Production is a constraint satisfaction problem.

---

### Blog
- **Publish** blog post #1 on rishavchatterjee.com
- Cross-post to dev.to and Hashnode
- Write LinkedIn + Twitter promotion posts for the published article

---

## Blog Post Queue

| # | Title | Status | Target Date |
|---|-------|--------|-------------|
| 1 | How I Architect 31 Projects as a Solo Engineer with AI Tools | Outlining | Week 4 |
| 2 | Building a Self-Healing AI System: Hysteresis + Remediation | Queued | Week 6 |
| 3 | I Built an AI Outreach Tool That Sends Its Own Emails | Queued | Week 8 |
| 4 | Hub Election in Distributed Mesh Networks | Queued | Week 10 |
| 5 | CARS: A Practical Metric for Local AI Model Evaluation | Queued | Week 12 |
| 6 | What Enterprise AI Gets Wrong (And How to Fix It) | Queued | Week 14 |

---

## Metrics to Track Weekly

| Metric | Week 1 | Week 2 | Week 3 | Week 4 |
|--------|--------|--------|--------|--------|
| LinkedIn post impressions | | | | |
| LinkedIn post engagement rate | | | | |
| LinkedIn follower growth | | | | |
| LinkedIn DMs sent / replies | | | | |
| Twitter impressions | | | | |
| Twitter follower growth | | | | |
| Blog views (if published) | | | | |
| Inbound messages received | | | | |
