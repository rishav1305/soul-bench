---
date: 2026-02-25
status: "Awaiting approval -- do not publish"
platform: Twitter
topic: soul-planner autonomous overnight task execution
---

<!-- PLATFORM OPTIMIZATION NOTES (remove before posting)

OPTIMAL POSTING TIME:
Post at 9:00-10:00 AM IST -- catches US East Coast evening scroll (7pm-8pm ET).
Alternatively 8:00 PM IST for US afternoon audience.

MEDIA (optional -- thread works without images too):
- Tweet 1: Attach a screenshot of `planner board` CLI output or a workflow diagram.
- Tweet 3: Attach a screenshot of the task-runner.md frontmatter showing the restricted tool list.
- Tweets 2, 4, 5: No image needed.

-->

1/ I built a Claude Code plugin so I can queue dev tasks before I sleep. The agent runs them overnight. I wake up and review the completed work. 1,022 lines of Python. 126 tests. Built in 48 hours.

2/ The queue is a SQLite-backed Kanban. Each IN_PROGRESS task runs through 5 substeps: plan, test, implement, review, validate. Tests are written before implementation. Nothing skips steps.

3/ The task-runner agent picks up the next ready task and runs the full workflow. If it hits a blocker, it stops and flags it with a reason. It does not guess. I review everything in the morning before anything ships.

4/ Schedule mode reads my daily planner markdown and auto-queues today's tasks. So the nightly handoff is: I update the planner, the agent reads it, picks up the queue, runs what it can, parks what it can't.

5/ 8 years of data engineering. I designed the system, directed Claude Code to build it. The overnight part works because the failure mode is tight -- blocked means stopped, not improvised. Repo dropping soon. What does your autonomous dev workflow look like?
