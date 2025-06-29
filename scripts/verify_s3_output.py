import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# AWS credentials & config
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
bucket_name = os.getenv("AWS_S3_BUCKET")

# Prefix to check (output folder in S3)
output_prefix = "data/raw/transactions_with_location.csv"
#"processed/cleaned_transactions/"

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

# List files in the S3 output prefix
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=output_prefix)

# Display results
if "Contents" in response:
    print(f"✅ Found {len(response['Contents'])} file(s) in: s3://{bucket_name}/{output_prefix}\n")
    for obj in response["Contents"]:
        print("📄", obj["Key"], f"({obj['Size']} bytes)")
else:
    print(f"❌ No files found at: s3://{bucket_name}/{output_prefix}")