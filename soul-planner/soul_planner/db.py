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

_SCHEMA = """\
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
    agent_id      TEXT,
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
            agent_id=row["agent_id"],
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

        # Only hardcoded column names are appended to `sets`.
        # Do NOT append user-supplied strings — values belong in `params`.
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

        if update.agent_id is not None:
            sets.append("agent_id = ?")
            params.append(update.agent_id)

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
        """Count backlog tasks whose dependencies are all met.

        Returns the count of ready tasks. Does not change status.
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
