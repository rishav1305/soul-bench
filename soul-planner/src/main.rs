/// soul-planner CLI -- task queue and scheduler for Claude Code.
///
/// Provides 16 subcommands for managing a Kanban-style task queue
/// backed by SQLite. Designed to match the output format of the
/// original Python implementation.

use std::process;

use clap::{Parser, Subcommand};

use soul_planner::board::format_board;
use soul_planner::db::TaskDB;
use soul_planner::models::{Priority, Substep, TaskCreate, TaskStatus};
use soul_planner::runner::Runner;
use soul_planner::scheduler::schedule_tasks;

// ---------------------------------------------------------------------------
// CLI definition
// ---------------------------------------------------------------------------

#[derive(Parser)]
#[command(name = "soul-planner", about = "Task queue and scheduler for Claude Code.")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add a new task to BACKLOG
    Add {
        title: String,
        #[arg(long, default_value = "")]
        details: String,
        #[arg(long, default_value = "")]
        acceptance: String,
        #[arg(long, default_value = "normal")]
        priority: String,
        /// Comma-separated dependency task IDs
        #[arg(long, default_value = "")]
        depends_on: String,
    },
    /// List tasks, optionally filtered by status
    List {
        #[arg(long)]
        status: Option<String>,
    },
    /// Show Kanban board view
    Board,
    /// Show detailed task status
    Status {
        task_id: i64,
    },
    /// Cancel a task
    Cancel {
        task_id: i64,
    },
    /// Block a task with a reason
    Block {
        task_id: i64,
        reason: String,
    },
    /// Resume a blocked task
    Unblock {
        task_id: i64,
    },
    /// Mark a task as done
    Done {
        task_id: i64,
        #[arg(long)]
        output: Option<String>,
    },
    /// Store a background agent ID on a task
    #[command(name = "set-agent")]
    SetAgent {
        task_id: i64,
        agent_id: String,
    },
    /// Append text to a task's output field
    #[command(name = "append-output")]
    AppendOutput {
        task_id: i64,
        text: String,
    },
    /// Move a task to VALIDATION (ready for review)
    Validate {
        task_id: i64,
    },
    /// Move from BACKLOG to IN_PROGRESS with PLANNING substep
    Promote {
        task_id: i64,
    },
    /// Advance to the next substep
    Advance {
        task_id: i64,
    },
    /// Update current substep
    Substep {
        task_id: i64,
        step: String,
    },
    /// Parse daily planner and queue tasks
    Schedule {
        #[arg(long)]
        block: Option<u8>,
        #[arg(long)]
        planner: Option<String>,
    },
    /// Show next ready task (highest priority, deps met)
    Next,
}

// ---------------------------------------------------------------------------
// DB initialization
// ---------------------------------------------------------------------------

/// Resolve the database path from env or default.
fn db_path() -> String {
    if let Ok(path) = std::env::var("PLANNER_DB_PATH") {
        return path;
    }
    let home = dirs::home_dir().unwrap_or_else(|| std::path::PathBuf::from("."));
    home.join(".claude/soul-planner/tasks.db")
        .to_string_lossy()
        .into_owned()
}

