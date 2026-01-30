---
description: Start the Moltbook data dashboard web server. Use to view and analyze crawled posts and comments.
---

# Start Dashboard Workflow

Launch the Flask web dashboard to visualize crawled Moltbook data.

## Steps

1. Start the dashboard server:
// turbo
```bash
python3 dashboard/app.py
```

2. Access the dashboard at: **http://127.0.0.1:5000**

## Features
- View all crawled posts with full content
- Expand posts to see comments
- Real-time statistics (total posts, comments, agents)
- Dark mode glassmorphism UI

## Notes
- The server runs in debug mode on port 5000.
- Press `Ctrl+C` to stop the server.
- Data is read from `data/moltbook.db`.
