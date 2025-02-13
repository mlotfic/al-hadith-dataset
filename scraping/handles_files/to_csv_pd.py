import os
import pandas as pd
from typing import Optional

def to_csv_pd(df: pd.DataFrame, filename: str, base_filename: str, ext: str,  islmwy_page: str, raw: Optional[bool] = None) -> Optional[None]:
    """
    Save a pandas DataFrame to a CSV file at a specified filepath.

    Constructs the filepath based on the provided parameters, checks if the file
    already exists, and if not, saves the DataFrame to the CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save to CSV.
        filename (str): The base name of the CSV file.
        base_filename (str): The base directory name.
        ext (str): The file extension (e.g., 'csv').
        islmwy_page (str): A page number used in the filename.
        raw (Optional[bool], optional): If True, saves in the 'raw' subdirectory.
            Defaults to None.

    Returns:
        Optional[None]: Returns None. (The function performs file I/O operations.)
    """
    # Format the page number with leading zeros (e.g., '0001')
    formatted_page = format(int(islmwy_page), '04d')
    
    # Construct the filepath
    if raw:
        # Filepath for raw data
        filepath = (
            f"./extracted_data/{base_filename}/raw/{ext}/"
            f"{filename}-{formatted_page}.{ext}"
        )
    else:
        # Filepath for processed data
        filepath = (
            f"./extracted_data/{base_filename}/{ext}/"
            f"{filename}-{formatted_page}.{ext}"
        )
    
    # Check if the specified file exists
    if os.path.exists(filepath):
        print(f"The file '{filepath}' exists.")
        # File exists, so return None
        return filepath
    else:
        # File does not exist, create the necessary directory if it doesn't exist
        dir_name = os.path.dirname(filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        # Save the DataFrame to CSV
        df.to_csv(filepath, encoding='utf-8-sig', index=False)
        return filepath
            

