# Testing Standards

## Coverage
- Minimum 80% line coverage for all packages.
- Critical paths (event pipeline, hypervisor decisions, auth middleware) must have 95%+ coverage.
- Coverage is enforced in CI — PRs that drop coverage below threshold are blocked.

## Organization
- Test files mirror the source structure: `src/foo/bar.ts` → `tests/foo/bar.test.ts`
- Group tests by behavior, not by method: describe what the module does, not its internal API.
- Use descriptive test names: `it("flushes buffer immediately on navigation event")` not `it("test flush")`.

## Test types
- **Unit tests** — test individual functions and classes in isolation. Mock external dependencies.
- **Integration tests** — test module interactions with real (or containerized) dependencies.
- **E2E tests** — test full user flows through the system. Use Playwright for frontend, httpx for backend.
- Every new feature must include unit tests. Integration tests required when the feature crosses module boundaries.

## Test quality
- Tests must be deterministic. No flaky tests. If a test depends on timing, use fake timers.
- No test should depend on another test's state. Each test sets up and tears down its own fixtures.
- Test edge cases and error paths, not just the happy path.
- Use factories or builders for test data — no hardcoded magic values scattered across tests.

## Before merging
- All tests pass in CI.
- No skipped tests without a linked issue explaining why.
- New code has tests. No exceptions.
