import pandas as pd
import re


# Clean the texts
def clean_text(text):
    # Remove all non-ASCII and non-standard characters except for common punctuation
    text = re.sub(r'[^\w\s,.?!$]', '', text)
    # Remove hashtags, mentions
    text = re.sub(r'[@#]\w+', '', text)
    # Remove stock tickers like $TSLA but keep monetary values like $1,000,000
    text = re.sub(r'\b\$\w+\b', '', text)
    return text


# Load the data and drop duplicates
def process_and_clean(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Drop duplicates based on the 'text' column
    df = df.drop_duplicates(subset='text')

    # Clean the 'text' column
    df['text'] = df['text'].apply(clean_text)

    return df
