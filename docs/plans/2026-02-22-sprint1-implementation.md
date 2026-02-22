# Sprint 1 Implementation Plan (Weeks 1-2)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extract soul-search and soul-import from the soul-app backup into standalone projects, scaffold soul-query and soul-viz from the delve-ai specs, and create project stubs in ~/soul/ for all four.

**Architecture:** Each project follows the soul extraction pattern: standalone Python package with pyproject.toml, pydantic-settings config, no `brain.*` or `soul.*` imports, pytest tests, and a README. Code is copied from the soul-app backup on titan-pc (192.168.0.113), then refactored to be standalone.

**Tech Stack:** Python 3.11+, pydantic-settings, httpx, aiosqlite, pytest, pytest-asyncio

**Source backup:** `/mnt/vault/backups/titan-pi-migration/configs/soul-app.tar.gz` on titan-pc (SSH: `ssh -p 22 rishav@192.168.0.113`)

---

## Task 1: Extract soul-search source files from backup

**Files:**
- Create: `~/soul/soul-search/` (entire directory tree)

**Step 1: Create project directory structure**

```bash
mkdir -p ~/soul/soul-search/soul_search
mkdir -p ~/soul/soul-search/tests
```

**Step 2: Extract source files from titan-pc backup**

```bash
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/search/base.py'" > ~/soul/soul-search/soul_search/base.py
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/search/models.py'" > ~/soul/soul-search/soul_search/models.py
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/search/aggregator.py'" > ~/soul/soul-search/soul_search/aggregator.py
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/search/duckduckgo.py'" > ~/soul/soul-search/soul_search/duckduckgo.py
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/search/brave.py'" > ~/soul/soul-search/soul_search/brave.py
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/search/tavily.py'" > ~/soul/soul-search/soul_search/tavily.py
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/search/cache.py'" > ~/soul/soul-search/soul_search/cache.py
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/search/playwright_google.py'" > ~/soul/soul-search/soul_search/playwright_google.py
```

**Step 3: Verify extraction**

Run: `ls -la ~/soul/soul-search/soul_search/`
Expected: 8 .py files (base, models, aggregator, duckduckgo, brave, tavily, cache, playwright_google)

Run: `grep -r "from soul\." ~/soul/soul-search/soul_search/`
Expected: Multiple hits (these will be fixed in Task 2)

**Step 4: Commit raw extraction**

```bash
cd ~/soul/soul-search
git init
git add -A
git commit -m "chore: raw extraction of search module from soul-app backup"
```

---

## Task 2: Make soul-search standalone (remove soul.* imports)

**Files:**
- Modify: `~/soul/soul-search/soul_search/aggregator.py` (remove `soul.config.Settings` dependency, replace with pydantic-settings)
- Modify: `~/soul/soul-search/soul_search/base.py` (fix internal imports)
- Modify: `~/soul/soul-search/soul_search/models.py` (no changes expected)
- Modify: `~/soul/soul-search/soul_search/duckduckgo.py` (fix imports)
- Modify: `~/soul/soul-search/soul_search/brave.py` (fix imports)
- Modify: `~/soul/soul-search/soul_search/tavily.py` (fix imports)
- Modify: `~/soul/soul-search/soul_search/cache.py` (fix imports)
- Modify: `~/soul/soul-search/soul_search/playwright_google.py` (fix imports)
- Create: `~/soul/soul-search/soul_search/config.py`
- Create: `~/soul/soul-search/soul_search/__init__.py`

**Step 1: Create config.py with pydantic-settings**

Create `~/soul/soul-search/soul_search/config.py`:
```python
"""Configuration for soul-search — all settings via SEARCH_ env vars."""
from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "SEARCH_"}

    # Comma-separated provider names: duckduckgo,brave,tavily,google_playwright
    providers: str = "duckduckgo"

    # API keys (optional per provider)
    brave_api_key: str = ""
    tavily_api_key: str = ""

    # Cache
    cache_ttl_s: int = 60

    # Browser (for Playwright Google provider)
    enable_browser: bool = False


settings = Settings()
```

**Step 2: Fix all `soul.*` imports to `soul_search.*`**

