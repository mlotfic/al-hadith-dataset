# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 01:23:01 2025

@author: m.lotfi
"""

import pickle

from .load_data_as_dict import load_data_as_dict

def get_matching_dict(file_path, filter_id):
    """
    Load a list of dictionaries from a pickle file and return the dictionary
    that matches the specified filter_id using hash indexing.
    
    Parameters:
    - file_path: str, path to the pickle file
    - filter_id: str, the ID to filter the dictionaries
    
    Returns:
    - dict: the dictionary that matches the filter_id
    - None: if no matching dictionary is found or if there's an error
    """
    # Load data as a hash map
    data_dict, file_exists = load_data_as_dict(file_path)
    
    # Check if data_dict is None (error case) or empty
    if data_dict is None or data_dict == {}:
        return None
    
    # Retrieve the dictionary using the filter_id
    matched_dict = data_dict.get(filter_id)
    
    if matched_dict:
        return matched_dict
    else:
        print(f"No entry found with _id = {filter_id}")
        return None