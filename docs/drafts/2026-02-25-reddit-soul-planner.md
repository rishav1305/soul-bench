---
date: 2026-02-25
status: "Awaiting approval -- do not publish"
platform: Reddit
subreddit: r/ClaudeAI
topic: soul-planner task queue architecture
---

TITLE: I built a persistent task queue plugin for Claude Code -- here's the architecture
SUBREDDIT: r/ClaudeAI

I kept losing context between Claude Code sessions. Tasks would vanish when the terminal closed. I wanted a persistent queue that survived restarts and could drive Claude through a structured dev workflow without me babysitting it. So I built one over a weekend.

**Architecture**

soul-planner is a Claude Code plugin backed by SQLite. Tasks persist in `~/.claude/soul-planner/tasks.db` across sessions. The core is a state machine:

```
BACKLOG -> IN_PROGRESS -> VALIDATION -> DONE
               |
               +-- planning     (1/5)
               +-- testing      (2/5)
               +-- implementing (3/5)
               +-- reviewing    (4/5)
               +-- validating   (5/5)
```

The five substeps inside IN_PROGRESS enforce a TDD workflow -- tests are written before implementation, and a review pass happens before anything moves to validation. Tasks support dependency ordering via topological sort, so blocked tasks stay queued until their dependencies resolve.

**Module breakdown**

6 Python modules, 1,022 lines total:

- `cli.py` (315 LOC) -- Click CLI with 12 subcommands: add, list, board, status, cancel, block, unblock, done, substep, next, schedule, sync
- `db.py` (313 LOC) -- async SQLite layer via aiosqlite, all queries parameterized with `?`
- `scheduler.py` (174 LOC) -- parses a daily planner markdown file and auto-queues tasks for the day
- `runner.py` (132 LOC) -- orchestrates the 5-substep workflow for a single task
- `models.py` (80 LOC) -- Pydantic models for task state, substep enum, priority

**Claude Code integration**

Three pieces make this work as a plugin:

1. `/planner` slash command -- routes to all 12 subcommands. Each one syncs state back to Claude Code's native `TaskCreate`/`TaskUpdate` tools so the session task panel stays consistent with the SQLite source of truth.

2. `task-runner` agent -- a markdown agent definition that picks up the next ready task and executes the full 5-substep workflow autonomously. If it hits a blocker, it calls `block ID "reason"` and stops instead of guessing. Tool access is restricted to `[Bash, Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate]` -- it cannot reach outside its scope.

3. `task-awareness` skill -- triggers on session start and on phrases like "what's next" or "any tasks." Reads the SQLite DB and restores in-progress state into the Claude Code task panel. This is how session continuity actually works.

**Test coverage**

126 tests via pytest + pytest-asyncio. Covers the state machine transitions, dependency ordering, CLI subcommands, scheduler parsing, and edge cases like circular dependencies and concurrent substep updates.

**What I learned about the Claude Code plugin surface**

Commands (markdown in `commands/`) are essentially scoped system prompts. Agents (markdown in `agents/`) are more powerful because they support `run_in_background: true` for autonomous execution. Skills are the fuzziest -- triggering heuristics required very explicit keyword lists in the skill description to fire reliably.

The agent definition being plain markdown with YAML frontmatter is surprisingly effective. The `tools` list in frontmatter acts as a capability boundary. Restricting the task-runner agent to specific tools felt like the right primitive for autonomous work.

**Background**

I have 8 years of data engineering experience (Python, SQL, Airflow, dbt). I designed soul-planner's architecture and directed Claude Code to implement it. The distinction matters -- I am not claiming I typed 1,022 lines manually. I designed the system, wrote the specs, and used AI tooling to ship it in 48 hours.

Not published yet. Happy to share the plugin structure or agent/skill markdown files if anyone is interested.

---

What are others doing for task persistence across Claude Code sessions? Has anyone found a different approach to the session-state problem?
