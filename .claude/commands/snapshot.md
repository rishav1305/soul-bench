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
