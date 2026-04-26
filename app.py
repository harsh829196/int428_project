from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# ─── API KEYS (replace with yours) ──────────────────────────────────────────
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "demo")
NEWS_API_KEY      = os.environ.get("NEWS_API_KEY", "demo")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")   # Claude for chat

# ─── Helpers ─────────────────────────────────────────────────────────────────

def fetch_quote(symbol: str) -> dict:
    """Live quote via Alpha Vantage GLOBAL_QUOTE."""
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    )
    try:
        r = requests.get(url, timeout=8)
        data = r.json().get("Global Quote", {})
        if not data:
            return {}
        return {
            "symbol":   data.get("01. symbol", symbol),
            "price":    float(data.get("05. price", 0)),
            "change":   float(data.get("09. change", 0)),
            "change_pct": data.get("10. change percent", "0%"),
            "high":     float(data.get("03. high", 0)),
            "low":      float(data.get("04. low", 0)),
            "volume":   int(data.get("06. volume", 0)),
            "prev_close": float(data.get("08. previous close", 0)),
        }
    except Exception as e:
        return {"error": str(e)}


def fetch_news(query: str, symbol: str = "") -> list:
    """Headlines from NewsAPI (or Alpha Vantage NEWS_SENTIMENT as fallback)."""
    # Try Alpha Vantage news/sentiment first
    av_url = (
        f"https://www.alphavantage.co/query"
        f"?function=NEWS_SENTIMENT&tickers={symbol or query}"
        f"&limit=6&apikey={ALPHA_VANTAGE_KEY}"
    )
    try:
        r = requests.get(av_url, timeout=8)
        feed = r.json().get("feed", [])
        if feed:
            articles = []
            for a in feed[:6]:
                sentiment_score = 0
                for ts in a.get("ticker_sentiment", []):
                    if ts.get("ticker", "").upper() == symbol.upper():
                        sentiment_score = float(ts.get("ticker_sentiment_score", 0))
                articles.append({
                    "title":   a.get("title", ""),
                    "source":  a.get("source", ""),
                    "url":     a.get("url", "#"),
                    "time":    a.get("time_published", "")[:8],
                    "summary": a.get("summary", "")[:200],
                    "sentiment_score": sentiment_score,
                })
            return articles
    except:
        pass

    # Fallback: NewsAPI
    if NEWS_API_KEY and NEWS_API_KEY != "demo":
        try:
            news_url = (
                f"https://newsapi.org/v2/everything"
                f"?q={query}&sortBy=publishedAt&pageSize=6"
                f"&apiKey={NEWS_API_KEY}"
            )
            r = requests.get(news_url, timeout=8)
            arts = r.json().get("articles", [])
            return [
                {
                    "title":   a.get("title", ""),
                    "source":  a.get("source", {}).get("name", ""),
                    "url":     a.get("url", "#"),
                    "time":    a.get("publishedAt", "")[:10],
                    "summary": (a.get("description") or "")[:200],
                    "sentiment_score": 0,
                }
                for a in arts
            ]
        except:
            pass

    return []


def compute_sentiment(news_articles: list, quote: dict) -> dict:
    """Aggregate sentiment from Alpha Vantage scores + price momentum."""
    scores = [a["sentiment_score"] for a in news_articles if a["sentiment_score"] != 0]
    news_avg = sum(scores) / len(scores) if scores else 0

    # Price momentum contribution
    price_signal = 0
    if quote:
        chg = quote.get("change", 0)
        price_signal = min(max(chg / 5, -1), 1)   # clamp to [-1, 1]

    combined = 0.7 * news_avg + 0.3 * price_signal if news_avg else price_signal

    if combined > 0.25:
        label, emoji = "Bullish 🟢", "bullish"
    elif combined < -0.25:
        label, emoji = "Bearish 🔴", "bearish"
    else:
        label, emoji = "Neutral ⚪", "neutral"

    return {
        "label": label,
        "tag": emoji,
        "score": round(combined, 3),
        "news_avg": round(news_avg, 3),
        "price_signal": round(price_signal, 3),
    }


def build_context(symbol: str) -> dict:
    """Pull everything together for one ticker."""
    quote   = fetch_quote(symbol)
    news    = fetch_news(symbol, symbol)
    sentiment = compute_sentiment(news, quote)
    return {"symbol": symbol.upper(), "quote": quote, "news": news, "sentiment": sentiment}


def claude_chat(messages: list, system: str) -> str:
    """Call Anthropic claude-sonnet for the conversational layer."""
    if not ANTHROPIC_API_KEY:
        return "(Set ANTHROPIC_API_KEY to enable AI chat responses.)"
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 600,
                "system": system,
                "messages": messages,
            },
            timeout=20,
        )
        return r.json()["content"][0]["text"]
    except Exception as e:
        return f"AI error: {e}"


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stock", methods=["POST"])
def api_stock():
    symbol = request.json.get("symbol", "").strip().upper()
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400
    ctx = build_context(symbol)
    return jsonify(ctx)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    body     = request.json
    history  = body.get("history", [])
    symbol   = body.get("symbol", "")
    ctx_data = body.get("context", {})

    system = f"""You are FinBot, an elite stock market sentiment analyst.
You have access to real-time data for {symbol or 'various stocks'}.

Current data snapshot:
{json.dumps(ctx_data, indent=2)}

Your job:
- Analyse market sentiment using the news and price data provided.
- Give sharp, concise investment insights (NOT financial advice disclaimers—be direct).
- Reference specific headlines or price signals when relevant.
- Use trading terminology: support/resistance, RSI vibes, momentum, sentiment divergence, etc.
- When asked to compare stocks, reason about sector dynamics.
- Keep replies under 180 words unless the user asks for a deep dive.
- Be confident, analytical, and occasionally witty.
"""
    reply = claude_chat(history, system)
    return jsonify({"reply": reply})


@app.route("/api/compare", methods=["POST"])
def api_compare():
    symbols = request.json.get("symbols", [])
    results = {}
    for s in symbols[:4]:   # cap at 4
        results[s.upper()] = build_context(s.upper())
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
