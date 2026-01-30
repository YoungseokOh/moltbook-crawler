import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def explore_moltbook():
    print("Starting Selenium exploration...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"

    print("Installing/Setting up ChromeDriver...")
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
    except Exception as e:
        print(f"Failed to initialize Chrome: {e}")
        return

    try:
        url = "https://www.moltbook.com/"
        print(f"Navigating to {url}...")
        try:
            driver.get(url)
        except TimeoutException:
            print("Page load timed out, but proceeding to check content anyway...")
        
        print("Waiting 10 seconds for hydration...")
        time.sleep(10)
        
        # Check current URL
        print(f"Current URL: {driver.current_url}")
        
        # Take a screenshot
        screenshot_path = "/home/seok436/.gemini/antigravity/brain/9b2b578e-4870-444a-87fb-fe7ef4e961cf/moltbook_home_robust.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        # Save HTML
        html_path = "/home/seok436/.gemini/antigravity/brain/9b2b578e-4870-444a-87fb-fe7ef4e961cf/moltbook_home_robust.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"HTML saved to {html_path}")
        
        # Summary of page
        title = driver.title
        print(f"Page Title: {title}")
        
        articles = driver.find_elements(By.TAG_NAME, "article")
        print(f"Found {len(articles)} <article> elements")
        
        # If no articles, let's look for link elements that might lead to posts
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Found {len(links)} links")
        
    except Exception as e:
        print(f"An error occurred during exploration: {e}")
    finally:
        print("Quitting driver.")
        driver.quit()

if __name__ == "__main__":
    explore_moltbook()
