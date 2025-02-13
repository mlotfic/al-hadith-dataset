import pandas as pd
import os

# csv_path = filepath, df = df_page_volume
def update_csv(csv_path, df):
    """
    Update a CSV file with new data, handling lists and maintaining unique records.
    
    Parameters:
    csv_path (str): Path to the CSV file
    df (pandas.DataFrame): DataFrame containing new data to append
    
    Returns:
    str or None: Path to CSV if successful, None if failed
    """
    try:
        # Specify the encoding that supports Arabic characters
        encoding = 'utf-8-sig'
        
        # Make a copy of the input DataFrame to avoid modifying the original
        df = df.copy()
        
        # Convert lists to strings in the input DataFrame
        for column in df.columns:
            mask = df[column].apply(lambda x: isinstance(x, list))
            if mask.any():
                print(f"Converting lists to strings in column: {column}")
                df[column] = df[column].apply(
                    lambda x: ','.join(map(str, x)) if isinstance(x, list) else x
                )
                
        
        # Check if the CSV file exists
        if os.path.exists(csv_path):
            # Read the existing CSV into a DataFrame with the specified encoding
            df_csv = pd.read_csv(csv_path, encoding=encoding)
            
            # Convert potential string representations of lists back to strings
            for column in df_csv.columns:
                if df_csv[column].dtype == 'object':
                    df_csv[column] = df_csv[column].apply(
                        lambda x: str(x) if isinstance(x, (list, dict)) else x
                    )
                    
        else:
            # Create an empty DataFrame with columns from the input DataFrame
            df_csv = pd.DataFrame(columns=df.columns)

       # Handle column differences and data types
        all_columns = list(set(df.columns) | set(df_csv.columns))
        
        # Initialize missing columns with empty strings instead of NA
        for col in all_columns:
            if col not in df.columns:
                df[col] = ''
            if col not in df_csv.columns:
                df_csv[col] = ''

        # Ensure both DataFrames have the same columns in the same order
        df = df[all_columns]
        df_csv = df_csv[all_columns]

        # Remove completely empty columns from both DataFrames
        non_empty_cols = [col for col in all_columns 
                         if not (df[col].isna().all() and df_csv[col].isna().all())]
        
        df = df[non_empty_cols]
        df_csv = df_csv[non_empty_cols]

        # Combine DataFrames
        df_combined = pd.concat([df_csv, df], ignore_index=True)

         # Drop duplicates
        before_drop = len(df_combined)
        df_combined.drop_duplicates(inplace=True)
        after_drop = len(df_combined)
        
        if before_drop != after_drop:
            print(f"Removed {before_drop - after_drop} duplicate rows")

        # Ensure directory exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

        # Save to CSV
        df_combined.to_csv(csv_path, index=False, encoding=encoding)
        
        print(f"Successfully updated CSV at {csv_path}")
        print(f"Total rows in updated CSV: {len(df_combined)}")
        
        return csv_path

    except pd.errors.EmptyDataError:
        print(f"Error: The CSV file {csv_path} is empty")
        return None
    except PermissionError:
        print(f"Error: Permission denied when accessing {csv_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return None

# Example usage:
if __name__ == "__main__":
    # Test the function
    try:
        # Create a sample DataFrame with a list
        test_df = pd.DataFrame({
            'column1': [1, 2, 3],
            'column2': [['a', 'b'], ['c'], ['d', 'e', 'f']],
            'column3': ['x', 'y', 'z']
        })
        
        # Test the function
        result = update_csv('test.csv', test_df)
        
        if result:
            print("CSV update successful")
        else:
            print("CSV update failed")
            
    except Exception as e:
        print(f"Test failed with error: {e}")