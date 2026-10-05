from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from scraper import get_latest_headlines
from model import get_classifier

app = FastAPI(
    title="Financial News Sentiment API",
    description="Real-time news processing and sentiment classification pipeline."
)

# This function runs automatically as soon as you start the server
@app.on_event("startup")
def preload_model():
    print("----------------------------------------")
    print("Loading ML model into memory... Please wait.")
    get_classifier()
    print("Model loaded successfully! API is ready.")
    print("----------------------------------------")

class ArticleSentiment(BaseModel):
    title: str
    source: str
    url: str
    label: str
    score: float

class AnalysisResponse(BaseModel):
    total_articles: int
    articles: List[ArticleSentiment]

@app.get("/")
def root():
    return {"status": "active", "service": "Financial Sentiment Engine"}

@app.get("/analyze", response_model=AnalysisResponse)
def analyze_market_news():
    headlines = get_latest_headlines()
    if not headlines:
        raise HTTPException(status_code=503, detail="Unable to retrieve market news.")

    classifier = get_classifier()
    processed_articles = []

    for item in headlines:
        title = item["title"]
        res = classifier.analyze(title)
        
        processed_articles.append(ArticleSentiment(
            title=title,
            source=item["source"],
            url=item["url"],
            label=res["label"],
            score=res["score"]
        ))

    return AnalysisResponse(
        total_articles=len(processed_articles),
        articles=processed_articles
    )