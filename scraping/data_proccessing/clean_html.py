# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:41:18 2025

@author: User
"""

import logging
import time
import re

def clean_html(html):
    """
    Removes <script> and <style> tags along with their content.
    Also removes inline JavaScript events if needed and extra newlines.
    """
    # Remove <script> and <style> tags with content
    
    html = re.sub(r"<head>[\s\S]*?</head>", "", html, flags=re.DOTALL)
    html = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style.*?</style>", "", html, flags=re.DOTALL)
    
    # Remove extra newlines and spaces
    html = re.sub(r"\n\s*\n", "\n", html)  # Remove extra empty lines
    html = re.sub(r"\s{2,}", " ", html)    # Remove multiple spaces
    html = html.strip()  # Strip leading/trailing spaces
    return html

if __name__ == "__main__":
    # ✅ Example Usage
    raw_html = """
    <html>
    <head>
    <style>
        body { background-color: black; }
    </style>
    </head>
    <body>
    <h1>Hello</h1>
    <script>
        alert('This should be removed');
    </script>
    <button onclick="alert('Click')">Click Me</button>
    </body>
    </html>
    """

    cleaned_html = clean_html(raw_html)
    print(cleaned_html)