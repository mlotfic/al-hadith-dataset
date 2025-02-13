# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:11:07 2025

@author: m.lotfi

Package/module description goes here.
This file initializes the package and defines what should be exposed to users.
"""

# Version information
__version__ = '0.1.0'
__author__ = 'Your Name'
__author_email__ = 'your.email@example.com'

# Import commonly used modules/components to make them available at package level
from .data_extraction_tags import get_author
from .data_extraction_tags import get_chapters_tree
from .data_extraction_tags import get_hadith_base_info
from .data_extraction_tags import get_hadith_info
from .data_extraction_tags import get_hadith_info_thaskeel
from .data_extraction_tags import get_hadith_narrators
from .data_extraction_tags import get_page_navigation
from .data_extraction_tags import get_page_volume
from .data_extraction_tags import get_tkhreg_hadith_api
from .data_extraction_tags import get_toc_path
from .data_extraction_tags import get_narrator_data_from_tags
from .data_extraction_tags import json_normalize_tkhreg_hadith_response

from .data_proccessing import bytes_to_human_readable
from .data_proccessing import clean_text
from .data_proccessing import find_common_columns
from .data_proccessing import extract_number_before_haddathana
from .data_proccessing import extract_text_from_html
from .data_proccessing import get_h_wa_haddathana_count_occurrences
from .data_proccessing import get_url_components
from .data_proccessing import clean_html
from .data_proccessing import remove_diacritics_and_spaces
from .data_proccessing import remove_diacritics_spaces_and_normalize_numbers
from .data_proccessing import divide_pages_into_parts
from .data_proccessing import parse_query_params
from .data_proccessing import extract_ayat_info
from .data_proccessing import normalize_arabic_text
from .data_proccessing import get_text_id
from .data_proccessing import get_number_id
from .data_proccessing import get_narrators_chain_id


from .handles_files import to_json_csv
from .handles_files import to_csv_pd
from .handles_files import to_html_append
from .handles_files import to_json_with_arabic
from .handles_files import save_html_files
from .handles_files import convert_to_serializable
from .handles_files import is_files_saved
from .handles_files import read_html_files
from .handles_files import update_csv
from .handles_files import load_data_as_dict
from .handles_files import get_matching_dict
from .handles_files import save_data_from_dict
from .handles_files import update_pickle_dict
from .handles_files import update_chapters
from .handles_files import update_narrators
from .handles_files import update_ayat
from .handles_files import update_tree_subject
from .handles_files import update_main_subject


from .html_proccessing import parse_hadith_page
from .html_proccessing import parse_hadith_isnad

# ğŸ“Œ **time_date**
from .time_date  import generate_random_delay_gauss


from .web_automation import handle_modal_interaction
from .web_automation import get_driver
from .web_automation import try_open_modal_js
from .web_automation import try_open_modal
from .web_automation import get_api_response
from .web_automation import is_modal_open
from .web_automation import try_close_modal_js
from .web_automation import create_human_like_browser
from .web_automation import simulate_human_scroll
from .web_automation import simulate_human_typing
from .web_automation import move_mouse_randomly
from .web_automation import is_modal_open
from .web_automation import move_mouse_randomly
from .web_automation import simulate_human_scroll
from .web_automation import simulate_human_typing
from .web_automation import scrape_pages
from .web_automation import fetch_api_data






