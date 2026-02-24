---
date: 2026-02-25
status: "Awaiting approval -- do not publish"
platform: Twitter
topic: soul-planner task queue architecture
---

1/ I built a task queue for Claude Code in 48 hours. 1,022 lines of Python. 126 tests. 12 CLI subcommands. Here is how it works.

2/ The problem: Claude Code tasks die when your terminal closes. I wanted a persistent Kanban queue backed by SQLite that survives session restarts and drives Claude through a structured dev workflow autonomously.

3/ Architecture: 6 Python modules. State machine with 5 substeps inside IN_PROGRESS (plan, test, implement, review, validate). Task dependencies use topological ordering. All SQL parameterized. Async throughout via aiosqlite.

4/ The Claude Code layer: 3 slash commands, a task-runner agent that picks up the next ready task and runs the full workflow, and a skill that restores queue state on session start. Schedule mode parses my daily planner markdown and auto-queues tasks.

5/ 8 years of data engineering. I designed the system, directed Claude Code to build it, and shipped it in a weekend. That is what AI-augmented architecture looks like in practice. Repo dropping soon.
