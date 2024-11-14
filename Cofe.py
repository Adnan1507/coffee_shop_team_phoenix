# Import Streamlit and other necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import customer

# Configure page layout
st.set_page_config(
    page_title="Enhanced Coffee Shop Sales Dashboard",
    page_icon="☕",
    layout="wide"
)

# Custom CSS to change the background color and adjust spacing between KPI sections
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;  /* Light grey background */
    }
    .kpi-container {
        padding: 10px;
    }
    .kpi {
        border: 2px solid;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
df = pd.read_excel('coffee_shop.xlsx')
df2 = pd.read_csv('New_data.csv')
df2['transaction_date'] = pd.to_datetime(df2['transaction_date'])

# Sidebar Navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["📈 Overview", "🧍 Customer Behaviour", "💸 Pricing Strategy", "📅 Future Demands"]
)

# Sidebar Filters for Store Location and Date Range
st.sidebar.title("Filter Options")
locations = df2['store_location'].unique()
selected_locations = st.sidebar.multiselect("Select Store Locations", locations, default=locations)

min_date = df2['transaction_date'].min()
max_date = df2['transaction_date'].max()
selected_date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Filter data based on selections
filtered_df2 = df2[
    (df2['store_location'].isin(selected_locations)) &
    (df2['transaction_date'] >= pd.to_datetime(selected_date_range[0])) &
    (df2['transaction_date'] <= pd.to_datetime(selected_date_range[1]))
    ]

# Header Section
st.title("☕ Enhanced Coffee Shop Sales Dashboard")
st.write("An interactive dashboard to explore coffee shop sales performance across various locations and products.")

# Display KPIs and Pie Chart in the Overview Section
if page == "📈 Overview":
    st.header("🔍 Key Performance Indicators")

    # Create two columns for KPIs and the pie chart
    col1, col2 = st.columns([1, 1])

    # Left column for KPIs
    with col1:
        st.markdown("""
        <div class="kpi-container">
            <div class="kpi" style="border-color: green;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="font-size: 24px; color: green; margin: 0;">Total Sales Revenue</h2>
                    <h1 style="font-size: 36px; color: green; margin: 0;">$698,812.33</h1>
                </div>
            </div>
            <div class="kpi" style="border-color: blue;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="font-size: 24px; color: blue; margin: 0;">Total Orders</h2>
                    <h1 style="font-size: 36px; color: blue; margin: 0;">149,116</h1>
                </div>
            </div>
            <div class="kpi" style="border-color: orange;">
                <h2 style="font-size: 18px; color: orange; margin: 0; text-align: left;">Top Sales Location</h2>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <h1 style="font-size: 36px; color: orange; margin: 0;">Hell's Kitchen</h1>
                    <h3 style="font-size: 36px; color: orange; margin: 0;">$236,511.17</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Right column for Pie Chart of Top Sales Locations
    with col2:
        st.subheader("Top Sales Locations")
        st.image("pie chart.png", caption="Sales Distribution by Store Location", use_container_width=True)

# Customer Insights Section
elif page == "🧍 Customer Behaviour":
    st.header("🧍 Customer Behaviour")
    st.write("Analyze customer behavior based on selected product categories and store locations.")

    product_categories = df['product_category'].unique()
    selected_category = st.selectbox("Choose Product Category", product_categories)
    filtered_data = df[df['product_category'] == selected_category]

    st.write(f"Displaying data for product category: {selected_category}")
    # Replace with correct function in your customer module
    customer.transaction_in_hour_basis(filtered_data)

# Sales Analysis Section
elif page == "💸 Sales Analysis":
    st.header("💸 Sales Analysis")
    st.write("Explore monthly sales performance and sales distribution across locations.")

    st.subheader("Monthly Sales Trend")
    monthly_sales = filtered_df2.groupby('month')['sales'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_sales, x='month', y='sales', marker='o', ax=ax1)
    ax1.set_title('Sales by Month')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Sales')
    st.pyplot(fig1)

    st.subheader("Sales Distribution by Location")
    location_sales = filtered_df2.groupby('store_location')['sales'].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.pie(location_sales['sales'], labels=location_sales['store_location'], autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    ax2.set_title('Sales by Location')
    st.pyplot(fig2)

# Time Trends Section
elif page == "📅 Time Trends":
    st.header("📅 Time-Based Insights")
    st.write("Analyze sales distribution by hour of the day and day of the week to understand peak times.")

    st.subheader("Sales by Hour")
    hourly_sales = filtered_df2.groupby('hour')['transaction_id'].count().reset_index()
    hourly_sales.columns = ['hour', 'order_count']
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hourly_sales, x='hour', y='order_count', marker='o', ax=ax3)
    ax3.set_title('Peak Hour for Sales')
    ax3.set_xlabel('Hour')
    ax3.set_ylabel('Number of Orders')
    st.pyplot(fig3)

    st.subheader("Sales by Day of the Week")
    weekday_order_counts = filtered_df2['weekday'].value_counts().reindex(
        ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    ).reset_index()
    weekday_order_counts.columns = ['weekday', 'order_count']
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weekday_order_counts, x='weekday', y='order_count', ax=ax4)
    ax4.set_title('Sales by Day of the Week')
    ax4.set_xlabel('Weekday')
    ax4.set_ylabel('Order Count')
    st.pyplot(fig4)

# Product Performance Section
elif page == "📦 Product Performance":
    st.header("📦 Product Performance Analysis")
    st.write("Review the top-selling products and analyze their performance.")

    top_products = filtered_df2.groupby('product')['sales'].sum().reset_index().sort_values(by='sales',
                                                                                            ascending=False).head(10)
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_products, x='sales', y='product', palette='muted', ax=ax5)
    ax5.set_title('Top 10 Products by Revenue')
    ax5.set_xlabel('Revenue')
    ax5.set_ylabel('Product')
    st.pyplot(fig5)

    st.subheader("Average Order Value by Category")
    avg_order_by_category = filtered_df2.groupby('category')['sales'].mean().reset_index().sort_values(by='sales',
                                                                                                       ascending=False)
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=avg_order_by_category, x='sales', y='category', palette='muted', ax=ax6)
    ax6.set_title('Average Order Value by Category')
    ax6.set_xlabel('Average Sales Value')
    ax6.set_ylabel('Category')
    st.pyplot(fig6)

# Regional Insights Section
elif page == "📊 Regional Insights":
    st.header("📊 Regional Sales Insights")
    st.write("Explore regional trends and compare sales performance across different stores.")

    location_sales_sorted = filtered_df2.groupby('store_location')['sales'].sum().reset_index().sort_values(by='sales',
                                                                                                            ascending=False)
    fig7, ax7 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=location_sales_sorted, x='store_location', y='sales', palette='Blues_d', ax=ax7)
    ax7.set_title('Sales by Store Location')
    ax7.set_xlabel('Store Location')
    ax7.set_ylabel('Sales')
    st.pyplot(fig7)