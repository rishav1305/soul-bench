/// Enums and structs for soul-planner tasks.
///
/// Snake_case string representations match the SQLite schema
/// from the original Python implementation.

// ---------------------------------------------------------------------------
// TaskStatus
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TaskStatus {
    Backlog,
    InProgress,
    Blocked,
    Validation,
    Done,
    Cancelled,
}

impl TaskStatus {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "backlog" => Some(Self::Backlog),
            "in_progress" => Some(Self::InProgress),
            "blocked" => Some(Self::Blocked),
            "validation" => Some(Self::Validation),
            "done" => Some(Self::Done),
            "cancelled" => Some(Self::Cancelled),
            _ => None,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Backlog => "backlog",
            Self::InProgress => "in_progress",
            Self::Blocked => "blocked",
            Self::Validation => "validation",
            Self::Done => "done",
            Self::Cancelled => "cancelled",
        }
    }

    pub fn all_values() -> Vec<Self> {
        vec![
            Self::Backlog,
            Self::InProgress,
            Self::Blocked,
            Self::Validation,
            Self::Done,
            Self::Cancelled,
        ]
    }
}

// ---------------------------------------------------------------------------
// Substep
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Substep {
    Planning,
    Testing,
    Implementing,
    Reviewing,
    Validating,
}

impl Substep {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "planning" => Some(Self::Planning),
            "testing" => Some(Self::Testing),
            "implementing" => Some(Self::Implementing),
            "reviewing" => Some(Self::Reviewing),
            "validating" => Some(Self::Validating),
            _ => None,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Planning => "planning",
            Self::Testing => "testing",
            Self::Implementing => "implementing",
            Self::Reviewing => "reviewing",
            Self::Validating => "validating",
        }
    }

    pub fn all_values() -> Vec<Self> {
        vec![
            Self::Planning,
            Self::Testing,
            Self::Implementing,
            Self::Reviewing,
            Self::Validating,
        ]
    }

    /// 1-based position: Planning=1, Testing=2, ..., Validating=5.
    pub fn index(&self) -> usize {
        match self {
            Self::Planning => 1,
            Self::Testing => 2,
            Self::Implementing => 3,
            Self::Reviewing => 4,
            Self::Validating => 5,
        }
    }

    /// Returns the next substep in order, or `None` for Validating.
    pub fn next(&self) -> Option<Self> {
        match self {
            Self::Planning => Some(Self::Testing),
            Self::Testing => Some(Self::Implementing),
            Self::Implementing => Some(Self::Reviewing),
            Self::Reviewing => Some(Self::Validating),
            Self::Validating => None,
        }
    }
}

// ---------------------------------------------------------------------------
// Priority
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Priority {
    Critical,
    High,
    Normal,
    Low,
}

impl Priority {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "critical" => Some(Self::Critical),
            "high" => Some(Self::High),
            "normal" => Some(Self::Normal),
            "low" => Some(Self::Low),
            _ => None,
        }
    }

    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Critical => "critical",
            Self::High => "high",
            Self::Normal => "normal",
            Self::Low => "low",
        }
    }

    pub fn all_values() -> Vec<Self> {
        vec![Self::Critical, Self::High, Self::Normal, Self::Low]
    }

    /// Sort weight: Critical=0 (highest priority) through Low=3 (lowest).
    pub fn weight(&self) -> u8 {
        match self {
            Self::Critical => 0,
            Self::High => 1,
            Self::Normal => 2,
            Self::Low => 3,
        }
    }
}

// ---------------------------------------------------------------------------
// Task
// ---------------------------------------------------------------------------

#[derive(Debug, Clone)]
pub struct Task {
    pub id: i64,
    pub title: String,
    pub description: String,
    pub acceptance: String,
    pub status: TaskStatus,
    pub substep: Option<Substep>,
    pub priority: Priority,
    pub source: String,
    pub blocker: Option<String>,
    pub output: Option<String>,
    pub error: Option<String>,
    pub agent_id: Option<String>,
    pub retry_count: i32,
    pub max_retries: i32,
    pub created_at: String,
    pub started_at: Option<String>,
    pub completed_at: Option<String>,
    pub depends_on: Vec<i64>,
}

// ---------------------------------------------------------------------------
// TaskCreate
// ---------------------------------------------------------------------------

#[derive(Debug, Clone)]
pub struct TaskCreate {
    pub title: String,
    pub description: String,
    pub acceptance: String,
    pub priority: Priority,
    pub depends_on: Vec<i64>,
}

impl TaskCreate {
    /// Convenience constructor with sensible defaults.
    pub fn new(title: &str) -> Self {
        Self {
            title: title.to_string(),
            description: String::new(),
            acceptance: String::new(),
            priority: Priority::Normal,
            depends_on: Vec::new(),
        }
    }
}
