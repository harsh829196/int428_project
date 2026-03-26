import feedparser

def get_news(stock):
    # 🔥 Google News RSS (no API key needed)
    url = f"https://news.google.com/rss/search?q={stock}+stock&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    articles = []

    # ✅ Get latest 5 news
    for entry in feed.entries[:5]:
        articles.append(entry.title)

    # ❌ If no news found
    if not articles:
        return ["No recent news found"]

    return articles