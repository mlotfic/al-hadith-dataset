import os

def is_files_saved(base_folder, base_filename, islmwy_page):
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
        return True
    else:
        # At least one file does not exist, overwrite all files
        print("Not All files exist.")
        return None