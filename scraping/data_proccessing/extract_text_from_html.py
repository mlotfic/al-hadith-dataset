import re

# ✅ Function to extract text from HTML (removes tags)
def extract_text_from_html(html):
    """Removes HTML tags and returns clean text."""
    clean_text = re.sub(r"<.*?>", "", html)  # Remove all HTML tags
    return clean_text.strip()  # Remove extra spaces