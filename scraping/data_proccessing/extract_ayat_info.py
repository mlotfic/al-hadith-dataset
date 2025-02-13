
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 11:03:08 2025

@author: m.lotfi
"""

import re
from typing import Dict, Optional

def extract_ayat_info(onclick_str: str) -> Optional[Dict[str, str]]:
    """
    Extract Ayat information from onclick attribute string.
    
    Parameters:
    onclick_str (str): The onclick attribute string containing Ayat information
    
    Returns:
    Optional[Dict[str, str]]: Dictionary containing extracted information or None if parsing fails
    """
    try:
        # Define regex patterns
        url_pattern = r"src=['\"]([^'\"]+)['\"]"
        title_pattern = r"TITLE,\s*['\"](.*?)['\"]"
        params_pattern = r"surano=(\d+)&ayano=(\d+)"
        
        # Extract URL
        url_match = re.search(url_pattern, onclick_str)
        if not url_match:
            return None
        api_url = url_match.group(1)
        
        # Extract title
        title_match = re.search(title_pattern, onclick_str)
        title        = title_match.group(1) if title_match else ''
        
        # Extract surano and ayano
        params_match = re.search(params_pattern, api_url)
        if not params_match:
            return None
            
        surano, ayano = params_match.groups()
        
        # Create and return result dictionary
        return {
            "surano": surano,
            "ayano": ayano,
            "title": title,
            "api": api_url
        }
        
    except Exception as e:
        print(f"Error extracting Ayat information: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    onclick_str = """onclick="Tip('<IFRAME src=\'/ar/library/ayatafseer.php?surano=8&ayano=24\' border=0 frameborder=0 WIDTH=280 HEIGHT=165></IFRAME>', WIDTH, 280, TITLE, 'تفسير الآية', SHADOW, false, FADEIN, 600, FADEOUT, 600, STICKY, 1, CLOSEBTN, true, CLICKCLOSE, true)"""

    result = extract_ayat_info(onclick_str)
    if result:
        print("Extracted information:")
        for key, value in result.items():
            print(f"{key}: {value}")