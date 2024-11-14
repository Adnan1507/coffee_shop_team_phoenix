import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page layout to wide
st.set_page_config(layout="wide")

# Load your data
df = pd.read_excel('coffee_shop.xlsx')
df2 = pd.read_csv('New_data.csv')

# Assume 'total_revenue' is the correct column name based on inspection
def Sales(filtered_df, selected_product_category):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_df, x='store_location', y='transaction_qty', hue='product_detail')
    plt.title(f"Sales of {selected_product_category} by Location")
    plt.xlabel("Store Location")
    plt.ylabel("Total Sales Quantity")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)
def total_revenue_each_location(df):
    revenue_by_location = df.groupby('store_location')['total_revenue'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=revenue_by_location, x='store_location', y='total_revenue')
    plt.title('Total Revenue by Store Location')
    plt.xlabel('Store Location')
    plt.ylabel('Total Revenue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

def average_revenue_by_hour(df2):
    # Convert 'transaction_time' to datetime
    df2['transaction_time'] = pd.to_datetime(df2['transaction_time'], format='%H:%M:%S')

    # Extract the hour from 'transaction_time'
    df2['hour'] = df2['transaction_time'].dt.hour

    # Assume 'total_revenue' is the correct column name based on inspection
    avg_revenue_by_hour_location = df2.groupby(['store_location', 'hour'])['total_revenue'].mean().unstack(fill_value=0)

    # Plotting the result with time labels
    plt.figure(figsize=(10, 6))
    avg_revenue_by_hour_location.plot(kind='bar', stacked=True)
    plt.title('Average Revenue by Hour of the Day for Each Location')
    plt.xlabel('Hour')
    plt.ylabel('Average Revenue')
    plt.xticks(rotation=0)
    plt.legend(title='Store Location')

    st.pyplot(plt)

def Sales(filtered_df, selected_product_category):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_df, x='store_location', y='transaction_qty', hue='product_detail')
    plt.title(f"Sales of {selected_product_category} by Location")
    plt.xlabel("Store Location")
    plt.ylabel("Total Sales Quantity")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

def main():
    st.title("Coffee Shop Dashboard")

    # Sidebar Navigation
    st.sidebar.header("Phoenix")
    page = st.sidebar.radio("Choose Page", ["Home", "Customer Behaviour", "Pricing Strategy", "Future Demand"])

    if page == "Home":
        st.subheader("Dashboard Overview")
        st.write("Explore key visualizations of customer behavior across multiple metrics.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Revenues")
            total_revenue_each_location(df)

        with col2:
            st.markdown("### Top Product Categories")
            # Placeholder for future implementation of top product categories visualization

    elif page == "Customer Behaviour":
        st.header("Customer Behaviour")
        product_category = df['product_category'].unique()
        selected_product_type = st.selectbox("Select Product Type", options=product_category, index=0)

        filtered_df = df[df['product_category'] == selected_product_type]
        Sales(filtered_df, selected_product_type)

    elif page == "Pricing Strategy":
        st.header("Purchase Amount Distribution Analysis")

        # Select box for additional purchase amount-related analysis options
        st.subheader("Further Analysis Options")
        purchase_option = st.selectbox(
            "Choose additional analysis on Purchase Amount:",
            ["None", "Purchase by Region", "Purchase by Category"]
        )
        if purchase_option == "Purchase by Region":
            st.write("Display purchase distribution by region.")
            # Additional purchase amount analysis code here
        elif purchase_option == "Purchase by Category":
            st.write("Display purchase amount distribution by product category.")
            # Additional visualization code here

    elif page == "Future Demand":
        st.header("Revenue analysis of each location")
        total_revenue_each_location(df)

        # Select box for additional product category-related analysis options
        st.subheader("Further Analysis Options")
        category_option = st.selectbox(
            "Choose additional analysis on Categories:",
            ["None", "Category by Region", "Category by Purchase Volume"]
        )
        if category_option == "Category by Region":
            st.write("Display top categories by region.")
            # Additional category analysis code here
        elif category_option == "Category by Purchase Volume":
            st.write("Display top categories by purchase volume.")
            # Additional visualization code here

if __name__ == "_main_":
    main()