"""Daily planner parser and task scheduler for soul-planner.

Reads ~/soul/docs/daily-planner.md, finds today's date section,
extracts uncompleted tasks from specified blocks, and queues them
into the soul-planner backlog.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import aiofiles
import structlog

from soul_planner.db import TaskDB
from soul_planner.models import Priority, TaskCreate

logger = structlog.get_logger("soul-planner.scheduler")

# Map block numbers to priorities
BLOCK_PRIORITY = {
    1: Priority.HIGH,     # BUILD
    2: Priority.NORMAL,   # EXPLORE
    3: Priority.NORMAL,   # SOCIAL
    4: Priority.LOW,      # SCOUT
}

# Month name mapping
MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

DEFAULT_PLANNER_PATH = Path.home() / "soul" / "docs" / "daily-planner.md"


def _parse_date_from_header(header: str) -> date | None:
    """Extract a date from a day header like 'Day 2 -- Sun Feb 23'."""
    m = re.search(r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\w+)\s+(\d+)", header)
    if not m:
        return None
    month_str = m.group(1).lower()[:3]
    day_num = int(m.group(2))
    month_num = MONTHS.get(month_str)
    if not month_num:
        return None
    # Assume current year
    return date(date.today().year, month_num, day_num)


def _extract_block_number(header: str) -> int | None:
    """Extract block number from a block header like '### Block 1: BUILD ...'."""
    m = re.match(r"###\s+Block\s+(\d+)", header)
    return int(m.group(1)) if m else None


def parse_planner(content: str, target_date: date, block_filter: int | None = None) -> list[dict]:
    """Parse daily planner content and extract uncompleted tasks.

    Args:
        content: Full text of daily-planner.md
        target_date: Date to find tasks for
        block_filter: If set, only extract tasks from this block number (1-4)

    Returns:
        List of dicts with keys: title, block, priority
    """
    lines = content.split("\n")
    tasks: list[dict] = []

    in_target_day = False
    current_block: int | None = None

    for line in lines:
        # Detect day headers: ## Day N -- Weekday Month Date
        if line.startswith("## Day "):
            header_date = _parse_date_from_header(line)
            in_target_day = header_date == target_date
            current_block = None
            continue

        if not in_target_day:
            continue

        # Detect next day section (exit)
        if line.startswith("---"):
            break

        # Detect block headers
        if line.startswith("### Block "):
            current_block = _extract_block_number(line)
            continue

        # Skip non-block sections (like Evening Review)
        if line.startswith("### ") and not line.startswith("### Block"):
            current_block = None
            continue

        # Only process if we're in a block
        if current_block is None:
            continue

        # Apply block filter
        if block_filter is not None and current_block != block_filter:
            continue

        # Extract uncompleted tasks: - [ ] task text
        m = re.match(r"^- \[ \] (.+)$", line.strip())
        if m:
            title = m.group(1).strip()
            tasks.append({
                "title": title,
                "block": current_block,
                "priority": BLOCK_PRIORITY.get(current_block, Priority.NORMAL),
            })

    return tasks


async def schedule_tasks(
    db: TaskDB,
    planner_path: Path | None = None,
    target_date: date | None = None,
    block_filter: int | None = None,
) -> list[int]:
    """Parse daily planner and queue uncompleted tasks.

    Args:
        db: TaskDB instance
        planner_path: Path to daily-planner.md (default: ~/soul/docs/daily-planner.md)
        target_date: Date to schedule for (default: today)
        block_filter: Only schedule tasks from this block (1-4)

    Returns:
        List of created task IDs
    """
    path = planner_path or DEFAULT_PLANNER_PATH
    today = target_date or date.today()

    # Validate path exists before reading
    if not path.exists():
        logger.error("Planner file not found", path=str(path))
        return []

    async with aiofiles.open(path, encoding="utf-8") as f:
        content = await f.read()
    parsed = parse_planner(content, today, block_filter)

    if not parsed:
        logger.info("No uncompleted tasks found", date=str(today), block=block_filter)
        return []

    # Check for duplicates
    existing = await db.list()
    existing_titles = {t.title for t in existing}

    created_ids: list[int] = []
    for item in parsed:
        if item["title"] in existing_titles:
            logger.debug("Skipping duplicate task", title=item["title"])
            continue

        task = await db.add(TaskCreate(
            title=item["title"],
            description=f"From daily planner, Block {item['block']}",
            priority=item["priority"],
        ))
        created_ids.append(task.id)
        existing_titles.add(item["title"])

    logger.info("Tasks scheduled", count=len(created_ids), date=str(today), block=block_filter)
    return created_ids
