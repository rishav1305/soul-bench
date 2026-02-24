"""Tests for the soul-planner Click CLI."""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from soul_planner.cli import main
from soul_planner.db import TaskDB


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def memory_db(monkeypatch):
    """Patch CLI to use in-memory DB."""
    db = TaskDB(":memory:")

    import asyncio
    loop = asyncio.new_event_loop()
    loop.run_until_complete(db.init())

    def _get_db():
        return db

    monkeypatch.setattr("soul_planner.cli._get_db", _get_db)
    return db


class TestAdd:
    """CLI add command."""

    def test_add_basic(self, runner, memory_db):
        result = runner.invoke(main, ["add", "Build auth module"])
        assert result.exit_code == 0
        assert "Added task #1" in result.output
        assert "Build auth module" in result.output

    def test_add_with_priority(self, runner, memory_db):
        result = runner.invoke(main, ["add", "Urgent task", "--priority", "critical"])
        assert result.exit_code == 0
        assert "critical" in result.output.lower()

    def test_add_with_details(self, runner, memory_db):
        result = runner.invoke(main, ["add", "Task", "--details", "Some details"])
        assert result.exit_code == 0

    def test_add_with_acceptance(self, runner, memory_db):
        result = runner.invoke(main, ["add", "Task", "--acceptance", "Tests pass"])
        assert result.exit_code == 0


class TestList:
    """CLI list command."""

    def test_list_empty(self, runner, memory_db):
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "No tasks" in result.output

    def test_list_with_tasks(self, runner, memory_db):
        runner.invoke(main, ["add", "Task A"])
        runner.invoke(main, ["add", "Task B"])
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "Task A" in result.output
        assert "Task B" in result.output

    def test_list_filter_by_status(self, runner, memory_db):
        runner.invoke(main, ["add", "Backlog task"])
        result = runner.invoke(main, ["list", "--status", "backlog"])
        assert result.exit_code == 0
        assert "Backlog task" in result.output


class TestStatus:
    """CLI status command."""

    def test_status_existing(self, runner, memory_db):
        runner.invoke(main, ["add", "Check me"])
        result = runner.invoke(main, ["status", "1"])
        assert result.exit_code == 0
        assert "Check me" in result.output

    def test_status_nonexistent(self, runner, memory_db):
        result = runner.invoke(main, ["status", "999"])
        assert result.exit_code == 0
        assert "not found" in result.output.lower()


class TestBoard:
    """CLI board command."""

    def test_board_empty(self, runner, memory_db):
        result = runner.invoke(main, ["board"])
        assert result.exit_code == 0
        assert "BACKLOG" in result.output

    def test_board_with_tasks(self, runner, memory_db):
        runner.invoke(main, ["add", "Backlog item"])
        result = runner.invoke(main, ["board"])
        assert result.exit_code == 0
        assert "Backlog item" in result.output


class TestCancel:
    """CLI cancel command."""

    def test_cancel(self, runner, memory_db):
        runner.invoke(main, ["add", "Cancel me"])
        result = runner.invoke(main, ["cancel", "1"])
        assert result.exit_code == 0
        assert "cancelled" in result.output.lower()


class TestBlock:
    """CLI block/unblock commands."""

    def test_block(self, runner, memory_db):
        runner.invoke(main, ["add", "Block me"])
        result = runner.invoke(main, ["block", "1", "Need answer"])
        assert result.exit_code == 0
        assert "blocked" in result.output.lower()

    def test_unblock(self, runner, memory_db):
        runner.invoke(main, ["add", "Unblock me"])
        runner.invoke(main, ["block", "1", "Waiting"])
        result = runner.invoke(main, ["unblock", "1"])
        assert result.exit_code == 0


class TestSubstep:
    """CLI substep command."""

    def test_substep(self, runner, memory_db):
        runner.invoke(main, ["add", "Step me"])
        result = runner.invoke(main, ["substep", "1", "planning"])
        assert result.exit_code == 0
        assert "planning" in result.output.lower()


class TestDone:
    """CLI done command."""

    def test_done(self, runner, memory_db):
        runner.invoke(main, ["add", "Finish me"])
        result = runner.invoke(main, ["done", "1"])
        assert result.exit_code == 0
        assert "done" in result.output.lower()


class TestNext:
    """CLI next command."""

    def test_next_empty(self, runner, memory_db):
        result = runner.invoke(main, ["next"])
        assert result.exit_code == 0
        assert "No ready tasks" in result.output

    def test_next_with_tasks(self, runner, memory_db):
        runner.invoke(main, ["add", "Pick me"])
        result = runner.invoke(main, ["next"])
        assert result.exit_code == 0
        assert "Pick me" in result.output


class TestSetAgent:
    """CLI set-agent command."""

    def test_set_agent(self, runner, memory_db):
        runner.invoke(main, ["add", "Track agent"])
        result = runner.invoke(main, ["set-agent", "1", "agent-abc123"])
        assert result.exit_code == 0
        assert "agent-abc123" in result.output

    def test_set_agent_shown_in_status(self, runner, memory_db):
        runner.invoke(main, ["add", "Check status"])
        runner.invoke(main, ["set-agent", "1", "agent-xyz"])
        result = runner.invoke(main, ["status", "1"])
        assert result.exit_code == 0
        assert "agent-xyz" in result.output
