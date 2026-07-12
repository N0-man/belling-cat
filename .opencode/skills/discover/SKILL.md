---
name: discover
description: Discover one MVP increment through one-question-at-a-time requirements, decisions, useful domain language, and shared understanding of intent.
compatibility: opencode
metadata:
  workflow: discovery
---

# Discover One Increment

Every feature or behaviour-changing increment starts here.

## Objective

Reach shared understanding of:

- the user or stakeholder objective and beneficiary;
- detailed behaviour and scope boundaries;
- important failures, edge cases, and acceptance evidence;
- relevant technology, integration, deployment, quality, and architecture choices;
- deliberate trade-offs and ruled-out approaches;
- useful domain language and ownership;
- risks, dependencies, open decisions, and deferred work.

Treat one discovery interaction as one MVP increment. Several backlog stories may emerge from it.

## Start

1. Run the `check-handoff` skill for the discover command.
2. Inspect `AGENTS.md`, existing PRDs/backlogs, `CONTEXT.md`, repository structure, design records, ADRs, tests, and relevant code.
3. Resolve a stable kebab-case increment name early enough to name later artifacts.
4. Do not create a dedicated discovery file.

## Interview discipline

Use the `grilling` skill and ask exactly one question per response.

- Ask the highest-value unresolved question.
- Include current understanding and a recommended default.
- Do not ask questions answerable from the repository.
- Do not force the user through a generic questionnaire when a topic is irrelevant.
- Cover architecture, stack, deployment, NFRs, integration boundaries, and test strategy only to the depth needed for this increment.
- Distinguish the user's objective from implementation ideas suggested during discussion.

## Record durable information inline

As information is accepted:

- product behaviour and constraints: retain for PRD synthesis;
- useful business language: update `CONTEXT.md` through `domain-modeling`;
- module/dependency rules: update `docs/00-repo-structure.md`;
- increment-specific, reversible choices: use the `decision-recording` skill and update `docs/design/<increment>.md`;
- cross-cutting or costly-to-reverse trade-offs: use the `decision-recording` skill and create an ADR;
- unresolved choices: record as open decisions, not accepted decisions.

Do not leave accepted technical decisions only in chat or bury their rationale only in a PRD. Do not duplicate the same fact across several artifacts; choose one owner and reference it elsewhere.

## Ready to synthesize

Offer the increment for confirmation when:

1. the intended outcome, actors, and beneficiary are clear;
2. in-scope and out-of-scope behaviour are understood;
3. important failure behaviour and edge cases are understood;
4. the relevant repository and constraints were inspected;
5. blocking technical and architecture choices are decided or explicitly deferred;
6. deliberate trade-offs and ruled-out approaches are captured;
7. acceptance and demonstration evidence are understood;
8. story-sized outcomes can be identified;
9. no blocking ambiguity remains.

Present a concise shared-understanding summary covering objective, scope, key behaviours, accepted constraints, decisions, exclusions, open/deferred matters, and likely story boundaries. Ask one final question: approve this increment for PRD creation, or identify the single area to revisit?

After explicit confirmation, recommend `/create-prd <increment>`.

Do not create the PRD or backlog inside discovery unless the user explicitly asks to combine steps.
