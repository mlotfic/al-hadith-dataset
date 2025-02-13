# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:54:49 2025

@author: m.lotfi
"""

import logging
import time
from typing import Optional

import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def handle_modal_interaction(driver: webdriver.Chrome, wait_time: int = 10, retry_attempts: int = 2) -> bool:
    """
    Handle modal dialog interaction with human-like delays and proper waiting.
    
    Parameters
    ----------
    driver : webdriver.Chrome
        Selenium WebDriver instance
    wait_time : int, optional
        Maximum time to wait for element visibility/invisibility in seconds
    retry_attempts : int, optional
        Number of retry attempts for modal interactions
    
    Returns
    -------
    bool
        True if modal interaction was successful, False otherwise
    
    Notes
    -----
    This function handles the complete modal interaction cycle:
    1. Wait for modal to appear
    2. Wait for close button
    3. Click close button
    4. Wait for modal to disappear
    Each step includes human-like delays.
    """
    def wait_for_element(
        driver: webdriver.Chrome,
        by: By,
        selector: str,
        timeout: int,
        wait_type: str = 'visible'
    ) -> bool:
        """
        Wait for element with specified condition.
        
        Parameters
        ----------
        wait_type : str
            'visible' or 'invisible' to determine wait condition
        """
        try:
            condition = (
                EC.visibility_of_element_located if wait_type == 'visible'
                else EC.invisibility_of_element_located
            )
            WebDriverWait(driver, timeout).until(condition((by, selector)))
            return True
        except TimeoutException:
            logging.warning(f"Timeout waiting for element {selector} to be {wait_type}")
            return False

    def add_human_delay(action_name: str) -> None:
        """Add a random delay and log it."""
        delay = np.random.normal(2.0, 0.5)
        delay = max(1.0, min(delay, 5.0))  # Clamp between 1 and 5 seconds
        logging.info(f"Waiting {delay:.2f} seconds before {action_name}")
        time.sleep(delay)

    try:
        # Step 1: Wait for modal to appear
        logging.info("Waiting for modal dialog to appear")
        if not wait_for_element(driver, By.CLASS_NAME, "modal-dialog", wait_time, 'visible'):
            return False
        
        add_human_delay("looking for close button")
        
        # Step 2: Find and wait for close button
        logging.info("Looking for modal close button")
        close_button = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-bs-dismiss='modal'], .btn-close")
            )
        )
        
        add_human_delay("closing modal")
        
        # Step 3: Click close button
        try:
            close_button.click()
            logging.info("Clicked modal close button")
        except WebDriverException as e:
            logging.error(f"Failed to click close button: {str(e)}")
            return False
        
        # Step 4: Wait for modal to disappear
        logging.info("Waiting for modal to disappear")
        if not wait_for_element(driver, By.CLASS_NAME, "modal-dialog", wait_time, 'invisible'):
            return False
        
        add_human_delay("next action")
        
        logging.info("Modal interaction completed successfully")
        return True
        
    except Exception as e:
        logging.error(f"Error during modal interaction: {str(e)}")
        return False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Usage example
"""
def main():
    try:
        driver = webdriver.Chrome()
        
        # Handle modal interaction
        if handle_modal_interaction(driver):
            logging.info("Modal handled successfully")
        else:
            logging.error("Failed to handle modal")
            
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
"""