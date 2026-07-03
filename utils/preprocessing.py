"""
preprocessing.py
-----------------
Data loading, validation, cleaning and filtering utilities for the
Sales Dashboard application.
"""

import os
import warnings
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")

REQUIRED_COLUMNS = [
    "Order ID", "Order Date", "Region", "State", "City", "Category",
    "Sub Category", "Product Name", "Quantity", "Sales", "Profit",
    "Discount", "Customer Name", "Customer ID", "Segment", "Feedback",
]

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sales_data.csv")


@st.cache_data(show_spinner=False)
def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """
    Load, validate and clean the sales dataset.

    Handles:
        - Missing file
        - Empty dataset
        - Wrong / missing column names
        - Invalid dates
        - Missing values
    """
    if not os.path.exists(path):
        st.error(f"⚠️ Data file not found at: `{path}`. Please make sure "
                  f"`sales_data.csv` exists inside the `data/` folder.")
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        st.error("⚠️ The dataset file is empty. Please provide a valid CSV file.")
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    except Exception as e:
        st.error(f"⚠️ Could not read the dataset: {e}")
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    if df.empty:
        st.error("⚠️ The dataset contains no rows.")
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        st.error(f"⚠️ The dataset is missing required column(s): {', '.join(missing_cols)}")
        for c in missing_cols:
            df[c] = pd.NA

    # ---- Clean dates ----
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    invalid_dates = df["Order Date"].isna().sum()
    if invalid_dates > 0:
        df = df.dropna(subset=["Order Date"])

    # ---- Clean numeric columns ----
    numeric_cols = ["Quantity", "Sales", "Profit", "Discount"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(0)

    # ---- Clean text columns ----
    text_cols = ["Region", "State", "City", "Category", "Sub Category",
                 "Product Name", "Customer Name", "Customer ID", "Segment", "Feedback"]
    for col in text_cols:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()

    df["Feedback"] = df["Feedback"].replace("", "No feedback provided")

    # ---- Derived columns ----
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Profit Margin"] = df.apply(
        lambda r: (r["Profit"] / r["Sales"] * 100) if r["Sales"] != 0 else 0, axis=1
    )

    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    return df


def apply_filters(df: pd.DataFrame, region, state, category, sub_category,
                   segment, date_range) -> pd.DataFrame:
    """Apply sidebar filter selections to the dataframe."""
    filtered = df.copy()

    if region and "All" not in region:
        filtered = filtered[filtered["Region"].isin(region)]
    if state and "All" not in state:
        filtered = filtered[filtered["State"].isin(state)]
    if category and "All" not in category:
        filtered = filtered[filtered["Category"].isin(category)]
    if sub_category and "All" not in sub_category:
        filtered = filtered[filtered["Sub Category"].isin(sub_category)]
    if segment and "All" not in segment:
        filtered = filtered[filtered["Segment"].isin(segment)]

    if date_range and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[(filtered["Order Date"] >= start) & (filtered["Order Date"] <= end)]

    return filtered


def get_kpis(df: pd.DataFrame) -> dict:
    """Compute top-level KPI metrics from a (filtered) dataframe."""
    if df.empty:
        return {
            "total_sales": 0, "total_profit": 0, "orders": 0, "customers": 0,
            "avg_sales": 0, "avg_profit": 0, "avg_discount": 0,
        }

    return {
        "total_sales": df["Sales"].sum(),
        "total_profit": df["Profit"].sum(),
        "orders": df["Order ID"].nunique(),
        "customers": df["Customer ID"].nunique(),
        "avg_sales": df["Sales"].mean(),
        "avg_profit": df["Profit"].mean(),
        "avg_discount": df["Discount"].mean(),
    }
