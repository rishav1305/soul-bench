---
name: task-execution
description: "Bridge between soul-planner task substeps and soul-workflow skills. Maps each substep to the right skills and model. Supports interactive (checkpoint) and autonomous (background) modes."
---

# Task Execution Bridge

Maps soul-planner's 5 substeps to soul-workflow skills. This skill is invoked by the task-runner agent for each substep.

## Substep-to-Skill Mapping

| Substep | Skills Invoked | Model |
|---------|---------------|-------|
| PLANNING | `soul-workflow:brainstorming` + `soul-workflow:writing-plans` | opus |
| TESTING | `soul-workflow:test-driven-development` | opus |
| IMPLEMENTING | `soul-workflow:subagent-driven-development` | sonnet |
| REVIEWING | `soul-workflow:requesting-code-review` + `soul-workflow:verification-before-completion` | opus |
| VALIDATING | `soul-workflow:verification-before-completion` + `soul-workflow:finishing-a-development-branch` | sonnet |

## Execution Modes

### Interactive Mode

Used when invoked via `/planner-run` or manual block-execution. Identical to current block-execution behavior.

**4 mandatory checkpoints with user approval gates:**

1. After PLANNING: "Design approved? Plan saved to docs/plans/."
2. After TESTING: "Tests written and failing (RED). Proceed to implementation?"
3. After REVIEWING: "Code review complete, security clear. Proceed to validation?"
4. After VALIDATING: "All tests green, ready to merge. Confirm?"

At each checkpoint, **STOP and wait for user feedback** before continuing.

### Autonomous Mode

Used when invoked via `/planner-run-auto` background orchestrator. The orchestrator passes these config flags in the prompt:

```
BACKGROUND_MODE: true
RETRY_COUNT: 2
TIMEOUT_MINUTES: 30
```

**Autonomous behavior:**

- **No user approval gates** -- proceed through all substeps uninterrupted
- **Retry on failure**: If a substep fails (test failure, review issue), retry up to `RETRY_COUNT` times before blocking
- **Timeout**: If a substep exceeds `TIMEOUT_MINUTES`, block the task with reason and STOP
- **On exhausted retries or timeout**: Block task in SQLite with reason, STOP immediately

**Autonomous decision-making at checkpoints:**

When a checkpoint presents multiple approaches (e.g., brainstorming proposes 2-3 designs, writing-plans offers execution choices):
- Pick the **recommended approach** (first option or the one marked "Recommended")
- Log every decision to the task output via `append-output`:
  ```
  CHECKPOINT [planning]: Design approach chosen: "Approach A: Orchestrator pattern (Recommended)"
  Alternatives skipped: "Approach B: Sequential spawns", "Approach C: Direct execution"
  ```

**Checkpoint commits:**

A git commit is created after each checkpoint as a restore point:
```
checkpoint: planning complete -- chose orchestrator pattern
checkpoint: tests-red -- 8 tests written, all failing as expected
checkpoint: tests-green -- implementation done, 8/8 passing
checkpoint: security-clear -- no issues found
checkpoint: shipped -- all tests pass, merged to master
```

These serve as restore points: if the user disagrees with an autonomous decision, they can `git reset --hard <checkpoint-commit>` and re-run from that substep interactively.

## Substep Details

### PLANNING

1. Invoke `soul-workflow:brainstorming` -- explore the task, identify approaches
2. Invoke `soul-workflow:writing-plans` -- create phased implementation plan
3. Save plan to `docs/plans/YYYY-MM-DD-<task-topic>-impl.md`
4. **Checkpoint**: Design approved (interactive) or log chosen approach (autonomous)
5. **Snapshot**: `milestone=design-approved topic=<task-topic>`

### TESTING

1. Invoke `soul-workflow:test-driven-development`
2. Write tests BEFORE implementation code
3. Cover: happy path, edge cases, error conditions, security boundaries
4. Run tests -- confirm RED (failing)
5. **Checkpoint**: Tests written and failing (interactive) or log test count (autonomous)
6. **Snapshot**: `milestone=tests-red topic=<task-topic>`

### IMPLEMENTING

1. Invoke `soul-workflow:subagent-driven-development`
2. Dispatch fresh subagent per task, review between tasks
3. Run tests after each batch -- confirm GREEN (passing)
4. **Snapshot**: `milestone=tests-green topic=<task-topic>`

### REVIEWING

1. Invoke `soul-workflow:requesting-code-review`
2. Security checklist:
   - [ ] All SQL uses parameterized queries with `?`
   - [ ] No hardcoded secrets (use env vars with project prefix)
   - [ ] No silent `except: pass` blocks
   - [ ] No blocking calls in async functions
   - [ ] No `from brain` or cross-project imports
3. Invoke `soul-workflow:verification-before-completion` -- evidence before assertions
4. If issues found: fix them, rerun tests
5. **Checkpoint**: Security clear (interactive) or log audit result (autonomous)
6. **Snapshot**: `milestone=security-clear topic=<task-topic>`

### VALIDATING

1. Invoke `soul-workflow:verification-before-completion` -- run full test suite one final time
2. Confirm: zero failures, zero warnings, zero security issues
3. Invoke `soul-workflow:finishing-a-development-branch` -- merge, commit, cleanup
4. **Checkpoint**: Ready to merge (interactive) or auto-merge (autonomous)
5. **Snapshot**: `milestone=shipped topic=<task-topic>`

## Mode Detection

Read the prompt for `BACKGROUND_MODE: true`. If present, use autonomous mode. Otherwise, use interactive mode.

```
if "BACKGROUND_MODE: true" in prompt:
    mode = autonomous
    retry_count = parse RETRY_COUNT (default 2)
    timeout_minutes = parse TIMEOUT_MINUTES (default 30)
else:
    mode = interactive
```

## Error Handling

**Interactive mode**: If any substep fails, report the error and ask the user what to do.

**Autonomous mode**:
1. On test failure: retry the substep up to `RETRY_COUNT` times
2. On review issue: fix and retry up to `RETRY_COUNT` times
3. On exhausted retries: `python -m soul_planner block TASK_ID "SUBSTEP failed after N retries: ERROR"`
4. On timeout: `python -m soul_planner block TASK_ID "SUBSTEP timed out after N minutes"`
5. Always STOP after blocking -- never continue to the next substep
