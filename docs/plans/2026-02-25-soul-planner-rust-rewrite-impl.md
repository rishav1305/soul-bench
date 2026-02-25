# soul-planner Rust Rewrite Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite soul-planner from Python to Rust as a single binary with zero runtime dependencies.

**Architecture:** Cargo project in `soul-planner/` alongside existing Python code. 6 Rust source files map 1:1 to the Python modules. `rusqlite` with bundled SQLite for the DB layer, `clap` derive for CLI, same SQLite schema for backward compatibility.

**Tech Stack:** Rust, clap 4, rusqlite 0.32 (bundled), serde, chrono, tabled 0.17, regex, dirs 6

**Reference:** Design doc at `docs/plans/2026-02-25-soul-planner-rust-rewrite-design.md`. Python source at `soul-planner/soul_planner/`.

---

## Phase 1: Scaffold + Models (Tasks 1-3)

### Task 1: Install Rust toolchain and scaffold Cargo project

**Files:**
- Create: `soul-planner/Cargo.toml`
- Create: `soul-planner/src/main.rs`

**Step 1: Install Rust via rustup**

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
rustc --version  # Expect: rustc 1.8x.x
```

**Step 2: Initialize Cargo project inside soul-planner/**

The project already has `commands/`, `agents/`, `skills/`, `.claude-plugin/` which must be preserved. Initialize Cargo manually (not `cargo init` which would conflict):

```bash
cd ~/soul/soul-planner
mkdir -p src
```

Create `Cargo.toml`:

```toml
[package]
name = "soul-planner"
version = "0.1.0"
edition = "2021"
description = "Task queue and scheduler for Claude Code with Kanban workflow."
license = "Apache-2.0"
authors = ["Rishav"]

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

Create minimal `src/main.rs`:

```rust
fn main() {
    println!("soul-planner v0.1.0");
}
```

**Step 3: Build to verify toolchain works**

```bash
cd ~/soul/soul-planner && cargo build
```

Expected: Compiles, downloads crates, produces `target/debug/soul-planner`.

**Step 4: Run to verify**

```bash
./target/debug/soul-planner
```

Expected: `soul-planner v0.1.0`

**Step 5: Add to .gitignore**

Create `soul-planner/.gitignore`:

```
/target
```

**Step 6: Commit**

```bash
git add Cargo.toml src/main.rs .gitignore
git commit -m "feat(soul-planner): scaffold Rust project with Cargo.toml"
```

---

### Task 2: Write models module with enums and structs

**Files:**
- Create: `soul-planner/src/models.rs`
- Modify: `soul-planner/src/main.rs` (add `mod models;`)
- Create: `soul-planner/tests/model_tests.rs`

**Reference:** Python `soul_planner/models.py` (82 lines)

**Step 1: Write model tests first**

Create `tests/model_tests.rs`:

