# Item 00: Scaffolding & Tech Stack Setup

## Status

to-do

## Parent

.scratch/belling-cat-mvp/PRD.md

## What to build

Set up the foundational Python project structure with modern tooling and establish testing infrastructure. This vertical slice creates a working development environment with all dependencies configured, a Makefile for common tasks, and a pytest framework ready for TDD workflows.

The deliverable is a runnable project skeleton where developers can execute `make test`, `make lint`, and `make typecheck` successfully (even if tests are minimal at this stage).

## Acceptance criteria

- [ ] Python project initialized with `uv` for dependency management
- [ ] `pyproject.toml` configured with project metadata and dependencies (Rich, Yachalk, OpenAI SDK, LangGraph, pytest, pytest-asyncio)
- [ ] Makefile created with targets: `make test`, `make lint`, `make typecheck`, `make install`
- [ ] Pytest configured with basic project structure (`tests/` directory, `conftest.py` if needed)
- [ ] Basic smoke test passes (e.g., `test_imports.py` verifying core dependencies load)
- [ ] `.gitignore` includes Python artifacts (`__pycache__`, `.pytest_cache`, `.venv/`, etc.)
- [ ] README stub created with setup instructions

## Blocked by

None - can start immediately
