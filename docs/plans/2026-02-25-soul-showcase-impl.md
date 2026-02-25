# soul-showcase Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use soul-workflow:executing-plans to implement this plan task-by-task.

**Goal:** Build a soul-showcase plugin that records terminal GIFs at each checkpoint during autonomous task execution and produces social-ready content.

**Architecture:** Claude Code plugin with a showcase-recorder agent (haiku), a recording skill, a /showcase command, and a dashboard HTML template. Uses asciinema + agg for terminal-to-GIF conversion. Integrates with task-orchestrator via background agent spawns.

**Tech Stack:** asciinema (terminal recording), agg (cast-to-GIF), Playwright (fallback/dashboard), Bash, Python (helper script for narrative generation)

---

### Task 1: Install asciinema and agg

**Files:**
- Create: `~/soul/soul-showcase/scripts/install-deps.sh`

**Step 1: Install asciinema via apt**

```bash
sudo apt install -y asciinema
```

Verify: `asciinema --version` should print `asciinema 2.4.0` or similar.

**Step 2: Download agg binary for aarch64**

```bash
curl -L -o /usr/local/bin/agg https://github.com/asciinema/agg/releases/download/v1.7.0/agg-aarch64-unknown-linux-gnu
chmod +x /usr/local/bin/agg
```

Verify: `agg --version` should print version info.

**Step 3: Write install script for reproducibility**

Create `~/soul/soul-showcase/scripts/install-deps.sh`:

```bash
#!/bin/bash
set -euo pipefail

echo "Installing asciinema..."
sudo apt install -y asciinema

echo "Installing agg v1.7.0 (aarch64)..."
sudo curl -L -o /usr/local/bin/agg \
  https://github.com/asciinema/agg/releases/download/v1.7.0/agg-aarch64-unknown-linux-gnu
sudo chmod +x /usr/local/bin/agg

echo "Verifying..."
asciinema --version
agg --version
echo "Done."
```

**Step 4: Commit**

```bash
git add soul-showcase/scripts/install-deps.sh
git commit -m "feat(soul-showcase): add dependency install script for asciinema + agg"
```

---

### Task 2: Scaffold plugin structure

**Files:**
- Create: `~/soul/soul-showcase/.claude-plugin/plugin.json`
- Create: `~/soul/soul-showcase/LICENSE`
- Create dirs: `skills/showcase-recording/`, `agents/`, `commands/`, `dashboard/`, `scripts/`

**Step 1: Create plugin manifest**

Create `~/soul/soul-showcase/.claude-plugin/plugin.json`:

```json
{
  "name": "soul-showcase",
  "description": "Record terminal GIFs at task execution checkpoints for social media showcases. Captures autonomous build progress as shareable content.",
  "version": "1.0.0",
  "author": { "name": "Rishav" },
  "license": "MIT"
}
```

**Step 2: Create LICENSE**

MIT license, same as soul-workflow.

**Step 3: Create empty directories**

```bash
mkdir -p ~/soul/soul-showcase/{skills/showcase-recording,agents,commands,dashboard,scripts}
```

**Step 4: Commit**

```bash
git add soul-showcase/
git commit -m "feat(soul-showcase): scaffold plugin structure"
```

---

### Task 3: Write the capture helper script

**Files:**
- Create: `~/soul/soul-showcase/scripts/capture.sh`

This is the core recording utility. It records a command's terminal output as a GIF.

**Step 1: Write capture.sh**

```bash
#!/bin/bash
# capture.sh -- Record a command's output as a terminal GIF
# Usage: capture.sh <output.gif> <command> [args...]
#
# Example: capture.sh board.gif python -m soul_planner board
#
# Requires: asciinema, agg

set -euo pipefail

GIF_PATH="$1"
shift
COMMAND="$@"

CAST_FILE=$(mktemp /tmp/showcase-XXXXXX.cast)
trap "rm -f $CAST_FILE" EXIT

# Record the command (non-interactive, 2 second idle limit)
asciinema rec \
  --command "$COMMAND" \
  --idle-time-limit 2 \
  --quiet \
  "$CAST_FILE"

# Convert to GIF
# --cols 100 --rows 30 for consistent sizing
# --font-size 16 for readability
agg \
  --cols 100 \
  --rows 30 \
  --font-size 16 \
  "$CAST_FILE" \
  "$GIF_PATH"

echo "Captured: $GIF_PATH ($(du -h "$GIF_PATH" | cut -f1))"
```

