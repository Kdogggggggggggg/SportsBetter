import requests #allows us to get data from website
import pandas as pd
import tweepy
import time #pause between API calls 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #sentiment analysis tool

API_KEY = "74e277a5bce0ae06d3fd337a6bd6f50a"
SPORT = 'icehockey_nhl'
# Twitter API credentials (replace with your own)
TWITTER_API_KEY = "sFA588mhCM8CTgl8IY4P0xPeT"
TWITTER_API_SECRET = "OcmzPTOImP1035J8sKbqsyy6LyswGsfmgINRLk0C22d9pNVIFJ"
TWITTER_ACCESS_TOKEN = "3112053546-l3UO98frCNYmkLzgGawi8AXK4KGprULBWXpfRas"
TWITTER_ACCESS_SECRET = "XwhS8vwnhLpHBYHumZ8RnRlNnXRBxbBMJWfpgtPYjAWW1"
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJaUzwEAAAAAqDSDMCRy7ILHa%2BgZNzw%2FU68yFI0%3D4vYzlKQ0OUpwTbNkvqYV1xBkU72S1lu2PanqH0fBLhF7Dug09S"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Use Twitter API v2 Client
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)


def get_nhl_data():
    url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'
    params = {
        'apiKey': API_KEY,
        'regions': 'us',
        'markets': 'h2h',
        'oddsFormat': 'decimal',
        'dateFormat': 'iso'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch NHL data"}

    data = response.json()
    df = pd.DataFrame(data)

    # Extract relevant stats
    games = []
    for event in df.itertuples():
        home_team = event.home_team
        away_team = event.away_team
        games.append({"home": home_team, "away": away_team})

    return games

def analyze_sentiment():
    analyzer = SentimentIntensityAnalyzer()
    teams = ["Toronto Maple Leafs", "Boston Bruins", "Edmonton Oilers"]
    sentiment_scores = {}

    for team in teams:
        try:
            # ⬇️ FIX: Add delay before each request to avoid rate limits
            time.sleep(5)

            tweets = client.search_recent_tweets(query=team, max_results=10)   # Reduced to 10 tweets

            total_score = 0
            for tweet in tweets.data:
                score = analyzer.polarity_scores(tweet.text)['compound']
                total_score += score

            avg_score = total_score / len(tweets.data) if tweets.data else 0
            sentiment_scores[team] = avg_score

        except tweepy.TooManyRequests:
            print(f"Rate limit exceeded. Skipping {team} and waiting...")
            time.sleep(900)  # Wait 15 minutes before retrying

    return sentiment_scores