# soul-planner Day 2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build soul-planner's foundation — repo structure, Pydantic models, async SQLite DB layer, and Click CLI — as a Claude Code marketplace plugin.

**Architecture:** Claude Code plugin with `.claude-plugin/plugin.json` manifest. Python package `soul_planner/` provides backend logic (models, DB, CLI). Commands/skills/agents are markdown stubs for now (implemented Days 4-6). DB at `~/.claude/soul-planner/tasks.db`. Follows soul-mesh conventions: aiosqlite, structlog, Click, pytest-asyncio, ruff, setuptools.

**Tech Stack:** Python 3.11+, aiosqlite, structlog, click, pydantic, pydantic-settings, pytest, pytest-asyncio, ruff

---

### Task 1: Repo scaffold + plugin manifest

**Files:**
- Create: `~/soul/soul-planner/.claude-plugin/plugin.json`
- Create: `~/soul/soul-planner/pyproject.toml`
- Create: `~/soul/soul-planner/CLAUDE.md`
- Create: `~/soul/soul-planner/soul_planner/__init__.py`
- Create: `~/soul/soul-planner/tests/__init__.py`

**Step 1: Create directory structure**

```bash
mkdir -p ~/soul/soul-planner/.claude-plugin
mkdir -p ~/soul/soul-planner/soul_planner
mkdir -p ~/soul/soul-planner/tests
mkdir -p ~/soul/soul-planner/commands
mkdir -p ~/soul/soul-planner/agents
mkdir -p ~/soul/soul-planner/skills/task-awareness
```

**Step 2: Write plugin.json**

```json
{
  "name": "soul-planner",
  "description": "Task queue and scheduler for Claude Code. Kanban workflow with BACKLOG/IN_PROGRESS/VALIDATION/DONE. Queue tasks, Claude executes them in background with live status.",
  "version": "0.1.0",
  "author": {
    "name": "Rishav"
  }
}
```

**Step 3: Write pyproject.toml**

Follow soul-mesh convention: setuptools backend, py311, aiosqlite + structlog + click + pydantic.

```toml
[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.build_meta"

[project]
name = "soul-planner"
version = "0.1.0"
description = "Task queue and scheduler for Claude Code with Kanban workflow."
readme = "README.md"
license = {text = "Apache-2.0"}
requires-python = ">=3.11"
authors = [{name = "Rishav"}]
keywords = ["claude-code", "planner", "task-queue", "kanban"]

dependencies = [
    "aiosqlite>=0.20.0",
    "structlog>=24.0.0",
    "click>=8.0",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "ruff>=0.8.0",
]

[project.scripts]
soul-planner = "soul_planner.cli:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["soul_planner*"]

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Step 4: Write __init__.py**

```python
"""soul-planner -- Task queue and scheduler for Claude Code."""

__version__ = "0.1.0"
```

**Step 5: Write CLAUDE.md**

```markdown
# soul-planner

Claude Code plugin: persistent task queue with Kanban workflow.

## Conventions

- Python 3.11+, aiosqlite, structlog, click, pydantic
- All SQL parameterized with `?` — never concatenate
- Env vars prefixed `PLANNER_`
- Tests: pytest with pytest-asyncio, `asyncio_mode = "auto"`
- DB path: `~/.claude/soul-planner/tasks.db`

## Structure

- `soul_planner/` — Python package (models, db, cli, runner, scheduler)
- `commands/` — Claude Code slash commands (markdown)
- `agents/` — Claude Code agent definitions (markdown)
- `skills/` — Claude Code skills (markdown)
- `.claude-plugin/plugin.json` — Plugin manifest

## Task States

