# soul-planner Design — Claude Code Plugin

**Date:** 2026-02-23
**Status:** Approved
**Type:** Claude Code plugin (marketplace-ready)

---

## Overview

A Claude Code plugin that adds a persistent task queue with Kanban workflow. Users add tasks via `/task` commands, Claude executes them through a structured dev workflow, with live status visible in the Claude Code task panel.

## Kanban Workflow

```
BACKLOG ──> IN PROGRESS ──> VALIDATION ──> DONE
              │                  │
              ├── PLANNING       │ (user reviews)
              ├── TESTING        │
              ├── IMPLEMENTING   │
              ├── REVIEWING      │
              └── VALIDATING     │
                                 │
            BLOCKED <────────────┘ (questions/issues)
```

### States

| State | Meaning |
|-------|---------|
| **BACKLOG** | Created, waiting to be picked up |
| **IN PROGRESS** | Claude is actively working (5 substeps) |
| **BLOCKED** | Waiting for user input (question or decision) |
| **VALIDATION** | Claude finished, user reviews/approves |
| **DONE** | User approved, complete |
| **CANCELLED** | Dropped |

### IN PROGRESS Substeps

| # | Substep | What Claude Does |
|---|---------|-----------------|
| 1 | PLANNING | Read task, design approach, identify files |
| 2 | TESTING | Write tests first (TDD) |
| 3 | IMPLEMENTING | Write code to pass tests |
| 4 | REVIEWING | Self code-review, security audit |
| 5 | VALIDATING | Run full test suite, confirm green |

Status bar shows: `[Task #7: IMPLEMENTING 3/5]`

## Task Creation

### Quick mode (inline)

```
/task add "Build JWT auth for soul-mesh" --priority high
```

### Interactive mode (guided)

```
User: /task add
Claude: What's the task?
User: Build JWT auth for soul-mesh API
Claude: Any specific requirements or acceptance criteria?
User: Use bcrypt, refresh tokens, 1h expiry, store in DB
Claude: Added task #7 to BACKLOG
```

If `/task add` has no arguments, Claude asks interactively. If arguments provided, creates immediately.

## Blocker Handling

When Claude hits a question during IN PROGRESS:

1. Task state -> BLOCKED, substep preserved
2. Blocker reason stored in DB
3. Claude asks the user the question
4. User answers -> task resumes from where it paused

## Dual Storage

| Layer | Purpose |
|-------|---------|
| **SQLite** (persistent) | Source of truth. `~/.claude/soul-planner/tasks.db`. Survives across sessions. |
| **Claude Code Task UI** (live) | TaskCreate/TaskUpdate with `activeForm`. Shows spinner + status in UI panel. Synced from SQLite on session start. |

## Schema

```sql
CREATE TABLE tasks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT NOT NULL,
    description   TEXT NOT NULL DEFAULT '',
    acceptance    TEXT NOT NULL DEFAULT '',
    status        TEXT NOT NULL DEFAULT 'backlog'
                  CHECK(status IN ('backlog','in_progress','blocked','validation','done','cancelled')),
    substep       TEXT CHECK(substep IN ('planning','testing','implementing','reviewing','validating')),
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

CREATE TABLE task_dependencies (
    task_id    INTEGER NOT NULL REFERENCES tasks(id),
    depends_on INTEGER NOT NULL REFERENCES tasks(id),
    PRIMARY KEY (task_id, depends_on),
    CHECK(task_id != depends_on)
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_deps_task ON task_dependencies(task_id);
CREATE INDEX idx_deps_dep ON task_dependencies(depends_on);
```

## Plugin Structure

```
~/soul/soul-planner/
├── .claude-plugin/
│   └── plugin.json               # Marketplace manifest
├── commands/
│   ├── task.md                   # /task add|list|status|cancel|board
│   ├── task-run.md               # /task-run [id]
│   └── task-schedule.md          # /task-schedule (queue from daily-planner)
├── agents/
│   └── task-runner.md            # Background execution agent
├── skills/
│   └── task-awareness/
│       └── SKILL.md              # Auto-sync on session start
├── soul_planner/
│   ├── __init__.py
│   ├── models.py                 # Pydantic models + enums
│   ├── db.py                     # Async SQLite CRUD
│   ├── cli.py                    # Click CLI entry point
│   ├── runner.py                 # Task execution orchestrator
│   └── scheduler.py              # Daily-planner.md parser
├── tests/
│   ├── test_models.py
│   ├── test_db.py
│   ├── test_cli.py
│   ├── test_runner.py
│   └── test_scheduler.py
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

## Pydantic Models

```python
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

## Database Layer (db.py)

```python
class TaskDB:
    def __init__(self, db_path: Path): ...
    async def init(self) -> None:
    async def add(self, task: TaskCreate) -> Task:
    async def get(self, task_id: int) -> Task | None:
    async def list(self, status: TaskStatus | None = None) -> list[Task]:
    async def board(self) -> dict[TaskStatus, list[Task]]:
    async def update(self, task_id: int, update: TaskUpdate) -> Task:
    async def cancel(self, task_id: int) -> Task:
    async def block(self, task_id: int, reason: str) -> Task:
    async def unblock(self, task_id: int) -> Task:
    async def validate(self, task_id: int) -> Task:
    async def done(self, task_id: int) -> Task:
    async def substep(self, task_id: int, step: Substep) -> Task:
    async def next_ready(self) -> Task | None:
    async def check_dependencies(self, task_id: int) -> bool:
    async def promote_ready(self) -> int:
```

## CLI Commands

```
python -m soul_planner add "title" [--details "..."] [--acceptance "..."] [--priority high] [--depends-on 3,5]
python -m soul_planner list [--status backlog]
python -m soul_planner board
python -m soul_planner status <id>
python -m soul_planner cancel <id>
python -m soul_planner block <id> "reason"
python -m soul_planner unblock <id>
python -m soul_planner validate <id>
python -m soul_planner done <id>
python -m soul_planner substep <id> <step>
python -m soul_planner next
python -m soul_planner promote
```

## Config

Environment variables (pydantic-settings):

| Variable | Default | Purpose |
|----------|---------|---------|
| `PLANNER_DB_PATH` | `~/.claude/soul-planner/tasks.db` | SQLite path |
| `PLANNER_MAX_RETRIES` | `3` | Default retry count |
| `PLANNER_LOG_LEVEL` | `INFO` | structlog level |

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Plugin format | Claude Code marketplace plugin | User requirement |
| Data layer | Raw aiosqlite + Pydantic | Matches soul-mesh, no ORM overhead |
| Dependencies | Many-to-many | Supports complex workflows |
| Schedule mode | Manual `/task-schedule` trigger | No daemon needed |
| Blocker handling | Pause and ask user | User controls decisions |
| Status display | Sync to Claude Code TaskCreate/TaskUpdate | Native UI integration |
| DB location | `~/.claude/soul-planner/tasks.db` | Persists across sessions |

## Build Order

| Day | What |
|-----|------|
| Day 2 (today) | Repo structure, plugin manifest, models.py, db.py, cli.py, tests |
| Day 3 | Additional db tests, CLI polish |
| Day 4 | `commands/task.md` slash command, skill |
| Day 5 | `runner.py` — Task tool integration, `commands/task-run.md` |
| Day 6 | `scheduler.py` — planner parser, `commands/task-schedule.md`, agent |
| Day 7 | Integration tests, README, ship to GitHub |
