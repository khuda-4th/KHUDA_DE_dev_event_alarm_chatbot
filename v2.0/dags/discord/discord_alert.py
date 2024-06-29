import sys, os, time
from datetime import datetime, timedelta
import pandas as pd
import concurrent.futures
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .discord_bot import EventNotifier, ContestNotifier, TrendNotifier

TODAY = datetime.today().strftime('%y%m%d')
YSTRDAY = (datetime.today() - timedelta(1)).strftime("%y%m%d") 

def send_event(eNotifier, event):
    eNotifier.send_event_alarm(event['title'], event['url'], event['img_url'], \
        event['host'], event['period'], event['tags'])
    return "event alarm sent"
    
def send_contest(cNotifier, contest):
    cNotifier.send_contest_alarm(contest['title'], contest['url'], contest['img_url'], \
        contest['status'], contest['category'], contest['target'], contest['host'], \
        contest['sponsor'], contest['period'], contest['d-day'], contest['total_prize'], \
        contest['first_prize'])
    return "contest alarm sent"

def send_trend(tNotifier, trend):
    tNotifier.send_trend_alarm(trend['title'], trend['user'], trend['img'], \
                               trend['url'], trend['user_url'], trend['user_img'])

def extract_valid_data():
    event_file = f"/opt/airflow/data/event_{TODAY}.csv"
    contest_file = f"/opt/airflow/data/contest_{TODAY}.csv"
    trend_file = f"/opt/airflow/data/trend_{TODAY}.csv"

    event_file_y = f"/opt/airflow/data/event_{YSTRDAY}.csv"
    contest_file_y = f"/opt/airflow/data/contest_{YSTRDAY}.csv"
    trend_file_y = f"/opt/airflow/data/trend_{YSTRDAY}.csv"

    event_today = pd.read_csv(event_file, encoding='UTF-8')
    contest_today = pd.read_csv(contest_file, encoding='UTF-8')
    trend_today = pd.read_csv(trend_file, encoding='UTF-8')

    # event 어제 날짜 파일이 존재할 경우
    if os.path.exists(event_file_y):
        event_ystrday = pd.read_csv(event_file_y, encoding='UTF-8')
        event_diff = pd.concat([event_today, event_ystrday]).drop_duplicates(keep=False, ignore_index=True)
    else:
        event_diff = event_today
    
    # contest 어제 날짜 파일이 존재할 경우
    if os.path.exists(contest_file_y):
        contest_ystrday = pd.read_csv(contest_file_y, encoding='UTF-8')
        contest_diff = pd.concat([contest_today, contest_ystrday]).drop_duplicates(keep=False, ignore_index=True)
    else:
        contest_diff = contest_today
    
    # velog 어제 날짜 파일이 존재할 경우
    if os.path.exists(trend_file_y):
        trend_ystrday = pd.read_csv(trend_file_y)
        trend_diff = pd.concat([trend_today, trend_ystrday]).drop_duplicates(keep=False, ignore_index=True)
    else:
        trend_diff = trend_today

    return event_diff, contest_diff, trend_diff

### main ###
def discord_alert():
    eNotifier = EventNotifier('https://discord.com/api/webhooks/1255833370760577024/LD6YscAlr6rUwhip1WuiOOdxTFS3qr1aTnbZiynhSad4hNkZkahRN8VH--lxDdsc2z1z')
    cNotifier = ContestNotifier('https://discord.com/api/webhooks/1255835921077768232/x_qfUTCyCsjQJ1pauewPDNd7qt3r0GN0bSvPg4eLMRqtdc48itUy2F5MTmnoY6LAIadF')
    tNotifier = TrendNotifier('https://discord.com/api/webhooks/1255836145745526805/Ohs5hp-9k19DTGBzYHk69ngg8_g7jZLzario1LT-sKU3vc5YtNHxVJ58RGeSPwpUOl4a')
  
    event, contest, trend = extract_valid_data()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        futures.append(executor.submit(send_event, eNotifier, event))
        futures.append(executor.submit(send_contest, cNotifier, contest))
        futures.append(executor.submit(send_trend, tNotifier, trend))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"An error occured: {e}")
