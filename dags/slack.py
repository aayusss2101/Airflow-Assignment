# Import necessary modules
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

# Define a function that will be used as a PythonOperator to execute a dummy task
def dummyConditionalTask():
    
    import random
    # Generate a random integer between 1 and 100
    x=random.randint(1,100)
    # Raise an exception if the generated integer is greater than 50
    if x>50:
        raise Exception()

with DAG(dag_id='slack_dag',start_date=datetime(2023,4,17),schedule_interval='@daily',catchup=False) as dag:
    
    # Define a PythonOperator that will execute the dummy task
    dummy_task=PythonOperator(
        task_id='dummy_task',
        python_callable=dummyConditionalTask
    )

    # Define a SlackWebhookOperator that will send a success message to a Slack channel
    success_task=SlackWebhookOperator(
        task_id='success_task',
        http_conn_id='slack',
        message=':smile: Task Successfully Run',
        trigger_rule='all_success'
    )

    # Define a SlackWebhookOperator that will send a failure message to a Slack channel
    fail_task=SlackWebhookOperator(
        task_id='fail_task',
        http_conn_id='slack',
        message=':red_circle: Task Failed',
        trigger_rule='all_failed'
    )

    # Set up dependencies between the tasks
    dummy_task >> [success_task,fail_task]
