# Task Management Rules

## Structure

All tasks go in `tasks/todo/`. Each task gets its own folder named after the task (e.g. `tasks/todo/event-collector/`). Inside that folder, always create:

- **`TODO.md`** — a checkbox list of every item that needs to be done for the task. Check items off as they are implemented. When an item is checked off, add a brief description below it documenting: what was done, important files created or changed, key concepts, and anything someone would need to know. This is the living progress tracker and post-implementation reference.
- **`IMPLEMENTATION.md`** — a detailed study guide (see requirements below).

## File naming convention

- Root-level project files: UPPERCASE (`CLAUDE.md`, `README.md`)
- Task files: UPPERCASE (`TODO.md`, `IMPLEMENTATION.md`)
- Rules/config files: lowercase kebab-case (`conventions.md`, `guardrails.md`)

## IMPLEMENTATION.md requirements

The `IMPLEMENTATION.md` is a highly detailed, step-by-step implementation guide that doubles as a study guide. Someone reading it must be able to:

- Understand the feature end-to-end without reading any other file
- Reverse-engineer the feature from the document alone
- Follow it step by step to build the feature from scratch
- Study the architecture, data flow, and design decisions

### Required sections

1. **Overview** — what the feature does and why it exists
2. **Architecture** — how it fits into the system, with mermaid diagrams showing data flow, component relationships, and state transitions
3. **Data models** — every type, interface, schema, and state shape with field-level explanations
4. **Step-by-step implementation** — ordered sections, each covering one piece:
   - What to build and why
   - Files to create or modify
   - Code snippets or pseudocode
   - Edge cases and error handling
   - How this step connects to previous and next steps
5. **Integration points** — how this feature connects to existing code and other features
6. **Testing strategy** — what to test, how to test it, example test cases
7. **Glossary** — define any domain-specific terms

Be elaborate. Be clear. Do not assume the reader has context. Write it so someone new to the project can pick it up and learn.
