---
name: showcase-recording
description: "Record terminal GIFs at task execution checkpoints. Produces social-ready showcase with GIFs, narrative, and content brief."
---

# Showcase Recording

Record terminal output as GIFs at each checkpoint during task execution. Produces a showcase directory with GIFs, a narrative markdown, and a social brief for the content pipeline.

## Trigger

- Called automatically by task-orchestrator after each substep (via showcase-recorder agent)
- Called manually via /showcase command

## Input

The caller provides:
- **TASK_ID** (required): The soul-planner task ID
- **MILESTONE** (required): One of: design-approved, tests-red, tests-green, security-clear, shipped
- **TOPIC** (required): Kebab-case name (e.g., soul-os-task-queue)
- **PROJECT_DIR** (required): Project directory for running tests

## Process

### 1. Create showcase directory

```bash
mkdir -p docs/showcase/$(date +%Y-%m-%d)-TOPIC/
```

### 2. Capture milestone GIF

Use the capture script to record the appropriate command:

| Milestone | Command to Record | Output File |
|-----------|------------------|-------------|
| design-approved | python -m soul_planner board | planning-board.gif |
| tests-red | cd PROJECT_DIR && python -m pytest tests/ -v --tb=short 2>&1 \| head -60 | tests-red-output.gif |
| tests-green | cd PROJECT_DIR && python -m pytest tests/ -v --tb=short 2>&1 \| head -60 | tests-green-output.gif |
| security-clear | python -m soul_planner board | security-clear-board.gif |
| shipped | bash -c "python -m soul_planner board && echo '---' && git log --oneline -10" | shipped-final.gif |

Command:
```bash
~/soul/soul-showcase/scripts/capture.sh \
  docs/showcase/$(date +%Y-%m-%d)-TOPIC/FILENAME.gif \
  "COMMAND"
```

If asciinema/agg not available, fallback: run command, save output to .txt file, report that GIF capture is unavailable.

### 3. Capture metrics

```bash
# Get task status for metrics
python -m soul_planner status TASK_ID
```

Extract: test counts, files changed, substep state.

### 4. Write checkpoint entry

Append to `docs/showcase/$(date +%Y-%m-%d)-TOPIC/showcase.md`:

```markdown
## MILESTONE
- **Time:** HH:MM
- **GIF:** [FILENAME.gif](./FILENAME.gif)
- **Metrics:** (test counts, files changed, etc.)
- **Notes:** (auto-generated summary of what happened in this substep)
```

### 5. Generate social brief (shipped milestone only)

On the `shipped` milestone, generate `social-brief.md`:

```markdown
# Showcase: TOPIC
- Topic: TASK_TITLE description
- GIFs: N recordings covering full lifecycle
- Key metrics: N tests written, N passing, N security issues, N files changed
- Narrative: "one-liner summary"
- Best GIF for Twitter: tests-green-output.gif (shows passing tests -- most visual impact)
- Best GIF for LinkedIn: shipped-final.gif (shows complete professional workflow)
```

### 6. Update content-log

Append to docs/content-log.md:
```
YYYY-MM-DD | BUILD | TOPIC showcase | metrics | showcase: docs/showcase/YYYY-MM-DD-TOPIC/
```

## Fallback Behavior

If asciinema or agg is not installed:
1. Run the command normally
2. Save raw terminal output to `MILESTONE-terminal.txt` (same as build-snapshot)
3. Log warning: "GIF capture unavailable -- saved text fallback"
4. Continue with narrative and social brief generation

## Rules

- Never skip the content-log update
- Never overwrite existing showcase entries -- always append
- Keep GIFs short (< 15 seconds of recording)
- Keep narrative notes concise (2-3 sentences per milestone)
