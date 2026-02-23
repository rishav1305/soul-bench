"""Tests for the TaskRunner execution orchestrator."""

from __future__ import annotations

import pytest

from soul_planner.db import TaskDB
from soul_planner.models import Priority, Substep, TaskCreate, TaskStatus
from soul_planner.runner import TaskRunner, substep_index, substep_label


class TestSubstepHelpers:
    """Helper function tests."""

    def test_substep_index(self):
        assert substep_index(Substep.PLANNING) == 1
        assert substep_index(Substep.TESTING) == 2
        assert substep_index(Substep.IMPLEMENTING) == 3
        assert substep_index(Substep.REVIEWING) == 4
        assert substep_index(Substep.VALIDATING) == 5

    def test_substep_label_in_progress(self):
        from datetime import datetime
        from soul_planner.models import Task, TaskSource

        now = datetime(2026, 2, 23)
        task = Task(
            id=1, title="Build auth", description="", acceptance="",
            status=TaskStatus.IN_PROGRESS, substep=Substep.IMPLEMENTING,
            priority=Priority.HIGH, source=TaskSource.MANUAL,
            blocker=None, output=None, error=None,
            retry_count=0, max_retries=3,
            created_at=now, started_at=now, completed_at=None,
            depends_on=[],
        )
        assert substep_label(task) == "IMPLEMENTING: Build auth [3/5]"

    def test_substep_label_blocked(self):
        from datetime import datetime
        from soul_planner.models import Task, TaskSource

        now = datetime(2026, 2, 23)
        task = Task(
            id=1, title="Build auth", description="", acceptance="",
            status=TaskStatus.BLOCKED, substep=Substep.PLANNING,
            priority=Priority.HIGH, source=TaskSource.MANUAL,
            blocker="Need API key", output=None, error=None,
            retry_count=0, max_retries=3,
            created_at=now, started_at=now, completed_at=None,
            depends_on=[],
        )
        assert substep_label(task) == "BLOCKED: Build auth -- Need API key"

    def test_substep_label_backlog(self):
        from datetime import datetime
        from soul_planner.models import Task, TaskSource

        now = datetime(2026, 2, 23)
        task = Task(
            id=1, title="Build auth", description="", acceptance="",
            status=TaskStatus.BACKLOG, substep=None,
            priority=Priority.NORMAL, source=TaskSource.MANUAL,
            blocker=None, output=None, error=None,
            retry_count=0, max_retries=3,
            created_at=now, started_at=None, completed_at=None,
            depends_on=[],
        )
        assert substep_label(task) == "Queued: Build auth"


class TestRunner:
    """TaskRunner lifecycle tests."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    @pytest.fixture
    async def runner(self, db):
        return TaskRunner(db)

    async def test_pick_next(self, db, runner):
        await db.add(TaskCreate(title="Task A"))
        task = await runner.pick_next()
        assert task is not None
        assert task.title == "Task A"

    async def test_pick_next_empty(self, runner):
        task = await runner.pick_next()
        assert task is None

    async def test_start(self, db, runner):
        t = await db.add(TaskCreate(title="Start me"))
        started = await runner.start(t.id)
        assert started.status == TaskStatus.IN_PROGRESS
        assert started.substep == Substep.PLANNING

    async def test_advance_through_substeps(self, db, runner):
        t = await db.add(TaskCreate(title="Advance me"))
        await runner.start(t.id)

        # planning -> testing
        t = await runner.advance(t.id)
        assert t.substep == Substep.TESTING

        # testing -> implementing
        t = await runner.advance(t.id)
        assert t.substep == Substep.IMPLEMENTING

        # implementing -> reviewing
        t = await runner.advance(t.id)
        assert t.substep == Substep.REVIEWING

        # reviewing -> validating
        t = await runner.advance(t.id)
        assert t.substep == Substep.VALIDATING

        # validating -> VALIDATION status
        t = await runner.advance(t.id)
        assert t.status == TaskStatus.VALIDATION

    async def test_advance_not_in_progress_raises(self, db, runner):
        t = await db.add(TaskCreate(title="Not started"))
        with pytest.raises(ValueError, match="not in progress"):
            await runner.advance(t.id)

    async def test_complete(self, db, runner):
        t = await db.add(TaskCreate(title="Complete me"))
        await runner.start(t.id)
        done = await runner.complete(t.id)
        assert done.status == TaskStatus.DONE

    async def test_fail_retries(self, db, runner):
        t = await db.add(TaskCreate(title="Fail me"))
        await runner.start(t.id)

        # First failure -> back to backlog
        failed = await runner.fail(t.id, "some error")
        assert failed.status == TaskStatus.BACKLOG
        assert failed.retry_count == 1
        assert failed.error == "some error"

    async def test_fail_max_retries_cancels(self, db, runner):
        t = await db.add(TaskCreate(title="Fail 3x"))
        await runner.start(t.id)

        # Fail 3 times (max_retries default is 3)
        await runner.fail(t.id, "error 1")
        await runner.start(t.id)
        await runner.fail(t.id, "error 2")
        await runner.start(t.id)
        final = await runner.fail(t.id, "error 3")
        assert final.status == TaskStatus.CANCELLED

    async def test_block_and_unblock(self, db, runner):
        t = await db.add(TaskCreate(title="Block me"))
        await runner.start(t.id)

        blocked = await runner.block(t.id, "Need input")
        assert blocked.status == TaskStatus.BLOCKED
        assert blocked.blocker == "Need input"

        unblocked = await runner.unblock(t.id)
        assert unblocked.status == TaskStatus.IN_PROGRESS
        assert unblocked.blocker is None

    async def test_pick_respects_priority(self, db, runner):
        await db.add(TaskCreate(title="Low", priority=Priority.LOW))
        await db.add(TaskCreate(title="Critical", priority=Priority.CRITICAL))
        task = await runner.pick_next()
        assert task.title == "Critical"
