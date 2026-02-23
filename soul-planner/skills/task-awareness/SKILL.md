---
name: task-awareness
description: "Auto-sync soul-planner task queue with Claude Code task UI on session start. Triggers when user mentions tasks, backlog, kanban, or task queue."
version: 1.0.0
---

# Task Awareness

Sync soul-planner's persistent task queue with Claude Code's session task UI.

## When This Activates

- Session start (restore task state from SQLite)
- User mentions: "tasks", "backlog", "board", "queue", "what's next", "task status"
- After any `/task` command completes

## Session Start Sync

On session start, check for active tasks:

```bash
python -m soul_planner list --status in_progress 2>/dev/null
python -m soul_planner list --status blocked 2>/dev/null
```

If there are active tasks, sync them to Claude Code's task UI:
- For each IN_PROGRESS task: `TaskCreate` with `activeForm` showing current substep
- For each BLOCKED task: `TaskCreate` with `activeForm` showing blocker reason

## Quick Board

When the user asks about tasks informally ("what's on my plate?", "any tasks?"), show:

```bash
python -m soul_planner board
```

## Awareness Rules

1. If there are BLOCKED tasks, remind the user when relevant
2. If there are VALIDATION tasks, ask if the user wants to review them
3. After completing any work, check if it relates to a queued task and offer to mark it done
4. Keep the Claude Code task panel in sync with soul-planner state
