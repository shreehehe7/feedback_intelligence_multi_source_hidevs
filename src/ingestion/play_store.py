from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime

def fetch_play_store_reviews(app_id="com.whatsapp", count=100):
    """
    Fetches recent reviews from the Google Play Store for a given app ID.
    """
    try:
        result, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count
        )
        
        if not result:
            return pd.DataFrame()
            
        df = pd.DataFrame(result)
        
        # Standardize columns
        df = df[['reviewId', 'userName', 'content', 'score', 'at']]
        df.rename(columns={
            'reviewId': 'id',
            'userName': 'author',
            'content': 'review_text',
            'score': 'rating',
            'at': 'date'
        }, inplace=True)
        
        df['source'] = 'Google Play'
        return df
    except Exception as e:
        print(f"Error fetching Google Play reviews for {app_id}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = fetch_play_store_reviews()
    print(df.head())
