---
name: change-impact-analyzer
description: Estimate affected Python modules before cross-file changes, risky refactors, or regressions using a local reverse-import graph.
---

# Change Impact Analyzer

For non-trivial Python changes, use `python3 scripts/project_intelligence.py impact --root .` to inspect unstaged, staged and untracked changes; or pass `--path src/file.py` for a proposed change. Use `--base HEAD~1` to include a committed comparison. Graph is incrementally refreshed automatically.

The result is a **hint**, not a complete dependency analysis: Python static imports only, no runtime call graph, external consumers, or accurate JS/TS edges. Verify source, public contracts and tests. Never narrow validation solely because the graph omitted a dependency. Skip for trivial edits.
