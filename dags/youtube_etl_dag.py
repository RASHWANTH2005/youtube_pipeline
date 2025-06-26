from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import requests


def extract():
    API_KEY = 'YOUR API KEY' # Replace with your actual API key
    MAX_RESULTS = 10

    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=IN&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    records = []
    for item in data.get('items', []):
        video_id = item['id']
        title = item['snippet']['title']
        channel = item['snippet']['channelTitle']
        published_at = item['snippet']['publishedAt']
        views = item['statistics'].get('viewCount')
        records.append({
            'video_id': video_id,
            'title': title,
            'channel': channel,
            'published_at': published_at,
            'views': int(views) if views else 0
        })

    df = pd.DataFrame(records)
    df.to_csv('/opt/airflow/shared_data/raw_youtube.csv', index=False) # Save raw data to CSV


def transform():
    df = pd.read_csv('/opt/airflow/shared_data/raw_youtube.csv') # Load raw data
    df = df[['title', 'channel', 'views']]
    df = df.sort_values(by='views', ascending=False)
    df.to_csv('/opt/airflow/shared_data/clean_youtube.csv', index=False)


def load():
    df = pd.read_csv('/opt/airflow/shared_data/clean_youtube.csv') # Load cleaned data
    df.to_csv('/opt/airflow/shared_data/top10_youtube.csv', index=False)


default_args = {
    'owner': 'rashwanth',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

with DAG(
    dag_id='youtube_data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Fetch and process trending YouTube videos'
) as dag:

    t1 = PythonOperator(task_id='extract', python_callable=extract)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = PythonOperator(task_id='load', python_callable=load)

    t1 >> t2 >> t3

# This DAG fetches trending YouTube videos, processes the data, and saves it to a CSV file.
# Make sure to replace the API_KEY with your actual YouTube Data API key.