from flask import Flask, jsonify #imort flask for creating a web server 
from tasks import get_nhl_data, analyze_sentiment #imports functions from task.py
from past import analyze_videos #imports functions from past.py
from winner import predict_winner #import functions from winner.py

app = Flask(__name__) #creates a flask web server 


@app.route('/predict', methods=['GET']) #creates an endpoint at /predict 
def predict():
    # Step 1: Fetch past NHL data
    nhl_stats = get_nhl_data()

    # Step 2: Get Twitter Sentiment Analysis
    twitter_sentiment = analyze_sentiment()

    # Step 3: Analyze previous NHL game videos
    video_analysis = analyze_videos()

    # Step 4: Predict the winner
    prediction = predict_winner(nhl_stats, twitter_sentiment, video_analysis)

    return jsonify(prediction) #returns prediction as a JSON response 


if __name__ == '__main__': #runs app when this file is executed
    app.run(debug=True)
