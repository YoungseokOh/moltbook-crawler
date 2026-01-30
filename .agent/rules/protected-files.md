---
activation: always
description: Critical files and components that must NOT be modified without explicit user approval.
---

# Protected Files - DO NOT MODIFY

## ⚠️ Critical Warning
The following files and components are **protected**. Do NOT modify these without explicit user confirmation.

---

## Database
- **`data/moltbook.db`**: Production database containing crawled posts and comments.
  - ❌ Do not DELETE or TRUNCATE tables without user approval.
  - ❌ Do not modify the schema without updating `sql/schema.sql`.
  - ✅ INSERT/UPDATE operations via the crawler are allowed.

## Core Crawler Logic
- **`moltbook/crawler.py`**: 
  - `_init_driver()`: WebDriver initialization and evasion techniques.
  - `_wait_for_content()`: Dynamic content loading logic.
  - ❌ Do not change these methods without testing.

- **`moltbook/db.py`**:
  - `save_post()`, `save_comment()`: Database write operations.
  - ❌ Do not modify without ensuring data integrity.

## Configuration
- **`moltbook/config.py`**:
  - `BASE_URL`, `POST_BASE_URL`: Target website URLs.
  - `USER_AGENT`: Browser fingerprint for evasion.
  - ❌ Changing these may break the crawler or trigger bot detection.

## Schema
- **`sql/schema.sql`**:
  - Table definitions for `posts`, `comments`, `agents`.
  - ❌ Schema changes require migration planning.

---

## Safe to Modify
- `dashboard/`: UI and visualization code.
- `research/`: Experimental scripts and dumps.
- `test_crawl_post.py`: Testing utility.
- `.agent/`: Agent configuration files.
- `README.md`, `.gitignore`: Documentation.
