/// SQLite wrapper for soul-planner task persistence.
///
/// Provides synchronous CRUD operations using rusqlite.
/// Memory DBs keep a single connection alive via RefCell;
/// file DBs open a fresh connection per operation.

use std::cell::RefCell;
use std::collections::HashMap;

use chrono::Utc;
use rusqlite::{params, Connection, Row};

use crate::models::{Priority, Substep, Task, TaskCreate, TaskStatus};

// ---------------------------------------------------------------------------
// Result alias
// ---------------------------------------------------------------------------

pub type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

// ---------------------------------------------------------------------------
// Schema
// ---------------------------------------------------------------------------

const SCHEMA: &str = r#"
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

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_deps_task ON task_dependencies(task_id);
CREATE INDEX IF NOT EXISTS idx_deps_dep ON task_dependencies(depends_on);
"#;

// ---------------------------------------------------------------------------
// Priority sort weight for SQL ORDER BY
// ---------------------------------------------------------------------------

/// Map priority string to a numeric weight for SQL sorting.
/// Critical = 0 (highest) through Low = 3 (lowest).
fn priority_weight_sql() -> &'static str {
    "CASE priority \
     WHEN 'critical' THEN 0 \
     WHEN 'high' THEN 1 \
     WHEN 'normal' THEN 2 \
     WHEN 'low' THEN 3 \
     ELSE 4 END"
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/// Parse a single row into a Task (without depends_on -- caller fills that).
fn row_to_task(row: &Row) -> rusqlite::Result<Task> {
    let status_str: String = row.get("status")?;
    let substep_str: Option<String> = row.get("substep")?;
    let priority_str: String = row.get("priority")?;

    Ok(Task {
        id: row.get("id")?,
        title: row.get("title")?,
        description: row.get("description")?,
        acceptance: row.get("acceptance")?,
        status: TaskStatus::from_str(&status_str).unwrap_or(TaskStatus::Backlog),
        substep: substep_str.as_deref().and_then(Substep::from_str),
        priority: Priority::from_str(&priority_str).unwrap_or(Priority::Normal),
        source: row.get("source")?,
        blocker: row.get("blocker")?,
        output: row.get("output")?,
        error: row.get("error")?,
        agent_id: row.get("agent_id")?,
        retry_count: row.get("retry_count")?,
        max_retries: row.get("max_retries")?,
        created_at: row.get("created_at")?,
        started_at: row.get("started_at")?,
        completed_at: row.get("completed_at")?,
        depends_on: Vec::new(),
    })
}

/// Load dependency IDs for a given task.
fn get_deps(conn: &Connection, task_id: i64) -> rusqlite::Result<Vec<i64>> {
    let mut stmt = conn.prepare("SELECT depends_on FROM task_dependencies WHERE task_id = ?")?;
    let rows = stmt.query_map(params![task_id], |row| row.get(0))?;
    let mut deps = Vec::new();
    for dep in rows {
        deps.push(dep?);
    }
    Ok(deps)
}

/// Fetch a task by ID from an open connection (returns None if not found).
fn fetch_task(conn: &Connection, id: i64) -> Result<Option<Task>> {
    let mut stmt = conn.prepare("SELECT * FROM tasks WHERE id = ?")?;
    let mut rows = stmt.query_map(params![id], row_to_task)?;
    match rows.next() {
        Some(Ok(mut task)) => {
            task.depends_on = get_deps(conn, task.id)?;
            Ok(Some(task))
        }
        Some(Err(e)) => Err(e.into()),
        None => Ok(None),
    }
}

/// Require a task to exist -- return an error if not found.
fn require_task(conn: &Connection, id: i64) -> Result<Task> {
    fetch_task(conn, id)?
        .ok_or_else(|| format!("task {} not found", id).into())
}

/// Current UTC timestamp formatted for SQLite.
fn now() -> String {
    Utc::now().format("%Y-%m-%d %H:%M:%S").to_string()
}

// ---------------------------------------------------------------------------
// TaskDB
// ---------------------------------------------------------------------------

/// Storage backend for soul-planner tasks.
///
/// Two modes:
/// - **File**: stores a path, opens a new connection per operation.
/// - **Memory**: keeps a single `Connection` alive via `RefCell`.
pub struct TaskDB {
    inner: DbInner,
}

enum DbInner {
    File(String),
    Memory(RefCell<Connection>),
}

impl TaskDB {
    /// Create a file-backed database.
    pub fn new(path: &str) -> Self {
        Self {
            inner: DbInner::File(path.to_string()),
        }
    }

    /// Create an in-memory database (for testing).
    pub fn memory() -> Self {
        let conn = Connection::open_in_memory()
            .expect("failed to open in-memory SQLite database");
        Self {
            inner: DbInner::Memory(RefCell::new(conn)),
        }
    }

    // -- private helpers --

