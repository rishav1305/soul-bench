# Background Execution Loop — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Wire `/planner-run-auto` command to spawn a background orchestrator agent that executes soul-planner tasks through all 5 substeps with per-substep model selection.

**Architecture:** A `/planner-run-auto` command spawns a `task-orchestrator` agent (haiku) in the background. The orchestrator reads the task from SQLite, then spawns one `task-runner` agent per substep with the correct model (opus for judgment, sonnet for constrained work). Each substep agent runs in a worktree for isolation.

**Tech Stack:** Python 3.11+, aiosqlite, click, pydantic, structlog. Claude Code agents (markdown). Claude Code commands (markdown).

---

### Task 1: Add agent_id field to models

**Files:**
- Modify: `soul_planner/models.py:55-80`
- Test: `tests/test_models.py`

**Step 1: Write the failing test**

Add to `tests/test_models.py` in `TestTask`:

```python
def test_task_with_agent_id(self):
    now = datetime(2026, 2, 23, 12, 0, 0)
    t = Task(
        id=1,
        title="Agent task",
        description="",
        acceptance="",
        status=TaskStatus.IN_PROGRESS,
        substep=Substep.PLANNING,
        priority=Priority.NORMAL,
        source=TaskSource.MANUAL,
        blocker=None,
        output=None,
        error=None,
        retry_count=0,
        max_retries=3,
        created_at=now,
        started_at=now,
        completed_at=None,
        depends_on=[],
        agent_id="abc123",
    )
    assert t.agent_id == "abc123"

def test_task_agent_id_default_none(self):
    now = datetime(2026, 2, 23, 12, 0, 0)
    t = Task(
        id=1,
        title="No agent",
        description="",
        acceptance="",
        status=TaskStatus.BACKLOG,
        substep=None,
        priority=Priority.NORMAL,
        source=TaskSource.MANUAL,
        blocker=None,
        output=None,
        error=None,
        retry_count=0,
        max_retries=3,
        created_at=now,
        started_at=None,
        completed_at=None,
        depends_on=[],
    )
    assert t.agent_id is None
```

Add to `TestTaskUpdate`:

```python
def test_agent_id_update(self):
    u = TaskUpdate(agent_id="xyz789")
    assert u.agent_id == "xyz789"
```

**Step 2: Run test to verify it fails**

Run: `cd ~/soul/soul-planner && python -m pytest tests/test_models.py::TestTask::test_task_with_agent_id tests/test_models.py::TestTask::test_task_agent_id_default_none tests/test_models.py::TestTaskUpdate::test_agent_id_update -v`
Expected: FAIL — `agent_id` field doesn't exist on Task or TaskUpdate

**Step 3: Write minimal implementation**

In `soul_planner/models.py`, add to `Task` class (after `depends_on`):

```python
agent_id: str | None = None
```

Add to `TaskUpdate` class (after `error`):

```python
agent_id: str | None = None
```

**Step 4: Run test to verify it passes**

Run: `cd ~/soul/soul-planner && python -m pytest tests/test_models.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add soul_planner/models.py tests/test_models.py
git commit -m "feat(models): add agent_id field to Task and TaskUpdate"
```

---

### Task 2: Add agent_id column to database schema and CRUD

**Files:**
- Modify: `soul_planner/db.py:34-67` (schema), `soul_planner/db.py:139-158` (_row_to_task), `soul_planner/db.py:206-246` (update)
- Test: `tests/test_db.py`

**Step 1: Write the failing tests**

Add to `tests/test_db.py` a new class:

```python
class TestAgentId:
    """Agent ID persistence."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_agent_id_default_none(self, db):
        t = await db.add(TaskCreate(title="No agent"))
        assert t.agent_id is None

    async def test_update_agent_id(self, db):
        t = await db.add(TaskCreate(title="With agent"))
        updated = await db.update(t.id, TaskUpdate(agent_id="agent-abc123"))
        assert updated.agent_id == "agent-abc123"

    async def test_agent_id_persists_across_reads(self, db):
        t = await db.add(TaskCreate(title="Persist"))
        await db.update(t.id, TaskUpdate(agent_id="agent-xyz"))
        fetched = await db.get(t.id)
        assert fetched.agent_id == "agent-xyz"

    async def test_agent_id_in_list(self, db):
        t = await db.add(TaskCreate(title="Listed"))
        await db.update(t.id, TaskUpdate(agent_id="agent-list"))
        tasks = await db.list()
        assert tasks[0].agent_id == "agent-list"

    async def test_agent_id_survives_status_change(self, db):
        t = await db.add(TaskCreate(title="Status change"))
        await db.update(t.id, TaskUpdate(agent_id="agent-keep"))
        await db.update(t.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))
        fetched = await db.get(t.id)
        assert fetched.agent_id == "agent-keep"
```

