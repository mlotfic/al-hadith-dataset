import os

from bs4 import BeautifulSoup, Comment


def to_html_append(hadith_id, h_wa_haddathana, container, islmwy_page, filename="./extracted_html/hadith_parsed.html"):
    """
    Append HTML content and a descriptive comment to an HTML file.
    
    This function appends a provided HTML container (BeautifulSoup Tag) along with a descriptive comment
    into an existing HTML file. If the file or necessary tags do not exist, they are created.
    
    Parameters:
    - hadith_id (int or str): The identifier for the hadith.
    - h_wa_haddathana (str): Additional identifier or content related to the hadith.
    - container (bs4.element.Tag): A BeautifulSoup Tag object containing the HTML content to append.
    - islmwy_page (int or str): The page number or identifier from the source.
    - filename (str): The file path to the HTML file where content will be appended.
                      Defaults to './extracted_html/hadith_parsed.html'.
    
    Returns:
    - None
    """

    # Create a comment containing metadata to be inserted before the container.
    comment_text = f'[-] This is islmwy-page-id: {islmwy_page}; hadith-id: {hadith_id}; h_wa_haddathana: {h_wa_haddathana} '
    comment = Comment(comment_text)

    # Check if the specified HTML file exists.
    if os.path.exists(filename):
        # File exists. Read and parse its existing content.
        with open(filename, 'r', encoding='utf-8') as file:
            existing_content = file.read()

        # Parse the existing HTML content using BeautifulSoup.
        existing_soup = BeautifulSoup(existing_content, 'html.parser')

        # Find the <body> tag in the existing content.
        body_tag = existing_soup.find('body')
        if not body_tag:
            # If there's no <body> tag, create one.
            body_tag = existing_soup.new_tag('body')
            if existing_soup.html:
                # If an <html> tag exists, append the new <body> to it.
                existing_soup.html.append(body_tag)
            else:
                # If there's no <html> tag, create one and append the <body> tag to it.
                html_tag = existing_soup.new_tag('html')
                existing_soup.append(html_tag)
                html_tag.append(body_tag)

        # Append the comment and container to the <body> tag.
        body_tag.append(comment)
        body_tag.append(container)

        # Write the updated HTML content back to the file.
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(existing_soup))

    else:
        # File does not exist. Create the necessary directory if it doesn't exist.
        dir_name = os.path.dirname(filename)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # Create a new BeautifulSoup object with <html> and <body> tags.
        html_tag = BeautifulSoup('<html></html>', 'html.parser')
        body_tag = html_tag.new_tag('body')
        html_tag.html.append(body_tag)

        # Append the comment and container to the new <body> tag.
        body_tag.append(comment)
        body_tag.append(container)

        # Write the new HTML content to the file.
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(html_tag))