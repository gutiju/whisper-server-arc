---
name: python_code_review
description: Guidelines and best practices for performing code reviews in Python projects.
---

# Python Code Review Skill

This skill provides a checklist and best practices for performing effective code reviews on Python codebases.

## Prerequisites
- Knowledge of [PEP 8](https://peps.python.org/pep-0008/) style guide.
- Familiarity with the project's specific coding standards.

## Code Review Checklist

### 1. Style and Standards (PEP 8)
- [ ] **Naming Conventions**: Are variables (`snake_case`), functions (`snake_case`), classes (`PascalCase`), and constants (`UPPER_SNAKE_CASE`) named correctly?
- [ ] **Indentation**: Is the standard 4-space indentation used?
- [ ] **Line Length**: Are lines kept within a reasonable length (79-88 characters or project preference)?
- [ ] **Imports**: Are imports sorted (StdLib, Third Party, Local) and follow PEP 8?

### 2. Documentation and Type Hinting
- [ ] **Docstrings**: Are all public modules, classes, and functions documented? Use Google or NumPy style.
- [ ] **Type Hints**: Are function signatures annotated with type hints to improve readability and static analysis?
- [ ] **Comments**: Are comments used to explain *why* something is done, rather than *what* is done?

### 3. Logic and Efficiency
- [ ] **DRY (Don't Repeat Yourself)**: Is there duplicated logic that could be refactored?
- [ ] **Readability**: Is the logic easy to follow? Avoid overly complex one-liners.
- [ ] **Resource Management**: Are files and connections handled using context managers (`with` statements)?
- [ ] **Performance**: Are there obvious bottlenecks (e.g., nested loops that could be vectorized or optimized)?

### 4. Error Handling
- [ ] **Exceptions**: Are exceptions specific (e.g., `ValueError` instead of `Exception`)?
- [ ] **Graceful Degradation**: Does the code handle edge cases and failures gracefully?

### 5. Security
- [ ] **Sanitization**: Is user input properly sanitized?
- [ ] **Hardcoded Secrets**: Ensure no credentials or API keys are hardcoded.
