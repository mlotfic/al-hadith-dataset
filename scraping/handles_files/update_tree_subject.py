# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 22:35:48 2025

@author: m.lotfi
"""
"""
Tree Subject Processing Module

This module handles the processing and storage of tree subject information from
hadith texts. It includes functionality for fetching data from APIs, processing
HTML content, and maintaining persistent storage in pickle files.

The module is part of a larger system for processing and organizing hadith texts
and their associated metadata.

Dependencies:
    - requests: For making HTTP requests to the API
    - BeautifulSoup4: For parsing HTML content
    - typing: For type hints
    - Custom modules for text processing and data storage

Note: This module requires proper configuration of API endpoints and file paths
to function correctly.
"""

import requests
from typing import Dict, Set, List, Union, Any, Optional
from bs4 import BeautifulSoup, Tag

from ..data_proccessing.clean_text import clean_text
from ..data_proccessing.get_text_id import get_text_id
from ..data_proccessing.get_number_id import get_number_id
from .get_matching_dict import get_matching_dict
from .update_pickle_dict import update_pickle_dict
from ..data_proccessing.parse_query_params import parse_query_params

def update_tree_subject(
    main_subj: Tag, 
    base_api: str, 
    hadith_id: str, 
    base_filename: str, 
    is_thaskeel: bool = False
) -> tuple[list[str], list[str], str]:
    """
    Updates tree subject information by processing HTML content and storing it in pickle files.
    
    This function extracts tree subject information from a given HTML tag, fetches additional
    data from an API, and updates a pickle file with the processed information. It handles
    both regular and thaskeel (diacritical marks) versions of the text.

    Args:
        main_subj (Tag): BeautifulSoup Tag object containing the main subject information
        base_api (str): Base URL for the API endpoint
        hadith_id (str): Unique identifier for the hadith
        base_filename (str): Base filename for storing the processed data
        is_thaskeel (bool, optional): Flag to indicate if processing thaskeel version. 
            Defaults to False.

    Returns:
        tuple[list[str], list[str]]: A tuple containing two lists:
            - First list: Tree subject IDs (md5 hashes)
            - Second list: Tree subject texts

    Raises:
        requests.RequestException: If there's an error fetching data from the API
        requests.Timeout: If the API request times out
        requests.HTTPError: If the API returns an error status code
        
    Example:
        >>> tag = soup.find('div', class_='main-subject')
        >>> ids, texts = update_tree_subject(
        ...     tag, 
        ...     'https://api.example.com/', 
        ...     'hadith123', 
        ...     'base_file'
        ... )
        >>> print(len(ids), len(texts))
        2 2

    Notes:
        - The function creates or updates pickle files to store the processed data
        - Each tree subject is stored with its associated hadith IDs and main subject IDs
        - The function handles both new entries and updates to existing entries
        - URLs are constructed using the base_api and tree subject IDs
        - The function includes error handling for API requests and data processing
    """
    try:
        tree_subj_urls = []  # Initialize as empty list
        tree_subj_list = []
        tree_subj_ids  = []  # Initialize tree_subj_ids

        tree_subj_span = main_subj.find('span', class_="mainsubjatt")
        if not tree_subj_span:
            return [], [], ""  # Return empty lists if no span found

        tree_subj_api = tree_subj_span.text.strip()
        url_params = parse_query_params(tree_subj_api)
        tree_subj_normal_ids = url_params.get("link", "").split("_")
        tree_subj_urls = [f"{base_api}nindex.php?page=treesubj&link={num}" 
                         for num in tree_subj_normal_ids]

        for tree_subj_id, tree_subj_url in zip(tree_subj_normal_ids, tree_subj_urls):
            try:
                # Fetch the API data
                response = requests.get(
                    tree_subj_url,
                    timeout=30,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                )
                # Raise an exception for HTTP errors
                response.raise_for_status()
                api_soup = BeautifulSoup(response.text, 'html.parser')  # Specify parser
                tree_subj_text = clean_text(api_soup.text)
                
                if not tree_subj_text:
                    continue
                
                pickle_file = 'tree_subj_thaskeel' if is_thaskeel else 'tree_subj'
                file_path, normal_id, md5_hash_id = get_text_id(
                    tree_subj_text, 
                    base_filename, 
                    pickle_file
                )
                
                # Get existing data
                matched_dict = get_matching_dict(file_path, md5_hash_id)
                
                # Initialize sets
                hadith_ids = set()
                main_subj_ids = set()
                
                # Update sets from existing data
                if matched_dict:
                    if isinstance(matched_dict.get("hadith_ids"), list):
                        hadith_ids.update(matched_dict["hadith_ids"])
                    if isinstance(matched_dict.get("main_subj_ids"), list):
                        main_subj_ids.update(matched_dict["main_subj_ids"])
                
                # Add new hadith_id
                hadith_ids.add(get_number_id(hadith_id, base_filename))

                ### **📌 Hadith Sub (Tree) Subject Collection (:hadith_by_tree_subject)**
                tree_subj: Dict[str, Any] = {
                    "_id"               : md5_hash_id,
                    'id'                : tree_subj_id,
                    "tree_subj"         : tree_subj_text,
                    'main_subj_ids'     : list(main_subj_ids),
                    "hadith_ids"        : list(hadith_ids),
                    'url'               : tree_subj_url
                }

                # Update pickle file
                if not update_pickle_dict(file_path, tree_subj):
                    print(f"Failed to update {pickle_file}")
                    continue

                tree_subj_list.append(tree_subj_text)
                tree_subj_ids.append(md5_hash_id)

            except requests.RequestException as e:
                print(f"Error fetching {tree_subj_url}: {e}")
                continue
            except Exception as e:
                print(f"Error processing tree subject: {e}")
                continue

        return tree_subj_ids, tree_subj_list, base_api + tree_subj_api

    except Exception as e:
        print(f"Error in update_tree_subject: {e}")
        return [], [], ""