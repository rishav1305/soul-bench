/// Daily planner parser and task scheduler for soul-planner.
///
/// Reads ~/soul/docs/daily-planner.md, finds today's date section,
/// extracts uncompleted tasks from specified blocks, and queues them
/// into the soul-planner backlog.

use regex::Regex;

use crate::db::{Result, TaskDB};
use crate::models::{Priority, TaskCreate};

// ---------------------------------------------------------------------------
// Block-to-priority mapping
// ---------------------------------------------------------------------------

/// Map block number to priority.
/// Block 1 (BUILD) = High, Block 2 (EXPLORE) = Normal,
/// Block 3 (SOCIAL) = Normal, Block 4 (SCOUT) = Low.
fn block_priority(block: u8) -> Priority {
    match block {
        1 => Priority::High,
        2 => Priority::Normal,
        3 => Priority::Normal,
        4 => Priority::Low,
        _ => Priority::Normal,
    }
}

// ---------------------------------------------------------------------------
// Month name mapping
// ---------------------------------------------------------------------------

fn month_number(name: &str) -> Option<u32> {
    match name.to_lowercase().as_str() {
        "jan" | "january" => Some(1),
        "feb" | "february" => Some(2),
        "mar" | "march" => Some(3),
        "apr" | "april" => Some(4),
        "may" => Some(5),
        "jun" | "june" => Some(6),
        "jul" | "july" => Some(7),
        "aug" | "august" => Some(8),
        "sep" | "september" => Some(9),
        "oct" | "october" => Some(10),
        "nov" | "november" => Some(11),
        "dec" | "december" => Some(12),
        _ => None,
    }
}

// ---------------------------------------------------------------------------
// Header parsers
// ---------------------------------------------------------------------------

/// Parse a date from a day header like "Day 2 -- Sun Feb 23".
///
/// Uses the current year since daily-planner.md does not include the year.
pub fn parse_date_from_header(header: &str) -> Option<chrono::NaiveDate> {
    let re = Regex::new(
        r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\w+)\s+(\d+)"
    ).ok()?;
    let caps = re.captures(header)?;
    let month_str = &caps[1];
    let day_num: u32 = caps[2].parse().ok()?;
    let month_abbr = &month_str.to_lowercase()[..3.min(month_str.len())];
    let month_num = month_number(month_abbr)?;
    let year = chrono::Local::now().format("%Y").to_string().parse::<i32>().ok()?;
    chrono::NaiveDate::from_ymd_opt(year, month_num, day_num)
}

/// Extract block number from a header like "### Block 1: BUILD ...".
pub fn extract_block_number(header: &str) -> Option<u8> {
    let re = Regex::new(r"^###\s+Block\s+(\d+)").ok()?;
    let caps = re.captures(header)?;
    caps[1].parse().ok()
}

// ---------------------------------------------------------------------------
// PlannerTask
// ---------------------------------------------------------------------------

/// A parsed task from the daily planner.
#[derive(Debug, Clone)]
pub struct PlannerTask {
    pub title: String,
    pub block: u8,
    pub priority: Priority,
}

// ---------------------------------------------------------------------------
// parse_planner
// ---------------------------------------------------------------------------