```rust
use soul_planner::models::*;

#[test]
fn task_status_from_str() {
    assert_eq!(TaskStatus::from_str("backlog"), Some(TaskStatus::Backlog));
    assert_eq!(TaskStatus::from_str("in_progress"), Some(TaskStatus::InProgress));
    assert_eq!(TaskStatus::from_str("blocked"), Some(TaskStatus::Blocked));
    assert_eq!(TaskStatus::from_str("validation"), Some(TaskStatus::Validation));
    assert_eq!(TaskStatus::from_str("done"), Some(TaskStatus::Done));
    assert_eq!(TaskStatus::from_str("cancelled"), Some(TaskStatus::Cancelled));
    assert_eq!(TaskStatus::from_str("bogus"), None);
}

#[test]
fn task_status_to_str() {
    assert_eq!(TaskStatus::Backlog.as_str(), "backlog");
    assert_eq!(TaskStatus::InProgress.as_str(), "in_progress");
}

#[test]
fn substep_from_str() {
    assert_eq!(Substep::from_str("planning"), Some(Substep::Planning));
    assert_eq!(Substep::from_str("testing"), Some(Substep::Testing));
    assert_eq!(Substep::from_str("implementing"), Some(Substep::Implementing));
    assert_eq!(Substep::from_str("reviewing"), Some(Substep::Reviewing));
    assert_eq!(Substep::from_str("validating"), Some(Substep::Validating));
    assert_eq!(Substep::from_str("bogus"), None);
}

#[test]
fn substep_index_1based() {
    assert_eq!(Substep::Planning.index(), 1);
    assert_eq!(Substep::Testing.index(), 2);
    assert_eq!(Substep::Implementing.index(), 3);
    assert_eq!(Substep::Reviewing.index(), 4);
    assert_eq!(Substep::Validating.index(), 5);
}

#[test]
fn substep_next() {
    assert_eq!(Substep::Planning.next(), Some(Substep::Testing));
    assert_eq!(Substep::Validating.next(), None);
}

#[test]
fn priority_ordering() {
    // Critical < High < Normal < Low (sort weight)
    assert!(Priority::Critical.weight() < Priority::High.weight());
    assert!(Priority::High.weight() < Priority::Normal.weight());
    assert!(Priority::Normal.weight() < Priority::Low.weight());
}

#[test]
fn priority_from_str() {
    assert_eq!(Priority::from_str("critical"), Some(Priority::Critical));
    assert_eq!(Priority::from_str("high"), Some(Priority::High));
    assert_eq!(Priority::from_str("normal"), Some(Priority::Normal));
    assert_eq!(Priority::from_str("low"), Some(Priority::Low));
    assert_eq!(Priority::from_str("bogus"), None);
}
```

**Step 2: Run tests to verify they fail**

```bash
cd ~/soul/soul-planner && cargo test --test model_tests
```

Expected: Compilation error -- `models` module doesn't exist yet.

**Step 3: Write models.rs**

Create `src/models.rs` with all enums, conversion methods, and Task struct. Port from Python `models.py`. Include:
- `TaskStatus` enum with `from_str()`, `as_str()`, `all_values()`
- `Substep` enum with `from_str()`, `as_str()`, `index()`, `next()`, `all_values()`
- `Priority` enum with `from_str()`, `as_str()`, `weight()`
- `Task` struct with all fields matching the Python version
- `TaskCreate` struct (title, description, acceptance, priority, depends_on)

Update `src/main.rs` to declare the module as public (needed for integration tests):

```rust
pub mod models;

fn main() {
    println!("soul-planner v0.1.0");
}
```

Also add a `src/lib.rs` to expose modules for integration tests:

```rust
pub mod models;
```

**Step 4: Run tests to verify they pass**

```bash
cd ~/soul/soul-planner && cargo test --test model_tests
```

Expected: All tests pass.

**Step 5: Commit**

```bash
git add src/models.rs src/lib.rs tests/model_tests.rs
git commit -m "feat(soul-planner): add Rust models -- TaskStatus, Substep, Priority, Task"
```

---

### Task 3: Write DB module with SQLite CRUD

**Files:**
- Create: `soul-planner/src/db.rs`
- Modify: `soul-planner/src/lib.rs` (add `pub mod db;`)
- Create: `soul-planner/tests/db_tests.rs`

**Reference:** Python `soul_planner/db.py` (319 lines)

**Step 1: Write DB tests first**

Create `tests/db_tests.rs` porting key tests from `tests/test_db.py`:

