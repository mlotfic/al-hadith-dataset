# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 23:17:29 2025

@author: m.lotfi
"""

from typing import Dict, Optional, Union

import pandas as pd
from bs4 import BeautifulSoup, Tag


def get_page_navigation(soup: BeautifulSoup, islmwy_page: Optional[str] = None) -> pd.DataFrame:
    """
    Extract page navigation data from a BeautifulSoup parsed HTML page.
    
    This function processes HTML content to extract navigation information including
    previous page link, current page number, and next page link.
    
    Parameters
    ----------
    soup : BeautifulSoup
        Parsed HTML content containing the page navigation elements
    islmwy_page : str, optional
        Identifier or URL of the Islamic way page being processed
    
    Returns
    -------
    pd.DataFrame
        A single-row DataFrame containing:
        - islmwy_page: Page identifier
        - prev_page: URL of the previous page or ""
        - book_page_number: Current page number
        - next_page: URL of the next page or ""
    
    Examples
    --------
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> result_df = get_page_navigation(soup, 'page_123')
    >>> print(result_df['book_page_number'].iloc[0])
    '5'
    """
    # Initialize navigation data structure
    page_nav_data: Dict[str, str] = {
        "islmwy_page"     : islmwy_page,
        'prev_page'       : "",
        'book_page_number': "",
        'next_page'       : ""
    }
    try:
        # Find the main page navigation span
        page_span = soup.find('span', class_='page')
        
        if page_span:
            # Previous page button
            prev_button = page_span.find('a', class_='topprevbutton')        
            page_nav_data['prev_page'] = prev_button.get('href', "") if prev_button else ""

            # Current page dropdown
            # Manual text search
            for span in page_span.find_all('span'):
                if 'صفحة' in span.get_text():
                    dropdown_toggle = span.find('a', class_='dropdown-toggle')            
                    # Current page number
                    page_nav_data['book_page_number'] = dropdown_toggle.text.strip() if dropdown_toggle else ""
                    break
            
            # Next page button
            next_button = page_span.find('a', class_='topnextbutton')
            page_nav_data['next_page'] = next_button.get('href', "") if next_button else ""
    
    except Exception as e:
        # Log the error with more context
        logging.error(f"Error extracting page navigation data: {str(e)}")
        # Optionally: raise custom exception or handle error differently
    
    return pd.DataFrame([page_nav_data])