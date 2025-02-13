
import codecs
import json
import os
from datetime import datetime

from .convert_to_serializable import convert_to_serializable

def to_json_with_arabic(data, filename, base_filename, islmwy_page, raw=None, **kwargs):
    """
    Save dictionary/list with comprehensive Arabic text and complex object support
    
    Parameters:
    - data: Dictionary or list to save
    - filename: Custom filename (optional)
    - base_path: Directory to save JSON (optional)
    - **kwargs: Additional JSON dump parameters
    
    Returns:
    - Full path of saved JSON file
    """
    if raw:
        filepath = f"./extracted_data/{base_filename}/raw/json/{filename}-{format(int(islmwy_page), '04d')}.json"
    else:
        filepath = f"./extracted_data/{base_filename}/json/{filename}-{format(int(islmwy_page), '04d')}.json"
    
    # Check if the specified HTML file exists.
    if os.path.exists(filepath):
        print(f"The file '{filename}' exists.")
        # File exists. Return None.
        return None
    else:
        # File does not exist. Create the necessary directory if it doesn't exist.
        dir_name = os.path.dirname(filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        # Preprocess data to make it JSON serializable
        try:
            serializable_data = convert_to_serializable(data)
        except Exception as conversion_error:
            print(f"Data conversion error: {conversion_error}")
            serializable_data = str(data)
        
        # Default JSON saving configurations
        default_config = {
            'ensure_ascii': False,  # Critical for Arabic text
            'indent': 4,            # Readable formatting
            'sort_keys': False      # Preserve original order
        }
        
        # Merge default config with user-provided kwargs
        json_config = {**default_config, **kwargs}
        
        try:
            # Method 1: Using codecs (Recommended for Arabic)
            with codecs.open(filepath, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, **json_config)
            
            print(f"JSON saved successfully: {filepath}")
            return filepath
        
        except Exception as e:
            print(f"Error saving JSON: {e}")
            
            # Fallback method
            try:
                # Method 2: Standard JSON dump with UTF-8
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(serializable_data, f, **json_config)
                
                print(f"Fallback JSON save successful: {filepath}")
                return filepath
            
            except Exception as fallback_error:
                print(f"Fallback JSON save failed: {fallback_error}")
        
        return None
'''
# Example Usage Scenarios

# 1. Basic Dictionary Saving
arabic_dict = {
    "title": "حديث نبوي",
    "content": "الحمد لله رب العالمين"
}
to_json_with_arabic(arabic_dict, filename='arabic_data.json')

# 2. Complex Nested Dictionary
complex_arabic_data = {
    "book": {
        "name": "صحيح البخاري",
        "chapters": [
            {
                "chapter_name": "باب بدء الوحي",
                "hadiths": [
                    {
                        "text": "إقرأ باسم ربك الذي خلق",
                        "narrator": "عائشة رضي الله عنها"
                    }
                ]
            }
        ]
    }
}
to_json_with_arabic(
    complex_arabic_data, 
    filename='complex_arabic_data.json',
    base_path='./data/json_files/'
)

# 3. Advanced Saving with Preprocessing
def preprocess_arabic_data(data):
    """
    Preprocess data before saving
    - Clean text
    - Handle special characters
    """
    def clean_text(text):
        if isinstance(text, str):
            # Remove extra whitespaces
            text = ' '.join(text.split())
            
            # Optional: Normalize Arabic text
            try:
                import unicodedata
                text = unicodedata.normalize('NFKD', text)
            except ImportError:
                pass
        
        return text
    
    # Recursively clean dictionary/list
    def deep_clean(obj):
        if isinstance(obj, dict):
            return {k: deep_clean(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [deep_clean(item) for item in obj]
        elif isinstance(obj, str):
            return clean_text(obj)
        return obj
    
    return deep_clean(data)

# Usage with preprocessing
preprocessed_data = preprocess_arabic_data(complex_arabic_data)
to_json_with_arabic(
    preprocessed_data, 
    filename='preprocessed_arabic_data.json'
)

# 4. Logging and Tracking
def save_with_logging(data, identifier):
    """Save JSON with detailed logging"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'identifier': identifier,
        'data_type': type(data).__name__,
        'data_length': len(str(data))
    }
    
    # Save JSON
    json_path = to_json_with_arabic(
        data, 
        filename=f'{identifier}_data.json'
    )
    
    # Optional: Log to separate file
    to_json_with_arabic(
        log_entry, 
        filename='json_save_log.json', 
        mode='a'
    )
    
    return json_path

# 5. Error Handling and Validation
def safe_save_json(data, filename):
    """
    Comprehensive JSON saving with validation
    """
    try:
        # Validate data
        if not data:
            print("Warning: Empty data")
            return None
        
        # Type checking
        if not isinstance(data, (dict, list)):
            print("Error: Unsupported data type")
            return None
        
        # Size limitation (optional)
        data_size = len(str(data))
        if data_size > 10_000_000:  # 10 MB limit
            print("Warning: Large data file")
        
        # Save with custom filename
        return to_json_with_arabic(
            data, 
            filename=filename,
            base_path='./data/validated_json/'
        )
    
    except Exception as e:
        print(f"Save failed: {e}")
        return None

# Recommended Usage
if __name__ == "__main__":
    # Basic save
    to_json_with_arabic(
        complex_arabic_data, 
        filename='hadith_data.json'
    )

'''
