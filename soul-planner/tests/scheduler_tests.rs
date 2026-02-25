use soul_planner::scheduler::*;
use soul_planner::db::TaskDB;
use soul_planner::models::*;
use chrono::{Datelike, NaiveDate};

const PLANNER_CONTENT: &str = r#"# Daily Planner

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

### Evening Review
- [ ] Review notes

---

## Day 2 -- Sun Feb 23

### Block 1: BUILD (9am-1pm)
- [ ] Day 2 build task
"#;

#[test]
fn parse_extracts_uncompleted_tasks() {
    let date = NaiveDate::from_ymd_opt(2026, 2, 22).unwrap();
    let tasks = parse_planner(PLANNER_CONTENT, date, None);
    let titles: Vec<&str> = tasks.iter().map(|t| t.title.as_str()).collect();
    assert!(titles.contains(&"Uncompleted build task"));
    assert!(titles.contains(&"Explore task A"));
    assert!(titles.contains(&"Explore task B"));
    assert!(titles.contains(&"Write post"));
    assert!(titles.contains(&"Check job board"));
    // Should NOT contain completed, skipped, or blocked
    assert!(!titles.contains(&"Completed task"));
    assert!(!titles.contains(&"Skipped task"));
    assert!(!titles.contains(&"Blocked post"));
    // Should NOT contain Evening Review tasks (not in a Block section)
    assert!(!titles.contains(&"Review notes"));
}

#[test]
fn parse_block_filter() {
    let date = NaiveDate::from_ymd_opt(2026, 2, 22).unwrap();
    let tasks = parse_planner(PLANNER_CONTENT, date, Some(1));
    assert_eq!(tasks.len(), 1);
    assert_eq!(tasks[0].title, "Uncompleted build task");
    assert_eq!(tasks[0].block, 1);
}

#[test]
fn parse_priority_mapping() {
    let date = NaiveDate::from_ymd_opt(2026, 2, 22).unwrap();
    let tasks = parse_planner(PLANNER_CONTENT, date, None);
    let build_task = tasks.iter().find(|t| t.title == "Uncompleted build task").unwrap();
    assert_eq!(build_task.priority, Priority::High); // Block 1 = HIGH
    let explore_task = tasks.iter().find(|t| t.title == "Explore task A").unwrap();
    assert_eq!(explore_task.priority, Priority::Normal); // Block 2 = NORMAL
    let scout_task = tasks.iter().find(|t| t.title == "Check job board").unwrap();
    assert_eq!(scout_task.priority, Priority::Low); // Block 4 = LOW
}

#[test]
fn parse_wrong_date_returns_empty() {
    let date = NaiveDate::from_ymd_opt(2026, 3, 15).unwrap();
    let tasks = parse_planner(PLANNER_CONTENT, date, None);
    assert!(tasks.is_empty());
}

#[test]
fn parse_day2_only() {
    let date = NaiveDate::from_ymd_opt(2026, 2, 23).unwrap();
    let tasks = parse_planner(PLANNER_CONTENT, date, None);
    assert_eq!(tasks.len(), 1);
    assert_eq!(tasks[0].title, "Day 2 build task");
}

#[test]
fn schedule_creates_tasks() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let date = NaiveDate::from_ymd_opt(2026, 2, 22).unwrap();
    let ids = schedule_tasks_from_content(&db, PLANNER_CONTENT, date, None).unwrap();
    assert_eq!(ids.len(), 5);
    let tasks = db.list(None).unwrap();
    assert_eq!(tasks.len(), 5);
}

#[test]
fn schedule_skips_duplicates() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let date = NaiveDate::from_ymd_opt(2026, 2, 22).unwrap();
    let ids1 = schedule_tasks_from_content(&db, PLANNER_CONTENT, date, None).unwrap();
    assert_eq!(ids1.len(), 5);
    // Second call should skip all (duplicates)
    let ids2 = schedule_tasks_from_content(&db, PLANNER_CONTENT, date, None).unwrap();
    assert_eq!(ids2.len(), 0);
    assert_eq!(db.list(None).unwrap().len(), 5);
}

#[test]
fn parse_date_from_header_works() {
    // Test the date parsing function directly
    let header = "## Day 2 -- Sun Feb 23";
    let date = parse_date_from_header(header).unwrap();
    assert_eq!(date.month(), 2);
    assert_eq!(date.day(), 23);
}

#[test]
fn parse_date_from_header_returns_none_for_invalid() {
    assert!(parse_date_from_header("not a header").is_none());
    assert!(parse_date_from_header("## Day 2 -- no date").is_none());
}

#[test]
fn extract_block_number_works() {
    assert_eq!(extract_block_number("### Block 1: BUILD (9am-1pm)"), Some(1));
    assert_eq!(extract_block_number("### Block 2: EXPLORE (2pm-6pm)"), Some(2));
    assert_eq!(extract_block_number("### Block 3: SOCIAL (7pm-9pm)"), Some(3));
    assert_eq!(extract_block_number("### Block 4: SCOUT (9pm-11pm)"), Some(4));
    assert_eq!(extract_block_number("### Evening Review"), None);
    assert_eq!(extract_block_number("not a block header"), None);
}

#[test]
fn schedule_sets_source_description() {
    let db = TaskDB::memory();
    db.init().unwrap();
    let date = NaiveDate::from_ymd_opt(2026, 2, 22).unwrap();
    schedule_tasks_from_content(&db, PLANNER_CONTENT, date, None).unwrap();
    let tasks = db.list(None).unwrap();
    let build = tasks.iter().find(|t| t.title == "Uncompleted build task").unwrap();
    assert!(build.description.contains("Block 1"));
}
