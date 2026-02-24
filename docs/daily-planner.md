# Soul Ecosystem — Daily Planner

**Current Phase:** Phase 1 — soul-planner (Weeks 1-2)
**Strategy:** Sequential Focus on 5 Projects (`docs/plans/2026-02-23-focused-dev-strategy-design.md`)
**Content:** Daily content pipeline (`docs/plans/2026-02-23-daily-content-strategy-design.md`)

## Daily Rhythm

```
BLOCK 1: BUILD (9am - 1pm, 4h)
  Current phase project ONLY

BLOCK 2: EXPLORE (2pm - 6pm, 4h)
  Research that feeds current project

BLOCK 3: SOCIAL (7pm - 9pm, 2h)
  Content from Block 1+2 -> LinkedIn, Twitter, blog, dev.to, Reddit

BLOCK 4: SCOUT (9pm - 11pm, 2h)
  Job portals, freelance platforms, recruiter outreach, applications
```

## Build Order

```
Phase 1: soul-planner    (Weeks 1-2)   <- NOW
Phase 2: soul-mesh        (Weeks 3-5)
Phase 3: soul-outreach    (Weeks 6-8)
Phase 4: soul-viz         (Weeks 9-10)
Ongoing: soul-os          (side-effects)
```

## Legend

`[x]` done | `[ ]` pending | `[>]` in progress | `[-]` skipped | `[!]` blocked

---

# PHASE 1: soul-planner (Feb 22 - Mar 7)

**Milestone:** `/task add "do X"` queues a task, Claude executes it in background, output captured.

## Day 1 — Sat Feb 22

### Block 1: BUILD — soul-mesh continued (9am-1pm)
- [x] Review soul-mesh current state (16 tests, node/discovery/election done)
- [x] Identify next modules to extract (transport, sync, relay)
- [x] Extract and standalone-ify next module with tests
- [x] Verify: all tests pass, zero `from brain` imports

### Block 2: EXPLORE — CARS baseline setup (2pm-6pm)
- [x] SSH to titan-pc, install llama.cpp (compile from source for i5-8400)
- [x] Download 3B model (e.g., Phi-3-mini-4k GGUF 4-bit) to titan-pc
- [x] Run smoke test: simple prompt, verify inference works
- [x] Document hardware baseline: inference speed, memory usage

### Block 3: MARKET (7pm-11pm)
- [-] (Strategy not yet defined — redesigned on Day 2)

---

## Day 2 — Sun Feb 23

### Block 1: BUILD — Strategy redesign + soul-planner kickoff (9am-1pm)
- [x] Redesign dev strategy: 37 projects -> 5 focused projects
- [x] Define milestones for each project
- [x] Write design doc: `docs/plans/2026-02-23-focused-dev-strategy-design.md`
- [x] Update CLAUDE.md with new 5-project focus
- [x] Set up 4-block daily rhythm (BUILD/EXPLORE/SOCIAL/SCOUT)
- [x] Write content strategy: `docs/plans/2026-02-23-daily-content-strategy-design.md`
- [x] Create `~/soul/soul-planner/` repo structure (plugin manifest, pyproject.toml, CLAUDE.md)
- [x] Define SQLite schema: tasks + task_dependencies tables with Kanban states
- [x] Implement `soul_planner/db.py` — async SQLite wrapper for task CRUD (67 tests)
- [x] Implement `soul_planner/models.py` — Pydantic models + enums
- [x] Implement `soul_planner/cli.py` — Click CLI with 12 subcommands

### Block 2: EXPLORE — soul-planner research (2pm-6pm)
- [ ] Research Claude Code extension patterns (skills, agents, slash commands)
- [ ] Study existing task management in Claude Code (Task tool, TodoWrite)
- [ ] Design soul-planner architecture (queue + schedule modes)
- [ ] Identify what can be built as skills vs agents vs standalone code

