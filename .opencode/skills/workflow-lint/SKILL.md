---
name: workflow-lint
description: Validate OpenCode skills, commands, agents, references, permissions, templates, and documentation tables for structural drift.
compatibility: opencode
metadata:
  workflow: maintenance
---

# Workflow Lint

Run the repository-owned validator:

```bash
python scripts/validate_agent_workflow.py
```

or the canonical Make target:

```bash
make workflow-lint
```

## Checks

The validator should fail on:

- invalid JSON in `opencode.json`;
- missing or malformed skill frontmatter;
- unsupported OpenCode skill frontmatter keys;
- invalid skill names or names that do not match their directories;
- missing descriptions;
- command references to nonexistent skills or agents;
- task permission entries for nonexistent subagents;
- missing format/template files referenced by skills;
- review/audit subagents that are not explicitly read-only;
- commands or skills omitted from the canonical command documentation;
- known obsolete workflow markers or contradictory state vocabulary.

Warnings may identify weaker concerns that cannot be proven mechanically, but errors must produce a non-zero exit code.

## Source-of-truth rule

Do not duplicate build, test, lint, typecheck, or preflight commands across many instruction files. The `Makefile` or repository CI configuration owns executable commands; agent guidance references that owner.

Run workflow lint whenever skills, commands, agents, templates, `AGENTS.md`, `README.md`, or `opencode.json` change, and include it in preflight when the repository carries this workflow.
