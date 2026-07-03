# 📊 Sales Performance Dashboard

A complete, interactive, multi-page **Streamlit** sales analytics dashboard with **Plotly** visualizations and **TextBlob**-powered customer sentiment analysis.

---

## 🚀 Project Overview

This dashboard analyzes a realistic retail sales dataset (1,600+ orders) covering sales, profit, discounts, regions, products, customers, and customer feedback. It combines business KPIs, trend analysis, and NLP-based sentiment analysis into one professional, filterable dashboard.

---

## ✨ Features

- **Multi-page Streamlit app**: Overview, Sales Analysis, Customer Feedback, Profit Analysis, Regional Analysis
- **Global sidebar filters**: Region, State, Category, Sub Category, Segment, Date Range — applied consistently across every page
- **7 KPI cards**: Total Sales, Total Profit, Orders, Customers, Avg Sales, Avg Profit, Avg Discount
- **20+ Plotly charts**: line, area, bar, pie, donut, treemap, sunburst, heatmap, scatter, histogram, box plot, choropleth map
- **TextBlob sentiment analysis** on customer feedback: Polarity, Subjectivity, Sentiment label (Positive/Neutral/Negative), Top positive/negative reviews
- **Downloadable CSVs**: filtered dataset and full sales report from the sidebar
- **Modern UI**: gradient KPI cards, hover effects, rounded corners, custom CSS, wide responsive layout
- **Robust error handling**: missing file, empty dataset, wrong columns, invalid dates, missing values

---

## 📁 Folder Structure

```
Sales_Dashboard/
│
├── app.py                       # Main dashboard (Overview page)
├── requirements.txt
├── README.md
│
├── assets/
│   └── logo.png                 # Sidebar logo
│
├── data/
│   └── sales_data.csv           # Generated sales dataset (1,600+ rows)
│
├── pages/
│   ├── 1_Sales_Analysis.py
│   ├── 2_Customer_Feedback.py
│   ├── 3_Profit_Analysis.py
│   └── 4_Regional_Analysis.py
│
├── utils/
│   ├── helper.py                # CSS, KPI cards, sidebar filters, formatting
│   ├── charts.py                # All Plotly chart-building functions
│   ├── preprocessing.py         # Data loading, cleaning, filtering
│   └── sentiment.py             # TextBlob sentiment analysis
│
└── screenshots/
    └── dashboard.png            # Add your own screenshot here after running the app
```

---

## 🛠️ Installation & Setup (Visual Studio Code)

### 1. Create the project folder and open it in VS Code
Copy the `Sales_Dashboard` folder to your machine, then in VS Code:
`File → Open Folder... → Sales_Dashboard`

### 2. Create a virtual environment

**Windows (Command Prompt / PowerShell):**
```bash
python -m venv venv
```

**Mac / Linux:**
```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

### 4. Install the required packages
```bash
pip install -r requirements.txt
```

The first time TextBlob is used it may need its NLTK corpora. If sentiment analysis raises a corpora error, run:
```bash
python -m textblob.download_corpora
```

### 5. Run the application
```bash
streamlit run app.py
```

### 6. Open the dashboard
Streamlit will automatically open your browser at:
```
http://localhost:8501
```
If it doesn't open automatically, copy that URL into your browser manually.

---

## 🖥️ What Appears on Localhost

- **Sidebar** — logo, title, filters (Region, State, Category, Sub Category, Segment, Date Range), Reset Filters button, and CSV download buttons
- **Overview page** — 7 KPI cards, trend charts, category/region breakdowns, top performers, profit analysis, and advanced visuals (heatmap, treemap, sunburst)
- **Sales Analysis page** — deeper sales trend, category, and customer breakdowns
- **Customer Feedback page** — TextBlob sentiment KPIs, sentiment pie/bar/histogram charts, top positive & negative reviews, and a full review table
- **Profit Analysis page** — profit KPIs, profit trend/margin, profitable and loss-making products
- **Regional Analysis page** — region/state/city sales, a US choropleth sales map, and top cities

All KPIs and charts update dynamically based on the sidebar filter selections.

---

## 📸 Screenshots

Run the app locally and save a screenshot of the browser window as:
```
screenshots/dashboard.png
```

---

## 🔮 Future Improvements

- Add authentication / multi-user support
- Connect to a live database (PostgreSQL / SQL Server) instead of a static CSV
- Add forecasting (Prophet / ARIMA) for sales prediction
- Add export-to-PDF report generation
- Add more granular geographic mapping (city-level coordinates)
- Add caching layer / async data refresh for large datasets

---

## 📦 Tech Stack

`Python 3.12+` · `Streamlit` · `Pandas` · `NumPy` · `Plotly Express & Graph Objects` · `TextBlob` · `Matplotlib` · `OpenPyXL`
