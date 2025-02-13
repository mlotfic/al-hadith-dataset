# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 22:36:23 2025

@author: m.lotfi
"""



from typing import Dict, Set, List, Union, Optional, Any
from bs4 import Tag
import logging
from ..data_proccessing.get_text_id import get_text_id
from ..data_proccessing.get_number_id import get_number_id
from .get_matching_dict import get_matching_dict
from .update_pickle_dict import update_pickle_dict
from ..data_proccessing.parse_query_params import parse_query_params


logger = logging.getLogger(__name__)

def update_main_subject(
    tree_subj_ids: List[str],
    tree_subj_list: List[str],
    main_subj_text: str,
    main_subject_url: str,
    hadith_id: str,
    base_filename: str,
    is_thaskeel: bool = False
) -> Optional[str]:
    """
    Updates the main subject information and its relationships with tree subjects.

    This function processes main subject data, associates it with tree subjects,
    and stores the information in a pickle file. It handles both regular and
    thaskeel (diacritical marks) versions of the text.

    Args:
        tree_subj_ids (List[str]): List of tree subject IDs
        tree_subj_list (List[str]): List of tree subject texts
        main_subj_text (str): The main subject text content
        main_subject_url (str): URL of the main subject
        hadith_id (str): Unique identifier for the hadith
        base_filename (str): Base filename for storing the processed data
        is_thaskeel (bool, optional): Flag for thaskeel version. Defaults to False.

    Returns:
        Optional[str]: The MD5 hash ID of the processed main subject if successful,
                      None if processing fails

    Raises:
        ValueError: If input parameters are invalid or missing
        IOError: If there are issues with file operations
    """
    try:
    
        # Input validation
        if not all([tree_subj_ids, tree_subj_list, main_subj_text, main_subject_url, hadith_id]):
            raise ValueError("Missing required input parameters")

        if len(tree_subj_ids) != len(tree_subj_list):
            raise ValueError("Mismatched lengths of tree subject IDs and texts")

        # Clean and prepare data
        main_subj_text = main_subj_text.strip()
        if not main_subj_text:
            logger.warning("Empty main subject text provided")
            return None

        # Generate file path and IDs
        pickle_file = 'main_subject_thaskeel' if is_thaskeel else 'main_subject'
        text = main_subj_text
        file_path, normal_id, md5_hash_id = get_text_id(text, base_filename, pickle_file)
        
        # Get existing chapter data if any
        matched_dict = get_matching_dict(file_path, md5_hash_id)
        
        # Initialize sets with default values
        hadith_ids: Set[str] = set()

        # Update sets if matched_dict exists and has valid data
        if matched_dict is not None:
            # Safely get data from matched_dict with type checking
            if isinstance(matched_dict.get("hadith_ids"), list):
                hadith_ids = set(matched_dict["hadith_ids"])

        # Add new hadith_id to the set
        hadith_ids.add(get_number_id(hadith_id, base_filename))
        
        ### **📌 Hadith Main Subject Collection (:hadith_by_subject)**
        main_subject: Dict[str, Any] = {
            "_id"               : md5_hash_id,
            "main_subj"         : main_subj_text,
            'tree_subj_ids'     : list(tree_subj_ids),
            "tree_subjs"        : list(tree_subj_list),
            "hadith_ids"        : list(hadith_ids),
            "url"               : main_subject_url
        }

        # Update the pickle file
        success = update_pickle_dict(file_path, main_subject)
        if success:
            print(f"Updated {pickle_file} successfully")
        else:
            print(f"Failed to update {pickle_file}")
            
        return md5_hash_id
    
    except Exception as e:
        logger.error(f"Unexpected error in update_main_subject: {e}")
        return None        

    
