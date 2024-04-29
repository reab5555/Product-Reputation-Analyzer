import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample

# Balance samples for each month and year
# Balance samples for each month and year
def equalize_samples(df, group_by_cols):
    groups = df.groupby(group_by_cols)
    min_size = groups.size().min()
    def downsample_group(group):
        return resample(group, replace=False, n_samples=min_size, random_state=123)
    df_balanced = groups.apply(downsample_group).reset_index(drop=True)
    return df_balanced

# Calculate Influence score
def calculate_influence_score(df):
    temp_df = df.copy()
    tweet_counts = temp_df.groupby('screen_name').size().reset_index(name='tweet_count')
    followers_avg = temp_df.groupby('screen_name')['followers_count'].mean().reset_index()
    influence_data = pd.merge(tweet_counts, followers_avg, on='screen_name')
    influence_data['Influence'] = influence_data['followers_count'] * influence_data['tweet_count']
    result_df = pd.merge(df, influence_data[['screen_name', 'Influence']], on='screen_name', how='left')
    result_df['Influence'] = result_df['Influence'].fillna(0)
    return result_df

# Getting the KPIs
def tweet_kpi(df, stats_folder, keyword):
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)

    # Balancing data by month and year
    if df['year'].nunique() > 1:
        df = equalize_samples(df, ['year', 'month'])
    else:
        df = equalize_samples(df, ['month'])

    # Calculating Influence score
    df = calculate_influence_score(df)

    # Fill 0 where there is NA for all labels
    sentiment_emotion_labels = [
        'positive', 'negative', 'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion',
        'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
        'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 'relief',
        'remorse', 'sadness', 'surprise', 'neutral'
    ]
    for label in sentiment_emotion_labels:
        df[label] = df[label].fillna(0)

    # Calculate and prepare KPIs
    df['Volume'] = df['views'] + df['quotes'] + df['replies'] + df['retweets'] + df['bookmarks'] + df['favorites']
    df['Engagement'] = df['quotes'] + df['replies'] + df['retweets']

    # Aggregate the statistics
    agg_dict = {label: ['mean', 'count'] for label in sentiment_emotion_labels}
    agg_dict.update({
        'Volume': ['sum', 'count'],
        'Engagement': ['sum', 'count'],
        'Influence': ['sum', 'count']
    })

    # Check if 'revenue_value' column exists
    if 'stock_close_value' in df.columns:
        # Fill missing values with 0 and create a new 'stock_close_value' column
        df['stock_close_value'] = df['stock_close_value'].fillna(0)
        agg_dict['stock_close_value'] = ['mean']

    # Group by month and year, aggregate according to agg_dict
    if df['year'].nunique() > 1:
        by_year = df.groupby(['year']).agg(agg_dict)
        by_year.columns = ['_'.join(col).strip() for col in by_year.columns.values]
        by_year.to_csv(os.path.join(stats_folder, f'{keyword}_by_year_stats.csv'))

    by_month = df.groupby(['month']).agg(agg_dict)
    by_month.columns = ['_'.join(col).strip() for col in by_month.columns.values]
    by_month.to_csv(os.path.join(stats_folder, f'{keyword}_by_month_stats.csv'))

    print("KPIs Analysis complete. Results are saved to CSV files.")


def analyze_kpi(data_path):
    # Load the data from a CSV file
    df = pd.read_csv(data_path)
    keyword = df.loc[0, 'keyword']

    # Convert columns to numeric for all sentiment and emotion labels
    sentiment_emotion_labels = [
        'positive', 'negative', 'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion',
        'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
        'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 'relief',
        'remorse', 'sadness', 'surprise', 'neutral'
    ]
    for col in sentiment_emotion_labels:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, coerce errors to NaN

    # Define the path for the stats folder to be in the same directory as the data_path
    stats_folder = os.path.join(os.path.dirname(data_path), f'{keyword}_stats')

    tweet_kpi(df, stats_folder, keyword)
