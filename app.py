import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(
    page_title="Market Sentiment Radar",
    page_icon="📈",
    layout="wide"
)

API_ENDPOINT = "http://127.0.0.1:8000/analyze"

st.title("📈 Real-Time Financial News Sentiment Tracker")
st.markdown("Live sentiment analysis on high-impact financial news.")

@st.cache_data(ttl=300)
def fetch_data():
    try:
        response = requests.get(API_ENDPOINT, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Failed to connect to backend service: {e}")
    return None

col1, col2 = st.columns([1, 4])

with col1:
    if st.button("Refresh News Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

payload = fetch_data()

if payload:
    articles = payload["articles"]
    df = pd.DataFrame(articles)

    # Calculate overall metrics
    pos_count = len(df[df["label"] == "Positive"])
    neg_count = len(df[df["label"] == "Negative"])
    neu_count = len(df[df["label"] == "Neutral"])
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Headlines Analyzed", len(df))
    m2.metric("Positive Signal", f"{pos_count}")
    m3.metric("Negative Signal", f"{neg_count}")
    m4.metric("Neutral Signal", f"{neu_count}")

    st.markdown("---")

    # Visualizations section
    v_col1, v_col2 = st.columns(2)

    with v_col1:
        st.subheader("Sentiment Distribution")
        fig_pie = px.pie(
            df, 
            names="label", 
            color="label",
            color_discrete_map={"Positive": "#2ecc71", "Negative": "#e74c3c", "Neutral": "#95a5a6"},
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with v_col2:
        st.subheader("Confidence Scores by Sentiment")
        fig_box = px.box(
            df, 
            x="label", 
            y="score", 
            color="label",
            color_discrete_map={"Positive": "#2ecc71", "Negative": "#e74c3c", "Neutral": "#95a5a6"}
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.subheader("Latest Headlines & Output Predictions")

    for idx, row in df.iterrows():
        label_color = "🟢" if row["label"] == "Positive" else ("🔴" if row["label"] == "Negative" else "⚪")
        
        with st.expander(f"{label_color} {row['title']}"):
            st.write(f"**Source:** {row['source']}")
            st.write(f"**Prediction:** {row['label']} (Confidence: {row['score']:.2%})")
            st.markdown(f"[Read Full Article]({row['url']})")
else:
    st.info("Make sure the FastAPI backend is running locally at port 8000.")