```rust
use soul_planner::db::TaskDB;
use soul_planner::models::*;

#[test]
fn init_creates_tables() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let tables = db.table_names();
    assert!(tables.contains(&"tasks".to_string()));
    assert!(tables.contains(&"task_dependencies".to_string()));
}

#[test]
fn init_is_idempotent() {
    let db = TaskDB::memory();
    db.init().unwrap();
    db.init().unwrap(); // Should not panic
}

#[test]
fn add_minimal_task() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let task = db.add(TaskCreate::new("Test task")).unwrap();
    assert_eq!(task.id, 1);
    assert_eq!(task.title, "Test task");
    assert_eq!(task.status, TaskStatus::Backlog);
    assert_eq!(task.priority, Priority::Normal);
    assert!(task.substep.is_none());
    assert!(task.depends_on.is_empty());
}

#[test]
fn add_with_priority() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let create = TaskCreate {
        title: "Urgent".to_string(),
        priority: Priority::Critical,
        ..TaskCreate::new("Urgent")
    };
    let task = db.add(create).unwrap();
    assert_eq!(task.priority, Priority::Critical);
}

#[test]
fn add_with_dependencies() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t1 = db.add(TaskCreate::new("First")).unwrap();
    let t2 = db.add(TaskCreate {
        depends_on: vec![t1.id],
        ..TaskCreate::new("Second")
    }).unwrap();
    assert_eq!(t2.depends_on, vec![t1.id]);
}

#[test]
fn get_returns_none_for_missing() {
    let db = TaskDB::memory();
    db.init().unwrap();
    assert!(db.get(999).unwrap().is_none());
}

#[test]
fn list_by_status() {
    let db = TaskDB::memory();
    db.init().unwrap();
    db.add(TaskCreate::new("A")).unwrap();
    db.add(TaskCreate::new("B")).unwrap();
    let all = db.list(None).unwrap();
    assert_eq!(all.len(), 2);
    let backlog = db.list(Some(TaskStatus::Backlog)).unwrap();
    assert_eq!(backlog.len(), 2);
    let done = db.list(Some(TaskStatus::Done)).unwrap();
    assert_eq!(done.len(), 0);
}

#[test]
fn update_status() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let updated = db.update_status(t.id, TaskStatus::InProgress).unwrap();
    assert_eq!(updated.status, TaskStatus::InProgress);
    assert!(updated.started_at.is_some());
}

#[test]
fn update_done_sets_completed_at() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let updated = db.update_status(t.id, TaskStatus::Done).unwrap();
    assert_eq!(updated.status, TaskStatus::Done);
    assert!(updated.completed_at.is_some());
}

#[test]
fn block_and_unblock() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    db.update_status(t.id, TaskStatus::InProgress).unwrap();
    let blocked = db.block(t.id, "waiting for input").unwrap();
    assert_eq!(blocked.status, TaskStatus::Blocked);
    assert_eq!(blocked.blocker.as_deref(), Some("waiting for input"));
    let unblocked = db.unblock(t.id).unwrap();
    assert_eq!(unblocked.status, TaskStatus::InProgress);
    assert!(unblocked.blocker.is_none());
}

#[test]
fn cancel_task() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let cancelled = db.cancel(t.id).unwrap();
    assert_eq!(cancelled.status, TaskStatus::Cancelled);
    assert!(cancelled.completed_at.is_some());
}

#[test]
fn check_dependencies_all_done() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t1 = db.add(TaskCreate::new("A")).unwrap();
    let t2 = db.add(TaskCreate {
        depends_on: vec![t1.id],
        ..TaskCreate::new("B")
    }).unwrap();
    assert!(!db.check_deps_met(t2.id).unwrap());
    db.update_status(t1.id, TaskStatus::Done).unwrap();
    assert!(db.check_deps_met(t2.id).unwrap());
}

#[test]
fn next_ready_picks_highest_priority() {
    let db = TaskDB::memory();
    db.init().unwrap();
    db.add(TaskCreate {
        priority: Priority::Low,
        ..TaskCreate::new("Low")
    }).unwrap();
    db.add(TaskCreate {
        priority: Priority::Critical,
        ..TaskCreate::new("Critical")
    }).unwrap();
    let next = db.next_ready().unwrap().unwrap();
    assert_eq!(next.title, "Critical");
}

#[test]
fn board_groups_by_status() {
    let db = TaskDB::memory();
    db.init().unwrap();
    db.add(TaskCreate::new("A")).unwrap();
    let t2 = db.add(TaskCreate::new("B")).unwrap();
    db.update_status(t2.id, TaskStatus::Done).unwrap();
    let board = db.board().unwrap();
    assert_eq!(board.get(&TaskStatus::Backlog).unwrap().len(), 1);
    assert_eq!(board.get(&TaskStatus::Done).unwrap().len(), 1);
}

#[test]
fn append_output() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    db.append_output(t.id, "first").unwrap();
    let t = db.get(t.id).unwrap().unwrap();
    assert_eq!(t.output.as_deref(), Some("first"));
    db.append_output(t.id, "second").unwrap();
    let t = db.get(t.id).unwrap().unwrap();
    assert_eq!(t.output.as_deref(), Some("first\n---\nsecond"));
}

#[test]
fn set_agent() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    db.set_agent(t.id, "agent-123").unwrap();
    let t = db.get(t.id).unwrap().unwrap();
    assert_eq!(t.agent_id.as_deref(), Some("agent-123"));
}

#[test]
fn set_substep() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    db.set_substep(t.id, Substep::Testing).unwrap();
    let t = db.get(t.id).unwrap().unwrap();
    assert_eq!(t.substep, Some(Substep::Testing));
}

#[test]
fn file_db_persists() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("test.db");
    {
        let db = TaskDB::new(path.to_str().unwrap());
        db.init().unwrap();
        db.add(TaskCreate::new("Persistent")).unwrap();
    }
    {
        let db = TaskDB::new(path.to_str().unwrap());
        db.init().unwrap();
        let tasks = db.list(None).unwrap();
        assert_eq!(tasks.len(), 1);
        assert_eq!(tasks[0].title, "Persistent");
    }
}
```

