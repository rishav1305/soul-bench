"""Tests for the TaskDB async SQLite wrapper."""

from __future__ import annotations

import pytest

from soul_planner.db import TaskDB
from soul_planner.models import Priority, Substep, TaskCreate, TaskStatus, TaskUpdate


class TestInit:
    """Table creation and memory DB."""

    async def test_init_creates_tables(self):
        db = TaskDB(":memory:")
        await db.init()
        rows = await db._fetch_all("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        table_names = {r["name"] for r in rows}
        assert "tasks" in table_names
        assert "task_dependencies" in table_names

    async def test_init_is_idempotent(self):
        db = TaskDB(":memory:")
        await db.init()
        await db.init()  # Should not raise


class TestAdd:
    """Adding tasks."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_add_minimal_task(self, db):
        task = await db.add(TaskCreate(title="Test task"))
        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == TaskStatus.BACKLOG
        assert task.priority == Priority.NORMAL
        assert task.substep is None
        assert task.depends_on == []

    async def test_add_with_priority(self, db):
        task = await db.add(TaskCreate(title="Urgent", priority=Priority.CRITICAL))
        assert task.priority == Priority.CRITICAL

    async def test_add_with_dependencies(self, db):
        t1 = await db.add(TaskCreate(title="First"))
        t2 = await db.add(TaskCreate(title="Second", depends_on=[t1.id]))
        assert t2.depends_on == [t1.id]

    async def test_add_with_multiple_dependencies(self, db):
        t1 = await db.add(TaskCreate(title="A"))
        t2 = await db.add(TaskCreate(title="B"))
        t3 = await db.add(TaskCreate(title="C", depends_on=[t1.id, t2.id]))
        assert sorted(t3.depends_on) == [t1.id, t2.id]

    async def test_add_sets_created_at(self, db):
        task = await db.add(TaskCreate(title="Timestamped"))
        assert task.created_at is not None

    async def test_add_with_acceptance(self, db):
        task = await db.add(TaskCreate(title="Auth", acceptance="bcrypt, JWT"))
        assert task.acceptance == "bcrypt, JWT"

    async def test_autoincrement_ids(self, db):
        t1 = await db.add(TaskCreate(title="First"))
        t2 = await db.add(TaskCreate(title="Second"))
        assert t2.id == t1.id + 1


class TestGet:
    """Getting tasks by ID."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_get_existing(self, db):
        added = await db.add(TaskCreate(title="Find me"))
        found = await db.get(added.id)
        assert found is not None
        assert found.title == "Find me"

    async def test_get_nonexistent(self, db):
        result = await db.get(999)
        assert result is None

    async def test_get_includes_dependencies(self, db):
        t1 = await db.add(TaskCreate(title="A"))
        t2 = await db.add(TaskCreate(title="B", depends_on=[t1.id]))
        found = await db.get(t2.id)
        assert found.depends_on == [t1.id]


class TestList:
    """Listing tasks with optional status filter."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_list_empty(self, db):
        tasks = await db.list()
        assert tasks == []

    async def test_list_all(self, db):
        await db.add(TaskCreate(title="A"))
        await db.add(TaskCreate(title="B"))
        tasks = await db.list()
        assert len(tasks) == 2

    async def test_list_by_status(self, db):
        await db.add(TaskCreate(title="Backlog"))
        t2 = await db.add(TaskCreate(title="Done"))
        await db.update(t2.id, TaskUpdate(status=TaskStatus.DONE))
        backlog = await db.list(status=TaskStatus.BACKLOG)
        assert len(backlog) == 1
        assert backlog[0].title == "Backlog"


class TestBoard:
    """Kanban board view."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_board_groups_by_status(self, db):
        await db.add(TaskCreate(title="Backlog 1"))
        t2 = await db.add(TaskCreate(title="In progress"))
        await db.update(t2.id, TaskUpdate(status=TaskStatus.IN_PROGRESS, substep=Substep.PLANNING))
        t3 = await db.add(TaskCreate(title="Done"))
        await db.update(t3.id, TaskUpdate(status=TaskStatus.DONE))

        board = await db.board()
        assert len(board[TaskStatus.BACKLOG]) == 1
        assert len(board[TaskStatus.IN_PROGRESS]) == 1
        assert len(board[TaskStatus.DONE]) == 1

    async def test_board_empty_statuses(self, db):
        board = await db.board()
        for status in TaskStatus:
            assert status in board
            assert board[status] == []


class TestUpdate:
    """Updating task fields."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_update_status(self, db):
        t = await db.add(TaskCreate(title="Progress"))
        updated = await db.update(t.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))
        assert updated.status == TaskStatus.IN_PROGRESS

    async def test_update_substep(self, db):
        t = await db.add(TaskCreate(title="Substep"))
        await db.update(t.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))
        updated = await db.update(t.id, TaskUpdate(substep=Substep.TESTING))
        assert updated.substep == Substep.TESTING

    async def test_update_nonexistent_raises(self, db):
        with pytest.raises(ValueError, match="not found"):
            await db.update(999, TaskUpdate(status=TaskStatus.DONE))

    async def test_update_sets_started_at(self, db):
        t = await db.add(TaskCreate(title="Track time"))
        assert t.started_at is None
        updated = await db.update(t.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))
        assert updated.started_at is not None

    async def test_update_sets_completed_at(self, db):
        t = await db.add(TaskCreate(title="Complete"))
        await db.update(t.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))
        updated = await db.update(t.id, TaskUpdate(status=TaskStatus.DONE))
        assert updated.completed_at is not None


class TestCancel:
    """Cancelling tasks."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_cancel(self, db):
        t = await db.add(TaskCreate(title="Cancel me"))
        cancelled = await db.cancel(t.id)
        assert cancelled.status == TaskStatus.CANCELLED

    async def test_cancel_nonexistent_raises(self, db):
        with pytest.raises(ValueError, match="not found"):
            await db.cancel(999)


class TestBlock:
    """Blocking and unblocking tasks."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_block_with_reason(self, db):
        t = await db.add(TaskCreate(title="Block me"))
        await db.update(t.id, TaskUpdate(status=TaskStatus.IN_PROGRESS, substep=Substep.PLANNING))
        blocked = await db.block(t.id, "Need clarification on auth")
        assert blocked.status == TaskStatus.BLOCKED
        assert blocked.blocker == "Need clarification on auth"
        assert blocked.substep == Substep.PLANNING  # substep preserved

    async def test_unblock_resumes(self, db):
        t = await db.add(TaskCreate(title="Unblock me"))
        await db.update(t.id, TaskUpdate(status=TaskStatus.IN_PROGRESS, substep=Substep.TESTING))
        await db.block(t.id, "Waiting for answer")
        unblocked = await db.unblock(t.id)
        assert unblocked.status == TaskStatus.IN_PROGRESS
        assert unblocked.blocker is None
        assert unblocked.substep == Substep.TESTING  # substep preserved


class TestDependencies:
    """Dependency checking and promotion."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_check_deps_no_deps(self, db):
        t = await db.add(TaskCreate(title="No deps"))
        assert await db.check_dependencies(t.id) is True

    async def test_check_deps_incomplete(self, db):
        t1 = await db.add(TaskCreate(title="Dep"))
        t2 = await db.add(TaskCreate(title="Waiter", depends_on=[t1.id]))
        assert await db.check_dependencies(t2.id) is False

    async def test_check_deps_complete(self, db):
        t1 = await db.add(TaskCreate(title="Dep"))
        t2 = await db.add(TaskCreate(title="Waiter", depends_on=[t1.id]))
        await db.update(t1.id, TaskUpdate(status=TaskStatus.DONE))
        assert await db.check_dependencies(t2.id) is True

    async def test_promote_ready_counts(self, db):
        t1 = await db.add(TaskCreate(title="No deps"))
        t2 = await db.add(TaskCreate(title="Has dep", depends_on=[t1.id]))
        count = await db.promote_ready()
        # t1 has no deps -> ready; t2 has unmet dep -> not ready
        assert count == 1

    async def test_next_ready_respects_priority(self, db):
        await db.add(TaskCreate(title="Low", priority=Priority.LOW))
        await db.add(TaskCreate(title="Critical", priority=Priority.CRITICAL))
        await db.add(TaskCreate(title="Normal"))
        nxt = await db.next_ready()
        assert nxt.title == "Critical"

    async def test_next_ready_none_when_empty(self, db):
        nxt = await db.next_ready()
        assert nxt is None
