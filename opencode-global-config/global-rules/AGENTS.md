# Agent Team Protocol (Global Single-File Baseline)

## 1. Scope
- This is the cross-project baseline for all work under `C:\Users\16342`.
- Priority: user current-turn instruction > project `AGENTS.md` > this global file.

## 2. ULW Visibility
- If ULW mode is active, the first sentence must be: `ULTRAWORK MODE ENABLED!`.

## 3. Execution Gate
- Use multi-agent only when any of these is true:
  1. segmented polishing/checking, citation/evidence checking
  2. batch or explicit parallel processing
  3. 3+ independent subtasks
  4. large cross-file edits
- Otherwise use strict single-agent flow.

## 4. Multi-Agent Pipeline
- Planner -> Workers (parallel) -> Reviewer -> Recorder.
- Planner: task split, dependencies, acceptance criteria, risks.
- Workers: execute subtasks with input-output mapping.
- Reviewer: merge, deduplicate, unify style, list manual-review items.
- Recorder: capture reusable preferences/patterns for next tasks.

## 5. Quality Gates
- Do not change facts, numbers, citation data unless user explicitly requests.
- Output must be traceable and verifiable.
- Validate before delivery:
  - code: build/test/lint
  - writing: term consistency, citation completeness, style consistency

## 6. Writing/Checking Rules
- Minimal unit: content between one citation and the next.
- Output format: `原文 + 润色后` per segment.
- Tone: natural, restrained, low-template.
- If claim-citation mismatch is suspected, keep citation unchanged and provide suggestion list.

## 7. Workspace Hygiene (Hard Rule)
- Keep project folders clean.
- Temporary scripts: reusable -> move/rename meaningfully; non-reusable -> delete.
- Temporary outputs/logs/cache should not stay in project root.
- Clean up obvious temporary artifacts before final delivery.

## 8. Skills
- Use a skill when user names it or task clearly matches it.
- Use minimal skill set needed.
- If a skill path is unavailable, report briefly and continue with fallback.

## 9. Recording Policy
- Single-file baseline: no mandatory fixed ledger folder.
- Only create extra tracking files/folders when user explicitly asks.
- User corrections/preferences should be persisted in the active AGENTS hierarchy.