BACKLOG -> IN_PROGRESS -> VALIDATION -> DONE
IN_PROGRESS substeps: planning -> testing -> implementing -> reviewing -> validating
BLOCKED can occur from IN_PROGRESS (waiting for user input)
```

**Step 6: Write tests/__init__.py**

Empty file.

**Step 7: Verify structure and commit**

```bash
cd ~/soul/soul-planner && find . -type f | sort
```

Expected: all files present.

```bash
cd ~/soul/soul-planner && git init && git add -A && git commit -m "feat: scaffold soul-planner plugin repo"
```

---

### Task 2: Pydantic models + enums

**Files:**
- Create: `~/soul/soul-planner/soul_planner/models.py`
- Create: `~/soul/soul-planner/tests/test_models.py`

**Step 1: Write the failing tests**

```python
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
```

**Step 2: Run tests to verify they fail**

```bash
cd ~/soul/soul-planner && python -m pytest tests/test_models.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'soul_planner.models'`

**Step 3: Write models.py**

```python
"""Pydantic models and enums for soul-planner tasks."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class TaskStatus(str, Enum):
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    VALIDATION = "validation"
    DONE = "done"
    CANCELLED = "cancelled"


class Substep(str, Enum):
    PLANNING = "planning"
    TESTING = "testing"
    IMPLEMENTING = "implementing"
    REVIEWING = "reviewing"
    VALIDATING = "validating"


class Priority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TaskSource(str, Enum):
    MANUAL = "manual"
    SCHEDULE = "schedule"


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    acceptance: str = ""
    priority: Priority = Priority.NORMAL
    depends_on: list[int] = []

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be empty")
        return v.strip()


class Task(BaseModel):
    id: int
    title: str
    description: str
    acceptance: str
    status: TaskStatus
    substep: Substep | None
    priority: Priority
    source: TaskSource
    blocker: str | None
    output: str | None
    error: str | None
    retry_count: int
    max_retries: int
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    depends_on: list[int]


class TaskUpdate(BaseModel):
    status: TaskStatus | None = None
    substep: Substep | None = None
    blocker: str | None = None
    output: str | None = None
    error: str | None = None
```

**Step 4: Run tests to verify they pass**

```bash
cd ~/soul/soul-planner && python -m pytest tests/test_models.py -v
```

Expected: all PASS

**Step 5: Commit**

```bash
cd ~/soul/soul-planner && git add soul_planner/models.py tests/test_models.py && git commit -m "feat: add Pydantic models and enums for task management"
```

---

### Task 3: Async SQLite DB layer

**Files:**
- Create: `~/soul/soul-planner/soul_planner/db.py`
- Create: `~/soul/soul-planner/tests/test_db.py`

**Step 1: Write the failing tests**

```python
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
        # Verify tables exist by querying sqlite_master
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

    async def test_promote_ready(self, db):
        """Tasks with all deps met should be promotable."""
        t1 = await db.add(TaskCreate(title="First"))
        t2 = await db.add(TaskCreate(title="Second", depends_on=[t1.id]))
        # t2 depends on t1, t1 not done yet
        count = await db.promote_ready()
        # t1 has no deps -> already promotable, but t2 is not
        # t1 should be promoted (no deps, backlog)
        assert count >= 1
        t1_fresh = await db.get(t1.id)
        assert t1_fresh.status == TaskStatus.BACKLOG  # still backlog (promote doesn't change to in_progress)

    async def test_next_ready_respects_priority(self, db):
        await db.add(TaskCreate(title="Low", priority=Priority.LOW))
        await db.add(TaskCreate(title="Critical", priority=Priority.CRITICAL))
        await db.add(TaskCreate(title="Normal"))
        nxt = await db.next_ready()
        assert nxt.title == "Critical"
```

**Step 2: Run tests to verify they fail**

```bash
cd ~/soul/soul-planner && python -m pytest tests/test_db.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'soul_planner.db'`

**Step 3: Write db.py**

```python
"""Async SQLite wrapper for soul-planner task management.

Uses aiosqlite with connect-per-call for file DBs, persistent connection
for :memory: DBs. All SQL parameterized with ? placeholders.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import aiosqlite
import structlog

from soul_planner.models import (
    Priority,
    Substep,
    Task,
    TaskCreate,
    TaskSource,
    TaskStatus,
    TaskUpdate,
)

logger = structlog.get_logger("soul-planner.db")

_PRIORITY_ORDER = {
    Priority.CRITICAL: 0,
    Priority.HIGH: 1,
    Priority.NORMAL: 2,
    Priority.LOW: 3,
}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT NOT NULL,
    description   TEXT NOT NULL DEFAULT '',
    acceptance    TEXT NOT NULL DEFAULT '',
    status        TEXT NOT NULL DEFAULT 'backlog'
                  CHECK(status IN ('backlog','in_progress','blocked','validation','done','cancelled')),
    substep       TEXT CHECK(substep IS NULL OR substep IN ('planning','testing','implementing','reviewing','validating')),
    priority      TEXT NOT NULL DEFAULT 'normal'
                  CHECK(priority IN ('low','normal','high','critical')),
    source        TEXT NOT NULL DEFAULT 'manual'
                  CHECK(source IN ('manual','schedule')),
    blocker       TEXT,
    output        TEXT,
    error         TEXT,
    retry_count   INTEGER NOT NULL DEFAULT 0,
    max_retries   INTEGER NOT NULL DEFAULT 3,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    started_at    TEXT,
    completed_at  TEXT
);

