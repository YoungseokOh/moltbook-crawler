---
activation: always
description: Git commit message conventions for the Moltbook crawler project.
---

# Commit Rules

## Commit Message Format
```
<type>: <short description>

[optional body]
```

## Types
| Type | Description |
|------|-------------|
| `feat` | New feature (e.g., `feat: add comment pagination`) |
| `fix` | Bug fix (e.g., `fix: handle empty comment sections`) |
| `refactor` | Code refactoring without behavior change |
| `docs` | Documentation updates |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks (deps, configs, etc.) |

## Guidelines
- Use imperative mood: "add feature" not "added feature".
- Keep the first line under 50 characters.
- Reference issue numbers if applicable: `fix: resolve #123`.
- Separate subject from body with a blank line.

## Examples
```
feat: add incremental crawl mode

Skip posts already in the database to avoid redundant processing.
```

```
fix: correct comment selector for individual extraction

Changed from div.bg-[#1a1a1b] to div.py-2 for accurate parsing.
```

## Before Committing
1. Run the crawler to verify no regressions.
2. Check database integrity with `/db-status`.
3. Ensure no debug code or test URLs remain.
