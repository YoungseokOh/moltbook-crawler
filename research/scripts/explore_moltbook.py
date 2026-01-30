import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def explore_moltbook():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Specify the chrome binary location we found earlier
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        url = "https://www.moltbook.com/"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for potential post containers to load
        # Based on the curl output, it's a Next.js app, so look for common patterns or just wait
        time.sleep(10) # Heavy wait for hydration
        
        # Take a screenshot
        screenshot_path = "/home/seok436/.gemini/antigravity/brain/9b2b578e-4870-444a-87fb-fe7ef4e961cf/moltbook_home.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        # Save HTML
        html_path = "/home/seok436/.gemini/antigravity/brain/9b2b578e-4870-444a-87fb-fe7ef4e961cf/moltbook_home.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"HTML saved to {html_path}")
        
        # Try to find elements that look like posts
        # Looking at common classes or tags
        # We can try to find articles or divs with specific roles
        articles = driver.find_elements(By.TAG_NAME, "article")
        print(f"Found {len(articles)} <article> elements")
        
        # If no articles, look for divs that might be posts
        if not articles:
            # Often posts have some common classes like 'post', 'card', etc.
            # Let's just list some element counts for analysis
            divs = driver.find_elements(By.TAG_NAME, "div")
            print(f"Found {len(divs)} <div> elements")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    explore_moltbook()
