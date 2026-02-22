# soul-auth

> JWT authentication with token family replay detection and refresh rotation.

| Field | Value |
|-------|-------|
| Type | **PUBLIC** |
| Category | Library |
| Status | Production (in soul-os) |
| Source | `~/soul-os/brain/auth/` |
| License | MIT |

## What It Is

A JWT authentication system with non-trivial security features: short-lived access tokens (15 min), long-lived refresh tokens (30 days) with rotation, token family tracking for replay detection, bcrypt password hashing, and rate-limited auth endpoints.

## Architecture

```
Login -> bcrypt verify -> issue access + refresh tokens (token family)
    |
    v
Access Token (15 min) -> AuthMiddleware validates on every request
    |
    v (expired)
Refresh Token -> rotate (new access + refresh) -> invalidate old refresh
    |                                               |
    v (reused old refresh)                          v
Token Family Replay Detected -> revoke entire family
```

### Components

| File | Purpose |
|------|---------|
| jwt.py | Token creation/verification, bcrypt, refresh rotation |
| api/auth.py | Auth endpoints (login, refresh, logout) with rate limiting |
| middleware/auth.py | AuthMiddleware (JWT on all routes) + ws_verify_token |
| middleware/request_id.py | UUID per request, X-Request-ID header |
| middleware/security_headers.py | CSP, X-Content-Type-Options, X-Frame-Options |

### Key Security Features

- **Token family replay detection**: If a refresh token is reused after rotation, the entire token family is revoked (indicates token theft)
- **Short-lived access tokens**: 15-minute expiry limits blast radius
- **Refresh rotation**: Every refresh issues a new pair, old refresh invalidated
- **Rate limiting**: Auth endpoints rate-limited to prevent brute force
- **Security headers**: CSP, X-Frame-Options, X-Content-Type-Options on all responses

## Strategic Value

Token family replay detection is a non-trivial security pattern. Demonstrates depth in authentication security beyond basic JWT implementation. Relevant to security-focused engineering roles.
