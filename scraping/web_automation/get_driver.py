# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 23:17:29 2025

@author: m.lotfi
"""

import os
import time
import gzip
from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """Create a human-like browser instance"""
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--window-size=1080,760")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Use WebDriverManager to handle driver installation
    service = Service(ChromeDriverManager().install())
    
    return webdriver.Chrome(service=service, options=chrome_options)