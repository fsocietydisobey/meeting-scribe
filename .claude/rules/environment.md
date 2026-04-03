# Environment & Configuration

## Environment variables
- All configuration comes from environment variables in production.
- Use a `.env` file for local development. Never commit it.
- Commit a `.env.example` with every required variable, placeholder values, and comments:
  ```
  # Required — your Chimera API secret key
  CHIMERA_SECRET_KEY=sk_your_key_here

  # Required — PostgreSQL connection
  DATABASE_URL=postgresql://user:pass@localhost:5432/chimera

  # Required — Redis connection
  REDIS_URL=redis://localhost:6379/0

  # Optional — log level (default: INFO)
  LOG_LEVEL=INFO

  # Optional — max WebSocket connections per tenant (default: 1000)
  MAX_WS_CONNECTIONS=1000
  ```

## Config loading
- Use a single config module (`src/chimera_sdk/config/`) that reads env vars and validates them at startup.
- Fail fast: if a required env var is missing, the app should not start. Raise a clear error message naming the missing variable.
- Use Pydantic `BaseSettings` for config validation — typed, with defaults for optional values.
- Never scatter `os.getenv()` calls throughout the codebase. All env access goes through the config module.

## Environments
- `development` — local, debug logging, relaxed rate limits, SQLite or local PostgreSQL.
- `staging` — mirrors production config, synthetic data, full observability.
- `production` — strict validation, production secrets via secret manager, no debug logging.
- Environment is determined by a single `CHIMERA_ENV` variable (`development`, `staging`, `production`).
