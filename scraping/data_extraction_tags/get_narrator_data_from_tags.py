# hadith_meta_extractor.py

from typing import Dict, Optional

from bs4 import Tag

from ..data_proccessing.clean_text import clean_text
from ..data_proccessing.get_number_id import get_number_id
from ..data_proccessing.parse_query_params import parse_query_params


def get_narrator_data_from_tags(name_span: Tag, base_api: str) -> Optional[Dict[str, str]]:
    """
    Extracts metadata about a narrator from a given HTML element.

    Parameters:
    - name_span (Tag): A BeautifulSoup Tag object representing a <span> with class 'names'.
    - base_api (str): The base URL to prepend to relative URLs extracted from the HTML.

    Returns:
    - Optional[Dict[str, str]]: A dictionary containing narrator metadata if successful,
      or None if the necessary data could not be extracted.

    The returned dictionary has the following keys:
    - 'aliase': The name of the narrator (str).
    - 'narrators_id': The ID of the narrator extracted from the URL (str).
    - 'narrators_api': The relative API endpoint or URL fragment (str).
    - 'narrators_api_type': The type of API ('html' in this case) (str).
    - 'narrators_api_url': The full API URL constructed by combining base_api and the relative URL (str).

    The function performs the following steps:
    1. Checks if the provided Tag has the 'names' class.
    2. Extracts and cleans the narrator's name text.
    3. Finds the nested <span> with class 'namesatt' to extract the URL fragment.
    4. Parses the URL to extract the narrator's ID.
    5. Constructs the full API URL by combining base_api and the extracted URL fragment.
    6. Returns a dictionary containing all the extracted metadata.

    Note:
    - This function depends on external functions:
      - 'clean_text(text)' to clean and normalize the narrator's name.
      - 'parse_query_params(url)' to parse the URL and extract parameters.
    - Ensure that these functions are defined or imported in your code.
    """

    # Get the class attribute of the name_span safely (returns an empty list if not present)
    classes = name_span.get("class", [])

    if classes:
        if "names" not in classes:
            # The provided Tag does not have the required 'names' class
            return None
        else:
            # Found the person (narrator)
            # Extract and clean the narrator's name text
            text = name_span.text.strip()
            if text:
                # Clean the text (remove URL fragments, normalize whitespace)
                text = clean_text(text)
            else:
                # If text is empty after cleaning, return None
                return None

            # Extract the URL fragment from the nested <span> with class 'namesatt'
            namesatt_span = name_span.find('span', class_='namesatt')
            if namesatt_span:
                # Get the URL fragment or API endpoint
                namesatt = namesatt_span.text.strip()
                # Remove the nested <span> to prevent duplication or interference
                namesatt_span.decompose()
                # Parse the URL to extract parameters as a dictionary
                url_params = parse_query_params(namesatt)
                if url_params and 'ids' in url_params:
                    narrators_id = url_params['ids']
                else:
                    narrators_id = 'N/A'
                # Construct the full API URL
                url = base_api + namesatt
            else:
                # Unable to find the nested <span> with class 'namesatt'
                return None
    else:
        # The provided Tag does not have any classes
        return None
    
    ### **📌 Narrator (:narrator)**
    # Create narrator's metadat dictionary
    # Initialize narrator's metadata dictionary with the extracted values
    narrator: Dict[str, str] = {
        "_id"                   : narrators_id,   # Extracted ID from the URL parameters
        "aliase"                : text,           # Cleaned name of the narrator        
        "narrators_api"         : namesatt,       # Relative API endpoint or URL fragment
        "narrators_api_type"    : "html",         # Type of API (hardcoded as 'html')
        "narrators_api_url"     : url             # Full API URL constructed from base_api and namesatt
    }
    
    return narrator

'''
# trgmahadith json response class="namesatt" = "nindex.php?page=showalam&amp;ids=12070"
# {'page': 'showalam', 'ids': '12070'}
url = "nindex.php?page=showalam&ids=12070"
parse_query_params(url)
url = get_trgma_hadith_url(url)
, tag="span", tag_class="names", url_class = "namesatt"

'''