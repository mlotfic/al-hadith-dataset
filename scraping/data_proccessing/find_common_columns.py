# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:59:07 2025

@author: m.lotfi
"""
import pandas as pd


# Method 1: Using set intersection
def find_common_columns(df1, df2):
    """
    Find common columns between two DataFrames
    
    Args:
        df1 (pd.DataFrame): First DataFrame
        df2 (pd.DataFrame): Second DataFrame
    
    Returns:
        list: List of common column names
    """
    common_columns = list(set(df1.columns) & set(df2.columns))
    return common_columns