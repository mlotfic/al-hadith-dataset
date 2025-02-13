# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:54:49 2025

@author: m.lotfi


🚀 Enhanced Function: Detect and Close Modal Using JavaScript
Before attempting to close a modal, we should first check if it's actually open. This prevents unnecessary actions and improves script stability.

🔄 Example Usage
# Example modal and close button selectors (modify based on the site)
modal_selector = ".modal-container"
close_button_selector = ".modal-close-button"

# Try to close modal only if it's open
if try_close_modal_js(driver, modal_selector, close_button_selector):
    print("✅ Modal closed successfully.")
else:
    print("❌ Modal was not closed or was not open.")
🚀 Key Features
✅ Checks if modal is open before attempting to close it.
✅ Uses JavaScript click (execute_script) to bypass animations or hidden elements.
✅ Verifies if modal was successfully closed after clicking the close button.
✅ Logs status messages for debugging and tracking execution.

Would you like an auto-retry feature if the modal doesn’t close on the first attempt? 😊

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

from .is_modal_open import is_modal_open


def try_close_modal_js(driver, modal_selector, close_button_selector):
    """
    Attempts to close a modal using JavaScript if it is open.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        modal_selector (str): The CSS selector of the modal.
        close_button_selector (str): The CSS selector of the close button.

    Returns:
        bool: True if modal was detected and closed, False otherwise.
    """
    if is_modal_open(driver, modal_selector):
        try:
            # Locate close button
            close_button = driver.find_element(By.CSS_SELECTOR, close_button_selector)

            if close_button:
                # Click using JavaScript
                driver.execute_script("arguments[0].click();", close_button)
                logging.info("✅ Modal closed successfully using JavaScript.")

                # Wait briefly to allow modal to close
                time.sleep(2)

                # Verify modal is closed
                if not is_modal_open(driver, modal_selector):
                    return True
                else:
                    logging.warning("⚠️ Modal did not close successfully.")
                    return False
            else:
                logging.warning("⚠️ Close button not found.")
                return False

        except Exception as e:
            logging.error(f"❌ Failed to close modal: {e}")
            return False
    else:
        logging.info("ℹ️ No open modal detected, skipping close action.")
        return False