In every .py file under `soul_search/`:
- Replace `from soul.search.` with `from soul_search.`
- Replace `from soul.config import Settings` with `from soul_search.config import Settings`
- Replace `settings.soul_search_providers` with `settings.providers`
- Replace `settings.soul_brave_search_api_key` with `settings.brave_api_key`
- Replace `settings.soul_tavily_api_key` with `settings.tavily_api_key`
- Replace `settings.soul_search_cache_ttl_s` with `settings.cache_ttl_s`
- Replace `settings.soul_enable_browser` with `settings.enable_browser`

**Step 3: Create __init__.py**

Create `~/soul/soul-search/soul_search/__init__.py`:
```python
"""soul-search — multi-provider web search with aggregation."""
from soul_search.aggregator import SearchAggregator
from soul_search.base import SearchProviderBase
from soul_search.models import AggregatedResults, SearchProviderName, SearchResult

__all__ = [
    "AggregatedResults",
    "SearchAggregator",
    "SearchProviderBase",
    "SearchProviderName",
    "SearchResult",
]
```

**Step 4: Verify no soul.* imports remain**

Run: `grep -rn "from soul\." ~/soul/soul-search/soul_search/ | grep -v "soul_search"`
Expected: ZERO results

Run: `grep -rn "import soul\." ~/soul/soul-search/soul_search/`
Expected: ZERO results

**Step 5: Commit standalone conversion**

```bash
cd ~/soul/soul-search
git add -A
git commit -m "refactor: make soul-search standalone (replace soul.* imports)"
```

---

## Task 3: Add pyproject.toml, README, and project config for soul-search

**Files:**
- Create: `~/soul/soul-search/pyproject.toml`
- Create: `~/soul/soul-search/README.md`
- Create: `~/soul/soul-search/CLAUDE.md`

**Step 1: Create pyproject.toml**

Create `~/soul/soul-search/pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.build_meta"

[project]
name = "soul-search"
version = "0.1.0"
description = "Multi-provider web search aggregator with deduplication and scoring."
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [{name = "Rishav"}]
keywords = ["search", "web", "aggregator", "duckduckgo", "brave", "tavily"]

dependencies = [
    "pydantic-settings>=2.7.0",
    "httpx>=0.28",
]

[project.optional-dependencies]
duckduckgo = ["duckduckgo-search>=7.0"]
playwright = ["playwright>=1.40"]
all = ["duckduckgo-search>=7.0", "playwright>=1.40"]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "ruff>=0.8.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["soul_search*"]

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Step 2: Create README.md**

Create `~/soul/soul-search/README.md` with: project name, one-line description, features list (multi-provider, dedup, scoring, caching), quick start (install, configure env vars, usage example), provider table (DuckDuckGo free, Brave 1000/mo free, Tavily free tier, Google Playwright fallback), and config reference (SEARCH_ prefix env vars).

**Step 3: Create CLAUDE.md**

Create `~/soul/soul-search/CLAUDE.md` with: architecture overview, key files table, config reference, conventions (no soul.* imports, SEARCH_ prefix, async-first, httpx for HTTP).

**Step 4: Commit**

```bash
cd ~/soul/soul-search
git add -A
git commit -m "feat: add pyproject.toml, README, and CLAUDE.md"
```

---

## Task 4: Write tests for soul-search

**Files:**
- Create: `~/soul/soul-search/tests/__init__.py`
- Create: `~/soul/soul-search/tests/test_models.py`
- Create: `~/soul/soul-search/tests/test_cache.py`
- Create: `~/soul/soul-search/tests/test_aggregator.py`

**Step 1: Write test_models.py**

```python
"""Tests for search data models."""
from soul_search.models import AggregatedResults, SearchProviderName, SearchResult


def test_search_result_to_dict():
    r = SearchResult(title="Test", url="https://example.com", snippet="A snippet", provider="brave", score=1.2)
    d = r.to_dict()
    assert d["title"] == "Test"
    assert d["url"] == "https://example.com"
    assert d["score"] == 1.2


def test_search_result_defaults():
    r = SearchResult(title="T", url="https://x.com")
    assert r.snippet == ""
    assert r.provider == ""
    assert r.score == 0.0


