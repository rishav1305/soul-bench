# soul-consult

> AI-powered consulting CRM with lead qualification, discovery prep, and proposal generation.

| Field | Value |
|-------|-------|
| Type | **PRIVATE** |
| Category | Product |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/modules/outreach/consulting.py` |
| License | Proprietary |

## What It Is

A consulting pipeline management tool built into soul-os. Manages the full lifecycle: create leads, prepare discovery calls with AI research, log discovery outcomes, generate grounded proposals, track engagements, and view pipeline statistics.

## CLI Commands

```bash
consulting create-lead --account-id 1 --contact-id 2
consulting prep-discovery --lead-id 1
consulting log-discovery --lead-id 1 --notes "..." --outcome qualified
consulting draft-proposal --lead-id 1 --package Shield
consulting log-engagement --lead-id 1 --package Shield
consulting pipeline
consulting stats
consulting load-catalog
```

## Data Model

Lead -> DiscoveryCall -> Proposal -> Engagement (all in growth.db)

## Service Packages

| Package | Focus | Target |
|---------|-------|--------|
| Shield | Risk, Compliance, Security | Legal, Healthcare, Finance |
| Magnet | Customer Experience, Retention | SaaS, Subscription |
| Engine | Innovation, R&D | R&D-heavy orgs |
| Brain | Knowledge Management | Enterprise |

## Strategic Value

Internal tool for managing consulting revenue stream. Demonstrates CRM design and AI-assisted sales workflows.
