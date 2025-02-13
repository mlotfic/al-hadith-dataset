# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:59:07 2025

@author: m.lotfi
"""


import re


def remove_diacritics_spaces_and_normalize_numbers(text):
    # Regular expression pattern for Arabic diacritics
    arabic_diacritics = re.compile("""
        [\u0610-\u061A   # Various signs
         \u064B-\u065F   # Harakat (short vowels)
         \u06D6-\u06ED   # Additional Quranic annotations
         ]""", re.VERBOSE)
    # Remove diacritics
    text = re.sub(arabic_diacritics, '', text)
    # Remove spaces and whitespace characters
    text = re.sub(r'\s+', '', text)
    # Normalize Arabic-Indic numerals to Western numerals
    arabic_numerals = {'٠':'0','١':'1','٢':'2','٣':'3','٤':'4',
                       '٥':'5','٦':'6','٧':'7','٨':'8','٩':'9'}
    for arabic_num, western_num in arabic_numerals.items():
        text = text.replace(arabic_num, western_num)
    return text