**Step 2: Run tests to verify they fail**

```bash
cd ~/soul/soul-planner && cargo test --test db_tests
```

Expected: Compilation error -- `db` module doesn't exist.

**Step 3: Write db.rs**

Create `src/db.rs` implementing `TaskDB` with all methods. Port from Python `db.py`. Key methods:
- `TaskDB::new(path)` / `TaskDB::memory()` -- constructors
- `init()` -- create tables with same DDL
- `add(TaskCreate) -> Task`
- `get(id) -> Option<Task>`
- `list(Option<TaskStatus>) -> Vec<Task>`
- `board() -> HashMap<TaskStatus, Vec<Task>>`
- `update_status(id, TaskStatus) -> Task`
- `set_substep(id, Substep) -> Task`
- `block(id, reason) -> Task`
- `unblock(id) -> Task`
- `cancel(id) -> Task`
- `check_deps_met(id) -> bool`
- `next_ready() -> Option<Task>`
- `append_output(id, text) -> Task`
- `set_agent(id, agent_id) -> Task`
- `table_names() -> Vec<String>` (for testing)

Use `rusqlite::Connection` (sync, not async). Same parameterized queries with `?`.

Update `src/lib.rs`:

```rust
pub mod models;
pub mod db;
```

**Step 4: Run tests**

```bash
cd ~/soul/soul-planner && cargo test --test db_tests
```

Expected: All tests pass.

**Step 5: Commit**

```bash
git add src/db.rs tests/db_tests.rs
git commit -m "feat(soul-planner): add Rust DB module -- SQLite CRUD with rusqlite"
```

---

## Phase 2: Runner + Scheduler (Tasks 4-5)

### Task 4: Write runner module -- substep state machine

**Files:**
- Create: `soul-planner/src/runner.rs`
- Modify: `soul-planner/src/lib.rs` (add `pub mod runner;`)
- Create: `soul-planner/tests/runner_tests.rs`

**Reference:** Python `soul_planner/runner.py` (132 lines)

**Step 1: Write runner tests**

Port from `tests/test_runner.py`. Test:
- `start()` -- moves BACKLOG -> IN_PROGRESS with PLANNING substep
- `advance()` -- planning -> testing -> ... -> validating -> VALIDATION status
- `advance()` on non-in-progress task -> error
- `fail()` -- increments retry_count, moves to BACKLOG
- `fail()` past max_retries -> CANCELLED
- `block()` / `unblock()` round-trip
- `complete()` -- moves to DONE
- `substep_label()` -- formatting for each state

**Step 2: Run tests to verify they fail**

```bash
cd ~/soul/soul-planner && cargo test --test runner_tests
```

**Step 3: Write runner.rs**

