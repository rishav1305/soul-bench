"""Tests for soul-planner Pydantic models."""

from __future__ import annotations

from datetime import datetime

import pytest

from soul_planner.models import (
    Priority,
    Substep,
    Task,
    TaskCreate,
    TaskSource,
    TaskStatus,
    TaskUpdate,
)


class TestEnums:
    """Enum values and membership."""

    def test_task_status_values(self):
        assert TaskStatus.BACKLOG == "backlog"
        assert TaskStatus.IN_PROGRESS == "in_progress"
        assert TaskStatus.BLOCKED == "blocked"
        assert TaskStatus.VALIDATION == "validation"
        assert TaskStatus.DONE == "done"
        assert TaskStatus.CANCELLED == "cancelled"

    def test_substep_values(self):
        assert Substep.PLANNING == "planning"
        assert Substep.TESTING == "testing"
        assert Substep.IMPLEMENTING == "implementing"
        assert Substep.REVIEWING == "reviewing"
        assert Substep.VALIDATING == "validating"

    def test_priority_values(self):
        assert Priority.LOW == "low"
        assert Priority.NORMAL == "normal"
        assert Priority.HIGH == "high"
        assert Priority.CRITICAL == "critical"

    def test_source_values(self):
        assert TaskSource.MANUAL == "manual"
        assert TaskSource.SCHEDULE == "schedule"

    def test_substep_ordering(self):
        steps = list(Substep)
        assert steps == [
            Substep.PLANNING,
            Substep.TESTING,
            Substep.IMPLEMENTING,
            Substep.REVIEWING,
            Substep.VALIDATING,
        ]


class TestTaskCreate:
    """TaskCreate model validation."""

    def test_minimal_creation(self):
        t = TaskCreate(title="Do something")
        assert t.title == "Do something"
        assert t.description == ""
        assert t.acceptance == ""
        assert t.priority == Priority.NORMAL
        assert t.depends_on == []

    def test_full_creation(self):
        t = TaskCreate(
            title="Build auth",
            description="JWT-based auth for soul-mesh",
            acceptance="bcrypt, refresh tokens, 1h expiry",
            priority=Priority.HIGH,
            depends_on=[1, 3],
        )
        assert t.title == "Build auth"
        assert t.priority == Priority.HIGH
        assert t.depends_on == [1, 3]

    def test_empty_title_rejected(self):
        with pytest.raises(Exception):
            TaskCreate(title="")

    def test_whitespace_title_rejected(self):
        with pytest.raises(Exception):
            TaskCreate(title="   ")

    def test_title_stripped(self):
        t = TaskCreate(title="  Build auth  ")
        assert t.title == "Build auth"


class TestTask:
    """Full Task model."""

    def test_round_trip(self):
        now = datetime(2026, 2, 23, 12, 0, 0)
        t = Task(
            id=1,
            title="Test task",
            description="A test",
            acceptance="It works",
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
        assert t.id == 1
        assert t.status == TaskStatus.BACKLOG
        assert t.substep is None

    def test_in_progress_with_substep(self):
        now = datetime(2026, 2, 23, 12, 0, 0)
        t = Task(
            id=2,
            title="Active task",
            description="",
            acceptance="",
            status=TaskStatus.IN_PROGRESS,
            substep=Substep.IMPLEMENTING,
            priority=Priority.HIGH,
            source=TaskSource.MANUAL,
            blocker=None,
            output=None,
            error=None,
            retry_count=0,
            max_retries=3,
            created_at=now,
            started_at=now,
            completed_at=None,
            depends_on=[1],
        )
        assert t.substep == Substep.IMPLEMENTING
        assert t.depends_on == [1]

    def test_blocked_with_blocker(self):
        now = datetime(2026, 2, 23, 12, 0, 0)
        t = Task(
            id=3,
            title="Blocked task",
            description="",
            acceptance="",
            status=TaskStatus.BLOCKED,
            substep=Substep.PLANNING,
            priority=Priority.NORMAL,
            source=TaskSource.MANUAL,
            blocker="Should we use WebSocket or SSE?",
            output=None,
            error=None,
            retry_count=0,
            max_retries=3,
            created_at=now,
            started_at=now,
            completed_at=None,
            depends_on=[],
        )
        assert t.blocker == "Should we use WebSocket or SSE?"


class TestTaskUpdate:
    """TaskUpdate model for partial updates."""

    def test_empty_update(self):
        u = TaskUpdate()
        assert u.status is None
        assert u.substep is None

    def test_status_only(self):
        u = TaskUpdate(status=TaskStatus.IN_PROGRESS)
        assert u.status == TaskStatus.IN_PROGRESS

    def test_substep_update(self):
        u = TaskUpdate(substep=Substep.TESTING)
        assert u.substep == Substep.TESTING

    def test_blocker_update(self):
        u = TaskUpdate(blocker="Need clarification on auth method")
        assert u.blocker == "Need clarification on auth method"
