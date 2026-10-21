---
name: codex-token-saver
description: Minimize coding cost for implementations, fixes and refactors using scoped context, targeted tests and selective delegation.
---

# Codex Token Saver

Optimize **total cost to a verified correct result**, not merely prompt length. Never sacrifice correctness, security, or necessary tests for token savings.

## 1. Scope before reading

- Restate the goal internally in one sentence; identify acceptance criteria.
- Check `git status --short` before edits. Preserve unrelated user changes.
- Discover filenames with `rg --files` and narrow using glob patterns; search symbols with `rg -n` and bounded output. Avoid dumping whole trees or files.
- Read only relevant functions and nearby context (`sed -n 'START,ENDp'`). Expand if dependencies require it.
- Read repository instructions (`AGENTS.md`) for relevant directories and follow them.
- Keep a compact working map: relevant paths, symbols, assumptions, and test commands. Reuse findings instead of rereading.

## 2. Choose execution mode

- **Tiny**: one clear file, small edit, known tests. Work directly; no plan or subagents.
- **Normal**: 2–5 files or moderate uncertainty. Short 3-step plan; implement directly.
- **Complex**: cross-module design, unclear dependencies, or independent components. Brief plan and selective delegation if supported.
- Avoid subagents when their startup, duplicated exploration, or merging costs exceed the benefit.
- Never assume a model-routing feature exists. If the environment supports selecting a cheaper model per agent, use it for bounded discovery or test tasks; otherwise keep delegation minimal.

## 3. Delegate with a bounded contract

Each delegated task must specify:
- One objective and a concrete deliverable.
- Allowed file scope and whether edits are permitted.
- Explicit stop condition and verification method.
- Response budget: at most 200 words, unless a longer response is essential.
- Return only paths, symbols, findings, test results, and blockers. No full source dumps.

Parallelize only independent tasks. Avoid concurrent edits to the same file. Maximum two subagents by default; use more only when clearly justified.

## 4. Implement minimally

- Prefer small diffs and existing project patterns; do not refactor unrelated code.
- Apply targeted edits; avoid rewriting entire files for small changes.
- Don't generate large speculative scaffolding, docs, or tests beyond task requirements.
- Resolve ambiguity with existing code and tests before asking questions.
- Escalate model/reasoning only for genuinely difficult problems, not as a default.

## 5. Verify progressively

- Run the narrowest meaningful test first (single test/function/file).
- Then run impacted module tests; broader suite only when risk warrants it.
- On failure, inspect the specific error, make one hypothesis, and fix the cause. Do not blindly rerun the same command.
- Do not skip required security, integration, or regression checks for savings.
- Never claim a test passed unless it ran and passed.

## 6. Control context and output

- Prefer concise command output (`rg -n`, `git diff --stat`, `git diff --check`, focused test logs).
- Do not paste large logs, lockfiles, generated code, or repeated file contents into conversation.
- Before compaction/handoff, preserve only: task goal, changed files, key decisions, open blockers, next test command.
- Final response <= 150 words by default: changes, tests, remaining risks. Expand when user requests detail.

## 7. Completion checklist

- Requirements satisfied and no unrelated edits.
- Focused tests executed or explicitly marked unrun.
- Relevant security/data integrity risks considered.
- Diff reviewed; no accidental generated files or secrets.
- Concise final report.
