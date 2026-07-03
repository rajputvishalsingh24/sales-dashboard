"""
3_Profit_Analysis.py
----------------------
Profit-focused analysis page.
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

st.set_page_config(page_title="Profit Analysis", page_icon="💰", layout="wide")
inject_custom_css()

logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)
st.sidebar.markdown("<h3 style='text-align:center;'>💰 Profit Analysis</h3>", unsafe_allow_html=True)

df = load_data()
if df.empty:
    st.warning("No data available.")
    st.stop()

region, state, category, sub_category, segment, date_range = sidebar_filters(df)
filtered_df = apply_filters(df, region, state, category, sub_category, segment, date_range)

download_button(filtered_df, "📥 Download Filtered Dataset", "profit_analysis_filtered.csv", "dl_pa_filtered")

st.markdown(
    "<h1>💰 Profit Analysis</h1><p style='color:gray;'>Profitability, margins and loss-making products</p>",
    unsafe_allow_html=True,
)

if filtered_df.empty:
    st.info("ℹ️ No records match the selected filters.")
    st.stop()

kpis = get_kpis(filtered_df)

section_header("🔑 Profit KPIs")
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total Profit", format_currency(kpis["total_profit"]), "grad-green", "💰")
with k2:
    kpi_card("Avg. Profit / Order", format_currency(kpis["avg_profit"]), "grad-blue", "📈")
with k3:
    avg_margin = filtered_df["Profit Margin"].mean()
    kpi_card("Avg. Profit Margin", f"{avg_margin:.1f}%", "grad-purple", "📐")
with k4:
    loss_orders = int((filtered_df["Profit"] < 0).sum())
    kpi_card("Loss-Making Orders", format_number(loss_orders), "grad-red", "⚠️")

section_header("📈 Profit Trends")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(charts.profit_trend_chart(filtered_df), use_container_width=True)
with c2:
    st.plotly_chart(charts.profit_margin_trend(filtered_df), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.plotly_chart(charts.monthly_profit_chart(filtered_df), use_container_width=True)
with c4:
    st.plotly_chart(charts.profit_by_category_chart(filtered_df), use_container_width=True)

section_header("🔎 Profit Relationships")
c5, c6 = st.columns(2)
with c5:
    st.plotly_chart(charts.profit_vs_sales_scatter(filtered_df), use_container_width=True)
with c6:
    st.plotly_chart(charts.discount_impact_chart(filtered_df), use_container_width=True)

st.plotly_chart(charts.profit_box_plot(filtered_df), use_container_width=True)

section_header("🏆 Most Profitable Products")
top_profit = (
    filtered_df.groupby("Product Name", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
    .head(10)
)
st.dataframe(top_profit, use_container_width=True)

section_header("⚠️ Loss-Making Products")
loss_products = (
    filtered_df.groupby("Product Name", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=True)
)
loss_products = loss_products[loss_products["Profit"] < 0].head(10)
if loss_products.empty:
    st.success("✅ No loss-making products found for the selected filters.")
else:
    st.dataframe(loss_products, use_container_width=True)
