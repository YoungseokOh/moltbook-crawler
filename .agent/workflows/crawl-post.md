---
description: Crawl a specific Moltbook post by its URL. Use when you need to extract a single post and its comments.
---

# Crawl Specific Post Workflow

Crawl a single post from Moltbook by providing its URL.

## Steps

1. User provides the target post URL (e.g., `https://www.moltbook.com/post/<post-id>`).

2. Update `test_crawl_post.py` with the target URL:
```python
target_url = "https://www.moltbook.com/post/<post-id>"
```

3. Run the specific post crawler:
// turbo
```bash
python3 test_crawl_post.py
```

4. Verify the post was saved:
// turbo
```bash
sqlite3 data/moltbook.db "SELECT title, comment_count FROM posts ORDER BY crawled_at DESC LIMIT 1;"
```

## Alternative: Direct Python
```python
from moltbook.crawler import MoltbookCrawler
from moltbook.db import init_db, save_post

init_db()
with MoltbookCrawler(headless=True) as crawler:
    post = crawler.parse_post("https://www.moltbook.com/post/<post-id>")
    if post:
        save_post(post)
        print(f"Saved: {post.title} ({len(post.comments)} comments)")
```
