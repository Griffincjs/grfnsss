import streamlit as st
import requests
import pandas as pd

# 1. Page Configuration & Theme
st.set_page_config(
    page_title="Smart Clothing BI",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a "Tech" feel
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

API_URL = "https://grfnsss.onrender.com"

# --- SIDEBAR & BRANDING ---
st.sidebar.title("📊 BI Control Center")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Inventory & Forecasting", "Data Management"])

st.sidebar.markdown("---")
st.sidebar.subheader("Network Status")

# Live Health Check
try:
    health = requests.get(f"{API_URL}/")
    if health.status_code == 200:
        st.sidebar.success("● System Online")
    else:
        st.sidebar.warning("○ System Lagging")
except:
    st.sidebar.error("○ System Offline")

if menu == "Dashboard":
    st.title("👕 Smart Clothing Executive Overview")
    
    # 1. TOP LEVEL KPI TILES 
    try:
        sales_res = requests.get(f"{API_URL}/data/sales")
        if sales_res.status_code == 200 and sales_res.json():
            df_stats = pd.DataFrame(sales_res.json())
            
            # Calculations
            total_rev = (df_stats['quantity'] * df_stats['price']).sum()
            total_qty = df_stats['quantity'].sum()
            sku_count = df_stats['sku'].nunique()

            # Layout metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Revenue", f"${total_rev:,.2f}")
            m2.metric("Units Sold", f"{total_qty:,}")
            m3.metric("Unique SKUs", sku_count)
            st.markdown("---")
    except:
        st.info("Waiting for data stream... Run your generator to see metrics.")

    #  2. INTELLIGENT RECOMMENDATIONS 
    st.subheader("🤖 AI Action Plan")
    try:
        rec_res = requests.get(f"{API_URL}/ml/recommendations")
        if rec_res.status_code == 200:
            recs = rec_res.json()
            r_cols = st.columns(len(recs))
            for i, r in enumerate(recs):
                with r_cols[i]:
                    if r['type'] == "RESTOCK":
                        st.error(f"**{r['type']} REQUIRED**")
                    else:
                        st.warning(f"**{r['type']} SUGGESTED**")
                    st.write(f"**Item:** {r['sku']}")
                    st.caption(r['message'])
    except:
        st.caption("Unable to load recommendations.")

    st.markdown("---")

    #  3. VISUAL ANALYTICS 
    if 'df_stats' in locals():
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.subheader("Performance by Category")
            cat_data = df_stats.groupby("category")["quantity"].sum().reset_index()
            st.bar_chart(data=cat_data, x="category", y="quantity", use_container_width=True)
        with col_b:
            st.subheader("Live Feed")
            st.dataframe(df_stats.tail(8), use_container_width=True)

elif menu == "Inventory & Forecasting":
    st.title("📈 Demand Prediction")
    cat = st.selectbox("Select Product Category", ["T-Shirts", "Pants", "Outerwear"])
    
    if st.button("Run ML Forecast"):
        with st.spinner("Analyzing historical trends..."):
            res = requests.get(f"{API_URL}/ml/forecast/{cat}")
            if res.status_code == 200 and "error" not in res.json():
                f_df = pd.DataFrame(res.json())
                f_df.columns = ["Date", "Predicted Units"]
                st.line_chart(data=f_df, x="Date", y="Predicted Units")
                st.success(f"14-Day Forecast generated for {cat}")
            else:
                st.error("Insufficient historical data for a high-confidence forecast.")

elif menu == "Data Management":
    st.title("📂 Data Ingestion")
    st.info("The CSV Upload module is currently scheduled for the next update cycle.")
    st.file_uploader("Upload External Sales Records", type="csv", disabled=True)
    st.markdown("---")
    st.subheader("Database Status")
    st.write("Using: **SQLite (Local)**")
    st.write("Current Table: `sales`")
