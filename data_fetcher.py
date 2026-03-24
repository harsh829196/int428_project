def get_news(stock):
    import requests
    
    API_KEY = "YOUR_API_KEY"
    url = f"https://newsapi.org/v2/everything?q={stock}&apiKey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    articles = []
    for a in data['articles'][:10]:
        articles.append(a['title'])

    return articles