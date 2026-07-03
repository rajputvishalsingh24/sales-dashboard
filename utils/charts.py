"""
charts.py
---------
Reusable Plotly chart-building functions for the Sales Dashboard.
All charts are built with Plotly Express / Plotly Graph Objects only.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

TEMPLATE = "plotly_white"
COLOR_SEQUENCE = px.colors.qualitative.Vivid


def _empty_fig(message: str = "No data available for the selected filters"):
    fig = go.Figure()
    fig.add_annotation(text=message, x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="gray"))
    fig.update_layout(template=TEMPLATE, xaxis={"visible": False}, yaxis={"visible": False}, height=350)
    return fig


def sales_trend_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    trend = df.groupby("Year-Month", as_index=False)["Sales"].sum().sort_values("Year-Month")
    fig = px.line(trend, x="Year-Month", y="Sales", markers=True, template=TEMPLATE,
                   title="📈 Sales Trend Over Time", color_discrete_sequence=COLOR_SEQUENCE)
    fig.update_traces(line=dict(width=3))
    return fig


def profit_trend_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    trend = df.groupby("Year-Month", as_index=False)["Profit"].sum().sort_values("Year-Month")
    fig = px.area(trend, x="Year-Month", y="Profit", template=TEMPLATE,
                   title="💰 Profit Trend Over Time", color_discrete_sequence=COLOR_SEQUENCE)
    return fig


def revenue_trend_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    trend = df.groupby("Year-Month", as_index=False).agg({"Sales": "sum", "Profit": "sum"}).sort_values("Year-Month")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trend["Year-Month"], y=trend["Sales"], name="Sales", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=trend["Year-Month"], y=trend["Profit"], name="Profit", mode="lines+markers"))
    fig.update_layout(template=TEMPLATE, title="💵 Revenue vs Profit Trend")
    return fig


def monthly_sales_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    monthly = df.groupby("Month Name", as_index=False)["Sales"].sum()
    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly["Month Name"] = pd.Categorical(monthly["Month Name"], categories=order, ordered=True)
    monthly = monthly.sort_values("Month Name")
    fig = px.bar(monthly, x="Month Name", y="Sales", template=TEMPLATE, title="📅 Monthly Sales",
                 color="Sales", color_continuous_scale="Blues")
    return fig


def monthly_profit_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    monthly = df.groupby("Month Name", as_index=False)["Profit"].sum()
    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly["Month Name"] = pd.Categorical(monthly["Month Name"], categories=order, ordered=True)
    monthly = monthly.sort_values("Month Name")
    fig = px.bar(monthly, x="Month Name", y="Profit", template=TEMPLATE, title="📅 Monthly Profit",
                 color="Profit", color_continuous_scale="Greens")
    return fig


def sales_by_category_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    data = df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(data, x="Category", y="Sales", template=TEMPLATE, title="🗂️ Sales by Category",
                 color="Category", color_discrete_sequence=COLOR_SEQUENCE, text_auto=".2s")
    return fig


def sales_by_region_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    data = df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(data, x="Region", y="Sales", template=TEMPLATE, title="🌍 Sales by Region",
                 color="Region", color_discrete_sequence=COLOR_SEQUENCE, text_auto=".2s")
    return fig


def sales_by_state_chart(df: pd.DataFrame, top_n: int = 15):
    if df.empty:
        return _empty_fig()
    data = df.groupby("State", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(top_n)
    fig = px.bar(data, x="Sales", y="State", orientation="h", template=TEMPLATE,
                 title=f"🏙️ Top {top_n} States by Sales", color="Sales", color_continuous_scale="Purples")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def sales_by_segment_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    data = df.groupby("Segment", as_index=False)["Sales"].sum()
    fig = px.pie(data, names="Segment", values="Sales", template=TEMPLATE, title="🧩 Sales by Segment",
                 hole=0.0, color_discrete_sequence=COLOR_SEQUENCE)
    return fig


def top_products_chart(df: pd.DataFrame, top_n: int = 10):
    if df.empty:
        return _empty_fig()
    data = df.groupby("Product Name", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(top_n)
    fig = px.bar(data, x="Sales", y="Product Name", orientation="h", template=TEMPLATE,
                 title=f"🏆 Top {top_n} Products by Sales", color="Sales", color_continuous_scale="Teal")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def top_customers_chart(df: pd.DataFrame, top_n: int = 10):
    if df.empty:
        return _empty_fig()
    data = df.groupby("Customer Name", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(top_n)
    fig = px.bar(data, x="Sales", y="Customer Name", orientation="h", template=TEMPLATE,
                 title=f"👤 Top {top_n} Customers", color="Sales", color_continuous_scale="Oranges")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def profit_by_category_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    data = df.groupby("Category", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)
    fig = px.bar(data, x="Category", y="Profit", template=TEMPLATE, title="💹 Profit by Category",
                 color="Profit", color_continuous_scale="RdYlGn")
    return fig


def profit_vs_sales_scatter(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    fig = px.scatter(df, x="Sales", y="Profit", color="Category", size="Quantity",
                      hover_data=["Product Name", "Region"], template=TEMPLATE,
                      title="🔎 Profit vs Sales", color_discrete_sequence=COLOR_SEQUENCE)
    return fig


def discount_impact_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    fig = px.scatter(df, x="Discount", y="Profit", color="Category", template=TEMPLATE,
                      title="🏷️ Discount Impact on Profit", trendline=None,
                      color_discrete_sequence=COLOR_SEQUENCE)
    return fig


def sales_heatmap(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    pivot = df.pivot_table(index="Category", columns="Region", values="Sales", aggfunc="sum", fill_value=0)
    fig = px.imshow(pivot, template=TEMPLATE, title="🔥 Sales Heatmap (Category vs Region)",
                     color_continuous_scale="YlOrRd", text_auto=".2s", aspect="auto")
    return fig


def sales_treemap(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    fig = px.treemap(df, path=["Region", "Category", "Sub Category"], values="Sales",
                      template=TEMPLATE, title="🌳 Sales Treemap", color="Sales",
                      color_continuous_scale="Blues")
    return fig


def sales_sunburst(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    fig = px.sunburst(df, path=["Region", "Category", "Sub Category"], values="Sales",
                       template=TEMPLATE, title="☀️ Sales Sunburst", color="Sales",
                       color_continuous_scale="Sunset")
    return fig


def category_pie_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    data = df.groupby("Category", as_index=False)["Sales"].sum()
    fig = px.pie(data, names="Category", values="Sales", template=TEMPLATE, title="🥧 Category Share (Pie)",
                 color_discrete_sequence=COLOR_SEQUENCE)
    return fig


def region_donut_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    data = df.groupby("Region", as_index=False)["Sales"].sum()
    fig = px.pie(data, names="Region", values="Sales", hole=0.5, template=TEMPLATE,
                 title="🍩 Region Share (Donut)", color_discrete_sequence=COLOR_SEQUENCE)
    return fig


def sales_histogram(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    fig = px.histogram(df, x="Sales", nbins=40, template=TEMPLATE, title="📊 Sales Distribution",
                        color_discrete_sequence=COLOR_SEQUENCE)
    return fig


def profit_box_plot(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    fig = px.box(df, x="Category", y="Profit", template=TEMPLATE, title="📦 Profit Distribution by Category",
                 color="Category", color_discrete_sequence=COLOR_SEQUENCE)
    return fig


def sentiment_pie_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    data = df["Sentiment"].value_counts().reset_index()
    data.columns = ["Sentiment", "Count"]
    color_map = {"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"}
    fig = px.pie(data, names="Sentiment", values="Count", template=TEMPLATE, title="🥧 Sentiment Distribution",
                 color="Sentiment", color_discrete_map=color_map)
    return fig


def sentiment_bar_chart(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    data = df["Sentiment"].value_counts().reset_index()
    data.columns = ["Sentiment", "Count"]
    color_map = {"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"}
    fig = px.bar(data, x="Sentiment", y="Count", template=TEMPLATE, title="📊 Sentiment Count",
                 color="Sentiment", color_discrete_map=color_map, text_auto=True)
    return fig


def polarity_histogram(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    fig = px.histogram(df, x="Polarity", nbins=30, template=TEMPLATE, title="📊 Polarity Score Distribution",
                        color_discrete_sequence=["#3498db"])
    return fig


def region_sales_bar(df: pd.DataFrame):
    return sales_by_region_chart(df)


def city_sales_chart(df: pd.DataFrame, top_n: int = 15):
    if df.empty:
        return _empty_fig()
    data = df.groupby("City", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(top_n)
    fig = px.bar(data, x="City", y="Sales", template=TEMPLATE, title=f"🏙️ Top {top_n} Cities by Sales",
                 color="Sales", color_continuous_scale="Cividis")
    return fig


def profit_margin_trend(df: pd.DataFrame):
    if df.empty:
        return _empty_fig()
    trend = df.groupby("Year-Month", as_index=False)["Profit Margin"].mean().sort_values("Year-Month")
    fig = px.line(trend, x="Year-Month", y="Profit Margin", markers=True, template=TEMPLATE,
                   title="📐 Average Profit Margin Trend (%)", color_discrete_sequence=["#9b59b6"])
    return fig
