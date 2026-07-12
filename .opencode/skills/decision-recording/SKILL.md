---
name: decision-recording
description: Record one explicitly accepted decision from traceable evidence without synthesizing missing rationale, alternatives, trade-offs, or consequences.
compatibility: opencode
metadata:
  workflow: decision-management
---

# Decision Recording

Use this skill during discovery, PRD cleanup, implementation, review, validation, or audit when an explicitly accepted choice needs a durable record.

## Core rule

A decision record is a concise transcription of an agreed choice and its agreed reason. It is not a design exercise, best-practice essay, or reconstruction of why existing code might make sense.

Do not create a record merely because a document contains a section named `Decisions`, `Testing Decisions`, `Technical Notes`, `Prior Art`, `Architecture`, or similar. Classify the actual statements inside it.

## Evidence required before writing

Create an accepted decision record only when all three are traceable to approved evidence:

1. **Decision evidence** — the source explicitly states what was chosen.
2. **Reason evidence** — the source explicitly states why it was chosen.
3. **Acceptance evidence** — the user approved it, or an approved artifact records it as accepted.

Valid evidence sources are:

- an explicit user statement or confirmation in the current conversation;
- an approved PRD, story, ADR, or design record containing the statement;
- a repository rule explicitly accepted by the user.

The following are not evidence of rationale or acceptance:

- code, tests, dependencies, imports, or configuration;
- common practice or general software-engineering knowledge;
- likely benefits or drawbacks of a technology;
- section headings or document placement;
- the fact that an implementation already exists;
- an agent's interpretation of what the author probably intended.

Code may prove **what exists**. It does not prove **why it was chosen**, which alternatives were considered, or which consequences were accepted.

## Mandatory pre-write evidence check

Before creating each file, build this temporary evidence ledger in reasoning or report it to the user when confirmation is needed:

```text
Candidate decision: <one atomic choice>
Decision evidence: <exact source statement and source location>
Reason evidence: <exact source statement and source location>
Acceptance evidence: <exact confirmation or approved status>
Options evidence: <exact source statements, or absent>
Consequences evidence: <exact source statements, or absent>
```

Do not create the file when any of the first three evidence fields is missing.

When decision or reason evidence is missing, ask one focused question. Do not fill the gap. When acceptance is missing, ask the user to accept, reject, or revise the candidate.

## Atomicity rule

Each file records exactly one choice.

A candidate is too broad when it combines multiple independent choices such as:

- the testing seam;
- the test framework;
- terminal-capture mechanics;
- fixture strategy;
- test-data selection;
- coverage scope.

Separate independently agreed choices. Leave routine mechanics in code or a factual testing guide. Do not manufacture additional decisions merely to account for every implementation detail.

A useful atomic title generally reads as one choice, for example:

- `Use LangGraph for investigation orchestration`
- `Associate Evidence with the relevant Sub-claim`
- `Persist reports as Markdown files`

Avoid umbrella titles such as `Testing Strategy`, `Application Architecture`, or `Technology Stack` unless the user explicitly approved that complete bundled strategy as one decision.

## Bulk extraction from a PRD, audit, handoff, or codebase

When the input may contain several candidates, classify them before editing:

- **READY** — decision, reason, and acceptance are explicitly supported;
- **NEEDS CONFIRMATION** — the choice exists, but reason or acceptance is missing;
- **NOT A DECISION** — product behavior, implementation guidance, factual documentation, an unresolved option, or routine code detail.

Only create files for `READY` candidates.

If the user asks to “perform the refactor now”:

1. create records for `READY` candidates;
2. migrate only their source-supported text;
3. leave unsupported content untouched or move factual guidance only when the requested destination is clear;
4. ask one focused question for the first `NEEDS CONFIRMATION` candidate;
5. do not convert unresolved candidates into accepted records to make the refactor appear complete.

## Classification

Choose one primary destination.

### Product requirement

Observable behavior, user constraints, acceptance criteria, or product policy remain in the PRD.

### Design decision

An accepted, local, or reasonably reversible technical choice gets one file:

```text
docs/design/NNNN-<slug>.md
```

### ADR

An accepted, cross-cutting, long-lived, expensive-to-reverse, or materially surprising architecture choice gets one file:

```text
docs/adr/NNNN-<slug>.md
```

### Repository structure rule

Current module ownership or dependency direction belongs in `docs/00-repo-structure.md`. Create a separate decision record only when its rationale is independently supported.

### Open decision

When no option is accepted, retain it as an open decision in the PRD or relevant story and state what it blocks. Do not create an ADR or design decision.

### No durable record

Do not record routine implementation details whose rationale has no durable value.

## File and numbering rules

- One decision per file.
- Number `docs/design/` and `docs/adr/` independently.
- Inspect the target directory and allocate the next unused zero-padded number.
- Never renumber accepted or superseded records.
- Every record references its related PRD.
- Add related stories only when the relationship is explicit and useful. Never write `All stories` unless the approved source says the decision applies to all stories.

## Writing rules

The default record contains only:

- title;
- status;
- related PRD;
- optional explicitly relevant story references;
- `Decision`;
- `Why`.

Use the source's wording where practical. Paraphrase only to remove repetition or improve clarity without adding meaning.

Do not add claims such as `standard`, `best`, `flexible`, `robust`, `faster`, `safer`, `lower cost`, `easier to maintain`, `allows refactoring`, or similar unless the approved source explicitly states them.

Do not add examples, implementation recipes, testing scope, tools, fixture details, pros and cons, or explanatory background for completeness.

Keep the normal record brief. Prefer one short paragraph for `Decision` and one short paragraph for `Why`. Exceed roughly 200 words only when preserving explicit source material requires it.

## Optional sections

Append `Considered options` only when the exact options were discussed with or presented to the user.

Append `Consequences` only when the exact consequences were acknowledged or accepted by the user.

Do not infer either section from general knowledge, source code, or logical implications. Omit the section entirely when unsupported. Do not write placeholders such as `None`, `Not discussed`, or `N/A`.

## Status rules

Use `Accepted` only when acceptance evidence exists.

Do not create a `Proposed` record during extraction merely to capture an inference unless the user explicitly asks to preserve proposals. Keep the candidate in the PRD's open-decision section or ask the user.

## PRD refactoring rules

- Remove technical rationale from the PRD only after a supported decision record has been created and linked.
- Retain observable behavior, acceptance criteria, constraints, and product scope in the PRD.
- Do not delete unsupported source text merely because it did not qualify as a decision.
- Generic testing guidance belongs in `docs/testing.md` only when it is factual, useful, and the user asked for or approved that documentation.
- Installed tooling may be documented as current repository fact, but never as an accepted rationale unless the rationale is explicitly supported.

## Final anti-fabrication check

Before saving each record, verify every sentence:

1. Which exact approved source supports this sentence?
2. Does the sentence add a benefit, drawback, option, consequence, scope, tool, or reason absent from that source?
3. Is this one atomic choice?
4. Is the reason explicitly agreed rather than logically inferred?
5. Is `Accepted` justified by explicit evidence?

Delete any sentence that cannot pass this check. If deleting it removes the reason or acceptance, do not create the record; ask the user one focused question instead.
