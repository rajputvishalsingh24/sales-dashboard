"""
4_Regional_Analysis.py
------------------------
Region / State / City level sales analysis page.
"""

import os
import warnings
import streamlit as st
import plotly.express as px

from utils.preprocessing import load_data, apply_filters, get_kpis
from utils.helper import (
    inject_custom_css, format_currency, format_number, kpi_card,
    section_header, sidebar_filters, download_button,
)
from utils import charts

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Regional Analysis", page_icon="🌍", layout="wide")
inject_custom_css()

logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)
st.sidebar.markdown("<h3 style='text-align:center;'>🌍 Regional Analysis</h3>", unsafe_allow_html=True)

df = load_data()
if df.empty:
    st.warning("No data available.")
    st.stop()

region, state, category, sub_category, segment, date_range = sidebar_filters(df)
filtered_df = apply_filters(df, region, state, category, sub_category, segment, date_range)

download_button(filtered_df, "📥 Download Filtered Dataset", "regional_analysis_filtered.csv", "dl_ra_filtered")

st.markdown(
    "<h1>🌍 Regional Analysis</h1><p style='color:gray;'>Sales performance across regions, states and cities</p>",
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
    kpi_card("Regions Covered", format_number(filtered_df["Region"].nunique()), "grad-purple", "🌍")
with k3:
    kpi_card("States Covered", format_number(filtered_df["State"].nunique()), "grad-teal", "🗺️")
with k4:
    kpi_card("Cities Covered", format_number(filtered_df["City"].nunique()), "grad-orange", "🏙️")

section_header("🌍 Region-Wise Sales")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(charts.sales_by_region_chart(filtered_df), use_container_width=True)
with c2:
    st.plotly_chart(charts.region_donut_chart(filtered_df), use_container_width=True)

section_header("🗺️ State-Wise Sales")
st.plotly_chart(charts.sales_by_state_chart(filtered_df, top_n=15), use_container_width=True)

section_header("🏙️ City-Wise Sales")
st.plotly_chart(charts.city_sales_chart(filtered_df, top_n=15), use_container_width=True)

section_header("🗺️ Sales Map (US States)")
try:
    state_abbrev = {
        "California": "CA", "Washington": "WA", "Oregon": "OR", "Nevada": "NV",
        "New York": "NY", "Massachusetts": "MA", "Pennsylvania": "PA", "Florida": "FL",
        "Texas": "TX", "Illinois": "IL", "Ohio": "OH", "Michigan": "MI",
        "Georgia": "GA", "North Carolina": "NC", "Tennessee": "TN", "Louisiana": "LA",
    }
    map_data = filtered_df.groupby("State", as_index=False)["Sales"].sum()
    map_data["Code"] = map_data["State"].map(state_abbrev)
    map_data = map_data.dropna(subset=["Code"])

    if not map_data.empty:
        fig_map = px.choropleth(
            map_data, locations="Code", locationmode="USA-states", color="Sales",
            scope="usa", color_continuous_scale="Blues", title="🗺️ Sales by State (Map)",
            hover_name="State",
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("ℹ️ Map view unavailable for the current state selection.")
except Exception as e:
    st.info(f"ℹ️ Map could not be rendered: {e}")

section_header("🏆 Top Cities")
top_cities = (
    filtered_df.groupby(["City", "State", "Region"], as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)
st.dataframe(top_cities, use_container_width=True)
