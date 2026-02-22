---
name: daily-planner
description: Display today's tasks organized by BUILD/EXPLORE/MARKET blocks with progress tracking. Use when starting your day or checking what's next.
---

Read the daily planner at `~/soul/docs/daily-planner.md`. Find today's date and display today's tasks.

## Output Format

Show this exact structure:

```
## Today -- {Day Name}, {Month} {Date}
Phase: {current phase from top of file}
Progress: {X}/{Y} tasks done

### Block 1: BUILD (9am-1pm) -- Track A
{theme from the day's heading}
{X}/{Y} done
- [x] Completed task
- [ ] Pending task

### Block 2: EXPLORE (2pm-6pm) -- Tracks B/C/D
{theme from the day's heading}
{X}/{Y} done
- [ ] Task
- [ ] Task

### Block 3: MARKET (7pm-11pm) -- Track E + Channels
{theme from the day's heading}
{X}/{Y} done
- [ ] Task
- [ ] Task
```

After the blocks, show a compact tracker summary:

```
### Trackers
Extraction: {X}/{Y} projects shipped | Research: {X}/{Y} experiments | Marketing: {X}/{Y} channels | Blog: {X}/{Y} posts
```

## Rules

1. Match today's date to a "Day N -- {Day} {Month} {Date}" section in the planner
2. Count done `[x]` vs total tasks per block and overall
3. If yesterday has uncompleted `[ ]` tasks, add a "Carryover" section before the trackers
4. Show tracker tables from the bottom of the file in a compact one-line summary
5. If today's date is not found in the planner, say so and show the nearest upcoming day instead
