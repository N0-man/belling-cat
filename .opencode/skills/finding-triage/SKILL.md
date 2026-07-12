---
name: finding-triage
description: Classify review, audit, validation, test, and documentation findings by severity and decision ownership so safe repairs proceed and intent-changing choices return to the user.
compatibility: opencode
metadata:
  workflow: quality
---

# Finding Triage

Severity and action are independent. A severe defect may still require the user when its correction changes agreed behaviour, while a minor documentation gap may be repaired directly.

## Actions

Assign exactly one action to every finding.

### `repair`

Use when the correction is clearly inside approved intent and does not require a new product or material architecture choice.

Examples:

- specified behaviour is implemented incorrectly;
- error handling, security, resource cleanup, or validation is defective;
- an affected test, type check, or lint check fails;
- accepted documentation or decision references are stale in an unambiguous way;
- a local simplification preserves behaviour and accepted constraints.

Repairs to executable behaviour use a new protected TDD/safety cycle. Documentation-only repairs use a focused documentation commit with verification.

### `ask-user`

Use when resolving the finding would:

- change observable behaviour, a contract, data semantics, or scope;
- challenge a deliberate user choice or ruled-out approach;
- add or replace a material dependency;
- select among unresolved architecture alternatives;
- remove or restore functionality whose intent is unclear;
- require accepting a risk rather than correcting a defect.

When uncertain, choose `ask-user`. Preserve the finding verbatim enough for the user to make the decision. Never approve, repair, or dismiss it on the user's behalf.

### `record-decision`

Use when implementation may remain as-is but its material rationale, ownership rule, or trade-off is absent or stale.

- If the underlying choice was already approved, invoke the `decision-recording` skill and update references.
- If approval cannot be established, reclassify as `ask-user`.

### `no-op`

Use for an observation that requires no change: an acknowledged trade-off, optional future improvement, or information already covered by an accepted record.

## Finding contract

Each finding records:

- stable ID and source axis;
- severity: `blocking`, `major`, `minor`, or `observation`;
- action: `repair`, `ask-user`, `record-decision`, or `no-op`;
- precise evidence and impact;
- violated requirement, standard, decision, or invariant when applicable;
- focused remediation or decision question;
- status: `open`, `in-repair`, `awaiting-user`, `resolved`, or `accepted`;
- resolution commit or decision reference when closed.

## Round handling

- Preserve IDs across review and repair rounds.
- Mark findings resolved; do not erase their history.
- Deduplicate by underlying issue rather than file line alone.
- Add a finding the agent notices independently instead of hiding it because a reviewer missed it.
- Re-review the affected axis after repair.
- A validation gate passes only when no `blocking` or `major` finding remains open and no `ask-user` finding is unanswered.