Port `TaskRunner` struct and methods from Python. Key functions:
- `Runner::new(db: &TaskDB)`
- `start(task_id) -> Result<Task>`
- `advance(task_id) -> Result<Task>`
- `complete(task_id) -> Result<Task>`
- `fail(task_id, error) -> Result<Task>`
- `block(task_id, reason) -> Result<Task>`
- `unblock(task_id) -> Result<Task>`
- `substep_label(task: &Task) -> String`

**Step 4: Run tests**

```bash
cd ~/soul/soul-planner && cargo test --test runner_tests
```

**Step 5: Commit**

```bash
git add src/runner.rs tests/runner_tests.rs
git commit -m "feat(soul-planner): add runner -- substep state machine"
```

---

### Task 5: Write scheduler module -- daily planner parser

**Files:**
- Create: `soul-planner/src/scheduler.rs`
- Modify: `soul-planner/src/lib.rs` (add `pub mod scheduler;`)
- Create: `soul-planner/tests/scheduler_tests.rs`

**Reference:** Python `soul_planner/scheduler.py` (174 lines)

**Step 1: Write scheduler tests**

Port from `tests/test_scheduler.py`. Test with embedded markdown:
- Parse day header date extraction
- Extract block number from header
- `parse_planner()` -- finds uncompleted `- [ ]` tasks for target date
- Skips `[x]`, `[-]`, `[!]` tasks
- Block filter only returns matching block tasks
- `schedule_tasks()` -- creates tasks in DB, skips duplicates
- Priority mapping: Block 1=HIGH, 2=NORMAL, 3=NORMAL, 4=LOW

Use this test markdown:

```markdown
## Day 1 -- Sat Feb 22

### Block 1: BUILD (9am-1pm)
- [x] Completed task
- [ ] Uncompleted build task
- [-] Skipped task

### Block 2: EXPLORE (2pm-6pm)
- [ ] Explore task A
- [ ] Explore task B

### Block 3: SOCIAL (7pm-9pm)
- [ ] Write post
- [!] Blocked post

### Block 4: SCOUT (9pm-11pm)
- [ ] Check job board

---

## Day 2 -- Sun Feb 23
```

**Step 2: Run tests to verify they fail**

```bash
cd ~/soul/soul-planner && cargo test --test scheduler_tests
```

**Step 3: Write scheduler.rs**

Port `parse_planner()` and `schedule_tasks()`. Use `regex` crate for markdown parsing. Read files with `std::fs::read_to_string` (sync, no async needed).

**Step 4: Run tests**

```bash
cd ~/soul/soul-planner && cargo test --test scheduler_tests
```

**Step 5: Commit**

```bash
git add src/scheduler.rs tests/scheduler_tests.rs
git commit -m "feat(soul-planner): add scheduler -- daily planner parser"
```

---

## Phase 3: CLI + Board (Tasks 6-8)

### Task 6: Write board formatting module

**Files:**
- Create: `soul-planner/src/board.rs`
- Modify: `soul-planner/src/lib.rs` (add `pub mod board;`)

**Step 1: Write board.rs**

Format the Kanban board output matching the Python version exactly:

```
BACKLOG (2)
----------------------------------------
  #1  Build auth module  (high)
  #2  Write docs  (normal)

IN_PROGRESS (1)
----------------------------------------
  #3  Fix login bug  (critical) > testing

BLOCKED (0)
----------------------------------------
  (empty)
...
```

Use the `tabled` crate for alignment if helpful, or plain `format!()` to match exact Python output.

**Step 2: Verify output matches Python**

Run both Python and Rust with same DB, compare output.

**Step 3: Commit**

```bash
git add src/board.rs
git commit -m "feat(soul-planner): add board formatting module"
```

---

### Task 7: Write CLI with all 16 clap commands

**Files:**
- Rewrite: `soul-planner/src/main.rs`
- Create: `soul-planner/tests/cli_tests.rs`

**Reference:** Python `soul_planner/cli.py` (363 lines)

**Step 1: Write CLI integration tests**

Use `assert_cmd` to test the actual binary. Port from `tests/test_cli.py` and `tests/test_e2e.py`:

