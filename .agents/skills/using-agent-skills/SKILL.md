---
name: using-agent-skills
description: Route coding tasks to the single most relevant skill; avoid unnecessary skill chains. Use at task start when selecting a workflow.
---

# Skill routing: progressive disclosure

Choose **one primary skill** for the current task. Read its `SKILL.md` only after selecting it from metadata. Add a second skill only if a distinct requirement cannot be satisfied by the primary one. Never run a full lifecycle chain automatically.

## Routing precedence
1. Explicitly named skill or workflow from user.
2. Failure/regression -> `debugging-and-error-recovery`.
3. Security issue -> `security-and-hardening`; performance regression -> `performance-optimization`.
4. Existing diff review -> `code-review-and-quality`.
5. New API contract -> `api-and-interface-design`; UI change -> `frontend-ui-engineering`.
6. Clear implementation -> `incremental-implementation`; test-first requested -> `test-driven-development`.
7. Ambiguous major feature -> `spec-driven-development`; agreed spec to tasks -> `planning-and-task-breakdown`.
8. CI/deployment -> `ci-cd-and-automation` or `shipping-and-launch`.
9. Documentation -> `documentation-and-adrs`.
10. Other specialized tasks -> match precise skill description.
Use `codex-token-saver` as a **cost discipline** for coding tasks, not as an additional mandatory skill load; root AGENTS.md contains its short default rules. Explicitly invoke `$codex-token-saver` for its full workflow.

## Effort and skill budget
- FAST: <= 1-2 files, clear behavior, low risk: execute directly; no planning skill, no subagents.
- STANDARD: several files or uncertain dependencies: one primary skill, short plan, targeted tests.
- DEEP: cross-system architecture, migration, security-critical changes: primary skill + one relevant specialist if needed; justify each subagent.
- Do not start `interview-me`, `idea-refine`, `spec-driven-development`, `doubt-driven-development`, `source-driven-development`, or full TDD merely because code is being written.
- Do not require user approval for safe, reversible choices with clear repository conventions. Ask for clarification on consequential ambiguities, destructive operations, or conflicting requirements.
- Follow explicit user instructions, repository constraints, and applicable safety checks over generic workflow preferences.

## Verification
Verify changed behavior with the narrowest meaningful checks first. Expand for risk and dependencies. Report what was actually run, never imply unrun tests passed.
