import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import base64

import customer

# Set page layout to wide
st.set_page_config(layout="wide")

# Load your data
df = pd.read_excel("coffee_shop.xlsx")
df2 = pd.read_csv('New_data.csv')




# Function to load and encode images
def get_base64(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Encode background image and pie chart
background_image_path = 'background.png'
pie_chart_path = 'pie chart.png'
background_image_base64 = get_base64(background_image_path)
pie_chart_base64 = get_base64(pie_chart_path)

# CSS to set background image
background_image_style = f"""
<style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{background_image_base64}");
        background-size: cover;
        background-position: center;
    }}
</style>
"""
st.markdown(background_image_style, unsafe_allow_html=True)

# Header Section with Coffee Color Background Box
st.markdown(
    """
    <div style="padding: 10px; border: 2px solid black; border-radius: 10px; background-color: #6F4E37; color: white; width: 100%; max-width: 800px; margin: 0 auto;">
        <h1 style="text-align: center;">☕︎ Buzz & Beans: Sales Tracker</h1>
        <p style="text-align: center; color: white;">Discover insights into coffee shop sales across locations and product categories with this interactive tool.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Performance Benchmarks Header with Pie Chart
st.markdown(
    f"""
    <div style="padding: 10px; border: 2px solid black; border-radius: 10px; background-color: #6F4E37; color: white; width: 100%; max-width: 800px; margin: 20px auto;">
        <h2 style="text-align: center; color: white;">🔍 Performance Benchmarks</h2>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 10px;">
            <div style="flex: 1; min-width: 300px; max-width: 350px; padding: 10px; border: 2px solid green; border-radius: 10px; background-color: white; color: green; margin-bottom: 10px;">
                <h3 style="text-align: center; color: green;">Total Sales Revenue</h3>
                <h1 style="text-align: center; color: green;">$698,812.33</h1>
            </div>
            <div style="flex: 1; min-width: 300px; max-width: 350px; padding: 10px; border: 2px solid #6F4E37; border-radius: 10px; background-color: white; color: #4B4B4B; margin-bottom: 10px;">
                <h3 style="text-align: center; color: #4B4B4B;">Total Orders</h3>
                <h1 style="text-align: center; color: #4B4B4B;">149,116</h1>
            </div>
            <div style="flex: 1; min-width: 300px; max-width: 350px; padding: 10px; border: 2px solid orange; border-radius: 10px; background-color: white; color: orange; margin-bottom: 10px;">
                <h3 style="text-align: center; color: orange;">Top Sales Location</h3>
                <h1 style="text-align: center; color: orange;">Hell's Kitchen</h1>
                <h3 style="text-align: center; color: orange;">$236,511.17</h3>
            </div>
            <div style="flex: 1; min-width: 300px; max-width: 350px; margin-top: 20px;">
                <h3 style="text-align: center; color: white;">Top Sales Locations</h3>
                <img src="data:image/png;base64,{pie_chart_base64}" style="max-width: 100%; height: auto;" alt="Sales Distribution by Store Location">
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



def main():
    # Sidebar Navigation
    st.sidebar.header("Phoenix")
    page = st.sidebar.radio("Choose Page", ["Home", "Customer_Behaviour", "Pricing Strategy", "Future Demand"])

    if page == "Home":
        pass

    elif page == "Customer_Behaviour":
        st.header("Age Distribution Analysis")

        customer.transaction_in_hour_basis(df2)
        customer.transaction_in_day_basis(df)
        customer.transaction_in_month_basis(df)
        customer.display_barista_revenue(df2)

    elif page == "Pricing Strategy":
        st.header("Pricing Strategy")
        customer.average_price_basis(df2)
        customer.lowest_sale_product(df2)


    elif page == "Future Demand":
        st.header("Future Demand Analysis")
        customer.category_basis_transaction(df2)
        customer.average_category_transaction(df2)
        customer.category_transaction(df2)

if __name__ == "__main__":
    main()