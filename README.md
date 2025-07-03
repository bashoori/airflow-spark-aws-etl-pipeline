# Airflow + Spark + AWS ETL Pipeline 🚀

## 📊 Smart Transactions Dashboard

A professional, interactive data dashboard built with **Streamlit**, **Plotly**, and **Pandas**, designed to visualize customer transaction data from AWS S3 in real-time. This dashboard is ideal for business intelligence and financial insight teams.

---

## 🚀 Features

- 🔍 **Dynamic filters** (category, date range)
- 💰 **Total revenue summary** with visual emphasis
- 🥇 **Top 5 customers** by total spend
- 📦 **Revenue by product category** (pie chart)
- 📅 **Transactions by ISO week** (bar chart)
- 🌍 **Transaction map** (with geolocation)
- ⬇️ **Download filtered data as CSV**
- 🧾 **Expandable raw data preview**

---

## 🧱 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Visualization**: [Plotly](https://plotly.com/python/)  
- **Data Processing**: [Pandas](https://pandas.pydata.org/)  
- **Cloud Storage**: AWS S3  
- **Environment Management**: `dotenv` for secrets  
- **Data Format**: Parquet (via PyArrow)
---

## 🔍 Project Overview

This project showcases a modern ETL pipeline that:
- Ingests raw retail transaction data (CSV)
- Cleans and transforms the data using **PySpark**
- Automates the pipeline with **Apache Airflow**
- Stores processed data in **AWS S3** and/or **Redshift**
- Provides interactive visualizations with **Streamlit**

---

## 🧱 Tech Stack

| Layer          | Technology |
|----------------|------------|
| Orchestration  | Apache Airflow |
| Processing     | PySpark |
| Cloud Storage  | AWS S3, Redshift |
| Visualization  | Streamlit |
| Dev Environment| Docker |
| Extras         | Pandas, GitHub Actions, CI/CD ready |

---

## 📈 Business Scenario

A company receives daily retail transactions and wants to:
- Track sales by product category and customer
- Identify failed payments
- Aggregate revenue per day

The pipeline processes this data end-to-end, enabling analysts to view insights through an interactive dashboard.

## 📊 Architecture Overview

![Architecture Diagram](https://github.com/bashoori/repo/airflow-spark-aws-etl-pipeline/img1.png)


---

## 📂 Folder Structure

```
airflow-spark-aws-etl-pipeline/
├── dags/               → Airflow DAGs
├── spark_jobs/         → PySpark data processing scripts
├── data/               → Raw & processed data samples
├── docker/             → Docker + Airflow setup
├── dashboard/          → Streamlit dashboard app
├── docs/               → Architecture diagrams & notes
├── requirements.txt    → Python dependencies
├── .gitignore
└── README.md
```

## Architecture Diagram (Visual Overview)
```
        ┌──────────────────────────┐
        │   Sample CSV (raw data)  │
        └────────────┬─────────────┘
                     │
             [Spark Job: clean_transform.py]
                     │
        ┌────────────▼────────────┐
        │   Cleaned Transactions  │
        │     (Parquet format)    │
        └────────────┬────────────┘
                     │
              [Airflow DAG Task]
                     │
        ┌────────────▼────────────┐
        │   Load to AWS S3        │
        │   Optional: Redshift    │
        └────────────┬────────────┘
                     │
          [Streamlit Dashboard]
                     │
        ┌────────────▼────────────┐
        │   Sales & Customer KPIs │
        └─────────────────────────┘
```
---

## 🧪 How to Run (coming soon...)

- `docker-compose up` to start Airflow and Spark locally
- Run DAG to orchestrate data flow from raw CSV → S3/Redshift
- Launch Streamlit app for analytics

---

## 🎯 Key Skills Demonstrated

- End-to-end ETL design
- Cloud-native pipeline implementation
- Apache Airflow DAG orchestration
- PySpark-based data cleaning & transformation
- CI/CD readiness for production workflows

---

## 📌 Inspired By

This project aligns with real-world responsibilities of roles like:

- **Associate Data Engineer at IBM**
- **Cloud ETL Developer**
- **Data Engineer (AWS, Spark, Airflow)**

---

## 📎 Author

**Bita Ashoori** — [GitHub Portfolio](https://github.com/bashoori)  
Helping others build smart, scalable systems with cloud and code. ✨

---