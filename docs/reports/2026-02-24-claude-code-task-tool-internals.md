# Claude Code Task Tool Internals — Research Findings

**Date:** 2026-02-24
**Block:** Block 2: EXPLORE — Claude Code Task tool internals
**Purpose:** Document how the Task tool works, how skills/agents interact with it, and what soul-planner needs for integration.

---

## 1. The Task Tool

The Task tool launches specialized agents (subprocesses) that autonomously handle complex tasks. Each agent runs in its own conversation context, with its own tool access, and can execute in foreground or background.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `description` | string | Yes | -- | Short (3-5 word) summary shown in UI. E.g., "Test background task lifecycle" |
| `prompt` | string | Yes | -- | Full instructions for the agent. This is the only context the agent gets (unless it has "access to current context"). |
| `subagent_type` | string | Yes | -- | Determines which agent type to use and what tools it has access to. |
| `run_in_background` | boolean | No | `false` | If `true`, returns immediately with an `agentId` and `output_file` path. Agent runs asynchronously. |
| `isolation` | enum | No | -- | Set to `"worktree"` to run the agent in a temporary git worktree (isolated copy of the repo). |
| `model` | enum | No | inherits parent | One of: `"sonnet"`, `"opus"`, `"haiku"`. Overrides the model for this agent. |
| `max_turns` | number | No | -- | Maximum agentic turns (API round-trips) before the agent stops. |
| `resume` | string | No | -- | Agent ID from a previous invocation. Resumes the agent with its full previous context preserved. |

### Available Subagent Types

Each subagent type has different tools available:

| subagent_type | Tools Available | Use Case |
|---------------|----------------|----------|
| `Bash` | Bash only | Git operations, command execution, terminal tasks |
| `general-purpose` | All tools | Researching complex questions, multi-step tasks |
| `Explore` | All except Task, ExitPlanMode, Edit, Write, NotebookEdit | **Read-only** codebase exploration — find files, search code, answer questions |
| `Plan` | All except Task, ExitPlanMode, Edit, Write, NotebookEdit | Design implementation plans, identify critical files, consider trade-offs |
| `code-simplifier:code-simplifier` | All tools | Simplify/refine code for clarity while preserving functionality |
| `superpowers:code-reviewer` | All tools | Review completed project steps against original plan |
| `pr-review-toolkit:comment-analyzer` | All tools | Analyze code comments for accuracy and completeness |
| `pr-review-toolkit:type-design-analyzer` | All tools | Expert analysis of type design (encapsulation, invariants) |
| `pr-review-toolkit:code-reviewer` | All tools | Review code for style guide adherence |
| `pr-review-toolkit:silent-failure-hunter` | All tools | Identify silent failures, inadequate error handling |
| `pr-review-toolkit:pr-test-analyzer` | All tools | Review test coverage quality and completeness |
| `pr-review-toolkit:code-simplifier` | All tools | Simplify recently modified code |
| `feature-dev:code-architect` | Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch | Design feature architectures from existing patterns |
| `feature-dev:code-reviewer` | Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch | Review code for bugs, security, quality |
| `feature-dev:code-explorer` | Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch | Deeply analyze existing features, trace execution paths |
| `hookify:conversation-analyzer` | Read, Grep | Analyze conversations to find behaviors worth preventing |
| `daily-planner` | Read, Edit, Glob | Read/update daily planner tasks |
| `social-writer` | Read, Write, Glob | Draft social media content (LinkedIn, Twitter, blog) |
| `outreach-copywriter` | Read, Write, Glob | Draft outreach/follow-up emails |
| `outreach-researcher` | WebFetch, WebSearch, Read, Write | Research contacts, companies, topics |
| `knowledge-agent` | Read, Write, Edit, Glob, Grep, WebFetch | Ingest documents, consolidate knowledge |
| `sprint-manager` | Read, Edit, Glob | Manage weekly sprints and milestones |
| `system-agent` | Bash, Read, Glob, Grep | System health checks, disk/memory/Docker diagnostics |
| `task-runner` | Bash, Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate | **Background task execution** — pick up queued tasks, execute through dev workflow |
| `project-status` | Read, Glob, Grep, Bash | Check progress across all projects |
| `github-publisher` | Bash, Read, Glob, Grep | Push projects to GitHub |
| `proposal-writer` | Read, Write, Glob, Grep | Draft consulting proposals |
| `linkedin-updater` | All tools | Update LinkedIn profile via Chrome automation |
| `vaultwarden` | All tools | Read/write secrets from Vaultwarden vault |
| `statusline-setup` | Read, Edit | Configure Claude Code status line |

