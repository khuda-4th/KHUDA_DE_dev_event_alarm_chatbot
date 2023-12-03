from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import re
import boto3
import requests
from bs4 import BeautifulSoup
from airflow.utils.dates import days_ago
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import os
import csv
from dotenv import load_dotenv

load_dotenv()

AIRFLOW_CONN_ID = os.getenv("AIRFLOW_CONN_ID")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

date = datetime.now().strftime("%y%m%d")


async def fetch(session, url, csv_writer):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        contests = soup.select('.list_style_2 li')

        for contest in contests:
            try:
                title = contest.select_one('.title .txt').get_text(strip=True)
                category = contest.select_one(
                    '.title .category').get_text(strip=True).split("•")
                sponsor = contest.select_one('.host .icon_1').get_text(
                    strip=True).replace("주최. ", "")
                target = re.sub(r"\s", "", contest.select_one(
                    '.host .icon_2').get_text(strip=True)).replace("대상.", "").split(",")
                reception_period = re.sub(
                    r"[ㄱ-ㅣ가-힣]", "", contest.select_one('.date .step-1').get_text(strip=True)).split("~")
                evaluation_period = re.sub(
                    r"[ㄱ-ㅣ가-힣]", "", contest.select_one('.date .step-2').get_text(strip=True)).split('~')
                announcement_date = contest.select_one(
                    '.date .step-3').get_text(strip=True).replace("발표", "")
                d_day = contest.select_one('.d-day .day').get_text(strip=True)
                condition = contest.select_one(
                    '.d-day .condition').get_text(strip=True)

                # CSV 파일에 데이터 추가
                csv_writer.writerow([title, category, sponsor, target, reception_period[0], reception_period[1],
                                    evaluation_period[0], evaluation_period[1], announcement_date, d_day, condition])
            except:
                pass


def crawling_task():

    async def main():
        # 기본 url을 바탕으로 페이지별 크롤링
        BASE_URL = 'https://www.contestkorea.com/sub/list.php?displayrow=12&int_gbn=1&Txt_sGn=1&Txt_key=all&Txt_word=&Txt_bcode=030510001&Txt_code1=&Txt_aarea=&Txt_area=&Txt_sortkey=a.int_sort&Txt_sortword=desc&Txt_host=&Txt_tipyn=&Txt_comment=&Txt_resultyn=&Txt_actcode='
        urls = [f"{BASE_URL}&page={i}" for i in range(1, 30)]

        # 파일 구분을 위한 날짜

        # 데이터를 저장할 폴더 생성
        try:
            os.mkdir("./data")
        except FileExistsError:
            pass

        # CSV 파일 생성
        with open(f'/opt/airflow/data/contest_{date}.csv', 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            # CSV 파일 헤더 작성
            csv_writer.writerow(['제목', '카테고리', '주최', '대상', '접수 시작일',
                                '접수 마감일', '심사 시작일', '심사 종료일', '심사 마감일', 'D-Day', '상태'])

            # 비동기적으로 CSV 내용 작성
            async with aiohttp.ClientSession() as session:
                await asyncio.gather(*[fetch(session, url, csv_writer) for url in urls])

    asyncio.run(main())
    s3_bucket = 'airflow-contest'
    s3_key = f'contests/{date}_async.csv'
    upload_to_s3(s3_bucket, s3_key)


def upload_to_s3(bucket, s3_key):
    with open(f'/opt/airflow/data/contest_{date}.csv', 'r', newline='', encoding='utf-8') as file:
        csv_buffer = file.read().encode('utf-8')
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
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG(
    dag_id="async_crawl",
    default_args=args,
    start_date=days_ago(2),
    description='Crawl dev contests data and upload .csv to s3',
    schedule_interval='@daily',
    catchup=False,
)
crawl_upload_task = PythonOperator(
    task_id='crawl_and_upload',
    python_callable=crawling_task,
    dag=dag)

crawl_upload_task

if __name__ == "__main__":
    dag.cli()
