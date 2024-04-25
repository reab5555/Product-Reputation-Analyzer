import numpy as np
import pandas as pd
import os  # Import os module to handle file directory operations


# Save criticism report as a TXT file
def export_results(df_cleaned, criticisms, save_path):
    keyword = df_cleaned.loc[0, 'keyword']  # Assuming 'keyword' is in the first row
    folder_name = f"{keyword}_stats"
    directory_path = os.path.join(os.path.dirname(save_path), folder_name)

    # Create the directory if it does not exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Define the full path for the text file
    txt_file_path = os.path.join(directory_path, f"{keyword}_analysis_summary.txt")

    # Write the criticisms string directly to the file, respecting existing newline characters
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write(criticisms)

    print(f"Data written to: {txt_file_path}")