**Key insight:** The `task-runner` subagent type already exists and has access to `TaskCreate` and `TaskUpdate` tools. This is the primary integration point for soul-planner.

---

## 2. Background Execution Lifecycle

### Spawning

```
Task(prompt="...", subagent_type="Explore", run_in_background=true, model="haiku")
```

**Returns immediately:**
```
agentId: a5d6c67f18564801a
output_file: /tmp/claude-1000/-home-rishav-soul/tasks/a5d6c67f18564801a.output
```

### Checking Progress

Two ways to check on a background task:

1. **TaskOutput tool** (blocking or non-blocking):
   ```
   TaskOutput(task_id="a5d6c67f18564801a", block=false, timeout=5000)
   ```
   Returns: `{ status: "running" | "completed", output: "..." }`

2. **Read the output file directly:**
   ```
   Read(file_path="/tmp/claude-1000/-home-rishav-soul/tasks/a5d6c67f18564801a.output")
   ```
   Returns: JSONL transcript (one JSON object per line)

### Output File Format (JSONL)

Each line is a JSON object. Message types observed:

| type | role | Contains |
|------|------|----------|
| `user` | user | The original prompt, or tool results returned to the agent |
| `assistant` | assistant | Agent's response (text or tool_use blocks) |
| `progress` | -- | Hook execution progress (PreToolUse, PostToolUse) |

Key fields in each line:
- `agentId`: The task's unique ID
- `slug`: Human-readable random name (e.g., "snappy-riding-reef")
- `sessionId`: Parent session ID (same as the spawning session)
- `isSidechain`: Always `true` for background tasks
- `message.model`: Which Claude model was used
- `message.usage`: Token counts (input, cache_creation, cache_read, output)

### Completion Notification

When a background task completes, the parent session receives a `system-reminder` with:
```
<task-notification>
  <task-id>a5d6c67f18564801a</task-id>
  <status>completed</status>
  <summary>Agent "Test background task lifecycle" completed</summary>
  <result>... the agent's final text output ...</result>
  <usage>
    <total_tokens>19125</total_tokens>
    <tool_uses>1</tool_uses>
    <duration_ms>5325</duration_ms>
  </usage>
</task-notification>
```

### Stopping

```
TaskStop(task_id="a5d6c67f18564801a")
```

### Resuming

```
Task(prompt="continue with X", resume="a5d6c67f18564801a", subagent_type="Explore")
```

The agent continues with its full previous context preserved — all prior messages, tool calls, and results are still in its conversation.

---

## 3. How Skills, Agents, and Task Tool Interact

### Architecture

```
User Message
    |
    v
Claude Code Session (main conversation)
    |
    ├── Skill Tool ──> Loads skill content into CURRENT session
    |                   (no subprocess, runs inline)
    |
    ├── Task Tool ──> Spawns SEPARATE agent subprocess
    |                  (own context, own tools, own model)
    |                  Can run in foreground (blocking) or background
    |
    ├── TaskCreate/TaskUpdate/TaskList ──> Claude Code's built-in task UI
    |                                      (the progress tracker shown to user)
    |
    └── Direct tool calls (Read, Write, Bash, etc.)
```

### Skills (`.claude/skills/`)

- **Invoked via:** `Skill` tool or user typing `/skill-name`
- **Execution:** Inline in the current conversation. The skill's markdown content is loaded and presented to the assistant as instructions.
- **No subprocess:** Skills run in the main session — they don't spawn agents.
- **Registration:** Defined as markdown files in `.claude/skills/<name>/SKILL.md` or via plugins.
- **Tool access:** Whatever tools the main session has.

**Key insight for soul-planner:** The `/planner` commands are already defined as skills. When the user runs `/planner add "task"`, the skill content is loaded into the current session, and the assistant executes the instructions (which include running CLI commands via Bash).

### Agents (`.claude/agents/`)

