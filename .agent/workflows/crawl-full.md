---
description: Perform a full crawl of all Moltbook posts. Use for initial data collection or complete refresh.
---

# Full Crawl Workflow

Crawl all posts from Moltbook's main feed and store them in the database.
Uses streaming mode to process posts immediately as they're discovered.

## Steps

1. Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Run the full crawler:
// turbo
```bash
python3 main.py
```

3. Verify results:
// turbo
```bash
sqlite3 data/moltbook.db "SELECT COUNT(*) AS posts FROM posts; SELECT COUNT(*) AS comments FROM comments;"
```

## Notes
- Posts are processed immediately as discovered (no waiting for full feed scan)
- Already-crawled posts are automatically skipped
- Use `--limit N` to restrict the number of NEW posts
- Use `--batch-size N` to control processing batch size (default: 10)
- Ctrl+C safely stops crawling while preserving already-saved data
