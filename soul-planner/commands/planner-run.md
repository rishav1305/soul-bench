---
description: "Pick up and execute the next ready task from the queue"
argument-hint: "[task-id]"
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, Task, TaskCreate, TaskUpdate, TaskList]
model: opus
---

# /planner-run -- Execute a Task

Pick up a task from the queue and execute it through the full dev workflow.

## ID Convention

Claude Code task subjects use `SP#<id>:` prefix. Use `TaskList()` to find the matching task.

## Process

1. **Pick task**: If `$ARGUMENTS` contains an ID, use that task. Otherwise, get the next ready task:
   ```bash
   python -m soul_planner next
   ```

2. **Ensure task is in Claude Code UI**: Call `TaskList()` and check if `SP#ID:` exists.
   - If not found: `TaskCreate(subject="SP#ID: TITLE", description="DESCRIPTION", activeForm="Starting: TITLE")`
   - If found: note the Claude Code task ID for updates.

3. **Move to IN_PROGRESS**:
   ```bash
   python -m soul_planner substep TASK_ID planning
   ```
   Sync: `TaskUpdate(taskId=CC_ID, activeForm="PLANNING: TITLE [1/5]")`

4. **Execute the 5 substeps**:

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
   - Sync: `TaskUpdate(taskId=CC_ID, activeForm="TESTING: TITLE [2/5]")`

   ### Substep 3: IMPLEMENTING
   - Write minimal code to pass tests
   - Run tests to confirm GREEN
   - Update: `python -m soul_planner substep ID implementing`
   - Sync: `TaskUpdate(taskId=CC_ID, activeForm="IMPLEMENTING: TITLE [3/5]")`

   ### Substep 4: REVIEWING
   - Self code-review for quality and security
   - Check: parameterized SQL, no hardcoded secrets, proper error handling
   - Update: `python -m soul_planner substep ID reviewing`
   - Sync: `TaskUpdate(taskId=CC_ID, activeForm="REVIEWING: TITLE [4/5]")`

   ### Substep 5: VALIDATING
   - Run full test suite
   - Confirm all green
   - Update: `python -m soul_planner substep ID validating`
   - Sync: `TaskUpdate(taskId=CC_ID, activeForm="VALIDATING: TITLE [5/5]")`

5. **Move to VALIDATION** (user review):
   ```bash
   python -m soul_planner validate ID
   ```
   Sync: `TaskUpdate(taskId=CC_ID, activeForm="Review: TITLE")`
   Tell the user: "Task #ID is ready for your review."

6. **Handle blockers**: If at any point you need user input:
   ```bash
   python -m soul_planner block ID "Question or issue description"
   ```
   Sync: `TaskUpdate(taskId=CC_ID, activeForm="BLOCKED: TITLE -- reason")`
   Ask the user the question. When they answer:
   ```bash
   python -m soul_planner unblock ID
   ```
   Resume from the substep where you paused.

## After User Approves

When the user says the task is good:
```bash
python -m soul_planner done ID
```
Sync: `TaskUpdate(taskId=CC_ID, status="completed")`

The user invoked: $ARGUMENTS
