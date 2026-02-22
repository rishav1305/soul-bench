---
name: block-sql-string-concat
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.py$
  - field: new_text
    operator: regex_match
    pattern: (execute|executemany)\s*\(\s*f["']|\.format\(.*\)\s*\).*(?:SELECT|INSERT|UPDATE|DELETE|DROP)
---

**Possible SQL injection via string formatting!**

Use parameterized queries with `?` placeholders:
- Bad: `await db.execute(f"SELECT * FROM Contact WHERE email = '{email}'")`
- Good: `await db.execute("SELECT * FROM Contact WHERE email = ?", (email,))`

Never use f-strings or .format() in SQL queries.
