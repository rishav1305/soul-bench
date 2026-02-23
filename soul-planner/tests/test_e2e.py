"""End-to-end tests for soul-planner.

Tests full lifecycle scenarios: task creation through completion,
dependency chains, blocker workflows, scheduler integration, CLI
round-trips, and the runner advancement pipeline.
"""

from __future__ import annotations

from datetime import date

import pytest
from click.testing import CliRunner

from soul_planner.cli import main
from soul_planner.db import TaskDB
from soul_planner.models import Priority, Substep, TaskCreate, TaskStatus
from soul_planner.runner import TaskRunner, substep_label
from soul_planner.scheduler import schedule_tasks


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
async def db():
    db = TaskDB(":memory:")
    await db.init()
    return db


@pytest.fixture
async def runner(db):
    return TaskRunner(db)


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def cli_db(monkeypatch):
    """Patch CLI to use in-memory DB."""
    import asyncio
    db = TaskDB(":memory:")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(db.init())

    def _get_db():
        return db

    monkeypatch.setattr("soul_planner.cli._get_db", _get_db)
    return db


PLANNER_CONTENT = """\
# Daily Planner

## Day 1 -- Sun Feb 23

### Block 1: BUILD -- soul-planner (9am-1pm)
- [x] Design doc done
- [ ] Write models
- [ ] Write db layer
- [ ] Write CLI

### Block 2: EXPLORE -- Research (2pm-6pm)
- [ ] Research Claude Code plugins
- [ ] Study Task tool API

### Block 3: SOCIAL -- Content (7pm-9pm)
- [ ] Draft LinkedIn post

### Block 4: SCOUT -- Jobs (9pm-11pm)
- [ ] Apply to 3 roles

### Evening Review (11pm, 15min)
- [ ] All done?

---

## Day 2 -- Mon Feb 24

### Block 1: BUILD -- runner (9am-1pm)
- [ ] Day 2 task
"""


# ---------------------------------------------------------------------------
# E2E: Full Task Lifecycle (DB + Runner)
# ---------------------------------------------------------------------------

class TestFullLifecycle:
    """Test a task from creation through all substeps to completion."""

    async def test_backlog_to_done(self, db, runner):
        """Create task -> start -> advance through all 5 substeps -> complete."""
        task = await db.add(TaskCreate(
            title="Build JWT auth",
            description="JWT-based auth for soul-mesh API",
            acceptance="bcrypt, refresh tokens, 1h expiry",
            priority=Priority.HIGH,
        ))
        assert task.status == TaskStatus.BACKLOG

        # Start -> PLANNING
        task = await runner.start(task.id)
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.substep == Substep.PLANNING
        assert task.started_at is not None
        assert substep_label(task) == "PLANNING: Build JWT auth [1/5]"

        # Advance through all substeps
        task = await runner.advance(task.id)
        assert task.substep == Substep.TESTING
        assert substep_label(task) == "TESTING: Build JWT auth [2/5]"

        task = await runner.advance(task.id)
        assert task.substep == Substep.IMPLEMENTING
        assert substep_label(task) == "IMPLEMENTING: Build JWT auth [3/5]"

        task = await runner.advance(task.id)
        assert task.substep == Substep.REVIEWING
        assert substep_label(task) == "REVIEWING: Build JWT auth [4/5]"

        task = await runner.advance(task.id)
        assert task.substep == Substep.VALIDATING
        assert substep_label(task) == "VALIDATING: Build JWT auth [5/5]"

        # Final advance -> VALIDATION
        task = await runner.advance(task.id)
        assert task.status == TaskStatus.VALIDATION
        assert substep_label(task) == "Review: Build JWT auth"

        # Complete
        task = await runner.complete(task.id)
        assert task.status == TaskStatus.DONE
        assert task.completed_at is not None
        assert substep_label(task) == "Done: Build JWT auth"

    async def test_blocker_mid_workflow(self, db, runner):
        """Task gets blocked during implementation, resumes after."""
        task = await db.add(TaskCreate(title="Implement OAuth"))
        await runner.start(task.id)
        await runner.advance(task.id)  # TESTING
        await runner.advance(task.id)  # IMPLEMENTING

        # Hit a blocker
        task = await runner.block(task.id, "Should we use OAuth2 or OIDC?")
        assert task.status == TaskStatus.BLOCKED
        assert task.substep == Substep.IMPLEMENTING  # substep preserved
        assert task.blocker == "Should we use OAuth2 or OIDC?"
        assert substep_label(task) == "BLOCKED: Implement OAuth -- Should we use OAuth2 or OIDC?"

        # User answers, unblock
        task = await runner.unblock(task.id)
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.substep == Substep.IMPLEMENTING  # resumes where left off
        assert task.blocker is None

        # Continue to completion
        task = await runner.advance(task.id)  # REVIEWING
        task = await runner.advance(task.id)  # VALIDATING
        task = await runner.advance(task.id)  # VALIDATION
        task = await runner.complete(task.id)
        assert task.status == TaskStatus.DONE


