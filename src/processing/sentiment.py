from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

def analyze_sentiment(df):
    """
    Adds sentiment scores and classifications to a DataFrame of reviews.
    Expects 'review_text' column to exist.
    """
    if df is None or df.empty:
        return df
        
    if 'review_text' not in df.columns:
        print("Warning: 'review_text' column not found for sentiment analysis.")
        return df

    analyzer = SentimentIntensityAnalyzer()
    
    def get_sentiment(text):
        if not isinstance(text, str):
            text = str(text) if text is not None else ""
            
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            classification = 'Positive'
        elif compound <= -0.05:
            classification = 'Negative'
        else:
            classification = 'Neutral'
            
        return pd.Series([compound, classification])

    # Apply sentiment analysis
    df[['sentiment_score', 'sentiment_label']] = df['review_text'].apply(get_sentiment)
    
    return df
