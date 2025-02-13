# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:59:07 2025

@author: m.lotfi
"""

import re

from .remove_diacritics_spaces_and_normalize_numbers import remove_diacritics_spaces_and_normalize_numbers

def extract_number_before_haddathana(text): 
    # Normalize the text
    normalized_text = remove_diacritics_spaces_and_normalize_numbers(text)
    # Pattern to match one or more digits before 'حدثنا' as a whole word
    pattern_list = [r'(\d+)حدثنا', r'(\d+)وبه', r'(\d+)أخبرنا', r'(\d+)اخبرنا']
    # pattern = r'(\d+)وبه|حدثنا' 
    number = "N/A"
    for pattern in pattern_list:
        # Search for the pattern in the normalized text
        match = re.search(pattern, normalized_text)
        if match:
            number = match.group(1)  # Extract the number  
            break 
    return number

'''
# Sample texts
text1 = "هذا نص عربي يحتوي على 1 حَدَّثَنَا مع بعض الكلمات الأخرى."
text2 = "هذا نص عربي يحتوي على ١ حَدَّثَنَا مع بعض الكلمات الأخرى."
text3 = "هذا نص عربي لا يحتوي على العبارة المطلوبة."
text4 = "هذا نص عربي يحتوي على 555 حَدَّثَنَا مع بعض الكلمات الأخرى."
text5 = "هذا نص عربي يحتوي على ٩٩ حَدَّثَنَا مع بعض الكلمات الأخرى."
text6 = "هذا نص عربي يحتوي على حدثنا بدون رقم قبلها."

# Run Tests
result1 = extract_number_before_haddathana(text1)
result2 = extract_number_before_haddathana(text2)
result3 = extract_number_before_haddathana(text3)
result4 = extract_number_before_haddathana(text4)
result5 = extract_number_before_haddathana(text5)
result6 = extract_number_before_haddathana(text6)

print(f"Result 1: {result1}")  # Expected: '1'
print(f"Result 2: {result2}")  # Expected: '1'
print(f"Result 3: {result3}")  # Expected: 'N/A'
print(f"Result 4: {result4}")  # Expected: '555'
print(f"Result 5: {result5}")  # Expected: '99'
print(f"Result 6: {result6}")  # Expected: 'N/A'
'''