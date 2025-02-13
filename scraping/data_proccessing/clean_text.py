# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:41:18 2025

@author: User
"""

import re

def clean_text(text):
    """
    Cleans the input text by removing specific URL fragments and normalizing whitespace.

    Parameters:
    - text (str): The input text to be cleaned.

    Returns:
    - str: The cleaned text.

    This function performs the following operations:
    1. Removes specific URL fragments that match certain patterns.
    2. Replaces multiple spaces, newlines, and tabs with a single space.
    3. Strips leading and trailing whitespace from the result.

    The URL fragments removed are:
    - 'nindex.php?page=tafseer&surano=[digits]&ayano=[digits]'
    - 'nindex.php?page=showalam&ids=[digits]'
    - 'nindex.php?page=hadith&LINKID=[digits]'
    - 'nindex.php?page=treesubj&link=[digits and underscores]'

    Example:
    >>> raw_text = "Some text with URL nindex.php?page=tafseer&surano=12&ayano=34 and more text."
    >>> clean_text(raw_text)
    'Some text with URL and more text.'
    """

    # Ensure the input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text = text.strip()
    if text:
        # Remove URL fragments using regular expressions

        # Remove 'nindex.php?page=tafseer&surano=[digits]&ayano=[digits]'
        text = re.sub(r'nindex\.php\?page=tafseer&surano=\d+&ayano=\d+', '', text)

        # Remove 'nindex.php?page=showalam&ids=[digits]'
        text = re.sub(r'nindex\.php\?page=showalam&ids=\d+', '', text)

        # Remove 'nindex.php?page=hadith&LINKID=\d+'
        text = re.sub(r'nindex\.php\?page=hadith&LINKID=\d+', '', text)

        # Remove 'nindex.php?page=treesubj&link=[digits and underscores]'
        text = re.sub(r'nindex\.php\?page=treesubj&link=[\d_]+', '', text)

        # Replace multiple spaces, newlines, and tabs with a single space
        text = re.sub(r'[\s]+', ' ', text).strip()

    return text