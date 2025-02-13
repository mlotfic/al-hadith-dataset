# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 23:17:29 2025

@author: m.lotfi
"""

from typing import Dict, List, Union

import pandas as pd
from bs4 import BeautifulSoup, Tag


def get_page_volume(soup: BeautifulSoup, islmwy_page: str) -> pd.DataFrame:
    """
    Extract part dropdown menu data from a BeautifulSoup parsed HTML page.
    
    This function processes HTML content to extract information about the current part
    and available parts in the dropdown menu of an Islamic text.
    
    Parameters
    ----------
    soup : BeautifulSoup
        Parsed HTML content containing the part dropdown menu
    islmwy_page : str
        Identifier or URL of the Islamic way page being processed
    
    Returns
    -------
    pd.DataFrame
        A single-row DataFrame containing:
        - islmwy_page: Page identifier
        - book_page_volume: Currently selected part text
        - page_volumes: List of all available parts in the dropdown
    
    Examples
    --------
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> result_df = get_page_volume(soup, 'page_123')
    >>> print(result_df['book_page_volume'].iloc[0])
    'Part 1'
    """
    def extract_dropdown_items(dropdown_menu: Tag) -> List[str]:
        """
        Extract all dropdown item texts from the dropdown menu.
        
        Parameters
        ----------
        dropdown_menu : Tag
            BeautifulSoup Tag object containing the dropdown menu items
            
        Returns
        -------
        List[str]
            List of text content from dropdown items
        """
        return [
            anchor.text.strip()
            for li in dropdown_menu.find_all('li')
            if (anchor := li.find('a', class_="dropdown-item"))
        ]

    # Initialize data structure
    page_volume_data: Dict[str, Union[str, List[str]]] = {
        "islmwy_page": islmwy_page,
        'book_page_volume': "",
        'page_volumes': []
    }
    
    # Find the main part dropdown span
    part_span = soup.find('span', class_='part partdropmenu')
    
    if part_span:
        # Extract current part from dropdown toggle
        if dropdown_toggle := part_span.find('a', class_='dropdown-toggle'):
            page_volume_data['book_page_volume'] = dropdown_toggle.text.strip()
        
        # Extract dropdown menu items
        if dropdown_menu := part_span.find('ul', class_='dropdown-menu'):
            page_volume_data['page_volumes'] = extract_dropdown_items(dropdown_menu)
    
    return pd.DataFrame([page_volume_data])