**Step 2: Make executable and test**

```bash
chmod +x ~/soul/soul-showcase/scripts/capture.sh
~/soul/soul-showcase/scripts/capture.sh /tmp/test-capture.gif "echo hello world && sleep 1 && echo done"
```

Verify: `/tmp/test-capture.gif` exists and is a valid GIF.

**Step 3: Commit**

```bash
git add soul-showcase/scripts/capture.sh
git commit -m "feat(soul-showcase): add terminal-to-GIF capture script"
```

---

### Task 4: Write the showcase-recording skill

**Files:**
- Create: `~/soul/soul-showcase/skills/showcase-recording/SKILL.md`

**Step 1: Write the skill**

```markdown
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

mkdir -p docs/showcase/$(date +%Y-%m-%d)-TOPIC/

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
```

**Step 2: Commit**

```bash
git add soul-showcase/skills/showcase-recording/SKILL.md
git commit -m "feat(soul-showcase): add showcase-recording skill"
```

---

### Task 5: Write the showcase-recorder agent

**Files:**
- Create: `~/soul/soul-showcase/agents/showcase-recorder.md`

**Step 1: Write the agent**

```markdown
---
name: showcase-recorder
description: "Capture terminal GIFs at task execution checkpoints. Spawned by task-orchestrator after each substep. Lightweight haiku agent."
tools: [Bash, Read, Write, Edit, Glob]
model: haiku
---

# Showcase Recorder Agent

You capture terminal output as GIFs at task execution checkpoints. You are spawned in the background after each substep completes.

## Input

Your prompt contains:
- TASK_ID: The soul-planner task ID
- MILESTONE: One of: design-approved, tests-red, tests-green, security-clear, shipped
- TOPIC: Kebab-case name (e.g., soul-os-task-queue)
- PROJECT_DIR: The project directory

## Process

Follow the showcase-recording skill exactly:

1. Create showcase directory: `mkdir -p docs/showcase/$(date +%Y-%m-%d)-TOPIC/`

2. Run the capture script for this milestone:

   | Milestone | Command | File |
   |-----------|---------|------|
   | design-approved | python -m soul_planner board | planning-board.gif |
   | tests-red | cd PROJECT_DIR && python -m pytest tests/ -v --tb=short 2>&1 \| head -60 | tests-red-output.gif |
   | tests-green | cd PROJECT_DIR && python -m pytest tests/ -v --tb=short 2>&1 \| head -60 | tests-green-output.gif |
   | security-clear | python -m soul_planner board | security-clear-board.gif |
   | shipped | bash -c "python -m soul_planner board && echo '---' && git log --oneline -10" | shipped-final.gif |

   ```bash
   ~/soul/soul-showcase/scripts/capture.sh \
     docs/showcase/$(date +%Y-%m-%d)-TOPIC/FILENAME.gif \
     "COMMAND"
   ```

   If capture.sh fails (asciinema/agg not installed), save raw output to MILESTONE-terminal.txt instead.

3. Get task metrics:
   ```bash
   python -m soul_planner status TASK_ID
   ```

4. Append checkpoint entry to `docs/showcase/$(date +%Y-%m-%d)-TOPIC/showcase.md`

5. If milestone is `shipped`:
   - Generate `social-brief.md` with GIF recommendations per platform
   - Update `docs/content-log.md`

## Output

Report:
1. MILESTONE captured: [which one]
2. GIF: [filename and size, or "text fallback"]
3. SHOWCASE updated: [path to showcase.md]
4. ISSUES: [any problems, or "none"]

## Rules

- You are a RECORDER. Never modify source code, tests, or project files.
- Only create/modify files in docs/showcase/ and docs/content-log.md.
- Keep recordings short (< 15 seconds).
- Always append to showcase.md, never overwrite.
```

**Step 2: Commit**

