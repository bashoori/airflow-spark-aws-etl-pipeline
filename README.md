# 🚀 Airflow + Spark + AWS ETL Pipeline  
## 📊 Smart Transactions Dashboard – Real-Time Analytics on the Cloud

A fully automated, cloud-native data pipeline built using **Apache Airflow**, **PySpark**, **AWS S3**, and **Streamlit**. This project showcases how real-world retail transaction data can be ingested, transformed, monitored, and visualized — all in a scalable, production-style architecture.

---

## 🔍 Key Features

- 🔍 Dynamic filters (product category & date range)
- 💰 Total revenue KPIs
- 🥇 Top 5 customers by spend
- 📦 Revenue by product category (pie chart)
- 📅 Daily/weekly transaction volume (bar chart)
- 🌍 Transaction map using geolocation
- ⬇️ Download filtered data as CSV
- 🧾 Expandable raw data preview

---

## 🧱 Tech Stack Overview

| Layer              | Technology                         |
|--------------------|-------------------------------------|
| **Orchestration**  | Apache Airflow (Dockerized)         |
| **Data Processing**| PySpark 3.5.1                        |
| **Storage**        | AWS S3 (Parquet via PyArrow)        |
| **Visualization**  | Streamlit + Plotly                  |
| **Environment**    | Docker + Docker Compose             |
| **Utilities**      | Python-dotenv, boto3, s3fs          |

---

## 📈 Business Scenario

A company receives thousands of daily retail transactions in CSV and JSON formats. Their goals:

- Monitor revenue by product category  
- Track sales trends and customer behavior  
- Identify failed transactions  
- Present insights in a clean dashboard for stakeholders

This project simulates that entire flow with automation, cloud-native tools, and real-time visualizations.

## 📊 Architecture Overview

![Architecture Diagram](https://github.com/bashoori/repo/blob/master/airflow-spark-aws-etl-pipeline/img2.png)

---

## 🧪 ETL Pipeline Workflow

```text
        ┌──────────────────────────┐
        │   Raw Transactions (CSV) │
        └────────────┬─────────────┘
                     │
         [PySpark Job: clean_transform.py]
                     │
        ┌────────────▼────────────┐
        │   Cleaned Transactions  │
        │     (Parquet on S3)     │
        └────────────┬────────────┘
                     │
              [Airflow DAG Scheduler]
                     │
        ┌────────────▼────────────┐
        │   Streamlit Dashboard   │
        │   (Customer KPIs & Maps)│
        └─────────────────────────┘
```

##  📂 Project Structure

```
 airflow-spark-aws-etl-pipeline/
├── dags/               → Airflow DAGs
├── spark_jobs/         → PySpark ETL scripts
├── dashboard/          → Streamlit dashboard app
├── docker/             → Docker Compose + setup files
├── data/               → Sample raw/processed data
├── docs/               → Diagrams, notes, architecture
├── requirements.txt    → Python dependencies
├── .gitignore
└── README.md
```

## 💻 How to Run the Project

Before you begin, make sure you have Docker installed and a valid .env file with AWS and SMTP credentials.

### 1️⃣ Set up and launch Dockerized environment

```
cd docker/
docker compose down --remove-orphans
docker compose run --rm airflow-init
docker compose up --build
```

### 2️⃣ Open Airflow UI at http://localhost:8080

### 3️⃣ Trigger DAG from Airflow interface

### 4️⃣ Run the dashboard (in new terminal):
```
streamlit run dashboard/app.py
```

## 📊 Dashboard Preview

![Architecture Diagram](https://github.com/bashoori/repo/blob/master/airflow-spark-aws-etl-pipeline/img1.png)

## 🎯 Skills Demonstrated

	•	✅ ETL Workflow Orchestration (Airflow DAGs)
	•	✅ Distributed Data Transformation (PySpark)
	•	✅ Scalable Cloud Storage (AWS S3, boto3, s3fs)
	•	✅ Dashboard Development (Streamlit + Plotly)
	•	✅ Logging, Alerts & Monitoring
	•	✅ CI/CD and Production-Readiness with Docker


## 👩‍💻 Author

Bita Ashoori
✨ Passionate about building smart, scalable cloud solutions with Python, data, and clean architecture.