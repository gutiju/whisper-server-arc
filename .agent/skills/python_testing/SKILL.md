---
name: python_testing
description: Guidelines and best practices for creating unit and integration tests in Python.
---

# Python Testing Skill

This skill provides guidelines for implementing a robust testing strategy for Python applications, covering both unit and integration tests.

## Testing Frameworks
- **[pytest](https://docs.pytest.org/)**: The recommended framework for its simplicity and powerful features (fixtures, parameterization).
- **unittest**: The built-in Python library, useful for legacy projects or minimal dependencies.

## Testing Strategy

### 1. Unit Tests
- **Scope**: Focus on testing individual functions or classes in isolation.
- **Mocking**: Use `pytest-mock` to isolate the unit under test from external dependencies (databases, APIs, filesystem).
- **Naming**: Test files should be prefixed with `test_` and placed in a `tests/unit` directory (if categorized) or directly in `tests/`.

### 2. Integration Tests
- **Scope**: Verify that different components of the application work together correctly.
- **Dependencies**: May involve real or containerized dependencies (e.g., using `testcontainers`).
- **Placement**: Place in `tests/integration/` (if categorized) or `tests/`.

## Best Practices

### Writing Tests
- [ ] **Arrange-Act-Assert**: Follow this pattern to keep tests structured and readable.
- [ ] **Descriptive Names**: Name tests based on the behavior they verify (e.g., `test_transcribe_with_invalid_audio_format_returns_error`).
- [ ] **Parameterization**: Use `pytest.mark.parametrize` to run the same test logic with different input data.
- [ ] **Fast Execution**: Unit tests should be extremely fast. Integration tests can be slower but should still be optimized.

### Fixtures and Setup
- [ ] **Mocking External APIs**: Never call real external APIs in unit tests.
- [ ] **Cleanup**: Ensure tests clean up any resources they create (temp files, database entries).
- [ ] **Independence**: Each test must be independent and not rely on the state left by another test.

### Coverage and Verification
- [ ] **Maintainability**: Tests are code too. Keep them clean and avoid logic in tests.
- [ ] **Edge Cases**: Specifically test boundary conditions, empty inputs, and error states.
