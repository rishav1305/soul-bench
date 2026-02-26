---
date: 2026-02-25
status: "Awaiting approval -- do not publish"
platform: Reddit
subreddit: r/ClaudeAI
topic: soul-planner autonomous overnight task execution
---

<!-- PLATFORM OPTIMIZATION NOTES (remove before posting)

FLAIR:
Primary suggestion: "Project" -- this is a project showcase with enough technical depth
to justify it. If "Project" flair is not available, use "Discussion" and lean into the
question at the end to invite conversation.

OPTIMAL POSTING TIME:
Post at 8:00-9:00 AM IST (2:30-3:30 AM UTC) to land in the r/ClaudeAI feed during
US morning scroll (9pm-10pm ET the prior evening). Reddit front page ranking rewards
early votes -- catching active users in the first hour matters more than peak traffic.
Alternatively, 7:00-8:00 PM IST (1:30-2:30 PM UTC) for US East Coast lunch scroll.

CROSS-POST GUIDANCE:
Suitable for cross-post to r/programming with these adjustments:
- Remove the Claude Code-specific plugin surface observations (commands vs agents vs skills)
  -- r/programming audience does not care about Claude Code primitives
- Lead with the architecture decision instead: "The key design choice: fail-stop over
  improvise. The agent blocks and flags rather than guessing."
- Keep the state machine diagram, the numbers, and the TL;DR
- Change the closing question to: "Has anyone else built fail-stop guardrails into an
  autonomous dev workflow? Curious what the failure modes looked like in practice."
- Do NOT cross-post to r/LocalLLaMA -- no inference/hardware content here.
- Do NOT cross-post to r/selfhosted -- no self-hosted infrastructure angle.

-->

TITLE: Built a Claude Code plugin that lets me queue dev tasks before bed -- agent runs them overnight, I review in the morning
SUBREDDIT: r/ClaudeAI

**TL;DR:** soul-planner is a SQLite-backed task queue that plugs into Claude Code as an agent. You queue tasks in the evening. The task-runner agent executes them overnight through a 5-step TDD workflow (plan -> test -> implement -> review -> validate). Blockers stop execution and get flagged with a reason. Nothing ships without human review. 1,022 lines of Python, 126 tests, built in 48 hours.

---

I wanted to delegate development work to Claude Code without being at the keyboard. The pattern I landed on: queue tasks in the evening, the agent runs them overnight through a structured workflow, I review completed work in the morning before anything gets committed. Nothing ships without human review.

Here is how the architecture makes that actually work.

**The queue**

soul-planner is a SQLite-backed Kanban that lives in `~/.claude/soul-planner/tasks.db`. Tasks persist across sessions -- this is what makes overnight execution possible. Each task moves through four top-level states:

```
BACKLOG -> IN_PROGRESS -> VALIDATION -> DONE
```

The interesting part is what happens inside IN_PROGRESS. There are 5 ordered substeps:

```
1. planning      -- scope the task, write a spec
2. testing       -- write tests first (TDD enforced by workflow order)
3. implementing  -- make tests pass
4. reviewing     -- self-review pass before moving on
5. validating    -- confirm the work against original requirements
```

The agent cannot skip steps. It has to complete each substep and call the next CLI command to advance state. This is the guardrail that keeps autonomous execution structured.

**The task-runner agent**

A markdown agent definition (`agents/task-runner.md` in the plugin) with `run_in_background: true`. When invoked, it:

1. Calls `planner next` to get the next ready task (respects dependency ordering via topological sort)
2. Runs through the 5 substeps sequentially, calling `planner substep <id> <step>` to advance state
3. If it hits a blocker -- missing context, ambiguous requirement, failing test it cannot resolve -- it calls `planner block <id> "reason"` and stops

That last point is the most important design decision. The agent stops and flags rather than improvising. In the morning, the review is either: work completed and ready to inspect, or a specific blocker with a reason I can resolve. No surprises.

The agent's tool access is restricted in the frontmatter:

```yaml
tools: [Bash, Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate]
```

It cannot reach outside that scope. No web requests, no external API calls.

**Schedule mode**

I keep a daily planner in markdown (a simple format with dated headers and task bullets). The scheduler module parses this and auto-queues tasks for the current day. The nightly handoff becomes: update the planner file, the agent reads it on next invocation, queues what's ready, runs what it can.

This means I don't have to manually queue tasks each night -- I just maintain the planner I was already keeping.

**Numbers**

- 1,022 lines of Python across 6 modules
- 126 tests (pytest + pytest-asyncio) covering state transitions, dependency ordering, scheduler parsing, CLI subcommands, edge cases like circular dependencies
- 12 CLI subcommands
- Built in 48 hours over a weekend

**What I learned about the Claude Code plugin surface**

Commands (`commands/*.md`) are scoped system prompts -- useful for structured interactions but they don't support background execution. Agents (`agents/*.md`) are more capable because of `run_in_background: true`. The distinction matters a lot for this use case -- commands are interactive, agents can be autonomous.

Skills are the fuzziest primitive. Getting the `task-awareness` skill to trigger reliably required very explicit keyword lists in the skill description. The heuristics for when Claude Code fires a skill feel like keyword matching more than semantic understanding.

**Honest framing**

I have 8 years of data engineering (Python, SQL, Airflow, dbt). I designed soul-planner's architecture and directed Claude Code to implement it. The overnight execution pattern works not because the agent is infallible, but because the failure mode is well-defined: stop and flag, never guess.

The repo is not public yet. Happy to share the agent/skill markdown structure or the state machine design if anyone wants to go deeper.

---

Has anyone else built tooling on top of the Claude Code plugin surface (agents, skills, commands)? Curious what patterns others have found for keeping autonomous execution from going off the rails.
