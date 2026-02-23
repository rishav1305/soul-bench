# soul-planner

Claude Code plugin: persistent task queue with Kanban workflow.

## Conventions

- Python 3.11+, aiosqlite, structlog, click, pydantic
- All SQL parameterized with `?` -- never concatenate
- Env vars prefixed `PLANNER_`
- Tests: pytest with pytest-asyncio, `asyncio_mode = "auto"`
- DB path: `~/.claude/soul-planner/tasks.db`

## Structure

- `soul_planner/` -- Python package (models, db, cli, runner, scheduler)
- `commands/` -- Claude Code slash commands (markdown)
- `agents/` -- Claude Code agent definitions (markdown)
- `skills/` -- Claude Code skills (markdown)
- `.claude-plugin/plugin.json` -- Plugin manifest

## Task States

BACKLOG -> IN_PROGRESS -> VALIDATION -> DONE
IN_PROGRESS substeps: planning -> testing -> implementing -> reviewing -> validating
BLOCKED can occur from IN_PROGRESS (waiting for user input)
