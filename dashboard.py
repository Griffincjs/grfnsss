import os
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

# --- ENVIRONMENT-AWARE API URL ---
# Locally: points to your machine. On Render: reads the API_URL env variable.
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- SIDEBAR & BRANDING ---
st.sidebar.title("📊 BI Control Center")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Inventory & Forecasting", "Data Management"])

st.sidebar.markdown("---")
st.sidebar.subheader("Network Status")

# Live Health Check
try:
    health = requests.get(f"{API_URL}/", timeout=5)
    if health.status_code == 200:
        st.sidebar.success("● System Online")
    else:
        st.sidebar.warning("○ System Lagging")
except:
    st.sidebar.error("○ System Offline")

# ─────────────────────────────────────────
# PAGE 1: DASHBOARD
# ─────────────────────────────────────────
if menu == "Dashboard":
    st.title("👕 Smart Clothing Executive Overview")

    # 1. TOP LEVEL KPI TILES
    try:
        sales_res = requests.get(f"{API_URL}/data/sales", timeout=10)
        if sales_res.status_code == 200 and sales_res.json():
            df_stats = pd.DataFrame(sales_res.json())

            total_rev = (df_stats["quantity"] * df_stats["price"]).sum()
            total_qty = df_stats["quantity"].sum()
            sku_count = df_stats["sku"].nunique()

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Revenue", f"${total_rev:,.2f}")
            m2.metric("Units Sold", f"{total_qty:,}")
            m3.metric("Unique SKUs", sku_count)
            st.markdown("---")
    except:
        st.info("Waiting for data stream... Run your generator to see metrics.")

    # 2. INTELLIGENT RECOMMENDATIONS
    st.subheader("🤖 AI Action Plan")
    try:
        rec_res = requests.get(f"{API_URL}/ml/recommendations", timeout=10)
        if rec_res.status_code == 200:
            recs = rec_res.json()
            if recs:
                r_cols = st.columns(len(recs))
                for i, r in enumerate(recs):
                    with r_cols[i]:
                        if r["type"] == "RESTOCK":
                            st.error(f"**{r['type']} REQUIRED**")
                        else:
                            st.warning(f"**{r['type']} SUGGESTED**")
                        st.write(f"**Item:** {r['sku']}")
                        st.caption(r["message"])
            else:
                st.caption("No recommendations yet — upload some sales data first.")
    except:
        st.caption("Unable to load recommendations.")

    st.markdown("---")

    # 3. VISUAL ANALYTICS
    if "df_stats" in locals():
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.subheader("Performance by Category")
            cat_data = df_stats.groupby("category")["quantity"].sum().reset_index()
            st.bar_chart(data=cat_data, x="category", y="quantity", use_container_width=True)
        with col_b:
            st.subheader("Live Feed")
            st.dataframe(df_stats.tail(8), use_container_width=True)

# ─────────────────────────────────────────
# PAGE 2: INVENTORY & FORECASTING
# ─────────────────────────────────────────
elif menu == "Inventory & Forecasting":
    st.title("📈 Demand Prediction")
    cat = st.selectbox("Select Product Category", ["T-Shirts", "Pants", "Outerwear"])

    if st.button("Run ML Forecast"):
        with st.spinner("Analyzing historical trends..."):
            res = requests.get(f"{API_URL}/ml/forecast/{cat}", timeout=30)
            if res.status_code == 200 and "error" not in res.json():
                f_df = pd.DataFrame(res.json())
                f_df.columns = ["Date", "Predicted Units"]
                st.line_chart(data=f_df, x="Date", y="Predicted Units")
                st.success(f"14-Day Forecast generated for {cat}")
            else:
                st.error("Insufficient historical data for a high-confidence forecast.")

# ─────────────────────────────────────────
# PAGE 3: DATA MANAGEMENT
# ─────────────────────────────────────────
elif menu == "Data Management":
    st.title("📂 Data Ingestion")

    st.subheader("Upload CSV File")
    st.caption("Your CSV must have these columns: `date`, `sku`, `category`, `quantity_sold`, `price`")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Preview the file before uploading
        preview_df = pd.read_csv(uploaded_file)
        st.write(f"**Preview** — {len(preview_df)} rows detected:")
        st.dataframe(preview_df.head(5), use_container_width=True)
        uploaded_file.seek(0)  # Reset file pointer after preview read

        if st.button("✅ Confirm & Upload to Database"):
            with st.spinner("Uploading records..."):
                res = requests.post(
                    f"{API_URL}/data/upload/csv",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")},
                    timeout=30
                )
                if res.status_code == 200:
                    st.success(res.json()["message"])
                else:
                    st.error(f"Upload failed: {res.json().get('detail', 'Unknown error')}")

    st.markdown("---")
    st.subheader("Database Status")

    # Detect which DB is in use based on environment
    db_type = "PostgreSQL (Cloud)" if os.getenv("DATABASE_URL") else "SQLite (Local)"
    st.write(f"Using: **{db_type}**")
    st.write("Current Table: `sales`")
