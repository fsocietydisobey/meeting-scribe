# Git & Branching

## Branch naming
- `main` — production-ready, protected. No direct pushes.
- `develop` — integration branch. PRs merge here first.
- `feature/<ticket-or-name>` — new features (e.g. `feature/event-collector`)
- `fix/<description>` — bug fixes (e.g. `fix/websocket-reconnect`)
- `chore/<description>` — maintenance, deps, CI (e.g. `chore/update-deps`)
- `refactor/<description>` — structural changes with no behavior change

## Commits
- Use conventional commits: `feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:`, `perf:`, `ci:`
- Keep commits atomic — one logical change per commit.
- Write commit messages in imperative mood: "add event buffer" not "added event buffer".
- First line under 72 characters. Add a body for non-obvious changes.

## Pull requests
- PRs should be small and focused. One feature or fix per PR. If a PR touches 10+ files, consider splitting it.
- Every PR must have: a clear title, a description of what changed and why, and a test plan.
- PRs require at least one review before merging.
- Squash merge to keep history clean on main/develop.
- Delete branches after merging.

## Protected branches
- `main` and `develop` are protected. No force pushes, no direct commits.
- All changes go through PRs with passing CI.
