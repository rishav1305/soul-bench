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
