# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 23:17:29 2025

@author: m.lotfi
"""

from typing import Dict, Union

import pandas as pd
from bs4 import BeautifulSoup


def get_toc_path(soup: BeautifulSoup, islmwy_page: str) -> pd.DataFrame:
    """
    Extract hierarchical path data from a BeautifulSoup parsed HTML page and convert it to a DataFrame.
    
    This function processes HTML content to extract various levels of navigation hierarchy
    including book names, chapters, sections, and subsections along with their corresponding URLs.
    
    Parameters
    ----------
    soup : BeautifulSoup
        Parsed HTML content containing the navigation hierarchy
    islmwy_page : str
        Identifier or URL of the Islamic way page being processed
    
    Returns
    -------
    pd.DataFrame
        A single-row DataFrame containing the following columns:
        - islmwy_page                : Page identifier
        - anchor_main_data_href      : Main anchor URL
        - anchor_main_data_text      : Main anchor text
        - book_name_url              : Book URL
        - book_name                  : Book name
        - hadith_book_name_url       : Hadith book URL
        - hadith_book_name           : Hadith book name
        - hadith_chapter_url         : Chapter URL
        - hadith_chapter             : Chapter name
        - hadith_section_url         : Section URL
        - hadith_section             : Section name
        - hadith_sub_section_url     : Subsection URL
        - hadith_sub_section         : Subsection name
        - hadith_part_I_url : Sub-subsection URL
        - hadith_part_I     : Sub-subsection name
    
    Examples
    --------
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> result_df = get_toc_path(soup, '123')
    """
    # Initialize path data dictionary with default values
    path_data: Dict[str, str] = {
        "islmwy_page"                   : islmwy_page,
        'anchor_main_data_href'         : "",
        'anchor_main_data_text'         : "",
        'book_url'                      : "",
        'book'                          : "",
        'hadith_book_name_url'          : "",
        'hadith_book_name'              : "",
        'hadith_chapter_url'            : "",
        'hadith_chapter'                : "",
        'hadith_section_url'            : "",
        'hadith_section'                : "",
        'hadith_sub_section_url'        : "",
        'hadith_sub_section'            : "",
        'hadith_part_I_url'    : "",
        'hadith_part_I'        : ""
    }
    
    # Define mapping between index and data keys
    key_mapping = {
        0: ('anchor_main_data_href', 'anchor_main_data_text'),
        1: ('book_url', 'book'),
        2: ('hadith_book_name_url', 'hadith_book_name'),
        3: ('hadith_section_url', 'hadith_section'),
        4: ('hadith_sub_section_url', 'hadith_sub_section'),
        5: ('hadith_part_I_url', 'hadith_part_I'),
        6: ('hadith_chapter_url', 'hadith_chapter')
    }
    
    # Find the main ordered list containing the path
    ol_main = soup.find('ol', id="topPath")
    if ol_main:
        for index, li_main in enumerate(ol_main.find_all('li')):
            if (len((ol_main.find_all('li'))) == (index+1)):
                index = 6
            if index not in key_mapping:
                continue
                
            anchor_main = li_main.find('a')
            href_key, text_key = key_mapping[index]
            
            if anchor_main:
                # Extract href and text from anchor tag
                path_data[href_key] = anchor_main.get('href', "")
                path_data[text_key] = anchor_main.text.strip()
            else:
                # Extract text directly from list item if no anchor present
                path_data[text_key] = li_main.text.strip()
    
    return pd.DataFrame([path_data])