def test_aggregated_results_to_dict():
    r = AggregatedResults(
        results=[SearchResult(title="A", url="https://a.com")],
        query="test",
        providers_used=["brave"],
        total_raw=5,
    )
    d = r.to_dict()
    assert d["query"] == "test"
    assert d["result_count"] == 1
    assert d["total_raw"] == 5


def test_provider_names():
    assert SearchProviderName.DUCKDUCKGO.value == "duckduckgo"
    assert SearchProviderName.BRAVE.value == "brave"
    assert SearchProviderName.TAVILY.value == "tavily"
```

**Step 2: Write test_cache.py**

```python
"""Tests for search cache."""
import time
from unittest.mock import patch

from soul_search.cache import SearchCache
from soul_search.models import AggregatedResults, SearchResult


def test_cache_put_and_get():
    cache = SearchCache(ttl_seconds=60)
    results = AggregatedResults(results=[SearchResult(title="A", url="https://a.com")], query="q")
    key = cache._make_key("test query", 10)
    cache.put(key, results)
    got = cache.get(key)
    assert got is not None
    assert got.query == "q"


def test_cache_miss():
    cache = SearchCache(ttl_seconds=60)
    assert cache.get("nonexistent") is None


def test_cache_expiry():
    cache = SearchCache(ttl_seconds=1)
    results = AggregatedResults(query="q")
    key = "test_key"
    cache.put(key, results)
    assert cache.get(key) is not None

    with patch("soul_search.cache.time") as mock_time:
        mock_time.monotonic.return_value = time.monotonic() + 100
        assert cache.get(key) is None


def test_cache_clear():
    cache = SearchCache(ttl_seconds=60)
    cache.put("k1", AggregatedResults(query="a"))
    cache.put("k2", AggregatedResults(query="b"))
    cache.clear()
    assert cache.get("k1") is None
    assert cache.get("k2") is None


def test_make_key_normalizes():
    cache = SearchCache()
    assert cache._make_key("  Hello World  ", 10) == "hello world|10"
    assert cache._make_key("Hello World", 5) == "hello world|5"
```

**Step 3: Write test_aggregator.py**

```python
"""Tests for search aggregator scoring and dedup logic."""
from soul_search.aggregator import _normalize_url, _score_and_dedupe
from soul_search.models import SearchResult


def test_normalize_url_strips_www():
    assert _normalize_url("https://www.example.com/page") == "example.com/page"


def test_normalize_url_strips_trailing_slash():
    assert _normalize_url("https://example.com/page/") == "example.com/page"


def test_normalize_url_lowercases():
    assert _normalize_url("https://Example.COM/Page") == "example.com/page"


def test_score_and_dedupe_keeps_highest():
    items = [
        ("brave", 0, SearchResult(title="A", url="https://example.com/page")),
        ("duckduckgo", 0, SearchResult(title="A alt", url="https://www.example.com/page")),
    ]
    results = _score_and_dedupe(items)
    assert len(results) == 1
    # Brave has weight 1.2 at rank 0 = 1.2, DDG has weight 1.0 at rank 0 = 1.0
    assert results[0].provider == "brave"


def test_score_and_dedupe_different_urls():
    items = [
        ("brave", 0, SearchResult(title="A", url="https://a.com")),
        ("brave", 1, SearchResult(title="B", url="https://b.com")),
    ]
    results = _score_and_dedupe(items)
    assert len(results) == 2


def test_score_and_dedupe_empty():
    assert _score_and_dedupe([]) == []
```

**Step 4: Run tests**

Run: `cd ~/soul/soul-search && pip install -e ".[dev,duckduckgo]" && pytest tests/ -v`
Expected: All tests pass

**Step 5: Commit**

```bash
cd ~/soul/soul-search
git add -A
git commit -m "test: add unit tests for models, cache, and aggregator"
```

---

## Task 5: Extract soul-import source files from backup

**Files:**
- Create: `~/soul/soul-import/` (entire directory tree)

**Step 1: Create project directory structure**

```bash
mkdir -p ~/soul/soul-import/soul_import
mkdir -p ~/soul/soul-import/tests
```

**Step 2: Extract source files from titan-pc backup**

```bash
for f in chatgpt.py claude.py rss_intake.py url_intake.py email_intake.py csv_intake.py drive.py; do
    ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/importers/$f'" > ~/soul/soul-import/soul_import/$f
