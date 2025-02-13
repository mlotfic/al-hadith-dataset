# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 11:16:30 2025

@author: m.lotfi
"""

import requests

def get_api_response(url, headers=None, params=None, timeout=10):
    """
    Fetch API response from a web URL (typically found in browser's network tab)
    
    Args:
        url (str): API endpoint URL
        headers (dict): Optional headers dictionary
        params (dict): Optional parameters for GET request
        timeout (int): Request timeout in seconds
    
    Returns:
        dict/list: Parsed JSON response or None if failed
    """
    # Default headers if not provided
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
    }
    
    try:
        response = requests.get(
            url,
            headers=headers if headers else default_headers,
            params=params,
            timeout=timeout
        )
        response.raise_for_status()  # Raise exception for 4xx/5xx status codes
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Failed to parse JSON: {e}")
        return None
    
# Example usage:
if __name__ == "__main__":
    # These values should be identified from the website's network traffic
    api_url = "https://example.com/api/data"
    custom_headers = {
        'Referer': 'https://example.com/',
        'X-Requested-With': 'XMLHttpRequest'
    }
    parameters = {
        'page': 1,
        'items_per_page': 20
    }
    
    data = get_api_response(api_url, headers=custom_headers, params=parameters)
    if data:
        print("Successfully retrieved data:")
        print(data)