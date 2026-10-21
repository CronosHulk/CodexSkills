# Codex Token Saver

Install in your repository:

```bash
mkdir -p .agents/skills/codex-token-saver
cp SKILL.md .agents/skills/codex-token-saver/SKILL.md
```

For user-wide installation (Codex setups supporting user skills):

```bash
mkdir -p ~/.agents/skills/codex-token-saver
cp SKILL.md ~/.agents/skills/codex-token-saver/SKILL.md
```

Invoke in Codex with `$codex-token-saver` if explicit skill invocation is supported, or ask Codex to use the skill for the task. Model selection and subagent support depend on your Codex version and configuration; this skill does not change pricing or model selection automatically.