```rust
use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;

fn cmd() -> Command {
    let mut cmd = Command::cargo_bin("soul-planner").unwrap();
    let dir = tempdir().unwrap();
    cmd.env("PLANNER_DB_PATH", dir.path().join("test.db").to_str().unwrap());
    cmd
}

#[test]
fn board_empty() {
    cmd().arg("board").assert().success().stdout(predicate::str::contains("BACKLOG (0)"));
}

#[test]
fn add_task() {
    // Need shared temp DB across commands
    let dir = tempdir().unwrap();
    let db_path = dir.path().join("test.db");
    let db_str = db_path.to_str().unwrap();

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", db_str)
        .args(["add", "Test task"])
        .assert().success()
        .stdout(predicate::str::contains("Added task #1"));

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", db_str)
        .arg("board")
        .assert().success()
        .stdout(predicate::str::contains("Test task"));
}

#[test]
fn status_not_found() {
    cmd().args(["status", "999"]).assert().failure()
        .stderr(predicate::str::contains("Task #999 not found"));
}

#[test]
fn full_lifecycle() {
    let dir = tempdir().unwrap();
    let db_str = dir.path().join("test.db").to_str().unwrap().to_string();

    // Add
    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["add", "Lifecycle test", "--priority", "high"])
        .assert().success();

    // Promote
    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["promote", "1"])
        .assert().success()
        .stdout(predicate::str::contains("planning"));

    // Substep
    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["substep", "1", "testing"])
        .assert().success();

    // Done
    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["done", "1"])
        .assert().success()
        .stdout(predicate::str::contains("done"));
}

#[test]
fn add_with_all_options() {
    cmd().args(["add", "Full task", "--details", "Description", "--acceptance", "Criteria", "--priority", "critical"])
        .assert().success()
        .stdout(predicate::str::contains("Added task #1"));
}

#[test]
fn block_and_unblock() {
    let dir = tempdir().unwrap();
    let db_str = dir.path().join("test.db").to_str().unwrap().to_string();

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["add", "Block test"]).assert().success();

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["promote", "1"]).assert().success();

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["block", "1", "waiting for API"]).assert().success()
        .stdout(predicate::str::contains("blocked"));

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["unblock", "1"]).assert().success()
        .stdout(predicate::str::contains("unblocked"));
}

#[test]
fn next_empty() {
    cmd().arg("next").assert().success()
        .stdout(predicate::str::contains("No ready tasks"));
}

#[test]
fn append_output_and_status() {
    let dir = tempdir().unwrap();
    let db_str = dir.path().join("test.db").to_str().unwrap().to_string();

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["add", "Output test"]).assert().success();

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["append-output", "1", "Some output"]).assert().success();

    Command::cargo_bin("soul-planner").unwrap()
        .env("PLANNER_DB_PATH", &db_str)
        .args(["status", "1"]).assert().success()
        .stdout(predicate::str::contains("Some output"));
}
```

**Step 2: Run tests to verify they fail**

```bash
cd ~/soul/soul-planner && cargo test --test cli_tests
```

**Step 3: Write main.rs with full CLI**

Implement all 16 commands using `clap` derive macros. Each command:
1. Opens DB (from `PLANNER_DB_PATH` env or default `~/.claude/soul-planner/tasks.db`)
2. Calls init()
3. Performs the operation
4. Prints result to stdout
5. Prints errors to stderr, exits with code 1

Match the Python output format exactly for each command.

**Step 4: Run tests**

```bash
cd ~/soul/soul-planner && cargo test --test cli_tests
```

**Step 5: Commit**

```bash
git add src/main.rs tests/cli_tests.rs
git commit -m "feat(soul-planner): add full CLI with 16 clap commands"
```

---

### Task 8: Write E2E tests covering full workflows

**Files:**
- Create: `soul-planner/tests/e2e_tests.rs`

Port remaining tests from `tests/test_e2e.py` that aren't covered above:
- Full task lifecycle: add -> promote -> all 5 substeps -> validate -> done
- Dependency chain: A -> B -> C, complete in order, verify deps block correctly
- Scheduler -> runner integration: schedule tasks from planner, run next
- Multiple tasks with priority ordering
- Error cases: cancel non-existent task, block already-blocked task

