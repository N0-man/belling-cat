---
name: implement
description: Resolve or resume one product backlog story from tracker and handoff state, then complete it through scoped TDD cycles, intent-aware validation, repair, preflight, and tracker completion.
compatibility: opencode
metadata:
  workflow: implementation
---

# Implement One Story

## 1. Resolve current state

Run the `check-handoff` skill and the `workflow-state` skill.

Read the product backlog tracker first, then the handoff:

- matching `doing` story and handoff -> resume exact cycle/phase;
- `doing` story without handoff -> reconstruct and enter `reconcile` phase;
- handoff/story mismatch -> reconcile before product changes;
- no active story -> validate the explicit story or choose the lowest ordered ready `to-do` story;
- more than one `doing` story -> stop and repair the tracker.

Require the increment PRD and validate blockers.

## 2. Guard scope and establish intent

Invoke the `scope-guard` skill before changing the tracker, handoff, documentation, tests, or production code.

For a new story:

- read the story, PRD, backlog, context, design decisions, ADRs, tests, and relevant code;
- capture current HEAD as `story_base_sha` and record all pre-existing working-tree changes and their ownership;
- set only its tracker row to `doing`;
- bootstrap the handoff with the captured base SHA and scope baseline, without overwriting unrelated history;
- create the handoff intent packet.

The intent packet states:

- what the user or stakeholder set out to accomplish;
- who benefits and what can be demonstrated;
- accepted constraints, quality attributes, and deliberate trade-offs;
- ruled-out and deferred approaches;
- explicit out-of-scope matters.

Intent is not a summary of files or implementation. Do not infer missing product intent from the diff.

For a resumed story, continue from the handoff's exact phase and preserve its scope baseline, intent, cycle history, findings, and repair commits.

## 3. Plan adaptive cycles

Translate acceptance criteria and demonstration evidence into a small ordered behaviour list. This is an adaptive test list, not permission to write all tests first.

A story may be user-facing or a technical enabler. Preserve its stated value and showcase outcome rather than forcing a particular layer sequence.

## 4. Execute cycles

For each next behaviour, use the `tdd` skill:

- one test or credible safety signal;
- RED evidence;
- minimal GREEN;
- REFACTOR with proportionate architecture, language, and decision-record checks;
- VERIFY focused and affected tests;
- one green commit;
- handoff checkpoint after every phase and commit.

Do not begin the next RED while the current cycle is uncommitted or incompletely checkpointed. After each commit, use the `scope-guard` skill to confirm unrelated baseline changes remain outside the story.

When implementation reveals a new technical decision, invoke the `decision-recording` skill. When it reveals genuinely useful language or responsibility changes, invoke the `domain-modeling` skill. New product behaviour or scope returns to `/discover`.

## 5. Intent-aware validation

When acceptance criteria appear complete, keep the tracker status `doing`, check the candidate acceptance criteria, record test/demo evidence in the story file, and then invoke the `validate-change` skill in active-story, repair-enabled mode. Candidate evidence is subject to validation and may be corrected during repair.

The validation gate:

- reviews the exact `story_base_sha..HEAD` committed range;
- passes the intent packet, story, PRD, and decision sources to reviewers;
- checks documentation and decision traceability;
- uses `finding-triage` for every finding;
- repairs `repair` findings through additional committed cycles;
- records already-approved missing rationale through `decision-recording`;
- stops and asks the user for every `ask-user` finding;
- reruns affected review axes after repair;
- runs non-mutating preflight.

Never reset, restart, or replace the branch history in a way that drops earlier cycle or repair commits.

## 6. Complete

Complete only after validation returns `PASS`:

- confirm all acceptance criteria and recorded test/showcase evidence were validated;
- confirm scope baseline preservation and explain any remaining unrelated changes;
- update the tracker row from `doing` to `done`;
- checkpoint final state;
- archive and close the handoff;
- report story base/final HEAD, cycle and repair commits, tests, demonstration evidence, risk assessment, review result, preflight, decision records changed, and next ready story.

Do not create an extra squashing story commit. The cycle, repair, and focused documentation commits are the implementation history.
