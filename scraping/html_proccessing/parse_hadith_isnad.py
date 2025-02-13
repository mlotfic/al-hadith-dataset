# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:11:07 2025

@author: m.lotfi
"""

# hadith_parser.py

from bs4 import BeautifulSoup, NavigableString, Tag
import re
from copy import copy
from typing import Optional

from ..data_proccessing.extract_number_before_haddathana import (
    extract_number_before_haddathana,
)
from ..data_proccessing.get_h_wa_haddathana_count_occurrences import (
    get_h_wa_haddathana_count_occurrences,
)

def parse_hadith_isnad(container: BeautifulSoup, hadith_id: str, islmwy_page: str, h_wa_haddathana: int = 3) -> Tag:
    """
    Parse the Hadith Isnad (chain of narration) from a BeautifulSoup container.

    Args:
        container (BeautifulSoup): The source HTML container to parse.
        hadith_id (str): Unique identifier for the hadith.
        islmwy_page (str): Page reference for the Islamic source.
        h_wa_haddathana (int, optional): Number of narrator chains to create. 
                                         Defaults to 3.

    Returns:
        Tag: A BeautifulSoup Tag containing the structured Isnad content.

    Raises:
        ValueError: If the main content div with class 'hadith-isnad' is not found.
    """
    # Find the 'div' with class 'hadith-isnad' within the container
    h_isnad_div: Optional[Tag] = container.find('div', class_='hadith-isnad')

    # Check if the container is found; raise an exception if not
    if not h_isnad_div:
        raise ValueError(f"Could not find the main content div with class 'hadith-isnad'.")

    # Create a new BeautifulSoup object for building the structured content
    # Using 'html.parser' parser since we're constructing new HTML elements
    soup_dummy: BeautifulSoup = BeautifulSoup('', 'html.parser')

    # Create a new parent div to hold all content
    div_isnad: Tag = soup_dummy.new_tag('div', **{'class': 'hadith-isnad'})
    # Create narrator chain divs based on input parameter
    for i in range(1, h_wa_haddathana + 2):
        # Create the Isnad (chain of narration) divs
        div_isnad.append(soup_dummy.new_tag('div', **{
            'class'          : 'narrators-chain', 
            'data-id'        : f'{i}', 
            'data-hadith_id' : f'{hadith_id}',
            'data-islmwy_page': f'{islmwy_page}',
        }))
    
    # Initialize variables
    phrase: str = 'ح وَحَدَّثَنَا' # The phrase to search for in the isnad text
    idx: int    = 1
    
    # Find the first narrators chain div
    current_narrators_chain: Optional[Tag] = div_isnad.find(attrs={"data-id": f"{idx}"})
    
    # Iterate over the children of the container div
    for k, child in enumerate(h_isnad_div.children):
        if isinstance(child, NavigableString):
            # Process NavigableStrings (text nodes)
            # Strip whitespace and skip if the string is empty
            text: str = child.strip()
            
            # Replace multiple spaces, newlines, and tabs with a single space
            text_test: str = re.sub(r'[\s]+', ' ', text).strip()
            
            # Count occurrences of the specific phrase using the custom function
            h_wa_test: int = get_h_wa_haddathana_count_occurrences(text, phrase)
            
            if not text:
                continue  # Skip empty strings
                
            current_narrators_chain.append(copy(child))        
            
            if h_wa_test > 0:
                idx = idx + 1
                # Move to next chain
                current_narrators_chain = div_isnad.find(attrs={"data-id": f"{idx}"})

        elif isinstance(child, Tag):
            # Process Tag objects (HTML elements)
            current_narrators_chain.append(copy(child))   
    
    return div_isnad