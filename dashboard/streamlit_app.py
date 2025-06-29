import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# -----------------------------
# 📌 Page Configuration
# -----------------------------
st.set_page_config(page_title="Smart Transactions Dashboard", layout="wide")

# -----------------------------
# 🎨 Custom Styling
# -----------------------------
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-size: 22px !important;
        }
        h1, h2, h3 {
            font-size: 42px !important;
            font-weight: bold;
        }
        .stDataFrame th, .stDataFrame td {
            font-size: 20px !important;
        }
        section[data-testid="stSidebar"] {
            width: 35% !important;
            min-width: 350px;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 🧾 Dashboard Title
# -----------------------------
st.markdown("<h1>📊 Smart Transactions Dashboard</h1>", unsafe_allow_html=True)

# -----------------------------
# 🔐 Load environment variables
# -----------------------------
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET = os.getenv("AWS_S3_BUCKET")

# Set credentials for s3fs
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["AWS_DEFAULT_REGION"] = AWS_REGION

# -----------------------------
# 📦 Path to cleaned Parquet file
# -----------------------------
PARQUET_KEY = "processed/cleaned_transactions/"
s3_path = f"s3://{BUCKET}/{PARQUET_KEY}"

# -----------------------------
# 📥 Load Data
# -----------------------------
try:
    df = pd.read_parquet(s3_path, engine="pyarrow")
except Exception as e:
    st.error(f"❌ Failed to load data from:\n{s3_path}\n\n{e}")
    st.stop()

# Ensure correct types
if "transaction_date" in df.columns:
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

# Lowercase column names (important for consistency)
df.columns = [col.lower() for col in df.columns]

# -----------------------------
# 🔍 Sidebar Filters
# -----------------------------
with st.sidebar:
    st.markdown("## 🔎 Filters")

    categories = df["product_category"].dropna().unique().tolist()
    selected_categories = st.multiselect("Product Category", categories, default=categories)

    if "transaction_date" in df.columns:
        min_date = df["transaction_date"].min()
        max_date = df["transaction_date"].max()
        date_range = st.date_input("Transaction Date Range", [min_date, max_date])

# -----------------------------
# 🧼 Apply filters
# -----------------------------
df_filtered = df[df["product_category"].isin(selected_categories)]

if "transaction_date" in df.columns and len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered["transaction_date"] >= pd.to_datetime(date_range[0])) &
        (df_filtered["transaction_date"] <= pd.to_datetime(date_range[1]))
    ]

# -----------------------------
# 📊 Layout: Left & Right Columns
# -----------------------------
left_col, right_col = st.columns([1, 2.5])

# -----------------------------
# ⬅️ LEFT COLUMN
# -----------------------------
with left_col:
    st.subheader("📈 Summary")

    st.markdown(f"<h3>Total Transactions: {len(df_filtered):,}</h3>", unsafe_allow_html=True)

    # 🎨 Total Revenue Color Box
    total_revenue = df_filtered["amount_usd"].sum()
    st.markdown(f"""
        <div style='
            padding: 20px;
            border-radius: 12px;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: white;
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        '>
            💰 Total Revenue: ${total_revenue:,.2f}
        </div>
    """, unsafe_allow_html=True)

    # 🏅 Top Customers
    st.subheader("🏅 Top 5 Customers")
    top_customers = (
        df_filtered.groupby("customer_id")["amount_usd"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
        .rename(columns={"customer_id": "Customer ID", "amount_usd": "Revenue ($)"})
    )
    st.dataframe(top_customers, use_container_width=True)

    # 🗺️ Map
    st.subheader("🗺️ Transactions Map")
    if {"latitude", "longitude"}.issubset(df_filtered.columns):
        df_map = df_filtered.dropna(subset=["latitude", "longitude"])
        if not df_map.empty:
            st.map(df_map[["latitude", "longitude"]])
        else:
            st.info("ℹ️ No valid coordinates found.")
    else:
        st.warning("⚠️ Missing required columns: 'latitude' or 'longitude'.")

# -----------------------------
# ➡️ RIGHT COLUMN
# -----------------------------
with right_col:
    st.subheader("📦 Revenue by Product Category")
    pie1 = px.pie(
        df_filtered,
        names="product_category",
        values="amount_usd",
        hole=0.3,
        title="Revenue by Product",
        height=700  # 🆕 Bigger size
    )
    pie1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(pie1, use_container_width=True)

    # 🆕 Bar Chart: Transactions by Week
    st.subheader("📅 Transactions by Week (Bar Chart)")
    if "transaction_date" in df_filtered.columns:
        df_filtered["week"] = df_filtered["transaction_date"].dt.isocalendar().week
        week_counts = df_filtered["week"].value_counts().sort_index().reset_index()
        week_counts.columns = ["Week", "Count"]
        bar_week = px.bar(
            week_counts,
            x="Week",
            y="Count",
            title="Weekly Transactions",
            labels={"Count": "Number of Transactions", "Week": "ISO Week"},
            height=400
        )
        st.plotly_chart(bar_week, use_container_width=True)

# -----------------------------
# ⬇️ CSV Download
# -----------------------------
st.markdown("### 📥 Download Filtered CSV")
st.download_button(
    label="Download CSV",
    data=df_filtered.to_csv(index=False),
    file_name="filtered_transactions.csv",
    mime="text/csv"
)

# -----------------------------
# 📂 Show Raw Data
# -----------------------------
with st.expander("🔍 Show Raw Data"):
    st.dataframe(df_filtered, use_container_width=True)