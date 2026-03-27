import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Smart Clothing BI", layout="wide")

st.title("Smart Clothing Business Intelligence")

# --- SIDEBAR ---
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "Inventory & Forecasting", "Upload Data"])

# --- API CONFIG ---
# This is the URL where your FastAPI server is running
API_URL = "http://127.0.0.1:8000"

if menu == "Dashboard":
    st.subheader("Actionable Recommendations")
    
    # Fetch data from our FastAPI backend
    try:
        response = requests.get(f"{API_URL}/ml/recommendations")
        if response.status_code == 200:
            recs = response.json()
            
            # Display recommendations in nice "cards"
            cols = st.columns(len(recs))
            for i, rec in enumerate(recs):
                with cols[i]:
                    st.info(f"**{rec['type']}**")
                    st.write(rec['sku'])
                    st.caption(rec['message'])
        else:
            st.error("Could not fetch recommendations.")
    except Exception as e:
        st.error(f"Backend offline: {e}")

    # Add a placeholder chart
    st.divider()
    st.subheader("Sales Trend (Mock Data)")
    chart_data = pd.DataFrame({
        "Date": pd.date_range(start="2026-03-01", periods=10),
        "Sales": [15, 22, 18, 25, 30, 28, 35, 42, 38, 50]
    })
    st.line_chart(data=chart_data, x="Date", y="Sales")

elif menu == "Upload Data":
    st.subheader("Upload Sales CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        st.success("File uploaded! (Next step: Connect to API)")