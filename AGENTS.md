# AGENTS.md

## Agent instructions

This repository is intended to be developed by opencode agents. Treat this file as the primary,tool-agnostic contract for coding agents.

## Workflow

`/discover` scopes requirements — one or more features may emerge. Each feature then follows the full pipeline:

```
/discover → /create-prd → /create-backlog → [per backlog item: /implement → /review → /commit]
```

Run `/create-prd` once per feature. The phases after discovery are sequential — do not skip them.

**One backlog item at a time.** Each backlog item is a vertical slice cutting through all layers.

## Handoff

- `/handoff` writes `.scratch/handoff-context.md` for next-session continuation
- The handoff file is overwritten on every `/handoff` invocation
- Handoff metadata must include current commit hash and UTC timestamp
- If existing handoff commit differs from current `HEAD`, mark stale context in the new handoff

## Core Rules

- **Human owns:** product intent, architecture approval, merge decision
- **Agent may:** explore, plan, implement an approved issue, test, review
- **Agent must not:** invent scope, add unapproved dependencies, refactor unrelated files

## Local Skills & Commands

Skills live in `.opencode/skills/`, invoked via thin commands in `.opencode/commands/`:

| Command            | Skill             | Purpose                                                                         |
| ------------------ | ----------------- | ------------------------------------------------------------------------------- |
| `/discover`        | `discover`        | Discover requirements through relentless interview, capturing glossary and ADRs |
| `/grilling`        | `grilling`        | Socratic questioning to clarify scope                                           |
| `/domain-modeling` | `domain-modeling` | Maintain glossary (`CONTEXT.md`) and ADRs (`docs/adr/`)                         |
| `/create-prd`      | `create-prd`      | Synthesize conversation into PRD at `.scratch/<feature-name>/PRD.md`            |
| `/create-backlog`  | `create-backlog`  | Break PRD into backlog items under `.scratch/<feature-name>/backlog/`           |
| `/handoff`         | `handoff`         | Write `.scratch/handoff-context.md` mapped to current commit                    |
| `/tdd`             | `tdd`             | One test → minimal code → pass → next test (never all tests first)              |
| `/implement`       | (composite)       | Implement a single backlog item using TDD + self-review                         |
| `/review`          | `review`          | Three-axis review (Standards + Spec + Arechitecture) using parallel sub-agents                   |
| `/commit`          | `commit`          | Commit the current reviewed changes                                             |
| `/lint`            | `lint`            | Auto-fix lint and formatting (Python + frontend), then confirm workspace is clean |
| `/test-affected`   | `test-affected`   | Find and run tests affected by current changes (optional file path args)        |
| `/preflight`       | `preflight`       | Run full CI-equivalent checks (lint, format, tests, coverage) before pushing   |

Skills create files lazily. Do not pre-create `.scratch/`, `docs/`, or implementation directories.

## Permission Model

`opencode.json` enforces:

- `edit: ask` — agent must request permission for file changes
- `bash: ask` (except whitelisted git + make commands)
- `webfetch: deny`

Relax `edit` to `allow` only during focused `/implement` sessions, then revert.

## Backlog Tracker

Local markdown under `.scratch/<feature-name>/`. Each backlog item file:

- What to build (end-to-end behavior, not layer-by-layer)
- Acceptance criteria
- `Blocked by:` line for dependencies
- `Status:` field using `to-do`, `doing`, or `done`

`.scratch/<feature-name>/backlog.md` is the primary tracker for backlog items in that feature/PRD

## Repo Structure

repo structure instruction is in `docs/00-repo-structure.md`

## Domain Model

- `CONTEXT.md` — glossary only, maintained by `domain-modeling` skill
- `docs/adr/` — architecture decisions for hard/surprising trade-offs only

## Commands

The repo has **no Makefile yet**. Build commands will emerge after implementation starts. The playbook (`Opencode_NLQ.md`) mentions:

```
make test       — run the test suite
make lint       — run linter
make typecheck  — run type checker
make eval       — run golden evals
```

These are **forward references** — they don't exist until implementation creates them.

## TDD Discipline

From `tdd/SKILL.md`:

- **One test at a time** — tracer bullet approach (RED → GREEN → repeat)
- **No horizontal slicing** — never write all tests first, then all code
- Tests verify behavior through **public interfaces**, not implementation details
- Only refactor after GREEN, never while RED

## Review Process

From `review/SKILL.md`:

Sub-agent selection conventions: `docs/agents/subagent-conventions.md`

Two parallel sub-agents report separately:

- **Standards** — does the code follow documented coding standards?
- **Spec** — does the code match the originating issue/PRD?

A change can pass one axis and fail the other — they are not merged or reranked.

## Key notes

- `.scratch/` is the local backlog root — skills create it, not you
- Backlog scope is per feature: `.scratch/<feature-name>/backlog.md`
- `CONTEXT.md` lives at repo root, not in `docs/`
- ADRs only for **hard, surprising, trade-off decisions** — not every architectural choice
- PRD sections are auto-generated by `/create-prd` skill using a canonical template
- Commit messages reference backlog item numbers (e.g., `Item 01: Add end-to-end mocked NLQ query flow`)
