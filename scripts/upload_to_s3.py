import os
import boto3
from dotenv import load_dotenv

# -----------------------------
# 🔐 Load AWS credentials
# -----------------------------
load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region     = os.getenv("AWS_REGION")
bucket_name    = os.getenv("AWS_S3_BUCKET")

# -----------------------------
# 📁 Local & S3 file paths
# -----------------------------
local_file_path = "data/raw/transactions_with_location.csv"
s3_key = "raw/transactions_with_location.csv"  # 👈 This should overwrite the file used by Spark

# -----------------------------
# ✅ Check for missing .env vars
# -----------------------------
missing = []
if not aws_access_key: missing.append("AWS_ACCESS_KEY_ID")
if not aws_secret_key: missing.append("AWS_SECRET_ACCESS_KEY")
if not aws_region:     missing.append("AWS_REGION")
if not bucket_name:    missing.append("AWS_S3_BUCKET")

if missing:
    print("❌ Missing required environment variables:")
    for var in missing:
        print(f" - {var}")
    exit(1)

# -----------------------------
# ☁️ Create S3 client
# -----------------------------
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

# -----------------------------
# ⬆️ Upload file
# -----------------------------
try:
    s3.upload_file(local_file_path, bucket_name, s3_key)
    print(f"✅ Uploaded '{local_file_path}' to s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"❌ Upload failed: {e}")