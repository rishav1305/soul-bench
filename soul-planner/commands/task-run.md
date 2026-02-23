---
description: "Pick up and execute the next ready task from the queue"
argument-hint: "[task-id]"
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList]
model: opus
---

# /task-run -- Execute a Task

Pick up a task from the queue and execute it through the full dev workflow.

## Process

1. **Pick task**: If `$ARGUMENTS` contains an ID, use that task. Otherwise, get the next ready task:
   ```bash
   python -m soul_planner next
   ```

2. **Move to IN_PROGRESS**:
   ```bash
   python -m soul_planner substep TASK_ID planning
   ```
   Sync: `TaskUpdate(status=in_progress, activeForm="PLANNING: title [1/5]")`

3. **Execute the 5 substeps**:

   ### Substep 1: PLANNING
   - Read the task description and acceptance criteria
   - Understand what needs to be built
   - Identify files to create/modify
   - Design the approach
   - Update: `python -m soul_planner substep ID planning`

   ### Substep 2: TESTING
   - Write tests first (TDD)
   - Run tests to confirm RED (failing)
   - Update: `python -m soul_planner substep ID testing`
   - Sync: `TaskUpdate(activeForm="TESTING: title [2/5]")`

   ### Substep 3: IMPLEMENTING
   - Write minimal code to pass tests
   - Run tests to confirm GREEN
   - Update: `python -m soul_planner substep ID implementing`
   - Sync: `TaskUpdate(activeForm="IMPLEMENTING: title [3/5]")`

   ### Substep 4: REVIEWING
   - Self code-review for quality and security
   - Check: parameterized SQL, no hardcoded secrets, proper error handling
   - Update: `python -m soul_planner substep ID reviewing`
   - Sync: `TaskUpdate(activeForm="REVIEWING: title [4/5]")`

   ### Substep 5: VALIDATING
   - Run full test suite
   - Confirm all green
   - Update: `python -m soul_planner substep ID validating`
   - Sync: `TaskUpdate(activeForm="VALIDATING: title [5/5]")`

4. **Move to VALIDATION** (user review):
   ```bash
   python -m soul_planner validate ID
   ```
   Tell the user: "Task #ID is ready for your review."

5. **Handle blockers**: If at any point you need user input:
   ```bash
   python -m soul_planner block ID "Question or issue description"
   ```
   Ask the user the question. When they answer:
   ```bash
   python -m soul_planner unblock ID
   ```
   Resume from the substep where you paused.

## Validate Command

The `validate` CLI command doesn't exist yet. Use this instead:
```bash
python -m soul_planner substep ID validating
```
Then tell the user the task is ready for review.

## After User Approves

When the user says the task is good:
```bash
python -m soul_planner done ID
```
Sync: `TaskUpdate(status=completed)`

The user invoked: $ARGUMENTS
