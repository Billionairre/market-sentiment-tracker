import os
import requests
import feedparser
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")

def fetch_finnhub_news(category="general"):
    if not FINNHUB_API_KEY:
        return []
    
    url = f"https://finnhub.io/api/v1/news?category={category}&token={FINNHUB_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = []
            for item in data[:20]:
                articles.append({
                    "title": item.get("headline", ""),
                    "source": item.get("source", "Finnhub"),
                    "url": item.get("url", "#"),
                    "time": item.get("datetime", 0)
                })
            return articles
    except Exception as err:
        print(f"Error connecting to Finnhub API: {err}")
    
    return []

def fetch_rss_news():
    # Reliable backup source without API limits
    rss_url = "https://finance.yahoo.com/news/rssindex"
    feed = feedparser.parse(rss_url)
    
    articles = []
    for entry in feed.entries[:20]:
        articles.append({
            "title": entry.get("title", ""),
            "source": "Yahoo Finance RSS",
            "url": entry.get("link", "#"),
            "time": entry.get("published", "")
        })
    return articles

def get_latest_headlines():
    data = fetch_finnhub_news()
    if not data:
        data = fetch_rss_news()
    return data