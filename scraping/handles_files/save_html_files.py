# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 11:52:11 2025

@author: m.lotfi
"""

import os

from ..data_proccessing.clean_html import clean_html

def save_html_files(base_folder, base_filename, islmwy_page, extracted_html, extracted_texts, raw_html):
    """
    Saves different versions of HTML content to specified directories.
    If any target file does not exist, overwrite all files and return True.
    If all files exist, skip saving files and return None.

    Parameters:
    - base_folder (str)             : The base directory where files will be saved.
    - base_filename (str)           : The base name for the files.
    - islmwy_page (int or str)      : The current page number to format.
    - extracted_html (list of str)  : List of extracted raw HTML strings.
    - extracted_texts (list of str) : List of extracted clean text strings.
    - raw_html (str)                : The raw HTML content.
    - html (str)                    : The HTML content to be cleaned.
    - clean_html_function (callable): A function that cleans HTML content.

    Returns:
    - True if files were saved (i.e., any file did not exist)
    - None if all files existed and no files were saved
    """

    # Format page number with leading zeros (e.g., '0001', '0002')
    page_formatted = f"{int(islmwy_page):04d}"

    # Prepare file paths
    file_paths = []
    directory_paths = []

    # Paths for extracted raw HTML
    base_sub_folder_modal = "raw/modal/"
    file_path_modal = os.path.join(base_folder, base_sub_folder_modal, f"{base_filename}-modal-{page_formatted}.html")
    file_paths.append(file_path_modal)
    directory_paths.append(os.path.dirname(file_path_modal))

    # Paths for extracted clean text
    base_sub_folder_modal_clean = "raw/modal_clean/"
    file_path_modal_clean = os.path.join(base_folder, base_sub_folder_modal_clean, f"{base_filename}-modal-clean-{page_formatted}.html")
    file_paths.append(file_path_modal_clean)
    directory_paths.append(os.path.dirname(file_path_modal_clean))

    # Path for raw HTML
    base_sub_folder_raw_html = "raw/html/"
    file_path_raw_html = os.path.join(base_folder, base_sub_folder_raw_html, f"{base_filename}-{page_formatted}.html")
    file_paths.append(file_path_raw_html)
    directory_paths.append(os.path.dirname(file_path_raw_html))

    # Path for clean HTML
    base_sub_folder_html_clean = "raw/html_clean/"
    file_path_html_clean = os.path.join(base_folder, base_sub_folder_html_clean, f"{base_filename}-clean-{page_formatted}.html")
    file_paths.append(file_path_html_clean)
    directory_paths.append(os.path.dirname(file_path_html_clean))

    # Check if all files exist
    all_files_exist = all(os.path.exists(file_path) for file_path in file_paths)

    if all_files_exist:
        # All files exist, skip saving
        print("All files exist. Skipping saving files.")
        return None
    else:
        # At least one file does not exist, overwrite all files

        # ✅ Ensure directories exist
        for directory in set(directory_paths):
            os.makedirs(directory, exist_ok=True)

        # ✅ Save extracted modals raw HTML
        with open(file_path_modal, "w", encoding="utf-8") as file:
            file.write("\n".join(extracted_html))

        # ✅ Save extracted modals text
        with open(file_path_modal_clean, "w", encoding="utf-8") as file:
            file.write("\n".join(extracted_texts))

        # ✅ Save extracted raw HTML
        with open(file_path_raw_html, "w", encoding="utf-8") as file:
            file.write(raw_html)

        # ✅ Save Save clean html
        html_clean = clean_html(raw_html)
        with open(file_path_html_clean, "w", encoding="utf-8") as file:
            file.write(html_clean)

        print("✅ Extraction complete. Data saved.")
        return True
    
if __name__ == "__main__":
    # Example usage
    base_folder = "data/"
    base_filename = "example"
    islmwy_page = 1
    extracted_html = ["<div>Extracted raw HTML</div>"]
    extracted_texts = ["Extracted clean text"]
    raw_html = "<html><body>Raw HTML</body></html>"
    html = "<html><body>HTML content</body></html>"
    clean_html_function = lambda x: x  # No cleaning for this example
    save_html_files(base_folder, base_filename, islmwy_page, extracted_html, extracted_texts, raw_html, html, clean_html_function)