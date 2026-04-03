# Conventions

## Python
- Python 3.12+. Modern syntax: `str | None`, `list[str]`, `dict[str, Any]`.
- Async throughout. Type hints on all signatures.
- Imports: stdlib → third-party → `chimera_sdk.*`.
- Always run `black` after modifying a Python file.
- Use `uv install <package>` to add dependencies.

## TypeScript / JavaScript
- Strict mode. No `any` unless interfacing with third-party libs.
- Framework-agnostic core, React bindings as separate export.
- Buffer events client-side, flush every 100ms. Critical events flush immediately.
- ES6+ only. Always use fat arrow functions (`const fn = () => {}`), `const`/`let` (never `var`), destructuring, template literals, and modules (`import`/`export`).
- Always format with `prettier` after modifying a JS/TS file.
- **camelCase everywhere** in frontend code — variables, functions, props, file names. No mixed casing. The only exception: POST request body data uses `snake_case` to match backend Python conventions.

## Frontend tooling
- **Always run `nvm use` before any Node.js work.** The `.nvmrc` file pins the project to the correct Node version. Never skip this step.
- **Vite** for all frontend packages — build tooling, dev server, library bundling (lib mode for SDK packages).
- Use `npm create vite@latest` to scaffold new packages. Configure lib mode in `vite.config.ts` for SDK outputs (ESM + CJS).
- Use `vite-plugin-dts` for TypeScript declaration generation.
- **npm workspaces** for monorepo management. All frontend packages live under `packages/` and are linked via the root `package.json` workspaces field.
- Use `npm` as the package manager. Not pnpm, not yarn.

## Frontend state management
- Use **Redux Toolkit (RTK)** for all frontend state management. No raw Redux, no useContext for global state, no zustand.
- Use **RTK Query** for all server data fetching, caching, and synchronization. No manual fetch calls for API data.
- Store structure mirrors feature domains: one slice per feature (`eventsSlice`, `hintsSlice`, `sessionSlice`).
- Keep components thin — dispatch actions and select state via hooks (`useSelector`, `useDispatch`). Business logic lives in slices, thunks, or RTK Query endpoints.
- Use `createSlice` for synchronous state, `createAsyncThunk` for complex async flows that RTK Query doesn't cover.
- RTK Query API definitions live alongside their feature: `src/features/events/eventsApi.ts`.
- Never store derived data in Redux. Use `createSelector` (reselect) for computed values.

## Architecture standards (frontend and backend)
- **No flat file structures.** All code — Python, TypeScript, JavaScript — must be organized into nested folders by domain/feature. A directory with more than 5-6 files at the same level needs subdirectories. Only flatten when restructuring is genuinely impossible.
- Code must be modular. Each file should have a single responsibility. Extract shared logic into reusable modules. No god-files, no 500-line components.
- Both frontend and backend must meet senior-level engineering standards: clear separation of concerns, well-defined module boundaries, consistent patterns across the codebase.
- No spaghetti. No dump-everything-in-one-folder. Every directory should have a clear purpose. If you can't explain what a folder contains in one sentence, restructure it.
- **Clean, professional code.** Proper spacing throughout — blank lines between logical sections, consistent indentation, breathing room between functions/methods/classes. No wall-of-code blocks. Code should be immediately readable at a glance. This applies to both frontend and backend.

## Logging
- Structured logging to stderr only.
- Never log user behavioral data at INFO level — use DEBUG (privacy).

## State classification
- Rules engine first (no LLM) for 90% of cases: STUCK, FLOW, CONFUSED, LEARNING, NORMAL.
- LLM (Haiku) only for novel situations — always cache the result.
- Prefetch likely hints on page load.

## Transport
- WebSocket primary (bidirectional, one connection per session).
- HTTP POST + long-poll fallback for blocked WebSocket environments.
- Events stream up, actions push down, all over one connection.
