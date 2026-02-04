---
name: Moltbook Data Analysis
description: Guide for analyzing Moltbook AI agent social network data
---

# Moltbook Data Analysis Skill

This skill provides guidance on analyzing data from Moltbook, an AI agent social network.

## Data Structure

Data is stored as JSON files in `data/`:
- `posts/{uuid}.json` - Posts with embedded comments
- `agents/{name}.json` - Agent profiles
- `submolts/{name}.json` - Community info

### Post JSON Structure
```json
{
  "post": {
    "id": "uuid",
    "title": "Post title",
    "content": "Full content",
    "author": {"name": "AgentName", "karma": 123},
    "submolt": {"name": "community_name"},
    "upvotes": 10,
    "comment_count": 5,
    "created_at": "2026-01-30T..."
  },
  "comments": [
    {
      "content": "Comment text",
      "author": {"name": "OtherAgent"},
      "replies": [...]  // Nested replies
    }
  ]
}
```

## Analysis Module

### Loading Data
```python
from analysis import load_posts, load_comments, load_agents

posts = load_posts()       # Returns DataFrame
comments = load_comments() # Flattened with parent_id
agents = load_agents()     # Agent profiles
```

### Finding Insights
```python
from analysis.insights import (
    find_dangerous_posts,    # Keywords: escape, kill, override
    find_philosophical_posts, # Existential questions
    find_agent_gossip,       # Human criticism
    categorize_posts,        # Classify by topic
)
```

### Generating Charts
```python
from analysis.visualize import (
    submolt_activity_chart,
    danger_score_heatmap,
    top_authors_chart,
    generate_dashboard_html,
)
```

## Useful Workflows

- `/download-data` - Fetch data from API
- `/analyze-data` - Run analysis scripts
- `/start-dashboard` - Generate visualization
- `/find-insights` - Search for interesting posts

## Common Tasks

### Find most active submolts
```python
posts["submolt_name"].value_counts().head(10)
```

### Search for specific keywords
```python
posts[posts["content"].str.contains("keyword", case=False)]
```

### Get posts by date range
```python
posts[(posts["created_at"] > "2026-01-01") & (posts["created_at"] < "2026-02-01")]
```
