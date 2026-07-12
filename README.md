# Belling Cat

A terminal-based fact-checking application developed with an OpenCode workflow built around conversational discovery, INVEST-oriented stories, TDD, durable handoff state, focused commits, and intent-aware validation.

## Quick start

Prerequisites: OpenCode and `uv` are installed. Then install the locked development environment:

```bash
uv sync --locked
```

Start OpenCode in the repository and run:

```text
/discover belling-cat-mvp
/create-prd belling-cat-mvp
/create-backlog belling-cat-mvp
/implement
```

Run `/implement` again for each next ready story. Use `/workflow-status` whenever you want to see the active story, handoff phase, blockers, findings, and next valid action.

## How OpenCode pieces fit together

This repository uses three different concepts:

| Concept | What it is | Who invokes it |
|---|---|---|
| **Command** | A slash command under `.opencode/commands/` that starts a workflow entry point | Normally the human |
| **Skill** | Reusable instructions under `.opencode/skills/` loaded on demand | The primary `plan` or `build` agent |
| **Subagent** | A specialised reviewer/auditor under `.opencode/agents/` | Normally the `build` agent through the Task tool |

A command does not contain the full procedure. It selects a primary agent and tells that agent which skills to load. Skills may invoke other skills. Review and audit skills ask the `build` agent to invoke read-only subagents in parallel.

## Primary agents

| Agent | Used for | Permissions |
|---|---|---|
| `plan` | Discovery, PRD, backlog, context, design decisions, and ADRs | Edit and bash are allowed because planning creates files |
| `build` | Implementation, TDD, commits, review orchestration, audit, refactor, and validation | Edit and bash allowed; Task restricted to configured reviewers/auditors |

The default OpenCode `plan` agent is usually restrictive, but this repository deliberately grants it edit and bash access because planning is artifact-producing work.

## Internal subagents

These are hidden from normal `@` autocomplete. The normal workflow invokes them through `build`:

| Subagent | Invoked by | Responsibility |
|---|---|---|
| `standards-reviewer` | `review` / `validate-change` | Documented code and repository standards |
| `spec-reviewer` | `review` / `validate-change` | User intent, PRD, story, acceptance criteria, and scope |
| `architecture-reviewer` | `review`, `audit`, `validate-change` | Proportionate boundaries, dependency direction, decisions, and ownership |
| `code-auditor` | `audit` | Correctness, security, resilience, performance hazards, and maintainability |
| `traceability-auditor` | `audit` / `validate-change` | Missing decisions, stale artifacts, intent drift, and weak behavioural protection |

All five are read-only. They may inspect safe Git history and diffs but cannot edit files, run arbitrary shell commands, or invoke more agents. `hidden` only removes them from normal autocomplete; their explicit permissions and `build` task allowlist provide the actual workflow boundary.

## Skills and their normal callers

Skills are the reusable procedures agents load internally. Humans normally use commands rather than trying to invoke skills directly.

| Skill | Normally loaded by | Responsibility |
|---|---|---|
| `check-handoff` | Most workflow entry commands | Detect and reconcile existing active state |
| `discover` | `/discover` | Run one-increment discovery |
| `grilling` | `discover` | Ask exactly one high-value question |
| `domain-modeling` | Discovery, implementation, refactor | Maintain useful language and ownership |
| `decision-recording` | Discovery, PRD, implementation, audit, validation | Route choices to PRD, design record, ADR, or repository rules |
| `create-prd` | `/create-prd` | Synthesize the confirmed interaction into a PRD |
| `create-backlog` | `/create-backlog` | Produce INVEST-oriented stories and tracker |
| `workflow-state` | `/workflow-status`, `/implement`, planning gates | Reconcile tracker, handoff, Git, blockers, and next action |
| `scope-guard` | Implementation, refactor, repair validation, commit | Preserve unrelated workspace changes |
| `implement` | `/implement` | Orchestrate one story from start or resume to completion |
| `handoff` | Implementation and `/handoff` | Persist exact execution and recovery state |
| `tdd` | Implementation and refactor | Run one RED-GREEN-REFACTOR-VERIFY-COMMIT cycle |
| `test-affected` | TDD and validation | Select affected tests conservatively |
| `commit` | TDD, refactor, documentation repair | Commit one explicit verified cycle |
| `review` | Validation and `/review` | Orchestrate Standards, Spec, and Architecture subagents |
| `finding-triage` | Review, audit, validation | Assign severity and repair/user/decision ownership |
| `validate-change` | Story completion and `/validate` | Gate an exact committed range against intent and checks |
| `audit` | `/audit` | Orchestrate surprise audit subagents |
| `refactor` | `/refactor` | Resolve approved behaviour-preserving findings |
| `lint` | `/lint` | Check style by default; apply scoped fixes only with `--fix` |
| `preflight` | Validation and `/preflight` | Run non-mutating repository verification |
| `workflow-lint` | Preflight and `/workflow-lint` | Detect drift in workflow artifacts |

