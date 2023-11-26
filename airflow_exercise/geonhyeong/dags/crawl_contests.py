from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import re
import boto3
import requests
from bs4 import BeautifulSoup
import logging
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

AIRFLOW_CONN_ID = os.getenv("AIRFLOW_CONN_ID")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")


def crawl(pages):
    all_data = []

    for page in pages:
        data = {
            'title': [],
            'category': [],
            'sponsor': [],
            'target': [],
            'reception_period_start': [],
            'reception_period_end': [],
            'evalution_period_start': [],
            'evalution_period_end': [],
            'annountcement_date': [],
            'd_day': [],
            'condition': [],
            'image_link': [],
        }

        url = "https://www.contestkorea.com/sub/list.php?displayrow=12&int_gbn=1&Txt_sGn=1&Txt_key=all&Txt_word=&Txt_bcode=030510001&Txt_code1=&Txt_aarea=&Txt_area=&Txt_sortkey=a.int_sort&Txt_sortword=desc&Txt_host=&Txt_tipyn=&Txt_comment=&Txt_resultyn=&Txt_actcode=&page=" + \
            str(page)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        contests = soup.select('.list_style_2 li')

        for contest in contests:
            try:
                title = contest.select_one('.title .txt').get_text(strip=True)
                category = contest.select_one(
                    '.title .category').get_text(strip=True).split("•")
                sponsor = contest.select_one('.host .icon_1').get_text(
                    strip=True).replace("주최. ", "")
                target = contest.select_one(
                    '.host .icon_2').get_text(strip=True)
                target = re.sub(r"\s", "", target).replace(
                    " ", "").replace("\n", "").replace("대상.", "")
                target = target.split(",")
                reception_period = contest.select_one(
                    '.date .step-1').get_text(strip=True)
                reception_period_date_only = re.sub(
                    r'(접수|\s)', '', reception_period).split("~")
                reception_period_start = reception_period_date_only[0]
                reception_period_end = reception_period_date_only[1]
                evaluation_period = contest.select_one(
                    '.date .step-2').get_text(strip=True)
                evaluation_period_date_only = re.sub(
                    r'(심사|\s)', '', evaluation_period).split("~")
                evalution_period_start = evaluation_period_date_only[0]
                evalution_period_end = evaluation_period_date_only[1]
                announcement_date = contest.select_one(
                    '.date .step-3').get_text(strip=True).replace("발표", "")
                d_day = contest.select_one('.d-day .day').get_text(strip=True)
                condition = contest.select_one(
                    '.d-day .condition').get_text(strip=True)
                link = contest.select_one('a')['href']
                link = "https://www.contestkorea.com/sub/" + link

                response_b = requests.get(link)
                soup_b = BeautifulSoup(response_b.text, 'html.parser')

                image_link = soup_b.select_one(
                    'div.clfx>div.img_area > div > img')['src']
                image_link = 'https://www.contestkorea.com' + image_link

                contest_info = [title, category, sponsor, target, reception_period_start, reception_period_end,
                                evalution_period_start, evalution_period_end, announcement_date, d_day, condition, image_link]

                data = {key: value if value else 'None'
                        for key, value in zip(data.keys(), contest_info)}
                all_data.append(data)
            except Exception as e:
                # print(f"Error processing contest: {e}")
                # print(f"Contest data: {data}")
                continue

    df = pd.DataFrame(all_data)
    today = datetime.now().strftime("%y%m%d")
    s3_bucket = 'airflow-contest'
    s3_key = f'contests/{today}.csv'
    upload_to_s3(df, s3_bucket, s3_key)
    return df


def upload_to_s3(df, bucket, s3_key):

    csv_buffer = df.to_csv(index=False, encoding='utf-8')
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)
    try:
        s3.put_object(Body=csv_buffer, Bucket=bucket, Key=s3_key)
        print(f'Successfully uploaded file to {bucket}/{s3_key}')
    except NoCredentialsError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error: {e}')


args = {
    "owner": "airflow",
    "start_date": datetime(2023, 11, 24),
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG(
    dag_id="crawl_and_save_s3",
    default_args=args,
    description='Crawl dev contests data and upload .csv to s3',
    schedule_interval='@daily',
    catchup=False,
)
crawl_upload_task = PythonOperator(
    task_id='crawl_and_upload',
    python_callable=crawl,
    op_args=[range(1, 6)],
    dag=dag)

crawl_upload_task

if __name__ == "__main__":
    dag.cli()
