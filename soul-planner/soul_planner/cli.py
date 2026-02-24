"""Click-based CLI for soul-planner.

Commands
--------
- ``soul-planner add`` -- Add a new task to backlog
- ``soul-planner list`` -- List tasks (optionally by status)
- ``soul-planner board`` -- Kanban board view
- ``soul-planner status`` -- Show detailed task status
- ``soul-planner cancel`` -- Cancel a task
- ``soul-planner block`` -- Block a task with a reason
- ``soul-planner unblock`` -- Resume a blocked task
- ``soul-planner done`` -- Mark a task as done
- ``soul-planner set-agent`` -- Store a background agent ID on a task
- ``soul-planner substep`` -- Update a task's substep
- ``soul-planner next`` -- Show next ready task
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import click

from soul_planner.db import TaskDB
from soul_planner.models import Priority, Substep, TaskCreate, TaskStatus, TaskUpdate

_DEFAULT_DB_PATH = str(Path.home() / ".claude" / "soul-planner" / "tasks.db")


def _get_db() -> TaskDB:
    db_path = os.environ.get("PLANNER_DB_PATH", _DEFAULT_DB_PATH)
    return TaskDB(db_path)


def _run(coro):
    """Run an async coroutine synchronously."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, coro).result()
    return asyncio.run(coro)


@click.group()
def main():
    """soul-planner -- task queue and scheduler for Claude Code."""


@main.command()
@click.argument("title")
@click.option("--details", default="", help="Task description.")
@click.option("--acceptance", default="", help="Acceptance criteria.")
@click.option("--priority", type=click.Choice(["low", "normal", "high", "critical"]), default="normal")
@click.option("--depends-on", default="", help="Comma-separated task IDs this depends on.")
def add(title: str, details: str, acceptance: str, priority: str, depends_on: str):
    """Add a new task to BACKLOG."""
    db = _get_db()
    dep_ids = [int(x.strip()) for x in depends_on.split(",") if x.strip()] if depends_on else []

    async def _add():
        await db.init()
        return await db.add(TaskCreate(
            title=title,
            description=details,
            acceptance=acceptance,
            priority=Priority(priority),
            depends_on=dep_ids,
        ))

    task = _run(_add())
    click.echo(f"Added task #{task.id} to BACKLOG: \"{task.title}\"")
    if task.priority != Priority.NORMAL:
        click.echo(f"  Priority: {task.priority.value}")
    if task.depends_on:
        click.echo(f"  Depends on: {task.depends_on}")


@main.command("list")
@click.option("--status", type=click.Choice([s.value for s in TaskStatus]), default=None)
def list_tasks(status: str | None):
    """List tasks, optionally filtered by status."""
    db = _get_db()

    async def _list():
        await db.init()
        s = TaskStatus(status) if status else None
        return await db.list(status=s)

    tasks = _run(_list())
    if not tasks:
        click.echo("No tasks found.")
        return

    for t in tasks:
        substep_str = f" > {t.substep.value}" if t.substep else ""
        click.echo(f"  #{t.id}  [{t.status.value}{substep_str}]  {t.title}  ({t.priority.value})")


@main.command()
def board():
    """Show Kanban board view."""
    db = _get_db()

    async def _board():
        await db.init()
        return await db.board()

    board_data = _run(_board())

    for s in TaskStatus:
        tasks = board_data[s]
        click.echo(f"\n{s.value.upper()} ({len(tasks)})")
        click.echo("-" * 40)
        if not tasks:
            click.echo("  (empty)")
        for t in tasks:
            substep_str = f" > {t.substep.value}" if t.substep else ""
            click.echo(f"  #{t.id}  {t.title}  ({t.priority.value}){substep_str}")


@main.command()
@click.argument("task_id", type=int)
def status(task_id: int):
    """Show detailed task status."""
    db = _get_db()

    async def _status():
        await db.init()
        return await db.get(task_id)

    task = _run(_status())
    if not task:
        click.echo(f"Task #{task_id} not found.")
        return

    substep_str = f" > {task.substep.value}" if task.substep else ""
    click.echo(f"Task #{task.id}: {task.title}")
    click.echo(f"  Status:   {task.status.value}{substep_str}")
    click.echo(f"  Priority: {task.priority.value}")
    if task.description:
        click.echo(f"  Details:  {task.description}")
    if task.acceptance:
        click.echo(f"  Accept:   {task.acceptance}")
    if task.blocker:
        click.echo(f"  Blocker:  {task.blocker}")
    if task.depends_on:
        click.echo(f"  Deps:     {task.depends_on}")
    if task.agent_id:
        click.echo(f"  Agent:    {task.agent_id}")
    click.echo(f"  Created:  {task.created_at}")
    if task.started_at:
        click.echo(f"  Started:  {task.started_at}")
    if task.completed_at:
        click.echo(f"  Done:     {task.completed_at}")


