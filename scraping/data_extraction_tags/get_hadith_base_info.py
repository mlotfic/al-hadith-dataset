
from typing import Dict
import pandas as pd
from bs4 import BeautifulSoup
from .get_author import get_author
from .get_chapters_tree import get_chapters_tree
from .get_page_navigation import get_page_navigation
from .get_page_volume import get_page_volume
from .get_toc_path import get_toc_path
from ..handles_files.to_csv_pd import to_csv_pd
from ..handles_files.update_csv import update_csv



def get_hadith_base_info(soup, base_filename, islmwy_page, book_id):
        get_chapter_url       = lambda book_id, islmwy_page : f"https://www.islamweb.net/ar/library/content/{book_id}/{islmwy_page}/"
        get_prev_page_url     = lambda x: get_chapter_url(book_id, islmwy_page)  if x == 'N/A' else 'https://www.islamweb.net' + x
        get_next_page_url     = lambda x: get_chapter_url(book_id, islmwy_page)  if x == 'N/A' else 'https://www.islamweb.net' + x
        # (Parse chapters) 
        df_chapter_tree = get_chapters_tree(soup, islmwy_page)
        # Save to CSV
        # to_csv_pd(df            = df_chapter_tree, 
        #           filename      = "chapter-tree", 
        #           base_filename = base_filename, 
        #           ext           = "csv", 
        #           islmwy_page   = islmwy_page, 
        #           raw           = None
        #           )
        
        # Filepath for processed data
        filepath = f"./extracted_data/{base_filename}/csv/chapter-tree.csv"
        update_csv(filepath, df_chapter_tree) 
    
        # Parse header table of content path
        df_toc_path   = get_toc_path(soup, islmwy_page)
        # Save to CSV
        # to_csv_pd(df            = df_toc_path, 
        #           filename      = "toc-path-header", 
        #           base_filename = base_filename, 
        #           ext           = "csv", 
        #           islmwy_page   = islmwy_page, 
        #           raw           = None
        #           )
        # Filepath for processed data
        filepath = f"./extracted_data/{base_filename}/csv/toc-path-header.csv"
        update_csv(filepath, df_toc_path) 
        
    
        # Parse page_volume
        df_page_volume   = get_page_volume(soup, islmwy_page)
        # Save to CSV
        # to_csv_pd(df            = df_page_volume, 
        #           filename      = "page-volume", 
        #           base_filename = base_filename, 
        #           ext           = "csv", 
        #           islmwy_page   = islmwy_page, 
        #           raw           = None
        #           )
        filepath = f"./extracted_data/{base_filename}/csv/page-volume.csv"
        update_csv(filepath, df_page_volume)
    
        # Parse page_navigation
        df_page_navigation = get_page_navigation(soup, islmwy_page)    
        # Save to CSV
        # to_csv_pd(df            = df_page_navigation, 
        #           filename      = "page-navigation", 
        #           base_filename = base_filename, 
        #           ext           = "csv", 
        #           islmwy_page   = islmwy_page, 
        #           raw           = None
        #           )
        filepath = f"./extracted_data/{base_filename}/csv/page-navigation.csv"
        update_csv(filepath, df_page_navigation)
        
    
        ## ----------------------- Refined Extraction base info   ----------------------- ##        
        book                    = df_toc_path['book'].iloc[0]
        book_id                 = book_id
        book_url                = 'https://www.islamweb.net' + df_toc_path['book_url'].iloc[0]
        author                  = get_author(soup)
        
        prev_page               = get_prev_page_url(df_page_navigation['prev_page'].iloc[0])
        next_page               = get_next_page_url(df_page_navigation['next_page'].iloc[0])
        curr_page               = get_chapter_url(book_id, islmwy_page)
        
        book_page_number        = df_page_navigation['book_page_number'].iloc[0]
        book_page_volume        = df_page_volume['book_page_volume'].iloc[0]
        
        hadith_book_name        = df_toc_path['hadith_book_name'].iloc[0]
        hadith_section          = df_toc_path['hadith_section'].iloc[0]
        hadith_sub_section      = df_toc_path['hadith_sub_section'].iloc[0]
        hadith_part_I           = df_toc_path['hadith_part_I'].iloc[0]
        hadith_chapter          = df_toc_path['hadith_chapter'].iloc[0]
        
        ## ----------------------- store base info   ----------------------- ##   
        ### **📌 Scraping (:Scraping)**
        Scraping: Dict[str, str] = {
            "_id"                       : format(int(book_id), '04d') + '-' + format(int(islmwy_page), '04d'),
            'book_page'                 : book_page_number,             # رقم الصفحة بالكتاب            - [from] df_page_volume                  
            "page_volume"               : book_page_volume,             # رقم الجزء من الصفحة بالكتاب   - [from] df_page_volume 
            "book_hadith_number"        : "",
            
            "book_id"                   : "islamweb" + '-' + format(int(book_id), '04d'),          

            "book_name"                 : hadith_book_name,             # مثل : كتاب التوحيد            - [from] df_toc_path
            "section"                   : hadith_section,               # مثل : سورة الفاتحة            - [from] df_toc_path 
            "sub_section"               : hadith_sub_section,           # مثل : باب-بدء-الوحي           - [from] df_toc_path   
            "part_I"                    : hadith_part_I,                # مثل : باب-بدء-الوحي           - [from] df_toc_path             
            "chapter"                   : hadith_chapter,               # مثل : باب-بدء-الوحي           - [from] df_toc_path        
            
            'prev_page'                 : prev_page,                    # لينك الصفحة السابقة    
            'next_page'                 : next_page,                    # لينك الصفحة التالية         
            'curr_page'                 : curr_page,                    # لينك الصفحة الحالية    
            }
        
        df_scraping = pd.DataFrame([Scraping])
        filepath = f"./extracted_data/{base_filename}/db/Scraping.csv"
        update_csv(filepath, df_scraping)
        ### **📌 Book (:Book)**
        Book: Dict[str, str] = {
            "_id"                       : "islamweb" + '-' + format(int(book_id), '04d'),
            "islmwy_page"               : format(int(islmwy_page), '04d'),                  # مسلسل الصفحة بالموقع            
            "source"                    : "https://www.islamweb.net/",
            "copy_rights"               : "جميع الحقوق محفوظة © 2025 - 1998 لشبكة إسلام ويب",
            "website_book_id"           : book_id,                      # مسلسل الصفحة بالموقع            
            "name"                      : book,                         # اسم الكتاب                        - [from] df_toc_path
            "book_id"                   : book_id,                      # مسلسل الكتاب                      - [from] df_chapter_tree
            "url"                       : book_url,                     # لينك الكتاب                       - [from] df_toc_path
            "author"                    : author,                       # مؤلف المتاب
            
            "name_en"                   : "",                           # English title
            "description"               : "",                           # Description
            "total_hadiths"             : "",                           # Total hadith count
            "category"                  : "",                           # Tafseer, Hadith, etc.
            "methodology"               : "",                           # Methodology used in the tafseer          
            }
        
        df_Book = pd.DataFrame([Book])
        filepath = f"./extracted_data/{base_filename}/db/Book.csv"
        update_csv(filepath, df_Book)
        
        return Scraping, Book