CREATE TABLE IF NOT EXISTS task_dependencies (
    task_id    INTEGER NOT NULL REFERENCES tasks(id),
    depends_on INTEGER NOT NULL REFERENCES tasks(id),
    PRIMARY KEY (task_id, depends_on),
    CHECK(task_id != depends_on)
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_deps_task ON task_dependencies(task_id);
CREATE INDEX IF NOT EXISTS idx_deps_dep ON task_dependencies(depends_on);
"""


class TaskDB:
    """Async SQLite wrapper for task CRUD operations."""

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._memory_db: aiosqlite.Connection | None = None

    async def _connect(self) -> aiosqlite.Connection:
        if self._db_path == ":memory:":
            if self._memory_db is None:
                self._memory_db = await aiosqlite.connect(":memory:")
                self._memory_db.row_factory = aiosqlite.Row
            return self._memory_db
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = await aiosqlite.connect(self._db_path)
        conn.row_factory = aiosqlite.Row
        return conn

    async def _close(self, conn: aiosqlite.Connection) -> None:
        if self._db_path != ":memory:":
            await conn.close()

    async def _fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        conn = await self._connect()
        try:
            cursor = await conn.execute(sql, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            await self._close(conn)

    async def _fetch_one(self, sql: str, params: tuple = ()) -> dict | None:
        conn = await self._connect()
        try:
            cursor = await conn.execute(sql, params)
            row = await cursor.fetchone()
            return dict(row) if row else None
        finally:
            await self._close(conn)

    async def _execute(self, sql: str, params: tuple = ()) -> int:
        conn = await self._connect()
        try:
            cursor = await conn.execute(sql, params)
            await conn.commit()
            return cursor.lastrowid
        finally:
            await self._close(conn)

    async def init(self) -> None:
        """Create tables if they don't exist."""
        conn = await self._connect()
        try:
            await conn.executescript(_SCHEMA)
            await conn.commit()
            logger.info("Database initialized", path=self._db_path)
        finally:
            await self._close(conn)

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    async def _get_deps(self, task_id: int) -> list[int]:
        rows = await self._fetch_all(
            "SELECT depends_on FROM task_dependencies WHERE task_id = ?",
            (task_id,),
        )
        return [r["depends_on"] for r in rows]

    def _row_to_task(self, row: dict, deps: list[int]) -> Task:
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            acceptance=row["acceptance"],
            status=TaskStatus(row["status"]),
            substep=Substep(row["substep"]) if row["substep"] else None,
            priority=Priority(row["priority"]),
            source=TaskSource(row["source"]),
            blocker=row["blocker"],
            output=row["output"],
            error=row["error"],
            retry_count=row["retry_count"],
            max_retries=row["max_retries"],
            created_at=datetime.fromisoformat(row["created_at"]),
            started_at=datetime.fromisoformat(row["started_at"]) if row["started_at"] else None,
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
            depends_on=deps,
        )

    async def add(self, task: TaskCreate) -> Task:
        """Add a new task to BACKLOG and return it."""
        task_id = await self._execute(
            """INSERT INTO tasks (title, description, acceptance, priority)
               VALUES (?, ?, ?, ?)""",
            (task.title, task.description, task.acceptance, task.priority.value),
        )
        for dep_id in task.depends_on:
            await self._execute(
                "INSERT INTO task_dependencies (task_id, depends_on) VALUES (?, ?)",
                (task_id, dep_id),
            )
        logger.info("Task added", task_id=task_id, title=task.title)
        return await self.get(task_id)

    async def get(self, task_id: int) -> Task | None:
        """Get a task by ID, or None if not found."""
        row = await self._fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if not row:
            return None
        deps = await self._get_deps(task_id)
        return self._row_to_task(row, deps)

    async def list(self, status: TaskStatus | None = None) -> list[Task]:
        """List tasks, optionally filtered by status."""
        if status:
            rows = await self._fetch_all(
                "SELECT * FROM tasks WHERE status = ? ORDER BY id",
                (status.value,),
            )
        else:
            rows = await self._fetch_all("SELECT * FROM tasks ORDER BY id")
        tasks = []
        for row in rows:
            deps = await self._get_deps(row["id"])
            tasks.append(self._row_to_task(row, deps))
        return tasks

    async def board(self) -> dict[TaskStatus, list[Task]]:
        """Return all tasks grouped by status (Kanban board view)."""
        result: dict[TaskStatus, list[Task]] = {s: [] for s in TaskStatus}
        all_tasks = await self.list()
        for task in all_tasks:
            result[task.status].append(task)
        return result

    async def update(self, task_id: int, update: TaskUpdate) -> Task:
        """Update task fields. Raises ValueError if task not found."""
        existing = await self.get(task_id)
        if not existing:
            raise ValueError(f"Task {task_id} not found")

        sets: list[str] = []
        params: list = []

        if update.status is not None:
            sets.append("status = ?")
            params.append(update.status.value)
            if update.status == TaskStatus.IN_PROGRESS and existing.started_at is None:
                sets.append("started_at = ?")
                params.append(self._now())
            if update.status in (TaskStatus.DONE, TaskStatus.CANCELLED):
                sets.append("completed_at = ?")
                params.append(self._now())

        if update.substep is not None:
            sets.append("substep = ?")
            params.append(update.substep.value)

        if update.blocker is not None:
            sets.append("blocker = ?")
            params.append(update.blocker)

        if update.output is not None:
            sets.append("output = ?")
            params.append(update.output)

        if update.error is not None:
            sets.append("error = ?")
            params.append(update.error)

        if sets:
            sql = f"UPDATE tasks SET {', '.join(sets)} WHERE id = ?"
            params.append(task_id)
            await self._execute(sql, tuple(params))

        return await self.get(task_id)

    async def cancel(self, task_id: int) -> Task:
        """Cancel a task."""
        existing = await self.get(task_id)
        if not existing:
            raise ValueError(f"Task {task_id} not found")
        return await self.update(task_id, TaskUpdate(status=TaskStatus.CANCELLED))

    async def block(self, task_id: int, reason: str) -> Task:
        """Block a task with a reason. Preserves current substep."""
        existing = await self.get(task_id)
        if not existing:
            raise ValueError(f"Task {task_id} not found")
        await self._execute(
            "UPDATE tasks SET status = ?, blocker = ? WHERE id = ?",
            (TaskStatus.BLOCKED.value, reason, task_id),
        )
        return await self.get(task_id)

    async def unblock(self, task_id: int) -> Task:
        """Unblock a task. Resumes to IN_PROGRESS, clears blocker."""
        existing = await self.get(task_id)
        if not existing:
            raise ValueError(f"Task {task_id} not found")
        await self._execute(
            "UPDATE tasks SET status = ?, blocker = NULL WHERE id = ?",
            (TaskStatus.IN_PROGRESS.value, task_id),
        )
        return await self.get(task_id)

    async def check_dependencies(self, task_id: int) -> bool:
        """Check if all dependencies of a task are completed."""
        deps = await self._get_deps(task_id)
        if not deps:
            return True
        placeholders = ",".join("?" for _ in deps)
        row = await self._fetch_one(
            f"SELECT COUNT(*) as cnt FROM tasks WHERE id IN ({placeholders}) AND status != ?",
            (*deps, TaskStatus.DONE.value),
        )
        return row["cnt"] == 0

    async def promote_ready(self) -> int:
        """Check backlog tasks and count those whose deps are met.

        Returns the count of tasks that are ready (deps satisfied).
        Does not change status — tasks stay in backlog until picked up.
        """
        backlog = await self.list(status=TaskStatus.BACKLOG)
        ready_count = 0
        for task in backlog:
            if await self.check_dependencies(task.id):
                ready_count += 1
        return ready_count

    async def next_ready(self) -> Task | None:
        """Get the next ready task from backlog (highest priority, oldest)."""
        backlog = await self.list(status=TaskStatus.BACKLOG)
        ready = []
        for task in backlog:
            if await self.check_dependencies(task.id):
                ready.append(task)
        if not ready:
            return None
        ready.sort(key=lambda t: (_PRIORITY_ORDER.get(t.priority, 99), t.created_at))
        return ready[0]
