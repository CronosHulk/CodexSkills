---
name: graphify
description: Build, refresh, and query a persistent local code dependency graph when navigating a large or unfamiliar repository, tracing cross-file dependencies, or planning risky multi-module changes.
---

# Graphify — automatic, selective graph context

Use for unfamiliar repositories, cross-module dependency tracing, or changes touching 3+ connected files. **Do not** build a graph for a simple local edit or if `rg` already answers the question. This skill provides a **lightweight, static Python import/symbol graph**, not the full multimedia Graphify pipeline described by the original legacy `skill.md` (which is retained as `legacy-reference.md`).

## Workflow

1. Run `python3 .agents/skills/graphify/scripts/graph.py sync --root .` once before graph-assisted exploration. Sync is incremental using file hashes, and outputs `.graphify/graph.json`.
2. Search: `python3 .agents/skills/graphify/scripts/graph.py query --root . --term authentication --limit 12`.
3. Trace dependencies: `python3 .agents/skills/graphify/scripts/graph.py neighbors --root . --node path/to/module.py`.
4. Read source files to **verify** graph hints; never treat static edges as runtime truth.
5. After modifying Python files, run `sync` again. The graph is local and should be gitignored.
6. If optional Graphify MCP is configured, use `graphify_query` / `graphify_neighbors` instead of subprocess commands. The MCP server refreshes the graph on requests.

The graph is deliberately not generated on every trivial turn. Keep results bounded; prefer query before opening many files. It indexes Python imports and definitions, and file nodes for other supported source files. No LLM calls or token charges for indexing.

## MCP (optional)

Install `pip install mcp` in your local Python environment. Copy the example `.codex/config.toml` MCP section from `docs/GRAPH_CONTEXT.md` after replacing the absolute path. MCP runs locally over stdio and is not active merely because the skill is present.
