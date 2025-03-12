import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Twitter API credentials (replace with your own)
TWITTER_API_KEY = "sFA588mhCM8CTgl8IY4P0xPeT"
TWITTER_API_SECRET = "OcmzPTOImP1035J8sKbqsyy6LyswGsfmgINRLk0C22d9pNVIFJ"
TWITTER_ACCESS_TOKEN = "3112053546-l3UO98frCNYmkLzgGawi8AXK4KGprULBWXpfRas"
TWITTER_ACCESS_SECRET = "XwhS8vwnhLpHBYHumZ8RnRlNnXRBxbBMJWfpgtPYjAWW1"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def analyze_sentiment():
    analyzer = SentimentIntensityAnalyzer()
    teams = ["Toronto Maple Leafs", "Boston Bruins", "Edmonton Oilers"]
    sentiment_scores = {}

    for team in teams:
        tweets = api.search(q=team, count=100, lang='en', result_type='recent')
        total_score = 0
        for tweet in tweets:
            score = analyzer.polarity_scores(tweet.text)['compound']
            total_score += score
        avg_score = total_score / len(tweets) if tweets else 0
        sentiment_scores[team] = avg_score

    return sentiment_scores
