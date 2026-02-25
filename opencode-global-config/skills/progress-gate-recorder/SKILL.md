---
name: progress-gate-recorder
description: Enforce recorder protocol: every completed task must update .sisyphus/progress.md and .sisyphus/requirements.md, otherwise task is incomplete.
---

# Progress Gate Recorder

## Goal

Make task delivery deterministic by enforcing two ledgers:
- `.sisyphus/requirements.md` (stable constraints)
- `.sisyphus/progress.md` (execution timeline)

## Mandatory Protocol

1. Before execution, ensure both files exist.
2. On any requirement clarification/correction, append to `requirements.md`.
3. On each completed step, append to `progress.md`.
4. If either file is not updated, mark current task as **NOT DONE**.

## File Templates

If missing, create:

### `.sisyphus/requirements.md`

```markdown
# Requirements Ledger

## Active Constraints
- [YYYY-MM-DD HH:MM] ...
```

### `.sisyphus/progress.md`

```markdown
# Progress Ledger

## Timeline
- [YYYY-MM-DD HH:MM] Started: ...
- [YYYY-MM-DD HH:MM] Completed: ...
```

## Quality Gate

Before final response, verify:
- requirements ledger has latest constraints
- progress ledger has completion records for this turn

If missing -> continue working until both are updated.