# ---------------------------------------------------------------------------
# E2E: Dependency Chain
# ---------------------------------------------------------------------------

class TestDependencyChain:
    """Test tasks with dependencies execute in correct order."""

    async def test_chain_a_b_c(self, db, runner):
        """A -> B -> C: B can't start until A is done, C can't start until B is done."""
        a = await db.add(TaskCreate(title="Define schema"))
        b = await db.add(TaskCreate(title="Implement DB", depends_on=[a.id]))
        c = await db.add(TaskCreate(title="Write CLI", depends_on=[b.id]))

        # Only A should be ready
        next_task = await runner.pick_next()
        assert next_task.id == a.id

        # B and C are blocked by deps
        assert await db.check_dependencies(b.id) is False
        assert await db.check_dependencies(c.id) is False

        # Complete A
        await runner.start(a.id)
        await runner.complete(a.id)

        # Now B should be ready, C still blocked
        assert await db.check_dependencies(b.id) is True
        assert await db.check_dependencies(c.id) is False
        next_task = await runner.pick_next()
        assert next_task.id == b.id

        # Complete B
        await runner.start(b.id)
        await runner.complete(b.id)

        # Now C should be ready
        assert await db.check_dependencies(c.id) is True
        next_task = await runner.pick_next()
        assert next_task.id == c.id

    async def test_fan_in_dependencies(self, db, runner):
        """C depends on both A and B. C only ready when BOTH are done."""
        a = await db.add(TaskCreate(title="Build API"))
        b = await db.add(TaskCreate(title="Build frontend"))
        c = await db.add(TaskCreate(title="Integration test", depends_on=[a.id, b.id]))

        assert await db.check_dependencies(c.id) is False

        # Complete A only
        await runner.start(a.id)
        await runner.complete(a.id)
        assert await db.check_dependencies(c.id) is False  # still waiting on B

        # Complete B
        await runner.start(b.id)
        await runner.complete(b.id)
        assert await db.check_dependencies(c.id) is True  # both done


# ---------------------------------------------------------------------------
# E2E: Retry Logic
# ---------------------------------------------------------------------------

class TestRetryLogic:
    """Test failure and retry behavior."""

    async def test_retry_then_succeed(self, db, runner):
        """Task fails once, retries, then succeeds."""
        task = await db.add(TaskCreate(title="Flaky task"))

        # First attempt fails
        await runner.start(task.id)
        task = await runner.fail(task.id, "Connection timeout")
        assert task.status == TaskStatus.BACKLOG
        assert task.retry_count == 1
        assert task.error == "Connection timeout"

        # Second attempt succeeds
        await runner.start(task.id)
        task = await runner.complete(task.id)
        assert task.status == TaskStatus.DONE
        assert task.retry_count == 1  # retries don't reset

    async def test_max_retries_exhausted(self, db, runner):
        """Task fails max_retries times -> cancelled."""
        task = await db.add(TaskCreate(title="Always fails"))

        for i in range(3):
            await runner.start(task.id)
            task = await runner.fail(task.id, f"Error {i+1}")

        assert task.status == TaskStatus.CANCELLED
        assert task.retry_count == 3


