import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample

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
def tweet_kpi(df, stats_folder):
    if not os.path.exists(stats_folder):
        os.makedirs(stats_folder)

    # Balancing data by month and year
    df = equalize_samples(df, ['year', 'month'])

    # Calculating Influence score
    df = calculate_influence_score(df)

    # fill 0 where there is NA
    df['Positive'] = df['positive'].fillna(0)
    df['Negative'] = df['negative'].fillna(0)
    df['Anticipation'] = df['anticipation'].fillna(0)
    df['Curiosity'] = df['curiosity'].fillna(0)
    df['Surprise'] = df['surprise'].fillna(0)

    # Calculate and prepare KPIs
    df['Volume'] = df['views'] + df['quotes'] + df['replies'] + df['retweets'] + df['bookmarks'] + df['favorites']
    df['Engagement'] = df['quotes'] + df['replies'] + df['retweets']
    df['Positive'] = df['positive']
    df['Negative'] = df['negative']
    df['Anticipation'] = df['anticipation']
    df['Curiosity'] = df['curiosity']
    df['Surprise'] = df['surprise']

    # Aggregate the statistics
    agg_dict = {
        'Volume': ['sum', 'count'],
        'Engagement': ['sum', 'count'],
        'Influence': ['sum', 'count'],
        'Positive': ['mean', 'count'],
        'Negative': ['mean', 'count'],
        'Anticipation': ['mean', 'count'],
        'Curiosity': ['mean', 'count'],
        'Surprise': ['mean', 'count']
    }

    # Check if 'revenue_value' column exists
    if 'revenue_value' in df.columns:
        # Fill missing values with 0 and create a new 'Revenue' column
        df['Revenue'] = df['revenue_value'].fillna(0)
        agg_dict['Revenue'] = ['mean']

    # Group results by month and year
    by_all = df.groupby(['year', 'month']).agg(agg_dict)
    by_month = df.groupby(['month']).agg(agg_dict)
    by_year = df.groupby(['year']).agg(agg_dict)

    # Build column names
    by_all.columns = ['_'.join(col).strip() if 'sum' or 'mean' not in col else col[0] for col in by_all.columns.values]
    by_month.columns = ['_'.join(col).strip() if 'sum' or 'mean' not in col else col[0] for col in by_month.columns.values]

    # List of columns for which to calculate percentage change
    columns_to_calculate = ['Volume_sum', 'Engagement_sum', 'Influence_sum', 'Positive_mean', 'Negative_mean',
                            'Anticipation_mean', 'Curiosity_mean', 'Surprise_mean']
    # Calculate the percentage change for each column and assign it to a new column
    for col in columns_to_calculate:
        by_all[col + '_pct_change'] = by_all[col].pct_change() * 100
    for col in columns_to_calculate:
        by_month[col + '_pct_change'] = by_month[col].pct_change() * 100

    # Sort columns
    def sort_columns(df):
        scale_cols = [col for col in df.columns if 'count' not in col]
        count_cols = [col for col in df.columns if 'count' in col]
        return df[scale_cols + count_cols]
    by_all = sort_columns(by_all)
    by_month = sort_columns(by_month)

    # Save columns
    by_all.to_csv(os.path.join(stats_folder, 'main_stats.csv'))
    by_month.to_csv(os.path.join(stats_folder, 'by_month_stats.csv'))

    print("KPIs Analysis complete. Results are saved to CSV files.")

def analyze_kpi(data_path):
    # Load the data from a CSV file
    df = pd.read_csv(data_path)
    keyword = df.loc[0, 'keyword']

    # Convert columns to numeric
    numeric_cols = ['positive', 'negative', 'anticipation', 'curiosity', 'surprise']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Coerce errors will convert non-convertible values to NaN

    # Define the path for the stats folder to be in the same directory as the data_path
    stats_folder = os.path.join(os.path.dirname(data_path), f'{keyword}_stats')

    tweet_kpi(df, stats_folder)
