---
description: Perform a full crawl of all Moltbook posts. Use for initial data collection or complete refresh.
---

# Full Crawl Workflow

Crawl all posts from Moltbook's main feed using parallel processing (4 browser instances).

## Steps

1. Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Run the parallel crawler:
// turbo
```bash
python3 parallel_crawler.py
```

3. Verify results:
// turbo
```bash
sqlite3 data/moltbook.db "SELECT COUNT(*) AS posts FROM posts; SELECT COUNT(*) AS comments FROM comments;"
```

## Notes
- Uses 4 browser instances by default (~6 posts/min)
- Use `--workers N` to adjust parallelism
- Use `--limit N` to restrict the number of NEW posts
- Use `--batch-size N` to control link collection batch size (default: 50)
- Ctrl+C safely stops crawling while preserving already-saved data
- Estimated time for 11k posts: ~1 day
