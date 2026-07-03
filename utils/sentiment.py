"""
sentiment.py
------------
TextBlob-powered sentiment analysis utilities for customer feedback.
"""

import pandas as pd
import streamlit as st
from textblob import TextBlob


def _label_sentiment(polarity: float) -> str:
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    return "Neutral"


@st.cache_data(show_spinner=False)
def analyze_feedback(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run TextBlob sentiment analysis on the 'Feedback' column.

    Adds:
        Polarity        (-1.0 to 1.0)
        Subjectivity    (0.0 to 1.0)
        Sentiment       (Positive / Neutral / Negative)
        Word Count
    """
    if df.empty or "Feedback" not in df.columns:
        result = df.copy()
        result["Polarity"] = []
        result["Subjectivity"] = []
        result["Sentiment"] = []
        result["Word Count"] = []
        return result

    result = df.copy()
    polarities, subjectivities, word_counts = [], [], []

    for text in result["Feedback"].astype(str):
        try:
            blob = TextBlob(text)
            polarities.append(blob.sentiment.polarity)
            subjectivities.append(blob.sentiment.subjectivity)
        except Exception:
            polarities.append(0.0)
            subjectivities.append(0.0)
        word_counts.append(len(text.split()))

    result["Polarity"] = polarities
    result["Subjectivity"] = subjectivities
    result["Word Count"] = word_counts
    result["Sentiment"] = result["Polarity"].apply(_label_sentiment)

    return result


def sentiment_summary(df: pd.DataFrame) -> dict:
    """Compute summary sentiment statistics."""
    if df.empty:
        return {
            "positive": 0, "neutral": 0, "negative": 0,
            "avg_polarity": 0, "avg_subjectivity": 0, "avg_word_count": 0,
        }

    counts = df["Sentiment"].value_counts()
    return {
        "positive": int(counts.get("Positive", 0)),
        "neutral": int(counts.get("Neutral", 0)),
        "negative": int(counts.get("Negative", 0)),
        "avg_polarity": df["Polarity"].mean(),
        "avg_subjectivity": df["Subjectivity"].mean(),
        "avg_word_count": df["Word Count"].mean(),
    }


def top_reviews(df: pd.DataFrame, n: int = 5):
    """Return the top-n most positive and most negative reviews."""
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    top_positive = df.sort_values("Polarity", ascending=False).head(n)
    top_negative = df.sort_values("Polarity", ascending=True).head(n)
    return top_positive, top_negative
