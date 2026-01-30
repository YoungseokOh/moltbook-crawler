---
description: Perform an incremental crawl to collect only new Moltbook posts. Ideal for daily/hourly updates.
---

# Incremental Crawl Workflow

Crawl only new posts from Moltbook, skipping posts already in the database.

## Steps

1. Run the incremental crawler:
// turbo
```bash
python3 main.py --incremental
```

2. Verify new posts were added:
// turbo
```bash
sqlite3 data/moltbook.db "SELECT title, crawled_at FROM posts ORDER BY crawled_at DESC LIMIT 5;"
```

## Notes
- Use this workflow for periodic updates (e.g., cron jobs).
- Combine with `--limit N` to cap the number of new posts per run.
- Example cron entry for hourly updates:
  ```
  0 * * * * cd /home/seok436/projects/hack-the-moltbook && python3 main.py --incremental >> logs/cron.log 2>&1
  ```
