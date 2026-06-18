import requests
import pandas as pd
from datetime import datetime

def fetch_app_store_reviews(app_id="310633997", count=100):
    """
    Fetches recent reviews from the Apple App Store for a given app via RSS feed.
    """
    try:
        url = f"https://itunes.apple.com/us/rss/customerreviews/page=1/id={app_id}/sortby=mostrecent/json"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        entries = data.get('feed', {}).get('entry', [])
        
        if not entries:
            return pd.DataFrame()
            
        reviews = []
        for entry in entries:
            try:
                # The first entry is sometimes the app itself
                if 'author' not in entry:
                    continue
                    
                review = {
                    'id': entry.get('id', {}).get('label', ''),
                    'author': entry.get('author', {}).get('name', {}).get('label', ''),
                    'review_text': entry.get('title', {}).get('label', '') + " - " + entry.get('content', {}).get('label', ''),
                    'rating': int(entry.get('im:rating', {}).get('label', '0')),
                    'date': entry.get('updated', {}).get('label', ''),
                    'source': 'App Store'
                }
                reviews.append(review)
            except Exception as e:
                continue
                
        df = pd.DataFrame(reviews)
        return df.head(count)
    except Exception as e:
        print(f"Error fetching App Store reviews for ID {app_id}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = fetch_app_store_reviews()
    print(df.head())
