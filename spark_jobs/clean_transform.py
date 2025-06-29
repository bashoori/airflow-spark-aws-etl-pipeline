import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, date_format

# -----------------------------
# 🔐 Load .env credentials
# -----------------------------
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region     = os.getenv("AWS_REGION")
bucket         = os.getenv("AWS_S3_BUCKET")

# -----------------------------
# 📂 S3 Paths
# -----------------------------
input_path = f"s3a://{bucket}/raw/transactions_with_location.csv"
#f"s3a://{bucket}/raw/transactions.csv"
output_path = f"s3a://{bucket}/processed/cleaned_transactions"

# -----------------------------
# 🚀 Initialize Spark Session
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
# 📥 Load Raw CSV
# -----------------------------
print(f"📥 Reading from: {input_path}")
df = spark.read.csv(input_path, header=True, inferSchema=True)

# -----------------------------
# 🧼 Filter & Transform
# -----------------------------
df_cleaned = df.filter(col("status") == "Success")

# Add new column: day of week (e.g., Monday)
df_cleaned = df_cleaned.withColumn("day_of_week", date_format(to_date("transaction_date"), "EEEE"))

# ✅ Optional: select only the desired columns
expected_columns = [
    "transaction_id", "customer_id", "transaction_date", "amount_usd",
    "payment_method", "status", "product_category",
    "latitude", "longitude",  # 🗺️ Include for the map
    "day_of_week"
]

# Check for available columns
existing_columns = [c for c in expected_columns if c in df_cleaned.columns]
df_cleaned = df_cleaned.select(*existing_columns)

# -----------------------------
# 💾 Write to Parquet
# -----------------------------
print(f"💾 Writing cleaned data to: {output_path}")
df_cleaned.write.mode("overwrite").parquet(output_path)

print("✅ Transformation complete and saved to S3.")