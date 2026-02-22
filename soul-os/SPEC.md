# soul-os

## Overview
AI-native operating system — the foundational monolith from which the entire soul ecosystem is extracted.

## Status
**Production** | ~6,700 lines Python + ~3,000 lines React

## Description
soul-os is the original AI-native OS containing 18 extractable components. It serves as the source codebase for extracting standalone projects (soul-mesh, soul-agents, soul-outreach, etc.). The system includes:

- Agent framework with boundary enforcement
- Mesh networking (hub election, WebSocket sync, NAT relay)
- Outreach/CRM pipeline (campaigns, drafts, email sending, reply ingestion)
- Consulting pipeline (leads, discovery, proposals, engagements)
- Knowledge base (ChromaDB)
- Authentication (JWT)
- CLI + Web UI

## Key Paths
- `/home/rishav/soul-os/brain/` — Core Python backend
- `/home/rishav/soul-os/brain/modules/outreach/` — Outreach module (source for soul-outreach extraction)
- `/home/rishav/soul-os/brain/mesh/` — Mesh networking (source for soul-mesh extraction)
- `/home/rishav/soul-os/brain/agents/` — Agent framework (source for soul-agents extraction)
- `/home/rishav/soul-os/brain/config.py` — Configuration reference
- `/home/rishav/soul-os/brain/auth/jwt.py` — JWT auth reference

## Role in Ecosystem
Source monolith. All standalone extractions should replace `brain.*` imports with their own modules. soul-os continues as the integration layer but individual components gain independent life as open-source projects.

## Portfolio Signal
"You ship production systems, not demos" — 6,700 lines across 17 phases demonstrates real engineering.