### Block 3: SOCIAL (7pm-9pm)
- [ ] CAPTURE: Pull git commits (72h), update content-log, review post-log
- [ ] STRATEGY: Architect picks topic + platform routing
- [ ] DRAFT: Short-form + Long-form agents draft in parallel
- [ ] PUBLISH: Post after user approval, engage on Reddit
- [ ] TRACK: Log to post-log, pull engagement metrics

### Block 4: SCOUT — profile foundation (9pm-11pm)
- [ ] Audit each job portal: what fields exist, what information is needed
- [ ] Collate all missing profile information into a questionnaire for user
- [ ] Review job alert settings: expand roles beyond "AI Engineer", expand locations
- [ ] Draft expanded `docs/profile/identity.md` with all fields portals need

### Evening Review (11pm, 15min)
- [ ] Strategy redesign done? Planner research started? Content posted?

---

## Day 3 — Mon Feb 24

### Block 1: BUILD — soul-planner repo + task model (9am-1pm)
- [x] Create `~/soul/soul-planner/` repo structure (pyproject.toml, README, CLAUDE.md)
- [x] Define SQLite schema: tasks table (id, title, description, status, priority, depends_on, output, created_at)
- [x] Implement `planner/db.py` — async SQLite wrapper for task CRUD
- [x] Implement `planner/models.py` — Pydantic models (TaskCreate, TaskStatus, TaskResult)
- [x] Write tests for db layer (target: 10+ tests)

### Block 2: EXPLORE — Claude Code Task tool internals (2pm-6pm)
- [x] Read Claude Code docs on Task tool, run_in_background, subagent_type
- [x] Experiment: spawn a background task, capture its output
- [x] Understand how skills and agents interact with Task tool
- [x] Document findings for soul-planner integration

### Block 3: SOCIAL (7pm-9pm)
- [ ] CAPTURE: Pull git commits (72h), update content-log, review post-log
- [ ] STRATEGY: Architect picks topic + platform routing
- [ ] DRAFT: Short-form + Long-form agents draft in parallel
- [ ] PUBLISH: Post after user approval, engage on Reddit
- [ ] TRACK: Log to post-log, pull engagement metrics

### Block 4: SCOUT — more portals (9pm-11pm)
- [ ] Create Wellfound profile
- [ ] Create Instahyre profile
- [ ] Scan LinkedIn Jobs, apply to 3-5 matches

### Evening Review (11pm, 15min)
- [ ] Task model + DB working? Tests passing? Content posted?

---

## Day 4 — Tue Feb 25

### Block 1: BUILD — soul-planner queue mode (9am-1pm)
- [ ] Implement `/task add` slash command (SKILL.md)
- [ ] Implement `/task list` — show all tasks with status
- [ ] Implement `/task status <id>` — detailed view
- [ ] Implement `/task cancel <id>`
- [ ] Symlink skill into `~/.claude/skills/planner/`

### Block 2: EXPLORE — task scheduling patterns (2pm-6pm)
- [ ] Research priority queue algorithms (for task ordering)
- [ ] Research dependency resolution (topological sort for depends_on)
- [ ] Prototype: given tasks with dependencies, produce execution order
- [ ] Design schedule mode: how to read daily-planner.md and auto-queue

### Block 3: SOCIAL (7pm-9pm)
- [ ] CAPTURE: Pull git commits (72h), update content-log, review post-log
- [ ] STRATEGY: Architect picks topic + platform routing
- [ ] DRAFT: Short-form + Long-form agents draft in parallel
- [ ] PUBLISH: Post after user approval, engage on Reddit
- [ ] TRACK: Log to post-log, pull engagement metrics

### Block 4: SCOUT — freelance platforms (9pm-11pm)
- [ ] Apply to Toptal (screening)
- [ ] Apply to Turing (coding test)
- [ ] Connect with 5 recruiters on LinkedIn

### Evening Review (11pm, 15min)
- [ ] `/task add` and `/task list` working? Scheduling research done?