    /// Execute a closure with a borrowed connection.
    fn with_conn<F, T>(&self, f: F) -> Result<T>
    where
        F: FnOnce(&Connection) -> Result<T>,
    {
        match &self.inner {
            DbInner::File(path) => {
                let conn = Connection::open(path)?;
                conn.execute_batch("PRAGMA foreign_keys = ON;")?;
                f(&conn)
            }
            DbInner::Memory(cell) => {
                let conn = cell.borrow();
                f(&conn)
            }
        }
    }

    // -----------------------------------------------------------------------
    // Public API
    // -----------------------------------------------------------------------

    /// Create tables and indexes (idempotent).
    pub fn init(&self) -> Result<()> {
        self.with_conn(|conn| {
            conn.execute_batch("PRAGMA foreign_keys = ON;")?;
            conn.execute_batch(SCHEMA)?;
            Ok(())
        })
    }

    /// Insert a new task (with optional dependencies). Returns the created task.
    pub fn add(&self, create: TaskCreate) -> Result<Task> {
        self.with_conn(|conn| {
            let ts = now();
            conn.execute(
                "INSERT INTO tasks (title, description, acceptance, priority, created_at) \
                 VALUES (?1, ?2, ?3, ?4, ?5)",
                params![
                    create.title,
                    create.description,
                    create.acceptance,
                    create.priority.as_str(),
                    ts,
                ],
            )?;
            let id = conn.last_insert_rowid();

            for dep in &create.depends_on {
                conn.execute(
                    "INSERT INTO task_dependencies (task_id, depends_on) VALUES (?1, ?2)",
                    params![id, dep],
                )?;
            }

            require_task(conn, id)
        })
    }

    /// Fetch a task by ID (returns None if not found).
    pub fn get(&self, id: i64) -> Result<Option<Task>> {
        self.with_conn(|conn| fetch_task(conn, id))
    }

    /// List tasks, optionally filtered by status.
    pub fn list(&self, status: Option<TaskStatus>) -> Result<Vec<Task>> {
        self.with_conn(|conn| {
            let mut tasks = Vec::new();
            match status {
                Some(st) => {
                    let mut stmt =
                        conn.prepare("SELECT * FROM tasks WHERE status = ? ORDER BY id")?;
                    let rows = stmt.query_map(params![st.as_str()], row_to_task)?;
                    for row in rows {
                        let mut task = row?;
                        task.depends_on = get_deps(conn, task.id)?;
                        tasks.push(task);
                    }
                }
                None => {
                    let mut stmt = conn.prepare("SELECT * FROM tasks ORDER BY id")?;
                    let rows = stmt.query_map([], row_to_task)?;
                    for row in rows {
                        let mut task = row?;
                        task.depends_on = get_deps(conn, task.id)?;
                        tasks.push(task);
                    }
                }
            }
            Ok(tasks)
        })
    }

    /// Return all tasks grouped by status (Kanban board view).
    pub fn board(&self) -> Result<HashMap<TaskStatus, Vec<Task>>> {
        let all = self.list(None)?;
        let mut map: HashMap<TaskStatus, Vec<Task>> = HashMap::new();
        for task in all {
            map.entry(task.status).or_default().push(task);
        }
        Ok(map)
    }

    /// Update a task's status. Automatically sets `started_at` when moving to
    /// InProgress and `completed_at` when moving to Done or Cancelled.
    pub fn update_status(&self, id: i64, status: TaskStatus) -> Result<Task> {
        self.with_conn(|conn| {
            // Set timestamps based on target status
            match status {
                TaskStatus::InProgress => {
                    conn.execute(
                        "UPDATE tasks SET status = ?1, started_at = ?2 WHERE id = ?3",
                        params![status.as_str(), now(), id],
                    )?;
                }
                TaskStatus::Done | TaskStatus::Cancelled => {
                    conn.execute(
                        "UPDATE tasks SET status = ?1, completed_at = ?2 WHERE id = ?3",
                        params![status.as_str(), now(), id],
                    )?;
                }
                _ => {
                    conn.execute(
                        "UPDATE tasks SET status = ?1 WHERE id = ?2",
                        params![status.as_str(), id],
                    )?;
                }
            }
            require_task(conn, id)
        })
    }

    /// Set the current substep for a task.
    pub fn set_substep(&self, id: i64, substep: Substep) -> Result<Task> {
        self.with_conn(|conn| {
            conn.execute(
                "UPDATE tasks SET substep = ?1 WHERE id = ?2",
                params![substep.as_str(), id],
            )?;
            require_task(conn, id)
        })
    }

    /// Clear the substep field (set to NULL).
    pub fn clear_substep(&self, id: i64) -> Result<Task> {
        self.with_conn(|conn| {
            conn.execute(
                "UPDATE tasks SET substep = NULL WHERE id = ?1",
                params![id],
            )?;
            require_task(conn, id)
        })
    }

