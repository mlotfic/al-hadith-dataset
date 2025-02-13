from typing import Optional

from bs4 import BeautifulSoup, Tag


def get_author(soup: BeautifulSoup) -> str:
    """
    Extract author information from the HTML content.
    
    Parameters
    ----------
    soup : BeautifulSoup
        Parsed HTML content containing author information
    
    Returns
    -------
    str
        Author name if found, 'N/A' otherwise
    
    Examples
    --------
    >>> soup = BeautifulSoup('<h4 class="txt-secondary">John Doe</h4>', 'html.parser')
    >>> author = extract_author(soup)
    >>> print(author)
    'John Doe'
    """
    
    #
    h4 = soup.find('h4', class_='txt-secondary')
    author = h4.get_text()  if h4 else 'N/A'
    
    return author