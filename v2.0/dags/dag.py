from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from discord.discord_alert import discord_alert

import sys, os
sys.path.append(os.getcwd())

def upload_to_s3() :
    TODAY = datetime.now().strftime("%y%m%d")
    hook = S3Hook('connectionID') # connection ID
    
    event_filename = f'/opt/airflow/data/event_{TODAY}.csv'
    trend_filename = f'/opt//airflow/data/trend_{TODAY}.csv'
    contest_filename = f'/opt/airflow/data/contest_{TODAY}.csv'

    event_key = f'data/event_{TODAY}.csv'
    trend_key = f'data/trend_{TODAY}.csv'
    contest_key = f'data/contest_{TODAY}.csv'

    bucket_name = 'bucket_name'  # bucket name
    hook.load_file(filename=event_filename, key=event_key, bucket_name=bucket_name, replace=True)
    hook.load_file(filename=trend_filename, key=trend_key, bucket_name=bucket_name, replace=True)
    hook.load_file(filename=contest_filename, key=contest_key, bucket_name=bucket_name, replace=True)

default_args = {
    'owner': 'hyejiyu',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

dag_args = dict(
    dag_id='dev-event-contest-trend-notifier',
    default_args=default_args,
    description='KHUDA 4th de-project DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 29),
    tags=['de-project', 'dev-event', 'dev-contest', 'dev-trend', 'discord-notifier'],
)

with DAG( **dag_args ) as dag:
    start = BashOperator(
        task_id='start',
        bash_command='echo "start"',
    )

    # -------- trend -------- #
    trend_task = BashOperator(
        task_id='trend_get_data',
        bash_command="""
        cd /opt//airflow/dags/crawling/dev_trend/dev_trend/spiders &&
        scrapy crawl DevTrend
        """
    )

    # -------- event -------- #
    event_task = BashOperator(
        task_id="event_get_data", 
        bash_command="""
        cd /opt/airflow/dags/crawling/dev_event/dev_event/spiders &&
        scrapy crawl DevEvent
        """
    )

    # -------- contest -------- #
    contest_task = BashOperator(
        task_id='contest_get_data',
        bash_command="""
        cd /opt/airflow/dags/crawling/dev_contest/dev_contest/spiders &&
        scrapy crawl DevContest
        """
    )

    # ----- discord alert ----- #
    discord_alert_task = PythonOperator(
        task_id='discord_alert',
        python_callable=discord_alert,
        trigger_rule="all_done"
    )

    upload = PythonOperator(
        task_id = 'upload',
        python_callable = upload_to_s3
    )

    complete = BashOperator(
        task_id='complete_bash',
        bash_command='echo "complete"',
    )

    start >> event_task >> upload >> discord_alert_task >> complete
    start >> trend_task >> upload >> discord_alert_task >> complete
    start >> contest_task >> upload >> discord_alert_task >> complete
