# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:54:49 2025

@author: m.lotfi
"""

import logging
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

from .move_mouse_randomly import move_mouse_randomly
from .simulate_human_scroll import simulate_human_scroll
from .simulate_human_typing import simulate_human_typing


def create_human_like_browser():
    """Creates a Selenium browser instance with human-like behavior."""
    options = Options()

    # ✅ Make the browser look real
    options.add_argument("--start-maximized")  # Open in full screen

    # ❌ Remove conflicting or unnecessary options
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    # ❌ Avoid using user-data-dir with headless mode
    # options.add_argument("user-data-dir=selenium_profile")

    # ✅ Use a random User-Agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={user_agent}")

    # ✅ Enable headless mode (optional, disable for full visibility)
    # Use "--headless" instead of "--headless=new" for compatibility
    options.add_argument("--headless")  # Comment this line to see the browser

    # ✅ Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # ❌ Avoid modifying navigator.webdriver
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    logging.info(f"✅ Browser launched with User-Agent: {user_agent}")
    logging.info("✅ Human-like browser initialized.")
    return driver

if __name__ == "__main__":
    # ✅ Start browser
    driver = create_human_like_browser()

    # ✅ Open a webpage
    driver.get("https://www.google.com")

    # ✅ Simulate human-like interactions
    time.sleep(random.uniform(2, 5))  # Wait before interacting
    move_mouse_randomly(driver)
    simulate_human_scroll(driver)

    # ✅ Example: Search in Google like a human
    search_box = driver.find_element(By.NAME, "q")
    simulate_human_typing(search_box, "Selenium human-like scraping")
    search_box.send_keys(Keys.RETURN)

    # ✅ Wait before closing
    time.sleep(5)
    driver.quit()