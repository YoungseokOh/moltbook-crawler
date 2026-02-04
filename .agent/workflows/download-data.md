---
description: Download all posts, comments, and agents from Moltbook API
---

# Download Data from Moltbook

Downloads all available data using the public API.

## Steps

// turbo
1. Run the API downloader:
```bash
python3 api_downloader.py
```

2. Check download progress:
// turbo
```bash
ls data/posts | wc -l && ls data/agents 2>/dev/null | wc -l
```

## Notes
- Resumes from checkpoint automatically
- To start fresh: `python3 api_downloader.py --no-resume`
- Data saved to `data/posts/`, `data/agents/`, `data/submolts/`
- Rate limited: ~100 requests/min
