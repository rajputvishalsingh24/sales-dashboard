"""
2_Customer_Feedback.py
------------------------
Customer feedback and TextBlob sentiment analysis page.
"""

import os
import warnings
import streamlit as st

from utils.preprocessing import load_data, apply_filters
from utils.helper import (
    inject_custom_css, format_number, kpi_card, section_header,
    sidebar_filters, download_button,
)
from utils.sentiment import analyze_feedback, sentiment_summary, top_reviews
from utils import charts

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Customer Feedback", page_icon="💬", layout="wide")
inject_custom_css()

logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)
st.sidebar.markdown("<h3 style='text-align:center;'>💬 Customer Feedback</h3>", unsafe_allow_html=True)

df = load_data()
if df.empty:
    st.warning("No data available.")
    st.stop()

region, state, category, sub_category, segment, date_range = sidebar_filters(df)
filtered_df = apply_filters(df, region, state, category, sub_category, segment, date_range)

download_button(filtered_df, "📥 Download Filtered Dataset", "feedback_filtered.csv", "dl_fb_filtered")

st.markdown(
    "<h1>💬 Customer Feedback & Sentiment Analysis</h1>"
    "<p style='color:gray;'>Powered by TextBlob natural language sentiment analysis</p>",
    unsafe_allow_html=True,
)

if filtered_df.empty:
    st.info("ℹ️ No records match the selected filters.")
    st.stop()

with st.spinner("Analyzing customer feedback with TextBlob..."):
    sentiment_df = analyze_feedback(filtered_df)

summary = sentiment_summary(sentiment_df)

section_header("🔑 Sentiment KPIs")
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Positive Reviews", format_number(summary["positive"]), "grad-green", "😊")
with k2:
    kpi_card("Neutral Reviews", format_number(summary["neutral"]), "grad-orange", "😐")
with k3:
    kpi_card("Negative Reviews", format_number(summary["negative"]), "grad-red", "😞")
with k4:
    kpi_card("Avg. Polarity", f"{summary['avg_polarity']:.3f}", "grad-blue", "📐")

k5, k6, k7 = st.columns(3)
with k5:
    kpi_card("Avg. Subjectivity", f"{summary['avg_subjectivity']:.3f}", "grad-purple", "🧠")
with k6:
    kpi_card("Avg. Word Count", f"{summary['avg_word_count']:.1f}", "grad-teal", "🔤")
with k7:
    total_reviews = summary["positive"] + summary["neutral"] + summary["negative"]
    kpi_card("Total Reviews", format_number(total_reviews), "grad-pink", "📝")

section_header("📊 Sentiment Overview")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(charts.sentiment_pie_chart(sentiment_df), use_container_width=True)
with c2:
    st.plotly_chart(charts.sentiment_bar_chart(sentiment_df), use_container_width=True)

st.plotly_chart(charts.polarity_histogram(sentiment_df), use_container_width=True)

section_header("🌟 Top Positive & Negative Reviews")
top_pos, top_neg = top_reviews(sentiment_df, n=5)

col_pos, col_neg = st.columns(2)
with col_pos:
    st.markdown("#### 😊 Top Positive Reviews")
    for _, row in top_pos.iterrows():
        st.success(f"**{row['Customer Name']}** ({row['Polarity']:.2f}): {row['Feedback']}")
with col_neg:
    st.markdown("#### 😞 Top Negative Reviews")
    for _, row in top_neg.iterrows():
        st.error(f"**{row['Customer Name']}** ({row['Polarity']:.2f}): {row['Feedback']}")

section_header("🗃️ Review Table")
display_cols = ["Order ID", "Customer Name", "Region", "Category", "Feedback",
                 "Polarity", "Subjectivity", "Sentiment", "Word Count"]
st.dataframe(sentiment_df[display_cols], use_container_width=True, height=400)
