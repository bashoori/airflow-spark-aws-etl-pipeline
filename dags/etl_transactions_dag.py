from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import logging

default_args = {
    'owner': 'Bita',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'start_date': datetime(2025, 1, 1),
}

with DAG(
    dag_id='etl_transactions_pipeline',
    default_args=default_args,
    schedule_interval=None,  # ← manual only
    #schedule_interval='@daily', # ←daily only
    catchup=False,
    description='Manual ETL pipeline with PySpark for IBM-style data workflow',
    tags=['spark', 'etl', 'manual'],
) as dag:

    def run_spark_job():
        try:
            logging.info("🚀 Running Spark job: clean_transform.py")
            result = subprocess.run(
                ["spark-submit", "spark_jobs/clean_transform.py"],
                check=True,
                capture_output=True,
                text=True
            )
            logging.info("✅ Spark job output:\n%s", result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error("🔥 Spark job failed:\n%s", e.stderr)
            raise

    spark_etl_task = PythonOperator(
        task_id='clean_and_transform_transactions',
        python_callable=run_spark_job
    )

    spark_etl_task