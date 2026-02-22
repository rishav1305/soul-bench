# Vaultwarden Agent Design

**Date**: 2026-02-22
**Status**: Implemented

## Problem

Need a way to read/write secrets from Vaultwarden during Claude Code sessions. Three approaches were considered:

1. **Agent wrapping `bw` CLI** (chosen) -- zero code, uses existing CLI
2. **MCP Server wrapping `bw` CLI** -- adds structured tools but unnecessary complexity
3. **Direct Vaultwarden REST API** -- complex auth, undocumented API, reimplements `bw`

## Decision

Agent wrapping `bw` CLI. Same rationale as choosing `gh` CLI over browser automation for GitHub: the CLI is already installed, authenticated, and does everything needed.

## Architecture

- File: `.claude/agents/vaultwarden.md`
- Auth: `BW_SESSION` env var (user runs `bw unlock` before use)
- Operations: search, get (password/username/totp/notes/uri), create, edit, delete, list folders, sync, generate password
- Can write secrets to .env files with explicit user confirmation

## Safety

- Never echo passwords in Bash descriptions
- Never hardcode session keys
- Confirmation required for all writes (create, edit, delete, write to disk)
- Soft-delete only (no `--permanent`)
- No vault export
- Warn about .gitignore for secret files
