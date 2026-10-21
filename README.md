# Codex Skills — Token-Efficient Multi-Agent Development

**A modular collection of 27 AI coding skills with automatic skill selection, cost-aware agent orchestration, and context optimization for OpenAI Codex.**

Build software with structured AI workflows while reducing unnecessary model calls, repeated context processing, and expensive reasoning.

## Why this project?

AI coding agents are powerful, but inefficient workflows can waste tokens and increase development costs.

Common problems include:

- Reading entire repositories for small changes.
- Using expensive reasoning models for trivial tasks.
- Launching unnecessary subagents.
- Repeatedly analyzing the same files.
- Loading irrelevant instructions into context.
- Running extensive workflows for simple bug fixes.
- Generating verbose reports instead of actionable results.

**Codex Skills addresses these problems through intelligent workflow selection, lightweight agents, and task-specific development practices.**

## Key Features

### Automatic Skill Selection

Codex selects the most relevant skill based on the task.

Instead of executing every development workflow, the system prioritizes one primary skill and loads additional instructions only when necessary.

Examples:

| Task | Selected Skill |
|---|---|
| Fix a failing test | `debugging-and-error-recovery` |
| Implement a feature | `incremental-implementation` |
| Improve slow code | `performance-optimization` |
| Review a pull request | `code-review-and-quality` |
| Design an API | `api-and-interface-design` |
| Investigate security issues | `security-and-hardening` |
| Optimize context usage | `codex-token-saver` |

Skill selection is instruction-driven and depends on the capabilities of the installed Codex version.

### Token-Efficient Development

The `codex-token-saver` skill introduces practical optimization strategies:

- Search relevant symbols before opening files.
- Avoid unnecessary full-repository scans.
- Reuse previously discovered information.
- Keep code modifications focused.
- Minimize repeated tool calls.
- Prefer targeted tests before running complete test suites.
- Limit unnecessary subagent execution.
- Return concise implementation summaries.

The goal is to reduce token consumption without sacrificing correctness or maintainability.

### Cost-Aware Multi-Agent Orchestration

Different development tasks require different levels of reasoning.

This project provides six specialized subagent configurations.

| Agent | Default Model | Responsibility |
|---|---|---|
| Explorer | GPT-6 Luna | Repository exploration |
| Implementer | GPT-6 Luna | Scoped code changes |
| Tester | GPT-6 Luna | Test creation and execution |
| Reviewer | GPT-6 Luna | Code quality checks |
| Architect | GPT-6.1 Sol | Complex architecture and design |
| Security Reviewer | GPT-6.1 Sol | Security-sensitive analysis |

The main agent defaults to GPT-6 Luna, with GPT-6.1 Sol reserved for more demanding tasks.

Model assignments are configurable and depend on model availability and Codex support for custom agent configurations.

### Adaptive Development Workflows

Not every task requires a complete software engineering lifecycle.

The framework uses three execution levels:

| Mode | Use Case | Approach |
|---|---|---|
| FAST | Small fixes, localized changes | Direct execution, no subagents |
| STANDARD | Feature implementation, multi-file changes | Focused planning and selective delegation |
| DEEP | Complex architecture, migrations, critical changes | Specialized agents and additional verification |

This prevents unnecessary orchestration overhead.

## Architecture

```text
User Request
    |
    v
Codex Main Agent
    |
    +-- Automatic Skill Selection
    |       |
    |       +-- Debugging
    |       +-- Implementation
    |       +-- Testing
    |       +-- Security
    |       +-- Performance
    |       +-- Other specialized skills
    |
    +-- Task Complexity Evaluation
            |
            +-- FAST
            |    Direct execution
            |
            +-- STANDARD
            |    Luna subagents as needed
            |
            +-- DEEP
                 Luna for exploration/testing
                 Sol for complex reasoning
```

The main agent coordinates implementation, integrates results, and verifies the final changes.

Subagents receive bounded tasks and return concise findings rather than full execution histories.

## Project Structure

```text
.
├── AGENTS.md
├── .agents/
│   └── skills/
│       ├── using-agent-skills/
│       ├── codex-token-saver/
│       ├── context-engineering/
│       ├── incremental-implementation/
│       ├── debugging-and-error-recovery/
│       ├── test-driven-development/
│       └── ... 21 additional skills
├── .codex/
│   ├── config.toml
│   └── agents/
│       ├── explorer.toml
│       ├── implementer.toml
│       ├── tester.toml
│       ├── reviewer.toml
│       ├── architect.toml
│       └── security_reviewer.toml
└── references/
    ├── orchestration-patterns.md
    ├── testing-patterns.md
    ├── security-checklist.md
    └── ...
```

## Installation

### Project-Level Installation

Copy the following into your project root:

```text
AGENTS.md
.agents/
.codex/
references/
```

Merge existing `AGENTS.md` and `.codex/config.toml` configurations instead of overwriting them.

Restart Codex after installation. Project-level configuration may require the project to be trusted.

### Global Skill Installation

To make the skills available across projects, copy the skill directories into:

```bash
~/.agents/skills/
```

For global agent configurations, copy the agent TOML files into:

```bash
~/.codex/agents/
```

Merge the relevant agent settings into:

```bash
~/.codex/config.toml
```

## Usage

### Automatic Workflow

Simply describe the task:

```text
Fix the authentication bug and add regression tests.
```

Codex should select the relevant workflow, investigate the problem, implement the fix, and verify the result.

### Explicit Skill Invocation

```text
$codex-token-saver

Refactor the payment processing module.
Minimize token consumption while preserving behavior.
```

### Complex Tasks

```text
Analyze the current backend architecture and propose
a migration strategy.

Use lightweight agents for repository exploration.
Reserve stronger reasoning models for architecture
decisions and critical review.
```

## Design Principles

**1. Use the simplest effective workflow.**

Small tasks should not require complex orchestration.

**2. Prefer focused context over large prompts.**

Retrieve information when it becomes necessary.

**3. Delegate only when beneficial.**

Subagents should reduce work, isolate context, or provide useful specialization.

**4. Match model capability to task complexity.**

Expensive models should be reserved for problems that justify their cost.

**5. Preserve correctness.**

Token optimization must never replace appropriate testing, security validation, or code review.

## Measuring Efficiency

The project aims to improve:

- Token consumption per completed task.
- Number of unnecessary tool calls.
- Amount of repeated context processing.
- Subagent orchestration overhead.
- Development time and verification quality.

Actual savings depend on the task, model, repository, and Codex environment.

**No fixed percentage of token savings is guaranteed.** Reliable comparisons require running equivalent tasks with and without the framework.

## Compatibility

Designed for OpenAI Codex environments supporting:

- Agent Skills (`SKILL.md`)
- `AGENTS.md` instructions
- Custom agent configurations
- Multi-agent workflows

Some features depend on the installed Codex version and available models. Automatic routing is guided by instructions rather than enforced by an independent scheduling service.

## Roadmap

- [x] Modular coding skills
- [x] Automatic skill selection instructions
- [x] Token optimization skill
- [x] Task complexity classification
- [x] Cost-aware subagent configurations
- [x] Context-efficient delegation guidelines
- [ ] Automated token usage benchmarks
- [ ] Task-based model routing evaluation
- [ ] Skill selection accuracy tests
- [ ] Performance comparison across model combinations
- [ ] Automated reporting of token usage per task

## Contributing

Contributions are welcome, particularly improvements to skill routing, token efficiency, multi-agent orchestration, testing workflows, and measurable development performance.

When proposing changes, prioritize practical improvements that preserve correctness while reducing unnecessary work.

---

**Build smarter. Delegate selectively. Spend fewer tokens.**
