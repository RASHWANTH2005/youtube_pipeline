# 📺 YouTube Data Pipeline with Apache Airflow

This project demonstrates how to build an **end-to-end ETL pipeline** using **Apache Airflow**, where we fetch trending YouTube video data using the **YouTube Data API**, process it with **Pandas**, and store the final results in CSV format for downstream analysis or visualization.

---

## 🚀 Project Overview

| Step     | Description |
|----------|-------------|
| **Extract**  | Call the YouTube Data API to fetch top trending videos in India |
| **Transform** | Clean and sort videos by view count |
| **Load**      | Save the processed data into a CSV file for reporting/visualization |

---

## 🧑‍💻 How to Run

### 1️⃣ Clone the [Apache Airflow Docker Example Repo](https://github.com/apache/airflow)

We used the official Airflow Docker setup to run this project.

- git clone https://github.com/apache/airflow.git
- cd airflow

2️⃣ Map Volumes in docker-compose.yaml
Inside the airflow/docker-compose.yaml, add these volume mounts:

volumes:
  - ../youtube_pipeline/dags:/opt/airflow/dags
  - ../youtube_pipeline/shared_data:/opt/airflow/shared_data


3️⃣ Start Airflow
Run the following:

docker-compose up airflow-init     # One-time DB setup
docker-compose up                  # Start Airflow services

- Then open the Airflow UI at: http://localhost:8080
- Default login: airflow / airflow


4️⃣ Trigger the DAG
In the Airflow UI, turn on and trigger the DAG: youtube_data_pipeline

This will generate:

raw_youtube.csv → raw API data

clean_youtube.csv → sorted by views

top10_youtube.csv → final output


🔑 API Key
This pipeline uses the YouTube Data API v3. You'll need your own API key:

Create an API key here

Add it in your DAG file (later, use Airflow Variables or .env for security)


📊 Optional: Visualize with Streamlit
You can use the top10_youtube.csv file to build a Streamlit dashboard:
--streamlit run streamlit_app.py

👨‍💻 Built By Rashwanth KP
- Built as a hands-on project to understand real-time data ingestion, ETL pipelines, and Apache Airflow scheduling.

📚 References
- YouTube Data API v3 Docs
- Apache Airflow Docs