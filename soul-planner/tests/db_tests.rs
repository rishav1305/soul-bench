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
    db.init().unwrap();
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
    let t2 = db
        .add(TaskCreate {
            depends_on: vec![t1.id],
            ..TaskCreate::new("Second")
        })
        .unwrap();
    assert_eq!(t2.depends_on, vec![t1.id]);
}

#[test]
fn get_returns_none_for_missing() {
    let db = TaskDB::memory();
    db.init().unwrap();
    assert!(db.get(999).unwrap().is_none());
}

#[test]
fn list_all_and_by_status() {
    let db = TaskDB::memory();
    db.init().unwrap();
    db.add(TaskCreate::new("A")).unwrap();
    db.add(TaskCreate::new("B")).unwrap();
    assert_eq!(db.list(None).unwrap().len(), 2);
    assert_eq!(db.list(Some(TaskStatus::Backlog)).unwrap().len(), 2);
    assert_eq!(db.list(Some(TaskStatus::Done)).unwrap().len(), 0);
}

#[test]
fn update_status_sets_started_at() {
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
    assert!(updated.completed_at.is_some());
}

#[test]
fn block_and_unblock() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    db.update_status(t.id, TaskStatus::InProgress).unwrap();
    let blocked = db.block(t.id, "waiting").unwrap();
    assert_eq!(blocked.status, TaskStatus::Blocked);
    assert_eq!(blocked.blocker.as_deref(), Some("waiting"));
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
fn check_deps_met() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t1 = db.add(TaskCreate::new("A")).unwrap();
    let t2 = db
        .add(TaskCreate {
            depends_on: vec![t1.id],
            ..TaskCreate::new("B")
        })
        .unwrap();
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
    })
    .unwrap();
    db.add(TaskCreate {
        priority: Priority::Critical,
        ..TaskCreate::new("Critical")
    })
    .unwrap();
    let next = db.next_ready().unwrap().unwrap();
    assert_eq!(next.title, "Critical");
}

#[test]
fn next_ready_skips_blocked_deps() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t1 = db.add(TaskCreate::new("Dep")).unwrap();
    // Move Dep to in_progress so it is no longer in the backlog pool.
    db.update_status(t1.id, TaskStatus::InProgress).unwrap();
    db.add(TaskCreate {
        depends_on: vec![t1.id],
        ..TaskCreate::new("Blocked")
    })
    .unwrap();
    db.add(TaskCreate::new("Ready")).unwrap();
    let next = db.next_ready().unwrap().unwrap();
    assert_eq!(next.title, "Ready");
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
    let path_str = path.to_str().unwrap();
    {
        let db = TaskDB::new(path_str);
        db.init().unwrap();
        db.add(TaskCreate::new("Persistent")).unwrap();
    }
    {
        let db = TaskDB::new(path_str);
        db.init().unwrap();
        let tasks = db.list(None).unwrap();
        assert_eq!(tasks.len(), 1);
        assert_eq!(tasks[0].title, "Persistent");
    }
}

#[test]
fn set_output() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let updated = db.set_output(t.id, "result data").unwrap();
    assert_eq!(updated.output.as_deref(), Some("result data"));
}

#[test]
fn set_error() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    let updated = db.set_error(t.id, "something failed").unwrap();
    assert_eq!(updated.error.as_deref(), Some("something failed"));
}

#[test]
fn increment_retry() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let t = db.add(TaskCreate::new("Test")).unwrap();
    assert_eq!(t.retry_count, 0);
    let count = db.increment_retry(t.id).unwrap();
    assert_eq!(count, 1);
    let count = db.increment_retry(t.id).unwrap();
    assert_eq!(count, 2);
    let t = db.get(t.id).unwrap().unwrap();
    assert_eq!(t.retry_count, 2);
}
