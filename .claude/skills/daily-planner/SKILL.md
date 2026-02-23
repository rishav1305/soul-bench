---
name: daily-planner
description: Display today's tasks organized by BUILD/EXPLORE/SOCIAL/SCOUT blocks with progress tracking. Use when starting your day or checking what's next.
---

Read the daily planner at `~/soul/docs/daily-planner.md`. Find today's date and extract today's tasks.

## Step 1: Parse

1. Match today's date to a "Day N -- {Day} {Month} {Date}" section in the planner
2. Extract each block's theme and tasks (there are 4 blocks: BUILD, EXPLORE, SOCIAL, SCOUT)
3. Count done `[x]` vs total tasks per block and overall
4. Check yesterday for uncompleted `[ ]` tasks (carryover)
5. If today's date is not found, use the nearest upcoming day instead

## Step 2: Show summary + present block choices

Show a one-line summary:

```
Today -- {Day Name}, {Month} {Date} | Phase: {phase} | Progress: {X}/{Y} done
```

If there are carryover tasks from yesterday, add: `Carryover: {N} tasks from yesterday`

Then use AskUserQuestion to present the blocks as selectable options:

- **Question**: "Which block do you want to work on?"
- **Header**: "Block"
- **Options** (use `markdown` preview for each):
  - **Block 1: BUILD** — description: "{theme}, {X}/{Y} done" — markdown preview: the block's task list with checkboxes
  - **Block 2: EXPLORE** — description: "{theme}, {X}/{Y} done" — markdown preview: the block's task list with checkboxes
  - **Block 3: SOCIAL** — description: "{theme}, {X}/{Y} done" — markdown preview: the block's task list with checkboxes
  - **Block 4: SCOUT** — description: "{theme}, {X}/{Y} done" — markdown preview: the block's task list with checkboxes
  - **Full view** — description: "Show all blocks + trackers" — markdown preview: all 4 blocks + tracker summary

## Step 3: Respond to selection

- If user picks a specific block: Show that block's full task list and invoke `block-execution` skill for that block
- If user picks "Full view": Show all 4 blocks in the output format below, plus tracker summary

### Full view output format

```
## Today -- {Day Name}, {Month} {Date}
Phase: {current phase from top of file}
Progress: {X}/{Y} tasks done

### Block 1: BUILD (9am-1pm)
{theme} | {X}/{Y} done
- [x] Completed task
- [ ] Pending task

### Block 2: EXPLORE (2pm-6pm)
{theme} | {X}/{Y} done
- [ ] Task

### Block 3: SOCIAL (7pm-9pm)
{theme} | {X}/{Y} done
- [ ] Task

### Block 4: SCOUT (9pm-11pm)
{theme} | {X}/{Y} done
- [ ] Task

### Trackers
Projects: {milestone status} | Content: {posts count} | Scout: {applications count}
```
