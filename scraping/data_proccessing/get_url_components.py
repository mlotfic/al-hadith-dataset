# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:59:07 2025

@author: m.lotfi
"""

import re
from typing import Optional, Dict

def get_url_components(url: str) -> Optional[Dict[str, str]]:
    """
    Parse an Islamweb library URL and extract its components.

    This function takes a URL from the Islamweb library and extracts the `book_id`,
    `islmwy_page`, and `chapter_name` using a regular expression.

    Args:
        url (str): The URL to parse.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the extracted components if the URL
        matches the expected pattern, otherwise `None`.
    """
    # Regular expression pattern to match and extract components from the URL
    pattern = (
        r'.*/content/'
        r'(?P<book_id>\d+)/'
        r'(?P<islmwy_page>\d+)/'
        r'(?P<chapter_name>.+)?'
    )

    # Attempt to match the URL with the pattern
    match = re.match(pattern, url)
    if match.group('book_id'):
        # Extracted components from the URL
        book_id      = match.group('book_id')
    else: 
        book_id = ""
        
    if match.group('islmwy_page'):
        # Extracted components from the URL
        islmwy_page      = match.group('islmwy_page')
    else: 
        islmwy_page = ""
    
    if match.group('chapter_name'):
        # Extracted components from the URL
        chapter_name      = match.group('chapter_name')
    else: 
        chapter_name = ""
                    
    components: Dict[str, str] = {
            "book_id"      : book_id,
            "islmwy_page"  : islmwy_page,
            "chapter_name" : chapter_name
        }
    # Return the dictionary of extracted components
    return components 