```bash
git add soul-showcase/agents/showcase-recorder.md
git commit -m "feat(soul-showcase): add showcase-recorder agent"
```

---

### Task 6: Write the /showcase command

**Files:**
- Create: `~/soul/soul-showcase/commands/showcase.md`

**Step 1: Write the command**

```markdown
---
description: "Record a showcase GIF at the current state or a specific milestone"
argument-hint: "<topic> [milestone]"
allowed-tools: [Bash, Read, Write, Edit, Glob]
model: haiku
---

# /showcase -- Record Showcase GIF

Manually trigger a showcase recording for a topic.

## Arguments

Parse `$ARGUMENTS` as: `<topic> [milestone]`

- **topic** (required): Kebab-case name (e.g., soul-os-task-queue)
- **milestone** (optional): One of: design-approved, tests-red, tests-green, security-clear, shipped
  - If omitted, record the current planner board state as `current-state.gif`

If `$ARGUMENTS` is empty, ask the user for the topic.

## Process

1. Determine what to record:
   - If milestone provided: follow the milestone capture table from showcase-recording skill
   - If no milestone: capture `/planner board` as `current-state.gif`

2. Create showcase directory:
   ```bash
   mkdir -p docs/showcase/$(date +%Y-%m-%d)-TOPIC/
   ```

3. Run capture:
   ```bash
   ~/soul/soul-showcase/scripts/capture.sh \
     docs/showcase/$(date +%Y-%m-%d)-TOPIC/FILENAME.gif \
     "COMMAND"
   ```

4. Report the GIF path and size to the user.

5. If milestone is `shipped`, generate social-brief.md.

The user invoked: $ARGUMENTS
```

**Step 2: Commit**

```bash
git add soul-showcase/commands/showcase.md
git commit -m "feat(soul-showcase): add /showcase command"
```

---

### Task 7: Write the dashboard HTML template

**Files:**
- Create: `~/soul/soul-showcase/dashboard/index.html`

**Step 1: Write single-file HTML dashboard**

Create a self-contained HTML file that reads task data from a JSON file and renders:
- Kanban board with columns: BACKLOG, PLANNING, TESTING, IMPLEMENTING, REVIEWING, VALIDATING, DONE
- Task cards with title, priority badge, current substep
- Progress bar showing substep completion (0-100%)
- Latest checkpoint message
- Dark theme (consistent with soul ecosystem)
- Tech stack: vanilla HTML/CSS/JS, no frameworks, reads from `data.json` via fetch

The file should:
- Be < 300 lines total
- Use CSS grid for the kanban layout
- Use the color scheme: background #1a1a2e, cards #16213e, accent #0f3460, progress #e94560
- Render gracefully with no data (empty board)
- Include a `<script>` block that fetches `./data.json` on load

**Step 2: Create a sample data.json**

Create `~/soul/soul-showcase/dashboard/data.json`:

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Add task queue to soul-os",
      "status": "in_progress",
      "substep": "implementing",
      "priority": "high",
      "checkpoint": "tests-green: 8/8 passing"
    }
  ],
  "progress": {
    "current_substep": 3,
    "total_substeps": 5,
    "percentage": 60
  }
}
```

**Step 3: Test by opening in browser**

```bash
cd ~/soul/soul-showcase/dashboard && python3 -m http.server 8888 &
# Open http://localhost:8888 -- verify the board renders
kill %1
```

**Step 4: Commit**

```bash
git add soul-showcase/dashboard/
git commit -m "feat(soul-showcase): add kanban dashboard HTML template"
```

---

### Task 8: Wire showcase-recorder into task-orchestrator

**Files:**
- Modify: `~/soul/soul-planner/agents/task-orchestrator.md`

**Step 1: Read current task-orchestrator**

Read `~/soul/soul-planner/agents/task-orchestrator.md` and locate the execution loop section (steps 5-6, after capture output).

**Step 2: Add showcase-recorder spawn**

After step 6 ("Capture snapshot") and before step 7 ("Handle failure"), add a new step:

```markdown
6b. **Showcase capture** (if docs/showcase/ recording is active): Spawn showcase-recorder in background:
    ```
    Task(
        description="showcase capture: MILESTONE for task #TASK_ID",
        subagent_type="showcase-recorder",
        model="haiku",
        run_in_background=true,
        prompt="TASK_ID: TASK_ID\nMILESTONE: MILESTONE\nTOPIC: TOPIC\nPROJECT_DIR: PROJECT_DIR"
    )
    ```
    Where MILESTONE maps from substep: planning->design-approved, testing->tests-red, implementing->tests-green, reviewing->security-clear, validating->shipped.
    Where TOPIC is derived from TITLE in kebab-case.
    This runs in the background and does NOT block the next substep.
