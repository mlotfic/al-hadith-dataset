# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 01:23:01 2025

@author: m.lotfi
"""

import os
import pickle
  
def load_data_as_dict(file_path):
    """Load data from a pickle file and create a hash map for fast access."""
    try:
        # Check if file exists and has content
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return {}, False
            
        # Load existing data from pickle file
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
        
        # Ensure the data is a list of dictionaries
        if not isinstance(data, list):
            print("The data is not in the expected list format.")
            return None, False
        
        # Convert list of dictionaries to a dictionary with _id as keys
        data_dict = {entry['_id']: entry for entry in data}
        return data_dict, True
    except EOFError:
        print("File is empty or corrupted")
        return {}, False
    except FileNotFoundError:
        # If file does not exist, return empty hash map
        return {}, False
    except Exception as e:
        print(f"Error loading pickle file: {e}")
        return None, False