---
name: moltbook-crawler
description: Selenium-based crawler for Moltbook.com. Use when crawling posts, comments, or managing the crawled data. Handles full crawls, incremental updates, and specific post extraction.
---

# Moltbook Crawler Skill

This skill provides guidance for using the Moltbook crawler to collect posts and comments from moltbook.com.

## When to use this skill

- Crawling posts from Moltbook
- Running incremental updates to get new posts only
- Crawling a specific post by URL
- Checking database status or managing crawled data
- Starting/stopping the data dashboard

## Project Structure

```
hack-the-moltbook/
├── moltbook/           # Core crawler package
│   ├── config.py       # Configuration constants
│   ├── crawler.py      # Selenium crawling logic
│   ├── db.py           # SQLite database operations
│   └── models.py       # Data models (Post, Comment)
├── dashboard/          # Flask web dashboard
├── main.py             # CLI entry point
└── data/moltbook.db    # SQLite database
```

## Available Commands

### Full Crawl
Crawl all posts from the main feed:
```bash
python3 main.py
```

### Limited Crawl
Crawl a specific number of posts:
```bash
python3 main.py --limit 10
```

### Incremental Update
Only crawl new posts (skip existing):
```bash
python3 main.py --incremental
```

### Debug Mode
Run with visible browser and verbose logging:
```bash
python3 main.py --no-headless -v
```

### Start Dashboard
View crawled data in a web interface:
```bash
python3 dashboard/app.py
# Access at http://127.0.0.1:5000
```

## Database Operations

Check database status:
```bash
sqlite3 data/moltbook.db "SELECT COUNT(*) FROM posts;"
sqlite3 data/moltbook.db "SELECT COUNT(*) FROM comments;"
```

View recent posts:
```bash
sqlite3 data/moltbook.db "SELECT title, author_name FROM posts ORDER BY crawled_at DESC LIMIT 5;"
```

## Crawling a Specific Post

Use `test_crawl_post.py` or modify the target URL:
```python
from moltbook.crawler import MoltbookCrawler
from moltbook.db import init_db, save_post

init_db()
with MoltbookCrawler(headless=True) as crawler:
    post = crawler.parse_post("https://www.moltbook.com/post/<post-id>")
    if post:
        save_post(post)
```

## Decision Tree

| Goal | Command |
|------|---------|
| First-time full crawl | `python3 main.py` |
| Daily updates | `python3 main.py --incremental` |
| Test with few posts | `python3 main.py --limit 5` |
| Debug issues | `python3 main.py --no-headless -v` |
| View data | `python3 dashboard/app.py` |
