# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 21:17:09 2025

@author: m
"""

# "chapter"                   : ScrapingTable["chapter"][0],       
def handle_chapter_footer_tags(container_remaining, islmwy_page, chapter):
    if container_remaining is not None:
        print('Remaining Content:', "--------------------------------")
        chapter_footer: Dict[str, str] = {
            "islmwy_page"               : format(int(islmwy_page), '04d'), 
            "is_reamaining"             : False,                        
            "chapter"                   : chapter,                         
            "introduction"              : container_remaining.text.strip(),
            "div_tags"                  : str(container_remaining)
            }
        # Iterate over the children of the container div
        for child in container_remaining.children:
            if isinstance(child, Tag):
                # Get the class attribute safely (returns an empty list if not present)
                classes = child.get("class", [])
                if classes and 'hadith' in classes:
                    chapter_footer["is_reamaining"][0] = True
        df_chapter_footer = pd.DataFrame(chapter_footer, columns=chapter_footer[0].keys()) 
        filepath = f"./extracted_data/{base_filename}/db/chapter_footer.csv"
        update_csv(filepath, df_chapter_footer)                
        return chapter_footer
    else: 
        return None