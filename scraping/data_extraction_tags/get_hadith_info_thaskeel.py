# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 23:17:29 2025

@author: m.lotfi
"""

import re
import pandas as pd
from bs4 import BeautifulSoup

def get_hadith_info_thaskeel(soup, islmwy_page):
    """
    Extract details from the page content div
    
    Args:
        soup (BeautifulSoup): Parsed HTML content
    
    Returns:
        dict: Extracted page content details
    """
    
    hadith_info_thaskeel = {
        "islmwy_page" : islmwy_page,
        "html_hadith_narrators"   : 'N/A',
        "text_hadith_narrators"   : 'N/A',
        "hashiya_title"           : 'N/A',
        'narrators_chains'        : 'N/A',
        'hadith_content'          : 'N/A',
        'hadith_content_url'      : 'N/A',
        'hadith_subject'          : [],
        'quran_verses'            : [],
        'narrators'               : []
        
    }
    
    # Find the main content div
    container = soup.find('div', class_='bookcontent-dic', id='pagebody_thaskeel')
    
    # Extract html_hadith
    hadith_info_thaskeel['html_hadith_narrators'] = container
    
    if container:
        # [-] -----------------------------------------------------------------
        # Extract Hashiya Title
        hashiya_span = container.find('span', class_='hashiya_title')
        if hashiya_span:
            hadith_info_thaskeel['hashiya_title'] = hashiya_span.next_sibling.strip()
        
        # [-] -----------------------------------------------------------------
        # Extract text hadith + narra (clean)        
        # Remove URL fragment
        text_hadith = re.sub(r'nindex\.php\?page=tafseer&surano=[\d]*&ayano=[\d]*', '', container.text.strip())
        # Remove extra spaces and tabs
        hadith_info_thaskeel['text_hadith_narrators'] = re.sub(r'\s+', ' ', text_hadith).strip()
        
        # [-] -----------------------------------------------------------------
        # Extract Hadith Subject from first Quran link
        first_quran_link = container.find('a', onclick=True)
        if first_quran_link:
            subject = re.search(r"TITLE, '([^']+)'", first_quran_link['onclick'])
            if subject:
                hadith_info_thaskeel['hadith_subject'].append({
                    "hadith_subject": subject.group(1),
                    "url"           : first_quran_link.find('span', class_='quranatt').text.strip() if first_quran_link else 'N/A',
                })
        
        # [-] -----------------------------------------------------------------
        # Extract main Hadith content
        hadith_span = container.find('span', class_='hadith')
        
        if hadith_span:
            # Clean up tags and attributes
            hadith_text = hadith_span.get_text(separator=' ', strip=True)
            # Remove URL fragment
            hadith_text = re.sub(r'nindex\.php\?page=tafseer&surano=[\d]*&ayano=[\d]*', '', hadith_text)         
            # Remove extra spaces and tabs
            hadith_info_thaskeel['hadith_content'] = re.sub(r'\s+', ' ', hadith_text).strip()
            hadith_info_thaskeel['hadith_content_url'] = hadith_span.find('span', class_='hadithatt').text.strip() if hadith_span else 'N/A'
        
        # [-] -----------------------------------------------------------------
        # Extract Quran text and link
        # Regex pattern to extract verse and href
        pattern = r'<span class="quranatt"[^>]*>([^<]+)</span>([^<]+)'       
        verse_spans = container.find_all('span', class_='quran')
        for span in verse_spans:
            # Convert span to string
            span_str = str(span)
            
            # Find matches in the string
            matches = re.findall(pattern, span_str)
            
            if matches:
                for href, verse in matches:
                    hadith_info_thaskeel['quran_verses'].append({
                        'verse'     : verse.strip(),
                        'verse_href': href.strip()
                    })
                    
        # [-] -----------------------------------------------------------------
        # Extract main Hadith narrators_chains
        pattern = r'<span class="hashiya_title">[^<]*</span>(.*?)<span class="hadith"'
        match = re.search(pattern, str(container), re.DOTALL)
        if match:
            narrators_chains = str(match.group(1).strip())                  
            hadith_info_thaskeel['narrators_chains'] = narrators_chains
        else:
            narrators_chains = '<div></div>'
            
        # Parse the HTML content
        narrators_chains = BeautifulSoup(narrators_chains, 'html.parser')
             
        # Find all span tags with class 'names'
        name_spans = narrators_chains.find_all('span', class_='names')           

        for i, name_span in enumerate(name_spans):
            #print(i)
            
            # Get the text before this span
            text_before = ''
            if name_span.previous_sibling and not isinstance(name_span.previous_sibling, str):
                text_before = name_span.previous_sibling.text.strip() if name_span.previous_sibling else ''
            elif name_span.previous_sibling:
                text_before = name_span.previous_sibling.strip()
            
            # Get the text after this span
            text_after = ''
            if name_span.next_sibling and not isinstance(name_span.next_sibling, str):
                text_after = name_span.next_sibling.text.strip() if name_span.next_sibling else ''
            elif name_span.next_sibling:
                text_after = name_span.next_sibling.strip()
           
            # Extract the URL from the nested span with class 'namesatt'
            namesatt_span = name_span.find('span', class_='namesatt')
            if namesatt_span:
                url = namesatt_span.text.strip() if namesatt_span else 'N/A'                        
                namesatt_span.decompose()
                # print(url)
            
            # Extract the name
            name = name_span.text.strip()         

            # Append the extracted data to the narrators list
            hadith_info_thaskeel['narrators'].append({
                'name'   : name,
                'url'    : url,
                "before" : text_before,           
                "after"  : text_after
            })   
    return hadith_info_thaskeel              
            