# ---------------------------------------------------------------------------
# E2E: Scheduler -> Runner Pipeline
# ---------------------------------------------------------------------------

class TestSchedulerToRunner:
    """Test the full pipeline: parse planner -> queue tasks -> execute."""

    async def test_schedule_and_run(self, db, runner, tmp_path):
        """Schedule tasks from planner, then run the top-priority one."""
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(PLANNER_CONTENT)

        # Schedule Block 1 tasks
        ids = await schedule_tasks(
            db, planner_path=planner_file,
            target_date=date(2026, 2, 23), block_filter=1,
        )
        assert len(ids) == 3  # Write models, Write db layer, Write CLI

        # All should be in backlog with HIGH priority (Block 1)
        tasks = await db.list(status=TaskStatus.BACKLOG)
        assert len(tasks) == 3
        for t in tasks:
            assert t.priority == Priority.HIGH

        # Pick next and run it
        next_task = await runner.pick_next()
        assert next_task is not None
        await runner.start(next_task.id)

        # Verify board shows correct distribution
        board = await db.board()
        assert len(board[TaskStatus.BACKLOG]) == 2
        assert len(board[TaskStatus.IN_PROGRESS]) == 1

    async def test_schedule_all_blocks(self, db, tmp_path):
        """Schedule all blocks, verify priority mapping."""
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(PLANNER_CONTENT)

        ids = await schedule_tasks(
            db, planner_path=planner_file, target_date=date(2026, 2, 23),
        )
        # Block 1: 3, Block 2: 2, Block 3: 1, Block 4: 1 = 7 tasks
        assert len(ids) == 7

        tasks = await db.list()
        by_title = {t.title: t for t in tasks}
        assert by_title["Write models"].priority == Priority.HIGH
        assert by_title["Research Claude Code plugins"].priority == Priority.NORMAL
        assert by_title["Draft LinkedIn post"].priority == Priority.NORMAL
        assert by_title["Apply to 3 roles"].priority == Priority.LOW

    async def test_schedule_idempotent(self, db, tmp_path):
        """Running schedule twice doesn't create duplicates."""
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(PLANNER_CONTENT)

        ids1 = await schedule_tasks(db, planner_path=planner_file, target_date=date(2026, 2, 23))
        ids2 = await schedule_tasks(db, planner_path=planner_file, target_date=date(2026, 2, 23))
        assert len(ids2) == 0
        assert len(await db.list()) == len(ids1)


# ---------------------------------------------------------------------------
# E2E: CLI Round-Trip
# ---------------------------------------------------------------------------

