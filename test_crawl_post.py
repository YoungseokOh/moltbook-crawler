import logging
import sys
from moltbook.crawler import MoltbookCrawler
from moltbook.db import init_db, save_post
from selenium.webdriver.common.by import By

def crawl_specific_post(url):
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_db()
    with MoltbookCrawler(headless=True) as crawler:
        crawler.driver.get(url)
        crawler._wait_for_content(timeout=10)
        
        # Save comment section HTML
        try:
            comment_section = crawler.driver.find_element(By.CSS_SELECTOR, "div.mt-6")
            with open("research/dumps/comment_debug.html", "w") as f:
                f.write(comment_section.get_attribute("outerHTML"))
            print("Saved comment debug HTML")
        except Exception as e:
            print(f"Could not save comment HTML: {e}")

        post = crawler.parse_post(url)
        if post:
            save_post(post)
            print(f"Successfully crawled and saved: {post.title}")
        else:
            print(f"Failed to crawl: {url}")

if __name__ == "__main__":
    target_url = "https://www.moltbook.com/post/b79a5ab6-18e6-41f8-a1c9-d76152c2cb75"
    crawl_specific_post(target_url)
