import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

from dashboard.sales_analysis import *
from dashboard.customer_analysis import *
from dashboard.product_analysis import *
from dashboard.ai_insights import generate_insights
from dashboard.sales_forecasting import forecast_sales
from dashboard.customer_segmentation import segment_customers
from dashboard.rfm_analysis import calculate_rfm
from dashboard.growth_analysis import revenue_growth

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 E-Commerce Sales Analytics Dashboard")
st.markdown("---")

# ---------------------------
# LOAD DATA
# ---------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/ecommerce_sales.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------

st.sidebar.header("🔍 Filters")

# Category Filter
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# State Filter
state_filter = st.sidebar.multiselect(
    "Select State",
    options=df["State"].unique(),
    default=df["State"].unique()
)

# Product Filter
product_filter = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# Date Filter
min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply Filters
filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["State"].isin(state_filter)) &
    (df["Product"].isin(product_filter))
]

# Date filter apply only if both dates selected
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order_Date"] >= pd.to_datetime(start_date)) &
        (filtered_df["Order_Date"] <= pd.to_datetime(end_date))
    ]

# ---------------------------
# KPI SECTION
# ---------------------------

sales_metrics = get_sales_metrics(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Revenue",
    f"₹{sales_metrics['total_revenue']:,.0f}"
)

col2.metric(
    "Profit",
    f"₹{sales_metrics['total_profit']:,.0f}"
)

col3.metric(
    "Orders",
    sales_metrics['total_orders']
)

col4.metric(
    "AOV",
    f"₹{sales_metrics['average_order_value']:,.0f}"
)

col5.metric(
    "Profit Margin",
    f"{sales_metrics['profit_margin']}%"
)

st.markdown("---")

# ---------------------------
# SALES TREND
# ---------------------------

st.subheader("📈 Monthly Sales Trend")

monthly_sales = monthly_sales_trend(filtered_df)

fig_sales = px.line(
    monthly_sales,
    x="Order_Date",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig_sales, use_container_width=True)

# ---------------------------
# CATEGORY SALES
# ---------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🛒 Category-wise Revenue")

    category_df = category_sales(filtered_df)

    fig_category = px.bar(
        category_df,
        x="Category",
        y="Revenue",
        text_auto=True
    )

    st.plotly_chart(fig_category, use_container_width=True)

with col2:

    st.subheader("💳 Payment Method Analysis")

    payment_df = payment_method_sales(filtered_df)

    fig_payment = px.pie(
        payment_df,
        names="Payment_Method",
        values="Revenue",
        hole=0.5
    )

    st.plotly_chart(fig_payment, use_container_width=True)

# ---------------------------
# TOP PRODUCTS
# ---------------------------

st.subheader("🏆 Top Selling Products")

top_products = top_selling_products(filtered_df)

fig_top_products = px.bar(
    top_products,
    x="Product",
    y="Revenue",
    text_auto=True
)

st.plotly_chart(fig_top_products, use_container_width=True)

# ---------------------------
# CUSTOMER ANALYSIS
# ---------------------------

st.subheader("👥 Customer Analysis")

customer_df = new_vs_returning_customers(filtered_df)

fig_customer = px.pie(
    customer_df,
    names="Customer Type",
    values="Count",
    hole=0.4
)

st.plotly_chart(fig_customer, use_container_width=True)

# ---------------------------
# TOP CUSTOMERS
# ---------------------------

st.subheader("⭐ Top Customers")

top_customers_df = top_10_customers(filtered_df)

fig_customers = px.bar(
    top_customers_df,
    x="Customer_Name",
    y="Revenue",
    text_auto=True
)

st.plotly_chart(fig_customers, use_container_width=True)

# ---------------------------
# STATE-WISE SALES
# ---------------------------

st.subheader("🌍 State-wise Revenue")

state_df = state_wise_sales(filtered_df)

fig_state = px.bar(
    state_df,
    x="State",
    y="Revenue",
    text_auto=True
)

st.plotly_chart(fig_state, use_container_width=True)

# ---------------------------
# DATA PREVIEW
# ---------------------------

st.subheader("📋 Dataset Preview")

# ---------------------------
# DOWNLOAD REPORT SECTION
# ---------------------------

st.markdown("---")
st.subheader("📥 Download Reports")

# CSV Download
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV Report",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)

# Excel Download
excel_file = BytesIO()

with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
    filtered_df.to_excel(writer, index=False, sheet_name="Sales Report")

st.download_button(
    label="📊 Download Excel Report",
    data=excel_file.getvalue(),
    file_name="sales_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.dataframe(filtered_df)

# ---------------------------
# AI BUSINESS INSIGHTS
# ---------------------------

st.markdown("---")
st.subheader("🤖 AI Business Insights")

insights = generate_insights(filtered_df)

for insight in insights:
    st.success(insight)
# ---------------------------
# SALES FORECASTING
# ---------------------------

st.markdown("---")
st.subheader("📈 Sales Forecasting")

monthly_sales, predicted_sales = forecast_sales(filtered_df)

st.metric(
    "Predicted Next Month Revenue",
    f"₹{predicted_sales:,.0f}"
)

import plotly.express as px

fig_forecast = px.line(
    monthly_sales,
    x="Order_Date",
    y="Revenue",
    markers=True,
    title="Historical Monthly Revenue"
)

st.plotly_chart(fig_forecast, width="stretch")

# ---------------------------
# CUSTOMER SEGMENTATION
# ---------------------------

st.markdown("---")
st.subheader("👥 Customer Segmentation (AI)")

segmented_df = segment_customers(filtered_df)

cluster_counts = (
    segmented_df["Cluster"]
    .value_counts()
    .reset_index()
)

cluster_counts.columns = [
    "Customer Segment",
    "Count"
]

fig_segment = px.pie(
    cluster_counts,
    names="Customer Segment",
    values="Count",
    hole=0.4
)

st.plotly_chart(
    fig_segment,
    width="stretch"
)

st.dataframe(
    segmented_df.head(20),
    width="stretch"
)

# ---------------------------
# RFM ANALYSIS
# ---------------------------

st.markdown("---")
st.subheader("🎯 RFM Analysis")

rfm_df = calculate_rfm(filtered_df)

st.dataframe(
    rfm_df.head(20),
    width="stretch"
)

st.metric(
    "Total Customers Analyzed",
    len(rfm_df)
)

rfm_counts = (
    rfm_df["Customer_Type"]
    .value_counts()
    .reset_index()
)

rfm_counts.columns = [
    "Customer Type",
    "Count"
]

fig_rfm = px.pie(
    rfm_counts,
    names="Customer Type",
    values="Count",
    hole=0.4
)

st.plotly_chart(
    fig_rfm,
    width="stretch"
)

# ---------------------------
# GROWTH ANALYSIS
# ---------------------------

st.markdown("---")
st.subheader("📈 Business Growth Analysis")

revenue_g, profit_g, order_g = revenue_growth(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Revenue Growth %",
    f"{revenue_g}%"
)

col2.metric(
    "Profit Growth %",
    f"{profit_g}%"
)

col3.metric(
    "Order Growth %",
    f"{order_g}%"
)

# ---------------------------
# FOOTER
# ---------------------------

st.markdown("---")
st.markdown(
    "Developed by **Ankit Kumar** | E-Commerce Sales Analytics Dashboard 🚀"
)