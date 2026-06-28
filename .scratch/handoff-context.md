# Handoff Context

## Metadata

- Generated at (UTC): 2026-06-28T18:45:00Z
- Current HEAD: e824d6be3571ef1bb962be4f2d0a0d36e0eb528c
- Previous handoff HEAD: none
- Stale context detected: no

## Next-session focus

**Start implementation with Item 00: Scaffolding & Tech Stack Setup**

The next session should begin implementing the Belling Cat MVP by setting up the foundational Python project structure, configuring the tech stack (uv, Makefile, pytest), and establishing the testing infrastructure.

## Current status

**Discovery and planning phases complete. Ready for implementation.**

- ✅ Completed `/discover` session to gather requirements for Belling Cat fact-checking terminal
- ✅ Created PRD at `.scratch/belling-cat-mvp/PRD.md` with full scope, implementation decisions, and testing approach
- ✅ Created backlog with 8 vertical slices (Item 00 → Item 07) at `.scratch/belling-cat-mvp/backlog.md`
- ✅ Each backlog item has detailed acceptance criteria and clear dependencies
- 🔜 Ready to start Item 00 (Scaffolding & Tech Stack Setup)

### What Belling Cat Does

Belling Cat is a terminal-based fact-checking application that uses multi-agent LLM architecture to investigate news claims and events using open intelligence (OSINT) techniques.

**Key features:**
- `/investigate <claim>` command triggers LLM-powered investigation with real-time web search
- Multi-agent pipeline: Claim Decomposition → Investigation → Verification → Verdict
- Different LLM models per agent (GPT-4o mini, GPT-4 Turbo, GPT-4o) optimized for each phase
- Real-time streaming of findings to terminal (using Rich + Yachalk for UI)
- User reviews verdict with ambiguous claims highlighted before saving
- `/save <report-name>` generates Markdown reports to `.reports/` directory
- Session persistence with continuous auto-save to `.session/` for crash recovery

### Tech Stack Decisions

- **Language**: Python
- **Dependency management**: uv
- **Terminal UI**: Rich (structured output, Live Display) + Yachalk (colors)
- **LLM orchestration**: LangGraph for multi-agent coordination
- **LLM provider**: OpenAI Chat Completion API with web search capability
- **Testing**: pytest with fixtures for mocked LLM responses
- **Build automation**: Makefile (make test, make lint, make typecheck)

## Open decisions and blockers

**None.** All major decisions resolved during discovery:

- Multi-agent architecture defined (3 specialized agents)
- LLM model assignments per agent confirmed
- Terminal UI framework chosen (Rich + Yachalk)
- Report format (Markdown) and persistence strategy decided
- Session persistence approach specified (continuous auto-save to `.session/`)

## Suggested next actions

1. **Implement Item 00**: Set up project scaffolding with uv, create `pyproject.toml` with dependencies (Rich, Yachalk, OpenAI SDK, LangGraph, pytest), establish Makefile with targets for test/lint/typecheck
2. **Verify scaffolding**: Run `make test` to confirm basic smoke tests pass
3. **Implement Item 01**: Build CLI foundation with ASCII banner, command parser for `/investigate` and `/save`
4. **Continue through backlog**: Follow dependency order (Item 00 → Item 07) using TDD approach

## Suggested skills

- `/implement` - Use this skill to implement each backlog item using TDD (one test → minimal code → pass → next test)
- `/tdd` - If you want granular TDD workflow control
- `/review` - After completing one or more backlog items, review changes along Standards and Spec axes
- `/commit` - Commit completed and reviewed backlog items
- `/test-affected` - Run tests affected by recent changes during implementation
- `/lint` - Auto-fix lint and formatting issues before committing

## References

### Core Documents
- **PRD**: `.scratch/belling-cat-mvp/PRD.md`
- **Backlog tracker**: `.scratch/belling-cat-mvp/backlog.md`

### Backlog Items (Vertical Slices)
- **Item 00**: `.scratch/belling-cat-mvp/backlog/00-scaffolding-tech-stack.md` (NEXT)
- **Item 01**: `.scratch/belling-cat-mvp/backlog/01-cli-foundation.md`
- **Item 02**: `.scratch/belling-cat-mvp/backlog/02-claim-decomposition.md`
- **Item 03**: `.scratch/belling-cat-mvp/backlog/03-investigation-evidence.md`
- **Item 04**: `.scratch/belling-cat-mvp/backlog/04-verifier-verdict.md`
- **Item 05**: `.scratch/belling-cat-mvp/backlog/05-report-generation.md`
- **Item 06**: `.scratch/belling-cat-mvp/backlog/06-session-loop.md`
- **Item 07**: `.scratch/belling-cat-mvp/backlog/07-session-persistence.md`

### Important Context
- MVP scope excludes `/interview me` mode (deferred to post-MVP)
- Session persistence uses continuous auto-save to `.session/` directory
- Reports saved to `.reports/` directory as Markdown
- User approval required after verdict display before saving (Item 04)
- Testing uses mocked LLM responses for fast unit/integration tests, with optional slow tests using real OpenAI API

### Workflow Notes
- Each backlog item is a **tracer bullet** (vertical slice cutting through all layers)
- Use TDD discipline: one test at a time, RED → GREEN → refactor
- Tests verify external behavior only (not implementation details)
- Backlog items must be completed in dependency order
