# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:20:22 2025

@author: m.lotfi

📌 Steps in the Function:
✅ Convert text to lowercase
✅ Remove diacritics (harakat like َ ُ ٌ ً ّ)
✅ Remove tatweel (elongation ـ)
✅ Normalize Alef (أ → ا, إ → ا, آ → ا)
✅ Normalize Ya (ى → ي) and Waw (ؤ → و, ئ → ي)
✅ Remove extra spaces
✅ Compute MD5 hash


"""

import re
from typing import Dict, Union

def remove_diacritics(text: str) -> str:
    """Remove Arabic diacritical marks."""
    arabic_diacritics = re.compile("""
        ّ    | # Tashdid
        َ    | # Fatha
        ً    | # Tanwin Fath
        ُ    | # Damma
        ٌ    | # Tanwin Damm
        ِ    | # Kasra
        ٍ    | # Tanwin Kasr
        ْ    | # Sukun
        ـ    | # Tatwil/Kashida
        ٰ    | # Dagger Alif
        ٓ    | # Madda above
        ٔ    | # Hamza above
        ٕ      # Hamza below
    """, re.VERBOSE)
    return arabic_diacritics.sub('', text)

def normalize_lamalef(text: str) -> str:
    """Normalize Lam-Alef combinations."""
    return text.replace('لا', 'لا').replace('لإ', 'لا').replace('لأ', 'لا').replace('لآ', 'لا')

def normalize_hamza(text: str) -> str:
    """Normalize different forms of Hamza."""
    chars_map = {
        'أ': 'ا',
        'إ': 'ا',
        'آ': 'ا',
        'ٱ': 'ا',
        'ة': 'ه',
        'ى': 'ي',
        'ئ': 'ي',
        'ؤ': 'و'
    }
    return ''.join(chars_map.get(char, char) for char in text)

def remove_punctuation(text: str) -> str:
    """Remove punctuation marks."""
    punctuation = re.compile(r'[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E\u2000-\u206F]+')
    return punctuation.sub(' ', text)

def remove_extra_spaces(text: str) -> str:
    """Remove extra spaces, newlines, and tabs."""
    return ' '.join(text.split())

def remove_numbers(text: str) -> str:
    """Remove both Arabic and English numbers."""
    text = re.sub(r'[0-9]+', '', text)  # English numbers
    text = re.sub(r'[٠-٩]+', '', text)  # Arabic numbers
    return text

def normalize_arabic_text(
    text: str,
    remove_diacritics_: bool = True,
    normalize_lamalef_: bool = True,
    normalize_hamza_: bool = True,
    remove_punctuation_: bool = True,
    remove_numbers_: bool = False
) -> str:
    """
    Normalize Arabic text with specified options.
    
    Parameters:
    text (str): Input Arabic text
    remove_diacritics_ (bool): Remove diacritical marks
    normalize_lamalef_ (bool): Normalize Lam-Alef combinations
    normalize_hamza_ (bool): Normalize different forms of Hamza
    remove_punctuation_ (bool): Remove punctuation marks
    remove_numbers_ (bool): Remove both Arabic and English numbers
    
    Returns:
    str: Normalized text
    """
    if not text:
        return ""
    
    # Apply selected normalizations
    if remove_diacritics_:
        text = remove_diacritics(text)
    
    if normalize_lamalef_:
        text = normalize_lamalef(text)
    
    if normalize_hamza_:
        text = normalize_hamza(text)
    
    if remove_punctuation_:
        text = remove_punctuation(text)
    
    if remove_numbers_:
        text = remove_numbers(text)
    
    # Remove extra spaces
    text = remove_extra_spaces(text)
    
    return text