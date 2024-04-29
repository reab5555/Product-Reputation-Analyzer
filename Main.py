import os
import tkinter as tk
from tkinter import filedialog
from clean import process_and_clean
from sentiment_analysis_model_transformers import analyze_and_update_csv
from cluster_analysis_model import get_cluster_analysis
from results_export import export_results
from KPI_analysis import analyze_kpi

# Set your Google Cloud project name:
google_project = "your-google-cloud-project"

# Number of preferred critics:
n_critics = 10

# Initialize tkinter
root = tk.Tk()
root.withdraw()
# File Selection and Naming
file_path = filedialog.askopenfilename(title="Select the CSV file", filetypes=[("CSV files", "*.csv")])
if not file_path:
    raise FileNotFoundError("No file selected.")
# Extract the filename without the path
filename_with_extension = os.path.basename(file_path)
# Remove the extension from the filename
filename, _ = os.path.splitext(filename_with_extension)

#################################################################################################

# Clean data
df_cleaned = process_and_clean(file_path)

# Run sentiment analysis and save a modified CSV file with the sentiments
classified_csv_path = analyze_and_update_csv(file_path, df_cleaned)

# Run summarization analysis of important topics and criticisms
criticisms_topics = get_cluster_analysis(classified_csv_path, google_project, n_critics)

# Export report to a TXT file
export_results(df_cleaned, classified_csv_path, criticisms_topics)

# Export KPI data files
analyze_kpi(classified_csv_path)