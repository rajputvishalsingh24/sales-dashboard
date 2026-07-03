"""
1_Sales_Analysis.py
--------------------
Deep-dive sales analysis page.
"""

import os
import warnings
import streamlit as st

from utils.preprocessing import load_data, apply_filters, get_kpis
from utils.helper import (
    inject_custom_css, format_currency, format_number, kpi_card,
    section_header, sidebar_filters, download_button,
)
from utils import charts

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Sales Analysis", page_icon="📈", layout="wide")
inject_custom_css()

logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)
st.sidebar.markdown("<h3 style='text-align:center;'>📈 Sales Analysis</h3>", unsafe_allow_html=True)

df = load_data()
if df.empty:
    st.warning("No data available.")
    st.stop()

region, state, category, sub_category, segment, date_range = sidebar_filters(df)
filtered_df = apply_filters(df, region, state, category, sub_category, segment, date_range)

download_button(filtered_df, "📥 Download Filtered Dataset", "sales_analysis_filtered.csv", "dl_sa_filtered")

st.markdown(
    "<h1>📈 Sales Analysis</h1><p style='color:gray;'>Detailed breakdown of sales performance</p>",
    unsafe_allow_html=True,
)

if filtered_df.empty:
    st.info("ℹ️ No records match the selected filters.")
    st.stop()

kpis = get_kpis(filtered_df)
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total Sales", format_currency(kpis["total_sales"]), "grad-blue", "💵")
with k2:
    kpi_card("Total Orders", format_number(kpis["orders"]), "grad-purple", "🧾")
with k3:
    kpi_card("Avg. Sales / Order", format_currency(kpis["avg_sales"]), "grad-teal", "📊")
with k4:
    kpi_card("Total Quantity", format_number(filtered_df["Quantity"].sum()), "grad-orange", "📦")

section_header("📈 Sales Trends")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(charts.sales_trend_chart(filtered_df), use_container_width=True)
with c2:
    st.plotly_chart(charts.revenue_trend_chart(filtered_df), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(charts.monthly_sales_chart(filtered_df), use_container_width=True)
with c4:
    st.plotly_chart(charts.sales_histogram(filtered_df), use_container_width=True)

section_header("🗂️ Category & Product Insights")
c5, c6 = st.columns(2)
with c5:
    st.plotly_chart(charts.sales_by_category_chart(filtered_df), use_container_width=True)
with c6:
    st.plotly_chart(charts.category_pie_chart(filtered_df), use_container_width=True)

st.plotly_chart(charts.top_products_chart(filtered_df, top_n=10), use_container_width=True)

section_header("🌳 Hierarchical View")
c7, c8 = st.columns(2)
with c7:
    st.plotly_chart(charts.sales_treemap(filtered_df), use_container_width=True)
with c8:
    st.plotly_chart(charts.sales_sunburst(filtered_df), use_container_width=True)

section_header("👥 Segment & Customer Insights")
c9, c10 = st.columns(2)
with c9:
    st.plotly_chart(charts.sales_by_segment_chart(filtered_df), use_container_width=True)
with c10:
    st.plotly_chart(charts.top_customers_chart(filtered_df), use_container_width=True)

section_header("🗃️ Sales Data")
st.dataframe(filtered_df.drop(columns=["Year-Month"], errors="ignore"), use_container_width=True, height=350)