    /// Block a task with a reason string.
    pub fn block(&self, id: i64, reason: &str) -> Result<Task> {
        self.with_conn(|conn| {
            conn.execute(
                "UPDATE tasks SET status = 'blocked', blocker = ?1 WHERE id = ?2",
                params![reason, id],
            )?;
            require_task(conn, id)
        })
    }

    /// Unblock a task -- set status back to in_progress and clear blocker.
    pub fn unblock(&self, id: i64) -> Result<Task> {
        self.with_conn(|conn| {
            conn.execute(
                "UPDATE tasks SET status = 'in_progress', blocker = NULL WHERE id = ?1",
                params![id],
            )?;
            require_task(conn, id)
        })
    }

    /// Cancel a task (shortcut for update_status with Cancelled).
    pub fn cancel(&self, id: i64) -> Result<Task> {
        self.update_status(id, TaskStatus::Cancelled)
    }

    /// Check whether all dependencies for a task are in Done status.
    /// Returns true if the task has no dependencies.
    pub fn check_deps_met(&self, id: i64) -> Result<bool> {
        self.with_conn(|conn| {
            let count: i64 = conn.query_row(
                "SELECT COUNT(*) FROM task_dependencies td \
                 JOIN tasks t ON td.depends_on = t.id \
                 WHERE td.task_id = ?1 AND t.status != 'done'",
                params![id],
                |row| row.get(0),
            )?;
            Ok(count == 0)
        })
    }

    /// Find the next ready task: highest-priority backlog task with all
    /// dependencies satisfied (all deps in Done status).
    pub fn next_ready(&self) -> Result<Option<Task>> {
        self.with_conn(|conn| {
            let sql = format!(
                "SELECT * FROM tasks \
                 WHERE status = 'backlog' \
                   AND id NOT IN ( \
                       SELECT td.task_id FROM task_dependencies td \
                       JOIN tasks dep ON td.depends_on = dep.id \
                       WHERE dep.status != 'done' \
                   ) \
                 ORDER BY {}, id \
                 LIMIT 1",
                priority_weight_sql()
            );
            let mut stmt = conn.prepare(&sql)?;
            let mut rows = stmt.query_map([], row_to_task)?;
            match rows.next() {
                Some(Ok(mut task)) => {
                    task.depends_on = get_deps(conn, task.id)?;
                    Ok(Some(task))
                }
                Some(Err(e)) => Err(e.into()),
                None => Ok(None),
            }
        })
    }

    /// Append text to a task's output field with a `\n---\n` separator.
    pub fn append_output(&self, id: i64, text: &str) -> Result<Task> {
        self.with_conn(|conn| {
            // Read current output
            let current: Option<String> = conn.query_row(
                "SELECT output FROM tasks WHERE id = ?1",
                params![id],
                |row| row.get(0),
            )?;
            let new_output = match current {
                Some(existing) if !existing.is_empty() => {
                    format!("{}\n---\n{}", existing, text)
                }
                _ => text.to_string(),
            };
            conn.execute(
                "UPDATE tasks SET output = ?1 WHERE id = ?2",
                params![new_output, id],
            )?;
            require_task(conn, id)
        })
    }

    /// Set the agent_id for a task.
    pub fn set_agent(&self, id: i64, agent_id: &str) -> Result<Task> {
        self.with_conn(|conn| {
            conn.execute(
                "UPDATE tasks SET agent_id = ?1 WHERE id = ?2",
                params![agent_id, id],
            )?;
            require_task(conn, id)
        })
    }

    /// Directly set the output field (overwrite, not append).
    pub fn set_output(&self, id: i64, output: &str) -> Result<Task> {
        self.with_conn(|conn| {
            conn.execute(
                "UPDATE tasks SET output = ?1 WHERE id = ?2",
                params![output, id],
            )?;
            require_task(conn, id)
        })
    }

    /// Directly set the error field.
    pub fn set_error(&self, id: i64, error: &str) -> Result<Task> {
        self.with_conn(|conn| {
            conn.execute(
                "UPDATE tasks SET error = ?1 WHERE id = ?2",
                params![error, id],
            )?;
            require_task(conn, id)
        })
    }

    /// Increment retry_count and return the new value.
    pub fn increment_retry(&self, id: i64) -> Result<i32> {
        self.with_conn(|conn| {
            conn.execute(
                "UPDATE tasks SET retry_count = retry_count + 1 WHERE id = ?1",
                params![id],
            )?;
            let count: i32 = conn.query_row(
                "SELECT retry_count FROM tasks WHERE id = ?1",
                params![id],
                |row| row.get(0),
            )?;
            Ok(count)
        })
    }

    /// List table names from sqlite_master (for testing).
    pub fn table_names(&self) -> Vec<String> {
        self.with_conn(|conn| {
            let mut stmt = conn.prepare(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name",
            )?;
            let rows = stmt.query_map([], |row| row.get(0))?;
            let mut names = Vec::new();
            for name in rows {
                names.push(name?);
            }
            Ok(names)
        })
        .unwrap_or_default()
    }
}