```

**Step 4: Run tests to verify they pass**

```bash
cd ~/soul/soul-planner && python -m pytest tests/test_db.py -v
```

Expected: all PASS

**Step 5: Commit**

```bash
cd ~/soul/soul-planner && git add soul_planner/db.py tests/test_db.py && git commit -m "feat: add async SQLite DB layer with Kanban task CRUD"
```

---

### Task 4: Click CLI

**Files:**
- Create: `~/soul/soul-planner/soul_planner/cli.py`
- Create: `~/soul/soul-planner/soul_planner/__main__.py`
- Create: `~/soul/soul-planner/tests/test_cli.py`

**Step 1: Write the failing tests**

```python
"""Tests for the soul-planner Click CLI."""

from __future__ import annotations

import asyncio

import pytest
from click.testing import CliRunner

from soul_planner.cli import main
from soul_planner.db import TaskDB


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def memory_db(monkeypatch):
    """Patch CLI to use in-memory DB."""
    db = TaskDB(":memory:")
    asyncio.get_event_loop().run_until_complete(db.init())

    def _get_db():
        return db

    monkeypatch.setattr("soul_planner.cli._get_db", _get_db)
    return db


class TestAdd:
    """CLI add command."""

    def test_add_basic(self, runner, memory_db):
        result = runner.invoke(main, ["add", "Build auth module"])
        assert result.exit_code == 0
        assert "Added task #1" in result.output
        assert "Build auth module" in result.output

    def test_add_with_priority(self, runner, memory_db):
        result = runner.invoke(main, ["add", "Urgent task", "--priority", "critical"])
        assert result.exit_code == 0
        assert "critical" in result.output.lower()

    def test_add_with_details(self, runner, memory_db):
        result = runner.invoke(main, ["add", "Task", "--details", "Some details"])
        assert result.exit_code == 0

    def test_add_with_acceptance(self, runner, memory_db):
        result = runner.invoke(main, ["add", "Task", "--acceptance", "Tests pass"])
        assert result.exit_code == 0