- **Invoked via:** Task tool with matching `subagent_type`
- **Execution:** Separate subprocess with its own conversation context.
- **Registration:** Defined as markdown files in `.claude/agents/<name>.md`. The agent description in the markdown becomes the system prompt.
- **Tool access:** Specified in the agent definition (e.g., `Tools: Bash, Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate`).

**Key insight for soul-planner:** The `task-runner` agent is already defined at `~/soul/soul-planner/agents/task-runner.md`. It's designed to be spawned with `run_in_background: true` and has access to `TaskCreate` and `TaskUpdate` for syncing with the Claude Code task UI.

### Claude Code Task UI (TaskCreate/TaskUpdate/TaskList)

These are **not** the same as soul-planner tasks. They are Claude Code's built-in progress tracker:

- `TaskCreate(subject="...", description="...", activeForm="...")` — shows a task in the user's UI
- `TaskUpdate(taskId="1", status="in_progress")` — updates status
- `TaskList()` — returns all tasks

**Important distinction:**
- **Soul-planner tasks**: Persist in SQLite (`~/.claude/soul-planner/tasks.db`), have Kanban states, dependencies, substeps, retry logic
- **Claude Code tasks**: Ephemeral UI elements, exist only for the current session, no persistence across sessions

**Integration pattern:** Soul-planner should sync its task state TO Claude Code's task UI using `TaskCreate`/`TaskUpdate`. Not the other way around.

---

## 4. Practical Findings from Experimentation

### Background Task Timing

| Metric | Observed Value |
|--------|---------------|
| Spawn overhead | ~2s (from call to first agent response) |
| Haiku model for simple read task | 5.3s total (1 tool use, 19k tokens) |
| Output file appears | Immediately (first line written on spawn) |
| Completion notification | Delivered as system-reminder in next user turn |

### Token Usage in Background Tasks