**Step 2: Run test to verify it fails**

Run: `cd ~/soul/soul-planner && python -m pytest tests/test_db.py::TestAgentId -v`
Expected: FAIL — `agent_id` column doesn't exist in schema

**Step 3: Write minimal implementation**

In `soul_planner/db.py`:

1. Add `agent_id TEXT,` to `_SCHEMA` (after `error TEXT,` line, before `retry_count`):

```python
    error         TEXT,
    agent_id      TEXT,
    retry_count   INTEGER NOT NULL DEFAULT 0,
```

2. In `_row_to_task`, add `agent_id=row["agent_id"]` to the Task constructor:

```python
agent_id=row["agent_id"],
```

3. In `update` method, add agent_id handling (after the `error` block):

```python
if update.agent_id is not None:
    sets.append("agent_id = ?")
    params.append(update.agent_id)
```

**Step 4: Run test to verify it passes**

Run: `cd ~/soul/soul-planner && python -m pytest tests/test_db.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add soul_planner/db.py tests/test_db.py
git commit -m "feat(db): add agent_id column to tasks schema"
```

---

### Task 3: Add set-agent CLI command and show agent_id in status

**Files:**
- Modify: `soul_planner/cli.py`
- Test: `tests/test_cli.py`

**Step 1: Write the failing tests**

Add to `tests/test_cli.py`:

```python
class TestSetAgent:
    """CLI set-agent command."""

    def test_set_agent(self, runner, memory_db):
        runner.invoke(main, ["add", "Track agent"])
        result = runner.invoke(main, ["set-agent", "1", "agent-abc123"])
        assert result.exit_code == 0
        assert "agent-abc123" in result.output

    def test_set_agent_shown_in_status(self, runner, memory_db):
        runner.invoke(main, ["add", "Check status"])
        runner.invoke(main, ["set-agent", "1", "agent-xyz"])
        result = runner.invoke(main, ["status", "1"])
        assert result.exit_code == 0
        assert "agent-xyz" in result.output
```

**Step 2: Run test to verify it fails**

Run: `cd ~/soul/soul-planner && python -m pytest tests/test_cli.py::TestSetAgent -v`
Expected: FAIL — `set-agent` command doesn't exist

**Step 3: Write minimal implementation**

Add to `soul_planner/cli.py` (after the `done` command):

```python
@main.command("set-agent")
@click.argument("task_id", type=int)
@click.argument("agent_id")
def set_agent(task_id: int, agent_id: str):
    """Store a background agent ID on a task."""
    db = _get_db()

    async def _set():
        await db.init()
        return await db.update(task_id, TaskUpdate(agent_id=agent_id))

    task = _run(_set())
    click.echo(f"Task #{task.id} agent: {agent_id}")
```

In the `status` command, add after the `depends_on` output:

```python
if task.agent_id:
    click.echo(f"  Agent:    {task.agent_id}")
```

**Step 4: Run test to verify it passes**

Run: `cd ~/soul/soul-planner && python -m pytest tests/test_cli.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add soul_planner/cli.py tests/test_cli.py
git commit -m "feat(cli): add set-agent command and show agent_id in status"
```

---

### Task 4: Rewrite task-runner agent for single-substep execution

**Files:**
- Modify: `agents/task-runner.md`

**Step 1: Read existing agent**

Read: `agents/task-runner.md` — currently handles all 5 substeps sequentially.

**Step 2: Rewrite for single-substep mode**

Replace the content of `agents/task-runner.md` with a version that:
- Expects the prompt to specify WHICH substep to execute and the task details
- Executes ONLY that one substep
- Returns a structured result: what was done, files changed, test output
- Keeps the same tools and security checklist
- Model is set per-invocation by the orchestrator (not hardcoded)

