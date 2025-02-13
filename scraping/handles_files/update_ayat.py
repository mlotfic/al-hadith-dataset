# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 19:04:54 2025

@author: m.lotfi
"""

from typing import Dict, Set, List, Union, Optional
from bs4 import Tag
from ..data_proccessing.clean_text import clean_text
from ..data_proccessing.get_text_id import get_text_id
from ..data_proccessing.get_number_id import get_number_id
from .get_matching_dict import get_matching_dict
from .update_pickle_dict import update_pickle_dict
from ..data_proccessing.parse_query_params import parse_query_params


def update_ayat(anchor: Tag, base_api: str, hadith_id: str, base_filename: str, is_thaskeel: bool = False) -> Optional[str]:
    """
    Process Quran reference from an anchor tag and update the ayat database.
    
    Parameters:
    -----------
    anchor : Tag
        BeautifulSoup Tag containing the Quran reference
    base_api : str
        Base API URL for constructing full URLs
    hadith_id : str
        ID of the hadith containing this reference
    base_filename : str
        Base filename for file operations
    is_thaskeel : bool, optional
        Flag for using thaskeel version (default: False)
        
    Returns:
    --------
    Optional[str]
        md5_hash_id of the processed ayat if successful, None otherwise
    """
    anchor_aya = anchor.find("span", class_="quran")
    if anchor_aya is not None:
        api = anchor.find("span", class_="quranatt").text.strip()
        if api:
            result = parse_query_params(api)
            surano = result.get('surano', '')
            ayano = result.get('ayano', '')
        else:
            surano = ""
            ayano = ""
            
        aya = clean_text(anchor_aya.text)
        Quran = f"Quran {surano}:{ayano}"
        
        # Generate file path and IDs
        text = f"{Quran}-{aya}"
        pickle_file = 'ayat_thaskeel' if is_thaskeel else 'ayat'
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
        
        # Create ayat dictionary
        ayat: Dict[str, Union[str, List[str]]] = {
            "_id": md5_hash_id,
            "Quran": Quran,
            "api": api,
            "url": base_api + api,
            "hadith_ids": list(hadith_ids)  # Convert set back to list
        }

        # Update the pickle file
        success = update_pickle_dict(file_path, ayat)
        if success:
            print(f"Updated {pickle_file} successfully")
        else:
            print(f"Failed to update {pickle_file}")
            
        return md5_hash_id
    
    return None
