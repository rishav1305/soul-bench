/// Substep state machine for task lifecycle management.
///
/// Sits between the DB layer and the CLI. Orchestrates state transitions
/// through the 5-substep pipeline: Planning -> Testing -> Implementing ->
/// Reviewing -> Validating, then into VALIDATION status for final review.

use crate::db::{Result, TaskDB};
use crate::models::{Substep, Task, TaskStatus};

// ---------------------------------------------------------------------------
// Runner
// ---------------------------------------------------------------------------

/// Orchestrates task state transitions through the substep pipeline.
pub struct Runner<'a> {
    db: &'a TaskDB,
}

impl<'a> Runner<'a> {
    /// Create a new runner backed by the given database.
    pub fn new(db: &'a TaskDB) -> Self {
        Self { db }
    }

    /// Start a task: move from BACKLOG to IN_PROGRESS with PLANNING substep.
    pub fn start(&self, task_id: i64) -> Result<Task> {
        self.db.update_status(task_id, TaskStatus::InProgress)?;
        self.db.set_substep(task_id, Substep::Planning)
    }

    /// Advance to the next substep. If already at the last substep
    /// (Validating), transition the task to VALIDATION status.
    ///
    /// Returns an error if the task is not IN_PROGRESS.
    pub fn advance(&self, task_id: i64) -> Result<Task> {
        let task = self
            .db
            .get(task_id)?
            .ok_or_else(|| format!("task {} not found", task_id))?;

        if task.status != TaskStatus::InProgress {
            return Err(format!(
                "cannot advance task {}: status is {} (expected in_progress)",
                task_id,
                task.status.as_str()
            )
            .into());
        }

        match task.substep {
            Some(substep) => match substep.next() {
                Some(next) => self.db.set_substep(task_id, next),
                None => {
                    // Past last substep -> move to VALIDATION
                    self.db.clear_substep(task_id)?;
                    self.db.update_status(task_id, TaskStatus::Validation)
                }
            },
            None => {
                // No substep set but IN_PROGRESS -- start from Planning
                self.db.set_substep(task_id, Substep::Planning)
            }
        }
    }

    /// Mark a task as DONE with a completed_at timestamp.
    pub fn complete(&self, task_id: i64) -> Result<Task> {
        self.db.update_status(task_id, TaskStatus::Done)
    }

    /// Record a failure. Increments retry_count and sets the error message.
    ///
    /// - If retry_count >= max_retries: cancel the task.
    /// - Otherwise: move back to BACKLOG and clear the substep.
    pub fn fail(&self, task_id: i64, error: &str) -> Result<Task> {
        let new_count = self.db.increment_retry(task_id)?;
        self.db.set_error(task_id, error)?;

        let task = self
            .db
            .get(task_id)?
            .ok_or_else(|| format!("task {} not found", task_id))?;

        if new_count >= task.max_retries {
            self.db.update_status(task_id, TaskStatus::Cancelled)
        } else {
            self.db.clear_substep(task_id)?;
            self.db.update_status(task_id, TaskStatus::Backlog)
        }
    }

    /// Block a task with a reason string.
    pub fn block(&self, task_id: i64, reason: &str) -> Result<Task> {
        self.db.block(task_id, reason)
    }

    /// Unblock a task -- set status back to IN_PROGRESS.
    pub fn unblock(&self, task_id: i64) -> Result<Task> {
        self.db.unblock(task_id)
    }
}

// ---------------------------------------------------------------------------
// Free functions
// ---------------------------------------------------------------------------

/// Format a human-readable status bar label for a task.
///
/// - BLOCKED: "BLOCKED: {title} -- {reason}"
/// - IN_PROGRESS with substep: "{SUBSTEP}: {title} [{index}/5]"
/// - VALIDATION: "Review: {title}"
/// - DONE: "Done: {title}"
/// - Default (Backlog, Cancelled, etc.): "Queued: {title}"
pub fn substep_label(task: &Task) -> String {
    match task.status {
        TaskStatus::Blocked => {
            let reason = task.blocker.as_deref().unwrap_or("unknown");
            format!("BLOCKED: {} -- {}", task.title, reason)
        }
        TaskStatus::InProgress => match task.substep {
            Some(substep) => {
                let label = substep.as_str().to_uppercase();
                format!("{}: {} [{}/5]", label, task.title, substep.index())
            }
            None => format!("Queued: {}", task.title),
        },
        TaskStatus::Validation => format!("Review: {}", task.title),
        TaskStatus::Done => format!("Done: {}", task.title),
        _ => format!("Queued: {}", task.title),
    }
}
