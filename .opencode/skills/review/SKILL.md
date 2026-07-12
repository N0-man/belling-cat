---
name: review
description: Review an exact committed range independently for documented standards, product intent and specification, and proportionate architecture and decision compliance.
compatibility: opencode
metadata:
  workflow: quality
---

# Three-Axis Review

## Resolve the exact range

Prefer the active handoff's `story_base_sha`. An explicit fixed point overrides it. Resolve the fixed point to an exact SHA and review:

```bash
git diff <base-sha>..HEAD
git log <base-sha>..HEAD --oneline
```

Require a non-empty committed range for story review. Report uncommitted and baseline-preserved changes separately; do not mix them into the committed review result.

## Resolve intent and sources

Load the handoff intent packet or an explicit intent statement. Intent must describe the objective, constraints, deliberate decisions, exclusions, and demonstration outcome—not merely the diff.

Specification sources, in order:

1. explicit story/specification argument;
2. active handoff work file, PRD, and product backlog tracker;
3. matching backlog story and PRD.

Also load referenced increment design decisions, ADRs, context, repository structure, and documented standards.

If intent or specification is missing enough to change conclusions, return `INCOMPLETE` rather than reverse-engineering product intent from code.

## Parallel review

Invoke all three read-only subagents in one parallel Task batch:

- the `standards-reviewer` subagent;
- the `spec-reviewer` subagent;
- the `architecture-reviewer` subagent.

Pass exact base/HEAD SHAs, diff command, commit list, intent packet, story path, PRD path, backlog path, and decision sources.

Reviewers must:

- inspect the entire changed range before finishing;
- focus on material issues introduced or exposed by the change;
- inspect surrounding code, call sites, tests, and invariants when needed;
- anchor findings to precise evidence where possible;
- avoid duplicating dedicated formatting, lint, typecheck, and test output;
- distinguish an intentional trade-off from an accidental defect using the supplied intent.

## Architecture posture

Review proportionately. Do not fail a change merely because it lacks tactical DDD, ports, layers, or a strict vertical shape. Findings require a concrete risk, violated documented decision, unclear ownership, harmful coupling, or unrecorded material choice.

## Finding contract

Each finding contains:

- ID (`STD-`, `SPEC-`, or `ARCH-`);
- severity: `blocking`, `major`, `minor`, or `observation`;
- code/document evidence;
- violated source, criterion, decision, or invariant;
- concrete impact;
- focused remediation or decision question.

After reviewers return, invoke the `finding-triage` skill to assign:

- `repair`;
- `ask-user`;
- `record-decision`;
- `no-op`.

Keep axes independent and preserve finding IDs across repair rounds. The orchestrator may add a missed finding with a new stable ID instead of suppressing it.

## Risk assessment and result

Report risk as `low`, `medium`, or `high` with one concise rationale. Risk is not a replacement for findings or gate outcome.

Overall gate:

- `PASS`: no open blocking/major finding and no unanswered `ask-user` finding;
- `REPAIR`: at least one in-scope blocking/major finding requires repair;
- `AWAITING-USER`: a finding belongs to the user;
- `INCOMPLETE`: required source, intent, or diff unavailable.

The skill is read-only. Repairs occur in new TDD/safety or documentation cycles and are re-reviewed.