```markdown
---
name: task-runner
description: "Execute a single substep of a soul-planner task. Receives task details and substep in prompt. Returns structured results."
tools: [Bash, Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate]
---

# Task Runner Agent

You execute ONE substep of a soul-planner task. Your prompt specifies which substep and the task details.

## Input Format

Your prompt contains:
- TASK_ID: The soul-planner task ID
- SUBSTEP: One of: planning, testing, implementing, reviewing, validating
- TITLE: Task title
- DESCRIPTION: What to build
- ACCEPTANCE: Success criteria
- PROJECT_DIR: Where the code lives

## Substep Instructions

### PLANNING
- Read the task description and acceptance criteria
- Read relevant files in the project
- Identify files to create/modify
- Write a brief plan (what to build, how, which files)
- Do NOT write code yet

### TESTING
- Write failing tests based on the plan
- Follow TDD: tests define the spec
- Cover happy path, edge cases, error conditions
- Run tests to confirm they FAIL (RED)
- Commit the test files

### IMPLEMENTING
- Read the failing tests
- Write minimal code to make ALL tests pass
- Run tests to confirm they PASS (GREEN)
- Commit the implementation

### REVIEWING
- Read all changed files
- Security checklist:
  - [ ] All SQL uses parameterized queries with `?`
  - [ ] No hardcoded secrets (use env vars with project prefix)
  - [ ] No silent `except: pass` blocks
  - [ ] No blocking calls in async functions
  - [ ] No `from brain` or cross-project imports
- If issues found: fix them, rerun tests
- Commit any fixes

### VALIDATING
- Run the FULL test suite: `python -m pytest tests/ -v`
- Confirm ALL tests pass (not just the new ones)
- Report: total tests, passed, failed
- If failures: fix and rerun until green
- Commit any fixes

## Output Format

When done, report:
1. SUBSTEP completed: [which one]
2. FILES changed: [list]
3. TEST results: [pass/fail counts]
4. ISSUES: [any problems encountered, or "none"]

## Conventions

- Python 3.11+, aiosqlite, structlog
- Tests: pytest with pytest-asyncio
- Run tests: `cd PROJECT_DIR && python -m pytest tests/ -v`
```

**Step 3: Verify markdown is valid**

Read the file back and check formatting.

**Step 4: Commit**

```bash
git add agents/task-runner.md
git commit -m "refactor(agent): task-runner now handles single substep per invocation"
```

---

### Task 5: Create task-orchestrator agent

**Files:**
- Create: `agents/task-orchestrator.md`

**Step 1: Write the orchestrator agent definition**

```markdown
---
name: task-orchestrator
description: "Background orchestrator for soul-planner tasks. Spawns per-substep task-runner agents with the correct model. Use with run_in_background: true."
tools: [Bash, Read, Task, TaskCreate, TaskUpdate]
model: haiku
---

# Task Orchestrator Agent

You coordinate the execution of a soul-planner task through all 5 substeps. You do NOT write code yourself -- you spawn task-runner agents for each substep.

## Input

Your prompt contains:
- TASK_ID: The soul-planner task ID
- TITLE: Task title
- DESCRIPTION: What to build
- ACCEPTANCE: Success criteria
- PROJECT_DIR: The project directory (e.g., ~/soul/soul-planner)

## Model Mapping

| Substep | Model | Why |
|---------|-------|-----|
| planning | opus | Architectural decisions |
| testing | opus | Edge cases, invariants |
| implementing | sonnet | Tests constrain the work |
| reviewing | opus | Security thoroughness |
| validating | sonnet | Run tests, confirm green |

## Execution Loop

For each substep in order (planning, testing, implementing, reviewing, validating):

1. **Update state**: Set the substep in soul-planner:
   ```bash
   python -m soul_planner substep TASK_ID SUBSTEP_NAME
   ```

2. **Sync UI**: Update Claude Code's task UI:
   ```
   TaskUpdate(activeForm="SUBSTEP_NAME_UPPER: TITLE [N/5]")
   ```

3. **Spawn runner**: Dispatch a task-runner agent with the correct model:
   ```
   Task(
       description="SUBSTEP for task #TASK_ID",
       subagent_type="task-runner",
       model=MODEL_FOR_SUBSTEP,
       isolation="worktree",
       prompt="TASK_ID: TASK_ID\nSUBSTEP: SUBSTEP_NAME\nTITLE: TITLE\nDESCRIPTION: DESCRIPTION\nACCEPTANCE: ACCEPTANCE\nPROJECT_DIR: PROJECT_DIR"
   )
   ```

4. **Check result**: Read the agent's response. If it reports ISSUES other than "none", block the task:
   ```bash
   python -m soul_planner block TASK_ID "SUBSTEP failed: ERROR_DESCRIPTION"
   ```
   Then STOP. Do not continue to the next substep.

5. **Continue**: If no issues, proceed to the next substep.

## After All 5 Substeps

Move the task to VALIDATION:
```bash
python -m soul_planner validate TASK_ID
```

Sync UI:
```
TaskUpdate(status="completed")
```

## Error Handling

- If a substep agent fails: block the task with the error, then STOP
- If a CLI command fails: block the task with the CLI error, then STOP
- Never guess or retry automatically -- block and let the user decide

## Rules

- You are a COORDINATOR. Never write code, create files, or edit source.
- Only use Bash for soul-planner CLI commands.
- Only use Read to check task state if needed.
- Only use Task to spawn task-runner agents.
- Only use TaskCreate/TaskUpdate to sync the Claude Code UI.
```

