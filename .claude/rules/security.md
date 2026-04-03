# Security

## Secrets
- No secrets in code. Ever. Not in comments, not in defaults, not in examples.
- All secrets come from environment variables or a secret manager.
- `.env` files are gitignored. `.env.example` with placeholder values is committed.
- API keys use prefixed format: `pk_` (public/frontend), `sk_` (secret/backend). This makes accidental exposure immediately identifiable.

## Input validation
- Validate at system boundaries: API route handlers, WebSocket message handlers, SDK initialization.
- Use Pydantic models for all incoming backend data. No raw dict access on request bodies.
- Frontend: validate all data from the backend before rendering. Never trust the wire.
- Sanitize all user-provided strings that will be rendered in the DOM. Prevent XSS.
- Limit request body sizes. Reject payloads over 1MB for standard endpoints.

## Authentication & authorization
- Every API request must include a valid API key. No anonymous access.
- `pk_` keys: read-only, rate-limited, safe to expose in frontend bundles. Can only send events and receive hints.
- `sk_` keys: full access, higher rate limits, must stay server-side. Can configure flows, read analytics, manage rules.
- Validate API keys on every request via middleware. Cache key lookups (TTL 5 min) to avoid DB hits on every call.
- Tenant isolation: every query must be scoped to the authenticated tenant's `app_id`. No cross-tenant data access.

## Dependencies
- Run `npm audit` and `pip audit` in CI. Block merges with known high/critical vulnerabilities.
- Pin dependency versions. No floating ranges (`^`, `~`) in production packages.
- Review new dependencies before adding: check maintenance status, download count, license, and transitive dependency count.

## Data privacy
- Never log PII (emails, names, IPs) at INFO or above. DEBUG only, and only when necessary for debugging.
- Session data is scoped per-user per-app. No cross-user data leakage.
- All data stays within the tenant's scope. Row-level security in PostgreSQL enforces this at the database level.
- The frontend SDK never captures: keystroke content, password values, screen recordings, clipboard data, or browser content beyond the current page.
