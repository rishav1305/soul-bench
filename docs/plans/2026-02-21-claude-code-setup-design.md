# Design: Claude Code Environment Setup

## Date: 2026-02-21

## Problem
Opening Claude Code in ~/soul/ gave no hooks, no permissions, and a passive CLAUDE.md. Sessions required manual context-setting every time.

## Solution
- Rewrote CLAUDE.md as operational guide with Current Sprint, Daily Rhythm, Quick Commands, Conventions
- Added .claude/settings.local.json with broad permissions for cross-repo work
- Added 8 hookify rules cherry-picked from soul-os (12 rules), soul-outreach (4), soul-moa (4), soul-moe (3)
- Embedded Quick Commands ("today"/"status"/"sprint") directly in CLAUDE.md

## Hookify Rules

| Rule | Action | Source | What It Catches |
|------|--------|--------|----------------|
| block-hardcoded-secrets | block | soul-os | Credentials in code |
| block-sql-concat | warn | soul-os | SQL injection via f-strings |
| block-weak-password-hash | block | soul-os | SHA-256/MD5 for passwords |
| warn-direct-anthropic | warn | soul-outreach | Direct Anthropic SDK usage |
| warn-direct-send | warn | soul-outreach | Direct SMTP usage |
| warn-empty-except | warn | soul-os | Silent except: pass |
| warn-sync-in-async | warn | soul-os | Blocking calls in async |
| warn-cross-project-import | warn | NEW | brain.* imports outside soul-os |
