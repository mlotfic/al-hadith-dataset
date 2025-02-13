# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:59:07 2025

@author: m.lotfi
"""

import os
import requests                # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML content
from typing import List, Dict, Any
import json                    # For saving output_sequence to a JSON file

def json_normalize_tkhreg_hadith_response(
    islmwy_page : int                    ,
    json_data   : List[Dict[str, Any]]   ,
    folder      : str = "./extracted_data/bukhari/json"
) -> List[Dict[str, str]]:
    """
    Normalize and process Hadith response data from JSON.

    This function processes JSON data containing Hadith information. It checks if
    a corresponding JSON file exists, and if not, it iterates through the data to
    extract and compile relevant Hadith details. The output is saved to a JSON file
    and returned as a list of dictionaries.

    Args:
        islmwy_page (int): The Islamic page number associated with the data.
        json_data (List[Dict[str, Any]]): The JSON data to be processed.
        folder (str, optional): The folder path where JSON files are stored.
                                Defaults to "./extracted_data/bukhari/json".

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the extracted Hadith details.
    """
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Construct the filename using the provided folder and page number, with .json extension
    filename: str = f"{folder}/hadith_{islmwy_page:04d}.json"

    # Check if the specified JSON file exists
    if os.path.exists(filename):
        print(f"The file '{filename}' exists.")
        # File exists. Return the existing data if needed
        with open(filename, 'r', encoding='utf-8') as f:
            output_sequence = json.load(f)
        return output_sequence

    # Initialize an empty list to store the output sequence
    output_sequence: List[Dict[str, str]] = []

    # Define the base URL for constructing full URLs
    base_url: str = "https://example.com"  # Replace with the actual base URL

    # Iterate over each book item in the JSON data
    for book_item in json_data:
        xref_book_name : str = book_item.get('bookname', '')
        xref_book_id   : str = book_item.get('id', '')

        # Iterate over each detail in the book's details
        details: List[Dict[str, Any]] = book_item.get('details', [])
        for detail in details:
            xref_islmwy_page       : str = detail.get('source_id', '')
            xref_hadith_book_name  : str = detail.get('bookname', '')
            xref_hadith_id         : str = detail.get('bookhad', '')
            xref_hadith_href       : str = detail.get('href', '')
            xref_hadith_api        : str = ''
            xref_hadith_url_content: str = ''

            # Proceed only if 'bookhad' (Hadith ID) is present
            if xref_hadith_id != '':
                # Parse the HTML in xref_hadith_href to extract the data-url attribute
                if xref_hadith_href != '':
                    soup             = BeautifulSoup(xref_hadith_href, 'html.parser')
                    a_tag            = soup.find('a', class_='hadithTak')
                    xref_hadith_api  = a_tag.get('data-url', '') if a_tag else ''

                    # Construct the full URL by combining the base URL and the data-url
                    if xref_hadith_api != '':
                        xref_hadith_full_url: str = base_url + xref_hadith_api

                        # Make a request to the full URL to get the response content
                        try:
                            hadith_response         = requests.get(xref_hadith_full_url)
                            hadith_response.raise_for_status()
                            xref_hadith_url_content = hadith_response.text
                        except requests.HTTPError as http_err:
                            print(f"HTTP error occurred: {http_err}")
                        except Exception as err:
                            print(f"An error occurred: {err}")

            # Construct the output dictionary with type hint
            output_item: Dict[str, str] = {
                "islmwy_page"          : str(islmwy_page),           # The Islamic page number
                "xref_book_name"       : xref_book_name,             # The name of the book
                "xref_book_id"         : xref_book_id,               # The ID of the book
                "xref_islmwy_page"     : xref_islmwy_page,           # Source page ID from the detail
                "xref_hadith_book_name": xref_hadith_book_name,      # The name of the Hadith book
                "xref_hadith_id"       : xref_hadith_id,             # The Hadith ID
                "xref_hadith_href"     : xref_hadith_href,           # The HTML href content
                "xref_hadith_api"      : xref_hadith_api,            # The API endpoint extracted from href
                "xref_hadith_url"      : xref_hadith_url_content,    # The content retrieved from the Hadith URL
            }

            # Append the output item to the sequence
            output_sequence.append(output_item)

    # Save 'output_sequence' to the file specified by 'filename'
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_sequence, f, ensure_ascii=False, indent=4)
        print(f"Data saved to '{filename}' successfully.")
    except Exception as e:
        print(f"An error occurred while saving data to '{filename}': {e}")

    # Return the output sequence
    return output_sequence