---
description: "Manage tasks -- add, list, board, status, cancel, block, unblock, done, substep, next"
argument-hint: "<add|list|board|status|cancel|block|unblock|done|substep|next> [args]"
allowed-tools: [Bash, Read, TaskCreate, TaskUpdate, TaskList]
---

# /task -- Task Queue Manager

Manage the soul-planner task queue. All task data persists in SQLite across sessions.

## Setup

The CLI lives at `~/soul/soul-planner/`. If not installed:
```bash
cd ~/soul/soul-planner && pip install -e ".[dev]"
```

## Commands

Route based on the first argument in `$ARGUMENTS`:

### add [title] [--priority low|normal|high|critical] [--details "..."] [--acceptance "..."] [--depends-on 1,2]

**If no title provided (just `/task add`):** Start interactive mode.
1. Ask: "What's the task?"
2. After user answers, ask: "Any specific requirements or acceptance criteria?"
3. Ask: "Priority?" with options: low, normal, high (default), critical
4. Create the task with collected info

**If title provided:** Create immediately.

```bash
python -m soul_planner add "TITLE" --priority PRIORITY --details "DETAILS" --acceptance "CRITERIA" --depends-on IDS
```

After creating, also sync to Claude Code's task UI:
- Use `TaskCreate` with subject = task title, description = task details, activeForm = "Queued: TITLE"

### list [--status STATUS]

```bash
python -m soul_planner list [--status backlog|in_progress|blocked|validation|done|cancelled]
```

Show output to user in a clean table format.

### board

```bash
python -m soul_planner board
```

Show the Kanban board output. This is the default if user just says `/task` with no arguments.

### status ID

```bash
python -m soul_planner status ID
```

Show detailed task info.

### cancel ID

```bash
python -m soul_planner cancel ID
```

### block ID "reason"

```bash
python -m soul_planner block ID "REASON"
```

### unblock ID

```bash
python -m soul_planner unblock ID
```

### done ID

```bash
python -m soul_planner done ID
```

After marking done, update the Claude Code task UI: `TaskUpdate(status=completed)`.

### substep ID STEP

```bash
python -m soul_planner substep ID STEP
```

Where STEP is one of: planning, testing, implementing, reviewing, validating.

After updating, sync to Claude Code task UI: `TaskUpdate(activeForm="STEP: TITLE [N/5]")`.

### next

```bash
python -m soul_planner next
```

Show the next ready task (highest priority with all dependencies met).

## Default Behavior

If `$ARGUMENTS` is empty or unrecognized, show the board:
```bash
python -m soul_planner board
```

## Status Bar Sync

Whenever a task status changes, keep the Claude Code task panel in sync:
- BACKLOG: `TaskCreate(subject=title, activeForm="Queued: title")`
- IN_PROGRESS: `TaskUpdate(status=in_progress, activeForm="SUBSTEP: title [N/5]")`
- BLOCKED: `TaskUpdate(activeForm="BLOCKED: title -- reason")`
- VALIDATION: `TaskUpdate(activeForm="Review: title")`
- DONE: `TaskUpdate(status=completed)`

The user invoked: $ARGUMENTS
