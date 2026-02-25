use soul_planner::db::TaskDB;
use soul_planner::models::*;
use soul_planner::runner::{Runner, substep_label};

fn setup() -> TaskDB {
    let db = TaskDB::memory();
    db.init().unwrap();
    db
}

#[test]
fn start_moves_to_in_progress() {
    let db = setup();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let runner = Runner::new(&db);
    let started = runner.start(t.id).unwrap();
    assert_eq!(started.status, TaskStatus::InProgress);
    assert_eq!(started.substep, Some(Substep::Planning));
    assert!(started.started_at.is_some());
}

#[test]
fn advance_through_all_substeps() {
    let db = setup();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let runner = Runner::new(&db);
    runner.start(t.id).unwrap();

    let t = runner.advance(t.id).unwrap();
    assert_eq!(t.substep, Some(Substep::Testing));

    let t = runner.advance(t.id).unwrap();
    assert_eq!(t.substep, Some(Substep::Implementing));

    let t = runner.advance(t.id).unwrap();
    assert_eq!(t.substep, Some(Substep::Reviewing));

    let t = runner.advance(t.id).unwrap();
    assert_eq!(t.substep, Some(Substep::Validating));

    // Past last substep -> VALIDATION status
    let t = runner.advance(t.id).unwrap();
    assert_eq!(t.status, TaskStatus::Validation);
}

#[test]
fn advance_non_in_progress_errors() {
    let db = setup();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let runner = Runner::new(&db);
    let result = runner.advance(t.id);
    assert!(result.is_err());
}

#[test]
fn complete_marks_done() {
    let db = setup();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let runner = Runner::new(&db);
    let done = runner.complete(t.id).unwrap();
    assert_eq!(done.status, TaskStatus::Done);
    assert!(done.completed_at.is_some());
}

#[test]
fn fail_retries_then_cancels() {
    let db = setup();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let runner = Runner::new(&db);
    runner.start(t.id).unwrap();

    // First fail -> back to BACKLOG
    let t = runner.fail(t.id, "error 1").unwrap();
    assert_eq!(t.status, TaskStatus::Backlog);
    assert_eq!(t.retry_count, 1);
    assert!(t.substep.is_none());

    // Start again and fail twice more (max_retries=3)
    runner.start(t.id).unwrap();
    let t = runner.fail(t.id, "error 2").unwrap();
    assert_eq!(t.status, TaskStatus::Backlog);
    assert_eq!(t.retry_count, 2);

    runner.start(t.id).unwrap();
    let t = runner.fail(t.id, "error 3").unwrap();
    assert_eq!(t.status, TaskStatus::Cancelled);
    assert_eq!(t.retry_count, 3);
}

#[test]
fn block_and_unblock() {
    let db = setup();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let runner = Runner::new(&db);
    runner.start(t.id).unwrap();

    let blocked = runner.block(t.id, "need input").unwrap();
    assert_eq!(blocked.status, TaskStatus::Blocked);

    let unblocked = runner.unblock(t.id).unwrap();
    assert_eq!(unblocked.status, TaskStatus::InProgress);
}

#[test]
fn substep_label_formats() {
    let db = setup();
    let t = db.add(TaskCreate::new("Build auth")).unwrap();
    assert_eq!(substep_label(&t), "Queued: Build auth");

    let runner = Runner::new(&db);
    let t = runner.start(t.id).unwrap();
    assert_eq!(substep_label(&t), "PLANNING: Build auth [1/5]");

    let t = runner.advance(t.id).unwrap();
    assert_eq!(substep_label(&t), "TESTING: Build auth [2/5]");

    let blocked = runner.block(t.id, "waiting for API").unwrap();
    assert_eq!(substep_label(&blocked), "BLOCKED: Build auth -- waiting for API");

    let done = runner.complete(t.id).unwrap();
    assert_eq!(substep_label(&done), "Done: Build auth");
}
