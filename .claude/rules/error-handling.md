# Error Handling

## Backend (Python)
- All API endpoints return a consistent error envelope:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Human-readable description",
      "details": {}
    }
  }
  ```
- Use typed exception classes that map to HTTP status codes. Never raise raw `Exception`.
- Catch errors at the boundary (route handler), not deep in business logic. Let exceptions propagate naturally.
- Log errors with full context (request ID, tenant ID, endpoint) at ERROR level. Log stack traces at DEBUG.
- Never expose internal details (stack traces, file paths, SQL queries) in API responses.
- Use `try/except` only when you have a specific recovery strategy. Don't catch-and-ignore.

## Frontend (TypeScript)
- Use React Error Boundaries to catch rendering errors. Never let the SDK crash the host app.
- All async operations must have error handling. No unhandled promise rejections.
- Network errors: retry with exponential backoff (max 3 retries). If all retries fail, degrade gracefully — the host app must continue working.
- The SDK must be invisible when it fails. No error modals, no console spam. Log to an internal error buffer that the developer can optionally access.
- Validate all data coming from the backend before rendering. Never trust the wire.

## Both
- Never swallow errors silently. Every caught error must be logged or re-thrown.
- Error messages must be actionable: say what went wrong AND what to do about it.
- Use error codes (not just messages) for programmatic handling.