done
```

Also extract the importers CLAUDE.md if present:
```bash
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'soul/importers/CLAUDE.md'" > ~/soul/soul-import/docs/IMPORTERS_CLAUDE.md 2>/dev/null || true
```

**Step 3: Verify extraction**

Run: `ls -la ~/soul/soul-import/soul_import/`
Expected: 7 .py files

**Step 4: Commit raw extraction**

```bash
cd ~/soul/soul-import
git init
git add -A
git commit -m "chore: raw extraction of importers module from soul-app backup"
```

---

## Task 6: Make soul-import standalone (remove soul.* imports)

**Files:**
- Modify: all .py files in `~/soul/soul-import/soul_import/`
- Create: `~/soul/soul-import/soul_import/config.py`
- Create: `~/soul/soul-import/soul_import/__init__.py`
- Create: `~/soul/soul-import/soul_import/store.py` (abstract interface replacing `soul.memory.store.MemoryStore`)

**Step 1: Create store.py — abstract storage interface**

The original importers depend on `soul.memory.store.MemoryStore`. Create a minimal abstract interface so importers work with any storage backend.

```python
"""Abstract storage interface for importers."""
from __future__ import annotations

import abc


class ImportStore(abc.ABC):
    """Minimal interface that importers need from a storage backend."""

    @abc.abstractmethod
    async def begin_import(self, *, source: str, file_hash: str) -> tuple[int, bool]:
        """Start an import. Returns (import_id, already_done)."""

    @abc.abstractmethod
    async def finish_import(self, *, import_id: int, messages_imported: int, facts_extracted: int) -> None:
        """Mark an import as complete."""

    @abc.abstractmethod
    async def delete_messages_by_import_id(self, import_id: int) -> None:
        """Delete all messages from a previous import attempt."""

    @abc.abstractmethod
    async def upsert_session(self, *, session_id: str, title: str | None = None, commit: bool = True) -> None:
        """Create or update a conversation session."""

    @abc.abstractmethod
    async def add_message(
        self, *, session_id: str, role: str, content: str, import_id: int | None = None, commit: bool = True
    ) -> None:
        """Add a message to a session."""

    @abc.abstractmethod
    async def commit(self) -> None:
        """Commit pending changes."""
```

**Step 2: Create config.py**

```python
"""Configuration for soul-import — all settings via IMPORT_ env vars."""
from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "IMPORT_"}

    # Google Drive credentials path (optional)
    google_credentials_path: str = ""

    # RSS feed timeout
    rss_timeout_s: int = 30


settings = Settings()
```

**Step 3: Fix all soul.* imports**

In every .py file under `soul_import/`:
- Replace `from soul.memory.store import MemoryStore` with `from soul_import.store import ImportStore`
- Replace all `MemoryStore` type hints with `ImportStore`
- Replace `store.conn.commit()` with `await store.commit()`
- Replace any `from soul.` with appropriate `from soul_import.` equivalents

**Step 4: Create __init__.py**

```python
"""soul-import — conversation importers for ChatGPT, Claude, RSS, email, CSV, and more."""
from soul_import.store import ImportStore

