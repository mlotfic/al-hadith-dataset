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


def is_modal_open(driver, modal_selector):
    """
    Checks if the modal is currently open by verifying its visibility.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        modal_selector (str): The CSS selector for the modal.

    Returns:
        bool: True if modal is open, False otherwise.
    """
    try:
        modal = driver.find_element(By.CSS_SELECTOR, modal_selector)
        if modal.is_displayed():
            logging.info("✅ Modal is open.")
            return True
        else:
            logging.info("⚠️ Modal is not visible.")
            return False
    except Exception:
        logging.info("⚠️ Modal not found.")
        return False