/// Open (or create) the database and ensure schema is initialized.
fn open_db() -> TaskDB {
    let path = db_path();

    // Ensure parent directory exists for file-backed DBs.
    if let Some(parent) = std::path::Path::new(&path).parent() {
        if !parent.exists() {
            std::fs::create_dir_all(parent).unwrap_or_else(|e| {
                eprintln!("Failed to create directory {}: {}", parent.display(), e);
                process::exit(2);
            });
        }
    }

    let db = TaskDB::new(&path);
    if let Err(e) = db.init() {
        eprintln!("Failed to initialize database: {}", e);
        process::exit(2);
    }
    db
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/// Parse a comma-separated list of IDs into a Vec<i64>.
fn parse_dep_ids(s: &str) -> Vec<i64> {
    if s.is_empty() {
        return Vec::new();
    }
    s.split(',')
        .filter_map(|part| part.trim().parse::<i64>().ok())
        .collect()
}

/// Parse a priority string, printing valid options and exiting on error.
fn parse_priority(s: &str) -> Priority {
    match Priority::from_str(s) {
        Some(p) => p,
        None => {
            eprintln!(
                "Invalid priority: \"{}\". Valid options: critical, high, normal, low",
                s
            );
            process::exit(1);
        }
    }
}

/// Parse a status string, printing valid options and exiting on error.
fn parse_status(s: &str) -> TaskStatus {
    match TaskStatus::from_str(s) {
        Some(st) => st,
        None => {
            eprintln!(
                "Invalid status: \"{}\". Valid options: backlog, in_progress, blocked, validation, done, cancelled",
                s
            );
            process::exit(1);
        }
    }
}

/// Parse a substep string, printing valid options and exiting on error.
fn parse_substep(s: &str) -> Substep {
    match Substep::from_str(s) {
        Some(sub) => sub,
        None => {
            eprintln!(
                "Invalid substep: \"{}\". Valid options: planning, testing, implementing, reviewing, validating",
                s
            );
            process::exit(1);
        }
    }
}

/// Get a task or print error and exit.
fn require_task(db: &TaskDB, id: i64) -> soul_planner::models::Task {
    match db.get(id) {
        Ok(Some(task)) => task,
        Ok(None) => {
            eprintln!("Task #{} not found", id);
            process::exit(1);
        }
        Err(e) => {
            eprintln!("Database error: {}", e);
            process::exit(2);
        }
    }
}

/// Handle a DB result, printing error and exiting on failure.
fn handle_db<T>(result: soul_planner::db::Result<T>) -> T {
    match result {
        Ok(v) => v,
        Err(e) => {
            eprintln!("Database error: {}", e);
            process::exit(2);
        }
    }
}

// ---------------------------------------------------------------------------
// Command implementations
// ---------------------------------------------------------------------------

fn cmd_add(db: &TaskDB, title: String, details: String, acceptance: String, priority: String, depends_on: String) {
    let prio = parse_priority(&priority);
    let deps = parse_dep_ids(&depends_on);

    let create = TaskCreate {
        title: title.clone(),
        description: details,
        acceptance,
        priority: prio,
        depends_on: deps.clone(),
    };

    let task = handle_db(db.add(create));
    println!("Added task #{} to BACKLOG: \"{}\"", task.id, task.title);
    if prio != Priority::Normal {
        println!("  priority: {}", prio.as_str());
    }
    if !deps.is_empty() {
        let dep_strs: Vec<String> = deps.iter().map(|d| format!("#{}", d)).collect();
        println!("  depends on: {}", dep_strs.join(", "));
    }
}

fn cmd_list(db: &TaskDB, status: Option<String>) {
    let filter = status.map(|s| parse_status(&s));
    let tasks = handle_db(db.list(filter));

    if tasks.is_empty() {
        println!("No tasks found.");
        return;
    }

    for task in &tasks {
        let status_str = match task.substep {
            Some(substep) => format!("{} > {}", task.status.as_str(), substep.as_str()),
            None => task.status.as_str().to_string(),
        };
        println!(
            "  #{}  [{}]  {}  ({})",
            task.id,
            status_str,
            task.title,
            task.priority.as_str()
        );
    }
}

fn cmd_board(db: &TaskDB) {
    let board = handle_db(db.board());
    println!("{}", format_board(&board));
}

fn cmd_status(db: &TaskDB, task_id: i64) {
    let task = require_task(db, task_id);
    println!("Task #{}", task.id);
    println!("  title: {}", task.title);
    println!("  status: {}", task.status.as_str());
    if let Some(substep) = task.substep {
        println!("  substep: {} [{}/5]", substep.as_str(), substep.index());
    }
    println!("  priority: {}", task.priority.as_str());
    if !task.description.is_empty() {
        println!("  description: {}", task.description);
    }
    if !task.acceptance.is_empty() {
        println!("  acceptance: {}", task.acceptance);
    }
    println!("  source: {}", task.source);
    if let Some(ref blocker) = task.blocker {
        println!("  blocker: {}", blocker);
    }
    if let Some(ref output) = task.output {
        println!("  output: {}", output);
    }
    if let Some(ref error) = task.error {
        println!("  error: {}", error);
    }
    if let Some(ref agent_id) = task.agent_id {
        println!("  agent: {}", agent_id);
    }
    println!("  retries: {}/{}", task.retry_count, task.max_retries);
    println!("  created: {}", task.created_at);
    if let Some(ref started) = task.started_at {
        println!("  started: {}", started);
    }
    if let Some(ref completed) = task.completed_at {
        println!("  completed: {}", completed);
    }
    if !task.depends_on.is_empty() {
        let dep_strs: Vec<String> = task.depends_on.iter().map(|d| format!("#{}", d)).collect();
        println!("  depends on: {}", dep_strs.join(", "));
    }
}

fn cmd_cancel(db: &TaskDB, task_id: i64) {
    require_task(db, task_id);
    let task = handle_db(db.cancel(task_id));
    println!("Task #{} cancelled: \"{}\"", task.id, task.title);
}

fn cmd_block(db: &TaskDB, task_id: i64, reason: String) {
    require_task(db, task_id);
    let task = handle_db(db.block(task_id, &reason));
    println!("Task #{} blocked: \"{}\"", task.id, reason);
}

fn cmd_unblock(db: &TaskDB, task_id: i64) {
    require_task(db, task_id);
    let task = handle_db(db.unblock(task_id));
    println!("Task #{} unblocked, resumed to {}", task.id, task.status.as_str());
}

fn cmd_done(db: &TaskDB, task_id: i64, output: Option<String>) {
    require_task(db, task_id);
    if let Some(ref text) = output {
        handle_db(db.append_output(task_id, text));
    }
    let runner = Runner::new(db);
    let task = handle_db(runner.complete(task_id));
    println!("Task #{} done: \"{}\"", task.id, task.title);
}

fn cmd_set_agent(db: &TaskDB, task_id: i64, agent_id: String) {
    require_task(db, task_id);
    handle_db(db.set_agent(task_id, &agent_id));
    println!("Task #{} agent: {}", task_id, agent_id);
}

fn cmd_append_output(db: &TaskDB, task_id: i64, text: String) {
    require_task(db, task_id);
    let task = handle_db(db.append_output(task_id, &text));
    let output_len = task.output.as_ref().map_or(0, |o| o.len());
    println!("Task #{} output updated ({} chars)", task.id, output_len);
}

fn cmd_validate(db: &TaskDB, task_id: i64) {
    require_task(db, task_id);
    let task = handle_db(db.update_status(task_id, TaskStatus::Validation));
    println!("Task #{} moved to validation: \"{}\"", task.id, task.title);
}

fn cmd_promote(db: &TaskDB, task_id: i64) {
    require_task(db, task_id);
    let runner = Runner::new(db);
    let task = handle_db(runner.start(task_id));
    let substep = task.substep.unwrap_or(Substep::Planning);
    println!(
        "Task #{} started: \"{}\" [{} {}/5]",
        task.id,
        task.title,
        substep.as_str(),
        substep.index()
    );
}

fn cmd_advance(db: &TaskDB, task_id: i64) {
    require_task(db, task_id);
    let runner = Runner::new(db);
    let task = handle_db(runner.advance(task_id));
    if task.status == TaskStatus::Validation {
        println!("Task #{} moved to validation: \"{}\"", task.id, task.title);
    } else {
        let substep = task.substep.unwrap_or(Substep::Planning);
        println!("Task #{} advanced to: {}", task.id, substep.as_str());
    }
}

fn cmd_substep(db: &TaskDB, task_id: i64, step: String) {
    require_task(db, task_id);
    let substep = parse_substep(&step);
    handle_db(db.set_substep(task_id, substep));
    println!("Task #{} substep: {}", task_id, substep.as_str());
}

fn cmd_schedule(db: &TaskDB, block: Option<u8>, planner: Option<String>) {
    let result = schedule_tasks(db, planner.as_deref(), None, block);
    match result {
        Ok(ids) if ids.is_empty() => {
            println!("No new tasks to schedule.");
        }
        Ok(ids) => {
            let id_strs: Vec<String> = ids.iter().map(|id| format!("#{}", id)).collect();
            println!("Scheduled {} tasks: [{}]", ids.len(), id_strs.join(", "));
        }
        Err(e) => {
            eprintln!("Schedule error: {}", e);
            process::exit(2);
        }
    }
}

fn cmd_next(db: &TaskDB) {
    let task = handle_db(db.next_ready());
    match task {
        Some(t) => {
            println!(
                "Next: #{}  {}  ({})",
                t.id,
                t.title,
                t.priority.as_str()
            );
        }
        None => {
            println!("No ready tasks.");
        }
    }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

fn main() {
    let cli = Cli::parse();
    let db = open_db();

    match cli.command {
        Commands::Add { title, details, acceptance, priority, depends_on } => {
            cmd_add(&db, title, details, acceptance, priority, depends_on);
        }
        Commands::List { status } => cmd_list(&db, status),
        Commands::Board => cmd_board(&db),
        Commands::Status { task_id } => cmd_status(&db, task_id),
        Commands::Cancel { task_id } => cmd_cancel(&db, task_id),
        Commands::Block { task_id, reason } => cmd_block(&db, task_id, reason),
        Commands::Unblock { task_id } => cmd_unblock(&db, task_id),
        Commands::Done { task_id, output } => cmd_done(&db, task_id, output),
        Commands::SetAgent { task_id, agent_id } => cmd_set_agent(&db, task_id, agent_id),
        Commands::AppendOutput { task_id, text } => cmd_append_output(&db, task_id, text),
        Commands::Validate { task_id } => cmd_validate(&db, task_id),
        Commands::Promote { task_id } => cmd_promote(&db, task_id),
        Commands::Advance { task_id } => cmd_advance(&db, task_id),
        Commands::Substep { task_id, step } => cmd_substep(&db, task_id, step),
        Commands::Schedule { block, planner } => cmd_schedule(&db, block, planner),
        Commands::Next => cmd_next(&db),
    }
}
