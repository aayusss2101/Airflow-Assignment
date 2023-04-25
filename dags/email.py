from airflow import DAG
from datetime import datetime, timedelta

from airflow.operators.empty import EmptyOperator
from airflow.operators.email import EmailOperator

default_args={
    'owner': 'admin',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG('email_dag', start_date=datetime(2023, 4, 17), default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    dummy_task = EmptyOperator(
        task_id='dummy_task'
    )

    email_task = EmailOperator(
        task_id='email_task',
        to=['aayush.s@sigmoidanalytics.com'],
        subject='Airflow success',
        html_content='Some content',
        conn_id='smtp_default'
    )

    dummy_task >> email_task
