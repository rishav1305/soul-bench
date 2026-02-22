# soul-web

> React 19 Progressive Web App with 8 pages, dark theme, and WebSocket streaming.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | App |
| Status | Production (in soul-os) |
| Source | `~/soul-os/frontend/` |
| License | MIT |

## What It Is

The shared frontend for soul-os, built as a React PWA. Same codebase serves web, desktop (via Tauri), Android (via WebView), and iOS (via WKWebView). Features streaming chat with Claude via WebSocket, system dashboard, task board, and approval queue.

## Pages

| Page | Purpose |
|------|---------|
| Chat | Streaming conversation with Claude (ThinkingBlock, ToolCallCard) |
| Dashboard | System health, resource pool, mesh status |
| TaskBoard | Task list with status tracking |
| Approvals | Pending items requiring human review |
| Devices | Mesh device management |
| Outreach | Campaign status, draft review |
| Knowledge | Knowledge base search |
| Settings | Resource limits, API key, account |

## Tech Stack

- React 18 + Vite
- Dark theme (bg: #0d0d0d, accent: #7C3AED)
- WebSocket for streaming Claude responses
- Responsive (320px mobile to 4K desktop)
- Service worker with network-first caching + 503 offline fallback
- PWA install prompt + offline indicator

### Key Features

- `manifest.json` for "Add to Home Screen"
- Service worker v2 with precaching
- Online/offline event handling
- Served by FastAPI via `StaticFiles` mount (one process, one port)

## Strategic Value

Demonstrates full-stack capability. One React app that ships to web, desktop, mobile — shows efficient cross-platform thinking.
