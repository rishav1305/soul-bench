/// Kanban board formatter for terminal display.
///
/// Formats tasks grouped by status into a readable board layout
/// matching the original Python implementation's output.

use std::collections::HashMap;

use crate::models::{Task, TaskStatus};

/// Status display order for the Kanban board.
const BOARD_ORDER: [TaskStatus; 6] = [
    TaskStatus::Backlog,
    TaskStatus::InProgress,
    TaskStatus::Blocked,
    TaskStatus::Validation,
    TaskStatus::Done,
    TaskStatus::Cancelled,
];

/// Display name for a status column header.
fn status_display(status: TaskStatus) -> &'static str {
    match status {
        TaskStatus::Backlog => "BACKLOG",
        TaskStatus::InProgress => "IN_PROGRESS",
        TaskStatus::Blocked => "BLOCKED",
        TaskStatus::Validation => "VALIDATION",
        TaskStatus::Done => "DONE",
        TaskStatus::Cancelled => "CANCELLED",
    }
}

/// Format a single task line: `  #ID  TITLE  (PRIORITY)` with optional ` > SUBSTEP`.
fn format_task_line(task: &Task) -> String {
    let base = format!(
        "  #{}  {}  ({})",
        task.id,
        task.title,
        task.priority.as_str()
    );
    match task.substep {
        Some(substep) => format!("{} > {}", base, substep.as_str()),
        None => base,
    }
}

/// Format a full Kanban board from a status-to-tasks map.
///
/// Output format:
/// ```text
/// BACKLOG (2)
/// ----------------------------------------
///   #1  Build auth module  (high)
///   #2  Write docs  (normal)
///
/// IN_PROGRESS (0)
/// ----------------------------------------
///   (empty)
/// ```
pub fn format_board(board: &HashMap<TaskStatus, Vec<Task>>) -> String {
    let mut sections = Vec::new();

    for status in &BOARD_ORDER {
        let tasks = board.get(status);
        let count = tasks.map_or(0, |v| v.len());
        let header = format!("{} ({})", status_display(*status), count);
        let separator = "-".repeat(40);

        let body = if count == 0 {
            "  (empty)".to_string()
        } else {
            tasks
                .unwrap()
                .iter()
                .map(format_task_line)
                .collect::<Vec<_>>()
                .join("\n")
        };

        sections.push(format!("{}\n{}\n{}", header, separator, body));
    }

    sections.join("\n\n")
}

// ---------------------------------------------------------------------------
// Unit tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use crate::models::{Priority, Substep};

    fn make_task(id: i64, title: &str, priority: Priority, substep: Option<Substep>) -> Task {
        Task {
            id,
            title: title.to_string(),
            description: String::new(),
            acceptance: String::new(),
            status: TaskStatus::Backlog,
            substep,
            priority,
            source: "manual".to_string(),
            blocker: None,
            output: None,
            error: None,
            agent_id: None,
            retry_count: 0,
            max_retries: 3,
            created_at: "2026-01-01 00:00:00".to_string(),
            started_at: None,
            completed_at: None,
            depends_on: Vec::new(),
        }
    }

    #[test]
    fn empty_board() {
        let board: HashMap<TaskStatus, Vec<Task>> = HashMap::new();
        let output = format_board(&board);
        assert!(output.contains("BACKLOG (0)"));
        assert!(output.contains("IN_PROGRESS (0)"));
        assert!(output.contains("BLOCKED (0)"));
        assert!(output.contains("VALIDATION (0)"));
        assert!(output.contains("DONE (0)"));
        assert!(output.contains("CANCELLED (0)"));
        // All sections should show (empty)
        assert_eq!(output.matches("(empty)").count(), 6);
    }

    #[test]
    fn board_with_tasks() {
        let mut board: HashMap<TaskStatus, Vec<Task>> = HashMap::new();
        board.insert(
            TaskStatus::Backlog,
            vec![
                make_task(1, "Build auth module", Priority::High, None),
                make_task(2, "Write docs", Priority::Normal, None),
            ],
        );
        let output = format_board(&board);
        assert!(output.contains("BACKLOG (2)"));
        assert!(output.contains("#1  Build auth module  (high)"));
        assert!(output.contains("#2  Write docs  (normal)"));
    }

    #[test]
    fn board_with_substep() {
        let mut board: HashMap<TaskStatus, Vec<Task>> = HashMap::new();
        board.insert(
            TaskStatus::InProgress,
            vec![make_task(
                3,
                "Fix login bug",
                Priority::Critical,
                Some(Substep::Testing),
            )],
        );
        let output = format_board(&board);
        assert!(output.contains("IN_PROGRESS (1)"));
        assert!(output.contains("#3  Fix login bug  (critical) > testing"));
    }

    #[test]
    fn board_section_order() {
        let board: HashMap<TaskStatus, Vec<Task>> = HashMap::new();
        let output = format_board(&board);
        let backlog_pos = output.find("BACKLOG").unwrap();
        let in_progress_pos = output.find("IN_PROGRESS").unwrap();
        let blocked_pos = output.find("BLOCKED").unwrap();
        let validation_pos = output.find("VALIDATION").unwrap();
        let done_pos = output.find("DONE").unwrap();
        let cancelled_pos = output.find("CANCELLED").unwrap();
        assert!(backlog_pos < in_progress_pos);
        assert!(in_progress_pos < blocked_pos);
        assert!(blocked_pos < validation_pos);
        assert!(validation_pos < done_pos);
        assert!(done_pos < cancelled_pos);
    }

    #[test]
    fn format_task_line_no_substep() {
        let task = make_task(5, "Test task", Priority::Low, None);
        let line = format_task_line(&task);
        assert_eq!(line, "  #5  Test task  (low)");
    }

    #[test]
    fn format_task_line_with_substep() {
        let task = make_task(10, "Impl task", Priority::High, Some(Substep::Implementing));
        let line = format_task_line(&task);
        assert_eq!(line, "  #10  Impl task  (high) > implementing");
    }
}
