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
fn task_status_all_values() {
    let all = TaskStatus::all_values();
    assert_eq!(all.len(), 6);
    assert!(all.contains(&TaskStatus::Backlog));
    assert!(all.contains(&TaskStatus::Cancelled));
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
    assert_eq!(Substep::Testing.next(), Some(Substep::Implementing));
    assert_eq!(Substep::Implementing.next(), Some(Substep::Reviewing));
    assert_eq!(Substep::Reviewing.next(), Some(Substep::Validating));
    assert_eq!(Substep::Validating.next(), None);
}

#[test]
fn substep_all_values() {
    let all = Substep::all_values();
    assert_eq!(all.len(), 5);
    assert_eq!(all[0], Substep::Planning);
    assert_eq!(all[4], Substep::Validating);
}

#[test]
fn priority_ordering() {
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

#[test]
fn priority_all_values() {
    let all = Priority::all_values();
    assert_eq!(all.len(), 4);
}

#[test]
fn task_create_new_defaults() {
    let tc = TaskCreate::new("Test");
    assert_eq!(tc.title, "Test");
    assert_eq!(tc.description, "");
    assert_eq!(tc.acceptance, "");
    assert_eq!(tc.priority, Priority::Normal);
    assert!(tc.depends_on.is_empty());
}
