"""
@file: tar_archiver.py
@description: This module provides functionality to create and manage tar.gz archives.
"""

import sys
import os
import tarfile
import shutil
import json
import tempfile
from typing import Optional, Literal, List, Dict, Union

# Adjust the import path to correctly import from the parent directory

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the Python path
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from functions._data_proccessing.bytes_to_human_readable import bytes_to_human_readable

class TarGzArchiver:
    def __init__(self, archive_path: str):
        """
        Initialize the TarGzArchiver with an archive path.
        
        Args:
            archive_path (str): Path to the tar.gz archive
        """
        self.archive_path = os.path.abspath(archive_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.archive_path) or '.', exist_ok=True)

    def append_file(
        self, 
        file_path: str, 
        arcname: Optional[str] = None, 
        mode: Literal['append', 'replace', 'skip'] = 'append'
    ) -> bool:
        """
        Append a file to the tar.gz archive with different handling modes.
        
        Args:
            file_path (str): Path to the file to be added
            arcname (Optional[str]): Custom name within the archive (optional)
            mode (str): Handling mode for existing files
                - 'append': Add file, allowing duplicates
                - 'replace': Replace existing file with the same name
                - 'skip': Skip if file already exists
        
        Returns:
            bool: True if file was successfully added, False otherwise
        """
        # Validate input file
        if not os.path.exists(file_path):
            print(f"Error: Source file {file_path} does not exist.")
            return False

        # Determine archive name
        if arcname is None:
            arcname = os.path.basename(file_path)
            
        # Determine tar mode and handle different scenarios
        if (not os.path.exists(self.archive_path)) or (mode == 'replace'):
            # Create new archive
            tar_mode = 'w:gz'
        
        # Handle skip mode
        elif mode == 'skip':
            print(f"File {arcname} already exists. Skipping.")
            return False
        
        else:
            tar_mode == 'a:gz'
        

        # Create a temporary directory for safe file manipulation
        with tempfile.TemporaryDirectory() as temp_dir:
            # Temporary archive path
            temp_archive = os.path.join(temp_dir, 'temp_archive.tar.gz')

            try:
                # Determine if file exists in current archive
                file_exists = False
                if os.path.exists(self.archive_path):
                    with tarfile.open(self.archive_path, 'r:gz') as existing_tar:
                        file_exists = arcname in existing_tar.getnames()


                # Open tar file in the appropriate mode
                with tarfile.open(temp_archive, tar_mode) as tar:
                    # If appending to existing archive, copy existing files
                    if tar_mode == 'a:gz' and os.path.exists(self.archive_path):
                        with tarfile.open(self.archive_path, 'r:gz') as existing_tar:
                            for member in existing_tar.getmembers():
                                if member.name != arcname:
                                    file_obj = existing_tar.extractfile(member)
                                    if file_obj:
                                        tar.addfile(member, file_obj)

                    # Add the new file
                    tar.add(file_path, arcname=arcname)

                # Replace the original archive
                shutil.copy2(temp_archive, self.archive_path)

                print(f"File {arcname} {'replaced' if mode == 'replace' else 'added'} successfully.")
                return True

            except Exception as e:
                print(f"Unexpected error appending file: {e}")
                # Additional debugging information
                import traceback
                traceback.print_exc()
                return False

    def _remove_file_from_archive(self, filename: str):
        """
        Remove a specific file from the tar.gz archive.
        
        Args:
            filename (str): Name of the file to remove
        """
        # Create a temporary archive
        temp_archive = self.archive_path + '.temp'
        
        try:
            with tarfile.open(self.archive_path, 'r:gz') as src_tar:
                with tarfile.open(temp_archive, 'w:gz') as dest_tar:
                    for member in src_tar.getmembers():
                        if member.name != filename:
                            file_obj = src_tar.extractfile(member)
                            if file_obj:
                                dest_tar.addfile(member, file_obj)

            # Replace the original archive with the temporary one
            shutil.move(temp_archive, self.archive_path)
            print(f"Removed {filename} from archive.")
        
        except Exception as e:
            print(f"Error removing file from archive: {e}")
            if os.path.exists(temp_archive):
                os.remove(temp_archive)

    def list_files(self) -> list:
        """
        List all files in the tar.gz archive.
        
        Returns:
            list: List of filenames in the archive
        """
        try:
            with tarfile.open(self.archive_path, 'r:gz') as tar:
                return tar.getnames()
        except FileNotFoundError:
            print(f"Archive {self.archive_path} not found.")
            return []
        except tarfile.TarError as e:
            print(f"Error reading archive: {e}")
            return []

    def extract_file(self, filename: str, extract_path: Optional[str] = None):
        """
        Extract a specific file from the archive.
        
        Args:
            filename (str): Name of the file to extract
            extract_path (Optional[str]): Destination path for extraction
        """
        try:
            with tarfile.open(self.archive_path, 'r:gz') as tar:
                if filename not in tar.getnames():
                    print(f"File {filename} not found in archive.")
                    return False

                if extract_path:
                    os.makedirs(extract_path, exist_ok=True)
                    tar.extract(filename, path=extract_path)
                else:
                    tar.extract(filename)
                
                print(f"Extracted {filename} successfully.")
                return True
        
        except Exception as e:
            print(f"Error extracting file: {e}")
            return False
        
    def get_archive_size(self):
        """
        Get the total size of a tar.gz file using os module.
        
        Returns:
            dict: File size information
        """
        try:
            # Check if file exists before getting size
            if not os.path.exists(self.archive_path):
                print(f"Error: Archive {self.archive_path} not found.")
                return None
            
            file_size = os.path.getsize(self.archive_path)
            
            return {
                'size_bytes': file_size,
                'size_readable': bytes_to_human_readable(file_size)  # Assuming bytes_to_human_readable is correctly imported
            }
        except Exception as e:
            print(f"Error getting archive size: {e}")
            return None
        
    def get_file_info(self, filename: str) -> Dict[str, Union[str, int]]:
        """
        Get detailed information about a specific file in the archive.
        
        Args:
            filename (str): Name of the file to get info for
        
        Returns:
            Dict with file information or None if file not found
        """
        try:
            with tarfile.open(self.archive_path, 'r:gz') as tar:
                file_info = tar.getmember(filename)
                return {
                    'name': file_info.name,
                    'size': file_info.size,
                    'size_readable': bytes_to_human_readable(file_info.size),
                    'modified': file_info.mtime,
                    'mode': file_info.mode
                }
        except KeyError:
            print(f"File {filename} not found in archive.")
            return None
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None

    def extract_all(self, extract_path: Optional[str] = None):
        """
        Extract all files from the archive.
        
        Args:
            extract_path (Optional[str]): Destination path for extraction
        
        Returns:
            List of extracted file paths
        """
        if extract_path is None:
            extract_path = os.getcwd()
        
        os.makedirs(extract_path, exist_ok=True)
        
        try:
            with tarfile.open(self.archive_path, 'r:gz') as tar:
                extracted_files = []
                tar.extractall(path=extract_path)
                
                for member in tar.getmembers():
                    if member.isfile():
                        extracted_files.append(os.path.join(extract_path, member.name))
                
                print(f"Extracted {len(extracted_files)} files to {extract_path}")
                return extracted_files
        
        except Exception as e:
            print(f"Error extracting all files: {e}")
            return []

    def add_json_data(
        self, 
        data: Union[Dict, List], 
        filename: str = 'data.json', 
        mode: Literal['append', 'replace', 'skip'] = 'append'
    ) -> bool:
        """
        Add JSON data to the archive.
        
        Args:
            data (Union[Dict, List]): JSON serializable data
            filename (str): Filename in the archive
            mode (str): Handling mode for existing files
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create a temporary JSON file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                json.dump(data, temp_file, ensure_ascii=False, indent=2)
                temp_file_path = temp_file.name
            
            # Use existing append_file method
            result = self.append_file(temp_file_path, arcname=filename, mode=mode)
            
            # Remove temporary file
            os.unlink(temp_file_path)
            
            return result
        
        except Exception as e:
            print(f"Error adding JSON data: {e}")
            return False

    def read_json_file(self, filename: str) -> Union[Dict, List, None]:
        """
        Read a JSON file from the archive.
        
        Args:
            filename (str): Name of the JSON file in the archive
        
        Returns:
            Parsed JSON data or None if error
        """
        try:
            with tarfile.open(self.archive_path, 'r:gz') as tar:
                file_obj = tar.extractfile(filename)
                if file_obj:
                    return json.load(file_obj)
                else:
                    print(f"File {filename} not found in archive.")
                    return None
        
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filename}")
            return None
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return None

    def archive_summary(self) -> Dict[str, Union[int, str, List]]:
        """
        Generate a comprehensive summary of the archive.
        
        Returns:
            Dictionary with archive details
        """
        try:
            with tarfile.open(self.archive_path, 'r:gz') as tar:
                members = tar.getmembers()
                
                # Filter files and directories
                files = [m for m in members if m.isfile()]
                dirs = [m for m in members if m.isdir()]
                
                # Calculate total size
                total_size = sum(f.size for f in files)
                
                return {
                    'total_files': len(files),
                    'total_directories': len(dirs),
                    'total_size': bytes_to_human_readable(total_size),
                    'total_size_bytes': total_size,
                    'file_list': [f.name for f in files],
                    'directory_list': [d.name for d in dirs]
                }
        
        except Exception as e:
            print(f"Error generating archive summary: {e}")
            return {}

    

# Example usage
def main():
    # Create an archiver instance
    archiver = TarGzArchiver('example.tar.gz')

    # Append files with different modes
    archiver.append_file('/path/to/file1.txt')  # Default append mode
    archiver.append_file('/path/to/file2.txt', arcname='custom_name.txt')
    archiver.append_file('/path/to/file3.txt', mode='replace')
    archiver.append_file('/path/to/file4.txt', mode='skip')

    # List files in the archive
    files = archiver.list_files()
    print("Files in archive:", files)

    # Extract a specific file
    archiver.extract_file('custom_name.txt', extract_path='./extracted')

if __name__ == "__main__":
    main()