/// Parse daily planner content and extract uncompleted tasks for a target date.
///
/// Behavior:
/// - Find `## Day N -- Weekday Month Date` section matching `target_date`
/// - Within that section, find `### Block N:` headers
/// - Extract `- [ ]` tasks (uncompleted only)
/// - Skip `[x]` (done), `[-]` (skipped), `[!]` (blocked)
/// - Stop at `---` (day separator)
/// - Apply `block_filter` if set
pub fn parse_planner(
    content: &str,
    target_date: chrono::NaiveDate,
    block_filter: Option<u8>,
) -> Vec<PlannerTask> {
    let task_re = Regex::new(r"^- \[ \] (.+)$").unwrap();
    let mut tasks = Vec::new();
    let mut in_target_day = false;
    let mut current_block: Option<u8> = None;

    for line in content.lines() {
        // Detect day headers: ## Day N -- Weekday Month Date
        if line.starts_with("## Day ") {
            let header_date = parse_date_from_header(line);
            in_target_day = header_date == Some(target_date);
            current_block = None;
            continue;
        }

        if !in_target_day {
            continue;
        }

        // Detect day separator (exit current day)
        if line.starts_with("---") {
            break;
        }

        // Detect block headers
        if line.starts_with("### Block ") {
            current_block = extract_block_number(line);
            continue;
        }

        // Non-block section headers (e.g., "### Evening Review") reset current_block
        if line.starts_with("### ") && !line.starts_with("### Block") {
            current_block = None;
            continue;
        }

        // Only process lines if we're inside a block
        let block = match current_block {
            Some(b) => b,
            None => continue,
        };

        // Apply block filter
        if let Some(filter) = block_filter {
            if block != filter {
                continue;
            }
        }

        // Extract uncompleted tasks: - [ ] task text
        let trimmed = line.trim();
        if let Some(caps) = task_re.captures(trimmed) {
            let title = caps[1].trim().to_string();
            tasks.push(PlannerTask {
                title,
                block,
                priority: block_priority(block),
            });
        }
    }

    tasks
}

// ---------------------------------------------------------------------------
// schedule_tasks_from_content
// ---------------------------------------------------------------------------

/// Parse planner content string and queue tasks to DB (skips duplicates).
///
/// This is the testable core of `schedule_tasks` -- accepts content as `&str`
/// rather than reading from a file.
pub fn schedule_tasks_from_content(
    db: &TaskDB,
    content: &str,
    target_date: chrono::NaiveDate,
    block_filter: Option<u8>,
) -> Result<Vec<i64>> {
    let parsed = parse_planner(content, target_date, block_filter);
    if parsed.is_empty() {
        return Ok(Vec::new());
    }

    // Build set of existing task titles for duplicate detection
    let existing = db.list(None)?;
    let mut existing_titles: std::collections::HashSet<String> =
        existing.into_iter().map(|t| t.title).collect();

    let mut created_ids = Vec::new();
    for item in &parsed {
        if existing_titles.contains(&item.title) {
            continue;
        }

        let create = TaskCreate {
            title: item.title.clone(),
            description: format!("From daily planner, Block {}", item.block),
            acceptance: String::new(),
            priority: item.priority,
            depends_on: Vec::new(),
        };
        let task = db.add(create)?;
        created_ids.push(task.id);
        existing_titles.insert(item.title.clone());
    }

    Ok(created_ids)
}

// ---------------------------------------------------------------------------
// schedule_tasks (file-based entry point)
// ---------------------------------------------------------------------------

/// Parse planner file and queue tasks to DB (skips duplicates).
///
/// Reads from `planner_path` (default `~/soul/docs/daily-planner.md`),
/// parses for `target_date` (default today), and creates tasks in the DB.
pub fn schedule_tasks(
    db: &TaskDB,
    planner_path: Option<&str>,
    target_date: Option<chrono::NaiveDate>,
    block_filter: Option<u8>,
) -> Result<Vec<i64>> {
    let default_path = dirs::home_dir()
        .map(|h| h.join("soul/docs/daily-planner.md"))
        .unwrap_or_else(|| std::path::PathBuf::from("docs/daily-planner.md"));
    let path = match planner_path {
        Some(p) => std::path::PathBuf::from(p),
        None => default_path,
    };

    if !path.exists() {
        return Err(format!("Planner file not found: {}", path.display()).into());
    }

    let content = std::fs::read_to_string(&path)?;
    let today = target_date.unwrap_or_else(|| chrono::Local::now().date_naive());

    schedule_tasks_from_content(db, &content, today, block_filter)
}
