from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.cncf.kubernetes.secret import Secret
import os

ods_secrets = Secret(deploy_type= "env", None, secret = "ods-database")
ods_secrets.to_env_secret()
dict_secrets = ods_secrets.__dict__ 
secret = ods_secrets.secret

def print_secrets():
    print("secret object:", ods_secrets)
    print("secret:", secret) 
    print("dict secrets:", dict_secrets)
    print("env var database name:", os.getenv('ODS_DATABASE'))
    print("index secret:" ods_secrets.secret('ODS_DATABASE'))

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'secrets_example',
    default_args=default_args,
    description='A simple DAG to print code',
    schedule=None # adjust as needed
)

print_task = PythonOperator(
    task_id='secrets_example',
    python_callable=print_secrets,
    dag=dag,
)
