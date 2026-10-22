# Efficient Codex workflow

Default to **Luna** for small and medium coding tasks. The main agent owns the final diff and correctness. Use **Sol** only for ambiguity, complex cross-module reasoning, security-sensitive changes, or failed Luna attempts supported by evidence.

## Automatic skill selection
Select the single most specific matching skill from `.agents/skills/` using its name and description. Read its SKILL.md only when applicable. Do not load unrelated skills or all references. Use `using-agent-skills` for ambiguous routing. `codex-token-saver` principles below apply by default; read its full skill only when the task benefits from deeper cost optimization.

## Token discipline
- Start with `git status --short`; preserve unrelated changes.
- Locate symbols with bounded `rg` searches; open small relevant file ranges, not the repository.
- Reuse prior findings and avoid duplicate tool calls or large logs.
- Make minimal diffs; no unsolicited refactors, docs, scaffolding or lengthy plans.
- Verify with focused tests first, then broader tests according to risk.
- Keep responses concise: changed files, tests, remaining issues.

## Subagent policy
- FAST: do not spawn agents.
- STANDARD: delegate only independent, bounded discovery/testing/implementation; normally <= 1 subagent.
- DEEP: up to 2 concurrent agents; prefer Luna roles; Sol only for architect/security_reviewer when justified.
- Explicitly select a role, with objective, file scope, edit permission, stop condition, and <=150-word report.
- Never have two agents edit the same files concurrently.
- Do not ask a Sol agent to repeat Luna exploration; pass paths, facts and failures.
- Do not spawn a reviewer on every trivial change.
- A custom agent's model setting is authoritative only if supported by the installed Codex version; check `/status` or agent details when validating.
- If a lightweight attempt fails, diagnose once, then escalate to Sol with evidence. Avoid endless retries.
- For security/payment correctness, prioritize verification over token savings.

## Skill precedence
User instructions and applicable repository-specific AGENTS.md take precedence over generic optimization guidance. Read references only when a relevant skill explicitly needs them.

## Automatic graph context
For unfamiliar repositories, dependency tracing, or multi-module changes, select `graphify` and run `python3 .agents/skills/graphify/scripts/graph.py sync --root .` before broad source exploration. Query the local graph first, then verify source files. Refresh after changes. Skip graph creation for FAST tasks and narrow searches. MCP is optional; see `docs/GRAPH_CONTEXT.md`.

## Selective project intelligence
For non-trivial work, consult `project-memory` only if relevant verified project decisions or pitfalls may exist; retrieve bounded notes with `python3 scripts/project_intelligence.py recall --root . --term <topic>`. Never persist secrets or unverified assumptions. For Python cross-module/risky changes, invoke `change-impact-analyzer` using `python3 scripts/project_intelligence.py impact --root . --path <file>`; after edits use `smart-test-selection` with `tests --root .` to suggest focused checks. Do not run these tools for FAST tasks. Always verify code and expand tests for critical behavior. Graph-based hints are not authoritative.
