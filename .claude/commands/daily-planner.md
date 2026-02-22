Read the daily planner at `~/soul/docs/daily-planner.md`. Find today's date (today is $CURRENT_DATE) and display today's tasks.

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

## Rules

1. Match today's date to a "Day N -- {Day} {Month} {Date}" section in the planner
2. Count done `[x]` vs total tasks per block and overall
3. If yesterday has uncompleted `[ ]` tasks, add a "Carryover" section at the end
4. Show tracker tables (Extraction, Research, Marketing, Blog) in a compact summary after the blocks
5. If today's date is not found in the planner, say so and show the nearest upcoming day instead
