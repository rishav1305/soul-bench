---
name: block-weak-password-hash
enabled: true
event: file
action: block
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.py$
  - field: new_text
    operator: regex_match
    pattern: hashlib\.(sha256|sha1|md5)\(.*password|hashlib\.(sha256|sha1|md5)\(.*passwd
---

**Weak password hashing detected!**

Never use SHA-256/SHA-1/MD5 for password hashing. These are fast hashes designed for integrity checks, not password storage.

Use proper key derivation:
- `bcrypt` (used in soul-os and soul-outreach)
- `argon2` (alternative)

Note: SHA-256 IS used correctly for email payload hash verification in soul-outreach — that's integrity checking, not password storage.
