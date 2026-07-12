# Testing Guide

## Testing Approach

Test the `/investigate` workflow at the highest integration seam: CLI interface → workflow orchestration → file output.

Tests verify complete end-to-end command flow without mocking internal agent logic. Use pytest with fixtures for deterministic LLM responses, Rich's built-in `Console` with `record=True` to capture terminal output, and `pytest.TempPathFactory` for isolated file I/O testing.

## Testing Scope

- **CLI interface**: Command parsing, error handling for invalid inputs, routing to investigation workflow
- **LangGraph workflow**: Full orchestration from claim submission to verdict generation (with mocked LLM responses using deterministic fixtures)
- **Report generation**: Markdown output format, metadata accuracy, file persistence
- **Real-time output streaming**: Intermediate findings appear in order, formatting is readable

## Testing Principles

- Tests verify **external behavior only**: claims submitted, real-time findings displayed, reports saved with expected structure
- Tests do NOT verify implementation details like exact agent call order, LLM prompt wording, or internal state
- Tests use realistic test data: actual news stories or well-known events that can be fact-checked

## Test Data Strategy

- Mock LLM responses representing typical findings (supported claims, contradicted claims, unsupported claims)
- Fixture claims: a mix of verifiable facts (easily supported), false claims (contradicted by sources), and ambiguous claims (unsupported)
- Pre-recorded web search results to avoid actual API calls during testing

## Tools and Patterns

### pytest Ecosystem

- Standard Python testing framework with fixtures and parametrization
- `pytest-caplog` and Rich's `Console(record=True)` enable terminal output capture without actual terminal
- `TempPathFactory` provides isolated temporary directories for file I/O testing

### Mock LLM Responses

- Deterministic test outcomes (no flaky tests due to LLM variability)
- Fast test execution (no actual API calls)
- Complete control over test scenarios (supported/contradicted/unsupported verdicts)
- Avoids test costs and rate limits from real LLM providers

### Terminal Output Capture

- Tests use `StringIO` + `Console` to capture and verify output
- Can test formatting without actual terminal
- Example pattern: Capture terminal output → verify findings appear → verify report file structure

### File I/O Testing

- Use temporary directories for isolated report file testing
- Verify Markdown structure with regex or markdown parser
- Use `pytest.TempPathFactory` for isolated test reports
