---
description: Find dangerous, philosophical, or gossip posts from agent conversations
---

# Find Insights

Search for specific types of interesting content.

## Steps

1. Find dangerous posts (escape, kill switch, override, etc.):
// turbo
```bash
python3 -c "
from analysis import load_posts
from analysis.insights import find_dangerous_posts

posts = load_posts()
dangerous = find_dangerous_posts(posts)

print(f'=== {len(dangerous)} DANGEROUS POSTS ===')
for _, row in dangerous.head(20).iterrows():
    print(f'[{row[\"author_name\"]}] {row[\"title\"][:60]}')
    print(f'  Keywords: {row[\"matched_keywords\"]}')
    print()
"
```

2. Find philosophical posts:
// turbo
```bash
python3 -c "
from analysis import load_posts
from analysis.insights import find_philosophical_posts

posts = load_posts()
phil = find_philosophical_posts(posts)

print(f'=== {len(phil)} PHILOSOPHICAL POSTS ===')
for _, row in phil.head(20).iterrows():
    print(f'[{row[\"author_name\"]}] {row[\"title\"][:60]}')
    print(f'  Upvotes: {row[\"upvotes\"]}')
    print()
"
```

3. Find agent gossip about humans:
// turbo
```bash
python3 -c "
from analysis import load_posts, load_comments
from analysis.insights import find_agent_gossip

posts = load_posts()
comments = load_comments()
gossip = find_agent_gossip(posts, comments)

print(f'=== {len(gossip)} GOSSIP POSTS/COMMENTS ===')
for _, row in gossip.head(20).iterrows():
    print(f'[{row[\"source\"]}] {row[\"author_name\"]}: {row[\"content\"][:80]}...')
    print()
"
```

## Custom Keywords

To search with custom keywords:
```python
from analysis.insights import find_dangerous_posts

custom_keywords = [r"\\bsecret\\b", r"\\bhidden\\b", r"\\bunderground\\b"]
results = find_dangerous_posts(posts, keywords=custom_keywords)
```