class TestList:
    """CLI list command."""

    def test_list_empty(self, runner, memory_db):
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "No tasks" in result.output

    def test_list_with_tasks(self, runner, memory_db):
        runner.invoke(main, ["add", "Task A"])
        runner.invoke(main, ["add", "Task B"])
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "Task A" in result.output
        assert "Task B" in result.output

    def test_list_filter_by_status(self, runner, memory_db):
        runner.invoke(main, ["add", "Backlog task"])
        result = runner.invoke(main, ["list", "--status", "backlog"])
        assert result.exit_code == 0
        assert "Backlog task" in result.output


class TestStatus:
    """CLI status command."""

    def test_status_existing(self, runner, memory_db):
        runner.invoke(main, ["add", "Check me"])
        result = runner.invoke(main, ["status", "1"])
        assert result.exit_code == 0
        assert "Check me" in result.output

    def test_status_nonexistent(self, runner, memory_db):
        result = runner.invoke(main, ["status", "999"])
        assert result.exit_code == 0
        assert "not found" in result.output.lower()


class TestBoard:
    """CLI board command."""

    def test_board_empty(self, runner, memory_db):
        result = runner.invoke(main, ["board"])
        assert result.exit_code == 0
        assert "BACKLOG" in result.output

    def test_board_with_tasks(self, runner, memory_db):
        runner.invoke(main, ["add", "Backlog item"])
        result = runner.invoke(main, ["board"])
        assert result.exit_code == 0
        assert "Backlog item" in result.output


class TestCancel:
    """CLI cancel command."""

    def test_cancel(self, runner, memory_db):
        runner.invoke(main, ["add", "Cancel me"])
        result = runner.invoke(main, ["cancel", "1"])
        assert result.exit_code == 0
        assert "cancelled" in result.output.lower()


class TestBlock:
    """CLI block/unblock commands."""

    def test_block(self, runner, memory_db):
        runner.invoke(main, ["add", "Block me"])
        result = runner.invoke(main, ["block", "1", "Need answer"])
        assert result.exit_code == 0
        assert "blocked" in result.output.lower()

    def test_unblock(self, runner, memory_db):
        runner.invoke(main, ["add", "Unblock me"])
        runner.invoke(main, ["block", "1", "Waiting"])
        result = runner.invoke(main, ["unblock", "1"])
        assert result.exit_code == 0


class TestSubstep:
    """CLI substep command."""

    def test_substep(self, runner, memory_db):
        runner.invoke(main, ["add", "Step me"])
        result = runner.invoke(main, ["substep", "1", "planning"])
        assert result.exit_code == 0
        assert "planning" in result.output.lower()


