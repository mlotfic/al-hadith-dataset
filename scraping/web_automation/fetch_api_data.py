# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 11:03:08 2025

@author: m.lotfi
"""

import requests
import json 
import time

from bs4 import BeautifulSoup

from ..data_proccessing.clean_text import clean_text
 
    
def fetch_api_data(api_url, ext, max_retries = 3 ):    
      
    # Retry mechanism for API request
    for attempt in range(max_retries):
        try:
            # Send GET request with timeout and error handling
            response = requests.get(
                api_url, 
                timeout=30,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            
            # Raise an exception for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            if ext == 'json':
                data = response.json()
                
                return data
            else:
                data = response.text            
                # Parse the HTML
                api_soup = BeautifulSoup(data, 'lxml')
                api_text = clean_text(api_soup.text)
                
                return api_text
            
        except requests.exceptions.RequestException as req_error:
            print(f"Request attempt {attempt + 1} failed: {req_error}")
            
            # Wait before retrying (exponential backoff)
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"Failed to fetch data after {max_retries} attempts")
                return None
        
        except json.JSONDecodeError as json_error:
            print(f"JSON decoding error: {json_error}")
            return None
        
        except IOError as io_error:
            print(f"File writing error: {io_error}")
            return None

if __name__ == "__main__":
    # Define the parameters
    
    api_url = f'https://www.islamweb.net/ar/library/maktaba/nindex.php?page=hadith&LINKID=650001&json=1'

    ext = "json"
    # Fetch the API data and save it to disk
    data = fetch_api_data(api_url, "json") 
    if data is None:
        print("Failed to fetch or save data")