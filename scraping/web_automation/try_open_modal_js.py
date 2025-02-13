# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:54:49 2025

@author: m.lotfi
"""
def try_open_modal_js(driver, element):
    """Opens a modal using JavaScript click."""
    try:
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        logging.error(f"Failed to open modal: {e}")
        return False