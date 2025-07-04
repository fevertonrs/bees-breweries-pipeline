import sys
sys.path.append('/opt/airflow')
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.api.fetch_breweries import fetch_brewery_data
from src.transformations.brewery_transforms import transform_to_silver, generate_gold_layer

default_args = {
    'owner': 'everton',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='brewery_pipeline',
    default_args=default_args,
    description='Pipeline de ingestão e transformação da Open Brewery DB',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['bees', 'brewery', 'etl'],
) as dag:

    task_fetch_bronze = PythonOperator(
        task_id='fetch_brewery_data',
        python_callable=fetch_brewery_data,
    )

    task_transform_silver = PythonOperator(
        task_id='transform_to_silver',
        python_callable=transform_to_silver,
    )

    task_generate_gold = PythonOperator(
        task_id='generate_gold_layer',
        python_callable=generate_gold_layer,
    )

    task_fetch_bronze >> task_transform_silver >> task_generate_gold
