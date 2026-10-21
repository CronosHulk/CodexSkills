---
name: solid-pragmatic
description: Apply SOLID or ports-and-adapters patterns to a concrete architecture or refactoring problem.
---

# Pragmatic SOLID

Improve the ability to understand and change code without adding more concepts
than the problem requires. Use this as a design lens alongside existing testing,
review, and implementation workflows, not a second competing process.

## Scope and coordination

- Follow the user's scope and repository instructions. Do not change quality
  thresholds, public formats, or product behavior as architectural cleanup.
- If another active skill already covers testing or review, reuse its evidence
  rather than repeating the same workflow. Honor stricter project requirements.
- Refactor only the responsibility affected by the task. In a review-only request,
  report findings and proposed boundaries without editing production code.
- A large file is a reason to inspect cohesion, not permission for a rewrite.

## Locate the actual responsibility problem

Read the callers, state transitions, dependency direction, and behavioral tests
before choosing a split. Identify independently changing concerns, repeated
invariants, and side effects hidden behind innocent-looking methods.

For an overloaded object, describe which decisions it owns and which it merely
schedules. A coordinator should delegate specialized decisions, not contain
their implementation or expose all collaborators through a shared context.
Specify the state owned by each extracted component and how it interacts with
the coordinator; passing the entire old object into extracted helpers preserves
the original coupling.

## Boundaries that earn their cost

- Keep domain decisions independent of UI frameworks, operating systems,
  persistence, network libraries, and concrete launchers. Put external effects
  behind small consumer-owned contracts, constructed in composition roots.
- Use the language's natural mechanisms: Python Protocols and typed callables,
  dataclasses for records, modules/functions for cohesive stateless logic.
  A boundary does not automatically need a new class or directory hierarchy.
- Introduce strategies or dispatch only for demonstrated alternatives. Extending
  an explicit branch can be clearer than inventing a plugin framework.
- Preserve substitution contracts: accepted inputs, results, exceptions, timing
  assumptions, cancellation, resource ownership, and cleanup on partial failure.
- Limit each consumer's access to the operations and state it actually needs.
  Avoid service locators and a context object that becomes access to everything.

## Simplify without turning heuristics into laws

- Judge methods and classes by cohesion and cognitive load. There is no universal
  maximum of 10 method lines, 50 class lines, two fields, or one indentation level.
  Respect explicit repository limits when they exist.
- Multiple fields can belong to one coherent state or value. Add a value object
  when validation, units, identity, or operations justify it; ordinary scalars and
  collections do not require wrappers just to satisfy a style rule.
- Extract duplication when it expresses the same policy or invariant that must
  evolve together. Similar syntax with different semantics can remain separate.
  Do not wait for a third copy of a correctness-critical invariant.
- Prefer one named operation for repeated state resets when the lifecycle
  semantics match. Keep distinct reset modes explicit; do not hide differences
  behind a growing list of boolean arguments.
- Keep useful explanations of intent and constraints. Do not remove comments,
  forbid else, or replace ordinary control flow solely to make metrics smaller.

## Verify a small, complete change

For changed behavior or a bug fix, establish a failing behavioral test first,
then implement the smallest complete fix. For behavior-preserving extraction,
use existing behavioral tests and add characterization coverage only for missing
contracts; do not invent a behavior change to manufacture a failing test.

Verify outcomes through fake ports or isolated adapters. Do not replace
behavioral assertions with assertions about the new helper layout. Preserve
failure paths, ordering of effects, cancellation, and resource release. Follow
the repository's required architecture, inventory, coverage, formatting, and
build checks. Repeat checks when relevant inputs change, not for reassurance.

Before finishing, check that the split actually reduced the reasons a component
changes and the state a reader must track. If it only moved lines elsewhere or
added pass-through objects, simplify it. Report concrete improvements, remaining
coupling, and verification limits without claiming that passing tests proves
complete SOLID compliance.

## Origin

Independently written adaptation inspired by
[ramziddin/solid-skills](https://github.com/ramziddin/solid-skills).
It retains responsibility-driven design and test-first behavior changes while
replacing universal object-size rules and mandatory primitive wrappers with
project-specific constraints and demonstrated design needs.
