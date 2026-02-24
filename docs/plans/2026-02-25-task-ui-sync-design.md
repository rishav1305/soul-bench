# Claude Code Task UI Sync — Design

**Date:** 2026-02-25
**Gap:** #2 from `docs/reports/2026-02-24-claude-code-task-tool-internals.md`
**Goal:** Make all soul-planner commands consistently sync with Claude Code's TaskCreate/TaskUpdate UI using a convention-based ID mapping.

---

## Convention

All Claude Code task subjects follow: `SP#<soul-planner-id>: <title>`

To find a task for update: `TaskList()`, scan for subject matching `SP#ID:`.

This convention is rebuilt every session by task-awareness. No persistent mapping needed.

## Files to Modify

### 1. `commands/planner.md`

Tighten sync instructions:
- `add`: `TaskCreate(subject="SP#ID: title", activeForm="Queued: title")`
- `cancel`: Find via TaskList, `TaskUpdate(status="completed")`
- `block`: Find via TaskList, `TaskUpdate(activeForm="BLOCKED: title -- reason")`
- `unblock`: Find via TaskList, `TaskUpdate(activeForm="SUBSTEP: title [N/5]")`
- `done`: Find via TaskList, `TaskUpdate(status="completed")`

### 2. `commands/planner-run.md`

- Add TaskCreate at start if task not in UI
- Remove stale note about validate command
- Use SP#ID: prefix

### 3. `skills/task-awareness/SKILL.md`

- Sync VALIDATION tasks too (not just IN_PROGRESS and BLOCKED)
- Use SP#ID: prefix convention
- Document the convention

## No Python/test changes

All markdown instruction updates only.
