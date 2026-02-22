---
name: warn-empty-except
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.py$
  - field: new_text
    operator: regex_match
    pattern: except.*:\s*\n\s*(pass|\.\.\.)\s*$
---

**Empty except/pass block detected!**

Silent failures are forbidden across all Soul ecosystem projects. Always:
1. Log the error with context (`structlog` or `logging`)
2. Re-raise or return an appropriate error response
3. Use specific exception types, not bare `except:`

Bad: `except Exception: pass`
Good: `except sqlite3.IntegrityError as e: logger.error("duplicate entry", error=str(e)); raise`
