# soul-planner

A Claude Code plugin that adds a persistent task queue with Kanban workflow.

## What It Does

Queue tasks, track them through a structured dev workflow, and see live status in the Claude Code task panel.

```
BACKLOG --> IN PROGRESS --> VALIDATION --> DONE
              |
              +-- PLANNING
              +-- TESTING
              +-- IMPLEMENTING
              +-- REVIEWING
              +-- VALIDATING
```

## Install

```bash
cd ~/soul/soul-planner
pip install -e ".[dev]"
```

## CLI Usage

```bash
# Add tasks
soul-planner add "Build JWT auth" --priority high
soul-planner add "Write tests" --depends-on 1

# View tasks
soul-planner list
soul-planner board
soul-planner status 1
soul-planner next

# Lifecycle
soul-planner promote 1        # BACKLOG -> IN_PROGRESS (planning)
soul-planner advance 1        # Move to next substep
soul-planner validate 1       # IN_PROGRESS -> VALIDATION
soul-planner done 1           # VALIDATION -> DONE
soul-planner cancel 1

# Blockers
soul-planner block 1 "Need clarification on auth method"
soul-planner unblock 1

# Schedule from daily planner
soul-planner schedule          # Queue all uncompleted tasks for today
soul-planner schedule --block 1  # Only Block 1 (BUILD) tasks
```

## Claude Code Commands

| Command | Description |
|---------|-------------|
| `/task` | Manage tasks (add, list, board, status, cancel, etc.) |
| `/task-run` | Pick up and execute the next task through the full workflow |
| `/task-schedule` | Parse daily planner and queue today's tasks |

## Task States

| State | Meaning |
|-------|---------|
| BACKLOG | Created, waiting to be picked up |
| IN_PROGRESS | Claude is working (5 substeps visible) |
| BLOCKED | Waiting for user input |
| VALIDATION | Work done, needs user review |
| DONE | User approved |
| CANCELLED | Dropped |

## Architecture

- **Plugin manifest**: `.claude-plugin/plugin.json`
- **Python backend**: `soul_planner/` (models, db, cli, runner, scheduler)
- **Commands**: `commands/` (markdown slash commands)
- **Agent**: `agents/task-runner.md` (background execution)
- **Skill**: `skills/task-awareness/` (session sync)
- **Database**: `~/.claude/soul-planner/tasks.db` (SQLite, persists across sessions)

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## License

Apache-2.0
