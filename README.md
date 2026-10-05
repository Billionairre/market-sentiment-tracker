# Real-Time Financial News Sentiment Engine

An end-to-end sentiment analysis pipeline that fetches real-time financial market headlines, evaluates sentiment using a transformer-based NLP model, and serves predictions through a REST API and an interactive web dashboard.

I built this project to demonstrate how to take a machine learning model out of a standalone notebook environment and package it into a decoupled, production-style software pipeline.

## Architecture Overview

```mermaid
 External APIs / RSS Feeds
             │
             ▼
 Data Ingestion Layer (scraper.py)
             │
             ▼
 FastAPI Backend Service (api.py)  ──(Inference)──► [ RoBERTa Transformer (model.py) ]
             │
             ▼ (JSON REST Payload)
[ Streamlit Web Dashboard (app.py) ] ──(Render)──► User Visualizations
```

The system is split into distinct components:

- **Ingestion Layer (scraper.py):** Fetches live market headlines using the Finnhub REST API. To prevent service disruptions from API rate limits or missing credentials, it automatically falls back to Yahoo Finance RSS feeds.

- **Inference Engine (model.py):** Uses cardiffnlp/twitter-roberta-base-sentiment-latest via Hugging Face Transformers to classify text as Positive, Negative, or Neutral along with confidence scores.

- **REST API Service (api.py):** A FastAPI app that exposes endpoints to trigger data collection and inference. It pre-loads model weights into memory at startup to ensure fast responses without request timeouts.

- **Analytics Dashboard (app.py):** A Streamlit front-end featuring high-level market metrics, sentiment distribution charts built with Plotly, and expandable news cards.

## Tech Stack

**Language:** Python 3.10+

**Frameworks & API:** FastAPI, Uvicorn, Streamlit

**ML & NLP:** Hugging Face Transformers, PyTorch

**Data & Visualization:** Pandas, Plotly, Feedparser, Requests

## Directory Structure

```bash
market-sentiment-tracker/
├── api.py # FastAPI server and lifecycle management
├── app.py # Streamlit dashboard UI
├── model.py # Transformer model loader and classifier
├── scraper.py # Data fetching logic (Finnhub API + RSS fallback)
├── requirements.txt # Python package dependencies
├── .gitignore # Git exclusion rules
└── README.md # Technical project documentation
```

## Getting Started Locally

### Prerequisites

Make sure that Python is installed on the system.

**1. To Clone the Repository**

```bash
git clone https://github.com/Billionairre/market-sentiment-tracker.git
cd market-sentiment-tracker
```

**2. Set Up Virtual Environment**

```bash
python -m venv venv

# Activate the virtual environment
source venv/bin/activate # Linux/macOS
.\venv\Scripts\Activate.ps1 # Windows (PowerShell)
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Optional API Key Setup**

The project runs out of the box using public RSS feeds. If you want to use live Finnhub market news, create a `.env` file in the root directory:

```bash
FINNHUB_API_KEY=your_api_key_here
```

## Running the Application

You will need two terminal tabs active inside your virtual environment.

**Step 1: Launch the Backend API**

```bash
uvicorn api:app --reload --port 8000
```

Wait until you see Model loaded successfully! API is ready. in the console.
Interactive Swagger API documentation will be available at `http://127.0.0.1:8000/docs`.

**Step 2: Launch the Front-End Dashboard**
In a second terminal tab:

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

## Key Engineering Considerations & Challenges

- **Handling Cold-Start Latency:** Downloading and initializing transformer weights on the fly during a web request caused HTTP timeouts on the front-end. I resolved this by utilizing FastAPI's startup lifecycle hook (`@app.on_event("startup")`) to pre-warm the model in memory when the server boots.

- **Fault Tolerance in Data Fetching:** Web APIs can fail or hit rate limits. Adding an RSS parsing layer ensures the dashboard always has live data to render even when third-party API quotas are exhausted.

- **Decoupled Architecture:** Keeping the model inference engine separated from the UI allows other clients (like CLI tools or automated trading scripts) to reuse the API without needing the Streamlit front-end.