class TestDone:
    """CLI done command."""

    def test_done(self, runner, memory_db):
        runner.invoke(main, ["add", "Finish me"])
        result = runner.invoke(main, ["done", "1"])
        assert result.exit_code == 0
        assert "done" in result.output.lower()
```

**Step 2: Run tests to verify they fail**

```bash
cd ~/soul/soul-planner && python -m pytest tests/test_cli.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'soul_planner.cli'`

**Step 3: Write cli.py**

```python
"""Click-based CLI for soul-planner.

Commands
--------
- ``soul-planner add`` -- Add a new task to backlog
- ``soul-planner list`` -- List tasks (optionally by status)
- ``soul-planner board`` -- Kanban board view
- ``soul-planner status`` -- Show detailed task status
- ``soul-planner cancel`` -- Cancel a task
- ``soul-planner block`` -- Block a task with a reason
- ``soul-planner unblock`` -- Resume a blocked task
- ``soul-planner done`` -- Mark a task as done
- ``soul-planner substep`` -- Update a task's substep
- ``soul-planner next`` -- Show next ready task
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import click

from soul_planner.db import TaskDB
from soul_planner.models import Priority, Substep, TaskCreate, TaskStatus, TaskUpdate

_DEFAULT_DB_PATH = str(Path.home() / ".claude" / "soul-planner" / "tasks.db")


def _get_db() -> TaskDB:
    db_path = os.environ.get("PLANNER_DB_PATH", _DEFAULT_DB_PATH)
    return TaskDB(db_path)


def _run(coro):
    """Run an async coroutine synchronously."""
    return asyncio.get_event_loop().run_until_complete(coro)


@click.group()
def main():
    """soul-planner -- task queue and scheduler for Claude Code."""


@main.command()
@click.argument("title")
@click.option("--details", default="", help="Task description.")
@click.option("--acceptance", default="", help="Acceptance criteria.")
@click.option("--priority", type=click.Choice(["low", "normal", "high", "critical"]), default="normal")
@click.option("--depends-on", default="", help="Comma-separated task IDs this depends on.")
def add(title: str, details: str, acceptance: str, priority: str, depends_on: str):
    """Add a new task to BACKLOG."""
    db = _get_db()

    dep_ids = [int(x.strip()) for x in depends_on.split(",") if x.strip()] if depends_on else []

    async def _add():
        await db.init()
        task = await db.add(TaskCreate(
            title=title,
            description=details,
            acceptance=acceptance,
            priority=Priority(priority),
            depends_on=dep_ids,
        ))
        return task

    task = _run(_add())
    click.echo(f"Added task #{task.id} to BACKLOG: \"{task.title}\"")
    if task.priority != Priority.NORMAL:
        click.echo(f"  Priority: {task.priority.value}")
    if task.depends_on:
        click.echo(f"  Depends on: {task.depends_on}")


@main.command("list")
@click.option("--status", type=click.Choice([s.value for s in TaskStatus]), default=None)
def list_tasks(status: str | None):
    """List tasks, optionally filtered by status."""
    db = _get_db()

    async def _list():
        await db.init()
        s = TaskStatus(status) if status else None
        return await db.list(status=s)

    tasks = _run(_list())
    if not tasks:
        click.echo("No tasks found.")
        return

    for t in tasks:
        substep_str = f" > {t.substep.value}" if t.substep else ""
        click.echo(f"  #{t.id}  [{t.status.value}{substep_str}]  {t.title}  ({t.priority.value})")


@main.command()
def board():
    """Show Kanban board view."""
    db = _get_db()

    async def _board():
        await db.init()
        return await db.board()

    board_data = _run(_board())

    for s in TaskStatus:
        tasks = board_data[s]
        click.echo(f"\n{s.value.upper()} ({len(tasks)})")
        click.echo("-" * 40)
        if not tasks:
            click.echo("  (empty)")
        for t in tasks:
            substep_str = f" > {t.substep.value}" if t.substep else ""
            click.echo(f"  #{t.id}  {t.title}  ({t.priority.value}){substep_str}")


@main.command()
@click.argument("task_id", type=int)
def status(task_id: int):
    """Show detailed task status."""
    db = _get_db()

    async def _status():
        await db.init()
        return await db.get(task_id)

    task = _run(_status())
    if not task:
        click.echo(f"Task #{task_id} not found.")
        return

    substep_str = f" > {task.substep.value}" if task.substep else ""
    click.echo(f"Task #{task.id}: {task.title}")
    click.echo(f"  Status:   {task.status.value}{substep_str}")
    click.echo(f"  Priority: {task.priority.value}")
    if task.description:
        click.echo(f"  Details:  {task.description}")
    if task.acceptance:
        click.echo(f"  Accept:   {task.acceptance}")
    if task.blocker:
        click.echo(f"  Blocker:  {task.blocker}")
    if task.depends_on:
        click.echo(f"  Deps:     {task.depends_on}")
    click.echo(f"  Created:  {task.created_at}")
    if task.started_at:
        click.echo(f"  Started:  {task.started_at}")
    if task.completed_at:
        click.echo(f"  Done:     {task.completed_at}")


@main.command()
@click.argument("task_id", type=int)
def cancel(task_id: int):
    """Cancel a task."""
    db = _get_db()

    async def _cancel():
        await db.init()
        return await db.cancel(task_id)

    task = _run(_cancel())
    click.echo(f"Task #{task.id} cancelled: \"{task.title}\"")


@main.command()
@click.argument("task_id", type=int)
@click.argument("reason")
def block(task_id: int, reason: str):
    """Block a task with a reason."""
    db = _get_db()

    async def _block():
        await db.init()
        return await db.block(task_id, reason)

    task = _run(_block())
    click.echo(f"Task #{task.id} blocked: \"{task.blocker}\"")


@main.command()
@click.argument("task_id", type=int)
def unblock(task_id: int):
    """Resume a blocked task."""
    db = _get_db()

    async def _unblock():
        await db.init()
        return await db.unblock(task_id)

    task = _run(_unblock())
    click.echo(f"Task #{task.id} unblocked, resumed to {task.status.value}")


@main.command()
@click.argument("task_id", type=int)
def done(task_id: int):
    """Mark a task as done."""
    db = _get_db()

    async def _done():
        await db.init()
        return await db.update(task_id, TaskUpdate(status=TaskStatus.DONE))

    task = _run(_done())
    click.echo(f"Task #{task.id} done: \"{task.title}\"")


@main.command()
@click.argument("task_id", type=int)
@click.argument("step", type=click.Choice([s.value for s in Substep]))
def substep(task_id: int, step: str):
    """Update a task's current substep."""
    db = _get_db()

    async def _substep():
        await db.init()
        return await db.update(task_id, TaskUpdate(substep=Substep(step)))

    task = _run(_substep())
    click.echo(f"Task #{task.id} substep: {task.substep.value}")


