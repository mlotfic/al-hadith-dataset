# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 21:01:09 2025

@author: m.lotfi
"""

from typing import Union, Optional, Dict, List, Tuple
import os
import re
import hashlib

def get_narrators_chain_id(
    hadith_id: Union[int, str], 
    chain_number: Union[int, str], 
    base_filename: str, 
    padding: int = 5
) -> str:
    """
    Generate an ID for a narrators chain by combining base_filename, hadith_id, and chain_number.
    
    Parameters:
    -----------
    hadith_id : Union[int, str]
        The hadith ID number to format
    chain_number : Union[int, str]
        The chain number to format (will be padded to 2 digits)
    base_filename : str
        Base name to prepend to the formatted numbers
    padding : int, optional
        Number of digits to pad the hadith_id with (default is 5)
        
    Returns:
    --------
    str
        Formatted ID string (e.g., 'bukhari-04204-01')
        
    Examples:
    --------
    >>> get_narrators_chain_id(4204, 1, 'bukhari')
    'bukhari-04204-01'
    >>> get_narrators_chain_id('1623', '2', 'bukhari')
    'bukhari-01623-02'
        
    Raises:
    -------
    ValueError
        If base_filename is empty or numbers are invalid
    """
    try:
        # Clean and validate base_filename
        if not base_filename or not isinstance(base_filename, str) or not base_filename.strip():
            raise ValueError("Base filename must be a non-empty string")
            
        # Convert hadith_id to integer
        try:
            hadith_num = int(hadith_id)
            if hadith_num < 0:
                raise ValueError("Hadith ID must be a positive number")
        except (TypeError, ValueError):
            raise ValueError(f"Invalid hadith ID: {hadith_id}")
            
        # Convert chain_number to integer
        try:
            chain_num = int(chain_number)
            if chain_num < 0:
                raise ValueError("Chain number must be a positive number")
        except (TypeError, ValueError):
            raise ValueError(f"Invalid chain number: {chain_number}")
        
        # Format the numbers with zero padding
        formatted_hadith_id = f"{hadith_num:0{padding}d}"
        formatted_chain_number = f"{chain_num:02d}"  # Always pad chain number to 2 digits
        
        # Combine components and return
        return f"{base_filename.strip()}-{formatted_hadith_id}-{formatted_chain_number}"
        
    except Exception as e:
        print(f"Error in get_narrators_chain_id: {str(e)}")
        raise