class TestCLIRoundTrip:
    """Test full workflows through the CLI interface."""

    def test_add_promote_advance_validate_done(self, cli_runner, cli_db):
        """Full lifecycle via CLI commands."""
        # Add
        result = cli_runner.invoke(main, ["add", "Build feature X", "--priority", "high"])
        assert result.exit_code == 0
        assert "Added task #1" in result.output

        # Promote (start)
        result = cli_runner.invoke(main, ["promote", "1"])
        assert result.exit_code == 0
        assert "started" in result.output.lower()

        # Advance 4 times (planning -> testing -> implementing -> reviewing -> validating)
        for _ in range(4):
            result = cli_runner.invoke(main, ["advance", "1"])
            assert result.exit_code == 0

        # Last advance -> validation
        result = cli_runner.invoke(main, ["advance", "1"])
        assert result.exit_code == 0
        assert "validation" in result.output.lower()

        # Done
        result = cli_runner.invoke(main, ["done", "1"])
        assert result.exit_code == 0
        assert "done" in result.output.lower()

        # Verify on board
        result = cli_runner.invoke(main, ["board"])
        assert result.exit_code == 0
        assert "Build feature X" in result.output

    def test_add_block_unblock_done(self, cli_runner, cli_db):
        """Blocker workflow via CLI."""
        cli_runner.invoke(main, ["add", "Implement auth"])

        # Block
        result = cli_runner.invoke(main, ["block", "1", "JWT or session cookies?"])
        assert result.exit_code == 0
        assert "blocked" in result.output.lower()

        # Status shows blocker
        result = cli_runner.invoke(main, ["status", "1"])
        assert "JWT or session cookies?" in result.output

        # Unblock
        result = cli_runner.invoke(main, ["unblock", "1"])
        assert result.exit_code == 0

        # Done
        result = cli_runner.invoke(main, ["done", "1"])
        assert result.exit_code == 0

    def test_dependency_chain_cli(self, cli_runner, cli_db):
        """Create tasks with dependencies via CLI."""
        cli_runner.invoke(main, ["add", "Schema"])
        cli_runner.invoke(main, ["add", "DB layer", "--depends-on", "1"])

        # Next should be Schema (no deps)
        result = cli_runner.invoke(main, ["next"])
        assert "Schema" in result.output

        # Done with Schema
        cli_runner.invoke(main, ["done", "1"])

        # Now DB layer should be next
        result = cli_runner.invoke(main, ["next"])
        assert "DB layer" in result.output

    def test_schedule_from_planner(self, cli_runner, cli_db, tmp_path):
        """Schedule command queues tasks from planner file."""
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(PLANNER_CONTENT)

        result = cli_runner.invoke(main, ["schedule", "--planner", str(planner_file), "--block", "1"])
        assert result.exit_code == 0
        assert "Scheduled 3 tasks" in result.output

        # List should show them
        result = cli_runner.invoke(main, ["list"])
        assert "Write models" in result.output
        assert "Write db layer" in result.output
        assert "Write CLI" in result.output

    def test_board_shows_all_columns(self, cli_runner, cli_db):
        """Board command shows all Kanban columns."""
        cli_runner.invoke(main, ["add", "Backlog item"])
        cli_runner.invoke(main, ["add", "Done item"])
        cli_runner.invoke(main, ["done", "2"])

        result = cli_runner.invoke(main, ["board"])
        assert "BACKLOG" in result.output
        assert "IN_PROGRESS" in result.output
        assert "BLOCKED" in result.output
        assert "VALIDATION" in result.output
        assert "DONE" in result.output
        assert "CANCELLED" in result.output


# ---------------------------------------------------------------------------
# E2E: Priority Queue
# ---------------------------------------------------------------------------

class TestPriorityQueue:
    """Test that priority ordering works across the full stack."""

    async def test_critical_picked_first(self, db, runner):
        """Critical tasks jump ahead of normal and low."""
        await db.add(TaskCreate(title="Low task", priority=Priority.LOW))
        await db.add(TaskCreate(title="Normal task", priority=Priority.NORMAL))
        await db.add(TaskCreate(title="Critical task", priority=Priority.CRITICAL))
        await db.add(TaskCreate(title="High task", priority=Priority.HIGH))

        next_task = await runner.pick_next()
        assert next_task.title == "Critical task"

        # Start critical, pick next -> high
        await runner.start(next_task.id)
        next_task = await runner.pick_next()
        assert next_task.title == "High task"

        # Start high, pick next -> normal
        await runner.start(next_task.id)
        next_task = await runner.pick_next()
        assert next_task.title == "Normal task"

        # Start normal, pick next -> low
        await runner.start(next_task.id)
        next_task = await runner.pick_next()
        assert next_task.title == "Low task"

    async def test_oldest_within_same_priority(self, db, runner):
        """Among same-priority tasks, oldest is picked first."""
        t1 = await db.add(TaskCreate(title="First normal"))
        await db.add(TaskCreate(title="Second normal"))

        next_task = await runner.pick_next()
        assert next_task.id == t1.id  # oldest first
