---
name: warn-sync-in-async
enabled: true
event: file
action: warn
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.py$
  - field: new_text
    operator: regex_match
    pattern: async\s+def.*\n(?:.*\n)*?.*(?:open\(|time\.sleep|requests\.|subprocess\.run)
---

**Blocking call inside async function!**

This will block the event loop. Use async equivalents:
- `open()` -> `aiofiles.open()`
- `time.sleep()` -> `asyncio.sleep()`
- `requests.` -> `httpx.AsyncClient`
- `subprocess.run` -> `asyncio.create_subprocess_exec`

All Soul ecosystem backends use FastAPI (async). Blocking calls cause request timeouts.
