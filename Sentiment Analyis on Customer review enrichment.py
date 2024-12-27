# Install required libraries: pip install pandas nltk sqlalchemy pyodbc
import pandas as pd
from sqlalchemy import create_engine
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon for sentiment analysis if not already present.
nltk.download('vader_lexicon')

# Function to fetch data from SQL Server
def fetch_data_from_sql():
    # Define the SQLAlchemy connection string
    conn_str = "mssql+pyodbc://DESKTOP-A5D5QUG/PortfolioProject_MarketingAnalytics?driver=SQL+Server"
    # Create the SQLAlchemy engine
    engine = create_engine(conn_str)
    
    # SQL query to fetch customer reviews data
    query = """
    SELECT ReviewID, CustomerID, ProductID,CONVERT(VARCHAR, ReviewDate, 23) AS ReviewDate, Rating, ReviewText
    FROM dbo.customer_reviews
    """
    
    # Fetch the data into a DataFrame
    df = pd.read_sql(query, engine)
    
    # Return the fetched DataFrame
    return df

# Fetch data from the SQL database
customer_reviews_df = fetch_data_from_sql()

# Initialize the VADER sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

# Function to calculate sentiment scores using VADER
def calculate_sentiment(review):
    sentiment = sia.polarity_scores(review)
    return sentiment['compound']

# Function to categorize sentiment using both the sentiment score and the review rating
def categorize_sentiment(score, rating):
    if score > 0.05:  # Positive sentiment
        if rating >= 4:
            return 'Positive'
        elif rating == 3:
            return 'Mixed Positive'
        else:
            return 'Mixed Negative'
    elif score < -0.05:  # Negative sentiment
        if rating <= 2:
            return 'Negative'
        elif rating == 3:
            return 'Mixed Negative'
        else:
            return 'Mixed Positive'
    else:  # Neutral sentiment
        if rating >= 4:
            return 'Positive'
        elif rating <= 2:
            return 'Negative'
        else:
            return 'Neutral'

# Function to bucket sentiment scores into text ranges
def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'
    else:
        return '-1.0 to -0.5'

# Calculate sentiment scores for each review
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

# Categorize sentiment using the sentiment score and the review rating
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1
)

# Bucket sentiment scores into ranges
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)
customer_reviews_df['ReviewDate'] = pd.to_datetime(customer_reviews_df['ReviewDate'], format='%Y-%m-%d')

# Display the first few rows of the DataFrame
print(customer_reviews_df.head())

# Save the DataFrame with sentiment analysis to a CSV file in the specified directory
output_path = r"C:\Users\91897\Desktop\Project\Sentiment Analysis.csv"
customer_reviews_df.to_csv(output_path, index=False)
print(f"CSV file saved at: {output_path}")
