# Classification Rules Sync Policy

## Rule
When adding, removing, or modifying a classification rule in `src/chimera_sdk/classifier/rules/builtin.py`, you MUST also update `docs/CLASSIFICATION-RULES.md` in the same commit. The documentation must always match the code.

## What to update
- The "Active Rules" table (rule name, priority, state, triggers)
- The "Rule Details" section (detailed description of the rule)
- The "Metrics Used" table if new metrics are referenced
- Any threshold changes in existing rules

## Source of truth
- Code: `src/chimera_sdk/classifier/rules/builtin.py`
- Documentation: `docs/CLASSIFICATION-RULES.md`
- Both must stay in sync. If they diverge, that's a bug — fix immediately.