__all__ = ["ImportStore"]
```

**Step 5: Verify no soul.* imports remain**

Run: `grep -rn "from soul\." ~/soul/soul-import/soul_import/ | grep -v "soul_import"`
Expected: ZERO results

**Step 6: Commit**

```bash
cd ~/soul/soul-import
git add -A
git commit -m "refactor: make soul-import standalone (abstract ImportStore, remove soul.* imports)"
```

---

## Task 7: Add pyproject.toml, README, CLAUDE.md for soul-import

**Files:**
- Create: `~/soul/soul-import/pyproject.toml`
- Create: `~/soul/soul-import/README.md`
- Create: `~/soul/soul-import/CLAUDE.md`

**Step 1: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.build_meta"

[project]
name = "soul-import"
version = "0.1.0"
description = "Conversation importers for ChatGPT, Claude, RSS, email, CSV, and Google Drive."
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [{name = "Rishav"}]
keywords = ["import", "chatgpt", "claude", "rss", "email", "csv", "conversations"]

dependencies = [
    "pydantic-settings>=2.7.0",
    "aiosqlite>=0.20.0",
]

[project.optional-dependencies]
rss = ["feedparser>=6.0"]
drive = [
    "google-auth>=2.0.0",
    "google-auth-oauthlib>=1.0.0",
    "google-api-python-client>=2.0.0",
]
all = [
    "feedparser>=6.0",
    "google-auth>=2.0.0",
    "google-auth-oauthlib>=1.0.0",
    "google-api-python-client>=2.0.0",
]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "ruff>=0.8.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["soul_import*"]

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Step 2: Create README.md and CLAUDE.md**

README.md: project name, description, supported importers table (ChatGPT ZIP, Claude ZIP/JSON, RSS, URL, email MBOX, CSV, Google Drive), quick start, config reference.

CLAUDE.md: architecture overview, key files table, conventions (ImportStore interface, no soul.* imports, IMPORT_ prefix).

**Step 3: Commit**

```bash
cd ~/soul/soul-import
git add -A
git commit -m "feat: add pyproject.toml, README, and CLAUDE.md"
```

---

## Task 8: Write tests for soul-import

**Files:**
- Create: `~/soul/soul-import/tests/__init__.py`
- Create: `~/soul/soul-import/tests/test_chatgpt.py`
- Create: `~/soul/soul-import/tests/test_claude.py`
- Create: `~/soul/soul-import/tests/conftest.py`

**Step 1: Create conftest.py with mock ImportStore**

```python
"""Shared test fixtures for soul-import."""
import pytest
from soul_import.store import ImportStore


class MockStore(ImportStore):
    """In-memory mock store for testing importers."""

    def __init__(self):
        self.imports = {}
        self.sessions = {}
        self.messages = []
        self._next_import_id = 1
        self._committed = False

    async def begin_import(self, *, source: str, file_hash: str) -> tuple[int, bool]:
        key = f"{source}:{file_hash}"
        if key in self.imports and self.imports[key]["done"]:
            return self.imports[key]["id"], True
        iid = self._next_import_id
        self._next_import_id += 1
        self.imports[key] = {"id": iid, "done": False, "source": source}
        return iid, False

    async def finish_import(self, *, import_id: int, messages_imported: int, facts_extracted: int) -> None:
        for v in self.imports.values():
            if v["id"] == import_id:
                v["done"] = True

    async def delete_messages_by_import_id(self, import_id: int) -> None:
        self.messages = [m for m in self.messages if m.get("import_id") != import_id]

    async def upsert_session(self, *, session_id: str, title: str | None = None, commit: bool = True) -> None:
        self.sessions[session_id] = {"title": title}

    async def add_message(
        self, *, session_id: str, role: str, content: str, import_id: int | None = None, commit: bool = True
    ) -> None:
        self.messages.append({"session_id": session_id, "role": role, "content": content, "import_id": import_id})

    async def commit(self) -> None:
        self._committed = True


@pytest.fixture
def mock_store():
    return MockStore()
