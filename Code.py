import pandas as pd
import numpy as np
import re

def calculate_text_count(data):
    """
    Calculate the word count of text content in the DataFrame.

    Args:
    data (DataFrame): DataFrame containing text content.

    Returns:
    DataFrame: DataFrame with an additional column 'text_count' representing the word count of text content.
    """
    for index, row in data.iterrows():
        if pd.isnull(row['text']):
            data.at[index, 'text_count'] = 0
        else:
            word_count = len(re.split(r'[.,\s]', row['text']))
            data.at[index, 'text_count'] = word_count
    return data

def merge_dataframes(datatotal, page_duration, text_count):
    """
    Merge multiple DataFrames into a single DataFrame based on common indices.

    Args:
    datatotal (DataFrame): DataFrame containing total data.
    page_duration (DataFrame): DataFrame containing page duration data.
    text_count (DataFrame): DataFrame containing text count data.

    Returns:
    DataFrame: Merged DataFrame.
    """
    data = pd.merge(datatotal, page_duration, left_index=True, right_index=True)
    data_for_model = pd.merge(data, text_count, left_index=True, right_index=True)
    data_for_model.drop(labels=['Unnamed: 0_x', 'Unnamed: 0.1_x', 'page_duration_x', 'Unnamed: 0_y', 'user_id_y',
                                'page_y', 'Unnamed: 0', 'Unnamed: 0.1_y', 'user_id', 'page', 'learning_round_y',
                                'behavior_category_y', 'text_y', 'time1_y', 'time2_y', 'duration_y', 'page_length_y',
                                'page_duration'], axis=1, inplace=True)
    data_for_model.rename(columns={'user_id_x': 'user_id', 'page_x': 'page', 'learning_round_x': 'learning_round',
                                   'behavior_category_x': 'behavior_category', 'text_x': 'text_content',
                                   'time1_x': 'times_tart', 'time2_x': 'time_end', 'duration_x': 'text_duration',
                                   'page_length_x': 'page_length', 'page_duration_y': 'page_duration'}, inplace=True)
    return data_for_model

def calculate_seconds(data):
    """
    Convert time duration columns to seconds.

    Args:
    data (DataFrame): DataFrame containing time duration columns.

    Returns:
    DataFrame: DataFrame with time duration columns converted to seconds.
    """
    data['text_duration'] = pd.to_timedelta(data['text_duration'])
    data['text_duration_seconds'] = data['text_duration'].dt.total_seconds()
    data['page_duration'] = pd.to_timedelta(data['page_duration'])
    data['page_duration_seconds'] = data['page_duration'].dt.total_seconds()
    return data

def fill_nan_text_duration(data):
    """
    Fill NaN values in 'text_duration_seconds' column with zeros.

    Args:
    data (DataFrame): DataFrame containing 'text_duration_seconds' column.

    Returns:
    DataFrame: DataFrame with NaN values filled with zeros in 'text_duration_seconds' column.
    """
    data['text_duration_seconds'].fillna(0, inplace=True)
    return data

def calculate_text_operation_time(data):
    """
    Calculate cumulative text operation time for each page.

    Args:
    data (DataFrame): DataFrame containing text operation time data.

    Returns:
    DataFrame: DataFrame with an additional column 'text_operation_time' representing cumulative text operation time.
    """
    data = data.reset_index(drop=True)
    currentpage = 0
    ol = {}
    result = 0
    for index, row in data.iterrows():
        if row['page'] == currentpage:
            ol[index] = index
            result += row['text_duration_seconds']
            add = {'text_operation_time': result}
            continue
        else:
            for x in ol.values():
                data.at[x - 1, 'text_operation_time'] = add.get('text_operation_time')
                data.at[x, 'text_operation_time'] = add.get('text_operation_time')
            result = 0
            ol = {}
            result += row['text_duration_seconds']
            currentpage = row['page']
    return data

def calculate_text_count_total(data):
    """
    Calculate total text count for each page.

    Args:
    data (DataFrame): DataFrame containing text count data.

    Returns:
    DataFrame: DataFrame with an additional column 'text_count_total' representing total text count.
    """
    currentpage = 0
    ol = {}
    result = 0
    for index, row in data.iterrows():
        if row['page'] == currentpage:
            ol[index] = index
            result += row['text_count']
            add = {'resultw': result}
            continue
        else:
            for i in ol.values():
                data.at[i - 1, 'text_count_total'] = add.get('resultw')
                data.at[i, 'text_count_total'] = add.get('resultw')
            result = 0
            ol = {}
            result += row['text_count']
            currentpage = row['page']
    return data

def analyze_learning_behavior(data):
    """
    Analyze learning behavior trends over time.

    Args:
    data (DataFrame): DataFrame containing learning behavior data.

    Returns:
    None
    """
    behavior_trends = data.groupby(['learning_round', 'behavior_category'])['behavior_count'].sum().unstack()

    # Visualization of behavior trends can be added here using matplotlib or any other plotting library

def generate_summary_statistics(data):
    """
    Generate summary statistics for each user.

    Args:
    data (DataFrame): DataFrame containing user data.

    Returns:
    DataFrame: DataFrame with summary statistics for each user.
    """
    summary_stats = data.groupby(['user_id']).agg({
        'total_duration': 'sum',
        'behavior_count': 'sum',
        'behavior_time_proportion': 'mean'
    })
    return summary_stats


# Load input data
datatotal = pd.read_csv('datatotal.csv')
page_duration = pd.read_csv('page_duration.csv')
text_count = pd.read_csv('text_count.csv')

# Apply optimization methods
text_count = calculate_text_count(text_count)
data_for_model = merge_dataframes(datatotal, page_duration, text_count)
data_for_model = calculate_seconds(data_for_model)
data_for_model = fill_nan_text_duration(data_for_model)
data_for_model = calculate_text_operation_time(data_for_model)
data_for_model = calculate_text_count_total(data_for_model)

# Analyze learning behavior trends
analyze_learning_behavior(data_for_model)

# Generate summary statistics
summary_stats = generate_summary_statistics(data_for_model)
summary_stats.to_csv("summary_statistics.csv")