@main.command()
@click.argument("task_id", type=int)
def cancel(task_id: int):
    """Cancel a task."""
    db = _get_db()

    async def _cancel():
        await db.init()
        return await db.cancel(task_id)

    task = _run(_cancel())
    click.echo(f"Task #{task.id} cancelled: \"{task.title}\"")


@main.command()
@click.argument("task_id", type=int)
@click.argument("reason")
def block(task_id: int, reason: str):
    """Block a task with a reason."""
    db = _get_db()

    async def _block():
        await db.init()
        return await db.block(task_id, reason)

    task = _run(_block())
    click.echo(f"Task #{task.id} blocked: \"{task.blocker}\"")


@main.command()
@click.argument("task_id", type=int)
def unblock(task_id: int):
    """Resume a blocked task."""
    db = _get_db()

    async def _unblock():
        await db.init()
        return await db.unblock(task_id)

    task = _run(_unblock())
    click.echo(f"Task #{task.id} unblocked, resumed to {task.status.value}")


@main.command()
@click.argument("task_id", type=int)
def done(task_id: int):
    """Mark a task as done."""
    db = _get_db()

    async def _done():
        await db.init()
        return await db.update(task_id, TaskUpdate(status=TaskStatus.DONE))

    task = _run(_done())
    click.echo(f"Task #{task.id} done: \"{task.title}\"")


@main.command("set-agent")
@click.argument("task_id", type=int)
@click.argument("agent_id")
def set_agent(task_id: int, agent_id: str):
    """Store a background agent ID on a task."""
    db = _get_db()

    async def _set():
        await db.init()
        return await db.update(task_id, TaskUpdate(agent_id=agent_id))

    task = _run(_set())
    click.echo(f"Task #{task.id} agent: {agent_id}")


@main.command()
@click.argument("task_id", type=int)
def validate(task_id: int):
    """Move a task to VALIDATION (ready for user review)."""
    db = _get_db()

    async def _validate():
        await db.init()
        return await db.update(task_id, TaskUpdate(status=TaskStatus.VALIDATION))

    task = _run(_validate())
    click.echo(f"Task #{task.id} moved to validation: \"{task.title}\"")


@main.command()
@click.argument("task_id", type=int)
def promote(task_id: int):
    """Move a task from BACKLOG to IN_PROGRESS with PLANNING substep."""
    db = _get_db()

    async def _promote():
        await db.init()
        from soul_planner.runner import TaskRunner
        runner = TaskRunner(db)
        return await runner.start(task_id)

    task = _run(_promote())
    click.echo(f"Task #{task.id} started: \"{task.title}\" [planning 1/5]")


@main.command()
@click.argument("task_id", type=int)
def advance(task_id: int):
    """Advance a task to the next substep."""
    db = _get_db()

    async def _advance():
        await db.init()
        from soul_planner.runner import TaskRunner
        runner = TaskRunner(db)
        return await runner.advance(task_id)

    task = _run(_advance())
    if task.status == TaskStatus.VALIDATION:
        click.echo(f"Task #{task.id} moved to validation: \"{task.title}\"")
    else:
        click.echo(f"Task #{task.id} advanced to: {task.substep.value}")


@main.command()
@click.argument("task_id", type=int)
@click.argument("step", type=click.Choice([s.value for s in Substep]))
def substep(task_id: int, step: str):
    """Update a task's current substep."""
    db = _get_db()

    async def _substep():
        await db.init()
        return await db.update(task_id, TaskUpdate(substep=Substep(step)))

    task = _run(_substep())
    click.echo(f"Task #{task.id} substep: {task.substep.value}")


@main.command("schedule")
@click.option("--block", "block_num", type=int, default=None, help="Only schedule tasks from this block (1-4).")
@click.option("--planner", default=None, type=click.Path(exists=True), help="Path to daily-planner.md.")
def schedule(block_num: int | None, planner: str | None):
    """Parse daily planner and queue today's uncompleted tasks."""
    db = _get_db()

    async def _schedule():
        await db.init()
        from pathlib import Path
        from soul_planner.scheduler import schedule_tasks
        planner_path = Path(planner) if planner else None
        return await schedule_tasks(db, planner_path=planner_path, block_filter=block_num)

    ids = _run(_schedule())
    if not ids:
        click.echo("No new tasks to schedule.")
    else:
        click.echo(f"Scheduled {len(ids)} tasks: {ids}")


@main.command("next")
def next_task():
    """Show next ready task (highest priority, deps met)."""
    db = _get_db()

    async def _next():
        await db.init()
        return await db.next_ready()

    task = _run(_next())
    if not task:
        click.echo("No ready tasks.")
        return
    click.echo(f"Next: #{task.id}  {task.title}  ({task.priority.value})")
