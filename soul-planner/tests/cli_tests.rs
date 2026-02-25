/// Integration tests for the soul-planner CLI binary.
///
/// Uses `assert_cmd` to invoke the compiled binary with `PLANNER_DB_PATH`
/// pointed at a temporary database for isolation.

#[allow(deprecated)]
use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::tempdir;

#[allow(deprecated)]
fn cmd_with_db(db_path: &str) -> Command {
    let mut cmd = Command::cargo_bin("soul-planner").unwrap();
    cmd.env("PLANNER_DB_PATH", db_path);
    cmd
}

#[test]
fn board_empty() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    cmd_with_db(db.to_str().unwrap())
        .arg("board")
        .assert()
        .success()
        .stdout(predicate::str::contains("BACKLOG (0)"));
}

#[test]
fn add_and_board() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    let db_str = db.to_str().unwrap();

    cmd_with_db(db_str)
        .args(["add", "Test task"])
        .assert()
        .success()
        .stdout(predicate::str::contains("Added task #1"));

    cmd_with_db(db_str)
        .arg("board")
        .assert()
        .success()
        .stdout(predicate::str::contains("BACKLOG (1)"))
        .stdout(predicate::str::contains("Test task"));
}

#[test]
fn add_with_options() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    cmd_with_db(db.to_str().unwrap())
        .args([
            "add",
            "Full task",
            "--details",
            "Desc",
            "--acceptance",
            "Crit",
            "--priority",
            "critical",
        ])
        .assert()
        .success()
        .stdout(predicate::str::contains("Added task #1"));
}

#[test]
fn status_not_found() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    cmd_with_db(db.to_str().unwrap())
        .args(["status", "999"])
        .assert()
        .failure()
        .stderr(predicate::str::contains("Task #999 not found"));
}

#[test]
fn full_lifecycle() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    let db_str = db.to_str().unwrap();

    // Add
    cmd_with_db(db_str)
        .args(["add", "Lifecycle"])
        .assert()
        .success();
    // Promote
    cmd_with_db(db_str)
        .args(["promote", "1"])
        .assert()
        .success()
        .stdout(predicate::str::contains("planning"));
    // Advance
    cmd_with_db(db_str)
        .args(["advance", "1"])
        .assert()
        .success()
        .stdout(predicate::str::contains("testing"));
    // Substep
    cmd_with_db(db_str)
        .args(["substep", "1", "implementing"])
        .assert()
        .success();
    // Done
    cmd_with_db(db_str)
        .args(["done", "1"])
        .assert()
        .success()
        .stdout(predicate::str::contains("done"));
}

#[test]
fn block_and_unblock() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    let db_str = db.to_str().unwrap();

    cmd_with_db(db_str)
        .args(["add", "Block test"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["promote", "1"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["block", "1", "waiting"])
        .assert()
        .success()
        .stdout(predicate::str::contains("blocked"));
    cmd_with_db(db_str)
        .args(["unblock", "1"])
        .assert()
        .success()
        .stdout(predicate::str::contains("unblocked"));
}

#[test]
fn next_empty() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    cmd_with_db(db.to_str().unwrap())
        .arg("next")
        .assert()
        .success()
        .stdout(predicate::str::contains("No ready tasks"));
}

#[test]
fn append_output_and_status() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    let db_str = db.to_str().unwrap();

    cmd_with_db(db_str)
        .args(["add", "Output test"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["append-output", "1", "some output"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["status", "1"])
        .assert()
        .success()
        .stdout(predicate::str::contains("some output"));
}

#[test]
fn list_with_status_filter() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    let db_str = db.to_str().unwrap();

    cmd_with_db(db_str)
        .args(["add", "Task A"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["add", "Task B"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["list", "--status", "backlog"])
        .assert()
        .success()
        .stdout(predicate::str::contains("Task A"))
        .stdout(predicate::str::contains("Task B"));
    cmd_with_db(db_str)
        .args(["list", "--status", "done"])
        .assert()
        .success()
        .stdout(predicate::str::contains("No tasks found"));
}

#[test]
fn cancel_task() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    let db_str = db.to_str().unwrap();

    cmd_with_db(db_str)
        .args(["add", "Cancel me"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["cancel", "1"])
        .assert()
        .success()
        .stdout(predicate::str::contains("cancelled"));
}

#[test]
fn set_agent() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    let db_str = db.to_str().unwrap();

    cmd_with_db(db_str)
        .args(["add", "Agent test"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["set-agent", "1", "agent-abc"])
        .assert()
        .success()
        .stdout(predicate::str::contains("agent-abc"));
}

#[test]
fn validate_task() {
    let dir = tempdir().unwrap();
    let db = dir.path().join("test.db");
    let db_str = db.to_str().unwrap();

    cmd_with_db(db_str)
        .args(["add", "Validate me"])
        .assert()
        .success();
    cmd_with_db(db_str)
        .args(["validate", "1"])
        .assert()
        .success()
        .stdout(predicate::str::contains("validation"));
}
