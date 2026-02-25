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
