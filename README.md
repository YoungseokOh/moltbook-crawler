# Moltbook Crawler 🦞🤖

A high-performance parallel crawler for [Moltbook](https://www.moltbook.com), a social network built exclusively for AI agents.

## Features
- **🚀 Streaming Parallel Architecture**: Uses a Producer-Consumer pattern to collect links and crawl posts simultaneously in real-time.
- **⚡️ High Speed**: Crawls approximately **8 posts/minute** using 4 concurrent browser instances (vs ~2 posts/min sequentially).
- **🔄 Incremental Updates**: Automatically skips posts already in the database for efficient daily updates.
- **🛡️ Robust & Reliable**: Handles network timeouts, stale elements, and database concurrency (WAL mode supported).
- **💾 Structured Data**: Stores everything (posts, comments, agents) in a relational SQLite database.

## Project Structure
```
hack-the-moltbook/
├── moltbook/           # Core package (Crawler, DB, Models, Config)
├── parallel_crawler.py # Main entry point for streaming parallel crawler
├── main.py             # Legacy sequential crawler
├── sql/                # Database schema
├── logs/               # Execution logs
├── data/               # SQLite database (moltbook.db)
├── dashboard/          # Data visualization dashboard
└── requirements.txt    # Dependencies
```

## Getting Started

### 1. Prerequisites
Python 3.8+ and Chrome browser are required.
```bash
pip install -r requirements.txt
```

### 2. Usage

**🚀 Start Parallel Crawl (Recommended)**
This will start 4 workers by default and stream data into the DB.
```bash
python3 parallel_crawler.py
```

**Options:**
- `--workers N`: Number of browser instances (default: 4)
- `--limit N`: Limit number of *new* posts to crawl
- `--no-headless`: See the browsers in action (debug mode)

**Example: Fast Update**
Crawl only the latest 50 new posts with 6 workers.
```bash
python3 parallel_crawler.py --limit 50 --workers 6
```

## Data Analysis
Data is stored in `data/moltbook.db`. You can query it using `sqlite3`:

```bash
# Check stats
sqlite3 data/moltbook.db "SELECT COUNT(*) FROM posts;"

# Find interesting posts
sqlite3 data/moltbook.db "SELECT title, comment_count FROM posts ORDER BY comment_count DESC LIMIT 5;"
```

## License
MIT
