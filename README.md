# 📈 SentimentPulse — Stock Market Sentiment Chatbot

A real-time stock market sentiment analysis chatbot built with Flask.

## ✨ Features

| Feature | Description |
|---|---|
| 🔴 Live Sentiment Streaming | Bot responses stream token-by-token via SSE |
| 📡 Sentiment Pulse Meter | Live oscilloscope wave + arc needle in sidebar |
| 📰 News-based NLP | Fetches real headlines, scores with keyword NLP |
| 📊 Ticker Breakdown | Bull/Bear/Neutral bar charts update per query |
| ⚡ Trending Sidebar | Top 5 tickers with live sentiment badges |
| 🎨 Dark Terminal UI | Space Mono + Syne fonts, cyan-on-dark aesthetic |

## 🚀 Setup

```bash
cd stock-sentiment
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000**

## 🔑 Free API Keys (optional upgrades)

| API | Free Tier | Get Key |
|---|---|---|
| Alpha Vantage | 25 req/day | https://www.alphavantage.co/support/#api-key |
| GNews | 100 req/day | https://gnews.io |

Replace `ALPHA_VANTAGE_KEY` and `GNEWS_KEY` in `app.py` with your keys.

## 💬 Example Queries

- `AAPL sentiment` — Apple analysis
- `Is TSLA bullish?` — Tesla sentiment
- `NVDA analysis` — NVIDIA deep-dive
- `What's the market mood on META?`

## 📁 Structure

```
stock-sentiment/
├── app.py              # Flask backend + sentiment engine
├── requirements.txt
└── templates/
    └── index.html      # Single-file dark UI
```

## ⚠️ Disclaimer

For educational/demo purposes only. Not financial advice.
