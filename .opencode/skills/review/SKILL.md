---
name: review
description: Review the changes since a fixed point along three axes — Standards (coding conventions), Spec (acceptance criteria), and Architecture (domain model, DDD layer placement, ADR compliance). Runs all three in parallel sub-agents and reports them side by side.
---

Three-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?
- **Architecture** — does the code respect the domain model, DDD layer boundaries, and ADRs?

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) and map them to local issue artifacts under `.scratch/<feature-name>/issues/` and `.scratch/<feature-name>/issue-tracker.md` when available.
2. A path the user passed as an argument.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

### 4. Identify the architecture sources

- `CONTEXT.md` — domain glossary with DDD building block types
- `docs/00-repo-structure.md` — layer layout and dependency rules
- `docs/adr/` — all ADRs

If none of these exist, the **Architecture** sub-agent will skip and report "no architecture sources available".

### 5. Spawn all three sub-agents in parallel

Send a single message with two `Agent` tool calls.

Sub-agent selection policy:

- Prefer the `Explore` sub-agent for both axes when it is available.
- If `Explore` is unavailable, use the current/default agent as fallback.
- Use the same agent choice for both axes in a single review run.

**Standards sub-agent prompt** — include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3.
- The brief: "Report — per file/hunk where relevant — every place the diff violates a documented standard. Cite the standard (file + the rule). Distinguish hard violations from judgement calls. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** — include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

**Architecture sub-agent prompt** — include:

- The diff command and commit list.
- The paths to `CONTEXT.md`, `docs/00-repo-structure.md`, and `docs/adr/`.
- The brief: "Report: (a) domain terms used with the wrong DDD building block type; (b) layer dependency rule violations (inner layer importing outer); (c) external I/O not behind a port; (d) ADR decisions contradicted by the diff. Cite the source for each finding. Under 400 words."

If architecture sources are missing, skip this sub-agent and note it in the final report.

### 6. Aggregate

Present the three reports under `## Standards`, `## Spec`, and `## Architecture` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings — the axes are deliberately separate.

End with a one-line summary: total findings per axis and the worst issue within each (if any).

## Why three axes

Each axis catches failures the others miss:

- Correct standard, wrong feature → **Standards pass, Spec fail**
- Correct feature, messy code → **Spec pass, Standards fail**
- Both clean, but a Value Object is making HTTP calls → **Architecture fail**

Keeping them separate stops one axis from masking another.