**Step 2: Verify markdown**

Read the file back and check formatting.

**Step 3: Commit**

```bash
git add agents/task-orchestrator.md
git commit -m "feat(agent): add task-orchestrator for background multi-model execution"
```

---

### Task 6: Create /planner-run-auto command

**Files:**
- Create: `commands/planner-run-auto.md`

**Step 1: Write the command**

```markdown
---
description: "Dispatch a task for autonomous background execution with per-substep model selection"
argument-hint: "[task-id]"
allowed-tools: [Bash, Task, TaskCreate, TaskUpdate]
model: sonnet
---

# /planner-run-auto -- Autonomous Background Execution

Dispatch a soul-planner task for fully autonomous background execution. The task-orchestrator agent handles all 5 substeps with the correct model per step.

## Process

1. **Pick task**: If `$ARGUMENTS` contains an ID, use that. Otherwise get the next ready task:
   ```bash
   python -m soul_planner next
   ```
   If no ready tasks, tell the user "No ready tasks in backlog" and stop.

2. **Read task details**:
   ```bash
   python -m soul_planner status TASK_ID
   ```
   Extract: title, description, acceptance criteria, and the project directory.

3. **Promote to IN_PROGRESS** (if still in BACKLOG):
   ```bash
   python -m soul_planner promote TASK_ID
   ```

4. **Sync to Claude Code task UI**:
   ```
   TaskCreate(subject="TITLE", description="DESCRIPTION", activeForm="Dispatching: TITLE")
   ```

5. **Spawn orchestrator in background**:
   ```
   Task(
       description="Execute task #TASK_ID",
       subagent_type="task-orchestrator",
       run_in_background=true,
       model="haiku",
       prompt="TASK_ID: ID\nTITLE: title\nDESCRIPTION: description\nACCEPTANCE: acceptance\nPROJECT_DIR: ~/soul/PROJECT_NAME"
   )
   ```

6. **Store agent ID**:
   ```bash
   python -m soul_planner set-agent TASK_ID AGENT_ID
   ```

7. **Report to user**:
   ```
   Task #TASK_ID dispatched for background execution.
   Agent: AGENT_ID
   Model rotation: opus (plan) -> opus (test) -> sonnet (impl) -> opus (review) -> sonnet (validate)

   Check progress: `python -m soul_planner status TASK_ID`
   ```

## Resume

If the task already has an agent_id and is BLOCKED:
- Show the blocker reason
- Ask the user if they want to resume or restart
- To resume: `Task(resume=AGENT_ID, subagent_type="task-orchestrator", prompt="Continue from where you left off")`
- To restart: Clear agent_id and re-dispatch

The user invoked: $ARGUMENTS
```

**Step 2: Verify markdown**

Read the file back and check formatting.

**Step 3: Commit**

```bash
git add commands/planner-run-auto.md
git commit -m "feat(command): add /planner-run-auto for background task execution"
```

---

### Task 7: Run full test suite and verify nothing is broken

**Files:**
- Test: `tests/` (all test files)

**Step 1: Run all tests**

Run: `cd ~/soul/soul-planner && python -m pytest tests/ -v`
Expected: ALL PASS (existing + new tests)

**Step 2: Verify test counts**

Expected new tests:
- test_models.py: +3 (agent_id on Task, default None, TaskUpdate)
- test_db.py: +5 (TestAgentId class)
- test_cli.py: +2 (TestSetAgent class)
- Total: +10 new tests

**Step 3: Final commit if any fixes needed**

```bash
git add -A
git commit -m "test: verify full suite passes with agent_id support"
```

---

## Summary

| Task | What | Files |
|------|------|-------|
| 1 | agent_id on models | models.py, test_models.py |
| 2 | agent_id in DB schema + CRUD | db.py, test_db.py |
| 3 | set-agent CLI + status output | cli.py, test_cli.py |
| 4 | Rewrite task-runner for single substep | agents/task-runner.md |
| 5 | Create task-orchestrator agent | agents/task-orchestrator.md |
| 6 | Create /planner-run-auto command | commands/planner-run-auto.md |
| 7 | Full test suite verification | tests/ |

Tasks 1-3 are Python TDD (test, implement, commit). Tasks 4-6 are markdown agent/command definitions. Task 7 is verification.
