# Performance Budgets

## Frontend
- Core SDK bundle (event collector + transport): < 8 KB gzipped.
- Full SDK with widget: < 25 KB gzipped.
- Widget with React bindings: < 35 KB gzipped.
- No SDK operation should block the main thread for more than 16ms (one frame at 60fps).
- Measure bundle size in CI. Block PRs that exceed budgets.

## Backend
- API response times (p95):
  - Health check: < 10ms
  - Event ingestion (WebSocket batch): < 20ms
  - Rules classification: < 50ms
  - Hint generation (cached): < 5ms
  - Hint generation (Haiku fallback): < 300ms
  - Spatial query (vision model): < 1s
  - Dashboard analytics queries: < 200ms
- WebSocket connection establishment: < 100ms.
- Database queries: no query should exceed 100ms. Use EXPLAIN ANALYZE on any new query.

## Monitoring
- Track and alert on p50, p95, p99 response times.
- Track bundle size trends over time. Catch regressions early.
- Load test: the backend must handle 10,000 concurrent WebSocket connections per instance.
