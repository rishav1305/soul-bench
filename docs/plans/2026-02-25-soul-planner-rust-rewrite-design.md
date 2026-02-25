# soul-planner Rust Rewrite Design

**Date:** 2026-02-25
**Status:** Approved
**Goal:** Rewrite soul-planner from Python to Rust for zero-dependency, single-binary distribution.

## Problem

soul-planner is a Claude Code plugin CLI that requires Python 3.11+, pip, and 6 packages. On diverse user machines:
- `python` vs `python3` vs `python3.12` — binary name varies
- PEP 668 restrictions require `--break-system-packages` on newer Debian/Ubuntu
- No Python at all on some systems
- Dependency install failures crash with cryptic errors
- Cold start ~500ms due to Python interpreter + import chain

A compiled Rust binary eliminates all of these.

## Approach

Full Rust rewrite of all 5 Python modules (~1,070 lines) into a single binary. Same SQLite schema for backward compatibility. Drop-in replacement.

## Project Structure

```
soul-planner/
  src/
    main.rs          # clap CLI definition + dispatch
    db.rs            # rusqlite wrapper (sync)
    models.rs        # TaskStatus, Substep, Priority enums + Task struct
    runner.rs        # Substep state machine (start, advance)
    scheduler.rs     # Daily planner markdown parser
    board.rs         # Kanban board terminal formatting
  Cargo.toml
  tests/
    cli_tests.rs     # assert_cmd integration tests
    db_tests.rs      # In-memory SQLite unit tests
    model_tests.rs   # Enum conversion + validation
    runner_tests.rs  # State machine transitions
    scheduler_tests.rs # Markdown parsing
    e2e_tests.rs     # Full workflow with temp DB
  # Unchanged:
  commands/          # Claude Code slash commands
  agents/            # Claude Code agent definitions
  skills/            # Claude Code skills
  .claude-plugin/    # Plugin manifest
```

## Dependencies

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
rusqlite = { version = "0.32", features = ["bundled"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
chrono = { version = "0.4", features = ["serde"] }
tabled = "0.17"
regex = "1"
dirs = "6"

[dev-dependencies]
assert_cmd = "2"
predicates = "3"
tempfile = "3"
```

`rusqlite` with `bundled` feature compiles SQLite into the binary -- zero system deps.

## Module Mapping

| Python | Rust | Crates Used |
|--------|------|-------------|
| models.py (82 LOC) | models.rs | serde |
| db.py (319 LOC) | db.rs | rusqlite, chrono |
| cli.py (363 LOC) | main.rs | clap |
| runner.py (132 LOC) | runner.rs | (none) |
| scheduler.py (174 LOC) | scheduler.rs | regex, chrono |
| (board formatting in cli.py) | board.rs | tabled |

## DB Schema

Identical to Python version -- same tables, constraints, column names:

```sql
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
```

DB path: `~/.claude/soul-planner/tasks.db` (override with `PLANNER_DB_PATH`).

## CLI Commands

All 16 commands ported 1:1 via clap derive:

| Command | Args | Maps to Python |
|---------|------|----------------|
| `soul-planner add TITLE` | --details, --acceptance, --priority, --depends-on | cli.add |
| `soul-planner list` | --status | cli.list_tasks |
| `soul-planner board` | (none) | cli.board |
| `soul-planner status ID` | (none) | cli.status |
| `soul-planner cancel ID` | (none) | cli.cancel |
| `soul-planner block ID REASON` | (none) | cli.block |
| `soul-planner unblock ID` | (none) | cli.unblock |
| `soul-planner done ID` | --output | cli.done |
| `soul-planner set-agent ID AGENT_ID` | (none) | cli.set_agent |
| `soul-planner append-output ID TEXT` | (none) | cli.append_output |
| `soul-planner validate ID` | (none) | cli.validate |
| `soul-planner promote ID` | (none) | cli.promote |
| `soul-planner advance ID` | (none) | cli.advance |
| `soul-planner substep ID STEP` | (none) | cli.substep |
| `soul-planner schedule` | --block, --planner | cli.schedule |
| `soul-planner next` | (none) | cli.next_task |

## Error Handling

| Scenario | Behavior |
|----------|----------|
| DB doesn't exist | Auto-create directory + init schema |
| DB corrupted | "Database corrupted at PATH. Remove to start fresh." |
| Task not found | "Task #N not found." (exit 1) |
| Invalid enum value | "Invalid status 'foo'. Valid: backlog, in_progress, ..." (exit 1) |
| No write permission | "Cannot write to PATH. Set PLANNER_DB_PATH." (exit 2) |
| Disk full | "Disk full. Cannot write to PATH." (exit 2) |

Exit codes: 0 = success, 1 = user error, 2 = system error.

## Distribution

Install via Cargo:
```bash
cd soul-planner && cargo install --path .
```

Requires Rust toolchain. Binary goes to `~/.cargo/bin/soul-planner` (already on PATH for Rust users).

Bootstrap script `scripts/install.sh`:
1. Check if `soul-planner` on PATH -> done
2. Check if `cargo` exists -> `cargo install --path .`
3. Neither -> print install instructions for rustup

## Command Reference Update

All Claude Code files (commands/, agents/, skills/) change:

| Before | After |
|--------|-------|
| `python3 -m soul_planner board` | `soul-planner board` |
| `python3 -m soul_planner add "title"` | `soul-planner add "title"` |
| `python3 -m soul_planner substep 1 planning` | `soul-planner substep 1 planning` |

## Testing

Port all 126 Python tests:
- `cargo test` runs all unit + integration tests
- DB tests use `:memory:` SQLite
- CLI tests use `assert_cmd` to test actual binary output
- E2E tests use `tempfile` for isolated DB files

## Migration Path

1. Build Rust binary
2. Verify same output as Python for all commands
3. Update commands/agents/skills to reference `soul-planner`
4. Keep Python code in repo as reference (can delete later)
5. Existing `tasks.db` continues working unchanged
