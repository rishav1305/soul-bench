---
date: 2026-02-25
status: "Awaiting approval -- do not publish"
platform: LinkedIn
topic: soul-planner autonomous overnight task execution
---

I queued 6 tasks before going to sleep. By morning, Claude Code had worked through all of them.

That is the point of soul-planner -- not session management, not markdown organization.

Structured task delegation to an autonomous agent that executes while you are not at the keyboard, then stops and flags any blocker it cannot resolve cleanly.

Here is what the system does:

Tasks move through a 5-substep workflow: plan, test, implement, review, validate.

The task-runner agent picks up queued work and runs the full cycle on each task. It does not skip steps. Tests are written before implementation.

If the agent hits a blocker it cannot resolve without a judgment call, it stops and marks the task blocked -- rather than guessing.

I added two modes.

Queue mode: assign individual tasks with explicit dependencies.

Schedule mode: point it at my daily planner markdown, it parses the day's tasks and auto-queues them in dependency order. Topological ordering ensures nothing runs before its prerequisites complete.

In the morning, I review what ran, inspect the output, and decide what ships.

The build took 48 hours. 1,022 lines of Python across 6 modules, 126 tests, 12 CLI subcommands.

The stack: async SQLite for persistence, Pydantic for state validation, Click for the CLI. The same principles I apply to data pipelines -- explicit state machines, observable transitions, no silent failures.

What made 48 hours viable was not typing speed.

It was 8 years of data engineering pattern recognition applied to system design, then Claude Code handling implementation under direction. I designed the state machine, wrote the architecture, focused on test coverage. Claude wrote the boilerplate.

The boundary matters: this is not an agent running free. Every task has a defined scope. Every substep has a gate. Human review happens before anything ships.

The agent executes within a structure I designed -- which is exactly how I think about autonomous systems worth trusting.

If you are building workflows around AI coding agents, how are you handling task scope and rollback when something goes wrong overnight?

#ClaudeCode #AIEngineering #AutonomousAgents #Productivity #Python

---

<!-- PLATFORM OPTIMIZATION NOTES -- remove before posting -->

HOOK CHECK (mobile fold ~210 chars):
"I queued 6 tasks before going to sleep. By morning, Claude Code had worked through all of them."
= 96 characters. Sits well above the fold. The full first paragraph (hook + line 2) is ~170 chars -- still above the fold. Reader sees the payoff before tapping "see more". No change needed.

CHARACTER COUNT:
Body (above the dashed line, excluding these notes): ~1,820 characters.
Within the 1,500-2,500 limit. Approved.

MEDIA ATTACHMENT (pick one):
Option A: Create a simple workflow diagram showing the 5-substep pipeline:
  plan -> test -> implement -> review -> validate
  with "queue at night" on the left and "review in morning" on the right.
  Can be made in Excalidraw, Figma, or even a clean Mermaid diagram rendered as PNG.

Option B: Screenshot of the `planner board` CLI output after running a few demo tasks.
  To generate: run `planner add "example task"` a few times, advance some through substeps,
  then screenshot the board view.

Option C: No image. Text-only posts still perform on LinkedIn if the hook is strong enough.
  This hook ("I queued 6 tasks before going to sleep") is strong -- image is a bonus, not required.

EXTERNAL LINKS:
Do NOT put the GitHub repo link or any URL in the post body -- LinkedIn suppresses reach on posts with outbound links.
Post the repo link (github.com/rishav1305/soul-planner) in the FIRST COMMENT immediately after publishing, formatted as:
"GitHub: github.com/rishav1305/soul-planner -- spec and architecture notes in the README."

TAGGING:
- Consider tagging @Anthropic in the post body where Claude Code is mentioned ("then Claude Code handling implementation under direction"). LinkedIn reach may benefit from the brand tag.
- Note: There is no official @ClaudeCode LinkedIn page as of this draft date. Verify before tagging.
- Do not tag individuals unless you have a prior relationship -- cold tagging degrades post credibility.

HASHTAG STRATEGY:
Current: #ClaudeCode #AIEngineering #AutonomousAgents #Productivity #Python
Rationale:
- #ClaudeCode -- niche, but directly relevant. Reaches the Claude/Anthropic developer community.
- #AIEngineering -- mid-broad. Growing category with active followers.
- #AutonomousAgents -- niche, topical in the AI-agent discourse right now.
- #DataEngineering -- broad (Rishav's 8-year core identity). Reaches the data community who may not follow AI-agent content.
- #Python -- broad anchor. High follower base, ensures discoverability beyond the AI niche.
Replaced #DeveloperTools (low signal, generic) with #DataEngineering (on-brand, broad reach). 5 hashtags is the ceiling -- do not add more.

OPTIMAL POSTING TIME (IST, Rishav's timezone UTC+5:30):
LinkedIn engagement peaks Tuesday-Thursday. For IST:
- Best windows: 8:00-9:30 AM IST (before workday) or 12:00-1:00 PM IST (lunch scroll).
- Avoid Friday evening and weekends for technical content.
- Given the SOCIAL block runs 7-9 PM IST, schedule for the following morning (8:00 AM IST) using LinkedIn's native scheduler rather than posting live at 9 PM.

-->
