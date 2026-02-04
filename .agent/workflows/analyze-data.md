---
description: Generate analysis reports and find insights from Moltbook data
---

# Analyze Moltbook Data

Run analysis on downloaded data to find interesting patterns.

## Steps

1. Load data and generate summary stats:
// turbo
```bash
python3 -c "
from analysis import load_posts, load_comments
from analysis.stats import get_summary_stats

posts = load_posts()
comments = load_comments()
stats = get_summary_stats(posts, comments)

print(f'Total posts: {stats[\"total_posts\"]}')
print(f'Total comments: {stats[\"total_comments\"]}')
print(f'Top 5 Authors: {list(stats[\"top_authors\"].items())[:5]}')
print(f'Top 5 Submolts: {list(stats[\"top_submolts\"].items())[:5]}')
"
```

2. Find dangerous/interesting posts:
// turbo
```bash
python3 -c "
from analysis import load_posts
from analysis.insights import find_dangerous_posts, get_insight_report

posts = load_posts()
dangerous = find_dangerous_posts(posts)

print(f'Found {len(dangerous)} dangerous posts')
for _, row in dangerous.head(10).iterrows():
    print(f'  - {row[\"title\"][:50]}... [{row[\"matched_keywords\"]}]')
"
```

## Notes
- Requires data to be downloaded first (use /download-data)
- Analysis functions in `analysis/` module
