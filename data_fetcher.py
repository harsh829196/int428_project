
import requests

def get_news(stock):
    API_KEY = "YOUR_API_KEY"
    url = f"https://newsapi.org/v2/everything?q={stock}&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    # 🔥 Debug print
    print("API RESPONSE:", data)

    # ✅ Safe check
    if 'articles' not in data:
        print("Error from API:", data.get("message", "Unknown error"))
        return ["No news found or API error"]

    articles = []
    for a in data['articles'][:10]:
        articles.append(a['title'])

    return articles