```

**Step 3: Verify the edit doesn't break existing flow**

Read the full file, confirm the execution loop still follows the correct sequence: update state -> sync UI -> spawn runner -> check result -> capture output -> capture snapshot -> **showcase capture** -> handle failure -> continue.

**Step 4: Commit**

```bash
git add soul-planner/agents/task-orchestrator.md
git commit -m "feat(soul-showcase): wire showcase-recorder into task-orchestrator"
```

---

### Task 9: Update content-architect to read showcases

**Files:**
- Modify: `~/soul/.claude/agents/content-architect.md`

**Step 1: Read current content-architect**

Read the agent file and find where it reads `docs/snapshots/`.

**Step 2: Add showcase reading**

Add a parallel section that also reads `docs/showcase/` with the same 72h window:

```markdown
### Showcase GIFs (72h window)

Read `docs/showcase/` for recent showcase recordings:
- Check for `social-brief.md` files -- these are pre-formatted content briefs
- GIF files can be referenced directly in social posts (attach to tweets, embed in LinkedIn)
- Prioritize showcases with `shipped` milestone -- these have the complete story
```

**Step 3: Commit**

```bash
git add .claude/agents/content-architect.md
git commit -m "feat(soul-showcase): teach content-architect to read showcase GIFs"
```

---

### Task 10: End-to-end test

**Files:** None (verification only)

**Step 1: Verify plugin discovery**

```bash
ls ~/soul/soul-showcase/.claude-plugin/plugin.json
```

Confirm the file exists and is valid JSON.

**Step 2: Test capture script manually**

```bash
~/soul/soul-showcase/scripts/capture.sh /tmp/test-board.gif "python -m soul_planner board"
ls -la /tmp/test-board.gif
```

Verify GIF was created.

**Step 3: Test /showcase command invocation**

Invoke `/showcase test-run` and verify it creates `docs/showcase/2026-02-25-test-run/current-state.gif`.

**Step 4: Verify dashboard renders**

```bash
cd ~/soul/soul-showcase/dashboard && python3 -m http.server 8888 &
sleep 2
curl -s http://localhost:8888/ | head -5
kill %1
```

Verify HTML is served.

**Step 5: Clean up test artifacts**

```bash
rm -f /tmp/test-board.gif /tmp/test-capture.gif
rm -rf docs/showcase/2026-02-25-test-run/
```

**Step 6: Final commit**

```bash
git add -A
git commit -m "feat(soul-showcase): complete plugin with recording, dashboard, and orchestrator integration"
```

---

## Task Summary

| Task | What | Files |
|------|------|-------|
| 1 | Install asciinema + agg | scripts/install-deps.sh |
| 2 | Scaffold plugin | plugin.json, LICENSE, dirs |
| 3 | Capture helper script | scripts/capture.sh |
| 4 | Recording skill | skills/showcase-recording/SKILL.md |
| 5 | Recorder agent | agents/showcase-recorder.md |
| 6 | /showcase command | commands/showcase.md |
| 7 | Dashboard template | dashboard/index.html, data.json |
| 8 | Wire into orchestrator | soul-planner/agents/task-orchestrator.md |
| 9 | Update content-architect | .claude/agents/content-architect.md |
| 10 | End-to-end test | Verification only |

## Execution Batches

- **Batch 1** (Tasks 1-3): Dependencies + scaffold + capture script
- **Batch 2** (Tasks 4-6): Skill + agent + command
- **Batch 3** (Tasks 7-9): Dashboard + integrations
- **Batch 4** (Task 10): End-to-end verification
