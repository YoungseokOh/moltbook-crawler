import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def explore_post(post_url):
    print(f"Starting Selenium exploration for post: {post_url}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Failed to initialize Chrome: {e}")
        return

    try:
        print(f"Navigating to {post_url}...")
        driver.get(post_url)
        
        timeout = 30
        start_time = time.time()
        found_content = False
        
        while time.time() - start_time < timeout:
            # Look for indicators of post content
            # The homepage used <h3> for title and <p> for body
            # Let's look for h1 or large h2 which is common for post pages
            h1s = driver.find_elements(By.TAG_NAME, "h1")
            content_ps = driver.find_elements(By.TAG_NAME, "p")
            
            if h1s and len(content_ps) > 5:
                print(f"Content found! Title: {h1s[0].text}")
                found_content = True
                break
            
            print(f"Waiting for content... ({int(time.time() - start_time)}s)")
            time.sleep(3)
            
        # Save HTML
        html_path = "/home/seok436/.gemini/antigravity/brain/9b2b578e-4870-444a-87fb-fe7ef4e961cf/moltbook_post_wait.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"HTML saved to {html_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    explore_post("https://www.moltbook.com/post/87299292-4fd5-4b0a-83d1-4d1c042c4979")
