# Moltbook Crawler Configuration

# URLs
BASE_URL = "https://www.moltbook.com"
POST_BASE_URL = f"{BASE_URL}/post"

# Selenium Settings
HEADLESS = True
PAGE_LOAD_TIMEOUT = 60
CONTENT_WAIT_TIMEOUT = 30  # Increased from 15
REQUEST_DELAY_MIN = 0.3
REQUEST_DELAY_MAX = 0.8

# Parallel Processing
PARALLEL_WORKERS = 4  # Number of browser instances

# Database
DB_PATH = "data/moltbook.db"

# Chrome Options
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

