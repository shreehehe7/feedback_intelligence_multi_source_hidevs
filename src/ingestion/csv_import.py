import pandas as pd
import io

def parse_csv_reviews(file_contents):
    """
    Parses a CSV file containing reviews.
    Expected columns: author, review_text, rating, date
    """
    try:
        df = pd.read_csv(io.StringIO(file_contents.decode("utf-8")))
        
        # Make sure essential columns exist, map them if needed
        required_cols = ['review_text']
        if not all(col in df.columns for col in required_cols):
            # Try to find a column that might be the review
            if 'text' in df.columns:
                df.rename(columns={'text': 'review_text'}, inplace=True)
            elif 'content' in df.columns:
                df.rename(columns={'content': 'review_text'}, inplace=True)
            elif 'review' in df.columns:
                df.rename(columns={'review': 'review_text'}, inplace=True)
            else:
                raise ValueError("CSV must contain a 'review_text', 'text', 'content', or 'review' column.")
        
        if 'rating' not in df.columns and 'score' in df.columns:
            df.rename(columns={'score': 'rating'}, inplace=True)
            
        if 'date' not in df.columns and 'time' in df.columns:
            df.rename(columns={'time': 'date'}, inplace=True)
            
        if 'author' not in df.columns and 'user' in df.columns:
            df.rename(columns={'user': 'author'}, inplace=True)
            
        # Add missing optional columns
        for col in ['author', 'rating', 'date']:
            if col not in df.columns:
                if col == 'rating':
                    df[col] = 3 # default rating
                else:
                    df[col] = 'Unknown'
                    
        df['id'] = [f"CSV_{i}" for i in range(len(df))]
        df['source'] = 'CSV Upload'
        
        return df[['id', 'author', 'review_text', 'rating', 'date', 'source']]
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return pd.DataFrame()
