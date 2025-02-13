# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:54:49 2025

@author: m.lotfi
"""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

def try_open_modal(driver: webdriver.Chrome, element_class: str, wait_time: int = 10, retry_attempts: int = 2) -> bool:
    """
    Open a modal, simulate human-like interaction, and close it.
    
    Parameters
    ----------
    driver : webdriver.Chrome
        Selenium WebDriver instance
    element_class : str
        CSS class name of the element to click
    wait_time : int, optional
        Maximum time to wait for element visibility in seconds (default: 10)
    retry_attempts : int, optional
        Number of retry attempts if interaction fails (default: 2)
    
    Returns
    -------
    bool
        True if modal interaction was successful, False otherwise
    
    Notes
    -----
    This function includes human-like delays and proper error handling
    for modal interactions.
    """
    def wait_for_element(driver: webdriver.Chrome, class_name: str, timeout: int) -> Optional[webdriver.remote.webelement.WebElement]:
        """Wait for element to be visible and return it."""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )
        except TimeoutException:
            return None

    def attempt_click(element: webdriver.remote.webelement.WebElement) -> bool:
        """Attempt to click element with error handling."""
        try:
            element.click()
            return True
        except WebDriverException as e:
            logging.warning(f"Click failed: {str(e)}")
            return False

    logging.info(f"Attempting to open modal with class: {element_class}")
    
    for attempt in range(retry_attempts):
        try:
            # Wait for element to be visible
            element = wait_for_element(driver, element_class, wait_time)
            
            if not element:
                logging.warning(
                    f"Element with class '{element_class}' not found "
                    f"(Attempt {attempt + 1}/{retry_attempts})"
                )
                continue
            
            # Ensure element is in viewport
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            
            # Add small delay for scroll completion
            driver.implicitly_wait(0.5)
            
            # Attempt to click
            if attempt_click(element):
                logging.info("Modal opened successfully")
                return True
            
            logging.warning(
                f"Click attempt {attempt + 1}/{retry_attempts} failed, retrying..."
            )
            
        except WebDriverException as e:
            logging.error(f"Unexpected WebDriver error: {str(e)}")
            if attempt == retry_attempts - 1:
                break
    
    logging.error(f"Failed to open modal after {retry_attempts} attempts")
    return False

# Usage example

def main():
    try:
        driver = webdriver.Chrome()
        
        # Basic usage
        success = try_open_modal(driver, "modal-trigger")
        
        # Advanced usage with custom parameters
        success = try_open_modal(
            driver=driver,
            element_class="custom-modal",
            wait_time=15,
            retry_attempts=3
        )
        
        if not success:
            logging.error("Modal interaction failed")
            # Handle failure case
            
    except Exception as e:
        logging.error(f"Error in modal interaction: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()