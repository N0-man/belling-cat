# Belling Cat

A terminal-based fact-checking application using multi-agent LLM architecture.

## Setup

Install dependencies using `uv`:

```bash
uv sync
```

## Development

Run tests:
```bash
make test
```

Run linter:
```bash
make lint
```

Run type checker:
```bash
make typecheck
```

## Usage

Start the application:
```bash
uv run python -m belling_cat
```

## Agentic Workflow

This repo is developed with [opencode](https://opencode.ai) agents. The pipeline for each feature is:

```
/discover → /create-prd → /create-backlog → [per item: /implement → /review → /commit]
```

Phases are sequential — do not skip them. **One backlog item at a time.**

### Human-triggered commands

All human-triggered commands run in **build mode** (`build` agent — full permissions).

| Command            | Purpose                                                          |
| ------------------ | ---------------------------------------------------------------- |
| `/discover`        | Interview-driven requirements capture; produces glossary and ADRs |
| `/domain-modeling` | Build domain model — classify DDD building blocks, write `CONTEXT.md` and `docs/00-repo-structure.md`, record ADRs |
| `/create-prd`      | Synthesise conversation into `.scratch/<feature>/PRD.md`         |
| `/create-backlog`  | Break PRD into backlog items under `.scratch/<feature>/backlog/` |
| `/implement`       | Implement one backlog item using TDD + self-review               |

### Agent-triggered commands

Called internally by other commands — do not invoke these directly.

| Command            | Called by       | Purpose                                                         |
| ------------------ | --------------- | --------------------------------------------------------------- |
| `/grilling`        | `/discover`     | Socratic questioning to sharpen scope                           |
| `/domain-modeling` | `/discover`     | Called inline during discovery to capture terms as they emerge  |
| `/tdd`             | `/implement`    | Red-green-refactor loop (one test at a time)                    |
| `/review`          | `/implement`    | Three-axis review — Standards, Spec, and Architecture — via parallel sub-agents |
| `/test-affected`   | `/implement`    | Run only the tests affected by current changes                  |
| `/commit`          | `/implement`    | Stage and commit reviewed changes                               |
| `/preflight`       | `/implement`, `/commit` | Full CI-equivalent checks before committing or pushing  |
| `/lint`            | `/preflight`    | Auto-fix lint and formatting                                    |
| `/handoff`         | `/implement`    | Bootstrap handoff at item start; append TDD log entries after each GREEN cycle |

### Backlog item format

Each item in `.scratch/<feature>/backlog/` contains:

- What to build (end-to-end behaviour, not layer-by-layer)
- Acceptance criteria
- `Blocked by:` dependencies
- `Status:` — `to-do` | `doing` | `done`

### Resuming work

`/implement` manages crash recovery automatically. At the start of each item it bootstraps `.scratch/handoff-context.md`, then appends a one-line log entry after every GREEN TDD cycle. If opencode crashes, reopen the session and re-run `/implement` — it will resolve the same in-progress item from the backlog and the TDD log shows exactly how far it got.