---

## Day 5 — Wed Feb 26

### Block 1: BUILD — soul-planner runner (9am-1pm)
- [ ] Implement `planner/runner.py` — picks next task (priority + deps), spawns Claude Code Task tool
- [ ] Implement background execution with `run_in_background: true`
- [ ] Implement output capture (read task output, store in DB)
- [ ] Implement `/task output <id>` — view captured output
- [ ] Write tests for runner (mock Task tool)

### Block 2: EXPLORE — schedule mode design (2pm-6pm)
- [ ] Design daily-planner.md parser (extract block tasks as queueable items)
- [ ] Prototype: parse today's block, output task list
- [ ] Design auto-queue trigger (when does schedule mode kick in?)
- [ ] Document schedule mode spec

### Block 3: SOCIAL (7pm-9pm)
- [ ] CAPTURE: Pull git commits (72h), update content-log, review post-log
- [ ] STRATEGY: Architect picks topic + platform routing
- [ ] DRAFT: Short-form + Long-form agents draft in parallel
- [ ] PUBLISH: Post after user approval, engage on Reddit
- [ ] TRACK: Log to post-log, pull engagement metrics

### Block 4: SCOUT — applications (9pm-11pm)
- [ ] Apply to Andela
- [ ] Scan job portals, apply to 3-5 roles
- [ ] Follow up on any recruiter responses

### Evening Review (11pm, 15min)
- [ ] Runner executing tasks? Schedule mode designed?

---

## Day 6 — Thu Feb 27

### Block 1: BUILD — soul-planner schedule mode + polish (9am-1pm)
- [ ] Implement `planner/scheduler.py` — reads daily-planner.md, auto-queues block tasks
- [ ] Implement `/task run` — starts the runner (picks up queued tasks)
- [ ] Implement `/task retry <id>` — retry failed tasks
- [ ] Error handling: task failures, retries with backoff
- [ ] Write agent definition: `agents/task-runner.md`

### Block 2: EXPLORE — integration testing (2pm-6pm)
- [ ] End-to-end test: `/task add "create a hello world file"` -> runs -> check output
- [ ] Test dependency chain: Task A -> Task B (B waits for A)
- [ ] Test schedule mode: parse today's planner, queue tasks, run
- [ ] Fix bugs found during integration testing

### Block 3: SOCIAL (7pm-9pm)
- [ ] CAPTURE: Pull git commits (72h), update content-log, review post-log
- [ ] STRATEGY: Architect picks topic + platform routing
- [ ] DRAFT: Short-form + Long-form agents draft in parallel
- [ ] PUBLISH: Post after user approval, engage on Reddit
- [ ] TRACK: Log to post-log, pull engagement metrics

### Block 4: SCOUT — recruiter outreach (9pm-11pm)
- [ ] Connect with 5 more recruiters on LinkedIn
- [ ] Join MLOps Community Slack
- [ ] Scan portals, apply to 3-5 roles

### Evening Review (11pm, 15min)
- [ ] End-to-end working? Schedule mode functional?

---

## Day 7 — Fri Feb 28

### Block 1: BUILD — soul-planner ship (9am-1pm)
- [ ] README.md with usage examples and setup guide
- [ ] Verify all symlinks work (skill, agent)
- [ ] Run full test suite, fix any failures
- [ ] Git init, commit, push to Gitea
- [ ] Push to GitHub (public repo)

