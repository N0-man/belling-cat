# Agent workflow contract

This repository is developed with OpenCode. Keep this file concise: detailed procedures live in `.opencode/skills/`, while `README.md` is the human guide.

## Core workflow

Behaviour-changing work follows:

```text
/discover -> /create-prd -> /create-backlog -> /implement
```

One discovery interaction normally defines one MVP increment and may produce several stories. Run `/implement` one story at a time until the backlog is complete.

Unplanned structural work follows:

```text
/audit -> /refactor
```

Use `/validate` to gate an already committed range outside the normal story flow.

## Ownership

- **Human:** product intent, scope approval, material architecture and dependency choices, accepted risk, push/merge decisions.
- **Primary agent:** inspect, question, document accepted decisions, plan, implement one ready story, test, review, validate, and commit focused verified cycles.
- **Review subagents:** read-only analysis only.

Never invent scope, silently choose a material alternative, absorb unrelated workspace changes, bypass tests/hooks, rewrite away earlier repair commits, or mark incomplete work done.

## Artifact ownership

| Artifact                               | Owns                                                                                     |
| -------------------------------------- | ---------------------------------------------------------------------------------------- |
| `CONTEXT.md`                           | Useful business language and responsibility definitions                                  |
| `docs/00-repo-structure.md`            | Current module ownership and dependency rules                                            |
| `docs/design/<increment>.md`           | Reversible increment-level design decisions                                              |
| `docs/adr/NNNN-*.md`                   | Cross-cutting, long-lived, costly, or surprising architecture decisions                  |
| `.scratch/<increment>/PRD.md`          | Product outcome, behaviour, constraints, and acceptance evidence                         |
| `.scratch/<increment>/backlog.md`      | Story order, status, and blockers                                                        |
| `.scratch/<increment>/backlog/NN-*.md` | Story intent, value, scope, criteria, and evidence                                       |
| `.scratch/handoff-context.md`          | Active story, scope baseline, exact cycle/phase, commits, findings, and validation state |
| `Makefile` or CI                       | Executable verification commands                                                         |

Use one primary owner per durable fact and link from other artifacts rather than copying full rationale. `.scratch/` is local workflow state; durable decisions live under `docs/`.

## Discovery and planning

- Every product feature or behaviour change starts with `/discover`.
- Ask exactly one question at a time and inspect the repository before asking codebase-answerable questions.
- Record accepted technical choices in a design record or ADR; do not leave them only in chat or bury them only in the PRD.
- Apply DDD and Clean Architecture pragmatically. Use them when they clarify language, ownership, dependency direction, or testability—not as mandatory ceremony.
- Stories use INVEST as a heuristic and must demonstrate useful value. A strict vertical slice is not required; a technical enabler is valid when it unlocks, de-risks, or proves a meaningful capability.

## State and recovery

The backlog tracker and handoff are always read together:

1. One `doing` story plus matching handoff: resume the exact phase.
2. One `doing` story without handoff: reconstruct cautiously in `reconcile` phase.
3. Handoff and tracker disagree: reconcile before changing production code.
4. No active story or handoff: select the requested or next ready `to-do` story.
5. More than one `doing` story: invalid state; repair the tracker first.

The tracker owns story lifecycle (`to-do`, `doing`, `done`). The handoff owns execution detail. Never overwrite or discard recovery history implicitly.

## Implementation rules

Before changes, capture HEAD and all staged, modified, and untracked files with `scope-guard`. Preserve unrelated work and stage explicit intended files only.

Each behaviour or executable repair follows:

```text
RED -> GREEN -> REFACTOR -> VERIFY -> COMMIT
```

- One behaviour at a time.
- Observe the intended RED or a credible safety signal for a pure refactor.
- Refactor only while green.
- Commit every complete green cycle; never commit RED separately.
- Keep earlier cycle and repair commits.
- Record each phase and commit in the handoff.

Before final validation, record candidate acceptance and demonstration evidence in the story file while the tracker remains `doing`.

## Review and validation

Review the exact committed range recorded in the handoff:

```text
story_base_sha..HEAD
```

Do not guess `main`, `HEAD~1`, or a branch-based fixed point.

Every finding receives a severity and one action:

- `repair` — clearly inside approved intent;
- `ask-user` — changes behaviour, scope, contract, dependency, material architecture, or risk acceptance;
- `record-decision` — approved rationale is missing or stale;
- `no-op` — accepted trade-off or observation.

Repairs are additive focused commits followed by re-review. Preflight is non-mutating and uses repository-owned commands.

## Completion

A story moves to `done` only when:

- acceptance criteria and demo evidence are recorded and verified;
- all cycles and repairs are committed and green;
- no blocking/major or unanswered user finding remains;
- decision and documentation ownership is current;
- preflight passes without changing tracked files;
- unrelated baseline changes remain preserved;
- the handoff is finalized and archived.

## Permissions

`plan` intentionally has edit and bash access because discovery and planning create PRDs, backlogs, context, design records, and ADRs. `build` has edit/bash access and may invoke only the configured internal review/audit subagents. Those subagents are hidden and read-only.

## Important rules to follow

- Do not provide time, effort, completion-date, or story-point estimates unless the user explicitly requests an estimate
