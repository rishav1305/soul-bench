---
description: "Parse today's daily planner and queue block tasks"
argument-hint: "[block-number]"
allowed-tools: [Bash, Read, TaskCreate, TaskUpdate, TaskList]
---

# /task-schedule -- Queue Tasks from Daily Planner

Parse `~/soul/docs/daily-planner.md`, find today's date, and queue uncompleted tasks into the soul-planner backlog.

## Process

1. **Read the daily planner**:
   ```bash
   cat ~/soul/docs/daily-planner.md
   ```

2. **Find today's section**: Match today's date to a "Day N -- {Day} {Month} {Date}" section.

3. **Parse blocks**: If `$ARGUMENTS` contains a block number (1-4), only parse that block. Otherwise parse all 4 blocks.

4. **Queue uncompleted tasks**: For each `[ ]` task in the target block(s):
   ```bash
   python -m soul_planner add "TASK_TITLE" --details "From daily planner Day N, Block B"
   ```

   Skip tasks marked `[x]` (done), `[-]` (skipped), or `[!]` (blocked).

5. **Set dependencies**: If tasks within a block have natural ordering (e.g., "define schema" before "implement db"), add `--depends-on` accordingly.

6. **Show result**:
   ```bash
   python -m soul_planner board
   ```

## Example

```
/task-schedule 1
```

Parses Block 1 (BUILD) for today, queues all uncompleted tasks.

```
/task-schedule
```

Parses all 4 blocks for today, queues everything uncompleted.

## Notes

- Tasks are created with `source=schedule` (handled by the scheduler.py module when available)
- Duplicate detection: check if a task with the same title already exists before adding
- Priority mapping: BUILD tasks get `high`, EXPLORE get `normal`, SOCIAL get `normal`, SCOUT get `low`

The user invoked: $ARGUMENTS
