# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:59:07 2025

@author: m.lotfi
"""

import re  # Import the regular expressions module for pattern matching

from .remove_diacritics_and_spaces import remove_diacritics_and_spaces

def get_h_wa_haddathana_count_occurrences(text: str, pattern: str) -> int:
    """
    Count the number of non-overlapping occurrences of a normalized pattern in a text.

    This function removes diacritics and whitespace from both the input text and the pattern,
    escapes any special regex characters in the pattern, and then counts the number of
    non-overlapping occurrences of the pattern within the text.

    Args:
        text (str): The input text in which to search for pattern occurrences.
        pattern (str): The pattern to search for within the text.

    Returns:
        int: The number of non-overlapping occurrences of the pattern in the text.
    """
    # Normalize the text and pattern
    normalized_text   : str = remove_diacritics_and_spaces(text)    # Text without diacritics and spaces
    normalized_pattern: str = remove_diacritics_and_spaces(pattern)  # Pattern without diacritics and spaces

    # Escape special regex characters in the pattern
    escaped_pattern: str = re.escape(normalized_pattern)  # Pattern safe for regex matching

    # Use re.findall to count non-overlapping occurrences
    matches: list = re.findall(escaped_pattern, normalized_text)  # List of matches found

    # Return the count of matches
    return len(matches)


'''
# Sample text
text = """
حَدَّثَنَا أَبُو بَكْرٍ، حَدَّثَنَا عَبْدُ اللَّهِ، حَدَّثَنَا أَبُو خَالِدٍ، عَنْ الْحَسَنِ، قَالَ: حَدَّثَنَا رَجُلٌ،
ح وَحَدَّثَنَا أَبُو عُبَيْدٍ، حَدَّثَنَا عَبْدُ الرَّحْمَنِ، حَدَّثَنَا سُفْيَانُ
ح وَحَدَّثَنَا مَالِكٌ، عَنْ نَافِعٍ
ح وحدثنا شعبة عن قتادة
"""

# The phrase you're searching for
phrase = 'ح وَحَدَّثَنَا'

# Use a variable name that's valid in Python
h_wa_haddathana_count = count_occurrences(text, phrase)

print(f"The phrase '{phrase}' occurs {h_wa_haddathana_count} times in the text.")'''