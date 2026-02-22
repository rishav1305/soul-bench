# soul-knowledge

> Semantic search engine with ChromaDB vectors and SQLite full-text search.

| Field | Value |
|-------|-------|
| Type | **PRIVATE** |
| Category | Product |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/modules/knowledge/` |
| License | Proprietary |

## What It Is

A domain knowledge ingestion and search system combining ChromaDB vector embeddings with SQLite FTS5 full-text search. Supports URL/file ingestion with SSRF protection, automatic chunking, deduplication, and thread-safe operations.

## Components

| File | Purpose |
|------|---------|
| chromadb_store.py | ChromaDB wrapper (thread-safe, graceful degradation) |
| ingest.py | URL/file ingestion (SSRF-protected, chunked, deduped) |
| search.py | Unified semantic + keyword search |
| cve_scanner.py | Ubuntu CVE scanner (systemd timer) |
| orientation.py | Hardware/software self-orientation profiling |
| cli.py | CLI: ingest, search, cve-scan, orient, health |

### Domain Collections (ChromaDB)

system, security, networking, hardware, apps, business, outreach, research

## Strategic Value

Powers soul-os's knowledge base. Vertical knowledge bases (CVE, security) could become a standalone SaaS product. Demonstrates semantic search engineering and data pipeline design.
