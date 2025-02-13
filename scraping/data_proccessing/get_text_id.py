import hashlib
import os
from typing import Tuple, Optional

from .normalize_arabic_text import normalize_arabic_text

def get_text_id(text: str, base_filename: str, pickle_file: str = "chapters", hash_algorithm: str = 'md5', max_normal_id_length: int = 100) -> Tuple[str, str, str]:
    """
    Enhanced version of get_text_id with additional features.
    
    Parameters:
    -----------
    text : str
        The Arabic text to process
    base_filename : str
        Base directory/file name for storage
    pickle_file : str, optional
        Name of the pickle file (default is "chapters")
    hash_algorithm : str, optional
        Hash algorithm to use ('md5', 'sha1', 'sha256')
    max_normal_id_length : int, optional
        Maximum length for normal_id
        
    Returns:
    --------
    Tuple[str, str, str]
        - file_path: Path to pickle file
        - normal_id: Normalized text ID
        - hash_id: Hash of original text
    """
    try:
        # Validate inputs
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        if not base_filename or not base_filename.strip():
            raise ValueError("Base filename cannot be empty")
            
        # Clean inputs
        text = text.strip()
        base_filename = base_filename.strip()
        pickle_file   = pickle_file.strip()
        
        # Generate file path
        file_path = os.path.join("extracted_data", base_filename, "db", f"{pickle_file}.pkl")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Normalize text and create normal_id
        normalized_text = normalize_arabic_text(text)
        
        # Truncate normalized text if too long
        if len(normalized_text) > max_normal_id_length:
            normalized_text = normalized_text[:max_normal_id_length]
        
        # Create normal_id
        normal_id = f"{base_filename}-{normalized_text}"
        
                # Generate hash based on selected algorithm
        if hash_algorithm == 'md5':
            hash_id = hashlib.md5(text.encode('utf-8')).hexdigest()
        elif hash_algorithm == 'sha1':
            hash_id = hashlib.sha1(text.encode('utf-8')).hexdigest()
        elif hash_algorithm == 'sha256':
            hash_id = hashlib.sha256(text.encode('utf-8')).hexdigest()
        else:
            raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
        
        return file_path, normal_id, hash_id
        
    except Exception as e:
        print(f"Error in get_text_id: {str(e)}")
        raise

# Example usage:
if __name__ == "__main__":
    # Test text
    text = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"
    base_filename = "quran"
    
    try:
        # Basic version
        file_path, normal_id, md5_hash = get_text_id(text, base_filename)
        print("\nBasic version results:")
        print(f"File path: {file_path}")
        print(f"Normal ID: {normal_id}")
        print(f"MD5 hash: {md5_hash}")
        
        # Enhanced version
        file_path, normal_id, hash_id = get_text_id(
            text=text,
            base_filename=base_filename,
            pickle_file="chapters",
            hash_algorithm='sha256',
            max_normal_id_length=50
        )
        print("\nEnhanced version results:")
        print(f"File path: {file_path}")
        print(f"Normal ID: {normal_id}")
        print(f"Hash: {hash_id}")
        
    except Exception as e:
        print(f"Error: {e}")