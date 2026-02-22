# soul-desktop

> Tauri v2 cross-platform desktop app with system tray, brain lifecycle, and auto-update.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | App |
| Status | Production (in soul-os) |
| Source | `~/soul-os/desktop/` |
| License | MIT |

## What It Is

A native desktop wrapper for soul-os using Tauri v2. Loads the same React frontend in a native webview (~5MB binary, 10x smaller than Electron). Manages the brain process lifecycle, provides system tray integration, and supports auto-updates via GitHub Releases.

## Architecture

```
Tauri v2 (Rust shell, ~5MB)
├── WebView -> loads React frontend (same as soul-web)
├── Tray icon -> menu events (show/hide, quit)
├── Brain manager -> health polling, CLI delegation
├── IPC commands -> Tauri commands for native features
└── Auto-updater -> GitHub Releases
```

### Components

| File | Purpose |
|------|---------|
| src-tauri/src/main.rs | Tray icon, menu events, brain lifecycle |
| src-tauri/src/lib.rs | Brain management, health polling, IPC |
| src-tauri/tauri.conf.json | CSP, window settings, bundle targets |
| src-tauri/capabilities/default.json | Tauri v2 permissions (no shell:allow-execute) |

### Builds

macOS (.dmg), Windows (.msi), Linux (.AppImage) via GitHub Actions CI.

### Security

- CSP locked to 127.0.0.1:8000 (only local brain)
- No `shell:allow-execute` permission
- Brain process managed via CLI delegation, not direct shell exec

## Strategic Value

Shows native app development skills. Tauri v2 choice (over Electron) demonstrates awareness of binary size and resource efficiency tradeoffs.
