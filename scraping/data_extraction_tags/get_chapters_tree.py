# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 23:17:29 2025

@author: m.lotfi
"""

import re
from typing import Any, Dict, List

import pandas as pd
from bs4 import BeautifulSoup, Tag


def determine_tree_level(row: pd.Series) -> str:
    """
    Determine the hierarchical level of a given row in the chapter tree.
    
    Parameters
    ----------
    row : pd.Series
        A pandas Series containing the row data with chapter hierarchy information
    
    Returns
    -------
    str
        The determined tree level:
        - 'grand_child': Lowest level in hierarchy (individual chapters)
        - 'child': Second-level nodes (book parts)
        - 'first': First-level nodes (main book sections)
        - 'main': Root level of the tree
    """
    if not pd.isna(row.get('hadith_chapter_id', "")):
        return 'grand_child'
    elif not pd.isna(row.get('li_children_data_id', "")):
        return 'child'
    elif not pd.isna(row.get('input_first_level_data_id', "")):
        return 'first'
    return 'main'


def get_chapters_tree(soup: BeautifulSoup, islmwy_page: str) -> pd.DataFrame:
    """
    Extract hierarchical chapter data from a BeautifulSoup parsed HTML page and convert it to a DataFrame.
    
    This function processes HTML content to extract a tree structure of chapters and their metadata,
    including main level, first level, children level, and grand children level information.
    
    Parameters
    ----------
    soup : BeautifulSoup
        Parsed HTML content containing the chapter hierarchy
    islmwy_page : str
        Identifier or URL of the Islamic way page being processed
    
    Returns
    -------
    pd.DataFrame
        A DataFrame containing hierarchical chapter data with columns including:
        - Basic identifiers (islmwy_page, hidden_input_main_data_*)
        - First level data (input_first_level_*, hadith_book_name_*)
        - Children level data (li_children_*, label_children_*)
        - Grand children level data (hidden_input_grand_children_*, hadith_chapter_*)
        - tree_level: Indicates hierarchy level ('main', 'first', 'child', 'grand_child')
    
    Notes
    -----
    The function processes four levels of hierarchy:
    1. Main level (ul.tree)
    2. First level (li.first-level)
    3. Children level (li.booknode)
    4. Grand children level (li with style="padding: 0px;")
    """
    # Create an empty list to store all rows
    all_rows = []
    
    for ul_main in soup.find_all('ul', class_='tree'):
        # Find the corresponding hidden input
        hidden_input_main = ul_main.find_next_sibling('input', type='hidden')
        
        # [-] data ---------------------------------------------------------------------------------------------
        # Base data for this iteration
        base_data: Dict[str, str] = {
            "islmwy_page"                 : islmwy_page,
            "hidden_input_main_data_id"   : hidden_input_main.get('id', "")    if hidden_input_main else "",
            "hidden_input_main_data_value": hidden_input_main.get('value', "") if hidden_input_main else "",
            "hidden_input_main_data_name" : hidden_input_main.get('name', "")  if hidden_input_main else ""
        }
        
        # Add main level row
        all_rows.append(base_data.copy())
        
        # Find the first-level list [li]
        for li_first_level in ul_main.find_all('li', class_='first-level'):
            first_level_data = base_data.copy()
            
            # Add first level data
            input_first_level = li_first_level.find('input', type='checkbox')
            label_first_level = li_first_level.find('label', class_="tree_label")
            hidden_input_first_level = li_first_level.find_next_sibling('input', type='hidden')
            
            # [-] data ---------------------------------------------------------------------------------------------
            first_level_data.update({
                "input_first_level_data_id"           : input_first_level.get('id', "")           if input_first_level else "",
                "hidden_input_first_level_data_id"    : hidden_input_first_level.get('id', "")    if hidden_input_first_level else "",
                "hidden_input_first_level_data_value" : hidden_input_first_level.get('value', "") if hidden_input_first_level else "",
                "hadith_book_name_level"        : label_first_level.get('data-level', "")   if label_first_level else "",
                "hadith_book_name_id"           : label_first_level.get('data-id', "")      if label_first_level else "",
                "hadith_book_name_href"         : label_first_level.get('data-href', "")    if label_first_level else "",
                "hadith_book_name_idfrom"       : label_first_level.get('data-idfrom', "")  if label_first_level else "",
                "hadith_book_name_idto"         : label_first_level.get('data-idto', "")    if label_first_level else "",
                "hadith_book_name_node"         : label_first_level.get('data-node', "")    if label_first_level else "",
                "book_id"       : label_first_level.get('data-bookid', "")  if label_first_level else "",
                "hadith_book_name_for"          : label_first_level.get('for', "")          if label_first_level else "",
                "hadith_chapter"      : label_first_level.text.strip()               if label_first_level else ""
            })
            
            # Add first level row
            all_rows.append(first_level_data.copy())
            
            ul_childrens = li_first_level.find_all('ul', id=re.compile(r"childrens[\d]+"))
            
            if ul_childrens:
                for ul_children in ul_childrens:
                    for li_children in ul_children.find_all('li', class_='booknode'):
                        children_data = first_level_data.copy()
                        
                        input_children = li_children.find('input', type='checkbox')
                        hidden_input_children = li_children.find_next_sibling('input', type='hidden')
                        label_children = li_children.find('label', class_="tree_label")
                        # [-] data ---------------------------------------------------------------------------------------------
                        children_data.update({
                            "li_children_data_level"           : li_children.get('data-level', "")      if li_children else "",
                            "li_children_data_id"              : li_children.get('data-id', "")         if li_children else "",
                            "hadith_book_name_part_url"        : li_children.get('data-href', "")       if li_children else "",
                            "li_children_data_idfrom"          : li_children.get('data-idfrom', "")     if li_children else "",
                            "li_children_data_idto"            : li_children.get('data-idto', "")       if li_children else "",
                            "li_children_data_node"            : li_children.get('data-node', "")       if li_children else "",
                            "li_children_data_bookid"          : li_children.get('data-bookid', "")     if li_children else "",
                            "li_children_data_for"             : li_children.get('for', "")             if li_children else "",
                            "li_children_data_tag_id"          : li_children.get('id', "")              if li_children else "",
                            "input_children_data_id"           : input_children.get('id', "")           if input_children else "",
                            "hidden_input_children_data_id"    : hidden_input_children.get('id', "")    if hidden_input_children else "",
                            "hidden_input_children_data_value" : hidden_input_children.get('value', "") if hidden_input_children else "",
                            "label_children_data_chapter"      : label_children.text.strip()               if label_children else "",
                            "label_children_data_level"        : label_children.get('data-level', "")   if label_children else "",
                            "label_children_data_id"           : label_children.get('data-id', "")      if label_children else "",
                            "label_children_data_href"         : label_children.get('data-href', "")    if label_children else "",
                            "label_children_data_idfrom"       : label_children.get('data-idfrom', "")  if label_children else "",
                            "label_children_data_idto"         : label_children.get('data-idto', "")    if label_children else "",
                            "label_children_data_node"         : label_children.get('data-node', "")    if label_children else "",
                            "label_children_data_bookid"       : label_children.get('data-bookid', "")  if label_children else "",
                            "label_children_data_for"          : label_children.get('for', "")          if label_children else "",
                            "label_children_data_tag_id"       : label_children.get('id', "")           if label_children else ""
                        })
                        
                        # Add children level row
                        all_rows.append(children_data.copy())
                        
                        ul_grand_child = li_children.find('ul', id=re.compile(r"childrens[\d]+"))
                        
                        if ul_grand_child:
                            for li_grand_child in ul_grand_child.find_all('li', style="padding: 0px;"):
                                grand_child_data = children_data.copy()
                                
                                hidden_input_grand_children = li_grand_child.find_next_sibling('input', type='hidden')
                                
                                for span_grand_children in li_grand_child.find_all('span', class_="tree_label"):
                                    anchor_grand_children = span_grand_children.find('a')
                                    
                                    grand_child_data.update({
                                        "hidden_input_grand_children_data_id"      : hidden_input_grand_children.get('id', "") if hidden_input_grand_children else "",
                                        "hidden_input_grand_children_data_value"   : hidden_input_grand_children.get('value', "") if hidden_input_grand_children else "",
                                        "hadith_chapter_href"          : anchor_grand_children.get('href', "") if anchor_grand_children else "",
                                        "hadith_chapter_id"            : anchor_grand_children.get('id', "") if anchor_grand_children else "",
                                        "hadith_chapter" : anchor_grand_children.text.strip() if anchor_grand_children else "",
                                    })
                                    
                                    # Add grand children level row
                                    all_rows.append(grand_child_data.copy())
    
    # Create DataFrame from all collected rows
    df = pd.DataFrame(all_rows)
    
    '''
    # Add a level indicator column
    df['tree_level'] = df.apply(lambda row: 
        'grand_child' if not pd.isna(row.get('hadith_chapter_id', "")) else
        'child' if not pd.isna(row.get('li_children_data_id', "")) else
        'first' if not pd.isna(row.get('input_first_level_data_id', "")) else
        'main', axis=1)
    '''
    # Add hierarchical level indicator column
    df['tree_level'] = df.apply(determine_tree_level, axis=1)

    # Reset DataFrame index for consistent numbering
    df = df.reset_index(drop=True)
     
    return df


