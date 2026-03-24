print("App is starting...")
from flask import Flask, render_template, request
from data_fetcher import get_news
from sentiment import analyze_sentiment

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        stock = request.form["stock"]

        news = get_news(stock)
        sentiment, score = analyze_sentiment(news)

        return render_template("index.html",
                               stock=stock,
                               sentiment=sentiment,
                               score=score,
                               news=news[:5])

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)