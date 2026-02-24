---
description: "Dispatch a task for autonomous background execution with per-substep model selection"
argument-hint: "[task-id]"
allowed-tools: [Bash, Task, TaskCreate, TaskUpdate]
model: sonnet
---

# /planner-run-auto -- Autonomous Background Execution

Dispatch a soul-planner task for fully autonomous background execution. The task-orchestrator agent handles all 5 substeps with the correct model per step.

## Process

1. **Pick task**: If `$ARGUMENTS` contains an ID, use that. Otherwise get the next ready task:
   ```bash
   python -m soul_planner next
   ```
   If no ready tasks, tell the user "No ready tasks in backlog." and stop.

2. **Read task details**:
   ```bash
   python -m soul_planner status TASK_ID
   ```
   Extract: title, description, acceptance criteria. Determine the project directory from the task description or default to `~/soul/soul-planner`.

3. **Check for resume**: If the task already has an agent_id and is BLOCKED:
   - Show the blocker reason to the user
   - Ask: "Resume previous agent or restart fresh?"
   - To resume: `Task(resume=AGENT_ID, subagent_type="task-orchestrator", prompt="Continue from where you left off. The blocker has been resolved.")`
   - To restart: proceed to step 4

4. **Promote to IN_PROGRESS** (if still in BACKLOG):
   ```bash
   python -m soul_planner promote TASK_ID
   ```

5. **Sync to Claude Code task UI**:
   ```
   TaskCreate(subject="TITLE", description="DESCRIPTION", activeForm="Dispatching: TITLE")
   ```

6. **Spawn orchestrator in background**:
   ```
   Task(
       description="Execute task #TASK_ID",
       subagent_type="task-orchestrator",
       run_in_background=true,
       model="haiku",
       prompt="TASK_ID: ID\nTITLE: title\nDESCRIPTION: description\nACCEPTANCE: acceptance\nPROJECT_DIR: project_dir"
   )
   ```

7. **Store agent ID**:
   ```bash
   python -m soul_planner set-agent TASK_ID AGENT_ID
   ```

8. **Report to user**:
   ```
   Task #TASK_ID dispatched for background execution.
   Agent: AGENT_ID
   Model rotation: opus (plan) -> opus (test) -> sonnet (impl) -> opus (review) -> sonnet (validate)

   Check progress: python -m soul_planner status TASK_ID
   Stop agent: use TaskStop with the agent ID above
   ```

The user invoked: $ARGUMENTS
