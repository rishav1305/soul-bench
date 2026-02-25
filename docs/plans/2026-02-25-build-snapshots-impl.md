# Build Snapshots Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a snapshot skill that captures structured text + terminal screenshots at key build milestones, feeding the SOCIAL block with rich content material.

**Architecture:** Standalone skill at `.claude/skills/build-snapshot/SKILL.md` invoked from block-execution at 5 milestones. Snapshots stored in `docs/snapshots/<date>-<topic>/`. Content-log extended with snapshot path. Content-architect agent updated to read snapshots.

**Tech Stack:** Claude Code skills (markdown), Bash (git diff, screenshots), content pipeline agents

---

### Task 1: Create the build-snapshot skill

**Files:**
- Create: `.claude/skills/build-snapshot/SKILL.md`

**Step 1: Write the skill file**

```markdown
---
name: build-snapshot
description: "Capture a structured snapshot of build progress at a milestone. Saves text summary + terminal screenshot to docs/snapshots/. Use during block-execution or manually via /snapshot."
---

# Build Snapshot

Capture the current state of a build at a milestone moment. Produces structured text and a terminal screenshot for the content pipeline.

## Trigger

- Called automatically by block-execution at 5 milestones
- Called manually when the user says "snapshot", "capture this", or invokes /snapshot

## Input

The caller provides (via prompt or user input):
- **milestone** (required): One of: design-approved, tests-red, tests-green, security-clear, shipped
- **topic** (required): Kebab-case name for the snapshot directory (e.g., soul-planner-integration)
- **notes** (optional): Free-text context to include

If inputs are missing, ask the user.

## Process

### 1. Create snapshot directory

```bash
mkdir -p docs/snapshots/$(date +%Y-%m-%d)-TOPIC/
```

### 2. Capture git state

```bash
git diff --stat HEAD
git log --oneline -5
```

If this is the `shipped` milestone, also capture:
```bash
git log --oneline --since="today" | wc -l   # commits today
find . -name "*.py" -path "*/soul_*" | xargs wc -l 2>/dev/null | tail -1  # LOC
```

### 3. Capture test state (if applicable)

For `tests-red`, `tests-green`, `security-clear`, `shipped` milestones:
```bash
# Run the project's test suite and capture output
# The exact command depends on the project -- check for .venv/bin/python, pytest, etc.
```

### 4. Take terminal screenshot

Use the Bash tool to run the relevant command (test suite, git log, board view), then capture the terminal output as a text snapshot. Save it as a `.txt` file alongside the markdown:

```
docs/snapshots/YYYY-MM-DD-TOPIC/MILESTONE-terminal.txt
```

Note: If browser automation is available, use it to take an actual screenshot. Otherwise, save the raw terminal output as text.

### 5. Write snapshot entry

Append to `docs/snapshots/YYYY-MM-DD-TOPIC/snapshot.md`:

```markdown
## MILESTONE
- **Time:** HH:MM
- **Files changed:** (from git diff --stat)
- **LOC delta:** +X / -Y
- **Tests:** N total, N passed, N failed (if applicable)
- **Notes:** (auto summary + user notes)
- **Terminal:** [MILESTONE-terminal.txt](./MILESTONE-terminal.txt)
```

### 6. Update content-log

Check if today's content-log already has an entry for this topic.
- If yes: append `| snapshot: docs/snapshots/YYYY-MM-DD-TOPIC/` to the existing line
- If no: add a new entry:
```
YYYY-MM-DD | BUILD | TOPIC description | metrics | snapshot: docs/snapshots/YYYY-MM-DD-TOPIC/
```

## Milestone-Specific Guidance

| Milestone | Key data to capture |
|-----------|-------------------|
| design-approved | Design summary from the plan doc, key files identified, approach chosen |
| tests-red | Test file names, test count, which assertions will flip, terminal of failing tests |
| tests-green | Files changed since tests-red, LOC delta, all-green terminal output |
| security-clear | Audit checklist results, any fixes applied, clean confirmation |
| shipped | Final commit hash, total files/LOC/tests, full green terminal, content-log update |

## Rules

- Never skip the content-log update
- Never overwrite existing snapshot entries -- always append
- Keep notes concise (2-3 sentences max per milestone)
- Terminal captures should show the most relevant output (truncate if very long)
```

**Step 2: Verify skill file is valid**

Run: `cat .claude/skills/build-snapshot/SKILL.md | head -3`
Expected: Shows the YAML frontmatter

**Step 3: Commit**

```bash
git add .claude/skills/build-snapshot/SKILL.md
git commit -m "feat: add build-snapshot skill for content pipeline"
```

---

### Task 2: Create the /snapshot command

**Files:**
- Create: `.claude/commands/snapshot.md`

**Step 1: Write the command file**

