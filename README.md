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
| `/discover`        | Interview-driven requirements capture; produces `CONTEXT.md`, `docs/00-repo-structure.md`, and ADRs inline |
| `/domain-modeling` | _(optional)_ Re-run after discovery to fill gaps, reverify building blocks, or update layer structure |
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

---

## End-to-End Journey for building the next increment

A complete walkthrough from first conversation to committed code, with every artifact produced along the way.

---

### Step 1 — Discovery

**You run:** `/discover`

The agent interviews you using Socratic questioning to scope the feature. `/domain-modeling` is called inline as terms crystallise — writing artifacts on the spot, not batched at the end.

**Artifacts produced:**
```
CONTEXT.md                          ← domain glossary; every term tagged with its DDD building block type
                                       e.g. Claim (Aggregate Root), Verdict (Value Object)
docs/00-repo-structure.md           ← layer layout and dependency rules for this project
docs/adr/0001-<decision subject>.md   ← only if a hard, reversible architectural decision was made
```

**Example `CONTEXT.md` entry:**
```md
**Claim** _(Aggregate Root)_:
A user-submitted statement to be investigated. Owns its decomposed sub-claims and final verdict.
_Avoid_: query, statement, input
```

### Step 2 — PRD (product requirement document for the increment)

**You run:** `/create-prd`

Synthesises the discovery conversation into a structured requirements document.

**Artifacts produced:**
```
.scratch/belling-cat-mvp/PRD.md     ← full product requirements with acceptance criteria
```

---

### Step 3 — Create Backlog for the increment

**You run:** `/create-backlog`

Breaks the PRD into vertical slices, each a deployable end-to-end behaviour.

**Artifacts produced:**
```
.scratch/belling-cat-mvp/backlog.md              ← tracker with status, blockers, item links
.scratch/belling-cat-mvp/backlog/00-scaffolding.md
.scratch/belling-cat-mvp/backlog/01-blah-foundation.md
.scratch/belling-cat-mvp/backlog/02-claim-decomposition.md
...
```

**Example backlog item header:**
```md
# Item 01: blah Foundation & Command Parsing
Status: to-do
Blocked by: Item 00
```

---

### Step 4 — Implement (per backlog item)

**You run:** `/implement` (or `/implement .scratch/belling-cat-mvp/backlog/01-blah-foundation.md`)

#### 5a. Item resolution

The agent resolves which item to work on:
- Argument provided → validates it is not blocked; stops with a clear message if it is
- No argument → picks the lowest-numbered `to-do` or `doing` item with all dependencies `done`

#### 5b. Handoff bootstrap

Before any code is written, the agent creates the crash-recovery log:

```
.scratch/handoff-context.md         ← records current item, HEAD commit, UTC timestamp
```

#### 5c. TDD loop — RED → GREEN → REFACTOR (repeat)

Each cycle is a complete loop. The agent never starts the next RED until REFACTOR is done.

**Cycle example — "parse /investigate command":**

```
RED:      tests/blah_test.py  ← new failing test added
GREEN:    boo/blah.py        ← minimal code to pass the test
REFACTOR: boo/domain/commands.py  ← InvestigateCommand value object extracted
          boo/blah.py              ← blah.py now delegates, no business logic
```

After each GREEN the agent appends one line to the handoff:
```
## TDD Log
- [2026-06-28T14:32Z] GREEN: /investigate command parsed into InvestigateCommand value object
- [2026-06-28T14:45Z] GREEN: unknown command returns helpful error message
```

#### 5d. Review

After all cycles for the item are complete, `/review` runs three parallel sub-agents:

| Axis | Checks |
|---|---|
| **Standards** | Coding conventions, type annotations, naming |
| **Spec** | Every acceptance criterion in the backlog item met; no scope creep |
| **Architecture** | Layer violations, domain logic purity, unabstracted I/O, ADR compliance |

**Example Architecture finding:**
```
FAIL: boo/blah.py imports openai directly (line 12).
      External I/O must be behind a port (see docs/adr/0002-ports-for-llm.md).
      Move to boo/adapters/openai_llm.py and reference via LLMPort.
```

The agent fixes any findings before continuing.

#### 5e. Preflight & commit

```bash
make preflight   # lint, format, typecheck, full test suite
git commit       # single commit per backlog item
                 # message format: "Item 01: blah foundation and command parsing"
```

**Artifacts produced by the end of one implement cycle:**
```
boo/domain/commands.py      ← new domain value object
boo/ports/llm.py            ← LLMPort interface (if introduced this cycle)
boo/adapters/openai_llm.py  ← concrete adapter
boo/blah.py                  ← updated (thin wiring only)
tests/agents/test_blah.py            ← new behaviour tests
.scratch/handoff-context.md         ← updated TDD log
.scratch/belling-cat-mvp/backlog/01-blah-foundation.md  ← Status: done
```

---

### Step 5 — Next item

Run `/implement` again. The agent reads the backlog, finds item 02 is now unblocked (item 01 is `done`), and starts the same loop from 5b onwards.

```
Item 00 done → Item 01 done → Item 02 unlocked → /implement picks it up automatically
```
