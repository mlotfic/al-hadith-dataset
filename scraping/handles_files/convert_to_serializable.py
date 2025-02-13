import codecs
import json
import os
from datetime import datetime

def convert_to_serializable(obj):
    """
    Recursively convert BeautifulSoup Tags and complex objects to serializable format
    
    Strategies:
    1. Convert BeautifulSoup Tags to text
    2. Handle datetime objects
    3. Convert complex objects to strings
    4. Recursively process nested structures
    """
    if hasattr(obj, 'get_text'):
        # BeautifulSoup Tag conversion
        return obj.get_text()
    elif isinstance(obj, datetime):
        # Datetime serialization
        return obj.isoformat()
    elif isinstance(obj, dict):
        # Recursively process dictionary
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # Recursively process list
        return [convert_to_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        # Convert object with __dict__ to dictionary
        return convert_to_serializable(obj.__dict__)
    else:
        # Try to serialize, if fails convert to string
        try:
            json.dumps(obj)
            return obj
        except TypeError:
            return str(obj)
