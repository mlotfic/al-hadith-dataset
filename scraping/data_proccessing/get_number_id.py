from typing import Union, Optional, Dict, List, Tuple
import os
import re
import hashlib

# For the normalize_arabic_text function if you're using it
from arabic_reshaper import reshape  # optional
from bidi.algorithm import get_display  # optional

def get_number_id(number: Union[int, str], base_filename: str, padding: int = 5) -> str:
    """
    Generate an ID by combining base_filename and formatted number.
    
    Parameters:
    -----------
    number : Union[int, str]
        The number to format (can be string or integer)
    base_filename : str
        Base name to prepend to the formatted number
    padding : int, optional
        Number of digits to pad the number with (default is 5)
        
    Returns:
    --------
    str
        Formatted ID string (e.g., 'bukhari-04204')
        
    Examples:
    --------
    >>> get_number_id(4204, 'bukhari')
    'bukhari-04204'
    >>> get_number_id('1623', 'bukhari')
    'bukhari-01623'
    """
    try:
        # Clean inputs
        if not base_filename or not base_filename.strip():
            raise ValueError("Base filename cannot be empty")
            
        # Convert number to integer
        try:
            num = int(number)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid number: {number}")
            
        # Format the number with zero padding
        formatted_number = f"{num:0{padding}d}"
        
        # Combine base_filename and formatted number
        return f"{base_filename.strip()}-{formatted_number}"
        
    except Exception as e:
        print(f"Error in get_number_id: {str(e)}")
        raise