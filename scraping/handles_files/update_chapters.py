# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 20:09:36 2025

@author: m
"""

from typing import Dict, List, Tuple, Optional, Any
from ..data_proccessing import clean_text, get_text_id, get_number_id
from .get_matching_dict import get_matching_dict
from .update_pickle_dict import update_pickle_dict

def update_chapters(hadith_id: str, 
                    ayat_ids: list,
                    narrator_ids: list,
                    div_intro_text: str, 
                    scraping_table: Dict[str, List], 
                    base_filename: str) -> bool:
    """
    Update the Ayat database with chapter information and hadith references.
    
    Parameters:
    -----------
    hadith_id : str
        The ID of the hadith to be added
    div_intro_text : str
        The introduction text for the chapter
    scraping_table : Dict[str, List]
        Dictionary containing scraped data with keys:
        ['book_page', 'chapter', 'book_id', 'book_name', 'section', 
         'sub_section', 'part_I']
    base_filename : str
        Base filename for ID generation
        
    Returns:
    --------
    bool
        True if update was successful, False otherwise
    """
    # Extract basic information
    book_page = scraping_table["book_page"][0]
    text      = scraping_table["chapter"][0]
    
    # Generate file path and IDs
    file_path, normal_id, md5_hash_id = get_text_id(text, base_filename, pickle_file="chapters")
    
    # Get existing chapter data if any
    matched_dict = get_matching_dict(file_path, md5_hash_id)
    
    # Handle hadith list
    if matched_dict:
        print("Matched dictionary found")
        hadith_ids = matched_dict.get("hadith_ids", [])
    else:
        print("No matching dictionary found. Creating new entry.")
        hadith_ids = []
    
    # Add new hadith ID and remove duplicates
    hadith_ids.append(get_number_id(hadith_id, base_filename))
    hadith_ids = list(set(hadith_ids))
    
    ### **📌 Chapter Introduction (:chapter_intro)**
    # Create chapter dictionary
    chapter: Dict[str, Any] = {
        "_id"                       : md5_hash_id,
        "normal_id"                 : normal_id,
        'book_page'                 : get_number_id(book_page, base_filename), 
        "book_id"                   : scraping_table["book_id"][0], 
        "book_name"                 : scraping_table["book_name"][0],   
        "section"                   : scraping_table["section"][0],
        "sub_section"               : scraping_table["sub_section"][0], 
        "part_I"                    : scraping_table["part_I"][0],         
        "chapter"                   : scraping_table["chapter"][0],
        "text"                      : div_intro_text,
        "hadith_ids"                : hadith_ids,
        "ayat_ids"                  : ayat_ids,
        "narrator_ids"              : narrator_ids                
        }
    # Update the database
    return update_pickle_dict(file_path, chapter)
