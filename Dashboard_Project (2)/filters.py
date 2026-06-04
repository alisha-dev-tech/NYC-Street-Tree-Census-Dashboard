import pandas as pd
from datetime import datetime, timedelta

def apply_filters(df, filters):
    """
    Apply all filters to the dataframe
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe
    filters : dict
        Dictionary containing filter specifications
        - 'date_range': tuple of (start_date, end_date)
        - 'boroughs': list of borough names
        - 'health_status': list of health statuses
        - 'species': list of tree species
        - 'user_types': list of user types
        - 'dbh_range': tuple of (min_dbh, max_dbh)
        - 'address_keyword': str for address search
    
    Returns:
    --------
    pandas.DataFrame
        Filtered dataframe
    """
    filtered_df = df.copy()
    
    # Date range filter
    if 'date_range' in filters and filters['date_range']:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['created_at'].dt.date >= start_date) &
            (filtered_df['created_at'].dt.date <= end_date)
        ]
    
    # Borough filter
    if 'boroughs' in filters and filters['boroughs']:
        filtered_df = filtered_df[filtered_df['borough'].isin(filters['boroughs'])]
    
    # Health status filter
    if 'health_status' in filters and filters['health_status']:
        filtered_df = filtered_df[filtered_df['health'].isin(filters['health_status'])]
    
    # Species filter
    if 'species' in filters and filters['species']:
        filtered_df = filtered_df[filtered_df['spc_common'].isin(filters['species'])]
    
    # User type filter
    if 'user_types' in filters and filters['user_types']:
        filtered_df = filtered_df[filtered_df['user_type'].isin(filters['user_types'])]
    
    # DBH range filter
    if 'dbh_range' in filters and filters['dbh_range']:
        min_dbh, max_dbh = filters['dbh_range']
        filtered_df = filtered_df[
            (filtered_df['tree_dbh'] >= min_dbh) &
            (filtered_df['tree_dbh'] <= max_dbh)
        ]
    
    # Address search filter
    if 'address_keyword' in filters and filters['address_keyword']:
        keyword = filters['address_keyword'].upper()
        filtered_df = filtered_df[filtered_df['address'].str.contains(keyword, na=False)]
    
    return filtered_df

def get_filter_widgets():
    """
    Return filter widget specifications
    Used for consistent filter UI across the dashboard
    """
    return {
        'date_range': {
            'label': 'Date Range',
            'type': 'date_input',
            'icon': '📅'
        },
        'borough': {
            'label': 'Borough Selection',
            'type': 'multiselect',
            'icon': '🏘️'
        },
        'health': {
            'label': 'Tree Health Status',
            'type': 'multiselect',
            'icon': '💚'
        },
        'species': {
            'label': 'Tree Species (Top 10)',
            'type': 'multiselect',
            'icon': '🌱'
        },
        'user_type': {
            'label': 'User Type',
            'type': 'multiselect',
            'icon': '👤'
        },
        'dbh_range': {
            'label': 'Tree Diameter (DBH)',
            'type': 'slider',
            'icon': '📏'
        },
        'address': {
            'label': 'Search Address',
            'type': 'text_input',
            'icon': '🔎'
        }
    }

def get_filter_stats(df, filtered_df):
    """
    Generate filter statistics
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Original unfiltered dataframe
    filtered_df : pandas.DataFrame
        Filtered dataframe
    
    Returns:
    --------
    dict
        Dictionary containing filter statistics
    """
    original_count = len(df)
    filtered_count = len(filtered_df)
    
    stats = {
        'original_records': original_count,
        'filtered_records': filtered_count,
        'records_removed': original_count - filtered_count,
        'percentage_retained': round((filtered_count / original_count * 100), 2) if original_count > 0 else 0,
        'data_quality_metrics': {
            'missing_health': filtered_df['health'].isna().sum(),
            'missing_species': filtered_df['spc_common'].isna().sum(),
            'missing_dates': filtered_df['created_at'].isna().sum(),
        }
    }
    
    return stats

def suggest_filters(df):
    """
    Generate filter suggestions based on data exploration
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe to analyze
    
    Returns:
    --------
    dict
        Dictionary with filter suggestions
    """
    suggestions = {
        'most_common_borough': df['borough'].value_counts().index[0] if len(df) > 0 else None,
        'most_common_species': df['spc_common'].value_counts().index[0] if len(df) > 0 else None,
        'most_common_health': df['health'].value_counts().index[0] if len(df) > 0 else None,
        'average_dbh': round(df['tree_dbh'].mean(), 2),
        'median_dbh': round(df['tree_dbh'].median(), 2),
    }
    
    return suggestions
