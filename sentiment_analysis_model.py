import os
import csv
import re
import requests
from datetime import datetime
import time
import vertexai
from vertexai.generative_models import GenerativeModel
from tqdm import tqdm


def get_sentiment_analysis(tweets, keyword, google_project):
    cleaned_tweets_with_ids = []
    for tweet in tweets:
        # Splitting the tweet into its components (ID and text)
        parts = tweet.split(" | ")
        if len(parts) > 1:
            tweet_id_part, text_part = parts[0], parts[1]
            # Extracting the ID and the text
            tweet_id = tweet_id_part.replace("tweet_id: ", "").strip()
            text = clean_tweet_text(text_part.replace("text: ", ""))
            # Combining the tweet ID and cleaned text
            cleaned_tweet_with_id = f"{tweet_id} | text: {text}"
            cleaned_tweets_with_ids.append(cleaned_tweet_with_id)
    # Joining the cleaned tweets with IDs into a single string for analysis
    texts = ' || '.join(cleaned_tweets_with_ids)

    # Task for LLM
    task = f'You will receive a number of texts from various ids. for each text, your task is to find out where there is a reference to the word [{keyword}], and analyze the attitude toward it and to classify it. get probabilities from 0.00 to 1.00 for sentiments (the sum of all three probabilities of the three sentiments must equal to 1.00) and rating numbers from 0 to 100 for emotions for how much the text fit the category. also please mention as short as possible with 10 words maximum what is the criticism toward the keyword. if there is no criticism, simply write none. the output results must be only in the following format for example: INDEX: 1 || tweetid: id number | sentiments - negative: 0.25, positive: 0.55, neutral: 0.25 | emotions - anticipation: 83, happiness: 15, sadness: 22, anger: 50, fear: 67, disgust: 68, surprise: 32, contempt: 0, guilt: 21, shame: 80, curiosity: 2, pride: 8, sympathy: 100 | criticism: he must release the hostages INDEX: 2 || tweetid: id number |... there is no need to give any explanations for the classifications or the texts, just write the output format I mentioned. notice that if the texts contain emojis, so take them into consideration when classifying.'
    attempt = 0
    while attempt < 2:  # Allow for a second attempt if the first fails
        try:
            # Initialize Model
            vertexai.init(project=google_project, location="us-central1")
            model = GenerativeModel("gemini-1.5-pro-preview-0409")
            responses = model.generate_content(
                [f"""{task}
            input: {texts}
            """],
                generation_config={
            "temperature": 1,
            "top_p": 1
            }
            )

            content = responses.text
            return content

        except Exception as e:
            print(f"Error occurred: {e}")
            if attempt == 0:  # Only wait and retry if it's the first attempt
                print("Waiting 30 seconds before retrying...")
                time.sleep(30)
        attempt += 1
    return None


# clean texts from links and unique symbols
def clean_tweet_text(text):
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = text.replace('\n', ' ')
    return text.strip()


# Parse the sentiments results from the LLM
def parse_sentiment_data(sentiment_data):
    tweets_data = [data for data in sentiment_data.split("INDEX:") if data.strip()]
    sentiment_info = {}
    for index, tweet_data in enumerate(tweets_data):
        try:
            # Basic extraction of tweet_id (not used as key here, just for reference)
            tweet_id_match = re.search(r'tweetid: (\d+\.?\d+E?\d*)', tweet_data)
            tweet_id = tweet_id_match.group(1) if tweet_id_match else "Unknown"

            # Extract sentiments
            sentiments_match = re.search(
                r'sentiments - negative: ([0-1]\.\d+), positive: ([0-1]\.\d+), neutral: ([0-1]\.\d+)', tweet_data)
            sentiments = {'negative': sentiments_match.group(1),
                           'positive': sentiments_match.group(2),
                           'neutral': sentiments_match.group(3)} if sentiments_match else {}

            # Extract emotions
            emotions_match = re.search(
                r'emotions - (anticipation: \d+, happiness: \d+, sadness: \d+, anger: \d+, fear: \d+, disgust: \d+, surprise: \d+, contempt: \d+, guilt: \d+, shame: \d+, curiosity: \d+, pride: \d+, sympathy: \d+)',
                tweet_data)
            emotions = dict(item.split(": ") for item in emotions_match.group(1).split(", ")) if emotions_match else {}

            # Extracting criticism
            criticism_match = re.search(r'criticism: (none|[^\|]+)', tweet_data)
            criticism = criticism_match.group(1).strip() if criticism_match and criticism_match.group(1).lower() != 'none' else None

            # Use index as the key for each set of parsed data
            sentiment_info[index + 1] = {
                'tweet_id': tweet_id,
                **sentiments,
                **emotions,
                'criticism': criticism
            }
        except Exception as e:
            print(f"Error parsing tweet data: {e}. Data: {tweet_data}")

    return sentiment_info


