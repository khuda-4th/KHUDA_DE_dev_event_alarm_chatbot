from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule


import sys, os
sys.path.append(os.getcwd())

from crawling.crawling_velog import *

def print_result(**kwargs):
    r = kwargs["task_instance"].xcom_pull(key='result_msg')
    print("message : ", r)

default_args = {
    'owner': 'owner-name',
    'depends_on_past': False,
    'email': ['your-email@g.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

dag_args = dict(
    dag_id="crawling-velog",
    default_args=default_args,
    description='tutorial DAG ml',
    schedule_interval=timedelta(minutes=50),
    start_date=datetime.datetime(2023, 11, 24),
    tags=['example-sj'],
)

with DAG( **dag_args ) as dag:
    start = BashOperator(
        task_id='start',
        bash_command='echo "start!"',
    )

    get_url_task = PythonOperator(
        task_id='selenium_get_url',
        python_callable=get_url_list,
    )

    get_info_task = PythonOperator(
        task_id='bs_get_info',
        python_callable=crawling,
        op_kwargs={'url_list':"url_list"}
    )

    msg = PythonOperator(
        task_id='msg',
        python_callable=print_result
    )

    complete = BashOperator(
        task_id='complete_bash',
        bash_command='echo "complete!"',
    )

    start >> get_url_task >> get_info_task >> msg >> complete