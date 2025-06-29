import os
import pandas as pd
from dotenv import load_dotenv

# Load env vars
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket         = os.getenv("AWS_S3_BUCKET")

# Set env for s3fs
os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key

# Path to the raw CSV file
s3_path = f"s3://{bucket}/raw/transactions_with_location.csv"

# Read and show columns
try:
    df = pd.read_csv(s3_path, storage_options={
        "key": aws_access_key,
        "secret": aws_secret_key
    })
    print("✅ Raw CSV loaded successfully.")
    print("📋 Columns:")
    print(df.columns.tolist())
except Exception as e:
    print("❌ Failed to read raw CSV.")
    print(e)