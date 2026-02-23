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
