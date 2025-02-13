# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 22:18:21 2025

@author: m.lotfi
"""
import pickle

from .load_data_as_dict import load_data_as_dict
from .get_matching_dict import get_matching_dict
from .save_data_from_dict import save_data_from_dict

# new_dict = chapter
def update_pickle_dict(file_path, new_dict):
    """
    Update or append an entry in a hash map and save to pickle.
    - if the file does not exist, it will be created.
    - if the dictionary with the same _id exists, it will be updated (merged).
    - if the dictionary with the same _id does not exist, it will be appended.   
    
    Args:
        file_path (str): Path to the pickle file
        new_dict (dict): Dictionary containing the data to update/append with '_id' key
    
    Returns:
        bool: True if operation was successful, False otherwise
    """
    # Check if new_dict has '_id' key
    if '_id' not in new_dict:
        print("Error: new_dict must contain '_id' key")
        return False

    # Load data as a hash map
    data_dict, file_exists = load_data_as_dict(file_path)
    
    # Check if load was successful
    if data_dict is None:
        return False
        
    # Get the _id from new_dict
    _id = new_dict['_id']
    
    if _id in data_dict:
        # If entry exists, update it (merge the dictionaries)
        data_dict[_id].update(new_dict)
    else:
        # If entry doesn't exist, add it as a new entry
        data_dict[_id] = new_dict
    
    # Save the updated data back to the pickle file
    return save_data_from_dict(data_dict, file_path)
    
if __name__ == '__main__':
    # Example usage of the function:
    file_path = 'ayat.pkl'
    filter_id = '1234-5678'

    matched_dict = get_matching_dict(file_path, filter_id)
    if matched_dict:
        print("Matched dictionary:")
        print(matched_dict)
    else:
        print("No matching dictionary found.")


    # Example usage:
    ayat_file_path = 'ayat.pkl'
    new_narrator_dict = {
        "_id": "1234-5678",
        "islmwy_page": "5678",
        "hadith_id": "H123",
        "h_wa_haddathana": "chain1",
        "h_wa_chain": 1,
        "is_thaskeel": True,
        "ayat_chain_number": 2  # Updated value
    }

    success = update_ayat(ayat_file_path, new_narrator_dict)
    if success:
        print("Operation completed successfully.")
    else:
        print("Operation failed.")   
