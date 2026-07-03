"""
helper.py
---------
UI helpers: custom CSS, gradient KPI cards, number formatting,
and shared sidebar filter widgets.
"""

import streamlit as st
import pandas as pd


def inject_custom_css():
    """Inject professional custom CSS for a modern, responsive dashboard look."""
    st.markdown(
        """
        <style>
        .main { background-color: #f5f7fa; }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .kpi-card {
            border-radius: 16px;
            padding: 20px 18px;
            color: white;
            text-align: left;
            box-shadow: 0 4px 14px rgba(0,0,0,0.15);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 10px;
        }
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }
        .kpi-title {
            font-size: 14px;
            font-weight: 600;
            opacity: 0.9;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 26px;
            font-weight: 800;
        }

        .grad-blue   { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .grad-purple { background: linear-gradient(135deg, #7f7fd5 0%, #86a8e7 50%, #91eae4 100%); }
        .grad-green  { background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); }
        .grad-orange { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); }
        .grad-pink   { background: linear-gradient(135deg, #f857a6 0%, #ff5858 100%); }
        .grad-teal   { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
        .grad-red    { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }

        section[data-testid="stSidebar"] {
            background-color: #1c2333;
        }
        section[data-testid="stSidebar"] * {
            color: #f0f2f6 !important;
        }

        .section-header {
            font-size: 22px;
            font-weight: 700;
            margin-top: 18px;
            margin-bottom: 8px;
            color: #1c2333;
            border-left: 5px solid #4facfe;
            padding-left: 10px;
        }

        div[data-testid="stMetric"] {
            background-color: white;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_currency(value: float) -> str:
    if value is None:
        return "$0"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"${value/1_000:,.1f}K"
    return f"${value:,.2f}"


def format_number(value: float) -> str:
    if value is None:
        return "0"
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"{value/1_000:,.1f}K"
    return f"{value:,.0f}"


def kpi_card(title: str, value: str, gradient_class: str, icon: str = "📊"):
    st.markdown(
        f"""
        <div class="kpi-card {gradient_class}">
            <div class="kpi-title">{icon} {title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(text: str):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def sidebar_filters(df: pd.DataFrame):
    """Render sidebar filters and return the selected values."""
    st.sidebar.markdown("### 🔎 Filters")

    def multiselect_with_all(label, options, key):
        options = sorted(options)
        selected = st.sidebar.multiselect(label, ["All"] + options, default=["All"], key=key)
        return selected

    region = multiselect_with_all("Region", df["Region"].unique().tolist(), "flt_region")
    state = multiselect_with_all("State", df["State"].unique().tolist(), "flt_state")
    category = multiselect_with_all("Category", df["Category"].unique().tolist(), "flt_category")
    sub_category = multiselect_with_all("Sub Category", df["Sub Category"].unique().tolist(), "flt_subcategory")
    segment = multiselect_with_all("Segment", df["Segment"].unique().tolist(), "flt_segment")

    min_date = df["Order Date"].min()
    max_date = df["Order Date"].max()
    date_range = st.sidebar.date_input(
        "Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="flt_date",
    )

    col1, col2 = st.sidebar.columns(2)
    with col1:
        reset = st.button("🔄 Reset Filters", use_container_width=True)
    with col2:
        pass

    if reset:
        for key in ["flt_region", "flt_state", "flt_category", "flt_subcategory", "flt_segment", "flt_date"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    return region, state, category, sub_category, segment, date_range


def download_button(df: pd.DataFrame, label: str, filename: str, key: str):
    csv = df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
        key=key,
    )
