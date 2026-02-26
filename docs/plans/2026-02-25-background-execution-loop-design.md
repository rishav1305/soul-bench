# Background Execution Loop — Design

**Date:** 2026-02-25
**Gap:** #1 from `docs/reports/2026-02-24-claude-code-task-tool-internals.md`
**Goal:** Wire `/planner-run-auto` to spawn a background orchestrator that executes soul-planner tasks through all 5 substeps with per-substep model selection.

---

## Architecture

```
User: /planner-run-auto 42

[command loads into session]
  |
  v
Bash: python -m soul_planner status 42     # read task details
  |
  v
Task(subagent_type="task-orchestrator",
     run_in_background=true, model="haiku",
     prompt="Execute task #42: {title}\n{description}\n{acceptance}")
  |  -> returns agentId
  v
Bash: python -m soul_planner set-agent 42 "abc123"
  |
  v
"Task #42 dispatched for background execution (agent: abc123)"

--- Meanwhile, in background ---

task-orchestrator (haiku):
  1. Bash: python -m soul_planner substep 42 planning
  2. TaskUpdate(activeForm="PLANNING: title [1/5]")
  3. Task(subagent_type="task-runner", model="opus", isolation="worktree",
         prompt="PLANNING substep for task #42: ...")
  4. [wait for completion]
  5. Bash: python -m soul_planner substep 42 testing
  6. TaskUpdate(activeForm="TESTING: title [2/5]")
  7. Task(subagent_type="task-runner", model="opus", isolation="worktree",
         prompt="TESTING substep for task #42: ...")
  ...repeat for IMPLEMENTING (sonnet), REVIEWING (opus), VALIDATING (sonnet)...
  8. Bash: python -m soul_planner validate 42
  9. TaskUpdate(status="completed")

--- Completion notification arrives in parent session ---
```

## Model Mapping

| Substep | Model | Rationale |
|---------|-------|-----------|
| PLANNING | opus | Architectural decisions, creative design |
| TESTING | opus | Edge cases, invariants, security boundaries |
| IMPLEMENTING | sonnet | Tests constrain the work, well-defined |
| REVIEWING | opus | Security audit thoroughness |
| VALIDATING | sonnet | Run tests, confirm green |

Source: `.claude/skills/block-execution/SKILL.md` model selection table.

## Files to Create

### 1. `agents/task-orchestrator.md`

Lightweight coordinator agent:
- Model: haiku
- Tools: `[Bash, Read, Task, TaskCreate, TaskUpdate]`
- Receives task ID and details in prompt
- Reads task from SQLite via CLI
- Spawns one `task-runner` agent per substep with correct model
- Each child uses `isolation: "worktree"` for safe code changes
- Between substeps: advances state via CLI, syncs UI via TaskUpdate
- On substep failure: blocks the task with error, stops
- On final success: moves task to VALIDATION

### 2. `commands/planner-run-auto.md`

Slash command that:
- Reads task details from SQLite
- Spawns the orchestrator in background
- Stores returned agentId in the task record
- Shows immediate feedback to user

## Files to Modify

### 3. `agents/task-runner.md`

Currently handles all 5 substeps. Modified to:
- Accept a single substep in the prompt
- Execute only that substep
- Return results (what was done, files changed, test output)
- Keep existing tools: `[Bash, Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate]`

### 4. `soul_planner/models.py`

- Add `agent_id: str | None = None` field to `Task` model
- Add `agent_id: str | None = None` field to `TaskUpdate` model

### 5. `soul_planner/db.py`

- Add `agent_id TEXT` column to schema
- Handle `agent_id` in `_row_to_task()` mapping
- Handle `agent_id` in `update()` method

### 6. `soul_planner/cli.py`

- Add `set-agent` command: `soul-planner set-agent TASK_ID AGENT_ID`
- Show `agent_id` in `status` command output

### 7. Tests

- `tests/test_models.py`: agent_id field on Task and TaskUpdate
- `tests/test_db.py`: agent_id persistence, schema migration
- `tests/test_cli.py`: set-agent command, status output

## Error Handling

- If a substep agent fails (non-zero exit, error output): orchestrator blocks the task with the error message and stops
- If the orchestrator itself crashes: task stays at whatever substep it reached; user can check status and resume
- Resume: `/planner-run-auto 42` checks for existing agent_id, uses `Task(resume=agent_id)` if present

## Constraints

- Background agents can't pause for user checkpoints (unlike foreground block-execution)
- Worktree isolation means each substep agent gets a clean copy; changes must be committed within the agent
- The orchestrator (haiku) only coordinates -- never writes code itself
