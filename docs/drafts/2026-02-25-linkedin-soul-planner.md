---
date: 2026-02-25
status: "Awaiting approval -- do not publish"
platform: LinkedIn
topic: soul-planner task queue for Claude Code
---

Claude Code has no persistent memory between sessions. Every conversation starts from zero -- no backlog, no priorities, no dependency graph.

So I built one. In 48 hours, soul-planner became a SQLite-backed task queue that plugs directly into Claude Code. 1,022 lines of Python across 6 modules. 126 tests. 12 CLI subcommands.

The problem is straightforward: I run multiple projects simultaneously, each with interdependent tasks. Tracking them in markdown files worked until it didn't. I needed structured state -- something that persists between sessions, enforces ordering, and lets Claude pick up where it left off.

The architecture leans on patterns from 8 years of data pipeline work. Tasks move through Kanban states (BACKLOG, IN_PROGRESS with 5 substeps, VALIDATION, DONE) with explicit transitions. Dependencies use topological ordering -- task B can't start until task A completes. The scheduler reads my daily planner and auto-queues the day's work.

The stack is intentionally boring: async SQLite via aiosqlite for persistence, Pydantic models for task state validation, Click CLI for the 12 subcommands. Security-audited before shipping -- parameterized SQL throughout, no blocking calls in async paths, no hardcoded secrets.

What made this possible in 48 hours wasn't typing speed. It was knowing what to build. Data engineering teaches you that reliable infrastructure is predictable infrastructure: explicit state machines, observable transitions, no magic. I designed the system, directed Claude Code to implement it, and focused my time on architecture decisions and test coverage.

The part worth paying attention to: Claude Code's extension points (CLAUDE.md, agents, skills, slash commands, hooks) make it a configurable platform, not just an autocomplete. soul-planner plugs into all of them -- a task-runner agent, slash commands, and a skill that syncs session state.

If you're building tools on top of AI coding platforms, what patterns are working for you?

#ClaudeCode #AIEngineering #DeveloperTools #Python #TaskAutomation
