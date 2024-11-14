import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configure page layout
st.set_page_config(
    page_title="Dashboard",
    page_icon="☕",
    layout="wide"
)

# Load data
df = pd.read_csv('Coffee Shop Sales.csv')
df2 = pd.read_csv('cleaned_coffee_sales_dataset.csv')

# Sidebar Navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["📈 Overview", "🧍 Customer Insights", "💸 Sales Analysis", "📅 Time Trends", "📦 Product Performance", "📊 Regional Insights"]
)

# Header Section


# Display KPIs in the Overview Section
if page == "📈 Overview":
    st.title("☕ Coffee Shop Sales Dashboard")

    # Load data
    df2 = pd.read_csv('cleaned_coffee_sales_dataset.csv')

    # Key Performance Indicators
    st.header("🔍 Key Performance Indicators")

    # Calculate metrics
    total_revenue = df2['sales'].sum()
    total_orders = df2['id'].nunique()
    avg_order_value = total_revenue / total_orders
    peak_sales_location = df2.groupby('location')['sales'].sum().idxmax()
    peak_sales_location_revenue = df2.groupby('location')['sales'].sum().max()

    st.write(
        f"**Total Sales Revenue:** ${total_revenue:,.2f} &nbsp;&nbsp; | &nbsp;&nbsp; "
        f"**Total Orders:** {total_orders:,} &nbsp;&nbsp; | &nbsp;&nbsp; "
        f"**Average Order Value:** ${avg_order_value:.2f} &nbsp;&nbsp; | &nbsp;&nbsp; "
        f"**Top Sales Location:** {peak_sales_location} (${peak_sales_location_revenue:,.2f})"
    )

    st.markdown("---")

    # Sidebar for choosing visualization options
    st.sidebar.title("Explore Insights")
    st.write("Select a visualization from the sidebar to explore more insights.")

# Customer Insights Section
elif page == "🧍 Customer Insights":
    st.header("👥 Customer Insights")
    st.write("Analyze customer behavior based on selected product categories and store locations.")

    product_categories = df['product_category'].unique()
    selected_category = st.selectbox("Choose Product Category", product_categories)
    filtered_data = df[df['product_category'] == selected_category]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=filtered_data, x='store_location', y='transaction_qty', hue='product_detail', ax=ax)
    ax.set_title(f"Sales of {selected_category} by Location")
    st.pyplot(fig)

# Sales Analysis Section
elif page == "💸 Sales Analysis":
    st.header("💸 Sales Analysis")
    st.write("Explore monthly sales performance and sales distribution across locations.")

    # Monthly Sales Trend
    st.subheader("Monthly Sales Trend")
    monthly_sales = df2.groupby('month')['sales'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_sales, x='month', y='sales', marker='o', ax=ax1)
    ax1.set_title('Sales by Month')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Sales')
    st.pyplot(fig1)

    # Sales by Location
    st.subheader("Sales Distribution by Location")
    location_sales = df2.groupby('location')['sales'].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.pie(location_sales['sales'], labels=location_sales['location'], autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    ax2.set_title('Sales by Location')
    st.pyplot(fig2)

# Time Trends Section
elif page == "📅 Time Trends":
    st.header("📅 Time-Based Insights")
    st.write("Analyze sales distribution by hour of the day and day of the week to understand peak times.")

    # Sales by Hour
    st.subheader("Sales by Hour")
    hourly_sales = df2.groupby('hour')['id'].count().reset_index()
    hourly_sales.columns = ['hour', 'order_count']
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hourly_sales, x='hour', y='order_count', marker='o', ax=ax3)
    ax3.set_title('Peak Hour for Sales')
    ax3.set_xlabel('Hour')
    ax3.set_ylabel('Number of Orders')
    st.pyplot(fig3)

    # Sales by Weekday
    st.subheader("Sales by Day of the Week")
    weekday_order_counts = df2['weekday'].value_counts().reindex(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']).reset_index()
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

    # Top Products by Revenue
    top_products = df2.groupby('product')['sales'].sum().reset_index().sort_values(by='sales', ascending=False).head(10)
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_products, x='sales', y='product', palette='muted', ax=ax5)
    ax5.set_title('Top 10 Products by Revenue')
    ax5.set_xlabel('Revenue')
    ax5.set_ylabel('Product')
    st.pyplot(fig5)

    # Average Order Value by Category
    st.subheader("Average Order Value by Category")
    avg_order_by_category = df2.groupby('category')['sales'].mean().reset_index().sort_values(by='sales', ascending=False)
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=avg_order_by_category, x='sales', y='category', palette='muted', ax=ax6)
    ax6.set_title('Average Order Value by Category')
    ax6.set_xlabel('Sales')
    ax6.set_ylabel('Category')
    st.pyplot(fig6)

# Regional Insights Section
elif page == "📊 Regional Insights":
    st.header("📊 Regional Insights")
    st.write("Explore sales performance and customer behavior across different regions.")

    # Sales by Region
    st.subheader("Sales by Region")
    region_sales = df2.groupby('region')['sales'].sum().reset_index