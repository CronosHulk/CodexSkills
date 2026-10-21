# Model routing: configuration vs verification

The agent TOMLs express preferred models. `AGENTS.md` instructs the coordinator to choose roles based on task complexity. **Neither guarantees that the running Codex client supports the selected model or honors every key.**

## Intended policy
- FAST: main Luna; no subagents.
- STANDARD: main Luna; optional one Luna specialist.
- DEEP: Luna for exploration/tests; Sol architect or security reviewer only when complexity justifies it.
- If Luna fails with new evidence of complexity, escalate once rather than looping.
- Never allow concurrent edits to the same file.

## Validation
1. `python3 scripts/validate.py` checks syntax and intended role assignments.
2. `python3 scripts/check_runtime.py` checks local CLI presence/version, not effective routing.
3. Open a trusted Codex project; inspect `/status` and `/model`, run a small task, and inspect actual agent roles/models in the session.
4. Repeat with a complex task and verify Sol is used only for its intended role.
5. Record real usage using `benchmarks/README.md`.

**Fallback:** if a configured model is unavailable, choose an available cheaper model with sufficient capability, or run directly in the main session. Never silently claim a role used Luna or Sol if not verified.

Codex CLI configuration and OpenAI Agents API configuration are separate interfaces; do not copy API-only settings into `.codex/config.toml`.
