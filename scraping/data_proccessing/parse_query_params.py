from urllib.parse import parse_qs
from typing import Dict, List

def parse_query_params(input_str: str) -> Dict[str, str]:
    """
    Parse query parameters from a URL string, handling HTML entity encoding.

    This function does the following:
    1. Replaces HTML entity '&amp;' with '&'
    2. Extracts the query string part
    3. Parses the query parameters into a dictionary
    4. Returns a dictionary of all query parameters

    Args:
        input_str (str): The input URL string containing query parameters

    Returns:
        Dict[str, List[str]]: A dictionary with all parsed query parameters
    """
    try:
        # Replace HTML entity '&amp;' with '&'
        cleaned_str = input_str.replace('&amp;', '&')

        # Extract the query string part (after '?')
        query_string = cleaned_str.split('?', 1)[1]

        # Parse the query parameters into a dictionary
        params = parse_qs(query_string)
        
        # Convert to Dict[str, str] by taking first value of each list    
        return {key: values[0] if values else '' for key, values in params.items()}
    
    except IndexError:
        # Handle cases where there's no '?' in the input string
        return {}
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An error occurred: {e}")
        return {}

# Example usage
if __name__ == "__main__":
    input_str = "nindex.php?id=2336&amp;treeLevel=2&amp;bookid=0&amp;page=bookssubtree"
    result = parse_query_params(input_str)
    print(result)
    
    # Accessing specific parameters
    print("ID:", result.get('id', [''])[0])
    print("Tree Level:", result.get('treeLevel', [''])[0])