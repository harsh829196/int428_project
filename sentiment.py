from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(news_list):
    scores = []

    for news in news_list:
        score = analyzer.polarity_scores(news)['compound']
        scores.append(score)

    avg = sum(scores) / len(scores)

    if avg > 0.05:
        sentiment = "Positive"
    elif avg < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, avg