```markdown
---
description: "Capture a build snapshot at the current milestone"
argument-hint: "<milestone> <topic> [notes]"
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep]
model: haiku
---

# /snapshot -- Capture Build Snapshot

Invoke the build-snapshot skill to capture the current build state.

## Arguments

Parse `$ARGUMENTS` as: `<milestone> <topic> [notes...]`

- **milestone**: One of: design-approved, tests-red, tests-green, security-clear, shipped
- **topic**: Kebab-case name (e.g., soul-planner-integration)
- **notes**: Everything after topic is free-text notes (optional)

If `$ARGUMENTS` is empty, ask the user for milestone and topic.

## Process

Follow the build-snapshot skill process exactly:

1. Create `docs/snapshots/$(date +%Y-%m-%d)-TOPIC/` directory
2. Capture git state (`git diff --stat HEAD`, `git log --oneline -5`)
3. If milestone involves tests: run the project test suite, capture output
4. Save terminal output to `MILESTONE-terminal.txt`
5. Append structured entry to `snapshot.md`
6. Update `docs/content-log.md` with snapshot path

The user invoked: $ARGUMENTS
```

**Step 2: Verify command file**

Run: `cat .claude/commands/snapshot.md | head -3`
Expected: Shows YAML frontmatter

**Step 3: Commit**

```bash
git add .claude/commands/snapshot.md
git commit -m "feat: add /snapshot command for manual build captures"
```

---

### Task 3: Add snapshot calls to block-execution skill

**Files:**
- Modify: `.claude/skills/block-execution/SKILL.md`

**Step 1: Add snapshot invocations at 5 milestone points**

After Step 1 (PLAN), add:
```markdown
**Snapshot:** Invoke build-snapshot skill: `milestone=design-approved topic=<block-topic>`
```

After Step 4 (TDD), add:
```markdown
**Snapshot:** Invoke build-snapshot skill: `milestone=tests-red topic=<block-topic>`
```

After Step 5 (EXECUTE) when tests are green, add:
```markdown
**Snapshot:** Invoke build-snapshot skill: `milestone=tests-green topic=<block-topic>`
```

After Step 8 (SECURITY AUDIT), add:
```markdown
**Snapshot:** Invoke build-snapshot skill: `milestone=security-clear topic=<block-topic>`
```

After Step 10 (COMMIT + MERGE), add:
```markdown
**Snapshot:** Invoke build-snapshot skill: `milestone=shipped topic=<block-topic>`
```

Also add a note at the top of the Steps section:
```markdown
> **Snapshots:** This workflow captures build snapshots at 5 milestones for the content pipeline. The `<block-topic>` is derived from the block's primary task name in kebab-case (e.g., `soul-planner-integration`).
```

**Step 2: Verify the skill still parses correctly**

Run: `head -5 .claude/skills/block-execution/SKILL.md`
Expected: Valid YAML frontmatter

**Step 3: Commit**

```bash
git add .claude/skills/block-execution/SKILL.md
git commit -m "feat: add snapshot captures at 5 milestones in block-execution"
```

---

### Task 4: Update content-architect agent to read snapshots

**Files:**
- Modify: `.claude/agents/content-architect.md`

**Step 1: Add snapshots to input sources**

In the `## Input Sources` section, add item 6:
```markdown
6. **Build snapshots** -- `~/soul/docs/snapshots/` -- Structured milestone captures from BUILD blocks. Check for directories modified in the last 72 hours. Each contains `snapshot.md` with metrics, design decisions, and terminal output references.
```

**Step 2: Add snapshot references to the output brief**

In the `### Artifacts to Reference` section of the Output Format, update to:
```markdown
### Artifacts to Reference
- {Specific file, commit, metric, or screenshot the writers should pull from}
- {Snapshot directory if available: `docs/snapshots/YYYY-MM-DD-topic/`}
- {Terminal captures from snapshots: test output, board views, git stats}
```

**Step 3: Add snapshot awareness to Process section**

After step 2 (Scan), add:
```markdown
2b. **Read snapshots** -- Check `~/soul/docs/snapshots/` for directories from the last 72h. Read `snapshot.md` in each for structured metrics, design decisions, and terminal output paths. These are richer than git diffs alone.
```

**Step 4: Commit**

```bash
git add .claude/agents/content-architect.md
git commit -m "feat: teach content-architect to read build snapshots"
```

---

### Task 5: Create docs/snapshots/ directory and extend content-log format

**Files:**
- Create: `docs/snapshots/.gitkeep`
- Modify: `docs/content-log.md`

**Step 1: Create the snapshots directory**

```bash
mkdir -p docs/snapshots
touch docs/snapshots/.gitkeep
```

**Step 2: Update content-log format documentation**

In `docs/content-log.md`, update the Format section to:
```markdown
## Format

```
DATE | BLOCK | What happened (1-2 lines) | Content type hint | snapshot: path (optional)
```

Content type hints: `deep-dive`, `metrics`, `architecture`, `opinion`, `progress`

The `snapshot:` field links to a `docs/snapshots/YYYY-MM-DD-topic/` directory containing structured milestone data and terminal captures from the build-snapshot skill.
```

**Step 3: Commit**

```bash
git add docs/snapshots/.gitkeep docs/content-log.md
git commit -m "feat: add snapshots directory and extend content-log format"
```
