# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 16:44:09 2025

@author: m.lotfi
"""

from typing import Dict, Set, List, Optional, Any
from .get_matching_dict import get_matching_dict
from .update_pickle_dict import update_pickle_dict

def update_narrators(narrator: Dict[str, Any], text_before: Optional[str], text_after: Optional[str], file_path: str) -> bool:
    """
    Update narrator information in the database with new aliases and keywords.
    
    Parameters:
    -----------
    narrator : Dict[str, Any]
        Dictionary containing narrator information with keys:
        ['_id', 'aliase', 'narrators_api', 'narrators_api_type', 'narrators_api_url']
    text_before : Optional[str]
        Text that appears before the narrator's name
    text_after : Optional[str]
        Text that appears after the narrator's name
    file_path : str
        Path to the pickle file storing narrator data
        
    Returns:
    --------
    bool
        True if update was successful, False otherwise
    """
    try:
        # Validate input
        if not narrator or '_id' not in narrator:
            raise ValueError("Invalid narrator dictionary: missing '_id'")
            
        filter_id = narrator.get("_id")
        if not filter_id:
            raise ValueError("Invalid narrator ID")

        # Get existing narrator data
        matched_dict = get_matching_dict(file_path, filter_id)

        # Initialize sets with default values
        aliases: Set[str] = set()
        before_keyword_list: Set[str] = set()
        after_keyword_list: Set[str] = set()
        name: str = ""

        # Update sets if matched_dict exists and has valid data
        if matched_dict is not None:
            # Safely get data from matched_dict with type checking
            if isinstance(matched_dict.get("aliases"), list):
                aliases = set(matched_dict["aliases"])
            
            if isinstance(matched_dict.get("name"), str):
                name = matched_dict["name"]
            
            if isinstance(matched_dict.get("before_keyword_list"), list):
                before_keyword_list = set(matched_dict["before_keyword_list"])
            
            if isinstance(matched_dict.get("after_keyword_list"), list):
                after_keyword_list = set(matched_dict["after_keyword_list"])

        # Add new values to sets if they exist
        if aliase := narrator.get("aliase"):
            aliases.add(aliase)
        
        if text_before:
            before_keyword_list.add(text_before)
        
        if text_after:
            after_keyword_list.add(text_after)
     
        # Update narrator dictionary with new lists
        ### **📌 Narrator (:narrator)**
        narrator_updates: Dict[str, str] = {
            "_id"                   : narrator.get("_id"),               # Extracted ID from the URL parameters
            "name"                  : name,
            "api"                   : narrator.get("narrators_api"),              # Relative API endpoint or URL fragment
            "api_type"              : narrator.get("narrators_api_type"),         # Type of API (hardcoded as 'html')
            "url"                   : narrator.get("narrators_api_url"),          # Full API URL constructed from base_api and namesatt
            'aliases'               : list(aliases),
            'before_keyword_list'   : list(before_keyword_list),
            'after_keyword_list'    : list(after_keyword_list)
        } 
        
        return update_pickle_dict(file_path, narrator_updates)
    except Exception as e:
       print(f"Error in update_narrators: {str(e)}")
       return None
    