**Step 1: Write tests, Step 2: Run, Step 3: Fix any issues, Step 4: Commit**

```bash
git add tests/e2e_tests.rs
git commit -m "test(soul-planner): add E2E tests -- full lifecycle and edge cases"
```

---

## Phase 4: Install + Wire Up (Tasks 9-11)

### Task 9: Install binary and verify against existing DB

**Step 1: Build release binary**

```bash
cd ~/soul/soul-planner && cargo build --release
```

**Step 2: Install to PATH**

```bash
cargo install --path .
```

Verify: `which soul-planner` should point to `~/.cargo/bin/soul-planner`.

**Step 3: Test against existing tasks.db**

```bash
soul-planner board
```

Should show same output as `python3 -m soul_planner board` (both read same DB).

**Step 4: Run full test suite**

```bash
cd ~/soul/soul-planner && cargo test
```

Expected: All tests pass.

**Step 5: Commit any fixes**

---

### Task 10: Update all Claude Code files to use `soul-planner` binary

**Files:**
- Modify: `soul-planner/commands/planner.md`
- Modify: `soul-planner/commands/planner-run.md`
- Modify: `soul-planner/commands/planner-run-auto.md`
- Modify: `soul-planner/commands/planner-schedule.md`
- Modify: `soul-planner/agents/task-orchestrator.md`
- Modify: `soul-planner/agents/task-runner.md`
- Modify: `soul-planner/skills/task-awareness/SKILL.md`

**Step 1: Replace all `python3 -m soul_planner` with `soul-planner`**

Global search-and-replace across all `.md` files in commands/, agents/, skills/:

```
python3 -m soul_planner -> soul-planner
```

Also replace `python3 -m pytest` with `cargo test` in task-runner.md (for Rust projects).

**Step 2: Remove Python install instructions from planner.md**

Replace the Setup section:

```markdown
## Setup

The CLI lives at `~/soul/soul-planner/`. If not installed:
\`\`\`bash
cd ~/soul/soul-planner && cargo install --path .
\`\`\`
```

**Step 3: Test that `/planner` still works**

```bash
soul-planner board
```

**Step 4: Commit**

```bash
git add commands/ agents/ skills/
git commit -m "refactor(soul-planner): update all Claude Code files to use Rust binary"
```

---

### Task 11: Create install script and update plugin manifest

**Files:**
- Create: `soul-planner/scripts/install.sh`
- Modify: `soul-planner/.claude-plugin/plugin.json` (bump version)

**Step 1: Write install.sh**

```bash
#!/bin/bash
set -euo pipefail

# Check if soul-planner is already installed
if command -v soul-planner &>/dev/null; then
    echo "soul-planner $(soul-planner --version 2>/dev/null || echo 'installed')"
    exit 0
fi

# Check for Cargo
if ! command -v cargo &>/dev/null; then
    echo "Error: Rust toolchain not found."
    echo "Install via: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# Build and install
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Building soul-planner..."
cd "$SCRIPT_DIR"
cargo install --path . --quiet
echo "Installed: $(which soul-planner)"
```

**Step 2: Bump plugin version**

```json
{
  "name": "soul-planner",
  "description": "Task queue and scheduler for Claude Code. Kanban workflow with BACKLOG/IN_PROGRESS/VALIDATION/DONE.",
  "version": "0.2.0",
  "author": { "name": "Rishav" }
}
```

**Step 3: Commit**

```bash
chmod +x scripts/install.sh
git add scripts/install.sh .claude-plugin/plugin.json
git commit -m "feat(soul-planner): add install script, bump to v0.2.0 (Rust)"
```

---

## Summary

| Phase | Tasks | What |
|-------|-------|------|
| 1 | 1-3 | Scaffold + Models + DB |
| 2 | 4-5 | Runner + Scheduler |
| 3 | 6-8 | Board + CLI + E2E tests |
| 4 | 9-11 | Install + Wire up + Script |

Total: 11 tasks, ~1,000 lines Rust + ~300 lines tests. Same SQLite schema. Drop-in replacement.