### Block 2: EXPLORE — soul-mesh prep (2pm-6pm)
- [ ] Review soul-mesh current state (253 tests, what's missing)
- [ ] Research: unified SSH gateway approaches (how to present multiple machines as one)
- [ ] Research: shared filesystem patterns (rsync, NFS, custom)
- [ ] Plan Phase 2 (soul-mesh) first week priorities

### Block 3: SOCIAL + weekly wrap (7pm-9pm)
- [ ] CAPTURE: Pull full week's git commits, review content-log + post-log
- [ ] STRATEGY: Architect picks topic + platform routing
- [ ] DRAFT: Short-form + Long-form agents draft in parallel
- [ ] DRAFT: Substack weekly digest from week's content
- [ ] PUBLISH: Post after user approval
- [ ] TRACK: Log to post-log, Analyst runs weekly pivot report

### Block 4: SCOUT — week review (9pm-11pm)
- [ ] Review all inbound matches (Instahyre, Wellfound, Naukri)
- [ ] Refresh portal profiles
- [ ] Log weekly SCOUT metrics
- [ ] Plan next week's applications

### Week 1 Review (11pm, 30min)
```
## Week 1 Review — Feb 28

### Phase 1 Progress (soul-planner)
- Task model + SQLite DB: [ ]
- Queue mode (/task add, list, status, cancel): [ ]
- Runner (background execution + output capture): [ ]
- Schedule mode (daily-planner parser): [ ]
- Integration tested: [ ]
- README + shipped to GitHub: [ ]
- MILESTONE: "Queue a task, Claude executes it" [ ]

### Block 3 (SOCIAL)
- LinkedIn posts published: __ / 3 (Mon/Wed/Fri)
- Tweets published: __
- Reddit threads engaged: __
- Substack digest: [ ]
- Content-log entries: __
- Post-log entries: __

### Block 4 (SCOUT)
- Job portals live: __ / 4
- Freelance platforms applied: __ / 3
- Recruiter connections: __
- Job applications submitted: __

### Next Phase Prep
- soul-mesh research done? [ ]
- Phase 2 plan ready? [ ]
```

---

# TRACKING

## Project Milestones

| # | Project | Milestone | Status |
|---|---------|-----------|--------|
| 1 | soul-planner | Queue tasks, Claude executes in background | [ ] In progress |
| 2 | soul-mesh | SSH into mesh as one machine, run LLM inference | [ ] Waiting |
| 3 | soul-outreach | CLI pipeline: import -> enrich -> draft -> send | [ ] Waiting |
| 4 | soul-viz | POST data + prompt, get rendered chart | [ ] Waiting |
| 5 | soul-os | Autonomous loop uses soul-planner | [ ] Waiting |

## Content Tracker

| Week | LinkedIn (3/wk) | Twitter (daily) | Reddit | Substack (1/wk) | Blog | dev.to |
|------|-----------------|-----------------|--------|-----------------|------|--------|
| 1 (Feb 22-28) | __ / 3 | __ | __ threads | __ / 1 | __ / 1 | -- |
| 2 (Mar 1-7) | | | | | | |

## Scout Tracker

| Channel | Setup | Active | Metric |
|---------|-------|--------|--------|
| Naukri | [x] | [x] | recruiter views: __ |
| Indeed | [x] | [x] | applications: __ |
| Instahyre | [x] | [ ] | inbound matches: __ |
| Wellfound | [x] | [x] | applications: __ |
| LinkedIn Jobs | [x] | [x] | applications: __ |
| Toptal | [ ] | [ ] | status: needs signup |
| Turing | [ ] | [ ] | status: needs signup |
| Andela | [ ] | [ ] | status: __ |
| Recruiters | [ ] | [ ] | connected: __ |

## Revenue Tracker

| Month | Consulting | Freelance | Product | Total |
|-------|-----------|-----------|---------|-------|
| Mar | $0 | $0 | $0 | $0 |
| Apr | | | | |
| May | | | | |

---

# DAILY REVIEW TEMPLATE

```
## Day __ Review — [date]
### Block 1 (BUILD — soul-planner)
- Completed: ...
- Blocked: ...
### Block 2 (EXPLORE)
- Completed: ...
- Blocked: ...
### Block 3 (SOCIAL)
- Posts: ...
### Block 4 (SCOUT)
- Applications: ...
### Tomorrow Focus
1. ...
2. ...
```
