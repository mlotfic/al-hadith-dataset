# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:59:07 2025

@author: m.lotfi
"""

import re  # Import the regular expressions module for pattern matching

def remove_diacritics_and_spaces(text: str) -> str:
    """
    Remove Arabic diacritics and whitespace characters from the input text.

    This function removes Arabic diacritics (tashkeel) from the given text,
    as well as any spaces or other whitespace characters, resulting in a
    string that contains only the base Arabic letters.

    Args:
        text (str): The input string from which to remove diacritics and spaces.

    Returns:
        str: The cleaned string without diacritics and whitespace.
    """
    # Regular expression pattern for Arabic diacritics
    arabic_diacritics_pattern: str = (
        r"[\u0610-\u061A"  # Various signs
        r"\u064B-\u065F"   # Harakat
        r"\u06D6-\u06ED"   # Additional marks
        r"]"
    )
    # Compile the regular expression pattern for efficiency
    arabic_diacritics: re.Pattern = re.compile(arabic_diacritics_pattern, flags=re.UNICODE)
    
    # Remove diacritics using the compiled pattern
    text = re.sub(arabic_diacritics, '', text)
    
    # Remove spaces and other whitespace characters
    text = re.sub(r'\s+', '', text)
    
    return text