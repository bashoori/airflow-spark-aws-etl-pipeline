import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# -----------------------------
# 🌍 Load AWS credentials from .env
# -----------------------------
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET = os.getenv("AWS_S3_BUCKET")

# -----------------------------
# 📦 S3 Parquet path (cleaned output folder)
# -----------------------------
PARQUET_KEY = "processed/cleaned_transactions/"
s3_path = f"s3://{BUCKET}/{PARQUET_KEY}"

# Set AWS credentials for s3fs
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["AWS_DEFAULT_REGION"] = AWS_REGION

# -----------------------------
# 🎨 Streamlit UI
# -----------------------------
st.set_page_config(page_title="Transactions Dashboard", page_icon="🧾", layout="wide")
st.title("🧾 Transactions Dashboard")

# -----------------------------
# 🧪 Load Data
# -----------------------------
try:
    df = pd.read_parquet(s3_path, engine="pyarrow")
except Exception as e:
    st.error(f"❌ Failed to load data: {s3_path}\n\n{e}")
    st.stop()

# -----------------------------
# 📊 Summary Metrics
# -----------------------------
st.subheader("📈 Overview")
col1, col2 = st.columns(2)
col1.metric("Total Transactions", f"{len(df):,}")
col2.metric("Total Revenue", f"${df['amount_usd'].sum():,.2f}")

# -----------------------------
# 📊 Revenue by Product Category
# -----------------------------
st.subheader("📦 Revenue by Product Category")
category_rev = df.groupby("product_category")["amount_usd"].sum().sort_values(ascending=False)
st.bar_chart(category_rev)

# -----------------------------
# 📆 Transactions by Day of Week
# -----------------------------
st.subheader("📅 Transactions by Day of Week")
day_counts = df["day_of_week"].value_counts().sort_index()
st.bar_chart(day_counts)

# -----------------------------
# 🗃️ View Raw Data (optional)
# -----------------------------
with st.expander("🔍 Show Raw Data"):
    st.dataframe(df.head(20))