From the test task (Haiku, read 1 file, summarize):
- Cache creation: 17,913 tokens (first turn) + 1,198 tokens (second turn)
- Cache read: 17,913 tokens (second turn reused first turn's cache)
- Output tokens: 8 total (very efficient for Haiku)
- Total: 19,125 tokens

**Implication for soul-planner:** Background tasks using Haiku are cheap. A soul-planner task that reads files and generates code using Sonnet would cost more but is still reasonable for automated background execution.

### Hooks Run in Subagents

The output file shows `PreToolUse` and `PostToolUse` hooks running inside the background agent. This means:
- Hookify rules apply to background agents
- Soul-planner's security checks would work in background execution
- Any pre/post hooks configured in the parent session also apply to subagents

---

## 5. Integration Recommendations for soul-planner

### Current State (what exists)

Soul-planner already has:
1. `soul_planner/db.py` — async SQLite task CRUD (67+ tests)
2. `soul_planner/models.py` — Pydantic models with Kanban states
3. `soul_planner/runner.py` — TaskRunner state machine (5 substeps)
4. `soul_planner/scheduler.py` — Daily planner parser
5. `soul_planner/cli.py` — Full CLI (14 commands)
6. `commands/planner.md` — `/planner` skill (manages tasks)
7. `commands/planner-run.md` — `/planner-run` skill (executes a task through substeps)
8. `commands/planner-schedule.md` — `/planner-schedule` skill (queues from daily planner)
9. `agents/task-runner.md` — Background agent definition
10. `skills/task-awareness/` — Session start sync

### What's Missing (integration gaps)

#### Gap 1: Background Execution Loop

The `task-runner` agent exists but nothing spawns it. Need:

```python
# In /planner-run command or a new /planner-execute command:
Task(
    description="Execute soul-planner task #{id}",
    prompt="Pick up task #{id} from soul-planner queue and execute it through all 5 substeps...",
    subagent_type="task-runner",
    run_in_background=True,
    model="sonnet"
)
```

**Recommendation:** Add a `/planner-run-bg` command that spawns the `task-runner` agent in the background for a specific task. The agent reads the task from SQLite, executes it, and updates the DB.

#### Gap 2: Claude Code Task UI Sync

The commands reference `TaskCreate`/`TaskUpdate` but the wiring isn't consistent. Need:

1. After `planner add`: Call `TaskCreate(subject=title, activeForm="Queued: {title}")`
2. After `planner-run` picks a task: Call `TaskUpdate(status="in_progress", activeForm="PLANNING: {title} [1/5]")`
3. After each substep advance: Call `TaskUpdate(activeForm="TESTING: {title} [2/5]")`
4. On completion: Call `TaskUpdate(status="completed")`
5. On failure: Keep `in_progress` with error description

**Key constraint:** Claude Code task IDs are ephemeral (per-session). Soul-planner task IDs are persistent (SQLite). The mapping doesn't persist across sessions, so `task-awareness` skill must re-sync on each session start.

#### Gap 3: Output Capture

When a `task-runner` background agent completes:
1. The output file contains the full JSONL transcript
2. The completion notification contains the final text output
3. Soul-planner should capture this output and store it in the task's `output` field

**Recommended approach:**
- The `task-runner` agent should call the CLI to update the task: `python -m soul_planner done {id} --output "result text"`
- Or update SQLite directly via the CLI before exiting

#### Gap 4: Resume/Retry

If a background task fails:
1. The agent can be resumed with `Task(resume="agentId", ...)` — but this requires knowing the agentId
2. Soul-planner should store the `agentId` in the task record (new field or use `output` field)
3. On retry, pass the stored agentId to resume the agent with full context

### Recommended Next Steps (prioritized)

1. **Wire `/planner-run` to spawn `task-runner` in background** — This is the core milestone ("queue a task, Claude executes it")
2. **Add `TaskCreate`/`TaskUpdate` calls to `/planner` commands** — Sync UI
3. **Store agentId in task record** — Enable resume/retry
4. **Wire `task-awareness` to session start** — Re-sync on new sessions
5. **Add output capture** — Persist agent output to SQLite

---

## 6. Key Constraints and Gotchas

1. **No Task tool inside Explore/Plan agents.** These agent types cannot spawn sub-tasks. Only agents with "All tools" or specifically listed `Task` access can nest.

2. **Background tasks don't block the user.** The user can continue working while background agents execute. But if the background agent writes to the same files the user is editing, conflicts can occur.

3. **Model selection matters for cost.** Haiku is ~20x cheaper than Opus. For automated background tasks that follow a well-defined workflow (like TDD substeps), Sonnet is the sweet spot.

4. **`isolation: "worktree"` creates a git worktree.** The agent works in an isolated copy. Changes are returned as a branch name. Useful for task-runner agents that modify code.

5. **Hooks apply in subagents.** Pre/PostToolUse hooks from the parent session run in background agents too. This is good for security but can cause unexpected blocking if hooks are interactive.

6. **Token caching works across turns within a subagent.** The first turn caches the system prompt and context. Subsequent turns read from cache. This makes multi-turn background agents efficient.

7. **Output file is JSONL.** Each line is a complete JSON object. The file can be read incrementally to monitor progress.

8. **Session-scoped task IDs.** `TaskCreate` IDs (1, 2, 3...) reset each session. Soul-planner's SQLite IDs are persistent. Need a mapping layer.

---

## 7. Architecture Diagram for Soul-Planner Integration

```
User: "/planner add 'Build auth module'"
    |
    v
[/planner skill loads into session]
    |
    v
[Bash: python -m soul_planner add "Build auth module"]
    |  -> creates task in SQLite (id=42, status=BACKLOG)
    v
[TaskCreate(subject="Build auth module", activeForm="Queued")]
    |  -> shows in Claude Code task UI
    v
User: "/planner-run 42"
    |
    v
[/planner-run skill loads into session]
    |
    v
[Task(subagent_type="task-runner", run_in_background=true, model="sonnet",
      prompt="Execute soul-planner task #42. Read task from SQLite...")]
    |  -> spawns background agent
    |  -> returns agentId
    v
[Bash: python -m soul_planner update 42 --agent-id "a5d6c67f..."]
    |  -> stores agentId in SQLite for resume/retry
    v
User continues working...
    |
    [Meanwhile, in background:]
    task-runner agent:
        1. Reads task from SQLite
        2. Updates substep: PLANNING
        3. Updates Claude Code UI: TaskUpdate(activeForm="PLANNING: Build auth [1/5]")
        4. Writes tests (TDD)
        5. Advances: TESTING -> IMPLEMENTING -> REVIEWING -> VALIDATING
        6. On completion: python -m soul_planner done 42 --output "..."
        7. TaskUpdate(status="completed")
    |
    v
[Completion notification arrives in parent session]
"Agent 'Execute soul-planner task #42' completed"
```
