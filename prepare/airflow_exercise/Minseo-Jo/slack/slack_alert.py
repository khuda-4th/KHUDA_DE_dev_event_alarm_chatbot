from slack_sdk import WebClient
from datetime import datetime

import csv
import sys, os
sys.path.append("/home/ubuntu/airflow")

from crawling.requirements import *
from crawling.crawling_contest_final import *
from crawling.crawling_velog import *
from crawling.crawling_event import *


class SlackAlert:
    def __init__(self, channel, token):
        self.channel = channel
        self.client = WebClient(token=token)


    def notify_msg(self, context):
        date = datetime.today().strftime('%Y%m%d')
        event_filename = f'/home/ubuntu/airflow/airflow/data/event_{date}.csv'
        velog_filename = f'/home/ubuntu/airflow/airflow/data/velog_{date}.csv'
        contest_filename = f'/home/ubuntu/airflow/airflow/data/contest_{date}.csv'

        # csv 파일 읽기
        with open(event_filename, 'r', encoding='utf-8') as eventfile:
            event_reader = csv.DictReader(eventfile)
            event_content = f"""
                        Today's Date: {date}\n\n
                        """
            for row in event_reader:
                event_content += f"""
                *📣개발행사 정보입니다.📣*\n
                        '행사명' : {row['title']},
                        '주최사' : {row['host']},
                        '날짜' : {row['start_date']},
                        '포스터 링크' : {row['image']},
                        '관련 링크' : {row['link']} \n\n"""
            self.client.chat_postMessage(channel=self.channel, text=event_content)

        with open (contest_filename, 'r', encoding = 'utf-8') as contestfile:
            contest_reader = csv.DictReader(contestfile)
            contest_text = f"""
                        Today's Date: {date} \n\n
                        """
            for row in contest_reader :
                contest_text += f"""
                         *📣공모전 정보입니다.📣*\n
                            '대회명' : {row['제목']},
                            '카테고리' : {row['카테고리']}, 
                             '주최사' : {row['주최']}, 
                             '접수 시작일' : {row['접수 시작일']}, 
                             '접수 마감일' : {row['접수 마감일']},
                             '심사 시작일' : {row['심사 시작일']}, 
                             '심사 종료일' : {row['심사 종료일']}, 
                             '심사 마감일' : {row['심사 마감일']},
                             'D-day' : {row['D-Day']},
                             '접수 상태' : {row['상태']},
                             '관련 포스터' : {row['이미지 링크']},
                             '관련 링크' : {row['링크']},
                             \n\n"""

            self.client.chat_postMessage(channel=self.channel, text= contest_text)


        with open (velog_filename, 'r', encoding = 'utf-8') as velogfile:
            velog_reader = csv.DictReader(velogfile)
            velog_text = f"""
                            Today's Date: {date} \n\n """
            for row in velog_reader :
                velog_text += f"""
                *📣IT 트렌드 정보입니다.📣*
                            '제목' : {row['title']},
                            '작성자' : {row['writer']}, 
                            '하단 링크에서 자세한 내용을 확인해보세요'\n : {row['link']}\n\n
                            """
            self.client.chat_postMessage(channel=self.channel, text= velog_text)                                                                                                                                        1,31          Top
