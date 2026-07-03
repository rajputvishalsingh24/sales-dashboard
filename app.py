"""
app.py
------
Main entry point for the Sales Performance Dashboard.
Run with:  streamlit run app.py
"""

import os
import warnings
import streamlit as st
import pandas as pd

from utils.preprocessing import load_data, apply_filters, get_kpis
from utils.helper import (
    inject_custom_css, format_currency, format_number, kpi_card,
    section_header, sidebar_filters, download_button,
)
from utils import charts

warnings.filterwarnings("ignore")

# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

# ------------------------------------------------------------------
# SIDEBAR HEADER
# ------------------------------------------------------------------
logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)

st.sidebar.markdown(
    """
    <h2 style='text-align:center; margin-top:-10px;'>📊 Sales Dashboard</h2>
    <p style='text-align:center; color:#a0a8c0; margin-top:-10px;'>Performance & Insights</p>
    <hr style='border-color:#3a4468;'>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------------
df = load_data()

if df.empty:
    st.warning("No data available to display. Please check the `data/sales_data.csv` file.")
    st.stop()

# ------------------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------------------
region, state, category, sub_category, segment, date_range = sidebar_filters(df)

st.sidebar.markdown("<hr style='border-color:#3a4468;'>", unsafe_allow_html=True)
st.sidebar.markdown("### ⬇️ Downloads")

filtered_df = apply_filters(df, region, state, category, sub_category, segment, date_range)

download_button(filtered_df, "📥 Download Filtered Dataset", "filtered_sales_data.csv", "dl_filtered")
download_button(df, "📥 Download Full Sales Report", "sales_report.csv", "dl_full")

st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; color:#7a8399; margin-top:20px;'>"
    "Built with ❤️ using Streamlit & Plotly</p>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# MAIN HEADER
# ------------------------------------------------------------------
st.markdown(
    """
    <h1 style='margin-bottom:0;'>📈 Sales Performance Dashboard</h1>
    <p style='color:gray; margin-top:0;'>A complete overview of sales, profit and customer insights</p>
    """,
    unsafe_allow_html=True,
)

if filtered_df.empty:
    st.info("ℹ️ No records match the selected filters. Please adjust your filter selections.")
    st.stop()

# ------------------------------------------------------------------
# KPI CARDS
# ------------------------------------------------------------------
kpis = get_kpis(filtered_df)

section_header("🔑 Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total Sales", format_currency(kpis["total_sales"]), "grad-blue", "💵")
with k2:
    kpi_card("Total Profit", format_currency(kpis["total_profit"]), "grad-green", "💰")
with k3:
    kpi_card("Total Orders", format_number(kpis["orders"]), "grad-purple", "🧾")
with k4:
    kpi_card("Total Customers", format_number(kpis["customers"]), "grad-orange", "👥")

k5, k6, k7 = st.columns(3)
with k5:
    kpi_card("Avg. Sales / Order", format_currency(kpis["avg_sales"]), "grad-teal", "📊")
with k6:
    kpi_card("Avg. Profit / Order", format_currency(kpis["avg_profit"]), "grad-pink", "📈")
with k7:
    kpi_card("Avg. Discount", f"{kpis['avg_discount']*100:.1f}%", "grad-red", "🏷️")

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# TREND CHARTS
# ------------------------------------------------------------------
section_header("📈 Sales & Profit Trends")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(charts.sales_trend_chart(filtered_df), use_container_width=True)
with c2:
    st.plotly_chart(charts.profit_trend_chart(filtered_df), use_container_width=True)

st.plotly_chart(charts.revenue_trend_chart(filtered_df), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(charts.monthly_sales_chart(filtered_df), use_container_width=True)
with c4:
    st.plotly_chart(charts.monthly_profit_chart(filtered_df), use_container_width=True)

# ------------------------------------------------------------------
# CATEGORY / REGION BREAKDOWN
# ------------------------------------------------------------------
section_header("🗂️ Sales Breakdown")
c5, c6 = st.columns(2)
with c5:
    st.plotly_chart(charts.sales_by_category_chart(filtered_df), use_container_width=True)
with c6:
    st.plotly_chart(charts.sales_by_region_chart(filtered_df), use_container_width=True)

c7, c8 = st.columns(2)
with c7:
    st.plotly_chart(charts.sales_by_state_chart(filtered_df), use_container_width=True)
with c8:
    st.plotly_chart(charts.sales_by_segment_chart(filtered_df), use_container_width=True)

# ------------------------------------------------------------------
# TOP PERFORMERS
# ------------------------------------------------------------------
section_header("🏆 Top Performers")
c9, c10 = st.columns(2)
with c9:
    st.plotly_chart(charts.top_products_chart(filtered_df), use_container_width=True)
with c10:
    st.plotly_chart(charts.top_customers_chart(filtered_df), use_container_width=True)

# ------------------------------------------------------------------
# PROFIT ANALYSIS
# ------------------------------------------------------------------
section_header("💹 Profit Analysis")
c11, c12 = st.columns(2)
with c11:
    st.plotly_chart(charts.profit_by_category_chart(filtered_df), use_container_width=True)
with c12:
    st.plotly_chart(charts.profit_vs_sales_scatter(filtered_df), use_container_width=True)

st.plotly_chart(charts.discount_impact_chart(filtered_df), use_container_width=True)

# ------------------------------------------------------------------
# ADVANCED VISUALS
# ------------------------------------------------------------------
section_header("🧭 Advanced Visuals")
c13, c14 = st.columns(2)
with c13:
    st.plotly_chart(charts.sales_heatmap(filtered_df), use_container_width=True)
with c14:
    st.plotly_chart(charts.sales_treemap(filtered_df), use_container_width=True)

st.plotly_chart(charts.sales_sunburst(filtered_df), use_container_width=True)

c15, c16 = st.columns(2)
with c15:
    st.plotly_chart(charts.category_pie_chart(filtered_df), use_container_width=True)
with c16:
    st.plotly_chart(charts.region_donut_chart(filtered_df), use_container_width=True)

c17, c18 = st.columns(2)
with c17:
    st.plotly_chart(charts.sales_histogram(filtered_df), use_container_width=True)
with c18:
    st.plotly_chart(charts.profit_box_plot(filtered_df), use_container_width=True)

# ------------------------------------------------------------------
# DATA TABLE
# ------------------------------------------------------------------
section_header("🗃️ Filtered Data Preview")
st.dataframe(filtered_df.drop(columns=["Year-Month"], errors="ignore"), use_container_width=True, height=350)

st.caption(
    "💡 Use the sidebar to filter by Region, State, Category, Sub Category, Segment and Date Range. "
    "Explore **Sales Analysis**, **Customer Feedback**, **Profit Analysis** and **Regional Analysis** "
    "in the pages menu for deeper insights."
)
