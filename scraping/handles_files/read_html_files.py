import os

def read_html_files(base_folder, base_filename, islmwy_page):
    """
    Reads different versions of saved HTML content from specified directories.
    
    Parameters:
    - base_folder (str)    : The base directory where files are stored.
    - base_filename (str)  : The base name for the files.
    - islmwy_page (int or str) : The current page number to format.

    Returns:
    - A dictionary containing file content for each type of stored HTML.
    """
    page_formatted = f"{int(islmwy_page):04d}"
    
    file_paths = {
        "modal_raw": os.path.join(base_folder, "raw/modal/", f"{base_filename}-modal-{page_formatted}.html"),
        "modal_clean": os.path.join(base_folder, "raw/modal_clean/", f"{base_filename}-modal-clean-{page_formatted}.html"),
        "raw_html": os.path.join(base_folder, "raw/html/", f"{base_filename}-{page_formatted}.html"),
        "clean_html": os.path.join(base_folder, "raw/html_clean/", f"{base_filename}-clean-{page_formatted}.html"),
    }
    
    file_contents = {}
    
    for key, path in file_paths.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                file_contents[key] = file.read()
        else:
            file_contents[key] = None  # Indicate missing files
    
    return file_contents
