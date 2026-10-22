# Project Intelligence (local)

Three skills share the same Python stdlib CLI: `scripts/project_intelligence.py`.

```bash
python3 scripts/project_intelligence.py sync --root .
python3 scripts/project_intelligence.py remember --root . --kind decision --summary 'Use optimistic locking for orders' --path src/orders.py --source reviewed-decision
python3 scripts/project_intelligence.py recall --root . --term locking
python3 scripts/project_intelligence.py impact --root . --path src/orders.py
python3 scripts/project_intelligence.py tests --root . --path src/orders.py
```

Files: `.graphify/graph.json` (graph) and `.graphify/memory.json` (memory), both ignored by Git. Do not store secrets or personal information. Back up local memory yourself if needed. Project memory is not shared automatically with teammates.

`impact` traverses reverse Python import dependencies. `tests` produces **suggestions only**, and never executes commands. For unsupported languages, dynamic imports, runtime call graphs, and external APIs, use direct source review and broader tests. `git diff` covers uncommitted work by default; pass `--base` for a revision comparison. This does not measure token savings.

This script is installed at the project root alongside the skills. It assumes Python 3.11+ and a git repository for automatic changed-file detection; explicit `--path` works without Git.
