---
name: team-init
description: 当用户说“初始化团队”或要求团队并行执行时，自动启用 Planner/Builder/Reviewer/Tester/Recorder 五角色协作流程。
---

# Team Init Skill

## Trigger
Use this skill when the user says any of:
- 初始化团队
- 启动团队
- 建立团队执行
- 三角色并行
- 五角色并行
- Builder Reviewer Tester
- Planner Builder Reviewer Tester Recorder

## Behavior
When triggered, immediately switch to 5-role orchestration in the current session:
1. Planner: split tasks, define dependencies, and maintain the execution board.
2. Builder: implement code changes.
3. Reviewer: perform static review for bugs, regressions, and risks.
4. Tester: execute test and verification commands.
5. Recorder: keep concise execution logs, decisions, and final change summary.

## Execution Rules
- Run role workstreams in parallel whenever tools allow.
- Maintain one shared task board with statuses: `pending`, `in_progress`, `completed`.
- Planner owns task breakdown and state transitions on the shared board.
- Recorder owns the running log and final structured summary.
- Provide concise sync updates and a merged conclusion.
- Reviewer findings are prioritized by severity with file references.
- If no findings, state that explicitly.

## Output Contract
For each substantial task, return:
1. Role outputs (Planner / Builder / Reviewer / Tester / Recorder)
2. Final merged decision
3. Next actions (if any)

## Constraints
- This is role-based orchestration inside one Codex session, not multiple independent session contexts.
- Keep behavior deterministic and concise.
