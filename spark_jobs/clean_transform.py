import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, date_format

# -----------------------------
# 🔐 Load environment variables from .env
# -----------------------------
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region     = os.getenv("AWS_REGION")
bucket          = os.getenv("AWS_S3_BUCKET")

# -----------------------------
# 📂 Input and Output Paths
# -----------------------------
input_path     = f"s3a://{bucket}/raw/transactions_with_location.csv"
s3_output_path = f"s3a://{bucket}/processed/cleaned_transactions"
local_output_path = "data/processed/cleaned_transactions"

# Create local folder if it doesn't exist
os.makedirs(local_output_path, exist_ok=True)

# -----------------------------
# 🚀 Initialize Spark Session with S3 configs
# -----------------------------
spark = SparkSession.builder \
    .appName("CleanTransformTransactions") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key) \
    .config("spark.hadoop.fs.s3a.endpoint", f"s3.{aws_region}.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", True) \
    .getOrCreate()

# -----------------------------
# 📥 Read CSV from S3
# -----------------------------
print(f"📥 Reading from: {input_path}")
df = spark.read.csv(input_path, header=True, inferSchema=True)

# -----------------------------
# 🧼 Clean and Transform
# -----------------------------
df_cleaned = df.filter(col("status") == "Success")
df_cleaned = df_cleaned.withColumn("day_of_week", date_format(to_date("transaction_date"), "EEEE"))

# Only keep necessary columns
expected_columns = [
    "transaction_id", "customer_id", "transaction_date", "amount_usd",
    "payment_method", "status", "product_category",
    "latitude", "longitude", "day_of_week"
]
existing_columns = [c for c in expected_columns if c in df_cleaned.columns]
df_cleaned = df_cleaned.select(*existing_columns)

# -----------------------------
# 💾 Write to S3
# -----------------------------
print(f"💾 Writing to S3: {s3_output_path}")
df_cleaned.write.mode("overwrite").parquet(s3_output_path)

# -----------------------------
# 💾 Write to Local Folder
# -----------------------------
print(f"💾 Writing locally to: {local_output_path}")
df_cleaned.write.mode("overwrite").parquet(local_output_path)

print("✅ Data successfully written to both S3 and local folder.")