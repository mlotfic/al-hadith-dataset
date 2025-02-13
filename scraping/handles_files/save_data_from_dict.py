    
import pickle

def save_data_from_dict(data_dict, file_path):
    """
    Save data stored in hash map back to pickle file.
    
    Parameters:
    - data_dict (dict): Dictionary containing the data to save
    - file_path (str): Path where the pickle file should be saved
    
    Returns:
    - bool: True if save was successful, False otherwise
    """
    try:
        # Convert the dictionary back to a list of dictionaries
        data_list = list(data_dict.values())
        
        with open(file_path, 'wb') as file:
            pickle.dump(data_list, file)
        return True
    except Exception as e:
        print(f"Error saving pickle file: {e}")
        return False