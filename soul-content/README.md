# soul-content

> AI content pipeline with research ingestion, social drafts, and approval queue.

| Field | Value |
|-------|-------|
| Type | **PRIVATE** |
| Category | Product |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/modules/content/` |
| License | Proprietary |

## What It Is

A content generation pipeline that ingests structured research results into the knowledge base, generates social content drafts (LinkedIn, blog, Twitter) using a social_writer AI agent, and routes drafts through an approval queue before publishing.

## Pipeline

```
Research Results (JSON) -> ChromaDB ingestion -> Knowledge enrichment
    |
    v
Draft Generation (social_writer agent) -> content_drafts table
    |
    v
Approval Queue -> human review -> publish with URL tracking
```

### Components

| File | Purpose |
|------|---------|
| research_ingest.py | Structured JSON -> ChromaDB + knowledge table |
| drafts.py | Social content drafts with approval queue (atomic rate limits) |
| cli.py | CLI: ingest-results, draft-post, list-drafts, publish-draft |

### Agent

`social_writer.yaml` — LinkedIn, blog, Twitter content writer with platform-specific formatting.

### Deployment

`soul-os-content.timer` — Bi-weekly content flywheel (systemd timer).

## Strategic Value

Automates technical content creation. Content feeds soul-blog and LinkedIn presence, which drives visibility for job search and consulting.
