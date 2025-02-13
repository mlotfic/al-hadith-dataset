import requests
from bs4 import BeautifulSoup


def get_tkhreg_hadith_api(islmwy_page, base_url, api_url):
    """
    Fetch and process Hadith data from the specified Islamweb API to produce a structured output.

    Args:
        islmwy_page (str): The value representing the `LINKID` used in the API URL.
        base_url (str): The base URL of the Islamweb website.
        api_url (str): The full API URL to fetch data from.

    Returns:
        list: A list of dictionaries containing the processed Hadith data.

    The function fetches data from the provided `api_url`, processes the JSON response,
    and extracts specific fields to create a list of dictionaries containing the required information.
    It parses HTML content to extract additional URLs and makes subsequent requests to retrieve more data.
    """
    # Fetch the data from the API
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    data = response.json()  # Parse the JSON response

    # Initialize an empty list to store the output data
    output_sequence = []

    # Iterate over each book item in the data
    for book_item in data:
        xref_book_name = book_item.get('bookname')  # Get the book name
        xref_book_id = book_item.get('id')          # Get the book ID

        # Iterate over each detail in the book's details
        for detail in book_item.get('details', []):
            xref_islmwy_page = detail.get('source_id')          # Get the source ID
            xref_hadith_book_name = detail.get('bookname')      # Get the Hadith book name
            xref_hadith_id = detail.get('bookhad')              # Get the Hadith ID
            xref_hadith_href = detail.get('href')               # Get the href containing HTML

            # Parse the HTML in xref_hadith_href to extract the data-url attribute
            soup = BeautifulSoup(xref_hadith_href, 'html.parser')
            a_tag = soup.find('a', class_='hadithTak')
            xref_hadith_api = a_tag.get('data-url') if a_tag else None  # Extract data-url

            # Construct the full URL by combining the base URL and the data-url
            xref_hadith_full_url = base_url + xref_hadith_api if xref_hadith_api else None

            # Make a request to the full URL to get the response content
            if xref_hadith_full_url:
                hadith_response = requests.get(xref_hadith_full_url)
                hadith_response.raise_for_status()
                xref_hadith_url_content = hadith_response.text  # Get the response content
            else:
                xref_hadith_url_content = None

            # Construct the output dictionary
            output_item = {
                "islmwy_page": islmwy_page,
                "xref_book_name": xref_book_name,
                "xref_book_id": xref_book_id,
                "xref_islmwy_page": xref_islmwy_page,
                "xref_hadith_book_name": xref_hadith_book_name,
                "xref_hadith_id": xref_hadith_id,
                "xref_hadith_href": xref_hadith_href,
                "xref_hadith_api": xref_hadith_api,
                "xref_hadith_url": xref_hadith_url_content,
            }

            # Append the output item to the sequence
            output_sequence.append(output_item)

    # Return the list of processed Hadith data
    return output_sequence