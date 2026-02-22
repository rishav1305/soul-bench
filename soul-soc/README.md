# soul-soc

> Security operations toolkit with CVE scanning and security knowledge base.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Library |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/modules/knowledge/cve_scanner.py` |
| License | MIT |

## What It Is

An Ubuntu CVE scanner that runs on a systemd timer, checks installed packages against known vulnerabilities, and stores findings in the security knowledge base (ChromaDB collection). Part of soul-os's self-awareness capabilities.

## How It Works

```
systemd timer (daily) -> cve_scanner.py
    |
    v
Check installed packages -> query Ubuntu CVE database
    |
    v
Store findings in ChromaDB "security" collection
    |
    v
Available via knowledge search: "What CVEs affect this system?"
```

### Key Features

- Scans installed packages against Ubuntu CVE feeds
- Stores findings with severity ratings in knowledge base
- Queryable via semantic search
- Runs as systemd timer (non-interactive, hardened)

## Strategic Value

Demonstrates security awareness and operational security practices. Shows that the system actively monitors its own vulnerability surface.
