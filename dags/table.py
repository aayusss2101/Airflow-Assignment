# Importing the necessary libraries
from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator


with DAG('table_dag',start_date=datetime(2023,4,17),schedule_interval='@daily',catchup=False) as dag:
    
    # Create a task to create the table in the Postgres database
    create_table=PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS users (
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL,
                country TEXT NOT NULL
            );
        '''
    )

    # Create a task to insert data into the table using a BashOperator
    insert_data=BashOperator(
        task_id='insert_data',
        bash_command='''PGPASSWORD=airflow psql -h postgres -p 5432 -U airflow -d airflow -c "INSERT INTO users (name,age,email,country) VALUES ('Aayush',22,'some@gmail.com','India'), ('John Smith', 35, 'john.smith@example.com', 'USA'), ('Emma Brown', 28, 'emma.brown@example.com', 'Canada'), ('Michael Lee', 42, 'michael.lee@example.com', 'Australia'), ('Sophie Kim', 23, 'sophie.kim@example.com', 'South Korea'), ('Daniel Chen', 30, 'daniel.chen@example.com', 'China') "'''
    )

    # Create a task to select data from the table using a BashOperator
    select_data=BashOperator(
        task_id='select_data',
        bash_command='''PGPASSWORD=airflow psql -h postgres -p 5432 -U airflow -d airflow -c "SELECT * FROM users"'''
    )

    # Define the task dependencies
    create_table >> insert_data >> select_data
