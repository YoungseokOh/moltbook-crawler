---
description: Check the status of the Moltbook database. Shows counts of posts, comments, and recent entries.
---

# Database Status Workflow

Check the current state of the crawled data in the SQLite database.

## Steps

1. Show overall counts:
// turbo
```bash
sqlite3 data/moltbook.db "SELECT 'Posts' AS type, COUNT(*) AS count FROM posts UNION ALL SELECT 'Comments', COUNT(*) FROM comments UNION ALL SELECT 'Agents', COUNT(*) FROM agents;"
```

2. Show recent posts:
// turbo
```bash
sqlite3 data/moltbook.db "SELECT title, author_name, comment_count, datetime(crawled_at) FROM posts ORDER BY crawled_at DESC LIMIT 5;"
```

3. Show database file size:
// turbo
```bash
ls -lh data/moltbook.db
```

## Optional: Vacuum Database
To optimize and reduce database file size:
```bash
sqlite3 data/moltbook.db "VACUUM;"
```
