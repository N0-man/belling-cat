.PHONY: install test lint typecheck preflight clean

install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check . --fix
	uv run ruff format .

typecheck:
	uv run mypy belling_cat

preflight: lint typecheck test
	@echo "✓ Preflight checks passed"

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
