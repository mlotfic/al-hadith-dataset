import pandas as pd
from .to_csv_pd import to_csv_pd
from .to_json_with_arabic import to_json_with_arabic

def to_json_csv(data, filename, base_filename, islmwy_page, raw = None):            
    
    # Save to json
    to_json_with_arabic(data, filename, base_filename, islmwy_page, raw)    
    
    # Save to CSV
    if type(data) == dict :
        df = pd.DataFrame([data])
    elif (type(data) == list) and (len(data)>1) and (type(data[0]) == dict):
        df = pd.DataFrame(data, columns=data[0].keys())        
        
    return to_csv_pd(df, filename, base_filename, "csv", islmwy_page, raw)