---
name: create-prd
description: Turn the current conversation into a single-feature PRD saved locally under .scratch/<feature-name>/PRD.md — this is just synthesis of what you've already discussed.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a PRD. Each PRD and conversation is for a single feature only. Do not run a broad interview. Synthesize from existing context; ask at most one targeted clarification only if testing seams are ambiguous.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

If seam choice is ambiguous, ask one focused confirmation question to align expectations. If seams are already clear from context, do not ask follow-up questions.

3. The PRD will be saved under .scratch/<feature-name>/PRD.md. Define the feature name based on the current conversation context.

4. Write the PRD using the template below and save it to `.scratch/<feature-name>/PRD.md`.

5. If a per-feature tracker exists at `.scratch/<feature-name>/backlog.md`, do not rewrite historical backlog item statuses. Only add a short note (optional) linking this PRD to that tracker.

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Scope

A LONG, numbered list of GIVEN, WHEN, THEN statements based on the conversation

1. GIVEN user enters query, WHEN the user hits enter, THEN the solution should
   (a) Extract filter cues from the query such as time and location using LLM
   (b) Decompose query into smaller CLIP style caption queries using LLM
   (c) Both a and b should be structured into JSON

This list of scope statements should be extremely extensive and cover all aspects of the feature (positive and negative scenarios).

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
