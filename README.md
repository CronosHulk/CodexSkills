# Codex Optimized v2.1

27 coding skills, selective skill routing, token-saving discipline, and six model-specific subagent role definitions.

## Install

Requires Python 3.11+ for local tooling.

```bash
python3 scripts/install.py --target /path/to/project
python3 scripts/install.py --target /path/to/project --apply
```

The first command is a dry run. Existing files are preserved by default. Merge your existing `AGENTS.md` and `.codex/config.toml` manually; **do not blindly overwrite custom settings**. To replace with `.bak` backups, use `--apply --overwrite`.

## Check

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/check_runtime.py
```

Validation checks files, frontmatter, TOML and intended model mappings. It **does not** prove the running Codex instance honors model routing. See `docs/MODEL_ROUTING.md` for manual verification.

## Benchmarks

```bash
python3 scripts/benchmark.py benchmarks/example.jsonl
```

The included example is **synthetic**. See `benchmarks/README.md` for real A/B testing. No measured cost savings are claimed.

## Intended orchestration

- Main: GPT-6 Luna.
- Explorer, Implementer, Tester, Reviewer: Luna.
- Architect, Security Reviewer: GPT-6.1 Sol.
- FAST tasks: no subagents. STANDARD: at most one normally. DEEP: up to two concurrently.
- Skill routing chooses one primary skill; `codex-token-saver` principles are always summarized in `AGENTS.md`, so its full skill need not load on every turn.

## Project contents

- `AGENTS.md`: low-overhead rules and automatic skill selection
- `.agents/skills/`: 27 skills
- `.codex/agents/`: 6 model-specific role definitions
- `.codex/config.toml`: intended default model and agent settings
- `scripts/install.py`: dry-run-first installer with overwrite backups
- `scripts/validate.py`: offline static validation
- `scripts/check_runtime.py`: Codex CLI probe
- `scripts/benchmark.py`: real-token comparison tool
- `tests/`: unit tests and routing-policy fixtures
- `.github/workflows/validate.yml`: automated checks
- `docs/MODEL_ROUTING.md`: limits and verification steps
- `AUDIT.md`: original audit

**Important:** Routing fixtures test configuration expectations, not model behavior. Model availability and effective subagent configuration must be verified on the actual Codex version.
