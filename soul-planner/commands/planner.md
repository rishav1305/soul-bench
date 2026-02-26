---
description: "Manage tasks -- add, list, board, status, cancel, block, unblock, done, substep, next"
argument-hint: "<add|list|board|status|cancel|block|unblock|done|substep|next> [args]"
allowed-tools: [Bash, Read, TaskCreate, TaskUpdate, TaskList]
---

# /planner -- Task Queue Manager

Manage the soul-planner task queue. All task data persists in SQLite across sessions.

## Setup

The CLI lives at `~/soul/soul-planner/`. If not installed:
```bash
cd ~/soul/soul-planner && pip3 install -e ".[dev]" --break-system-packages
```

## ID Convention

Claude Code task subjects use the prefix `SP#<id>:` to map to soul-planner IDs.
Example: `SP#42: Build auth module`

To find a Claude Code task for a soul-planner ID:
1. Call `TaskList()`
2. Find the task whose subject starts with `SP#ID:`

## Commands

Route based on the first argument in `$ARGUMENTS`:

### add [title] [--priority low|normal|high|critical] [--details "..."] [--acceptance "..."] [--depends-on 1,2]

**If no title provided (just `/planner add`):** Start interactive mode.
1. Ask: "What's the task?"
2. After user answers, ask: "Any specific requirements or acceptance criteria?"
3. Ask: "Priority?" with options: low, normal, high (default), critical
4. Create the task with collected info

**If title provided:** Create immediately.

```bash
python3 -m soul_planner add "TITLE" --priority PRIORITY --details "DETAILS" --acceptance "CRITERIA" --depends-on IDS
```

After creating, sync to Claude Code's task UI:
```
TaskCreate(subject="SP#ID: TITLE", description="DETAILS", activeForm="Queued: TITLE")
```

### list [--status STATUS]

```bash
python3 -m soul_planner list [--status backlog|in_progress|blocked|validation|done|cancelled]
```

Show output to user in a clean table format.

### board

```bash
python3 -m soul_planner board
```

Show the Kanban board output. This is the default if user just says `/planner` with no arguments.

### status ID

```bash
python3 -m soul_planner status ID
```

Show detailed task info.

### cancel ID

```bash
python3 -m soul_planner cancel ID
```

After cancelling, sync: find `SP#ID:` via `TaskList()`, then:
```
TaskUpdate(taskId=CC_TASK_ID, status="completed")
```

### block ID "reason"

```bash
python3 -m soul_planner block ID "REASON"
```

After blocking, sync: find `SP#ID:` via `TaskList()`, then:
```
TaskUpdate(taskId=CC_TASK_ID, activeForm="BLOCKED: TITLE -- REASON")
```

### unblock ID

```bash
python3 -m soul_planner unblock ID
```

After unblocking, sync: find `SP#ID:` via `TaskList()`, then:
```
TaskUpdate(taskId=CC_TASK_ID, activeForm="SUBSTEP: TITLE [N/5]")
```
Where SUBSTEP and N come from the task's current substep.

### done ID

```bash
python3 -m soul_planner done ID
```

After marking done, sync: find `SP#ID:` via `TaskList()`, then:
```
TaskUpdate(taskId=CC_TASK_ID, status="completed")
```

### substep ID STEP

```bash
python3 -m soul_planner substep ID STEP
```

Where STEP is one of: planning, testing, implementing, reviewing, validating.

After updating, sync: find `SP#ID:` via `TaskList()`, then:
```
TaskUpdate(taskId=CC_TASK_ID, activeForm="STEP_UPPER: TITLE [N/5]")
```
Where N is: planning=1, testing=2, implementing=3, reviewing=4, validating=5.

### next

```bash
python3 -m soul_planner next
```

Show the next ready task (highest priority with all dependencies met).

## Default Behavior

If `$ARGUMENTS` is empty or unrecognized, show the board:
```bash
python3 -m soul_planner board
```

## Status Bar Sync Reference

Whenever a task status changes, keep the Claude Code task panel in sync:
- BACKLOG: `TaskCreate(subject="SP#ID: title", activeForm="Queued: title")`
- IN_PROGRESS: `TaskUpdate(activeForm="SUBSTEP: title [N/5]")`
- BLOCKED: `TaskUpdate(activeForm="BLOCKED: title -- reason")`
- VALIDATION: `TaskUpdate(activeForm="Review: title")`
- DONE/CANCELLED: `TaskUpdate(status="completed")`

Always use `TaskList()` to find the matching Claude Code task ID before calling `TaskUpdate`.

The user invoked: $ARGUMENTS
