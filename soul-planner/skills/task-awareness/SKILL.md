---
name: task-awareness
description: "Auto-sync soul-planner task queue with Claude Code task UI on session start. Triggers when user mentions tasks, backlog, kanban, or task queue."
version: 1.1.0
---

# Task Awareness

Sync soul-planner's persistent task queue with Claude Code's session task UI.

## ID Convention

Claude Code task subjects use the prefix `SP#<id>:` to map to soul-planner IDs.
Example: `SP#42: Build auth module`

This convention is rebuilt every session. No persistent mapping needed.

## When This Activates

- Session start (restore task state from SQLite)
- User mentions: "tasks", "backlog", "board", "queue", "what's next", "task status"
- After any `/planner` command completes

## Session Start Sync

On session start, check for active tasks:

```bash
python3 -m soul_planner list --status in_progress 2>/dev/null
python3 -m soul_planner list --status blocked 2>/dev/null
python3 -m soul_planner list --status validation 2>/dev/null
```

If there are active tasks, sync them to Claude Code's task UI using `TaskCreate`:

- For each IN_PROGRESS task:
  ```
  TaskCreate(subject="SP#ID: TITLE", activeForm="SUBSTEP: TITLE [N/5]")
  ```
  Where SUBSTEP and N come from the task's current substep.

- For each BLOCKED task:
  ```
  TaskCreate(subject="SP#ID: TITLE", activeForm="BLOCKED: TITLE -- REASON")
  ```

- For each VALIDATION task:
  ```
  TaskCreate(subject="SP#ID: TITLE", activeForm="Review: TITLE")
  ```

## Quick Board

When the user asks about tasks informally ("what's on my plate?", "any tasks?"), show:

```bash
python3 -m soul_planner board
```

## Awareness Rules

1. If there are BLOCKED tasks, remind the user when relevant
2. If there are VALIDATION tasks, ask if the user wants to review them
3. After completing any work, check if it relates to a queued task and offer to mark it done
4. Keep the Claude Code task panel in sync with soul-planner state
5. Always use the `SP#ID:` prefix when creating Claude Code tasks
