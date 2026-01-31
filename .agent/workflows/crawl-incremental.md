---
description: Perform an incremental crawl to collect only new Moltbook posts. Ideal for daily/hourly updates.
---

# Incremental Crawl Workflow

Crawl only new posts from Moltbook using parallel processing. Already-crawled posts are automatically skipped.

## Steps

1. Run the parallel crawler (auto-skips existing posts):
// turbo
```bash
python3 parallel_crawler.py --limit 100
```

2. Verify new posts were added:
// turbo
```bash
sqlite3 data/moltbook.db "SELECT title, crawled_at FROM posts ORDER BY crawled_at DESC LIMIT 5;"
```

## Notes
- Parallel crawler automatically skips posts already in DB
- Use `--limit N` to cap the number of new posts per run
- Use `--workers N` to adjust parallelism (default: 4)
- Example cron entry for hourly updates:
  ```
  0 * * * * cd /home/seok436/projects/hack-the-moltbook && python3 parallel_crawler.py --limit 50 >> logs/cron.log 2>&1
  ```

