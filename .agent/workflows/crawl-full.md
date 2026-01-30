---
description: Perform a full crawl of all Moltbook posts. Use for initial data collection or complete refresh.
---

# Full Crawl Workflow

Crawl all posts from Moltbook's main feed and store them in the database.

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
- This crawl may take several minutes depending on the number of posts.
- Use `--limit N` to restrict the number of posts if needed.
- For subsequent updates, use `/crawl-incremental` instead.
