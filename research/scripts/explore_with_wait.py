import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def explore_with_wait():
    print("Starting Selenium exploration with wait loop...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # Custom UA and automation bypass
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "const newProto = navigator.__proto__; delete newProto.webdriver; navigator.__proto__ = newProto;"
        })
    except Exception as e:
        print(f"Failed to initialize Chrome: {e}")
        return

    try:
        url = "https://www.moltbook.com/"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        timeout = 60 # 1 minute timeout
        start_time = time.time()
        found_posts = False
        
        while time.time() - start_time < timeout:
            # Look for indicators of posts
            # Looking for text that isn't "0" in the stats
            stats = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-2xl font-bold')]")
            stat_texts = [s.text for s in stats if s.text != "0" and s.text != ""]
            
            # Also look for actual post titles or content
            # Based on the dump, posts are likely in divs within a main section
            # Let's check for any div that doesn't have 'animate-pulse'
            content_divs = driver.find_elements(By.XPATH, "//div[not(contains(@class, 'animate-pulse')) and contains(@class, 'p-4')]")
            
            if stat_texts or len(content_divs) > 10: # >10 because there are many p-4 divs in the layout
                print(f"Potential content found! Stats: {stat_texts}")
                found_posts = True
                break
            
            print(f"Waiting for content... ({int(time.time() - start_time)}s)")
            time.sleep(5)
            
        if not found_posts:
            print("Timed out waiting for posts.")
            
        # Take a screenshot
        screenshot_path = "/home/seok436/.gemini/antigravity/brain/9b2b578e-4870-444a-87fb-fe7ef4e961cf/moltbook_home_wait.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        # Save HTML
        html_path = "/home/seok436/.gemini/antigravity/brain/9b2b578e-4870-444a-87fb-fe7ef4e961cf/moltbook_home_wait.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"HTML saved to {html_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    explore_with_wait()
