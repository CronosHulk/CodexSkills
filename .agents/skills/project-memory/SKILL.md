---
name: project-memory
description: Recall or save verified local project decisions, constraints, pitfalls and failures when prior knowledge materially helps a coding task.
---

# Project Memory

Use for recurring project-specific facts and non-obvious decisions. This is **opt-in per fact**, not an automatic transcript or unrestricted memory store. Never store secrets, credentials, PII, unverified guesses, or entire source files. Only record user-confirmed or evidence-verified, reusable facts. Ask before persisting sensitive or surprising facts.

```bash
python3 scripts/project_intelligence.py recall --root . --term payment
python3 scripts/project_intelligence.py remember --root . --kind pitfall --summary 'Provider X returns numeric fields as strings (confirmed in adapter)' --path src/adapters/provider_x.py --source verified-code
```

Data is local in `.graphify/memory.json`, excluded from Git by default. Entries are exact-match filtered, not semantic embeddings. Verify stale notes against current code. Use `--path` to narrow recall. Never blindly apply remembered assumptions.
