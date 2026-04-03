# Versioning & Releases

## Semantic versioning
- Both packages (`@chimera/sdk` and `chimera-sdk`) follow strict semver: `MAJOR.MINOR.PATCH`.
- **MAJOR** — breaking API changes (removed exports, changed function signatures, incompatible config).
- **MINOR** — new features, new exports, backward-compatible additions.
- **PATCH** — bug fixes, performance improvements, internal refactors with no API change.
- Pre-release versions: `1.0.0-alpha.1`, `1.0.0-beta.1`, `1.0.0-rc.1`.

## Version sync
- NPM and PyPI packages share the same version number. When one bumps, the other bumps.
- Version is the single source of truth in `package.json` (npm) and `pyproject.toml` (PyPI).

## Changelog
- Maintain a `CHANGELOG.md` at the project root.
- Every version gets an entry with: date, version number, and grouped changes under `Added`, `Changed`, `Fixed`, `Removed`.
- Generated from conventional commit messages. Manual edits allowed for clarity.

## Release process
- Tag releases in git: `v1.0.0`. Tags trigger CI publish pipelines.
- Never publish from a local machine. All releases go through CI.
- Test the release artifact (install from registry, run smoke tests) before announcing.
