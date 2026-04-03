# Dependency Policy

## Adding dependencies
- Before adding a new dependency, check if an existing one or stdlib covers the need.
- Evaluate: maintenance activity, download count, license (MIT/Apache preferred), bundle size impact, transitive dependency count.
- Prefer small, focused packages over large frameworks. One dependency that does one thing well beats a kitchen-sink lib.
- Every new dependency must be justified in the PR description.

## Version pinning
- Pin exact versions in production packages (no `^`, no `~`).
- Use lockfiles: `uv.lock` for Python, `package-lock.json` or `pnpm-lock.yaml` for Node.
- Commit lockfiles to the repo. Always.

## Auditing
- Run `npm audit` and `pip audit` in CI on every PR.
- High/critical vulnerabilities block merges.
- Review and update dependencies monthly. Use Dependabot or Renovate for automated PRs.

## Banned patterns
- No dependencies for things the language provides (e.g., no lodash for `Array.map`, no moment.js when `Intl.DateTimeFormat` exists).
- No dependencies with known security issues that haven't been patched.
- No dependencies that haven't been updated in 2+ years without a strong justification.