```

**Step 2: Write test_chatgpt.py**

Test the internal parsing functions (_load_conversations, _iter_conversation_messages, _content_to_text, _normalize_role) using synthetic data. Create a temp ZIP with a minimal conversations.json and test the full import flow against MockStore.

**Step 3: Write test_claude.py**

Similar pattern: test internal parsing with synthetic Claude export data.

**Step 4: Run tests**

Run: `cd ~/soul/soul-import && pip install -e ".[dev]" && pytest tests/ -v`
Expected: All tests pass

**Step 5: Commit**

```bash
cd ~/soul/soul-import
git add -A
git commit -m "test: add unit tests for chatgpt and claude importers"
```

---

## Task 9: Scaffold soul-query from delve-ai specs

**Files:**
- Create: `~/soul/soul-query/` (entire directory tree)

**Step 1: Create project structure**

```bash
mkdir -p ~/soul/soul-query/soul_query
mkdir -p ~/soul/soul-query/tests
mkdir -p ~/soul/soul-query/docs/decisions
```

**Step 2: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.build_meta"

[project]
name = "soul-query"
version = "0.1.0"
description = "AI-powered NL-to-SQL engine with schema guardrails."
readme = "README.md"
license = {text = "BSL-1.1"}
requires-python = ">=3.11"
authors = [{name = "Rishav"}]
keywords = ["nlsql", "query", "sql", "ai", "guardrails", "redshift", "athena"]

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "pydantic-settings>=2.7.0",
    "aiosqlite>=0.20.0",
    "anthropic>=0.52.0",
    "structlog>=24.0.0",
    "httpx>=0.28",
]

[project.optional-dependencies]
redshift = ["boto3>=1.34"]
athena = ["boto3>=1.34"]
all = ["boto3>=1.34"]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "httpx>=0.28",
    "ruff>=0.8.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["soul_query*"]

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Step 3: Create config.py**

```python
"""Configuration for soul-query — all settings via QUERY_ env vars."""
from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "QUERY_"}

    # API
    host: str = "127.0.0.1"
    port: int = 8100
    data_dir: str = "./data"

    # Anthropic
    anthropic_api_key: str = ""
    model: str = "claude-sonnet-4-20250514"

    # Schema guardrails
    schema_whitelist_path: str = "./schema_whitelist.yaml"

    # Query engines
    default_engine: str = "redshift"  # or "athena"

    # AWS (for Redshift/Athena)
    aws_region: str = "us-east-1"
    redshift_cluster: str = ""
    redshift_database: str = ""
    redshift_user: str = ""
    athena_database: str = ""
    athena_output_bucket: str = ""


