---
activation: always
description: Python coding standards for the Moltbook crawler project.
---

# Coding Rules

## Python Style
- Follow PEP 8 style guidelines.
- Use type hints for function parameters and return values.
- Use f-strings for string formatting.
- Maximum line length: 100 characters.

## Naming Conventions
- Classes: `PascalCase` (e.g., `MoltbookCrawler`)
- Functions/Variables: `snake_case` (e.g., `get_post_links`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `BASE_URL`)
- Private methods: prefix with `_` (e.g., `_random_delay`)

## Imports
- Group imports: stdlib → third-party → local
- Use absolute imports for local modules (e.g., `from moltbook.db import save_post`)

## Error Handling
- Use specific exception types, not bare `except:`.
- Log errors with `logger.error()` before raising or returning.
- Always close resources (use `with` statements for files, DB connections).

## Logging
- Use the `logging` module, not `print()`.
- Log levels: DEBUG for verbose, INFO for normal, WARNING/ERROR for issues.

## Documentation
- Docstrings for all public classes and functions.
- Use `"""Triple quotes"""` for docstrings.
