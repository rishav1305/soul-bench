# claude-task-manager

> A Claude Code extension that lets users queue tasks and runs them autonomously in the background.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Developer Tools / Claude Code Extension |
| Status | Spec Only |
| License | MIT |

## What It Is

A task management extension for Claude Code that gives users a persistent task queue. Users add tasks (build this, fix that, research this), and Claude Code picks them up and executes them in the background -- one at a time or in parallel -- reporting results when done.

Think of it as a background job runner for AI coding tasks: you queue work, keep coding, and Claude handles it asynchronously.

## Problem

Today in Claude Code, tasks are synchronous. You ask Claude to do something, wait for it to finish, then ask the next thing. For multi-step work:

- You can't queue 5 tasks and walk away
- Background agents exist but lack a persistent queue with priorities and dependencies
- No way to schedule recurring tasks (daily code review, weekly dependency audit)
- No dashboard to see what's running, what's queued, what finished

## Architecture

```
User (Claude Code CLI)
  │
  ├── /task add "Extract soul-skills from backup"
  ├── /task add "Run full test suite" --depends-on 1
  ├── /task add "Update README" --priority high
  ├── /task list
  ├── /task status 1
  │
  ▼
┌─────────────────────────┐
│   Task Queue (SQLite)   │
│                         │
│  id | task | status     │
│  1  | Extract... | running │
│  2  | Run tests  | blocked │
│  3  | Update README | queued │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   Task Runner Engine    │
│                         │
│  - Picks next task      │
│  - Spawns Claude agent  │
│  - Monitors progress    │
│  - Captures output      │
│  - Handles failures     │
│  - Respects dependencies│
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Background Agents      │
│                         │
│  Agent 1: [extracting]  │
│  Agent 2: [idle]        │
│  Agent 3: [idle]        │
└─────────────────────────┘
```

## Core Concepts

### Task Lifecycle

```
queued -> running -> completed
                  -> failed -> retry (up to N times)
         blocked (waiting on dependency)
         cancelled (by user)
```

### Task Definition

```yaml
id: 1
title: "Extract soul-skills from backup"
description: "SSH to titan-pc, extract skills files, create standalone project"
priority: normal  # low | normal | high | critical
status: queued
depends_on: []
max_retries: 1
created_at: 2026-02-22T09:00:00Z
context:
  working_dir: ~/soul/soul-skills
  files: []
  instructions: "Follow extraction pattern from CLAUDE.md"
```

### Features

- **Persistent queue** -- tasks survive across sessions (SQLite-backed)
- **Dependencies** -- task 2 waits for task 1 to finish
- **Priority scheduling** -- critical tasks jump the queue
- **Parallel execution** -- configurable concurrency (default: 1 agent)
- **Progress tracking** -- real-time status updates per task
- **Failure handling** -- automatic retry with backoff, or mark failed
- **Context passing** -- each task gets working directory, relevant files, instructions
- **Output capture** -- full agent output saved per task for review
- **Recurring tasks** -- cron-like scheduling for repeating work

## CLI Interface

```
/task add "description"           # Add a task to the queue
/task add "desc" --priority high  # Add with priority
/task add "desc" --depends-on 1,2 # Add with dependencies
/task list                        # Show all tasks with status
/task status <id>                 # Detailed status of one task
/task output <id>                 # Show captured output
/task cancel <id>                 # Cancel a queued/running task
/task retry <id>                  # Retry a failed task
/task clear --completed           # Remove completed tasks
/task run                         # Start the runner (picks up queued tasks)
/task pause                       # Pause the runner (finish current, don't start new)
```

## Implementation Approach

### Claude Code Extension Points

- **Custom slash commands** -- `/task` command family
- **Background agents** -- Task tool with `run_in_background: true`
- **Persistent storage** -- SQLite in `~/.claude/task-manager/tasks.db`
- **Skills integration** -- Each task can reference a skill to use

### Tech Stack

- Python 3.11+
- SQLite (via aiosqlite) for task persistence
- Claude Code Task tool for background agent spawning
- Rich/Click for CLI formatting

## Strategic Value

- Demonstrates understanding of async task orchestration, job queues, and developer tooling
- Directly useful for Claude Code power users who want to queue work
- Portfolio piece: "I built a background task runner for AI coding agents"
- Could become an official Claude Code community extension

## Prior Art

- GitHub Actions (queue workflows, dependencies, parallel jobs)
- Celery (Python task queue with retry, priority, dependencies)
- soul-loop (soul-os autonomous task scheduler -- similar concept, different runtime)

## Relationship to Soul Ecosystem

- Replaces the need for soul-skills runtime engine (Claude Code handles orchestration natively)
- Complements soul-loop (soul-loop is for soul-os; this is for Claude Code)
- Can use `.claude/skills/` for task templates
