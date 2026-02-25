# Attribution

## Forked Skills

12 of the skills in this plugin were forked from the **superpowers** plugin v4.3.1:

- brainstorming
- writing-plans
- test-driven-development
- subagent-driven-development
- executing-plans
- requesting-code-review (including code-reviewer.md)
- receiving-code-review
- verification-before-completion
- finishing-a-development-branch
- using-git-worktrees
- dispatching-parallel-agents
- systematic-debugging (including supporting docs)

Additionally, the `agents/code-reviewer.md` agent and 3 commands (`brainstorm.md`, `write-plan.md`, `execute-plan.md`) were forked from superpowers v4.3.1.

**Original author:** Jesse Vincent
**Original license:** MIT
**Source:** https://github.com/anthropics/claude-code-plugins (superpowers plugin)
**Version forked:** 4.3.1

All `superpowers:` skill references were renamed to `soul-workflow:` to avoid conflicts with the original plugin.

## Soul-Specific Skills

The following skills were created for the soul ecosystem and are not derived from superpowers:

- block-execution (10-step daily block workflow)
- build-snapshot (milestone capture for content pipeline)
- task-execution (bridge between soul-planner substeps and soul-workflow skills)

The `snapshot.md` command was also created for the soul ecosystem.
