# API Design & System Architecture

## Architecture philosophy
This codebase must read like it was built by a team of senior engineers. Every file, folder, and function should demonstrate intentional design. If a company audits this code, the architecture alone should demonstrate hire-worthy engineering.

### Separation of concerns
- **Frontend:** presentation logic only. No business logic in components. State lives in RTK slices. Data fetching via RTK Query. Domain logic in slices/thunks. Components only dispatch and select.
  - `features/` — one folder per domain. Each contains: slice, API definition (RTK Query), components, hooks, types.
  - `store/` — Redux store configuration, root reducer, middleware setup.
  - `components/` — shared/generic UI components only (buttons, modals, overlays). Feature-specific components live inside their feature folder.
  - `hooks/` — shared custom hooks. Feature-specific hooks live inside their feature folder.
  - `types/` — shared TypeScript types. Feature-specific types live inside their feature folder.
- **Backend:** layered architecture with strict boundaries:
  - `routes/` — HTTP handlers. Thin. Validate input, call service, return response. No business logic.
  - `services/` — business logic. Orchestrates domain operations. Never touches HTTP or database directly.
  - `repositories/` — data access. SQL queries, Redis operations. Returns domain objects, not raw rows.
  - `models/` — domain models and schemas. Pydantic models for validation, TypedDict for state.
  - `middleware/` — cross-cutting concerns: auth, rate limiting, tenant resolution, request logging.
- Grow into layers as complexity demands. Start with routes + service per feature. Add repository when data access complexity justifies it.

### Modular by feature
- Organize code by feature/domain, not by type. Prefer:
  ```
  src/
    events/
      routes.py
      service.py
      repository.py
      models.py
    sessions/
      routes.py
      service.py
      ...
  ```
  Over:
  ```
  src/
    routes/
      events.py
      sessions.py
    services/
      events.py
      sessions.py
  ```
- Each feature module should be self-contained enough that you could extract it into its own package with minimal changes.
- No top-level `utils/` folder. Cross-cutting helpers go in a `shared/` module with strict boundaries on what belongs there.

### Dependency direction
- Dependencies flow inward: routes → services → repositories → models.
- Inner layers never import from outer layers. Services don't know about HTTP. Repositories don't know about services.
- Use dependency injection (constructor params or FastAPI's `Depends()`) to wire layers together. No hard-coded imports of concrete implementations in business logic.

### Consistency over cleverness
- Every feature module must follow the same structural patterns. If your event pipeline and rules classifier look structurally identical, that's senior engineering. If they each invented their own patterns, that's a red flag.

## REST API conventions
- All endpoints versioned: `/api/v1/...`
- Use plural nouns for resources: `/api/v1/events`, `/api/v1/sessions`
- Standard HTTP methods: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove).
- Consistent response envelope for success:
  ```json
  {
    "data": { ... },
    "meta": { "request_id": "...", "timestamp": "..." }
  }
  ```
- Pagination: cursor-based for event streams, offset-based for dashboard lists. Always include `total`, `has_more`, and `next_cursor`/`next_offset`.
- Filter/sort via query params: `?status=stuck&sort=-created_at`
- Rate limit headers on every response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Status codes
- `200` — success (GET, PUT, PATCH)
- `201` — created (POST)
- `204` — no content (DELETE)
- `400` — validation error (bad input)
- `401` — unauthorized (missing/invalid auth)
- `403` — forbidden (valid auth, insufficient permissions)
- `404` — not found
- `409` — conflict (duplicate resource)
- `422` — unprocessable entity (valid JSON, invalid semantics)
- `429` — rate limited
- `500` — internal server error (never intentional — this means a bug)

## WebSocket conventions
- Messages are JSON with a `type` field: `{ "type": "event_batch", "data": [...] }`
- Server pushes include a `type` and `action`: `{ "type": "hint", "action": "show", "data": {...} }`
- Error frames: `{ "type": "error", "code": "RATE_LIMITED", "message": "..." }`
- Heartbeat: client sends `{ "type": "ping" }` every 30s, server responds `{ "type": "pong" }`.
