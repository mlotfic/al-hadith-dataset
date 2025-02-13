# hadith_narrators_extractor.py

import re
from typing import Dict, TypedDict, Union, List, Optional

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

from .get_narrator_data_from_tags import get_narrator_data_from_tags
from ..data_proccessing.clean_text import clean_text
from ..data_proccessing.get_narrators_chain_id import get_narrators_chain_id
from ..handles_files.update_pickle_dict import load_data_as_dict
from ..handles_files.update_pickle_dict import get_matching_dict
from ..handles_files.update_pickle_dict import save_data_from_dict
from ..handles_files.update_pickle_dict import update_pickle_dict
from ..handles_files.update_narrators   import update_narrators

# class_ = 'hadith-isnad'
# class_ = "narrators-chain"
def get_hadith_narrators(container: Tag, 
                         base_api           : str, 
                         class_             : str, 
                         islmwy_page        : int, 
                         hadith_id          : str, 
                         book_id            : str, 
                         h_wa_haddathana    : str, 
                         base_filename      : str,
                         is_thaskeel        :bool = False) -> List[Dict[str, str]]:
    r"""
    Extracts narrators' data from a Hadith's isnad section within the given HTML container.

    Parameters:
    - container (Tag): The BeautifulSoup Tag object containing the Hadith data.
    - class_name (str): CSS class for the isnad section.
    - base_api (str): The base API URL to construct full URLs.
    - islmwy_page (int): The page number on the website.
    - hadith_id (int): The Hadith's ID within the book.
    - h_wa_haddathana (str): The Hadith's chain identifier, e.g., '1' or '2', extracted from '[\d]+ ح حَدَّثَنَا'.

    Returns:
    - narrators_list (List[Dict[str, str]]): A list of dictionaries containing narrators' information.

    This function performs the following steps:
    1. Finds the 'div' with class 'hadith-isnad' within the provided container.
    2. Iterates over its child nodes, handling NavigableString and Tag objects separately.
    3. Extracts and cleans text from text nodes and appends it to the overall text.
    4. For each Tag:
        - Cleans the text content.
        - Attempts to extract narrator data using 'get_narrator_data_from_tags'.
        - If narrator data is found:
            - Extracts text before and after the Tag.
            - Constructs a dictionary with narrator information.
            - Appends it to the narrators list.

    Note:
    - This function depends on external functions:
        - 'clean_text(text)' to clean and normalize text.
        - 'get_narrator_data_from_tags(child, base_api)' to extract narrator data from a Tag.
    - Ensure that these functions are defined or imported in your code.

    """

    # Find the 'div' with class 'hadith-isnad' within the container
    page_divs = container.find_all('div', class_)
    if not page_divs:
        # If the 'hadith-isnad' div is not found, return an empty list
        return []

    # Initialize variables
    page_div_text = ""
    order = 0  # Serial number for narrators in the chain
    narrators_list = []
    narrators_chain_list = []
    for i, page_div in enumerate(page_divs):
        # print(i)
        # Iterate over the child nodes of 'hadith-isnad'
        for j, child in enumerate(page_div.children):
            if isinstance(child, NavigableString):
                if isinstance(child, Comment):
                    # It's an HTML comment; skip processing
                    # print(f"Found a comment at position {j}: {child}")
                    continue
                else:
                    # It's a regular text node
                    # Strip whitespace and check if the string is not empty
                    text = child.strip()
                    if text:
                        # Replace multiple spaces, newlines, and tabs with a single space
                        text = re.sub(r'[\s]+', ' ', text).strip()
                        # Append to the overall text
                        page_div_text += " " + text
    
            elif isinstance(child, Tag):
                # It's an HTML Tag element
                # Extract and clean the text content of the tag
                text = child.text.strip()
                if text:
                    # Remove URL fragments and clean the text
                    text = clean_text(text)
                    # Append to the overall text
                    page_div_text += " " + text
    
                # Attempt to extract narrator data from the tag
                narrator = get_narrator_data_from_tags(child, base_api)
                
                if narrator:
                    # Get the text before this tag
                    text_before = ''
                    if child.previous_sibling:
                        if isinstance(child.previous_sibling, Tag):
                            text_before = child.previous_sibling.get_text()
                        elif isinstance(child.previous_sibling, NavigableString):
                            text_before = child.previous_sibling.strip()
    
                    # Get the text after this tag
                    text_after = ''
                    if child.next_sibling:
                        if isinstance(child.next_sibling, Tag):
                            text_after = child.next_sibling.get_text()
                        elif isinstance(child.next_sibling, NavigableString):
                            text_after = child.next_sibling.strip()
    
                    order += 1  # Increment the chain serial number
    
                    ### **📌 Narrators Chain (:narrators_chain)**
                    # Create narrators chain dictionary
                    narrators_chain : Dict[str, Union(str, list)] = {
                        "_id"                       : get_narrators_chain_id(hadith_id, i, base_filename),
                        "h_wa_haddathana"           : h_wa_haddathana,                                      # Chain identifier
                        "h_wa_chain"                : i,                                                    # 
                        "order"                     : order,                                                # Chain serial number
                        "aliase"                    : narrator.get("aliase"),                               # Narrator's name
                        "narrators_id"              : narrator.get("_id"),                                  # Narrator's ID
                        "before"                    : text_before,                                          # Text before the tag
                        "after"                     : text_after,                                           # Text after the tag
                        "context"                   : ""
                    }
                    
                    # Append the extracted data to the narrators_chain_list
                    narrators_chain_list.append(narrators_chain)

                    file_path = f"./extracted_data/{base_filename}/db/{'narrators_thaskeel.pkl' if is_thaskeel else 'narrators.pkl'}"
                    
                    success = update_narrators(narrator, text_before, text_after, file_path)
                    if success:
                        print(f"Chapter updated {'narrators_thaskeel.pkl' if is_thaskeel else 'narrators.pkl'} successfully.")
                    else:
                        print("Failed to update/append narrator pkl file")
    
    # add page_div_text to each narrator
    for narrators_chain in narrators_chain_list:
        narrators_chain["context"] = page_div_text
        
    return narrators_chain_list