# Moltbook Crawler Configuration

# URLs
BASE_URL = "https://www.moltbook.com"
POST_BASE_URL = f"{BASE_URL}/post"

# Selenium Settings
HEADLESS = True
PAGE_LOAD_TIMEOUT = 30
CONTENT_WAIT_TIMEOUT = 60
REQUEST_DELAY_MIN = 1.0  # seconds
REQUEST_DELAY_MAX = 3.0  # seconds

# Database
DB_PATH = "data/moltbook.db"

# Chrome Options
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
