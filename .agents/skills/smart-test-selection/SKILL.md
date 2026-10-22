---
name: smart-test-selection
description: Suggest focused Python pytest files based on changed modules and static dependencies without executing tests or claiming complete coverage.
---

# Smart Test Selection

After impact analysis, run `python3 scripts/project_intelligence.py tests --root .` or provide `--path` / `--base`. The output proposes pytest file paths and a sample command; inspect before executing. Graph matching and filename matching are heuristics, not proof of coverage.

Run relevant targeted tests first. Expand to integration/full tests for authentication, payments, migrations, public contracts, broad changes or incomplete graph. Do not suppress security or release checks to save tokens.