def clean_tweet_id(tweet_id):
    """Ensure tweet IDs are treated as strings and handle scientific notation."""
    return "{:.0f}".format(float(tweet_id))


# Add the sentiments to their corresponding texts or tweets
def update_with_sentiment(tweets, sentiments):
    # Assuming `tweets` are ordered the same as `sentiments` keys which are index-based
    for i, tweet in enumerate(tweets, start=1):
        if i in sentiments:
            tweet.update(sentiments[i])
        else:
            print(f"No sentiment data for tweet at index: {i}")
    return tweets


# Create and add data to the modified CSV file
def append_to_new_csv(tweets, sentiments, new_filepath, write_header=False):
    # Ensure all keys from the first tweet are used as fieldnames, if tweets list is not empty
    if tweets:
        example_tweet = tweets[0]
        # Collect keys from sentiments if available; example: 'positive', 'neutral', 'negative'
        additional_fields = list(sentiments[next(iter(sentiments))].keys()) if sentiments else []
        fieldnames = list(example_tweet.keys()) + additional_fields
        fieldnames = list(dict.fromkeys(fieldnames))  # Remove duplicates

        with open(new_filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            for tweet in tweets:
                # Merge tweet info with its corresponding sentiment data
                tweet_with_sentiment = {**tweet, **sentiments.get(tweet['tweet_id'], {})}
                try:
                    writer.writerow(tweet_with_sentiment)
                except ValueError as e:
                    # If there are still unexpected fields, skip this row
                    print(f"Skipping tweet {tweet['tweet_id']} due to missing fields: {e}")


def analyze_and_update_csv(file_path, df_cleaned, api_key):
    new_filepath = os.path.splitext(file_path)[0] + "_modified.csv"

    # Check if the modified CSV file already exists
    if os.path.exists(new_filepath):
        # If it exists, skip the processing and return the existing file path
        return new_filepath

    header_written = False

    # Initialize progress bar for DataFrame processing
    progress_bar = tqdm(total=len(df_cleaned), desc="Processing rows")

    batch = []
    for _, row in df_cleaned.iterrows():
        if row.get('tweet_id') and row.get('text'):
            tweet_data = row.to_dict()
            tweet_data['text'] = clean_tweet_text(tweet_data['text'])
            batch.append(tweet_data)

            if len(batch) == 50:  # Feed the LLM with a batch size of 50 each time
                process_batch(batch, new_filepath, header_written, api_key)
                header_written = True  # Only write header once
                batch = []

        progress_bar.update(1)  # Update progress after each row is processed

    if batch:  # Process remaining tweets if any
        process_batch(batch, new_filepath, header_written, api_key)

    progress_bar.close()  # Ensure the progress bar is closed after processing

    return new_filepath


# Use batches when feeding the LLM.
def process_batch(batch, new_filepath, header_written, api_key):
    tweets_for_analysis = [{"tweet_id": tweet["tweet_id"], "text": tweet["text"]} for tweet in batch]
    tweet_texts = [f"tweetid: {tweet['tweet_id']} | text: {clean_tweet_text(tweet['text'])}" for tweet in tweets_for_analysis]
    sentiment_results = get_sentiment_analysis(tweet_texts, batch[0].get('keyword', ''), api_key)
    parsed_sentiments = parse_sentiment_data(sentiment_results)
    updated_tweets = update_with_sentiment(batch, parsed_sentiments)
    append_to_new_csv(updated_tweets, parsed_sentiments, new_filepath, write_header=not header_written)

