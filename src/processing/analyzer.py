import pandas as pd
from collections import Counter
import re

def get_trend_summary(df):
    """
    Aggregates sentiment by date to find trends.
    """
    if df is None or df.empty or 'date' not in df.columns:
        return pd.DataFrame()
        
    try:
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        df['date_only'] = df['date'].dt.date
        
        # Group by date and sentiment
        trend = df.groupby(['date_only', 'sentiment_label']).size().unstack(fill_value=0).reset_index()
        
        # Make sure all sentiment columns exist
        for col in ['Positive', 'Negative', 'Neutral']:
            if col not in trend.columns:
                trend[col] = 0
                
        # Calculate daily average score
        daily_score = df.groupby('date_only')['sentiment_score'].mean().reset_index()
        trend = pd.merge(trend, daily_score, on='date_only')
        
        return trend.sort_values('date_only')
    except Exception as e:
        print(f"Error calculating trends: {e}")
        return pd.DataFrame()

def identify_critical_issues(df, top_n=10):
    """
    Extracts common keywords from negative reviews to identify issues.
    """
    if df is None or df.empty or 'sentiment_label' not in df.columns:
        return []
        
    negative_reviews = df[df['sentiment_label'] == 'Negative']
    if negative_reviews.empty:
        return []
        
    # Stop words for basic filtering
    stop_words = set(['the', 'is', 'in', 'and', 'to', 'it', 'that', 'of', 'for', 'on', 'with', 'as', 'this', 'was', 'app', 'not', 'but', 'i', 'my', 'a', 'you', 'so', 'have', 'are', 'be', 'they', 'just'])
    
    words = []
    for text in negative_reviews['review_text'].dropna():
        # Simple tokenization
        tokens = re.findall(r'\b[a-z]{3,}\b', str(text).lower())
        words.extend([w for w in tokens if w not in stop_words])
        
    # Get most common keywords
    common_words = Counter(words).most_common(top_n)
    return common_words

def prioritize_feedback(df):
    """
    Sorts feedback by importance (e.g., highly negative score, recent date).
    """
    if df is None or df.empty:
        return df
        
    # Sort by sentiment score ascending (most negative first) and date descending
    if 'date' in df.columns and 'sentiment_score' in df.columns:
        return df.sort_values(by=['sentiment_score', 'date'], ascending=[True, False])
    return df
