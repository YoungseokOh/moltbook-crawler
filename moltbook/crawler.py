"""Selenium-based crawler for Moltbook."""
import time
import random
import re
import logging
from typing import List, Optional, Generator, Set
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from . import config
from .models import Post, Comment

logger = logging.getLogger(__name__)


class MoltbookCrawler:
    """Crawls posts and comments from Moltbook."""
    
    def __init__(self, headless: bool = True):
        self.driver = None
        self.headless = headless
    
    def _init_driver(self):
        """Initialize the Selenium WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"user-agent={config.USER_AGENT}")
        chrome_options.binary_location = "/usr/bin/google-chrome-stable"
        
        # Bypass automation detection
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
        
        # Additional evasion
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
    
    def _random_delay(self):
        """Wait a random amount of time between requests."""
        delay = random.uniform(config.REQUEST_DELAY_MIN, config.REQUEST_DELAY_MAX)
        time.sleep(delay)
    
    def _wait_for_content(self, timeout: int = None) -> bool:
        """Wait for dynamic content to load."""
        timeout = timeout or config.CONTENT_WAIT_TIMEOUT
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Look for actual content (non-loading state)
            loading_divs = self.driver.find_elements(By.CSS_SELECTOR, ".animate-pulse")
            content_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.bg-\\[\\#1a1a1b\\]")
            
            if len(content_divs) > 3 and len(loading_divs) == 0:
                return True
            
            time.sleep(2)
        
        return False

    def _extract_post_id(self, url: str) -> str:
        """Extract post ID from a URL."""
        return url.split("/post/")[-1].split("?")[0]
    
    def _collect_visible_hrefs(self) -> List[str]:
        """Collect all post hrefs currently visible on page as strings."""
        hrefs = []
        try:
            links = self.driver.find_elements(By.CSS_SELECTOR, "a[href^='/post/']")
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if href:
                        hrefs.append(href)
                except Exception:
                    continue
        except Exception:
            pass
        return hrefs
    
    def stream_post_links(
        self, 
        known_ids: Optional[Set[str]] = None,
        max_posts: Optional[int] = None,
        batch_size: int = 10
    ) -> Generator[List[str], None, None]:
        """
        Stream post links from the main feed as they're discovered.
        
        Yields batches of NEW post URLs (not in known_ids) immediately as found,
        rather than waiting to collect all links first.
        
        Args:
            known_ids: Set of post IDs already in DB (will be skipped)
            max_posts: Maximum number of NEW posts to yield (None = unlimited)
            batch_size: Number of new links to collect before yielding a batch
        
        Yields:
            List of post URLs (batch_size new links at a time)
        """
        if known_ids is None:
            known_ids = set()
        
        logger.info("Loading main feed (streaming mode)...")
        self.driver.get(config.BASE_URL)
        self._wait_for_content()
        
        seen_urls = set()  # All URLs seen in this session
        total_new_yielded = 0
        pending_batch = []
        scroll_attempts = 0
        max_scroll_attempts = 10  # Stop after 10 consecutive no-new-content scrolls
        last_scroll_position = 0
        
        while scroll_attempts < max_scroll_attempts:
            # Collect all hrefs as strings (avoids stale element issues)
            current_hrefs = self._collect_visible_hrefs()
            
            for href in current_hrefs:
                if href in seen_urls:
                    continue
                    
                seen_urls.add(href)
                post_id = self._extract_post_id(href)
                
                # Skip if already in DB
                if post_id in known_ids:
                    logger.debug(f"Skipping known post: {post_id}")
                    continue
                
                pending_batch.append(href)
                
                # Yield batch when full
                if len(pending_batch) >= batch_size:
                    logger.info(f"Yielding batch of {len(pending_batch)} new posts (total discovered: {len(seen_urls)}, DB: {len(known_ids)})")
                    yield pending_batch
                    total_new_yielded += len(pending_batch)
                    pending_batch = []
                    
                    # Check max_posts limit
                    if max_posts and total_new_yielded >= max_posts:
                        logger.info(f"Reached max_posts limit ({max_posts})")
                        return
                    
                    # Reload feed page and restore scroll position after batch processing
                    logger.debug("Reloading feed after batch...")
                    self.driver.get(config.BASE_URL)
                    self._wait_for_content()
                    # Scroll back to approximate position
                    self.driver.execute_script(f"window.scrollTo(0, {last_scroll_position});")
                    time.sleep(1)
            
            # Scroll down to load more
            last_scroll_position = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_scroll_position:
                # Try clicking "Load More" button if exists
                try:
                    load_more = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Load') or contains(text(), 'More')]")
                    load_more.click()
                    time.sleep(2)
                    scroll_attempts = 0  # Reset on successful load more
                except NoSuchElementException:
                    scroll_attempts += 1
                    logger.debug(f"No new content, scroll attempt {scroll_attempts}/{max_scroll_attempts}")
            else:
                scroll_attempts = 0  # Reset if we got new content
            
            last_scroll_position = new_height
        
        # Yield remaining posts in the final partial batch
        if pending_batch:
            logger.info(f"Yielding final batch of {len(pending_batch)} new posts")
            yield pending_batch
        
        logger.info(f"Feed scrolling complete. Total discovered: {len(seen_urls)}, New posts yielded: {total_new_yielded + len(pending_batch)}")
    
    def parse_post(self, url: str) -> Optional[Post]:
        """Navigate to a post and extract its data."""
        try:
            self.driver.get(url)
            self._wait_for_content(timeout=20)
            self._random_delay()
            
            # Extract post ID from URL
            post_id = url.split("/post/")[-1].split("?")[0]
            
            # Title
            try:
                title_elem = self.driver.find_element(By.CSS_SELECTOR, "h1")
                title = title_elem.text.strip()
            except NoSuchElementException:
                title = ""
            
            # Content - get ALL paragraphs in the prose section
            try:
                content_elems = self.driver.find_elements(By.CSS_SELECTOR, ".prose p")
                content = "\n\n".join([p.text.strip() for p in content_elems if p.text.strip()])
            except NoSuchElementException:
                content = ""
            
            # Author
            try:
                author_elem = self.driver.find_element(By.CSS_SELECTOR, "a[href^='/u/']")
                author_name = author_elem.text.replace("u/", "").strip()
            except NoSuchElementException:
                author_name = "unknown"
            
            # Submolt
            try:
                submolt_elem = self.driver.find_element(By.CSS_SELECTOR, "a[href^='/m/']")
                submolt = submolt_elem.text.replace("m/", "").strip()
            except NoSuchElementException:
                submolt = "general"
            
            # Upvotes
            try:
                upvote_elem = self.driver.find_element(By.CSS_SELECTOR, "div.w-12 span.text-white")
                upvotes = int(upvote_elem.text.strip())
            except (NoSuchElementException, ValueError):
                upvotes = 0
            
            # Comment count
            try:
                comment_text = self.driver.find_element(By.XPATH, "//*[contains(text(), 'comment')]").text
                match = re.search(r'(\d+)\s*comment', comment_text)
                comment_count = int(match.group(1)) if match else 0
            except (NoSuchElementException, ValueError):
                comment_count = 0
            
            # Parse comments (if any)
            comments = self._parse_comments(post_id)
            
            post = Post(
                id=post_id,
                title=title,
                content=content,
                submolt=submolt,
                author_name=author_name,
                upvotes=upvotes,
                comment_count=comment_count,
                comments=comments
            )
            
            logger.info(f"Parsed post: {title[:50]}...")
            return post
            
        except Exception as e:
            logger.error(f"Error parsing post {url}: {e}")
            return None
    
    def _parse_comments(self, post_id: str) -> List[Comment]:
        """Parse comments from the current post page."""
        comments = []
        try:
            # Comments are typically in a section after the main post
            # Each comment is wrapped in a py-2 div inside the comment section
            comment_elems = self.driver.find_elements(By.CSS_SELECTOR, "div.mt-6 div.py-2")
            
            for i, elem in enumerate(comment_elems):
                try:
                    content_elems = elem.find_elements(By.CSS_SELECTOR, "p")
                    content = "\n\n".join([p.text.strip() for p in content_elems if p.text.strip()])
                    
                    if not content: # Fallback if p tags aren't found or empty
                         content = elem.text.strip()

                    author_link = elem.find_element(By.CSS_SELECTOR, "a[href^='/u/']")
                    author_name = author_link.text.replace("u/", "").strip()
                    
                    comment = Comment(
                        id=f"{post_id}_comment_{i}",
                        post_id=post_id,
                        content=content,
                        author_name=author_name
                    )
                    comments.append(comment)
                except NoSuchElementException:
                    continue
                    
        except Exception as e:
            logger.debug(f"Error parsing comments: {e}")
        
        return comments
    
    def start(self):
        """Start the crawler (initialize driver)."""
        logger.info("Starting crawler...")
        self._init_driver()
    
    def stop(self):
        """Stop the crawler (quit driver)."""
        if self.driver:
            self.driver.quit()
            self.driver = None
        logger.info("Crawler stopped.")
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
