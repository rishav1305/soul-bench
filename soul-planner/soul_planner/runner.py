"""Task execution orchestrator for soul-planner.

Picks up queued tasks and manages the execution lifecycle through
5 substeps: planning -> testing -> implementing -> reviewing -> validating.

This module provides the logic for task execution. The actual work is done
by Claude Code's Task tool (dispatched via the task-runner agent or
/task-run command). This module manages state transitions.
"""

from __future__ import annotations

import structlog

from soul_planner.db import TaskDB
from soul_planner.models import Substep, Task, TaskStatus, TaskUpdate

logger = structlog.get_logger("soul-planner.runner")

SUBSTEP_ORDER = list(Substep)


def substep_index(step: Substep) -> int:
    """Return the 1-based index of a substep."""
    return SUBSTEP_ORDER.index(step) + 1


def substep_label(task: Task) -> str:
    """Format a status bar label for a task's current state."""
    if task.status == TaskStatus.BLOCKED:
        reason = task.blocker or "unknown"
        return f"BLOCKED: {task.title} -- {reason}"
    if task.status == TaskStatus.IN_PROGRESS and task.substep:
        idx = substep_index(task.substep)
        return f"{task.substep.value.upper()}: {task.title} [{idx}/5]"
    if task.status == TaskStatus.VALIDATION:
        return f"Review: {task.title}"
    if task.status == TaskStatus.DONE:
        return f"Done: {task.title}"
    return f"Queued: {task.title}"


class TaskRunner:
    """Manages task execution lifecycle."""

    def __init__(self, db: TaskDB) -> None:
        self._db = db

    async def pick_next(self) -> Task | None:
        """Pick the next ready task from backlog."""
        return await self._db.next_ready()

    async def start(self, task_id: int) -> Task:
        """Move a task to IN_PROGRESS with PLANNING substep."""
        task = await self._db.update(
            task_id,
            TaskUpdate(status=TaskStatus.IN_PROGRESS, substep=Substep.PLANNING),
        )
        logger.info("Task started", task_id=task_id, title=task.title)
        return task

    async def advance(self, task_id: int) -> Task:
        """Advance to the next substep. Returns updated task.

        If already at VALIDATING (last substep), moves to VALIDATION status.
        """
        task = await self._db.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        if task.status != TaskStatus.IN_PROGRESS:
            raise ValueError(f"Task {task_id} is not in progress (status={task.status.value})")
        if not task.substep:
            raise ValueError(f"Task {task_id} has no current substep")

        idx = SUBSTEP_ORDER.index(task.substep)
        if idx >= len(SUBSTEP_ORDER) - 1:
            # Last substep -> move to validation
            updated = await self._db.update(
                task_id,
                TaskUpdate(status=TaskStatus.VALIDATION),
            )
            logger.info("Task moved to validation", task_id=task_id)
            return updated

        next_step = SUBSTEP_ORDER[idx + 1]
        updated = await self._db.update(task_id, TaskUpdate(substep=next_step))
        logger.info("Task advanced", task_id=task_id, substep=next_step.value)
        return updated

    async def complete(self, task_id: int) -> Task:
        """Mark a task as DONE."""
        task = await self._db.update(task_id, TaskUpdate(status=TaskStatus.DONE))
        logger.info("Task completed", task_id=task_id, title=task.title)
        return task

    async def fail(self, task_id: int, error: str) -> Task:
        """Mark a task as failed. Increments retry count."""
        task = await self._db.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        new_retry = task.retry_count + 1
        if new_retry >= task.max_retries:
            # Max retries exceeded -> cancel
            await self._db._execute(
                "UPDATE tasks SET error = ?, retry_count = ? WHERE id = ?",
                (error, new_retry, task_id),
            )
            updated = await self._db.cancel(task_id)
            logger.warning("Task max retries exceeded, cancelled", task_id=task_id, retries=new_retry)
            return updated

        # Move back to backlog for retry
        await self._db._execute(
            "UPDATE tasks SET status = ?, error = ?, retry_count = ?, substep = NULL WHERE id = ?",
            (TaskStatus.BACKLOG.value, error, new_retry, task_id),
        )
        updated = await self._db.get(task_id)
        logger.info("Task failed, will retry", task_id=task_id, retry=new_retry, max=task.max_retries)
        return updated

    async def block(self, task_id: int, reason: str) -> Task:
        """Block a task with a reason."""
        task = await self._db.block(task_id, reason)
        logger.info("Task blocked", task_id=task_id, reason=reason)
        return task

    async def unblock(self, task_id: int) -> Task:
        """Unblock a task and resume."""
        task = await self._db.unblock(task_id)
        logger.info("Task unblocked", task_id=task_id)
        return task
