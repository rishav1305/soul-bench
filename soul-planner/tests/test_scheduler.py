"""Tests for the daily planner parser and task scheduler."""

from __future__ import annotations

from datetime import date

import pytest

from soul_planner.db import TaskDB
from soul_planner.models import Priority
from soul_planner.scheduler import parse_planner, schedule_tasks

SAMPLE_PLANNER = """\
# Soul Ecosystem -- Daily Planner

**Current Phase:** Phase 1 -- soul-planner

## Day 1 -- Sat Feb 22

### Block 1: BUILD -- soul-mesh continued (9am-1pm)
- [x] Review soul-mesh current state
- [x] Identify next modules to extract

---

## Day 2 -- Sun Feb 23

### Block 1: BUILD -- Strategy redesign (9am-1pm)
- [x] Redesign dev strategy
- [ ] Create repo structure
- [ ] Define SQLite schema
- [ ] Implement db.py

### Block 2: EXPLORE -- Research (2pm-6pm)
- [ ] Research Claude Code patterns
- [ ] Study task management

### Block 3: SOCIAL -- Content (7pm-9pm)
- [ ] Draft LinkedIn post
- [-] Skipped task

### Block 4: SCOUT -- Job portals (9pm-11pm)
- [ ] Create Naukri profile

### Evening Review (11pm, 15min)
- [ ] Review done?

---

## Day 3 -- Mon Feb 24

### Block 1: BUILD -- task model (9am-1pm)
- [ ] Day 3 task
"""


class TestParsePlanner:
    """Test the planner parser."""

    def test_parse_target_date(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 23))
        titles = [t["title"] for t in tasks]
        assert "Create repo structure" in titles
        assert "Define SQLite schema" in titles
        assert "Implement db.py" in titles
        assert "Research Claude Code patterns" in titles
        assert "Draft LinkedIn post" in titles
        assert "Create Naukri profile" in titles

    def test_skips_completed_tasks(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 23))
        titles = [t["title"] for t in tasks]
        assert "Redesign dev strategy" not in titles

    def test_skips_skipped_tasks(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 23))
        titles = [t["title"] for t in tasks]
        assert "Skipped task" not in titles

    def test_block_filter(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 23), block_filter=1)
        titles = [t["title"] for t in tasks]
        assert "Create repo structure" in titles
        assert "Research Claude Code patterns" not in titles

    def test_block_priorities(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 23))
        by_title = {t["title"]: t for t in tasks}
        assert by_title["Create repo structure"]["priority"] == Priority.HIGH  # Block 1
        assert by_title["Research Claude Code patterns"]["priority"] == Priority.NORMAL  # Block 2
        assert by_title["Create Naukri profile"]["priority"] == Priority.LOW  # Block 4

    def test_no_tasks_for_missing_date(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 3, 15))
        assert tasks == []

    def test_different_day(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 22))
        # Day 1 has all [x] tasks, so none should be returned
        assert tasks == []

    def test_does_not_include_evening_review(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 23))
        titles = [t["title"] for t in tasks]
        assert "Review done?" not in titles

    def test_stops_at_day_boundary(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 23))
        titles = [t["title"] for t in tasks]
        assert "Day 3 task" not in titles

    def test_block_number_preserved(self):
        tasks = parse_planner(SAMPLE_PLANNER, date(2026, 2, 23))
        by_title = {t["title"]: t for t in tasks}
        assert by_title["Create repo structure"]["block"] == 1
        assert by_title["Research Claude Code patterns"]["block"] == 2
        assert by_title["Draft LinkedIn post"]["block"] == 3
        assert by_title["Create Naukri profile"]["block"] == 4


class TestScheduleTasks:
    """Test the async scheduler."""

    @pytest.fixture
    async def db(self):
        db = TaskDB(":memory:")
        await db.init()
        return db

    async def test_schedule_creates_tasks(self, db, tmp_path):
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(SAMPLE_PLANNER)

        ids = await schedule_tasks(db, planner_path=planner_file, target_date=date(2026, 2, 23))
        assert len(ids) > 0

        tasks = await db.list()
        titles = [t.title for t in tasks]
        assert "Create repo structure" in titles
        assert "Define SQLite schema" in titles

    async def test_schedule_skips_duplicates(self, db, tmp_path):
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(SAMPLE_PLANNER)

        # Schedule once
        ids1 = await schedule_tasks(db, planner_path=planner_file, target_date=date(2026, 2, 23))
        # Schedule again -- should skip duplicates
        ids2 = await schedule_tasks(db, planner_path=planner_file, target_date=date(2026, 2, 23))
        assert len(ids2) == 0

        tasks = await db.list()
        assert len(tasks) == len(ids1)

    async def test_schedule_with_block_filter(self, db, tmp_path):
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(SAMPLE_PLANNER)

        await schedule_tasks(db, planner_path=planner_file, target_date=date(2026, 2, 23), block_filter=1)
        tasks = await db.list()
        # Only Block 1 tasks
        for t in tasks:
            assert "Block 1" in t.description

    async def test_schedule_empty_date(self, db, tmp_path):
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(SAMPLE_PLANNER)

        ids = await schedule_tasks(db, planner_path=planner_file, target_date=date(2026, 3, 15))
        assert ids == []

    async def test_schedule_sets_priority(self, db, tmp_path):
        planner_file = tmp_path / "daily-planner.md"
        planner_file.write_text(SAMPLE_PLANNER)

        await schedule_tasks(db, planner_path=planner_file, target_date=date(2026, 2, 23))
        tasks = await db.list()
        by_title = {t.title: t for t in tasks}
        assert by_title["Create repo structure"].priority == Priority.HIGH
        assert by_title["Create Naukri profile"].priority == Priority.LOW
