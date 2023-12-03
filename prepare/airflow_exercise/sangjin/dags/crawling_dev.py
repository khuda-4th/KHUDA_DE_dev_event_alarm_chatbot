from datetime import date, datetime 
import requests
import pandas as pd
import json
import pathlib
import airflow.utils.dates
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
from bs4 import BeautifulSoup as bs
import numpy as np
import re
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

dag = DAG(
    dag_id="dev_event_crawling", #dag id
    description="dev event data", #dag의 설명
    start_date=datetime(2023, 11, 26, 0, 0),  # 시작 날짜 및 시간 설정
    schedule_interval='00 10 * * *', #날짜 상관없이 주기적으로 받을 시간 
)

def upload_to_s3():
    date = datetime.now().strftime("%Y%m%d")
    hook = S3Hook('aws_ccon') # connection ID 입력
    filename = f'/home/ubuntu/airflow/data/dev_{date}.csv'
    key = f'data/dev_{date}.csv'
    bucket_name = 'sj-example-bucket' 
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)

def get_urls(url):
    response = requests.get(url)
    html = response.text
    soup = bs(html, 'html.parser')
    return soup

def get_link(soup):
    # class_ = soup.find_all('div', class_='list_wrapper__tpe4x')
    link_list = []
    links = (soup.find_all('a', target='_blank'))
    for link in links:
        link_list.append(link.text)
        
    return link_list

def get_title(soup):
    title_all = soup.find_all('span', class_='Item_item__content__title___fPQa')
    titles = []
    for title in title_all:
        titles.append(title.text)
    return titles

def get_host(soup):
    hosts_all = soup.find_all('div', class_='Item_host__zNXMy')
    hosts = []
    for host in hosts_all:
        hosts.append(host.text)
    return hosts

def get_date(soup):
    dates_all = soup.find_all('div', class_='Item_date__kVMJZ')
    dates = []
    for date in dates_all:
        txt = re.sub(r"\s", "", date.text)
        txt = re.sub(r"\(.\)", "", txt)
        dates.append(txt.split("~"))
    return dates

def get_image(soup):
    images_all = soup.find_all('img', alt="/default/event_img.png")
    images = []
    for i, image in enumerate(images_all):
        if i % 2 == 1:
            text = 'https://dev-event.vercel.app'
            text += image.get('src')
            images.append(text)
    return images

def get_link(soup):
    link_all = soup.find_all('div', class_='Item_item__86e_I')
    links = []
    for link in link_all:
        txt = link.a.attrs["href"]
        links.append(txt)
    return links


def _get_data():
    url = 'https://dev-event.vercel.app/events'
    soup = get_urls(url)
    titles = get_title(soup) # 제목
    hosts = get_host(soup) # 주최자
    dates = get_date(soup) # 일시[시작일, 종료일,]
    images = get_image(soup) # 이미지
    links = get_link(soup) # 주최 링크

    start_dates = [start_end[0] for start_end in dates] #시작 날짜
    end_dates = [start_end[1] for start_end in dates] # 끝나는 날짜
    
    # dataframe으로 변환
    dev_df = pd.DataFrame({'title' : titles, 'host' : hosts, 'start_date' : start_dates, 'end_date' : end_dates, 'image' : images, 'link' : links})
    date = datetime.now().strftime("%Y%m%d")
    # csv 파일로 저장
    dev_df.to_csv(f"/home/ubuntu/airflow/data/dev_{date}.csv", index=False)
    
   
complete = BashOperator( task_id='complete_bash', bash_command='echo "complete!"', dag = dag)

upload = PythonOperator(
    task_id = 'upload',
    python_callable = upload_to_s3, 
    #op_kwargs={filename : "dev_", key = " ", bucket_name: " "}
    dag = dag
)

get_data = PythonOperator(
    task_id="get_data", python_callable=_get_data, dag=dag
)


get_data >> upload >>complete
#순서
