# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:11:07 2025

@author: m.lotfi
"""

# hadith_parser.py

import re
from copy import copy

from bs4 import BeautifulSoup, NavigableString, Tag

from ..data_proccessing.extract_number_before_haddathana      import extract_number_before_haddathana
from ..data_proccessing.get_h_wa_haddathana_count_occurrences import get_h_wa_haddathana_count_occurrences
from ..data_proccessing.clean_text import clean_text

from .parse_hadith_isnad import parse_hadith_isnad


def parse_hadith_page(soup, id='pagebody', islmwy_page = '', is_thaskeel = False):
    """
    Parses a Hadith page's HTML content and structures it into introduction, isnad, and matn sections.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object of the parsed HTML content.
    - id (str): The id attribute of the main content div (default is 'pagebody').

    Returns:
    - tuple: A tuple containing:
        - hadith_id (int or str): The extracted Hadith identifier.
        - h_wa_haddathana (int): The count of specific phrases in the isnad.
        - page_container (Tag): A BeautifulSoup Tag object containing the structured Hadith content.
        - container_remaining (Tag): A BeautifulSoup Tag object containing any remaining content.

    The returned structure is as follows:
    ```html
    <div>
        <div class="page-intro">
            <!-- Introduction content before the Hadith starts -->
        </div>
        <div class="page-hadith">
            <div class="hadith-isnad">
                <!-- Chain of narration (isnad) content -->
            </div>
            <div class="hadith-matn">
                <!-- Main text (matn) of the Hadith -->
            </div>
        </div>
    </div>
    ```

    Notes:
    - This function relies on external functions:
        - `extract_number_before_haddathana(text)`: Extracts the number before the word 'haddathana' in the provided text or returns 'N/A' if not found.
        - `get_h_wa_haddathana_count_occurrences(text, phrase)`: Counts occurrences of a specific phrase in the text.
    - Make sure these functions are defined and accessible in your codebase.

    Exceptions:
    - Raises `ValueError` if the main content div with class 'bookcontent-dic' and specified id is not found.
    """

    # Find the main content div with class 'bookcontent-dic' and specified id
    container = soup.find('div', class_='bookcontent-dic', id=id)

    # Check if the container is found; raise an exception if not
    if not container:
        raise ValueError(f"Could not find the main content div with class 'bookcontent-dic' and id '{id}'.")

    # Create a new BeautifulSoup object for building the structured content
    # Using 'html.parser' parser since we're constructing new HTML elements
    soup_dummy = BeautifulSoup('', 'html.parser')

    # Create a new parent div to hold all content
    page_container = soup_dummy.new_tag('div')

    # Create the introduction div and append it to the page container
    div_intro = soup_dummy.new_tag('div', **{'class': 'page-intro'})
    page_container.append(div_intro)

    # Create the Hadith content div and append it to the page container
    div_hadith = soup_dummy.new_tag('div', **{'class': 'page-hadith'})
    page_container.append(div_hadith)

    # Create the Isnad (chain of narration) and Matn (main text) divs
    div_isnad = soup_dummy.new_tag('div', **{'class': 'hadith-isnad'})
    div_hadith.append(div_isnad)

    div_matn = soup_dummy.new_tag('div', **{'class': 'hadith-matn'})
    div_hadith.append(div_matn)

    # Initialize variables
    h_wa_haddathana = 0   # Counter for specific phrase occurrences
    hadith_id = 0         # Initialize the Hadith ID

    # Create another BeautifulSoup object for remaining content after the Hadith
    soup_dummy1 = BeautifulSoup('', 'html.parser')

    # Create a container for any remaining content after parsing the Hadith
    container_remaining = soup_dummy1.new_tag('div')

    # Initialize a counter to keep track of Hadith sections
    hadith_number = 0

    # Iterate over the children of the container div
    for k, child in enumerate(container.children):
        if isinstance(child, NavigableString):
            # Process NavigableStrings (text nodes)
            # Strip whitespace and skip if the string is empty
            text = child.strip()
            if not text:
                continue  # Skip empty strings

            # Use the custom function to extract numbers before 'haddathana'
            haddathana = extract_number_before_haddathana(text)
            # print(haddathana)

            if haddathana != 'N/A':
                # Found 'haddathana'; increment the Hadith counter
                hadith_number += 1
                # Append a copy of the NavigableString to the isnad div
                div_isnad.append(copy(child))
                # Store the Hadith ID
                hadith_id = haddathana

            elif hadith_number == 0:
                # Before the Hadith starts; append to the introduction div
                div_intro.append(copy(child))

            elif hadith_number == 1:
                # Part of the isnad; append to the isnad div
                div_isnad.append(copy(child))

        elif isinstance(child, Tag):
            # Process Tag objects (HTML elements)
            if hadith_number == 0:
                # Before the Hadith starts; append to the introduction div
                div_intro.append(copy(child))

            elif hadith_number == 1:
                # Get the class attribute safely (returns an empty list if not present)
                classes = child.get("class", [])
                if classes and 'hadith' in classes:
                    # Found the matn (main text) of the Hadith; append to the matn div
                    div_matn.append(copy(child))
                else:
                    # Part of the isnad; append to the isnad div
                    div_isnad.append(copy(child))

            elif hadith_number >= 2:
                # Additional content after the Hadith; append to the remaining container
                container_remaining.append(copy(child))

    # The phrase to search for in the isnad text
    phrase = 'ح وَحَدَّثَنَا'

    # Get the text content of the isnad div for processing
    text = div_isnad.get_text()
    # Check if there is text to process
    if text:
        # Remove URL fragments or unwanted patterns from the text
        text = re.sub(r'nindex\.php\?page=tafseer&surano=[\d]*&ayano=[\d]*', '', text)
        text = re.sub(r'nindex\.php\?page=showalam&ids=[\d]*', '', text)
        text = re.sub(r'nindex\.php\?page=hadith&LINKID=[\d]*', '', text)
        text = re.sub(r'nindex\.php\?page=treesubj&link=([\d]|[0-9_]+)*', '', text)
        # Replace multiple spaces, newlines, and tabs with a single space
        text = re.sub(r'[\s]+', ' ', text).strip()

        # Count occurrences of the specific phrase using the custom function
        h_wa_haddathana = get_h_wa_haddathana_count_occurrences(text, phrase)

    # Check if container_remaining is empty
    if not container_remaining.contents:
        # If empty, set container_remaining to None
        container_remaining = None
    
    if page_container:        
        # Refactorin Isnad html
        temp_hadith_isnad = parse_hadith_isnad(page_container, hadith_id, islmwy_page, h_wa_haddathana)
        
        # Refactoring page_container html
        if temp_hadith_isnad:            
            # Create a new BeautifulSoup object for building the structured content
            # Using 'html.parser' parser since we're constructing new HTML elements
            soup_dummy = BeautifulSoup('', 'html.parser')

            # Create a new parent div to hold all content
            page_container_1 = soup_dummy.new_tag('div', **{
                'class'               : 'hadith-page',
                'data-islmwy-page'    : islmwy_page,
                'data-hadith-id'      : hadith_id,    
                'data-h_wa_haddathana': h_wa_haddathana,
                'data-is_thaskeel'    : is_thaskeel
            })
            
            # Find the introduction div and append it to the page container
            div_intro = page_container.find('div', class_='page-intro')
            if div_intro:
                page_container_1.append(copy(div_intro))
                
            # Append the Isnad (chain of narration)
            page_container_1.append(copy(temp_hadith_isnad))

            # Find the Hadith content div and append it to the page container
            div_matn = page_container.find('div', class_='hadith-matn')
            if div_matn:
                page_container_1.append(copy(div_matn))
   
    if container_remaining is not None:
        print('Remaining Content:', "container_remaining.prettify()")
        # Assign an id to the <div>
        container_remaining['data-islmwy-page']     = islmwy_page
        container_remaining['data-hadith-id']       = hadith_id
        container_remaining['data-h_wa_haddathana'] = h_wa_haddathana
        container_remaining['data-is_thaskeel']     = is_thaskeel
        
    # Return the structured content and relevant data
    return hadith_id, h_wa_haddathana, page_container_1, container_remaining

if __name__ == '__main__':
    from bs4 import BeautifulSoup

    # Assume 'html_content' contains the HTML of the Hadith page
    html_content = '<html>...</html>'

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Call the function to parse the Hadith page
    hadith_id, h_wa_haddathana, page_container, container_remaining = parse_hadith_page(soup)

    # You can now work with the returned data
    print('Hadith ID:', hadith_id)
    print('Phrase Occurrences:', h_wa_haddathana)
    print('Structured Content:', page_container.prettify())