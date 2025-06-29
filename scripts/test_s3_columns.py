import os
import pandas as pd
from dotenv import load_dotenv

# -----------------------------
# 🔐 Load environment variables from .env
# -----------------------------
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# -----------------------------
# ✅ Fetch environment variables
# -----------------------------
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region     = os.getenv("AWS_REGION")
bucket         = os.getenv("AWS_S3_BUCKET")

# -----------------------------
# ❗ Validate environment variables
# -----------------------------
missing = []
if not aws_access_key: missing.append("AWS_ACCESS_KEY_ID")
if not aws_secret_key: missing.append("AWS_SECRET_ACCESS_KEY")
if not aws_region:     missing.append("AWS_REGION")
if not bucket:         missing.append("AWS_S3_BUCKET")

if missing:
    print("❌ Missing required environment variables:")
    for var in missing:
        print(f" - {var}")
    exit(1)

# -----------------------------
# 🌍 Set environment variables for s3fs/pyarrow
# -----------------------------
os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key
os.environ["AWS_DEFAULT_REGION"] = aws_region

# -----------------------------
# 📦 Define the S3 path to cleaned Parquet data
# -----------------------------
parquet_path = f"s3://{bucket}/processed/cleaned_transactions/"

# -----------------------------
# 🧪 Read and display columns
# -----------------------------
try:
    df = pd.read_parquet(parquet_path, engine="pyarrow")
    print("✅ Successfully loaded data from S3.")
    print("📋 Columns in the dataset:")
    for col in df.columns:
        print(f" - {col}")

    # -----------------------------
    # 📍 Map compatibility check
    # -----------------------------
    required = {"latitude", "longitude"}
    if required.issubset(set(df.columns)):
        print("✅ ✅ Latitude and Longitude are present — Streamlit map is ready!")
    else:
        print("⚠️ Map will not work — missing 'latitude' or 'longitude' columns.")

except Exception as e:
    print("❌ Failed to load Parquet file from S3.")
    print(f"Error: {e}")