settings = Settings()
```

**Step 4: Create core module stubs**

Create `soul_query/__init__.py`, `soul_query/guardrails.py` (table whitelist + schema context), `soul_query/generator.py` (NL-to-SQL via Anthropic), `soul_query/engine.py` (abstract query engine base), `soul_query/engines/redshift.py`, `soul_query/engines/athena.py`, `soul_query/router.py` (intent classification + engine routing).

Each stub should have the class/function signatures with docstrings and `raise NotImplementedError` bodies.

**Step 5: Migrate delve-ai specs to docs/**

Copy brief.md, backlog.md, decisions.md from the backup:
```bash
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'projects/delve-ai/brief.md'" > ~/soul/soul-query/docs/BRIEF.md
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'projects/delve-ai/backlog.md'" > ~/soul/soul-query/docs/BACKLOG.md
ssh -p 22 rishav@192.168.0.113 "cd /mnt/vault/backups/titan-pi-migration/configs && tar -xzf soul-app.tar.gz --to-stdout 'projects/delve-ai/decisions.md'" > ~/soul/soul-query/docs/decisions/README.md
```

**Step 6: Create README.md and CLAUDE.md**

README.md: project name, description (from delve-ai brief), architecture overview, features (NL-to-SQL, schema guardrails, dual engine support, query history), quick start, config reference.

CLAUDE.md: full architecture, key files, security invariants (whitelist-only schema access, all AI calls through single client, query validation before execution), conventions.

**Step 7: Init git and commit**

```bash
cd ~/soul/soul-query
git init
git add -A
git commit -m "feat: scaffold soul-query from delve-ai specs (NL-to-SQL with guardrails)"
```

---

## Task 10: Scaffold soul-viz from delve-ai backlog

**Files:**
- Create: `~/soul/soul-viz/` (entire directory tree)

**Step 1: Create project structure**

```bash
mkdir -p ~/soul/soul-viz/soul_viz
mkdir -p ~/soul/soul-viz/tests
```

**Step 2: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.build_meta"

[project]
name = "soul-viz"
version = "0.1.0"
description = "Prompt-to-visualization engine for data analytics."
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [{name = "Rishav"}]
keywords = ["visualization", "charts", "dashboard", "analytics", "ai"]

dependencies = [
    "pydantic-settings>=2.7.0",
    "anthropic>=0.52.0",
    "structlog>=24.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "ruff>=0.8.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["soul_viz*"]

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Step 3: Create config.py and module stubs**

Create `soul_viz/config.py` (VIZ_ prefix), `soul_viz/__init__.py`, `soul_viz/chart.py` (chart type selection + spec generation), `soul_viz/dashboard.py` (layout generation from prompt), `soul_viz/models.py` (ChartSpec, DashboardSpec pydantic models).

**Step 4: Create README.md and CLAUDE.md**

**Step 5: Init git and commit**

```bash
cd ~/soul/soul-viz
git init
git add -A
git commit -m "feat: scaffold soul-viz (prompt-to-visualization engine)"
```

---

## Task 11: Update ~/soul/ ecosystem docs

**Files:**
- Modify: `~/soul/CLAUDE.md` (add soul-search, soul-import, soul-query, soul-viz to project table; update count to 37)
- Modify: `~/soul/docs/ecosystem-map.md` (add 4 new projects)
- Modify: `~/soul/.gitignore` (add soul-search/, soul-import/, soul-query/, soul-viz/)
- Modify: `~/.claude/projects/-home-rishav-soul/memory/MEMORY.md` (update project state)

**Step 1: Update CLAUDE.md project table**

Add to "From soul-os" section:
```
| 32 | soul-search | PUBLIC | Has Code | Multi-provider web search aggregator |
| 33 | soul-import | PUBLIC | Has Code | Conversation importers (ChatGPT, Claude, RSS, email) |
```

Add new section "From delve-ai (2)":
```
| 34 | soul-query | PUBLIC | Scaffolded | NL-to-SQL engine with schema guardrails |
| 35 | soul-viz | PUBLIC | Scaffolded | Prompt-to-visualization engine |
```

Update total count from 33 to 37.

**Step 2: Update .gitignore**

Add:
```
soul-search/
soul-import/
soul-query/
soul-viz/
```

**Step 3: Update ecosystem-map.md**

Add entries for all 4 new projects.

**Step 4: Update MEMORY.md**

Add soul-search and soul-import extraction status, soul-query and soul-viz scaffold status.

**Step 5: Commit to soul/ umbrella repo**

```bash
cd ~/soul
git add CLAUDE.md .gitignore docs/ecosystem-map.md
git commit -m "docs: add soul-search, soul-import, soul-query, soul-viz to ecosystem (37 projects)"
```

---

## Task 12: Push all new repos to Gitea

**Step 1: Push soul-search**

```bash
cd ~/soul/soul-search
git remote add origin ssh://git@git.titan.local:222/rishav/soul-search.git
git push -u origin master
```

**Step 2: Push soul-import**

```bash
cd ~/soul/soul-import
git remote add origin ssh://git@git.titan.local:222/rishav/soul-import.git
git push -u origin master
```

**Step 3: Push soul-query**

```bash
cd ~/soul/soul-query
git remote add origin ssh://git@git.titan.local:222/rishav/soul-query.git
git push -u origin master
```

**Step 4: Push soul-viz**

```bash
cd ~/soul/soul-viz
git remote add origin ssh://git@git.titan.local:222/rishav/soul-viz.git
git push -u origin master
```

**Step 5: Push soul/ umbrella**

```bash
cd ~/soul
git push origin master
```

**Step 6: Verify**

Run: `for repo in soul-search soul-import soul-query soul-viz; do echo "$repo:"; cd ~/soul/$repo && git remote -v && git log --oneline | head -3; echo; done`
Expected: Each repo has Gitea remote and 3-4 commits

---

## Summary

| Task | What | Type | Commits |
|------|------|------|---------|
| 1-4 | soul-search extraction + tests | Full extraction | 4 |
| 5-8 | soul-import extraction + tests | Full extraction | 4 |
| 9 | soul-query scaffold | Scaffold from spec | 1 |
| 10 | soul-viz scaffold | Scaffold from spec | 1 |
| 11 | Ecosystem docs update | Documentation | 1 |
| 12 | Push to Gitea | Deployment | 0 (pushes) |

**Total: 12 tasks, ~11 commits, 4 new projects**
