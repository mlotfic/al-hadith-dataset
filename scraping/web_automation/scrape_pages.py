
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 11:16:30 2025

@author: m.lotfi
"""


import logging
import time
logging.basicConfig(level=logging.INFO)
from selenium.webdriver.common.by import By

# - base_url (str): Base URL for the website being scraped.

## **✅ Setting up project urls**
base_url = 'https://www.islamweb.net'
base_api = base_url + "/ar/library/maktaba/"
book_url = base_url + "/ar/library/content/"

## **✅ Define the lambda function to get full path**
get_chapter_url       = lambda book_id, islmwy_page : book_url + f"{book_id}/{islmwy_page}/"
get_prev_page_url     = lambda x                    : get_chapter_url(book_id, islmwy_page)  if x == 'N/A' else base_url + x
get_next_page_url     = lambda x                    : get_chapter_url(book_id, islmwy_page)  if x == 'N/A' else base_url + x

from ..handles_files import is_files_saved
from ..handles_files import save_html_files
from ..time_date import generate_random_delay_gauss
from .try_open_modal_js import try_open_modal_js
from .try_close_modal_js import try_close_modal_js
from ..data_proccessing import clean_html
from ..data_proccessing import clean_text


def scrape_pages(start, end, base_folder, base_filename, next_page, book_id, modal_classes, driver):
    """
    Scrape pages in the given range, handle modals, extract content, and save data.

    Parameters:
    - start (int): Starting page number.
    - end (int): Ending page number.
    - base_folder (str): Path to the folder where files will be saved.
    - base_filename (str): Base filename for saving files.
    - next_page (str): URL of the next page, if applicable.
    
    - book_id (int): Identifier for the book being scraped.
    - modal_classes (list): List of modal class names to process.
    - driver (webdriver): Selenium WebDriver instance.
    """
    
    for islmwy_page in range(start, end + 1):

        # ✅ Check if page is already saved
        if not is_files_saved(base_folder, base_filename, islmwy_page):
            if next_page:
                url = next_page
            else:
                url = get_chapter_url(book_id, islmwy_page)

            ##################################################################
            print(f"# ✅ Scraping {url} ----------------------------------- ")
            # ✅ Open target website
            driver.get(url)

            # List to store extracted modal content
            extracted_texts = []   # Store extracted text
            extracted_html = []    # Store raw modal HTML

            # ✅ Loop through modal classes
            for modal_class in modal_classes:
                try:
                    elements = driver.find_elements(By.CLASS_NAME, modal_class)

                    for element in elements:
                        # Check if modal is visible (i.e., not display: none)
                        style_attr = element.get_attribute("style") or ""
                        if "display:none" not in style_attr.replace(" ", "").lower():
                            logging.info(f"🔍 Opening modal: {modal_class}")

                            if try_open_modal_js(driver, element):
                                time.sleep(2)  # Small delay to allow content to load

                                # ✅ Capture raw modal HTML
                                modal_content_element = driver.find_element(By.CLASS_NAME, "modal-content")
                                modal_content = modal_content_element.get_attribute("innerHTML")
                                extracted_html.append(f"Modal ({modal_class}):\n{modal_content}\n\n")

                                # ✅ Extract clean text
                                text_content = clean_html(modal_content)
                                extracted_texts.append(f"Modal ({modal_class}):\n{text_content}\n\n")

                                # ✅ Close modal
                                close_button_selector = ".modal-close-button"  # Adjust as needed
                                try_close_modal_js(driver, modal_class, close_button_selector)

                except Exception as e:
                    logging.error(f"Error processing modal {modal_class}: {e}")

            # ✅ Saving files
            print(f"✅ ========= Saving Data - {islmwy_page} ========= ")

            # Get the raw HTML
            raw_html = driver.page_source

            # ✅ Save files
            save_html_files(base_folder, base_filename, islmwy_page, extracted_html, extracted_texts, raw_html)

            # ✅ Simulate human delay
            generate_random_delay_gauss()  # Uncomment if you have this function implemented