@main.command()
def next():
    """Show next ready task (highest priority, deps met)."""
    db = _get_db()

    async def _next():
        await db.init()
        return await db.next_ready()

    task = _run(_next())
    if not task:
        click.echo("No ready tasks.")
        return
    click.echo(f"Next: #{task.id}  {task.title}  ({task.priority.value})")
```

**Step 4: Write __main__.py**

```python
"""Allow running as python -m soul_planner."""

from soul_planner.cli import main

main()
```

**Step 5: Run tests to verify they pass**

```bash
cd ~/soul/soul-planner && python -m pytest tests/test_cli.py -v
```

Expected: all PASS

**Step 6: Run full test suite**

```bash
cd ~/soul/soul-planner && python -m pytest tests/ -v
```

Expected: all tests across test_models.py, test_db.py, test_cli.py pass.

**Step 7: Commit**

```bash
cd ~/soul/soul-planner && git add soul_planner/cli.py soul_planner/__main__.py tests/test_cli.py && git commit -m "feat: add Click CLI with full task management commands"
```

---

### Task 5: Install dev deps + smoke test

**Step 1: Install the package in dev mode**

```bash
cd ~/soul/soul-planner && pip install -e ".[dev]"
```

**Step 2: Run the CLI smoke test**

```bash
soul-planner add "Test task" --priority high
soul-planner list
soul-planner board
soul-planner status 1
soul-planner substep 1 planning
soul-planner block 1 "Test blocker"
soul-planner unblock 1
soul-planner done 1
soul-planner next
```

**Step 3: Run full test suite one final time**

```bash
cd ~/soul/soul-planner && python -m pytest tests/ -v --tb=short
```

**Step 4: Final commit if any fixes needed**

```bash
cd ~/soul/soul-planner && git add -A && git commit -m "chore: dev setup and smoke test fixes"
```
