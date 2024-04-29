import os
import csv
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm


def get_sentiment_analysis(tweets):
    cleaned_tweets_with_ids = []
    for tweet in tweets:
        parts = tweet.split(" | ")
        if len(parts) > 1:
            tweet_id_part, text_part = parts[0], parts[1]
            tweet_id = tweet_id_part.replace("tweet_id: ", "").strip()
            text = clean_tweet_text(text_part.replace("text: ", ""))
            cleaned_tweet_with_id = f"{tweet_id} | {text}"
            cleaned_tweets_with_ids.append(cleaned_tweet_with_id)

    texts = [tweet.split("|")[1].strip() for tweet in cleaned_tweets_with_ids]  # Extracting texts for analysis

    # Check for CUDA availability and set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load sentiment model and tokenizer
    sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    sentiment_model.to(device)  # Move the model to GPU if available

    encoded_inputs_sentiment = sentiment_tokenizer(texts, max_length=150, padding=True, truncation=True, return_tensors='pt').to(device)
    with torch.no_grad():
        outputs_sentiment = sentiment_model(**encoded_inputs_sentiment)
        logits_sentiment = outputs_sentiment.logits

    # Load emotion model and tokenizer
    emotion_tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
    emotion_model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")
    emotion_model.to(device)  # Move the model to GPU if available

    encoded_inputs_emotion = emotion_tokenizer(texts, max_length=150, padding=True, truncation=True, return_tensors='pt').to(device)
    with torch.no_grad():
        outputs_emotion = emotion_model(**encoded_inputs_emotion)
        logits_emotion = outputs_emotion.logits

    # Define labels for sentiments and emotions
    sentiment_labels = ["negative", "positive"]
    emotion_labels = ["admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity",
                      "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear",
                      "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief",
                      "remorse", "sadness", "surprise", "neutral"]

    return logits_sentiment, logits_emotion, sentiment_labels, emotion_labels


def clean_tweet_text(text):
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = text.replace('\n', ' ')
    return text.strip()


# Parse the sentiments results from the LLM
def parse_sentiment_data(sentiment_logits, emotion_logits, sentiment_labels, emotion_labels):
    sentiment_info = {}
    # Process sentiment logits
    for i, logit in enumerate(sentiment_logits):
        for label, score in zip(sentiment_labels, logit.tolist()):
            if i + 1 not in sentiment_info:
                sentiment_info[i + 1] = {}
            sentiment_info[i + 1][label] = score  # Use label directly

    # Process emotion logits
    for i, logit in enumerate(emotion_logits):
        for label, score in zip(emotion_labels, logit.tolist()):
            if i + 1 not in sentiment_info:
                sentiment_info[i + 1] = {}
            sentiment_info[i + 1][label] = score  # Use label directly

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
    if tweets:
        # Determine all possible keys from the first sentiment entry (they should be the same across all entries)
        example_tweet = tweets[0]
        example_sentiment = sentiments[next(iter(sentiments))]

        fieldnames = list(example_tweet.keys()) + list(example_sentiment.keys())
        fieldnames = list(dict.fromkeys(fieldnames))  # Remove duplicates

        with open(new_filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            for i, tweet in enumerate(tweets, start=1):
                # Merge tweet info with its corresponding sentiment data
                tweet_with_sentiment = {**tweet, **sentiments.get(i, {})}
                try:
                    writer.writerow(tweet_with_sentiment)
                except ValueError as e:
                    print(f"Skipping tweet due to missing fields: {e}")





def analyze_and_update_csv(file_path, df_cleaned):
    classified_csv_path = os.path.splitext(file_path)[0] + "_classified.csv"

    # Check if the modified CSV file already exists
    if os.path.exists(classified_csv_path):
        # If it exists, skip the processing and return the existing file path
        return classified_csv_path

    header_written = False

    # Initialize progress bar for DataFrame processing
    progress_bar = tqdm(total=len(df_cleaned), desc="Processing rows")

    batch = []
    for _, row in df_cleaned.iterrows():
        if row.get('tweet_id') and row.get('text'):
            tweet_data = row.to_dict()
            tweet_data['text'] = clean_tweet_text(tweet_data['text'])
            batch.append(tweet_data)

            if len(batch) == 150:  # Feed the LLM with a batch size of 50 each time
                process_batch(batch, classified_csv_path, header_written)
                header_written = True  # Only write header once
                batch = []

        progress_bar.update(1)  # Update progress after each row is processed

    if batch:  # Process remaining tweets if any
        process_batch(batch, classified_csv_path, header_written)

    progress_bar.close()  # Ensure the progress bar is closed after processing

    return classified_csv_path


# Use batches when feeding the LLM.
def process_batch(batch, new_filepath, header_written):
    tweets_for_analysis = [{"tweet_id": tweet["tweet_id"], "text": tweet["text"]} for tweet in batch]
    tweet_texts = [f"tweetid: {tweet['tweet_id']} | text: {clean_tweet_text(tweet['text'])}" for tweet in
                   tweets_for_analysis]

    # Capturing both logits and labels
    sentiment_logits, emotion_logits, sentiment_labels, emotion_labels = get_sentiment_analysis(tweet_texts)
    # Passing all necessary arguments to parse_sentiment_data
    parsed_sentiments = parse_sentiment_data(sentiment_logits, emotion_logits, sentiment_labels, emotion_labels)

    updated_tweets = update_with_sentiment(batch, parsed_sentiments)
    append_to_new_csv(updated_tweets, parsed_sentiments, new_filepath, write_header=not header_written)


