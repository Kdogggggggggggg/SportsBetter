import requests #allows us to get data from website
import pandas as pd
import tweepy
import time #pause between API calls 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #sentiment analysis tool

API_KEY = "74e277a5bce0ae06d3fd337a6bd6f50a"
SPORT = 'icehockey_nhl'
# Twitter API credentials (replace with your own)
TWITTER_API_KEY = "TWITTER_API_KEY"
TWITTER_API_SECRET = "TWITTER_API_SECRET_KEY"
TWITTER_ACCESS_TOKEN = "TWITTER_ACCESS_TOKEN"
TWITTER_ACCESS_SECRET = "TWITTER_ACCESS_SECRET"
TWITTER_BEARER_TOKEN = "TWITTER_BEARER-TOKEN"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Use Twitter API v2 Client
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

NHL_TEAMS = [
    "Anaheim Ducks", "Arizona Coyotes", "Boston Bruins", "Buffalo Sabres",
    "Calgary Flames", "Carolina Hurricanes", "Chicago Blackhawks", "Colorado Avalanche",
    "Columbus Blue Jackets", "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers",
    "Florida Panthers", "Los Angeles Kings", "Minnesota Wild", "Montreal Canadiens",
    "Nashville Predators", "New Jersey Devils", "New York Islanders", "New York Rangers",
    "Ottawa Senators", "Philadelphia Flyers", "Pittsburgh Penguins", "San Jose Sharks",
    "Seattle Kraken", "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs",
    "Vancouver Canucks", "Vegas Golden Knights", "Washington Capitals", "Winnipeg Jets"
]


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
    teams = NHL_TEAMS
    sentiment_scores = {}

    for team in teams:
        try:
            time.sleep(5)

            tweets = client.search_recent_tweets(query=team, max_results=10)   

            total_score = 0
            for tweet in tweets.data:
                score = analyzer.polarity_scores(tweet.text)['compound']
                total_score += score

            avg_score = total_score / len(tweets.data) if tweets.data else 0
            sentiment_scores[team] = avg_score

        except tweepy.TooManyRequests:
            print(f"Rate limit exceeded. Skipping {team} and waiting...")
            time.sleep(900)  # Wait 15 minutes before retrying TO HELP REDUCE LOAD ON CALLS

    return sentiment_scores