## Main human workflow

### 1. Discover one increment

```text
/discover <increment-name-or-intent>
```

Runs as `plan`. The agent inspects the repository and asks exactly one question per response. One discovery interaction normally scopes one MVP increment and may identify several stories.

Discovery records durable information in the correct owner:

```text
CONTEXT.md                    useful business language
docs/00-repo-structure.md    module and dependency rules
docs/design/<increment>.md   reversible increment decisions
docs/adr/NNNN-*.md           significant architecture trade-offs
```

There is no mandatory discovery file. After you approve the shared-understanding summary, run `/create-prd` in the same OpenCode session. If the conversation context is no longer available, restart `/discover` rather than asking the agent to reconstruct product intent from code.

### 2. Create the PRD

```text
/create-prd <increment-name>
```

Runs as `plan`. It creates:

```text
.scratch/<increment>/PRD.md
```

The PRD owns observable product behaviour, constraints, quality attributes, exclusions, and acceptance/demo evidence. It references design decisions and ADRs instead of duplicating their rationale.

### 3. Create and review the backlog

```text
/create-backlog <increment-name-or-prd-path>
```

Runs as `plan`. It creates:

```text
.scratch/<increment>/backlog.md
.scratch/<increment>/backlog/NN-<story>.md
```

The agent writes the proposed backlog and asks you to review its scope, story size, value, and ordering. Stories use INVEST as a heuristic, not dogma. Each story must be testable and able to showcase useful value. Technical enablers are allowed when they unlock, de-risk, or prove a meaningful capability.

### 4. Implement one story

```text
/implement [ITEM-NN-or-story-path]
```

Runs as `build`. It reads both the backlog tracker and active handoff, then either resumes the exact phase or starts the next ready story.

Each behaviour follows:

```text
RED -> GREEN -> REFACTOR -> VERIFY -> COMMIT
```

Every completed green cycle gets its own commit, for example:

```text
ITEM-04 Cycle 01: classify supported evidence
ITEM-04 Cycle 02: explain conflicting sources
```

At story completion, the agent validates the exact committed range:

```text
story_base_sha..HEAD
```

It repairs clearly in-scope findings with additional commits, returns product or material architecture choices to you, runs non-mutating preflight, updates the tracker to `done`, and archives the handoff.

### 5. Check progress

```text
/workflow-status [increment]
```

Runs as `plan` in report-only mode. It shows tracker state, active story, handoff phase, scope baseline, blockers, findings, validation state, and the next valid command.

## Surprise review and refactoring

Use these outside the planned increment flow:

```text
/audit [path|module|range|--all]
/refactor <audit-report> <finding-ids>
```

`/audit` is read-only and writes findings under `.scratch/audits/`. `/refactor` accepts only approved behaviour-preserving findings. Behaviour, contract, dependency, or material architecture changes return to discovery or a focused user decision.

## Validate already committed work

```text
/validate <base-sha>..<target-sha> <intent-or-spec-path>
/validate --repair <base-sha>..<target-sha> <intent-or-spec-path>
```

Standalone validation is read-only by default. `--repair` permits only fixes clearly inside the supplied intent. It never pushes, rebases, opens a PR, merges, or rewrites history.

## State and artifacts

### Story status

The product backlog tracker is authoritative:

```text
to-do -> doing -> done
```

Only one story may be `doing`. `blocked` is derived from unfinished dependencies rather than stored as another status.

### Handoff state

`.scratch/handoff-context.md` records the active story’s:

