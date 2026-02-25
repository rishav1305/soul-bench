# soul-showcase Plugin Design

**Date:** 2026-02-25
**Status:** Approved

## Problem

soul-planner can now execute tasks autonomously through 5 substeps using soul-workflow skills. But there's no way to visually demonstrate this to an audience. Build snapshots capture text/terminal output for internal use, but social media needs compelling visual proof -- GIFs showing tests running, boards updating, code shipping.

## Solution

A `soul-showcase` plugin that records terminal GIFs at each checkpoint during autonomous task execution and produces social-ready content.

## Architecture

```
~/soul/soul-showcase/
  .claude-plugin/plugin.json
  skills/
    showcase-recording/SKILL.md     # Core recording workflow
  agents/
    showcase-recorder.md            # Haiku agent that captures GIFs at checkpoints
  commands/
    showcase.md                     # Manual /showcase command
  dashboard/
    index.html                      # Reusable Kanban + progress HTML template
                                    # (for future soul-os web client integration)
```

Auto-discovered via `.claude-plugin/plugin.json` under `~/soul/`.

## Data Flow

```
task-orchestrator runs a task autonomously (BACKGROUND_MODE: true)
  |
  v
After each substep completes:
  1. task-runner reports results via append-output
  2. showcase-recorder agent spawned in background (haiku)
     |
     +-- Runs /planner board -> captures terminal as GIF (asciinema + agg)
     +-- Runs test suite output -> captures as GIF (if applicable)
     +-- Runs git log -> captures as GIF
     +-- Writes checkpoint narrative to showcase/snapshot.md
  3. After all 5 substeps:
     +-- Compiles all GIFs into docs/showcase/<date>-<topic>/
     +-- Generates social-ready brief (social-brief.md)
     +-- Feeds content-architect for SOCIAL block
```

## Recording Mechanics

### Terminal GIF Capture

- `asciinema rec` captures terminal session as `.cast` file
- `agg` (asciinema gif generator) converts `.cast` -> `.gif`
- Each capture is short (5-15 seconds): run command, capture output, stop
- Fallback: save raw text + generate styled HTML, screenshot with Playwright

### Checkpoint Capture Table

| Checkpoint | GIF Content | File Name |
|------------|------------|-----------|
| design-approved | `/planner board` showing task in PLANNING | planning-board.gif |
| tests-red | Test suite run showing RED failures | tests-red-output.gif |
| tests-green | Test suite run showing all GREEN | tests-green-output.gif |
| security-clear | `/planner board` showing REVIEWING complete | security-clear-board.gif |
| shipped | Final DONE board + `git log --oneline -10` | shipped-final.gif |

## Output Artifacts

```
docs/showcase/YYYY-MM-DD-<topic>/
  planning-board.gif
  tests-red-output.gif
  tests-green-output.gif
  security-clear-board.gif
  shipped-final.gif
  showcase.md                 # Narrative with embedded GIF links
  social-brief.md             # Ready for content-architect
```

### social-brief.md Format

```markdown
# Showcase: <topic>
- Topic: <description>
- GIFs: N recordings covering full lifecycle
- Key metrics: N tests written, N passing, N security issues, N files changed
- Narrative: "<one-liner summary>"
- Best GIF for Twitter: <filename> (<why>)
- Best GIF for LinkedIn: <filename> (<why>)
```

## Integration Points

### task-orchestrator

After each substep's `append-output`, spawn showcase-recorder in background:

```
Task(
    description="showcase capture: MILESTONE for task #TASK_ID",
    subagent_type="showcase-recorder",
    model="haiku",
    run_in_background=true,
    prompt="TASK_ID: ID\nMILESTONE: milestone\nTOPIC: topic\nPROJECT_DIR: dir"
)
```

### content-architect

Reads `docs/showcase/` (72h window) alongside `docs/snapshots/` for richer briefs with embedded GIFs.

### /showcase command

Manual trigger for re-recording or demo purposes:
```
/showcase <topic> [milestone]
```
If milestone omitted, records current state.

## Dashboard Template

`dashboard/index.html` is a reusable single-file HTML template showing:
- Kanban board with task cards (BACKLOG, IN_PROGRESS substeps, VALIDATION, DONE)
- Progress bar (0-100% across 5 substeps)
- Latest checkpoint message

This is NOT served by the plugin. It's a template asset for:
- Future soul-os web client integration
- Manual demos (open in browser, screenshot with Playwright)

## Dependencies

- `asciinema` -- terminal recording (apt install asciinema)
- `agg` -- asciinema to GIF converter (cargo install agg, or download binary)
- Playwright (already available) -- fallback screenshots, dashboard captures

## Trigger Modes

1. **Auto-record**: task-orchestrator spawns showcase-recorder after each substep during `/planner-run-auto`
2. **Manual**: `/showcase <topic>` command for on-demand recording
