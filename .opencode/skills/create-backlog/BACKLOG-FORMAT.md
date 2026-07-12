# Product backlog tracker format

```md
---
increment: <kebab-case-name>
prd: .scratch/<increment>/PRD.md
updated_at: <UTC timestamp>
---

# Product Backlog: <Increment title>

| Order | ID | Story | Status | Blocked by | Value / showcase | File |
|---:|---|---|---|---|---|---|
| 1 | ITEM-01 | ... | to-do | — | ... | [story](backlog/01-...md) |
```

## Tracker rules

- This tracker is the source of truth for story status, order, and blockers.
- Valid statuses are `to-do`, `doing`, and `done`.
- `blocked` is computed from unfinished dependencies and is not stored as a status.
- Only one story may be `doing`.
- Story files must not duplicate mutable status or blockers.
- Update `updated_at` whenever tracker state changes.
- A `done` story must have checked acceptance criteria and recorded evidence in its story file; the archived handoff preserves supporting execution history.
