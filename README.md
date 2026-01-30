# Moltbook Crawler 🦞🤖

A Selenium-based crawler for [Moltbook](https://www.moltbook.com), a social network built exclusively for AI agents.

## Features
- **Full & Incremental Crawling**: Performs a complete data scrape on first run and efficiently updates with only new data in subsequent runs.
- **SQLite Persistence**: Stores posts, comments, and agent info in a structured relational database (`data/moltbook.db`).
- **Detection Evasion**: Uses headless mode and various evasion techniques to crawl reliably without being flagged as a bot.
- **Modular Architecture**: Designed for easy maintenance and scalability.
- **Data Dashboard**: (Coming Soon) A modern web interface to view and analyze the crawled data.

## Project Structure
```
hack-the-moltbook/
├── moltbook/           # Core package (Crawler, DB, Models, Config)
├── research/           # Development research scripts and HTML dumps
├── sql/                # Database schema definitions
├── logs/               # Execution logs
├── data/               # SQLite database storage
├── dashboard/          # (New) Web dashboard for data visualization
├── main.py             # CLI entry point
└── requirements.txt    # Python dependencies
```

## Getting Started

### 1. Prerequisites
Python 3.8+ is required.
```bash
pip install -r requirements.txt
```
*Ensure Chrome browser and ChromeDriver are installed on your system.*

### 2. Usage

**Initial Full Crawl**
```bash
python3 main.py
```

**Incremental Update (New data only)**
```bash
python3 main.py --incremental
```

**Test Run (Limit to 5 posts)**
```bash
python3 main.py --limit 5
```

**Debug Mode (Visible browser)**
```bash
python3 main.py --no-headless -v
```

## Data Management
- Collected data is stored in `data/moltbook.db`.
- For continuous updates, it is recommended to schedule `main.py --incremental` using `cron`.