- starting and current commit;
- pre-existing workspace changes to preserve;
- intent packet;
- current TDD cycle and phase;
- test and verification evidence;
- cycle and repair commits;
- review findings and decisions;
- preflight and validation state.

The tracker answers **which story is active**. The handoff answers **exactly where implementation stopped**. `/implement` and `/workflow-status` always read both.

`.scratch/` is local workflow state and is ignored by Git. Durable decisions and repository rules belong under `docs/` and should normally be committed.

### Decision ownership

| Decision type | Primary owner |
|---|---|
| Observable product behaviour or constraint | PRD |
| Reversible increment-specific technical choice | `docs/design/<increment>.md` |
| Cross-cutting, costly, long-lived, or surprising trade-off | ADR |
| Module ownership or dependency direction | `docs/00-repo-structure.md` |
| Useful business language | `CONTEXT.md` |
| Routine easily reversible implementation detail | Code/tests; no separate record |

Use `/record-decision` directly when needed. The discovery, implementation, audit, and validation skills may also load the decision-recording skill internally.

## Commands and who normally triggers them

### Normal human entry points

| Command | Runs as | Normally triggered by | Purpose |
|---|---|---|---|
| `/discover` | `plan` | Human | Scope one MVP increment through one-question interviewing |
| `/create-prd` | `plan` | Human after discovery approval | Create the increment PRD |
| `/create-backlog` | `plan` | Human after PRD review | Create stories and the authoritative tracker |
| `/implement` | `build` | Human, once per story | Start or resume one story through validation |
| `/workflow-status` | `plan` | Human anytime | Report state and next valid action |
| `/audit` | `build` | Human anytime | Surprise code, architecture, test, and traceability audit |
| `/refactor` | `build` | Human after selecting audit findings | Behaviour-preserving repair workflow |
| `/validate` | `build` | Human for committed work outside `/implement` | Intent-aware committed-range gate |

### Advanced or diagnostic commands

These are available to humans, but the normal workflows usually load the equivalent skills internally.

| Command | Runs as | Normally triggered by | Purpose |
|---|---|---|---|
| `/grilling` | `plan` | `/discover` skill; rarely human | Ask one Socratic discovery question |
| `/record-decision` | `plan` | Discovery/implementation/audit skills or human | Classify and record a decision |
| `/domain-modeling` | `plan` | Discovery/implementation skills or human | Clarify language and responsibility when useful |
| `/handoff` | `build` | Implementation workflow or human diagnostic | Inspect, checkpoint, reconcile, close, or discard state |
| `/tdd` | `build` | `/implement` or `/refactor`; optionally human | Run one protected behaviour cycle |
| `/review` | `build` | `/validate-change`; optionally human | Read-only three-axis review of an exact range |
| `/commit` | `build` | TDD/refactor workflow; optionally human | Commit one scoped verified cycle |
| `/test-affected` | `build` | TDD/validation workflow; optionally human | Run conservatively selected affected tests |
| `/lint` | `build` | Human or pre-repair diagnosis | Check lint/format; pass `--fix` to apply scoped fixes |
| `/preflight` | `build` | `/validate-change` or human | Run the non-mutating CI-equivalent gate |
| `/workflow-lint` | `build` | `make preflight` or human | Detect drift among commands, skills, agents, docs, and permissions |

Humans invoke slash commands. Agents normally load skills directly; they do not need to simulate typing slash commands.

## Development commands

The Makefile owns executable checks:

```bash
make test
make lint
make format-check
make typecheck
make workflow-lint
make preflight
```

All verification targets use the committed `uv.lock` and are non-mutating. To fix style explicitly:

```bash
make lint-fix PATHS="src tests"
make format PATHS="src tests"
```

Or from OpenCode:

```text
/lint --fix src tests
```

`make preflight` runs workflow lint, lint, format check, type checking, and tests. It must leave tracked files unchanged.

## Workflow maintenance

When changing `.opencode/`, `AGENTS.md`, `README.md`, `opencode.json`, templates, or the workflow validator, run:

```bash
make workflow-lint
```

The human-facing README must document every slash command. `AGENTS.md` intentionally contains only the durable agent contract so it does not consume excessive context in every session.

Supporting migration, harvest, and audit notes live under `docs/agent-workflow/`.
