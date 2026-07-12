.PHONY: install lock test lint lint-fix format format-check typecheck workflow-lint preflight clean

PATHS ?= .
MYPY_PATHS ?= .
PYTEST_ARGS ?=

install:
	uv sync --locked

lock:
	uv lock

# Non-mutating checks used by preflight/CI.
test:
	uv run --locked pytest $(PYTEST_ARGS)

lint:
	uv run --locked ruff check $(PATHS)

format-check:
	uv run --locked ruff format --check $(PATHS)

typecheck:
	uv run --locked mypy $(MYPY_PATHS)

workflow-lint:
	python scripts/validate_agent_workflow.py

# Explicitly mutating developer commands. Limit PATHS during focused work.
lint-fix:
	uv run --locked ruff check $(PATHS) --fix

format:
	uv run --locked ruff format $(PATHS)

preflight: workflow-lint lint format-check typecheck test

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -path './.venv' -prune -o -path './.git' -prune -o -type d -name __pycache__ -exec rm -rf {} +
