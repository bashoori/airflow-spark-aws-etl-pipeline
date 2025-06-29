import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, date_format

# ✅ Load .env from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# ✅ AWS credentials and target S3 bucket
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
s3_bucket = os.getenv("AWS_S3_BUCKET")

# ✅ Define S3 output path
output_path = f"s3a://{s3_bucket}/processed/cleaned_transactions"

# ✅ Initialize Spark with S3 support
spark = SparkSession.builder \
    .appName("CleanTransformTransactions") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key) \
    .config("spark.hadoop.fs.s3a.endpoint", f"s3.{aws_region}.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", True) \
    .getOrCreate()

# ✅ Read input data (still local)
input_path = "data/raw/transactions.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)

# ✅ Clean and transform
df_cleaned = df.filter(col("status") == "Success")
df_cleaned = df_cleaned.withColumn("day_of_week", date_format(to_date("transaction_date"), "EEEE"))

# ✅ Write cleaned data to S3
df_cleaned.write.mode("overwrite").parquet(output_path)

print(f"✅ Data written to S3: {output_path}")